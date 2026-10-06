from pathlib import Path
import pandas as pd

#project setup
PROJECT_DIR = Path(__file__).resolve().parent.parent

SALES_FILE = PROJECT_DIR / "data" / "processed" / "sales_transactions.csv"
RETURNS_FILE = PROJECT_DIR / "data" / "processed" / "returns_transactions.csv"

#check files
if not SALES_FILE.exists():
    raise FileNotFoundError(f"Sales file not found: {SALES_FILE}")

if not RETURNS_FILE.exists():
    raise FileNotFoundError(f"Returns file not found: {RETURNS_FILE}")


#load the data
sales = pd.read_csv(SALES_FILE, parse_dates=["InvoiceDate"])

returns = pd.read_csv(RETURNS_FILE, parse_dates=["InvoiceDate"])


#basic information
print("\n========== PROCESSED DATA VALIDATION ==========")

print("\nSALES DATASET")
print("Rows:", len(sales))
print("Columns:", len(sales.columns))

print("\nRETURNS DATASET")
print("Rows:", len(returns))
print("Columns:", len(returns.columns))


#duplicate check
print("\n========== DUPLICATE CHECK ==========")

print("Sales duplicate rows:", sales.duplicated().sum())

print("Returns duplicate rows:", returns.duplicated().sum())


#sales validation
print("\n========== SALES VALIDATION ==========")

print("Negative quantities:", (sales["Quantity"] < 0).sum())

print("Zero quantities:", (sales["Quantity"] == 0).sum())

print("Negative prices:", (sales["UnitPrice"] < 0).sum())

print("Zero prices:", (sales["UnitPrice"] == 0).sum())


#return validation
print("\n========== RETURN VALIDATION ==========")

print("Negative quantities:", (returns["Quantity"] < 0).sum())

print("Return value:", round(returns["ReturnValue"].sum(), 2))


#missing values
print("\n========== MISSING VALUES ==========")

print("Sales:")
print(sales.isnull().sum())

print("\nReturns:")
print(returns.isnull().sum())


#revenue information
calculated_revenue = (sales["Quantity"] * sales["UnitPrice"]).sum()

stored_revenue = sales["LineRevenue"].sum()

print("\n========== REVENUE VALIDATION ==========")

print("Calculated revenue: £", round(calculated_revenue, 2))

print("Stored revenue: £", round(stored_revenue, 2))

print("Revenue difference: £", round(calculated_revenue - stored_revenue, 2))


#date range
print("\n========== DATE RANGE ==========")

print("Sales start:", sales["InvoiceDate"].min())
print("Sales end:", sales["InvoiceDate"].max())

print("Returns start:", returns["InvoiceDate"].min())
print("Returns end:", returns["InvoiceDate"].max())


#customer coverage
print("\n========== CUSTOMER COVERAGE ==========")

print("Sales rows with CustomerID:", sales["CustomerID"].notna().sum())

print("Sales rows without CustomerID:", sales["CustomerID"].isna().sum())

print("Unique identified customers:", sales["CustomerID"].nunique())


#final status
print("\n========== VALIDATION COMPLETE ==========")
