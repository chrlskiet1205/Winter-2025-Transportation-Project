import pandas as pd
import os
from standardize_function import z_calculation

input_folder = 'data/processed'
output_folder = 'data/processed'

processed_dataset = 'finalized.csv'
input_path = os.path.join(input_folder, processed_dataset)

supply_index = pd.read_csv(input_path)