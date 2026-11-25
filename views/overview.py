"""Overview page: KPI cards, trends, mix and leaderboards."""
import streamlit as st

from analytics import queries
from analytics.filters import Filters
from ui import charts
from ui import components as ui
from ui.format import fmt_int, fmt_money
from ui.theme import ACCENT, TEAL


def _with_aov(k: dict) -> dict:
    k = dict(k)
    k["aov"] = k["total_sales"] / k["total_orders"] if k["total_orders"] else 0.0
    return k


def _pct_change(current: float, previous: float):
    return None if not previous else (current - previous) / abs(previous) * 100


def render(f: Filters) -> None:
    with st.spinner("Loading dashboard…"):
        cur = _with_aov(queries.kpis(f))
        prev = _with_aov(queries.kpis(f.previous_period()))
        trend = queries.monthly_trend(f)
        by_category = queries.breakdown(f, "category")
        by_region = queries.breakdown(f, "region")
        products = queries.top_products(f, n=5, by="sales")
        customers = queries.top_customers(f, n=5, by="sales")

    if cur["total_orders"] == 0:
        st.info("No orders match the current filters. Try widening the date range or clearing a filter.")
        return

    has_prev = prev["total_orders"] > 0

    def delta(key: str):
        return _pct_change(cur[key], prev[key]) if has_prev else None

    margin = cur["total_profit"] / cur["total_sales"] * 100 if cur["total_sales"] else 0

    cards = [
        ("Total Sales", fmt_money(cur["total_sales"]), delta("total_sales"), "revenue"),
        ("Total Profit", fmt_money(cur["total_profit"]), delta("total_profit"), f"{margin:.1f}% margin"),
        ("Total Orders", fmt_int(cur["total_orders"]), delta("total_orders"), "distinct orders"),
        ("Total Customers", fmt_int(cur["total_customers"]), delta("total_customers"), "active"),
        ("Quantity Sold", fmt_int(cur["total_quantity"]), delta("total_quantity"), "units"),
        ("Avg Order Value", fmt_money(cur["aov"]), delta("aov"), "per order"),
    ]
    for col, (label, value, d, hint) in zip(st.columns(6, gap="small"), cards):
        with col:
            ui.kpi_card(label, value, d, hint)

    st.write("")
    left, right = st.columns(2, gap="medium")
    with left:
        ui.chart_card(
            "Sales trend", "Monthly sales",
            charts.area_trend(trend, "month", "sales", ACCENT, "Sales"), "sales_trend",
        )
    with right:
        ui.chart_card(
            "Profit trend", "Monthly profit (red = loss-making month)",
            charts.profit_bars(trend, "month", "profit"), "profit_trend",
        )

    left, right = st.columns(2, gap="medium")
    with left:
        ui.chart_card(
            "Sales by category", "Share of revenue",
            charts.donut(by_category, "label", "sales"), "sales_category",
        )
    with right:
        ui.chart_card(
            "Sales by region", "Total sales per region",
            charts.hbar(by_region, "label", "sales", ACCENT), "sales_region",
        )

    left, right = st.columns(2, gap="medium")
    with left:
        ui.chart_card(
            "Top 5 products", "By sales",
            charts.hbar(products, "label", "sales", ACCENT, label_len=32), "top_products",
        )
    with right:
        ui.chart_card(
            "Top 5 customers", "By sales",
            charts.hbar(customers, "label", "sales", TEAL), "top_customers",
        )
