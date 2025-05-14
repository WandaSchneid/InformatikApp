import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar

st.set_page_config(page_title="🍎 Fette", page_icon="🧈", layout="centered")
hide_sidebar()

st.title("🧈 Fette")
st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
kategorien = ["Fette", "Öle"]
df = df[df["Kategorie"].str.contains('|'.join(kategorien), case=False, na=False)]
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

st.header("📊 Lebensmittel auswählen")
food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

daten = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

if st.button("💾 Speichern"):
    heute = datetime.now()
    speichern_tageseintrag(
        monat=heute.month, tag=heute.day,
        lebensmittel=food_selection,
        menge=gram_input,
        kcal=kcal_total
    )
    st.success(f"✅ {gram_input}g {food_selection} mit {kcal_total:.2f} kcal gespeichert!")

if "Bezugseinheit" in daten:
    st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")
