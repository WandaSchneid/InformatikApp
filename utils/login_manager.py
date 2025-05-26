import streamlit as st
import hashlib
import pandas as pd
import random
from utils.data_handler import DataHandler
from PIL import Image, ImageDraw, ImageFont
import io

class LoginManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.auth_credentials = self._load_auth_credentials()

    def _load_auth_credentials(self):
        self.data_manager.load_app_data(
            session_state_key='users',
            file_name='users.csv',
            initial_value=pd.DataFrame(columns=[
                'first_name', 'last_name', 'email', 'username',
                'password_hash', 'password_hint'
            ])
        )
        return st.session_state['users']

    def login_register(self):
        # ✅ Globales Styling inkl. Tabs
        st.markdown("""
        <style>
            body, .stApp {
                color: #1a1a1a !important;
            }
            h1, h2, h3, h4, h5, h6,
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #1a1a1a !important;
                font-weight: 700;
            }
            .stTextInput > label, .stSelectbox > label,
            .stForm label, .stRadio > label, .stCheckbox > label {
                color: #1a1a1a !important;
                font-weight: 500;
            }
            .stMarkdown, .markdown-text-container p {
                color: #333 !important;
                font-size: 17px;
            }
            .stAlert > div {
                color: #1a1a1a;
                font-size: 16px;
            }
            .stCaption {
                color: #444 !important;
                font-style: italic;
            }
            .stButton > button {
                background-color: #0077b6;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
            }
            .stButton > button:hover {
                background-color: #023e8a;
            }

            /* Tabs */
            div[data-testid="stTabs"] button {
                color: #1a1a1a !important;
                font-weight: 600;
                background-color: transparent;
            }
            div[data-testid="stTabs"] button[aria-selected="true"] {
                color: #1a1a1a !important;
                background-color: rgba(200, 200, 200, 0.2);
                border-bottom: 3px solid #1a1a1a;
            }

            /* Formular-Hintergrund und Text */
            div[data-testid="stForm"] {
                background-color: rgba(255,255,255,0.8);
                padding: 2rem;
                border-radius: 16px;
            }
            div[data-testid="stForm"] label,
            div[data-testid="stForm"] input,
            div[data-testid="stForm"] textarea {
                color: #1a1a1a !important;
            }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("🔐 Login / Registrierung")
        tabs = st.tabs(["🔑 Login", "🆕 Registrieren"])

        with tabs[0]:
            username = st.text_input("Benutzername", key="login_user")
            password = st.text_input("Passwort", type="password", key="login_pass")
            if st.button("Login"):
                self.login(username, password)

        with tabs[1]:
            self.register_user()

    def login(self, username, password):
        if not username or not password:
            st.warning("⚠️ Bitte Benutzername und Passwort eingeben.")
            return

        user_df = self.auth_credentials
        password_hash = self._hash_password(password)
        match = user_df[
            (user_df['username'] == username) &
            (user_df['password_hash'] == password_hash)
        ]

        if not match.empty:
            st.session_state['username'] = username
            st.success(f"✅ Willkommen {username}!")
            st.rerun()
        else:
            st.error("❌ Login fehlgeschlagen. Benutzername oder Passwort falsch.")

    def _generate_captcha_image(self, text):
        image = Image.new('RGB', (120, 40), color=(255, 255, 200))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, font=font, fill=(80, 20, 20))
        draw.line((0, 20, 120, 20), fill=(200, 200, 200), width=1)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def register_user(self):
        st.info("ℹ️ Passwort: 8–20 Zeichen, mit Groß-/Kleinbuchstaben, Zahl und Sonderzeichen @$!%*?&.")

        with st.form("register_form"):
            first_name = st.text_input("Vorname")
            last_name = st.text_input("Nachname")
            email = st.text_input("E-Mail")
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")
            repeat_password = st.text_input("Passwort wiederholen", type="password")
            password_hint = st.text_input("Passwort-Hinweis")

            if 'captcha' not in st.session_state:
                st.session_state['captcha'] = str(random.randint(1000, 9999))

            captcha_value = st.session_state['captcha']
            captcha_img = self._generate_captcha_image(captcha_value)
            st.image(captcha_img, width=150)

            captcha_input = st.text_input("Captcha eingeben")
            submit = st.form_submit_button("Registrieren")

        if submit:
            if not all([first_name, last_name, email, username, password, repeat_password, captcha_input]):
                st.warning("⚠️ Bitte alle Felder ausfüllen.")
                return

            if username in self.auth_credentials['username'].values:
                st.error("❌ Benutzername existiert bereits.")
                return

            if password != repeat_password:
                st.error("❌ Passwörter stimmen nicht überein.")
                return

            if not self._is_valid_password(password):
                st.error("❌ Passwort erfüllt nicht die Anforderungen.")
                return

            if captcha_input != st.session_state.get('captcha'):
                st.error("❌ Captcha ist falsch.")
                return

            password_hash = self._hash_password(password)
            new_user = pd.DataFrame([[first_name, last_name, email, username,
                                      password_hash, password_hint]],
                                    columns=[
                                        'first_name', 'last_name', 'email', 'username',
                                        'password_hash', 'password_hint'
                                    ])

            self.auth_credentials = pd.concat([self.auth_credentials, new_user], ignore_index=True)
            st.session_state['users'] = self.auth_credentials
            self.data_manager.save_data('users')
            st.success("✅ Registrierung erfolgreich! Bitte einloggen.")
            del st.session_state['captcha']

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _is_valid_password(password):
        import re
        return (
            8 <= len(password) <= 20 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[@$!%*?&]", password)
        )
