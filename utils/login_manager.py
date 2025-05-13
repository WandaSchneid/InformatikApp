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
        st.subheader("Login / Registrierung")
        tabs = st.tabs(["Login", "Registrieren"])

        with tabs[0]:
            username = st.text_input("Benutzername", key="login_user")
            password = st.text_input("Passwort", type="password", key="login_pass")
            if st.button("Login"):
                self.login(username, password)

        with tabs[1]:
            self.register_user()

    def login(self, username, password):
        if not username or not password:
            st.warning("Bitte Benutzername und Passwort eingeben.")
            return

        user_df = self.auth_credentials
        password_hash = self._hash_password(password)
        match = user_df[(user_df['username'] == username) & (user_df['password_hash'] == password_hash)]

        if not match.empty:
            st.session_state['username'] = username
            st.success(f"Willkommen {username}!")
        else:
            st.error("Login fehlgeschlagen. Benutzername oder Passwort falsch.")

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
        st.info("The password must be 8–20 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character from @$!%*?&.")

        with st.form("register_form"):
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            email = st.text_input("Email")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            repeat_password = st.text_input("Repeat password", type="password")
            password_hint = st.text_input("Password hint")

            if 'captcha' not in st.session_state:
                st.session_state['captcha'] = str(random.randint(1000, 9999))

            captcha_value = st.session_state['captcha']
            captcha_img = self._generate_captcha_image(captcha_value)
            st.image(captcha_img, width=150)

            captcha_input = st.text_input("Captcha")
            submit = st.form_submit_button("Registrieren")

        if submit:
            if not all([first_name, last_name, email, username, password, repeat_password, captcha_input]):
                st.warning("Bitte alle Felder ausfüllen.")
                return

            if username in self.auth_credentials['username'].values:
                st.error("Benutzername existiert bereits.")
                return

            if password != repeat_password:
                st.error("Passwörter stimmen nicht überein.")
                return

            if not self._is_valid_password(password):
                st.error("Passwort erfüllt nicht die Anforderungen.")
                return

            if captcha_input != st.session_state.get('captcha'):
                st.error("Captcha ist falsch.")
                return

            password_hash = self._hash_password(password)
            new_user = pd.DataFrame([[
                first_name, last_name, email, username,
                password_hash, password_hint
            ]], columns=[
                'first_name', 'last_name', 'email', 'username',
                'password_hash', 'password_hint'
            ])

            self.auth_credentials = pd.concat([self.auth_credentials, new_user], ignore_index=True)
            st.session_state['users'] = self.auth_credentials
            self.data_manager.save_data('users')
            st.success("Registrierung erfolgreich! Bitte einloggen.")
            del st.session_state['captcha']  # captcha zurücksetzen

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _is_valid_password(password):
        import re
        if 8 <= len(password) <= 20 and \
            re.search(r"[A-Z]", password) and \
            re.search(r"[a-z]", password) and \
            re.search(r"[0-9]", password) and \
            re.search(r"[@$!%*?&]", password):
            return True
        return False