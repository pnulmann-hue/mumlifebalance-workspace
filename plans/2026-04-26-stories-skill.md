# Plan-Stub: `/stories` Skill — Story-Assistent für beide Profile

**Status:** Stub — am Montag mit `/create-plan` verfeinern und `/implement`-fähig machen
**Erstellt:** 2026-04-26 (Auslöser: Wander-Stories ohne Story-Arc gerendert — siehe outputs/stories/2026-04-26-*)
**Vorgesehene Bauzeit:** ~60 Min Implementation + 30 Min Test mit echtem Material

---

## Auslöser

Am 2026-04-26 wurden Wander-Stories für beide Profile gerendert (10 PNGs). Patricia hat das Ergebnis als „lahm" bewertet: zu sehr Statement-Slideshow, kein Storytelling. Der bestehende Workflow (`/reels`-Logik auf Stories anwenden) liefert keinen Spannungsbogen — Stories brauchen eigene Mechanik (Hook → Reibung → Wendung → Punkt → CTA, native IG-Sticker, 24h-Logik, Engagement-Optimierung).

## Ziel

Ein dedizierter `/stories` Skill, der für beide Profile (Mentoring + doTERRA) **echte Story-Bögen** baut, die zur jeweils aktiven Funnel-Strategie passen — mit Render-Pipeline und Visual-QA.

## Skill-Modi (5)

### 1. Story-Arc aus Material
- **Input:** Bilder/Videos + 1-2 Sätze Kontext (Wo? Was passiert? Was geht dir durch den Kopf?)
- **Output:** 5-7-Slide-Bogen (Hook → Reibung → Wendung → Punkt → CTA) + Slide-Texte + Sticker-Anweisungen + gerenderte PNGs
- **Pflicht:** Erst `Stories die verkaufen.pdf` + `hook-framework.md` lesen, dann konzipieren

### 2. Story-Doktor
- **Input:** User zeigt fertige Story (Screenshot oder beschrieben)
- **Output:** Diagnose (Hook? Reibung? CTA? Sticker-Strategie?) + 3 konkrete Fixes

### 3. Sticker-Strategie
- **Input:** Story-Konzept ohne Sticker
- **Output:** Pro Slide passender IG-Sticker (Frage / Antwort / Quiz / Link / Slider / Umfrage / Countdown / Erwähnung) — ausgerichtet auf aktiven Funnel aus `active-funnels.json`

### 4. Story-Sequenz-Plan
- **Input:** Funnel/Launch-Ziel + Tage
- **Output:** Sequenz über N Tage (z.B. Mo Aufwärm → Mi Beweis → Fr Pitch → Sa Erinnerung) mit Story-Typ pro Tag

### 5. Render-Pipeline (Standalone)
- **Input:** Bestehendes Slide-Briefing
- **Output:** PNGs gerendert via `scripts/story-render/render_stories.py`

## Pflicht-Workflow (für jeden Modus)

1. **Profil-Frage** zuerst (Mentoring vs. doTERRA — keine Annahmen)
2. **Wissensbasen laden:**
   - `reference/julia-trost/Stories die verkaufen.pdf`
   - `reference/julia-trost/Transkripte Videocalls/_sortiert/Instagram Story Strategie/` (falls vorhanden)
   - `context/brand-voice.md` + `caption-formeln.md` + `hook-framework.md`
   - `context/active-funnels.json` (welcher CTA passt zur aktuellen Funnel-Priorität)
3. **Story-Arc aufbauen** (nicht 5 Statements!)
4. **Visual-QA vor Output:** Jede gerenderte Slide selbst prüfen — Gesicht frei? Hauptmotiv frei? Box-Position sinnvoll? Story-Arc erkennbar? — bevor User Output sieht
5. **Output strukturiert:** `outputs/stories/YYYY-MM-DD-[slug]/briefing.md` + `outputs/stories/YYYY-MM-DD-[slug]/renders/*.png`

## Wiederverwendbare Bausteine (existieren bereits)

- `scripts/story-render/render_stories.py` — Pillow-Pipeline für 1080×1920 PNGs (focal_y, top/bottom_padding, Brand-Farben, Philosopher + Source Sans 3)
- `scripts/story-render/fonts/` — Brand-Fonts (Philosopher Bold/Regular, Source Sans 3)
- `outputs/stories/01-05-*.jpg` — Naming-Convention für Source-Bilder
- `.gitignore` Ausnahme für `outputs/stories/renders/*.png` (Mobile-Download via GitHub)

## Erweiterungen, die der Skill braucht (gegenüber heutiger Render-Pipeline)

1. **Native IG-Sticker als Markdown-Annotation pro Slide** (im Briefing erklärt, beim Posten manuell drüber)
2. **Story-Bogen-Validator** (5 Slides ohne Bogen → Warnung)
3. **CTA-Auto-Mapping aus `active-funnels.json`** (Bio-Check → Link-Sticker auf mumlifebalance.ch/bio-check; doTERRA → Frage-Sticker oder Antwort-Sticker mit ENERGIE-Trigger)
4. **Visual-QA als Pflicht-Schritt** (Render → Self-Check → erst dann an User)

## Datei-Struktur (geplant)

```
.claude/commands/stories.md          # Skill-Definition (für /stories Aufruf)
context/stories-framework.md         # Story-Arc-Theorie + Sticker-Strategie + Beispiele
scripts/story-render/                # bereits da, ggf. erweitern um:
  ├─ render_stories.py              # bereits da
  ├─ visual_qa.py                   # NEU: Self-Check-Modul (Box vs. Hauptmotiv)
  └─ sticker_mapping.py             # NEU: Funnel → Sticker-Typ
outputs/stories/YYYY-MM-DD-[slug]/   # Output-Struktur pro Story
  ├─ briefing.md
  ├─ source/                        # Original-Bilder
  └─ renders/                       # gerenderte PNGs
```

## Offene Fragen für `/create-plan` am Montag

1. Bauen wir `visual_qa.py` automatisiert (z.B. mit OpenCV Face-Detection für „Gesicht frei?"-Check)? Oder bleibt Visual-QA manuell durch Claude (Read+anschauen)?
2. Sticker-Strategie pro Funnel — wo liegt das Mapping? In `active-funnels.json` ergänzen oder eigene Datei?
3. Soll der Skill Video-Slides (MP4) auch rendern, oder vorerst nur Bilder?
4. Story-Sequenz-Plan: in Notion-Content-DB einpflegen oder nur als Markdown?

## Referenz: Was am 2026-04-26 schiefging

Die Wander-Stories wurden als 5 unabhängige Statements gebaut (z.B. „Sonntag." / „Genau dafür hab ich mein Business so gebaut." / „4 Kinder. 1 Business. 0 Hustle-Kult." / „Das ist Freiheit für mich." / „Bio-Check"). Kein Bogen, keine Wendung, keine Reibung. Patricias Diagnose: „lahm". Korrekte Story-Logik wäre gewesen:
- Hook: Pattern-Break-Beobachtung („Es ist 14 Uhr Sonntag und ich tu nix")
- Reibung: Was war früher („Vor 2 Jahren hätte ich noch DM's beantwortet")
- Wendung: Was ist heute anders („Heute fließt's auch ohne mich")
- Punkt: Die Lehre / das Modell („Themenbasiert, magnetisch, Funnel statt Push")
- CTA: Konkreter erster Schritt („Bio-Check 👇" + Link-Sticker)

Diese Bogen-Logik muss der Skill **immer** durchziehen — auch bei spontanen Material-Stories.
