"""Anliegen-Bibliothek fürs Cockpit (doTERRA → Anliegen) — die Symptom-Suche über alle Unterlagen.

    python scripts/doterra/anliegen-bauen.py          # bauen (nimmt schon erkannte Scans mit)
    python scripts/doterra/anliegen-bauen.py --ocr    # vorher Scans Seite für Seite erkennen (dauert)

Liest Bücher, E-Books, Enjoils-Hefte, Produktwissen und Ernährungsnotizen, schneidet sie in Abschnitte
und sucht je Anliegen aus context/doTERRA/Produktwissen/anliegen.json die passendsten Stellen heraus —
mit Quelle und Seite. Zählt dazu, welche Öle in diesen Stellen in wie vielen Quellen genannt werden.

Ausgabe: outputs/cockpit/abgleich/oelwissen/anliegen-NN.json (gitignored — Buchauszüge, Repo ist public)
→ ArtifactData batch set, Sammlung "oelwissen", Dokumente "anliegen-NN".

🚨 NUR FÜR PATRICIA. Die Auszüge enthalten Heilaussagen aus den Büchern. Nach aussen geht ausschliesslich
das Feld 'kundinnen' aus anliegen.json.
Scans ohne Textebene (Essential-Emotion-Handbücher, Enjoils, Praxis-Aromatherapie …) liest die in Windows
eingebaute Texterkennung (ocr-windows.ps1). Die Seiten liegen als Bild + Text im Zwischenspeicher
outputs/cockpit/abgleich/ocr/ (gitignored) und werden nur einmal erkannt.
"""
import json
import logging
import pathlib
import re
import sys
import zipfile
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
logging.getLogger("pypdf").setLevel(logging.ERROR)
import pypdf  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
ANLIEGEN = WS / "context/doTERRA/Produktwissen/anliegen.json"
ZIEL = WS / "outputs/cockpit/abgleich/oelwissen"
ORTE = [WS / "context/doTERRA", WS / "context/persoenlich/ernaehrungswissen", WS / "kochwissen"]

# Was nicht in die Gesundheits-Suche gehört (Business, Vorlagen, Rezepte, Etiketten)
RAUS = re.compile(r"policy-manual|business-building|gopro|spiritual-leadership|ideen mastermind|rangplaner|"
                  r"br_|etikett|/rezepte/|business companion|swap mirella|direktverkauf|treueprogramm|"
                  r"5-kunden|brand dna|analyse zg|transkript-mit-zeitstempeln|/testwoche/|/kalender/|"
                  r"/freebie/|/oilmates/|scan –", re.I)

KATEGORIE = [
    (re.compile(r"perimenopause|wechseljahr|frauengesundheit|hormon", re.I), "Hormone"),
    (re.compile(r"protein|basen|mikronähr|mikronaehr|omega|moringa|ernaehrungswissen|kochwissen|ernährung", re.I), "Ernährung"),
    (re.compile(r"organuhr", re.I), "Rhythmus"),
    (re.compile(r"energieheilung|seele|emotion|energiearbeit", re.I), "Gemüt"),
]

OELE = ["Lavendel", "Pfefferminz", "Zitrone", "Weihrauch", "Teebaum", "Oregano", "Eukalyptus", "On Guard",
        "Breathe", "Air", "DigestZen", "ZenGest", "Deep Blue", "Balance", "Serenity", "Copaiba", "Kopaiba",
        "Wild Orange", "Orange", "Rosmarin", "Kamille", "Geranie", "Muskatellersalbei", "Clary Sage",
        "Ylang Ylang", "Zedernholz", "Vetiver", "Majoran", "Thymian", "Zimt", "Nelke", "Gewürznelke", "Ingwer",
        "Fenchel", "Basilikum", "Myrrhe", "Sandelholz", "Bergamotte", "Grapefruit", "Limette", "Rose",
        "Melisse", "Neroli", "Helichrysum", "Strohblume", "Ravintsara", "Kardamom", "Koriander", "Wintergrün",
        "Zypresse", "Tanne", "Fichte", "ClaryCalm", "PastTense", "Adaptiv", "Elevation", "Cheer", "Console",
        "Peace", "Purify", "TerraShield", "Whisper", "InTune", "Arise", "Zendocrine", "Thinker", "Steady",
        "Petitgrain", "Patchouli", "Spearmint", "Grüne Minze", "Kurkuma", "Schwarzer Pfeffer", "Blue Tansy",
        "Blauer Rainfarn", "Arborvitae", "Douglasie", "Wacholder", "Salbei", "Palmarosa", "Jasmin", "Tangerine",
        "Mandarine", "Bergamotte", "Lemongrass", "Zitronengras", "Melaleuca", "AromaTouch", "Citrus Bliss",
        "Frankincense", "Lavender", "Peppermint", "Lemon", "Tea Tree", "Cinnamon", "Clove", "Ginger"]
