---
tags: [skill, anleitung]
---

# Design-Bauplan — Anleitung

## Was dieser Skill macht

Sagt dir Folie für Folie, was in deine Design-Vorlage kommt. Erzeugt selbst keine Bilder — du arbeitest mit deiner Vorlage und echten Fotos.

Konkret kann er:

- Bauplan für Karussell-Folien
- Cover-Vorschlag
- Standbild für ein Reel

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

**Zugänge, die du brauchst:**

- Ein Design-Programm deiner Wahl

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `visuals` an einen dieser beiden Orte:

```
~/.claude/skills/visuals/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/visuals/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
visuals/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Beim ersten Aufruf fragt der Skill nach deinem Marken-Setup: Farben, Schriften, Vorlagen. Einmal beantworten.

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/visuals
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Mach mir den Bauplan für ein Karussell zu ...“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `visuals/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

