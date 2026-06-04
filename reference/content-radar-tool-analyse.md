---
tags: [tools, research, reference]
---

# Content Radar (Julia Trost) — Tool-Analyse + Build-Konzept

**Analyse-Datum:** 2.6.2026
**URL:** https://contentradar.juliatrost.de
**Tool-Version:** 0.2.0 (Beta)
**Patricia-Status:** Eingeloggt, 445 Credits verfügbar

> **Auftrag:** Tool reverse-engineeren, dokumentieren — und Build-Konzept für Patricia's eigene Version ausarbeiten.

---

## 1. Was das Tool macht (kurz)

**Pitch des Tools:** „Content Radar analyzes social media content via Apify scrapers and computes virality scores to help you understand what makes content perform well."

**6 Hauptfunktionen** (nach Sidebar-Struktur):

| Feature | Was es macht |
|---|---|
| **Mein Profil** | Eigenen Instagram-Account analysieren (Engagement-Score, Konsistenz-Score, Virality-Score, Posts/Woche) |
| **Wettbewerb** | Konkurrenz-Accounts hinzufügen + analysieren (Patricia trackt 2: Nikoleta Kolokytha, Julia Trost) |
| **Insights** | Intelligence Hub pro Account: KPIs + Benchmark + Stärken/Schwächen + Action Plan |
| **Vergleichen** | A/B-Vergleich zweier Accounts (Patricia hat das noch nicht genutzt) |
| **Generator → Content Plan** | Aus Analysen einen Wochen/Monats-Content-Plan generieren mit Hook-Varianten |
| **Generator → Bio Generator** | Instagram-Bio optimieren |

---

## 2. Tech-Stack (reverse-engineered)

