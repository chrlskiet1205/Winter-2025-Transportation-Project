import pandas as pd
import os
import numpy as np
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

pd.options.display.float_format = "{:,.2f}".format

uza_service_population = supply_index_df['Service_Area_Pop']
msa_population = supply_index_df['Total Population']
ratio = uza_service_population/msa_population

VRM_per_capita: pd.Series = calculating_per_capita(supply_index_df['VRM'], uza_service_population)
VRH_per_capita: pd.Series = calculating_per_capita(supply_index_df['VRH'], uza_service_population)

q1_VRM = np.percentile(VRM_per_capita, 25)
q3_VRM = np.percentile(VRM_per_capita, 75)
q1_VRH = np.percentile(VRH_per_capita, 25)
q3_VRH = np.percentile(VRH_per_capita, 75)

iqr_VRM = q3_VRM - q1_VRM
iqr_VRH = q3_VRH - q1_VRH

VRM_median = VRM_per_capita.median()
VRH_median = VRH_per_capita.median()

VRM_z = z_calculation(VRM_per_capita, VRM_median, iqr_VRM)
VRH_z = z_calculation(VRH_per_capita, VRH_median, iqr_VRH)

supply_index = index_calculation(VRM_z, VRH_z)

scaled_supply_index = supply_index * ratio
print(scaled_supply_index)


