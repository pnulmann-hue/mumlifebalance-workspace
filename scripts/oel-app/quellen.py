"""Öl-App — alle Unterlagen als durchsuchbare Abschnitte (gemeinsam für Produkte, Themen und Tipps).

Nimmt den Leser aus scripts/doterra/anliegen-bauen.py (Bücher, Enjoils, Ölschule, Emotions-Handbücher,
Produktwissen, Ernährungsnotizen — Scans über den OCR-Zwischenspeicher) und ergänzt die E-Books im
epub-Format, die der Cockpit-Leser auslässt. Ergebnis wird in outputs/oel-app/roh/abschnitte.json
zwischengespeichert; --neu baut neu.

🚨 NUR FÜR PATRICIA — Buchtext. Alles unter outputs/oel-app/ ist gitignored.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys
import zipfile

WS = pathlib.Path(__file__).resolve().parents[2]
CACHE = WS / "outputs/oel-app/roh/abschnitte.json"

_spec = importlib.util.spec_from_file_location("anliegen", WS / "scripts/doterra/anliegen-bauen.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)


def epub_teile(p):
    """[(Kapitel, text)] aus einem epub — je XHTML-Datei ein Teil, in Lesereihenfolge."""
    with zipfile.ZipFile(p) as z:
        namen = [n for n in z.namelist() if n.lower().endswith((".xhtml", ".html", ".htm"))]
        opf = next((n for n in z.namelist() if n.endswith(".opf")), None)
        if opf:  # Reihenfolge aus dem Inhaltsverzeichnis
            o = z.read(opf).decode("utf-8", "ignore")
            ids = dict(re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', o))
            ids.update({k: v for v, k in re.findall(r'<item[^>]*href="([^"]+)"[^>]*id="([^"]+)"', o)})
            basis = opf.rsplit("/", 1)[0] + "/" if "/" in opf else ""
            reihe = [basis + ids[i] for i in re.findall(r'<itemref[^>]*idref="([^"]+)"', o) if i in ids]
            namen = [n for n in reihe if n in z.namelist()] or namen
        teile = []
        for n in namen:
            x = z.read(n).decode("utf-8", "ignore")
            ueb = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", x, re.S)
            x = re.sub(r"</(p|div|h\d|li)>", "\n\n", x)
            x = html.unescape(re.sub(r"<[^>]+>", "", x))
            wo = re.sub(r"<[^>]+>|\s+", " ", ueb.group(1)).strip()[:80] if ueb else n.rsplit("/", 1)[-1]
            teile.append((wo, x))
    return teile


def abschnitte(neu=False):
    """Liste von {q: Titel, k: Kategorie, p: Pfad, w: Seite/Kapitel, t: Text}."""
    if CACHE.exists() and not neu:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    dateien = A.quellen() + sorted((WS / "context/doTERRA").rglob("*.epub"))
    alle, leer = [], []
    for p in dateien:
        rel = str(p.relative_to(WS)).replace("\\", "/")
        try:
            teile = epub_teile(p) if p.suffix.lower() == ".epub" else A.seiten(p)
        except Exception as e:
            print("  ⚠️  nicht lesbar:", rel, e)
            continue
        if sum(len(t) for _, t in teile) < 300:
            leer.append(rel)
            continue
        q = A.titel(p)
        m = re.match(r"(\d{4})-(\d\d)-(\d\d)", q)
        if "academy-oel-schule" in rel and m:  # Dateien heissen nur nach Datum
            q = f"Öl-Schule Academy {m.group(3)}.{m.group(2)}.{m.group(1)}"
        for wo, text in A.abschnitte(teile):
            if re.search(r"transkript", wo, re.I) or len(text) <= 120:
                continue
            alle.append({"q": q, "k": A.kategorie(rel), "p": rel, "w": wo, "t": text})
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(alle, ensure_ascii=False), encoding="utf-8")
    print(f"Abschnitte: {len(alle)} aus {len({a['p'] for a in alle})} Quellen · ohne Text: {len(leer)}")
    for x in leer:
        print("    ohne Text:", x)
    return alle


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    abschnitte(neu=True)
