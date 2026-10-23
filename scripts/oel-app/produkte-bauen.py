"""Öl-App, Schritt 3 — je Produkt ein Eintrag aus ALLEN Unterlagen.

    python scripts/oel-app/produkte-bauen.py               # nur fehlende Produkte
    python scripts/oel-app/produkte-bauen.py --nur lavender,frankincense
    python scripts/oel-app/produkte-bauen.py --neu         # alle neu schreiben

Je Produkt aus katalog.json: die Stellen aus Büchern, Enjoils, Ölschule und Emotions-Handbüchern
heraussuchen, in denen es vorkommt (quellen.py), und Claude daraus den Eintrag schreiben lassen —
Steckbrief, Anwendungen nach Art, Sicherheit, Emotion, Mischpartner, Themen, was die Bücher sagen
(mit Quelle und Seite), Rezepte.

Ausgabe: outputs/oel-app/daten/produkte/<id>.json (gitignored — Buchinhalte). Wiederholbar: fertige
Produkte werden übersprungen.
🚨 NUR FÜR PATRICIA. Die Einträge geben wieder, was die Bücher sagen, auch Heilaussagen — mit Quelle.
Nach aussen geht davon nichts (dafür gibt es die öffentliche Öl-Wissen-Seite).
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
KATALOG = WS / "outputs/oel-app/daten/katalog.json"
ZIEL = WS / "outputs/oel-app/daten/produkte"
MAX_ZEICHEN = 40_000
MAX_JE_QUELLE = 5


class Anwendung(BaseModel):
    art: Literal["aromatisch", "äusserlich", "innerlich", "Haushalt", "Emotion", "Kinder"]
    text: str


class Eintrag(BaseModel):
    kurz: str                     # ein Satz: was das Produkt ausmacht
    pflanze: str                  # botanischer Name, Pflanzenteil, Gewinnung; "" wenn unbekannt
    duft: str
    hauptbestandteile: List[str]  # chemische Hauptbestandteile, wenn in den Unterlagen genannt
    anwendungen: List[Anwendung]
    verduennung: str              # Empfehlung zur Verdünnung / Dosierung, "" wenn unbekannt
    sicherheit: List[str]         # Hinweise: Sonne, Schwangerschaft, Kinder, Haut, Einnahme
    emotion: str                  # emotionale Ebene aus den Emotions-Unterlagen, "" wenn keine
    passt_zu: List[str]           # Öle/Produkte zum Mischen oder Kombinieren
    themen: List[str]             # Anliegen, bei denen es in den Unterlagen genannt wird (kurz, z.B. "Schlaf")
    aus_den_buechern: List[Buchstelle]
    rezepte: List[Rezept]


AUFTRAG = """Du schreibst für Patricias private Öl-Nachschlage-App (nur sie selbst liest das) den Eintrag
zu einem doTERRA-Produkt. Grundlage sind der Katalogtext und Auszüge aus ihren Büchern, Enjoils-Heften,
Ölschule-Unterlagen und Emotions-Handbüchern.

Regeln:
- Nur was im Katalog oder in den Auszügen steht. Nichts aus eigenem Wissen ergänzen, nichts erfinden.
  Fehlt etwas, bleibt das Feld leer.
- Achte darauf, dass ein Auszug wirklich dieses Produkt meint (z.B. „Balance“ als Wort vs. die Mischung,
  Zitrone als Lebensmittel vs. das Öl).
- Gesundheitsaussagen der Bücher gibst du wieder, wie die Quelle sie macht, und nennst die Quelle.
- Das soll ein umfassendes Nachschlagewerk werden: lieber zu viel als zu wenig. Jede Anwendung, jeder
  Hinweis und jede Mischung aus den Auszügen, die etwas Neues bringt, gehört hinein.
- aus_den_buechern: jede Stelle, die etwas Eigenes sagt (bis 25), Titel und Seite genau wie im Auszug,
  „kern“ in eigenen Worten (kein Abschreiben langer Passagen).
- rezepte: ALLE Rezepte und Mischungen mit Mengen aus den Auszügen, in denen das Produkt vorkommt.
- duft: aus Katalog oder Auszügen; steht dort keine Duftbeschreibung, leer.
- Deutsch, Schweizer Schreibweise (ss statt ß), klar und kurz.

