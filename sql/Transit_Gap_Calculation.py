import pandas as pd
import sqlite3
import os

#README: This file merge two datasets in data/cleaned-unmerged and output into data/processed a completed dataset for calculations

#Specify output path for output file
output_folder = 'data/processed'

#Initialize a connection to the database
conn = sqlite3.connect("data/database/transit.db")

#Read indexes csv files
pd.read_csv("data/processed/transit_need_index.csv").to_sql(
    "need_index", conn, if_exists="replace", index=False
)

pd.read_csv("data/processed/transit_supply_index.csv").to_sql(
    "supply_index", conn, if_exists="replace", index=False
)

#Read mapping csv file
pd.read_csv("data/raw/transportation/output/uza_to_msa.csv").to_sql(
    "crosswalk", conn, if_exists="replace", index=False
)

#SQL query for joining need index and supply index using a crosswalk csv file
df = pd.read_sql(
    """SELECT "n"."RANK", "n"."MSA_Name", "s"."UZA_Name", "n"."Need Index", "s"."Scaled Supply Index"
    FROM "need_index" AS n
    JOIN "crosswalk" AS c ON "c"."MSA_Name" = "n"."MSA_Name"
    JOIN "supply_index" AS s ON "s"."UZA_Name" = "c"."UZA_Name";
    """,
    conn
)

#Calculating Transit Gap on MSAs Scale
df['Transit Gap'] = round(df['Need Index'] - df['Scaled Supply Index'], 4)

output_path = os.path.join(output_folder, 'transit_gap.csv')
df.to_csv(output_path, index=False)

#Close connection
conn.close()

print("Done")