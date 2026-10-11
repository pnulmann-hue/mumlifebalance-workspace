# -*- coding: utf-8 -*-
"""Setzt den MBA-Pitch in Mail 801 („Versand Aufzeichnung", geht 16:00 raus).

    python scripts/ki-kurs/mba-block-einfuegen.py          # trocken
    python scripts/ki-kurs/mba-block-einfuegen.py --los    # schreibt

Der Block steht **zwischen** dem Knopf „Alles zum Kurs" und dem Gruss — erst
das kleine Angebot, dann das grosse. So war auch der Aufbau im Webinar
(Kurs-Preis, dann die Einordnung zur Academy).

Alle Zahlen sind aus ThriveCart geprüft (08.10.2026, Produkt 48):
  Einmalzahlung 997 · 6 Raten zu 166.20 · 3 Raten zu 332.35
Regulärpreis 1347 steht so im Masterclass-Deck.

🚨 Die Frist ist der einzige Wert, der nicht aus einer Quelle kommt, sondern
   aus dem, was Patricia im Webinar gesagt hat („in den nächsten 24 Stunden").
   Sie steht als FRIST ganz oben und ist in einer Minute geändert.
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
KAMPAGNE = 801

# 🔁 Hier die Frist setzen, falls im Webinar etwas anderes gesagt wurde.
FRIST = "Dieses Fenster ist bis morgen Abend offen — Freitag, 21 Uhr"

KASSE = "https://mumlifebalance.thrivecart.com/mba-webinar/"
MARKE = "#12828c"   # Petrol
ORANGE = "#dc822e"
CREME = "#f1ecdd"
TINTE = "#0c1c30"
GRAU = "#5f5748"

# Der Anker: direkt nach dem Kurs-Knopf, vor dem Gruss.
ANKER = ('>Alles zum Kurs</a></td></tr></table>')

BLOCK = (
    '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;'
    'border-spacing:0px;margin:30px 0 0 0" role="none"><tr>'
    '<td style="background-color:%(creme)s;border-radius:14px;padding:26px 26px;" align="left">'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Georgia, serif;'
    'line-height:1.35;margin:0 0 12px 0;font-size:21px;font-weight:bold;color:%(tinte)s">'
    'Und wenn du gleich alles willst</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.7;margin:0 0 14px 0;font-size:16px;color:%(grau)s">'
    'Im Webinar habe ich dir am Schluss die Mum Business Academy gezeigt. Darin sind '
    'alle vier Kurse drin, der KI-Kurs ab dem 1. November inklusive, dazu ein ganzes '
    'Jahr Begleitung in der Gruppe und zweimal im Monat ein Call.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.7;margin:0 0 6px 0;font-size:17px;font-weight:bold;color:%(tinte)s">'
    'Weil du dabei warst, bekommst du sie f&uuml;r 997 statt 1347.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.7;margin:0 0 14px 0;font-size:16px;color:%(grau)s">'
    'Oder in sechs Raten zu 166.20 &mdash; derselbe Betrag, nur nicht alles auf einmal.</p>'

    '<p style="Margin:0;mso-line-height-rule:exactly;font-family:Arial, sans-serif;'
    'line-height:1.6;margin:0 0 18px 0;font-size:14px;font-weight:bold;'
    'text-transform:uppercase;letter-spacing:1px;color:#b56a24">%(frist)s</p>'

    '<a href="%(kasse)s" style="mso-line-height-rule:exactly;text-decoration:none;'
    'display:inline-block;background-color:%(orange)s;color:#ffffff;'
    'font-family:Arial, sans-serif;font-size:17px;font-weight:bold;'
    'padding:15px 34px;border-radius:30px" target="_blank">'
    'Zur Academy f&uuml;r 997</a>'

    '</td></tr></table>'
)
for _schl, _wert in (("%(creme)s", CREME), ("%(tinte)s", TINTE), ("%(grau)s", GRAU),
                     ("%(orange)s", ORANGE), ("%(frist)s", FRIST), ("%(kasse)s", KASSE)):
    BLOCK = BLOCK.replace(_schl, _wert)

TEXT_BLOCK = (
    "\n\nUND WENN DU GLEICH ALLES WILLST\n\n"
    "Im Webinar habe ich dir am Schluss die Mum Business Academy gezeigt. Darin sind "
    "alle vier Kurse drin, der KI-Kurs ab dem 1. November inklusive, dazu ein ganzes "
    "Jahr Begleitung in der Gruppe und zweimal im Monat ein Call.\n\n"
    "Weil du dabei warst, bekommst du sie für 997 statt 1347. "
    "Oder in sechs Raten zu 166.20 — derselbe Betrag, nur nicht alles auf einmal.\n\n"
    "%s\n\n%s\n" % (FRIST, KASSE))


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

    ms = ac("campaigns/%s/campaignMessages" % KAMPAGNE).get("campaignMessages", [])
    mid = ms[0]["message"]
    msg = ac("messages/%s" % mid)["message"]
    h, txt = msg.get("html") or "", msg.get("text") or ""

    # --- Gegenproben VOR dem Bauen ---------------------------------------
    if "mba-webinar" in h:
        print("🚨 Der MBA-Block steht schon drin — nichts zu tun."); sys.exit(0)
    n = h.count(ANKER)
    assert n == 1, "Anker kommt %dx vor (erwartet 1): %r" % (n, ANKER)

    neu_h = h.replace(ANKER, ANKER + BLOCK)
    neu_t = txt
    gruss = "Danke, dass du dabei warst"
    if gruss in neu_t:
        neu_t = neu_t.replace(gruss, TEXT_BLOCK.strip() + "\n\n" + gruss, 1)
    else:
        neu_t = neu_t + TEXT_BLOCK

    print("Mail %s · messageId %s" % (KAMPAGNE, mid))
    print("  HTML : %d → %d Zeichen (+%d)" % (len(h), len(neu_h), len(neu_h) - len(h)))
    print("  Text : %d → %d Zeichen" % (len(txt), len(neu_t)))
    print("  Frist: %s" % FRIST)
    print("  Kasse: %s" % KASSE)

    # Blackliste
    sicht = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", BLOCK))
    probleme = []
    for mus, name in [(r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "Nicht-X-sondern-Y"),
                      (r"[Ss]tell(e)? dir[^.!?]{0,40}vor", "Stell dir vor"),
                      (r"\bnie wieder\b", "nie wieder"), (r"ß", "deutsches Eszett"),
                      (r"\b\w*(ae|oe|ue)\w*\b", "Umlaut-Umschrift")]:
        tr = re.findall(mus, sicht)
        if name == "Umlaut-Umschrift":
            tr = [x for x in re.findall(r"\b\w*(?:ae|oe|ue)\w*\b", sicht)
                  if not x.lower().startswith(("auch", "auf", "aus", "neue", "genau"))]
        if tr:
            probleme.append("%s %s" % (name, sorted(set(map(str, tr)))[:3]))
    print("  Sprachprüfung: %s" % ("sauber ✓" if not probleme else " | ".join(probleme)))
    if probleme:
        sys.exit(1)

    if not args.los:
        print("\nTrockenlauf. Mit --los wird geschrieben.")
        return

    ac("messages/%s" % mid, "PUT", {"message": {"html": neu_h, "text": neu_t}})
    nach = ac("messages/%s" % mid)["message"].get("html") or ""
    ok = "mba-webinar" in nach and "997 statt 1347" in nach
    print("\n  gespeichert · Gegenprobe: %s" % ("sauber ✓" if ok else "🚨 WEICHT AB"))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
