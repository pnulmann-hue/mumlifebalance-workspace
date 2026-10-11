# -*- coding: utf-8 -*-
"""Der Telegram-Zugang fuer den Essensplan-Dialog.

Kein Schluessel im Code: Token und Chat-ID kommen aus einer .env.
Fehlt sie, bricht das Skript ab statt mit einem eingebauten Wert
weiterzulaufen.
"""
import io, os, json, time, urllib.request, urllib.error

HIER = os.path.dirname(os.path.abspath(__file__))

# Reihenfolge der Suche: eigene .env zuerst, dann die vorhandenen Bots.
KANDIDATEN = [
    os.path.join(HIER, ".env"),
    os.path.join(HIER, "..", "garten-telegram-bot", ".env"),
    os.path.join(HIER, "..", "telegram-news-bot", ".env"),
]


def zugang():
    for pfad in KANDIDATEN:
        if not os.path.exists(pfad):
            continue
        env = {}
        for zeile in io.open(pfad, encoding="utf-8", errors="replace"):
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#") or "=" not in zeile:
                continue
            k, v = zeile.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
        tok, chat = env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")
        if tok and chat:
            return tok, chat, os.path.normpath(pfad)
    raise SystemExit(
        "Kein Telegram-Zugang gefunden. Lege scripts/mealplan-dialog/.env an mit\n"
        "  TELEGRAM_BOT_TOKEN=...\n  TELEGRAM_CHAT_ID=...")


def ruf(methode, daten=None, versuche=3):
    tok, chat, _ = zugang()
    url = "https://api.telegram.org/bot%s/%s" % (tok, methode)
    leib = None
    if daten is not None:
        daten.setdefault("chat_id", chat)
        leib = json.dumps(daten).encode("utf-8")
    letzter = ""
    for n in range(versuche):
        try:
            anfrage = urllib.request.Request(
                url, data=leib,
                headers={"Content-Type": "application/json"} if leib else {})
            with urllib.request.urlopen(anfrage, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            antwort = e.read().decode("utf-8", "replace")
            try:
                return json.loads(antwort)
            except Exception:
                letzter = antwort[:200]
        except Exception as e:
            letzter = str(e)[:200]
        time.sleep(2 * (n + 1))   # wachsende Pause, ein Schluckauf kippt nichts
    return {"ok": False, "description": letzter}


def senden(text):
    """Schickt eine Nachricht. Telegram-Markdown bleibt bewusst aussen vor —
    ein Sternchen im Rezeptnamen wuerde sonst die ganze Nachricht ablehnen."""
    antwort = ruf("sendMessage", {"text": text, "disable_web_page_preview": True})
    if not antwort.get("ok"):
        raise SystemExit("Telegram: %s" % antwort.get("description"))
    return antwort["result"]["message_id"]
