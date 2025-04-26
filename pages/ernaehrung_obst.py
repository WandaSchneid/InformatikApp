import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ✅ Funktion zum sicheren Speichern
def speichern_lebensmittel(lebensmittel, menge, kcal):
    eintrag = {
        "tag": datetime.today().day,
        "lebensmittel": lebensmittel,
        "menge": menge,
        "kcal": kcal
    }
    pfad = "data/eintraege.csv"
    
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        df = pd.read_csv(pfad)
        df = pd.concat([df, pd.DataFrame([eintrag])], ignore_index=True)
    else:
        df = pd.DataFrame([eintrag])
    
    df.to_csv(pfad, index=False)

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🍎 Obst", page_icon="🍎", layout="centered")
st.title("🍎 Obst")

st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")

# 🔙 Zurück zur Ernährung
def go_to_ernaehrung():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/Ernaehrung" />
    """, unsafe_allow_html=True)

# 📄 Daten laden
df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

# 🍎 Kategorie für Obst definieren
kategorien_obst = ["Obst", "Früchte", "Fruchtsäfte"]
df = df[df["Kategorie"].str.contains('|'.join(kategorien_obst), case=False, na=False)]

# Nur Lebensmittel mit Kalorienangabe
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

# 📊 Lebensmittel-Auswahl
st.header("📊 Lebensmittel auswählen")
food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())

# Menge eingeben
gram_input = st.number_input("⚖️ Menge in Gramm oder ml", min_value=1, max_value=1000, value=100)

# 🔥 Kalorienberechnung
daten = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

st.success(f"📈 {gram_input}g/ml {food_selection} enthalten **{kcal_total:.2f} kcal**.")

# 💾 Speichern nur bei Button-Klick
if st.button("💾 Speichern"):
    speichern_lebensmittel(food_selection, gram_input, kcal_total)
    st.success("✅ Lebensmittel gespeichert!")

# Hinweis Bezugseinheit
st.caption(f"Bezugsbasis: {daten['Bezugseinheit']}")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    go_to_ernaehrung()