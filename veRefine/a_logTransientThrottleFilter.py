import os
import pandas as pd

# Set display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Get the absolute path to the log file within the container
file_path = os.path.abspath('/inputs/log.csv')

# Read the log file
df = pd.read_csv(file_path)

# Convert the 'Interval (ms)' column to a datetime object and then to a numeric data type
df['Interval (ms)'] = pd.to_datetime(df['Interval (ms)'], format='%Y-%m-%d::%H:%M:%S.%f')
df['Interval (ms)'] = df['Interval (ms)'].apply(lambda x: x.timestamp() * 1000)  # Convert to milliseconds

# Calculate the difference between consecutive TPS values and time interval
df['TPS_diff'] = df['PCM1.P2.TPS'].diff()
df['time_diff'] = df['Interval (ms)'].diff()

# Calculate the ramp rate of TPS
df['TPS_ramp_rate'] = df['TPS_diff'] / df['time_diff']

# Calculate the difference between consecutive Final_AFR1 values and time interval
df['Final_AFR1_diff'] = df['PCM1.P1.Final_AFR1'].diff()
df['time_diff'] = df['Interval (ms)'].diff()  # / 1000.0  # convert to seconds

# Calculate the ramp rate of Final_AFR1
df['Final_AFR1_ramp_rate'] = df['Final_AFR1_diff'] / df['time_diff']

# Create new data frame consisting of Interval (ms), TPS, and the calculated TPS Ramp Rate and Final_AFR1 Ramp Rate
df1 = df[['Interval (ms)', 'PCM1.P9.RPM', 'PCM1.P1.MAP', 'PCM1.P2.TPS', 'TPS_ramp_rate',
          'PCM1.P1.Final_AFR1', 'Final_AFR1_ramp_rate', 'PCM1.P20.Target_AFR']]

# Round the Ramp Rate values to the nearest thousandth
df1 = df1.round(5)

# Identify the rows where TPS ramp rate is greater than a threshold
# and Final_AFR1 ramp rate is greater than another threshold
throttle_threshold = 0.02499  # adjust the threshold as needed
afr_threshold = 0.00499  # adjust the threshold as needed
transient_throttle_events = df1[(df1['TPS_ramp_rate'].abs() <= throttle_threshold)
                                & (df1['Final_AFR1_ramp_rate'].abs() <= afr_threshold)]

# Save the resulting DataFrame as a CSV file
transient_throttle_events.to_csv('../outputs/logSansTt.csv', index=False)
