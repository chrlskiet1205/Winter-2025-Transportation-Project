import pandas as pd
import os

#README: This file processes ntd_annual_service_2022_to_2024.csv, filters it to keep only rows with Report Year 2024, Time Period 'Annual Total', Type of Service 'DO' or 'PT', ignores the Vanpool and Demand Response mode, retains the necessary columns, and outputs the result to data/raw/transportation/output/annual_2024_service.csv.

#Specifying path for input and output folder
input_folder = 'data/raw/transportation'
output_folder = 'data/raw/transportation/output'

#CSV files to process
annual_service = 'ntd_annual_service_2022_to_2024.csv'
agency_information = 'agency_information_2024.csv'


#Process annual service file
input_annual_service_path = os.path.join(input_folder, annual_service)
service_df = pd.read_csv(input_annual_service_path, low_memory=False)

##Columns keep for service dataset
service_cols = [
    'Agency', 
    'UZA Name',
    'UACE Code', 
    'Report Year', 
    'Mode Name', 
    'Type Of Service',
    'UZA Area Sq Miles',
    'UZA Population',
    'Service Area Sq Miles',
    'Service Area Population',
    'Time Period',
    'Actual Vehicle/Passenger Car Revenue Miles', 
    'Actual Vehicle/Passenger Car Revenue Hours', 
    'Unlinked Passenger Trips (UPT)'
    ]

## Extract rows for 2024, where the time period is 'Annual Total', the service type is either 'DO' or 'PT', and ignore Vanpool and Demand Response Mode
annual_2024_service = service_df[
    (service_df['Report Year'] == 2024) &
    (service_df['Time Period'] == 'Annual Total') &
    (service_df['Type Of Service'].isin(['DO', 'PT'])) &
    (~service_df['Mode Name'].isin(['Vanpool', 'Demand Response']))
][service_cols]

annual_2024_service.columns = ['Agency', 'UZA_Name', 'UACE_Code', 'Report_Year', 'Mode_Name', 'Service_Type', 'UZA_Area(Sq Miles)', 'UZA_Pop', 'Service_Area(Sq Miles)', 'Service_Area_Pop', 'Time_Period', 'VRM', 'VRH', 'UPT']

#Output to data/raw/transportation/output
output_annual_service_path = os.path.join(output_folder, 'annual_2024_service.csv')
annual_2024_service.to_csv(output_annual_service_path, index=False)

print("Done")
