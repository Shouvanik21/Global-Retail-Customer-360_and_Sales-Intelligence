from pathlib import Path
import getpass
import mysql.connector
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

SALES_FILE = PROJECT_DIR / "data" / "processed" / "sales_transactions.csv"
RETURNS_FILE = PROJECT_DIR / "data" / "processed" / "returns_transactions.csv"


# ============================================================
# 2. MYSQL CONNECTION DETAILS
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_DATABASE = "retail_analytics"


# ============================================================
# 3. GET MYSQL PASSWORD SECURELY
# ============================================================

MYSQL_PASSWORD = getpass.getpass(
    "Enter MySQL root password: "
)


# ============================================================
# 4. CONNECT TO MYSQL
# ============================================================

print("\n========== CONNECTING TO MYSQL ==========")

connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = connection.cursor()

print("MySQL connection successful.")


# ============================================================
# 5. LOAD SALES DATA
# ============================================================

print("\n========== LOADING SALES DATA ==========")

sales = pd.read_csv(
    SALES_FILE,
    dtype={
        "InvoiceNo": str,
        "StockCode": str
    }
)

sales = sales.where(pd.notna(sales), None)

sales_query = """
INSERT INTO sales_transactions
(
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    UnitPrice,
    CustomerID,
    Country,
    LineRevenue
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

sales_data = [
    tuple(row)
    for row in sales[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
            "LineRevenue"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(sales_query, sales_data)

connection.commit()

print("Sales rows inserted:", cursor.rowcount)


# ============================================================
# 6. LOAD RETURNS DATA
# ============================================================

print("\n========== LOADING RETURNS DATA ==========")

returns = pd.read_csv(
    RETURNS_FILE,
    dtype={
        "InvoiceNo": str,
        "StockCode": str
    }
)

returns = returns.where(pd.notna(returns), None)

returns_query = """
INSERT INTO returns_transactions
(
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    UnitPrice,
    CustomerID,
    Country,
    ReturnValue
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

returns_data = [
    tuple(row)
    for row in returns[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
            "ReturnValue"
        ]
    ].itertuples(index=False, name=None)
]

cursor.executemany(returns_query, returns_data)

connection.commit()

print("Return rows inserted:", cursor.rowcount)


# ============================================================
# 7. VERIFY ROW COUNTS
# ============================================================

print("\n========== VERIFYING MYSQL DATA ==========")

cursor.execute(
    "SELECT COUNT(*) FROM sales_transactions"
)

sales_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM returns_transactions"
)

returns_count = cursor.fetchone()[0]

print("Sales rows in MySQL:", sales_count)
print("Returns rows in MySQL:", returns_count)


# ============================================================
# 8. CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("\n========== MYSQL LOAD COMPLETE ==========")