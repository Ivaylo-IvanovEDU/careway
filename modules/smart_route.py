import streamlit as st
from streamlit_folium import st_folium

from core.services import road_route
from ui.components import build_map, metric_row


def render() -> None:
    st.markdown("### 🧭 Smart Route")
    origin = st.session_state.origin
    ps = st.session_state.pharmacies

    if not origin:
        st.warning("Задай начална точка.")
        return
    if not ps:
        st.info("Първо потърси аптеки в PharmaNearby.")
        return

    labels = [f'{p["name"]} · {p["distance_km"]:.2f} km · {p["address"]}' for p in ps]
    lookup = dict(zip(labels, ps))
    idx = next((i for i, p in enumerate(ps) if p["id"] == st.session_state.selected), 0)
    target = lookup[st.selectbox("Избери дестинация", labels, index=idx)]

    if st.button("Изчисли маршрут", type="primary"):
        try:
            with st.spinner("Изчисляване по пътната мрежа…"):
                st.session_state.route = road_route(origin, (target["lat"], target["lon"]))
            st.session_state.selected = target["id"]
        except Exception as e:
            st.error(f"Маршрутната услуга е недостъпна: {e}")

    rt = st.session_state.route
    if rt:
        metric_row([
            ("Разстояние по пътя", f'{rt["km"]:.1f} km'),
            ("Ориентировъчно време", f'{rt["min"]:.0f} min'),
            ("Дестинация", target["name"]),
        ])
        st_folium(
            build_map(origin, origin=origin, items=[target],
                      dest=(target["lat"], target["lon"]), route=rt),
            height=560, width=None, key="route_map",
        )
        st.caption("OSRM demo — времето е ориентировъчно.")
    else:
        st_folium(build_map(origin, origin=origin, items=ps), height=500, width=None, key="route_preview")