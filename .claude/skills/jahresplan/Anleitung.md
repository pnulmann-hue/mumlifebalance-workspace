---
tags: [skill, anleitung]
---

# Jahresplanung — Anleitung

## Was dieser Skill macht

Hält alle Launches, Produkte und Kampagnen eines Jahres in einer Sicht — und warnt, wenn sich zwei Dinge in die Quere kommen.

Konkret kann er:

- Wo stehe ich heute
- Neuen Launch eintragen
- Monatsvorschau
- Konflikte finden

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `active-funnels.json` | Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Optional: Planungs-Datenbank

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `jahresplan` an einen dieser beiden Orte:

```
~/.claude/skills/jahresplan/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/jahresplan/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
jahresplan/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Die Jahresdatei wird beim ersten Lauf angelegt — sie startet leer
- Datenbank-Kennung ersetzen oder den Abschnitt streichen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/jahresplan
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Zeig mir meinen Jahresplan“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `jahresplan/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

