---
tags: [content, reels]
---

# Reel-Cover · POV-Dorf (Sa 28.6.)

Cover für den POV-Dorf-Reel „Schnäuzer drauf, ab in den WhatsApp" (Caption: `outputs/content-kalender/2026-06-captions-v2.md`, Post #13).

## Was geändert wurde

**Problem:** Der Text lief auf **4 Zeilen** und quetschte sich unten an den Rand.

**Fix:** Text fix auf **3 Zeilen** umgebrochen + mehr Luft nach unten (`bottom: 260px`).

```
POV:
Wenn die aus meinem Dorf
meine ersten Stories
gesehen haben.
```

## Foto reinlegen

Das HQ-Pusteblumen-Foto (Patricia pustet Pusteblume im Feld) hier ablegen:

```
outputs/reels/2026-06-28-pov-dorf/assets/cover-foto.jpg
```

Dann ist der Hintergrund automatisch aktiv. Ohne Foto zeigt das Cover eine warme Wiesen-Platzhalterfarbe (zum Layout-Check). `object-position: center 28%` sorgt dafür, dass Gesicht + Pusteblume im oberen Drittel sitzen — bei Bedarf den Wert anpassen.

## Rendern zu PNG (1080×1920)

```bash
cd scripts/karussell-render && npm install   # einmalig (Puppeteer)
node render.js --input="../../outputs/reels/2026-06-28-pov-dorf/cover.html" --slug=pov-dorf-cover
```

Oder einfach `cover.html` im Browser öffnen (Fenster 1080×1920) und Screenshot.

## Brand-Specs

- Format: 1080×1920 (9:16 Reel-Cover)
- Eyebrow „POV:" — Source Sans 3, Petrol `#1aa7b2`, letter-spacing 14px
- Headline — Philosopher 92px, Creme `#f1ecdd`, line-height 1.12
- Lesbarkeits-Verlauf von unten (dunkel) nach oben (transparent)
