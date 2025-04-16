import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Ernaehrung", page_icon="🍎", layout="centered")

st.markdown("## 🍎 Ernährung")
st.markdown("Wähle eine Kategorie aus der Ernährungspyramide:")

# Button-Styling
st.markdown("""
    <style>
        .stButton > button {
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            display: block;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Pyramid-Stufen

# Stufe 1 – Süsses
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🍫 Süsses"):
        switch_page("suesses")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 2 – Fette
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🧈 Fette"):
        switch_page("fette")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 3 – Fleisch/Fisch
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🥩 Fleisch / Fisch"):
        switch_page("fleisch")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 4 – Milchprodukte
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🧀 Milchprodukte"):
        switch_page("milchprodukte")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 5 – Getreide
with st.container():
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🍞 Getreide / Reis / Kartoffeln"):
        switch_page("getreide")
    st.markdown("</div>", unsafe_allow_html=True)

# Stufe 6 – Gemüse & Obst nebeneinander
col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    if st.button("🥦 Gemüse"):
        switch_page("gemuese")
with col3:
    if st.button("🍎 Obst"):
        switch_page("obst")

# Wasser
st.markdown("---")
wasser = st.number_input("💧 Gläser Wasser (à 300ml)", min_value=0, step=1)
st.write(f"Das sind **{wasser * 300} ml Wasser**.")

if st.button("🔙 Zurück zum Start"):
    switch_page("start")