import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. PATH SETUP
# ==========================================

current_dir = os.path.dirname(os.path.abspath(__file__))

processed_dir = os.path.join(current_dir, "..", "data", "processed")

plots_dir = os.path.join(current_dir, "..", "plots")

os.makedirs(plots_dir, exist_ok=True)


# ==========================================
# 2. LOAD DATA
# ==========================================

executive = pd.read_csv(os.path.join(processed_dir, "executive_kpis.csv"))

segments = pd.read_csv(os.path.join(processed_dir, "customer_segment_summary.csv"))

sales = pd.read_csv(os.path.join(processed_dir, "sales_transactions.csv"))


# ==========================================
# 3. MONTHLY REVENUE TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(executive["Month"], executive["Gross_Revenue"], marker="o")

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(os.path.join(plots_dir, "monthly_revenue_trend.png"))

plt.close()


# ==========================================
# 4. MONTHLY ORDERS TREND
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(executive["Month"], executive["Orders"], marker="o")

plt.title("Monthly Order Volume")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(os.path.join(plots_dir, "monthly_orders_trend.png"))

plt.close()


# ==========================================
# 5. CUSTOMER SEGMENT REVENUE
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(segments["Segment"], segments["Revenue"])

plt.title("Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(os.path.join(plots_dir, "customer_segment_revenue.png"))

plt.close()


# ==========================================
# 6. TOP PRODUCTS
# ==========================================

product_sales = (
    sales[~sales["StockCode"].isin(["DOT", "POST", "M"])]
    .groupby("Description")["LineRevenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)


plt.figure(figsize=(10, 7))

plt.barh(product_sales.index, product_sales.values)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(os.path.join(plots_dir, "top_products_revenue.png"))

plt.close()


# ==========================================
# 7. COMPLETE
# ==========================================

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETE")
print("=" * 60)

print("\nCharts created:")

print("1. plots/monthly_revenue_trend.png")
print("2. plots/monthly_orders_trend.png")
print("3. plots/customer_segment_revenue.png")
print("4. plots/top_products_revenue.png")
