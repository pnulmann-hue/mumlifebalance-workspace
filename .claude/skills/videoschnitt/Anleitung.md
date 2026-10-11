---
tags: [skill, anleitung]
---

# Video-Rohschnitt — Anleitung

## Was dieser Skill macht

Du sprichst dein Material in einem Stück in die Kamera, mit Versprechern und Wiederholungen. Der Skill macht daraus den Rohschnitt nach deinen Regeln, setzt Untertitel und Textebenen.

Konkret kann er:

- Material abtippen mit Wortzeitstempeln
- Schnittliste vorlegen und freigeben lassen
- Rohschnitt und Einzelclips
- Wortgenaue Untertitel
- Textebene und automatische Zooms

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `videoschnitt-regeln.md` | Deine Schnittregeln: welcher Take gewinnt, wie viel Luft vor einem Satz, was unantastbar ist. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Hilfsprogramme, die mitkopiert werden müssen:**

- Drei Schnitt-Programme, die mitgeliefert werden müssen

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `videoschnitt` an einen dieser beiden Orte:

```
~/.claude/skills/videoschnitt/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/videoschnitt/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
videoschnitt/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- `videoschnitt-regeln.md` mit deinen eigenen Schnittregeln füllen — das ist das Herz
- Die Programme im Ordner `scripts/videoschnitt/` müssen mitkopiert werden
- Einmalig die Abhängigkeiten installieren — steht in der README im Programm-Ordner

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/videoschnitt
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Schneide mir das Video in video/input/“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `videoschnitt/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

