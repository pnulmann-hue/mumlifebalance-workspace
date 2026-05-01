---
description: Master-Jahresplanung — alle Produkte/Launches/Aktivitäten in einer Sicht. Liest und schreibt context/jahresplan-2026.md, syncs mit Notion-Jahresplanung-DB. Wird von /montag, /reels, /karussell gelesen für Wochen-Kontext.
---

# /jahresplan — Master-Jahresplanung für Mum Life Balance

**Skill-Status:** SPEC (zu bauen ab nächster Session)
**Master-Datei:** `context/jahresplan-2026.md` (TBD — wird vom Skill erstellt)
**Phase-Tracker:** `context/active-funnels.json` (existiert, wird parallel gepflegt)
**Notion-DB:** TBD (Patricia liefert DB-ID beim ersten Lauf)

---

## Was dieser Skill macht

Der `/jahresplan`-Skill ist die **EINE Wahrheit** für „Wann passiert was im Jahr". Er aggregiert alle Launches, Produkte, Kampagnen und parallel laufenden Aktivitäten (Mentoring + doTERRA) in einer Tag-für-Tag-Sicht.

**Datenfluss:**

```
/produkt erstellt outputs/produkte/[slug]/07-launch-kalender.md
        ↓
/jahresplan launch [slug]  →  fügt Launch-Phasen ins Master-Markdown
        ↓
context/jahresplan-2026.md  ←→  Notion-Jahresplanung-DB
        ↓
/montag · /reels · /karussell lesen Master + active-funnels.json
        ↓
Content-Skills wissen Tagesgenau, wo wir stehen
```

---

## 5 Modi

### Modus 1 — `/jahresplan status`

**Zweck:** „Wo stehe ich heute?"

Liest:
- `context/jahresplan-2026.md` für Wochen-Kontext
- `context/active-funnels.json` für aktuelle Phasen
- Datums-Logik aus aktuellem System-Datum

Antwortet mit:
- Aktuelle KW + Tag
- Alle parallel laufenden Produkte/Launches mit Phasen
- Diese Woche zu erledigen (aus active-funnels.json `phase_history`)
- Nächste Meilensteine (nächsten 14 Tage)

**Beispiel-Output:**
```
KW 19, Donnerstag 8.5.2026

PARALLEL AKTIV:
- Mama-CEO: Pre-Launch W1 Validierung (bis 8.5.) → ab Fr W2 Anwarming
- Bio-Check: Pilot-Phase Tag 14 → Retargeting möglich
- doTERRA: keine aktive Kampagne

NÄCHSTE MEILENSTEINE:
- 9.5.: Mama-CEO Pre-Launch W2 startet (Sales-Page-Bau)
- 16.5.: Mastermind-Anmelde-Page live
- 22.5. 09:00: Mama-CEO CART-OPEN
- 26.5. 09:00: KI-MASTERMIND LIVE
```

### Modus 2 — `/jahresplan launch [produkt-slug]`

**Zweck:** Neuen Launch in Master-Markdown eintragen

Liest:
- `outputs/produkte/[slug]/07-launch-kalender.md` (alle Phasen + Daten)
- `outputs/produkte/[slug]/00-briefing-FINAL.md` (Tagline + Preise)

Schreibt:
- Phasen ins `context/jahresplan-2026.md` (Monats-Tabelle + Tages-Detail)
- Markiert Konflikte mit existierenden Launches (Cart-Open-Überlappungen)

Fragt User:
- Soll Notion-DB-Eintrag synchron erstellt werden? (ja/nein)
- Konflikt mit Bio-Check-Pilot-Phase 22.-29.5.? (Lösungsvorschlag: Bio-Check pausieren)

### Modus 3 — `/jahresplan vorschau [monat]`

**Zweck:** Monats-Sicht — was kommt im Juni/Juli/etc.?

Liest:
- `context/jahresplan-2026.md`

Antwortet mit:
- Monats-Übersicht-Tabelle (Wochen-Spalten × Produkt-Zeilen)
- Konflikte/Überlappungen
- Ruhige Phasen (gut für Nesting/Audit/Pause)
- Empfohlene Next-Actions für Pre-Launch nächster Produkte

### Modus 4 — `/jahresplan konflikt-check`

**Zweck:** Überlappende Aktivitäten identifizieren

