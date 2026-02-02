import pandas as pd
import numpy as np
import os
import sys

base_path = 'data/raw/census'
output_dir = 'data/cleaned-unmerged'
output_file = 'top20_transit_need.csv'

# File Names
file_pop = 'acs_population_2024.csv'
file_inc = 'acs_income_2024.csv'
file_commute = 'acs_means_of_transport_to_work_2024.csv'
file_vehicle = 'acs_vehicle_ownership_2024.csv'

