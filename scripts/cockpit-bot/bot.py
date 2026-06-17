"""Cockpit-Bot — Patricia's Daily Operator (Telegram).

Schedule:
- Mo-Fr 06:30: Tagesbriefing + News (Push)
- Mo 08:00: Business-News-Digest (Push)
- Sa+So: kurzer Auszeit-Push 06:30 (Default: kein Push)

Telegram-Commands:
- /start    → Welcome
- /cockpit  → Tagesbriefing on-demand
- /cockpit-woche → Wochenblick on-demand
- /news     → Aktuelle News-Sektion on-demand
- /status   → Bot-Status
"""

import asyncio
import logging
import sys
from datetime import datetime, date, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

import config
import notion_reader
import notion_writer
import briefing_builder
import news_fetcher
import ads_fetcher
import posting_checker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


# Setup-Check
missing = config.validate_setup()
if missing:
    logger.error("Setup unvollstaendig: " + ", ".join(missing))
    sys.exit(1)
logger.info("Setup OK — Cockpit-Bot startet.")


# ========================================
# Helpers
# ========================================
def _is_authorized(update: Update) -> bool:
    if not update.effective_chat:
        return False
    return update.effective_chat.id == config.TELEGRAM_CHAT_ID


async def _build_kontext(heute: date = None) -> dict:
    """Sammelt Notion-Kontext für Briefing-Generator."""
    if heute is None:
        heute = date.today()

    kw = heute.isocalendar().week
    monatsplan = notion_reader.get_monatsplan(heute.month, heute.year)
    wochenplan = notion_reader.get_wochenplan_kw(kw, heute.year)
    offene_tasks = notion_reader.get_offene_tasks_heute(heute, limit=10)
    habit_goals = notion_reader.get_aktive_habit_goals()

    return {
        "monatsplan": monatsplan,
        "wochenplan": wochenplan,
        "offene_tasks": offene_tasks,
        "habit_goals": habit_goals,
        "kw": kw,
    }


async def _send_telegram(text: str):
    """Sendet Text an Patricia's Chat."""
    from telegram import Bot
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    try:
        # Telegram-Limit: 4096 Zeichen
        if len(text) > 4000:
            text = text[:4000] + "\n... (gekürzt)"
        await bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Telegram-Send-Fehler: {e}")


# ========================================
# Telegram-Commands
# ========================================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    await update.message.reply_text(
        "Hi Patricia! 👋\n\n"
        "Ich bin dein Cockpit-Bot — dein täglicher Tagesblick.\n\n"
        "Auto-Push:\n"
        "🌅 Mo-Fr 06:30 → Tagesbriefing + News\n"
        "📰 Mo 08:00 → Business-News-Digest\n"
        "🌿 Sa+So → kurze Auszeit-Erinnerung\n\n"
        "Manuelle Befehle:\n"
        "/cockpit — Tagesbriefing on-demand\n"
        "/cockpit-woche — Wochenblick\n"
        "/news — News-Sektion on-demand\n"
        "/status — Bot-Status"
    )


async def cmd_cockpit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    await update.message.reply_text("📋 Generiere Tagesbriefing ...")

    try:
        kontext = await _build_kontext()
        # News parallel - mache erst ohne News für Speed, optional mit News
        result = briefing_builder.generate_briefing("morgen", kontext)
        if not result.get("ok"):
            await update.message.reply_text(f"Fehler: {result.get('error')}")
            return
        await _send_telegram(result["text"])
    except Exception as e:
        logger.exception("cmd_cockpit failed")
        await update.message.reply_text(f"Crash: {e}")


async def cmd_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    await update.message.reply_text("📰 Suche aktuelle News ...")
    try:
        block = news_fetcher.fetch_news_block()
        await _send_telegram(block)
    except Exception as e:
        logger.exception("cmd_news failed")
        await update.message.reply_text(f"Crash: {e}")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    now = datetime.now(pytz.timezone(config.TIMEZONE))
    text = (
        f"🤖 Cockpit-Bot läuft\n"
        f"⏰ Lokal: {now.strftime('%a %d.%m. %H:%M')}\n"
        f"📅 Schedule:\n"
        f"   Mo-Fr 06:30 Tagesbriefing\n"
        f"   Mo 08:00 Business-News-Digest\n"
        f"🤖 Modell: {config.CLAUDE_MODEL}"
    )
    await update.message.reply_text(text)


# ========================================
# Scheduled Tasks
# ========================================
async def task_posting_check_abend():
    """Mo-Fr 19:00 — Posting-Check: heute live im Feed?"""
    if not config.TELEGRAM_CHAT_ID:
        logger.warning("Telegram-Chat-ID fehlt — Posting-Check übersprungen")
        return
    try:
        heute = date.today()
        if heute.weekday() >= 5:  # Sa/So → kein Check
            return
        msg = posting_checker.format_posting_check_message(heute)
        if not msg:
            logger.info(f"Posting-Check {heute}: keine geplanten Posts → kein Push")
            return
        await _send_telegram(msg)
        logger.info(f"Posting-Check {heute} an Patricia geschickt")
    except Exception:
        logger.exception("task_posting_check_abend crashed")


