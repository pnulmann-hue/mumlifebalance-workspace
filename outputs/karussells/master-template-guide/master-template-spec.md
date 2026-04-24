# Master-Template Build-Spec — Karussell

Referenz für Patricia wenn sie das 11-seitige Master-Template in Canva baut.

**Format:** 1080×1350 px (4:5, Instagram-Karussell)
**Visual-Referenz:** `outputs/samples/karussell-v3-preview.html` — kannst du im Browser offen haben beim Bauen

**Grund-Idee:** Dieses Template wird EINMAL gebaut. Danach klont Claude es für jedes neue Karussell und ersetzt nur die Platzhalter-Texte und Fotos. Dadurch ist das Branding IMMER konsistent und der Workflow vollautomatisch.

---

## Basis-Einstellungen (für alle Folien identisch)

### Farben (aus MumLifeBalance Markenkit)
| Rolle | Farbe | Hex |
|---|---|---|
| Haupt-Hintergrund | Creme | `#f1ecdd` |
| Petrol-Akzent | Petrol | `#12828c` |
| Dunkelblau-Akzent | Dunkelblau | `#29556d` |
| Orange-Akzent | Orange | `#dc822e` |
| Text | Fast-Schwarz | `#0c1c30` |

### Schriften (aus Markenkit)
| Rolle | Font | Brand-Kit-Label |
|---|---|---|
| Hero/Überschrift | **Philosopher** (Serif) | „Überschrift" |
| Body | **Source Sans Pro** (Sans) | „Text" |
| Akzent/Handschrift | **Silver South Script** | „Zwischenüberschrift" |

