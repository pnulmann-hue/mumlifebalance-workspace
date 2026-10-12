"""Zielgruppe & Markt fürs Cockpit — die Content-Shortcut-Analysen als ein Dokument.

Patricia am 12.10.2026: *„wäre cool wenn du mir die ergebnisse aus zielgruppe,
nische, wettbewerbsanalyse und den contentsäulen auch im cockpit ablegen
könntest"*.

Liest die fünf Markdown-Dateien aus
`outputs/zielgruppen-research/2026-10-12-content-shortcut/` und schreibt
`zielgruppe.json` — danach `ArtifactData set` → Sammlung `daten`, Dokument
`zielgruppe`. Das Cockpit zeigt es unter **Instagram → Zielgruppe & Markt**
(`patch-zielgruppe.py`).

🚨 **Die Quelle ist das Markdown, nicht das Cockpit.** Ändert sich eine Analyse,
die Datei ändern und das Skript neu laufen lassen. Das Dokument ist eine
erzeugte Kopie, der Abgleich darf es nicht schreiben.

    python scripts/cockpit/zielgruppe-bauen.py [zielordner]
"""

import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs/zielgruppen-research/2026-10-12-content-shortcut"

TEILE = [
    ("blick", "Auf einen Blick: Säulen und deine Themen",
     "Wie die fünf Säulen der Analyse auf deine Themen passen, was du vor einem Hook prüfen solltest, die vier stärksten Befunde.",
     "2026-10-12-saeulen-abgleich.md"),
    ("zielgruppe", "Zielgruppe",
     "Persona, Kern-Pain, Gedanken in der Nacht, Sprache, Sehnsüchte, Einwände, Formate und die fünf Content-Säulen mit Hook-Ideen.",
     "2026-10-12-zielgruppenanalyse-network-mamas.md"),
    ("fragen", "Fragen und Sprache",
     "Was sie googelt, 24 konkrete Fragen mit Content-Idee, Pain-Points, Einwände, Caption-Bausteine.",
     "2026-10-12-zielgruppen-fragen-analyse.md"),
    ("wettbewerb", "Wettbewerb",
     "Vier Konten im Vergleich: Themen, Hook-Stile, Formate, was trägt, wo deine Lücke liegt, Hook-Bank.",
     "2026-10-12-instagram-wettbewerbsanalyse.md"),
    ("trends", "Nische und Trends",
     "Marktlage in Zahlen, was wächst, was bleibt, was ausläuft, acht Themen für die nächsten Wochen.",
     "2026-10-12-nischen-trendanalyse.md"),
]


def ohne_kopf(text):
    """Frontmatter weg — im Cockpit liest das niemand."""
    if text.startswith("---\n"):
        ende = text.find("\n---\n", 4)
        if ende >= 0:
            text = text[ende + 5:]
    return text.strip() + "\n"


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs/cockpit/abgleich"
    ziel.mkdir(parents=True, exist_ok=True)
    teile = []
    for tid, titel, kurz, datei in TEILE:
        p = QUELLE / datei
        if not p.exists():
            sys.exit("🚨 Fehlt: %s" % p)
        md = ohne_kopf(p.read_text(encoding="utf-8"))
        # Die H1 steht schon als Titel auf der Karte.
        md = re.sub(r"\A# [^\n]*\n+", "", md)
        teile.append({"id": tid, "titel": titel, "kurz": kurz, "datei": datei, "md": md})
        print("  %-11s %6d Zeichen" % (tid, len(md)))
    doc = {
        "stand": "2026-10-12",
        "naechste_pruefung": "Januar 2027",
        "quelle": "Content-Shortcut-Analysen, outputs/zielgruppen-research/2026-10-12-content-shortcut/",
        "teile": teile,
    }
    raus = ziel / "zielgruppe.json"
    roh = json.dumps(doc, ensure_ascii=False)
    if len(roh.encode("utf-8")) > 250_000:
        sys.exit("🚨 Dokument über 250 KB — die Datenbank nimmt höchstens 256 KB.")
    raus.write_text(roh, encoding="utf-8")
    print("→ %s (%d KB)" % (raus, len(roh.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
