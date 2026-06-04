"""
Konfiguration für den Telegram News-Bot (Tageszeitung-Modus).
Feed-URLs, Schedule, Zielgruppen-Profil und Message-Templates.
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
# Tageszeitung: läuft jeden Tag. Default 07:00 Zürich (zum Morgenkaffee).
# DIGEST_FREQUENCY: "daily" (jeden Tag) oder "weekly" (nur SCHEDULE_DAY).
DIGEST_FREQUENCY = os.getenv("DIGEST_FREQUENCY", "daily")
SCHEDULE_DAY = int(os.getenv("SCHEDULE_DAY", "0"))  # nur bei weekly relevant (0=Mo)
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "7"))  # 07:00
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Zurich")

# --- Zielgruppen-Profil (Herzstück der Relevanz-Auswahl) ---
# So entscheidet der Bot, was "für deine Zielgruppe relevant" ist.
ZIELGRUPPE = """Patricia ist Mentorin & Solopreneurin ("Mum Life Balance"). Sie und ihre \
Zielgruppe sind Mamas (oft mehrfach-Mamas), die sich neben der Familie ein \
ortsunabhängiges Online-Business und/oder Network-Marketing (doTERRA) aufbauen. \
Ihre Welt: Instagram als Haupt-Marketingkanal (Reels, Karussells, Stories), \
digitale Produkte & Online-Kurse, Kundengewinnung über Content statt Kaltakquise, \
KI als Hebel (besonders Claude / Claude Code, ChatGPT, Automationen), \
Zeitmanagement und schlanke Strukturen, um Business und 4 Kinder unter einen Hut \
zu bringen. Relevant ist alles, was diesen Frauen hilft, sichtbarer zu werden, \
mehr zu verkaufen, Zeit zu sparen oder smarter zu arbeiten. \
IRRELEVANT (rausfiltern): Gadget-Deals, Hardware-Reviews, Gaming, US-Politik, \
reine Enterprise-IT, Krypto-Spekulation, Promi-Klatsch."""

# --- RSS-Feeds nach Ressort ---
FEEDS = {
    "Instagram & Social Media": [
        {"name": "Social Media Examiner", "url": "https://www.socialmediaexaminer.com/feed/"},
        {"name": "allfacebook.de", "url": "https://allfacebook.de/feed"},
        {"name": "Hootsuite", "url": "https://blog.hootsuite.com/feed/"},
        {"name": "Metricool", "url": "https://metricool.com/feed/"},
        {"name": "Social Media Today", "url": "https://www.socialmediatoday.com/feeds/news/"},
    ],
    "Online-Business & Marketing": [
        {"name": "OMR", "url": "https://omr.com/de/feed"},
        {"name": "t3n", "url": "https://t3n.de/rss.xml"},
        {"name": "OMT", "url": "https://www.omt.de/feed/"},
        {"name": "HubSpot Marketing", "url": "https://blog.hubspot.com/marketing/rss.xml"},
        {"name": "Smart Passive Income", "url": "https://www.smartpassiveincome.com/feed/"},
        {"name": "Gründerszene", "url": "https://www.businessinsider.de/gruenderszene/feed/"},
    ],
    "Network Marketing": [
        {"name": "Business For Home", "url": "https://www.businessforhome.org/feed/"},
    ],
    "Zeitmanagement & Mama-CEO-Struktur": [
        {"name": "Zeit zu leben", "url": "https://www.zeitzuleben.de/feed/"},
        {"name": "t3n Produktivität", "url": "https://t3n.de/tag/produktivitaet/rss.xml"},
        {"name": "Toggl Blog", "url": "https://toggl.com/blog/feed"},
    ],
    "KI & Claude Code": [
        {"name": "The Decoder", "url": "https://the-decoder.de/feed/"},
        {"name": "Heise", "url": "https://www.heise.de/rss/heise-atom.xml"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
        {"name": "Hacker News: Claude Code", "url": "https://hnrss.org/newest?q=%22Claude+Code%22"},
        {"name": "Hacker News: Anthropic", "url": "https://hnrss.org/newest?q=Anthropic"},
    ],
}

# Emojis pro Ressort (für die Telegram-Nachricht)
CATEGORY_EMOJIS = {
    "Instagram & Social Media": "📸",
    "Online-Business & Marketing": "💼",
    "Network Marketing": "🤝",
    "Zeitmanagement & Mama-CEO-Struktur": "⏳",
    "KI & Claude Code": "🤖",
}

# --- Artikel-Limits ---
# Tageszeitung: kurzes Zeitfenster, damit nur frische News kommen.
ARTICLE_AGE_DAYS = 2          # nur Artikel der letzten 2 Tage einsammeln
MAX_CANDIDATES_PER_CATEGORY = 25   # so viele Rohartikel gehen max. in die Redaktion
MAX_PICKS_PER_CATEGORY = 5         # so viele dürfen es pro Ressort in die Ausgabe schaffen

# --- Redaktions-Prompt (Auswahl + Kurztext in einem Call pro Ressort) ---
CURATION_PROMPT = """Du bist die Chefredakteurin einer täglichen Newsletter-Ausgabe für \
folgende Leserin und ihre Zielgruppe:

{zielgruppe}

Heutiges Ressort: "{category}".

Unten sind die heutigen Roh-Meldungen aus den RSS-Feeds. Deine Aufgabe:
1. Wähle die maximal {max_picks} Meldungen aus, die für diese Zielgruppe WIRKLICH relevant sind.
   Lieber 1-2 starke Meldungen als 5 mittelmässige. Wenn NICHTS relevant ist, gib nur "KEINE" aus.
2. Schreibe zu jeder gewählten Meldung eine knackige deutsche Schlagzeile und 2 Sätze,
   die erklären WAS neu ist und WARUM es für eine Mama mit Online-Business zählt.
3. Sortiere nach Wichtigkeit (Wichtigstes zuerst).

Schreibe auf Deutsch, mit echten Umlauten (ä/ö/ü) und Schweizer "ss" statt "ß". \
Direkt und konkret, keine Floskeln, keine erfundenen Zahlen.

Antworte AUSSCHLIESSLICH in diesem Format (eine Meldung pro Block, getrennt durch "---"):
INDEX: <die Nummer der Original-Meldung>
TITEL: <deine Schlagzeile>
TEXT: <2 Sätze>
---

Wenn keine Meldung relevant ist, antworte nur mit: KEINE

Hier sind die Roh-Meldungen:

{articles}
"""

# --- Telegram Message Template ---
MESSAGE_HEADER = """🗞️ *Mum Life Daily*
📅 {date}

_Deine Morgenausgabe — kuratiert für Mama-Unternehmerinnen._

"""

CATEGORY_HEADER = """
{emoji} *{category}*
━━━━━━━━━━━━━━━
"""

ARTICLE_TEMPLATE = """*{title}*
{summary}
🔗 [Weiterlesen]({link})

"""

MESSAGE_FOOTER = """
———
_Automatisch kuratiert von deinem News-Bot_ 🤖
"""

NOTHING_TODAY = """🗞️ *Mum Life Daily*
📅 {date}

Heute keine relevanten Meldungen gefunden — geniess den ruhigen Tag. ☕
"""
