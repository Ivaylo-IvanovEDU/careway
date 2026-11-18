import streamlit as st
from core.data import FLEET

def render() -> None:
    st.markdown("### 🚐 SafeRide")
    st.warning("Демонстрационен каталог — не са реални оператори.")
    only = st.toggle("Само варианти за инвалидна количка")
    view = FLEET[FLEET["Количка"].isin(["Да", "По заявка"])] if only else FLEET
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.caption("За реална услуга използвай проверени общински или лицензирани оператори.")
