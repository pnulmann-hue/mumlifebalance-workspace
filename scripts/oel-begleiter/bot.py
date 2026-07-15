"""Öl-Sample-Begleiter — Patricias Mehrbenutzer-Telegram-Bot fürs Öle-Testen.

Jede Testerin chattet privat mit dem Bot:
  /start  → Onboarding (5 Fragen, Text oder Sprachnotiz) → Profil → Tag 1 sofort
  danach  → jeden Morgen automatisch die nächste Etappe (Tag 2..7)
            /heute   → heutige Etappe nochmal / abrufen
            /weiter  → nächste Etappe vorziehen (für Ungeduldige)
  freier Text/Voice → der Begleiter antwortet im Kontext ihres Profils + ihrer Öle

Das Öl-Wissen kommt aus dem Companion (Supabase category=product) — genau das, worauf
Patricias Kundinnen Zugriff haben. Siehe companion_kb.py.

Lokal testen:
    python config.py   # Setup-Check
    python bot.py      # startet Bot (Ctrl-C beendet)

Deploy: Railway (siehe README.md / Procfile).
"""

from __future__ import annotations

import asyncio
import logging
import sys
import tempfile
from datetime import time as dt_time
from pathlib import Path

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import begleiter_brain
import config
import onboarding
import store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("oel-begleiter")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

# Whisper optional laden
try:
    import transcribe  # type: ignore
    _HAS_TRANSCRIBE = True
except Exception:
    _HAS_TRANSCRIBE = False


# ========================================
# Hilfen
# ========================================
TELEGRAM_MAX = 4000  # Sicherheitsmarge unter 4096


