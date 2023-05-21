import pandas as pd

# Read in the CSV files, skipping the first row and first column
hit_count_df = pd.read_csv('../outputs/logHitCount.csv', skiprows=0, index_col=0)

# Convert columns to numeric data types
hit_count_df = hit_count_df.apply(pd.to_numeric)

# Apply threshold values using Pandas
hit_count_df = hit_count_df.where((hit_count_df < 5), 1) \
                           .where((hit_count_df >= 5), 0)

# Save the result to a new CSV file
hit_count_df.to_csv('../outputs/logHitCountThreshold.csv', index=True, header=True)
