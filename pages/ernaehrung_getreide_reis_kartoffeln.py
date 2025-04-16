import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Getreide / Reis / Kartoffeln", page_icon="🍞", layout="centered")
st.title("🍞 Getreide / Reis / Kartoffeln")
st.markdown("Gib entweder eine Menge direkt ein **oder** wähle ein Lebensmittel aus der Datenbank.")

# 👉 Variante 1: Manuelle Eingabe
st.header("🔢 Direkteingabe")
input0 = st.number_input("🍚 Reis (g)", min_value=0, step=5)
kcal_input0 = input0 * 1.3
input1 = st.number_input("🥔 Kartoffeln (g)", min_value=0, step=5)
kcal_input1 = input1 * 0.8

if kcal_input0 + kcal_input1 > 0:
    st.info(f"📊 Gesamt: **{kcal_input0 + kcal_input1:.1f} kcal** (🍚 Reis (g): {kcal_input0:.1f} kcal + 🥔 Kartoffeln (g): {kcal_input1:.1f} kcal)")

# 🔄 Trennlinie
st.markdown("---")

# 👉 Variante 2: Auswahl aus CSV
st.header("📊 Lebensmitteldatenbank")

# CSV-Dateien laden
df_food = pd.read_csv("data/food.csv")
df_category = pd.read_csv("data/food_category.csv")
df_nutrient = pd.read_csv("data/food_nutrient.csv")
df_nutrient_lookup = pd.read_csv("data/nutrient.csv")

# Kategorie-ID(s)
category_ids = df_category[df_category["description"].str.contains(r"Cereal Grains and Pasta", case=False, regex=True)]["id"].unique()
foods = df_food[df_food["food_category_id"].isin(category_ids)]
food_selection = st.selectbox("🍽️ Lebensmittel auswählen", foods["description"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

# Kalorien berechnen
fdc_id = foods[foods["description"] == food_selection]["fdc_id"].values[0]
energy_entry = df_nutrient[(df_nutrient["fdc_id"] == fdc_id) & (df_nutrient["nutrient_id"].isin([2047, 2048]))]

if not energy_entry.empty:
    kcal_per_100g = energy_entry["amount"].values[0]
    kcal_total = kcal_per_100g * (gram_input / 100)
    st.success(f"📈 Das sind **{kcal_total:.2f} kcal** für {gram_input}g von *{food_selection}*.")
else:
    st.warning("⚠️ Keine Kalorieninformationen für dieses Lebensmittel gefunden.")

if st.button("🔙 Zurück zur Ernährung"):
    switch_page("ernaehrung")