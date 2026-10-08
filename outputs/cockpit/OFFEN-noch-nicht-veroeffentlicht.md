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
