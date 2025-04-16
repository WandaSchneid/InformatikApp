import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Daten", page_icon="📊")
st.title("📊 Daten")
st.write("Hier bekommst du eine Übersicht über deine Gesundheitsdaten.")

if st.button("🔙 Zurueck zum Start"):
    switch_page("start")