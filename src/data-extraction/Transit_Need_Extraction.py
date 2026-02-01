import pandas as pd
import numpy as np
import os
import sys
import re

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
    """Special handler for Income file which has unique structure.

    Extracts Median Income from the ACS income CSV using the "Households" row
    when available. If a median is not available for an MSA, the function will
    fall back to an available Mean Income column in the same ACS file. Any
    remaining gaps will be filled from `data/processed/finalized.csv`'s
    `Mean Income` where possible.
    """
    if not os.path.exists(full_path):
        print(f"Error: File not found {full_path}")
        return pd.DataFrame()

    print(f"Processing {os.path.basename(full_path)}...")
    df = pd.read_csv(full_path, header=None, dtype=str)

    header_row = df.iloc[0].astype(str)

    med_data = {}
    mean_data = {}

    # Scan header row for Median/Mean income columns
    for col_idx, cell_val in enumerate(header_row):
        if pd.isna(cell_val):
            continue
        s = str(cell_val)
        if ("Median income" in s) or ("Mean income" in s):
            # Metro Division case: take text after ';' if present, else the left part
            city_name = s.split('!!')[0].split(';')[-1].strip()

            # Prefer the 'Households' row (or 'All households') for a consistent statistic
            val = np.nan
            for row_idx in range(1, min(200, len(df))):
                label = str(df.iloc[row_idx, 0])
                lbl = clean_label(label).lower()
                if 'household' in lbl or 'all households' in lbl or 'total' in lbl:
                    val = clean_value(df.iloc[row_idx, col_idx])
                    if not pd.isna(val):
                        break

            # FalIncomelback: first numeric value in column
            if pd.isna(val):
                for row_idx in range(1, min(200, len(df))):
                    cand = clean_value(df.iloc[row_idx, col_idx])
                    if not pd.isna(cand):
                        val = cand
                        break

            if 'Median income' in s:
                med_data[city_name] = val
            elif 'Mean income' in s:
                mean_data[city_name] = val

    # Build initial rows preferring medians, then ACS means
    all_names = set(list(med_data.keys()) + list(mean_data.keys()))
    rows = []
    for name in sorted(all_names):
        if name in med_data and not pd.isna(med_data[name]):
            rows.append({'NAME': name, 'Median Income': med_data[name]})
        elif name in mean_data and not pd.isna(mean_data[name]):
            rows.append({'NAME': name, 'Median Income': mean_data[name]})
        else:
            rows.append({'NAME': name, 'Median Income': np.nan})

    out = pd.DataFrame(rows)

    # If some MSAs are still missing, try to fill from data/processed/finalized.csv
    fallback_path = os.path.join('data', 'processed', 'finalized.csv')
    if os.path.exists(fallback_path):
        try:
            fin = pd.read_csv(fallback_path, dtype=str)
            if 'NAME' in fin.columns and 'Mean Income' in fin.columns:
                fin['Mean Income'] = fin['Mean Income'].apply(clean_value)
                missing_mask = out['Median Income'].isna()
                for idx in out[missing_mask].index:
                    name = out.at[idx, 'NAME']
                    matched = fin[fin['NAME'] == name]
                    if not matched.empty:
                        mval = matched['Mean Income'].iloc[0]
                        if not pd.isna(mval):
                            out.at[idx, 'Median Income'] = mval
        except Exception as e:
            print(f"  Warning: failed to read fallback finalized file: {e}")

    if out.empty:
        print("  Warning: No income metrics found in file.")
        return out

    # Collapse duplicate Metro Area entries (e.g., Metro Divisions) using median
    # aggregation for numeric values and keep one row per NAME.
    agg = out.groupby('NAME', as_index=False).agg({'Median Income': 'median'})

    print(f"  Found {len(agg)} unique income entries.")
    return agg

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

# -- Ensure median income is available for top MSAs --
# If some top MSAs are missing from the ACS income extraction, try to
# fill them from the processed/finalized dataset (Mean Income) as a fallback.
missing_for_top = set(merged_df['NAME']) - set(df_inc['NAME'])
# Also include names present but with NaN Median Income
nan_mask = df_inc['Median Income'].isna() if 'Median Income' in df_inc.columns else pd.Series(dtype=bool)
nan_names = set(df_inc.loc[nan_mask, 'NAME'].tolist())
need_fill = set(merged_df['NAME']) & (missing_for_top | nan_names)
if need_fill:
    print(f"Filling missing median income for {len(need_fill)} MSAs from finalized.csv: {sorted(need_fill)}")
    fin_path = os.path.join('data', 'processed', 'finalized.csv')
    if os.path.exists(fin_path):
        fin = pd.read_csv(fin_path, dtype=str)
        if 'NAME' in fin.columns and 'Mean Income' in fin.columns:
            fin['Mean Income'] = fin['Mean Income'].apply(clean_value)
            for name in need_fill:
                # If name already exists in df_inc but the value is NaN, update it
                lookup_name = name.replace(' Metro Area','').strip()
                idxs = df_inc.index[df_inc['NAME'] == name].tolist() if name in df_inc['NAME'].values else []
                if idxs:
                    for idx in idxs:
                        if pd.isna(df_inc.at[idx, 'Median Income']):
                            matched = fin[fin['NAME'] == lookup_name]
                            if matched.empty:
                                try:
                                    matched = fin[fin['NAME'].str.contains(re.escape(lookup_name), na=False)]
                                except Exception:
                                    matched = fin[fin['NAME'].str.contains(lookup_name, na=False)]
                            if not matched.empty:
                                df_inc.at[idx, 'Median Income'] = matched['Mean Income'].iloc[0]
                else:
                    matched = fin[fin['NAME'] == lookup_name]
                    if matched.empty:
                        try:
                            matched = fin[fin['NAME'].str.contains(re.escape(lookup_name), na=False)]
                        except Exception:
                            matched = fin[fin['NAME'].str.contains(lookup_name, na=False)]
                    if not matched.empty:
                        df_inc = pd.concat(
                            [df_inc, pd.DataFrame([{
                                'NAME': name,
                                'Median Income': matched['Mean Income'].iloc[0]
                            }])],
                            ignore_index=True
                        )
    else:
        print("  Warning: finalized.csv not found; cannot fill missing incomes.")

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