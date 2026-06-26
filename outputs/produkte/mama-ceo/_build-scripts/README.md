---
tags: [produkt, mama-ceo, tools]
---

# Build-Scripts — Mama-CEO Säule 4 + 5

Generieren die PPTX-Decks + Arbeitsblätter aus den Master-Dokumenten. Hier abgelegt, damit sie nicht verloren gehen und jederzeit neu gebaut werden können.

## PPTX (python-pptx)
Voraussetzung: `pip install python-pptx`
```
python build_pptx_s4.py    # → 03-praesentationen/saeule-4/ (6 Decks)
python build_pptx_s5.py    # → 03-praesentationen/saeule-5/ (4 Decks)
```
Brand-Look: 10×5.625", weiss · Navy 1A3A4A · Petrol 12828C · Orange-Eyebrow DC822E · Georgia-Titel + Calibri-Body · Sprechnotizen pro Folie (wie Säule 3).

## Arbeitsblätter (.docx, docx-js / Node)
Voraussetzung: `npm install docx`
```
node build-arbeitsblatt-s4.js <output.docx>   # → 04-arbeitsblaetter/mama-ceo-arbeitsblatt-saeule-4.docx
node build-arbeitsblatt-s5.js <output.docx>   # → 04-arbeitsblaetter/mama-ceo-arbeitsblatt-saeule-5.docx
```
Hinweis: `.docx` ist per `.gitignore` (`**/*.docx`) NICHT in Git — die Dateien liegen lokal in `04-arbeitsblaetter/` und werden bei Bedarf hieraus neu erzeugt.

## Inhalt-Quelle
Alle Texte/Folien/Sprechnotizen kommen aus `10-saeule-4-MASTER.md` bzw. `10-saeule-5-MASTER.md`. Bei Änderungen am Master die Daten-Arrays in den Scripts entsprechend anpassen.
