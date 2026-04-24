# Plan: Content-Engine Master (Reels + Karussells + Auto-Posting)

**Erstellt:** 2026-04-21
**Status:** DRAFT — wartet auf Entscheidungen von Patricia
**Umfang:** Gesamtes Instagram-Content-System (Reels + Karussells + Trend-Research + Auto-Posting + Repost-Automation)

---

## 1. Was dieser Plan löst

Patricia will ein voll-automatisiertes Instagram-Content-System, das:
- **Montags** den Markt scrapt (Trends, Pain Points) und 10 spezifische Hooks + 5 Karussells + 5 Reels generiert
- **Täglich** Entwürfe prüft, nach Freigabe automatisch zur Zielgruppen-Zeit postet (über Blotato)
- **Monatlich** die bestperformenden Beiträge automatisch reposted (adaptiert, nicht 1:1)
- **Pro Post** via ManyChat-Keyword eine Automation triggert (→ 0€-Produkt / Minikurs)
- **In Notion** den geplanten + geposteten Content pflegt

Beide Profile strikt getrennt: **Mentoring** (Online-Business) vs. **Network** (doTERRA/Regeneration).

---

## 2. Was bereits gebaut ist (fertig)

### Dateien
- `context/reels-framework.md` — Viral-Mechanik 2026, 3-Sek-Regel, Reel-Typen, Hook-Pflicht-Prozess (strikt nach `hook-framework.md`), Talking-Head-Drehanweisungen, Caption-Strategie, Top-5-Hashtags pro Profil, Content-Pillars, Reel-Serien, Reel-Cover, Rechtliches, Untertitel, Performance-Tracking + 4-Wochen-Repost, Posting-Zeiten, Engagement-Routine
- `.claude/commands/reels.md` — 6 Modi: Konzept-aus-Idee / Rohmaterial / Hook-Brainstorm / Reel-Doktor / Wochen-Plan / Batch-Dreh

### Integrationen im Briefing
- Profil-Abfrage IMMER zürst (Mentoring vs. doTERRA)
- WebSearch Trend-Research Pflicht vor jedem Briefing
- Canva-Asset-Priorisierung (eigene Videos > Stock)
- Julia-Trost-Kaufpsychologie in Captions (Transformation statt Features)

---

## 3. Was noch gebaut wird (dieser Plan)

### Modul A: Montags-Content-Engine (Scheduled Task)
**Trigger:** Jeden Montag 06:00 Europe/Zurich
**Zwei Durchläufe:** Einmal für Mentoring, einmal für doTERRA

**Ablauf pro Profil:**
1. **Trend-Scraping** auf 7 Quellen via WebSearch/WebFetch:
   - Instagram (Hashtag-Suche nach Top-Reels/Carousels in Nische)
   - TikTok (Trend-Formate in Mama-Business / Wellness)
   - Facebook Reels (ältere, breitere Reichweite)
   - Reddit (Subreddits: r/NetworkMarketing, r/workingmoms, r/MomsWorkingFromHome, r/essentialoils, r/aromatherapy)
   - Twitter/X (Hot Takes + virale Threads)
   - Google Trends (Suchbegriff-Wellen in DE/CH)
   - Mitbewerber-Scan: spezifische Creator-Profile (müssen wir festlegen — siehe Entscheidung E)
2. **Pain-Point-Extraktion** — 5-10 aktuelle Frustrationen der Zielgruppe (mit Quellen-Zitaten)
3. **10 spezifische Hooks** nach `hook-framework.md`-Pflicht-Prozess:
   - Jede Kategorie mind. 1x (Zahlen / Anleitung / Provokant / Neugier / Identifikation)
   - Beispiel-Niveau: „Wie du mit 500 Followern und einer 5-teiligen Story-Sequenz täglich 3 Verkäufe deines 287€-Produkts machst ohne einmal ‚kauf jetzt' zu sagen"
   - Für Network-Profil adaptiert: spezifisch für **erschöpfte Mamas, die nach Jahren im Funktionsmodus sich regenerieren wollen**
