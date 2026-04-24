"""
Konfiguration für den Telegram News-Bot.
Feed-URLs, Schedule und Message-Templates.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env Datei explizit aus dem gleichen Ordner laden
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path, override=True)

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Claude API ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# --- Schedule ---
# Wochentag (0=Mo, 6=So) und Uhrzeit für den wöchentlichen Digest
SCHEDULE_DAY = int(os.getenv("SCHEDULE_DAY", "0"))  # Montag
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))  # 08:00
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Zurich")

# --- RSS-Feeds ---
FEEDS = {
    "KI & AI": [
        {
            "name": "The Verge AI",
            "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        },
        {
            "name": "MIT Technology Review AI",
            "url": "https://www.technologyreview.com/feed/",
        },
        {
            "name": "Heise KI",
            "url": "https://www.heise.de/rss/heise-atom.xml",
        },
        {
            "name": "t3n KI",
            "url": "https://t3n.de/rss.xml",
        },
        {
            "name": "AI News (VentureBeat)",
            "url": "https://venturebeat.com/category/ai/feed/",
        },
    ],
    "Onlinemarketing": [
        {
            "name": "OMR",
            "url": "https://omr.com/de/feed",
        },
        {
            "name": "Search Engine Journal",
            "url": "https://www.searchenginejournal.com/feed/",
        },
        {
            "name": "HubSpot Marketing Blog",
            "url": "https://blog.hubspot.com/marketing/rss.xml",
        },
        {
            "name": "Social Media Examiner",
            "url": "https://www.socialmediaexaminer.com/feed/",
        },
        {
            "name": "Neil Patel Blog",
            "url": "https://neilpatel.com/blog/feed/",
        },
    ],
}

# --- Artikel-Limits ---
MAX_ARTICLES_PER_CATEGORY = 10
ARTICLE_AGE_DAYS = 7

# --- Zusammenfassung ---
SUMMARY_PROMPT_SINGLE = """Fasse den folgenden Artikel in 2-3 kurzen Sätzen auf Deutsch zusammen.
Fokus auf den Kerninhalt und warum er für Onlinemarketer relevant ist.
Schreibe direkt und informativ, ohne Einleitung.

Titel: {title}
Inhalt: {content}
"""

SUMMARY_PROMPT_BATCH = """Fasse jeden der folgenden Artikel in genau 2-3 kurzen Sätzen auf Deutsch zusammen.
Fokus auf den Kerninhalt und warum er für Onlinemarketer relevant ist.
Schreibe direkt und informativ, ohne Einleitung.

Antworte im exakten Format (eine Zusammenfassung pro Artikel, getrennt durch ---):
[1] Zusammenfassung hier
---
[2] Zusammenfassung hier
---
...usw.

Hier sind die Artikel:

{articles}
"""

# --- Telegram Message Template ---
MESSAGE_HEADER = """📰 *Wöchentlicher News-Digest*
📅 {date_range}

"""

CATEGORY_HEADER = """{emoji} *{category}*
━━━━━━━━━━━━━━━
"""

ARTICLE_TEMPLATE = """{number}. *{title}*
{summary}
🔗 [Artikel lesen]({link})

"""

MESSAGE_FOOTER = """
---
_Automatisch erstellt von deinem News-Bot_ 🤖
"""
