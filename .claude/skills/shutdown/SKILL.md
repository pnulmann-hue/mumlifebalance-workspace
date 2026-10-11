---
name: shutdown
description: "Session sauber beenden — Workspace prüfen, harmlosen Müll wegräumen, CLAUDE.md, Kontext und Gedächtnis nachziehen, Obsidian-Index pflegen, committen und pushen, kurzer Bericht und Verabschiedung. Dran bei /shutdown, „Feierabend“, „wir hören auf“, „mach zu“."
---

# /shutdown — die Session endet

Gegenstück zu `/start`. Herkunft: Ordner-Vorlage aus dem Claude-Kurs, angepasst an
diesen Workspace (04.10.2026). Die Schritte der Reihe nach, keinen überspringen.

**Der Aufruf von `/shutdown` ist der Auftrag zum Committen und Pushen.** Sonst wird in
diesem Workspace nur auf ausdrücklichen Wunsch committet.

## Schritt 1 · Was hat sich in dieser Session getan?

```bash
git status --short
git diff --stat
```

Daraus und aus dem Gesprächsverlauf eine Liste: neue Dateien, geänderte Dateien,
neue Skripte, Skills, Scheduled Tasks, Artifacts.

## Schritt 2 · Aufräumen — nur das Eindeutige

Löschen darf Claude nur, was **sicher Müll** ist:

- `__pycache__/`, `*.pyc`, `.DS_Store`
- `*.tmp`, `*.bak` und eigene Zwischendateien **aus dieser Session** im Workspace
  (Zwischenstände gehören ins Scratchpad, nicht in den Workspace)

🚨 **Alles andere wird nicht gelöscht**, auch wenn es verwaist aussieht — es kommt als
Frage in den Bericht. Nie etwas in `video/`, `context/persoenlich/`, `outputs/finanzen/`,
`outputs/cockpit/abgleich/` oder den Download-Ordnern anfassen. Löschen ist
Patricias Entscheidung.

## Schritt 3 · CLAUDE.md nachziehen

Für jede Änderung aus Schritt 1 die vier Fragen aus „Kritische Anweisung: Diese Datei
pflegen“: neue Funktion · Struktur geändert · neuer Befehl · braucht `context/` etwas?
Was erledigt ist, aus „⚠️ Offen“ streichen oder als erledigt markieren.
Bestehende Abschnitte ändern statt neue danebenlegen.

## Schritt 4 · Kontext und Gedächtnis

- `context/` — stimmt noch alles mit dem überein, was heute entschieden wurde?
  Neue Entscheidungen von Patricia (Zitat + Datum) dort ablegen, wo sie hingehören.
- Gedächtnis (`MEMORY.md` + Einzeldateien) — neue Korrekturen und bestätigte
  Vorgehensweisen festhalten; bestehende Datei ergänzen statt eine zweite anlegen.

## Schritt 5 · Obsidian

Neue MD-Dateien in `outputs/` brauchen Frontmatter-Tags und einen Eintrag im
`_INDEX.md` des Ordners. Sicherheitsnetz:

```bash
bash scripts/obsidian-reindex.sh
```

## Schritt 6 · Committen und pushen

1. `git status` — was ist noch nicht committet?
   🚨 **Das auto-sync sichert nur `outputs/`, `context/`, `plans/`, `reference/`.**
   Skills (`.claude/skills/`), `scripts/`, `.github/` und `CLAUDE.md` landen nur über
   `/shutdown` auf GitHub. Am 04.10.2026 lagen dort rund 100 Änderungen, die nie
   gesichert waren — ein kaputter PC hätte sie gelöscht.
2. **Alles stagen, was nicht ausgeschlossen ist** (`git add -A`) — `.gitignore` hält
   Schlüssel, Personendaten und Fremdmaterial draussen. Ausnahme: **gelöschte Dateien**
   (`git status` zeigt `D`) nicht mitnehmen, sondern im Bericht nachfragen.
3. **Danach die Gegenprobe**, bevor committet wird — das Repo ist öffentlich:
   `git diff --cached --name-only` durchsehen und
   `git diff --cached | grep -inE "api[_-]?key|secret|sk-[a-z0-9]|bearer |@gmail|@gmx|@bluewin|\+41 ?7"`.
   Bei einem echten Fund die Datei mit `git restore --staged <datei>` wieder herausnehmen,
   in `.gitignore` aufnehmen und im Bericht melden. Gekauftes Fremdmaterial (Julia,
   Kevin, Kursunterlagen) gehört nie dazu.
4. Commit: `Shutdown: <was gemacht wurde>`
5. `git push`. Schlägt es fehl (Lock-Datei, Konflikt), melden statt erzwingen —
   **nie** `--force`, nie `--no-verify`.

## Schritt 7 · Bericht

Kurz, auf Deutsch, Schweizer ss:

1. **Erledigt heute:** was wir gemeinsam geschafft haben
2. **Aufgeräumt / aktualisiert:** welche Dateien
3. **Offen — Fragen an dich:** was Claude nicht allein entscheiden durfte
4. **Nächste Session:** womit es am sinnvollsten weitergeht

## Schritt 8 · Verabschiedung

Persönlich und warm, wie eine gute Kollegin, die Feierabend macht. Kurz sagen, was
heute erreicht wurde, einen schönen Abend wünschen — und auf ihre Antwort warten.
