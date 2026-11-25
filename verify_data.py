
from sqlalchemy import text
from test_db import engine

with engine.connect() as connection:

    result = connection.execute(text("""
        SELECT
            COUNT(*) AS total_records,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            SUM(quantity) AS total_quantity
        FROM order_items
    """))

    row = result.fetchone()

    print("Total transaction records:", row[0])
    print("Total sales:", row[1])
    print("Total profit:", row[2])
    print("Total quantity sold:", row[3])
