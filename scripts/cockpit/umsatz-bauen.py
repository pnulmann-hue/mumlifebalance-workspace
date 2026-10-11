"""Rechnet den echten Umsatz aus den ThriveCart-Transaktionen.

Bis zum 24.09.2026 war „Zahlen & Ziele" im Cockpit Handarbeit und die Notion-
Felder „Erkenntnis Kennzahlen-Analyse" blieben leer — bei September **und**
Oktober. Nicht aus Nachlaessigkeit: die Zahlen lagen in ThriveCart und niemand
hat sie von Hand uebertragen.

    python scripts/cockpit/umsatz-bauen.py
    # danach: ArtifactData set -> Sammlung "daten", Dokument "umsatz"

🚨 **KEINE Kundendaten.** Jede Transaktion traegt ein `customer`-Objekt mit
Name, E-Mail, Adresse, IP-Adresse und Facebook-Tracking-Kennungen. Das ist genau
das, was nach dem 13.09.2026 nie wieder in eine Ablage gehoert, die weitergegeben
werden kann. Dieses Skript liest das Feld **gar nicht erst** aus — es zaehlt nur
Betraege. Wer hier spaeter „nur den Vornamen" mitnehmen will: nein.

🚨 **`amount` ist in Rappen.** 20500 heisst CHF 205.00. Wer die Zahl direkt
anzeigt, meldet hundertfachen Umsatz.

🚨 **Drei Transaktionsarten, die nicht dasselbe bedeuten:**
  • `charge` — ein Kauf
  • `rebill` — eine Folgerate einer Ratenzahlung
  • `finish` — die letzte Rate
Fuer „wie viel Geld kam rein" zaehlen alle. Fuer „wie viele Kundinnen kamen
dazu" **nur `charge`** — sonst zaehlt eine Ratenzahlerin dreimal.

🚨 **Die Liste ist paginiert.** `?page=2` funktioniert, `offset` und `start`
werden stillschweigend ignoriert und liefern wieder Seite 1. Wer das nicht
merkt, rechnet mit den ersten 25 von 85 und hat ein Drittel.
"""

import importlib.util
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

# Die Zugangs- und Abruflogik liegt schon in thrivecart-holen.py. Sie dort zu
# lassen heisst: ein Schluessel, ein Wiederholungsverhalten, eine Stelle.
_spec = importlib.util.spec_from_file_location(
    "tc", str(Path(__file__).resolve().parent / "thrivecart-holen.py"))
tc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tc)

# Wie viele Seiten hoechstens — Sicherheitsnetz gegen eine Endlosschleife,
# falls die Schnittstelle `page` einmal ignoriert.
MAX_SEITEN = 40


def alle_transaktionen(key) -> list:
    raus, gesehen = [], set()
    seite, gesamt = 1, None
    while seite <= MAX_SEITEN:
        r = tc.ruf("/transactions?page=%d" % seite, key)
        t = (r or {}).get("transactions") or []
        meta = (r or {}).get("meta") or {}
        if gesamt is None:
            gesamt = meta.get("total")
        neu = 0
        for x in t:
            eid = x.get("event_id")
            if eid and eid in gesehen:
                continue        # dieselbe Seite nochmal — dann ist Schluss
            if eid:
                gesehen.add(eid)
            raus.append(x)
            neu += 1
        if not t or not neu:
            break
        if gesamt and len(raus) >= gesamt:
            break
        seite += 1
    return raus, gesamt


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    key = tc.schluessel()
    roh, gemeldet = alle_transaktionen(key)
    if not roh:
        sys.exit("Keine Transaktionen erhalten — Zugang prüfen.")

    monate = defaultdict(lambda: {"umsatz": 0, "kaeufe": 0, "raten": 0, "zeilen": 0})
    # Tagesgenau, damit der Wochenbogen daraus Wochen bilden kann. Ein Monat
    # laesst sich aus Tagen zusammenzaehlen, eine Woche aus Monaten nicht.
    tage = defaultdict(lambda: {"umsatz": 0.0, "kaeufe": 0})
    produkte = defaultdict(lambda: {"name": "", "umsatz": 0, "kaeufe": 0})
    arten = defaultdict(int)
    waehrungen = set()

    for x in roh:
        # 🚨 `customer` wird bewusst nicht angefasst.
        datum = (x.get("date") or "")[:10]
        if not datum:
            continue
        monat = datum[:7]
        betrag = (x.get("amount") or 0) / 100.0      # Rappen -> Franken
        art = x.get("transaction_type") or "?"
        arten[art] += 1
        waehrungen.add(x.get("currency") or "?")

        t = tage[datum]
        t["umsatz"] += betrag
        if art == "charge":
            t["kaeufe"] += 1

        m = monate[monat]
        m["umsatz"] += betrag
        m["zeilen"] += 1
        if art == "charge":
            m["kaeufe"] += 1
        else:
            m["raten"] += 1

        pid = str(x.get("product_id") or x.get("item_id") or "?")
        p = produkte[pid]
        p["name"] = p["name"] or (x.get("item_name") or "")[:70]
        p["umsatz"] += betrag
        if art == "charge":
            p["kaeufe"] += 1

    monatsliste = [dict(monat=k, **{kk: (round(vv, 2) if kk == "umsatz" else vv)
                                    for kk, vv in v.items()})
                   for k, v in sorted(monate.items())]
    produktliste = sorted(
        [dict(id=k, name=v["name"], umsatz=round(v["umsatz"], 2), kaeufe=v["kaeufe"])
         for k, v in produkte.items()],
        key=lambda x: -x["umsatz"])

    heute = date.today()
    lauf = heute.strftime("%Y-%m")
    dieser = next((m for m in monatsliste if m["monat"] == lauf), None)

    daten = {
        "stand": heute.isoformat(),
        "waehrung": sorted(waehrungen)[0] if len(waehrungen) == 1 else "gemischt",
        "monate": monatsliste,
        "tage": [{"datum": k, "umsatz": round(v["umsatz"], 2), "kaeufe": v["kaeufe"]}
                 for k, v in sorted(tage.items())],
        "produkte": produktliste,
        "arten": dict(arten),
        "zeilen_gesamt": len(roh),
        "zeilen_gemeldet": gemeldet,
        "dieser_monat": dieser,
        "quelle": "ThriveCart /transactions (ohne Kundendaten)",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "umsatz.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Transaktionen gelesen (ThriveCart meldet %s)"
          % (len(roh), gemeldet))
    if gemeldet and len(roh) != gemeldet:
        print("  ⚠️ Das passt nicht zusammen — Paginierung prüfen.")
    print("  Arten: %s" % ", ".join("%s %d" % kv for kv in sorted(arten.items())))
    print()
    print("  %-9s %10s %7s %7s" % ("Monat", "Umsatz", "Käufe", "Raten"))
    for m in monatsliste[-8:]:
        print("  %-9s %10.2f %7d %7d"
              % (m["monat"], m["umsatz"], m["kaeufe"], m["raten"]))
    print()
    print("  Top-Produkte:")
    for p in produktliste[:6]:
        print("    %8.2f  %2d Käufe  %s" % (p["umsatz"], p["kaeufe"], p["name"]))
    print("\nAbgelegt in: %s" % (ziel / "umsatz.json"))


if __name__ == "__main__":
    main()
