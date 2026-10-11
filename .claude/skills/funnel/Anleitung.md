---
tags: [skill, anleitung]
---

# Funnel-Stratege — Anleitung

## Was dieser Skill macht

Plant und baut komplette Funnel: Leadmagnet, Landingpage, Werbeanzeigen, Mailsequenz, Launch und Auswertung.

Konkret kann er:

- Funnel-Strategie
- Funnel bauen
- Werbeanzeigen mit vorheriger Schmerzpunkt-Analyse
- Launch steuern
- Bestehenden Funnel auswerten

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `manychat-keywords.md` | Deine Stichwörter und was sie auslösen. |
| `active-funnels.json` | Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort. |
| `patricia-expertise.md` | Dein Fachwissen: woraus du Mehrwert schöpfst, damit nichts erfunden wird. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- E-Mail-Marketing
- Chat-Automation
- Website
- Checkout-Anbieter

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `funnel` an einen dieser beiden Orte:

```
~/.claude/skills/funnel/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/funnel/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
funnel/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Alle hinterlegten Zugänge sind meine — du brauchst deine eigenen
- `active-funnels.json` komplett durch deine Angebote ersetzen
- Alle Listen- und Automations-Nummern im Skill ersetzen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/funnel
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Lass uns einen Funnel planen“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `funnel/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

