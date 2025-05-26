import sys
import os
import base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.login_manager import LoginManager
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
from functions.speichern import speichern_tageseintrag, speichern_profil, laden_profil
from streamlit import switch_page
from utils.ui_utils import hide_sidebar

# --- Seitenkonfiguration ---
st.set_page_config(page_title="📊 Daten", page_icon="📊", layout="centered")
hide_sidebar()

# --- Hintergrundbild einfügen ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "docs/images/Daten.jpg"
img_base64 = get_base64_of_bin_file(img_path)

# --- Styling ---
st.markdown(
    f"""
    <style>
    body {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    .stApp {{
        background: transparent;
    }}
    .block-container {{
        background: rgba(255,255,255,0.7);
        border-radius: 20px;
        padding: 2rem;
    }}
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #1a1a1a !important;
        font-weight: 700;
    }}
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stMarkdown, .markdown-text-container p {{
        color: #1a1a1a !important;
        font-size: 17px;
    }}
    .stButton > button {{
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        display: block;
        margin: auto;
        color: white;
        background-color: #0077b6;
        border: none;
    }}
    .stButton > button:hover {{
        background-color: #023e8a;
    }}
    .stCaption, .stDataFrame, .stAlert > div {{
        color: #1a1a1a !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Titel ---
st.title("📊 Datenübersicht")

# --- Hilfsfunktion ---
def get_profil_value(profil, key, default):
    if profil is not None and not profil.empty and key in profil:
        return profil.get(key, default)
    return default

# --- Daten einlesen ---
pfad_eintraege = "data/eintraege.csv"
if os.path.exists(pfad_eintraege) and os.path.getsize(pfad_eintraege) > 0:
    df_eintraege = pd.read_csv(pfad_eintraege)
    if "wasser_ml" not in df_eintraege.columns:
        df_eintraege["wasser_ml"] = 0
else:
    df_eintraege = pd.DataFrame(columns=[
        "monat", "tag", "lebensmittel", "menge", "kcal",
        "bewegung", "bewegung_kcal", "schlaf_zusammenfassung", "wasser_ml"
    ])

profil = laden_profil()

# --- Profil ---
st.markdown("## 👤 Profil")

name = st.text_input("Name:", value=get_profil_value(profil, "Name", ""))
alter = st.number_input("Alter:", min_value=0, max_value=120, step=1,
                        value=int(get_profil_value(profil, "Alter", 0)))
gewicht = st.number_input("Gewicht (kg):", min_value=0.0, step=0.1,
                          value=float(get_profil_value(profil, "Gewicht", 0.0)))
geschlecht = st.selectbox("Geschlecht:", ["Weiblich", "Männlich", "Divers"],
                          index=["Weiblich", "Männlich", "Divers"].index(get_profil_value(profil, "Geschlecht", "Weiblich")))

# --- Ziele ---
st.markdown("## 🎯 Ziele")
ziele_liste = [
    "Mehr Schlafen", "Mehr kcal verbrauchen", "Mehr Gemüse essen",
    "Früher zu Bett gehen", "Längere Spaziergänge", "Mehr Wasser trinken"
]
ziel1 = st.selectbox("1. Ziel:", ziele_liste, index=ziele_liste.index(get_profil_value(profil, "Ziel1", ziele_liste[0])))
ziel2 = st.selectbox("2. Ziel:", ziele_liste, index=ziele_liste.index(get_profil_value(profil, "Ziel2", ziele_liste[1])))

if st.button("💾 Profil & Ziele speichern"):
    speichern_profil(name, alter, gewicht, geschlecht, ziel1, ziel2)
    st.success("✅ Profil und Ziele gespeichert!")

# --- Monat und Tag auswählen ---
st.markdown("## 📅 Monat und Eingabetage auswählen")

monatsnamen = [calendar.month_name[i] for i in range(1, 13)]
aktueller_monat = datetime.now().month
aktueller_tag = datetime.now().day

monat_name_anzeige = st.selectbox("📅 Monat:", monatsnamen, index=aktueller_monat-1)
monat_auswahl = monatsnamen.index(monat_name_anzeige) + 1

selected_day = aktueller_tag

# --- Tagesbuttons ---
st.markdown("### 🗓️ Tage:")
with st.container():
    cols = st.columns(7)
    for i in range(1, 32):
        if i % 7 == 1:
            cols = st.columns(7)

        tag_data = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == i)]
        icon = "🟢" if not tag_data.empty else "🔵"

        button_label = f"{icon} {i}"
        if i == aktueller_tag and monat_auswahl == aktueller_monat:
            button_label = f"⭐ {i}"

        if cols[(i - 1) % 7].button(button_label, key=f"tag_{i}"):
            selected_day = i

st.markdown("""
<br>**Legende:**  
🟢 = Eintrag vorhanden  
🔵 = Kein Eintrag  
⭐ = Heute
""", unsafe_allow_html=True)

# --- Tagesdaten anzeigen ---
if selected_day:
    st.markdown(f"## 📝 Eingaben für Tag {selected_day}")
    df_tag = df_eintraege[(df_eintraege["monat"] == monat_auswahl) & (df_eintraege["tag"] == selected_day)]

    if df_tag.empty:
        st.info("Keine Daten für diesen Tag.")
    else:
        df_tag_display = df_tag.copy()
        if "lebensmittel" in df_tag_display.columns:
            df_tag_display["lebensmittel"] = df_tag_display["lebensmittel"].astype(str).str.replace(", ", "\n")
        st.dataframe(df_tag_display, use_container_width=True)

# --- Diagramm ---
st.markdown("## 📈 Aufgenommene und verbrauchte kcal im Monat")

df_monat = df_eintraege[df_eintraege["monat"] == monat_auswahl]

if not df_monat.empty:
    kcal_aufnahme = df_monat.groupby("tag")["kcal"].sum().reindex(range(1, 32), fill_value=0)
    kcal_verbrauch = df_monat.groupby("tag")["bewegung_kcal"].sum().reindex(range(1, 32), fill_value=0)

    fig, ax = plt.subplots(figsize=(14, 6))
    bar_width = 0.4
    days = range(1, 32)

    ax.bar([d - bar_width/2 for d in days], kcal_aufnahme.values, width=bar_width, label="Aufgenommene kcal (Ernährung)")
    ax.bar([d + bar_width/2 for d in days], kcal_verbrauch.values, width=bar_width, label="Verbrauchte kcal (Bewegung)")

    ax.set_title(" Vergleich: Aufgenommene vs. Verbrannte Kalorien pro Tag", fontsize=18, fontweight='bold')
    ax.set_xlabel("Tag im Monat", fontsize=14)
    ax.set_ylabel("kcal", fontsize=14)
    ax.set_xticks(days)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Noch keine Daten für diesen Monat.")

# --- Zurück-Button ---
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    switch_page("Start.py")
