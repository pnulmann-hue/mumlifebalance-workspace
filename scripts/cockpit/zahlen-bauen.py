"""Macht aus den Instagram-Zahlen ein Cockpit-Dokument.

`scripts/instagram-insights/holen.py` holt Reichweite, Speicherungen und
Geteilt-Zahlen ueber die Meta Graph API und schreibt sie nach
`outputs/instagram-insights/JJJJ-MM-TT.json`. Bis zum 24.09.2026 endete der Weg
genau dort — in einer Datei, die niemand aufmacht.

    python scripts/cockpit/zahlen-bauen.py [zielordner]
    -> instagram-zahlen.json -> Artifact write_db, „daten" / „instagram"

🚨 Das Dokument heisst **`instagram`**, nicht `zahlen` — `state.zahlen` ist
im Cockpit schon Patricias haendische Umsatz-Tabelle.

Anlass war eine Werbeanzeige (24.09.2026), in der jemand seine Instagram-Zahlen
**im Dashboard** stehen hat, samt roter Warnung „seit 3 Tagen kein Abruf".
Genau diese Warnung ist der eigentliche Wert: eine Zahl ohne Datum daneben
sieht immer aktuell aus.

🚨 **Nichts wird hochgerechnet.** Reichweite je Beitrag, Durchschnitt, bester
und schwaechster Beitrag — alles gezaehlt, nichts geschaetzt. Bei zwei Konten
mit sehr unterschiedlicher Groesse (Mentoring rund 2'000, doTERRA rund 60) waere
ein gemeinsamer Mittelwert ohnehin irrefuehrend, deshalb bleibt je Konto
getrennt stehen.

🚨 **Der Median statt des Mittelwerts bei der Reichweite.** Ein einziges Reel
mit 4'000 Aufrufen zieht den Schnitt so weit hoch, dass die normale Woche
darunter unsichtbar wird. Beide Zahlen stehen drin, damit der Unterschied
sichtbar bleibt.
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path
from statistics import median

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "instagram-insights"

# Ab wann die Zahlen als alt gelten. Instagram-Beitraege sind auch Wochen
# spaeter abrufbar — wenn hier nichts Neues liegt, lief das Skript nicht.
ALT_AB_TAGEN = 3


def juengste() -> Path | None:
    dateien = sorted(QUELLE.glob("20*.json"))
    return dateien[-1] if dateien else None


def auswerten(konto: dict) -> dict:
    beitraege = konto.get("beitraege") or []
    reichweiten = [b.get("reach") or 0 for b in beitraege]
    mit = [r for r in reichweiten if r > 0]

    bester = max(beitraege, key=lambda b: b.get("reach") or 0, default=None)
    schwaechster = min((b for b in beitraege if (b.get("reach") or 0) > 0),
                       key=lambda b: b.get("reach") or 0, default=None)

    def knapp(b):
        if not b:
            return None
        return {
            "datum": b.get("datum", ""),
            "typ": b.get("typ", ""),
            "reach": b.get("reach") or 0,
            "saved": b.get("saved") or 0,
            "shares": b.get("shares") or 0,
            "anfang": (b.get("anfang") or "")[:90],
            "link": b.get("link", ""),
        }

    return {
        "handle": konto.get("handle", ""),
        "seite": konto.get("seite", ""),
        "follower": konto.get("follower") or 0,
        "beitraege_gezaehlt": len(beitraege),
        "reichweite_schnitt": round(sum(mit) / len(mit)) if mit else 0,
        "reichweite_median": round(median(mit)) if mit else 0,
        "gespeichert": sum(b.get("saved") or 0 for b in beitraege),
        "geteilt": sum(b.get("shares") or 0 for b in beitraege),
        "kommentare": sum(b.get("kommentare") or 0 for b in beitraege),
        "bester": knapp(bester),
        "schwaechster": knapp(schwaechster),
    }


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    datei = juengste()
    if not datei:
        sys.exit("Keine Zahlen in %s — erst `python scripts/instagram-insights/holen.py`"
                 % QUELLE)

    roh = json.loads(datei.read_text(encoding="utf-8"))
    stand = roh.get("stand") or datei.stem
    try:
        alter = (date.today() - date.fromisoformat(stand)).days
    except Exception:
        alter = None

    konten = [auswerten(k) for k in (roh.get("konten") or [])]

    daten = {
        "stand": stand,
        "alter_tage": alter,
        # 🚨 Die Warnung wird hier entschieden, nicht in der Anzeige. Sonst
        # muesste jede Ansicht dieselbe Regel nochmal kennen.
        "veraltet": alter is not None and alter >= ALT_AB_TAGEN,
        "konten": konten,
        "quelle": "outputs/instagram-insights/%s" % datei.name,
        "holen_mit": "python scripts/instagram-insights/holen.py",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "instagram-zahlen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  Stand %s%s" % (stand, "  ⚠️ %d Tage alt" % alter
                            if daten["veraltet"] else ""))
    for k in konten:
        print("\n  %s — %d Follower" % (k["handle"], k["follower"]))
        print("    %d Beiträge · Reichweite Ø %d · Median %d"
              % (k["beitraege_gezaehlt"], k["reichweite_schnitt"],
                 k["reichweite_median"]))
        print("    %d gespeichert · %d geteilt · %d Kommentare"
              % (k["gespeichert"], k["geteilt"], k["kommentare"]))
        if k["bester"]:
            print("    bester:  %s  %d  %s"
                  % (k["bester"]["datum"], k["bester"]["reach"],
                     k["bester"]["anfang"][:50]))
    print("\nAbgelegt in: %s" % (ziel / "instagram-zahlen.json"))


if __name__ == "__main__":
    main()
