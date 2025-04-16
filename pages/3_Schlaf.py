import streamlit as st
import matplotlib.pyplot as plt
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="🛌 Schlaf", page_icon="🛌", layout="centered")
st.title("🛌 Schlaf")

# -----------------------------------------------
# 📅 Wochentag-Auswahl mit Kuchendiagramm
# -----------------------------------------------
days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
selected_day = st.selectbox("Wochentag auswählen", days, index=0)

fig, ax = plt.subplots()
wedges, texts = ax.pie([1]*7, labels=days, startangle=90,
    colors=["#b2ebf2" if d == selected_day else "#eeeeee" for d in days])
ax.axis("equal")
st.pyplot(fig)

# -----------------------------------------------
# 😴 Eingaben
# -----------------------------------------------

# Stunden geschlafen: Dropdown mit festen Werten
stunden_optionen = [1.5, 3, 4.5, 5, 6.5, 7, 8.5, 10, 11, 12]
stunden = st.selectbox("⏱️ Stunden geschlafen:", stunden_optionen, index=6)

# Schlafenszeit
stunde = st.selectbox("🕙 Zu Bett gegangen um (Stunde):", list(range(18, 25)) + list(range(0, 6)), index=3)
minute = st.selectbox("⏱️ Minute:", [0, 15, 30, 45], index=0)
bettzeit = f"{stunde:02d}:{minute:02d}"

# Schlafqualität wie gezeichnet
qualitaets_optionen = [
    "gut, ausgeschlafen",
    "mittel, zu wenig geschlafen",
    "schlecht, unruhige Nacht"
]
qualitaet = st.selectbox("🌙 Schlafqualität:", qualitaets_optionen, index=0)

# -----------------------------------------------
# Ergebnis
# -----------------------------------------------
st.markdown("---")
st.markdown(f"""
### 📋 Zusammenfassung für **{selected_day}**  
- **Geschlafen:** {stunden} Stunden  
- **Zu Bett gegangen:** {bettzeit} Uhr  
- **Schlafqualität:** *{qualitaet}*
""")

if st.button("🔙 Zurück zum Start"):
    switch_page("start")