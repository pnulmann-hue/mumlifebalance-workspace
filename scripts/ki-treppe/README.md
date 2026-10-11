---
tags: [produkt, ki, kurs]
---

# Werkzeuge für den KI-Kurs

Zwei Skripte für „Deine KI-Mitarbeiterin" (333 CHF, ThriveCart-Kurs 232070).
Quelle für beide ist `outputs/produkte/ki-treppe/`.

---

## 1 · Beilagen als Brand-PDF

```bash
cd scripts/karussell-render        # dort liegt Puppeteer
cp ../ki-treppe/beilagen-bauen.mjs ./_t.mjs && node ./_t.mjs ; rm -f ./_t.mjs
```

Liest jede `.md` aus `outputs/produkte/ki-treppe/beilagen/`, macht daraus eine
A4-Seite in Patricias Branding (Creme · Petrol · Orange, Philosopher +
Source Sans 3) und legt HTML und PDF in `beilagen/pdf/` ab.

Ein Teilname als Argument baut nur die passenden Dateien neu:
`node ./_t.mjs checkliste` baut die neun Modul-Checklisten.

🚨 **Der Sprach-Wächter läuft bei jedem Bau mit.** Er meldet scharfes s und
umschriebene Umlaute im sichtbaren Text — genau dieser Fehler stand am
18.09.2026 dreimal in einer fertigen Startklar-Mail, und gefunden hat ihn
Patricia, nicht die Selbstprüfung. Echte ae/oe/ue-Wörter (bauen, dauert,
draussen, vertrauen) stehen in der Ausnahmeliste, sonst liest nach dem dritten
Fehlalarm niemand mehr hin.

🚨 **Die Vorschau im Browser zeigt keine Seitenränder.** Wer das HTML
anschaut, sieht randlosen Text und hält ihn für abgeschnitten. Für die
Sichtprüfung die `@page`-Ränder als Padding simulieren (17/16/20 mm sind bei
96 dpi rund 64/60/76 px) — oder ins PDF selbst schauen.

**Schriftschnitte sparsam halten.** Jeder geladene Schnitt wird in *jede* PDF
eingebettet. Bei 16 Beilagen sind das schnell 1,4 MB. Geladen wird nur, was
das CSS wirklich benutzt: Philosopher 700, Source Sans 3 in 400 und 600.

---

## 2 · Kopierseite für die Kursplattform

```bash
python scripts/ki-treppe/kopierseite-bauen.py
# dann: preview_start {"name": "ki-kurs-texte"}   ->  http://localhost:4387
```

Baut aus `04-kursplattform-texte.md` eine Seite mit Kopier-Knöpfen: Begrüssung,
zehn Modultexte, 62 Lektionen. Jeder Knopf legt den Text als `text/html` **und**
`text/plain` per `ClipboardItem` ab — in ThriveCart reicht dann Strg+V, und
Absätze wie Fettungen kommen mit.

**Titel und Beschreibung sind getrennte Knöpfe**, weil die Plattform dafür zwei
Felder hat. Das war bei Startklar die Erkenntnis: ein Knopf für beides nützt
nichts.

Der Haken **„steht schon drin"** kommt aus der Menge `ERLEDIGT` im Skript.
Stand 22.09.2026: 1.1 bis 2.3 eingetragen, 54 offen. Wenn Patricia weiterkommt,
dort die Nummern ergänzen — dann blendet der Filter oben sie aus.

---

## Was nicht geht

🚨 **Claude kann die PDFs nicht nach Google Drive laden.** Der Drive-Connector
nimmt Dateien nur als base64 im Aufruf entgegen; bei 16 PDFs à 65–141 KB wären
das rund 1,9 MB Text durch den Chat, zweimal — für etwas, das per
Drag-and-Drop zwanzig Sekunden dauert. Deshalb liegen sie fertig in
`Downloads/_fuer-drive/KI-Kurs — Deine KI-Mitarbeiterin/`, und der Zielordner
in Drive ist bereits angelegt:
[KI-Kurs — Deine KI-Mitarbeiterin](https://drive.google.com/drive/folders/1FzEiDo-R-qi9KXuN4tYRqydd9SkpZQXq)
(unter **Produkte**, wo auch die anderen Kurse liegen — einen Ordner „Kurse"
gibt es in ihrem Drive nicht).

🚨 **ThriveCart hat keine Schnittstelle für Kursinhalte.** Die API kennt
Produkte, Bumps, Upsells und Transaktionen — Module und Lektionen nicht. Das
Eintragen bleibt Handarbeit, die Kopierseite macht sie nur kurz.
