import sys
import os
import pandas as pd
from datetime import datetime
import streamlit as st
from streamlit import switch_page
import base64

# Eigene Module importieren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.login_manager import LoginManager
from functions.speichern import speichern_tageseintrag
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

# --- Seitenkonfiguration ---
st.set_page_config(page_title="1_Ernaehrung", page_icon="🍎", layout="centered")

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Ernaehrung.jpg"
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

# --- Sidebar ausblenden ---
hide_sidebar()
                                                        
# --- Titel ---
st.title("🍎 Ernaehrung")
st.markdown("Wähle eine Kategorie aus der Ernaehrungspyramide:")

# --- Button-Styling ---
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            display: block;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# --- Ernährungspyramide Buttons ---
ernaehrung_buttons = [
    ("🍫 Suesses", "pages/ernaehrung_suesses.py"),
    ("🧈 Fette", "pages/ernaehrung_fette.py"),
    ("🥩 Fleisch / Fisch", "pages/ernaehrung_fleisch_fisch.py"),
    ("🧀 Milchprodukte", "pages/ernaehrung_milchprodukte.py"),
    ("🍞 Getreide / Reis / Kartoffeln", "pages/ernaehrung_getreide_reis_kartoffeln.py"),
]
for label, page in ernaehrung_buttons:
    if st.button(label):
        switch_page(page)

col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    if st.button("🥦 Gemuese"):
        switch_page("pages/ernaehrung_gemuese.py")
with col3:
    if st.button("🍎 Obst"):
        switch_page("pages/ernaehrung_obst.py")

# --- Wasser Abschnitt ---
st.markdown("---")
st.header("💧 Wasser")

if "wasser_input" not in st.session_state:
    st.session_state["wasser_input"] = 0

anzahl_glaeser = st.number_input(
    "Wie viele Glaeser Wasser hast du getrunken? (à 300ml)",
    min_value=0,
    step=1,
    key="wasser_input"
)

wasser_ml = anzahl_glaeser * 300
st.write(f"Das sind **{wasser_ml} ml Wasser**.")

# Speichern-Button
if st.button("💾 Wasser speichern"):
    aktuelles_datum = datetime.now()
    speichern_tageseintrag(
        monat=aktuelles_datum.month,
        tag=aktuelles_datum.day,
        wasser_ml=wasser_ml
    )
    DataManager().append_record(
        session_state_key='ernaehrung_df',
        record_dict={
            "datum": aktuelles_datum.strftime("%Y-%m-%d"),
            "anzahl_glaeser": anzahl_glaeser,
            "wasser_ml": wasser_ml
        }
    )
    st.success(f"✅ {anzahl_glaeser} Gläser ({wasser_ml} ml) Wasser gespeichert!")

st.markdown("---")
if st.button("🔙 Zurueck zum Start"):
    switch_page("Start.py")