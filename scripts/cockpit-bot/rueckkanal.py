"""Der Rueckkanal — Patricia spricht oder tippt, der Bot antwortet.

Bis zum 24.09.2026 lief der Cockpit-Bot nur in eine Richtung: er schickte
morgens um 06:30 ein Briefing und nahm ansonsten nur feste Befehle
(`/cockpit`, `/news`). Wer am Handy sah, dass ein Beitrag noch nicht frei ist,
konnte nichts tun — der Rechner stand zu Hause.

Anlass war eine Werbeanzeige (`katrinkrappweis`, 24.09.2026), die genau diesen
Weg zeigt: eine Sprachnotiz ins Telegram, und die Aufgaben kommen zurueck.
Patricia dazu: *„setz das so um."*

    Sie:  „was steht heute an?"        -> Antwort aus Notion + Cockpit-Stand
    Sie:  „bei Mittwoch die Caption neu" -> Auftrag, Claude arbeitet ihn ein

🚨 **Der Bot kommt NICHT an die Cockpit-Datenbank.** Die Beitraege liegen in der
Artifact-Datenbank, und die kann nur Claude lesen (`ArtifactData`). Ein Worker
auf Railway hat dort keinen Zugang — kein Schluessel der Welt aendert das, es
gibt schlicht keine Schnittstelle. Deshalb zwei getrennte Wege:

| Absicht | Wie beantwortet |
|---|---|
| **Frage** | sofort, aus `cockpit-stand.json` (taeglich vom Abgleich geschrieben) + Notion-Aufgaben |
| **Auftrag** | als Notion-Aufgabe abgelegt; der Task `kommentare-einarbeiten` (19:30) holt sie ab |

🚨 **Ein Auftrag wird NIE stillschweigend als erledigt gemeldet.** Der Bot
bestaetigt nur die Annahme und sagt dazu, wann es bearbeitet wird. Alles andere
waere eine Zusage, die er nicht halten kann — genau der Fehler, der am 16.09.
bei der Freigabe passiert ist („abgelegt", obwohl nie etwas rausging).

**Sprachnotizen** brauchen einen Transkriptions-Dienst. Der OpenAI-Schluessel
wurde am 13.09.2026 widerrufen; ohne `OPENAI_API_KEY` sagt der Bot das ehrlich
und bittet um Text, statt so zu tun, als haette er verstanden.
"""

import json
import logging
import os
from datetime import date
from pathlib import Path

import anthropic
import httpx

import config

logger = logging.getLogger(__name__)

HIER = Path(__file__).resolve().parent
STAND = HIER / "cockpit-stand.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_URL = "https://api.openai.com/v1/audio/transcriptions"

# Telegram gibt Sprachnotizen als OGG/Opus. 20 MB ist Telegrams eigene Grenze
# fuer den Bot-Download; laenger als ein paar Minuten spricht niemand.
MAX_TON_BYTES = 20 * 1024 * 1024


