# Mealplan PDF + Telegram

Rendert einen Wochenplan-Markdown (mit Google-Doc-Links zu Rezepten) zu einem hübsch gestylten **PDF mit klickbaren Hyperlinks** und sendet es via Telegram-Bot an Patricia.

## Usage

```bash
cd scripts/mealplan-pdf-telegram
node send-mealplan.js ../../outputs/mealplans/2026-KW20-wochenplan.md KW20
```

## Was es macht

1. Liest Markdown-Datei
2. Markdown → HTML (via `marked`)
3. HTML → A4-PDF (via Puppeteer) — Hyperlinks bleiben klickbar
4. Speichert PDF neben der MD-Datei (z. B. `…/2026-KW20-wochenplan.pdf`)
5. Sendet PDF via Telegram Bot API (`sendDocument`) an Patricias Chat
6. Caption mit Wochen-Label

## Anforderungen

- Node 18+
- `../md-to-pdf/node_modules/` muss existieren (für `marked` + `puppeteer`)
- `../telegram-news-bot/.env` mit:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID` (Patricias Chat)

## Markdown-Konventionen

- Klickbare Rezeptlinks: standard Markdown-Syntax `[Rezept](https://docs.google.com/...)` 
- Tabellen mit `|` Spalten-Trennern (GFM)
- Headings `#`/`##`/`###`/`####`

## Erweitert von

`/mealplan` Skill — der Skill ruft dieses Script am Ende jeder Wochenplanung auf.

## Debug

PDF nicht erzeugt? Häufige Ursachen:
- Puppeteer Chrome-Download fehlt → `cd ../md-to-pdf && node node_modules/puppeteer/install.mjs`
- Telegram-Fehler → Token / Chat-ID prüfen mit:
  ```
  curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
  ```
