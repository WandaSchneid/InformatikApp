import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.login_manager import LoginManager
from datetime import datetime
from functions.speichern import speichern_tageseintrag
from streamlit_extras.switch_page_button import switch_page
from utils.ui_utils import hide_sidebar

# --- Seitenkonfiguration ---
st.set_page_config(page_title="ernaehrung", page_icon="🍎", layout="centered")

# --- Sidebar ausblenden ---
hide_sidebar()

# --- Titel ---
st.title("🍎 Ernährung")
st.markdown("Wähle eine Kategorie aus der Ernährungspyramide:")

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
# Stufe 1 – Süsses
if st.button("🍫 Süsses"):
    switch_page("ernaehrung_suesses")

# Stufe 2 – Fette
if st.button("🧈 Fette"):
    switch_page("ernaehrung_fette")

# Stufe 3 – Fleisch/Fisch
if st.button("🥩 Fleisch / Fisch"):
    switch_page("ernaehrung_fleisch_fisch")

# Stufe 4 – Milchprodukte
if st.button("🧀 Milchprodukte"):
    switch_page("ernaehrung_milchprodukte")

# Stufe 5 – Getreide / Reis / Kartoffeln
if st.button("🍞 Getreide / Reis / Kartoffeln"):
    switch_page("ernaehrung_getreide_reis_kartoffeln")

# Stufe 6 – Gemüse & Obst
col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    if st.button("🥦 Gemüse"):
        switch_page("ernaehrung_gemuese")
with col3:
    if st.button("🍎 Obst"):
        switch_page("ernaehrung_obst")

# --- Wasser Abschnitt ---
st.markdown("---")
st.header("💧 Wasser")

if "wasser_glaeser" not in st.session_state:
    st.session_state.wasser_glaeser = 0

st.session_state.wasser_glaeser = st.number_input(
    "Wie viele Gläser Wasser hast du getrunken? (à 300ml)",
    min_value=0, step=1,
    value=st.session_state.wasser_glaeser,
    key="wasser_input"
)
st.write(f"Das sind **{st.session_state.wasser_glaeser * 300} ml Wasser**.")

# Speicher-Button für Wasser
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
if st.button("🔙 Zurück zum Start"):
    switch_page("start")