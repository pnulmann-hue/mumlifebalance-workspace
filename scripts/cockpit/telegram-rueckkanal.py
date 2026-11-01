#!/usr/bin/env python3
"""Telegram-Rückkanal für die Cloud-Routine „Freigaben einplanen“.

Patricia schreibt dem Cockpit-Bot („Caption vom Sonntag kürzer“), die Routine liest
das beim nächsten Lauf, arbeitet es ein und plant erst nach ihrem „passt“ neu ein.
Das Deuten übernimmt Claude in der Routine; dieses Skript macht nur die Handgriffe:

  lesen                       neue Nachrichten aus Patricias Chat als JSON (bestätigt nichts)
  bestaetigen --bis <id>      Nachrichten bis einschliesslich <id> als gelesen markieren
  senden --datei <txt>        Nachricht an Patricia schicken
  blotato-suchen --zeitpunkt <ISO> [--profil mentoring|doterra]
                              eingeplante Blotato-Beiträge zu diesem Zeitpunkt
  blotato-loeschen --id <schedule-id>
                              einen eingeplanten Blotato-Beitrag zurücknehmen

Der Bot hat keinen Webhook. Darum liest `lesen` über getUpdates; Telegram hält
Nachrichten 24 Stunden. Erst `bestaetigen` nimmt sie aus der Schlange — stürzt ein
Lauf vorher ab, kommen sie beim nächsten wieder.

Zugang: TELEGRAM_BOT_TOKEN (oder TELEGRAM_COCKPIT_BOT_TOKEN) und TELEGRAM_CHAT_ID aus der
Umgebung, sonst aus der .env im Wurzelverzeichnis. Blotato läuft mit --proxy über den
Proxy der Cloud (der setzt den Schlüssel ein), sonst mit BLOTATO_API_KEY aus der .env.
Alle Aufrufe gehen über curl: Nodes fetch ignoriert den Proxy, curl nicht.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOTATO = "https://backend.blotato.com"
KONTO = {"mentoring": "mumlifebalance_patricia_ulmann", "doterra": "patricia_ulmann"}

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def env() -> dict:
    werte = {}
    datei = ROOT / ".env"
    if datei.exists():
        for zeile in datei.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)", zeile)
            if m:
                werte[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    werte.update({k: v for k, v in os.environ.items() if v})
    return werte


def telegram_zugang(e: dict) -> tuple[str, str]:
    token = e.get("TELEGRAM_BOT_TOKEN") or e.get("TELEGRAM_COCKPIT_BOT_TOKEN")
    chat = e.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        sys.exit("TELEGRAM_BOT_TOKEN oder TELEGRAM_CHAT_ID fehlt")
    return token, chat


def curl(url: str, methode: str = "GET", kopf: dict | None = None,
         daten: list[tuple[str, str]] | None = None, json_body: str | None = None) -> tuple[int, str]:
    args = ["curl", "-s", "-X", methode, "-w", "\n%{http_code}"]
    for k, v in (kopf or {}).items():
        args += ["-H", f"{k}: {v}"]
    eingabe = None
    if daten:
        for k, v in daten:
            args += ["--data-urlencode", f"{k}={v}"]
    if json_body is not None:
        args += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        eingabe = json_body
    args.append(url)
    r = subprocess.run(args, input=eingabe, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        sys.exit(f"curl fehlgeschlagen ({r.returncode})")
    text, _, status = r.stdout.rpartition("\n")
    return int(status or 0), text


def tg(token: str, methode: str, daten: list[tuple[str, str]]) -> dict:
    status, text = curl(f"https://api.telegram.org/bot{token}/{methode}", "POST", daten=daten)
    try:
        antwort = json.loads(text)
    except json.JSONDecodeError:
        sys.exit(f"Telegram antwortet nicht lesbar (HTTP {status})")
    if not antwort.get("ok"):
        sys.exit(f"Telegram: {antwort.get('description', status)}")
    return antwort


def lesen(_a) -> None:
    token, chat = telegram_zugang(env())
    antwort = tg(token, "getUpdates", [("timeout", "0"), ("allowed_updates", '["message"]')])
    nachrichten, hoechste = [], None
    for u in antwort["result"]:
        hoechste = max(hoechste or 0, u["update_id"])
        m = u.get("message") or {}
        # Sicherung gegen fremde Absender: nur Patricias Chat zählt.
        if str(m.get("chat", {}).get("id")) != str(chat):
            continue
        text = m.get("text") or m.get("caption") or ""
        if not text:
            text = "[Sprachnachricht — kann ich nicht hören]" if m.get("voice") else "[ohne Text]"
        bezug = m.get("reply_to_message") or {}
        nachrichten.append({
            "update_id": u["update_id"],
            "datum": m.get("date"),
            "text": text,
            "antwort_auf": bezug.get("text") or bezug.get("caption") or None,
        })
    print(json.dumps({"bis": hoechste, "nachrichten": nachrichten}, ensure_ascii=False, indent=1))


def bestaetigen(a) -> None:
    token, _ = telegram_zugang(env())
    tg(token, "getUpdates", [("offset", str(int(a.bis) + 1)), ("limit", "1"), ("timeout", "0")])
    print(json.dumps({"bestaetigt_bis": int(a.bis)}))


def senden(a) -> None:
    token, chat = telegram_zugang(env())
    text = Path(a.datei).read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("Nachricht ist leer")
    # Telegram nimmt höchstens 4096 Zeichen je Nachricht.
    teile = [text[i:i + 4000] for i in range(0, len(text), 4000)]
    for teil in teile:
        tg(token, "sendMessage", [("chat_id", chat), ("text", teil)])
    print(json.dumps({"gesendet": len(teile)}))


def blotato_kopf(a) -> dict:
    if a.proxy:
        return {}
    key = env().get("BLOTATO_API_KEY")
    if not key:
        sys.exit("BLOTATO_API_KEY fehlt (oder --proxy angeben)")
    return {"blotato-api-key": key}


def blotato_suchen(a) -> None:
    status, text = curl(f"{BLOTATO}/v2/schedules", kopf=blotato_kopf(a))
    if status != 200:
        sys.exit(f"Blotato /v2/schedules: HTTP {status}")
    ziel = a.zeitpunkt.replace("Z", "")[:16]
    treffer = []
    for s in json.loads(text).get("items", []):
        if (s.get("scheduledAt") or "").replace("Z", "")[:16] != ziel:
            continue
        konto = (s.get("account") or {}).get("username")
        if a.profil and konto != KONTO.get(a.profil):
            continue
        inhalt = (s.get("draft") or {}).get("content") or {}
        treffer.append({
            "id": s.get("id"),
            "scheduledAt": s.get("scheduledAt"),
            "konto": konto,
            "caption_anfang": (inhalt.get("text") or "")[:120],
            "folien": len(inhalt.get("mediaUrls") or []),
        })
    print(json.dumps(treffer, ensure_ascii=False, indent=1))


def blotato_loeschen(a) -> None:
    status, text = curl(f"{BLOTATO}/v2/schedules/{a.id}", "DELETE", kopf=blotato_kopf(a))
    if status not in (200, 202, 204):
        sys.exit(f"Blotato löschen: HTTP {status} {text[:200]}")
    print(json.dumps({"geloescht": a.id}))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="befehl", required=True)
    sub.add_parser("lesen").set_defaults(f=lesen)
    b = sub.add_parser("bestaetigen")
    b.add_argument("--bis", required=True)
    b.set_defaults(f=bestaetigen)
    s = sub.add_parser("senden")
    s.add_argument("--datei", required=True)
    s.set_defaults(f=senden)
    q = sub.add_parser("blotato-suchen")
    q.add_argument("--zeitpunkt", required=True)
    q.add_argument("--profil", choices=list(KONTO))
    q.add_argument("--proxy", action="store_true")
    q.set_defaults(f=blotato_suchen)
    d = sub.add_parser("blotato-loeschen")
    d.add_argument("--id", required=True)
    d.add_argument("--proxy", action="store_true")
    d.set_defaults(f=blotato_loeschen)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
