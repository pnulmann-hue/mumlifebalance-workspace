"""
Baut den doTERRA-Rang-Tracker fuers Cockpit.

Grundlage sind zwei Berichte aus dem Back Office:
  Schlagdistanz (QryID=EliteStriking)  PV, OV und Bein-Zaehler je Person
  Teamqualifikationsbericht (QryID=Qualifier)  Platzierungs-Struktur

Beide sind nur eingeloggt erreichbar. Deshalb kommen die Zahlen als Text
herein — abgelegt in `context/doterra/backoffice/schlagdistanz-<Monat>.txt`,
kopiert aus dem Bericht oder von Claude ueber Chrome geholt.

Rangvoraussetzungen (aus business-building-guide.pdf S. 108 und
train-guide.pdf S. 6/7 — nicht geraten):

  Executive   100 PV + 2.000 OV
  Elite       100 PV + 3.000 OV
  Premier     100 PV + 5.000 OV + 2 Executive-Beine
  Silver      100 PV + 3 Elite-Beine
  Gold        100 PV + 3 Premier-Beine

Aufruf:
  python scripts/cockpit/doterra-tracker-bauen.py [zielordner]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "context" / "doterra" / "backoffice"

# --------------------------------------------------------------------------
# Die Regeln
# --------------------------------------------------------------------------
RAENGE = [
    {"name": "Consultant", "pv": 0, "ov": 0, "beine": 0, "beinrang": ""},
    {"name": "Manager", "pv": 100, "ov": 500, "beine": 0, "beinrang": ""},
    {"name": "Director", "pv": 100, "ov": 1000, "beine": 0, "beinrang": ""},
    {"name": "Executive", "pv": 100, "ov": 2000, "beine": 0, "beinrang": ""},
    {"name": "Elite", "pv": 100, "ov": 3000, "beine": 0, "beinrang": ""},
    {"name": "Premier", "pv": 100, "ov": 5000, "beine": 2, "beinrang": "Executive"},
    {"name": "Silver", "pv": 100, "ov": 0, "beine": 3, "beinrang": "Elite"},
    {"name": "Gold", "pv": 100, "ov": 0, "beine": 3, "beinrang": "Premier"},
    {"name": "Platinum", "pv": 100, "ov": 0, "beine": 3, "beinrang": "Silver"},
]
RANGFOLGE = [r["name"] for r in RAENGE]
REGEL = {r["name"]: r for r in RAENGE}

# Patricias drei Qualifikations-Beine. Namen wie im Back Office.
IHRE_BEINE = ["14345977", "14394698", "16982542"]
IHRE_ID = "11658536"


def zahl(t):
    return float(str(t).replace(",", "").replace("'", "").strip() or 0)


def schlagdistanz_lesen(pfad):
    """Die Tabelle aus dem Schlagdistanz-Bericht in Zeilen verwandeln.

    Format je Zeile:
      Nr · Mitglieds-ID · Name · Leg-ID · Level · Rang · % · PV · OV · 6 Bein-Zahlen
    """
    zeilen = []
    muster = re.compile(
        r"^\s*\d+\s+­?(\d{6,9})\s+(.+?)\s+­?(\d{6,9}|0)\s+­?(\d+)\s+"
        r"([A-Za-zÄÖÜäöü ]+?)\s+([\d.]+)%\s+([\d,.']+)\s+([\d,.']+)\s+"
        r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$")
    for zeile in Path(pfad).read_text(encoding="utf-8").splitlines():
        m = muster.match(zeile)
        if not m:
            continue
        zeilen.append({
            "id": m.group(1),
            "name": m.group(2).strip(),
            "bein": m.group(3),
            "level": int(m.group(4)),
            "rang": m.group(5).strip(),
            "pv": zahl(m.group(7)),
            "ov": zahl(m.group(8)),
            "exec_beine": int(m.group(9)),
            "elite_beine": int(m.group(10)),
            "premier_beine": int(m.group(11)),
        })
    return zeilen


def luecke_zu(person, zielrang):
    """Was dieser Person zum Zielrang fehlt — als Liste von Klartext-Punkten."""
    r = REGEL.get(zielrang)
    if not r:
        return []
    offen = []
    if person["pv"] < r["pv"]:
        offen.append({"was": "PV", "fehlt": r["pv"] - person["pv"],
                      "ist": person["pv"], "soll": r["pv"]})
    if r["ov"] and person["ov"] < r["ov"]:
        offen.append({"was": "OV", "fehlt": r["ov"] - person["ov"],
                      "ist": person["ov"], "soll": r["ov"]})
    if r["beine"]:
        feld = {"Executive": "exec_beine", "Elite": "elite_beine",
                "Premier": "premier_beine"}.get(r["beinrang"])
        hat = person.get(feld, 0)
        if hat < r["beine"]:
            offen.append({"was": r["beinrang"] + "-Beine", "fehlt": r["beine"] - hat,
                          "ist": hat, "soll": r["beine"]})
    return offen


def naechster_rang(rang):
    try:
        return RANGFOLGE[RANGFOLGE.index(rang) + 1]
    except (ValueError, IndexError):
        return ""


def bauen(zeilen, monat):
    nach_id = {z["id"]: z for z in zeilen}
    ich = nach_id.get(IHRE_ID)
    if not ich:
        sys.exit("Deine eigene Zeile fehlt im Bericht.")

    beine = []
    for bid in IHRE_BEINE:
        kopf = nach_id.get(bid)
        if not kopf:
            continue
        # Alle, die in diesem Bein haengen, ohne den Kopf selbst
        leute = [z for z in zeilen
                 if z["bein"] == bid and z["id"] != bid and z["ov"] > 0]
        leute.sort(key=lambda z: -z["ov"])
        beine.append({
            "id": bid,
            "name": kopf["name"],
            "rang": kopf["rang"],
            "pv": kopf["pv"],
            "ov": kopf["ov"],
            "zu_elite": luecke_zu(kopf, "Elite"),
            "zu_premier": luecke_zu(kopf, "Premier"),
            "naechster": naechster_rang(kopf["rang"]),
            "zu_naechstem": luecke_zu(kopf, naechster_rang(kopf["rang"])),
            "leute": [{"name": p["name"], "rang": p["rang"], "pv": p["pv"],
                       "ov": p["ov"], "level": p["level"],
                       "zu_executive": luecke_zu(p, "Executive")}
                      for p in leute[:12]],
            "weitere": max(0, len(leute) - 12),
        })

    return {
        "monat": monat,
        "ich": {"name": ich["name"], "rang": ich["rang"], "pv": ich["pv"],
                "ov": ich["ov"], "exec_beine": ich["exec_beine"],
                "elite_beine": ich["elite_beine"],
                "premier_beine": ich["premier_beine"]},
        "zu_silver": luecke_zu(ich, "Silver"),
        "zu_gold": luecke_zu(ich, "Gold"),
        "beine": beine,
        "regeln": RAENGE,
        "stand": date.today().isoformat(),
    }


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    dateien = sorted(QUELLE.glob("schlagdistanz-*.txt"))
    if not dateien:
        sys.exit("Kein Bericht in %s — erst die Schlagdistanz ablegen." % QUELLE)
    neuste = dateien[-1]
    monat = neuste.stem.replace("schlagdistanz-", "")

    zeilen = schlagdistanz_lesen(neuste)
    if not zeilen:
        sys.exit("Aus %s liess sich keine Zeile lesen." % neuste.name)

    daten = bauen(zeilen, monat)
    (ziel / "doterra.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Zeilen gelesen aus %s" % (len(zeilen), neuste.name))
    print("  Du: %s · PV %.2f · OV %.2f" % (daten["ich"]["rang"],
                                            daten["ich"]["pv"], daten["ich"]["ov"]))
    for b in daten["beine"]:
        fehlt = ", ".join("%.2f %s" % (o["fehlt"], o["was"]) for o in b["zu_elite"])
        print("  %-22s %-11s OV %8.2f  zu Elite fehlt: %s"
              % (b["name"][:22], b["rang"], b["ov"], fehlt or "nichts"))
    print("\nAbgelegt in: %s" % (ziel / "doterra.json"))


if __name__ == "__main__":
    main()
