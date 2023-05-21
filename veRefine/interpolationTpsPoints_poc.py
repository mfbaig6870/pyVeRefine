import csv
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Read the CSV file
filename = '../outputs/logCharacterization.csv'
data = []
num_rows_to_analyze = 20000  # Specify the number of rows to analyze

with open(filename, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
        if len(data) >= num_rows_to_analyze:
            break

# Extract the TPS column values
tps_values = np.array([float(row['PCM1.P2.TPS']) for row in data])

# Create an array of time values (assuming the time values are in the first column)
time_values = np.array([float(row['Interval (ms)']) for row in data])

# Create the interpolation function
linear_interp = interp1d(time_values, tps_values, kind='linear')

# Generate new time values for interpolation
new_time_values = np.linspace(time_values.min(), time_values.max(), 1000)

# Interpolate using linear method
linear_interpolated = linear_interp(new_time_values)

# Calculate the difference between original data and linear interpolation
difference = linear_interp(time_values) - tps_values

# Set the threshold for significant difference
threshold = 0.05

# Find the indices where the difference exceeds the threshold
break_indices = np.where(np.abs(difference) > threshold)[0]

# Plot the original and interpolated TPS values
plt.plot(time_values, tps_values, 'b.', label='Original TPS')
plt.plot(new_time_values, linear_interpolated, 'r-', label='Linear Interpolation')

# Mark the points where the linear interpolation breaks or deviates significantly
plt.plot(time_values[break_indices], tps_values[break_indices], 'go', label='Break/Deviation')

plt.xlabel('Time')
plt.ylabel('TPS')
plt.legend()
plt.show()
