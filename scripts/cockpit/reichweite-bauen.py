"""Rechnet das Reichweiten-Tracking — Ersatz fuer die Notion-Tabelle.

Die Notion-Tabelle hatte elf Spalten, die alle von Hand gefuellt werden
mussten. **Sechs davon kommen aus Schnittstellen**, die Patricia ohnehin
bezahlt:

| Spalte | woher |
|---|---|
| Instagram Follower | Meta Graph API |
| Instagram erreichte Konten | Meta Graph API |
| Instagram Interaktionen | Meta Graph API |
| Newsletter Abonnenten | ActiveCampaign |
| Gesendete Newsletter | ActiveCampaign |
| Oeffnungsrate | ActiveCampaign |

Uebrig bleiben Website-Besucher (kein Zugang) und die beiden doTERRA-Zahlen
(kommen aus dem Back Office, das keine offene Schnittstelle hat).

    python scripts/cockpit/reichweite-bauen.py

🚨 **Der MCP-Server fuer ActiveCampaign liefert 403.** Er liest seine
Zugangsdaten nur beim Start, und der Schluessel wurde am 13.09.2026 gewechselt.
Dieses Skript liest die `.env` selbst und kommt deshalb durch — wer sich auf
die MCP-Tools verlaesst, haelt den Zugang faelschlich fuer kaputt.

🚨 **Automations-Mails sind keine Newsletter.** Von 351 Kampagnen gehen die
meisten an **eine** Empfaengerin: das sind die Mails aus den Automationen, die
bei jedem Eintritt neu gezaehlt werden. Wer sie mitzaehlt, meldet 30 „Newsletter"
im Monat und eine Oeffnungsrate, die nichts mit dem Verteiler zu tun hat.
Getrennt wird an der Empfaengerzahl.

🚨 **Oeffnungsrate auf die tatsaechlich Zugestellten.** `uniqueopens` geteilt
durch `send_amt` — nicht durch die Listengroesse. Sonst sinkt die Rate jedes
Mal, wenn die Liste waechst, ohne dass sich an den Mails etwas geaendert haette.
"""

import json
import sys
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ENV = ROOT / "04-projects" / "activecampaign-mcp" / ".env"

# Ab so vielen Empfaengerinnen gilt eine Kampagne als Newsletter und nicht als
# Automations-Mail. Siehe Kopf.
NEWSLETTER_AB = 5
SEITEN = 8          # 8 x 100 deckt die 351 Kampagnen ab


def zugang():
    if not ENV.exists():
        sys.exit("Keine .env bei 04-projects/activecampaign-mcp/")
    env = {}
    for zeile in ENV.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.strip().startswith("#"):
            k, v = zeile.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    if not env.get("AC_API_URL") or not env.get("AC_API_KEY"):
        sys.exit("AC_API_URL oder AC_API_KEY fehlt in der .env.")
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


def kampagnen(url, key):
    raus = []
    for i in range(SEITEN):
        pfad = ("%s/api/3/campaigns?limit=100&offset=%d&orders[sdate]=DESC"
                % (url, i * 100))
        req = urllib.request.Request(pfad, headers={"Api-Token": key})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print("  ⚠️ Abbruch nach %d Kampagnen (%s)" % (len(raus), str(e)[:80]))
            break
        c = d.get("campaigns") or []
        if not c:
            break
        raus.extend(c)
        if len(c) < 100:
            break
    return raus


