"""Öl-App, Schritt 1 — der Produktkatalog: jedes doTERRA-Produkt einmal, mit Kategorie und Katalogtext.

    python scripts/oel-app/katalog-bauen.py

Liest context/doTERRA/product-guide.pdf (Produktkatalog Europa, Deutsch) Seite für Seite und lässt Claude
daraus die Produkte herausschreiben. Seitenblöcke laufen parallel, danach werden Doppelte (ein Produkt auf
zwei Seiten, z.B. Öl und Touch) über die Kennung zusammengelegt.

Ausgabe: outputs/oel-app/daten/katalog.json (gitignored).
Zugang: ANTHROPIC_API_KEY aus der .env im Wurzelverzeichnis.
"""
import json
import pathlib
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import anthropic  # noqa: E402
import pypdf  # noqa: E402
from pydantic import BaseModel  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
QUELLE = WS / "context/doTERRA/product-guide.pdf"
ZIEL = WS / "outputs/oel-app/daten/katalog.json"
ZUSATZ = WS / "context/doTERRA/Produktwissen/oel-app-zusatzprodukte.json"
WISSENSBASIS = WS / "context/doTERRA/Produktwissen/produkt-wissensbasis.json"
BLOCK = 3


def env(name):
    for z in (WS / ".env").read_text(encoding="utf-8").splitlines():
        if z.startswith(name + "="):
            return z.split("=", 1)[1].strip().strip('"')
    sys.exit(f"❌ {name} fehlt in .env")


Kategorie = Literal["Einzelöl", "Mischung", "Touch / Roll-on", "Nahrungsergänzung", "Körperpflege",
                    "Haushalt", "Kit / Kollektion", "Zubehör / Diffuser", "Kinder", "Sonstiges"]


class Produkt(BaseModel):
    id: str               # kleingeschrieben, englischer Name, Bindestriche: "wild-orange", "on-guard-touch"
    name: str             # wie bei doTERRA: "Wild Orange", "dōTERRA On Guard™" ohne ™
    deutsch: str          # deutscher Name oder Beschreibung aus dem Katalog: "Wildorange", "Schützende Mischung"
    kategorie: Kategorie
    groesse: str          # "15 ml", "60 Kapseln", "" wenn nicht genannt
    inhaltsstoffe: List[str]   # bei Mischungen/Kits: enthaltene Öle oder Produkte; sonst leer
    katalogtext: str      # die Beschreibung des Katalogs, sinngemäss vollständig, auf Deutsch
    punkte: List[str]     # die Aufzählungspunkte des Katalogs, wörtlich
    seite: int


class Seitenblock(BaseModel):
    produkte: List[Produkt]


AUFTRAG = """Hier sind Seiten aus dem doTERRA-Produktkatalog Europa (Deutsch), Seite für Seite mit Nummer.
Schreib jedes Produkt heraus, das auf diesen Seiten vorgestellt wird — Öle, Mischungen, Touch-Roll-ons,
Nahrungsergänzungen, Pflege, Haushalt, Kits, Diffuser, Zubehör. Ein Produkt, das nur in einer Liste oder
einem Verweis („siehe Seite 24“) genannt wird, ohne eigene Beschreibung, lässt du weg. Die Kennung ist
der englische Name, klein, mit Bindestrichen. Katalogtext und Punkte nimmst du aus dem Katalog, nichts
dazu erfinden. Sind keine Produkte auf den Seiten, gib eine leere Liste zurück.

"""


def block(client, nr, texte):
    seiten = "\n\n".join(f"=== Seite {n} ===\n{t}" for n, t in texte)
    msg = client.messages.parse(
        model="claude-opus-5-5", max_tokens=16000, output_config={"effort": "low"},
        messages=[{"role": "user", "content": AUFTRAG + seiten}], output_format=Seitenblock,
    )
    produkte = msg.parsed_output.produkte
    print(f"  Seiten {texte[0][0]}–{texte[-1][0]}: {len(produkte)} Produkte")
    return produkte


def main():
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))
    r = pypdf.PdfReader(str(QUELLE))
    texte = [(i + 1, re.sub(r"[ \t]+", " ", p.extract_text() or "")) for i, p in enumerate(r.pages)]
    bloecke = [texte[i:i + BLOCK] for i in range(0, len(texte), BLOCK)]
    with ThreadPoolExecutor(6) as ex:
        ergebnisse = list(ex.map(lambda b: block(client, b[0], b[1]), enumerate(bloecke)))

    zusammenlegen([p.model_dump() for liste in ergebnisse for p in liste])


# Claude schreibt die Kennung nicht immer gleich ("doterra-air" und "air", "claryCalm" und "claryclam").
TIPPFEHLER = {"claryclam": "clarycalm", "doterra-kids-collection": "kids-collection-kit"}


def kennung(i):
    i = re.sub(r"^doterra-", "", i.lower())
    return TIPPFEHLER.get(i, i)


def zusammenlegen(roh):
    alle = {}
    for d in roh:
        d["id"] = kennung(d["id"])
        if d["id"] in alle:  # zweimal vorgestellt: längeren Text behalten, Punkte vereinen
            a = alle[d["id"]]
            if len(d["katalogtext"]) > len(a["katalogtext"]):
                a["katalogtext"] = d["katalogtext"]
            a["punkte"] = list(dict.fromkeys(a["punkte"] + d["punkte"]))
            a["inhaltsstoffe"] = list(dict.fromkeys(a["inhaltsstoffe"] + d["inhaltsstoffe"]))
        else:
            alle[d["id"]] = d
    # Was im Europa-Katalog fehlt, in Büchern, Enjoils und Convention-Notizen aber vorkommt
    zusatz = json.loads(ZUSATZ.read_text(encoding="utf-8"))["produkte"]
    # Saison- und Aktionsprodukte haben in der Wissensbasis fürs Cockpit schon einen eigenen Text
    wb = {p["id"]: p for p in json.loads(WISSENSBASIS.read_text(encoding="utf-8"))["produkte"]}
    for z in zusatz:
        if z["id"] not in alle:
            w = wb.get(z["id"], {})
            alle[z["id"]] = dict({"groesse": w.get("groesse", ""), "inhaltsstoffe": w.get("inhalt", []),
                                  "katalogtext": " ".join(filter(None, [w.get("kurz"), w.get("kundinnentext")])),
                                  "punkte": w.get("anwendung", []), "seite": 0, "zusatz": True}, **z)
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    produkte = sorted(alle.values(), key=lambda x: (x["kategorie"], x["name"].lower()))
    ZIEL.write_text(json.dumps({"quelle": QUELLE.name, "produkte": produkte}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    from collections import Counter
    print(f"→ {len(produkte)} Produkte in {ZIEL.relative_to(WS)}")
    for k, n in Counter(p["kategorie"] for p in produkte).most_common():
        print(f"   {n:4}  {k}")


if __name__ == "__main__":
    if "--zusammenlegen" in sys.argv:  # nur Kennungen bereinigen, ohne neu zu fragen
        zusammenlegen(json.loads(ZIEL.read_text(encoding="utf-8"))["produkte"])
    else:
        main()
