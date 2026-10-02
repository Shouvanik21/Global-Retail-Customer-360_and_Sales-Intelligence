from pathlib import Path
import pandas as pd

# Find the project directory automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Locate the original Excel dataset
DATA_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"

# Check whether the file exists
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_FILE}\n"
        "Please check the file name and data/raw folder."
    )

#Read the excel file into DataFrame
df=pd.read_excel(DATA_FILE)

#Display the basic information about the dataset

#print the no of rows and columns
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

#prints the column names
print("Column names:",df.columns.to_list())

#print the first five data
print("First five data:\n",df.head())

#print the different data types in each column 
print("Data Types:\n",df.dtypes)

#print the total no of values that are missing
print("Total no of missing values:\n",df.isnull().sum())

