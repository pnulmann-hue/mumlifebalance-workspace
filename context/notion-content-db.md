# Notion Content-Database — Mapping für Assistenten

**Zweck:** Zentrale Referenz für /reels, /karussell und alle Scheduled Tasks, wie mit den Notion-DBs zu interagieren ist.

---

## DB-IDs (alle im EXPERT BRAIN Teamspace)

| DB / Data Source | ID | URL |
|------------------|-----|-----|
| **Content-Management** (Haupt-DB) | `2ae7078e-8b7e-811a-ad14-000ba5820c09` | https://www.notion.so/2ae7078e8b7e81349e36f8c630a850f2 |
| **Content-Strategie** (Pillars) | `2ae7078e-8b7e-81a3-9f5f-000be0dd8dbc` | https://www.notion.so/2ae7078e8b7e81468f10ec4786130b13 |
| **Content-Plattformen** | `2ae7078e-8b7e-8103-81e2-000b93a36fc7` | https://www.notion.so/2ae7078e8b7e811c9ba7fe9503f0ecc2 |

Zusätzliche Relation-DBs (im Schema von Content-Management referenziert):
- Content-Themenplanung: `collection://2ae7078e-8b7e-81a2-bce1-000b9be1fb40`
- Aufgaben: `collection://2ae7078e-8b7e-81a2-a070-000b54019c80`
- Produkt: `collection://2ae7078e-8b7e-818c-9da2-000b09bae568`
- Mediathek: `collection://2ae7078e-8b7e-810f-a7a9-000b341277a2`

---

## Content-Plattformen — Page-IDs

