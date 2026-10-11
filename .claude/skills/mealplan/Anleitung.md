---
tags: [skill, anleitung]
---

# Kochassistent — Anleitung

## Was dieser Skill macht

Plant Wochenessen für deine Familie, hilft beim Spontan-Kochen aus dem was da ist und schreibt die Einkaufsliste.

Konkret kann er:

- Wochenplan Mittag und Abend
- Was koche ich aus diesen Zutaten
- Einkaufsliste nach Laden sortiert
- Vorkochen und Projekte
- Rezept aus einem Foto archivieren

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `meal-planning-bot.md` | Dein Koch-Briefing: Personenzahl, Vorlieben, Unverträglichkeiten, Einkaufsladen. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Optional: eigene Rezept-Datenbank

**Hilfsprogramme, die mitkopiert werden müssen:**

- Optional: Abfrage-Programm für die Rezept-Datenbank

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `mealplan` an einen dieser beiden Orte:

```
~/.claude/skills/mealplan/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/mealplan/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
mealplan/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- `meal-planning-bot.md` komplett neu schreiben: Personenzahl, Vorlieben, Unverträglichkeiten, dein Einkaufsladen
- Die Rezept-Datenbank ist meine und wird nicht mitgeliefert — der Skill funktioniert auch ohne, schlägt dann aber keine Rezepte aus dem Bestand vor

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/mealplan
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Mach mir den Wochenplan“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `mealplan/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

