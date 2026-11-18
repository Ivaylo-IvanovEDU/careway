"""CAREWAY — entry point."""
import streamlit as st

st.set_page_config(
    page_title="CAREWAY — Smart Healthcare Access",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bootstrap
from core.state import init_state
from ui.theme import inject_theme
from ui.components import hero
from ui.sidebar import render_sidebar

init_state()
inject_theme()

# ── Module registry ──────────────────────────────────────────
from modules import (
    dashboard, pharma_nearby, safe_ride, smart_route,
    accessibility, analytics, data_monitor,
)

REGISTRY = {
    "Dashboard":            dashboard.render,
    "PharmaNearby":         pharma_nearby.render,
    "SafeRide":             safe_ride.render,
    "Smart Route":          smart_route.render,
    "Accessibility Center": accessibility.render,
    "Data Analytics":       analytics.render,
    "Data Monitor":         data_monitor.render,
}

# ── Render ───────────────────────────────────────────────────
render_sidebar()
hero()
REGISTRY[st.session_state.module]()

st.divider()
st.markdown(
    "<center><small style='color:#71849A'>"
    "CAREWAY · Educational prototype · OpenStreetMap contributors · Transport catalogue simulated"
    "</small></center>",
    unsafe_allow_html=True,
)