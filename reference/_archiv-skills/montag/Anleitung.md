---
tags: [skill, anleitung]
---

# Wochen-Build — Anleitung

## Was dieser Skill macht

Baut die Karussells und Reel-Cover für die kommende Woche und plant sie ein. Ersatzweg, wenn der automatische Freitag-Lauf nicht durchlief.

Konkret kann er:

- Fünf Beiträge je Profil bauen
- Cover rendern
- Für die Woche einplanen

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `content-formel-5-typen.md` | Deine Beitragstypen und wie sie sich über die Woche verteilen. |
| `job-saeulen.md` | Welchen Job ein Beitrag hat: Autorität, Geschichte, Reichweite oder Verkauf. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Auto-Posting-Dienst
- Design-Programm

**Hilfsprogramme, die mitkopiert werden müssen:**

- Render-Pipeline

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `montag` an einen dieser beiden Orte:

```
~/.claude/skills/montag/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/montag/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
montag/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Der Skill greift auf meine Render-Pipeline und meinen Posting-Dienst zu — beides brauchst du selbst
- Bildordner-Pfade ersetzen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/montag
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Bau mir den Content für nächste Woche“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `montag/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

