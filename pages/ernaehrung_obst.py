import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Obst", page_icon="🍎")

st.title("🍎 Obst")
st.write("Trage hier ein, wie viel Obst du gegessen hast.")

apfel = st.number_input("Apfel (g)", min_value=0, step=10)
banane = st.number_input("Banane (g)", min_value=0, step=10)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")