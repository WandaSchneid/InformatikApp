import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager
import base64

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🍫 Süßes", page_icon="🍫", layout="centered")
hide_sidebar()

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Suesses.jpg"
img_base64 = get_base64_of_bin_file(img_path)

st.markdown(
    f"""
    <style>
    body {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    .stApp {{
        background: transparent;
    }}
    .block-container {{
        background: rgba(255,255,255,0.7); /* halbtransparentes Weiß */
        border-radius: 20px;
        padding: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍫 Süßes")
st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")

# 📄 Excel laden
try:
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
            try:
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
                    DataManager().append_record(
                        session_state_key='ernaehrung_df',
                        record_dict={
                            "datum": heute.strftime("%Y-%m-%d"),
                            "lebensmittel": food_selection,
                            "menge": gram_input,
                            "kcal": kcal_total,
                            "kcal_pro_100g": kcal_pro_100g,
                            "timestamp": heute
                        }
                    )
                    st.success(f"✅ {gram_input}g {food_selection} mit {kcal_total:.2f} kcal gespeichert!")
            except IndexError:
                st.error("⚠️ Fehler beim Zugriff auf Kalorienwert – bitte Auswahl prüfen.")
        else:
            st.warning("⚠️ Keine Nährwerte für dieses Lebensmittel gefunden.")

except FileNotFoundError:
    st.error("📁 Die Datei 'Ernaehrungsdaten.xlsx' wurde nicht gefunden.")
except Exception as e:
    st.error(f"🚨 Unerwarteter Fehler: {e}")

# 🔙 Zurück
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")