4. **5 Karussell-Entwürfe** (nach Karussell-Framework — siehe Modul C) basierend auf den stärksten Hooks
5. **5 Reel-Entwürfe** (nach `reels-framework.md`) basierend auf den stärksten Hooks
6. **Video-Bedarf-Flag**: pro Reel klar markieren — „Canva-Clip X existiert" ODER „Neu aufnehmen: Dreh-Anweisung siehe unten"
7. **Feed-Aesthetic-Check**: die 5 Karussell-Cover so gestalten, dass sie im Feed-Grid mit den letzten 6-9 Posts farblich abwechseln (Petrol → Creme → Orange → Petrol → ...) — das muss der Task tatsächlich prüfen durch Blick auf die letzten Canva-Designs im Ordner „Gepostete Beiträge"
8. **Output-Speicherung** in:
   - `outputs/reels/wochenplan-YYYY-KW##-mentoring.md` (oder -doterra.md)
   - `outputs/karussells/wochenplan-YYYY-KW##-mentoring.md` (oder -doterra.md)
9. **Notification** an Patricia: kurze Zusammenfassung + Zahl fehlender Video-Aufnahmen

**Scheduled-Task-File:** `reference/scheduled-task-montag-content-engine.md` (Prompt-Template zum Einfügen in `/schedule`)

### Modul B: Tägliche Posting-Queue mit Freigabe-Flow
**Trigger:** Täglich 07:00 Europe/Zurich

**Ablauf:**
1. **Canva-Ordner „Posting Queue"** prüfen (Reels + Karussells, beide Profile)
2. Pro Design:
   - Prüfen ob Caption existiert (Kommentar-Feld)
   - Wenn keine Caption: Slide-Inhalte lesen, Caption + 5 Hashtags generieren (nach reels-framework.md / Karussell-Framework), als Kommentar am Design speichern
   - **Status-Check**: Hat Patricia das Design als „Freigegeben" markiert?
     - Wir brauchen einen Marker — Vorschlag: **grüner Punkt** oder Tag „APPROVED" im Design-Titel, ODER ein eigener Canva-Unterordner „Freigegeben"
3. **Wenn freigegeben:**
   - Asset als PNG/MP4 exportieren (Canva MCP)
   - Über Blotato Post einplanen zur nächsten Zielgruppen-Zeit (Mentoring: Di/Mi/Fr 21:00, doTERRA: Mo/Mi/Sa 21:30)
   - Design in Ordner „Gepostete Beiträge" verschieben
   - Notion Content-Manager: Eintrag „geplant" → „gepostet"
4. **Wenn nicht freigegeben:**
   - Design in Ordner „Posting Queue" lassen
   - Täglich Notification an Patricia: „X Entwürfe warten auf deine Freigabe"

**Scheduled-Task-File:** `reference/scheduled-task-posting-queue.md`

### Modul C: /karussell-Command (neu, analog zu /reels)
**Datei:** `.claude/commands/karussell.md`
**Wissensbasis:** Neue Datei `context/karussell-framework.md` (analog zu reels-framework.md)

**6 Modi:**
1. Karussell-Konzept aus Idee
2. Rohmaterial → Karussell (aus Canva-Asset-Bibliothek)
3. Hook-Brainstorm (via `hook-framework.md`)
4. Karussell-Doktor (Kritik floppender Karussells)
5. Wochen-Karussell-Plan
6. Batch-Design-Mode (mehrere Karussell-Vorlagen auf Vorrat)

**Pflicht-Schritte:** identisch zu /reels (Profil, Trend-Research, Pillar, Julia-Trost-Caption, 5 Hashtags, Feed-Aesthetic-Check, Rechtliches)

**Karussell-Spezifika:**
- Cover-Slide + 5-8 Content-Slides + CTA-Slide
- Feed-Aesthetic (Farb-Rotation im Grid)
- Mehr Text als Reel → längere Captions okay
- Saves als Primär-CTA (Karussells werden für Wissen gespeichert)

### Modul D: Monats-Repost-Automation
**Trigger:** Jeden 1. Monatstag 08:00

