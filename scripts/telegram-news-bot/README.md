# Telegram News-Bot: Onlinemarketing & KI

Wöchentlicher News-Digest mit KI-Zusammenfassungen per Telegram.

## Was der Bot macht

- Sammelt Artikel aus 10+ RSS-Feeds (Onlinemarketing & KI)
- Filtert auf die letzten 7 Tage, entfernt Duplikate
- Fasst jeden Artikel mit Claude in 2-3 Sätzen auf Deutsch zusammen
- Sendet den Digest jeden Montag um 08:00 per Telegram

## Setup

### 1. Telegram Bot erstellen

1. Öffne Telegram und suche nach **@BotFather**
2. Sende `/newbot` und folge den Anweisungen
3. Kopiere den **Bot Token**

### 2. Chat-ID ermitteln

1. Sende deinem neuen Bot eine beliebige Nachricht
2. Öffne im Browser: `https://api.telegram.org/bot<DEIN_TOKEN>/getUpdates`
3. Finde deine `chat.id` in der Antwort

### 3. Claude API Key

1. Gehe zu [console.anthropic.com](https://console.anthropic.com)
2. Erstelle einen API-Key unter Settings > API Keys

### 4. Umgebungsvariablen

Kopiere `.env.example` zu `.env` und trage deine Werte ein:

```bash
cp .env.example .env
```

### 5. Lokal testen

```bash
# Dependencies installieren
pip install -r requirements.txt

# Sofort einen Digest senden (zum Testen)
python bot.py --now

# Bot mit wöchentlichem Schedule starten
python bot.py
```

## Deployment auf Railway

1. Erstelle ein [Railway](https://railway.app) Projekt
2. Verbinde dein GitHub-Repository
3. Setze die Umgebungsvariablen in Railway:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `ANTHROPIC_API_KEY`
   - `TIMEZONE=Europe/Zurich`
4. Railway erkennt das `Procfile` automatisch und startet den Worker

## Konfiguration

### Feeds anpassen

In `config.py` unter `FEEDS` kannst du RSS-Feeds hinzufügen oder entfernen.

### Schedule ändern

Über Umgebungsvariablen:
- `SCHEDULE_DAY` — Wochentag (0=Montag, 6=Sonntag)
- `SCHEDULE_HOUR` — Stunde (0-23)
- `SCHEDULE_MINUTE` — Minute (0-59)
- `TIMEZONE` — Zeitzone (z.B. `Europe/Zurich`)

## Kosten

- **Telegram**: Kostenlos
- **Railway**: Free Tier (500h/Monat) reicht für diesen Bot
- **Claude API**: ~$0.05-0.15 pro wöchentlichen Digest (je nach Artikelanzahl)
