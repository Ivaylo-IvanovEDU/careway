import streamlit as st
from core.data import FLEET
from ui.components import metric_row


def render() -> None:
    st.markdown("### 🏠 Общ преглед")
    ps = st.session_state.pharmacies
    metric_row([
        ("Аптеки в търсенето", str(len(ps))),
        ("Транспортни записа", str(len(FLEET))),
        ("Модули", "7"),
        ("Последно търсене", st.session_state.last_search),
    ])

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💊 PharmaNearby")
        st.write("Откриване на аптеки по GPS или населено място.")
        if st.button("Отвори PharmaNearby", use_container_width=True):
            st.session_state.module = "PharmaNearby"
            st.rerun()
    with c2:
        st.markdown("#### 🧭 Smart Route")
        st.write("Маршрут до избрана аптека по пътната мрежа.")
        if st.button("Отвори Smart Route", use_container_width=True):
            st.session_state.module = "Smart Route"
            st.rerun()

    if st.session_state.origin:
        st.success(f"Начална точка: {st.session_state.origin_label}")
    else:
        st.warning("Задай GPS позиция или населено място от менюто.")