**Ablauf:**
1. Notion Content-Manager auslesen: alle Posts des letzten Monats mit Performance-Daten
2. Top-Performer nach Profil selektieren (Kriterien: Saves, Shares, DMs-via-Keyword)
3. **Pro Profil 2 Reposts** auswählen (1 Reel + 1 Karussell) — Gesamt 4/Monat
4. Automatisch adaptieren:
   - Neuer Hook-Text (andere Kategorie oder Template aus `hook-framework.md`)
   - Neue Caption (andere Caption-Formel)
   - Falls Reel: neuer trendiger Sound
   - Falls Karussell: Cover neu einfärben für Grid-Aesthetic
5. In Canva-Ordner „Posting Queue" ablegen als „Repost v2: [Original-Titel]"
6. Normaler Freigabe-Flow (Modul B) übernimmt

**Scheduled-Task-File:** `reference/scheduled-task-monats-repost.md`

### Modul E: ManyChat-Keyword-CTA-Integration
**In Briefings pro Post:**
- CTA-Format: „Kommentier **[KEYWORD]** und ich schick dir [konkrete Sache]"
- Keyword immer GROSSBUCHSTABEN + fett/farbig in Caption
- Pro Keyword: was wird in ManyChat getriggert (DM-Sequenz) → führt immer zu 0€-Produkt oder Minikurs
- Keywords werden aus einer zentralen Liste gezogen (**Blocker A** — siehe unten)

**Datei:** `context/manychat-keywords.md` (von Patricia zu befüllen ODER durch Vorschlag)

### Modul F: Notion-Content-Manager-Integration
**Datei:** `context/notion-content-db.md` (DB-ID + Field-Mapping)

**Pro Post wird angelegt/aktualisiert:**
- Plattform (Instagram — später erweiterbar)
- Profil (Mentoring / doTERRA)
- Typ (Reel / Karussell / Repost)
- Pillar
- Serie
- Status (Entwurf → Freigegeben → Gepostet → Archiviert)
- Posting-Datum + Uhrzeit
- ManyChat-Keyword
- Caption
- Hashtags
- Link zum Canva-Design
- Link zum Briefing-File
- Performance-Felder (Views/Saves/Shares/Comments/DMs — 48h/7d/30d)

---

## 4. Blocker — Entscheidungen die Patricia treffen muss

### Blocker A: ManyChat-Keywords
Ich finde im Workspace und Notion KEINE Keyword-Liste.

**Optionen:**
- **A1**: Du gibst mir deine aktuelle ManyChat-Keyword-Liste (Keyword → Automation-Name + was die DM schickt)
- **A2**: Ich schlage basierend auf deinen Angeboten ein Keyword-Set vor:
  - **Mentoring:**
    - `ECHT` → Workbook „Von 0 auf echt" (0€)
    - `INSTA` → Info-DM Instagram-Kundenmaschine-Minikurs
    - `NISCHE` → Info-DM Magnet-ich 1:1
    - `PRODUKT` → Info-DM „Vom Networkwissen zur digitalen Produktwelt"
    - `BUSINESS` → Info-DM „Aus Nebenbei wird Business"
  - **doTERRA:**
    - `OEL` → 0€-Mini-Notfallapotheke-Checkliste
    - `RUHE` → Abend-Routine-Guide
    - `REGENERATION` → 5-Tage-Challenge-Anmeldung
    - `SAMPLE` → Sample-Anfrage-DM

**Ich brauche**: „A1 — ich schicke Liste" ODER „A2 — nimm deinen Vorschlag"

### Blocker B: Notion Content-Manager-DB
Im Notion finde ich „Jahresplan 2026", „Wochen-Aktivitäten", „Monats-Fokus", „Content-Marketing"-Seite — aber nichts das klar als Content-Manager-DB identifizierbar ist.

**Optionen:**
- **B1**: Du gibst mir die URL/ID der existierenden DB (dann prüfe ich ob die Felder reichen oder ergänzt werden müssen)
- **B2**: Ich lege eine neue DB „Content-Manager" an mit den unter Modul F genannten Feldern (im passenden Teamspace — wo? „Mum Life Balance"-Teamspace, falls vorhanden?)

**Ich brauche**: „B1 — URL ist X" ODER „B2 — leg neu an, unter Teamspace Y"

### Blocker C: Blotato (Auto-Posting)
Blotato-MCP ist NICHT verbunden (kein Tool verfügbar). In `scheduled-tasks-instagram.md` steht Account-ID als „NOCH EINTRAGEN".

