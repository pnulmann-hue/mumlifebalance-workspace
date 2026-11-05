"""Holt das Aktions-Booklet des Monats aus der Telegram-Gruppe „dōTERRA Business“ und legt es bereit.

    python scripts/oelgruppe/newsletter-holen.py 2026-12

-> outputs/newsletter/quelle-<monat>/ (Booklet, Flyer, treffer.json, booklet.txt, aktuelles.txt; gitignored)
-> lädt das Booklet verkleinert in die WordPress-Mediathek und nennt die Adresse.
Code 3: Booklet noch nicht in der Gruppe. Liest nur, schreibt nichts in Telegram.
"""
import pathlib
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
MONATE = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


def main():
    monat = sys.argv[1]
    jahr, m = monat.split("-")
    name = MONATE[int(m)]
    ziel = ROOT / "outputs/newsletter" / ("quelle-" + monat)
    bot = ROOT / "scripts/telegram-userbot"
    subprocess.run('npx tsx src/newsletter-suchen.ts --chat "terra business" --ziel "%s" --tage 9' % ziel,
                   shell=True, check=True, cwd=bot, capture_output=True)
    pdfs = [p for p in ziel.glob("*.pdf") if name.lower() in p.name.lower() and "aktion" in p.name.lower()]
    if not pdfs:
        print("Noch kein Booklet für", name, "in der Gruppe")
        sys.exit(3)
    roh = subprocess.run('npx tsx src/gruppe-neueste.ts "terra business" --tage 7 --voll', shell=True, cwd=bot, capture_output=True)
    (ziel / "aktuelles.txt").write_bytes(roh.stdout)

    from pypdf import PdfReader, PdfWriter
    leser = PdfReader(str(pdfs[0]))
    texte = []
    for i, s in enumerate(leser.pages):
        t = s.extract_text() or ""
        # Das Booklet setzt Text mit Leerraum zwischen den Buchstaben: „A K T I O N E N“
        t = re.sub(r"(?<=\S) (?=\S)(?!\S\S)", "", t) if re.search(r"(\S ){6}", t) else t
        texte.append("--- Seite %d\n%s" % (i + 1, t))
    (ziel / "booklet.txt").write_text("\n".join(texte), encoding="utf-8")

    klein = ROOT / "outputs/newsletter" / ("Aktionen-%s-%s-klein.pdf" % (name.replace("ä", "ae"), jahr))
    w = PdfWriter()
    for s in leser.pages:
        w.add_page(s)
    for s in w.pages:
        for bild in s.images:
            try:
                bild.replace(bild.image.convert("RGB"), quality=55)
            except Exception:
                pass
    w.write(str(klein))
    hoch = subprocess.run('node --env-file=.env wp-api.js upload-media "%s"' % klein, shell=True, cwd=ROOT / "scripts/wordpress",
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    treffer = re.search(r"https://\S+\.pdf", hoch.stdout)
    if not treffer:
        sys.exit("🚨 Upload ging nicht: " + hoch.stdout + hoch.stderr)
    print("Booklet:", pdfs[0].name, "· Seiten", len(leser.pages))
    print("Adresse:", treffer.group(0))
    print("Text:", ziel / "booklet.txt")
    print("Aktuelles aus der Gruppe:", ziel / "aktuelles.txt")


if __name__ == "__main__":
    main()
