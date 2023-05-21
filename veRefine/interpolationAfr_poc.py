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

# Extract the AFR column values
afr_values = [float(row['PCM1.P1.Final_AFR1']) for row in data]

# Create an array of time values (assuming the time values are in the first column)
time_values = np.array([float(row['Interval (ms)']) for row in data])

# Create the interpolation function
linear_interp = interp1d(time_values, afr_values, kind='linear')

# Generate new time values for interpolation
new_time_values = np.linspace(time_values.min(), time_values.max(), 1000)

# Interpolate using linear method
linear_interpolated = linear_interp(new_time_values)

# Append the linear interpolated values to the original dataset
for i, row in enumerate(data):
    if i < len(linear_interpolated):  # Check the index is within the bounds
        interpolated_value = linear_interpolated[i]
        row['Linear_Interpolation'] = interpolated_value
    else:
        break  # Break the loop if the index exceeds the available interpolated values

# Write the updated dataset to a new CSV file
new_filename = '../outputs/logCharacterization_with_interpolation.csv'
fieldnames = data[0].keys()

with open(new_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

# Plot the original and interpolated AFR values
plt.plot(time_values, afr_values, 'b.', label='Original TPS')
plt.plot(new_time_values, linear_interpolated, 'r-', label='Linear Interpolation')
plt.xlabel('Time')
plt.ylabel('AFR')
plt.legend()
plt.show()
