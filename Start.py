import streamlit as st

# ✅ Funktion für Button-Navigation via HTML Redirect
def go_to_page(page_name: str):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url=./{page_name}" />
    """, unsafe_allow_html=True)

# ✅ Seiteneinstellungen
st.set_page_config(page_title="Gesundheits-Tracker", page_icon="💪", layout="centered")

# Titel
st.title("💪 Gesundheits-Tracker")
st.markdown("Wähle einen Bereich aus:")

# CSS für größere, dickere Texte in runden Buttons
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 50px;
            padding: 20px 40px;
            font-size: 24px;  /* 👈 größer */
            font-weight: 800; /* 👈 dicker */
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
        go_to_page("Ernaehrung")

    if st.button("🏃 :orange[Bewegung]"):
        go_to_page("Bewegung")

    if st.button("🛌 :blue[Schlaf]"):
        go_to_page("Schlaf")