"""Wissensbibliothek fürs Cockpit — die Kurs-Learnings nach Thema (27.10.2026).

Patricia: *„vielleicht könnte man direkt im cockpit die wissensbibliothek anpassen
vielleicht pro Thema. Dann das Wissensebook wo die Learnings zum Thema drin sind
und die PDFS dazu mitabgelegt?"* · *„du kannst den link zum workbook einfügen"*.

Liest
  reference/julia-trost/learnings/*.md            je Kurs die vollständigen Learnings
  reference/julia-trost/learnings/_unterlagen.json  Unterlagen je Thema (Drive-Links)
und schreibt nach outputs/cockpit/abgleich/bibliothek/:
  _index.json        Themen, Kurse, Unterlagen        -> bibliothek/_index
  k-<kurs>-<n>.json  der Text, in Stücke unter 200 KB -> bibliothek/k-<kurs>-<n>

Danach `ArtifactData batch set` in die Sammlung `bibliothek` des Cockpits.
Der Reiter steht unter Produkte -> Wissensbibliothek (`patch-bibliothek.py`).

🚨 Gekauftes Fremdmaterial. Alle Quellen und die Ausgabe sind gitignored, und das
Cockpit muss auf privat stehen, bevor die Dokumente hochgehen.
🚨 Die Quelle ist das Markdown — ändert sich ein Kurs, Datei ändern, Skript neu.

    python scripts/cockpit/bibliothek-bauen.py
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
QUELLE = ROOT / "reference/julia-trost/learnings"
# Learnings anderer Mentorinnen (seit 29.10.2026: Laura Hersche, Mia Pejic). Sie
# landen als Kurse in den Themen, aber nicht in Julias Themenbüchern. Der Name der
# Mentorin steht im Titel („Laura Hersche · …“). Ebenfalls gitignored.
WEITERE = ROOT / "reference/mentorinnen/learnings"
ZIEL = ROOT / "outputs/cockpit/abgleich/bibliothek"
STUECK = 200_000  # Zeichen je Dokument; die Datenbank nimmt höchstens 256 KB

# Die Business-Schritte aus plans/2026-10-27-julia-kurs-learnings.md, Phase 4.
# `woerter` muss im Kopf der Learnings-Datei vorkommen („Gehört zu den
# Business-Schritten: …"), damit ein Kurs dem Thema zugeordnet wird.
THEMEN = [
    ("positionierung", "Positionierung", "Nische, Zielgruppe, wofür du stehst.", ["positionierung"]),
    ("angebotstreppe", "Angebotstreppe", "Was du anbietest, in welcher Reihenfolge, zu welchem Preis.", ["angebotstreppe", "produkttreppe"]),
    ("freebie", "Freebie", "0€-Angebot, Leadmagnet, Liste aufbauen.", ["freebie", "leadmagnet"]),
    ("funnel", "Funnel & Mails", "Automationen, Mail-Strecken, was nach dem Eintrag passiert.", ["funnel", "mails"]),
    ("verkaufsseite", "Verkaufsseite & Kasse", "Salespage, Checkout, Bump, Upsell, Downsell.", ["verkaufsseite", "kasse"]),
    ("launch", "Launch", "Phasen, Secret Offer, Käufertypen, Live-Formate.", ["launch"]),
    ("storys", "Storys", "Storys, die verkaufen.", ["storys", "story"]),
    ("content", "Content", "Beiträge, Reels, Hooks, Reichweite.", ["content"]),
    ("werbung", "Werbung", "Anzeigen bei Meta und anderswo.", ["werbung", "anzeigen"]),
    ("strategie", "Stufe & Strategie", "Wo du stehst, was als Nächstes dran ist.", ["stufe", "strategie"]),
    ("jahresplan", "Jahresplan", "Das Jahr planen, Monate verteilen.", ["jahresplan"]),
    ("zeit", "Mama-CEO & Zeit", "Struktur, Fokus, Mindset.", ["mama-ceo", "zeit", "mindset"]),
    ("ki", "KI & Automatisierung", "ChatGPT, Claude, Skills, Bots, Content automatisieren.", ["ki", "claude", "chatgpt", "automatisierung"]),
]


def kopf(md):
    """Frontmatter weg, H1 lesen."""
    if md.startswith("---\n"):
        ende = md.find("\n---\n", 4)
        if ende >= 0:
            md = md[ende + 5:]
    titel = ""
    m = re.match(r"\s*# ([^\n]+)\n+", md)
    if m:
        titel = re.sub(r"\s*[—-]\s*Learnings\s*$", "", m.group(1)).strip()
        md = md[m.end():]
    return titel, md.strip() + "\n"


def themen_von(md):
    m = re.search(r"Gehört zu den Business-Schritten:\s*([^\n]+)", md)
    zeile = (m.group(1) if m else "").lower()
    # In der Reihenfolge der Zeile: das erste ist das Hauptthema des Kurses.
    treffer = []
    for tid, _, _, woerter in THEMEN:
        pos = [zeile.find(w) for w in woerter if w in zeile]
        if pos:
            treffer.append((min(pos), tid))
    return [tid for _, tid in sorted(treffer)]


def stuecke(md):
    """An ## / ### teilen, nie mitten in einer Lektion."""
    if len(md) <= STUECK:
        return [md]
    teile, akt = [], ""
    for block in re.split(r"(?m)^(?=#{2,3} )", md):
        if akt and len(akt) + len(block) > STUECK:
            teile.append(akt)
            akt = ""
        while len(block) > STUECK:  # eine einzelne Lektion über 200 KB
            teile.append(block[:STUECK])
            block = block[STUECK:]
        akt += block
    if akt:
        teile.append(akt)
    return teile


