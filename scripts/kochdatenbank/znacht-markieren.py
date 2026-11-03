"""Kochdatenbank — bestehende Einträge als Znacht einordnen (für Einträge ohne Feld `znacht`).

    python scripts/kochdatenbank/znacht-markieren.py

Neue Einträge bekommen `znacht` schon beim Einlesen. Dieses Skript holt es für ältere nach: Claude
sieht nur Titel, Kurzbeschreibung und Kategorie (je 150 auf einmal) und nennt die Znacht-tauglichen.
Wiederholbar: Einträge mit Feld `znacht` werden übersprungen.
"""
import json
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import anthropic  # noqa: E402
from pydantic import BaseModel  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).parent))
einlesen = __import__("einlesen")

PAKET = 150


class Auswahl(BaseModel):
    znacht: List[str]   # die Kennungen, die als Znacht taugen


def einordnen(client, paket):
    zeilen = "\n".join(f"{e['id']} | {e['kategorie']} | {e['titel']} — {e['kurz']}" for e in paket)
    auftrag = (f"Patricias Rezeptliste (Schweiz, Familie mit 4 Kindern). Welche taugen als Znacht?\n"
               f"Znacht = {einlesen.ZNACHT_REGEL}\n\nGib die Kennungen (erste Spalte) der passenden zurück.\n\n{zeilen}")
    with client.messages.stream(
        model="claude-sonnet-5-5", max_tokens=8000, output_config={"effort": "low"},
        messages=[{"role": "user", "content": auftrag}], output_format=Auswahl,
    ) as s:
        fertig = s.get_final_message()
    return set(Auswahl.model_validate_json("".join(b.text for b in fertig.content if b.type == "text")).znacht)


def main():
    dateien = sorted(einlesen.EINTRAEGE.glob("*.json"))
    alle = {f: json.loads(f.read_text(encoding="utf-8")) for f in dateien}
    offen = [e for es in alle.values() for e in es if "znacht" not in e]
    print(f"{len(offen)} Einträge ohne Znacht-Einordnung")
    if not offen:
        return
    client = anthropic.Anthropic(api_key=einlesen.env("ANTHROPIC_API_KEY"))
    pakete = [offen[i:i + PAKET] for i in range(0, len(offen), PAKET)]
    ja = set()
    with ThreadPoolExecutor(6) as pool:
        for paket, treffer in zip(pakete, pool.map(lambda p: einordnen(client, p), pakete)):
            ja |= treffer
            for e in paket:
                e["znacht"] = e["id"] in treffer
    for f, es in alle.items():
        f.write_text(json.dumps(es, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ja)} als Znacht eingeordnet")


if __name__ == "__main__":
    main()
