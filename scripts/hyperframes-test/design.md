# Mum Life Balance — Design System

Source of truth für alle HyperFrames-Compositions in Patricia's Business.

## Brand-Farben (Hex)

| Token | Hex | Verwendung |
|---|---|---|
| `--petrol` | `#12828c` | Primärfarbe Mentoring, Akzente, Caption-Boxen |
| `--dunkelblau` | `#29556d` | Sekundärfarbe Mentoring, Statement-Text |
| `--creme` | `#f1ecdd` | Standard-Hintergrund, Caption-Bubble-BG |
| `--orange` | `#dc822e` | Akzent (EIN Wort pro Slide) — primär doTERRA |
| `--text` | `#0c1c30` | Body-Text Standard |
| `--white` | `#ffffff` | Pure-Hintergrund, Caption-Inner-Bubble |

## Fonts

| Token | Font | Verwendung | Quelle |
|---|---|---|---|
| `--font-headline` | `Philosopher` | Hooks, Headlines, Statements | Google Fonts (400, 700) |
| `--font-body` | `Source Sans 3` | Body, Captions, Subtext | Google Fonts (300, 400, 600, 700) |
| `--font-accent` | `Silver South Script` | Signatur, Mini-Akzente (sparsam) | Lokal |

Google-Fonts-Import:
```css
@import url('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
```

## Profil-Variants

### Mentoring (Standard)
- Primärakzent: Petrol `#12828c`
- Sekundärakzent: Dunkelblau `#29556d`
- Tonalität: warm, professionell, mama-nah

### doTERRA (Wellness)
- Primärakzent: Orange `#dc822e`
- Sekundärakzent: Petrol `#12828c`
- Tonalität: Lifestyle, sinnlich, "bei mir war"-Frame
- **Compliance:** keine Heilversprechen, keine medizinischen Aussagen

## Caption-Styles (Liane-Meusel-inspiriert)

### Style 1 — Bubble-Caption (Talking-Head)
- Position: unteres Drittel (bottom 240px)
- Bubble: Creme-BG `#f1ecdd`, padding 32px 48px, border-radius 24px
- Text: Source Sans 3, 600-weight, 64px, Text-Farbe `#0c1c30`
- Akzent-Wörter: Petrol `#12828c` (Mentoring) oder Orange `#dc822e` (doTERRA)
- Shadow: `0 8px 24px rgba(12, 28, 48, 0.15)`

### Style 2 — Hero-Statement (Reichweite)
- Position: zentriert vertikal
- Headline: Philosopher 700, 120px, Text-Farbe Dunkelblau
- Subline: Source Sans 3 400, 48px, italic, 70% opacity
- Hintergrund: Creme `#f1ecdd` mit subtilem Foto-Overlay

### Style 3 — Pop-Up-Akzent (Sales-Reels)
- Trigger: bei Schlüsselwörtern (z.B. "997 CHF", "29.6.")
- Effekt: GSAP scale 0 → 1.2 → 1 mit overshoot ease
- Box: Petrol-BG `#12828c`, Text White, Source Sans 3 700, 56px
- Padding: 16px 32px, border-radius 12px

## Bewegungs-Sprache

- **Entrances:** `gsap.from()` mit `ease: "power2.out"`, duration 0.4-0.6s
- **Exits:** `gsap.to()` mit `ease: "power2.in"`, duration 0.3s
- **Caption-Word-Reveal:** stagger 0.05-0.08s zwischen Wörtern
- **Akzent-Pop-Ups:** `ease: "back.out(1.7)"`, scale 0 → 1
- **Keine Spinning, kein Bounce-übertrieben, kein 3D-Flip** — warm + ruhig, nicht hektisch

## Anti-Patterns (NIE)

- Schwarzer Hintergrund pur (keine "edgy" Brand)
- Neon-Farben (nichts ausserhalb der Brand-Palette)
- Mehr als 1 Akzent-Wort pro Caption-Frame
- Schnelle Pulsierung (epileptisch wirkend)
- Drop-Shadows härter als `rgba(12, 28, 48, 0.20)`
- Gradient-Hintergründe (Brand bleibt flach + warm)
- Sans-Serif für Headlines (Philosopher ist gesetzt)

## Composition-Konstanten

- Resolution: **1080×1920** (Reels portrait)
- Frame-Rate: 30 fps Standard
- Safe-Zone (Instagram-UI): oben 250px, unten 350px frei halten von Critical-Text
- Letterboxing: NIE (vollflächig)
