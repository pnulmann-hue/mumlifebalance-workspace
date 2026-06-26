"""Patricia's Story-Render-Bot — Haupt-Einstiegspunkt für Railway.

Architektur:
  - APScheduler triggert daily-story-render Mo-So 06:30 (Europe/Zurich)
  - Bot wartet zwischen Triggern auf Patricia-Replies (Telegram)
  - Bei Trigger: ruft task_daily_story.run() auf
  - Patricia interagiert via Sprachnotiz oder Text — Bot transkribiert + verarbeitet

Lokal testen:
    python config.py    # Setup-Check
    python bot.py       # startet Bot (Ctrl-C zum Beenden)

Railway-Deploy:
    siehe deploy_to_railway.py
"""

import asyncio
import logging
import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import config
import state
import task_daily_story
import transcribe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Reduziere Telegram/HTTPX Spam
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)


# ========================================
# Railway-Setup: Bundle → context/ entpacken (falls Bundle existiert + context fehlt)
# ========================================
def _setup_bundle_if_needed():
    """Auf Railway: kopiert _bundle/* nach context/* damit HTML-Pfade funktionieren.

    Lokal (Patricia-PC): context/ ist da mit allen 1007 Shootingbildern → nichts tun.
    Railway: context/ ist gitignored → Bundle wird zu context/ kopiert.
    """
    bundle = Path(__file__).resolve().parent / "_bundle"
    if not bundle.exists():
        return  # kein Bundle = lokaler Mode

    # Workspace-Root vom Bundle aus: scripts/content-assistent/_bundle → 3x .parent
    workspace = bundle.parent.parent.parent
    context_dir = workspace / "context"

    # Brauchen wir Setup? Wenn context/Shootingbilder schon Inhalt hat, skip.
    sb = context_dir / "Shootingbilder"
    if sb.exists() and any(sb.iterdir()):
        return

    print("[BUNDLE-SETUP] context/ ist leer — entpacke _bundle/ nach context/")
    context_dir.mkdir(parents=True, exist_ok=True)

    # 1. Photo-Ordner symlinken (oder kopieren falls Symlink fehlschlägt)
    for sub in ["Shootingbilder", "stock-fotos", "doTERRA"]:
        src = bundle / sub
        dst = context_dir / sub
        if not src.exists() or dst.exists():
            continue
        try:
            os.symlink(src, dst, target_is_directory=True)
            print(f"[BUNDLE-SETUP]   symlink {sub}")
        except (OSError, NotImplementedError):
            shutil.copytree(src, dst)
            print(f"[BUNDLE-SETUP]   copytree {sub}")

    # 2. Context-Markdown-Dateien kopieren
    ctx_md = bundle / "context"
    if ctx_md.exists():
        copied = 0
        for f in ctx_md.rglob("*"):
            if f.is_file():
                rel = f.relative_to(ctx_md)
                dst = context_dir / rel
                if not dst.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dst)
                    copied += 1
        print(f"[BUNDLE-SETUP]   {copied} context-Dateien kopiert")

    print("[BUNDLE-SETUP] Fertig.")


# Beim Start ausführen — VOR config-validate, damit RENDER_SCRIPT etc. existiert
_setup_bundle_if_needed()


# ========================================
# Render-Pipeline einrichten (npm install puppeteer)
# ========================================
def _setup_render_pipeline_if_needed():
    """Auf Railway: stellt sicher dass node_modules/puppeteer existiert."""
    bundle_render = Path(__file__).resolve().parent / "render"
    if not bundle_render.exists():
        return  # Bundle nicht aktiv → workspace karussell-render wird genutzt
    nm = bundle_render / "node_modules"
    if nm.exists() and (nm / "puppeteer").exists():
        return  # schon installiert
    print("[RENDER-SETUP] npm install in render/ ...")
    try:
        import subprocess
        subprocess.run(["npm", "install", "--no-audit", "--no-fund"],
                      cwd=bundle_render, check=True, timeout=180)
        print("[RENDER-SETUP] npm install fertig.")
    except Exception as e:
        print(f"[RENDER-SETUP] npm install Fehler: {e}")


