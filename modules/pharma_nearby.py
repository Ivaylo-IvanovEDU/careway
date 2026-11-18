import streamlit as st
from datetime import datetime
from streamlit_folium import st_folium
from core.config import RADIUS_OPTIONS
from core.services import haversine_km, pharmacies_near
from ui.components import build_map, pharmacy_card

def render() -> None:
    st.markdown("### 💊 PharmaNearby")
    st.write("Търси аптеки, отбелязани в OpenStreetMap.")

    radius = st.select_slider(
        "Радиус на търсене",
        options=RADIUS_OPTIONS,
        value=10,
        format_func=lambda x: f"{x} km",
    )

    if st.button("🔎 Потърси аптеки", type="primary"):
        if not st.session_state.origin:
            st.warning("Първо задай местоположение.")
        else:
            with st.spinner("Търсене в OpenStreetMap…"):
                try:
                    lat, lon = st.session_state.origin
                    found = pharmacies_near(lat, lon, radius * 1000)
                    for p in found:
                        p["distance_km"] = haversine_km(st.session_state.origin, (p["lat"], p["lon"]))
                    found.sort(key=lambda p: p["distance_km"])
                    st.session_state.pharmacies = found
                    st.session_state.last_search = datetime.now().strftime("%d.%m.%Y %H:%M")
                    st.session_state.selected = None
                    st.session_state.route = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Грешка при търсенето: {e}")

    ps = st.session_state.pharmacies
    if not ps:
        st.info("Задай местоположение и натисни „Потърси аптеки“.")
        return

    left, right = st.columns([1.35, 1])
    with left:
        st_folium(
            build_map(st.session_state.origin, origin=st.session_state.origin, items=ps),
            height=560, width=None, key="pharmacy_map",
        )
    with right:
        st.markdown(f"#### Намерени аптеки: {len(ps)}")
        for p in ps:
            if pharmacy_card(p):
                st.session_state.selected = p["id"]
                st.session_state.module = "Smart Route"
                st.rerun()
    st.caption("Източник: OpenStreetMap contributors. Данните може да са непълни.")
