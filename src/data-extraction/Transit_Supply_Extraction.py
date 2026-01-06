import pandas as pd
import os 

#README: This file uses two csv files in data/raw/transportation/out, process data from the annual_2024_service.csv by sum VRM, VRH, and UPT, group by UACE Code. It then outputs the result to a new csv file outputed in data/clean-unmerged.

#Specifying path for input and output folder
input_folder = 'data/raw/transportation/output'
output_folder = 'data/cleaned-unmerged'

#CSV files to process
map_file = 'uza_to_msa.csv'
annual_2024_service_file = 'annual_2024_service.csv'

map_path = os.path.join(input_folder, map_file)
annual_2024_service_path = os.path.join(input_folder, annual_2024_service_file) 

#Convert csv files to DataFrame
map_df_uacecode_only = pd.read_csv(map_path, dtype=str)['UACE_Code'] #Take only UACE_Code from uza_to_msa.csv file
annual_2024_service_df = pd.read_csv(annual_2024_service_path).dropna()

annual_2024_service_df['UACE_Code'] = annual_2024_service_df['UACE_Code'].astype('int64').astype(str)

#Take only UZAs that correlate with MSAs
filtered_service_df = annual_2024_service_df[
    annual_2024_service_df['UACE_Code'].isin(map_df_uacecode_only)
]

#Sum VRM, VRH, UPT of all agencies in UZAs based on UACE Code
aggregated_df = filtered_service_df.groupby('UACE_Code', as_index=False).agg({
    'UZA_Name': 'first',
    'UACE_Code': 'first',
    'Report_Year': 'first',
    'UZA_Area(Sq Miles)': 'first',
    'UZA_Pop': 'first',
    'Service_Area(Sq Miles)': 'first',
    'Service_Area_Pop': 'first',
    'Time_Period': 'first',
    'VRM': 'sum',
    'VRH': 'sum',
    'UPT': 'sum',
})

aggregated_df = aggregated_df.sort_values(by='UZA_Pop', ascending=False)
aggregated_df['UZA_Name'] = aggregated_df['UZA_Name'].str.replace("--","-", regex=False) #Process to delete double hyphen from UZA Names

#Output
output_path = os.path.join(output_folder, 'transit_supply.csv')
aggregated_df.to_csv(output_path, index=False)

print("Done")