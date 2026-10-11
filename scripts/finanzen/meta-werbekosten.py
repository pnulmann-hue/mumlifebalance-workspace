"""Holt die Werbeausgaben aus dem Meta-Werbekonto — Monat fuer Monat.

🚨 **Diese Kosten kommen nie per Mail.** Anthropic, Railway und Supabase
schicken eine Quittung ins Postfach; Meta rechnet ueber das Werbekonto ab. Wer
die Buchhaltung aus dem Postfach rekonstruiert, uebersieht sie deshalb
vollstaendig — und Werbung ist der Posten, der am ehesten weh tut, wenn er
fehlt.

🚨 **Der Beleg ist nicht diese Datei.** Was hier herauskommt, ist die
*Auskunft* des Werbekontos. Die Rechnung selbst steht im Abrechnungsbereich des
Business Managers und muss dort als PDF geholt werden — die Schnittstelle gibt
sie nicht heraus. Das Skript sagt am Ende, wo sie liegt.

🚨 **Kein Schluessel im Code.** Der Zugang kommt aus `scripts/meta-ads/.env`;
fehlt er, bricht das Skript ab, statt mit einem eingebauten Wert weiterzulaufen.

    python scripts/finanzen/meta-werbekosten.py [--ab 2026-01-01]
"""

import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ENV = ROOT / "scripts" / "meta-ads" / ".env"
VERSION = "v21.0"
RECHNUNGEN = "https://business.facebook.com/billing_hub/accounts"


def zugang():
    if not ENV.exists():
        sys.exit("Keine .env bei scripts/meta-ads/ — ohne Zugang kein Abruf.")
    env = {}
    for zeile in ENV.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.strip().startswith("#"):
            k, v = zeile.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    if not env.get("META_ACCESS_TOKEN") or not env.get("META_AD_ACCOUNT_ID"):
        sys.exit("META_ACCESS_TOKEN oder META_AD_ACCOUNT_ID fehlt in der .env.")
    konto = env["META_AD_ACCOUNT_ID"]
    if not konto.startswith("act_"):
        konto = "act_" + konto
    return env["META_ACCESS_TOKEN"], konto, env.get("META_CURRENCY", "CHF")


def hole(token, konto, ab, bis):
    """Ausgaben je Monat. time_increment=monthly macht die Gruppierung."""
    p = urllib.parse.urlencode({
        "access_token": token,
        "time_range": json.dumps({"since": ab, "until": bis}),
        "time_increment": "monthly",
        "fields": "spend,impressions,clicks,date_start,date_stop",
        "level": "account",
        "limit": 200,
    })
    url = "https://graph.facebook.com/%s/%s/insights?%s" % (VERSION, konto, p)
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            return json.loads(r.read().decode("utf-8")).get("data") or []
    except urllib.error.HTTPError as e:
        leib = e.read().decode("utf-8", "replace")[:400]
        sys.exit("Meta antwortet %s:\n  %s" % (e.code, leib))


def main():
    ab = "2026-01-01"
    if "--ab" in sys.argv:
        ab = sys.argv[sys.argv.index("--ab") + 1]
    bis = date.today().isoformat()

    token, konto, whr = zugang()
    zeilen = hole(token, konto, ab, bis)

    monate = defaultdict(lambda: {"spend": 0.0, "impressions": 0, "clicks": 0})
    for z in zeilen:
        m = (z.get("date_start") or "")[:7]
        if not m:
            continue
        monate[m]["spend"] += float(z.get("spend") or 0)
        monate[m]["impressions"] += int(z.get("impressions") or 0)
        monate[m]["clicks"] += int(z.get("clicks") or 0)

    liste = [{"monat": m,
              "betrag": round(v["spend"], 2),
              "waehrung": whr,
              "impressionen": v["impressions"],
              "klicks": v["clicks"]}
             for m, v in sorted(monate.items())]

    ziel = ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / "meta-werbekosten.json").write_text(json.dumps({
        "monate": liste,
        "konto": konto,
        "waehrung": whr,
        "summe": round(sum(e["betrag"] for e in liste), 2),
        "stand": bis,
        "beleg_hinweis": ("Die Rechnungen als PDF liegen im Business Manager "
                          "unter Abrechnung: %s — die Schnittstelle gibt sie "
                          "nicht heraus." % RECHNUNGEN),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if not liste:
        print("  Keine Werbeausgaben im Zeitraum %s bis %s." % (ab, bis))
        return
    print("  %-9s %10s %12s %8s" % ("Monat", whr, "Impress.", "Klicks"))
    for e in liste:
        print("  %-9s %10.2f %12s %8d"
              % (e["monat"], e["betrag"],
                 format(e["impressionen"], ",d").replace(",", "'"), e["klicks"]))
    print("  %-9s %10.2f" % ("Summe", sum(e["betrag"] for e in liste)))
    print()
    print("  🚨 Das sind die Zahlen, nicht die Belege.")
    print("     Die Rechnungs-PDFs: %s" % RECHNUNGEN)
    print("     Danach nach context/finanzen/2026/belege/ legen als")
    print("     JJJJ-MM-TT_meta_Rechnung-<nummer>.pdf")


if __name__ == "__main__":
    main()
