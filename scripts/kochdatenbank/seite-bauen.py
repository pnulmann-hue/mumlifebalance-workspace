"""Kochdatenbank, Schritt 2 — die Seite aus den eingelesenen Rezepten bauen.

    python scripts/kochdatenbank/seite-bauen.py

Liest outputs/kochdatenbank/daten/eintraege/*.json, legt sie in vorlage.html und schreibt
outputs/kochdatenbank/kochdatenbank.html (gitignored). Danach mit demselben Pfad neu veröffentlichen.
"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HIER = pathlib.Path(__file__).parent
WS = HIER.parents[1]
DATEN = WS / "outputs/kochdatenbank/daten/eintraege"
ZIEL = WS / "outputs/kochdatenbank/kochdatenbank.html"

rezepte = []
for f in sorted(DATEN.glob("*.json")):
    rezepte += json.loads(f.read_text(encoding="utf-8"))
# gleiche Titel aus zwei Dateien (z.B. „Appenzeller Filet“ einzeln und im Sammel-PDF) nur einmal
gesehen, rest = set(), []
for r in sorted(rezepte, key=lambda r: (-len(r["schritte"]), r["datei"])):
    k = r["titel"].lower().strip()
    if "Coaching-Plan" in r["merkmale"]:  # die Pläne geben derselben Mahlzeit je Fassung einen anderen Titel
        k = "plan:" + "|".join(sorted(re.sub(r"[^a-zäöü]", "", z.lower()) for z in r["zutaten"]))
    if k not in gesehen:
        gesehen.add(k)
        rest.append(r)

vorlage = (HIER / "vorlage.html").read_text(encoding="utf-8")
assert vorlage.count("/*DATEN*/[]") == 1
daten = json.dumps(rest, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
daten = daten.replace("�", "")  # unleserliche Zeichen aus Scans
ZIEL.write_text(vorlage.replace("/*DATEN*/[]", daten), encoding="utf-8")
print(f"{len(rest)} Rezepte ({len(rezepte) - len(rest)} doppelte weggelassen) → {ZIEL}")
