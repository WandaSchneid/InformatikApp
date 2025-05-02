import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.login_manager import LoginManager
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit import switch_page
from utils.ui_utils import hide_sidebar

# --- Seitenkonfiguration ---
st.set_page_config(page_title="1_Ernaehrung", page_icon="🍎", layout="centered")

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

# --- Pyramid-Stufen ---
if st.button("🍫 Suesses"):
    switch_page("pages/ernaehrung_suesses.py")

if st.button("🧈 Fette"):
    switch_page("pages/ernaehrung_fette.py")

if st.button("🥩 Fleisch / Fisch"):
    switch_page("pages/ernaehrung_fleisch_fisch.py")

if st.button("🧀 Milchprodukte"):
    switch_page("pages/ernaehrung_milchprodukte.py")

if st.button("🍞 Getreide / Reis / Kartoffeln"):
    switch_page("pages/ernaehrung_getreide_reis_kartoffeln.py")

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

if "wasser_glaeser" not in st.session_state:
    st.session_state.wasser_glaeser = 0

st.session_state.wasser_glaeser = st.number_input(
    "Wie viele Glaeser Wasser hast du getrunken? (à 300ml)",
    min_value=0, step=1,
    value=st.session_state.wasser_glaeser,
    key="wasser_input"
)
st.write(f"Das sind **{st.session_state.wasser_glaeser * 300} ml Wasser**.")

if st.button("💾 Wasser speichern"):
    aktuelles_datum = datetime.now()
    monat = aktuelles_datum.month
    tag = aktuelles_datum.day
    wasser_ml = st.session_state.wasser_glaeser * 300

    speichern_tageseintrag(monat=monat, tag=tag, wasser_ml=wasser_ml)
    st.success(f"✅ {wasser_ml} ml Wasser gespeichert!")

    st.session_state.wasser_glaeser = 0
    st.experimental_rerun()

# --- Zurück zur Startseite ---
st.markdown("---")
if st.button("🔙 Zurueck zum Start"):
    switch_page("Start.py") 