import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager
import base64

st.set_page_config(page_title="🍎 Fleisch / Fisch", page_icon="🥩", layout="centered")
hide_sidebar()

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Fleisch_Fisch.jpg"
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

# --- Titel zentriert mit weißem Hintergrund ---
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.markdown(
        """
        <div style="background-color:#fff; border-radius:16px; padding: 1em; text-align:center; margin-bottom:1em;">
            <h1 style="color:#222; margin:0;">🥩 Fleisch / Fisch</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

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

if "Bezugseinheit" in auswahl:
    st.caption(f"ℹ️ Bezugsbasis: {auswahl['Bezugseinheit']}")

st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("pages/Ernaehrung.py")