_setup_render_pipeline_if_needed()


# ========================================
# Setup-Check beim Start
# ========================================
missing = config.validate_setup()
if missing:
    logger.error("Setup unvollstaendig — Bot startet nicht.")
    for m in missing:
        logger.error(f"   - fehlt: {m}")
    logger.error("Setze Environment-Variablen oder editiere .env, dann neu starten.")
    sys.exit(1)

logger.info("Setup OK — Bot startet.")


# ========================================
# Telegram-Handler
# ========================================
def _is_authorized(update: Update) -> bool:
    """Nur Patricia darf den Bot benutzen."""
    if not update.effective_chat:
        return False
    return update.effective_chat.id == config.TELEGRAM_CHAT_ID


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    await update.message.reply_text(
        "Hi Patricia! Ich bin dein Story-Ideen-Bot.\n\n"
        "🎬 <b>Täglicher Ablauf (Story-Idee):</b>\n"
        "1. Mo-So 06:30 schicke ich dir den <b>Plan des Tages</b> + frage, was bei dir los ist.\n"
        "2. Du schickst mir <b>1 Sprachnotiz</b> zu deinem Tag.\n"
        "3. Ich verweb deinen Tag mit dem Plan zu einer <b>fertigen Story-Idee</b> "
        "(Hook + Slide-für-Slide-Konzept + CTA) — die Slides baust du selbst.\n"
        "4. Optional: <b>/render</b> → ich render dir die Slides als PNG.\n\n"
        "Commands:\n"
        "/idee — Story-Idee für heute jetzt bauen (mit/ohne deinen Input)\n"
        "/idee mentoring · /idee doterra — mit Profil\n"
        "/render — letzte Idee zu PNG-Slides rendern\n"
        "/fokus &lt;thema&gt; — Wochenfokus setzen, z.B. <code>/fokus bio-check</code>\n"
        "/fokus reset — Override löschen, wieder Notion/Plan nutzen\n"
        "/status — Bot-Status\n"
        "/notion — Notion-Healthcheck\n\n"
        "<i>Alter Render-Workflow bleibt: /run (Sparring) · /run schnell · /generieren</i>",
        parse_mode="HTML",
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    now = datetime.now(pytz.timezone(config.TIMEZONE))
    kw = now.isocalendar().week

    fokus_override = state.get_wochen_fokus_override(kw)
    fokus_info = "—"
    if fokus_override:
        fokus_info = f"<b>{fokus_override['thema']}</b> (Override)"

    briefing = state.get_briefing_pending()
    briefing_info = "—"
    if briefing:
        n_antworten = len(briefing.get("patricia_antworten", []))
        n_fotos = len(briefing.get("patricia_fotos", []))
        briefing_info = f"offen ({briefing['profil']}, {n_antworten} Antworten, {n_fotos} Fotos)"

    text = (
        f"<b>Bot laeuft</b>\n"
        f"Lokal: {now.strftime('%a %d.%m. %H:%M')} (KW {kw})\n"
        f"Naechster Auto-Lauf: Mo-So 06:30\n"
        f"Modell: <code>{config.CLAUDE_MODEL}</code>\n"
        f"DISG heute: <b>{state.empfehle_disg_heute()}</b>\n"
        f"Diese Woche DISG: {sorted(state.disg_diese_woche()) or '—'}\n"
        f"Wochenfokus: {fokus_info}\n"
        f"Offenes Briefing: {briefing_info}\n"
        f"Whisper: {'OK' if transcribe.is_available() else 'AUS'}"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def cmd_fokus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Setzt einen Wochenfokus-Override."""
    if not _is_authorized(update):
        return
    args = context.args or []
    if not args:
        # Status anzeigen
        kw = datetime.now().isocalendar().week
        f = state.get_wochen_fokus_override(kw)
        if f:
            await update.message.reply_text(
                f"<b>Aktueller Fokus-Override (KW {kw}):</b>\n"
                f"Thema: <b>{f['thema']}</b>\n"
                f"Funnel-ID: {f.get('funnel_id') or '—'}\n"
                f"Produkt: {f.get('produkt') or '—'}\n\n"
                f"Loeschen mit /fokus reset",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text(
                "Kein Fokus-Override aktiv (Bot nutzt Notion-Wochenplan).\n\n"
                "Setzen mit: <code>/fokus bio-check</code>\n"
                "Oder: <code>/fokus thema-finden</code>\n"
                "Oder: <code>/fokus instagram-kundenmaschine</code>",
                parse_mode="HTML",
            )
        return

    if args[0].lower() == "reset":
        state.clear_wochen_fokus_override()
        await update.message.reply_text("Fokus-Override gelöscht. Bot nutzt wieder Notion-Wochenplan.")
        return

    # Bekannte Funnel-IDs erkennen
    eingabe = " ".join(args).strip()
    funnel_id = None
    funnel_aliase = {
        "bio-check": "bio-check", "biocheck": "bio-check", "bio": "bio-check",
        "thema-finden": "thema-finden", "thema": "thema-finden",
        "expertin": "expertin",
        "instagram-kundenmaschine": "instagram-kundenmaschine", "ikm": "instagram-kundenmaschine",
        "lead-challenge": "lead-challenge",
        "workbook": "workbook-von-0-auf-echt", "von-0-auf-echt": "workbook-von-0-auf-echt",
        "potenzial": "0e-potenzial-test", "potenzialtest": "0e-potenzial-test",
        "starterguide": "0e-starterguide",
        "story-challenge": "story-challenge",
        "energie-kur": "doterra-energie-kur", "energie": "doterra-energie-kur",
    }
    for alias, fid in funnel_aliase.items():
        if alias in eingabe.lower():
            funnel_id = fid
            break

    data = state.set_wochen_fokus_override(thema=eingabe, funnel_id=funnel_id)
    await update.message.reply_text(
        f"<b>Fokus-Override gesetzt fuer KW {data['kw']}:</b>\n"
        f"Thema: <b>{data['thema']}</b>\n"
        f"Funnel-ID: {data.get('funnel_id') or '—'}\n\n"
        f"Bot nutzt das ab jetzt fuer alle Story-Generierungen diese Woche.\n"
        f"Override loeschen mit: /fokus reset",
        parse_mode="HTML",
    )


async def cmd_notion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Notion-Healthcheck."""
    if not _is_authorized(update):
        return
    import notion_reader
    await update.message.reply_text("Pruefe Notion-Zugang ...")
    try:
        hc = notion_reader.healthcheck()
    except Exception as e:
        await update.message.reply_text(f"Fehler: {e}")
        return

    lines = ["<b>Notion-Healthcheck</b>"]
    lines.append(f"Gesamt: {'OK' if hc['ok'] else 'FEHLER'}")
    for name, info in hc["details"].items():
        ok = info.get("ok", False)
        lines.append(f"  {'OK' if ok else 'FEHLER'} — {name}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def cmd_run_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manueller Trigger.

    /run                        → Sparring-Modus (Briefing-Frage zuerst)
    /run mentoring              → Sparring-Modus mit Profil
    /run schnell                → Direkt generieren (alter Modus, ohne Sparring)
    /run schnell mentoring      → Direkt + Profil
    """
    if not _is_authorized(update):
        return

    args = [a.lower() for a in (context.args or [])]
    schnell_modus = "schnell" in args
    profil_override = None
    for a in args:
        if a in {"mentoring", "doterra", "beide"}:
            profil_override = a
            break

    try:
        if schnell_modus:
            await update.message.reply_text(
                "⚡ Schnell-Modus — generiere ohne Sparring-Fragen "
                "(Risiko: Bot erfindet Details wenn Notion zu wenig hergibt)."
            )
            result = await task_daily_story.run(
                modus="schnell",
                profil_override=profil_override,
            )
        else:
            await update.message.reply_text("🤝 Starte Sparring-Briefing ...")
            result = await task_daily_story.briefing_anfragen(
                profil_override=profil_override,
            )
        if not result.get("ok"):
            await update.message.reply_text(
                f"Fehler: {result.get('error', 'unbekannt')}"
            )
    except Exception as e:
        logger.exception("cmd_run_now failed")
        await update.message.reply_text(f"Crash: {e}")


async def cmd_generieren(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generiert Story aus offenem Sparring-Briefing."""
    if not _is_authorized(update):
        return
    await update.message.reply_text("🎨 Baue Story aus deinen Briefing-Antworten ...")
    try:
        result = await task_daily_story.generiere_story_aus_briefing()
        if not result.get("ok"):
            err = result.get("error", "unbekannt")
            if err == "no_pending_briefing":
                await update.message.reply_text(
                    "Kein offenes Briefing — tippe /run um eines zu starten."
                )
            elif err == "no_patricia_input":
                pass  # Message wurde schon gesendet
            else:
                await update.message.reply_text(f"Fehler: {err}")
    except Exception as e:
        logger.exception("cmd_generieren failed")
        await update.message.reply_text(f"Crash: {e}")


async def cmd_idee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generiert die Story-Idee jetzt — aus gesammeltem Input oder nur aus dem Plan.

    /idee            → Story-Idee fuer heute (nutzt Tages-Input falls vorhanden)
    /idee mentoring  → mit Profil
    """
    if not _is_authorized(update):
        return
    args = [a.lower() for a in (context.args or [])]
    profil_override = next((a for a in args if a in {"mentoring", "doterra", "beide"}), None)
    await update.message.reply_text("✍️ Bau dir die Story-Idee fuer heute …")
    try:
        result = await task_daily_story.generiere_idee_aus_input(profil_override=profil_override)
        if not result.get("ok"):
            await update.message.reply_text(f"Fehler: {result.get('error', 'unbekannt')}")
    except Exception as e:
        logger.exception("cmd_idee failed")
        await update.message.reply_text(f"Crash: {e}")


async def cmd_render(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Rendert die zuletzt gelieferte Story-Idee zu PNG-Slides."""
    if not _is_authorized(update):
        return
    try:
        result = await task_daily_story.render_aus_letzter_idee()
        if not result.get("ok") and result.get("error") not in {"keine_idee"}:
            await update.message.reply_text(f"Fehler: {result.get('error', 'unbekannt')}")
    except Exception as e:
        logger.exception("cmd_render failed")
        await update.message.reply_text(f"Crash: {e}")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sprachnotiz-Handler — transkribieren und in offenes Briefing einsammeln."""
    if not _is_authorized(update):
        return

    msg = update.message
    voice = msg.voice or msg.audio
    if not voice:
        return

    if not transcribe.is_available():
        await msg.reply_text("Whisper nicht verfuegbar (kein OPENAI_API_KEY).")
        return

    await msg.reply_text("🎙️ Transkribiere Sprachnotiz ...")

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
        logger.exception("Voice-Download fehlgeschlagen")
        await msg.reply_text(f"Voice-Download-Fehler: {e}")
        return

    if not text:
        await msg.reply_text("Konnte nichts transkribieren — leer zurueck.")
        return

    # In offenes Briefing einsammeln
    briefing = state.get_briefing_pending()
    if briefing:
        state.add_patricia_antwort(text=text)
        # IDEE-Modus: erste Antwort loest direkt die Story-Idee aus (kein /generieren)
        if briefing.get("modus") == "idee":
            await msg.reply_text(
                f"<b>📝 Hab deinen Tag:</b>\n<i>{text[:400]}</i>",
                parse_mode="HTML",
            )
            try:
                await task_daily_story.generiere_idee_aus_input()
            except Exception as e:
                logger.exception("generiere_idee_aus_input failed")
                await msg.reply_text(f"Crash bei Idee-Generierung: {e}")
            return
        n = len(state.get_briefing_pending().get("patricia_antworten", []))
        await msg.reply_text(
            f"<b>📝 Transkript ({n}. Antwort):</b>\n<i>{text[:500]}</i>\n\n"
            f"Weitere Voice-Notizen / Fotos schicken oder /generieren tippen.",
            parse_mode="HTML",
        )
    else:
        # Kein offenes Briefing — speichere als Standalone Session-Input
        sess = state.get_active_session() or state.set_active_session(profil="auto", kontext={})
        state.update_session(input_text=text)
        await msg.reply_text(
            f"<b>📝 Transkript:</b>\n<i>{text[:500]}</i>\n\n"
            f"Kein offenes Briefing — tippe /run um eines zu starten, "
            f"oder /run schnell um direkt eine Story damit zu bauen.",
            parse_mode="HTML",
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foto-Handler — speichert Foto fuer offenes Briefing."""
    if not _is_authorized(update):
        return
    msg = update.message
    if not msg.photo:
        return

    photo = msg.photo[-1]
    foto_dir = config.OUTPUTS_STORIES_DIR / "_uploads"
    foto_dir.mkdir(parents=True, exist_ok=True)
    foto_path = foto_dir / f"patricia-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jpg"

    try:
        tg_file = await photo.get_file()
        await tg_file.download_to_drive(custom_path=str(foto_path))
    except Exception as e:
        await msg.reply_text(f"Foto-Download-Fehler: {e}")
        return

    briefing = state.get_briefing_pending()
    if briefing:
        state.add_patricia_antwort(foto=str(foto_path))
        n = len(state.get_briefing_pending().get("patricia_fotos", []))
        await msg.reply_text(
            f"📸 Foto gespeichert ({n}. Foto). "
            f"Wird in der Story als Patricia-Bild verwendet."
        )
    else:
        sess = state.get_active_session() or state.set_active_session(profil="auto", kontext={})
        state.update_session(foto_path=str(foto_path))
        await msg.reply_text(
            f"📸 Foto gespeichert: <code>{foto_path.name}</code>\n"
            f"Wird bei naechstem /run verwendet.",
            parse_mode="HTML",
        )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video-Note Handler — speichert + transkribiert wenn moeglich."""
    if not _is_authorized(update):
        return
    msg = update.message
    video = msg.video or msg.video_note or msg.document
    if not video:
        return

    foto_dir = config.OUTPUTS_STORIES_DIR / "_uploads"
    foto_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".mp4"
    if msg.video_note:
        suffix = ".mp4"
    elif msg.document and msg.document.mime_type and "video" in msg.document.mime_type:
        suffix = ".mp4"
    video_path = foto_dir / f"patricia-video-{datetime.now().strftime('%Y%m%d-%H%M%S')}{suffix}"

    await msg.reply_text("🎬 Lade Video herunter ...")
    try:
        tg_file = await video.get_file()
        await tg_file.download_to_drive(custom_path=str(video_path))
    except Exception as e:
        logger.exception("Video-Download fehlgeschlagen")
        await msg.reply_text(f"Video-Download-Fehler: {e}")
        return

    # Audio-Spur transkribieren wenn verfuegbar
    text = ""
    if transcribe.is_available():
        try:
            text = transcribe.transkribiere_audio(video_path)
        except Exception as e:
            logger.warning(f"Video-Transkription fehlgeschlagen: {e}")

    briefing = state.get_briefing_pending()
    if briefing:
        state.add_patricia_antwort(video=str(video_path), text=text or None)
        await msg.reply_text(
            f"🎬 Video gespeichert.\n"
            + (f"<b>Audio-Transkript:</b> <i>{text[:400]}</i>\n\n" if text else "")
            + f"Tippe /generieren wenn du fertig bist.",
            parse_mode="HTML",
        )
    else:
        await msg.reply_text(
            f"🎬 Video gespeichert: <code>{video_path.name}</code>\n"
            + (f"Transkript: <i>{text[:300]}</i>\n\n" if text else "")
            + f"Tippe /run um eine Story damit zu starten.",
            parse_mode="HTML",
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text-Handler — sammelt Antworten in offenes Briefing."""
    if not _is_authorized(update):
        return
    msg = update.message
    if not msg.text or msg.text.startswith("/"):
        return

    briefing = state.get_briefing_pending()
    if briefing:
        state.add_patricia_antwort(text=msg.text)
        # IDEE-Modus: erste Antwort loest direkt die Story-Idee aus
        if briefing.get("modus") == "idee":
            await msg.reply_text("📝 Hab deinen Tag — bau dir die Story-Idee …")
            try:
                await task_daily_story.generiere_idee_aus_input()
            except Exception as e:
                logger.exception("generiere_idee_aus_input failed")
                await msg.reply_text(f"Crash bei Idee-Generierung: {e}")
            return
        n = len(state.get_briefing_pending().get("patricia_antworten", []))
        await msg.reply_text(
            f"📝 Notiert ({n}. Antwort). Weitere Infos schicken oder /generieren tippen."
        )
    else:
        sess = state.get_active_session() or state.set_active_session(profil="auto", kontext={})
        state.update_session(input_text=msg.text)
        await msg.reply_text(
            f"📝 Notiert: <i>{msg.text[:200]}</i>\n"
            f"Kein offenes Briefing — tippe /run um eines zu starten.",
            parse_mode="HTML",
        )


# ========================================
# Scheduled Task: Daily Story (06:30)
# ========================================
async def daily_story_task():
    """Laeuft Mo-So 06:30 Europe/Zurich — schickt Morgen-Ping (Plan + Frage nach dem Tag)."""
    now = datetime.now(pytz.timezone(config.TIMEZONE))
    logger.info(f"daily_story_task gestartet um {now.strftime('%a %d.%m. %H:%M')}")

    try:
        # 06:30 = Morgen-Ping: zeigt heutigen Plan + fragt nach Patricias Tag.
        # Die naechste Sprachnotiz/Text loest die Story-Idee aus.
        await task_daily_story.morgen_ping()
    except Exception as e:
        logger.exception("daily_story_task crashed")
        try:
            from telegram import Bot
            bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            await bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=f"daily_story_task crashed: {e}",
            )
        except Exception:
            pass


# ========================================
# MAIN
# ========================================
async def main():
    # Telegram-Application
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("run", cmd_run_now))
    app.add_handler(CommandHandler("generieren", cmd_generieren))
    app.add_handler(CommandHandler("idee", cmd_idee))
    app.add_handler(CommandHandler("render", cmd_render))
    app.add_handler(CommandHandler("fokus", cmd_fokus))
    app.add_handler(CommandHandler("notion", cmd_notion))

    # Reihenfolge wichtig: Voice/Video/Photo VOR Text
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, handle_video))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Scheduler
    tz = pytz.timezone(config.TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(
        daily_story_task,
        CronTrigger(
            hour=config.DAILY_STORY_TIME["hour"],
            minute=config.DAILY_STORY_TIME["minute"],
            timezone=tz,
        ),
        id="daily_story_render",
        name="Daily Story Render Mo-So 06:30",
    )
    scheduler.start()
    logger.info(
        f"Scheduler aktiv: Mo-So "
        f"{config.DAILY_STORY_TIME['hour']:02d}:{config.DAILY_STORY_TIME['minute']:02d} "
        f"{config.TIMEZONE}"
    )

    # Telegram polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Telegram-Polling aktiv. Bot ist online.")

    # Forever-Loop (bis Ctrl-C oder Railway-Stop)
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
