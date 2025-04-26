import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🏃‍♂️ Bewegung", page_icon="🏃‍♂️", layout="wide")
st.title("🏃‍♂️ Bewegung")

# 🔁 Funktion: Zurück zum Start
def go_to_start():
    st.markdown("""<meta http-equiv="refresh" content="0; url=/" />""", unsafe_allow_html=True)

# ------------------ Layout ------------------
col1, col2 = st.columns([2, 1])

# ------------------ Linke Seite ------------------
with col1:
    st.markdown("### 📅 Wähle einen Wochentag")

    # Woche-Tage Auswahl
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    selected_day = st.selectbox("Wochentag auswählen", days, index=4)

    # Kuchendiagramm
    fig, ax = plt.subplots()
    ax.pie([1]*7, labels=days, startangle=90,
           colors=["#e0e0e0" if d != selected_day else "#90caf9" for d in days])
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("### 🏃‍♀️ Laufen (min)")
    laufen_min = st.slider("Laufen", 0, 110, step=5)
    laufen_kcal = laufen_min * 7.2

    st.markdown("### 🧘 Weitere Aktivitäten")

    sportarten = {
        "Tennis": 8.3,
        "Curling": 4.8,
        "Yoga": 3.0,
        "Fahrrad": 6.5,
        "Pilates": 4.0,
        "Schwimmen": 9.5,
        "Aerobic": 7.0
    }

    sport1 = st.selectbox("1. Sportart", list(sportarten.keys()), key="sport1")
    min1 = st.selectbox("Minuten 1. Sportart", list(range(0, 121, 5)), key="min1")
    sport2 = st.selectbox("2. Sportart", list(sportarten.keys()), key="sport2")
    min2 = st.selectbox("Minuten 2. Sportart", list(range(0, 121, 5)), key="min2")

    sport1_kcal = min1 * sportarten[sport1]
    sport2_kcal = min2 * sportarten[sport2]
    total_kcal = laufen_kcal + sport1_kcal + sport2_kcal

    # Bewegung zusammenfassen
    bewegung_text = ""
    if laufen_min > 0:
        bewegung_text += f"Laufen {laufen_min}min"
    if min1 > 0:
        bewegung_text += (", " if bewegung_text else "") + f"{sport1} {min1}min"
    if min2 > 0:
        bewegung_text += (", " if bewegung_text else "") + f"{sport2} {min2}min"

    st.markdown(f"### 🔥 Gesamtverbrauch: **{total_kcal:.1f} kcal**")

    # 💾 Speichern-Button
    if st.button("💾 Bewegung speichern"):
        heute = datetime.now()
        speichern_tageseintrag(
            monat=heute.month,
            tag=heute.day,
            bewegung=bewegung_text,
            bewegung_kcal=total_kcal
        )
        st.success("✅ Bewegung für heute gespeichert!")

    st.markdown("---")

    # 🔙 Zurück zur Startseite
    if st.button("🔙 Zurück zum Start"):
        go_to_start()

# ------------------ Rechte Seite ------------------
with col2:
    st.markdown("### 🧾 Übersicht kcal/min pro Sportart")
    df = pd.DataFrame(
        [{"Sportart": k, "kcal/min": v} for k, v in sportarten.items()]
    )
    st.table(df)