Prüft:
- Cart-Open-Phasen aus active-funnels.json (alle Produkte)
- Live-Events (Webinar/Mastermind/Challenge)
- Patricia-Kapazität (z.B. „Patricia kann nicht 2 Live-Calls am gleichen Tag")

Antwortet mit:
- Liste aller Konflikte (Datum + Produkte)
- Lösungsvorschläge (verschieben, parallel laufen lassen, eines pausieren)

### Modus 5 — `/jahresplan notion-sync`

**Zweck:** Manueller Sync mit Notion-Jahresplanung-DB

Liest:
- `context/jahresplan-2026.md` (Quelle)
- Notion-DB-ID (aus User-Input oder gespeicherter Konfig)

Schreibt:
- Neue/aktualisierte Pages in Notion-Jahresplanung-DB
- Verknüpfungen zu Notion-Produkte-DB
- Updated `_meta.last_sync_with_notion` in Master-Markdown

---

## Datei-Struktur `context/jahresplan-2026.md` (zu erstellen)

```markdown
# Jahresplan 2026 — Master-Sicht Mum Life Balance

**Stand:** 2026-05-XX
**Letzte Aktualisierung:** [Datum]
**Quelle der Wahrheit:** Diese Datei + `active-funnels.json`
**Notion-Sync:** [Datum + DB-Link]

## Q1 (Jan-Mrz) — RÜCKBLICK
[Zusammenfassung: was lief, was Lehre gezogen]

## Q2 (Apr-Jun) — AKTIV
### April 2026
[Bio-Check Launch]

### Mai 2026
**Hauptfokus:** Mama-CEO Pilot-Launch
**Mit Bio-Check parallel** (Tag 8-30 Pilot-Phase)

#### KW 19 (2.-8.5.)
| Tag | Mama-CEO | Bio-Check | doTERRA | Notes |
|---|---|---|---|---|
| Do 2.5. | Story-Umfrage Tagline-A/B | Tag 8 | — | Beide Profile aktiv |
| Fr 3.5. | Urmotiv-Call #1 | — | — | |
[...]

#### KW 22 (Launch-Week)
[...]

### Juni 2026
[Premium 1:1 Strategie-Skill aufsetzen, Säule-3-Pilot läuft, Säule 4-Aufnahmen]

## Q3 (Jul-Sep) — GEPLANT
[Mama-CEO Final-Launch September, Säulen-Auslieferung Pilot]

## Q4 (Okt-Dez) — VORLÄUFIG
[Premium 1:1 Launch, Minikurse extrahieren]
```

---

## Wie andere Skills den Jahresplan nutzen

### `/montag` (Wochen-Content)

Liest beim Start:
1. `context/jahresplan-2026.md` für Wochen-Kontext
2. `context/active-funnels.json` für Phase-Marker
3. Antwortet: „Diese Woche ist Mama-CEO Pre-Launch W2 + Bio-Check Tag 11. Empfohlene Pillars: Brandastic-Story (Mama-CEO) + Retargeting-Bio-Tipps (Bio-Check)."

### `/reels` und `/karussell`

Lesen optional auf User-Befehl: „Schau in den Jahresplan und gib mir 3 Reel-Ideen für die kommende Mama-CEO-Pre-Launch-W3."

Liest dann:
1. Master-Datei (Wochen-Plan)
2. active-funnels.json (Pillar pro Phase)
3. Produkt-Briefing für Brand-Bausteine

### `/funnel`

Liest beim Strategie-Modus:
- Master-Datei für Cart-Open-Konflikte
- active-funnels.json für ManyChat-Keyword-Konflikte

---

## Implementierungs-TODO (für nächste Session)

1. **`context/jahresplan-2026.md` v0 anlegen** mit aktuellen Q1-Q2-Daten (Bio-Check + Mama-CEO + doTERRA-Plätze leer)
2. **Skill-Logik in claude-Hooks** integrieren (lesen + schreiben automatisiert)
3. **Notion-DB-ID** von Patricia holen — welche existiert (Jahresplanung)?
4. **Notion-Sync-Mechanismus** definieren (push vs. pull, manuell vs. automatisch)
5. **CLAUDE.md** updaten (Skill in Commands-Sektion ergänzen)
6. **Stop-Hook erweitern** (`stop-hook-git-check.sh`) — bei Master-Datei-Änderungen Notion-Sync vorschlagen

---

## Patricia-Hinweise

- Du musst NICHTS manuell synchronisieren — Skills lesen automatisch
- Wenn du dem Content-Assistenten sagen willst „schau in den Jahresplan", reicht das — die Skills wissen wo
- Notion-Update läuft via `/jahresplan notion-sync` (manuell, einmal pro Woche)
- Konfliktwarnung: bevor du `/produkt launch` machst, läuft auto-Konflikt-Check

---

**Status:** Skill-Spec, Implementierung erfolgt in nächster Session sobald Patricia die Notion-Jahresplanung-DB-ID liefert.
