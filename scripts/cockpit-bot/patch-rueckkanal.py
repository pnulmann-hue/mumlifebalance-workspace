"""Haengt den Rueckkanal in `bot.py` ein — Text und Sprachnotiz.

Bis zum 24.09.2026 nahm der Bot nur feste Befehle (`/cockpit`, `/news`). Wer
ihm etwas schrieb, bekam keine Antwort — die Nachricht fiel ins Leere. Genau
das war die Luecke: Patricia sieht am Handy, dass ein Beitrag noch nicht frei
ist, und kann nichts tun.

Danach:

    Sie:  „was steht heute an?"          -> Antwort aus Cockpit-Stand + Notion
    Sie:  🎤 „bei Mittwoch die Caption neu" -> Auftrag, Claude arbeitet ihn ein

🚨 Anker-Pruefung: fehlt oder doppelt sich eine Fundstelle, bricht das Skript
ab. Danach prueft Python selbst die Syntax der geaenderten Datei.

Aufruf:
  python scripts/cockpit-bot/patch-rueckkanal.py [--pruefen]
"""

import ast
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = Path(__file__).resolve().parent
BOT = HIER / "bot.py"

# --------------------------------------------------------------------------
# 1) Module dazu
# --------------------------------------------------------------------------
ALT_IMPORT = """from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)"""
NEU_IMPORT = """from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)"""

ALT_MOD = "import posting_checker"
NEU_MOD = "import posting_checker\nimport rueckkanal"

# --------------------------------------------------------------------------
# 2) Die Handler selbst
# --------------------------------------------------------------------------
ALT_MAIN = """# ========================================
# MAIN
# ========================================"""

NEU_MAIN = '''# ========================================
# RUECKKANAL — sie schreibt oder spricht, der Bot antwortet
# ========================================
async def _beantworten(update: Update, nachricht: str, aus_sprache: bool = False):
    """Ein Weg fuer Text und Sprache — was danach passiert, ist dasselbe."""
    if aus_sprache:
        await update.message.reply_text("🎤 Verstanden: „%s“" % nachricht[:280])

    gedeutet = rueckkanal.absicht(nachricht)
    art = gedeutet.get("art")

    if art == "frage":
        await update.message.reply_chat_action("typing")
        try:
            tasks = notion_reader.get_offene_tasks_heute()
        except Exception as e:
            logger.warning("Notion-Tasks nicht erreichbar: %s", e)
            tasks = []
        text = rueckkanal.antwort_auf_frage(
            nachricht, tasks, rueckkanal.cockpit_stand())
        await update.message.reply_text(text, parse_mode="Markdown")
        return

    if art == "auftrag":
        ergebnis = rueckkanal.auftrag_ablegen(nachricht, gedeutet)
        if ergebnis.get("ok"):
            # 🚨 NIE „erledigt" melden. Der Bot fuehrt nichts aus — er nimmt
            # entgegen. Eine Bestaetigung, die nach Erledigung klingt, ist
            # genau der Fehler, an dem am 16.09. die Freigabe gescheitert ist.
            await update.message.reply_text(
                "📥 Aufgenommen: %s\\n\\n"
                "Ich arbeite es heute Abend um 19:30 ein und melde mich, "
                "wenn es zur Freigabe steht." % (gedeutet.get("thema") or "dein Auftrag"))
        else:
            await update.message.reply_text(
                "Ich konnte es nicht ablegen (%s). Sag es mir nachher nochmal."
                % ergebnis.get("fehler", "unbekannt"))
        return

    await update.message.reply_text(
        "Das habe ich nicht sicher verstanden. Meinst du\\n"
        "• eine *Frage* („was steht heute an?“) oder\\n"
        "• einen *Auftrag* („bei Mittwoch die Caption neu“)?",
        parse_mode="Markdown")


async def nachricht_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    text = (update.message.text or "").strip()
    if not text:
        return
    await _beantworten(update, text)


async def nachricht_sprache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_authorized(update):
        return
    await update.message.reply_chat_action("typing")
    try:
        ton = update.message.voice or update.message.audio
        datei = await context.bot.get_file(ton.file_id)
        roh = bytes(await datei.download_as_bytearray())
    except Exception as e:
        logger.exception("Sprachnotiz nicht ladbar")
        await update.message.reply_text("Die Sprachnotiz kam nicht an (%s)." % e)
        return

    ergebnis = await rueckkanal.sprachnotiz_zu_text(roh)
    if not ergebnis.get("ok"):
        await update.message.reply_text(ergebnis.get("hinweis", "Hat nicht geklappt."))
        return
    text = ergebnis.get("text", "").strip()
    if not text:
        await update.message.reply_text("Ich habe nichts verstanden. Nochmal?")
        return
    await _beantworten(update, text, aus_sprache=True)


# ========================================
# MAIN
# ========================================'''

# --------------------------------------------------------------------------
# 3) Anmelden — NACH den Befehlen, sonst schluckt der Text-Handler sie
# --------------------------------------------------------------------------
ALT_REG = """    app.add_handler(CommandHandler("posting_nein", cmd_posting_nein))"""
NEU_REG = """    app.add_handler(CommandHandler("posting_nein", cmd_posting_nein))

    # 🚨 Der Rueckkanal kommt ZULETZT und schliesst Befehle aus. Sonst
    # verschluckt er `/cockpit` und die festen Befehle antworten nie mehr.
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, nachricht_text))
    app.add_handler(MessageHandler(
        filters.VOICE | filters.AUDIO, nachricht_sprache))"""

ERSETZUNGEN = [
    ("Import telegram.ext", ALT_IMPORT, NEU_IMPORT),
    ("Modul rueckkanal", ALT_MOD, NEU_MOD),
    ("Handler-Funktionen", ALT_MAIN, NEU_MAIN),
    ("Handler anmelden", ALT_REG, NEU_REG),
]


def main():
    nur_pruefen = "--pruefen" in sys.argv
    quelle = BOT.read_text(encoding="utf-8")
    vorher = len(quelle)

    if "import rueckkanal" in quelle:
        sys.exit("Der Rueckkanal ist schon eingebaut — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = quelle.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        quelle = quelle.replace(alt, neu)
        print("  %-20s ersetzt" % name)

    try:
        ast.parse(quelle)
    except SyntaxError as e:
        sys.exit("ABBRUCH — Syntaxfehler in Zeile %s: %s" % (e.lineno, e.msg))
    print("\n  Syntax: in Ordnung")

    if nur_pruefen:
        print("\nPROBELAUF — nichts geschrieben.")
        return
    BOT.write_text(quelle, encoding="utf-8")
    print("\nGeschrieben: %s  (%d -> %d Zeichen)" % (BOT, vorher, len(quelle)))


if __name__ == "__main__":
    main()
