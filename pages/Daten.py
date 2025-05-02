import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.login_manager import LoginManager
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
from functions.speichern import speichern_tageseintrag, speichern_profil, laden_profil
from streamlit import switch_page
from utils.ui_utils import hide_sidebar

# --- Seitenkonfiguration ---
st.set_page_config(page_title="📊 Daten", page_icon="📊", layout="centered")

# --- Sidebar ausblenden ---
hide_sidebar()

st.title("📊 Datenübersicht")

# 🔁 Bessere Funktion: Zurück zum Start
def go_to_start():
    switch_page("Start")

# 📄 Einträge laden
pfad_eintraege = "data/eintraege.csv"
if os.path.exists(pfad_eintraege) and os.path.getsize(pfad_eintraege) > 0:
    df_eintraege = pd.read_csv(pfad_eintraege)
    if "wasser_ml" not in df_eintraege.columns:
        df_eintraege["wasser_ml"] = 0
else:
    df_eintraege = pd.DataFrame(columns=["monat", "tag", "lebensmittel", "menge", "kcal", "bewegung", "bewegung_kcal", "schlaf_zusammenfassung", "wasser_ml"])

# 📄 Profil laden
profil = laden_profil()

# --------------------------- Profil ----------------------------
st.markdown("## 👤 Profil")

name = st.text_input("Name:", value=profil.get("Name", "") if profil else "")
alter = st.number_input("Alter:", min_value=0, max_value=120, step=1, value=int(profil.get("Alter", 0)) if profil else 0)
gewicht = st.number_input("Gewicht (kg):", min_value=0.0, step=0.1, value=float(profil.get("Gewicht", 0.0)) if profil else 0.0)
geschlecht = st.selectbox("Geschlecht:", ["Weiblich", "Männlich", "Divers"],
    index=["Weiblich", "Männlich", "Divers"].index(profil.get("Geschlecht", "Weiblich")) if profil else 0)

# --------------------------- Ziele ----------------------------
st.markdown("## 🎯 Ziele")

ziele_liste = [
    "Mehr Schlafen", "Mehr kcal verbrauchen", "Mehr Gemüse essen",
    "Früher zu Bett gehen", "Längere Spaziergänge", "Mehr Wasser trinken"
]

ziel1 = st.selectbox("1. Ziel:", ziele_liste, index=ziele_liste.index(profil.get("Ziel1", ziele_liste[0])) if profil else 0)
ziel2 = st.selectbox("2. Ziel:", ziele_liste, index=ziele_liste.index(profil.get("Ziel2", ziele_liste[1])) if profil else 1)

if st.button("💾 Profil & Ziele speichern"):
    speichern_profil(name, alter, gewicht, geschlecht, ziel1, ziel2)
    st.success("✅ Profil und Ziele gespeichert!")

# --------------------------- Monat & Tag auswählen ----------------------------
st.markdown("## 📅 Monat und Eingabetage auswählen")

monatsnamen = [calendar.month_name[i] for i in range(1, 13)]
aktueller_monat = datetime.now().month
aktueller_tag = datetime.now().day

monat_name_anzeige = st.selectbox("📅 Monat:", monatsnamen, index=aktueller_monat-1)
monat_auswahl = monatsnamen.index(monat_name_anzeige) + 1

selected_day = aktueller_tag

# 🗓️ Tage darstellen
st.markdown("### 🗓️ Tage:")

with st.container():
    cols = st.columns(7)
    for i in range(1, 32):
        if i % 7 == 1:
            cols = st.columns(7)

        tag_data = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == i)]
        icon = "🟢" if not tag_data.empty else "🔵"

        button_label = f"{icon} {i}"
        button_key = f"tag_{i}"

        if i == aktueller_tag and monat_auswahl == aktueller_monat:
            button_label = f"⭐ {i}"
            if selected_day is None:
                selected_day = i

        if cols[(i-1)%7].button(button_label, key=button_key):
            selected_day = i

# 🧭 Legende
st.markdown("""<br>**Legende:**  
🟢 = Eintrag vorhanden  
🔵 = Kein Eintrag  
⭐ = Heute
""", unsafe_allow_html=True)

# --------------------------- Tagesdaten ----------------------------
if selected_day:
    st.markdown(f"## 📝 Eingaben für Tag {selected_day}")

    df_tag = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == selected_day)]

    if df_tag.empty:
        st.info("Keine Daten für diesen Tag.")
    else:
        df_tag_display = df_tag.copy()
        if "lebensmittel" in df_tag_display.columns:
            df_tag_display["lebensmittel"] = df_tag_display["lebensmittel"].astype(str).str.replace(", ", "\n")

        st.dataframe(df_tag_display, use_container_width=True)

# --------------------------- Diagramm ----------------------------
st.markdown("## 📈 Aufgenommene und verbrauchte kcal im Monat")

df_monat = df_eintraege[df_eintraege["monat"] == monat_auswahl]

if not df_monat.empty:
    kcal_aufnahme = df_monat.groupby("tag")["kcal"].sum().reindex(range(1, 32), fill_value=0)
    kcal_verbrauch = df_monat.groupby("tag")["bewegung_kcal"].sum().reindex(range(1, 32), fill_value=0)

    fig, ax = plt.subplots(figsize=(14,6))
    bar_width = 0.4
    days = range(1, 32)

    ax.bar([d - bar_width/2 for d in days], kcal_aufnahme.values, width=bar_width, label="Aufgenommene kcal (Ernährung)")
    ax.bar([d + bar_width/2 for d in days], kcal_verbrauch.values, width=bar_width, label="Verbrauchte kcal (Bewegung)")

    ax.set_title("📊 Vergleich: Aufgenommene vs. Verbrannte Kalorien pro Tag", fontsize=18, fontweight='bold')
    ax.set_xlabel("Tag im Monat", fontsize=14)
    ax.set_ylabel("kcal", fontsize=14)
    ax.set_xticks(days)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Noch keine Daten für diesen Monat.")

# --- Zurück zur Startseite ---
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    switch_page("Start.py")