import pandas as pd
import os

# ==========================================
# 1. PATH SETUP
# ==========================================

current_dir = os.path.dirname(os.path.abspath(__file__))

sales_path = os.path.join(
    current_dir, "..", "data", "processed", "sales_transactions.csv"
)


# ==========================================
# 2. LOAD SALES DATA
# ==========================================

sales = pd.read_csv(sales_path)

sales["InvoiceDate"] = pd.to_datetime(sales["InvoiceDate"])

sales = sales[sales["CustomerID"].notna()].copy()


# ==========================================
# 3. REFERENCE DATE
# ==========================================
# One day after the last transaction in the dataset.
# This gives every customer a measurable recency.

reference_date = sales["InvoiceDate"].max() + pd.Timedelta(days=1)

print("\n" + "=" * 60)
print("RFM CUSTOMER SEGMENTATION")
print("=" * 60)

print(f"\nReference date: {reference_date}")


# ==========================================
# 4. CALCULATE RFM METRICS
# ==========================================

rfm = (
    sales.groupby("CustomerID")
    .agg(
        Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("LineRevenue", "sum"),
    )
    .reset_index()
)


# ==========================================
# 5. CREATE RFM SCORES
# ==========================================

# Recency:
# Lower number = better
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]
).astype(int)


# Frequency:
# Higher number = better
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
).astype(int)


# Monetary:
# Higher spending = better
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
).astype(int)


# ==========================================
# 6. COMBINED RFM SCORE
# ==========================================

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
)


# ==========================================
# 7. CUSTOMER SEGMENTS
# ==========================================


def assign_segment(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "New Customers"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    else:
        return "Potential Loyalists"


rfm["Segment"] = rfm.apply(assign_segment, axis=1)


# ==========================================
# 8. DISPLAY SUMMARY
# ==========================================

print("\nCUSTOMER SEGMENT DISTRIBUTION")
print("-" * 60)

segment_summary = rfm["Segment"].value_counts().reset_index()

segment_summary.columns = ["Segment", "Customers"]

segment_summary["Percentage"] = segment_summary["Customers"] / len(rfm) * 100

print(
    segment_summary.to_string(index=False, formatters={"Percentage": "{:.2f}%".format})
)


# ==========================================
# 9. SEGMENT REVENUE
# ==========================================

print("\nREVENUE BY CUSTOMER SEGMENT")
print("-" * 60)

segment_revenue = (
    rfm.groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        Revenue=("Monetary", "sum"),
        Average_Revenue=("Monetary", "mean"),
        Average_Frequency=("Frequency", "mean"),
        Average_Recency=("Recency", "mean"),
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

print(
    segment_revenue.to_string(
        index=False,
        formatters={
            "Revenue": "£{:,.2f}".format,
            "Average_Revenue": "£{:,.2f}".format,
            "Average_Frequency": "{:.2f}".format,
            "Average_Recency": "{:.1f}".format,
        },
    )
)


# ==========================================
# 10. TOP CUSTOMERS
# ==========================================

print("\nTOP 20 RFM CUSTOMERS")
print("-" * 60)

top_rfm = rfm.sort_values(["R_Score", "F_Score", "M_Score"], ascending=False).head(20)

print(
    top_rfm[
        ["CustomerID", "Recency", "Frequency", "Monetary", "RFM_Score", "Segment"]
    ].to_string(index=False)
)


# ==========================================
# 11. SAVE RFM DATA
# ==========================================

output_path = os.path.join(current_dir, "..", "data", "processed", "customer_rfm.csv")

rfm.to_csv(output_path, index=False)


# ==========================================
# 12. SAVE SEGMENT SUMMARY
# ==========================================

summary_path = os.path.join(
    current_dir, "..", "data", "processed", "customer_segment_summary.csv"
)

segment_revenue.to_csv(summary_path, index=False)


print("\n" + "=" * 60)
print("RFM ANALYSIS COMPLETE")
print("=" * 60)

print("\nFiles created:")
print("customer_rfm.csv")
print("customer_segment_summary.csv")
