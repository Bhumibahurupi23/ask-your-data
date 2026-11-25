
import pandas as pd

# Load the CSV dataset
file_path = "data/raw/Sample - Superstore.csv"

df = pd.read_csv(file_path)

# Display the first 5 records
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# Display column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# Display dataset dimensions
print("\n--- DATASET SIZE ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Display data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

# Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# Check duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())
