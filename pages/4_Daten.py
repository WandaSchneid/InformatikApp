import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Seitenkonfiguration
st.set_page_config(page_title="📊 Daten", page_icon="📊", layout="centered")
st.title("📊 Daten")

# 🔁 HTML-Redirect Funktion zur Startseite (leer für root)
def go_to_page(filename: str):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url=../{filename}" />
    """, unsafe_allow_html=True)

# --------------------------- Profil ----------------------------
st.markdown("## 👤 Profil")

name = st.text_input("Name:")
alter = st.number_input("Alter:", min_value=0, max_value=120, step=1)
gewicht = st.number_input("Gewicht (kg):", min_value=0.0, step=0.1)
geschlecht = st.selectbox("Geschlecht:", ["Weiblich", "Männlich", "Divers"])

# --------------------------- Ziele ----------------------------
st.markdown("## 🎯 Ziele")

ziele_liste = [
    "Mehr Schlafen",
    "Mehr kcal verbrauchen",
    "Mehr Gemüse essen",
    "Früher zu Bett gehen",
    "Längere Spaziergänge",
    "Mehr Wasser trinken"
]

ziel1 = st.selectbox("1. Ziel", ziele_liste, key="ziel1")
ziel2 = st.selectbox("2. Ziel", ziele_liste, key="ziel2")

# --------------------------- Eingabetage ----------------------------
st.markdown("## 📆 Datenübersicht Eingabetage")

with st.container():
    cols = st.columns(7)
    for i in range(1, 32):
        if i % 7 == 1:
            cols = st.columns(7)
        with cols[(i - 1) % 7]:
            st.button(str(i), key=f"tag_{i}")

# --------------------------- Diagramm ----------------------------
st.markdown("## 📈 Verbrauchte kcal")

tage = np.arange(1, 32)
verbrauchte_kcal = np.random.normal(2200, 200, size=31).clip(min=1500, max=3000)

fig, ax = plt.subplots()
ax.plot(tage, verbrauchte_kcal, color="green", linewidth=2)
ax.set_title("Täglicher Kalorienverbrauch")
ax.set_xlabel("Tag")
ax.set_ylabel("kcal")
st.pyplot(fig)

# --------------------------- Zurück-Button ----------------------------
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    go_to_page("") 