### Crop-Safe-Zone (WICHTIG)
- **Oben 169 px** und **unten 169 px** (= 12.5% von 1350) werden im Instagram-Feed-Grid abgeschnitten
- Wichtiger Text NIEMALS in diese Zonen
- Nur Deko in Safe-Zone (Slide-Nr. oben rechts, „Weiter →" unten rechts)

---

## Platzhalter-Konvention (kritisch für Klon-Automation!)

Damit Claude später automatisch Texte ersetzen kann, nutze in allen Text-Boxes **eindeutige Platzhalter** in geschweiften Klammern:

**Text-Platzhalter:**
- `{{HOOK}}` — Cover-Hook
- `{{FOLIE_2_HOOK}}`, `{{FOLIE_2_BODY}}`, `{{FOLIE_2_SCRIPT}}` — usw pro Folie
- `{{FOLIE_N_NUMMER}}` — Slide-Nr (z.B. „2/11")
- `{{HAUPT_BOTSCHAFT}}` — zentrale Botschaft (Folie 10)
- `{{ABOUT_ME_HOOK}}` — „Hey, ich bin Patricia."
- `{{CTA_KEYWORD}}` — Keyword (z.B. „SICHTBAR")

**Bild-Platzhalter (als Bild-Container, später via `update_fill` ersetzt):**
- `COVER_PHOTO` (Folie 1, Full-Bleed)
- `EMPATHIE_PHOTO` (Folie 5, runder Kreis 90px)
- `ABOUT_ME_PHOTO` (Folie 11, runder Kreis 110px)

---

## Folie 1 — COVER

**Hintergrund:** Full-Bleed-Foto `COVER_PHOTO` (Patricia-Shot) mit Creme-Overlay-Gradient unten 40% (rgba(241,236,221,0.75))

**Elemente:**
| Element | Text | Font | Grösse | Farbe | Position |
|---|---|---|---|---|---|
| Hero-Text | `{{HOOK}}` | Philosopher Bold | ~60px (angepasst an Text-Länge) | Text (#0c1c30) | Mittig unten über Overlay |
| Akzent | Orange-Unterstreichung auf Key-Wort im Hook | | | Orange (#dc822e) | |
| Slide-Nr | „1/11" | Source Sans Pro | 11px | 50% Opacity | oben rechts, innerhalb Safe-Zone |

**Beispiel-Text:** „5 Sätze, nach denen deine Freundinnen aufhören zu **kaufen**."

---

## Folie 2 — STORY-EINSTIEG

**Hintergrund:** Creme (#f1ecdd)

**Elemente:**
| Element | Text | Font | Grösse | Farbe |
|---|---|---|---|---|
| Quote-Icon | „" | Philosopher | 80px | Orange 30% |
| Dreizeiler | `{{FOLIE_2_QUOTE}}` (z.B. „Du postest. Du schreibst. Du fragst.") | Philosopher Bold | 60px | Text |
| Bridge | „Und trotzdem:" | Philosopher Italic | 40px | Dunkelblau |
| Script-Wort | `{{FOLIE_2_SCRIPT}}` (z.B. „Stille.") | Silver South Script | 70px | Orange |
| Slide-Nr + Weiter | „2/11" + „Weiter →" | Source Sans Pro | 11/13px | 50%/100% |

---

## Folie 3 — PROBLEM-FRAME

**Hintergrund:** Creme

**Elemente:**
| Element | Text | Font | Grösse | Farbe |
|---|---|---|---|---|
| Sub-Hook | `{{FOLIE_3_SUB}}` | Philosopher Italic | 28px | Dunkelblau |
| Haupt-Frage | `{{FOLIE_3_FRAGE}}` | Philosopher Bold | 48px | Text |
| Body | `{{FOLIE_3_BODY}}` (1-2 Sätze) | Source Sans Pro | 20px | Text 85% |
| Slide-Nr + Weiter | | | | |

---

## Folie 4 — FEHLER NR. 1

**Hintergrund:** Creme

**Layout:** grosse Hintergrund-Zahl + Zitat + Erklärung

**Elemente:**
| Element | Text | Font | Grösse | Farbe |
|---|---|---|---|---|
| Hintergrund-Zahl | „1" als Outline | Philosopher Bold | 220px | Petrol 40% (als Outline, nicht Fill) |
| Zitat | `{{FOLIE_4_ZITAT}}` („Ich hab da was Tolles…") | Philosopher Italic | 32px | Text |
| Akzent-Wort | Key-Wort in Zitat | Philosopher Bold | 32px | Orange |
| Label | „warum das killt" | Silver South Script | 22px | Orange |
| Body | `{{FOLIE_4_BODY}}` (3 kurze Zeilen) | Source Sans Pro | 16px | Text 90% |

---

## Folie 5 — EMPATHIE-BREAK (MIT FOTO)

**Hintergrund:** Creme

**Elemente:**
| Element | Text/Asset | Font | Grösse | Farbe |
|---|---|---|---|---|
| Foto-Kreis | `EMPATHIE_PHOTO` (runder Crop 90px) | — | — | Orange 2px Border |
| Script-Hook | „Hey, erwischt?" | Silver South Script | 52px | Orange |
| Lead | `{{FOLIE_5_LEAD}}` („Keine Sorge — ich hab das selbst genau so gemacht.") | Philosopher Bold Italic | 30px | Text |
| Akzent | „genau so" | Philosopher Bold | 30px | Orange |
| Reassure | `{{FOLIE_5_REASSURE}}` (2 Zeilen) | Source Sans Pro | 15px | Text 90% |

---

## Folien 6–9 — FEHLER NR. 2, 3, 4, 5

**Hintergrund:** Creme

**Gleiches Layout wie Folie 4**, aber mit jeweils:
- Hintergrund-Zahl „2", „3", „4", „5"
- Zitat `{{FOLIE_N_ZITAT}}`
- Label `{{FOLIE_N_LABEL}}` (z.B. „sie hat das 12× erlebt")
- Body `{{FOLIE_N_BODY}}`

**Wichtig Folie 8 (ehemals die „gequetschte" Version):**
- Zahl „4" als Outline (nicht gefüllt), damit Zitat drüber lesbar bleibt

---

## Folie 10 — LÖSUNG (DUNKELBLAU-MOMENT)

**Hintergrund:** Dunkelblau (#29556d) — der einzige Farbwechsel im Karussell

**Elemente:**
| Element | Text | Font | Grösse | Farbe |
|---|---|---|---|---|
| Intro | `{{FOLIE_10_INTRO}}` („Statt zu fragen, ob sie kaufen will —") | Philosopher Italic | 26px | Creme 80% |
| Haupt-Botschaft | `{{HAUPT_BOTSCHAFT}}` (3-Zeiler, z.B. „Zeig ihr, dass du ihr Problem verstehst.") | Philosopher Bold | 52px | Creme |
| Akzent-Wort | z.B. „ihr" | Silver South Script | 54px | Orange |
| Sub-Text | `{{FOLIE_10_SUB}}` („Dann verkauft dein Thema. Nicht dein Pitch.") | Source Sans Pro | 20px | Creme 90% |
| Unterstreichung | auf Key-Wort | — | — | Orange |

---

## Folie 11 — ABOUT-ME

**Hintergrund:** Creme

**Elemente:**
| Element | Text/Asset | Font | Grösse | Farbe |
|---|---|---|---|---|
| Foto-Kreis | `ABOUT_ME_PHOTO` (runder Crop 110px) | — | — | Orange 3px Border |
| Hook | „Hey, ich bin Patricia." | Philosopher Bold + Silver South für „Hey," | 34px/54px | Text/Orange |
| Bio-Zeile | „4-FACH MAMA · NETWORKERIN SEIT 2018 · MENTORIN" | Source Sans Pro Bold | 14px | Dunkelblau |
| Pitch | „Ich zeig dir, wie du sichtbar wirst — ohne Freundinnen zu nerven." | Philosopher Italic | 22px | Text |
| CTA-Button | Rechteck mit Text „Kommentier `{{CTA_KEYWORD}}`" | Source Sans Pro Bold | 16px | Creme auf Orange-Rechteck |
| „Kommentier" | vor Keyword | Silver South Script | 18px | Creme (auf Orange) |

---

## Weiter-Marker (alle Folien 1–10)

Unten rechts, in der Safe-Zone, kleiner Text:
- „Weiter →" — Source Sans Pro Bold 13px, Orange (#dc822e), 50px vom rechten Rand, 170px vom unteren Rand

## Slide-Nummer (alle Folien)

Oben rechts, in der Safe-Zone:
- „1/11", „2/11" etc. — Source Sans Pro Bold 11px, 50% Opacity, 50px vom rechten Rand, 170px vom oberen Rand

---

## Nach Fertigstellung

1. Design in Ordner „Claude Designs" (ID `FAHHgyd2stU`) speichern
2. Design umbenennen: **„Master-Karussell v1"** (genau so, damit Claude es findet)
3. Mir kurz Bescheid geben — ich teste dann den Klon-Flow mit dem Template + den ersten echten Inhalten

---

_Erstellt 2026-04-22 aus der HTML-Preview-Spec. Die Textgrössen sind relativ, kannst du in Canva nach Augenmass anpassen — wichtig ist dass die Hierarchie stimmt (Hero > Body > Akzent)._
