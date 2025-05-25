import streamlit as st
import pandas as pd 
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
from streamlit import switch_page
import base64

# --- Seitenkonfiguration ---
st.set_page_config(page_title="Start", page_icon="💪", layout="centered")

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Start.jpg"
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

# --- Seitenleiste verstecken ---
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialisierung DataManager + LoginManager ---
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Gesundheits-Tracker")
login_manager = LoginManager(data_manager=data_manager)

# --- Login-Schutz ---
if 'username' not in st.session_state:
    login_manager.login_register()
    st.stop()  # ⛔️ Stoppt den Seitenaufbau, bis Login erfolgt ist

# --- Daten laden nach Login ---
data_manager.load_user_data(session_state_key='data_df', file_name='data.csv', initial_value=pd.DataFrame())
data_manager.load_user_data(session_state_key='ernaehrung_df', file_name='ernaehrung.csv', initial_value=pd.DataFrame())
data_manager.load_user_data(session_state_key='bewegung_df', file_name='bewegung.csv', initial_value=pd.DataFrame())
data_manager.load_user_data(session_state_key='schlaf_df', file_name='schlaf.csv', initial_value=pd.DataFrame())

# --- Hauptbereich ---
st.title("💪 Gesundheits-Tracker")
st.markdown(f"Willkommen **{st.session_state['username']}**! Gib deine Ernaehrungs-, Bewegungs- und Schlafdaten des heutigen Tages ein:")

# --- Button-Styling ---
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

# --- Navigation ---
pages = [
    ("🍎 Ernaehrung", "pages/Ernaehrung.py"),
    ("🏃 Bewegung", "pages/Bewegung.py"),
    ("🛌 Schlaf", "pages/Schlaf.py"),
    ("📊 Daten", "pages/Daten.py"),
]

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    for label, page in pages:
        if st.button(label):
            switch_page(page)

# --- Logout-Button ---
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()