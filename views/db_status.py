"""Database Status page: connection health, table sizes, guardrails."""
import logging
import os
import time

import streamlit as st

from analytics.db import run_query
from ui import components as ui
from ui.format import fmt_int

logger = logging.getLogger(__name__)

# Fixed allow-list of tables (never user input).
TABLES = ("customers", "products", "orders", "order_items")


def render() -> None:
    if st.button("Re-run health check", key="db_refresh"):
        st.cache_data.clear()

    started = time.perf_counter()
    try:
        meta = run_query("SELECT DATABASE() AS db, VERSION() AS version").iloc[0]
        latency_ms = (time.perf_counter() - started) * 1000
        connected, error_name = True, ""
    except Exception as exc:  # show a safe summary; full detail goes to the log
        logger.exception("Database health check failed")
        connected, error_name = False, type(exc).__name__
        meta, latency_ms = None, 0.0

    gemini_ok = bool(os.getenv("GEMINI_API_KEY"))

    with st.container(border=True, key="card_db_status"):
        if connected:
            st.markdown(
                '<div class="status-line"><span class="status-dot ok"></span>Connected</div>',
                unsafe_allow_html=True,
            )
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Database", meta["db"])
            c2.metric("MySQL version", meta["version"])
            c3.metric("Response time", f"{latency_ms:.0f} ms")
            c4.metric("Gemini API key", "Configured" if gemini_ok else "Missing")
        else:
            st.markdown(
                '<div class="status-line"><span class="status-dot bad"></span>Not connected</div>',
                unsafe_allow_html=True,
            )
            st.error(
                f"Connection failed ({error_name}). Check that MySQL is running and that "
                "DB_USER, DB_PASSWORD, DB_HOST, DB_PORT and DB_NAME in your .env file are correct."
            )
            return

    st.write("")
    counts = {}
    for table in TABLES:
        counts[table] = int(run_query(f"SELECT COUNT(*) AS n FROM {table}").iloc[0]["n"])

    for col, table in zip(st.columns(4, gap="small"), TABLES):
        with col:
            ui.kpi_card(table.replace("_", " ").title(), fmt_int(counts[table]), None, "rows")

    st.write("")
    with st.container(border=True, key="card_guardrails"):
        ui.section_title("AI query guardrails", "Enforced by sql_validator.py before anything touches MySQL")
        st.markdown(
            "- Exactly one SQL statement per request\n"
            "- `SELECT` only — INSERT, UPDATE, DELETE, DROP and similar are rejected\n"
            "- `SELECT … INTO` and locking reads are rejected\n"
            "- A `LIMIT 1000` is added (or enforced) on every query"
        )

    with st.expander("Schema the AI sees"):
        try:
            from schema_inspector import get_database_schema

            st.code(get_database_schema(), language="text")
        except Exception as exc:
            logger.exception("Schema inspection failed")
            st.warning(f"Could not read the schema ({type(exc).__name__}).")