def _split(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    out, rest = [], text
    while len(rest) > size:
        cut = rest.rfind("\n", 0, size)
        if cut < size // 2:
            cut = size
        out.append(rest[:cut])
        rest = rest[cut:].lstrip("\n")
    if rest:
        out.append(rest)
    return out


async def _send_raw(bot, chat_id: int, text: str):
    """Sendet Text an eine Chat-ID — HTML mit Klartext-Fallback, gechunkt."""
    for chunk in _split(text, TELEGRAM_MAX):
        try:
            await bot.send_message(chat_id, chunk, parse_mode="HTML",
                                   disable_web_page_preview=True)
        except Exception:
            try:
                await bot.send_message(chat_id, chunk, disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Senden an {chat_id} fehlgeschlagen: {e}")


async def _send(update: Update, text: str):
    await _send_raw(update.get_bot(), update.effective_chat.id, text)


def _firstname(update: Update) -> str:
    u = update.effective_user
    return (u.first_name if u and u.first_name else "").strip()


async def _typing(update: Update):
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except Exception:
        pass


# ========================================
# Auslieferung einer Etappe
# ========================================
async def _liefere_etappe(bot, data: dict, day_num: int) -> bool:
    """Generiert + sendet die Etappe day_num an die Testerin. True bei Erfolg."""
    uid = data["user_id"]
    profil = data.get("profil", {})
    result = await asyncio.to_thread(begleiter_brain.generate_day, day_num, profil)
    if not result.get("ok"):
        logger.error(f"Etappe {day_num} für {uid} fehlgeschlagen: {result.get('error')}")
        return False
    store.store_day(uid, day_num, result["text"])
    await _send_raw(bot, uid, result["text"])
    return True


# ========================================
# Commands
# ========================================
def _mission_hinweis() -> str:
    return ("Jeden Morgen kommt automatisch deine nächste Etappe. 🌿\n"
            "• /heute — deine heutige Etappe nochmal\n"
            "• /weiter — die nächste Etappe schon jetzt\n"
            "• /profil — was ich über dich weiss · /neu — von vorne")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    data = store.load_user(uid)

    if data and data.get("state") == "ready":
        name = data["profil"].get("name", "du")
        await _send(update,
            f"Schön, dass du wieder da bist, {name}! 💛\n\n" + _mission_hinweis())
        return

    if not data:
        data = store.create_user(uid, name=_firstname(update))
    frage = onboarding.frage_fuer_schritt(data.get("onboarding_step", 0))
    if frage:
        await _send(update, frage["frage"])
    else:
        # Onboarding-Schritt out of range → sauber abschliessen
        await _finish_onboarding(update, uid)


async def cmd_neu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    store.reset_user(uid, name=_firstname(update))
    await _send(update, "Alles auf Anfang. 🌱 Lass uns nochmal starten.\n\n"
                + onboarding.FRAGEN[0]["frage"])


async def cmd_profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    data = store.load_user(uid)
    if not data:
        await _send(update, "Ich kenn dich noch nicht — tippe /start, dann lern ich dich kennen. 💛")
        return
    await _send(update,
        "<b>Das hab ich über dich:</b>\n\n"
        + onboarding.profil_zusammenfassung(data.get("profil", {}))
        + "\n\nStimmt was nicht? /neu startet von vorne.")


async def cmd_hilfe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send(update,
        "<b>So funktioniere ich 🌿</b>\n\n"
        "Ich bin dein Öl-Begleiter. In 7 Tagen entdecken wir zusammen deine Pröbchen — "
        "jeden Morgen eine kleine, machbare Etappe.\n\n"
        + _mission_hinweis()
        + "\n\nDu kannst mir auch einfach schreiben oder eine Sprachnotiz schicken, wenn "
        "du eine Frage zu deinen Ölen hast. 💛")


async def cmd_heute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Heutige Etappe: die letzte gesendete nochmal, oder die nächste fällige."""
    uid = update.effective_chat.id
    data = store.load_user(uid)
    if not data or data.get("state") != "ready":
        await _send(update, "Lass uns zuerst dein Profil fertig machen — tippe /start. 💛")
        return

    geliefert = data.get("delivered_day", 0)
    # Wenn heute noch nichts kam und eine Etappe fällig ist → jetzt liefern.
    if not store.schon_heute_geliefert(data) and store.naechste_etappe(data) \
            and store.faellige_etappe(data) > geliefert:
        await _typing(update)
        naechster = store.naechste_etappe(data)
        if await _liefere_etappe(update.get_bot(), data, naechster):
            return
    # Sonst: letzte Etappe nochmal zeigen.
    if geliefert >= 1:
        letzte = data.get("outputs", {}).get(f"tag{geliefert}", {}).get("text")
        if letzte:
            await _send(update, "Hier nochmal deine aktuelle Etappe 🌿\n\n" + letzte)
            return
    await _send(update, "Deine erste Etappe ist unterwegs — magst du /weiter tippen, "
                        "dann leg ich los? 💛")


async def cmd_weiter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nächste Etappe vorziehen (unabhängig vom Kalender)."""
    uid = update.effective_chat.id
    data = store.load_user(uid)
    if not data or data.get("state") != "ready":
        await _send(update, "Lass uns zuerst dein Profil fertig machen — tippe /start. 💛")
        return
    naechster = store.naechste_etappe(data)
    if not naechster:
        await _send(update,
            "Du hast schon alle 7 Etappen durch — wie schön, dass du dabei geblieben bist! 💛\n"
            "Wenn du magst, tippe /heute für deine Mini-Routine nochmal.")
        return
    await _typing(update)
    if not await _liefere_etappe(update.get_bot(), data, naechster):
        await _send(update, "Ups, da ist gerade was schiefgelaufen — probier's gleich nochmal. 💛")


async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nur Patricia: kleine Statistik."""
    uid = update.effective_chat.id
    if not config.ADMIN_CHAT_ID or uid != config.ADMIN_CHAT_ID:
        return
    users = store.all_users()
    ready = [u for u in users if u.get("state") == "ready"]
    onb = len(users) - len(ready)
    durch = sum(1 for u in ready if u.get("delivered_day", 0) >= store.GESAMT_TAGE)
    await _send(update,
        f"<b>Öl-Begleiter-Statistik</b>\n"
        f"Testerinnen gesamt: {len(users)}\n"
        f"Profil fertig: {len(ready)}\n"
        f"Mitten im Onboarding: {onb}\n"
        f"Alle 7 Tage durch: {durch}")


# ========================================
# Onboarding-Fortschritt + freie Fragen
# ========================================
async def _finish_onboarding(update: Update, uid: int):
    store.mark_ready(uid)
    data = store.load_user(uid)
    name = data["profil"].get("name", "du")
    await _send(update,
        f"Perfekt, {name} — ich hab alles, was ich brauche. 💛\n\n"
        + onboarding.profil_zusammenfassung(data["profil"])
        + "\n\n<b>Und jetzt geht's los — hier ist deine erste Etappe:</b> 🌿")
    # Tag 1 sofort ausliefern
    ok = await _liefere_etappe(update.get_bot(), data, 1)
    if ok:
        await _send(update,
            "\nAb morgen früh schick ich dir automatisch die nächste Etappe. "
            "Wenn du nicht warten magst, tippe einfach /weiter. 💛")
    else:
        await _send(update, "Deine erste Etappe kommt gleich — tippe kurz /heute. 💛")


async def _handle_antwort(update: Update, antwort_text: str):
    uid = update.effective_chat.id
    data = store.get_or_create(uid, name=_firstname(update))

    if data.get("state") == "onboarding":
        step = data.get("onboarding_step", 0)
        frage = onboarding.frage_fuer_schritt(step)
        if frage:
            store.set_answer(uid, frage["key"], antwort_text.strip())
            data = store.advance_onboarding(uid)
            naechste = onboarding.frage_fuer_schritt(data["onboarding_step"])
            if naechste:
                await _send(update, naechste["frage"])
                return
            await _finish_onboarding(update, uid)
            return

    # Fertig eingerichtet → freie Frage an den Begleiter
    await _typing(update)
    result = await asyncio.to_thread(
        begleiter_brain.freie_frage, data.get("profil", {}), antwort_text.strip()
    )
    if result.get("ok"):
        await _send(update, result["text"])
    else:
        await _send(update,
            "Das hab ich gerade nicht ganz verstanden — magst du's nochmal anders sagen? "
            "Oder tippe /heute für deine Etappe. 💛")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return
    await _handle_antwort(update, msg.text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    voice = msg.voice or msg.audio
    if not voice:
        return
    if not (_HAS_TRANSCRIBE and transcribe.is_available()):
        await _send(update, "Sprachnotizen kann ich gerade nicht verarbeiten — "
                            "schreib mir bitte kurz als Text. 💛")
        return
    await _typing(update)
    try:
        tg_file = await voice.get_file()
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        await tg_file.download_to_drive(custom_path=str(tmp_path))
        text = transcribe.transkribiere_telegram_voice(tmp_path)
        try:
            tmp_path.unlink()
        except Exception:
            pass
    except Exception as e:
        logger.error(f"Voice-Fehler: {e}")
        await _send(update, "Beim Anhören ist was schiefgelaufen — schreib's mir bitte als Text. 💛")
        return
    if not text:
        await _send(update, "Ich hab leider nichts verstanden — magst du's nochmal sagen oder tippen?")
        return
    await _handle_antwort(update, text)


# ========================================
# Täglicher Push (JobQueue)
# ========================================
async def daily_push(context: ContextTypes.DEFAULT_TYPE):
    """Läuft 1×/Tag: schickt jeder Testerin ihre nächste fällige Etappe (max 1/Tag)."""
    bot = context.bot
    users = store.all_users()
    gesendet = 0
    for data in users:
        if data.get("state") != "ready":
            continue
        if store.schon_heute_geliefert(data):
            continue  # heute hat sie schon eine (Auto oder manuell) bekommen
        naechster = store.naechste_etappe(data)
        if not naechster:
            continue  # alle 7 durch
        if store.faellige_etappe(data) < naechster:
            continue  # nach Kalender noch nicht dran
        try:
            if await _liefere_etappe(bot, data, naechster):
                gesendet += 1
                await asyncio.sleep(0.5)  # sanftes Rate-Limiting
        except Exception as e:
            logger.error(f"Push an {data.get('user_id')} fehlgeschlagen: {e}")
    if gesendet:
        logger.info(f"Tages-Push: {gesendet} Etappen verschickt.")


# ========================================
# MAIN
# ========================================
async def main():
    missing = config.validate_setup()
    if missing:
        logger.error("Setup unvollstaendig — Bot startet nicht:")
        for m in missing:
            logger.error(f"   - fehlt: {m}")
        sys.exit(1)

    app = Application.builder().token(config.OEL_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("neu", cmd_neu))
    app.add_handler(CommandHandler("profil", cmd_profil))
    app.add_handler(CommandHandler("hilfe", cmd_hilfe))
    app.add_handler(CommandHandler("help", cmd_hilfe))
    app.add_handler(CommandHandler("heute", cmd_heute))
    app.add_handler(CommandHandler("weiter", cmd_weiter))
    app.add_handler(CommandHandler("admin", cmd_admin))

    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Täglicher Push zur eingestellten Stunde (Europe/Zurich).
    if app.job_queue is not None:
        try:
            import pytz
            tz = pytz.timezone(config.TIMEZONE)
        except Exception:
            tz = None
        app.job_queue.run_daily(
            daily_push,
            time=dt_time(hour=config.SEND_HOUR, minute=0, tzinfo=tz),
            name="oel-daily-push",
        )
        logger.info(f"Tages-Push geplant für {config.SEND_HOUR:02d}:00 {config.TIMEZONE}.")
    else:
        logger.warning("JobQueue nicht verfügbar — kein Auto-Push. "
                       "Installiere python-telegram-bot[job-queue]. "
                       "Testerinnen können weiter mit /weiter selbst abrufen.")

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("Öl-Begleiter ist online. (Ctrl-C zum Beenden)")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Öl-Begleiter wird beendet …")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
