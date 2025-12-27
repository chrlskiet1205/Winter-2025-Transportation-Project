import pandas as pd
import os

# ==========================================
# PATH CONFIGURATION
# ==========================================
# Get the directory where this script is currently located (i.e., inside 'src')
script_dir = 'src/Transit_Need_Extraction.py'

# Construct the path to the raw census data
# We go '..' to go up one level from 'src', then into 'data/raw/census'
base_path = 'data/raw/census'

# Construct the output path
output_dir = 'data/processed'
output_file = 'top20_transit_need.csv'

# ==========================================
# FILE NAMES
# ==========================================
# Update these if your actual file names differ!
file_pop = 'acs_population_2024.csv'       # Needs 'Total Population'
file_inc = 'acs_income_2024.csv'           # Needs 'Median Income'
file_commute = 'acs_means_of_transport_to_work_2024.csv'      # Needs 'Public Transit Share'
file_vehicle = 'acs_vehicle_ownership_2024.csv'      # Needs 'No Vehicle Available'

# The common column to merge on (e.g. "GEOID" or "NAME")
merge_col = 'NAME'

# ==========================================
# 1. LOAD DATASETS
# ==========================================
print(f"Reading data from: {os.path.abspath(base_path)}")

try:
    df_pop = pd.read_csv(os.path.join(base_path, file_pop))
    df_inc = pd.read_csv(os.path.join(base_path, file_inc))
    df_commute = pd.read_csv(os.path.join(base_path, file_commute))
    df_vehicle = pd.read_csv(os.path.join(base_path, file_vehicle))
    print("All files loaded successfully.")
except FileNotFoundError as e:
    print(f"\nError: Could not find a file.\n{e}")
    print("Check that your CSV files are in the 'data/raw/census' folder and match the filenames in the script.")
    exit()

# ==========================================
# 2. IDENTIFY TOP 20 MSAs
# ==========================================
print("Identifying Top 20 MSAs by Population...")

# Adjust 'Total Population' to your actual column name if different
pop_col_name = 'Total Population' 

if pop_col_name not in df_pop.columns:
    print(f"WARNING: Column '{pop_col_name}' not found. Available columns: {list(df_pop.columns)}")
    # If the script fails here, copy-paste the printed column names to fix 'pop_col_name' above
    exit()

# Sort by population descending and take top 20
top_20_pop = df_pop.sort_values(by=pop_col_name, ascending=False).head(20)
top_20_ids = top_20_pop[merge_col].unique()

print(f"Top 20 MSAs identified. First 3: {top_20_ids[:3]}")

# ==========================================
# 3. FILTER & MERGE
# ==========================================
print("Merging datasets...")

# Start with the population dataframe
transit_need_df = top_20_pop[[merge_col, pop_col_name]].copy()

# Helper function to merge a specific column from other files
def merge_data(base_df, source_df, col_name):
    # Filter source to only Top 20
    filtered = source_df[source_df[merge_col].isin(top_20_ids)]
    # Merge
    return base_df.merge(filtered[[merge_col, col_name]], on=merge_col, how='left')

# NOTE: Ensure these column names ('Median Income', etc.) match your CSV headers
transit_need_df = merge_data(transit_need_df, df_inc, 'Median Income')
transit_need_df = merge_data(transit_need_df, df_commute, 'Public Transit Share')
transit_need_df = merge_data(transit_need_df, df_vehicle, 'No Vehicle Available')

# ==========================================
# 4. EXPORT
# ==========================================
os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist
output_path = os.path.join(output_dir, output_file)

transit_need_df.to_csv(output_path, index=False)
print(f"Success! Data extracted to: {os.path.abspath(output_path)}")
print(transit_need_df.head())