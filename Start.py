import streamlit as st

# Seitenkonfiguration
st.set_page_config(page_title="Gesundheits-Tracker", page_icon="💪", layout="centered")

# Benutzerdefinierte CSS für runde, farbige Buttons
st.markdown("""
    <style>
        .button-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            margin-top: 50px;
        }
        .runde-button {
            border: none;
            border-radius: 50px;
            padding: 20px 40px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            width: 250px;
            text-align: center;
            cursor: pointer;
        }
        .gruen { background-color: #4CAF50; }
        .orange { background-color: #FF9800; }
        .blau { background-color: #2196F3; }
    </style>
""", unsafe_allow_html=True)

# Seiteninhalte als Funktionen
def hauptseite():
    st.title("💪 Gesundheits-Tracker")
    st.markdown("Wähle einen Bereich aus:")

    # HTML-Buttons mit Form (wegen Streamlit)
    st.markdown("""
        <div class="button-container">
            <form action="?seite=ernaehrung" method="get">
                <button class="runde-button gruen" type="submit">🍎 Ernährung</button>
            </form>
            <form action="?seite=bewegung" method="get">
                <button class="runde-button orange" type="submit">🏃 Bewegung</button>
            </form>
            <form action="?seite=schlaf" method="get">
                <button class="runde-button blau" type="submit">🛌 Schlaf</button>
            </form>
        </div>
    """, unsafe_allow_html=True)

def ernaehrung_seite():
    st.title("🍎 Ernährung")
    st.write("Hier kannst du deine Mahlzeiten und Kalorien tracken.")
    if st.button("🔙 Zurück"):
        st.switch_page("main.py")

def bewegung_seite():
    st.title("🏃 Bewegung")
    st.write("Hier kannst du deine Aktivitäten erfassen.")
    if st.button("🔙 Zurück"):
        st.switch_page("main.py")

def schlaf_seite():
    st.title("🛌 Schlaf")
    st.write("Hier kannst du deinen Schlaf dokumentieren.")
    if st.button("🔙 Zurück"):
        st.switch_page("main.py")

# Navigation über URL-Parameter
seite = st.query_params.get("seite", "haupt")

if seite == "haupt":
    hauptseite()
elif seite == "ernaehrung":
    ernaehrung_seite()
elif seite == "bewegung":
    bewegung_seite()
elif seite == "schlaf":
    schlaf_seite()