# --------------------------------------------------------------------------
# Der Cockpit-Stand — was der Bot ueber die Beitraege weiss
# --------------------------------------------------------------------------
def cockpit_stand() -> dict:
    """Liest den letzten Abzug aus dem Cockpit.

    Geschrieben von `scripts/cockpit/stand-fuer-bot.py`, das in Claude Code
    laeuft und damit an die Artifact-Datenbank kommt. Fehlt die Datei, sagt der
    Bot das — ein leerer Stand darf nie als „nichts offen" durchgehen.
    """
    if not STAND.exists():
        return {"fehlt": True}
    try:
        return json.loads(STAND.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("cockpit-stand.json unlesbar: %s", e)
        return {"fehlt": True, "fehler": str(e)}


def stand_alter_tage(stand: dict) -> int | None:
    """Wie alt ist der Stand? Ein alter Stand ist schlimmer als keiner,
    weil er aussieht wie ein aktueller."""
    roh = stand.get("stand")
    if not roh:
        return None
    try:
        return (date.today() - date.fromisoformat(roh[:10])).days
    except Exception:
        return None


# --------------------------------------------------------------------------
# Sprachnotiz -> Text
# --------------------------------------------------------------------------
async def sprachnotiz_zu_text(datei_bytes: bytes, dateiname: str = "notiz.ogg") -> dict:
    """Gibt {ok, text} oder {ok: False, grund}."""
    if not OPENAI_API_KEY:
        return {
            "ok": False,
            "grund": "kein_schluessel",
            "hinweis": (
                "Sprachnotizen kann ich gerade nicht abhören — dafür fehlt der "
                "Zugang zum Transkriptions-Dienst. Schreib es mir kurz als Text, "
                "dann geht es sofort."
            ),
        }
    if len(datei_bytes) > MAX_TON_BYTES:
        return {"ok": False, "grund": "zu_gross",
                "hinweis": "Die Sprachnotiz ist zu lang. Zwei Sätze reichen mir."}

    try:
        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.post(
                WHISPER_URL,
                headers={"Authorization": "Bearer %s" % OPENAI_API_KEY},
                files={"file": (dateiname, datei_bytes, "audio/ogg")},
                data={"model": "whisper-1", "language": "de"},
            )
        if r.status_code != 200:
            logger.warning("Whisper %s: %s", r.status_code, r.text[:200])
            return {"ok": False, "grund": "dienst",
                    "hinweis": "Das Abhören hat nicht geklappt. Schreib es mir kurz."}
        return {"ok": True, "text": (r.json().get("text") or "").strip()}
    except Exception as e:
        logger.exception("Transkription gescheitert")
        return {"ok": False, "grund": "fehler", "hinweis":
                "Das Abhören ist abgebrochen (%s). Schreib es mir kurz." % e}


# --------------------------------------------------------------------------
# Absicht erkennen
# --------------------------------------------------------------------------
ABSICHT_BRIEF = """Du ordnest EINE Nachricht von Patricia ein. Sie steuert damit
ihr Content-Cockpit vom Handy aus.

Antworte NUR mit JSON, ohne Fliesstext drumherum:
{"art": "frage" | "auftrag" | "unklar", "thema": "<max 60 Zeichen>", "beitrag": "<Tag oder Name, falls genannt, sonst leer>"}

"frage"   = sie will etwas wissen (was steht an, was fehlt, was ist fertig,
            welche Zahlen, was ging raus)
"auftrag" = sie will, dass etwas geaendert oder gemacht wird (Caption neu,
            Hook anders, Video passt nicht, verschieben, Idee festhalten)
"unklar"  = beides denkbar oder zu wenig Information

Bei einer Sprachnotiz ist der Text automatisch transkribiert — Tippfehler und
schiefe Woerter sind normal, rate nicht zu viel hinein.

Nachricht: %s"""


def absicht(nachricht: str) -> dict:
    """Frage oder Auftrag? Im Zweifel 'unklar' — lieber nachfragen als raten."""
    if not config.ANTHROPIC_API_KEY:
        return {"art": "unklar", "thema": "", "beitrag": ""}
    try:
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        antwort = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": ABSICHT_BRIEF % nachricht[:1500]}],
        )
        roh = antwort.content[0].text.strip()
        # Das Modell packt JSON gern in einen Codeblock.
        if roh.startswith("```"):
            roh = roh.split("```")[1]
            if roh.startswith("json"):
                roh = roh[4:]
        d = json.loads(roh.strip())
        if d.get("art") not in ("frage", "auftrag", "unklar"):
            d["art"] = "unklar"
        return d
    except Exception as e:
        logger.warning("Absicht nicht erkannt: %s", e)
        return {"art": "unklar", "thema": "", "beitrag": ""}


# --------------------------------------------------------------------------
# Antworten auf eine Frage
# --------------------------------------------------------------------------
def _zeile(b: dict) -> str:
    tag = b.get("tag") or "ohne Datum"
    prof = "doTERRA" if (b.get("profil") == "doterra") else "Mentoring"
    return "• %s · %s — %s" % (tag, prof, b.get("name") or b.get("id") or "?")


