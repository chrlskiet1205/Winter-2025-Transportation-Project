import pandas as pd
import numpy as np
import os
import sys

# ==========================================
# CONFIGURATION
# ==========================================
# Base path relative to where you run the script (project root)
base_path = 'data/raw/census'
output_dir = 'data/cleaned-unmerged'
output_file = 'top20_transit_need.csv'

# File Names
file_pop = 'acs_population_2024.csv'
file_inc = 'acs_income_2024.csv'
file_commute = 'acs_means_of_transport_to_work_2024.csv'
file_vehicle = 'acs_vehicle_ownership_2024.csv'

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def clean_value(val):
    """Converts strings like '1,234', '12.5%', or '-' to floats."""
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    
    # Remove hidden characters and standard cleaning
    val = str(val).strip().replace(',', '').replace('\xa0', '')
    
    if val.endswith('%'):
        return float(val.replace('%', ''))
    if val in ['-', 'N', '(X)']:
        return np.nan
    try:
        return float(val)
    except ValueError:
        return np.nan

def clean_label(label):
    """Removes non-breaking spaces, regular spaces, and colons."""
    if pd.isna(label):
        return ""
    # Replace non-breaking space with space, strip whitespace, remove trailing colon
    return str(label).replace('\xa0', ' ').strip().rstrip(':')

def process_standard_acs(full_path, target_col_map):
    """
    Reads a standard ACS file, cleans labels, transposes, and extracts vars.
    Handles duplicate labels by taking the first occurrence.
    """
    if not os.path.exists(full_path):
        print(f"Error: File not found {full_path}")
        return pd.DataFrame()

    print(f"Processing {os.path.basename(full_path)}...")
    
    # Read file
    df = pd.read_csv(full_path, dtype=str)
    
    # Clean the Row Labels (which become columns)
    # This fixes issues with "Total:" vs "Total" vs "  Total"
    df['Clean_Label'] = df['Label (Grouping)'].apply(clean_label)
    
    # Handle duplicates (e.g., 'No vehicle available' appears multiple times)
    # We keep the first one, which is usually the 'Total' category
    df = df.drop_duplicates(subset=['Clean_Label'], keep='first')
    
    # Set index and Transpose
    df = df.set_index('Clean_Label').drop(columns=['Label (Grouping)']).T
    
    # Reset index to get City Name
    df = df.reset_index()
    df.rename(columns={'index': 'NAME_RAW'}, inplace=True)
    
    # Clean City Name
    df['NAME'] = df['NAME_RAW'].apply(lambda x: x.split('!!')[0].strip())
    
    out_df = df[['NAME']].copy()
    
    # Extract columns based on cleaned map
    for csv_clean_label, new_name in target_col_map.items():
        if csv_clean_label in df.columns:
            out_df[new_name] = df[csv_clean_label].apply(clean_value)
        else:
            print(f"  Warning: '{csv_clean_label}' not found in file.")
            out_df[new_name] = np.nan
            
    return out_df

def process_income_acs(full_path):
    """Special handler for Income file which has unique structure."""
    if not os.path.exists(full_path):
        print(f"Error: File not found {full_path}")
        return pd.DataFrame()

    print(f"Processing {os.path.basename(full_path)}...")
    df = pd.read_csv(full_path, header=None, dtype=str)
    
    header_row = df.iloc[0]
    target_metric = "Median income (dollars)"
    if not header_row.str.contains(target_metric, regex=False).any():
        target_metric = "Median income (dollars)"
    
    data = []
    for col_idx, cell_val in enumerate(header_row):
        if pd.isna(cell_val): continue
        if target_metric in str(cell_val) and "!!Estimate" in str(cell_val):
            city_name = str(cell_val).split('!!')[0].strip()
            
            # Find the "All households" or "Total" row
            val = np.nan
            for row_idx in range(1, min(10, len(df))):
                label = str(df.iloc[row_idx, 0])
                if "Households" in label or "Households" in clean_label(label):
                    val = clean_value(df.iloc[row_idx, col_idx])
                    break
            data.append({'NAME': city_name, 'Median Income': val})
            
    return pd.DataFrame(data)

# ==========================================
# MAIN EXECUTION
# ==========================================

# 1. POPULATION
path_pop = os.path.join(base_path, file_pop)
df_pop = process_standard_acs(path_pop, {
    'Total': 'Total Population'
})

if df_pop.empty:
    print("CRITICAL ERROR: Population data not loaded. Stopping.")
    sys.exit(1)

# 2. VEHICLE OWNERSHIP
path_vehicle = os.path.join(base_path, file_vehicle)
df_vehicle = process_standard_acs(path_vehicle, {
    'Total': 'Total households',
    'No vehicle available': 'No Vehicle Available'
})

# 3. COMMUTE (TRANSIT)
path_commute = os.path.join(base_path, file_commute)
df_commute = process_standard_acs(path_commute, {
    'Total': 'Total Workers',
    'Public transportation (excluding taxicab)': 'Transit Count'
})

# Calculation for Commute
if not df_commute.empty:
    df_commute['Public Transit Share'] = (df_commute['Transit Count'] / df_commute['Total Workers'])
else:
    df_commute['Public Transit Share'] = np.nan

# 4. INCOME
path_inc = os.path.join(base_path, file_inc)
df_inc = process_income_acs(path_inc)

# ==========================================
# MERGE
# ==========================================
print("\nMerging Datasets...")

merged_df = df_pop.copy()
merged_df = merged_df.sort_values(by='Total Population', ascending=False).head(20)

print(f"Top 5 MSAs by Population: {merged_df['NAME'].head(5).tolist()}")

merged_df = merged_df.merge(df_inc, on='NAME', how='left')

# --- Merge Vehicle Data ---
merged_df = merged_df.merge(
    df_vehicle[['NAME', 'Total households', 'No Vehicle Available']], 
    on='NAME', 
    how='left'
)

# UPDATED: Calculate Percentage and Reorder
merged_df['Pct No Vehicle Available'] = merged_df['No Vehicle Available'] / merged_df['Total households']

# Move 'Pct No Vehicle Available' to the left of 'No Vehicle Available'
cols = list(merged_df.columns)
cols.remove('Pct No Vehicle Available')
# Find the position of 'No Vehicle Available'
target_idx = cols.index('No Vehicle Available')
# Insert Pct before it
cols.insert(target_idx, 'Pct No Vehicle Available')
merged_df = merged_df[cols]

# --- Merge Commute Data ---
merged_df = merged_df.merge(
    df_commute[['NAME', 'Transit Count', 'Total Workers', 'Public Transit Share']], 
    on='NAME', 
    how='left'
)

# --- CLEANING & INDEXING ---
# Remove " Metro Area" from the NAME column
merged_df['NAME'] = merged_df['NAME'].str.replace(' Metro Area', '', regex=False)

# Create an index column (Rank 1 to 20)
merged_df.reset_index(drop=True, inplace=True)
merged_df.index = merged_df.index + 1
merged_df.index.name = 'Rank'
merged_df.reset_index(inplace=True) # Move Rank into the columns

# ==========================================
# SAVE
# ==========================================
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

out_path = os.path.join(output_dir, output_file)
merged_df.to_csv(out_path, index=False)

print(f"\nSuccess! Data saved to: {out_path}")
# Displaying the new column structure
print(merged_df[['Rank', 'NAME', 'Total households', 'Pct No Vehicle Available', 'No Vehicle Available']].head())