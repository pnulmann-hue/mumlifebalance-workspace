---
tags: [skill, anleitung]
---

# Caption-Schreiber — Anleitung

## Was dieser Skill macht

Schreibt dir eine fertige Instagram-Caption in deiner Stimme — mit Zeitanker, einer echten Zahl und genau einer Handlungsaufforderung.

Konkret kann er:

- Caption aus einer groben Idee oder einem Hook bauen
- Bestehende Caption überarbeiten
- Handlungsaufforderung auf dein Stichwort setzen

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `caption-formeln.md` | Deine Caption-Baupläne und Handlungsaufforderungen. |
| `patricia-expertise.md` | Dein Fachwissen: woraus du Mehrwert schöpfst, damit nichts erfunden wird. |
| `patricia-freebies.md` | Deine Gratis-Angebote mit Inhalt — damit im Text darauf Bezug genommen werden kann. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `caption` an einen dieser beiden Orte:

```
~/.claude/skills/caption/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/caption/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
caption/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- In `brand-voice.md` deine eigene Stimme und deine Wortverbote eintragen
- In `caption-formeln.md` deine Caption-Baupläne hinterlegen
- Dein Kommentar-Stichwort setzen — im Skill steht als Beispiel eines von mir

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/caption
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Schreib mir eine Caption zu diesem Hook: ...“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `caption/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

