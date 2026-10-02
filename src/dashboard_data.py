import pandas as pd
import os

# ==========================================
# 1. PATH SETUP
# ==========================================

current_dir = os.path.dirname(os.path.abspath(__file__))

processed_dir = os.path.join(current_dir, "..", "data", "processed")


# ==========================================
# 2. LOAD DATA
# ==========================================

sales = pd.read_csv(os.path.join(processed_dir, "sales_transactions.csv"))

customer_360 = pd.read_csv(os.path.join(processed_dir, "customer_360.csv"))

rfm = pd.read_csv(os.path.join(processed_dir, "customer_rfm.csv"))

executive = pd.read_csv(os.path.join(processed_dir, "executive_kpis.csv"))


# ==========================================
# 3. CUSTOMER 360 + RFM
# ==========================================

customer_dashboard = customer_360.merge(
    rfm[["CustomerID", "R_Score", "F_Score", "M_Score", "RFM_Score", "Segment"]],
    on="CustomerID",
    how="left",
)


# ==========================================
# 4. PRODUCT PERFORMANCE
# ==========================================

product_dashboard = (
    sales[~sales["StockCode"].isin(["DOT", "POST", "M"])]
    .groupby(["StockCode", "Description"], dropna=False)
    .agg(
        Orders=("InvoiceNo", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Revenue=("LineRevenue", "sum"),
    )
    .reset_index()
)

product_dashboard["Average_Order_Revenue"] = (
    product_dashboard["Revenue"] / product_dashboard["Orders"]
)


# ==========================================
# 5. COUNTRY PERFORMANCE
# ==========================================

country_dashboard = (
    sales.groupby("Country")
    .agg(
        Orders=("InvoiceNo", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Revenue=("LineRevenue", "sum"),
        Customers=("CustomerID", "nunique"),
    )
    .reset_index()
)


# ==========================================
# 6. SAVE DASHBOARD DATASETS
# ==========================================

customer_dashboard.to_csv(
    os.path.join(processed_dir, "dashboard_customers.csv"), index=False
)

product_dashboard.to_csv(
    os.path.join(processed_dir, "dashboard_products.csv"), index=False
)

country_dashboard.to_csv(
    os.path.join(processed_dir, "dashboard_countries.csv"), index=False
)


print("\n" + "=" * 60)
print("POWER BI DATA PREPARATION COMPLETE")
print("=" * 60)

print("\nFiles created:")

print("dashboard_customers.csv")
print("dashboard_products.csv")
print("dashboard_countries.csv")

print("\nRows:")
print(f"Customers: {len(customer_dashboard):,}")

print(f"Products: {len(product_dashboard):,}")

print(f"Countries: {len(country_dashboard):,}")

print(f"Monthly KPI rows: {len(executive):,}")
