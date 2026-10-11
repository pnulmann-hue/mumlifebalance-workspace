---
tags: [skill, anleitung]
---

# Material-Abholer — Anleitung

## Was dieser Skill macht

Holt neue Fotos und Videos aus einem festen Album auf deinem Handy und sortiert sie ein. Auf dem Handy wird nichts gelöscht.

Konkret kann er:

- Videos und Fotos abholen
- Standbild je Video erzeugen, damit der Inhalt sichtbar ist
- Bericht schreiben, was neu ist

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

**Zugänge, die du brauchst:**

- Handy-Verbindung zum Rechner

**Hilfsprogramme, die mitkopiert werden müssen:**

- Ein Abhol-Programm

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `handy` an einen dieser beiden Orte:

```
~/.claude/skills/handy/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/handy/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
handy/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Den Album-Namen auf deinen ändern
- Den Verbindungspfad zum Handy anpassen — meiner ist gerätespezifisch
- Das Programm aus `scripts/handy/` mitkopieren

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/handy
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Hol mein neues Material vom Handy“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `handy/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