"""


ALIAS = json.loads((WS / "context/doTERRA/Produktwissen/oel-app-zusatzprodukte.json").read_text(encoding="utf-8"))["namen"]


def suchwoerter(p):
    # dazu die deutschen und alten Namen, unter denen die Bücher das Produkt führen (Breathe → Air)
    roh = [p["name"], p["deutsch"]] + ([p["id"].replace("-", " ")] if len(p["id"]) > 5 else [])
    roh += [n for n, i in ALIAS.items() if i == p["id"]]
    woerter = set()
    for w in roh:
        w = re.sub(r"d[oō]TERRA|™|®|\(.*?\)|touch|roll-on|\d+\s*ml", "", w, flags=re.I).strip(" -,")
        # „Air“ ist kurz, aber ein Produktname — muster() verlangt dann die genaue Schreibweise
        kurz_ok = w == re.sub(r"d[oō]TERRA|™", "", p["name"]).strip()
        if len(w) >= 3 and (len(w) >= 4 or kurz_ok) and not re.search(r"mischung|kollektion|kit\b|set\b|pack", w, re.I):
            woerter.add(w)
    return woerter


def muster(w):
    # kurze oder allgemeine Wörter nur mit grossem Anfang (Balance, Air, Rose, Peace)
    # 🚨 In gescannten Heften stehen Namen oft in Versalien („AMAVI“) — die zählen mit.
    if len(w) <= 7:
        return re.compile(r"(?<![\wäöü])(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?![\wäöü])")
    return re.compile(r"(?<![\wäöü])" + re.escape(w) + r"(?![\wäöü])", re.I)


def stellen(p, alle):
    rx = [muster(w) for w in suchwoerter(p)]
    if not rx:
        return []
    treffer = []
    for a in alle:
        n = sum(len(r.findall(a["t"])) for r in rx)
        # 🚨 Die Emotions-Handbücher heissen nach dem Öl, im Text steht der Name aber kaum („Amavi“)
        if any(r.search(a["q"]) for r in rx):
            n += 5
        if n:
            treffer.append((n + (3 if a["k"] in ("Öle", "Gemüt") else 0), a))
    treffer.sort(key=lambda x: -x[0])
    je_q, gesehen, aus, zeichen = defaultdict(int), set(), [], 0
    for _, a in treffer:
        fp = quellen.A.norm(a["t"])[:160]
        if je_q[a["q"]] >= MAX_JE_QUELLE or fp in gesehen:
            continue
        if zeichen + len(a["t"]) > MAX_ZEICHEN:
            break
        gesehen.add(fp)
        je_q[a["q"]] += 1
        aus.append(a)
        zeichen += len(a["t"])
    return aus


def schreiben(client, p, alle):
    ziel = ZIEL / f"{p['id']}.json"
    st = stellen(p, alle)
    teile = [f"PRODUKT: {p['name']} ({p['deutsch']}) · {p['kategorie']} · {p['groesse']}",
             f"Inhaltsstoffe laut Katalog: {', '.join(p['inhaltsstoffe']) or '–'}",
             f"KATALOGTEXT: {p['katalogtext']}", "Punkte: " + " · ".join(p["punkte"]),
             f"\nAUSZÜGE ({len(st)}):"]
    teile += [f"\n[{a['q']} · {a['w']}]\n{a['t']}" for a in st]
    try:
        # lange Antworten: ab dieser Grösse verlangt die Schnittstelle Streaming
        with client.messages.stream(
            model="claude-opus-5-5", max_tokens=32000, output_config={"effort": "medium"},
            messages=[{"role": "user", "content": AUFTRAG + "\n".join(teile)}], output_format=Eintrag,
        ) as s:
            fertig = s.get_final_message()
        roh = "".join(b.text for b in fertig.content if b.type == "text")
        eintrag = Eintrag.model_validate_json(roh)
    except Exception as e:
        print(f"  ❌ {p['id']}: {e}")
        return
    e = eintrag.model_dump()
    e.update({k: p[k] for k in ("id", "name", "deutsch", "kategorie", "groesse", "inhaltsstoffe",
                                "katalogtext", "punkte")})
    e["anzahl_stellen"] = len(st)
    e["quellen"] = sorted({a["q"] for a in st})
    ziel.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ {p['id']:32} {len(st):3} Stellen · {len(e['aus_den_buechern'])} Buchstellen · "
          f"{len(e['rezepte'])} Rezepte")


def main():
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))
    produkte = json.loads(KATALOG.read_text(encoding="utf-8"))["produkte"]
    alle = quellen.abschnitte()
    ZIEL.mkdir(parents=True, exist_ok=True)
    if "--nur" in sys.argv:
        nur = set(sys.argv[sys.argv.index("--nur") + 1].split(","))
        produkte = [p for p in produkte if p["id"] in nur]
    elif "--duenne" in sys.argv:  # Öle und Ergänzungen mit wenig Stoff nochmals, z.B. nach einer besseren Suche
        def duenn(p):
            f = ZIEL / f"{p['id']}.json"
            return p["kategorie"] in ("Einzelöl", "Mischung", "Touch / Roll-on", "Nahrungsergänzung", "Kinder") and (
                not f.exists() or json.loads(f.read_text(encoding="utf-8")).get("anzahl_stellen", 0) < 8)
        produkte = [p for p in produkte if duenn(p)]
    elif "--neu" not in sys.argv:
        produkte = [p for p in produkte if not (ZIEL / f"{p['id']}.json").exists()]
    print(f"{len(produkte)} Produkte zu schreiben, {len(alle)} Abschnitte als Grundlage")
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda p: schreiben(client, p, alle), produkte))


if __name__ == "__main__":
    main()
