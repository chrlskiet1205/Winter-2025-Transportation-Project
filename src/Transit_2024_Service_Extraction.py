import pandas as pd
import os

#README: This file process the ntd_annual_service_2022_to_2024.csv, filter to keep only the report year of 2024 with needed columns, and output it to data/raw/transportation/output/annual_2024_service.csv

#Specifying path for input and output folder
input_folder = 'data/raw/transportation'
output_folder = 'data/raw/transportation/output'

#CSV files to process
annual_service = 'ntd_annual_service_2022_to_2024.csv'
agency_information = 'agency_information_2024.csv'


#Process annual service .csv file to filter out 2024 service only
input_annual_service_path = os.path.join(input_folder, annual_service)
service_df = pd.read_csv(input_annual_service_path, low_memory=False)

#Columns keep for service dataset
service_cols = [
    'Agency', 
    'UZA Name',
    'UACE Code', 
    'Report Year', 
    'Mode Name', 
    'Actual Vehicle/Passenger Car Revenue Miles', 
    'Actual Vehicle/Passenger Car Revenue Hours', 
    'Unlinked Passenger Trips (UPT)'
    ]
annual_2024_service = service_df[service_df['Report Year'] == 2024][service_cols]

#Output to data/raw/transportation/output
output_annual_service_path = os.path.join(output_folder, 'annual_2024_service.csv')
annual_2024_service.to_csv(output_annual_service_path, index=False)

print("Done")
