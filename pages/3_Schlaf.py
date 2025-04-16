import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Schlaf", page_icon="🛌")
st.title("🛌 Schlaf")
st.write("Hier kannst du deinen Schlaf dokumentieren.")

if st.button("🔙 Zurueck zum Start"):
    switch_page("start")