"""Reusable UI pieces — hero, cards, metric rows."""
from __future__ import annotations

import folium
import streamlit as st
from folium.plugins import MarkerCluster

from core.config import APP_TAGLINE, APP_TITLE


def hero() -> None:
    st.markdown(
        f"""
        <div class="cw-hero">
            <div class="cw-kicker">Smart Mobility · Healthcare Access · Bulgaria</div>
            <h1>{APP_TITLE}</h1>
            <p>Открий аптека. Намери достъпен транспорт. Планирай придвижването си.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(items: list[tuple[str, str]]) -> None:
    """items: list of (label, value)."""
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def pharmacy_card(p: dict, key_prefix: str = "ph") -> bool:
    """Render one pharmacy as a styled card. Returns True if user clicked select."""
    st.markdown(
        f"""
        <div class="cw-card">
            <h4>💊 {p['name']}</h4>
            <div class="meta">
                <b>{p['distance_km']:.2f} km</b> · {p['address']}<br>
                ☎ {p['phone']}<br>
                🕒 {p['hours']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return st.button("Избери аптека →", key=f"{key_prefix}_sel_{p['id']}", use_container_width=True)


# ── Folium maps ───────────────────────────────────────────────
def build_map(
    center: tuple[float, float],
    *,
    origin: tuple[float, float] | None = None,
    items: list[dict] | None = None,
    dest: tuple[float, float] | None = None,
    route: dict | None = None,
    zoom: int = 13,
) -> folium.Map:
    m = folium.Map(location=center, zoom_start=zoom, tiles=None, control_scale=True)
    folium.TileLayer(
        "CartoDB dark_matter",
        name="Dark",
        attr="© OpenStreetMap © CartoDB",
    ).add_to(m)

    if origin:
        folium.Marker(
            origin,
            tooltip="Начална точка",
            icon=folium.Icon(color="blue", icon="user", prefix="fa"),
        ).add_to(m)
        folium.Circle(origin, radius=80, color="#19B8FF", fill=True, fill_opacity=.10).add_to(m)

    if items:
        cluster = MarkerCluster(name="Аптеки").add_to(m)
        for p in items:
            folium.Marker(
                (p["lat"], p["lon"]),
                tooltip=p["name"],
                popup=folium.Popup(
                    f"<b>{p['name']}</b><br>{p['address']}<br>{p['phone']}<br>{p['hours']}",
                    max_width=280,
                ),
                icon=folium.Icon(color="green", icon="plus-sign", prefix="glyphicon"),
            ).add_to(cluster)

    if dest:
        folium.Marker(
            dest,
            tooltip="Дестинация",
            icon=folium.Icon(color="red", icon="flag", prefix="fa"),
        ).add_to(m)

    if route:
        folium.PolyLine(route["line"], color="#19B8FF", weight=5, opacity=.85).add_to(m)
        m.fit_bounds(route["line"])
    elif origin and items:
        m.fit_bounds([origin] + [(p["lat"], p["lon"]) for p in items[:40]])
    return m