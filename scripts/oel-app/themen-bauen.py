"""Öl-App, Schritt 4 — je Anliegen ein Thema aus ALLEN Unterlagen.

    python scripts/oel-app/themen-bauen.py              # nur fehlende Themen
    python scripts/oel-app/themen-bauen.py --nur schlaf,husten
    python scripts/oel-app/themen-bauen.py --neu

Die Anliegen kommen aus context/doTERRA/Produktwissen/anliegen.json (dieselbe Liste wie im Cockpit).
Je Anliegen die passendsten Stellen aus Büchern, Enjoils, Ölschule und Emotions-Handbüchern
(quellen.py) — Claude schreibt daraus: Überblick, welche Öle und Produkte wie, Mischungen und Rezepte,
Ernährung und Alltag, Sicherheit, was die Bücher sagen.

Ausgabe: outputs/oel-app/daten/themen/<id>.json (gitignored). 🚨 NUR FÜR PATRICIA.
"""
import json
import pathlib
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import anthropic  # noqa: E402
from pydantic import BaseModel  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import quellen  # noqa: E402
from produkte_gemeinsam import env, Buchstelle, Rezept  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
ANLIEGEN = WS / "context/doTERRA/Produktwissen/anliegen.json"
KATALOG = WS / "outputs/oel-app/daten/katalog.json"
ZIEL = WS / "outputs/oel-app/daten/themen"
MAX_ZEICHEN = 45_000
MAX_JE_QUELLE = 4


class Empfehlung(BaseModel):
    produkt: str      # Name wie im Katalog, z.B. "Lavender", "dōTERRA Serenity", "Deep Blue Rub"
    wie: str          # konkrete Anwendung: wo, wie viel, wie oft
    art: Literal["aromatisch", "äusserlich", "innerlich", "Haushalt", "Emotion"]
    quellen: List[str]


class Thema(BaseModel):
    ueberblick: str              # 2–4 Sätze: worum es geht, was die Unterlagen grundsätzlich empfehlen
    empfehlungen: List[Empfehlung]
    rezepte: List[Rezept]
    alltag: List[str]            # Ernährung, Lebensstil, Gewohnheiten aus den Unterlagen
    emotion: str                 # emotionale Seite des Themas, wenn die Unterlagen eine nennen
    sicherheit: List[str]
    aus_den_buechern: List[Buchstelle]


AUFTRAG = """Du schreibst für Patricias private Öl-Nachschlage-App (nur sie selbst liest das) die Themenseite
zu einem Anliegen. Grundlage sind Auszüge aus ihren Büchern, Enjoils-Heften, Ölschule-Unterlagen und
Emotions-Handbüchern, dazu die Liste der doTERRA-Produkte.

Regeln:
- Nur was in den Auszügen steht, nichts aus eigenem Wissen ergänzen. Fehlt etwas, bleibt es leer.
- empfehlungen: die Öle und Produkte, die in den Auszügen für dieses Anliegen genannt werden, die am
  häufigsten genannten zuerst, je mit der konkreten Anwendung aus den Auszügen und den Quellen.
  Produktnamen so schreiben, wie sie in der Produktliste stehen.
- Gesundheitsaussagen gibst du wieder, wie die Quelle sie macht, und nennst die Quelle.
- aus_den_buechern: Titel und Seite genau wie im Auszug, „kern“ in eigenen Worten.
- Das soll ein umfassendes Nachschlagewerk werden: lieber zu viel als zu wenig. aus_den_buechern bis 25
  Stellen, rezepte: ALLE Rezepte und Mischungen mit Mengen aus den Auszügen.
- Deutsch, Schweizer Schreibweise (ss statt ß), klar und kurz.

"""


def stellen(a, alle):
    rx = [re.compile(r"(?<![\wäöü])" + re.escape(s.strip()), re.I) for s in a["suche"]]
    treffer = []
    for x in alle:
        n = sum(len(r.findall(x["t"])) for r in rx)
        if n:
            treffer.append((n + (2 if x["k"] in ("Öle", "Gemüt", "Hormone") else 0), x))
    treffer.sort(key=lambda t: -t[0])
    je_q, gesehen, aus, zeichen = defaultdict(int), set(), [], 0
    for _, x in treffer:
        fp = quellen.A.norm(x["t"])[:160]
        if je_q[x["q"]] >= MAX_JE_QUELLE or fp in gesehen:
            continue
        if zeichen + len(x["t"]) > MAX_ZEICHEN:
            break
        gesehen.add(fp)
        je_q[x["q"]] += 1
        aus.append(x)
        zeichen += len(x["t"])
    return aus


def schreiben(client, a, alle, namen):
    st = stellen(a, alle)
    if not st:
        print(f"  – {a['id']}: keine Stellen")
        return
    teile = [f"ANLIEGEN: {a['name']} (Gruppe {a['gruppe']})",
             "PRODUKTLISTE: " + ", ".join(namen), f"\nAUSZÜGE ({len(st)}):"]
    teile += [f"\n[{x['q']} · {x['w']}]\n{x['t']}" for x in st]
    try:
        # lange Antworten: ab dieser Grösse verlangt die Schnittstelle Streaming
        with client.messages.stream(
            model="claude-opus-5-5", max_tokens=32000, output_config={"effort": "medium"},
            messages=[{"role": "user", "content": AUFTRAG + "\n".join(teile)}], output_format=Thema,
        ) as s:
            fertig = s.get_final_message()
        roh = "".join(b.text for b in fertig.content if b.type == "text")
        thema = Thema.model_validate_json(roh)
    except Exception as e:
        print(f"  ❌ {a['id']}: {e}")
        return
    t = thema.model_dump()
    t.update({"id": a["id"], "name": a["name"], "gruppe": a["gruppe"], "anzahl_stellen": len(st),
              "quellen": sorted({x["q"] for x in st})})
    (ZIEL / f"{a['id']}.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ {a['id']:24} {len(st):3} Stellen · {len(t['empfehlungen'])} Empfehlungen · "
          f"{len(t['rezepte'])} Rezepte")


def main():
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))
    anl = json.loads(ANLIEGEN.read_text(encoding="utf-8"))["anliegen"]
    namen = [p["name"] for p in json.loads(KATALOG.read_text(encoding="utf-8"))["produkte"]]
    alle = quellen.abschnitte()
    ZIEL.mkdir(parents=True, exist_ok=True)
    if "--nur" in sys.argv:
        nur = set(sys.argv[sys.argv.index("--nur") + 1].split(","))
        anl = [a for a in anl if a["id"] in nur]
    elif "--neu" not in sys.argv:
        anl = [a for a in anl if not (ZIEL / f"{a['id']}.json").exists()]
    print(f"{len(anl)} Themen zu schreiben")
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda a: schreiben(client, a, alle, namen), anl))


if __name__ == "__main__":
    main()