# englisch → deutsch, damit eine Quelle nicht doppelt zählt
GLEICH = {"Frankincense": "Weihrauch", "Lavender": "Lavendel", "Peppermint": "Pfefferminz", "Lemon": "Zitrone",
          "Tea Tree": "Teebaum", "Melaleuca": "Teebaum", "Cinnamon": "Zimt", "Clove": "Gewürznelke",
          "Nelke": "Gewürznelke", "Ginger": "Ingwer", "Kopaiba": "Copaiba", "Clary Sage": "Muskatellersalbei",
          "ZenGest": "DigestZen", "Air": "Breathe", "Strohblume": "Helichrysum", "Blauer Rainfarn": "Blue Tansy",
          "Zitronengras": "Lemongrass", "Grüne Minze": "Spearmint", "Orange": "Wild Orange"}
OEL_RE = [(o, re.compile(r"(?<![\wäöü])" + re.escape(o) + (r"e?\b" if o != "Air" else r"\b"),
                          re.I if o not in ("Air", "Rose", "Peace", "Balance", "Cheer", "Steady") else 0))
          for o in dict.fromkeys(OELE)]

MAX_JE_QUELLE = 3
MAX_JE_ANLIEGEN = 24
ABSCHNITT = 750
OCR = WS / "outputs/cockpit/abgleich/ocr"


def norm(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)


def kategorie(pfad):
    for rx, k in KATEGORIE:
        if rx.search(pfad):
            return k
    return "Öle"


def titel(p):
    t = re.sub(r"_\d{10,}.*$|\(\d\)|\[\d\]|~\d", "", p.stem)
    return re.sub(r"[_]+", " ", t).strip(" -")


def docx_text(p):
    with zipfile.ZipFile(p) as z:
        x = z.read("word/document.xml").decode("utf-8", "ignore")
    x = re.sub(r"</w:p>", "\n", x)
    return re.sub(r"<[^>]+>", "", x)


def seiten(p):
    """Liefert [(seite oder Überschrift, text)]."""
    suf = p.suffix.lower()
    if suf == ".pdf":
        r = pypdf.PdfReader(str(p))
        teile = [("S. %d" % (i + 1), (pg.extract_text() or "")) for i, pg in enumerate(r.pages)]
        if sum(len(t) for _, t in teile) >= 300:
            return teile
        ordner = OCR / ocr_name(p)
        return [("S. %d" % int(f.stem), f.read_text(encoding="utf-8-sig", errors="ignore"))
                for f in sorted(ordner.glob("*.txt"))] if ordner.exists() else teile
    text = docx_text(p) if suf == ".docx" else p.read_text(encoding="utf-8", errors="ignore")
    teile, ueb, puffer = [], "", []
    for zeile in text.splitlines():
        m = re.match(r"#{1,4}\s+(.+)", zeile)
        if m:
            if puffer:
                teile.append((ueb, "\n".join(puffer)))
            ueb, puffer = m.group(1).strip()[:80], []
        else:
            puffer.append(zeile)
    if puffer:
        teile.append((ueb, "\n".join(puffer)))
    return teile


def ocr_name(p):
    return norm(str(p.relative_to(WS)))[-60:]