**Bestätigt:**
- **Frontend:** Next.js (App Router) — sichtbar an `/_next/static/chunks/` Pfaden
- **Hosting:** Vermutlich Vercel (Standard für Next.js-Tools)
- **Scraper-Layer:** Apify (steht explizit in der „About"-Sektion)
- **Auth:** E-Mail/Passwort (vermutlich NextAuth oder Supabase Auth)

**Stark vermutet (basierend auf Pricing-Modell):**
- **AI-Layer:** OpenAI GPT-4o (oder Claude Sonnet) für Report-Generierung + Hook-Varianten
- **Vision:** GPT-4o Vision oder Claude Vision für Bild-Analyse
- **Transkription:** OpenAI Whisper für Video-Transkription
- **Datenbank:** Supabase oder PlanetScale (für Multi-Tenant + Credit-System)
- **Queue:** BullMQ oder Inngest (für lang laufende Scrape+Analyse-Jobs)
- **Storage:** S3/R2 für Bild/Video-Caches

**URL-Struktur:**
```
/generator       → Content-Plan-Generator
/profile         → Mein Profil
/runs            → History der Scrape-Jobs
/insights        → Intelligence Hub pro Account
/vergleichen     → A/B-Vergleich
/settings        → Konto + Accounts
```

---

## 3. Credit-System & Pricing-Logik

**Verraten in der UI** („Was kostet Credits?"):

| Operation | Credits | Vermutete API-Kosten |
|---|---|---|
| 🔍 Profil-Scraping | 20-25 / Profil | Apify: $0.30-0.50 |
| 🌄 Bild-Analyse | 2 / Bild | GPT-4o Vision: ~$0.01-0.02 |
| 🎬 Video-Analyse | 5 / Video | Frames extrahieren + Vision: ~$0.05 |
| 🎙️ Video-Transkription | 3 / Video | Whisper: ~$0.006/min |
| 📊 Report & Strategie | 85 pauschal | GPT-4o lange Context: ~$0.50-1.50 |
| ✨ Bio Generator | 5 pauschal | GPT-4o-mini: ~$0.02 |

**Was ein typischer Patricia-Report kostet:**
- Scraping: 25 Credits
- 13 Videos × (5 + 3) = 104 Credits
- 12 Bilder × 2 = 24 Credits
- Report: 85 Credits
- **Total ≈ 238 Credits**

→ Bei 500 Credits-Paket „bald verfügbar" sind das ungefähr 2 Voll-Reports pro Paket.

→ Kosten für Tool-Betreiber pro Voll-Report: schätzungsweise **2-3 USD** (Apify + AI + Vision)

→ Bei einem angenommenen Preis von 49-79€ pro 500 Credits hat das Tool eine 90%+ Marge.

---

## 4. Datenmodell (aus UI abgeleitet)

### Tabelle: `users`
- id, email, display_name, created_at, credits

### Tabelle: `accounts` (Instagram-Accounts, die User trackt)
- id, user_id, handle (@mumlifebalance_patricia_ulmann), platform, status (active/inactive)
- is_competitor (boolean — eigenes Profil vs. Wettbewerber)

### Tabelle: `scrape_runs`
- id, account_id, started_at, completed_at, status (running/completed/failed)
- credits_spent, items_scraped

### Tabelle: `content_items` (gescrapte Posts/Reels/Stories)
- id, scrape_run_id, instagram_id, format (reel/carousel/image/story)
- caption, hashtags, posted_at, views, likes, comments, shares
- video_url, image_urls, transcription
- vision_analysis (JSON), virality_score (0-100)

### Tabelle: `content_plans`
- id, user_id, account_id, name, theme, target_weeks, posts_per_week
- created_at

### Tabelle: `planned_posts`
- id, content_plan_id, week (1-4), day, time, format, theme
- virality_score (0-10), strategy_rationale (Text)
- status (nicht_gepostet/geplant/gepostet/abgelehnt)
- recommended_hook, recommended_hook_type (STORIES/STATEMENTS/...)
- caption, cta, hashtags

### Tabelle: `hook_variants`
- id, planned_post_id, variant_number (0=empfohlen, 1, 2)
- hook_pattern (z.B. „DIREKTE FRAGE / NEUGIER-LÜCKE")
- hook_category (z.B. „OFFENE FRAGEN", „STATEMENTS", „STORIES")
- text

### Tabelle: `insights` (pro Account-Scan aggregiert)
- account_id, engagement_score, consistency_score, virality_score
- posts_per_week, total_followers, total_following, total_posts
- strengths (JSON), weaknesses (JSON), action_plan (JSON)

---

## 5. Was das Tool besonders macht (USPs)

1. **Virality-Score** — eigene Bewertungsskala (sichtbar 0-100 oder 0-10 je nach Kontext) — proprietäre Formel basierend auf Engagement + Watch-Time + Hook-Stärke
2. **Hook-Klassifikation** — jedem Hook wird ein Pattern zugewiesen (STORIES, OFFENE FRAGEN, STATEMENTS, etc.)
3. **3-Hook-Varianten pro Post** — empfohlen + 2 alternative Pattern
4. **Strategie-Begründung pro Post** — Text-Erklärung warum dieser Hook funktioniert
5. **Wochenziele pro KW** — übergreifender Frame über alle 5 Posts der Woche
6. **Wettbewerbs-Vergleich** — Side-by-Side A/B-Analyse
7. **Insights-Hub** mit Action-Plan — automatische Empfehlungen aus Daten

---

## 6. Was das Tool NICHT kann (Schwächen)

1. **Keine echten Patricia-Daten** — Hooks/Captions sind Fantasie-Zahlen (siehe „Sandra 1.400€"-Testimonial)
2. **Keine MBA-Korrektur** — kennt nicht Patricia's reale Produktstruktur
3. **Kein Brand-Voice-Layer** — generischer Coach-Hype-Style statt Patricia-Voice
4. **Keine Schweizer-ss-Unterstützung** — defaultet auf deutsches ß
5. **Kein doTERRA-Profil** — nur Mentoring trackbar
6. **Kein Pillar-/Säulen-System** — Themen werden flach, nicht aus Strategie abgeleitet
7. **Keine echte Markt-Recherche** — keine Reddit/Google-Trends-Integration
8. **Keine Story-Briefings** — nur Posts (Reel/Carousel), keine Story-Sequenzen
9. **Keine Visual-Generation** — keine Slides/Cover, nur Text-Output
10. **Kein Posting** — kein Blotato/Buffer-Integration, manueller Copy/Paste

---

## 7. Build-Konzept: Patricia's eigene Version

### MVP-Scope (4-6 Wochen Build)

**Modul A: Account-Tracker** (Apify-Integration für Instagram-Scrape)
- Wir haben schon `apify-scrape.yml` (täglicher Watchlist-Lauf)
- Erweitern um: Eigenes Profil + Wettbewerber + Strategie-Posts (nicht nur Aggregat)
- Speicher: Supabase (kostengünstig + DACH-Hosting)

**Modul B: Item-Analyse-Pipeline**
- Scraping → Bild-Analyse (Claude Vision) → Video-Transkription (Whisper) → Virality-Score
- **Patricia-Vorteil:** wir koppeln das an `content-radar-juni-2026.md` und `patricia-vollprofil.md` — der Score wird kalibriert auf Patricia's Top-Performer

**Modul C: Insights-Hub**
- KPIs aggregieren pro Account
- Stärken/Schwächen aus echten Patricia-Daten
- Action-Plan generieren mit Claude + bestehender Wissensbasis

**Modul D: Content-Plan-Generator**
- Wochenziel aus Patricia's Notion-Wochenplanung-DB
- Pro Slot: 3 Hook-Varianten aus verschiedenen Pattern (Zeitanker/POV/Contrarian/Story/Zahl)
- **Patricia-Vorteil:** Hooks/Captions IMMER mit echten Patricia-Zahlen aus `patricia-expertise.md` + MBA-Bundle-Struktur (siehe `KRITISCH-mba-bundle-struktur.md`)
- Markt-Recherche-Integration (Reddit/Google-Trends → Pain-Points einbauen)
- Brand-Voice-Filter (kein Stakkato, Schweizer ss, keine Hype-Preise)

**Modul E: Story-Sequenz-Generator** *(neu, hat das Tool nicht)*
- Story-Bogen über 5-8 Slides aus einem Reel-Thema ableiten
- Käufertyp-Rotation (Rot/Gelb/Grün/Blau)

**Modul F: Visual-Pipeline-Integration**
- Karussell-Briefings → bestehende `render-v2.js` Pipeline (PNG 1080×1350)
- Story-Briefings → bestehende `render-stories.js` Pipeline (PNG 1080×1920)
- Reel-Cover → automatisch generieren

**Modul G: Auto-Post via Blotato**
- Plan → Render → Upload via WP Media → Blotato Schedule
- Mit Telegram-Override (kennen wir bereits)

### Architektur-Vorschlag

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend: Next.js auf Vercel (mumlifebalance.ch/cockpit)   │
│ - Login (Auth.js)                                            │
│ - Dashboard + Plan-Generator + Insights                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend: Node.js API Routes (in Next.js)                    │
│ - /api/scrape (proxied zu Apify)                            │
│ - /api/analyze (Claude Vision + Whisper)                     │
│ - /api/generate-plan (Claude mit Patricia-Kontext)           │
│ - /api/render (Puppeteer für PNG-Output)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Daten-Layer: Supabase (Postgres + Storage + Auth)           │
│ - users, accounts, scrape_runs, content_items                │
│ - content_plans, planned_posts, hook_variants, insights      │
│ - patricia_knowledge (Embeddings der Memory-Files)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Worker-Queue: Inngest oder BullMQ                           │
│ - Scrape-Jobs (Apify)                                        │
│ - Analyse-Jobs (Claude/OpenAI)                               │
│ - Render-Jobs (Puppeteer)                                    │
│ - Schedule-Jobs (Blotato)                                    │
└─────────────────────────────────────────────────────────────┘

  Externe Services:
  ├── Apify (Scraping) — bereits live in unserer GitHub Action
  ├── Anthropic API (Claude Sonnet/Vision)
  ├── OpenAI API (Whisper für Transkription)
  ├── Notion API (Wochenplanung-DB Sync)
  ├── WordPress API (Media-Upload)
  └── Blotato API (Auto-Posting)
```

### Aufwand-Schätzung

| Modul | Tage | Komplexität |
|---|---|---|
| Modul A (Scraper) | 2-3 | Niedrig (Apify-Action existiert) |
| Modul B (Analyse) | 5-7 | Mittel (Claude Vision + Whisper Pipeline) |
| Modul C (Insights) | 4-5 | Mittel (Aggregation + Claude-Prompts) |
| Modul D (Plan-Generator) | 7-10 | Hoch (Brand-Voice-Filter + Markt-Recherche) |
| Modul E (Story-Generator) | 3-4 | Mittel |
| Modul F (Visual-Pipeline) | 2 | Niedrig (haben wir bereits) |
| Modul G (Blotato-Auto-Post) | 1-2 | Niedrig (haben wir bereits) |
| Frontend + Auth + Deploy | 5-7 | Mittel |
| **TOTAL MVP** | **29-40 Tage** | (1-Person, fokussiert) |

### Laufende Kosten (geschätzt)

Pro Patricia-Monat (Mentoring + doTERRA, ~30 Posts):
- Apify (täglicher Scrape eigene Profile + 10 Wettbewerber): ~5-10 USD
- Anthropic API (Claude für Plans + Vision): ~20-40 USD
- OpenAI API (Whisper für 30-50 Video-Transkriptionen): ~5-10 USD
- Supabase (Postgres + Storage): ~25 USD
- Vercel Hosting: 0-20 USD
- **TOTAL: ~55-105 USD/Monat**

→ Bei 500 USD Wert pro Monat (Zeit gespart + Content-Qualität) eindeutig positiv.

### Was Patricia bereits hat (Bauteile)

**Schon vorhanden, muss nur integriert werden:**
- ✅ `scripts/karussell-render/render-v2.js` (PNG-Rendering)
- ✅ `scripts/karussell-render/render-stories.js` (Story-Slides)
- ✅ `scripts/apify/` + GitHub Action (Scraping)
- ✅ `scripts/wordpress/wp-api.js` (Media-Upload)
- ✅ `scripts/blotato-post/` (Auto-Posting)
- ✅ `scripts/content-bot/telegram-send.js` (Push)
- ✅ `context/patricia-vollprofil.md` (Brand-Voice-Wissensbasis)
- ✅ `context/content-radar-juni-2026.md` (Hook-Patterns)
- ✅ Notion-Integration (Wochenplanung-DB)
- ✅ Memory-System für KRITISCHE Regeln

**Heisst:** Wir müssen nicht von Null bauen. ~60-70% der Bausteine liegen schon im Workspace. Was fehlt:
- **Frontend** (Dashboard)
- **Supabase-Backend** (zentrale DB)
- **Insights-Aggregator** (Claude-Pipeline)
- **Plan-Generator-UI** (Patricia's Tool-Interface)

→ Realistisch: **15-20 Tage** für funktionalen MVP wenn Patricia die bestehenden Skripte als Bausteine wiederverwendet.

---

## 8. Strategische Empfehlung

### Option 1: Eigenes Tool bauen (empfohlen wenn langfristige Vision)

**Pro:**
- 100% auf Patricia-Voice/MBA/doTERRA kalibriert
- Notion-Integration nativ
- Visual-Pipeline + Auto-Post integriert (das Content-Radar hat nicht)
- Story-Sequenzen + Käufertyp-Rotation eingebaut
- Skalierbar: kann später für Mentees freigeschaltet werden (= eigenes Produkt)

**Contra:**
- 15-20 Tage Build-Aufwand
- Laufende Wartung
- Initial-Investment

### Option 2: Content Radar nutzen + Übersetzungs-Layer bauen

**Pro:**
- Kein Build-Aufwand
- Tool ist bezahlt, nutze es

**Contra:**
- Patricia muss jeden Vorschlag manuell durch Brand-Voice-Filter (was wir heute machen)
- Fantasie-Zahlen müssen jedesmal ersetzt werden
- doTERRA nicht abgedeckt
- Hängt von Julia Trosts Roadmap ab (Tool ist Version 0.2.0 = sehr früh)

### Option 3: Hybrid

- Content Radar für Wettbewerbs-Tracking + Markt-Insights nutzen (das ist tatsächlich gut)
- Eigenes Tool nur für den Content-Plan-Generator-Layer bauen (das ist der schwächste Teil im Content Radar)

→ Geringster Initial-Aufwand: ~7-10 Tage

---

## 9. Mein konkreter Vorschlag

**Schritt 1 (sofort, 0 Tage):** Bestehende Workspace-Bausteine besser dokumentieren + verlinken. Wir haben schon einen halben Content-Radar — er ist nur Skript-basiert, nicht Web-UI.

**Schritt 2 (2-3 Tage):** Mini-MVP als Slash-Command `/content-radar` in Claude Code bauen, der:
- Apify-Scrape eigene Profile auslöst
- Top-Performer aus letzten 30 Tagen herausstellt
- Hook-Patterns aus echten Patricia-Posts extrahiert
- Plan mit echten Zahlen + Brand-Voice generiert

→ Patricia hat 80% des Tools dann im eigenen Workspace, ohne Frontend-Bau.

**Schritt 3 (später, wenn Bedarf):** Frontend dazu bauen wenn Patricia es als eigenes Produkt für Mentees anbieten will.

---

## 🔗 Verwandte Notizen

- [[content-radar-juni-2026]] — Hook-Patterns aus echter Analyse
- [[../scripts/apify/README]] — bestehende Scraper-Infrastruktur
- [[../scripts/karussell-render/render-v2]] — Visual-Pipeline
- [[../context/patricia-vollprofil]] — Brand-Voice-Quelle
- [[KRITISCH-mba-bundle-struktur]] — MBA-Produktstruktur (Pflicht-Quelle für Plan-Generator)
