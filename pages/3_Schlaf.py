import streamlit as st
from functions.speichern import speichern_tageseintrag
from datetime import datetime

# Seitenkonfiguration
st.set_page_config(page_title="🛋 Schlaf", page_icon="🛋", layout="centered")
st.title("🛋 Schlaf")

# ✅ Funktion für Redirect zur Startseite
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/" />
    """, unsafe_allow_html=True)

# -----------------------------------------------
# 📅 Aktueller Tag (automatisch)
# -----------------------------------------------
heute = datetime.now()
aktueller_tag = heute.strftime("%A")

# -----------------------------------------------
# 🛌 Eingaben
# -----------------------------------------------
stunden_optionen = [1.5, 3, 4.5, 5, 6.5, 7, 8.5, 10, 11, 12]
stunden = st.selectbox("⏱️ Stunden geschlafen:", stunden_optionen, index=6)

# 🕒 Uhrzeit-Eingabe als Text
bettzeit_eingabe = st.text_input("🕒 Zu Bett gegangen (Format: HH:MM)", value="22:00")

try:
    stunde, minute = map(int, bettzeit_eingabe.split(":"))
    bettzeit = f"{stunde:02d}:{minute:02d}"
except:
    bettzeit = "00:00"
    st.warning("⚠️ Bitte Uhrzeit im Format HH:MM eingeben!")

# Schlafqualität
qualitaets_optionen = [
    "gut, ausgeschlafen",
    "mittel, zu wenig geschlafen",
    "schlecht, unruhige Nacht"
]
qualitaet = st.selectbox("🌙 Schlafqualität:", qualitaets_optionen, index=0)

# -----------------------------------------------
# Ergebnis
# -----------------------------------------------
zusammenfassung = f"Geschlafen: {stunden}h, Zu Bett: {bettzeit} Uhr, Qualität: {qualitaet}"

st.markdown("---")
st.markdown(f"""
### 📋 Zusammenfassung für heute ({heute.strftime('%d.%m.%Y')})  
- **Geschlafen:** {stunden} Stunden  
- **Zu Bett gegangen:** {bettzeit} Uhr  
- **Schlafqualität:** *{qualitaet}*
""")

# -----------------------------------------------
# 💾 Speichern-Button
# -----------------------------------------------
if st.button("💾 Schlaf speichern"):
    speichern_tageseintrag(monat=heute.month, tag=heute.day, schlaftext=zusammenfassung)
    st.success("✅ Schlafdaten gespeichert!")

# -----------------------------------------------
# 🔙 Zurück zur Startseite
# -----------------------------------------------
if st.button("🔙 Zurück zum Start"):
    go_to_start()