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
        {"name": "Google News: Zeitmanagement", "url": "https://news.google.com/rss/search?q=Zeitmanagement%20Selbstst%C3%A4ndige%20OR%20Produktivit%C3%A4t&hl=de&gl=CH&ceid=CH:de"},
        {"name": "Zeit zu leben", "url": "https://www.zeitzuleben.de/feed/"},
        {"name": "t3n Produktivität", "url": "https://t3n.de/tag/produktivitaet/rss.xml"},
        {"name": "Toggl Blog", "url": "https://toggl.com/blog/feed"},
    ],
    "KI & Claude Code": [
        {"name": "Google News: Claude Code", "url": "https://news.google.com/rss/search?q=%22Claude%20Code%22&hl=de&gl=CH&ceid=CH:de"},
        {"name": "Google News: Anthropic", "url": "https://news.google.com/rss/search?q=Anthropic%20Claude&hl=de&gl=CH&ceid=CH:de"},
        {"name": "The Decoder", "url": "https://the-decoder.de/feed/"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    ],
}

# Pro Ressort ein eigenes Zeitfenster (Tage). News-Ressorts: 2 Tage (frisch).
# Langsame/zeitlose Ressorts (Blogs posten nicht täglich): längeres Fenster,
# damit der Bot trotzdem fast immer etwas zu zeigen hat.
CATEGORY_AGE_DAYS = {
    "Zeitmanagement & Mama-CEO-Struktur": 7,
    "Network Marketing": 7,
}

# --- YouTube-Kanäle pro Ressort ---
# RSS pro Kanal: https://www.youtube.com/feeds/videos.xml?channel_id=<ID>
# channel_id findest du über die Kanalseite (oder frag Claude, sie aufzulösen).
YOUTUBE_CHANNELS = {
    "Instagram & Social Media": [
        {"name": "Social Media Examiner", "channel_id": "UC453ZoE-0Pf7r4qKa30NlLw"},
    ],
    "Online-Business & Marketing": [
        {"name": "t3n", "channel_id": "UCSUisuyxfH1OoPCV_6qIuMw"},
        {"name": "HubSpot Marketing", "channel_id": "UCkWVA1_vkY9GLyuLAre97AQ"},
    ],
    "Network Marketing": [
        # noch kein frischer Kanal hinterlegt — bei Bedarf ergänzen
    ],
    "Zeitmanagement & Mama-CEO-Struktur": [
        {"name": "Ali Abdaal", "channel_id": "UChfo46ZNOV-vtehDc25A1Ug"},
    ],
    "KI & Claude Code": [
        {"name": "Anthropic", "channel_id": "UCrDwWp7EBBv4NwvScIpBDOA"},
        {"name": "The Morpheus (KI, DE)", "channel_id": "UCLGY6_j7kZfA1dmmjR1J_7w"},
    ],
}

VIDEO_AGE_DAYS = 7              # Videos der letzten 7 Tage gelten als "aktuell"
MAX_VIDEO_CANDIDATES = 8       # so viele Video-Kandidaten gehen max. pro Ressort in die Redaktion
MAX_VIDEOS_PER_CATEGORY = 2    # so viele Videos dürfen es pro Ressort in die Ausgabe schaffen

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
CURATION_PROMPT = """Du bist die Chefredakteurin einer täglichen Newsletter-Ausgabe (als PDF) für \
folgende Leserin und ihre Zielgruppe:

{zielgruppe}

Heutiges Ressort: "{category}".

Unten sind die heutigen Roh-Meldungen aus RSS-Feeds und YouTube. Einige Einträge sind \
YouTube-Videos — sie sind mit "(VIDEO)" markiert. Deine Aufgabe:
1. Wähle die maximal {max_picks} Beiträge aus, die für diese Zielgruppe WIRKLICH relevant sind.
   Lieber 1-2 starke Beiträge als 5 mittelmässige. Wenn NICHTS relevant ist, gib nur "KEINE" aus.
   Wenn ein wirklich relevantes, aktuelles Video dabei ist, nimm es mit auf — aber höchstens \
   {max_videos} Videos in diesem Ressort.
2. Schreibe zu jedem gewählten Beitrag eine knackige deutsche Schlagzeile und einen \
   AUSFÜHRLICHEN Absatz (4-6 Sätze): WAS ist neu/der Kern, WARUM zählt das für eine Mama mit \
   Online-Business, und – wenn möglich – ein konkreter Gedanke, wie sie es nutzen kann.
3. Sortiere nach Wichtigkeit (Wichtigstes zuerst).

Schreibe auf Deutsch, mit echten Umlauten (ä/ö/ü) und Schweizer "ss" statt "ß". \
Direkt, warm und konkret, keine Floskeln, keine erfundenen Zahlen. Bei englischsprachigen \
Quellen trotzdem auf Deutsch zusammenfassen.

Antworte AUSSCHLIESSLICH in diesem Format (ein Beitrag pro Block, getrennt durch "---"):
INDEX: <die Nummer des Original-Beitrags>
TITEL: <deine Schlagzeile>
TEXT: <ausführlicher Absatz, 4-6 Sätze>
---

Wenn kein Beitrag relevant ist, antworte nur mit: KEINE

Hier sind die Roh-Beiträge:

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

# --- PDF / Versand ---
PDF_TITLE = "Mum Life Daily"
PDF_SUBTITLE = "Deine Morgenausgabe — kuratiert für Mama-Unternehmerinnen"
PDF_INTRO = (
    "Nur das, was für dein Online-Business, dein Network und deinen Mama-CEO-Alltag "
    "wirklich zählt. Tippe auf »Weiterlesen«, um zum Beitrag zu kommen."
)
PDF_FILENAME = "mum-life-daily-{date}.pdf"  # date = YYYY-MM-DD

# Kurze Begleitnachricht, mit der das PDF in Telegram ankommt
TELEGRAM_CAPTION = """🗞️ *Mum Life Daily* — {date}

Deine heutige Ausgabe ist da: *{count} Beiträge* aus {sections} Ressorts. 📄👇"""
