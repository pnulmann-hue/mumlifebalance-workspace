---
tags: [skill, anleitung]
---

# Content-Maschine — Anleitung

## Was dieser Skill macht

Schreibt den kompletten Content für eine Woche oder einen Monat — Marktcheck, Hooks, Reels, Karussells, Captions, Design-Bauplan und den passenden Story-Bogen. Liest deine Planung und baut alles darauf auf.

Konkret kann er:

- Marktcheck: was beschäftigt deine Zielgruppe gerade, mit Zitat und Quelle
- Hooks über den Hook-Skill, geprüft und auf deine Sprache zugeschnitten
- Fertige Reels und Karussells samt Captions
- Story-Bogen, der an die Beiträge anknüpft
- Dreh-Liste zum Abfilmen an ein, zwei Tagen (beim Monat)
- Läuft auf Wunsch automatisch als geplanter Auftrag

## Was du vorher brauchst

Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:

| Datei | Was hineingehört |
|---|---|
| `brand-voice.md` | Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir. |
| `ki-phrasen-blackliste.md` | Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen. |
| `patricia-vollprofil.md` | Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest. |
| `business-info.md` | Deine Positionierung: was du anbietest, für wen, was dich unterscheidet. |
| `caption-formeln.md` | Deine Caption-Baupläne und Handlungsaufforderungen. |
| `patricia-expertise.md` | Dein Fachwissen: woraus du Mehrwert schöpfst, damit nichts erfunden wird. |
| `patricia-freebies.md` | Deine Gratis-Angebote mit Inhalt — damit im Text darauf Bezug genommen werden kann. |
| `active-funnels.json` | Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort. |
| `job-saeulen.md` | Welchen Job ein Beitrag hat: Autorität, Geschichte, Reichweite oder Verkauf. |
| `content-formel-5-typen.md` | Deine Beitragstypen und wie sie sich über die Woche verteilen. |

> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.

> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.

**Zugänge, die du brauchst:**

- Optional: Planungs-Datenbank
- Optional: Auto-Posting-Dienst
- Optional: Messenger für die Benachrichtigung

**Hilfsprogramme, die mitkopiert werden müssen:**

- Der Hook-Skill (wird mitgeliefert oder ersetzt)
- Optional: Render- und Schnitt-Programme

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `content` an einen dieser beiden Orte:

```
~/.claude/skills/content/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/content/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
content/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Alle Kontextdateien mit deinen eigenen Inhalten füllen — ohne sie wird der Output generisch
- Deine Angebote und Stichwörter eintragen, sonst wird auf meine verwiesen
- Die Ordnerpfade zu deinem Bildmaterial anpassen
- Datenbank-Kennungen und Posting-Zugänge ersetzen oder die Abschnitte streichen
- Die Testzahlen im Skill sind meine — deine eigenen erst sammeln, dann eintragen

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/content
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Bau mir den Content für nächste Woche“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `content/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

