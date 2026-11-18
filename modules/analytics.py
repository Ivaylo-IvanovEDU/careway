import pandas as pd
import plotly.express as px
import streamlit as st
from ui.components import metric_row

PLOT_LAYOUT = dict(
    paper_bgcolor="#111C2D",
    plot_bgcolor="#111C2D",
    font_color="#F0F5FA",
    margin=dict(l=20, r=20, t=40, b=20),
)


def render() -> None:
    st.markdown("### 📊 Data Analytics")
    ps = st.session_state.pharmacies
    if not ps:
        st.info("Потърси аптеки в PharmaNearby за генериране на анализ.")
        return

    df = pd.DataFrame(ps)
    metric_row([
        ("Аптеки", str(len(df))),
        ("Средно разстояние", f'{df.distance_km.mean():.2f} km'),
        ("Най-близка", f'{df.distance_km.min():.2f} km'),
    ])
    fig = px.histogram(df, x="distance_km", nbins=10, title="Разстояния до намерените аптеки")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Статистиката е само за текущото търсене.")