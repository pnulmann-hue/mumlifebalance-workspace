"""Öl-App — neue Hefte, Bücher, Unterlagen in den Kompass nachführen. Ein Befehl für alles.

    python scripts/oel-app/nachfuehren.py --trocken   # zeigen, was neu ist und was es kosten würde
    python scripts/oel-app/nachfuehren.py             # nachführen

Patricia legt Neues dort ab, wo sie es sowieso ablegt: in OneDrive unter
„Patricia/Arbeit&Politik/Business/doTERRA“ (z.B. ein neues Enjoils-Heft in Ebooks/Enjoils/<Saison>/)
oder direkt in context/doTERRA/. Dann laufen der Reihe nach:

1. fehlende Dateien aus OneDrive nach context/doTERRA/ kopieren (pdf, epub, docx — nur neue)
2. Scans per Windows-Texterkennung lesen (über anliegen-bauen.py --ocr, frischt auch das Cockpit auf)
3. alle Unterlagen neu in Abschnitte schneiden (quellen.py)
4. den vollständigen Durchgang nur für die NEUEN Pakete (wissen-ausziehen.py — je Quelle eigene Pakete,
   ein neues Heft kostet nur sich selbst)
5. die App neu packen (app-bauen.py)

Veröffentlichen macht danach Claude im Chat (Artifact publish, siehe CLAUDE.md „Öl-Kompass“) — ein Skript
kommt nicht an das Artifact.
"""
import pathlib
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WS = pathlib.Path(__file__).resolve().parents[2]
ONEDRIVE = pathlib.Path.home() / "OneDrive/Dokumente/Patricia/Arbeit&Politik/Business/doTERRA"
ZIEL = WS / "context/doTERRA"
ENDUNGEN = {".pdf", ".epub", ".docx"}


def neue_dateien():
    if not ONEDRIVE.exists():
        print(f"⚠️  OneDrive-Ordner nicht gefunden: {ONEDRIVE} — nur context/doTERRA wird gelesen")
        return []
    neu = []
    for p in ONEDRIVE.rglob("*"):
        if p.is_file() and p.suffix.lower() in ENDUNGEN:
            ziel = ZIEL / p.relative_to(ONEDRIVE)
            if not ziel.exists():
                neu.append((p, ziel))
    return neu


def lauf(*befehl):
    print("\n▶", " ".join(befehl[1:]))
    r = subprocess.run([sys.executable, *befehl[1:]], cwd=WS)
    if r.returncode:
        sys.exit(f"❌ abgebrochen bei: {' '.join(befehl[1:])}")


def main():
    trocken = "--trocken" in sys.argv
    neu = neue_dateien()
    print(f"{len(neu)} neue Dateien in OneDrive:")
    for quelle, _ in neu[:40]:
        print("   ", quelle.relative_to(ONEDRIVE))
    if trocken:
        lauf("python", "scripts/oel-app/wissen-ausziehen.py", "--trocken")
        print("\n(Die Kostenschätzung zählt nur, was schon im Workspace liegt — neue Dateien kommen erst nach dem Kopieren dazu.)")
        return
    for quelle, ziel in neu:
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(quelle, ziel)
    lauf("python", "scripts/doterra/anliegen-bauen.py", "--ocr")
    lauf("python", "scripts/oel-app/quellen.py")
    lauf("python", "scripts/oel-app/wissen-ausziehen.py")
    lauf("python", "scripts/oel-app/app-bauen.py")
    print("\n✓ Nachgeführt. Jetzt im Chat veröffentlichen lassen.")


if __name__ == "__main__":
    main()
