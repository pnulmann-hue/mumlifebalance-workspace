"""Baut den Steuer-Block fuers Cockpit — je Jahr eine Bilanz plus Postenliste.

Der Knopf im Cockpit gibt eine CSV heraus. Das vollstaendige Paket **mit den
Belegdateien** baut `scripts/finanzen/steuer-export.py` lokal.

🚨 **Das Cockpit hat die Belege nicht und kann sie nicht bekommen.** Ein
Artifact kommt nicht an den Dateiordner; die PDFs liegen in
`context/finanzen/JJJJ/belege/`. Der Knopf liefert deshalb die **Zahlen** und
nennt je Posten den Dateinamen — er behauptet nie, die Datei mitzuliefern. Ein
Knopf, der „Steuer-Export" heisst und nur die halbe Sache abgibt, ohne das zu
sagen, ist schlimmer als keiner.

    python scripts/cockpit/steuer-fuer-cockpit.py [zielordner]
    # danach: Artifact write_db -> Sammlung "daten", Dokument "steuer"
"""

import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]


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

    umsatz = lade(ziel, "umsatz.json")
    kosten = lade(ziel, "kosten.json")
    if not umsatz or not kosten:
        sys.exit("umsatz.json oder kosten.json fehlt.")

    jahre = defaultdict(lambda: {
        "einnahmen": 0.0, "kaeufe": 0, "chf": 0.0, "usd": 0.0,
        "posten": 0, "mit_beleg": 0, "nach_art": defaultdict(float),
    })

    for t in umsatz.get("tage") or []:
        j = (t.get("datum") or "")[:4]
        if not j:
            continue
        jahre[j]["einnahmen"] += t.get("umsatz") or 0
        jahre[j]["kaeufe"] += t.get("kaeufe") or 0

    zeilen = []
    for p in kosten.get("posten") or []:
        j = (p.get("monat") or "")[:4]
        if not j:
            continue
        e = jahre[j]
        e["posten"] += 1
        if p.get("belege"):
            e["mit_beleg"] += 1
        if p["waehrung"] == "CHF":
            e["chf"] += p["betrag"]
            e["nach_art"][p["art"]] += p["betrag"]
        elif p["waehrung"] == "USD":
            e["usd"] += p["betrag"]
        zeilen.append({
            "jahr": j,
            "datum": p.get("datum") or (p["monat"] + "-01"),
            "was": p["was"],
            "art": p["art"],
            "betrag": round(p["betrag"], 2),
            "waehrung": p["waehrung"],
            "beleg": " | ".join(p.get("belege") or []),
            "quelle": p.get("quelle") or "",
        })

    liste = []
    for j in sorted(jahre, reverse=True):
        e = jahre[j]
        ohne = e["posten"] - e["mit_beleg"]
        liste.append({
            "jahr": j,
            "einnahmen": round(e["einnahmen"], 2),
            "kaeufe": e["kaeufe"],
            "kosten_chf": round(e["chf"], 2),
            "kosten_usd": round(e["usd"], 2),
            "posten": e["posten"],
            "mit_beleg": e["mit_beleg"],
            "ohne_beleg": ohne,
            "nach_art": {k: round(v, 2) for k, v in sorted(e["nach_art"].items())},
            # 🚨 Gewinn nur, wenn jeder Posten belegt ist UND nichts in USD
            # offen steht. Sonst waere es eine Zahl, die aussieht wie gerechnet.
            "gewinn": (round(e["einnahmen"] - e["chf"], 2)
                       if e["posten"] and not ohne and not e["usd"] else None),
            # ⚠ Der Grund nennt NUR, was die Spalte «Belege» daneben nicht
            # schon sagt. Sonst steht dieselbe Auskunft zweimal nebeneinander,
            # und man liest beide nicht mehr.
            "gewinn_warum_nicht": (
                "" if (e["posten"] and not ohne and not e["usd"]) else
                ("USD noch nicht in Franken" if e["usd"] else
                 ("keine Kosten erfasst" if not e["posten"] else ""))),
        })

    daten = {
        "jahre": liste,
        "zeilen": sorted(zeilen, key=lambda z: z["datum"], reverse=True),
        "stand": date.today().isoformat(),
        "belegordner": "context/finanzen/2026/belege/",
        "vollexport": "python scripts/finanzen/steuer-export.py 2026 --zip",
        "hinweis": ("Der Knopf gibt die Zahlen als CSV heraus. Die Belegdateien "
                    "liegen im Workspace und kommen über den Vollexport dazu — "
                    "ein Artifact kann nicht an den Dateiordner."),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "steuer.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %-6s %12s %12s %12s %12s" %
          ("Jahr", "Einnahmen", "Kosten CHF", "Kosten USD", "ohne Beleg"))
    for e in liste:
        print("  %-6s %12.2f %12.2f %12.2f %9d/%d"
              % (e["jahr"], e["einnahmen"], e["kosten_chf"], e["kosten_usd"],
                 e["ohne_beleg"], e["posten"]))
    print()
    print("  %d Kostenzeilen · %.0f KB"
          % (len(zeilen), (ziel / "steuer.json").stat().st_size / 1024))
    print("\nAbgelegt in: %s" % (ziel / "steuer.json"))


if __name__ == "__main__":
    main()
