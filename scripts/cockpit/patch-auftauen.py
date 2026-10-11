"""Daten aus der Datenbank auftauen, bevor sie bearbeitet werden (08.10.2026).

🚨 **Die Artifact-Datenbank liefert `snap.data()` und `doc.data()` eingefroren**
(`db.d.ts`, Laufzeit 0.2.43: „snapshots and their data() are frozen"). Das Cockpit
läuft mit `"use strict"` — jede Zuweisung an ein eingefrorenes Objekt wirft dort
einen TypeError. Gefunden, weil PIA am 08.10. jeden Eintrag mit „1 Eintrag liess
sich nicht anlegen" quittierte: `aufgaben` kam direkt aus `snap.data()`, und
`aufgaben.items.unshift(...)` fiel um.

Betroffen war alles, was nach dem Laden aus der Datenbank verändert wird:
Aufgaben abhaken, Jahresplan, Ziele, Bogen-Notizen, Ketten, Termine, offene
Chats, Folientexte in Storys und Karussells (`frames`/`slides` wurden als
Verweis übernommen). Lokal fiel es nie auf — die Testfassung lädt aus
`localStorage`, und das ist nicht eingefroren.

Behebung: eine Hilfsfunktion `tief()` (tiefe Kopie über JSON) und **jeder**
`*.data()`-Aufruf läuft durch sie. Lesen kostet damit eine Kopie — bei den
Dokumentgrössen hier unmerklich, und eine Stelle, an der man es vergisst,
gibt es danach nicht mehr.

Läuft als letzter Patch nach patch-mein-tisch → patch-bereiche → patch-offene-chats.

    python scripts/cockpit/patch-auftauen.py [--datei <pfad>]
"""

import argparse
import importlib.util
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
MARKE = "function tief(x)"

HILFE_ANKER = "  function lsGet(key, fallback) {"
HILFE = (
    "  /* 🚨 Die Datenbank liefert eingefrorene Objekte — unter \"use strict\" wirft\n"
    "     jede Zuweisung daran. Siehe Kopf von patch-auftauen.py. */\n"
    "  function tief(x) {\n"
    "    if (x === null || x === undefined || typeof x !== \"object\") return x;\n"
    "    try { return JSON.parse(JSON.stringify(x)); } catch (e) { return x; }\n"
    "  }\n"
)


def patchen(t: str) -> str:
    if MARKE in t:
        print("Schon gepatcht — nichts zu tun.")
        return t
    assert t.count(HILFE_ANKER) == 1, "Anker lsGet fehlt"
    t = t.replace(HILFE_ANKER, HILFE + HILFE_ANKER)
    vorher = len(re.findall(r"\b(snap|doc|d|b)\.data\(\)", t))
    t = re.sub(r"\b(snap|doc|d|b)\.data\(\)", r"tief(\1.data())", t)
    # Gegenprobe: kein ungekapselter Aufruf mehr übrig.
    rest = re.findall(r"(?<!tief\()\b(?:snap|doc|d|b)\.data\(\)", t)
    assert not rest, "Ungekapselte data()-Aufrufe: %d" % len(rest)
    assert vorher >= 40, "Weniger data()-Aufrufe als erwartet: %d" % vorher
    print("Aufgetaut:", vorher, "Stellen")
    return t


def main():
    spec = importlib.util.spec_from_file_location(
        "tisch", Path(__file__).with_name("patch-mein-tisch.py"))
    tisch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tisch)

    ap = argparse.ArgumentParser()
    ap.add_argument("--datei", default=str(ROOT / "outputs/cockpit/mlb-cockpit.html"))
    args = ap.parse_args()
    pfad = Path(args.datei)
    roh = pfad.read_bytes().decode("utf-8")
    crlf = "\r\n" in roh
    t = roh.replace("\r\n", "\n")
    neu = patchen(t)
    if neu == t:
        return
    tisch.node_check(neu)
    pfad.write_bytes((neu.replace("\n", "\r\n") if crlf else neu).encode("utf-8"))
    print("Eingebaut:", pfad)


if __name__ == "__main__":
    main()
