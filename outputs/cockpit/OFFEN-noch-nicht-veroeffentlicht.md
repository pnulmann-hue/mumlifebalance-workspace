---
tags: [tools, cockpit]
---

# Erledigt: beide Patches sind veroeffentlicht

**08.10.2026, Version 90** (`1791469052-0493`). Die Datei
`outputs/cockpit/mlb-cockpit.html` und das Live-Artifact
https://claude.ai/artifact/WWF7EWhCiAf2cVi1vytGFM sind wieder gleich.

Drin sind:

| Patch | Was |
|---|---|
| `scripts/cockpit/patch-entwurf-quelle.py` | Die Beschriftung ueber einer Mail-Karte haengt am Feld `quelle`. Bei den 130 Live-Mails aus ActiveCampaign stand vorher „noch nicht in ActiveCampaign" — eine Falschaussage. |
| `scripts/cockpit/patch-launch-reiter.py` | Der Reiter **Produkte → Launch**: wo stehe ich · Kaeufertypen diese Woche · der Fahrplan ueber die fuenf Phasen · Launches anlegen. Code daneben in `launch-reiter.js` und `launch-reiter.css`. |

## 🚨 Was dabei passiert ist, und was daraus folgt

Zwischen dem Bauen und dem Veroeffentlichen wurde
`outputs/cockpit/mlb-cockpit.html` **auf den Live-Stand zurueckgesetzt** — beide
Patches waren danach weg, obwohl beide Skripte Erfolg gemeldet hatten und der
Launch-Reiter in der lokalen Testfassung lief. Gemerkt habe ich es nur, weil ich
die Live-Fassung vor dem Publish Zeile fuer Zeile gegen die lokale gehalten habe.

**Die Lehre: vor jedem Publish diffen, nicht auf die Erfolgsmeldung des
Patch-Skripts vertrauen.** Ein Skript sagt, was es getan hat — nicht, ob es
danach noch dasteht. Beide Skripte sind wiederholbar; das Zurueckholen war
zweimal ein Befehl.

```bash
python scripts/cockpit/patch-entwurf-quelle.py
python scripts/cockpit/patch-launch-reiter.py
```

## 🚨 Zwei Befunde nebenbei

**Das Cockpit steht auf „Anyone with the link".** Seit dem 24.09.2026 liegen
darin 32 Klarnamen und 3 Mailadressen von Kundinnen (CLAUDE.md,
„Personendaten im Cockpit"). Ein oeffentlicher Link passt nicht dazu. Aendern
kann das nur Patricia selbst ueber das Share-Menue der Seite.

**Die Preisstufen des KI-Launches sind verkehrt herum.** Bei 199 · 277 · 333
ist der Schritt vom Secret Offer zum Fruehbucher **78**, der zum regulaeren
Preis nur **56**. Nach der Methodik gehoert es umgekehrt: vorne klein, hinten
gross — wer frueh vertraut, soll den groessten Abstand zum Normalpreis haben.
Der neue Reiter zeigt diese Gegenprobe von selbst an.