**Optionen:**
- **C1**: Du hast Blotato eingerichtet — gib mir Account-ID + MCP-Server-Name
- **C2**: Blotato ist noch nicht eingerichtet → ich baü zürst den **Halb-Automatisch-Flow**: Alles wird vorbereitet (Caption, Hashtags, Export), du musst nur den „Post"-Button in Instagram/Canva klicken. Auto-Posting kommt später.
- **C3**: Alternative wie n8n/Make nutzen (braucht Setup)

**Ich brauche**: „C1", „C2" oder „C3".

### Blocker D: doTERRA Content-Pillars bestätigen
Du hast gesagt du hast „noch keine richtigen Content-Säulen" für doTERRA. Ich habe aus `business-info.md` diese 5 vorgeschlagen:

1. Regeneration & Nervensystem
2. Selbstfürsorge-Routinen
3. Ätherische Öle im Alltag
4. Hausapotheke & Natur
5. Rückkehr zu sich selbst

**Ich brauche**: „Passt so", „Ergänze X", „Streiche X" oder „Lass uns neu definieren".

### Blocker E: Mitbewerber-Scan
Welche Creator soll der Montags-Scan aktiv beobachten?

**Beispiele wie ich es mir vorstelle:**
- **Mentoring**: Julia Trost, Laura Melina Seiler, Lina Duve, Elke Mayr (sind alle schon in `reference/` abgelegt)
- **doTERRA**: hier brauche ich von dir 3-5 Namen / Profile aus deinem Umfeld die gut performen

**Ich brauche**: Liste Mitbewerber für beide Profile (max. 5 pro Profil).

### Blocker F: Monats-Repost-Anzahl
Modul D — wie viele Reposts pro Monat?

**Vorschlag**: 2 pro Profil (1 Reel + 1 Karussell) = 4/Monat total.

**Ich brauche**: „Passt" oder andere Zahl.

---

## 5. Umsetzungsreihenfolge (wenn Blocker gelöst)

1. **Sofort (0 Blocker):** `context/karussell-framework.md` + `.claude/commands/karussell.md` anlegen
2. **Nach Blocker A + D + E:** `reference/scheduled-task-montag-content-engine.md` schreiben
3. **Nach Blocker B:** `context/notion-content-db.md` + Notion-DB ggf. anlegen
4. **Nach Blocker C:** `reference/scheduled-task-posting-queue.md` schreiben (Auto-Post oder Halb-Auto)
5. **Nach Blocker F:** `reference/scheduled-task-monats-repost.md` schreiben
6. **Zum Schluss:** CLAUDE.md aktualisieren mit /karussell + 3 Scheduled Tasks

**Aktivierung der Scheduled Tasks**: Erst nach Testlauf manüll (wir feuern den Montags-Task einmal manüll zum Check, dann aktivieren wir den Cron).

---

## 6. Technische Notizen

- **Instagram-Feed-Scraping** über WebFetch auf IG-URL liefert nur dünne Daten (Plattform blockt). Alternativen: Notion-Cache-Screenshots, Playwright-MCP (falls verfügbar) — oder wir akzeptieren dass die Aesthetic-Rotation durch Farb-Rotation in den letzten N Canva-Designs aus „Gepostete Beiträge" bestimmt wird (Canva MCP kann die Designs abrufen).
- **Mitbewerber-Scan**: gleiches Problem — nicht alle IG-Profile sind via WebFetch crawlbar. Reddit + Google Trends + Twitter/X sind die ergiebigsten Quellen für Pain-Point-Research.
- **Scheduled Task Setup**: Claude Code Scheduled Tasks (MCP `scheduled-tasks` ist verbunden, täglicher Garten-Bot läuft dort bereits). Jeden Cron-Task als Prompt-File in `reference/` abspeichern, dann manüll per `/schedule` hochladen — das ist der bereits etablierte Workflow.

---

## 7. Freigabe

- [ ] Patricia hat Blocker A-F beantwortet
- [ ] Umsetzungsreihenfolge (Abschnitt 5) akzeptiert
- [ ] Plan kann in `/implement` gegeben werden