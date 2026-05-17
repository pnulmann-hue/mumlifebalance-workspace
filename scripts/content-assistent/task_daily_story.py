"""Daily-Story-Task — der Workflow-Orchestrator.

ZWEI MODI:

1. SPARRING (Default für 06:30-Cron + /run):
   - Bot lädt Notion-Kontext + active-funnels
   - Bot fragt Patricia via Telegram: „Diese Woche ist X im Fokus, ich denke Y,
     gib mir bitte folgende Infos: Frage 1, Frage 2, ... Hast du ein Foto?"
   - Patricia antwortet via Voice/Text/Foto
   - Bot generiert dann die Story mit den echten Antworten

2. SCHNELL (/run schnell oder Cron-Override):
   - Bot generiert sofort ohne Rückfrage (alter Modus)
   - Risiko: Halluzinationen wenn Notion-Kontext nicht reicht

Beide Modi nutzen am Ende die gleiche Generierung:
  Stage A: Notion-Kontext
  Stage B: Claude (System-Prompt mit Pflicht-Lese-Liste)
  Stage C: Render-Caller → 8 PNGs
  Stage D: Telegram-Versand
  Stage E: Wochenlog updaten
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, datetime
from pathlib import Path

import pytz
from telegram import Bot, InputMediaPhoto

import config
import claude_caller
import notion_reader
import render_caller
import state

logger = logging.getLogger(__name__)


# ========================================
# Profil-Bestimmung
# ========================================

def bestimme_profil_heute(heute: date = None) -> str:
    """Welches Profil wird heute beworben?

    Default: Wochentag-Rotation aus config.TAGES_PROFIL_ROTATION.
    Override: könnte später aus Notion-Wochenplan kommen.
    """
    if heute is None:
        heute = date.today()
    return config.TAGES_PROFIL_ROTATION.get(heute.weekday(), "mentoring")


# ========================================
# Telegram-Helper
# ========================================

async def send_status(bot: Bot, text: str):
    """Sendet Status-Update an Patricia."""
    try:
        await bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Telegram-Send-Fehler: {e}")


async def send_slides(bot: Bot, png_paths: list[str], caption_intro: str = ""):
    """Sendet die 8 Story-PNGs einzeln mit Slide-Nummer als Caption."""
    if not png_paths:
        return

    if caption_intro:
        await send_status(bot, caption_intro)

    # Sende einzeln (Telegram-Group-Limit ist 10, aber einzeln ist robuster)
    for idx, p in enumerate(png_paths, start=1):
        try:
            with open(p, "rb") as f:
                await bot.send_photo(
                    chat_id=config.TELEGRAM_CHAT_ID,
                    photo=f,
                    caption=f"Slide {idx}/{len(png_paths)}",
                )
            await asyncio.sleep(0.4)  # Telegram-Rate-Limit-Schoner
        except Exception as e:
            logger.error(f"Foto-Send-Fehler {p}: {e}")


# ========================================
# Hauptfunktion
# ========================================

async def briefing_anfragen(profil_override: str = None) -> dict:
    """SPARRING-MODUS: Bot fragt Patricia VOR Generierung.

    Workflow:
      1. Lädt Notion-Kontext + active-funnels
      2. Generiert Briefing-Text via Claude (3-5 konkrete Fragen)
      3. Schickt Briefing per Telegram an Patricia
      4. Speichert State (briefing_pending) — wartet auf Antwort
      5. Patricia antwortet (Voice/Text/Foto/Video) — wird im bot.py verarbeitet
      6. Wenn Patricia /generieren tippt → ruft generiere_story_aus_briefing()
    """
    started = datetime.now()
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    heute = date.today()
    profil = profil_override or bestimme_profil_heute(heute)

    logger.info(f"=== Briefing-Anfrage: {heute} {profil} ===")

    # Notion + Override Kontext
    try:
        kontext = notion_reader.lade_wochen_kontext()
    except Exception as e:
        logger.error(f"Notion-Fehler: {e}")
        kontext = {"monatsplan": None, "wochenplan": None, "themen": []}

    # Briefing generieren
    await send_status(
        bot,
        f"<b>📋 Story-Briefing wird vorbereitet …</b>\n"
        f"Datum: {heute.strftime('%a %d.%m.%Y')}\n"
        f"Profil: <b>{profil}</b>\n"
        f"DISG heute: <b>{state.empfehle_disg_heute()}</b>"
    )

    try:
        briefing = claude_caller.generate_briefing_anfrage(profil, kontext, heute)
    except Exception as e:
        logger.exception("Briefing-Generierung crashed")
        await send_status(bot, f"<b>Briefing-Fehler:</b> {e}")
        return {"ok": False, "error": str(e)}

    if not briefing.get("ok"):
        await send_status(bot, f"<b>Fehler:</b> {briefing.get('error')}")
        return briefing

    # Briefing speichern + an Patricia senden
    state.set_briefing_pending(
        profil=profil,
        briefing_text=briefing["telegram_text"],
        fragen=briefing["fragen"],
        kontext_snapshot=kontext,
    )

    # Telegram-Sendung mit Hinweisen am Ende
    final_text = briefing["telegram_text"] + (
        "\n\n———\n"
        "<i>📨 Antworte mir per Sprachnotiz / Text / Foto / Video.</i>\n"
        "<i>🚀 Wenn fertig: tippe /generieren</i>\n"
        "<i>⚡ Oder: /run schnell — Story sofort ohne weitere Infos</i>"
    )

    await send_status(bot, final_text)
    duration = (datetime.now() - started).total_seconds()
    logger.info(f"Briefing gesendet ({briefing['tokens_in']}/{briefing['tokens_out']} Tokens, {duration:.1f}s)")

    return {
        "ok": True,
        "modus": "sparring",
        "profil": profil,
        "fragen_count": len(briefing["fragen"]),
        "tokens": {"in": briefing["tokens_in"], "out": briefing["tokens_out"]},
        "duration_sec": duration,
    }


async def generiere_story_aus_briefing() -> dict:
    """Wird aufgerufen wenn Patricia /generieren tippt.

    Liest: briefing-pending.json (mit Patricia-Antworten)
    Baut Patricia-Input zusammen aus allen Voice/Text-Antworten
    Ruft dann run(modus="schnell", patricia_input=...) auf.
    """
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    briefing = state.get_briefing_pending()

    if not briefing:
        await send_status(bot, "Kein offenes Briefing — tippe /run um eines zu starten.")
        return {"ok": False, "error": "no_pending_briefing"}

    # Patricia-Input aus allen Antworten zusammenbauen
    antworten_text = []
    for a in briefing.get("patricia_antworten", []):
        antworten_text.append(a.get("text", ""))
    patricia_input = "\n\n".join(t for t in antworten_text if t.strip())

    foto_path = None
    if briefing.get("patricia_fotos"):
        foto_path = briefing["patricia_fotos"][-1]  # neuestes Foto

    if not patricia_input and not foto_path:
        await send_status(
            bot,
            "Du hast noch nichts beantwortet. Schick mir bitte Voice/Text mit deinen Infos, "
            "dann tippe /generieren.\n\nOder: /run schnell — generiere ohne deine Infos (Risiko: Halluzinationen)."
        )
        return {"ok": False, "error": "no_patricia_input"}

    profil = briefing["profil"]
    state.clear_briefing_pending()

    return await run(
        modus="schnell",
        profil_override=profil,
        patricia_input=patricia_input,
        patricia_foto=foto_path,
    )


async def run(modus: str = "schnell", profil_override: str = None,
              patricia_input: str = None, patricia_foto: str = None) -> dict:
    """SCHNELL-MODUS: generiert Story sofort ohne weitere Patricia-Frage.

    Args:
        modus: "schnell" oder "test" (test = test-prefix im slug)
        profil_override: forciere ein Profil
        patricia_input: Patricia-Voice/Text-Antworten (aus Briefing oder direkt)
        patricia_foto: optionaler Foto-Pfad

    Returns:
        {ok, profil, slug, html_path, png_paths, tokens, duration_sec}
    """
    started = datetime.now()
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    heute = date.today()

    profil = profil_override or bestimme_profil_heute(heute)
    logger.info(f"=== Story-Generierung: {heute} {profil} (modus={modus}) ===")

    await send_status(
        bot,
        f"<b>🎨 Story wird generiert</b>\n"
        f"Datum: {heute.strftime('%a %d.%m.%Y')}\n"
        f"Profil: <b>{profil}</b>\n"
        f"DISG heute: <b>{state.empfehle_disg_heute()}</b>"
        + (f"\nPatricia-Input: {len(patricia_input)} Zeichen" if patricia_input else "")
        + (f"\nPatricia-Foto: ja" if patricia_foto else "")
    )

    # Notion-Kontext
    try:
        kontext = notion_reader.lade_wochen_kontext()
    except Exception as e:
        logger.error(f"Notion-Fehler: {e}")
        await send_status(bot, f"Notion-Fehler: {e}")
        kontext = {"monatsplan": None, "wochenplan": None, "themen": []}

    if patricia_input:
        kontext["patricia_input"] = patricia_input
    if patricia_foto:
        kontext["patricia_foto"] = patricia_foto

    # Stage 3: Slug bauen
    slug_prefix = "test-" if modus == "test" else ""
    fokus_text = ""
    if kontext.get("wochenplan") and kontext["wochenplan"].get("fokus_der_woche"):
        fokus = kontext["wochenplan"]["fokus_der_woche"]
        # Erste 5 Wörter als slug-Teil
        fokus_text = "-".join(w.lower() for w in fokus.split()[:4])
        # Sonderzeichen raus
        import re as _re
        fokus_text = _re.sub(r"[^a-z0-9-]", "", fokus_text)[:30]
    slug = f"{slug_prefix}{heute.isoformat()}-{profil}-{fokus_text or 'auto'}"

    # Stage 4: Claude-Caller
    await send_status(bot, "Claude generiert Slide-Texte ...")
    try:
        result = claude_caller.generate_story_html(
            profil=profil,
            kontext=kontext,
            heute=heute,
            slug=slug,
        )
    except Exception as e:
        logger.exception("Claude-Generierung crashed")
        await send_status(bot, f"<b>Fehler bei Claude-Aufruf:</b>\n{e}")
        return {"ok": False, "error": str(e)}

    if not result.get("ok"):
        await send_status(bot, f"<b>Fehler:</b> {result.get('error', 'unbekannt')}")
        return result

    logger.info(f"Story generiert: {result['slug']} (Tokens in/out: {result['tokens_in']}/{result['tokens_out']})")

    # Stage 5: Render-Caller
    await send_status(bot, "Rendere PNG-Folien (Puppeteer) ...")
    output_dir = Path(result["output_dir"])
    png_dir = output_dir / "png"
    try:
        render_result = render_caller.render_stories(
            html_path=result["html_path"],
            output_dir=png_dir,
        )
    except Exception as e:
        logger.exception("Render crashed")
        await send_status(bot, f"<b>Render-Fehler:</b> {e}")
        return {"ok": False, "error": str(e)}

    if not render_result.get("ok"):
        await send_status(
            bot,
            f"<b>Render-Fehler:</b> {render_result.get('error', 'unbekannt')}\n\n"
            f"HTML-Datei: {result['html_path']}"
        )
        return render_result

    # Stage 6: Telegram-Versand
    await send_status(
        bot,
        f"<b>{render_result['slides_count']} Folien fertig</b> — sende einzeln ..."
    )
    await send_slides(bot, render_result["png_paths"])

    # Stage 7: Wochenlog updaten
    state.add_to_wochenlog(heute.isoformat(), {
        "profil": profil,
        "disg": state.empfehle_disg_heute(),
        "slug": slug,
        "slides": render_result["slides_count"],
    })

    # Stage 8: Final-Push
    duration = (datetime.now() - started).total_seconds()
    await send_status(
        bot,
        f"<b>Fertig!</b>\n"
        f"Slides: {render_result['slides_count']}\n"
        f"Tokens: {result['tokens_in']:,} in / {result['tokens_out']:,} out\n"
        f"Dauer: {duration:.0f}s\n"
        f"Ordner: <code>{slug}</code>"
    )

    return {
        "ok": True,
        "profil": profil,
        "slug": slug,
        "html_path": str(result["html_path"]),
        "png_paths": render_result["png_paths"],
        "slides_count": render_result["slides_count"],
        "tokens": {"in": result["tokens_in"], "out": result["tokens_out"]},
        "duration_sec": duration,
    }


# ========================================
# CLI-Tester
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    profil = sys.argv[1] if len(sys.argv) > 1 else None
    sub_modus = sys.argv[2] if len(sys.argv) > 2 else "sparring"

    if sub_modus == "schnell":
        print(f"=== Schnell-Modus Test (profil={profil or 'auto'}) ===")
        result = asyncio.run(run(modus="test", profil_override=profil))
    else:
        print(f"=== Sparring-Modus Test (profil={profil or 'auto'}) ===")
        result = asyncio.run(briefing_anfragen(profil_override=profil))

    if result.get("ok"):
        print(f"\n[OK] {result['slug']}")
        print(f"  Slides: {result['slides_count']}")
        print(f"  Tokens: {result['tokens']}")
        print(f"  Dauer: {result['duration_sec']:.0f}s")
    else:
        print(f"\n[FEHLER] {result.get('error', 'unbekannt')}")
        sys.exit(1)
