from utils.data_manager import DataManager
import pandas as pd
import streamlit as st

class DualDataManager:
    """
    DualDataManager speichert und lädt Daten sowohl lokal als auch auf SwitchDrive (WebDAV).
    
    - Beim Laden: zuerst lokal versuchen, dann SwitchDrive
    - Beim Speichern: immer lokal UND auf SwitchDrive sichern
    """

    def __init__(self):
        self.local_manager = DataManager(fs_protocol='file', fs_root_folder='data')
        self.remote_manager = DataManager(fs_protocol='webdav', fs_root_folder='app_data')

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        """
        Versucht zuerst lokal zu laden. Falls nicht vorhanden, von SwitchDrive.
        """
        if session_state_key in st.session_state:
            return

        try:
            self.local_manager.load_user_data(session_state_key, file_name, initial_value=initial_value, **load_args)
        except Exception:
            # Lokales Laden fehlgeschlagen -> SwitchDrive probieren
            self.remote_manager.load_user_data(session_state_key, file_name, initial_value=initial_value, **load_args)

    def save_data(self, session_state_key):
        """
        Speichert immer lokal UND auf SwitchDrive.
        """
        self.local_manager.save_data(session_state_key)
        self.remote_manager.save_data(session_state_key)

    def append_record(self, session_state_key, record_dict):
        """
        Fügt Datensatz an und speichert danach.
        """
        data_value = st.session_state.get(session_state_key, None)

        if data_value is None:
            raise ValueError(f"DualDataManager: Kein Wert für {session_state_key} im Session-State gefunden!")

        if not isinstance(record_dict, dict):
            raise ValueError("DualDataManager: Record muss ein Dictionary sein.")

        if isinstance(data_value, pd.DataFrame):
            data_value = pd.concat([data_value, pd.DataFrame([record_dict])], ignore_index=True)
        elif isinstance(data_value, list):
            data_value.append(record_dict)
        else:
            raise ValueError("DualDataManager: Nur DataFrame oder Liste werden unterstützt.")

        st.session_state[session_state_key] = data_value

        # Nach Anhängen: auf beiden Speichern
        self.save_data(session_state_key)
