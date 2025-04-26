import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import calendar
from datetime import datetime
from functions.speichern import speichern_tageseintrag, speichern_profil, laden_profil

# ✅ Seitenkonfiguration
st.set_page_config(page_title="📊 Daten", page_icon="📊", layout="centered")
st.title("📊 Daten")

# 🔁 Zurück zum Start
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/" />
    """, unsafe_allow_html=True)

# 📄 Einträge laden
pfad_eintraege = "data/eintraege.csv"
if os.path.exists(pfad_eintraege) and os.path.getsize(pfad_eintraege) > 0:
    df_eintraege = pd.read_csv(pfad_eintraege)
else:
    df_eintraege = pd.DataFrame(columns=["monat", "tag", "lebensmittel", "menge", "kcal", "bewegung", "bewegung_kcal", "schlaf_zusammenfassung"])

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
    "Mehr Schlafen",
    "Mehr kcal verbrauchen",
    "Mehr Gemüse essen",
    "Früher zu Bett gehen",
    "Längere Spaziergänge",
    "Mehr Wasser trinken"
]

ziel1 = st.selectbox("1. Ziel:", ziele_liste, index=ziele_liste.index(profil.get("Ziel1", ziele_liste[0])) if profil else 0)
ziel2 = st.selectbox("2. Ziel:", ziele_liste, index=ziele_liste.index(profil.get("Ziel2", ziele_liste[1])) if profil else 1)

# 💾 Speichern Button
if st.button("💾 Profil & Ziele speichern"):
    speichern_profil(name, alter, gewicht, geschlecht, ziel1, ziel2)
    st.success("✅ Profil und Ziele gespeichert!")

# --------------------------- Monat & Tag ----------------------------
st.markdown("## 📅 Datenübersicht Eingabetage")

# 🔵 Monat auswählen (mit Namen + Highlight)
monatsnamen = [calendar.month_name[i] for i in range(1, 13)]
verfuegbare_monate = df_eintraege["monat"].unique() if not df_eintraege.empty else []
monatsnamen_anzeige = [f"{calendar.month_name[i]} 🌟" if i in verfuegbare_monate else calendar.month_name[i] for i in range(1, 13)]

aktueller_monat = datetime.now().month
vorauswahl_index = aktueller_monat - 1

monat_name_anzeige = st.selectbox("📅 Monat auswählen:", monatsnamen_anzeige, index=vorauswahl_index)
monat_auswahl = monatsnamen.index(monat_name_anzeige.replace(" 🌟", "")) + 1

# 🗓️ Tag auswählen
selected_day = None
with st.container():
    cols = st.columns(7)
    for i in range(1, 32):
        if i % 7 == 1:
            cols = st.columns(7)
        
        tag_data = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == i)]
        icon = "🟢" if not tag_data.empty else "🔵"

        button_label = f"{icon} {i}"
        button_key = f"tag_{i}"
        if i == datetime.now().day and monat_auswahl == aktueller_monat:
            button_label = f"⭐ {i}"

        if cols[(i - 1) % 7].button(button_label, key=button_key):
            selected_day = i

# 🧭 Legende
st.markdown("""
**Legende:**  
🟢 = Eintrag vorhanden  
🔵 = Kein Eintrag  
⭐ = Heute
""")

# --------------------------- Tabellenanzeige ----------------------------
if selected_day:
    st.markdown(f"### 📋 Eingaben für Tag {selected_day}")

    df_tag = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == selected_day)]
    
    if df_tag.empty:
        st.info("Keine Daten für diesen Tag.")
    else:
        st.dataframe(df_tag)

# --------------------------- Diagramm ----------------------------
st.markdown("## 📈 Verbrauchte kcal im Monat")

df_monat = df_eintraege[df_eintraege["monat"] == monat_auswahl]

if not df_monat.empty:
    kcal_summen = df_monat.groupby("tag")["kcal"].sum().reindex(range(1, 32), fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(kcal_summen.index, kcal_summen.values, marker="o", linewidth=2)
    ax.set_title("Täglicher Kalorienverbrauch", fontsize=16, fontweight='bold')
    ax.set_xlabel("Tag", fontsize=12)
    ax.set_ylabel("kcal", fontsize=12)
    ax.set_xticks(range(1, 32))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_ylim(bottom=0)
    st.pyplot(fig)
else:
    st.info("Noch keine Daten für diesen Monat.")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    go_to_start()