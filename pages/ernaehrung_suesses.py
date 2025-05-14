import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🍫 Süßes", page_icon="🍫", layout="centered")
hide_sidebar()

st.title("🍫 Süßes")
st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

# 📄 Excel laden
df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

# 🧹 Whitespace bereinigen
df["Kategorie"] = df["Kategorie"].astype(str).str.strip()
df["Name"] = df["Name"].astype(str).str.strip()

# ✅ Filter: Nur Daten aus Kategorie "Suesses"
df = df[df["Kategorie"] == "Suesses"]
df = df.dropna(subset=["Energie, Kalorien (kcal)"])

if df.empty:
    st.warning("⚠️ Keine Lebensmittel in dieser Kategorie gefunden.")
else:
    # 📊 Auswahl
    food_selection = st.selectbox("🍬 Lebensmittel auswählen", df["Name"].unique())
    gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

    auswahl = df[df["Name"] == food_selection]

    if not auswahl.empty:
        kcal_pro_100g = auswahl.iloc[0]["Energie, Kalorien (kcal)"]
        kcal_total = kcal_pro_100g * (gram_input / 100)

        st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

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
            st.success("✅ Gespeichert!")
    else:
        st.warning("⚠️ Keine Nährwerte für dieses Lebensmittel gefunden.")

# 🔙 Zurück
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")
