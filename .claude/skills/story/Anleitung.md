---
tags: [skill, anleitung]
---

# Story-Begleiter — Anleitung

## Was dieser Skill macht

Täglicher Begleiter für Instagram-Stories. Jede Sequenz bekommt eine Handlungsaufforderung, und über die Woche werden alle Käufertypen bedient.

Konkret kann er:

- Tagesplan mit drei bis fünf Slides
- Kompletter Verkaufstag während eines Launches
- Aus einer rohen Idee eine Story-Struktur
- Ein-Slide-Tag für wenig Zeit
- Story-Serie über mehrere Tage

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `caption-formeln.md` | Deine Caption-Baupläne und Handlungsaufforderungen. |
| `active-funnels.json` | Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort. |
| `content-formel-5-typen.md` | Deine Beitragstypen und wie sie sich über die Woche verteilen. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Optional: Planungs-Datenbank

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `story` an einen dieser beiden Orte:

```
~/.claude/skills/story/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/story/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
story/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Kontextdateien mit deinen Inhalten füllen
- Deine Angebote in `active-funnels.json` eintragen
- Datenbank-Kennung im Skill ersetzen oder den Abschnitt streichen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/story
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Was poste ich heute in die Story?“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `story/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

