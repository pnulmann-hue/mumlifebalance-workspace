"""Öl-App — die offiziellen Produktfotos aus dem doTERRA Europe Digital Marketing Kit holen.

    python scripts/oel-app/fotos-holen.py            # nur fehlende
    python scripts/oel-app/fotos-holen.py --zeigen   # nur anzeigen, was zugeordnet würde

Quelle: share.doterra.com/v/Europe (Canto-Bilddatenbank, ohne Anmeldung lesbar). Unter „Product
Information“ liegt je Produkt ein Ordner mit der freigestellten Flasche als PNG („Wild Orange 15ml.png“),
daneben Studio- und Stimmungsbilder. Genommen wird nur die freigestellte Flasche.
Patricia hat das Herunterladen am 22.10.2026 freigegeben („Ja, alle Produktfotos“).

Ausgabe: outputs/oel-app/roh/fotos/<kennung>.png (Original, gitignored) — fotos-bauen.py macht daraus
die kleinen Bilder für die App.
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WS = pathlib.Path(__file__).resolve().parents[2]
KATALOG = WS / "outputs/oel-app/daten/katalog.json"
ZUSATZ = WS / "context/doTERRA/Produktwissen/oel-app-zusatzprodukte.json"
ZIEL = WS / "outputs/oel-app/roh/fotos"
BASIS = "https://share.doterra.com/"
PRODUKTINFO = "RI6TT/"   # Ordner „Product Information“ — alles andere sind Länderkopien und Aktionen
KOPF = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}


def holen(url, json_=True):
    req = urllib.request.Request(url if url.startswith("http") else BASIS + url, headers=KOPF)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r) if json_ else r.read()


def falten(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("ō", "o")):
        s = s.replace(a, b)
    s = re.sub(r"d[oō]terra|™|®|\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]", "", s)


def kern(name):
    """„Wild Orange 15ml.png“ → wildorange · „Lavender Touch 10ml.png“ → lavendertouch"""
    n = re.sub(r"\.(png|jpe?g)$", "", name, flags=re.I)
    # die Bilddatenbank hat mehrere Namensmuster nebeneinander:
    # „Basil 15 mL-Essential Oils-Product Image-Transparent-EU Market-PNG-v1“ · „Thyme_15ml“ · „EU_Deep Blue Stick“
    n = re.sub(r"-Essential Oils-.*$|-Product Image.*$", "", n)
    n = re.sub(r"^EU_|_\d{6}(_\d)?$|_?(NEW|nobook).*$", "", n).replace("_", " ")
    n = n.replace("Chamomille", "Chamomile")
    n = re.sub(r"\b\d+(\.\d+)?\s?(ml|g|oz|ct|count)\b|\broll[- ]?on\b|\bnew\b|\bsilo\b|\bfront\b", "", n, flags=re.I)
    return falten(n)


def main():
    produkte = json.loads(KATALOG.read_text(encoding="utf-8"))["produkte"]
    alias = json.loads(ZUSATZ.read_text(encoding="utf-8"))["namen"]
    namen = {}
    for p in produkte:
        for n in (p["name"], p.get("deutsch", ""), p["id"].replace("-", " ")):
            if len(falten(n)) >= 3:
                namen.setdefault(falten(n), p["id"])
    for n, i in alias.items():
        namen.setdefault(falten(n), i)

    # alle PNG der Bilddatenbank, seitenweise
    treffer, start = [], 0
    while True:
        h = holen(f"rest/v/Europe/search?keyword=png&start={start}&limit=500")["hits"]
        treffer += h["hit"]
        start += len(h["hit"])
        if not h["hit"] or start >= h["found"]:
            break
    pngs = [x for x in treffer if x["displayName"].lower().endswith(".png")
            and any(c.startswith(PRODUKTINFO) for c in x["data"].get("contained_by", []))]
    print(f"{len(treffer)} PNG insgesamt, {len(pngs)} unter „Product Information“")

    # je Produkt das schlichteste Bild: ohne „Studio“, „LS“, Nummern, Gruppenbilder
    wahl = {}
    for x in pngs:
        name = x["displayName"]
        # 🚨 geprüft am Namen OHNE den langen Anhang — „…-PNG-v1.png“ endet sonst auf eine Ziffer und fällt raus
        kurz = re.sub(r"-Essential Oils-.*$|-Product Image.*$", "", name)
        if re.search(r"studio|\bls\b|group|model|style|counter|slice|reflection|\d+\.png$|lifestyle|banner", kurz, re.I):
            continue
        k = kern(name)
        i = namen.get(k)
        if not i and k.endswith("touch") and namen.get(k[:-5]):  # „Rescuer Touch“ für das Kinder-Öl Rescuer
            i = namen[k[:-5]]
        if not i:
            continue
        rang = len(name)  # kürzester Name ist meist die nackte Flasche
        if i not in wahl or rang < wahl[i][0]:
            wahl[i] = (rang, name, x["data"]["uri"][0])
    # Öle, die es dort nur als Touch-Roller gibt (Neroli, Manuka): dessen Foto nehmen
    for p in produkte:
        if p["id"] not in wahl and f"{p['id']}-touch" in wahl:
            wahl[p["id"]] = wahl[f"{p['id']}-touch"]
    print(f"zugeordnet: {len(wahl)} von {len(produkte)} Produkten")
    ohne = [p["id"] for p in produkte if p["id"] not in wahl]
    print("ohne Foto:", ", ".join(ohne[:60]), "…" if len(ohne) > 60 else "")
    if "--zeigen" in sys.argv:
        for i, (_, name, _) in sorted(wahl.items()):
            print(f"  {i:34} ← {name}")
        return

    ZIEL.mkdir(parents=True, exist_ok=True)
    neu = 0
    for i, (_, name, uri) in sorted(wahl.items()):
        ziel = ZIEL / f"{i}.png"
        if ziel.exists():
            continue
        try:
            ziel.write_bytes(holen(uri, json_=False))
            neu += 1
            print(f"  ✓ {i:34} {name}")
        except Exception as e:
            print(f"  ❌ {i}: {e}")
        time.sleep(0.4)
    print(f"→ {neu} neu geladen nach {ZIEL.relative_to(WS)}")


if __name__ == "__main__":
    main()
