---
tags: [skill, anleitung]
---

# Gartenassistent — Anleitung

## Was dieser Skill macht

Berater für deinen Garten: was jetzt ansteht, was neben was gepflanzt wird, was in deiner Höhenlage noch geht.

Konkret kann er:

- Was steht diese Woche an
- Beetplanung mit Mischkultur
- Aussaat- und Pflanzzeiten
- Fruchtfolge über Jahre

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

**Zugänge, die du brauchst:**

- Optional: Datenbank für Samen, Beete und Tagebuch

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `garten` an einen dieser beiden Orte:

```
~/.claude/skills/garten/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/garten/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
garten/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Standort, Höhenlage und Klima ersetzen — meine Angaben passen nur zu meinem Garten
- Deine Beete und Dauerkulturen eintragen
- Datenbank-Kennungen ersetzen oder den Abschnitt streichen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/garten
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Was steht diese Woche im Garten an?“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `garten/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

