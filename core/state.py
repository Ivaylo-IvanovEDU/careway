"""Session state bootstrap — single source of truth."""
import streamlit as st

_DEFAULTS = {
    "origin": None,
    "origin_label": "",
    "pharmacies": [],
    "module": "Dashboard",
    "selected": None,
    "route": None,
    "last_search": "—",
    "search_error": None,
}

def init_state() -> None:
    for k, v in _DEFAULTS.items():
        st.session_state.setdefault(k, v)