import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# --- GESUNDHEITS-TRACKER ---
st.set_page_config(page_title="Gesundheits-Tracker", page_icon="💪", layout="centered")

# --- LOGIN ---
data_manager = DataManager(fs_protocol='file', fs_root_folder="app_data")
login_manager = LoginManager(data_manager)
login_manager.login_register()

st.title("💪 Gesundheits-Tracker")
st.markdown("Wähle einen Bereich aus:")

# CSS für größere, dickere Texte in runden Buttons
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

# Zentrierte Buttons mit farbigem Text
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🍎 :green[Ernaehrung]"):
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=./Ernaehrung" />
        """, unsafe_allow_html=True)

    if st.button("🏃 :orange[Bewegung]"):
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=./Bewegung" />
        """, unsafe_allow_html=True)

    if st.button("📌 :blue[Schlaf]"):
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=./Schlaf" />
        """, unsafe_allow_html=True)