def ocr_vorbereiten(dateien):
    """Rendert die Seiten der Scans als Bild und lässt die Windows-Texterkennung laufen."""
    import subprocess
    import pypdfium2
    neu = 0
    for p in dateien:
        if p.suffix.lower() != ".pdf":
            continue
        r = pypdf.PdfReader(str(p))
        if sum(len(pg.extract_text() or "") for pg in r.pages[:4]) > 200:
            continue
        ordner = OCR / ocr_name(p)
        ordner.mkdir(parents=True, exist_ok=True)
        try:
            doc = pypdfium2.PdfDocument(str(p))
        except Exception as e:
            print("  ⚠️  nicht renderbar:", p.name, e)
            continue
        for i in range(len(doc)):
            png = ordner / ("%04d.png" % (i + 1))
            if png.exists() or png.with_suffix(".txt").exists():
                continue
            try:
                img = doc[i].render(scale=2.2).to_pil()
            except Exception:
                continue
            img.thumbnail((2600, 2600))
            img.save(png)
            neu += 1
        print("  Seiten bereit:", p.name, len(doc))
    print("Neue Seiten zum Erkennen:", neu)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File",
                    str(WS / "scripts/doterra/ocr-windows.ps1"), str(OCR)], check=True)
    for png in OCR.rglob("*.png"):  # Bild weg, sobald der Text da ist
        if png.with_suffix(".txt").exists():
            png.unlink()


def abschnitte(teile):
    for wo, text in teile:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"-\n(?=[a-zäöü])", "", text)
        absaetze = [a.strip().replace("\n", " ") for a in re.split(r"\n\s*\n|\n(?=[A-ZÄÖÜ•\-–])", text) if a.strip()]
        # 🚨 Manche Bücher kommen ohne Absätze — ein „Absatz“ ist dann ein ganzes Kapitel und gewinnt
        #    jedes Anliegen, weil darin alles vorkommt. Lange Absätze werden an Satzgrenzen geteilt.
        kurz = []
        for a in absaetze:
            if len(a) <= ABSCHNITT:
                kurz.append(a)
                continue
            satz = ""
            for s in re.split(r"(?<=[.!?])\s+", a):
                if len(satz) + len(s) > ABSCHNITT and satz:
                    kurz.append(satz.strip())
                    satz = ""
                satz += " " + s
            if satz.strip():
                kurz.append(satz.strip()[:ABSCHNITT * 2])
        absaetze = kurz
        stueck = ""
        for a in absaetze:
            if len(stueck) + len(a) > ABSCHNITT and stueck:
                yield wo, stueck.strip()
                stueck = ""
            stueck += " " + a
        if stueck.strip():
            yield wo, stueck.strip()


