"""Placeholder for pages built in later stages."""
import streamlit as st

from ui import components as ui


def render(page: str) -> None:
    with st.container(border=True, key="card_coming_soon"):
        ui.section_title(page, "This page is built in an upcoming stage.")
        st.caption("Overview and Database Status are live. The rest follow stage by stage.")
