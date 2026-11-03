"""Patricias eigenes Kurswissen fürs Cockpit (31.10.2026).

Der Upsell-Ersteller baut für jedes vorgeschlagene KI-Tool einen fertigen
Bauplan (System-Prompt, Ablauf, Auftrag für Claude Code). Das Wissen darin soll
zuerst aus Patricias EIGENEN Kursen kommen — Patricia: *„logischerweise mit
meinem wissensmaterial z.B. contentsäulen-planer bei upsell magnet-ich“*.
Eine Artifact-Seite kommt nicht an `context/`, deshalb landen die Transkripte
als Sammlung `eigenwissen` in der Cockpit-Datenbank.

Nur ihre eigenen Kurse. Fremde Kurse (Content-Shortcut, Jenya, Kevin,
Schmetterlingsmethode) bleiben draussen. Ordner mit `_` sind Archiv.

    python scripts/cockpit/eigenwissen-bauen.py [zielordner]
    # danach: ArtifactData batch set -> Sammlung "eigenwissen"
"""

import json
import pathlib
import re
import sys
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
KURSE = ROOT / "context" / "Kurse" / "aktuelle kurse"
EIGENE = [
    ("digitale-produktwelt", "Digitale Produktwelt"),
    ("finde-dein-thema", "Finde dein Thema als Network-Mama in 60 Minuten"),
    ("instagram-kundenmaschine", "Instagram Kundenmaschine"),
    ("eigenes-produkt", "Vom Network-Wissen zum eigenen Produkt"),
    ("mama-ceo", "Mama-CEO"),
    ("startklar", "Startklar"),
    ("easy-ki", "Easy-KI"),
    ("expertin", "Expertin statt Verkäuferin"),
]
GRUNDLAGEN = [ROOT / "context" / "patricia-expertise.md", ROOT / "context" / "patricia-freebies.md"]
STUECK = 180_000  # Zeichen je Dokument, die Datenbank nimmt höchstens 256 KB


def lesen(pfad):
    t = pfad.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"\r\n?", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def main():
    ziel = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "cockpit" / "abgleich"
    ziel = ziel / "eigenwissen"
    ziel.mkdir(parents=True, exist_ok=True)
    for alt in ziel.glob("*.json"):
        alt.unlink()

    quellen = [("grundlagen", "Patricias Kurse und Freebies im Überblick",
                [p for p in GRUNDLAGEN if p.exists()])]
    for slug, ordner in EIGENE:
        d = KURSE / ordner
        dateien = sorted(p for p in d.rglob("*")
                         if p.suffix in (".txt", ".md") and not any(t.startswith("_") for t in p.relative_to(d).parts))
        if dateien:
            quellen.append((slug, ordner, dateien))

    index = {"stand": date.today().isoformat(), "kurse": []}
    gesamt = 0
    for slug, name, dateien in quellen:
        text = "\n\n".join("# " + p.stem.replace("-", " ") + "\n\n" + lesen(p) for p in dateien)
        teile = [text[i:i + STUECK] for i in range(0, len(text), STUECK)] or [""]
        for n, stueck in enumerate(teile, 1):
            (ziel / f"{slug}-{n}.json").write_text(
                json.dumps({"md": stueck}, ensure_ascii=False), encoding="utf-8")
        index["kurse"].append({"id": slug, "name": name, "teile": len(teile), "zeichen": len(text)})
        gesamt += len(text)
        print(f"  {name}: {len(dateien)} Dateien, {len(text):,} Zeichen, {len(teile)} Teil(e)")
    (ziel / "_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(index['kurse'])} Quellen, {gesamt:,} Zeichen -> {ziel}")


if __name__ == "__main__":
    main()
