---
tags: [produkt, launch, story]
---

# Käufertypen in den Launch-Storys — Durchsicht 08.10.2026

**Anlass:** Patricia, 08.10.2026 — *„sorg dafür, dass in den vorbereiteten storys im
launch alle käufertypen berücksichtigt sind"*.

Durchgesehen: **alle 19 Story-Tage des KI-Launches** aus der Cockpit-Sammlung
`storys` (`kw40-story-m-ki-*` bis `kw43-story-m-ki-*`), zusammen **139 Folien**.
Gelesen wurde aus der Datenbank, nicht aus den lokalen Dateien — der
Donnerstagabend (`kw41-story-m-ki-do`, Folien 7–16) liegt nur im Cockpit.

Die sechs Typen sind die aus dem Launch-Reiter (Cockpit → Produkte → Launch),
benannt nach dem, was sie brauchen.

---

## Befund je Woche

| Typ | KW41 (5.–11.10.) | KW42 (12.–18.10.) | KW43 (19.–23.10.) |
|---|---|---|---|
| **Die Inspirierte** | ✓ Mo „mein kleines KI-Team … während ich bei den Kindern bin" · So „Sonntagabend ohne Menüplan" | ✓ Fr „der Kern von allem" · Sa · So „Was wäre im März anders?" | ✓ Di „was meine Helfer an einem normalen Tag erledigen" |
| **Die Beweis-Sucherin** | ✓ Mo „O-Ton aus meinen DMs" · Do Sprachnachricht einer Kundin · Fr zwei Learnings · Sa Learning | ✓ Do Learning | ✓ Mo · Di zwei Learnings · Do Learning |
| **Die Zahlen-Person** | ✓ Do Kurs-Karte „Frühbucherpreis 277 statt 333, gilt bis 15.10." | ✓ Di ganzer Tag dafür: Lektionen 8–15 Min, Telegram-Gruppe, Preis · Do | ✓ Do „Zehn Module mit 62 Lektionen ab 1.11." |
| **Die Mitmacherin** | 🚨 **fehlt** | 🚨 **fehlt** | 🚨 **fehlt** |
| **Die Zögernde** | ✓ Di „Ich hab ja schon ChatGPT" · Mi Secret endet · Do „keine Technikerin" · Sa Bonus-Frist | ✓ Do Umfrage „Was hält dich zurück" · Fr „in den ersten drei Modulen musst du nichts installieren" | ✓ Mo „für wen der Kurs nichts ist" · Mi „was ‚irgendwann' kostet" |
| **Die Entschlossene** | ✓ Link-Sticker auf jeder CTA-Folie | ✓ | ✓ |

**Fünf von sechs sind je Woche bedient. Die Mitmacherin kam in keiner einzigen
der 139 Folien vor.** Die Suche nach *sind dabei · ist dabei · schon drin ·
haben sich · die ersten · Plätze · Vornamen* findet null Treffer.

🚨 **Das war kein Versehen, sondern eine Lücke mit Ursache:** Die Storys wurden
am 25.09. und 08.10. geschrieben, da gab es noch keine Käufe. „Wer schon dabei
ist" lässt sich nicht vorschreiben. Deshalb fehlte genau der Typ, der am Schluss
kauft, weil andere schon dabei sind — und genau der steht als Pflicht in der
Verkaufsphase (*„Jeden Tag teilen, wer schon dabei ist — echte Vornamen"*).

---

## Was eingebaut wurde

`python scripts/launch/storys-mitmacherin.py <quelle> --ziel <ordner>` legt in
**15 Story-Tage** (9.10. bis 23.10., also die ganze Verkaufsphase) eine Folie
`s-dabei` **vor** die letzte Folie — der CTA bleibt das Letzte.

- **Fünf Wortlaute im Wechsel**, damit nicht fünfzehnmal dieselbe Folie steht:
  „Die Ersten sind dabei." · „Heute ist wieder jemand dazugekommen." · „Schau
  mal, wer sich entschieden hat." · „Die Gruppe füllt sich." · „Noch eine, die
  im November dabei ist."
- **Drei Looks im Wechsel** (Foto · Creme · Petrol), keine zwei gleichen Tage
  hintereinander.
- **Anweisung in `notiz`**, nie im Bild: Screenshot der Bestellung oder der
  Nachricht, **Vornamen nur mit Okay der Kundin**, sonst Namen abdecken. Und:
  *gibt es heute wirklich keinen neuen Kauf, Folie weglassen statt etwas
  behaupten.*

🚨 **Keine erfundenen Namen und keine erfundenen Zahlen** — dieselbe Regel wie
in `context/kundinnen-geschichten.md`. Die Folie ist ein **Platz**, kein Inhalt.

🚨 **`layout` muss zum Hintergrund passen.** Beim ersten Anlauf standen alle
fünfzehn als `layout: "bild"` da, zehn davon ohne Foto. Sichtbar wäre das nicht
gewesen — der Hintergrund kommt aus `hg` —, aber `storys-gestalten.py` stuft
nach `layout` ein und hätte den zehn später ein Foto untergelegt. Jetzt ist
`bild` nur bei `hg: "foto"`, sonst `text`. Gültige Werte stehen in
`scripts/cockpit/story-bibliothek.js`: `hg` = foto · creme · dunkel · petrol ·
orange, `balken` = aus · zeilen · karte.

---

## 🔗 Verwandte Notizen

- [[09-funnel-geruest]]
- [[07-launch-kalender]]
- [[2026-10-08-julia-funnel-durchsicht]]
