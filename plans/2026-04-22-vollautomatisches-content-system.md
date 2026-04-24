# Vollautomatisches Content-System — Masterplan

**Stand:** 2026-04-22
**Status:** Plan-Phase
**Auftrag:** Patricia will ein System das Montag früh 20 Hooks liefert (10 Mentoring + 10 doTERRA), sie wählt 5, Claude baut Caption + Canva-Design, postet automatisch via Blotato, legt in Notion ab, und reposted Best-Performer nach 4 Wochen.

---

## Was schon existiert (= Fundament)

| Baustein | Status | Ort |
|---|---|---|
| `/karussell` Command | ✅ live | `.claude/commands/karussell.md` |
| `/reels` Command | ✅ live | `.claude/commands/reels.md` |
| `/produkt` Command | ✅ live (neu) | `.claude/commands/produkt.md` |
| Hook-Framework + 4 neue Kategorien | ✅ live | `context/hook-framework.md` |
| KI-Phrasen-Blackliste | ✅ Pflicht-Pre-Check | `context/ki-phrasen-blackliste.md` |
| Content-Engine 5 Framework-Docs | ✅ Julia-Trost-Sync integriert | `context/` |
| Notion Content-Management-DB | ✅ verbunden | DB-ID `2ae7078e-8b7e-811a-ad14-000ba5820c09` |
| Canva Master-Template „Vorlage Caude" | ✅ built | Design `DAHHkGW0g1k` |
| Canva-Klon-Flow (find_and_replace auf 27 Texte) | ✅ API-validiert | bewiesen 22.04. |
| HTML→PNG Render-Pipeline (Pfad B) | ✅ läuft | `scripts/karussell-render/` |
| Blotato API-Key + Account-IDs | ✅ in .env | Mentoring 41414, doTERRA 41413 |
| Scheduled-Task-Prompts (als Specs) | ✅ dokumentiert | `reference/scheduled-task-*.md` |
| Zielgruppen-Research Mentoring (10 Pain-Points) | ✅ live | `outputs/zielgruppen-research/mentoring-2026-04-21.md` |
| Zielgruppen-Research doTERRA | ⏳ fehlt noch | TODO |
| Wochen-Fokus-Struktur (welches Produkt wann?) | ⏳ unklar | **→ offene Frage 1** |

---

## Die 4 Pipeline-Phasen (Wochen-Zyklus)

