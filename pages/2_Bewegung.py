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
col1, _ = st.columns([2, 1])

# ------------------ Sportarten Dictionary ------------------
sportarten = {
    "Aerobic": 7.0,
    "Assault Air Bike": 13.0,
    "Badminton": 7.0,
    "Basketball": 8.0,
    "Crosstrainer, langsam": 6.0,
    "Crosstrainer, schnell": 9.0,
    "Croquet": 3.5,
    "Curling": 4.8,
    "Fahrrad": 6.5,
    "Inliner": 7.5,
    "Intervalltraining": 10.0,
    "Joggen, langsam": 8.0,
    "Joggen, schnell": 11.5,
    "Judo": 9.0,
    "Krafttraining": 6.0,
    "Laufen": 7.2,
    "Leichtathletik": 8.0,
    "Liegestütze": 8.0,
    "Pilates": 4.0,
    "Radfahren": 6.5,
    "Reiten": 5.5,
    "Schwimmen": 9.5,
    "Seilspringen": 12.0,
    "Sit Ups": 5.0,
    "Spinning": 10.0,
    "Skifahren": 7.0,
    "Tanzen": 6.5,
    "Tennis": 8.3,
    "Tischtennis": 4.0,
    "Trampolin": 5.0,
    "Wandern": 5.5,
    "Walken": 4.5,
    "Wassergymnastik": 4.0,
    "Yoga": 3.0,
    "Zumba": 8.5
}

# ------------------ Linke Seite ------------------
with col1:
    st.markdown("### 🏃‍♀️ Laufen (min)")
    laufen_min = st.slider("Laufen", 0, 110, step=5)
    laufen_kcal = laufen_min * sportarten["Laufen"]

    st.markdown("### 🧘 Weitere Aktivitäten")

    sport1 = st.selectbox("1. Sportart", list(sportarten.keys()), key="sport1")
    min1 = st.selectbox("Minuten 1. Sportart", list(range(0, 121, 5)), key="min1")
    sport2 = st.selectbox("2. Sportart", list(sportarten.keys()), key="sport2")
    min2 = st.selectbox("Minuten 2. Sportart", list(range(0, 121, 5)), key="min2")

    sport1_kcal = min1 * sportarten[sport1]
    sport2_kcal = min2 * sportarten[sport2]
    total_kcal = laufen_kcal + sport1_kcal + sport2_kcal

    bewegung_text = ""
    if laufen_min > 0:
        bewegung_text += f"Laufen {laufen_min}min"
    if min1 > 0:
        bewegung_text += (", " if bewegung_text else "") + f"{sport1} {min1}min"
    if min2 > 0:
        bewegung_text += (", " if bewegung_text else "") + f"{sport2} {min2}min"

    st.markdown(f"### 🔥 Gesamtverbrauch: **{total_kcal:.1f} kcal**")

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

    if st.button("🔙 Zurück zum Start"):
        go_to_start()