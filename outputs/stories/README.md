# Stories — Outputs vom /story-Skill

Dieser Ordner enthält alle generierten Story-Briefings + gerenderten PNG-Slides.

## Verzeichnis-Struktur

```
outputs/stories/
├── YYYY-MM-DD-tagesplan-mentoring-[slug]/         # Modus 1 (Standard)
│   ├── briefing.md
│   ├── slides.html
│   └── slides-png/
│       ├── 01.png
│       └── ...
│
├── YYYY-MM-DD-tagesplan-doterra-[slug]/
├── YYYY-MM-DD-salesday-[produkt-slug]/             # Modus 2 (Launch)
├── YYYY-MM-DD-doktor-[idee-slug]/                  # Modus 3 (aus Idee)
├── YYYY-MM-DD-oneslide-[profil]-[slug]/            # Modus 4 (Low-Effort)
├── YYYY-KW##-serie-[thema-slug]/                   # Modus 5 (Mehrtages-Bogen)
├── YYYY-MM-DD-bts-[anlass]/                        # Modus 6 (Behind-the-Scenes)
├── YYYY-MM-DD-reaktiv-[anlass]/                    # Modus 8 (Reaktiv)
│
├── highlights-[profil]-stand-YYYY-MM-DD.md         # Modus 7 (Highlight-Pflege)
│
├── wochen-log.json                                 # Käufertyp-Tracking
└── wochen-kontext-KW##.json                        # Notion-Wochenplan-Cache
```

## Pro Story-Ordner

**briefing.md** — Vollständiger Slide-Plan inkl. Hooks, Käufertyp-Tags, Sticker-Vorschläge, CTA-Link, Foto-Wahl, Voice-Check-Status.

**slides.html** — HTML-Quelle (Single-Source-of-Truth für das Rendering). Nutzt Templates aus `scripts/karussell-render/brand-stories.css`.

**slides-png/** — Die fertigen PNGs (1080×1920, 9:16). Direkt Instagram-Story-postbar.

## Render-Befehl

```bash
cd scripts/karussell-render
node render-stories.js \
  --input=../../outputs/stories/YYYY-MM-DD-.../slides.html \
  --output=../../outputs/stories/YYYY-MM-DD-.../slides-png/
```

## Wochen-Log

`wochen-log.json` trackt welche Käufertypen über die letzten 7 Tage angesprochen wurden. Skill nutzt das, um Rotation zu garantieren (alle 4 DISG-Achsen pro Woche).

Beispiel-Struktur:
```json
{
  "2026-04-30": {
    "profil": "mentoring",
    "modus": "tagesplan",
    "disg": "Blau",
    "nadja_persona": "Wilma",
    "story_saeule": "Expertise"
  },
  "2026-04-29": {
    "profil": "doterra",
    "modus": "tagesplan",
    "disg": "Grün",
    "nadja_persona": "Petra",
    "story_saeule": "Persönlichkeit"
  }
}
```

## Wochen-Kontext-Cache

`wochen-kontext-KW##.json` cached die Antwort aus Patricias Notion-Wochenplan, damit der Skill nicht jedes Mal Notion abfragen muss.

Beispiel-Struktur:
```json
{
  "kw": 18,
  "zeitraum": "27.04.-03.05.2026",
  "fokus_der_woche": "Story-Challenge bewerben",
  "content_creation": "Tägliche Story zur Story-Challenge",
  "abgerufen_am": "2026-04-30T08:15:00Z"
}
```

## Wann werden alte Stories gelöscht?

**Nie automatisch.** Ältere Story-Outputs sind wertvolle Repost-Kandidaten + Inspirationsquelle.

Nach 60 Tagen kann Patricia manuell archivieren in `outputs/stories/_archiv/YYYY/`.
