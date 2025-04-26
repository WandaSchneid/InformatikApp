import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Seitenkonfiguration
st.set_page_config(page_title="📊 Daten", page_icon="📊", layout="centered")
st.title("📊 Daten")

# 🔁 Zurück zum Start
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/" />
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

# --------------------------- Dateneingabe ----------------------------
st.markdown("## 📅 Datenübersicht Eingabetage")

# 📄 Daten laden
pfad = "data/eintraege.csv"
if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
    df = pd.read_csv(pfad)
else:
    df = pd.DataFrame(columns=["tag", "lebensmittel", "menge", "kcal"])

selected_day = None
with st.container():
    cols = st.columns(7)
    for i in range(1, 32):
        if i % 7 == 1:
            cols = st.columns(7)
        
        tag_data = df[df["tag"] == i]
        icon = "🟢" if not tag_data.empty else "🔵"
        
        if cols[(i - 1) % 7].button(f"{icon} {i}", key=f"tag_{i}"):
            selected_day = i

# 🧭 Legende
st.markdown("""
**Legende:**  
🟢 = Eintrag vorhanden  
🔵 = Kein Eintrag
""")

# 📋 Tabelle anzeigen
if selected_day:
    st.markdown(f"### 📋 Eingaben für Tag {selected_day}")

    df_tag = df[df["tag"] == selected_day]
    
    if df_tag.empty:
        st.info("Keine Daten für diesen Tag.")
    else:
        st.dataframe(df_tag)

# 📈 Diagramm: kcal pro Tag
st.markdown("## 📈 Verbrauchte kcal im Monat")

if not df.empty:
    kcal_summen = df.groupby("tag")["kcal"].sum().reindex(range(1, 32), fill_value=0)
    
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
    st.info("Noch keine Daten vorhanden.")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    go_to_start()