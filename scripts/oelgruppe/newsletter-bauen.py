"""doTERRA-Monatsnewsletter: Inhalt als JSON -> Mail-HTML, Lesefassung und Cockpit-Dokument.

    python scripts/oelgruppe/newsletter-bauen.py outputs/newsletter/2026-11-doterra.json

-> outputs/newsletter/2026-11-doterra.html · 2026-11-doterra.md (für texte-pruefen.py)
-> outputs/cockpit/abgleich/doterra-freigaben/nl-2026-11.json (Sammlung doterra-freigaben)
Gerüst aus scripts/startklar/mails-bauen.py importiert. Text kommt von /copywriting, Betreff von /ueberschrift.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)


def block(b):
    t = b["typ"]
    if t == "absatz":
        return sk.absatz(b["text"], letzter=b.get("letzter", False))
    if t == "h2":
        return sk.h2(b["text"])
    if t == "knopf":
        return sk.knopf(b["text"], b["ziel"])
    if t == "gruss":
        return sk.gruss(b["text"])
    if t == "ps":
        return sk.ps(b["text"])
    if t == "liste":
        return sk.liste(b.get("kopf"), b["zeilen"])
    if t == "kasten":
        return sk.kasten("".join(sk.P_ENG % z for z in b["zeilen"]), "#fdf1e6", rand=sk.ORANGE,
                         kopf=b.get("kopf"), kopffarbe=sk.ORANGE)
    sys.exit("Unbekannter Block: " + t)


def main():
    quelle = pathlib.Path(sys.argv[1])
    n = json.loads(quelle.read_text(encoding="utf-8"))
    m = {"datei": quelle.with_suffix(".html").name, "marke": "Mum Life Balance", "betreff": n["betreffe"][0],
         "betreff2": n["betreffe"][1], "preheader": n["preheader"], "wann": "nach deiner Freigabe", "notiz": n.get("notiz", ""),
         "h1": n["h1"], "bloecke": [block(b) for b in n["bloecke"]]}
    seite = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "DOTERRA-NEWSLETTER").replace(
        "scripts/startklar/mails-bauen.py", "scripts/oelgruppe/newsletter-bauen.py")
    sk.umlaute_pruefen(m["datei"], seite)
    quelle.with_suffix(".html").write_text(seite, encoding="utf-8")

    zeilen = ["---", "tags: [content, newsletter, doterra]", "---", "", "# " + n["name"], "",
              "**Fokus:** %s · **Quelle:** %s" % (n["fokus"], quelle.name), "", "## Betreffzeilen", ""]
    zeilen += ["%d. %s" % (i + 1, b) for i, b in enumerate(n["betreffe"])]
    zeilen += ["", "**Vorschautext:** " + n["preheader"], "", "## Mail", "", n["h1"], ""]
    for b in n["bloecke"]:
        roh = [b["text"]] if "text" in b else b.get("zeilen", [])
        zeilen += [html.unescape(re.sub(r"<[^>]+>", "", z)) + "\n" for z in roh]
    quelle.with_suffix(".md").write_text("\n".join(zeilen), encoding="utf-8")

    doc = {"art": "newsletter", "monat": n["monat"], "titel": n["name"], "fokus": n["fokus"], "betreffe": n["betreffe"],
           "betreffWahl": 0, "preheader": n["preheader"], "html": seite, "listen": n["listen"], "notiz": n.get("notiz", ""),
           "status": "entwurf", "quelle": str(quelle.resolve().relative_to(ROOT)).replace("\\", "/")}
    ziel = ROOT / "outputs/cockpit/abgleich/doterra-freigaben"
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / ("nl-%s.json" % n["monat"])).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print("✓", quelle.with_suffix(".html").name, len(seite), "Zeichen ->", ziel / ("nl-%s.json" % n["monat"]))


if __name__ == "__main__":
    main()
