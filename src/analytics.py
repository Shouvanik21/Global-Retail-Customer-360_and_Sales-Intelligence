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
# 3. BASIC DATA CHECK
# ==========================================

print("\n" + "=" * 60)
print("GLOBAL RETAIL CUSTOMER 360 - PYTHON ANALYTICS")
print("=" * 60)

print("\nSALES DATA")
print("-" * 60)
print(f"Rows: {len(sales):,}")
print(f"Columns: {len(sales.columns)}")
print(f"Revenue: £{sales['LineRevenue'].sum():,.2f}")
print(f"Orders: {sales['InvoiceNo'].nunique():,}")
print(f"Customers: {sales['CustomerID'].nunique():,}")
print(f"Products: {sales['StockCode'].nunique():,}")

print("\nRETURNS DATA")
print("-" * 60)
print(f"Rows: {len(returns):,}")
print(f"Return Value: £{returns['ReturnValue'].sum():,.2f}")
print(f"Return Orders: {returns['InvoiceNo'].nunique():,}")


# ==========================================
# 4. CUSTOMER 360
# ==========================================

customer_data = sales[sales["CustomerID"].notna()].copy()

customer_360 = (
    customer_data.groupby("CustomerID")
    .agg(
        total_orders=("InvoiceNo", "nunique"),
        total_units=("Quantity", "sum"),
        total_revenue=("LineRevenue", "sum"),
        first_purchase=("InvoiceDate", "min"),
        last_purchase=("InvoiceDate", "max"),
    )
    .reset_index()
)


# Average Order Value
customer_360["average_order_value"] = (
    customer_360["total_revenue"] / customer_360["total_orders"]
)


# Purchase lifetime in days
customer_360["customer_lifetime_days"] = (
    customer_360["last_purchase"] - customer_360["first_purchase"]
).dt.days


# ==========================================
# 5. CUSTOMER 360 SUMMARY
# ==========================================

print("\nCUSTOMER 360")
print("-" * 60)

print(f"Customers analyzed: {len(customer_360):,}")
print(f"Average customer revenue: " f"£{customer_360['total_revenue'].mean():,.2f}")

print(f"Average orders per customer: " f"{customer_360['total_orders'].mean():.2f}")

print(f"Average customer AOV: " f"£{customer_360['average_order_value'].mean():,.2f}")


# ==========================================
# 6. TOP CUSTOMERS
# ==========================================

top_customers = customer_360.sort_values("total_revenue", ascending=False).head(20)

print("\nTOP 20 CUSTOMERS BY REVENUE")
print("-" * 60)

print(
    top_customers[
        [
            "CustomerID",
            "total_orders",
            "total_units",
            "total_revenue",
            "average_order_value",
        ]
    ].to_string(index=False)
)


# ==========================================
# 7. SAVE CUSTOMER 360 DATA
# ==========================================

output_path = os.path.join(current_dir, "..", "data", "processed", "customer_360.csv")

customer_360.to_csv(output_path, index=False)

print("\n" + "=" * 60)
print(f"Customer 360 saved to:")
print(output_path)
print("=" * 60)
