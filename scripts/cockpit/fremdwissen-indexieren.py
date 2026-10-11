"""
Macht fremdes Kursmaterial auffindbar, ohne es abzuschreiben.

Patricias Wunsch: „wäre geil, wenn ich beim Suchfeld eine Verlinkung zum Inhalt
von Julia oder sonst einem Kurs hätte, wenn ich mal was suche."

Deshalb steht hier bewusst **kein** Inhalt, sondern ein Wegweiser: Kursname,
Datei, Seitenzahl und eine kurze Zeile zum Wiedererkennen. Damit findet man die
Stelle und schlaegt sie im Original nach — so, wie man in einem Buch ein
Register benutzt.

Jeder Eintrag ist als fremd gekennzeichnet. Das ist nicht Kosmetik: was hier
steht, darf nie in einem Kundendokument landen.

Aufruf:
  python scripts/cockpit/fremdwissen-indexieren.py [zielordner]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Wie der Ordner heisst → wie die Quelle im Cockpit genannt wird.
QUELLEN = {
    "julia-trost": "Julia Trost",
    "Elke": "Elke",
    "Karriere Mum": "Karriere Mum",
    "Nadja": "Nadja",
    "Networkmarketing-Training": "Network-Training",
    "Workbookkurs": "Workbookkurs",
    "Brandastic": "Brandastic",
    "hormozi": "Hormozi",
}

# So kurz, dass es ein Wegweiser bleibt und keine Kopie wird.
ZEILE = 110
MAX_SEITEN = 80


def quelle_von(rel):
    for ordner, name in QUELLEN.items():
        if "/%s/" % ordner in rel or rel.startswith("reference/%s/" % ordner):
            return name
    # Ordnernamen wie „Nadja Grunenberg_Stroys, Content" sind Ablage-Namen,
    # keine Quellenangaben — bis zum ersten Trennzeichen reicht.
    teile = rel.split("/")
    name = teile[1] if len(teile) > 1 else "Fremd"
    return re.split(r"[_,(]", name)[0].strip()


def erste_zeile(text):
    """Die erste sinnvolle Zeile einer Seite — dient dem Wiedererkennen."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) < 25:
        return ""
    return text[:ZEILE]


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf fehlt: pip install pypdf")

    dateien = sorted(p for p in (ROOT / "reference").rglob("*.pdf")
                     if "private" not in p.as_posix()
                     and "persoenlich" not in p.as_posix())
    print("  %d fremde PDFs" % len(dateien))

    eintraege, gelesen, fehler = [], 0, 0
    for n, f in enumerate(dateien, 1):
        rel = f.relative_to(ROOT).as_posix()
        quelle = quelle_von(rel)
        try:
            r = PdfReader(f)
        except Exception:
            fehler += 1
            continue
        gelesen += 1
        for seite in range(min(len(r.pages), MAX_SEITEN)):
            try:
                zeile = erste_zeile(r.pages[seite].extract_text())
            except Exception:
                continue
            if not zeile:
                continue
            eintraege.append({
                "d": rel,
                "t": "%s · S. %d" % (f.stem[:70], seite + 1),
                "a": zeile,
                "b": "Fremd · " + quelle,
            })
        if n % 25 == 0:
            print("    %d von %d …" % (n, len(dateien)))

    # In Haeppchen unter 256 KB
    proTeil = 500
    teile = [eintraege[i:i + proTeil] for i in range(0, len(eintraege), proTeil)]
    heute = date.today().isoformat()
    for nr, teil in enumerate(teile):
        (ziel / ("fremd-%02d.json" % nr)).write_text(
            json.dumps({"teil": nr, "items": teil, "stand": heute},
                       ensure_ascii=False), encoding="utf-8")

    groesse = sum((ziel / ("fremd-%02d.json" % n)).stat().st_size
                  for n in range(len(teile)))
    print("\n  %d Fundstellen aus %d Dateien (%d unlesbar)"
          % (len(eintraege), gelesen, fehler))
    print("  %d Teildateien, zusammen %.1f MB" % (len(teile), groesse / 1e6))
    print("\nAbgelegt in: %s" % ziel.resolve())


if __name__ == "__main__":
    main()
