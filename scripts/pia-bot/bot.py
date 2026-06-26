"""PIA — Patricias KI-Mentorin fürs 5-Tage-Bootcamp (Mehrbenutzer-Telegram-Bot).

Jede Teilnehmerin chattet privat mit PIA:
  /start  → Onboarding (6 Fragen, Text oder Sprachnotiz) → Profil
  danach  → Tages-Missionen abrufen:
            /bio /hooks /struktur /leadmagnet /roterfaden
  freier Text/Voice → PIA antwortet im Kontext ihres Profils

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

import config
import onboarding
import pia_brain
import store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pia")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

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


async def _send(update: Update, text: str):
    """Sendet Text — versucht HTML, fällt bei Parse-Fehler auf Klartext zurück.
    Lange Texte werden in Chunks gesplittet."""
    chunks = _split(text, TELEGRAM_MAX)
    for chunk in chunks:
        try:
            await update.message.reply_text(chunk, parse_mode="HTML",
                                            disable_web_page_preview=True)
        except Exception:
            # HTML-Parse fehlgeschlagen → ohne Formatierung
            try:
                await update.message.reply_text(chunk, disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Senden fehlgeschlagen: {e}")


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


def _firstname(update: Update) -> str:
    u = update.effective_user
    return (u.first_name if u and u.first_name else "").strip()


async def _typing(update: Update):
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except Exception:
        pass


# ========================================
# Commands
# ========================================
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    data = store.load_user(uid)

    if data and data.get("state") == "ready":
        await _send(update,
            f"Schön, dass du wieder da bist, {data['profil'].get('name','du')}! 💛\n\n"
            "Du bist startklar. Hol dir deine Mission:\n"
            "• /bio — Tag 1: dein Thema + deine Bio\n"
            "• /hooks — Tag 2: deine 3 Hooks\n"
            "• /struktur — Tag 3: deine Zeit-Struktur\n"
            "• /leadmagnet — Tag 4: dein Leadmagnet\n"
            "• /roterfaden — Tag 5: dein roter Faden\n\n"
            "Oder stell mir einfach eine Frage. /profil zeigt dein Profil, "
            "/neu startet von vorne.")
        return

    # Neu oder mitten im Onboarding → (neu) anlegen + erste/aktuelle Frage stellen
    if not data:
        data = store.create_user(uid, name=_firstname(update))
    frage = onboarding.frage_fuer_schritt(data.get("onboarding_step", 0))
    if frage:
        await _send(update, frage["frage"])
    else:
        store.mark_ready(uid)
        await _send(update, "Du bist schon fertig eingerichtet — tippe /bio für Tag 1. 💛")


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
        "<b>So funktioniere ich 💛</b>\n\n"
        "Ich bin PIA, deine KI-Mentorin fürs Bootcamp. In den 5 Tagen baust du mit mir "
        "Schritt für Schritt dein Fundament.\n\n"
        "<b>Deine Missionen:</b>\n"
        "• /bio — Tag 1: dein Thema + deine Bio\n"
        "• /hooks — Tag 2: deine 3 Hooks\n"
        "• /struktur — Tag 3: deine Zeit-Struktur\n"
        "• /leadmagnet — Tag 4: dein Leadmagnet\n"
        "• /roterfaden — Tag 5: dein roter Faden\n\n"
        "• /profil — was ich über dich weiss\n"
        "• /neu — von vorne starten\n\n"
        "Du kannst mir auch einfach schreiben oder eine Sprachnotiz schicken.")


async def _run_task(update: Update, task_key: str):
    uid = update.effective_chat.id
    data = store.load_user(uid)
    if not data or data.get("state") != "ready":
        await _send(update,
            "Lass uns zuerst dein Profil fertig machen, dann kann ich dir was Persönliches "
            "bauen. 💛 Tippe /start.")
        return
    await _typing(update)
    label = pia_brain.TASKS.get(task_key, {}).get("label", task_key)
    await _send(update, f"Einen Moment — ich bau dir <b>{label}</b> … ✍️")
    result = pia_brain.generate(task_key, data.get("profil", {}))
    if not result.get("ok"):
        await _send(update, "Ups, da ist gerade was schiefgelaufen. Probier's gleich nochmal — "
                            "und wenn's bleibt, sag Patricia kurz Bescheid. 💛")
        logger.error(f"Task {task_key} für {uid} fehlgeschlagen: {result.get('error')}")
        return
    store.store_output(uid, task_key, result["text"])
    await _send(update, result["text"])


async def cmd_bio(update, context):        await _run_task(update, "bio")
async def cmd_hooks(update, context):      await _run_task(update, "hooks")
async def cmd_struktur(update, context):   await _run_task(update, "struktur")
async def cmd_leadmagnet(update, context): await _run_task(update, "leadmagnet")
async def cmd_roterfaden(update, context): await _run_task(update, "roterfaden")


async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nur Patricia: kleine Statistik."""
    uid = update.effective_chat.id
    if not config.ADMIN_CHAT_ID or uid != config.ADMIN_CHAT_ID:
        return
    users = store.all_users()
    ready = sum(1 for u in users if u.get("state") == "ready")
    onb = len(users) - ready
    await _send(update,
        f"<b>PIA-Statistik</b>\n"
        f"Teilnehmerinnen gesamt: {len(users)}\n"
        f"Profil fertig: {ready}\n"
        f"Mitten im Onboarding: {onb}")


