import streamlit as st
import matplotlib.pyplot as plt
from functions.speichern import speichern_tageseintrag
from datetime import datetime  # Wichtig!

# Seitenkonfiguration
st.set_page_config(page_title="🛌 Schlaf", page_icon="🛌", layout="centered")
st.title("🛌 Schlaf")

# ✅ Funktion für Redirect zur Startseite
def go_to_start():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/" />
    """, unsafe_allow_html=True)

# -----------------------------------------------
# 📅 Wochentag-Auswahl mit Kuchendiagramm
# -----------------------------------------------
days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
selected_day = st.selectbox("Wochentag auswählen:", days, index=0)

fig, ax = plt.subplots()
wedges, texts = ax.pie([1]*7, labels=days, startangle=90,
    colors=["#b2ebf2" if d == selected_day else "#eeeeee" for d in days])
ax.axis("equal")
st.pyplot(fig)

# -----------------------------------------------
# 😴 Eingaben
# -----------------------------------------------
stunden_optionen = [1.5, 3, 4.5, 5, 6.5, 7, 8.5, 10, 11, 12]
stunden = st.selectbox("⏱️ Stunden geschlafen:", stunden_optionen, index=6)

# 🕙 Uhrzeit-Eingabe als Text
bettzeit_eingabe = st.text_input("🕙 Zu Bett gegangen (Format: HH:MM)", value="22:00")

# Eingabe validieren
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
### 📋 Zusammenfassung für **{selected_day}**  
- **Geschlafen:** {stunden} Stunden  
- **Zu Bett gegangen:** {bettzeit} Uhr  
- **Schlafqualität:** *{qualitaet}*
""")

# -----------------------------------------------
# 💾 Speichern-Button (mit Monat und Tag)
# -----------------------------------------------
if st.button("💾 Schlaf speichern"):
    aktueller_monat = datetime.now().month
    aktueller_tag = datetime.now().day
    speichern_tageseintrag(monat=aktueller_monat, tag=aktueller_tag, schlaftext=zusammenfassung)
    st.success("✅ Schlafdaten gespeichert!")

# -----------------------------------------------
# Zurück-Button zur Startseite
# -----------------------------------------------
if st.button("🔙 Zurück zum Start"):
    go_to_start()