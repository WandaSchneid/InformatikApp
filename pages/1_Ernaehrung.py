import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.login_manager import LoginManager
from datetime import datetime
from functions.speichern import speichern_tageseintrag

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Ernaehrung", page_icon="🍎", layout="centered")

# --- Login-Überprüfung ---
if 'login' not in st.session_state:
    LoginManager().go_to_login('Start.py')

# 🔁 Funktion zum Seitenwechsel (Unterseiten)
def go_to_page(page_name: str):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url=./{page_name}" />
    """, unsafe_allow_html=True)

# ✅ Funktion zum Zurück zur Startseite (robust)
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/" />
    """, unsafe_allow_html=True)

# --- Titel ---
st.markdown("## 🍎 Ernährung")
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
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🍫 Süsses"):
        go_to_page("ernaehrung_suesses")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 2 – Fette
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🧈 Fette"):
        go_to_page("ernaehrung_fette")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 3 – Fleisch/Fisch
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🥩 Fleisch / Fisch"):
        go_to_page("ernaehrung_fleisch_fisch")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 4 – Milchprodukte
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🧀 Milchprodukte"):
        go_to_page("ernaehrung_milchprodukte")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 5 – Getreide / Reis / Kartoffeln
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🍞 Getreide / Reis / Kartoffeln"):
        go_to_page("ernaehrung_getreide_reis_kartoffeln")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 6 – Gemüse & Obst
col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    if st.button("🥦 Gemüse"):
        go_to_page("ernaehrung_gemuese")
with col3:
    if st.button("🍎 Obst"):
        go_to_page("ernaehrung_obst")

# --- Wasser Abschnitt ---
st.markdown("---")
st.markdown("## 💧 Wasser")

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
col_save = st.columns([1, 2, 1])[1]
with col_save:
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
    go_to_start()