# ========================================
# Onboarding-Fortschritt aus einer Antwort
# ========================================
async def _handle_antwort(update: Update, antwort_text: str):
    uid = update.effective_chat.id
    data = store.get_or_create(uid, name=_firstname(update))

    # Im Onboarding? → Antwort speichern + nächste Frage
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
            # Fertig!
            store.mark_ready(uid)
            data = store.load_user(uid)
            name = data["profil"].get("name", "du")
            await _send(update,
                f"Perfekt, {name} — ich hab alles, was ich brauche. 💛\n\n"
                + onboarding.profil_zusammenfassung(data["profil"])
                + "\n\n<b>Du bist startklar!</b> Sobald das Bootcamp läuft, gehen wir Tag für "
                "Tag durch. Du kannst jederzeit loslegen:\n"
                "• /bio — dein Thema + deine Bio (Tag 1)\n\n"
                f"Wir sehen uns auch in der Gruppe: {config.BOOTCAMP_GRUPPE_LINK}\n"
                f"Start: {config.BOOTCAMP_START}. Ich freu mich auf dich!")
            return

    # Fertig eingerichtet → freie Frage an PIA
    await _typing(update)
    result = pia_brain.freie_frage(data.get("profil", {}), antwort_text.strip())
    if result.get("ok"):
        await _send(update, result["text"])
    else:
        await _send(update,
            "Das hab ich gerade nicht verstanden — magst du's nochmal anders sagen? "
            "Oder hol dir eine Mission mit /bio, /hooks, /struktur, /leadmagnet, /roterfaden. 💛")


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
# MAIN
# ========================================
async def main():
    missing = config.validate_setup()
    if missing:
        logger.error("Setup unvollstaendig — Bot startet nicht:")
        for m in missing:
            logger.error(f"   - fehlt: {m}")
        sys.exit(1)

    app = Application.builder().token(config.PIA_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("neu", cmd_neu))
    app.add_handler(CommandHandler("profil", cmd_profil))
    app.add_handler(CommandHandler("hilfe", cmd_hilfe))
    app.add_handler(CommandHandler("help", cmd_hilfe))
    app.add_handler(CommandHandler("bio", cmd_bio))
    app.add_handler(CommandHandler("hooks", cmd_hooks))
    app.add_handler(CommandHandler("struktur", cmd_struktur))
    app.add_handler(CommandHandler("leadmagnet", cmd_leadmagnet))
    app.add_handler(CommandHandler("roterfaden", cmd_roterfaden))
    app.add_handler(CommandHandler("admin", cmd_admin))

    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("PIA ist online. (Ctrl-C zum Beenden)")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("PIA wird beendet …")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
