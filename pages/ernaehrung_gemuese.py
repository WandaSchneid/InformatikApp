import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Gemuese", page_icon="🥦")

st.title("🥦 Gemuese")
st.write("Hier kannst du deine Gemüsemengen erfassen.")

karotten = st.number_input("Karotten (g)", min_value=0, step=10)
brokkoli = st.number_input("Brokkoli (g)", min_value=0, step=10)

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")