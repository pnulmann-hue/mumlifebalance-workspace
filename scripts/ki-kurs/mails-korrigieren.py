# -*- coding: utf-8 -*-
"""Korrigiert die Launch-Mails in ActiveCampaign.

    python scripts/ki-kurs/mails-korrigieren.py          # trocken, zeigt nur
    python scripts/ki-kurs/mails-korrigieren.py --los    # schreibt

Zwei Funde vom 08.10.2026, beide vor dem 16:00-Versand von Mail 801:

  1 `#aufzeichnung-folgt` — ein Platzhalter-Anker. Wer darauf klickt, bleibt
    stehen. Betroffen: 801 (Automation 84) und 792 (Automation 83, b-Zweig).

  2 „ab dem 2. November" — die Verkaufsseite, die Replay-Seite und der
    Checkout sagen alle **1. November**. Nur die Mail sagt etwas anderes.

🚨 Jede Ersetzung prüft vorher, dass der Suchtext wirklich vorkommt, und
   danach, dass er weg ist. Ein `replace`, das ins Leere läuft, meldet sonst
   Erfolg und ändert nichts.

🚨 Der Zugang kommt aus der .env, nie aus dem Code. Der MCP-Server antwortet
   hier mit 403, weil er die Zugangsdaten nur beim Start liest.
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

REPLAY = "https://mumlifebalance.ch/ki-masterclass-replay/"

# (Kampagnen-ID, Beschreibung)
MAILS = [(801, "Versand Aufzeichnung · Automation 84"),
         (802, "Pitch KI Kurs · Automation 84"),
         (805, "letzte Erinnerung Bonuscall · Automation 84"),
         (807, "Letzte Chance Frühbucher · Automation 84"),
         (809, "Pitch KI Kurs · Automation 84"),
         (811, "Pitch KI Kurs 2 · Automation 84"),
         (813, "Erinnerung Pitch · Automation 84"),
         (815, "Letzter Pitch · Automation 84"),
         (792, "1. Mail Stimmcheck nach Masterclass · Automation 83"),
         (794, "2. Mail Stimmcheck nach Webinar · Automation 83"),
         (796, "3. Mail Stimmcheck nach Webinar · Automation 83"),
         (790, "Auslieferung Stimm-Check nach Webinar · Automation 83")]

ERSETZUNGEN = [
    ("#aufzeichnung-folgt", REPLAY, "toter Anker → Replay-Seite"),
    ("ab dem 2. November", "ab dem 1. November", "Startdatum 2. → 1. November"),
    ("am 2. November", "am 1. November", "Startdatum 2. → 1. November"),
]


def zugang():
    env = {}
    for zeile in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", zeile)
        if m:
            env[m.group(1)] = m.group(2).strip("\"'")
    assert env.get("AC_API_URL") and env.get("AC_API_KEY"), "AC-Zugang fehlt in der .env"
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


U, K = zugang()


def seite_lebt(url):
    """🚨 Nie auf eine Seite verlinken, die es noch nicht gibt. Die
    Replay-Seite entsteht als Entwurf (NinjaFirewall blockt `publish`) und
    antwortet bis zum Veröffentlichen mit 404."""
    try:
        r = urllib.request.Request(url, method="HEAD",
                                   headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(r, timeout=15) as a:
            return a.status == 200
    except Exception:
        return False


def ac(pfad, methode="GET", daten=None):
    r = urllib.request.Request(
        U + "/api/3/" + pfad, method=methode,
        headers={"Api-Token": K, "Content-Type": "application/json"},
        data=json.dumps(daten).encode("utf-8") if daten else None)
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        print("   HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:220]))
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--los", action="store_true")
    args = ap.parse_args()

    lebt = seite_lebt(REPLAY)
    print("Replay-Seite %s: %s\n" % (REPLAY, "erreichbar ✓" if lebt
          else "🚨 noch 404 — Link-Ersetzung wird übersprungen"))
    ersetzungen = ERSETZUNGEN if lebt else [e for e in ERSETZUNGEN if not e[1].startswith("http")]

    gesamt = 0
    for cid, was in MAILS:
        print("=" * 70)
        # 🚨 Immer den AC-Titel nennen, die Nummer hoechstens in Klammern —
        #    eine Nummer sagt niemandem, welche Mail gemeint ist.
        try:
            titel = ac("campaigns/%s" % cid)["campaign"].get("name") or was
        except Exception:
            titel = was
        print("%s  (%s · %s)" % (titel, cid, was))
        ms = ac("campaigns/%s/campaignMessages" % cid).get("campaignMessages", [])
        if not ms:
            print("   keine Nachricht gefunden"); continue
        mid = ms[0]["message"]
        msg = ac("messages/%s" % mid)["message"]
        html_alt = msg.get("html") or ""
        text_alt = msg.get("text") or ""

        html_neu, text_neu, getan = html_alt, text_alt, []
        for alt, neu, name in ersetzungen:
            n_h, n_t = html_neu.count(alt), text_neu.count(alt)
            if not (n_h or n_t):
                continue
            html_neu = html_neu.replace(alt, neu)
            text_neu = text_neu.replace(alt, neu)
            getan.append("%s (%dx HTML, %dx Text)" % (name, n_h, n_t))

        if not getan:
            print("   nichts zu ändern"); continue
        for g in getan:
            print("   ✓ %s" % g)
        gesamt += len(getan)

        # Gegenproben VOR dem Schreiben
        for alt, _, name in ersetzungen:
            assert alt not in html_neu, "steht noch drin: %s" % alt

        if not args.los:
            continue

        ac("messages/%s" % mid, "PUT", {"message": {"html": html_neu, "text": text_neu}})
        # und zurücklesen
        nach = ac("messages/%s" % mid)["message"]
        h2 = nach.get("html") or ""
        ok = all(alt not in h2 for alt, _, _ in ersetzungen)
        print("   gespeichert · Gegenprobe: %s" % ("sauber ✓" if ok else "🚨 WEICHT AB"))
        if not ok:
            sys.exit(1)

    print()
    print("%d Änderung(en)%s" % (gesamt, "" if args.los else " — Trockenlauf, mit --los schreiben"))


if __name__ == "__main__":
    main()
