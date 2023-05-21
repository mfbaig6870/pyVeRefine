import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load log file into DataFrame
df = pd.read_csv('../outputs/logSansTt.csv')

# Filter data by PCM1.P2.TPS column
tps_threshold_value = 10
df = df[df['PCM1.P2.TPS'] > tps_threshold_value]

# Define partition ranges for RPM and MAP values
rpm_partitions = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250,
                  4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000]
map_partitions = [-13.05339642, -11.93950659, -11.08668469, -10.2338628, -9.381040894, -8.528218994, -7.675397095,
                  -6.822575196, -5.969753296, -5.116931397, -4.264109497, -3.411287598, -2.558465698, -1.705643799,
                  -0.852821899, 0, 2.311538949, 4.54753741, 6.803680001, 9.066537302, 11.33163284, 13.59747446,
                  15.86356477, 18.12973798, 20.39593882, 22.66214887, 24.92836199, 27.19457613, 29.46079062,
                  31.72700522, 33.99321985, 36.2594345]

# Create bins for RPM and MAP values using partition ranges
rpm_bins = pd.cut(df['PCM1.P9.RPM'], bins=[0] + rpm_partitions + [np.inf])
map_bins = pd.cut(df['PCM1.P1.MAP'], bins=map_partitions)

# Group by RPM and MAP bins and calculate mean Target AFR value
df_grouped = df.groupby([map_bins, rpm_bins])['PCM1.P20.Target_AFR'].mean().fillna(0)

# Round the mean AFR values to the nearest thousandth
df_grouped = df_grouped.round(3)

# Reshape the resulting Series into a grid of MAP vs RPM with mean AFR values displayed in each cell
grid = df_grouped.unstack().sort_index(axis=0, ascending=False)

# Save the resulting DataFrame as a CSV file
grid.to_csv('../outputs/avgTargetAfrBins.csv')