async def cmd_posting_ja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Patricia bestätigt: alle Posts heute live."""
    await update.message.reply_text(
        "✅ Super — Posting heute durch.\n"
        "Ich frag morgen 19:00 wieder."
    )


async def cmd_posting_nein(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Patricia: etwas fehlt. Sie schreibt dazu was."""
    args = " ".join(context.args).strip() if context.args else ""
    if args:
        msg = (
            f"⚠️ Verstanden — fehlt: *{args}*\n\n"
            "Schreib mir kurz welcher Slug genau, dann starte ich Catch-up.\n"
            "Oder lass es manuell + ich erinnere dich morgen wieder."
        )
    else:
        msg = (
            "⚠️ Verstanden — was genau fehlt?\n"
            "Antworte mit `/posting_nein <slug>` oder beschreib's kurz.\n"
            "Ich kann dann Catch-up direkt starten."
        )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def task_business_news_montag():
    """Mo 08:00 — Wochen-Business-News-Digest (KI + Onlinemarketing + Network Marketing + Mama-CEO)."""
    if not config.TELEGRAM_CHAT_ID:
        return
    logger.info("Business-News-Digest startet")
    try:
        from feeds_business import fetch_all_feeds
        from summarizer_business import curate_all

        articles = await asyncio.to_thread(fetch_all_feeds)
        total = sum(len(a) for a in articles.values())
        if total == 0:
            logger.info("Keine News-Artikel gefunden")
            return

        articles = await asyncio.to_thread(curate_all, articles)
        heute = date.today()
        woche_zurueck = heute - timedelta(days=7)
        date_range = f"{woche_zurueck.strftime('%d.%m.')} - {heute.strftime('%d.%m.%Y')}"

        msg = f"📰 *Business Wochen-News*\n📅 {date_range}\n\n"
        emojis = {
            "KI & AI": "🤖", "KI & Claude Code": "🤖",
            "Onlinemarketing": "📊", "Instagram Marketing": "📱",
            "Network Marketing": "🤝",
            "Mama-CEO & Zeitmanagement": "⏰",
            "Zeitmanagement & Mama-CEO-Struktur": "⏰",
            "Online-Business & Marketing": "💼",
        }
        for category, arts in articles.items():
            if not arts:
                continue
            emoji = emojis.get(category, "📌")
            msg += f"{emoji} *{category}*\n" + "━" * 15 + "\n"
            for i, a in enumerate(arts, 1):
                title = a["title"].replace("*", "").replace("_", "")
                summary = a.get("summary", "")
                msg += f"{i}. *{title}*\n{summary}\n🔗 [Link]({a['link']})\n\n"

        # Aufteilen in Chunks (Telegram 4000 Limit)
        max_len = 3800
        chunks = []
        remaining = msg
        while remaining:
            if len(remaining) <= max_len:
                chunks.append(remaining)
                break
            split_at = remaining.rfind("\n", 0, max_len)
            if split_at == -1:
                split_at = max_len
            chunks.append(remaining[:split_at])
            remaining = remaining[split_at:].lstrip("\n")

        for c in chunks:
            await _send_telegram(c)
        logger.info(f"Business-News-Digest gesendet ({len(chunks)} Chunks)")
    except Exception:
        logger.exception("Business-News-Digest-Fehler")


