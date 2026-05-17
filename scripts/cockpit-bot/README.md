# Cockpit-Bot — Patricia's Daily Operator

Telegram-Bot der täglich morgens 06:30 + mittags 12:00 Patricia mit Tagesbriefing + News versorgt.

## Features

- 🌅 **Mo-Fr 06:30** — Tagesbriefing aufs Handy:
  - Profil heute (Mentoring/doTERRA)
  - Hauptbrocken
  - Top 3 Hebel (Money-Making-First)
  - Tasks aus Notion
  - **📊 Ads-Performance** (Mo-Fr wenn aktive Kampagnen laufen)
  - News-Block (Mo: KI/Instagram/Digitale Produkte, Di-Fr: leer)

- 🍽️ **Mo-Fr 12:00** — Mittag-Check:
  - Status-Prüfung (Hebel/Story/DMs)
  - Wenn-noch-nicht-Hilfe
  - Auszeit-Reminder

- 🌿 **Sa+So** — kurzer Auszeit-Push

## Telegram-Commands

| Command | Was |
|---|---|
| `/start` | Welcome |
| `/cockpit` | Tagesbriefing on-demand |
| `/news` | News-Sektion on-demand |
| `/status` | Bot-Status |

## Setup-Anleitung

### 1. Telegram-Bot erstellen
Falls noch nicht: `@BotFather` → `/newbot` → Token kopieren

### 2. Env-Vars in `.env` (Workspace-Root)
```
TELEGRAM_COCKPIT_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...        (deine Chat-ID, gleiche wie Content-Bot)
ANTHROPIC_API_KEY=...
NOTION_API_KEY=...

# Optional — wenn Werbeanzeigen-Performance im Briefing erscheinen soll:
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_...
META_CURRENCY=CHF
```

### 3. Lokal testen
```bash
cd scripts/cockpit-bot
pip install -r requirements.txt
python config.py     # Setup-Check
python bot.py        # Bot starten
```

### 4. Bei Telegram-Bot `/start` tippen
Damit der Bot deine Chat-ID kennt + bei Push aktiv ist.

### 5. Railway-Deploy
- https://railway.app → bestehendes Projekt → **+ New Service** → GitHub-Repo
- Root Directory: `scripts/cockpit-bot`
- Variables: gleiche 4 Env-Vars wie oben
- Deploy startet automatisch

## Architektur

```
bot.py                  Haupt-Einstiegspunkt (Cron + Telegram)
config.py               Tokens + Notion-IDs + Meta-Credentials
notion_reader.py        Notion-DB-Reads
notion_writer.py        Notion-Tagesplaner-Page-Updates
briefing_builder.py     Claude-API für Briefings
news_fetcher.py         Web-Search für News-Aggregation (Mo)
ads_fetcher.py          Meta-Marketing-API → Ads-Performance (Mo-Fr)
```

## Kosten

- Anthropic Claude: ~$0.05 pro Briefing × 5 Tagebriefings + 5 Mittag = $0.50/Woche = ~$2-3/Monat
- News-Fetcher: Claude mit web_search-Tool, ~$0.10 pro Briefing-mit-News = $2/Monat extra
- Railway: $0 zusätzlich (im bestehenden Project-Plan)

**Total: ~$5/Monat**
