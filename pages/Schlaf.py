import os
import sys
from datetime import datetime
import streamlit as st
from streamlit import switch_page

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.login_manager import LoginManager
from functions.speichern import speichern_tageseintrag
from utils.ui_utils import hide_sidebar
from utils.data_manager import DataManager

# --- Seitenkonfiguration ---
st.set_page_config(page_title="🛋 Schlaf", page_icon="🛋", layout="centered")

# --- Sidebar ausblenden ---
hide_sidebar()

# --- Titel ---
st.title("🛋 Schlaf")

# --- Aktueller Tag ---
heute = datetime.now()

# --- Eingaben ---
stunden_optionen = [1.5, 3, 4.5, 5, 6.5, 7, 8.5, 10, 11, 12]
stunden = st.selectbox("⏱️ Stunden geschlafen:", stunden_optionen, index=6)

bettzeit_eingabe = st.text_input("🕒 Zu Bett gegangen (Format: HH:MM)", value="22:00")
try:
    stunde, minute = map(int, bettzeit_eingabe.split(":"))
    bettzeit = f"{stunde:02d}:{minute:02d}"
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

# --- Speichern-Button ---
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