def antwort_auf_frage(nachricht: str, notion_tasks: list, stand: dict) -> str:
    """Baut die Antwort aus echten Daten. Claude formuliert nur — die Zahlen
    kommen aus dem Stand, nie aus dem Modell."""
    teile = []

    if stand.get("fehlt"):
        teile.append("⚠️ Ich komme gerade nicht an den Cockpit-Stand. "
                     "Was ich habe, sind die Notion-Aufgaben.")
    else:
        alter = stand_alter_tage(stand)
        if alter is not None and alter >= 2:
            teile.append("⚠️ Mein Cockpit-Stand ist %d Tage alt (%s)."
                         % (alter, stand.get("stand", "?")[:10]))

        deine = stand.get("offen_du") or []
        meine = stand.get("offen_claude") or []
        fertig = stand.get("fertig") or []
        durch = stand.get("datum_durch") or []

        # Reihenfolge nach Dringlichkeit: was sie mit einem Klick erledigen
        # kann, steht oben. „Bei mir liegt" ist nur zur Beruhigung da.
        if fertig:
            teile.append("*Kann raus — nur noch freigeben* (%d)" % len(fertig))
            teile += [_zeile(b) for b in fertig[:6]]
            if len(fertig) > 6:
                teile.append("… und %d weitere" % (len(fertig) - 6))
        if deine:
            teile.append("\n*Braucht dich* (%d)" % len(deine))
            teile += ["%s — %s" % (_zeile(b), b.get("was") or "") for b in deine[:6]]
            if len(deine) > 6:
                teile.append("… und %d weitere" % (len(deine) - 6))
        if durch:
            # 🚨 Muss sichtbar sein: diese Beitraege sehen fertig aus, gehen
            # aber nie raus, weil Blotato nichts in der Vergangenheit annimmt.
            teile.append("\n*Datum ist durch — neu einplanen* (%d)" % len(durch))
            teile += [_zeile(b) for b in durch[:4]]
            if len(durch) > 4:
                teile.append("… und %d weitere" % (len(durch) - 4))
        if meine:
            teile.append("\n_Bei mir liegt: %d_" % len(meine))
        if not (deine or meine or fertig or durch):
            teile.append("Im Cockpit ist gerade nichts offen.")

    if notion_tasks:
        teile.append("\n*Aus Notion* (%d)" % len(notion_tasks))
        for t in notion_tasks[:6]:
            name = t.get("name") or t.get("title") or "?"
            teile.append("• %s" % name)

    return "\n".join(teile) if teile else "Ich finde gerade nichts Offenes."


# --------------------------------------------------------------------------
# Auftrag annehmen
# --------------------------------------------------------------------------
def auftrag_ablegen(nachricht: str, gedeutet: dict) -> dict:
    """Legt den Auftrag als Notion-Aufgabe ab.

    🚨 Der Bot fuehrt NICHTS aus. Er nimmt entgegen und sagt, wann es bearbeitet
    wird. Eine Bestaetigung, die nach Erledigung klingt, waere eine Luege — und
    genau daran ist am 16.09. die Freigabe gescheitert.
    """
    try:
        from notion_client import Client
        client = Client(auth=config.NOTION_API_KEY)
        titel = "Cockpit-Auftrag: %s" % (gedeutet.get("thema") or nachricht[:50])
        eigenschaften = {
            "Name": {"title": [{"text": {"content": titel[:100]}}]},
        }
        seite = client.pages.create(
            parent={"database_id": config.NOTION_DB_AUFGABEN},
            properties=eigenschaften,
            children=[{
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {
                    "content": "Von Patricia über Telegram, %s:\n\n%s"
                               % (date.today().isoformat(), nachricht[:1800])}}]},
            }],
        )
        return {"ok": True, "id": seite.get("id", "")}
    except Exception as e:
        logger.exception("Auftrag konnte nicht abgelegt werden")
        return {"ok": False, "fehler": str(e)}
