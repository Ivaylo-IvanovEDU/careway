"""Injects the CSS asset into the Streamlit page."""
from pathlib import Path
import streamlit as st

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "styles.css"

def inject_theme() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)