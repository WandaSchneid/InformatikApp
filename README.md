# BMLD Gesundheits-Tracker

Diese App dient der **Erfassung und Analyse von Gesundheitsdaten** im Rahmen eines Studienprojekts. Sie richtet sich speziell an Menschen **ab etwa 50 Jahren** und unterstützt diese dabei, ihre **Ernährung**, **Bewegung** und **Schlafgewohnheiten** im Alltag bewusst zu verfolgen und aktiv an ihrer Gesundheit zu arbeiten.

## ✨ Ziel der App

Ziel ist die Entwicklung einer **benutzerfreundlichen, altersgerechten Applikation für Personen fortgeschrittenen Alters**, die:

- Gesundheitsdaten wie **Mahlzeiten & Kalorien**, **körperliche Aktivität** und **Schlafverhalten** erfasst
- diese **verständlich aufbereitet** (z. B. über einfache Eingabemasken und Filter)
- visuelle **Diagramme** und **Auswertungen** bietet
- zur **Reflexion und Motivation** für gesündere Entscheidungen anregt

Die App ist bewusst **einfach gestaltet**, um auch **technisch weniger versierten Nutzer*innen** einen intuitiven Zugang zu ihren Daten zu ermöglichen.

---

## 🧭 Funktionen der App

- **Ernährungstagebuch** (Eingabe tägliche getrunkene Wassermenge, Eingabe nach Lebensmittelkategorien, z. B.      Gemüse, Obst, Getreide etc.)
- **Bewegungserfassung** (z. B. Gehzeit, Sportart + Zeitangabe, Anzeige verbrannte Kalorien)
- **Schlafprotokoll** (Einschlaf- und Aufwachzeiten, Schlafqualität)
- **Tagesauswertung** und **übersichtliches Diagramm verbrauchte und aufgenommene Kalorien**
- **Datenspeicherung lokal oder serverbasiert** (je nach Modus)
- **Login-System** (je nach Version)

---

## 🚀 Nutzungshinweise

1. Öffne die App unter folgendem Link:👉 [https://gesundheits-tracker.streamlit.app](https://gesundheits-tracker.streamlit.app)
2. Wähle im Menü den gewünschten Bereich:

   - *Ernährung* → Lebensmittel pro Kategorie eingeben + Eingabe getrunkene Wassermenge
   - *Bewegung* → Regelleiste für gelaufene Zeit + Eingabe zweier sportlichen Akitivitäten mit Zeitangabe 
   - *Schlaf* → Daten eintragen (Dauer, Einschätzung Qualität)
3. Klicke auf **„Speichern“**, um deine Eingaben zu sichern.
4. Wechsel zu **„Auswertung“**, um deine Einträge als **Diagramm für verbauchte und aufgenommene Kalorien** zu sehen.

---

## 🧪 Technische Umsetzung (optional)

- Die App wurde mit **Python** & **Streamlit** entwickelt
- Die Seitenstruktur ist modular aufgebaut:
  `pages/` enthält einzelne Themenbereiche
  `utils/` enthält Datenverarbeitung & UI-Elemente

---

## 👥 Autoren

- Wanda Schneid (schnewan@students.zhaw.ch)
- Riccardo Reich (reichri1@students.zhaw.ch)
- Dana Schnekenburger (schned06@students.zhaw.ch)

---

*Dieses Projekt entstand im Rahmen des Moduls „Informatik für Angewandte Gesundheitswissenschaften“ an der ZHAW.*
