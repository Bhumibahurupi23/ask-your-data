
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from schema_inspector import engine
from sql_generator import generate_sql
from query_executor import execute_query


st.set_page_config(
    page_title="Ask-Your-Data",
    page_icon="📊",
    layout="wide"
)

# ---------- DATABASE HELPER ----------

@st.cache_data(ttl=60)
def load_data(query):
    with engine.connect() as connection:
        return pd.read_sql_query(text(query), connection)


# ---------- SIDEBAR ----------

st.sidebar.title("📊 Ask-Your-Data")
st.sidebar.caption("AI-Powered Business Intelligence")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Ask AI"]
)

st.sidebar.divider()
st.sidebar.caption("Dataset: Sample Superstore")
st.sidebar.caption("Database: MySQL")


# ---------- OVERVIEW PAGE ----------

if page == "Overview":

    st.title("Business Overview")
    st.caption("Explore your business performance using actual MySQL data.")

    try:
        kpis = load_data("""
            SELECT
                ROUND(SUM(sales), 2) AS total_sales,
                ROUND(SUM(profit), 2) AS total_profit,
                COUNT(DISTINCT order_id) AS total_orders,
                SUM(quantity) AS total_quantity
            FROM order_items
        """)

        customers = load_data("""
            SELECT COUNT(*) AS total_customers
            FROM customers
        """)

        sales = float(kpis.loc[0, "total_sales"] or 0)
        profit = float(kpis.loc[0, "total_profit"] or 0)
        orders = int(kpis.loc[0, "total_orders"] or 0)
        quantity = int(kpis.loc[0, "total_quantity"] or 0)
        customer_count = int(customers.loc[0, "total_customers"])

        average_order_value = sales / orders if orders else 0

        # KPI CARDS

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Sales", f"${sales:,.2f}")
        col2.metric("Total Profit", f"${profit:,.2f}")
        col3.metric("Total Orders", f"{orders:,}")
        col4.metric("Customers", f"{customer_count:,}")

        col5, col6 = st.columns(2)

        col5.metric("Quantity Sold", f"{quantity:,}")
        col6.metric("Average Order Value", f"${average_order_value:,.2f}")

        st.divider()

        # MONTHLY SALES

        st.subheader("Monthly Sales Trend")

        monthly = load_data("""
            SELECT
                DATE_FORMAT(o.order_date, '%Y-%m') AS month,
                ROUND(SUM(oi.sales), 2) AS sales
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
            ORDER BY month
        """)

        if not monthly.empty:
            fig = px.line(
                monthly,
                x="month",
                y="sales",
                markers=True,
                title="Sales over time",
                labels={"month": "Month", "sales": "Sales ($)"}
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        # CATEGORY AND REGION

        left, right = st.columns(2)

        with left:
            st.subheader("Sales by Category")

            category = load_data("""
                SELECT
                    p.category,
                    ROUND(SUM(oi.sales), 2) AS sales
                FROM products p
                JOIN order_items oi
                    ON p.product_id = oi.product_id
                GROUP BY p.category
                ORDER BY sales DESC
            """)

            fig = px.bar(
                category,
                x="category",
                y="sales",
                color="category",
                title="Category Performance"
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.subheader("Sales by Region")

            region = load_data("""
                SELECT
                    o.region,
                    ROUND(SUM(oi.sales), 2) AS sales
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                GROUP BY o.region
                ORDER BY sales DESC
            """)

            fig = px.pie(
                region,
                names="region",
                values="sales",
                title="Regional Sales Distribution",
                hole=0.45
            )
            st.plotly_chart(fig, use_container_width=True)

        # TOP CUSTOMERS

        st.subheader("Top 5 Customers")

        top_customers = load_data("""
            SELECT
                c.customer_name,
                COUNT(DISTINCT o.order_id) AS total_orders,
                ROUND(SUM(oi.sales), 2) AS total_sales
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            JOIN order_items oi
                ON o.order_id = oi.order_id
            GROUP BY c.customer_id, c.customer_name
            ORDER BY total_sales DESC
            LIMIT 5
        """)

        st.dataframe(
            top_customers,
            use_container_width=True,
            hide_index=True
        )

    except Exception as error:
        st.error(f"Could not load dashboard data: {error}")


# ---------- ASK AI PAGE ----------

elif page == "Ask AI":

    st.title("Ask Your Data")
    st.caption(
        "Ask business questions in plain English. "
        "Gemini will generate SQL and retrieve answers from MySQL."
    )

    examples = [
        "What are my total sales?",
        "Show the top 5 customers by number of orders.",
        "Which category generates the highest profit?",
        "Compare sales across regions.",
        "Show monthly sales trends."
    ]

    st.subheader("Try asking")

    for question in examples:
        if st.button(question, use_container_width=True):
            st.session_state["selected_question"] = question

    question = st.text_input(
        "Your business question",
        value=st.session_state.get("selected_question", ""),
        placeholder="Example: Which products generate the highest sales?"
    )

    if st.button("Generate Insights", type="primary"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:
            try:
                with st.spinner("Gemini is generating your SQL..."):
                    generated_sql = generate_sql(question)

                with st.spinner("Validating and querying MySQL..."):
                    safe_sql, results = execute_query(generated_sql)

                st.success("Query executed successfully!")

                with st.expander("View Generated SQL"):
                    st.code(safe_sql, language="sql")

                st.subheader("Query Results")

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                st.info(
                    f"Your query returned {len(results)} rows "
                    f"and {len(results.columns)} columns."
                )

            except Exception as error:
                st.error(f"Unable to process your question: {error}")
