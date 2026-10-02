---
tags: [skill, anleitung]
---

# Sales-Page-Texter — Anleitung

## Was dieser Skill macht

Führt ein Interview zu deinem Angebot und liefert dir dreizehn fertige Textblöcke zum Einsetzen in deine Verkaufsseite.

Konkret kann er:

- Interview zu Angebot, Zielgruppe, Verwandlung, Modulen
- Dreizehn Textblöcke zum Kopieren
- Häufige Fragen samt Antworten

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Ein Checkout-Anbieter deiner Wahl

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `salespage` an einen dieser beiden Orte:

```
~/.claude/skills/salespage/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/salespage/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
salespage/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- `patricia-vollprofil.md` durch dein eigenes Profil ersetzen
- Im Skill-Text wird eine fremde Methodik namentlich genannt — vor der Weitergabe entfernen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/salespage
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Bau mir die Sales-Page für mein Angebot ...“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `salespage/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

