import streamlit as st
from utils.data_manager import DataManager

class DualDataManager:
    """
    Verwaltet sowohl lokalen als auch WebDAV-basierten DataManager und wählt je nach Verfügbarkeit.
    """

    def __init__(self, fs_root_folder="Gesundheits-Tracker"):
        self.local = DataManager(fs_protocol='file', fs_root_folder=fs_root_folder)

        if 'webdav' in st.secrets:
            self.remote = DataManager(fs_protocol='webdav', fs_root_folder=fs_root_folder)
            self.use_remote = True
        else:
            self.remote = None
            self.use_remote = False

    def _active(self):
        return self.remote if self.use_remote and self.remote else self.local

    def load_app_data(self, *args, **kwargs):
        return self._active().load_app_data(*args, **kwargs)

    def load_user_data(self, *args, **kwargs):
        return self._active().load_user_data(*args, **kwargs)

    def save_data(self, *args, **kwargs):
        return self._active().save_data(*args, **kwargs)

    def save_all_data(self, *args, **kwargs):
        return self._active().save_all_data(*args, **kwargs)

    def append_record(self, *args, **kwargs):
        return self._active().append_record(*args, **kwargs)

    @property
    def data_reg(self):
        return self._active().data_reg
