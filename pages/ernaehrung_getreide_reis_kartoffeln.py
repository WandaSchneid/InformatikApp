import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Getreide / Reis / Kartoffeln", page_icon="🍞")

st.title("🍞 Getreide / Reis / Kartoffeln")
st.write("Trage deine verzehrten Portionen ein.")

reis = st.number_input("Reis (g)", min_value=0, step=10)
brot = st.number_input("Brot (g)", min_value=0, step=10)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")