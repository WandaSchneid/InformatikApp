import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🥦 Gemüse", page_icon="🥦", layout="centered")
hide_sidebar()

st.title("🥦 Gemüse")
st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

try:
    # 📄 Excel laden
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")

    # 🧹 Whitespace bereinigen
    df["Kategorie"] = df["Kategorie"].astype(str).str.strip()
    df["Name"] = df["Name"].astype(str).str.strip()

    # ✅ Filter: Nur Kategorie "Gemuese"
    df = df[df["Kategorie"] == "Gemuese"]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])

    if df.empty:
        st.warning("⚠️ Keine Lebensmittel in dieser Kategorie gefunden.")
    else:
        # 📊 Auswahl
        st.header("📊 Lebensmittel auswählen")
        food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique())

        if food_selection:
            gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)
            auswahl = df[df["Name"] == food_selection]

            if not auswahl.empty:
                try:
                    kcal_pro_100g = auswahl.iloc[0]["Energie, Kalorien (kcal)"]
                    kcal_total = kcal_pro_100g * (gram_input / 100)

                    DataManager().append_record( session_state_key='ernaehrung_df', record_dict={"kcal_pro_100g": kcal_pro_100g})

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
                        st.success(f"✅ {gram_input}g {food_selection} mit {kcal_total:.2f} kcal gespeichert!")

                    # ℹ️ Bezugseinheit anzeigen
                    if "Bezugseinheit" in auswahl.columns:
                        bezugswert = auswahl.iloc[0]["Bezugseinheit"]
                        if pd.notna(bezugswert):
                            st.caption(f"ℹ️ Bezugsbasis: {bezugswert}")
                except IndexError:
                    st.error("⚠️ Fehler beim Zugriff auf Kaloriendaten.")
            else:
                st.warning("⚠️ Keine Nährwerte für dieses Lebensmittel gefunden.")
        else:
            st.info("ℹ️ Bitte ein Lebensmittel auswählen.")

except FileNotFoundError:
    st.error("📁 Die Datei 'Ernaehrungsdaten.xlsx' wurde nicht gefunden.")
except Exception as e:
    st.error(f"🚨 Ein unerwarteter Fehler ist aufgetreten: {e}")

# 🔙 Zurück
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")
