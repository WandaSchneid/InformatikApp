import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Suesses", page_icon="🍫")

st.title("🍫 Süsses")
st.write("Erfasse deinen Konsum von Süssem.")

schokolade = st.number_input("Schokolade (g)", min_value=0, step=10)
guetzli = st.number_input("Guetzli (g)", min_value=0, step=10)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")