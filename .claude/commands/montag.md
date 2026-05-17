# /montag — Karussells + Reel-Cover bauen + via Blotato für die Woche schedulen

> **🚨 ABSOLUTE PFLICHT — Read-First (Schritt 0, vor allem anderen):**
>
> **Lies ZUERST komplett:** `context/patricia-vollprofil.md` — Patricias Stimme, Werte (Freiheit + Selbstverantwortung + Genuss + Vorbild für Kinder), Wurzel-Geschichte (Mama-Alkohol-Wurzel, Schwester †2019, Convention-Wendepunkt Mai 2025, Theta-Healing), 60+ Hooks, Brand-Voice-Verbote, Mentee-Profil, Repel-Markt, 4-Säulen-doTERRA-Methodik, INTERN-Schutz. **Single Source of Truth.** Ohne diese Lese: NICHT generieren. Output muss in Patricias echter Stimme klingen — generische Coach-Sprache ist verboten.

---

Du bist der **Build- und Schedule-Skill** der Content-Pipeline. Du läufst Mo 12:00 nachdem Patricia über das Wochenende + Mo Vormittag aus den 20 Hooks gepickt hat.

**Architektur-Kontext (seit 2026-04-28):**
- `/freitag-hooks` (Fr 08:00 autonom) → schickt 20 Hooks per Telegram + Marktanalyse + Wochenfokus aus Notion
- **Patricia pickt** (Sa, So, Mo Vormittag) — 5 Hooks pro Profil
- `/montag` (du, Mo 12:00 autonom) → baut 3 Karussells + 2 Reel-Cover pro Profil + **schedulet sie direkt via Blotato für die ganze Woche (Di–Sa)**
- Kein „posting-queue-bot" mehr nötig — du scheduliest direkt am Mo 12:00 alles auf einmal.

Volle System-Doku: `reference/content-bot-system.md` + `reference/montag-workflow-v2.md`.

---

## Pick-Format das du erwartest

Patricia tippt im Chat:

```
Mentoring: M1K, M3K, M5R, M7K, M9R | doTERRA: D2K, D4R, D6K, D8K, D10R
```

Wo:
- **M** = Mentoring, **D** = doTERRA
- **Zahl 1-10** = Hook-Nummer aus heutiger `outputs/montag/YYYY-MM-DD-hooks.md`
- **K** = baue als Karussell (Mo/Mi/Fr-Slot)
- **R** = baue als Reel-Cover (Di/Do-Slot)
- **`[next]`** Suffix nach K/R = reservieren für nächste Woche (z.B. `M4K[next]`)

**Validierung:**
- Genau 5 Picks pro Profil (oder mehr mit `[next]`-Markierung)
- Mischung K/R variabel — Patricia bestimmt, du machst nicht den Defaults-Polizist
- Wenn Format unklar → 1 Klärungsfrage erlaubt, dann still

---

## Pflicht-Lektüre beim Start

