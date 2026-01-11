import pandas as pd
import os
import numpy as np
from utils.standardize_function import z_calculation

def index_calculation(
    z_no_vehicle: pd.Series,
    z_transit_commute: pd.Series,
    z_mean_income: pd.Series
) -> pd.Series:
    """
    Calculates an unweighted transit need index.
    Higher income = lower need, so income is inverted.
    """
    return (
        z_no_vehicle +
        z_transit_commute -
        z_mean_income
    ) / 3


input_folder = 'data/processed'
output_folder = 'data/processed'

processed_dataset = 'finalized.csv'
input_path = os.path.join(input_folder, processed_dataset)

need_index_df = pd.read_csv(input_path)

pd.options.display.float_format = "{:,.2f}".format

no_vehicle_pct = need_index_df['Pct No Vehicle Available']
transit_commute_pct = need_index_df['Public Transit Share']
mean_income = need_index_df['Mean Income']

q1_no_vehicle_pct = np.percentile(no_vehicle_pct, 25)
q3_no_vehicle_pct = np.percentile(no_vehicle_pct, 75)
iqr_no_vehicle_pct = q3_no_vehicle_pct - q1_no_vehicle_pct
q1_transit_commute_pct = np.percentile(transit_commute_pct, 25)
q3_transit_commute_pct = np.percentile(transit_commute_pct, 75)
iqr_transit_commute_pct = q3_transit_commute_pct - q1_transit_commute_pct
q1_mean_income = np.percentile(mean_income, 25)
q3_mean_income = np.percentile(mean_income, 75)
iqr_mean_income = q3_mean_income - q1_mean_income

z_no_vehicle_pct = z_calculation(no_vehicle_pct, no_vehicle_pct.median(), iqr_no_vehicle_pct)
z_transit_commute_pct = z_calculation(transit_commute_pct, transit_commute_pct.median(), iqr_transit_commute_pct)
z_mean_income = z_calculation(mean_income, mean_income.median(), iqr_mean_income)

need_index = index_calculation(z_no_vehicle_pct, z_transit_commute_pct, z_mean_income)

print(need_index)