def lade(ordner, name):
    p = ordner / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    url, key = zugang()
    roh = kampagnen(url, key)

    monate = defaultdict(lambda: {
        "newsletter": 0, "empfaenger": 0, "oeffnungen": 0, "klicks": 0,
        "automationsmails": 0,
    })
    for c in roh:
        tag = (c.get("sdate") or "")[:10]
        if not tag or (c.get("status") or "") in ("0", "1"):   # Entwurf/geplant
            continue
        m = monate[tag[:7]]
        anz = int(c.get("send_amt") or 0)
        if anz >= NEWSLETTER_AB:
            m["newsletter"] += 1
            m["empfaenger"] += anz
            m["oeffnungen"] += int(c.get("uniqueopens") or 0)
            m["klicks"] += int(c.get("linkclicks") or 0)
        else:
            m["automationsmails"] += 1

    # Instagram und Listen dazu
    gepostet = lade(ziel, "gepostet-voll.json") or lade(ziel, "gepostet.json")
    mailings = lade(ziel, "mailings.json")

    ig = defaultdict(lambda: {"beitraege": 0, "reichweite": 0, "interaktionen": 0})
    if gepostet:
        for b in gepostet.get("beitraege") or []:
            if b.get("alte_positionierung") or not b.get("datum"):
                continue
            e = ig[b["datum"][:7]]
            e["beitraege"] += 1
            e["reichweite"] += b.get("reach") or 0
            e["interaktionen"] += (b.get("likes") or 0) + (b.get("kommentare") or 0) \
                + (b.get("saved") or 0) + (b.get("shares") or 0)

    follower = {}
    if gepostet:
        for h, f in (gepostet.get("follower") or {}).items():
            for punkt in f.get("verlauf") or []:
                follower[(punkt.get("stand") or "")[:7]] = punkt.get("wert")

    abonnenten = 0
    if mailings:
        abonnenten = sum(int(l.get("kontakte") or 0)
                         for l in (mailings.get("listen") or []))

    heute = date.today()
    lauf = heute.strftime("%Y-%m")
    alle_m = sorted(set(list(monate.keys()) + list(ig.keys())), reverse=True)
    alle_m = [m for m in alle_m if m <= lauf][:14]

    liste = []
    for m in alle_m:
        a, i = monate.get(m, {}), ig.get(m, {})
        empf = a.get("empfaenger") or 0
        liste.append({
            "monat": m,
            "laeuft_noch": m == lauf,
            "newsletter": a.get("newsletter") or 0,
            "empfaenger": empf,
            "oeffnungen": a.get("oeffnungen") or 0,
            # 🚨 Auf die Zugestellten, nicht auf die Listengroesse — siehe Kopf.
            "oeffnungsrate": round((a.get("oeffnungen") or 0) / empf * 100, 1) if empf else None,
            "klicks": a.get("klicks") or 0,
            "automationsmails": a.get("automationsmails") or 0,
            "ig_beitraege": i.get("beitraege") or 0,
            "ig_reichweite": i.get("reichweite") or 0,
            "ig_interaktionen": i.get("interaktionen") or 0,
            "follower": follower.get(m),
        })

    daten = {
        "monate": liste,
        "stand": heute.isoformat(),
        "abonnenten_jetzt": abonnenten,
        "kampagnen_gelesen": len(roh),
        "von_hand": ["Website-Besucher", "doTERRA Botschafterinnen",
                     "doTERRA Neukunden"],
        "quellen": {"newsletter": "ActiveCampaign", "instagram": "Meta Graph API"},
        "hinweis": "Sechs der elf Notion-Spalten kommen jetzt von allein. "
                   "Website-Besucher und die doTERRA-Zahlen bleiben Handarbeit — "
                   "dafür gibt es keine Schnittstelle.",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "reichweite.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Kampagnen gelesen · %d Abonnentinnen auf allen Listen"
          % (len(roh), abonnenten))
    print()
    print("  %-9s %5s %7s %7s %8s %6s %9s"
          % ("Monat", "NL", "Empf.", "Öffn.", "Rate", "Beitr", "Reichw."))
    for e in liste[:10]:
        print("  %-9s %5d %7d %7d %7s %6d %9d"
              % (e["monat"], e["newsletter"], e["empfaenger"], e["oeffnungen"],
                 ("%.0f %%" % e["oeffnungsrate"]) if e["oeffnungsrate"] is not None else "—",
                 e["ig_beitraege"], e["ig_reichweite"]))
    print("\nAbgelegt in: %s" % (ziel / "reichweite.json"))


if __name__ == "__main__":
    main()
