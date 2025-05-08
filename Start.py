import streamlit as st
import pandas as pd 
from utils.data_manager import DataManager
from utils.dual_data_manager import DualDataManager
from utils.login_manager import LoginManager
from streamlit import switch_page

# Initialisieren des Data Managers
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Gesundheits-Tracker") 

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Start", page_icon="💪", layout="centered")

# --- Seitenleiste verstecken ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialisierung ---
local_data_manager = DataManager(fs_protocol='file', fs_root_folder="app_data")
data_manager = DualDataManager()
login_manager = LoginManager(data_manager=local_data_manager)
login_manager.login_register()

# Laden der Daten aus dem persistenten Speicher in den Session-State
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value=pd.DataFrame()
)

# --- Hauptbereich ---
st.title("💪 Gesundheits-Tracker")
st.markdown("Wähle einen Bereich aus:")

# --- Button Styling ---
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

# --- Buttons für Navigation ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🍎 Ernaehrung"):
        switch_page("pages/Ernaehrung.py")

    if st.button("🏃 Bewegung"):
        switch_page("pages/Bewegung.py")

    if st.button("🛌 Schlaf"):
        switch_page("pages/Schlaf.py")

    if st.button("📊 Daten"):
        switch_page("pages/Daten.py")