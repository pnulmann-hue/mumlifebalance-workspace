# -*- coding: utf-8 -*-
"""Der Weg zu Patricia: der Kochassistent (Telegram-Bot auf kochbot.mumlifebalance.ch).

Seit 27.10.2026 laufen die Samstagsfragen ueber ihn statt ueber den Gartenbot. Der
Gartenbot laeuft auf Railway noch und hat die Antworten verschluckt.

* senden: der Bot schickt die Fragen selbst (/api/essensfragen) und legt sie in
  seinen Chatverlauf, damit er die Antwort einordnen kann.
* lesen:  die Antworten stehen in seiner Datenbank (Supabase, Tabelle messages),
  auch Sprachnachrichten, die er schon in Text umgewandelt hat.

Zugang: Supabase-Adresse und Schluessel aus C:/Users/pnulm/koch-bot/.env.local.
Den Telegram-Schluessel braucht es hier nicht, der bleibt beim Bot.
"""
import json, os, urllib.parse, urllib.request

ENV = r"C:/Users/pnulm/koch-bot/.env.local"
BOT = "https://kochbot.mumlifebalance.ch"
KOPF = "\U0001f37d Essensplan:"  # gleich wie ESSENSFRAGEN_KOPF in koch-bot/lib/essensfragen.ts


def _zugang():
    if not os.path.exists(ENV):
        raise SystemExit("Kochassistent-Zugang fehlt: %s" % ENV)
    env = {}
    for zeile in open(ENV, encoding="utf-8"):
        if "=" in zeile and not zeile.lstrip().startswith("#"):
            k, v = zeile.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    url, key = env.get("NEXT_PUBLIC_SUPABASE_URL"), env.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise SystemExit("In %s fehlen NEXT_PUBLIC_SUPABASE_URL oder SUPABASE_SERVICE_ROLE_KEY." % ENV)
    return url.rstrip("/"), key


def _hole(pfad, key, daten=None, kopf=None):
    req = urllib.request.Request(pfad, data=daten, headers=kopf or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def senden(text):
    """Schickt die Fragen (Text beginnt mit KOPF); gibt den Zeitpunkt (ISO, UTC) zurueck."""
    _, key = _zugang()
    antwort = _hole(BOT + "/api/essensfragen", key,
                    json.dumps({"text": text}).encode("utf-8"),
                    {"Content-Type": "application/json", "x-service-key": key})
    if not antwort.get("ok") or not antwort.get("gesendet"):
        raise SystemExit("Kochassistent hat nichts geschickt: %s" % antwort)
    return antwort["gefragt_am"]


def antworten():
    """Ihre Nachrichten seit den letzten Fragen: (frage_zeit, [(zeit, text), ...])."""
    url, key = _zugang()
    kopf = {"apikey": key, "Authorization": "Bearer " + key}
    q = urllib.parse.urlencode({
        "select": "chat_id,created_at", "role": "eq.assistant",
        "content": "like." + KOPF + " vier Fragen*",
        "order": "created_at.desc", "limit": "1"})
    frage = _hole("%s/rest/v1/messages?%s" % (url, q), key, kopf=kopf)
    if not frage:
        return None, []
    f = frage[0]
    q = urllib.parse.urlencode([
        ("select", "content,created_at"), ("chat_id", "eq." + f["chat_id"]),
        ("role", "eq.user"), ("created_at", "gt." + f["created_at"]),
        ("order", "created_at.asc")])
    zeilen = _hole("%s/rest/v1/messages?%s" % (url, q), key, kopf=kopf)
    return f["created_at"], [(z["created_at"], (z["content"] or "").strip())
                             for z in zeilen if (z["content"] or "").strip()]
