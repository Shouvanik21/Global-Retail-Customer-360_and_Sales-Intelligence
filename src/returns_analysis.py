import pandas as pd
import os

# ==========================================
# 1. PATH SETUP
# ==========================================

current_dir = os.path.dirname(os.path.abspath(__file__))

sales_path = os.path.join(
    current_dir, "..", "data", "processed", "sales_transactions.csv"
)

returns_path = os.path.join(
    current_dir, "..", "data", "processed", "returns_transactions.csv"
)


# ==========================================
# 2. LOAD DATA
# ==========================================

sales = pd.read_csv(sales_path)
returns = pd.read_csv(returns_path)

sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"])
returns["InvoiceDate"] = pd.to_datetime(returns["InvoiceDate"])


# ==========================================
# 3. OVERALL RETURNS ANALYSIS
# ==========================================

gross_sales = sales["LineRevenue"].sum()

return_value = returns["ReturnValue"].sum()

net_sales = gross_sales - return_value

returned_units = abs(returns["Quantity"].sum())

sold_units = sales["Quantity"].sum()

return_rate_value = return_value / gross_sales * 100

return_rate_units = returned_units / sold_units * 100


print("\n" + "=" * 60)
print("RETURNS & NET SALES ANALYSIS")
print("=" * 60)

print(f"\nGross Sales: £{gross_sales:,.2f}")
print(f"Return Value: £{return_value:,.2f}")
print(f"Net Sales: £{net_sales:,.2f}")

print(f"\nUnits Sold: {sold_units:,}")
print(f"Units Returned: {returned_units:,}")

print(f"\nReturn Rate by Value: {return_rate_value:.2f}%")
print(f"Return Rate by Units: {return_rate_units:.2f}%")


# ==========================================
# 4. MONTHLY SALES VS RETURNS
# ==========================================

sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
returns["Month"] = returns["InvoiceDate"].dt.to_period("M").astype(str)

monthly_sales = (
    sales.groupby("Month")
    .agg(Gross_Sales=("LineRevenue", "sum"), Units_Sold=("Quantity", "sum"))
    .reset_index()
)

monthly_returns = (
    returns.groupby("Month")
    .agg(Return_Value=("ReturnValue", "sum"), Units_Returned=("Quantity", "sum"))
    .reset_index()
)

# Quantity in returns is negative
monthly_returns["Units_Returned"] = monthly_returns["Units_Returned"].abs()


monthly = monthly_sales.merge(monthly_returns, on="Month", how="left")

monthly["Return_Value"] = monthly["Return_Value"].fillna(0)

monthly["Units_Returned"] = monthly["Units_Returned"].fillna(0)

monthly["Net_Sales"] = monthly["Gross_Sales"] - monthly["Return_Value"]

monthly["Return_Rate"] = monthly["Return_Value"] / monthly["Gross_Sales"] * 100


# ==========================================
# 5. DISPLAY MONTHLY RESULTS
# ==========================================

print("\nMONTHLY SALES & RETURNS")
print("-" * 60)

print(
    monthly.to_string(
        index=False,
        formatters={
            "Gross_Sales": "£{:,.2f}".format,
            "Return_Value": "£{:,.2f}".format,
            "Net_Sales": "£{:,.2f}".format,
            "Return_Rate": "{:.2f}%".format,
        },
    )
)


# ==========================================
# 6. TOP RETURNED PRODUCTS
# ==========================================

top_returns = (
    returns.groupby(["StockCode", "Description"])
    .agg(
        Units_Returned=("Quantity", lambda x: abs(x.sum())),
        Return_Value=("ReturnValue", "sum"),
    )
    .reset_index()
    .sort_values("Return_Value", ascending=False)
    .head(20)
)


print("\nTOP 20 RETURNED PRODUCTS")
print("-" * 60)

print(
    top_returns.to_string(index=False, formatters={"Return_Value": "£{:,.2f}".format})
)


# ==========================================
# 7. SAVE RESULTS
# ==========================================

monthly_path = os.path.join(
    current_dir, "..", "data", "processed", "monthly_sales_returns.csv"
)

returns_product_path = os.path.join(
    current_dir, "..", "data", "processed", "top_returned_products.csv"
)

monthly.to_csv(monthly_path, index=False)

top_returns.to_csv(returns_product_path, index=False)


print("\n" + "=" * 60)
print("RETURNS ANALYSIS COMPLETE")
print("=" * 60)

print("\nFiles created:")
print("monthly_sales_returns.csv")
print("top_returned_products.csv")
