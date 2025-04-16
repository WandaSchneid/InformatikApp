import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Milchprodukte", page_icon="🧀")

st.title("🧀 Milchprodukte")
st.write("Erfasse deine konsumierten Milchprodukte.")

milch = st.number_input("Milch (ml)", min_value=0, step=50)
joghurt = st.number_input("Joghurt (g)", min_value=0, step=50)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")