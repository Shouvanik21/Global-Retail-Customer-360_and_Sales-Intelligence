from pathlib import Path
import pandas as pd

# project setup
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

SALES_FILE = PROCESSED_DIR / "sales_transactions.csv"
RETURNS_FILE = PROCESSED_DIR / "returns_transactions.csv"

# check input file
if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found at: {RAW_FILE}")

# Create processed folder if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# load raw data
print("\n========== LOADING DATA ==========")
df = pd.read_excel(RAW_FILE)
print("Original rows:", len(df))

# remove exact duplicates
duplicate_count = df.duplicated().sum()
print("Duplicate rows removed:", duplicate_count)
df = df.drop_duplicates().copy()
print("Rows after duplicate removal:", len(df))


# clean text columns
df["Description"] = df["Description"].fillna("Unknown Product")
df["StockCode"] = df["StockCode"].astype(str).str.strip()
df["Country"] = df["Country"].astype(str).str.strip()

# identify returns/cancellations
invoice_numbers = df["InvoiceNo"].astype(str)
return_mask = (df["Quantity"] < 0) | invoice_numbers.str.startswith("C")
returns_df = df[return_mask].copy()
sales_df = df[~return_mask].copy()
print("\n========== RETURNS / CANCELLATIONS ==========")
print("Return/cancellation rows:", len(returns_df))
print("Sales rows:", len(sales_df))

# remove invalid sales price
print("\n========== PRICE CLEANING ==========")
negative_price_rows = (sales_df["UnitPrice"] < 0).sum()
print("Negative-price rows removed:", negative_price_rows)
zero_price_rows = (sales_df["UnitPrice"] == 0).sum()
print("Zero-price rows removed:", zero_price_rows)
sales_df = sales_df[sales_df["UnitPrice"] > 0].copy()

# calculate the line revenue
sales_df["LineRevenue"] = sales_df["Quantity"] * sales_df["UnitPrice"]
returns_df["ReturnValue"] = returns_df["Quantity"].abs() * returns_df["UnitPrice"]

# save the cleaned data
sales_df.to_csv(SALES_FILE, index=False)
returns_df.to_csv(RETURNS_FILE, index=False)

# final summary
print("\n========== CLEANING COMPLETE ==========")

print("Sales dataset:")
print("Rows:", len(sales_df))
print("Columns:", len(sales_df.columns))
print("Revenue: £", round(sales_df["LineRevenue"].sum(), 2))

print("\nReturns dataset:")
print("Rows:", len(returns_df))
print("Return value: £", round(returns_df["ReturnValue"].sum(), 2))

print("\nFiles created:")
print(SALES_FILE)
print(RETURNS_FILE)
