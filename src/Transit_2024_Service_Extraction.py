import pandas as pd
import os

#README: This file process the ntd_annual_service_2022_to_2024.csv, filter to keep only the report year of 2024 and time period of Annual Total with needed columns, and output it to data/raw/transportation/output/annual_2024_service.csv

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
    'UZA Area Sq Miles',
    'UZA Population',
    'Service Area Sq Miles',
    'Service Area Population',
    'Time Period',
    'Actual Vehicle/Passenger Car Revenue Miles', 
    'Actual Vehicle/Passenger Car Revenue Hours', 
    'Unlinked Passenger Trips (UPT)'
    ]

#Extract rows with Report Year of 2024 and Time Period of Annual Total only
annual_2024_service = service_df[(service_df['Report Year'] == 2024) & (service_df['Time Period'] == 'Annual Total')][service_cols]

annual_2024_service.columns = ['Agency', 'UZA_Name', 'UACE_Code', 'Report_Year', 'Mode_Name', 'UZA_Area(Sq Miles)', 'UZA_Pop', 'Service_Area(Sq Miles)', 'Service_Area_Pop', 'Time_Period', 'VRM', 'VRH', 'UPT']

#Output to data/raw/transportation/output
output_annual_service_path = os.path.join(output_folder, 'annual_2024_service.csv')
annual_2024_service.to_csv(output_annual_service_path, index=False)

print("Done")
