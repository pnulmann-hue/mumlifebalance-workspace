#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
digi-index.py — Index und Suche für Patricias digitales Bastel-Material.

Scannt den Basteln-Ordner, liest ALLE Dateinamen (keine Bildanalyse) und macht
sie durchsuchbar. Damit sind die ~8'000 digitalen Dateien genauso auffindbar
wie die physischen Stempel im Register.

Nutzung
-------
    python scripts/basteln/digi-index.py --neu-aufbauen
        Scannt den Quellordner und schreibt context/basteln/digi-index.json

    python scripts/basteln/digi-index.py badewanne
        Sucht "badewanne" in Dateinamen UND Ordnernamen

    python scripts/basteln/digi-index.py schmetterling --limit 40
    python scripts/basteln/digi-index.py hochzeit --ordner
        --ordner  zeigt nur passende Themenwelten (Ordner), nicht jede Datei

Warum ein Script und keine Markdown-Liste: 8'000 Zeilen Markdown wären nicht
lesbar. Das Script filtert und zeigt nur, was passt.
"""
import json
import os
import re
import sys
from collections import defaultdict

QUELLE = r"C:\Users\pnulm\OneDrive\Dokumente\Patricia\Hobby\Basteln"
INDEX = os.path.join("context", "basteln", "digi-index.json")

# Formate, die als Motiv/Vorlage zählen
NUTZBAR = {".svg", ".png", ".dxf", ".studio3", ".studio", ".fcm", ".jpg", ".jpeg", ".pdf"}

# Dateinamen ohne Aussagekraft (Facebook-Downloads, Kamera-Dateien, Hashes)
UNBRAUCHBAR = re.compile(
    r"^(\d{8,}[_-].*|IMG[_-]?\d+|DSC\d+|[0-9a-f]{16,}|unbenannt\d*|image\d+)$",
    re.IGNORECASE,
)


def aufbauen():
    if not os.path.isdir(QUELLE):
        print(f"FEHLER: Quellordner nicht gefunden:\n  {QUELLE}")
        print("Liegt der OneDrive-Ordner woanders? Dann QUELLE im Script anpassen.")
        return 1

    eintraege = []
    ordner_zaehler = defaultdict(int)
    uebersprungen = 0

    for pfad, _, dateien in os.walk(QUELLE):
        rel_ordner = os.path.relpath(pfad, QUELLE)
        thema = os.path.basename(pfad)
        for datei in dateien:
            stamm, ext = os.path.splitext(datei)
            if ext.lower() not in NUTZBAR:
                continue
            if UNBRAUCHBAR.match(stamm.strip()):
                uebersprungen += 1
                continue
            eintraege.append(
                {"name": stamm, "ext": ext.lower().lstrip("."), "thema": thema, "pfad": rel_ordner}
            )
            ordner_zaehler[rel_ordner] += 1

    # PNG/SVG/DXF mit gleichem Namen im gleichen Ordner zusammenfassen
    gruppen = defaultdict(lambda: {"formate": set()})
    for e in eintraege:
        key = (e["pfad"], e["name"])
        g = gruppen[key]
        g["name"] = e["name"]
        g["thema"] = e["thema"]
        g["pfad"] = e["pfad"]
        g["formate"].add(e["ext"])

    motive = [
        {"name": g["name"], "thema": g["thema"], "pfad": g["pfad"], "formate": sorted(g["formate"])}
        for g in gruppen.values()
    ]
    motive.sort(key=lambda m: (m["pfad"].lower(), m["name"].lower()))

    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        json.dump(
            {
                "quelle": QUELLE,
                "dateien_gezaehlt": len(eintraege),
                "motive": len(motive),
                "ordner": len(ordner_zaehler),
                "uebersprungen_ohne_aussage": uebersprungen,
                "eintraege": motive,
            },
            f,
            ensure_ascii=False,
            indent=1,
        )

    print(f"Index gebaut: {INDEX}")
    print(f"  {len(eintraege)} nutzbare Dateien")
    print(f"  {len(motive)} Motive (Formate zusammengefasst)")
    print(f"  {len(ordner_zaehler)} Ordner / Themenwelten")
    print(f"  {uebersprungen} Dateien ohne sprechenden Namen übersprungen")
    return 0


def laden():
    if not os.path.exists(INDEX):
        print(f"Kein Index gefunden. Erst aufbauen:\n  python {sys.argv[0]} --neu-aufbauen")
        sys.exit(1)
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)


def suchen(begriff, limit=25, nur_ordner=False):
    daten = laden()
    b = begriff.lower()

    if nur_ordner:
        treffer = sorted({e["pfad"] for e in daten["eintraege"] if b in e["pfad"].lower()})
        print(f"{len(treffer)} Themenwelten mit „{begriff}“:\n")
        for t in treffer[:limit]:
            anzahl = sum(1 for e in daten["eintraege"] if e["pfad"] == t)
            print(f"  {t}   ({anzahl} Motive)")
        return

    treffer = [e for e in daten["eintraege"] if b in e["name"].lower() or b in e["pfad"].lower()]
    # Namenstreffer zuerst — die sind konkreter als Ordnertreffer
    treffer.sort(key=lambda e: (b not in e["name"].lower(), e["name"].lower()))

    print(f"{len(treffer)} Treffer für „{begriff}“ (von {daten['motive']} Motiven)\n")
    nach_thema = defaultdict(list)
    for e in treffer[:limit]:
        nach_thema[e["pfad"]].append(e)

    for pfad, gruppe in nach_thema.items():
        print(f"--- {pfad}")
        for e in gruppe:
            print(f"    {e['name']}  [{', '.join(e['formate'])}]")
        print()

    if len(treffer) > limit:
        print(f"… {len(treffer) - limit} weitere. Mit --limit {min(len(treffer), 200)} alle zeigen.")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--neu-aufbauen":
        return aufbauen()

    limit = 25
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        del args[i : i + 2]
    nur_ordner = "--ordner" in args
    if nur_ordner:
        args.remove("--ordner")

    if not args:
        print("Kein Suchbegriff angegeben.")
        return 1
    suchen(" ".join(args), limit=limit, nur_ordner=nur_ordner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
