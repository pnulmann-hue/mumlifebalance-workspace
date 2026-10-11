# Startklar — Handybildschirm ins Zoom-Video legen

Der Kurs **Startklar** wurde am 17.09.2026 über Zoom aufgenommen: Präsentation,
Ton und Webcam. Wo Patricia am Handy gezeigt hat, lief parallel eine
Bildschirmaufnahme auf dem Handy — **ohne** dass der Bildschirm in Zoom geteilt
wurde. Im Zoom-Video ist an diesen Stellen deshalb nur schwarzes Bild plus
Webcam. Diese Skripte legen die Handyaufnahme dort hinein.

## Der Ausgangsbestand

| Zoom-Teil | Länge | Inhalt | Handybild |
|---|---|---|---|
| 1 | 6:48 | Konto-Entscheid (umstellen oder neu) | **nicht nötig** — Präsentation läuft durch |
| 2 | 5:11 | Name, Benutzername, Profilbild, Suchfeld | `Screen_Recording_…110812` |
| 3 | 4:16 | Die Bio | `Screen_Recording_…110914` |
| 4 | 12:31 | Highlights und Links | `Screen_Recording_…112245` |
| 5 | 2:50 | Zwei-Faktor und Privatsphäre | `Screen_Recording_…112548` |

Zwei Handyaufnahmen bleiben liegen: eine 3,9-Sekunden-Datei (Fehlstart) und
eine von 10:57–10:58, die in Teil 1 fällt — dort läuft die Präsentation.

## Warum der Versatz von Hand kommt

🚨 **Die Tonspur der Handyaufnahmen ist digital still** (−91 dB) — Samsung nimmt
nur den Medienton auf, und Instagram-Bedienung macht keinen. Damit fällt die
übliche Synchronisation über Tonabgleich aus. Es gibt keinen gemeinsamen Ton,
über den sich die beiden Spuren automatisch ausrichten liessen.

Die Startwerte in `sync.json` stammen deshalb aus dem **Wortlaut im Zoom-Ton**.
Jeder Wert hat seinen Anker im Feld `notiz`, zum Beispiel für Teil 3:

> bei 186,6 s sagt sie wörtlich „Wir starten wieder die Bildschirmaufnahme"

Für Teil 4 stimmt zusätzlich die Länge: 300 s Versatz plus 441 s Handyaufnahme
ergibt 741 s bei 751 s Teillänge.

🚨 **Die Zeitstempel in den Handy-Dateinamen sind Endzeiten, keine Startzeiten.**
Mit „Start" würden sich zwei Aufnahmen überlappen, was nicht sein kann; mit
„Ende" geht die Reihenfolge lückenlos auf. Bestätigt durch die Uhr in der
Statusleiste der Aufnahmen selbst.

## Der Weg

### 1. Einpassen — Sync-Editor

```bash
# in Claude Code: preview_start {"name": "startklar-sync"}   → http://localhost:4382
```

Zeigt das Endlayout mit echtem Ton: Handy links, Webcam rechts. Der Regler
verschiebt die Handyaufnahme, `[` und `]` gehen in 0,1-Sekunden-Schritten.
Läuft mit kleinen Vorschaudateien, damit das Schieben flüssig bleibt.

Die Werte bleiben im Browser gespeichert. „Kopieren" gibt alle vier als Zeile
heraus — die gehören dann in `sync.json` unter `versatz`.

### 2. Bauen

```bash
python scripts/startklar/bauen.py                          # alle vier Teile
python scripts/startklar/bauen.py --teil 4                 # nur einer
python scripts/startklar/bauen.py --teil 4 --versatz 302.5  # Wert testen
python scripts/startklar/bauen.py --teil 4 --probe          # nur 40 s, schnell
```

`--probe` beginnt 8 Sekunden vor dem Einblenden — damit ist in einer halben
Minute zu sehen, ob der Übergang sitzt, statt 12 Minuten zu rendern.

Ergebnis: `video/startklar/fertig/teilN.mp4`, 1920×1080, 25 fps.

## Das Layout

Ein Handybild ist 1080×2340, also sehr schmal. Auf voller Bildhöhe nimmt es
gut ein Viertel der Breite ein — mehr geht nur, indem man links und rechts
etwas abschneidet, und das kostet bei einer Klickanleitung genau die Ränder,
auf die es ankommt. Deshalb: **volle Höhe, nichts abgeschnitten**, die Webcam
kleiner daneben, Hintergrund in Dunkelblau (#0c1c30).

Oben werden 96 Pixel Statusleiste weggeschnitten — sonst läuft der rote
Aufnahme-Punkt durch das ganze Kursvideo mit. Die Navigationsleiste unten
bleibt, weil die Zurück-Taste zur Anleitung gehört.

Alle Masse stehen in `sync.json` unter `layout` und lassen sich dort ändern,
ohne das Skript anzufassen.

## Ordner

```
video/startklar/
├── zoom/         Zoom-Teile (Kopie aus OneDrive)
├── roh/          Handyaufnahmen (Kopie vom Handy) + Standbilder
├── proxy/        (leer, reserviert)
├── sync-editor/  die Seite zum Einpassen + kleine Vorschaudateien
├── kontrolle/    Standbilder zum Selbst-Prüfen
└── fertig/       die gebauten Videos
```

🚨 `video/**` ist gitignored — das Repo ist öffentlich, und in den Aufnahmen
sind Patricias Gesicht, ihr Instagram-Konto und ihre Zahlen zu sehen.
