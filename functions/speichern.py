import pandas as pd
import os
from datetime import datetime

# ✅ Funktion zum Speichern eines Tages-Eintrags
def speichern_tageseintrag(monat, tag, lebensmittel=None, menge=None, kcal=None, bewegung=None, bewegung_kcal=None, schlaftext=None, wasser_ml=None):
    pfad = "data/eintraege.csv"
    
    # Bestehende Daten laden oder neues DataFrame erstellen
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        df = pd.read_csv(pfad)
        if "wasser_ml" not in df.columns:
            df["wasser_ml"] = 0
    else:
        df = pd.DataFrame(columns=["monat", "tag", "lebensmittel", "menge", "kcal", "bewegung", "bewegung_kcal", "schlaf_zusammenfassung", "wasser_ml"])
    
    # Eintrag suchen oder neu erstellen
    idx = df[(df["monat"] == monat) & (df["tag"] == tag)].index
    if idx.empty:
        new_row = {
            "monat": monat,
            "tag": tag,
            "lebensmittel": "",
            "menge": 0,
            "kcal": 0,
            "bewegung": "",
            "bewegung_kcal": 0,
            "schlaf_zusammenfassung": "",
            "wasser_ml": 0
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        idx = [df.index[-1]]

    idx = idx[0]

    # Felder ergänzen
    if lebensmittel:
        if pd.notna(df.at[idx, "lebensmittel"]) and df.at[idx, "lebensmittel"] != "":
            df.at[idx, "lebensmittel"] += ", " + lebensmittel
        else:
            df.at[idx, "lebensmittel"] = lebensmittel

    if menge:
        df.at[idx, "menge"] += menge

    if kcal:
        df.at[idx, "kcal"] += kcal

    if bewegung:
        if pd.isna(df.at[idx, "bewegung"]):
            df.at[idx, "bewegung"] = ""
        df.at[idx, "bewegung"] = str(df.at[idx, "bewegung"])
        
        if df.at[idx, "bewegung"] != "":
            df.at[idx, "bewegung"] += ", " + bewegung
        else:
            df.at[idx, "bewegung"] = bewegung

    if bewegung_kcal:
        df.at[idx, "bewegung_kcal"] += bewegung_kcal
        df.at[idx, "kcal"] += bewegung_kcal   # 🚀 Bewegung auch in kcal ergänzen!

    if schlaftext:
        df.at[idx, "schlaf_zusammenfassung"] = schlaftext

    if wasser_ml:
        df.at[idx, "wasser_ml"] += wasser_ml

    # Speichern
    df.to_csv(pfad, index=False)

# ✅ Funktion Profil speichern
def speichern_profil(name, alter, gewicht, geschlecht, ziel1, ziel2):
    df = pd.DataFrame([{
        "Name": name,
        "Alter": alter,
        "Gewicht": gewicht,
        "Geschlecht": geschlecht,
        "Ziel1": ziel1,
        "Ziel2": ziel2
    }])
    df.to_csv("data/profil.csv", index=False)

# ✅ Funktion Profil laden
def laden_profil():
    pfad = "data/profil.csv"
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        return pd.read_csv(pfad).iloc[0]
    else:
        return None