import streamlit as st
from utils.data_manager import DataManager  # Lokaler Manager für Login
from utils.dual_data_manager import DualDataManager  # Dualer Manager für Userdaten
from utils.login_manager import LoginManager
from streamlit_extras.switch_page_button import switch_page  # für echte Navigation

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Gesundheits-Tracker", page_icon="💪", layout="centered")

# --- Initialisierung ---
# Lokaler Manager NUR für Login
local_data_manager = DataManager(fs_protocol='file', fs_root_folder="app_data")

# DualManager für User-Daten
data_manager = DualDataManager()

# LoginManager bekommt den lokalen DataManager
login_manager = LoginManager(data_manager=local_data_manager)

# Login/Register
login_manager.login_register()

# --- Hauptbereich ---
st.title("💪 Gesundheits-Tracker")
st.markdown("Wähle einen Bereich aus:")

# Button Styling
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 50px;
            padding: 20px 40px;
            font-size: 24px;
            font-weight: 800;
            width: 280px;
            text-align: center;
            display: block;
            margin: 15px auto;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🍎 :green[Ernährung]"):
        switch_page("ernaehrung")   # Kein "1_" mehr!

    if st.button("🏃 :orange[Bewegung]"):
        switch_page("bewegung")

    if st.button("🛌 :blue[Schlaf]"):
        switch_page("schlaf")

    if st.button("📊 :violet[Daten]"):
        switch_page("daten")