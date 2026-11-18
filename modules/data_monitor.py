import pandas as pd
import streamlit as st
from ui.components import metric_row


def render() -> None:
    st.markdown("### 🛡️ Data Monitor")
    ps = st.session_state.pharmacies
    if not ps:
        st.info("Няма записи за проверка. Зареди аптеки в PharmaNearby.")
    else:
        df = pd.DataFrame(ps)
        metric_row([
            ("Без адрес", str(int((df.address == "Няма адрес в OSM").sum()))),
            ("Без телефон", str(int((df.phone == "Няма телефон в OSM").sum()))),
            ("Без работно време", str(int((df.hours == "Няма работно време в OSM").sum()))),
            ("Дублирани", str(int(df.duplicated(["name", "lat", "lon"]).sum()))),
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Експорт CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "careway_pharmacies.csv", "text/csv",
        )

    st.markdown("#### Източници и ограничения")
    st.write("Аптеки: OpenStreetMap / Overpass · Геокодиране: Nominatim · Маршрути: OSRM · Транспорт: симулиран каталог.")