# Story-Framework — Patricias Daily Story Sales Companion

**Erstellt:** 2026-04-30
**Zentrales Wissensdokument für `/story`-Skill.**
Lädt Julia + Brandastic + Nadja-Wissensbasen und konsolidiert sie zu einem konsistenten System.

---

## Die zwei nicht-verhandelbaren Kernregeln

### Regel 1: Jede Story-Sequenz hat einen CTA-Link
- Tagesplan (5 Slides): mind. 1 Slide mit Link (Freebie ODER Produkt)
- One-Slide-Tag: Link auf der einen Slide
- Sales-Day: jede 2.-3. Slide hat Link
- Behind-the-Scenes: Soft-Link (Freebie) ist Pflicht — nie nur „Lifestyle ohne Brücke"

**Ausnahme:** Reconnect-Modus bei Engagement-Crash (Julias Tipp: 1-2 Tage emotionale Story OHNE Link, um Algorithmus zu reanimieren).

### Regel 2: Käufertyp-Rotation über die Woche
Skill trackt in `outputs/stories/wochen-log.json` welche Käufertypen die letzten 7 Tage angesprochen wurden.
- Brandastic-DISG (4 Typen): Rot/Gelb/Grün/Blau — alle müssen jede Woche vorkommen
- Wenn Skill drei Tage lang nur Rot+Blau nutzt → nächster Tag automatisch Grün+Gelb

---

## Pflicht-Lese-Liste vor jedem Skill-Lauf

Skill liest IMMER zuerst:

**Story-spezifisch:**
- `context/story-framework.md` (diese Datei)
- `context/julia-stories-die-verkaufen.md` (Slide-Struktur + 7 Storytelling-Regeln)
- `context/julia-insta-stories-anleitung.md` (10 Verkaufs-Templates)
- `context/julia-story-ideen.md` (3-Säulen-Bibliothek)
- `context/brandastic-kaeufertypen.md` (DISG + AIDA)
- `context/nadja-story-prompts.md` (7 Personas)

**Patricia-spezifisch:**
- `context/brand-voice.md`
- `context/hook-framework.md`
- `context/caption-formeln.md`
- `context/business-info.md`
- `context/active-funnels.json`
- `context/ki-phrasen-blackliste.md`

**Bei doTERRA-Profil zusätzlich:**
- `context/doterra/` (komplett)
- `context/doterra/patricia-wendepunkt-story.md`
- Memory: `feedback_doterra-compliance-no-heilversprechen`

**Memory-Regeln (immer beachten):**
- `feedback_keine-erfundenen-zahlen` — keine fiktiven Zahlen, nur aus patricia-expertise.md
- `feedback_umlaute-echte` — echte Umlaute, Schweizer „ss"
- `feedback_hooks-inspiration-nicht-copypaste` — Vorlagen sind Muster, nicht Copy-Paste
- `feedback_transformation-statt-features` — Zustand statt Module
- `feedback_brand-metaphern-patricia` — Schaufenster, violettes Kleid, Schuhladen

---

## Slide-Struktur (Julia-Goldformel, in /story angewendet)

```
Slide 1:        BÄM-Hook (direkter Einstieg, keine „Hallo ihr Lieben")
Slide 2-X:      PIE-Mittelteil (Problem → Insight → Example)
Letzte Slide:   Angebot + CTA + Link
                (+ optional: Testimonial-Slide davor)
                (+ optional: Outro-Slide nach CTA)
ÜBER ALLEM:     Storytelling — kein Lehrbuch-Ton
```

---

## Käufertyp-System (konsolidiert)

Skill nutzt **Brandastic-DISG (4 Typen) als Hauptachse** für Wochenrotation, und **Nadjas 7 Personas als Granularität** für tiefere Skripte.

### DISG-Wochenrotation (Standard)

| Tag | Hauptzielgruppe | Sekundär | Story-Pattern-Beispiel |
|---|---|---|---|
| Mo | Stetig (Grün) | Initiativ (Gelb) | Behind-the-Scenes, Wir-Sprache |
| Di | Dominant (Rot) | Gewissenhaft (Blau) | Action-Hook, Erfolgs-Zahl |
| Mi | Initiativ (Gelb) | Stetig (Grün) | Spielerisch, Quiz-Sticker |
| Do | Gewissenhaft (Blau) | Dominant (Rot) | Daten, Schritt-für-Schritt |
| Fr | Initiativ (Gelb) | Stetig (Grün) | Lifestyle-Glimpse |
| Sa | Stetig (Grün) | Initiativ (Gelb) | Familie, Mama-Realität |
| So | Dominant (Rot) | Gewissenhaft (Blau) | Reflexion + Vorschau |

### DISG → Nadja-Persona-Mapping

