from pathlib import Path
import pandas as pd

# Locate the project folder and dataset
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "raw" / "Online Retail.xlsx"

# Load the original dataset
df = pd.read_excel(DATA_FILE)

# Identify potentially cancelled invoices
invoice_numbers = df["InvoiceNo"].astype(str)
cancelled_rows = invoice_numbers.str.startswith("C")

# Calculate preliminary line revenue of each transation/row
df["LineRevenue"] = df["Quantity"] * df["UnitPrice"]

print("\n========== DATA PROFILE ==========")

print("\n1. DATE RANGE")
print("First transaction:", df["InvoiceDate"].min())
print("Last transaction:", df["InvoiceDate"].max())

print("\n2. UNIQUE COUNTS")
#this tells us how many different invoice no exists each invoice with same no can have multiple transactions under it
print("Unique invoice numbers:", df["InvoiceNo"].nunique())
#this tells us how many different stock code exists 
print("Unique products:", df["StockCode"].nunique())
#this tells us how many different customers exists 
print("Unique customers:", df["CustomerID"].nunique())
#this tells us how many different country exists 
print("Unique countries:", df["Country"].nunique())

print("\n3. DUPLICATE ROWS")
#this tells us if any complete row is repeated or not
print("Exact duplicate rows:", df.duplicated().sum())

print("\n4. QUANTITY CHECKS")
#this may represent returns or cancellations
print("Rows with negative quantity:", (df["Quantity"] < 0).sum())
print("Rows with zero quantity:", (df["Quantity"] == 0).sum())

print("\n5. UNIT PRICE CHECKS")
#this may be promotional or unusual
print("Rows with negative unit price:", (df["UnitPrice"] < 0).sum())
print("Rows with zero unit price:", (df["UnitPrice"] == 0).sum())

print("\n6. CANCELLATION CHECK")
#this tells the total no of cancelled transactions
print("Rows with invoice numbers starting with C:", cancelled_rows.sum())

print("\n7. PRELIMINARY REVENUE")
#this is the sum of Quantity × UnitPrice across the raw data. It is not yet our final reported sales figure because returns and cancellations require separate treatment
print("Total line revenue in raw data: £", round(df["LineRevenue"].sum(), 2))

print("\n8. TOP 10 COUNTRIES BY ROW COUNT")
#this helps us understand the dataset's geographic coverage
print(df["Country"].value_counts().head(10))

print("\n9. MISSING CUSTOMER IDs BY COUNTRY")
print(df.loc[df["CustomerID"].isna(), "Country"].value_counts().head(10))

print("\n========== PROFILE COMPLETE ==========")
