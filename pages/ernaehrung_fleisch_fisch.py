import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

st.set_page_config(page_title="🍎 Fleisch / Fisch", page_icon="🥩", layout="centered")
hide_sidebar()

st.title("🥩 Fleisch / Fisch")
st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
df = df[df["Kategorie"] == "Fleisch / Fisch"]
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

st.header("📊 Lebensmittel auswählen")
food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

auswahl = df[df["Name"] == food_selection].iloc[0]
kcal_pro_100g = auswahl["Energie, Kalorien (kcal)"]
kcal_total = kcal_pro_100g * (gram_input / 100)

DataManager().append_record( session_state_key='ernaehrung_df', record_dict={"kcal_pro_100g": kcal_pro_100g, "Timestamp": datetime.now()})

st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

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

if "Bezugseinheit" in auswahl:
    st.caption(f"ℹ️ Bezugsbasis: {auswahl['Bezugseinheit']}")

st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")