| DISG | Nadja-Persona | Trigger |
|---|---|---|
| Rot | Charlie (Chancensucher) | Innovation, Exklusivität |
| Rot | Stefan (Schnäppchenjäger) | Deals, Knappheit |
| Gelb | Isabell (Interaktive) | Dialog, Q&A |
| Grün | Werner (Wertorientierter) | Mission, Ethik |
| Grün | Petra (Persönliche) | Emotion, Gesicht |
| Blau | Wilma (Wissbegierige) | How-to, tiefe Analysen |
| Blau | Bärbel (Bestätigungssuchende) | Reviews, Fallstudien |

---

## Die 8 Modi des /story-Skills

### Modus 1: Tagesplan (Standard)
**Trigger:** Patricia tippt nur „/story" oder beschreibt was heute los ist.

**Ablauf:**
1. Profil-Frage (Mentoring/doTERRA)
2. Wochen-Fokus aus Notion holen (Wochenplanung-DB) ODER 1-Satz-Frage
3. Aktiven Funnel aus active-funnels.json wählen
4. Käufertyp-Wochenlog prüfen → Tageszielgruppe wählen
5. 3-5 Slides bauen:
   - Slide 1: BÄM-Hook (aus hook-framework.md, an heutigen Käufertyp angepasst)
   - Slide 2-3: PIE-Mittelteil (Problem → Insight → Example aus Patricias Realität)
   - Slide 4: Brücke zum Angebot („Falls du das auch kennst…")
   - Slide 5: CTA mit Link (Freebie oder Produkt)
6. Sticker-Vorschläge pro Slide
7. Foto-Wahl pro Slide (aus `context/Shootingbilder/`)
8. HTML rendern → PNGs

### Modus 2: Sales-Day (Launch-Operationalisierung)
**Trigger:** Patricia tippt „/story sales-day" oder es gibt aktiven Launch in active-funnels.json.

**Ablauf:**
1. Welcher Launch? Tag im Launch (Tag 0/Vorlauf/Tag X)?
2. Skill liest `outputs/funnels/[slug]/launch-plan.md` falls vorhanden
3. 8-12 Slides über den Tag verteilt:
   - Morgens (Slide 1-3): Aufwärm + Pain-Point-Tease (Stetig + Persönliche-Petra)
   - Mittags (Slide 4-6): Transformation-Story + Social Proof (Bärbel + Werner)
   - Nachmittags (Slide 7-9): Angebot + Bonus + Knappheit (Stefan + Charlie)
   - Abends (Slide 10-12): Letzte Chance + Harter CTA (Dominant + Knappheit)
4. Alle 7 Nadja-Personas mind. 1× abgedeckt
5. Stündlicher Sticker-Plan
6. Link-Plan: Welcher Slide hat welchen CTA-Link

### Modus 3: Story-Doktor (aus roher Idee)
**Trigger:** Patricia: „Ich hab heute folgendes erlebt: [...]"

**Ablauf:**
1. Skill matcht Idee gegen 10 Julia-Templates → wählt passendstes
2. Schlägt Hook-Variante vor (3 Optionen)
3. Baut 3-5-Slide-Aufbau
4. CTA passend zum aktuellen Funnel
5. Voice-Check gegen brand-voice.md
6. Optional: HTML rendern

### Modus 4: One-Slide-Tag (Low-Effort)
**Trigger:** Patricia tippt „heute kein Bock" / „nur eine Slide" / „/story 1-slide"

**Ablauf:**
1. Skill zieht aus julia-story-ideen.md (Säule 3 Persönlich) eine zur Wochenphase passende Idee
2. ODER aus nadja-story-prompts.md eine Persona-passende Idee
3. 1 Slide mit:
   - Persönlich-relevanter Hook
   - Sticker (Frage oder Quiz)
   - Soft-Link zum aktiven Freebie
4. HTML rendern

### Modus 5: Story-Serie (Mehrtages-Strang)
**Trigger:** Patricia: „/story serie 3 tage über [thema]"

**Ablauf:**
1. Thema + Anzahl Tage klären
2. Skill kombiniert 3-7 Templates über mehrere Tage zu einem Bogen
3. Pro Tag: Cliff-Hanger am Ende
4. Letzter Tag: harter Pitch
5. Alle Slides werden gerendert + nummeriert (`tag-1-slide-1.png`, `tag-1-slide-2.png` etc.)

**Standard-Bögen:**
- 3-Tage-Bogen: Problem → Insight → Lösung (mit Pitch)
- 5-Tage-Bogen: Hook → Story → Anti-Story → Insight → Lösung
- 7-Tage-Bogen: Vor-Launch (Aufwärmen)

### Modus 6: Behind-the-Scenes
**Trigger:** Patricia: „/story bts" oder beschreibt Foto/Erlebnis

**Ablauf:**
1. Patricia tippt Erlebnis / lädt Foto-Beschreibung hoch
2. Skill prüft welche Käufertypen heute dran sind (Wochenlog)
3. Baut 3-5 Slides mit Brand-Voice + Verkaufs-Brücke
4. Pflicht: mind. 1 Soft-Link am Ende
5. Beispiel-Pattern für doTERRA: „Garten + Kinder + Erschöpfung" → Bridge zur Wendepunkt-Story → Bridge zur Energie-Kur

### Modus 7: Highlight-Pflege
**Trigger:** „/story highlights"

**Ablauf:**
1. Patricia listet bestehende Highlights (oder lädt Screenshots)
2. Skill empfiehlt:
   - Welche zusammenfassen (zu generisch)
   - Welche aktualisieren (veraltet)
   - Welche neu anlegen (Lücken)
3. Cover-Vorschläge in Brand-Look
4. Reihenfolge-Empfehlung (wichtigstes zuerst)

### Modus 8: Reaktiv (auf Reaktionen)
**Trigger:** Patricia: „Jemand hat geantwortet [X]" oder „Umfrage-Ergebnis: 80% sagen [Y]"

**Ablauf:**
1. Skill analysiert Reaktion
2. Schlägt nächsten Schritt vor:
   - Antwort-Slides (1-2)
   - DM-Anstoss (Text-Vorschlag)
   - Folge-Story (3-5 Slides)
3. Skill prüft, ob Reaktion zu aktivem Funnel passt → leitet ggf. zu /funnel weiter

---

## Visual-Pipeline (Pfad B: HTML → PNG)

### Render-Flow im Skill

```
1. Skill generiert Briefing (Slide-Texte + Foto-Wahl + Template-Auswahl)
   ↓
2. Skill schreibt slides.html (jedes Slide nutzt 1 Template + füllt Inhalt)
   ↓
3. Skill ruft `node scripts/karussell-render/render-stories.js` auf
   ↓
4. PNGs landen in outputs/stories/YYYY-MM-DD-.../slides-png/
   ↓
5. Skill zeigt Patricia: Briefing + PNG-Vorschau + Direktlink zur HTML
```

### Die 8 Slide-Templates (in brand-stories.css)

1. **Hook-Slide** — Grosser Hook-Text + Kontrastfarbe + Foto-Akzent unten
2. **Story-Text-Slide** — Mehrzeiliger Text + dezentes Foto im Hintergrund
3. **Zitat-Slide** — Zentrales Zitat mit Anführungszeichen + Patricia-Foto rechts
4. **Frage-Slide** — Frage + Sticker-Anker + Whitespace
5. **CTA-Slide** — Produkt-Visual + „Tipp den Link" + Pfeil + Swipe-Up-Marker
6. **Behind-Scenes-Slide** — Foto im Vordergrund + Text-Overlay unten
7. **Vorher-Nachher-Slide** — Geteiltes Layout für Transformation
8. **Countdown-Slide** — Grosses Datum/Zahl + Knappheits-Text + CTA

### Profil-Varianten
- **Mentoring:** Creme `#f1ecdd` + Petrol-Akzent
- **doTERRA:** Creme `#f1ecdd` + Orange/Erdton-Akzent
- **Beide:** Philosopher (Headlines) + Source Sans 3 (Body)

### Foto-Pool
`context/Shootingbilder/` (>1000 Patricia-Fotos)

Foto-Auswahl-Logik:
- Skill mappt Stimmungs-Tags („morgens energiegeladen" / „nachdenklich" / „mit Kindern" / „im Garten") gegen Foto-Inventar
- Falls Patricia keine Stimmung angibt: Skill wählt Foto-Set passend zum Käufertyp des Tages

---

## Notion-Anbindung

### Wochenplan-Lese-Logik

```
1. Skill berechnet aktuelle KW-Nummer
2. notion-search query: "Wochenplanung KW {nummer}"
3. notion-fetch der gefundenen Page
4. Skill liest:
   - Property "Fokus der Woche"
   - Body-Tabelle "Was planst du je Business-Säule?"
     → Insbesondere "Content-Creation"-Spalte
5. Falls keine Page für aktuelle KW: Skill fragt Patricia 1 Satz
6. Skill cached Antwort in outputs/stories/wochen-kontext-KW##.json
   (gilt für ganze Woche, kein erneuter Notion-Call nötig)
```

### Notion-DB-IDs

- **Wochenplanung-DB:** `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`
- **Aufgaben-DB:** `3167078e-8b7e-80baa770dc1a6c38c41e`
- **Tagesplaner-DB:** `3167078e-8b7e-8065a8a2f3ebe4e485e8`
- **Content-Management-DB:** `2ae7078e-8b7e-811a-ad14-000ba5820c09`
- **Produkte-DB:** `2ae7078e-8b7e-81ef-aafa-f03993ef344f`

### Optional Phase 2: Skill schreibt Notion-Eintrag

Nach Story-Erstellung kann Skill (auf Patricias Wunsch) automatisch einen Eintrag in Content-Management-DB erstellen mit:
- Titel: erste Slide-Hook
- Status: „Idee" (Patricia muss freigeben)
- Plattform: Instagram Mentoring / doTERRA
- Pillar: aus Strategie-DB
- Slide-PNGs als Anhang

---

## Output-Struktur

```
outputs/stories/
├── YYYY-MM-DD-tagesplan-mentoring-[slug]/         # Modus 1
│   ├── briefing.md
│   ├── slides.html
│   ├── slides-png/
│   │   ├── 01.png
│   │   └── ...
│   └── notion-eintrag.json (optional)
│
├── YYYY-MM-DD-salesday-[produkt-slug]/             # Modus 2
├── YYYY-MM-DD-doktor-[idee-slug]/                  # Modus 3
├── YYYY-MM-DD-oneslide-[profil]/                   # Modus 4
├── YYYY-KW##-serie-[thema-slug]/                   # Modus 5 (mehrtägig)
├── YYYY-MM-DD-bts-[anlass]/                        # Modus 6
├── highlights-[profil]-stand-YYYY-MM-DD.md         # Modus 7
├── YYYY-MM-DD-reaktiv-[anlass]/                    # Modus 8
│
├── wochen-log.json                                 # Käufertyp-Tracking
└── wochen-kontext-KW##.json                        # Notion-Wochenplan-Cache
```

### briefing.md-Struktur (für jede Story)

```markdown
# Story-Briefing — [Datum] — [Modus] — [Profil]

## Kontext
- Aktiver Funnel: [Name + URL]
- Wochen-Fokus: [aus Notion oder Patricia-Input]
- Käufertyp(en) heute: [DISG-Achse + Nadja-Persona]
- Story-Säule(n): [Expertise / Inspiration / Persönlichkeit]

## Slides

### Slide 1 — [Template-Name]
- **Hook:** ...
- **Käufertyp-Tag:** ...
- **Foto:** [Pfad zu Shootingbild]
- **Sticker:** [Frage / Umfrage / Quiz / keine]
- **Sprechtext (falls Talking-Head):** ...

### Slide 2 — ...

## CTA-Plan
- Slide X enthält Link zu: [Freebie / Produkt + URL]

## Compliance-Status
- [x] Voice-Check brand-voice.md
- [x] Keine erfundenen Zahlen
- [x] doTERRA-Compliance (kein Heilversprechen) — falls doTERRA-Profil
- [x] Echte Umlaute

## Render-Status
- HTML: slides.html
- PNGs: slides-png/01-XX.png
- Render-Befehl: `node scripts/karussell-render/render-stories.js --input=...`
```

---

## Verzahnung mit anderen Skills

### `/montag` (Wochen-Planning)
- Erweiterung: am Ende des Montag-Workflows zeichnet Skill kurz den Wochen-Story-Bogen vor (3-Punkte-Notiz pro Tag) → `/story` greift es morgens auf

### `/reels` und `/karussell`
- Zero-Overlap (Feed vs. 24h)
- Wenn Reel/Karussell veröffentlicht wurde, kann `/story` das in 3 Story-Slides verlängern (Modus 5 Story-Serie)

### `/funnel` (Launch-Strategie)
- Modus 4 Launch in /funnel = Launch-Plan
- Modus 2 Sales-Day in /story = OPERATIVE UMSETZUNG dieses Plans
- /story liest `outputs/funnels/[slug]/launch-plan.md` automatisch

### `/produkt` (Produkterstellung)
- /produkt generiert Käufer-Archetyp-Profile
- Diese werden bei /story-Sales-Day automatisch genutzt

---

## Erfolgs-Kriterien (für Iteration nach Test-Lauf)

Der Skill ist erfolgreich, wenn:
- Patricia in **unter 10 Minuten** morgens ihren Tagesplan + Slide-PNGs hat
- **100% der Story-Tage** mind. 1 Verkaufs-Link enthalten
- Sales-Day-Modus den **kompletten Launch-Funnel** liefert ohne Patricias eigene Logik zu zwingen
- Käufertyp-Mix über 7 Tage **alle 4 DISG-Achsen** abdeckt
- doTERRA-Stories **0 Compliance-Verstösse** haben
- Patricia an Tagen ohne Lust trotzdem mit One-Slide posten kann
