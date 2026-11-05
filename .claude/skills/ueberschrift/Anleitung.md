---
tags: [skill, anleitung]
---

# Überschriften-Schreiber — Anleitung

## Was dieser Skill macht

Schreibt die Hauptüberschrift deiner Verkaufsseite: im Imperativ, mit einer Zahl, mit dem Leben danach statt dem Kursinhalt und mit einem Bild, das neugierig macht. Prüft jede Überschrift, bevor sie zu dir kommt.

Konkret kann er:

- Fünf Überschriften aus verschiedenen Blickwinkeln mit Vorzeile und Unterzeile
- Bestehende Überschrift prüfen und neu schreiben
- Passende Hook-Fassungen und Betreffzeilen auf Wunsch

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `kern-painpoint.md` | Dein Hintergrundwissen zu diesem Thema. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Hilfsprogramme, die mitkopiert werden müssen:**

- Das Prüfskript scripts/cockpit/texte-pruefen.py

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `ueberschrift` an einen dieser beiden Orte:

```
~/.claude/skills/ueberschrift/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/ueberschrift/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
ueberschrift/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Die Beispiele im Skill durch deine eigenen Lieblings-Überschriften ersetzen
- Das durchgerechnete Beispiel gegen eines deiner Angebote tauschen
- Die Pfade zu Bauplan und Kontextdateien auf deinen Ordner setzen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/ueberschrift
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Schreib mir die Überschrift für meine Verkaufsseite zu ...“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `ueberschrift/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

