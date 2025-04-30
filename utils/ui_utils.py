# utils/ui_utils.py
import streamlit as st

def hide_sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="stSidebarCollapsedControl"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)