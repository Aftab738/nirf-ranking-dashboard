import pandas as pd
import glob
import os

# Path to all CSV files
files = glob.glob("data/raw/*.csv")

# Empty list to store dataframes
all_data = []

# Read each CSV file
for file in files:

    # Read CSV
    df = pd.read_csv(file)

    # Extract year from filename
    filename = os.path.basename(file)

    year = ''.join(filter(str.isdigit, filename))

    # Add year column
    df["Year"] = year

    # Store dataframe
    all_data.append(df)

# Merge all datasets
merged_df = pd.concat(all_data, ignore_index=True)

# Remove duplicate rows
merged_df = merged_df.drop_duplicates()

# Clean column names
merged_df.columns = merged_df.columns.str.strip()
merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]

# Fill missing values
merged_df = merged_df.fillna(0)

# Show dataset information
print("\nFIRST 5 ROWS:")
print(merged_df.head())

print("\nDATASET SHAPE:")
print(merged_df.shape)

print("\nCOLUMN NAMES:")
for col in merged_df.columns:
    print(col)

print("\nMISSING VALUES:")
print(merged_df.isnull().sum())

# Save cleaned merged dataset
merged_df.to_csv(
    "data/cleaned/nirf_merged.csv",
    index=False
)

print("\nMerged dataset saved successfully!")