# Session-Zusammenfassung 16.-17.5.2026 — Meta Ads + Cockpit-Bot live

## Was wir heute geschafft haben

### 1. Meta Marketing API Setup (komplett)
- Facebook-Developer-App **„Mum Life Balance Bot"** erstellt (App-ID 984115153982698, Live-Mode)
- System-User **„Patricia Cockpit-Bot"** angelegt (61589883837818)
- 60-Tage User-Token generiert mit allen 5 Permissions (ads_management/ads_read/business_management/pages_read_engagement/pages_show_list)
- Token läuft bis ~15. August 2026, gespeichert in `scripts/meta-ads/.env`
- `scripts/meta-ads/meta-api.js` CLI-Helper (whoami, list, insights, pause, activate, set-budget)
- `scripts/meta-ads/create-webinar-ad.js` One-Shot-Helper (Image-Upload + Creative + Ad)

### 2. Webinar-Anzeige für KI-Mastermind 20.5.
- **Campaign:** `120250147108050054` „KI-Mastermind Webinar Mai 2026" — OUTCOME_TRAFFIC, ACTIVE
- **AdSet:** `120250147119200054` „Cold DACH Frauen 30-45 · CHF 15/Tag"
  - Targeting: CH+DE+AT, Frauen 30-45, Deutsch
  - Interest-Layer: Female Entrepreneur Association + Unternehmerin + Social-Media-Marketing
  - Optimization: LANDING_PAGE_VIEWS
  - Laufzeit: bis Mi 20.5. 07:30 (Webinar-Start 09:00)
- **Creative:** `1614930772899502` (Variante B — Hormozi-Reframe „Tool-Frage statt Disziplin-Frage")
- **Ad:** `120250148012690054` „KI-Webinar B Mompreneurin-Reframe · 20.5."
- Visual: Mama+KI-Mockup mit Brand-Farben (von Manus, Mompreneurin am Laptop + Kind unscharf im Hintergrund)
- Alte ACTIVE-Kampagne „03/26 PU_Umsatz_Finde dein Thema" pausiert

### 3. Cockpit-Bot mit Ads-Performance erweitert + deployed
- Code: `scripts/cockpit-bot/` mit 11 Python-Files + Procfile/nixpacks.toml
- **NEU: `ads_fetcher.py`** liest Meta-API täglich, baut Performance-Block mit Diagnose
- `briefing_builder.py` erweitert: Ads-Sektion in Kompakt + Volltext-Modus
- `bot.py` ruft Ads-Block bei jedem Morgen-Briefing
- Performance-Diagnose nach Julia-Heuristik (CTR/CPL/Frequency-Thresholds mit Skalierungs-Empfehlung)

### 4. Deployment auf Railway
- **Service:** `mumlifebalance-workspace` im Projekt `captivating-balance`
- **Root Directory:** `scripts/cockpit-bot`
- **Python 3.12.7**, 7 Env-Vars eingetragen
- Build #1 failed (Code noch nicht in main) → PR #5 gemerged (mit Konflikt-Resolve) → Build #2 erfolgreich
- Service-Status: ACTIVE, ONLINE
- Erster Telegram-`/start` getestet ✅

### 5. Schedule live ab 18.5.
- Mo-Fr 06:30 → Tagesbriefing + Ads-Performance (Mo zusätzlich Wochen-News)
- Mo-Fr 12:00 → Mittag-Check
- Sa+So 06:30 → kurzer Auszeit-Push

## ⚠️ Offene Punkte
- **Railway-Trial läuft in 2 Tagen ab** (orange Banner „2 days or $2.52 left") — Patricia muss upgraden, sonst alle Services offline
- `/ads`-Skill formal bauen (kommt nächste Session) — kompletter Werbeanzeigen-Workflow als Skill
- Worker-Service zeigte „Crashed" beim Variables-Update — vermutlich self-recovered, beobachten

## Kosten
- Meta Ads: CHF 15/Tag × 4 Tage = ~CHF 60 für Webinar-Push
- Cockpit-Bot: ~$5/Monat (Claude + Railway-Anteil)

## Tracking
- Performance-Daten kommen morgen früh automatisch per Telegram + in Notion-Tagesplaner-Page
- Performance-Review Sa 17.5. (heute spät) / So 18.5. morgens
- Webinar-Tag 20.5. 06:00: Ads pausieren via `/cockpit` oder manuell in Meta
