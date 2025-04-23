import streamlit as st
import pandas as pd

# ✅ Seitenkonfiguration
st.set_page_config(page_title="🧈 Fette", page_icon="🧈", layout="centered")
st.title("🧈 Fette & Öle")

# ✅ Zurück zur Ernährung
def go_to_ernaehrung():
    st.markdown("""
        <meta http-equiv="refresh" content="0; url=/Ernaehrung" />
    """, unsafe_allow_html=True)

st.markdown("Gib entweder die Menge für Butter / Öl direkt ein **oder** wähle ein Lebensmittel aus der Datenbank.")

# 🔢 Direkteingabe
st.header("🔢 Direkteingabe")
butter = st.number_input("🧈 Butter (g)", min_value=0, step=5)
oel = st.number_input("🫒 Öl (ml)", min_value=0, step=5)

kcal_butter = butter * 7.5
kcal_oel = oel * 9

if butter > 0 or oel > 0:
    st.info(f"🥄 Gesamt: **{kcal_butter + kcal_oel:.1f} kcal** (Butter: {kcal_butter:.1f} kcal, Öl: {kcal_oel:.1f} kcal)")

# 📊 Lebensmitteldatenbank
st.markdown("---")
st.header("📊 Lebensmitteldatenbank")

df_food = pd.read_csv("data/Generische_Lebensmittel.csv")
df_category = pd.read_csv("data/food_category.csv")
df_nutrient = pd.read_csv("data/food_nutrient.csv")

fats_category_id = df_category[df_category["description"].str.contains("Fats and Oils", case=False)]["id"].values[0]
foods_fat = df_food[df_food["food_category_id"] == fats_category_id]

food_selection = st.selectbox("🍽️ Lebensmittel auswählen", foods_fat["description"].unique())
gram_input = st.number_input("⚖️ Menge in Gramm", min_value=1, max_value=1000, value=100)

fdc_id = foods_fat[foods_fat["description"] == food_selection]["fdc_id"].values[0]
energy_entry = df_nutrient[(df_nutrient["fdc_id"] == fdc_id) & (df_nutrient["nutrient_id"] == 2047)]

if not energy_entry.empty:
    kcal_per_100g = energy_entry["amount"].values[0]
    kcal_total = kcal_per_100g * (gram_input / 100)
    st.success(f"📈 Das sind **{kcal_total:.2f} kcal** für {gram_input}g von *{food_selection}*.")
else:
    st.warning("⚠️ Keine Kalorieninformationen gefunden.")

# 🔙 Zurück-Button
st.markdown("---")
if st.button("🔙 Zurück zur Ernährung"):
    go_to_ernaehrung()