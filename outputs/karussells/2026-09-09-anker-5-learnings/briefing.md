---
tags: [content, karussell, mentoring, hybridmodell]
---

# Karussell — Anker-Prinzip: 3 Jahre Network + eigenes Business, 5 Learnings

**Profil:** Mumlifebalance (Mentoring) · **Typ:** Karussell, 8 Folien, 1080×1350
**Job-Säule:** A-Autorität · **Ziel:** Saves + Vertrauen · **Launch-Phase:** Evergreen
**Herkunft:** Notion Content-Management `3ce7078e-8b7e-812f-b9ec-fc80fe4e7854`
(geplant für 8.9., nicht gepostet → nachgezogen am 9.9.)

## Design

Petrol-Cover (`#12828c`), Navy-Body (`#0c1c30`), Orange-Akzent (`#dc822e`),
Türkis-Akzent (`#5cc4cf`). Philosopher (Headlines) + Source Sans 3 (Body).
Kein Foto — reines Typo-Template.

**Feed-Aesthetic:** Template-Cover ist zulässig, weil die letzten Feed-Posts (1.–4.9.)
alle Reels waren. Petrol-Cover ist zulässig, weil dies **kein** Lead-Post mit
Keyword-CTA ist (CTA = Kommentar-Nummer).

## Dateien

- `slides.html` — Quelle (1080×1350 nativ)
- `png/slide-01.png … slide-08.png` — gerendert
- Config: `scripts/blotato-post/post-configs/2026-09-09-mi-mentoring-anker-5-learnings.json`

**Render-Befehl** (wichtig: `render-fullsize.js`, NICHT `render.js` — letzteres
skaliert um 3.18× für 340px-Grid-Vorlagen und zerlegt dieses Layout):

```
node scripts/karussell-render/render-fullsize.js \
  --input=outputs/karussells/2026-09-09-anker-5-learnings/slides.html \
  --output=outputs/karussells/2026-09-09-anker-5-learnings/png
```

## Visual-QA

- [x] Alle 8 PNGs exakt 1080×1350
- [x] Fonts laden (Google-Fonts-Link im HTML — fehlte in der KW35-Vorlage)
- [x] Kein Text-Overlap mit dem Footer
- [x] Story-Arc: Cover → 5 Learnings → Kernsatz → CTA
- [x] Brand-Farben + Schriften korrekt
- [x] Kein Foto → kein Gesicht-/Hauptmotiv-Check nötig
- [x] Keine erfundenen Zahlen (3 Jahre + 4 Kinder sind belegt)
