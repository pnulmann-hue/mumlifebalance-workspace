---
name: start
description: "Session-Start — liest Workspace, Kontext und den Stand der letzten Tage, fasst kurz zusammen, was gerade läuft und was ansteht, und fragt dann, woran wir heute arbeiten. Dran bei /start, „starte“, „guten Morgen, leg los“ und am Anfang jeder neuen Session."
---

# /start — die Session beginnt

Löst `/prime` ab (Patricia, 04.10.2026). Herkunft: Ordner-Vorlage aus dem Claude-Kurs
(dort `/start` und `/shutdown` als festes Paar). Gegenstück am Ende: `/shutdown`.

**Ziel:** In zwei Minuten weiss Claude, wer Patricia ist, was in den letzten Tagen
passiert ist und was heute ansteht — ohne dass sie etwas erklären muss.
Lesen, nicht nachfragen. Erst am Schluss eine einzige Frage.

## Schritt 1 · Stand des Repos

```bash
git fetch --quiet
git status --short | head -20
git log --since="3 days ago" --pretty="%ad %s" --date=format:"%d.%m. %H:%M" | grep -v "auto-sync" | head -15
git log --since="3 days ago" --name-only --pretty="" | sort | uniq -c | sort -rn | head -20
ls .git/index.lock 2>/dev/null
```

🚨 Liegt eine `.git/index.lock` herum, **läuft kein auto-sync** (am 16.09. acht Tage
unbemerkt). Melden, nicht selbst löschen — erst prüfen, ob gerade ein Git-Prozess läuft.

Die meisten Commits heissen „auto-sync“ und sagen nichts. Aussagekräftig ist die
**Liste der geänderten Dateien** — daraus ablesen, woran zuletzt gearbeitet wurde.

## Schritt 2 · Kontext lesen

CLAUDE.md und MEMORY.md sind schon geladen. Dazu lesen:

| Datei | Wozu |
|---|---|
| `context/patricia-interview-2026-10.md` | **neuester Stand** über sie und ihr Business — neuer als das Vollprofil |
| `context/business-info.md` | Angebote, Profile, Positionierung |
| `context/strategy.md` | Ziele und Prioritäten |
| `context/personal-info.md` | Rolle, Familie, Rahmen |

`context/patricia-vollprofil.md` (über 100 KB) **nicht** beim Start lesen — erst, wenn ein
Kundentext entsteht. Steht bei einer Datei ein Datum, das Monate zurückliegt, das in der
Zusammenfassung sagen (z. B. `current-data.md` vom Mai), statt den Inhalt als aktuell
auszugeben.

## Schritt 2b · Aufträge von PIA (seit 08.10.2026)

Im Cockpit nimmt PIA Aufträge an Claude entgegen. Sie liegen in `daten/aufgaben`
(Artifact `eeee48d5-3e50-4cff-8047-1ec5eccbb074`) mit `fuerClaude: true`.
`ArtifactData get` auf `daten/aufgaben`, alle offenen mit `fuerClaude` herausziehen
und in der Zusammenfassung **zuerst** nennen („PIA hat für dich hinterlegt: …“).
Nicht selbst abhaken — erst wenn ein Auftrag wirklich erledigt ist und Patricia es
sieht, `erledigt: true` + `erledigt_am` setzen.

## Schritt 3 · Was ansteht

- Heutiges Datum und Wochentag **ausrechnen**, nie raten.
- In CLAUDE.md und den zuletzt geänderten Plänen (`plans/`, neueste zuerst) nach
  Terminen der nächsten 14 Tage suchen (Launch, Masterclass, Ferien, Fristen) und
  nach Zeilen mit **⚠️ Offen**.
- Der Scheduled-Task-Rhythmus steht in CLAUDE.md (Fr 08:00 Content, 19:30 Kommentare,
  20:00 Freigaben, 06:15 Abgleich) — erwähnen, was heute davon läuft.

## Schritt 4 · Zusammenfassung — kurz

Höchstens rund 15 Zeilen, auf Deutsch, mit Schweizer ss:

1. **Heute:** Datum, Wochentag, was heute automatisch läuft
2. **Zuletzt gearbeitet an:** zwei, drei Punkte aus Schritt 1
3. **Steht an:** Termine der nächsten 14 Tage
4. **Offen:** was liegengeblieben ist (höchstens fünf Punkte)
5. Falls etwas klemmt (Lock-Datei, veraltete Kontextdatei, Repo zurück): eine Zeile

Dann **eine** Frage: *„Woran arbeiten wir heute?“* — und gegebenenfalls einen
Vorschlag, was am meisten bringt (der Engpass steht bei `/strategie`).

## Regeln

- **Nichts ändern, nichts committen, nichts löschen.** `/start` liest nur.
- Keine Liste aller Skills herunterbeten — die stehen in CLAUDE.md.
- Wenn etwas nicht zu finden ist, das sagen, statt es zu erfinden.
