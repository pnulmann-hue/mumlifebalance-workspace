# -*- coding: utf-8 -*-
"""Schickt Bilder und Text ueber den Cockpit-Bot auf Patricias Handy.

Anlass: Patricia am 08.10.2026 — *„kannst du mir das per telegram schicken
inkl. der caption?"*. Fertige Karussell-Folien liegen im Workspace, gepostet
wird aber vom Handy aus. Bisher gab es dafuer kein Werkzeug ausserhalb der
Scheduled Tasks.

    python scripts/telegram/senden.py --bilder outputs/.../renders/*.png \\
        --text-datei caption.txt --titel "Pin · 0€ Stimm-Check"

🚨 **Als Foto, nicht als Datei.** Telegram rechnet Fotos herunter, aber sie
   landen mit einem Tipp in der Galerie — und genau von dort laedt Instagram
   sie hoch. Als Datei waere die Qualitaet besser, die Datei landet aber in
   den Downloads und muss von Hand gesucht werden. Instagram rechnet beim
   Hochladen ohnehin neu.

🚨 **Caption als eigene Nachricht.** Die Bildunterschrift in einem Album ist
   auf 1024 Zeichen begrenzt, Patricias Captions sind laenger. Als eigene
   Nachricht laesst sie sich ausserdem am Handy mit einem Tipp kopieren.

🚨 **Hoechstens 10 Bilder je Album** — Telegram nimmt nicht mehr an. Mehr
   Bilder werden auf mehrere Alben verteilt, in der richtigen Reihenfolge.

Zugang aus der `.env` im Wurzelverzeichnis: `TELEGRAM_COCKPIT_BOT_TOKEN`
und `TELEGRAM_CHAT_ID`. Kein Schluessel im Code.
"""
import argparse
import json
import mimetypes
import pathlib
import sys
import urllib.request
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[2]


def env():
    datei = ROOT / ".env"
    if not datei.exists():
        sys.exit("\U0001f6a8 .env im Wurzelverzeichnis fehlt")
    werte = {}
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.strip().startswith("#"):
            k, _, v = zeile.partition("=")
            werte[k.strip()] = v.strip().strip('"').strip("'")
    token = werte.get("TELEGRAM_COCKPIT_BOT_TOKEN")
    chat = werte.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        sys.exit("\U0001f6a8 TELEGRAM_COCKPIT_BOT_TOKEN oder "
                 "TELEGRAM_CHAT_ID fehlt in der .env")
    return token, chat


def post(token, methode, felder, dateien=None):
    """multipart/form-data von Hand — kein zusaetzliches Paket noetig."""
    grenze = "----" + uuid.uuid4().hex
    teile = []
    for k, v in felder.items():
        teile.append(("--" + grenze).encode())
        teile.append(('Content-Disposition: form-data; name="%s"' % k).encode())
        teile.append(b"")
        teile.append(str(v).encode("utf-8"))
    for name, pfad in (dateien or []):
        p = pathlib.Path(pfad)
        typ = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        teile.append(("--" + grenze).encode())
        teile.append(('Content-Disposition: form-data; name="%s"; filename="%s"'
                      % (name, p.name)).encode())
        teile.append(("Content-Type: " + typ).encode())
        teile.append(b"")
        teile.append(p.read_bytes())
    teile.append(("--" + grenze + "--").encode())
    teile.append(b"")
    koerper = b"\r\n".join(teile)

    req = urllib.request.Request(
        "https://api.telegram.org/bot%s/%s" % (token, methode),
        data=koerper,
        headers={"Content-Type": "multipart/form-data; boundary=" + grenze})
    with urllib.request.urlopen(req, timeout=120) as r:
        antwort = json.loads(r.read().decode("utf-8"))
    if not antwort.get("ok"):
        sys.exit("\U0001f6a8 Telegram: %s" % antwort)
    return antwort


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bilder", nargs="*", default=[])
    p.add_argument("--text")
    p.add_argument("--text-datei")
    p.add_argument("--titel", help="kurze Zeile vor den Bildern")
    a = p.parse_args()

    token, chat = env()

    text = a.text
    if a.text_datei:
        text = pathlib.Path(a.text_datei).read_text(encoding="utf-8")
    if not a.bilder and not text:
        sys.exit("\U0001f6a8 nichts zu senden")

    if a.titel:
        post(token, "sendMessage", {"chat_id": chat, "text": a.titel})
        print("Titel gesendet")

    bilder = [pathlib.Path(b) for b in a.bilder]
    fehlt = [str(b) for b in bilder if not b.exists()]
    if fehlt:
        sys.exit("\U0001f6a8 nicht gefunden: %s" % ", ".join(fehlt))

    for i in range(0, len(bilder), 10):
        teil = bilder[i:i + 10]
        medien = [{"type": "photo", "media": "attach://f%d" % n}
                  for n in range(len(teil))]
        dateien = [("f%d" % n, b) for n, b in enumerate(teil)]
        post(token, "sendMediaGroup",
             {"chat_id": chat, "media": json.dumps(medien)}, dateien)
        print("Album %d: %d Bilder gesendet" % (i // 10 + 1, len(teil)))

    if text:
        # 4096 Zeichen je Nachricht; laengere Texte werden geteilt.
        rest = text
        while rest:
            post(token, "sendMessage", {"chat_id": chat, "text": rest[:4000]})
            rest = rest[4000:]
        print("Text gesendet (%d Zeichen)" % len(text))


if __name__ == "__main__":
    main()
