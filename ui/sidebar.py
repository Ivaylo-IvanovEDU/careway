"""Sidebar — navigation + location picker."""
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

from core.config import DEFAULT_PLACE, MODULES
from core.services import geocode


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## 💙 CAREWAY")
        st.caption("SMART HEALTHCARE ACCESS")
        st.divider()

        for name, icon in MODULES:
            label = f"{icon}  {name}"
            active = st.session_state.module == name
            if st.button(
                label,
                use_container_width=True,
                key=f"nav_{name}",
                type="primary" if active else "secondary",
            ):
                st.session_state.module = name
                st.rerun()

        st.divider()
        st.markdown("### 📍 Местоположение")

        # GPS
        gps = streamlit_geolocation()
        if isinstance(gps, dict) and gps.get("latitude") is not None:
            st.session_state.origin = (float(gps["latitude"]), float(gps["longitude"]))
            st.session_state.origin_label = "GPS устройство"
            st.success("GPS позиция получена")
            if gps.get("accuracy"):
                st.caption(f"Точност ±{float(gps['accuracy']):.0f} m")

        # Manual
        place = st.text_input("Населено място", DEFAULT_PLACE, key="sidebar_place")
        if st.button("Задай местоположение", use_container_width=True):
            try:
                g = geocode(place)
                if g:
                    st.session_state.origin = (g[0], g[1])
                    st.session_state.origin_label = g[2]
                    st.success("Зададено")
                else:
                    st.error("Не е намерено населено място.")
            except Exception as e:
                st.error(f"Грешка: {e}")

        if st.session_state.origin:
            st.caption(f"Текуща: {st.session_state.origin_label}")