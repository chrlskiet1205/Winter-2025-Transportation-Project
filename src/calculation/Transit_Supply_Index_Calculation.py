import pandas as pd
import os
from utils.standardize_function import z_calculation
from utils.index_function import index_calculation

def calculating_per_capita(data:pd.Series, population_data:pd.Series) -> pd.Series:
    result_lst = []

    for i in range(len(data)):
        result_lst.append(data[i]/population_data[i])
    
    return pd.Series(result_lst)


input_folder = 'data/processed'
output_folder = 'data/processed'

processed_dataset = 'finalized.csv'
input_path = os.path.join(input_folder, processed_dataset)

supply_index_df = pd.read_csv(input_path)

#Calculating per capita values
uza_service_population = supply_index_df['Service_Area_Pop']
msa_population = supply_index_df['Total Population']
ratio = uza_service_population/msa_population

VRM_per_capita: pd.Series = calculating_per_capita(supply_index_df['VRM'], uza_service_population)
VRH_per_capita: pd.Series = calculating_per_capita(supply_index_df['VRH'], uza_service_population)

#Calculating mean values
VRM_mean = VRM_per_capita.mean()
VRH_mean = VRH_per_capita.mean()

#Calculating std
VRM_std = VRM_per_capita.std()
VRH_std = VRH_per_capita.std()

#Calculating supply index for each UZAs
VRM_z = z_calculation(VRM_per_capita, VRM_mean, VRM_std)
VRH_z = z_calculation(VRH_per_capita, VRH_mean, VRH_std)

supply_index = index_calculation(VRM_z, VRH_z)

scaled_supply_index = supply_index * ratio
print(scaled_supply_index)