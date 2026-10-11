"""
Baut den Suchindex fuers Cockpit.

Patricias Frage war: „wenn ich ein Stichwort eingebe, zum Beispiel Keyword —
wo ging es ueberall darum?" Genau das macht dieser Index: er zerlegt alle
Markdown-Dateien in Abschnitte und legt pro Abschnitt Pfad, Ueberschrift und
einen kurzen Auszug ab.

Was NICHT hineinkommt: alles unter `private/` und `persoenlich/`, die
Finanz-Ordner und die Kurs-Transkripte von fremden Kursen. Der Index landet
im Cockpit, und dort gehoert nichts hinein, was nicht hineingehoert.

Aufruf:
  python scripts/cockpit/suchindex-bauen.py [zielordner]
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

ORDNER = ["context", "outputs", "reference", "plans"]

# Nichts Privates, nichts Fremdes, nichts Maschinelles.
TABU = ("private", "persoenlich", "finanzen", "node_modules", ".git",
        "worktrees", "apify-runs", "Transkripte", "transkripte", "_INDEX",
        "abgleich")

# Wieviele Zeichen eines Abschnitts als Auszug mitkommen.
AUSZUG = 220
MINDESTLAENGE = 60


def lesbar(text):
    """Markdown-Zierrat entfernen, damit der Auszug wie ein Satz aussieht."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#*_>`|-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def bereich(pfad):
    """Grobe Schublade fuer die Trefferliste."""
    teile = pfad.split("/")
    if teile[0] == "context":
        return "Grundlagen"
    if teile[0] == "reference":
        return "Wissen"
    if teile[0] == "plans":
        return "Pläne"
    return {"produkte": "Produkte", "funnels": "Funnel", "reels": "Reels",
            "karussells": "Karussells", "stories": "Stories",
            "monatsplaene": "Monatspläne",
            "zielgruppen-research": "Recherche"}.get(
        teile[1] if len(teile) > 1 else "", "Arbeit")


def abschnitte(datei, rel):
    """Eine Datei in Abschnitte an den Ueberschriften zerlegen."""
    try:
        text = datei.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    # Frontmatter weg
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)

    raus = []
    titel = datei.stem
    puffer = []

    def ablegen():
        inhalt = lesbar("\n".join(puffer))
        if len(inhalt) >= MINDESTLAENGE:
            raus.append({"d": rel, "t": titel[:110],
                         "a": inhalt[:AUSZUG], "b": bereich(rel)})

    for zeile in text.splitlines():
        if zeile.startswith("#"):
            ablegen()
            titel = lesbar(zeile)[:110] or datei.stem
            puffer = []
        else:
            puffer.append(zeile)
    ablegen()
    return raus


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    eintraege, dateien = [], 0
    for ordner in ORDNER:
        wurzel = ROOT / ordner
        if not wurzel.exists():
            continue
        for datei in wurzel.rglob("*.md"):
            rel = datei.relative_to(ROOT).as_posix()
            if any(t in rel for t in TABU):
                continue
            neu = abschnitte(datei, rel)
            if neu:
                dateien += 1
                eintraege += neu

    heute = date.today().isoformat()
    # In Haeppchen, damit kein Dokument zu gross wird: die Artifact-Datenbank
    # nimmt hoechstens 256 KB je Dokument. 500 Abschnitte landen bei rund
    # 170 KB und lassen Luft nach oben.
    proTeil = 500
    teile = [eintraege[i:i + proTeil] for i in range(0, len(eintraege), proTeil)]
    for nr, teil in enumerate(teile):
        (ziel / ("suche-%02d.json" % nr)).write_text(
            json.dumps({"teil": nr, "items": teil, "stand": heute},
                       ensure_ascii=False), encoding="utf-8")

    groesse = sum((ziel / ("suche-%02d.json" % n)).stat().st_size
                  for n in range(len(teile)))
    print("  %d Abschnitte aus %d Dateien" % (len(eintraege), dateien))
    print("  %d Teildateien, zusammen %.1f MB" % (len(teile), groesse / 1e6))
    print("\nAbgelegt in: %s" % ziel.resolve())


if __name__ == "__main__":
    main()
