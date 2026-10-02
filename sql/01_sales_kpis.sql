USE retail_analytics;

--KPI = Key Performance Indicator
-- ============================================================
-- 1. OVERALL SALES KPIs
-- ============================================================
SELECT
    ROUND(SUM(LineRevenue), 2) AS total_revenue,
    SUM(Quantity) AS total_units_sold,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    COUNT(DISTINCT StockCode) AS total_products,
    COUNT(DISTINCT CustomerID) AS identified_customers
FROM
    sales_transactions
WHERE
    CustomerID IS NOT NULL;

-- ============================================================
-- 2. MONTHLY REVENUE
-- ============================================================
SELECT
    DATE_FORMAT (InvoiceDate, '%Y-%m') AS sales_month,
    ROUND(SUM(LineRevenue), 2) AS revenue
FROM
    sales_transactions
GROUP BY
    DATE_FORMAT (InvoiceDate, '%Y-%m')
ORDER BY
    sales_month;

-- ============================================================
-- 3. MONTHLY ORDERS
-- ============================================================
SELECT
    DATE_FORMAT (InvoiceDate, '%Y-%m') AS sales_month,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM
    sales_transactions
GROUP BY
    DATE_FORMAT (InvoiceDate, '%Y-%m')
ORDER BY
    sales_month;

-- ============================================================
-- 4. AVERAGE ORDER VALUE(AOV)
-- ============================================================
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS sales_month,
    COUNT(DISTINCT InvoiceNo) AS orders,
    ROUND(SUM(LineRevenue), 2) AS revenue,
    ROUND(
        SUM(LineRevenue) / COUNT(DISTINCT InvoiceNo),
        2
    ) AS average_order_value
FROM sales_transactions
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY sales_month;

-- ============================================================
-- 5. REVENUE BY COUNTRY
-- ============================================================
SELECT
    Country,
    ROUND(SUM(LineRevenue), 2) AS revenue,
    SUM(Quantity) AS units_sold,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM
    sales_transactions
GROUP BY
    Country
ORDER BY
    revenue DESC;

-- ============================================================
-- 6. TOP 20 PRODUCTS BY REVENUE
-- ============================================================
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(LineRevenue), 2) AS revenue
FROM
    sales_transactions
GROUP BY
    StockCode,
    Description
ORDER BY
    revenue DESC
LIMIT
    20;

-- ============================================================
-- 7. TOP 20 CUSTOMERS BY REVENUE
-- ============================================================
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS orders,
    SUM(Quantity) AS units_purchased,
    ROUND(SUM(LineRevenue), 2) AS revenue
FROM
    sales_transactions
WHERE
    CustomerID IS NOT NULL
GROUP BY
    CustomerID
ORDER BY
    revenue DESC
LIMIT
    20;

-- ============================================================
-- 8. FINAL PRODUCT PERFORMANCE
-- ============================================================
    SELECT
    StockCode,
    Description,
    COUNT(DISTINCT InvoiceNo) AS orders,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(LineRevenue), 2) AS revenue
FROM sales_transactions
WHERE StockCode NOT IN ('DOT', 'POST', 'M')
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 20;