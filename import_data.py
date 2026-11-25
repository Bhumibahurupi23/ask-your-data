
import pandas as pd
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL safely
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(connection_url)

# Read CSV
df = pd.read_csv(
    "data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Prepare customers: one row per customer ID
customers = df[
    ["Customer ID", "Customer Name", "Segment"]
].drop_duplicates(subset=["Customer ID"])

customers.columns = [
    "customer_id", "customer_name", "segment"
]

# Prepare products: one row per product ID
products = df[
    ["Product ID", "Product Name", "Category", "Sub-Category"]
].drop_duplicates(subset=["Product ID"])

products.columns = [
    "product_id", "product_name", "category", "sub_category"
]

# Prepare orders: one row per order ID
orders = df[
    [
        "Order ID", "Customer ID", "Order Date", "Ship Date",
        "Ship Mode", "Country", "City", "State",
        "Postal Code", "Region"
    ]
].drop_duplicates(subset=["Order ID"])

orders.columns = [
    "order_id", "customer_id", "order_date", "ship_date",
    "ship_mode", "country", "city", "state",
    "postal_code", "region"
]

# Prepare order items: one row per transaction line
order_items = df[
    [
        "Row ID", "Order ID", "Product ID",
        "Sales", "Quantity", "Discount", "Profit"
    ]
]

order_items.columns = [
    "row_id", "order_id", "product_id",
    "sales", "quantity", "discount", "profit"
]

# Import everything in one transaction
try:
    with engine.begin() as connection:
        customers.to_sql(
            "customers", connection, if_exists="append", index=False
        )

        products.to_sql(
            "products", connection, if_exists="append", index=False
        )

        orders.to_sql(
            "orders", connection, if_exists="append", index=False
        )

        order_items.to_sql(
            "order_items", connection, if_exists="append", index=False
        )

    print("Data imported successfully!")
    print("Customers:", len(customers))
    print("Products:", len(products))
    print("Orders:", len(orders))
    print("Order Items:", len(order_items))

except Exception as error:
    print("Import failed:", error)