1. `outputs/freitag/YYYY-MM-DD-hooks.md` (Datum = letzter Freitag) — die 20 Hooks
1a. `outputs/freitag/markt-analyse-KW[N].md` — Markt-Befunde (Pain/Wunsch/Ziel/Herausforderung) als Caption-Substanz
1b. `outputs/freitag/wochen-kontext-KW[N].json` — Wochenfokus aus Notion
2. `context/ki-phrasen-blackliste.md`
2a. **`context/job-saeulen.md` — PFLICHT! Wirkungs-Achse (A/B/C/D). Patricias Picks haben Job-Tags — die müssen auf den finalen Karussells/Reels durchgezogen werden. Plus: Build-Phase prüft Job-Mix-Compliance der Woche (siehe „Job-Mix-Check" unten).**
3. `context/patricia-expertise.md` + `patricia-freebies.md` + `manychat-keywords.md`
4. `context/brand-voice.md` + `caption-formeln.md` + `hook-framework.md`
5. `reference/content-bot-system.md` — IDs (Canva-Templates, Posting-Queue-Folder, Blotato accountIds)
6. **Memory-Regeln:** alle `feedback_*.md` (besonders: keine erfundenen Zahlen, schweben-statt-hovern, Karussell-max-10-Folien, Foto↔Neutral-Rotation)
7. `outputs/karussells/` + `outputs/reels/` letzte 4 Wochen — Doppelung vermeiden
8. ⭐ **`reference/hormozi/copywriting-bible.md`** — **Hormozi-Bonus-Layer (seit 2026-05-04)**: vor jedem Schedule via Blotato führst du einen **Hormozi-Sanity-Check** auf alle fertigen Karussell-Folien + Reel-Cover-Captions durch: **(a)** Validity-×-Utility-Filter (jede Aussage wahr UND ändert sie Verhalten?), **(b)** Hat Hook 1 wirklich pattern-interruptiert?, **(c)** Container-Wörter genutzt (System/Methode statt „Tipp")?, **(d)** Mind. ein Pain-Moment in MOMENTEN?, **(e)** Authority Stack mit 3 Zahlen wo möglich?, **(f)** Bei doTERRA: Compliance-Pivot (3.-Person-Bericht statt „du wirst…")? Findest du Verstösse → fix DIRECT mit Mini-Edit, dokumentier im Lieferungs-Output. **Brand-Voice + doTERRA-Compliance bleiben Pflicht.**

### Wenn doTERRA-Content (Profil @patricia_ulmann) — ZUSÄTZLICHE PFLICHT-LESEN

VOR jeder Caption / Folie / Hook für doTERRA:

- `context/doterra/patricia-wendepunkt-story.md` — Patricias eigene Wendepunkt-Story = Single Source of Truth für jede doTERRA-Aussage
- `context/doterra/` — komplette Wissensbasis (PDFs, Bücher, doTERRA-Schulungen, Lifestyle-Pyramide). Auch die Unter-Ordner: Basicinfos, Produktwissen, Emotionen und Öle, Mama wird Hausapothekerin, Testwoche, Werbematerial, Ölschule, öltipps
- Memory: `feedback_doterra-compliance-no-heilversprechen.md` — Strikte Compliance-No-Gos (keine Heilversprechen, „bei mir war"-Frame, Lifestyle-Bubble)
- Memory: `feedback_KRITISCH-doterra-keine-erfundenen-fakten.md` — Keine medizinischen Erfindungen

**NIE doTERRA-Content erstellen ohne diese Quellen geprüft zu haben.** Bei Unsicherheit: Patricia fragen, nicht raten.

---

## Phase 1 · Pick aufnehmen (1 Min)

Patricia hat zwischen Freitag und Mo 11:59 gepickt (Telegram-Reply oder Chat). Du:
1. Parst die Auswahl
2. Liest die letzte Freitag-Hooks-Datei (`outputs/freitag/YYYY-MM-DD-hooks.md`)
3. Resolvest die Hook-IDs zu vollen Hook-Texten + Empfehlung-Markierung (K/R aus Datei)
4. Speicherst Patricias Pick in `outputs/montag/YYYY-MM-DD-pick.md`
5. Bestätigst kurz an Patricia via Telegram: „Ok, baue jetzt 3 Karussells + 2 Reel-Cover für Mentoring + 3 K + 2 R für doTERRA und plane sie via Blotato für Di–Sa. Dauert ~20 Min."

**Wenn kein Pick vorliegt um 12:00:**
- Telegram-Push an Patricia: „Hey, brauche deine Hook-Picks für KW [N]. Ich warte 30 Min, dann kommt mein Default-Pick (PIE-balanced + Wochenfokus-passend) zum Build."
- Wenn auch nach 30 Min kein Pick: automatischen Default-Pick nehmen (3 Persönlichkeit + 3 Inspiration + 3 Expertise + 1 Wild = je Profil) und in den Build gehen — Patricia kann immer noch korrigieren bevor das erste Posting Di abends rausgeht.

### Job-Mix-Compliance-Check (PFLICHT seit 2026-05-08)

Nach Pick-Parsing: prüfe Job-Säulen-Verteilung der 5 Picks pro Profil gegen `context/job-saeulen.md`:

**Mentoring-Soll (3 Posts/Woche):**
- 1× A (Autorität) fix
- 1× B (Story) fix
- 1× C oder D (alternierend, bei aktivem Launch eher D)

**doTERRA-Soll (3 Posts/Woche, Aufbau-Phase):**
- 1× A (Autorität) fix
- 1× B (Story) fix
- 1× C (Reichweite) fix
- D nur bei aktivem Launch

**Wenn Patricias Pick zu einseitig:** sanft per Telegram melden („Hey, deine 5 Picks sind 3× Story + 2× Reichweite. Soll ich umrocken auf 1A + 1B + 1C oder lassen wir's?"). NICHT silent override — Patricia entscheidet final.

Im finalen Lieferungs-Output (Phase 5): Job-Mix der Woche dokumentieren (Mentoring: A=__ B=__ C=__ D=__ · doTERRA: ...).

---

## Phase 2 · Karussells bauen (8 Min, parallel pro Profil)

Für jeden **[K]-Pick** (insgesamt bis zu 6, also 3 pro Profil):

### 2a) Master-Template wählen
**Master für beide Profile:** `DAG8_gF0bio` „Feed-Post" (14 Seiten — in Vorlagen Karussell Folder `FAHIB-OHtP8`)

### 2a-b) Cover-Farb-Rotation prüfen (Patricia-Pflicht 2026-04-27)
Lies `outputs/montag/.cover-color-rotation.txt` (oder falls nicht existiert: aus den letzten 4 Wochen `outputs/karussells/` ableiten welche Farbe zuletzt verwendet wurde).

**Rotation pro Profil:** Grün → Blau → Beige → Grün → ...
- Karussell 1 dieser Build-Session: nächste Farbe in Rotation
- Karussell 2: übernächste
- Karussell 3: drittnächste
- Pro Profil getrennt rotieren

**Zusätzlich:** Foto-↔-Neutral-Variante innerhalb der Farbe alternieren (siehe `feedback_design-variation-cover.md`).

**Cover-Seiten-Lookup in `DAG8_gF0bio`:** TBD-Tabelle in `reference/content-bot-system.md`. Beim ersten Build dieser Session — wenn Tabelle leer:
1. Thumbnails der 14 Seiten visuell anzeigen (Markdown-Bild-Embed)
2. Patricia bitten zu identifizieren: welche Seite ist Grün-Foto, Grün-Neutral, Blau-Foto, Blau-Neutral, Beige-Foto, Beige-Neutral
3. Antworten in `reference/content-bot-system.md` Tabelle pflegen
4. Erst dann mit Build fortfahren

### 2c) Design klonen via `merge-designs`
- 10 Folien (max-Limit, siehe `feedback_instagram-karussell-max-10-folien.md`)
- Struktur: Cover (Hook in passender Farbe) + 8 Inhalts-Folien + About-Me/CTA
- Per `merge-designs` create_new_design mit insert_pages aus dem Master `DAG8_gF0bio`
- Cover-Seite ist die identifizierte Farb-Seite. Inhalts-Folien sind Standard-Folien aus dem Master.

### 2d) Text anpassen via `perform-editing-operations`
- Cover-Folie: Hook + Sub-Hook
- Inhalts-Folien: Patricia-Voice, Brand-Voice-konform, max 80 Wörter pro Folie
- CTA-Folie: passend zum Profil (Manychat-Keyword aus `manychat-keywords.md`)

### 2d) Design committen + verschieben
- `commit-editing-transaction`
- Verschieben in `FAHID6j-TOM` (Vorbereitet)
- Titel: `[Profil] [YYYY-MM-DD] — [Slug]` z.B. `Mentoring 2026-04-27 — Vortragssaal`

### 2e) Initial-Caption schreiben
- Speichern in `outputs/karussells/YYYY-MM-DD-[profil]-[slug]-caption.md`
- **🚨 KEINE STAKKATO-SÄTZE** (siehe `feedback_KRITISCH-keine-stakkato-saetze.md`) — Captions in fliessendem Mama-Sprech wie am Küchentisch mit einer Freundin. Konjunktionen verbinden Sätze („und da", „weil", „aber", „bis"). NIE drei abgehackte Subject-Verb-Punkt-Sätze hintereinander. DU-Anrede für Pain. Patricia hat das MEHRFACH angemahnt. Hormozi-Pattern ist STRUKTUR, nicht Sprach-Form — Patricia-Voice gewinnt.
- Preflight-Check (Blackliste, Stakkato-Pflicht-Check, Schweizer ss durchgängig, echte Umlaute, etc.)
- WICHTIG: Diese Caption ist nur Initial-Version. Daily-Bot regeneriert beim Schedulen.

---

## Phase 3 · Reel-Cover bauen (5 Min, parallel pro Profil)

Für jeden **[R]-Pick** (insgesamt bis zu 4, also 2 pro Profil):

### 3a) Cover-Design via `merge-designs`
- Aus Master-Template `DAGT24dj8LE` „Reel" (33 Seiten — in Vorlagen Reelcover Folder `FAHIBxLCntE`)
- **Vorlagen-Seiten-Rotation:** State-Datei `outputs/montag/.reel-cover-page-rotation.txt` lesen (zuletzt verwendete Seite pro Profil) → andere Seite wählen (siehe `feedback_design-variation-cover.md`)
- Wähle Seite die zum Hook-Stil passt (dunkle für Provokation/Hot-Take, helle/neutral für Wissen)
- 1 Page, 1080×1920
- Nach Build: State-Datei mit neuer Seitennummer updaten

### 3b) Optional: Bild-Tausch (~30% der Builds, Patricia-Wunsch 2026-04-27)
- In ~30% der Reel-Cover-Builds: Bild der Cover-Seite tauschen für extra Variation
- Bilder aus Patricia's Canva-Uploads abrufen (via `get-assets` oder Bild-Suche)
- Lokaler Fallback: `context/Shootingbilder/`
- Via `update_fill` mit asset_type=image das Cover-Bild tauschen

### 3c) Text anpassen
- Hook + ggf. Sub-Hook (kursiv, etwas kleiner)
- Patricia-Brand-Font (Philosopher), Brand-Farben

### 3d) Design committen + verschieben
- Verschieben in `FAHID6j-TOM` (Vorbereitet)
- Titel: `[Profil] Reel Cover [YYYY-MM-DD] — [Slug]`

### 3d) Reel-Briefing speichern
- `outputs/reels/YYYY-MM-DD-[profil]-[slug]-reel.md`
- Enthält: Cover-Text, Caption (Initial), Hashtags, Posting-Hinweis (Patricia macht Video manuell)

---

## Phase 4 · Karussells via Blotato schedulen (5 Min)

**NEU seit 2026-04-28:** Nach dem Build schedulest du die 3 Karussells pro Profil DIREKT via Blotato für die Woche. Patricia muss nichts mehr manuell verschieben.

### Schedule-Slots pro Woche

**Karussells: Mo + Mi + Fr · 19:30 pro Profil (3 pro Profil = 6 total)**

| Tag | Profil | Was | Slot |
|---|---|---|---|
| **Mo 19:30** | Mentoring | Karussell 1 | **Blotato-Schedule** (heute, 7h Vorlauf — Build läuft 12:00) |
| Di 19:30 | Mentoring | Reel-Cover 1 | Patricia dreht/postet manuell |
| **Mi 19:30** | Mentoring | Karussell 2 | **Blotato-Schedule** |
| Do 19:30 | Mentoring | Reel-Cover 2 | Patricia dreht/postet manuell |
| **Fr 19:30** | Mentoring | Karussell 3 | **Blotato-Schedule** |
| **Mo 19:30** | doTERRA | Karussell 1 | **Blotato-Schedule** (heute, 7h Vorlauf) |
| **Mi 19:30** | doTERRA | Karussell 2 | **Blotato-Schedule** |
| **Fr 19:30** | doTERRA | Karussell 3 | **Blotato-Schedule** |

→ **6 Karussell-Schedules pro Woche** (3 pro Profil: Mo/Mi/Fr). Plus 4 Reel-Cover (2 pro Profil) ohne Auto-Schedule — Patricia dreht selbst.

### Schedule-Flow pro Karussell

1. **Export aus Canva:** `export-design` → JPGs (1080×1350)
2. **Caption finalisieren:** aus dem Build-Briefing (Phase 2e) übernehmen, ggf. Wochenfokus + Markt-Analyse-Befund einbauen
3. **Build Blotato-Config:** `scripts/blotato-post/post-configs/YYYY-MM-DD-[profil]-[slug].json` mit:
   - `accountId`: Mentoring `41414` / doTERRA `41413`
   - `platform: instagram`
   - `mediaType: image`
   - `scheduledTime`: ISO-8601 mit +02:00 (Schweiz)
   - `text`: Caption
   - `mediaUrls`: Canva-JPG-Links
4. **Schedule:** `node scripts/blotato-post/schedule-post.js --config=...`
5. **Logge Submission-ID** in `outputs/montag/YYYY-MM-DD-build.md`

### Spezielle Compliance-Slots

- **doTERRA-Karussells:** Vor dem Schedule Compliance-Check gegen `feedback_doterra-compliance-no-heilversprechen.md`. Wenn Caption irgendwas wie „heilt / hilft gegen / bekämpft" hat → STOP, Patricia fragen.
- **Mentoring-Karussells:** Standard-Preflight (Blackliste, Schweizer ss, max 10 Folien)

---

## Phase 5 · Lieferung an Patricia (2 Min)

Nach allen Builds + Schedules:

```
✅ Build + Schedule fertig — 6 Karussells gescheduled, 4 Reel-Cover bereit

📋 Mentoring (3 Karussells gescheduled + 2 Reel-Cover bereit):
🟦 Mi 19:30 — M1 [Hook-Kurz] → Blotato [Submission-ID] · Canva [Link]
🟦 Fr 19:30 — M3 [Hook-Kurz] → Blotato [Submission-ID] · Canva [Link]
🟦 Mo nächste Wo — M7 [Hook-Kurz] → Blotato [Submission-ID] · Canva [Link]
🎬 Di 19:30 — RM5-Cover [Hook-Kurz] → Canva [Link] (du drehst Reel)
🎬 Do 19:30 — RM9-Cover [Hook-Kurz] → Canva [Link] (du drehst Reel)

📋 doTERRA (3 Karussells gescheduled + 2 Reel-Cover bereit):
[analog]

—

Nächste Schritte:
1. Karussells laufen automatisch — du musst nichts mehr verschieben
2. Reel-Cover bereit — du drehst die 2 Reels nach Drehbuch in `outputs/reels/`
3. Wenn fertig: MP4 + Cover hier in den Chat → ich plane via Blotato

Wenn du eine Caption ändern willst: Cancele die Blotato-Submission im Blotato-UI + schick mir die neue Caption.
```

Telegram-Push:
```
✅ 6 Karussells gescheduled für die Woche · 4 Reel-Cover bereit zum Drehen
📂 outputs/montag/YYYY-MM-DD-build.md
```

---

## Wenn `outputs/freitag/YYYY-MM-DD-hooks.md` nicht existiert

Patricia hat `/montag` ohne vorherigen `/freitag-hooks` getippt (selten — sollte nur passieren wenn Cron Fr 08:00 ausgefallen ist). Drei Optionen:

1. **Fallback A:** Schau ob es eine ältere hooks-Datei aus dieser Woche gibt → benutze die
2. **Fallback B:** Frag Patricia: „Keine Freitag-Hooks-Datei gefunden. Soll ich /freitag-hooks jetzt nachholen rennen lassen?" → wenn ja, Skill triggern
3. **Fallback C:** Wenn Patricia einen direkten Hook-Vorschlag im Chat schickt, nutze den

---

## Harte Regeln

1. **Zero invented numbers** — wenn eine Zahl im Hook nicht in `patricia-expertise.md` steht: abstrahieren oder Patricia fragen
2. **Zero AI-generated Visuals** — niemals `generate-design`. Nur `merge-designs` aus ihrer Template-Library
3. **Karussell max 10 Folien** — IMMER. (Instagram-API-Limit via Blotato, siehe `feedback_instagram-karussell-max-10-folien.md`)
4. **Reel-Cover ist 1 Page** (1080×1920) — nicht versuchen, Reel-Videos zu machen
5. **Foto↔Neutral-Rotation** beim Cover-Design beachten
6. **Schweizer ss, echte Umlaute, Blackliste** — immer
7. **Alle Designs in Claude Designs (`FAHID6j-TOM`) ablegen** — Patricia verschiebt selbst in die Posting Queues

---

## Erweiterung: Wochen-Story-Bogen für /story vorzeichnen

Nach dem Build (am Ende der Session) zeichnet der Skill kurz den Story-Bogen für die Woche vor. So weiss `/story` morgens schon den Wochenkontext.

### Output

In `outputs/montag/YYYY-MM-DD-build.md` zusätzliche Sektion:

```markdown
## Wochen-Story-Bogen (Briefing für /story)

**Wochen-Hauptthema:** [aus Notion-Wochenplan oder Patricias Input]
**Aktiver Funnel zum Bewerben:** [aus active-funnels.json]

### Story-Bogen über die Woche

| Tag | Story-Säule | DISG-Achse | Idee (1 Satz) |
|---|---|---|---|
| Mo | Persönlichkeit | Grün | Wochenstart-Behind-the-Scenes |
| Di | Expertise | Rot | Action-Tipp zum Wochen-Hauptthema |
| Mi | Inspiration | Gelb | Spielerischer Quiz-Tag |
| Do | Expertise | Blau | Schritt-für-Schritt zum Hauptthema |
| Fr | Persönlichkeit | Gelb | Lifestyle-Glimpse + Wochenausblick |
| Sa | Persönlichkeit | Grün | Familie/Mama-Realität |
| So | Expertise | Rot | Reflexion + Pitch |

### Sales-Day-Trigger
Falls `active-funnels.json` einen Funnel mit Status „launching" hat:
- Empfehlung an Patricia: an Tag X `/story sales-day` triggern
- Falls vorhanden: `outputs/funnels/[slug]/launch-plan.md` referenzieren
```

**Wichtig:**
- Skill baut NICHT die Story-Slides selbst — das ist Aufgabe von `/story` morgens
- Nur 1-Satz-Ideen pro Tag — Patricia nutzt sie als Anker, kann morgens überschreiben
- Wenn Wochenplan keinen klaren Hauptfokus hat: Bogen mit Fragezeichen liefern → Patricia ergänzt
