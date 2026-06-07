"""
Telegram News-Bot — Hauptskript (Tageszeitung-Modus).
Sammelt täglich News aus RSS-Feeds, lässt Claude die für die Zielgruppe
relevantesten Meldungen kuratieren und sendet die Ausgabe per Telegram.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from telegram.constants import ParseMode

from config import (
    ARTICLE_TEMPLATE,
    CATEGORY_EMOJIS,
    CATEGORY_HEADER,
    DIGEST_FREQUENCY,
    MAX_CANDIDATES_PER_CATEGORY,
    MAX_VIDEO_CANDIDATES,
    MESSAGE_FOOTER,
    MESSAGE_HEADER,
    NOTHING_TODAY,
    SCHEDULE_DAY,
    SCHEDULE_HOUR,
    SCHEDULE_MINUTE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CAPTION,
    TELEGRAM_CHAT_ID,
    TIMEZONE,
)
from feeds import fetch_all_feeds
from pdf import build_pdf
from store import add_seen, load_seen
from summarizer import curate_all
from youtube import fetch_all_videos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

WEEKDAYS_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def build_message(articles_by_category: dict[str, list[dict]]) -> str:
    """Baut die formatierte Telegram-Nachricht zusammen."""
    today = datetime.now()
    date_str = f"{WEEKDAYS_DE[today.weekday()]}, {today.strftime('%d.%m.%Y')}"

    msg = MESSAGE_HEADER.format(date=date_str)

    for category, articles in articles_by_category.items():
        if not articles:
            continue

        emoji = CATEGORY_EMOJIS.get(category, "📌")
        msg += CATEGORY_HEADER.format(emoji=emoji, category=category)

        for article in articles:
            summary = article.get("summary", "")
            source = article.get("source", "")
            if source:
                summary = f"{summary} _({source})_" if summary else f"_({source})_"
            prefix = "🎥 " if article.get("is_video") else ""
            msg += ARTICLE_TEMPLATE.format(
                title=prefix + escape_markdown(article["title"]),
                summary=summary,
                link=article["link"],
            )

    msg += MESSAGE_FOOTER
    return msg


def escape_markdown(text: str) -> str:
    """Escaped die für Telegram-Markdown (v1) relevanten Zeichen im Titel.

    Im Legacy-Markdown-Modus werden nur _ * [ ` als Entity-Marker gewertet —
    nur diese escapen, sonst erscheinen Backslashes sichtbar im Text.
    """
    for char in ("_", "*", "[", "`"):
        text = text.replace(char, f"\\{char}")
    return text


async def send_telegram_message(text: str) -> None:
    """Sendet eine Nachricht via Telegram Bot API."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Telegram hat ein 4096-Zeichen-Limit pro Nachricht
    max_len = 4000
    if len(text) <= max_len:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    else:
        # Bei langen Nachrichten aufteilen
        chunks = split_message(text, max_len)
        for chunk in chunks:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=chunk,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )


async def send_document(path: str, caption: str) -> None:
    """Sendet eine Datei (PDF) als Telegram-Dokument mit kurzer Begleitnachricht."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(path, "rb") as f:
        await bot.send_document(
            chat_id=TELEGRAM_CHAT_ID,
            document=f,
            filename=os.path.basename(path),
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
        )


def merge_candidates(
    articles: dict[str, list[dict]],
    videos: dict[str, list[dict]],
    seen: set[str],
) -> dict[str, list[dict]]:
    """Führt Artikel + Videos pro Ressort zusammen, filtert bereits Gesendetes."""
    merged = {}
    for category, arts in articles.items():
        fresh_arts = [a for a in arts if a.get("link") not in seen][:MAX_CANDIDATES_PER_CATEGORY]
        vids = [v for v in videos.get(category, []) if v.get("link") not in seen][:MAX_VIDEO_CANDIDATES]
        merged[category] = fresh_arts + vids
    return merged


def split_message(text: str, max_len: int) -> list[str]:
    """Teilt eine lange Nachricht in Chunks auf."""
    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # Am letzten Zeilenumbruch vor dem Limit trennen
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")
    return chunks


async def run_digest() -> None:
    """Führt den kompletten Digest-Workflow aus (PDF-Ausgabe)."""
    logger.info("=== Tagesausgabe wird erstellt ===")
    today = datetime.now()
    date_str = f"{WEEKDAYS_DE[today.weekday()]}, {today.strftime('%d.%m.%Y')}"
    date_iso = today.strftime("%Y-%m-%d")

    logger.info("Schritt 1: RSS-Feeds + YouTube abrufen...")
    articles = fetch_all_feeds()
    videos = fetch_all_videos()
    seen = load_seen()
    candidates = merge_candidates(articles, videos, seen)

    total = sum(len(a) for a in candidates.values())
    if total == 0:
        logger.warning("Keine frischen Beiträge gefunden. Sende 'ruhiger Tag'-Nachricht.")
        await send_telegram_message(NOTHING_TODAY.format(date=date_str))
        return

    logger.info("Schritt 2: %d Roh-Beiträge redigieren...", total)
    edited = curate_all(candidates)

    picks = sum(len(a) for a in edited.values())
    if picks == 0:
        logger.info("Keine relevanten Beiträge ausgewählt. Sende 'ruhiger Tag'-Nachricht.")
        await send_telegram_message(NOTHING_TODAY.format(date=date_str))
        return

    sections = sum(1 for items in edited.values() if items)
    logger.info("Schritt 3: PDF bauen und senden (%d Beiträge, %d Ressorts)...", picks, sections)

    try:
        pdf_path = build_pdf(edited, date_str, date_iso)
        caption = TELEGRAM_CAPTION.format(date=date_str, count=picks, sections=sections)
        await send_document(pdf_path, caption)
    except Exception:
        logger.exception("PDF-Versand fehlgeschlagen — sende Textfassung als Fallback.")
        await send_telegram_message(build_message(edited))

    # Gesendete Links merken, damit sie morgen nicht wiederkehren
    sent_links = [a["link"] for items in edited.values() for a in items if a.get("link")]
    add_seen(sent_links)

    logger.info("=== Tagesausgabe erfolgreich gesendet! ===")


async def main() -> None:
    """Startet den Bot mit täglichem (oder wöchentlichem) Schedule."""
    # Konfiguration prüfen
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN nicht gesetzt!")
        sys.exit(1)
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID nicht gesetzt!")
        sys.exit(1)

    # Prüfen ob manueller Trigger gewünscht ist
    if "--now" in sys.argv:
        logger.info("Manueller Trigger: Tagesausgabe wird jetzt erstellt...")
        await run_digest()
        return

    # Scheduler einrichten — täglich oder (Fallback) wöchentlich
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    weekly = DIGEST_FREQUENCY.lower() == "weekly"
    trigger = CronTrigger(
        day_of_week=SCHEDULE_DAY if weekly else None,  # None = jeden Tag
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        timezone=TIMEZONE,
    )
    scheduler.add_job(run_digest, trigger, id="news_digest", name="News-Tagesausgabe")
    scheduler.start()

    if weekly:
        logger.info(
            "Bot gestartet! Ausgabe jeden %s um %02d:%02d (%s).",
            WEEKDAYS_DE[SCHEDULE_DAY], SCHEDULE_HOUR, SCHEDULE_MINUTE, TIMEZONE,
        )
    else:
        logger.info(
            "Bot gestartet! Tägliche Ausgabe um %02d:%02d (%s).",
            SCHEDULE_HOUR, SCHEDULE_MINUTE, TIMEZONE,
        )

    # Bot am Laufen halten
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot wird beendet...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
