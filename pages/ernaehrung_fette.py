import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Fette", page_icon="🧈")

st.title("🧈 Fette")
st.write("Gib hier die konsumierte Fettmenge ein.")

butter = st.number_input("Butter (g)", min_value=0, step=5)
oel = st.number_input("Öl (ml)", min_value=0, step=5)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")