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
# 3. MONTHLY SALES METRICS
# ==========================================

sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

returns["Month"] = returns["InvoiceDate"].dt.to_period("M").astype(str)


monthly_sales = (
    sales.groupby("Month")
    .agg(
        Gross_Revenue=("LineRevenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Customers=("CustomerID", "nunique"),
    )
    .reset_index()
)


# ==========================================
# 4. MONTHLY RETURNS
# ==========================================

monthly_returns = (
    returns.groupby("Month").agg(Return_Value=("ReturnValue", "sum")).reset_index()
)


# ==========================================
# 5. COMBINE SALES + RETURNS
# ==========================================

monthly = monthly_sales.merge(monthly_returns, on="Month", how="left")

monthly["Return_Value"] = monthly["Return_Value"].fillna(0)


# ==========================================
# 6. NET SALES
# ==========================================

monthly["Net_Sales"] = monthly["Gross_Revenue"] - monthly["Return_Value"]


# ==========================================
# 7. AVERAGE ORDER VALUE
# ==========================================

monthly["AOV"] = monthly["Gross_Revenue"] / monthly["Orders"]


# ==========================================
# 8. MONTH-OVER-MONTH GROWTH
# ==========================================

monthly["Revenue_MoM_Growth"] = monthly["Gross_Revenue"].pct_change() * 100

monthly["Net_Sales_MoM_Growth"] = monthly["Net_Sales"].pct_change() * 100

monthly["Orders_MoM_Growth"] = monthly["Orders"].pct_change() * 100


# ==========================================
# 9. OVERALL KPIs
# ==========================================

gross_revenue = sales["LineRevenue"].sum()
return_value = returns["ReturnValue"].sum()
net_sales = gross_revenue - return_value

orders = sales["InvoiceNo"].nunique()
units = sales["Quantity"].sum()
customers = sales["CustomerID"].nunique()

aov = gross_revenue / orders


# ==========================================
# 10. EXECUTIVE SUMMARY
# ==========================================

print("\n" + "=" * 65)
print("EXECUTIVE SALES KPI ANALYSIS")
print("=" * 65)

print("\nKEY PERFORMANCE INDICATORS")
print("-" * 65)

print(f"Gross Revenue       : £{gross_revenue:,.2f}")
print(f"Return Value        : £{return_value:,.2f}")
print(f"Net Sales           : £{net_sales:,.2f}")
print(f"Orders              : {orders:,}")
print(f"Units Sold          : {units:,}")
print(f"Identified Customers: {customers:,}")
print(f"Average Order Value : £{aov:,.2f}")


# ==========================================
# 11. MONTHLY PERFORMANCE
# ==========================================

print("\nMONTHLY PERFORMANCE")
print("-" * 65)

print(
    monthly.to_string(
        index=False,
        formatters={
            "Gross_Revenue": "£{:,.2f}".format,
            "Return_Value": "£{:,.2f}".format,
            "Net_Sales": "£{:,.2f}".format,
            "AOV": "£{:,.2f}".format,
            "Revenue_MoM_Growth": lambda x: "N/A" if pd.isna(x) else f"{x:.2f}%",
            "Net_Sales_MoM_Growth": lambda x: "N/A" if pd.isna(x) else f"{x:.2f}%",
            "Orders_MoM_Growth": lambda x: "N/A" if pd.isna(x) else f"{x:.2f}%",
        },
    )
)


# ==========================================
# 12. BEST AND LOWEST MONTHS
# ==========================================

best_month = monthly.loc[monthly["Gross_Revenue"].idxmax()]

lowest_month = monthly.loc[monthly["Gross_Revenue"].idxmin()]

print("\nREVENUE RANGE")
print("-" * 65)

print(
    f"Highest revenue month : "
    f"{best_month['Month']} "
    f"(£{best_month['Gross_Revenue']:,.2f})"
)

print(
    f"Lowest revenue month  : "
    f"{lowest_month['Month']} "
    f"(£{lowest_month['Gross_Revenue']:,.2f})"
)


# ==========================================
# 13. SAVE DASHBOARD DATASET
# ==========================================

output_path = os.path.join(current_dir, "..", "data", "processed", "executive_kpis.csv")

monthly.to_csv(output_path, index=False)


print("\n" + "=" * 65)
print("EXECUTIVE KPI ANALYSIS COMPLETE")
print("=" * 65)

print("\nCreated:")
print("executive_kpis.csv")
