import fsspec, posixpath
import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler

class DataManager:
    def __new__(cls, *args, **kwargs):
        if 'data_manager' in st.session_state:
            return st.session_state.data_manager
        else:
            instance = super(DataManager, cls).__new__(cls)
            st.session_state.data_manager = instance
            return instance

    def __init__(self, fs_protocol='file', fs_root_folder='app_data'):
        if hasattr(self, 'fs'):
            return

        self.fs_root_folder = fs_root_folder
        self.fs = self._init_filesystem(fs_protocol)
        self.app_data_reg = {}
        self.user_data_reg = {}

    def _init_filesystem(self, protocol: str):
        if protocol == 'webdav':
            if 'webdav' not in st.secrets:
                st.error("WebDAV-Zugangsdaten fehlen in den Streamlit-Secrets.")
                st.stop()

            secrets = st.secrets['webdav']
            base_url = secrets.get('base_url')
            username = secrets.get('username')
            password = secrets.get('password')

            if not base_url or not username or not password:
                st.error("Fehler: WebDAV-Zugangsdaten sind unvollständig.")
                st.stop()

            return fsspec.filesystem('webdav', base_url=base_url, auth=(username, password))

        elif protocol == 'file':
            return fsspec.filesystem('file')

        else:
            raise ValueError(f"DataManager: Invalid filesystem protocol: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        if subfolder is None:
            return DataHandler(self.fs, self.fs_root_folder)
        else:
            return DataHandler(self.fs, posixpath.join(self.fs_root_folder, subfolder))

    def load_app_data(self, session_state_key, file_name, initial_value=None, **load_args):
        if session_state_key in st.session_state:
            return

        dh = self._get_data_handler()
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.app_data_reg[session_state_key] = file_name

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        username = st.session_state.get('username', None)
        if username is None:
            for key in self.user_data_reg:
                st.session_state.pop(key, None)
            self.user_data_reg = {}
            return

        elif session_state_key in st.session_state:
            return

        user_data_folder = 'user_data_' + username
        dh = self._get_data_handler(user_data_folder)
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.user_data_reg[session_state_key] = dh.join(user_data_folder, file_name)

    @property
    def data_reg(self):
        return {**self.app_data_reg, **self.user_data_reg}

    def save_data(self, session_state_key):
        if session_state_key not in self.data_reg:
            raise ValueError(f"DataManager: No data registered for session state key {session_state_key}")

        if session_state_key not in st.session_state:
            raise ValueError(f"DataManager: Key {session_state_key} not found in session state")

        dh = self._get_data_handler()
        dh.save(self.data_reg[session_state_key], st.session_state[session_state_key])

    def save_all_data(self):
        keys = [key for key in self.data_reg.keys() if key in st.session_state]
        for key in keys:
            self.save_data(key)

    def append_record(self, session_state_key, record_dict):
        data_value = st.session_state.get(session_state_key)

        if data_value is None:
            raise ValueError(f"DataManager: Key {session_state_key} not found in session state")

        if not isinstance(record_dict, dict):
            raise ValueError(f"DataManager: The record_dict must be a dictionary")

        if isinstance(data_value, pd.DataFrame):
            data_value = pd.concat([data_value, pd.DataFrame([record_dict])], ignore_index=True)
        elif isinstance(data_value, list):
            data_value.append(record_dict)
        else:
            raise ValueError(f"DataManager: The session state value for key {session_state_key} must be a DataFrame or a list")

        st.session_state[session_state_key] = data_value
        self.save_data(session_state_key)
