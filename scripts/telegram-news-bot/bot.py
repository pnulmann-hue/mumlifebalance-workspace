"""
Telegram News-Bot — Hauptskript (Tageszeitung-Modus).
Sammelt täglich News aus RSS-Feeds, lässt Claude die für die Zielgruppe
relevantesten Meldungen kuratieren und sendet die Ausgabe per Telegram.
"""

import asyncio
import logging
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
    MESSAGE_FOOTER,
    MESSAGE_HEADER,
    NOTHING_TODAY,
    SCHEDULE_DAY,
    SCHEDULE_HOUR,
    SCHEDULE_MINUTE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TIMEZONE,
)
from feeds import fetch_all_feeds
from summarizer import curate_all

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
            msg += ARTICLE_TEMPLATE.format(
                title=escape_markdown(article["title"]),
                summary=summary,
                link=article["link"],
            )

    msg += MESSAGE_FOOTER
    return msg


def escape_markdown(text: str) -> str:
    """Escaped spezielle Markdown-Zeichen für Telegram."""
    special_chars = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]
    for char in special_chars:
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
    """Führt den kompletten Digest-Workflow aus."""
    logger.info("=== News-Digest wird erstellt ===")

    logger.info("Schritt 1: RSS-Feeds abrufen...")
    articles = fetch_all_feeds()

    total = sum(len(a) for a in articles.values())
    if total == 0:
        logger.warning("Keine Artikel gefunden. Digest wird übersprungen.")
        return

    logger.info("Schritt 2: %d Artikel zusammenfassen...", total)
    articles = summarize_articles(articles)

    logger.info("Schritt 3: Nachricht formatieren und senden...")
    message = build_message(articles)
    await send_telegram_message(message)

    logger.info("=== Digest erfolgreich gesendet! ===")


async def main() -> None:
    """Startet den Bot mit wöchentlichem Schedule."""
    # Konfiguration prüfen
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN nicht gesetzt!")
        sys.exit(1)
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID nicht gesetzt!")
        sys.exit(1)

    # Prüfen ob manueller Trigger gewünscht ist
    if "--now" in sys.argv:
        logger.info("Manueller Trigger: Digest wird jetzt erstellt...")
        await run_digest()
        return

    # Scheduler einrichten
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    trigger = CronTrigger(
        day_of_week=SCHEDULE_DAY,
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        timezone=TIMEZONE,
    )
    scheduler.add_job(run_digest, trigger, id="weekly_digest", name="Wöchentlicher News-Digest")
    scheduler.start()

    day_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    logger.info(
        "Bot gestartet! Digest wird jeden %s um %02d:%02d (%s) gesendet.",
        day_names[SCHEDULE_DAY],
        SCHEDULE_HOUR,
        SCHEDULE_MINUTE,
        TIMEZONE,
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
