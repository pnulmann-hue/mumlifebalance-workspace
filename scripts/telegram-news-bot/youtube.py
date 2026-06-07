"""
YouTube-Videos pro Ressort einsammeln (über die offiziellen Kanal-RSS-Feeds).
Liefert dieselbe Item-Struktur wie feeds.py, nur mit is_video=True.
"""

import logging
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

from config import (
    MAX_VIDEOS_PER_CHANNEL,
    VIDEO_AGE_DAYS,
    VIDEO_CATEGORY_AGE_DAYS,
    YOUTUBE_CHANNELS,
)

logger = logging.getLogger(__name__)

_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={cid}"


def _published(entry):
    for field in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, field, None)
        if parsed:
            return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
    return None


def _description(entry) -> str:
    """Holt die Videobeschreibung aus dem media:group, falls vorhanden."""
    media = entry.get("media_description")
    if media:
        return media
    if hasattr(entry, "summary"):
        return entry.summary
    return ""


def fetch_channel(channel: dict, age_days: int) -> list[dict]:
    """Lädt die neuesten Videos eines Kanals (innerhalb des Zeitfensters)."""
    try:
        feed = feedparser.parse(_FEED_URL.format(cid=channel["channel_id"]))
        if not feed.entries:
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=age_days)
        videos = []
        for entry in feed.entries:
            pub = _published(entry)
            if pub and pub < cutoff:
                continue
            videos.append({
                "title": entry.get("title", "Ohne Titel"),
                "link": entry.get("link", ""),
                "published": pub or datetime.now(timezone.utc),
                "content": _description(entry)[:1500],
                "source": channel["name"],
                "is_video": True,
            })
        return videos
    except Exception:
        logger.exception("Fehler beim Abrufen von YouTube-Kanal %s", channel["name"])
        return []


def fetch_all_videos() -> dict[str, list[dict]]:
    """Videos pro Ressort als {Kategorie: [Video, ...]}."""
    result = {}
    for category, channels in YOUTUBE_CHANNELS.items():
        age_days = VIDEO_CATEGORY_AGE_DAYS.get(category, VIDEO_AGE_DAYS)

        # Pro Kanal nur die N neuesten — damit ein Vielposter die selten
        # postenden Kanäle nicht aus dem Pool verdrängt.
        per_channel = []
        for channel in channels:
            vids = fetch_channel(channel, age_days)
            vids.sort(key=lambda v: v["published"], reverse=True)
            per_channel.append(vids[:MAX_VIDEOS_PER_CHANNEL])
            logger.info("%s: %d Videos von %s", category, len(vids), channel["name"])

        # Faire Rotation (Reissverschluss): jeder Kanal zuerst sein neuestes,
        # dann zweitneuestes usw. So sind alle Kanäle im Kandidaten-Pool vertreten.
        interleaved = []
        depth = max((len(pc) for pc in per_channel), default=0)
        for i in range(depth):
            for pc in per_channel:
                if i < len(pc):
                    interleaved.append(pc[i])
        result[category] = interleaved
    return result
