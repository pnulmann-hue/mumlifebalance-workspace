---
tags: [skill, anleitung]
---

# Monats-Content-Stratege — Anleitung

## Was dieser Skill macht

Führt dich in vier Schritten durch die Monatsplanung: Marktcheck, Monatsfokus, Content-Plan, Dreh-Liste. Nach jedem Schritt wird angehalten und du gibst frei.

Konkret kann er:

- Markt und Zielgruppe prüfen
- Monatsfokus festlegen
- Beitragsplan für vier Wochen
- Dreh-Liste zum Abfilmen an einem Tag

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `content-monat` an einen dieser beiden Orte:

```
~/.claude/skills/content-monat/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/content-monat/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
content-monat/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Nichts Festes — der Skill fragt dich alles ab. Je besser deine Antworten, desto besser der Plan.

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/content-monat
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Lass uns den nächsten Monat planen“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `content-monat/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

