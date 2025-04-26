import streamlit as st
import pandas as pd
from datetime import datetime
from functions.speichern import speichern_tageseintrag

# Seitenkonfiguration
st.set_page_config(page_title="Ernaehrung", page_icon="🍎", layout="centered")

st.title("🍎 Ernährung")
st.markdown("Wähle eine Kategorie aus der Ernährungspyramide:")

# Auswahlmenü
kategorie = st.radio(
    "Kategorie wählen:",
    [
        "🍫 Süsses",
        "🧈 Fette",
        "🥩 Fleisch / Fisch",
        "🧀 Milchprodukte",
        "🍞 Getreide / Reis / Kartoffeln",
        "🥦 Gemüse",
        "🍎 Obst"
    ],
    horizontal=False
)

# Inhalt je nach Auswahl
if kategorie == "🍫 Süsses":
    st.subheader("🍫 Süsses")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge in Gramm ein.")
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_suesses = ["Süßwaren", "Snacks", "Backwaren", "Desserts", "Gebäck", "Kuchen", "Schokolade"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_suesses), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])
    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="suesses_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100, key="suesses_gramm")
    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)
    st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")
    if st.button("💾 Speichern", key="suesses_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(heute.month, heute.day, food_selection, gram_input, kcal_total)
        st.success(f"✅ {gram_input}g {food_selection} mit {kcal_total:.2f} kcal gespeichert!")
    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

elif kategorie == "🧈 Fette":
    st.subheader("🧈 Fette & Öle")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_fette = ["Fette", "Öle", "Butter", "Pflanzenöl", "Speisefette"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_fette), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])
    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="fette_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm oder ml", min_value=1, max_value=1000, value=100, key="fette_gramm")
    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)
    st.success(f"📈 {gram_input}g/ml {food_selection} enthalten **{kcal_total:.2f} kcal**.")
    if st.button("💾 Speichern", key="fette_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(heute.month, heute.day, food_selection, gram_input, kcal_total)
        st.success("✅ Lebensmittel gespeichert!")
    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

elif kategorie == "🥩 Fleisch / Fisch":
    st.subheader("🥩 Fleisch & Fisch")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_fleisch_fisch = ["Fleisch", "Geflügel", "Fisch", "Meeresfrüchte"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_fleisch_fisch), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])
    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="fleisch_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100, key="fleisch_gramm")
    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)
    st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")
    if st.button("💾 Speichern", key="fleisch_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(heute.month, heute.day, food_selection, gram_input, kcal_total)
        st.success("✅ Lebensmittel gespeichert!")
    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

elif kategorie == "🧀 Milchprodukte":
    st.subheader("🧀 Milchprodukte")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")

    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_milchprodukte = ["Milch", "Käse", "Joghurt", "Sahne", "Milchprodukte"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_milchprodukte), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])

    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="milch_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm oder ml", min_value=1, max_value=1000, value=100, key="milch_gramm")

    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)

    st.success(f"📈 {gram_input}g/ml {food_selection} enthalten **{kcal_total:.2f} kcal**.")

    if st.button("💾 Speichern", key="milch_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(
            monat=heute.month,
            tag=heute.day,
            lebensmittel=food_selection,
            menge=gram_input,
            kcal=kcal_total
        )
        st.success("✅ Lebensmittel gespeichert!")

    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")


elif kategorie == "🍞 Getreide / Reis / Kartoffeln":
    st.subheader("🍞 Getreide / Reis / Kartoffeln")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")

    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien = ["Getreide", "Reis", "Kartoffeln", "Pasta", "Teigwaren"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])

    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="getreide_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100, key="getreide_gramm")

    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)

    st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")

    if st.button("💾 Speichern", key="getreide_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(
            monat=heute.month,
            tag=heute.day,
            lebensmittel=food_selection,
            menge=gram_input,
            kcal=kcal_total
        )
        st.success("✅ Lebensmittel gespeichert!")

    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")


elif kategorie == "🥦 Gemüse":
    st.subheader("🥦 Gemüse")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_gemuese = ["Gemüse"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_gemuese), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])
    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="gemuese_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100, key="gemuese_gramm")
    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)
    st.success(f"📈 {gram_input}g {food_selection} enthalten **{kcal_total:.2f} kcal**.")
    if st.button("💾 Speichern", key="gemuese_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(heute.month, heute.day, food_selection, gram_input, kcal_total)
        st.success("✅ Lebensmittel gespeichert!")
    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

elif kategorie == "🍎 Obst":
    st.subheader("🍎 Obst")
    st.markdown("Wähle ein Lebensmittel aus der Datenbank und gib die Menge ein.")
    df = pd.read_excel("data/Ernaehrungsdaten.xlsx", sheet_name="Tabelle1")
    kategorien_obst = ["Obst", "Früchte", "Fruchtsäfte"]
    df = df[df["Kategorie"].str.contains('|'.join(kategorien_obst), case=False, na=False)]
    df = df.dropna(subset=["Energie, Kalorien (kcal)"])
    st.header("📊 Lebensmittel auswählen")
    food_selection = st.selectbox("🍽️ Lebensmittel", df["Name"].unique(), key="obst_selectbox")
    gram_input = st.number_input("⚖️ Menge in Gramm oder ml", min_value=1, max_value=1000, value=100, key="obst_gramm")
    daten = df[df["Name"] == food_selection].iloc[0]
    kcal_pro_100g = daten["Energie, Kalorien (kcal)"]
    kcal_total = kcal_pro_100g * (gram_input / 100)
    st.success(f"📈 {gram_input}g/ml {food_selection} enthalten **{kcal_total:.2f} kcal**.")
    if st.button("💾 Speichern", key="obst_speichern"):
        heute = datetime.now()
        speichern_tageseintrag(heute.month, heute.day, food_selection, gram_input, kcal_total)
        st.success("✅ Lebensmittel gespeichert!")
    if "Bezugseinheit" in daten:
        st.caption(f"ℹ️ Bezugsbasis: {daten['Bezugseinheit']}")

# 💧 Wasser
st.markdown("---")
st.markdown("## 💧 Wasser")
if "wasser_glaeser" not in st.session_state:
    st.session_state.wasser_glaeser = 0
st.session_state.wasser_glaeser = st.number_input(
    "Wie viele Gläser Wasser hast du getrunken? (à 300ml)", 
    min_value=0, step=1,
    value=st.session_state.wasser_glaeser
)
st.write(f"Das sind **{st.session_state.wasser_glaeser * 300} ml Wasser**.")
if st.button("💾 Wasser speichern"):
    st.success(f"✅ {st.session_state.wasser_glaeser * 300} ml Wasser gespeichert!")

# 🔙 Zurück zur Startseite
st.markdown("---")
if st.button("🔙 Zurück zum Start"):
    st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)


