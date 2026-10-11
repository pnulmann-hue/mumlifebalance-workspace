---
tags: [skill, anleitung]
---

# Blog-Schreiber — Anleitung

## Was dieser Skill macht

Schreibt einen suchmaschinen-optimierten Blogartikel zu deinem Monatsthema — und daraus gleich Stories, Karussell, Reel und Newsletter.

Konkret kann er:

- Artikel-Konzept
- Kompletter Artikel
- Bestehenden Artikel aktualisieren
- Aus einem Artikel weiteren Content ableiten

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `hook-framework.md` | Deine Hook-Regeln: welche Einstiege funktionieren, welche verboten sind. |
| `active-funnels.json` | Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Website mit Blog
- Optional: Planungs-Datenbank

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `blog` an einen dieser beiden Orte:

```
~/.claude/skills/blog/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/blog/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
blog/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Kontextdateien füllen
- Deine Website-Adresse und deine internen Links im Skill ersetzen
- Datenbank-Kennungen ersetzen oder streichen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/blog
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Schreib mir den Blogartikel zum Monatsthema“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `blog/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

