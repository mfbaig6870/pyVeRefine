import pandas as pd
import numpy as np

# Read in the CSV files, skipping the first row and first column
avg_afr_delta_df = pd.read_csv('../outputs/avgAfrDelta.csv', skiprows=0, index_col=0)
ve_table_df = pd.read_csv('../inputs/ve_table.csv', skiprows=0, index_col=0)

# Convert columns to numeric data types
avg_afr_delta_df = avg_afr_delta_df.apply(pd.to_numeric)
ve_table_df = ve_table_df.apply(pd.to_numeric)

# Replace 0.0 values with 1.0 in avg_afr_delta_df
avg_afr_delta_df = np.where(avg_afr_delta_df == 0.0, 1.0, avg_afr_delta_df)

# Multiply the dataframes element-wise
result = avg_afr_delta_df * ve_table_df

# Round the result to the nearest thousandth
result = result.round(decimals=3)

# Save the result to a new CSV file
result.to_csv("../outputs/correctedVeTable_g1.csv", index=True, header=True)
