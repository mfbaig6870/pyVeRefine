import pandas as pd

# read the first input CSV file
avgAfr = pd.read_csv('../outputs/avgAfrBins.csv')

# read the second input CSV file
avgTargetAfr = pd.read_csv('../outputs/avgTargetAfrBins.csv')

# create a new CSV file for output
with open('../outputs/avgAfrDelta.csv', mode='w', newline='') as output_file:
    # create a CSV writer using pandas
    writer = pd.DataFrame(columns=avgAfr.columns)

    # iterate over the rows of the first input CSV file
    for i in range(len(avgAfr)):
        row = []

        # iterate over the columns of the first input CSV file
        for j in range(len(avgAfr.columns)):
            # skip the first row and first column, which are headers
            if j == 0:
                row.append(avgTargetAfr.iloc[i, j])
            else:
                # calculate the percentage difference between the corresponding values from the two input CSV files
                try:
                    value = (float(avgTargetAfr.iloc[i, j]) - float(avgAfr.iloc[i, j])) / float(avgAfr.iloc[i, j]) + 1
                    row.append(round(value, 3))  # round the value to 3 decimal places
                except ZeroDivisionError:
                    row.append(0)

        # append the row to the CSV writer
        writer.loc[i] = row

    # write the data to the output CSV file
    writer.to_csv(output_file, index=False, header=True)
