# Telegram News-Bot: Deine tägliche Mama-Business-Zeitung

Tägliche, kuratierte News-Ausgabe per Telegram — wie eine Tageszeitung, aber nur
mit dem, was für Mama-Unternehmerinnen wirklich zählt.

## Was der Bot macht

- Sammelt täglich Artikel aus RSS- & Google-News-Feeds zu **5 Ressorts**:
  - 📸 Instagram & Social Media
  - 💼 Online-Business & Marketing
  - 🤝 Network Marketing
  - ⏳ Zeitmanagement & Mama-CEO-Struktur
  - 🤖 KI & Claude Code
- Filtert auf die letzten Tage und entfernt Duplikate.
- **Claude redigiert** wie eine Chefredakteurin: pro Ressort wählt sie die für
  die Zielgruppe relevantesten Meldungen aus, filtert Rauschen (Gadget-Deals,
  US-Politik, Krypto …) und schreibt zu jeder Meldung eine Schlagzeile + 2 Sätze
  „warum das für eine Mama mit Online-Business zählt".
- Sendet die Ausgabe jeden Morgen um **07:00** per Telegram (mehrere Nachrichten,
  falls länger als das Telegram-Limit).

## Architektur

| Datei | Zweck |
|---|---|
| `config.py` | Feeds, Schedule, **Zielgruppen-Profil** (steuert die Relevanz-Auswahl), Templates |
| `feeds.py` | RSS-Abruf, Zeitfilter (pro Ressort), Deduplizierung |
| `summarizer.py` | **Redaktions-Logik** — Claude wählt aus + schreibt Schlagzeilen |
| `bot.py` | Orchestrierung, Telegram-Versand, Scheduler |

## Setup

### 1. Telegram Bot & Chat-ID
1. In Telegram **@BotFather** öffnen, `/newbot` → Token kopieren.
2. Dem Bot eine Nachricht schreiben, dann `https://api.telegram.org/bot<TOKEN>/getUpdates` öffnen → `chat.id` ablesen.

### 2. Claude API Key
[console.anthropic.com](https://console.anthropic.com) → Settings → API Keys.

### 3. Umgebungsvariablen
```bash
cp .env.example .env   # Werte eintragen
```

### 4. Lokal testen
```bash
pip install -r requirements.txt
python bot.py --now    # sofort eine Ausgabe senden (zum Testen)
python bot.py          # mit täglichem Schedule starten
```

## Deployment auf Railway
1. [Railway](https://railway.app)-Projekt mit dem GitHub-Repo verbinden.
2. Umgebungsvariablen setzen: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`,
   `ANTHROPIC_API_KEY`, `DIGEST_FREQUENCY=daily`, `SCHEDULE_HOUR=7`,
   `TIMEZONE=Europe/Zurich`.
3. Railway erkennt das `Procfile` und startet den Worker.

## Anpassen

- **Themen / Feeds:** `config.py` → `FEEDS` (Ressort hinzufügen/entfernen) und
  `CATEGORY_EMOJIS`.
- **Was ist relevant?** `config.py` → `ZIELGRUPPE` — das ist der Hebel, mit dem
  Claude entscheidet, was reinkommt und was rausfliegt.
- **Frische:** `ARTICLE_AGE_DAYS` (Default 2) bzw. `CATEGORY_AGE_DAYS` für
  langsame Ressorts (Blogs, die nicht täglich posten → längeres Fenster).
- **Menge:** `MAX_PICKS_PER_CATEGORY` (wie viele Meldungen pro Ressort).
- **Zeitpunkt / Rhythmus:** `SCHEDULE_HOUR`, `DIGEST_FREQUENCY` (`daily`/`weekly`).

## Kosten
- **Telegram:** kostenlos
- **Railway:** Free Tier reicht
- **Claude API:** ~5 kleine Haiku-Calls pro Ausgabe (ein Call pro Ressort) —
  wenige Cent pro Tag.
