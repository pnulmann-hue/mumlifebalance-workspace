---
tags: [skill, anleitung]
---

# Monats-Hook-Planer — Anleitung

## Was dieser Skill macht

Macht dir Hook-Vorschläge für einen ganzen Monat — abwechselnd über die Beitragstypen und passend zur Launch-Phase.

Konkret kann er:

- Hooks für vier Wochen auf einmal
- Abwechslung über die Beitragstypen erzwingen
- Auf eine laufende Verkaufsphase abstimmen

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `hook-master-liste.md` | Dein Vorrat an bewährten Roh-Hooks zum Zuschneiden. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `monats-hooks` an einen dieser beiden Orte:

```
~/.claude/skills/monats-hooks/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/monats-hooks/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
monats-hooks/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Deine Marktanalyse und deinen Monatsfokus bereithalten — der Skill baut darauf auf
- `hook-master-liste.md` mit deinen Hooks füllen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/monats-hooks
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Mach mir die Hooks für den nächsten Monat“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `monats-hooks/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

