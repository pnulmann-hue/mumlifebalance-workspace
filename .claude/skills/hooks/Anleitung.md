---
tags: [skill, anleitung]
---

# Hook & Kundensprache — Anleitung

## Was dieser Skill macht

Alles über die erste Zeile an einem Ort: wie deine Wunschkundin denkt, welche Formeln bei ihr funktionieren, welche gesperrt sind, und der Check, durch den jeder Hook muss.

Konkret kann er:

- Zehn Hooks über mehrere Angles zu einem Thema
- Bewusstseinsstufe bestimmen und den Hook danach ausrichten
- 22 Formeln und 10 Reveal-Frameworks zuschneiden
- Bestehende Hooks prüfen und reparieren
- Hook-Muster rotieren, damit nicht alles gleich klingt

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `kern-painpoint.md` | Dein Hintergrundwissen zu diesem Thema. |
| `hook-master-liste.md` | Dein Vorrat an bewährten Roh-Hooks zum Zuschneiden. |
| `reichweitenherz-voice-layer.md` | Sprachliche Kniffe, die deine Texte lebendig machen. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Hilfsprogramme, die mitkopiert werden müssen:**

- Das Prüfskript scripts/content/hook-pruefen.py

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `hooks` an einen dieser beiden Orte:

```
~/.claude/skills/hooks/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/hooks/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
hooks/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- `kern-painpoint.md` mit dem Schmerz deiner eigenen Zielgruppe füllen — das ist das Herz
- Themen-Pool und Antagonist-Figuren auf deine Nische umschreiben
- Die Testdaten im Skill sind meine — deine eigenen erst sammeln, dann eintragen
- Das Prüfskript mitkopieren und die Wortlisten darin anpassen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/hooks
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Mach mir zehn Hooks zum Thema ... für ...“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `hooks/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