def main():
    if not QUELLE.exists():
        sys.exit("🚨 Fehlt: %s" % QUELLE)
    ZIEL.mkdir(parents=True, exist_ok=True)
    for alt in ZIEL.glob("*.json"):
        alt.unlink()

    unterlagen = {}
    u = QUELLE / "_unterlagen.json"
    if u.exists():
        unterlagen = json.loads(u.read_text(encoding="utf-8"))

    kurse = {}
    dateien = sorted(QUELLE.glob("*.md"))
    if WEITERE.exists():
        dateien += sorted(WEITERE.glob("*.md"))
    for p in dateien:
        if p.name.startswith("_"):
            continue
        titel, md = kopf(p.read_text(encoding="utf-8"))
        slug = p.stem
        teile = stuecke(md)
        for n, t in enumerate(teile, 1):
            (ZIEL / ("k-%s-%d.json" % (slug, n))).write_text(
                json.dumps({"kurs": slug, "teil": n, "md": t}, ensure_ascii=False), encoding="utf-8")
        th = themen_von(md)
        kurse[slug] = {"titel": titel or slug, "teile": len(teile), "zeichen": len(md), "themen": th}
        print("  %-40s %7d Zeichen  %d Teil(e)  -> %s" % (slug, len(md), len(teile), ", ".join(th) or "⚠️ kein Thema"))

    # Stufe 2: je Thema ein Buch (themen/<thema>.md), jeder Punkt einmal.
    buecher = {}
    for p in sorted((QUELLE / "themen").glob("*.md")):
        _, md = kopf(p.read_text(encoding="utf-8"))
        teile = stuecke(md)
        for n, t in enumerate(teile, 1):
            (ZIEL / ("t-%s-%d.json" % (p.stem, n))).write_text(
                json.dumps({"thema": p.stem, "teil": n, "md": t}, ensure_ascii=False), encoding="utf-8")
        buecher[p.stem] = {"teile": len(teile), "zeichen": len(md)}
        print("  Buch %-35s %7d Zeichen  %d Teil(e)" % (p.stem, len(md), len(teile)))

    themen = []
    for tid, titel, kurz, _ in THEMEN:
        themen.append({
            "buch": buecher.get(tid),
            "id": tid, "titel": titel, "kurz": kurz,
            "kurse": [s for s, k in kurse.items() if k["themen"][:1] == [tid]],
            "auch": [s for s, k in kurse.items() if tid in k["themen"][1:]],
            "unterlagen": unterlagen.get(tid, []),
        })
    index = {"stand": date.today().isoformat(), "themen": themen, "kurse": kurse}
    raus = ZIEL / "_index.json"
    raus.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    groesste = max([f.stat().st_size for f in ZIEL.glob("*.json")] or [0])
    print("%d Kurse, %d Themen -> %s (grösstes Dokument %d KB)" % (
        len(kurse), len(themen), ZIEL, groesste // 1024))
    if groesste > 250_000:
        sys.exit("🚨 Ein Dokument ist über 250 KB — STUECK verkleinern.")


if __name__ == "__main__":
    main()
