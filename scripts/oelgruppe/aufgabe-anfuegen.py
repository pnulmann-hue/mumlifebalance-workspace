"""Hängt eine Erinnerung an einen Abzug von daten/aufgaben (nur anhängen, nichts sonst ändern).

    python scripts/oelgruppe/aufgabe-anfuegen.py <aufgaben.json> --id af-… --aufgabe "…" --datum 2026-11-06 --notiz "…"

Danach die Datei mit ArtifactData set (if_version des Abzugs) zurückschreiben. Gibt es die Kennung schon, passiert nichts.
"""
import argparse
import json
import pathlib

ap = argparse.ArgumentParser()
ap.add_argument("datei")
ap.add_argument("--id", required=True)
ap.add_argument("--aufgabe", required=True)
ap.add_argument("--datum", required=True)
ap.add_argument("--notiz", default="")
a = ap.parse_args()
p = pathlib.Path(a.datei)
d = json.loads(p.read_text(encoding="utf-8"))
if any(i.get("id") == a.id for i in d["items"]):
    print("schon da:", a.id)
else:
    d["items"].append({"aufgabe": a.aufgabe, "bereich": "business", "datum": a.datum, "erledigt": False, "id": a.id,
                       "notiz": a.notiz, "prio": "hoch", "quelle": "doTERRA-Freigaben", "status": "offen"})
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print("angefügt:", a.id)
