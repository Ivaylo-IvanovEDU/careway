import pandas as pd
import streamlit as st
from core.data import FLEET


def render() -> None:
    st.markdown("### ♿ Accessibility Center")
    st.info("Липсващ OSM етикет не означава, че обектът е недостъпен.")
    ps = st.session_state.pharmacies
    if ps:
        st.dataframe(
            pd.DataFrame([{"Аптека": p["name"], "Адрес": p["address"], "Wheelchair": p["wheelchair"]} for p in ps]),
            use_container_width=True, hide_index=True,
        )
    else:
        st.info("Зареди аптеки от PharmaNearby.")
    st.markdown("#### Транспортни характеристики")
    st.dataframe(FLEET[["Тип", "Район", "Рампа", "Количка"]], use_container_width=True, hide_index=True)