| Plattform-Name | Page-ID |
|----------------|---------|
| **Instagram Mentoring** (früher „Instagram") | `2ae7078e-8b7e-815e-95ad-d1219851d55c` |
| **Instagram doTERRA** (neu 2026-04-21) | `3497078e-8b7e-8164-8150-feb68e686e29` |
| Facebookgruppe | `2b77078e-8b7e-8015-b55a-e2d85c94fb65` |
| Telegramgruppe | `2b77078e-8b7e-8053-9ce0-eee41dd32635` |

---

## Content-Säulen — Page-IDs

### Mentoring-Säulen (schon existierend, von Patricia)
| Säule | Page-ID |
|--------|---------|
| 1. Positionierung im Networkmarketing 2.0 | `2bd7078e-8b7e-8066-911b-d051a401e3ca` |
| 2. Businessaufbau mit hybriden Einkommensströmen | `2bd7078e-8b7e-80cf-ba1a-e3ec3ff29991` |
| 3. Mindset & Alltag: Mama, Business, Leadership | `2bd7078e-8b7e-802e-8f87-d7df9b4b530c` |
| (Rolle) Persönlichkeit | `2c47078e-8b7e-8012-97b4-f80f91c81cd7` |
| (Rolle) Inspiration | `2c47078e-8b7e-80b5-b578-e46cd64f25c3` |
| (Rolle) Expertise | `2c47078e-8b7e-80d3-a7af-df0293b56448` |

### doTERRA-Säulen (angelegt 2026-04-21)
| Säule | Page-ID | Anteil |
|--------|---------|--------|
| 1. Der Wake-Up: Wenn dein Körper spricht | `3497078e-8b7e-81ec-a9b0-e250d752c42a` | 15% |
| 2. Mama-Körper ab 35: Was du wirklich brauchst | `3497078e-8b7e-8119-b9b2-daf36eb7c9cd` | 25% |
| 3. Zurück zu deiner Energie — 4 Säulen der Regeneration | `3497078e-8b7e-81b5-9488-f36fddc282ad` | 25% |
| 4. Mental Load & Stressmanagement | `3497078e-8b7e-81ff-bb00-fba8e899c3ee` | 20% |
| 5. Rückkehr zu dir — die neue Mama-Identität | `3497078e-8b7e-812c-a8cd-e1b21c242971` | 15% |

---

## Content-Management Schema — Pflicht-Felder für Assistenten

Beim Anlegen neuer Posts (von /reels, /karussell, Scheduled Tasks) diese Felder immer setzen:

| Feld | Typ | Pflicht | Quelle |
|------|-----|---------|--------|
| **Content-Titel** | TITLE | ✓ | Aus Briefing |
| **Content-Typ** | multi_select (Reel/Karussell/Story/…) | ✓ | Je nach Post-Art |
| **Status** | select (Idee/Geplant/Erstellung begonnen/Erstellung abgeschlossen/Veröffentlicht) | ✓ | Start: „Idee" |
| **Content-Plattformen** | RELATION | ✓ | Instagram Mentoring ODER Instagram doTERRA |
| **Content-Säule** | RELATION | ✓ | Passende Pillar |
| **Kurzbeschreibung** | text | ✓ | 1-2 Sätze zum Inhalt |
| **Keyword** | text | ✓ | Aus `manychat-keywords.md` |
| **Storyart** | select | empfohlen | Persönliche Geschichte / Mythos-Brecher / Schritt-für-Schritt / Kunden-Transformation / Behind-the-Scenes / Meinungs-Post / Community-Story |
| **Ziel** | multi_select | empfohlen | Persönlichkeit zeigen / Interaktion / Expertise / Vertrauen / Reichweite / Verkaufen |
| **Briefing-Link** | URL | ✓ | URL zum MD-File in outputs/ |
| **Canva-Link** | URL | empfohlen | Link zum Canva-Design (falls existiert) |
| **Käufertypen** | multi_select | empfohlen | Willi / Amelie / Ina / Zoe / Rudi / Frank (Julia-Trost-Archetypen) |
| **Launch-Phase** | select | optional | Aufwärmphase / Secret Offer / Verkaufsphase / Nachkaufphase / Evergreen |
| **Veröffentlichung** | date | später | Wird bei Planung gesetzt |
| **Bewertung** | select (1-5 Sterne) | später | Nach Performance-Auswertung |

**Performance-Felder** (werden nach dem Posten nachgetragen — von Patricia oder später per Instagram Graph API):
- Ansichten / Reichweite (TEXT)
- Gespeichert (TEXT)
- Shares (TEXT — gibt es nicht als separates Feld, müsste ergänzt werden ODER in A N A L Y S E)
- Gefällt mir (TEXT)
- Kommentare (TEXT)
- neue Follower (NUMBER)
- URL veröffentlicht (URL)
- A N A L Y S E (TEXT — Freitextfeld für Learnings)

**Recycling Content (Self-Relation)** = Bei Reposts Link zum Original-Eintrag.

---

## Rezept: Neuen Post anlegen (für Assistenten)

```python
# Pseudocode für den Assistenten
def create_post_in_notion(briefing):
    # Notion-Tool aufrufen: create-pages
    parent = {"type": "data_source_id", "data_source_id": "2ae7078e-8b7e-811a-ad14-000ba5820c09"}
    properties = {
        "Content-Titel": briefing.title,
        "Content-Typ": "Reel" or "Karussell",
        "Status": "Idee",
        "Content-Plattformen": [get_plattform_page_id(profil)],  # Mentoring oder doTERRA
        "Content-Säule": [get_pillar_page_id(pillar_name)],
        "Kurzbeschreibung": briefing.short_desc,
        "Keyword": briefing.manychat_keyword,  # "ENERGIE", "SYSTEM", etc.
        "Storyart": briefing.storyart,
        "Ziel": briefing.ziele,  # Liste
        "Briefing-Link": f"outputs/reels/{briefing.slug}.md",  # oder karussells
        "Canva-Link": briefing.canva_link or "",
        "Käufertypen": briefing.archetypen,
    }
```

---

## Views & Query-Muster

**Alle Ideen (Status = Idee)** für das kommende Posten:
- Filter: Status = „Idee"
- Sortierung: createdTime ASC

**Alle Geplanten** für die nächsten 7 Tage:
- Filter: Status = „Geplant" AND Veröffentlichung zwischen heute + 7d

**Veröffentlichte Posts der letzten 30 Tage** (für Monats-Repost):
- Filter: Status = „Veröffentlicht" AND Veröffentlichung zwischen today-30d AND today-4d

**Best-Performer Mentoring** (für Repost-Engine):
- Filter: Status = „Veröffentlicht" AND Content-Plattformen CONTAINS „Instagram Mentoring"
- Sortierung: nach Bewertung + Gespeichert DESC

---

## Wichtige Warnings

- **„Gespeichert", „Shares", „Gefällt mir", „Ansichten / Reichweite", „Kommentare" sind TEXT-Felder!** → Beim Query als String parsen, als Zahl casten.
- **Status-Pipeline strikt einhalten**: Idee → Geplant → Erstellung begonnen → Erstellung abgeschlossen → Veröffentlicht. Keine Sprünge.
- **Profile NIE mischen**: Content-Plattformen-Relation immer nur EINER der zwei (Mentoring ODER doTERRA, nicht beide).
- **Pillar-Zuordnung PFLICHT**: Jeder Post braucht genau EINE Säule aus Content-Strategie-DB.

---

_Zuletzt aktualisiert: 2026-04-21_
