# Telegram News-Bot: Deine tägliche Mama-Business-Zeitung

Tägliche, kuratierte News-Ausgabe per Telegram — wie eine Tageszeitung, aber nur
mit dem, was für Mama-Unternehmerinnen wirklich zählt.

## Was der Bot macht

- Sammelt täglich **Artikel (RSS + Google News)** und **YouTube-Videos** zu **5 Ressorts**:
  - 📸 Instagram & Social Media
  - 💼 Online-Business & Marketing
  - 🤝 Network Marketing
  - ⏳ Zeitmanagement & Mama-CEO-Struktur
  - 🤖 KI & Claude Code
- Filtert auf die letzten Tage, entfernt Duplikate und merkt sich bereits
  gesendete Beiträge (`seen_links.json`), damit nichts mehrfach kommt.
- **Claude redigiert** wie eine Chefredakteurin: pro Ressort wählt sie die für
  die Zielgruppe relevantesten Beiträge aus (inkl. max. 2 Videos), filtert
  Rauschen (Gadget-Deals, US-Politik, Krypto …) und schreibt zu jedem Beitrag
  eine Schlagzeile + einen ausführlichen Absatz „warum das für eine Mama mit
  Online-Business zählt".
- **Liefert die Ausgabe als PDF** (klickbare Links, Brand-Farben, Video-
  Markierung) mit kurzer Begleitnachricht — jeden Morgen um **07:00** per Telegram.
  Fällt der PDF-Bau aus, geht automatisch die Textfassung raus.

## Architektur

| Datei | Zweck |
|---|---|
| `config.py` | Feeds, **YouTube-Kanäle**, Schedule, **Zielgruppen-Profil** (steuert die Relevanz-Auswahl), Templates |
| `feeds.py` | RSS-Abruf, Zeitfilter (pro Ressort), Deduplizierung |
| `youtube.py` | YouTube-Videos pro Ressort (Kanal-RSS) |
| `summarizer.py` | **Redaktions-Logik** — Claude wählt aus + schreibt Schlagzeilen + Texte |
| `pdf.py` | PDF-Erzeugung (reportlab) mit Links & Video-Markierung |
| `store.py` | „schon gesendet"-Speicher gegen Wiederholungen |
| `bot.py` | Orchestrierung, PDF-/Telegram-Versand, Scheduler |

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
- **YouTube-Kanäle:** `config.py` → `YOUTUBE_CHANNELS`. Pro Kanal brauchst du die
  `channel_id` (Format `UC…`). Findest du auf der Kanalseite im Quelltext
  (`"channelId":"UC…"`) — oder bitte Claude, einen @handle aufzulösen.
- **Was ist relevant?** `config.py` → `ZIELGRUPPE` — das ist der Hebel, mit dem
  Claude entscheidet, was reinkommt und was rausfliegt.
- **Frische:** `ARTICLE_AGE_DAYS` (Default 2), `CATEGORY_AGE_DAYS` für langsame
  Ressorts, `VIDEO_AGE_DAYS` (Default 7) für Videos.
- **Menge:** `MAX_PICKS_PER_CATEGORY` (Beiträge/Ressort) und
  `MAX_VIDEOS_PER_CATEGORY` (Videos/Ressort).
- **PDF-Optik:** `pdf.py` (Brand-Farben oben) und `PDF_TITLE`/`PDF_SUBTITLE`/
  `PDF_INTRO` in `config.py`.
- **Zeitpunkt / Rhythmus:** `SCHEDULE_HOUR`, `DIGEST_FREQUENCY` (`daily`/`weekly`).

## Kosten
- **Telegram:** kostenlos
- **Railway:** Free Tier reicht
- **Claude API:** ~5 kleine Haiku-Calls pro Ausgabe (ein Call pro Ressort) —
  wenige Cent pro Tag.
