---
tags: [moc, research, konkurrenz]
---

# 🔍 Markt-Research & Konkurrenz — Map of Content

Daten-Grundlage für jeden Content-Output. Patricias Mantra: *„Ich will dass meine Zielgruppe denkt, ich kann ihre Gedanken lesen."*

## 🎯 Daten-Quellen
- [[competitor-watchlist.json|Konkurrenz-Watchlist]] — definierte Accounts (Apify-Cron täglich)
- [[discovery-keywords.json|Discovery-Keywords]] — Nischen-Hashtags (monatlicher Cron)

## 📊 Live-Daten (Indexe)
- [[outputs/marktrecherche/_INDEX|🔍 Marktrecherche]]
- [[outputs/zielgruppen-research/_INDEX|🎯 Zielgruppen-Research]]
- `outputs/apify-runs/` — Tägliche Scrapes (gitignored)
- [[outputs/freitag/_INDEX|📅 Freitag-Hooks (mit Markt-Analyse)]]

## 📋 Templates
- [[marktrecherche-bericht-template|Marktrecherche-Bericht-Template]]

## ⚡ Workflows
- **Täglich 06:00**: GitHub Action `apify-scrape.yml` scraped 6 Konkurrenz-Accounts
- **Monatlich 1.**: `apify-discover.yml` findet neue Top-Creator
- Doku: in `CLAUDE.md` Abschnitt "Apify Konkurrenz-Scraper"

## 🎯 Verwandte Bereiche
- [[MOC-Content-Engine]] — Hook-Generator nutzt Marktdaten
- [[MOC-Externe-Wissensbasen]] — Julia + Hormozi für Markt-Verständnis

#research #konkurrenz #markt
