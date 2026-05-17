---
tags: [moc, tools, scripts]
---

# 🛠️ Tools & Skripte — Map of Content

Die technische Infrastruktur. Alles in `scripts/` und `.github/workflows/`.

## 📱 Content-Auslieferung
- `scripts/blotato-post/` — Instagram-Auto-Post (Karussells + Reels)
- `scripts/karussell-render/` — HTML→PNG-Renderer (1080×1350)
- `scripts/story-render/` — Python-Story-Renderer (1080×1920)
- `scripts/story-render-bot/` — Railway-Deploy für Story-Renderer

## 🌐 WordPress
- `scripts/wordpress/` — REST-API-Helper für mumlifebalance.ch
- Tool: `wp-api.js`
- Slash-Command: `/wp`
- Memory: [[project_wordpress-integration|WordPress-Integration]]

## 💬 Bots
- `scripts/telegram-news-bot/` — Wöchentlicher News-Digest
- `scripts/telegram-userbot/` — Mail-Sweep + Telegram-Userbot
- `scripts/garten-telegram-bot/` — Garten-Bot (Submodule)
- `scripts/instagram-kundenmaschine-bot/` — IKM-Companion (in Aufbau)

## 🍳 Kochbot
- `scripts/kochbot-rag/` — Supabase Vector-DB für Rezepte

## 💰 Finanzen
- `scripts/finanzen/` — Cashflow-Tracker (PayPal + Bank)
- Memory: Cashflow-Tracker-Plan in `plans/2026-05-09-cashflow-tracker.md`

## 📊 Konkurrenz-Scraping
- GitHub Actions:
  - `apify-scrape.yml` (täglich, Watchlist)
  - `apify-discover.yml` (monatlich, Hashtag-Discovery)

## 📢 Meta Ads
- `scripts/meta-ads/` — Werbekonto-API
- Memory: [[project_meta-ads-api|Meta Marketing API]]

## ⏰ GitHub Actions (Cron)
- `.github/workflows/freitag-hooks.yml` — Fr 08:00 Voll-Auto Wochenpaket
- `.github/workflows/montag-build.yml` — Mo 12:00 Plan B
- `.github/workflows/story-reminder-daily.yml` — Tägliche Story-Erinnerung
- `.github/workflows/paypal-monthly.yml` — Cashflow

## 🎯 Verwandte Bereiche
- [[MOC-Content-Engine]] — Was die Tools auslösen

#tools #scripts #automation
