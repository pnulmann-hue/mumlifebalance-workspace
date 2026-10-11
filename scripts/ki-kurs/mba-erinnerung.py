# -*- coding: utf-8 -*-
"""Setzt die kurze MBA-Erinnerung in „Pich KI Kurs".

    python scripts/ki-kurs/mba-erinnerung.py          # trocken
    python scripts/ki-kurs/mba-erinnerung.py --los    # schreibt

Warum genau diese eine Mail: Sie geht **einen Tag nach „Versand Aufzeichnung"**
raus, also Freitag gegen 16:00 — und die Academy-Frist endet Freitag 21 Uhr.
Fünf Stunden davor ist die letzte Gelegenheit, daran zu erinnern.

Alles danach („letzte erinnerung bonuscall" am Samstag und später) liegt hinter
der Frist. Dort gehört die Academy **nicht** hinein: Nach Freitag kostet sie
wieder 1347, und ein Angebot zu wiederholen, das es nicht mehr gibt, macht
jede weitere Frist unglaubwürdig.

🚨 Kurz halten. Das ist eine Erinnerung, kein zweiter Pitch — der ganze Pitch
   steht in „Versand Aufzeichnung". Wer ihn gelesen hat, braucht hier nur noch
   den Stichtag.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
KAMPAGNE = 802          # „Pich KI Kurs"
KASSE = "https://mumlifebalance.thrivecart.com/mba-webinar/"

# 🔁 muss zur Frist in mba-block-einfuegen.py passen
FRIST_TEXT = "noch bis heute Abend, 21 Uhr"

# 🚨 Im HTML steht der Gruss mit einem <br> dazwischen: „Herzlich,<br>Patricia".
#    Der Anker muss die HTML-Schreibweise treffen, nicht den sichtbaren Text —
#    daran ist der erste Versuch gescheitert.
ANKER = "Herzlich,<br>Patricia</p>"
ANKER_TEXT = "Herzlich,"

BLOCK = (
    '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;'
    'border-spacing:0px;margin:4px 0 24px 0" role="none"><tr>'
    '<td style="background-color:#f1ecdd;border-radius:14px;padding:22px 24px;" align="left">'
    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.7;margin:0 0 12px 0;font-size:16px;color:#5f5748">'
    'Und falls du mit dem Gedanken spielst, gleich alles zu nehmen: Die '
    '<strong>Mum Business Academy</strong> gibt es f&uuml;r dich noch '
    '<strong>f&uuml;r 997 statt 1347</strong> &mdash; alle vier Kurse, ein Jahr '
    'Begleitung, zweimal im Monat ein Call. ' + FRIST_TEXT.capitalize() +
    ', danach gilt wieder der normale Preis.</p>'
    '<a href="' + KASSE + '" style="mso-line-height-rule:exactly;text-decoration:none;'
    'display:inline-block;background-color:#dc822e;color:#ffffff;'
    'font-family:Arial, sans-serif;font-size:16px;font-weight:bold;'
    'padding:13px 30px;border-radius:30px" target="_blank">Zur Academy</a>'
    '</td></tr></table>'
)

TEXT_BLOCK = (
    "\n\nUnd falls du mit dem Gedanken spielst, gleich alles zu nehmen: Die Mum "
    "Business Academy gibt es für dich noch für 997 statt 1347 — alle vier Kurse, "
    "ein Jahr Begleitung, zweimal im Monat ein Call. " + FRIST_TEXT.capitalize() +
    ", danach gilt wieder der normale Preis.\n\n" + KASSE + "\n\n")


def zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", z)
        if m:
            env[m.group(1)] = m.group(2).strip("\"'")
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


U, K = zugang()


def ac(pfad, methode="GET", daten=None):
    r = urllib.request.Request(
        U + "/api/3/" + pfad, method=methode,
        headers={"Api-Token": K, "Content-Type": "application/json"},
        data=json.dumps(daten).encode("utf-8") if daten else None)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("   HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:200]))
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--los", action="store_true")
    args = ap.parse_args()

    name = ac("campaigns/%s" % KAMPAGNE)["campaign"].get("name")
    ms = ac("campaigns/%s/campaignMessages" % KAMPAGNE).get("campaignMessages", [])
    mid = ms[0]["message"]
    msg = ac("messages/%s" % mid)["message"]
    h, txt = msg.get("html") or "", msg.get("text") or ""

    print("%s  (%s)" % (name, KAMPAGNE))

    if "mba-webinar" in h:
        print("   🚨 steht schon drin — nichts zu tun"); return
    n = h.count(ANKER)
    assert n >= 1, "Anker %r nicht gefunden" % ANKER
    if n > 1:
        print("   ⚠ Anker kommt %dx vor — es wird der erste genommen" % n)

    neu_h = h.replace(ANKER, BLOCK + ANKER, 1)
    neu_t = (txt.replace(ANKER_TEXT, TEXT_BLOCK + ANKER_TEXT, 1)
             if ANKER_TEXT in txt else txt + TEXT_BLOCK)

    print("   HTML : %d → %d (+%d)" % (len(h), len(neu_h), len(neu_h) - len(h)))
    print("   Frist: %s" % FRIST_TEXT)

    sicht = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", BLOCK))
    schlecht = []
    for mus, bez in [(r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "Nicht-X-sondern-Y"),
                     (r"[Ss]tell(e)? dir[^.!?]{0,40}vor", "Stell dir vor"),
                     (r"\bnie wieder\b", "nie wieder"), (r"ß", "deutsches Eszett")]:
        if re.search(mus, sicht):
            schlecht.append(bez)
    print("   Sprachprüfung: %s" % ("sauber ✓" if not schlecht else " | ".join(schlecht)))
    if schlecht:
        sys.exit(1)

    if not args.los:
        print("\nTrockenlauf. Mit --los wird geschrieben.")
        return

    ac("messages/%s" % mid, "PUT", {"message": {"html": neu_h, "text": neu_t}})
    nach = ac("messages/%s" % mid)["message"].get("html") or ""
    ok = "mba-webinar" in nach and "997 statt 1347" in nach
    print("\n   gespeichert · Gegenprobe: %s" % ("sauber ✓" if ok else "🚨 WEICHT AB"))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
