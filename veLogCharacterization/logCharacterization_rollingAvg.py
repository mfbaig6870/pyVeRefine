import pandas as pd

# Set display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Set input and output file paths
input_file_path = '../inputs/log.csv'
output_file_path = '../outputs/logCharacterization.csv'

# Read the log file
df = pd.read_csv(input_file_path)

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

# Calculate the ramp rate of Final_AFR1
df['Final_AFR1_ramp_rate'] = df['Final_AFR1_diff'] / df['time_diff']

# Calculate the difference between consecutive RPM values and time interval
df['RPM_diff'] = df['PCM1.P9.RPM'].diff()

# Calculate the ramp rate of RPM
df['RPM_ramp_rate'] = df['RPM_diff'] / df['time_diff']

# Round the Ramp Rate values to the nearest thousandth
df = df.round({'TPS_ramp_rate': 5, 'Final_AFR1_ramp_rate': 5, 'RPM_ramp_rate': 5})

# Calculate the rolling average of RPM_diff
rpm_rolling_avg = df['RPM_ramp_rate'].rolling(window=10, min_periods=1).mean()

# Calculate the rolling average of TPS_diff
tps_rolling_avg = df['TPS_ramp_rate'].rolling(window=10, min_periods=1).mean()

# Add an event characterization column to the DataFrame
df['event_type'] = ''

# Assign "idle" events to the event_type column
idle_condition = (df['PCM1.P9.RPM'] < 1500) & (df['PCM1.P2.TPS'] <= 5)
df.loc[idle_condition, 'event_type'] = 'idle'

# Assign "cruise" events to the event_type column
cruise_condition = ((df['PCM1.P9.RPM'] >= 1500) & (df['PCM1.P9.RPM'] <= 4500)) & (df['PCM1.P2.TPS'] < 15)
df.loc[cruise_condition, 'event_type'] = 'cruise'

# Assign "transThrtl" (Transient Throttle) events to the event_type column
# trans_thrtl_condition = (df['TPS_ramp_rate'].abs() >= 0.02499) & (df['Final_AFR1_ramp_rate'].abs() >= 0.00499)
trans_thrtl_condition = (tps_rolling_avg.abs() >= 0.02499)
df.loc[trans_thrtl_condition, 'event_type'] = 'transThrtl'

# Assign "lgtAccel" (Light Acceleration) events to the event_type column
lgt_accel_condition = ((df['PCM1.P9.RPM'] >= 2500) & (df['PCM1.P9.RPM'] <= 6000)) & ((df['PCM1.P2.TPS'] >= 15) &
                                                                                     (df['PCM1.P2.TPS'] <= 60))
df.loc[lgt_accel_condition, 'event_type'] = 'lgtAccel'

# Assign "hrdAccel" (Hard Acceleration) events to the event_type column
hrd_accel_condition = (df['PCM1.P9.RPM'] >= 3000) & ((df['PCM1.P2.TPS'] >= 60) & (df['PCM1.P2.TPS'] <= 100))
df.loc[hrd_accel_condition, 'event_type'] = 'hrdAccel'

# Assign "decel" (Deceleration) events to the event_type column
decel_condition = (rpm_rolling_avg < -0.89999) & (df['PCM1.P2.TPS'] <= 10)
df.loc[decel_condition, 'event_type'] = 'decel'

# Save the resulting DataFrame as a CSV file
df.to_csv(output_file_path, index=False)
