import pandas as pd
import os
from datetime import datetime

def speichern_tageseintrag(lebensmittel=None, menge=None, kcal=None, bewegung=None, bewegung_kcal=None, schlaftext=None):
    pfad = "data/eintraege.csv"
    heute = datetime.today().day

    # Wenn Datei existiert und nicht leer ist
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        df = pd.read_csv(pfad)
    else:
        df = pd.DataFrame(columns=["tag", "lebensmittel", "menge", "kcal", "bewegung", "bewegung_kcal", "schlaf_zusammenfassung"])

    # Prüfen ob Eintrag für heutigen Tag existiert
    if heute in df["tag"].values:
        idx = df.index[df["tag"] == heute][0]
    else:
        # Neuen Tag anlegen
        new_row = {
            "tag": heute,
            "lebensmittel": "",
            "menge": 0,
            "kcal": 0,
            "bewegung": "",
            "bewegung_kcal": 0,
            "schlaf_zusammenfassung": ""
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        idx = df.index[df["tag"] == heute][0]

    # Aktualisieren
    if lebensmittel:
        if df.at[idx, "lebensmittel"]:
            df.at[idx, "lebensmittel"] += ", " + lebensmittel
        else:
            df.at[idx, "lebensmittel"] = lebensmittel

    if menge:
        df.at[idx, "menge"] += menge

    if kcal:
        df.at[idx, "kcal"] += kcal

    if bewegung:
        if df.at[idx, "bewegung"]:
            df.at[idx, "bewegung"] += ", " + bewegung
        else:
            df.at[idx, "bewegung"] = bewegung

    if bewegung_kcal:
        df.at[idx, "bewegung_kcal"] += bewegung_kcal

    if schlaftext:
        df.at[idx, "schlaf_zusammenfassung"] = schlaftext

    # Speichern
    df.to_csv(pfad, index=False)