import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🍫 Süßes", page_icon="🍫", layout="centered")
st.title("🍫 Süßes")

st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

# 🔙 Funktion: Zurück zur Ernährung
def go_to_ernaehrung():
    st.markdown("""<meta http-equiv="refresh" content="0; url=/Ernaehrung" />""", unsafe_allow_html=True)

# 📄 Ernährungsdaten laden
df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

# 🍬 Filter: Nur Süßes / Snacks / Backwaren
kategorien_suesses = ["Süßwaren", "Snacks", "Backwaren", "Desserts", "Gebäck", "Kuchen", "Schokolade"]
df = df[df["Kategorie"].str.contains('|'.join(kategorien_suesses), case=False, na=False)]
df = df.dropna(subset=["Energie, Kalorien (kcal)"])  # Nur Einträge mit kcal

# 📊 Lebensmittel-Auswahl
st.header("📊 Lebensmittel auswählen")

food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

# 🔥 Kalorienberechnung
daten = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

# 💾 Speichern-Button
if st.button("💾 Speichern"):
    heute = datetime.now()
    speichern_tageseintrag(
        monat=heute.month,
        tag=heute.day,
        lebensmittel=food_selection,
        menge=gram_input,
        kcal=kcal_total
    )
    st.success(f"✅ {gram_input}g {food_selection} mit {kcal_total:.2f} kcal gespeichert!")

# 📋 Hinweis: Bezugseinheit
if "Bezugseinheit" in daten:
    st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

# 🔙 Zurück zur Ernährung
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    go_to_ernaehrung()