import streamlit as st
from utils.data_manager import DataManager
from utils.dual_data_manager import DualDataManager
from utils.login_manager import LoginManager
from streamlit_extras.switch_page_button import switch_page

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Gesundheits-Tracker", page_icon="💪", layout="centered")

# --- Initialisierung ---
local_data_manager = DataManager(fs_protocol='file', fs_root_folder="app_data")
data_manager = DualDataManager()
login_manager = LoginManager(data_manager=local_data_manager)
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

# --- Buttons für Navigation ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🍎 :green[Ernährung]"):
        switch_page("ernaehrung")  # <- exakt wie der Dateiname ohne ".py"

    if st.button("🏃 :orange[Bewegung]"):
        switch_page("bewegung")

    if st.button("🛌 :blue[Schlaf]"):
        switch_page("schlaf")

    if st.button("📊 :violet[Daten]"):
        switch_page("daten")