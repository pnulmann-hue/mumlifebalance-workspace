---
tags: [skill, anleitung]
---

# Berufswahl-Kompass — Anleitung

## Was dieser Skill macht

Begleitet einen Jugendlichen ohne klare Richtung über Monate. Fragt konsequent nach Tätigkeiten statt nach Berufen und sammelt Beobachtungen auf fünf Achsen.

Konkret kann er:

- Start-Gespräch
- Kurzer Impuls alle ein bis zwei Wochen
- Erlebnis nachbesprechen
- Richtungen zeigen, sobald genug Beobachtungen da sind
- Eltern-Auswertung zweimal im Jahr

## Was du vorher brauchst

Nichts. Der Skill fragt dich alles ab, was er wissen muss.

## Installation

**Schritt 1 — Ordner kopieren**

Kopiere den kompletten Ordner `berufswahl` an einen dieser beiden Orte:

```
~/.claude/skills/berufswahl/               <- in jedem Projekt verfügbar
DEIN-PROJEKT/.claude/skills/berufswahl/    <- nur in diesem einen Projekt
```

Danach muss es so aussehen:

```
berufswahl/
├── SKILL.md      <- das Herzstück, das Claude liest
└── Anleitung.md  <- diese Datei, nur für dich
```

Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.

> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`

**Schritt 2 — Claude neu starten**

Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.

**Schritt 3 — Platzhalter ersetzen**

- Alle Angaben zur Person liegen bei mir in einem privaten Ordner und werden nicht mitgeliefert — du legst sie neu an
- Die Bildungswege sind für die Schweiz beschrieben. Für ein anderes Land muss dieser Teil neu geschrieben werden

## So rufst du ihn auf

Entweder mit Schrägstrich und Namen:

```
/berufswahl
```

Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:

> „Lass uns die nächste Runde Fragen machen“

## Wenn etwas nicht klappt

| Was du siehst | Woran es liegt | Was du tust |
|---|---|---|
| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |
| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |
| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `berufswahl/` liegen |
| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |
| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |

