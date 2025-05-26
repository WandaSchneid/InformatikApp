import os
import sys
from datetime import datetime
import streamlit as st
from streamlit import switch_page
import base64

# --- Eigene Module importieren ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.login_manager import LoginManager
from functions.speichern import speichern_tageseintrag
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

# --- Seitenkonfiguration ---
st.set_page_config(page_title="🛋 Schlaf", page_icon="🛋", layout="centered")

# --- Hintergrundbild laden und umwandeln ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Schlaf.jpg"
img_base64 = get_base64_of_bin_file(img_path)

# --- CSS Styling für Text und Layout ---
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
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #1a1a1a !important;
    }}
    .markdown-text-container p, .stMarkdown,
    .stTextInput > label, .stSelectbox > label {{
        color: #333333 !important;
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
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ausblenden ---
hide_sidebar()

# --- Titel ---
st.title("🛋 Schlaf")

# --- Aktuelles Datum ---
heute = datetime.now()

# --- Eingaben ---
stunden_optionen = [1.5, 3, 4.5, 5, 6.5, 7, 8.5, 10, 11, 12]
stunden = st.selectbox("⏱️ Stunden geschlafen:", stunden_optionen, index=6)

bettzeit_eingabe = st.text_input("🕒 Zu Bett gegangen (Format: HH:MM)", value="22:00")

# --- Zeitvalidierung ---
try:
    stunde, minute = map(int, bettzeit_eingabe.strip().split(":"))
    if 0 <= stunde <= 23 and 0 <= minute <= 59:
        bettzeit = f"{stunde:02d}:{minute:02d}"
    else:
        bettzeit = "00:00"
        st.warning("⚠️ Bitte gültige Uhrzeit im Format HH:MM angeben (00:00 – 23:59).")
except:
    bettzeit = "00:00"
    st.warning("⚠️ Bitte Uhrzeit im Format HH:MM eingeben!")

qualitaets_optionen = [
    "gut, ausgeschlafen",
    "mittel, zu wenig geschlafen",
    "schlecht, unruhige Nacht"
]
qualitaet = st.selectbox("🌙 Schlafqualität:", qualitaets_optionen, index=0)

# --- Zusammenfassung ---
st.markdown("---")
st.markdown(f"""
### 📋 Zusammenfassung für heute ({heute.strftime('%d.%m.%Y')})
- **Geschlafen:** {stunden} Stunden  
- **Zu Bett gegangen:** {bettzeit} Uhr  
- **Schlafqualität:** *{qualitaet}*
""")

# --- Speichern ---
if st.button("💾 Schlaf speichern"):
    zusammenfassung = f"Geschlafen: {stunden}h, Zu Bett: {bettzeit} Uhr, Qualität: {qualitaet}"
    speichern_tageseintrag(
        monat=heute.month,
        tag=heute.day,
        schlaftext=zusammenfassung
    )
    DataManager().append_record(
        session_state_key='schlaf_df',
        record_dict={
            "datum": heute.strftime("%Y-%m-%d"),
            "stunden": stunden,
            "bettzeit": bettzeit,
            "qualitaet": qualitaet,
            "timestamp": datetime.now()
        }
    )
    st.success("✅ Schlafdaten gespeichert!")

# --- Zurück zur Startseite ---
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    switch_page("Start.py")
