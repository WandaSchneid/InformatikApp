import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Fleisch / Fisch", page_icon="🥩")

st.title("🥩 Fleisch / Fisch")
st.write("Hier kannst du deine Fleisch- und Fischportionen eingeben.")

rind = st.number_input("Rind (g)", min_value=0, step=10)
poulet = st.number_input("Poulet (g)", min_value=0, step=10)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")