def quellen():
    gesehen_md = set()
    dateien = []
    for ort in ORTE:
        if not ort.exists():
            continue
        for p in sorted(ort.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in (".pdf", ".md", ".txt", ".docx"):
                continue
            rel = str(p.relative_to(WS)).replace("\\", "/")
            if RAUS.search("/" + rel.lower()):
                continue
            if "kochwissen" in rel and p.parent != WS / "kochwissen":
                continue
            dateien.append(p)
            if p.suffix.lower() == ".md":
                gesehen_md.add(norm(titel(p))[:14])
    # PDF/MD-Dubletten: das Markdown gewinnt (sauberer Text)
    raus = []
    for p in dateien:
        if p.suffix.lower() == ".pdf" and any(k and k in norm(p.stem) for k in gesehen_md):
            continue
        raus.append(p)
    # Inhaltsgleiche Dateien (gleicher Titel in doTERRA/wissen und kochwissen)
    eindeutig, namen = [], set()
    for p in raus:
        k = norm(titel(p))
        if k in namen:
            continue
        namen.add(k)
        eindeutig.append(p)
    return eindeutig


def main():
    anl = json.loads(ANLIEGEN.read_text(encoding="utf-8"))["anliegen"]
    muster = {a["id"]: [re.compile(r"(?<![\wäöü])" + re.escape(s.strip()), re.I) for s in a["suche"]] for a in anl}

    alle, leer = [], []
    if "--ocr" in sys.argv:
        ocr_vorbereiten(quellen())
    for p in quellen():
        rel = str(p.relative_to(WS)).replace("\\", "/")
        try:
            teile = seiten(p)
        except Exception as e:  # kaputte Datei überspringen, aber melden
            print("  ⚠️  nicht lesbar:", rel, e)
            continue
        zeichen = sum(len(t) for _, t in teile)
        if zeichen < 300:
            leer.append(rel)
            continue
        q = {"titel": titel(p), "kat": kategorie(rel), "pfad": rel}
        for wo, text in abschnitte(teile):
            if re.search(r"transkript", wo, re.I):  # Gesprochenes: viel Wort, wenig Inhalt
                continue
            if len(text) > 120:
                alle.append((q, wo, text))
    print("Abschnitte:", len(alle), "aus", len({id(a[0]) for a in alle}), "Quellen")

    ZIEL.mkdir(parents=True, exist_ok=True)
    for f in ZIEL.glob("anliegen-*.json"):
        f.unlink()

    ergebnis = []
    for a in anl:
        treffer = []
        for q, wo, text in alle:
            n = sum(len(m.findall(text)) for m in muster[a["id"]])
            if not n:
                continue
            oele = {GLEICH.get(o, o) for o, rx in OEL_RE if rx.search(text)}
            treffer.append((n * (1 + 0.25 * min(len(oele), 4)), q, wo, text, oele))
        treffer.sort(key=lambda x: -x[0])

        # Öle: in wie vielen QUELLEN wird ein Öl im Zusammenhang mit dem Anliegen genannt
        oel_quellen = defaultdict(set)
        for _, q, _, _, oele in treffer:
            if q["kat"] in ("Öle", "Gemüt", "Hormone"):
                for o in oele:
                    oel_quellen[o].add(q["titel"])
        oele_top = sorted(oel_quellen.items(), key=lambda x: (-len(x[1]), x[0]))[:12]

        je_q, stellen, gesehen = defaultdict(int), [], set()
        for s, q, wo, text, oele in treffer:
            if je_q[q["titel"]] >= MAX_JE_QUELLE:
                continue
            fp = norm(text)[:160]  # dasselbe Buch unter zwei Dateinamen
            if fp in gesehen:
                continue
            gesehen.add(fp)
            je_q[q["titel"]] += 1
            stellen.append({"q": q["titel"], "k": q["kat"], "w": wo, "t": text[:ABSCHNITT + 150],
                            "o": sorted(oele)[:8]})
            if len(stellen) >= MAX_JE_ANLIEGEN:
                break
        ergebnis.append({"id": a["id"], "name": a["name"], "gruppe": a["gruppe"], "kundinnen": a["kundinnen"],
                         "quellen_gesamt": len({t[1]["titel"] for t in treffer}),
                         "oele": [{"oel": o, "n": len(qs), "quellen": sorted(qs)[:6]} for o, qs in oele_top],
                         "stellen": stellen})
        print("  %-30s %3d Stellen aus %2d Quellen · Öle: %s" % (
            a["name"], len(treffer), len({t[1]['titel'] for t in treffer}),
            ", ".join("%s %d" % (o, len(qs)) for o, qs in oele_top[:5])))

    # In Dokumente unter 230 KB teilen
    docs, aktuell = [], []
    for e in ergebnis:
        probe = aktuell + [e]
        if aktuell and len(json.dumps({"items": probe}, ensure_ascii=False).encode()) > 230_000:
            docs.append(aktuell)
            aktuell = [e]
        else:
            aktuell = probe
    if aktuell:
        docs.append(aktuell)
    for i, d in enumerate(docs, 1):
        (ZIEL / ("anliegen-%02d.json" % i)).write_text(
            json.dumps({"items": d, "stand": __import__("datetime").date.today().isoformat()}, ensure_ascii=False),
            encoding="utf-8")
    print("→ %d Dokumente in %s" % (len(docs), ZIEL.relative_to(WS)))
    if leer:
        print("⚠️  Ohne Text (noch nicht erkannt → --ocr):", len(leer))
        for x in leer:
            print("    ", x)


if __name__ == "__main__":
    main()
