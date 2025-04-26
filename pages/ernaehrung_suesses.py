import streamlit as st
import pandas as pd
from functions.speichern import speichern_tageseintrag

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🍫 Süßes", page_icon="🍫", layout="centered")
st.title("🍫 Süßes")

st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")

# 🔙 Zurück zur Ernährung
def go_to_ernaehrung():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/Ernaehrung" />
    """, unsafe_allow_html=True)

# 📄 Daten laden
df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

# 🍫 Kategorien für Süßes / Snacks / Backwaren definieren
kategorien_suesses = ["Süßwaren", "Snacks", "Backwaren", "Desserts", "Gebäck", "Kuchen", "Schokolade"]
df = df[df["Kategorie"].str.contains('|'.join(kategorien_suesses), case=False, na=False)]

# Nur Lebensmittel mit Kalorienangabe
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

# 📊 Lebensmittel-Auswahl
st.header("📊 Lebensmittel auswählen")
food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())

# Menge eingeben
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

# 🔥 Kalorienberechnung
daten = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

# 💾 Speichern nur bei Button-Klick
if st.button("💾 Speichern"):
    speichern_tageseintrag(lebensmittel=food_selection, menge=gram_input, kcal=kcal_total)
    st.success("✅ Lebensmittel gespeichert!")

# Hinweis Bezugseinheit
st.caption(f"Bezugsbasis: {daten['Bezugseinheit']}")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    go_to_ernaehrung()