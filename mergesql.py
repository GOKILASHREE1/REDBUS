import pandas as pd
import os

# Directory where all the CSV files are located
directory = 'C:\REDBUD_PROJECT\envi'

# List to store individual DataFrames
dfs = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        dfs.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(dfs, ignore_index=True)

# Optionally, you can save the merged DataFrame to a new CSV file
merged_df.to_csv('mergedtransport_output.csv', index=False)

print("CSV files have been merged successfully!")

