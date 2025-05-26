import os
import sys
from datetime import datetime
import streamlit as st
from streamlit import switch_page
import base64

# --- Modulpfade erweitern ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.login_manager import LoginManager
from functions.speichern import speichern_tageseintrag
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

# --- Seitenkonfiguration ---
st.set_page_config(page_title="2_Bewegung", page_icon="🏃‍♂️", layout="wide")

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Bewegung.jpg"
img_base64 = get_base64_of_bin_file(img_path)

# --- CSS Styling: Hintergrund & Textfarben ---
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
        background: rgba(255,255,255,0.7);
        border-radius: 20px;
        padding: 2rem;
    }}
    h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #1a1a1a !important;
    }}
    .stTextInput > label, .stSelectbox > label, .stSlider > label {{
        color: #1a1a1a !important;
    }}
    .markdown-text-container p, .stMarkdown {{
        color: #333333;
        font-size: 18px;
    }}
    .stButton > button {{
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        display: block;
        margin: auto;
        color: white;
        background-color: #0077b6;
        border: none;
    }}
    .stButton > button:hover {{
        background-color: #023e8a;
    }}
    div[data-testid="stSlider"] {{
        background: #ffffff;
        border-radius: 10px;
        padding: 1.2em 1em 0.5em 1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ausblenden ---
hide_sidebar()

# --- Sportarten Dictionary ---
sportarten = {
    "Aerobic": 7.0, "Assault Air Bike": 13.0, "Badminton": 7.0, "Basketball": 8.0,
    "Crosstrainer, langsam": 6.0, "Crosstrainer, schnell": 9.0, "Croquet": 3.5, "Curling": 4.8,
    "Fahrrad": 6.5, "Inliner": 7.5, "Intervalltraining": 10.0, "Joggen, langsam": 8.0,
    "Joggen, schnell": 11.5, "Judo": 9.0, "Krafttraining": 6.0, "Laufen": 7.2,
    "Leichtathletik": 8.0, "Liegestuetze": 8.0, "Pilates": 4.0, "Radfahren": 6.5,
    "Reiten": 5.5, "Schwimmen": 9.5, "Seilspringen": 12.0, "Sit Ups": 5.0,
    "Spinning": 10.0, "Skifahren": 7.0, "Tanzen": 6.5, "Tennis": 8.3,
    "Tischtennis": 4.0, "Trampolin": 5.0, "Wandern": 5.5, "Walken": 4.5,
    "Wassergymnastik": 4.0, "Yoga": 3.0, "Zumba": 8.5
}

# --- Layout: Titel zentriert ---
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.markdown(
        """
        <div style="background-color:#fff; border-radius:16px; padding: 1em; text-align:center; margin-bottom:1em;">
            <h1 style="color:#1a1a1a; margin:0;">🏃‍♂️ Bewegung</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Layout für Eingaben ---
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.markdown("### 🏃‍♀️ Laufen (min)")
    laufen_min = st.slider("Laufen", 0, 110, step=5, key="laufen_slider")
    laufen_kcal = laufen_min * sportarten["Laufen"]

    st.markdown("### 🧘 Weitere Aktivitäten")
    sport_keys = list(sportarten.keys())

    sport1 = st.selectbox("1. Sportart", sport_keys, key="sport1")
    min1 = st.selectbox("Minuten 1. Sportart", range(0, 121, 5), key="min1")

    sport2 = st.selectbox("2. Sportart", sport_keys, key="sport2")
    min2 = st.selectbox("Minuten 2. Sportart", range(0, 121, 5), key="min2")

    sport1_kcal = min1 * sportarten[sport1]
    sport2_kcal = min2 * sportarten[sport2]
    total_kcal = laufen_kcal + sport1_kcal + sport2_kcal

    # Zusammenfassungstext
    bewegung_text = ", ".join(
        [f"Laufen {laufen_min}min"] if laufen_min > 0 else [] +
        [f"{sport1} {min1}min"] if min1 > 0 else [] +
        [f"{sport2} {min2}min"] if min2 > 0 else []
    )

    st.markdown(f"### 🔥 Gesamtverbrauch: **{total_kcal:.1f} kcal**")

    if st.button("💾 Bewegung speichern"):
        heute = datetime.now()
        speichern_tageseintrag(
            monat=heute.month,
            tag=heute.day,
            bewegung=bewegung_text,
            bewegung_kcal=total_kcal
        )
        DataManager().append_record(
            session_state_key='bewegung_df',
            record_dict={
                "datum": heute.strftime("%Y-%m-%d"),
                "bewegung": bewegung_text,
                "kcal": total_kcal,
                "timestamp": heute
            }
        )
        st.success("✅ Bewegung für heute gespeichert!")

    st.markdown("---")
    if st.button("🔙 Zurück zum Start"):
        switch_page("Start.py")
