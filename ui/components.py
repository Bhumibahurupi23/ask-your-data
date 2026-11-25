"""Layout building blocks: sidebar, header, KPI cards, filter bar, chart cards."""
from datetime import datetime

import streamlit as st

from analytics.filters import Filters
from ui.format import fmt_int
from ui.theme import PLOT_CONFIG

NAV = {
    "Overview": ":material/dashboard: Overview",
    "Sales Analytics": ":material/trending_up: Sales Analytics",
    "Product Analytics": ":material/inventory_2: Product Analytics",
    "Customer Analytics": ":material/group: Customer Analytics",
    "Regional Analytics": ":material/public: Regional Analytics",
    "Ask AI": ":material/auto_awesome: Ask AI",
    "Database Status": ":material/database: Database Status",
}

FILTER_KEYS = ("f_dates", "f_regions", "f_categories", "f_segments", "f_ship_modes")


def sidebar_nav() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
              <div class="brand-mark">A</div>
              <div><div class="brand-name">Ask-Your-Data</div>
              <div class="brand-sub">AI Business Intelligence</div></div>
            </div>
            <div class="nav-label">Workspace</div>
            """,
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigation", list(NAV), format_func=NAV.get,
            label_visibility="collapsed", key="nav",
        )
        st.markdown(
            '<div class="side-foot">Superstore dataset · MySQL · Gemini</div>',
            unsafe_allow_html=True,
        )
    return page


def page_header(title: str, subtitle: str, info: dict | None = None) -> None:
    today = datetime.now().strftime("%A, %d %B %Y")
    chips = ""
    if info:
        chips = (
            f'<span class="chip">{fmt_int(info["line_items"])} line items</span>'
            f'<span class="chip">{fmt_int(info["orders"])} orders</span>'
            f'<span class="chip">{fmt_int(info["customers"])} customers</span>'
            f'<span class="chip">{info["first_order"]:%b %Y} – {info["last_order"]:%b %Y}</span>'
        )
    st.markdown(
        f"""
        <div class="page-header">
          <div>
            <div class="eyebrow">{today}</div>
            <div class="page-title">{title}</div>
            <div class="page-sub">{subtitle}</div>
          </div>
          <div class="chips">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = "") -> None:
    sub = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f'<div class="sec-title">{title}</div>{sub}', unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: float | None = None, hint: str = "") -> None:
    delta_html = ""
    if delta is not None:
        cls = "up" if delta > 0.05 else "down" if delta < -0.05 else "flat"
        arrow = "▲" if cls == "up" else "▼" if cls == "down" else "•"
        delta_html = f'<span class="kpi-delta {cls}">{arrow} {abs(delta):.1f}%</span>'
        hint = f"vs prior period · {hint}" if hint else "vs prior period"
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-foot">{delta_html}<span>{hint}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card(title: str, subtitle: str, fig, key: str) -> None:
    with st.container(border=True, key=f"card_{key}"):
        section_title(title, subtitle)
        st.plotly_chart(fig, width="stretch", config=PLOT_CONFIG, key=f"chart_{key}")


def _reset_filters(min_date, max_date) -> None:
    st.session_state["f_dates"] = (min_date, max_date)
    for key in FILTER_KEYS[1:]:
        st.session_state[key] = []


def filter_bar(options: dict) -> Filters:
    """Render the global filter bar and return the active Filters."""
    min_date, max_date = options["min_date"], options["max_date"]
    st.session_state.setdefault("f_dates", (min_date, max_date))

    with st.container(border=True, key="filter_bar"):
        cols = st.columns([1.5, 1, 1, 1, 1, 0.6], vertical_alignment="bottom")
        with cols[0]:
            dates = st.date_input(
                "Date range", min_value=min_date, max_value=max_date,
                format="YYYY-MM-DD", key="f_dates",
            )
        with cols[1]:
            regions = st.multiselect("Region", options["regions"], key="f_regions", placeholder="All regions")
        with cols[2]:
            categories = st.multiselect("Category", options["categories"], key="f_categories", placeholder="All categories")
        with cols[3]:
            segments = st.multiselect("Segment", options["segments"], key="f_segments", placeholder="All segments")
        with cols[4]:
            ship_modes = st.multiselect("Ship mode", options["ship_modes"], key="f_ship_modes", placeholder="All modes")
        with cols[5]:
            st.button(
                "Reset", key="f_reset", on_click=_reset_filters,
                args=(min_date, max_date), width="stretch",
            )

    if not isinstance(dates, (tuple, list)) or len(dates) != 2:
        st.info("Pick an end date to apply the date range.")
        st.stop()

    return Filters(
        start=dates[0], end=dates[1],
        regions=tuple(regions), categories=tuple(categories),
        segments=tuple(segments), ship_modes=tuple(ship_modes),
    )


def db_error(exc: Exception) -> None:
    st.error(
        f"Couldn't reach the database ({type(exc).__name__}). "
        "Check that MySQL is running and your .env values are correct, "
        "then open **Database Status** from the sidebar."
    )
