"""
RSS-Feed-Parsing, Deduplizierung und Zeitfilter.
"""

import logging
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

from config import ARTICLE_AGE_DAYS, FEEDS, MAX_CANDIDATES_PER_CATEGORY

logger = logging.getLogger(__name__)


def parse_published_date(entry):
    """Extrahiert das Veröffentlichungsdatum aus einem Feed-Entry."""
    for date_field in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, date_field, None)
        if parsed:
            return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
    return None


def fetch_feed(feed_info: dict) -> list[dict]:
    """Einzelnen RSS-Feed abrufen und Artikel extrahieren."""
    try:
        feed = feedparser.parse(feed_info["url"])
        if feed.bozo and not feed.entries:
            logger.warning("Feed-Fehler bei %s: %s", feed_info["name"], feed.bozo_exception)
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=ARTICLE_AGE_DAYS)
        articles = []

        for entry in feed.entries:
            published = parse_published_date(entry)
            if published and published < cutoff:
                continue

            content = ""
            if hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "content"):
                content = entry.content[0].value if entry.content else ""

            articles.append({
                "title": entry.get("title", "Ohne Titel"),
                "link": entry.get("link", ""),
                "published": published or datetime.now(timezone.utc),
                "content": content[:2000],  # Limit für API-Calls
                "source": feed_info["name"],
            })

        return articles

    except Exception:
        logger.exception("Fehler beim Abrufen von %s", feed_info["name"])
        return []


def deduplicate(articles: list[dict]) -> list[dict]:
    """Entfernt Duplikate basierend auf dem Titel (normalisiert)."""
    seen = set()
    unique = []
    for article in articles:
        key = article["title"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(article)
    return unique


def fetch_all_feeds() -> dict[str, list[dict]]:
    """
    Alle konfigurierten Feeds abrufen, filtern und nach Kategorie gruppieren.
    Gibt ein Dict zurück: {Kategorie: [Artikel, ...]}.
    """
    result = {}

    for category, feed_list in FEEDS.items():
        all_articles = []
        for feed_info in feed_list:
            articles = fetch_feed(feed_info)
            all_articles.extend(articles)
            logger.info("%s: %d Artikel von %s", category, len(articles), feed_info["name"])

        # Deduplizieren und nach Datum sortieren (neueste zuerst)
        unique = deduplicate(all_articles)
        unique.sort(key=lambda a: a["published"], reverse=True)

        # Auf Maximum begrenzen (Rohmaterial für die Redaktion)
        result[category] = unique[:MAX_CANDIDATES_PER_CATEGORY]
        logger.info("%s: %d Artikel nach Filter", category, len(result[category]))

    return result
