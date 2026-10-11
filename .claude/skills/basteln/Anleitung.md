---
tags: [skill, anleitung]
---

# Bastel-Assistent — Anleitung

## Was dieser Skill macht

Hält Überblick über dein Bastelmaterial und schlägt nur Projekte vor, die du aus dem vorhandenen Bestand machen kannst.

Konkret kann er:

- Was schenke ich dieser Person
- Material per Foto erfassen
- Anlass rechtzeitig vorbereiten
- Verpackung bauen
- Bastel-Nachmittag planen

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

**Hilfsprogramme, die mitkopiert werden müssen:**

- Zwei Suchprogramme für den Materialbestand

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `basteln` an einen dieser beiden Orte:

```
~/.claude/skills/basteln/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/basteln/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
basteln/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Die Inventar-Dateien sind meine — sie müssen durch deine ersetzt werden, sonst schlägt der Skill Material vor, das du nicht hast
- Der Pfad zu deinem digitalen Material muss angepasst werden
- Die Anlass-Liste mit Namen und Geburtstagen ist bei mir privat und wird nicht mitgeliefert

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/basteln
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Was kann ich für ... basteln?“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `basteln/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