async def task_morgen_briefing():
    """Mo-Fr 06:30 — Tagesbriefing + News."""
    heute = date.today()
    if heute.weekday() not in config.WORKDAYS:
        # Sa+So: kurzer Auszeit-Push
        await _send_telegram(
            f"🌿 {['Mo','Di','Mi','Do','Fr','Sa','So'][heute.weekday()]} {heute.strftime('%d.%m.')}\n\n"
            "Heute AUSZEIT. Familie. Garten. Pause.\n\n"
            "→ Mo morgen 06:30 kommt das nächste Briefing.\n"
            "Lieb dich. 💛"
        )
        return

    logger.info(f"Morgen-Briefing startet für {heute}")
    try:
        kontext = await _build_kontext(heute)

        # News-Block NUR montags (sonst Token-Overload)
        ist_montag = heute.weekday() == 0
        if ist_montag:
            try:
                logger.info("Mo-Tag: lade ausführlichen Wochen-News-Bericht")
                news_block = news_fetcher.fetch_news_block(
                    monatsplan=kontext.get("monatsplan"),
                    wochenplan=kontext.get("wochenplan"),
                    max_zeichen=5000,
                )
                kontext["news_block"] = news_block
            except Exception as e:
                logger.warning(f"News-Fetcher fehlgeschlagen: {e}")
                kontext["news_block"] = "🎬 NEWS: heute kein Update verfügbar"
        else:
            # Di-Fr: kein News-Bericht, kompakter Brief
            kontext["news_block"] = ""

        # Ads-Block TÄGLICH (Mo-Fr) — wenn aktive Kampagnen laufen
        try:
            ads_kompakt = ads_fetcher.fetch_ads_block(modus="kompakt")
            ads_volltext = ads_fetcher.fetch_ads_block(modus="volltext")
            kontext["ads_block_kompakt"] = ads_kompakt
            kontext["ads_block_volltext"] = ads_volltext
            if ads_kompakt:
                logger.info(f"Ads-Block geladen ({len(ads_kompakt)} Zeichen kompakt)")
        except Exception as e:
            logger.warning(f"Ads-Fetcher fehlgeschlagen: {e}")
            kontext["ads_block_kompakt"] = ""
            kontext["ads_block_volltext"] = ""

        # 1) Notion-Volltext-Briefing generieren
        result_volltext = briefing_builder.generate_briefing("morgen_volltext", kontext, heute)
        if not result_volltext.get("ok"):
            logger.error(f"Volltext-Briefing-Fehler: {result_volltext.get('error')}")
            volltext = "Briefing-Generierung fehlgeschlagen — siehe Cockpit-Bot-Logs."
        else:
            volltext = result_volltext["text"]

        # 2) Notion-Page erstellen oder updaten
        notion_url = None
        try:
            tagesfokus = _extract_tagesfokus(volltext)
            notion_url = notion_writer.create_or_update_tagesplaner(
                heute, tagesfokus, volltext
            )
            logger.info(f"Notion-Tagesplaner-Page: {notion_url}")
        except Exception as e:
            logger.warning(f"Notion-Page-Erstellung fehlgeschlagen: {e}")

        # 3) Telegram-Kompakt-Briefing generieren
        result_kompakt = briefing_builder.generate_briefing("morgen_kompakt", kontext, heute)
        if not result_kompakt.get("ok"):
            await _send_telegram(f"⚠️ Briefing-Fehler: {result_kompakt.get('error')}")
            return

        text = result_kompakt["text"]
        if notion_url:
            text += f"\n\n📋 Voller Bericht mit Links:\n{notion_url}"

        await _send_telegram(text)
        total_tokens_in = result_volltext.get("tokens_in", 0) + result_kompakt.get("tokens_in", 0)
        total_tokens_out = result_volltext.get("tokens_out", 0) + result_kompakt.get("tokens_out", 0)
        logger.info(f"Tagesbriefing gesendet ({total_tokens_in}/{total_tokens_out} Tokens)")

    except Exception as e:
        logger.exception("task_morgen_briefing crashed")
        await _send_telegram(f"⚠️ Bot-Crash beim Morgen-Briefing: {e}")


def _extract_tagesfokus(volltext: str) -> str:
    """Extrahiert den Tagesfokus aus dem Volltext-Briefing.

    Sucht nach 'Hauptbrocken:' oder ähnlichem Pattern und gibt 1-Zeile zurück.
    """
    for line in volltext.split("\n"):
        if "**Hauptbrocken:**" in line or "Hauptbrocken:" in line:
            # Extract was nach „Hauptbrocken:" kommt
            parts = line.split(":", 1)
            if len(parts) > 1:
                fokus = parts[1].strip().strip("*").strip()
                return fokus[:200]
    # Fallback: erste H2-Sektion
    for line in volltext.split("\n"):
        if line.startswith("## ") and "Briefing" not in line:
            return line[3:].strip()[:200]
    return "Tagesplan"


# ========================================
# MAIN
# ========================================
async def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("cockpit", cmd_cockpit))
    app.add_handler(CommandHandler("news", cmd_news))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("posting_ja", cmd_posting_ja))
    app.add_handler(CommandHandler("posting_nein", cmd_posting_nein))

    # Scheduler
    tz = pytz.timezone(config.TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(
        task_morgen_briefing,
        CronTrigger(
            hour=config.MORNING_BRIEFING_TIME["hour"],
            minute=config.MORNING_BRIEFING_TIME["minute"],
            timezone=tz,
        ),
        id="morgen_briefing",
        name="Mo-Fr 06:30 Tagesbriefing",
    )
    # Mo 08:00 — Business-News-Digest (KI/Marketing/Mama-CEO)
    scheduler.add_job(
        task_business_news_montag,
        CronTrigger(day_of_week=0, hour=8, minute=0, timezone=tz),
        id="business_news_montag",
        name="Mo 08:00 Business-News-Digest",
    )
    # Mo-Fr 19:00 — Posting-Check (heute live?)
    scheduler.add_job(
        task_posting_check_abend,
        CronTrigger(day_of_week="mon-fri", hour=19, minute=0, timezone=tz),
        id="posting_check_abend",
        name="Mo-Fr 19:00 Posting-Check",
    )
    scheduler.start()
    logger.info(
        f"Scheduler aktiv: 06:30 Tagesbriefing + Mo 08:00 Business-News + Mo-Fr 19:00 Posting-Check {config.TIMEZONE}"
    )

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Telegram-Polling aktiv. Cockpit-Bot ist online.")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot wird beendet ...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        scheduler.shutdown()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
