import pandas as pd
from scipy.ndimage import gaussian_filter

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('../outputs/correctedVeTable.csv', index_col=0)

# Convert the DataFrame to a Numpy array
data = df.to_numpy()

# Apply a Gaussian filter to smooth the data
sigma = 1
smooth_data = gaussian_filter(data, sigma=sigma)

# Convert the smoothed data back to a DataFrame
smooth_df = pd.DataFrame(smooth_data, columns=df.columns, index=df.index)

# Round the result to the nearest thousandth
smooth_df = smooth_df.round(decimals=3)

# Reverse the order of the rows in the result dataframe
smooth_df = smooth_df[::-1]

# Save the smoothed data to a new CSV file
smooth_df.to_csv('../outputs/smoothedVeTable.csv')
