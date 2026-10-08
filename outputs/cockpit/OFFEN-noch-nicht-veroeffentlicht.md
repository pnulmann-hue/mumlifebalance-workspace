---
tags: [tools, cockpit]
---

# Offen: ein Patch liegt lokal, ist aber nicht veröffentlicht

**Stand 08.10.2026.** `outputs/cockpit/mlb-cockpit.html` trägt eine Änderung,
die im Live-Artifact **noch nicht** drin ist. Das ist bewusst dokumentiert und
nicht still — ein unbemerktes Auseinanderlaufen war schon einmal das Problem
(CLAUDE.md: „war bis dahin ab Zeile 3126 auseinandergelaufen").

| | |
|---|---|
| **Artifact** | https://claude.ai/artifact/WWF7EWhCiAf2cVi1vytGFM |
| **Live-Version** | `1791451533-b9f6` (635'436 Bytes, 13'120 Zeilen) |
| **Was fehlt dort** | der Patch aus `scripts/cockpit/patch-entwurf-quelle.py` |

## Was der Patch tut

Über jeder Mail-Karte in „Listen & Automationen" stand bis jetzt immer derselbe Satz:

> „Neue Fassung von mir, noch nicht in ActiveCampaign. Schau dir die Vorschau an,
> kopier das HTML und setz es in der Automation ein."

Seit dem 08.10. liegen dort **130 Live-Mails aus ActiveCampaign** (Feld
`quelle: "activecampaign"`). Für die ist der Satz eine **Falschaussage** — sie
stehen dort längst, und wer ihn befolgt, baut etwas ein, was schon drin ist.
Der Patch macht die Beschriftung vom Feld `quelle` abhängig.

## Gegenprobe ist gemacht

Lokal und live sind **sonst Zeile für Zeile identisch** — maschinell geprüft
(Rahmen abgezogen, Zeilenenden normiert): 21 Diff-Zeilen, alle aus diesem einen
Patch. Die 13 KB Grössenunterschied waren CRLF in der gespeicherten Kopie, kein
Inhalt. „Mein Tisch" (Version 84) ist in beiden Fassungen vorhanden.

## Warum es liegengeblieben ist

Ein Publish verlangt, dass die Live-Fassung in derselben Session **Zeile für
Zeile gelesen** wurde. Das sind 13'120 Zeilen und rund 340'000 Token — in einer
schon gefüllten Session ein schlechter Tausch für einen Satz.

## So wird es nachgezogen

In einer **frischen** Session, als erste Handlung:

```bash
python scripts/cockpit/patch-entwurf-quelle.py   # falls lokal zurückgesetzt wurde
```

Dann `Artifact read` auf die URL oben, die gespeicherte Datei vollständig lesen,
und mit `Artifact publish` + `url` aus `outputs/cockpit/mlb-cockpit.html`
veröffentlichen. Das Skript ist wiederholbar und prüft selbst mit `node --check`.

🚨 **Nicht ohne den Read publishen** und nicht mit `force` — das verwirft die
Live-Version, und darin steckt „Mein Tisch".

---

## Zweiter Patch, ebenfalls offen (08.10.2026)

`scripts/cockpit/patch-launch-reiter.py` baut den **Reiter „Launch" unter
Produkte** ein (Code daneben in `launch-reiter.js` und `launch-reiter.css`).
Vier Blöcke: wo stehe ich · Käufertypen diese Woche · der Fahrplan über die
fünf Phasen · Launches anlegen. Neues Dokument **`daten/launch` — gehört
Patricia**, der Abgleich schreibt dort nie hinein.

**Geprüft ist er**: `node --check` über das JS einzeln und über die ganze
Seite, dann lokal in der Testfassung (`scripts/cockpit/testfassung-bauen.py`,
Port 4381) am Desktop und am Handy, mit einem echten Testlauf — Phase, Zähler,
Preis-Gegenprobe, Käufertyp-Haken, keine Konsolenfehler.

🚨 **Beide Patches hängen an einem einzigen Publish.** Dafür muss die
Live-Fassung einmal ganz gelesen werden (rund 640 KB), sonst lehnt der Server
die Veröffentlichung ab. Das ist eine Ansage wert, keine Nebenbei-Aktion —
deshalb steht es hier und nicht still im Code.

**Befund aus dem eigenen Testlauf:** bei den Preisen des KI-Launches
(199 · 277 · 333) schlägt die Gegenprobe an. Der Schritt vom Secret Offer zum
Frühbucher ist **78**, der zum regulären Preis nur **56** — nach der Methodik
gehört es umgekehrt: vorne klein, hinten gross. Wer früh vertraut, soll den
grössten Abstand zum Normalpreis haben.
