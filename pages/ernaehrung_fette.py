import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="🧈 Fette", page_icon="🧈", layout="centered")

st.title("🧈 Fette & Öle")
st.markdown("Gib entweder die Menge für Butter / Öl direkt ein **oder** wähle ein Lebensmittel aus der Datenbank.")

# 👉 Variante 1: Manuelle Eingabe
st.header("🔢 Direkteingabe")
butter = st.number_input("🧈 Butter (g)", min_value=0, step=5)
oel = st.number_input("🫒 Öl (ml)", min_value=0, step=5)

# Annahme: 1g Butter ≈ 7.5 kcal, 1ml Öl ≈ 9 kcal (vereinfacht)
kcal_butter = butter * 7.5
kcal_oel = oel * 9

if butter > 0 or oel > 0:
    st.info(f"🥄 Gesamt: **{kcal_butter + kcal_oel:.1f} kcal** (Butter: {kcal_butter:.1f} kcal, Öl: {kcal_oel:.1f} kcal)")

# 🔄 Trennlinie
st.markdown("---")

# 👉 Variante 2: Auswahl aus CSV
st.header("📊 Lebensmitteldatenbank")

# CSV-Dateien laden
df_food = pd.read_csv("data/food.csv")
df_category = pd.read_csv("data/food_category.csv")
df_nutrient = pd.read_csv("data/food_nutrient.csv")
df_nutrient_lookup = pd.read_csv("data/nutrient.csv")

# Kategorie-ID für "Fats and Oils"
fats_category_id = df_category[df_category["description"].str.contains("Fats and Oils", case=False)]["id"].values[0]
foods_fat = df_food[df_food["food_category_id"] == fats_category_id]

# Dropdown Auswahl
food_selection = st.selectbox("🍽️ Lebensmittel auswählen", foods_fat["description"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

# Kalorien berechnen
fdc_id = foods_fat[foods_fat["description"] == food_selection]["fdc_id"].values[0]
energy_id = 2047
energy_entry = df_nutrient[(df_nutrient["fdc_id"] == fdc_id) & (df_nutrient["nutrient_id"] == energy_id)]

if not energy_entry.empty:
    kcal_per_100g = energy_entry["amount"].values[0]
    kcal_total = kcal_per_100g * (gram_input / 100)
    st.success(f"📈 Das sind **{kcal_total:.2f} kcal** für {gram_input}g von *{food_selection}*.")
else:
    st.warning("⚠️ Keine Kalorieninformationen für dieses Lebensmittel gefunden.")

# Zurück-Button
if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")