```
┌─────────────────────────────────────────────────────────────┐
│ MO 08:00 — HOOK-LIEFERUNG (Scheduled Task)                  │
│ Deep-Research → 10 Hooks Mentoring + 10 Hooks doTERRA       │
│ synchronisiert mit Produkt-Fokus der Woche                  │
│ → landet in Notion-Board "Wochen-Hooks" + Benachrichtigung  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ MO/DI — PATRICIAS AUSWAHL (Interaktiv)                      │
│ Patricia wählt 5 Hooks aus + setzt Format (Reel/Karussell)  │
│ Chat oder Notion-Checkbox (→ offene Frage 2)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ DI-FR — CLAUDE BAUT CONTENT (pro gewähltem Hook)            │
│ 1. Caption + Hashtags + ManyChat-Keyword                    │
│ 2. Canva-Design aus "Vorlage Caude" klonen + Texte ersetzen │
│ 3. Design in "Claude Designs" → Patricia prüft              │
│ 4. Patricia setzt [OK] im Titel = Freigabe                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ TÄGLICH 07:00 — POSTING-QUEUE (Scheduled Task)              │
│ Check [OK]-Designs → zur Zielgruppen-Zeit via Blotato       │
│ Notion-Eintrag auf Status "Gepostet" + Timestamp            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. MONATS-TAG 08:00 — REPOST-ENGINE (Scheduled Task)        │
│ Best-Performer (Saves+Shares+DMs) identifizieren            │
│ 4 Wochen nach Original → Repost (neue Caption, evtl Cover)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Offene Architektur-Entscheidungen (brauche Input von Patricia)

### Frage 1 — Produkt-Assistent-Sync: Wo steht der Wochen-Fokus?

**Kontext:** Claude muss Montag 08:00 wissen: *„Welches Produkt ist diese Woche im Fokus? Welches Keyword zum Push?"*

**Optionen:**
- **A)** Neue Notion-DB „Launch-Kalender" mit Spalten: Woche-Start, Produkt (Relation), Fokus-Business (M/D), Keyword, Ziel (Sale/Lead)
- **B)** Patricia pflegt einen einfachen Kalender-Eintrag pro Woche manuell (z.B. eine MD-Datei `context/wochen-fokus.md`)
- **C)** `/produkt` Output speichert schon eine Produkttreppe mit Launch-Daten — ich lese das

Meine Empfehlung: **A** (Notion-DB) — weil das auch gut mit der Content-Management-DB verknüpfbar ist und Patricia einen Überblick bekommt.

### Frage 2 — Auswahl-Interface: Wie wählst du die 5 Hooks aus?

**Kontext:** Claude liefert Montag 08:00 die 20 Hooks. Patricia wählt 5 aus + Format.

**Optionen:**
- **A)** Notion-Board mit Checkboxen pro Hook (+ Select-Feld für Reel/Karussell) — voll visuell, persistent, mobil nutzbar
- **B)** Chat-basiert: Claude postet die 20 Hooks, Patricia schreibt: „Nimm 2, 5, 8, 11, 14 — 2 als Reel, rest Karussell"
- **C)** Mini-Webapp (overkill)

Meine Empfehlung: **A** (Notion). Konsistent mit deiner sonstigen Arbeitsweise, mobil nutzbar, Claude kann den Status über Notion-API lesen.

### Frage 3 — Posting-Frequenz: „Jeden Tag für jedes Business" vs. 5 Hooks/Woche?

**Kontext:** Du sagst „jeden Tag für jedes Business posten" = 2×7 = 14 Posts/Woche. Aber „5 Hooks/Woche aus 10" = nur 5 neue Posts/Business.

**Mögliche Interpretationen:**
- **A)** Wirklich täglich 2 neue Posts (14/Woche) → du wählst 7 pro Business, nicht 5
- **B)** 5 neue + 2 aus Archiv-Recycling pro Business pro Woche = 7/Business = 14/Woche
- **C)** 5 Feed-Posts + Storys täglich (Storys sind extra)
- **D)** Weniger als täglich — vielleicht nur 3-5×/Woche pro Business

Meine Empfehlung: **B** (Neu + Recycling). Julia-Trost-Sync hat gezeigt: Wiederholung ist Pflicht, nicht Fehler. 5 Neue + 2 Top-Performer-Reposts/Woche/Business ist realistisch.

### Frage 4 — Deep-Research-Tiefe vs. Geschwindigkeit

**Kontext:** Claude soll KI-Welt + Google + alle Social-Medien durchsuchen nach aktuellen Pain-Points.

**Realität:** Das sind 20-40 WebSearches und AI-Abfragen. Braucht 10-20 Minuten jeden Montag.

**Optionen:**
- **A)** Volle Tiefe jeden Montag (Zeit egal, weil automatisiert)
- **B)** Tiefe Research einmal monatlich → speichert Pain-Point-Datenbank → wöchentlich nur neue Trends draufsetzen (viel schneller, weniger Redundanz)

Meine Empfehlung: **B** (Monatliche tiefe Research + Wöchentliche Trend-Updates). Pain-Points ändern sich nicht jede Woche; Trends schon.

### Frage 5 — Canva-Duplizieren: Wie genau?

Wir haben das vorhin als offene Frage gelassen. Drei Lösungsvarianten:

- **A)** Chrome-UI klickt „Kopie erstellen" (1 Klick via MCP, fragil)
- **B)** 7-10 „Arbeitskopien" als feste Slots (du machst sie einmal, Claude überschreibt sie rollierend)
- **C)** Export→Import-Roundtrip (sauber aber verliert native Editierbarkeit)

Meine Empfehlung: **B** (feste Slots). Du legst 10 Kopien von „Vorlage Caude" an („Vorlage W01", „Vorlage W02", …). Claude überschreibt jede Woche die entsprechenden Slots. Alte Inhalte werden beim Überschreiben verworfen. Robust, null Duplizier-Logik.

---

## Bau-Reihenfolge (falls du grünes Licht für die Empfehlungen gibst)

**Woche 1 (diese):**
1. Notion-DB „Launch-Kalender" erstellen + erste 4 Wochen eintragen
2. doTERRA-Zielgruppen-Research durchführen (parallel zu Mentoring-Research)
3. Montags-Engine aktualisieren: `reference/scheduled-task-montags-engine.md` erweitert mit Produkt-Sync

**Woche 2:**
4. Notion-Auswahl-Board bauen + Claude's Read-Flow
5. Klon-Flow produktiv (Canva-API integriert in `/karussell` + `/reels`)
6. Caption-Generator der aus Hook + Format + Wochen-Fokus die ganze Caption baut

**Woche 3:**
7. Blotato-Integration: Daily-Posting-Queue scharf schalten
8. Notion-Logging (jeder Post bekommt Eintrag mit Metriken-Trackfeldern)

**Woche 4:**
9. Monats-Repost scharf schalten (nutzt die 4 Wochen Metrik-Daten aus Schritt 8)
10. End-to-End-Test mit einem Wochenplan

---

## Kritischer Punkt — Scheduled Tasks + Claude-Session

Das ist ein technisches Detail, aber wichtig:

**Claude braucht eine laufende Session** um MCP-Tools zu nutzen (Canva, Notion, Blotato). Die „Scheduled Tasks" die bisher als `reference/scheduled-task-*.md` dokumentiert sind, sind Prompts die eine Claude-Session triggern müssen.

Lösungen:
- **Option X — MCP Scheduled Tasks** (`mcp__scheduled-tasks__create_scheduled_task`) — läuft Claude automatisch zu definierter Zeit
- **Option Y — `schedule` Skill** (`/schedule` mit Cron-Pattern)
- **Option Z — Telegram-Bot-ähnlich** — eigener Prozess der zur Zeit eine Claude-API-Anfrage macht

Ich empfehle **Option X oder Y** — beides ist im Workspace schon verfügbar.

---

## Mein Vorschlag zum Weiterfahren

**Heute noch (dauert 15 Min Gespräch):**
1. Du bestätigst/korrigierst meine Empfehlungen zu Frage 1-5
2. Ich starte mit dem doTERRA-Research im Hintergrund (parallel)
3. Ich lege die Notion-DB „Launch-Kalender" an (wenn du „A" sagst)

**Morgen:**
4. Montags-Engine erweitern
5. Erste Test-Hook-Lieferung für die kommende Woche

Was denkst du?
