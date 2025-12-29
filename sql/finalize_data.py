import pandas as pd
import sqlite3
import os

#README: This file merge two datasets in data/cleaned-unmerged and output into data/processed a completed dataset for calculations

#Specify output path for output file
output_folder = 'data/processed'

#Initialize a connection to the database
conn = sqlite3.connect("data/database/transit.db")

#Read MSAs demand csv file
pd.read_csv("data/cleaned-unmerged/top20_transit_need.csv").to_sql(
    "msa_demand", conn, if_exists="replace", index=False
)

#Read UZAs supply csv file
pd.read_csv("data/cleaned-unmerged/transit_supply.csv").to_sql(
    "uza_supply", conn, if_exists="replace", index=False
)

#Read UZAs to MSAs crosswalk csv file
pd.read_csv("data/raw/transportation/output/uza_to_msa.csv").to_sql(
    "crosswalk", conn, if_exists="replace", index=False
)

#Joining MSAs transit demand and UZAs transit supply tables
df = pd.read_sql(
    """SELECT "m".*, "u".* 
    FROM "msa_demand" AS m 
    JOIN "crosswalk" AS c ON "c"."MSA_Name" = "m"."NAME"
    JOIN "uza_supply" AS u ON "u"."UZA_Name" = "c"."UZA_Name";
    """,
    conn
)

output_path = os.path.join(output_folder, 'finalized.csv')
df.to_csv(output_path, index=False)

#Close connection
conn.close()

print("Done")