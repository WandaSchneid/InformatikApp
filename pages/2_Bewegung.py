import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Seitenkonfiguration
st.set_page_config(page_title="🏃‍♂️ Bewegung", page_icon="🏃‍♂️", layout="wide")
st.title("🏃‍♂️ Bewegung")

# 🔁 Funktion zum Zurückspringen
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=../" />
    """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# ------------------ Linke Seite ------------------
with col1:
    st.markdown("### 📅 Wähle einen Tag")

    # Kuchendiagramm
    days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    selected_day = st.selectbox("Wochentag auswählen", days, index=4)

    # Kuchen zeichnen
    fig, ax = plt.subplots()
    ax.pie([1]*7, labels=days, startangle=90,
           colors=["#e0e0e0" if d != selected_day else "#90caf9" for d in days])
    ax.axis("equal")
    st.pyplot(fig)

    # ---------------- Laufen Slider ----------------
    st.markdown("### 🏃‍♀️ Laufen (min)")
    laufen_min = st.slider("Laufen", 0, 110, step=5)
    laufen_kcal = laufen_min * 7.2  # z. B. 7.2 kcal/min beim Laufen

    # ---------------- Sportarten ----------------
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

    sport1 = st.selectbox("1. Sportart", list(sportarten.keys()), key="s1")
    min1 = st.selectbox("Minuten", list(range(0, 121, 5)), key="m1")
    sport2 = st.selectbox("2. Sportart", list(sportarten.keys()), key="s2")
    min2 = st.selectbox("Minuten", list(range(0, 121, 5)), key="m2")

    # Berechnung
    sport1_kcal = min1 * sportarten[sport1]
    sport2_kcal = min2 * sportarten[sport2]
    total_kcal = laufen_kcal + sport1_kcal + sport2_kcal

    st.markdown(f"### 🔥 Gesamtverbrauch: **{total_kcal:.1f} kcal**")

    # 🔙 Zurück zur Startseite
    if st.button("🔙 Zurück zum Start"):
        go_to_start()

# ------------------ Rechte Seite ------------------
with col2:
    st.markdown("### 🧾 Sportarten & kcal/min")
    df = pd.DataFrame(
        [{"Sportart": k, "kcal/min": v} for k, v in sportarten.items()]
    )
    st.table(df)