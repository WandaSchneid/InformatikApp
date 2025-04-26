import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🧈 Fette", page_icon="🧈", layout="centered")
st.title("🧈 Fette & Öle")

st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")

# 🔙 Zurück zur Ernährung
def go_to_ernaehrung():
    st.markdown("""<meta http-equiv="refresh" content="0; url=/Ernaehrung" />""", unsafe_allow_html=True)

# 📄 Daten laden
df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

# 🧈 Nur passende Kategorien filtern
kategorien_fette = ["Fette", "Öle", "Butter", "Pflanzenöl", "Speisefette"]
df = df[df["Kategorie"].str.contains('|'.join(kategorien_fette), case=False, na=False)]

# Nur Lebensmittel mit Kalorienangabe
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

# 📊 Lebensmittel auswählen
st.header("📊 Lebensmittel auswählen")
food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())

# ⚖️ Menge eingeben
gram_input = st.number_input("⚖️ Menge in Gramm oder ml", min_value=1, max_value=1000, value=100)

# 🔥 Kalorienberechnung
daten = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

st.success(f"📈 {gram_input}g/ml {food_selection} enthalten **{kcal_total:.2f} kcal**.")

# 💾 Speichern
if st.button("💾 Speichern"):
    heute = datetime.now()
    speichern_tageseintrag(
        monat=heute.month,
        tag=heute.day,
        lebensmittel=food_selection,
        menge=gram_input,
        kcal=kcal_total
    )
    st.success("✅ Lebensmittel gespeichert!")

# ℹ️ Bezugseinheit Hinweis
if "Bezugseinheit" in daten:
    st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    go_to_ernaehrung()