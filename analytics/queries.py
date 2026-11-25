"""All SQL used by the dashboard pages (cached, parameterised)."""
import pandas as pd
import streamlit as st

from analytics.db import run_query
from analytics.filters import BASE_FROM, Filters

CACHE_SECONDS = 300

# Allow-lists: column names are never taken from user input.
DIMENSIONS = {
    "category": "p.category",
    "sub_category": "p.sub_category",
    "region": "o.region",
    "state": "o.state",
    "city": "o.city",
    "segment": "c.segment",
    "ship_mode": "o.ship_mode",
}
RANKING = {"sales": "sales", "profit": "profit", "quantity": "quantity"}


def _to_date(value):
    return pd.to_datetime(value).date()


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def dataset_info() -> dict:
    row = run_query(
        """
        SELECT
            (SELECT COUNT(*) FROM customers)   AS customers,
            (SELECT COUNT(*) FROM products)    AS products,
            (SELECT COUNT(*) FROM orders)      AS orders,
            (SELECT COUNT(*) FROM order_items) AS line_items,
            (SELECT MIN(order_date) FROM orders) AS first_order,
            (SELECT MAX(order_date) FROM orders) AS last_order
        """
    ).iloc[0]
    return {
        "customers": int(row["customers"]),
        "products": int(row["products"]),
        "orders": int(row["orders"]),
        "line_items": int(row["line_items"]),
        "first_order": _to_date(row["first_order"]),
        "last_order": _to_date(row["last_order"]),
    }


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def filter_options() -> dict:
    """Distinct filter values and the available date range, read from the DB."""
    def distinct(sql):
        return run_query(sql).iloc[:, 0].dropna().tolist()

    info = dataset_info()
    return {
        "min_date": info["first_order"],
        "max_date": info["last_order"],
        "regions": distinct("SELECT DISTINCT region FROM orders ORDER BY region"),
        "categories": distinct("SELECT DISTINCT category FROM products ORDER BY category"),
        "segments": distinct("SELECT DISTINCT segment FROM customers ORDER BY segment"),
        "ship_modes": distinct("SELECT DISTINCT ship_mode FROM orders ORDER BY ship_mode"),
    }


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def kpis(f: Filters) -> dict:
    where, params = f.where()
    row = run_query(
        f"""
        SELECT
            COALESCE(SUM(oi.sales), 0)       AS total_sales,
            COALESCE(SUM(oi.profit), 0)      AS total_profit,
            COUNT(DISTINCT o.order_id)       AS total_orders,
            COUNT(DISTINCT o.customer_id)    AS total_customers,
            COALESCE(SUM(oi.quantity), 0)    AS total_quantity
        {BASE_FROM}
        WHERE {where}
        """,
        params,
    ).iloc[0]
    return {key: float(row[key]) for key in row.index}


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def monthly_trend(f: Filters) -> pd.DataFrame:
    where, params = f.where()
    df = run_query(
        f"""
        SELECT
            DATE_SUB(o.order_date, INTERVAL (DAYOFMONTH(o.order_date) - 1) DAY) AS month,
            SUM(oi.sales)               AS sales,
            SUM(oi.profit)              AS profit,
            COUNT(DISTINCT o.order_id)  AS orders
        {BASE_FROM}
        WHERE {where}
        GROUP BY month
        ORDER BY month
        """,
        params,
    )
    df["month"] = pd.to_datetime(df["month"])
    return df


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def breakdown(f: Filters, dimension: str) -> pd.DataFrame:
    """Sales / profit / quantity / orders grouped by an allow-listed dimension."""
    column = DIMENSIONS[dimension]
    where, params = f.where()
    return run_query(
        f"""
        SELECT
            {column}                    AS label,
            SUM(oi.sales)               AS sales,
            SUM(oi.profit)              AS profit,
            SUM(oi.quantity)            AS quantity,
            COUNT(DISTINCT o.order_id)  AS orders
        {BASE_FROM}
        WHERE {where}
        GROUP BY {column}
        ORDER BY sales DESC
        """,
        params,
    )


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def top_products(f: Filters, n: int = 5, by: str = "sales") -> pd.DataFrame:
    order_col = RANKING[by]
    where, params = f.where()
    return run_query(
        f"""
        SELECT
            p.product_name              AS label,
            SUM(oi.sales)               AS sales,
            SUM(oi.profit)              AS profit,
            SUM(oi.quantity)            AS quantity
        {BASE_FROM}
        WHERE {where}
        GROUP BY p.product_id, p.product_name
        ORDER BY {order_col} DESC
        LIMIT {int(n)}
        """,
        params,
    )


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def top_customers(f: Filters, n: int = 5, by: str = "sales") -> pd.DataFrame:
    order_col = "orders" if by == "orders" else RANKING[by]
    where, params = f.where()
    return run_query(
        f"""
        SELECT
            c.customer_name             AS label,
            SUM(oi.sales)               AS sales,
            SUM(oi.profit)              AS profit,
            COUNT(DISTINCT o.order_id)  AS orders
        {BASE_FROM}
        WHERE {where}
        GROUP BY c.customer_id, c.customer_name
        ORDER BY {order_col} DESC
        LIMIT {int(n)}
        """,
        params,
    )
