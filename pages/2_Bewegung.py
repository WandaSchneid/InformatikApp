import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Bewegung", page_icon="🏃")
st.title("🏃 Bewegung")
st.write("Hier kannst du deine sportlichen Aktivitäten erfassen.")

if st.button("🔙 Zurueck zum Start"):
    switch_page("start")