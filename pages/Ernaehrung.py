import sys
import os
import pandas as pd
from datetime import datetime
import streamlit as st
from streamlit import switch_page

# Eigene Module importieren
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.login_manager import LoginManager
from functions.speichern import speichern_tageseintrag
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

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

# --- Ernährungspyramide Buttons ---
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

# Session-State initialisieren
if "wasser_input" not in st.session_state:
    st.session_state["wasser_input"] = 0

# Wassermenge eingeben
anzahl_glaeser = st.number_input(
    "Wie viele Glaeser Wasser hast du getrunken? (à 300ml)",
    min_value=0,
    step=1,
    key="wasser_input"
)

# Anzeige der Menge
st.write(f"Das sind **{anzahl_glaeser * 300} ml Wasser**.")

# Speichern-Button
if st.button("💾 Wasser speichern"):
    wasser_ml = anzahl_glaeser * 300
    aktuelles_datum = datetime.now()

    speichern_tageseintrag(monat=aktuelles_datum.month, tag=aktuelles_datum.day, wasser_ml=wasser_ml)

    st.success(f"✅ {wasser_ml} ml Wasser gespeichert!")

    # Umleitung zurück auf dieselbe Seite (Seite neuladen)
    switch_page("pages/Ernaehrung.py")

# --- Zurück zur Startseite ---
st.markdown("---")
if st.button("🔙 Zurueck zum Start"):
    switch_page("Start.py")