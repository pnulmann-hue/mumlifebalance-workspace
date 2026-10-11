"""
Bringt die Startklar-Werkstatt von der Arbeitsfassung in die Auslieferung.

🚨 Die Werkstatt liegt an zwei Stellen, und das ist eine Falle:

  outputs/produkte/instagram-startklar/04-arbeitsblaetter/startklar-werkstatt.html
      die QUELLE — hier wird gearbeitet

  scripts/startklar-service/public/index.html
      was Vercel unter startklar.mumlifebalance.ch ausliefert

Der einzige Unterschied ist ein HTML-Kopf, den die Auslieferung braucht und
die Quelle nicht hat. Wer die Quelle aendert und das hier vergisst, aendert
nichts an dem, was die Kaeuferinnen sehen — und merkt es erst, wenn sich
jemand beschwert.

Aufruf:
  python scripts/startklar/werkstatt-ausliefern.py            # uebertragen
  python scripts/startklar/werkstatt-ausliefern.py --pruefen  # nur vergleichen
"""
import argparse
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "produkte" / "instagram-startklar" / "04-arbeitsblaetter" / "startklar-werkstatt.html"
ZIEL = ROOT / "scripts" / "startklar-service" / "public" / "index.html"

KOPF = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
"""
FUSS = "\n</html>\n"


def bauen():
    roh = QUELLE.read_text(encoding="utf-8")
    # Die Quelle beginnt ohne Kopf. Falls doch einer da ist, nicht doppeln.
    if roh.lstrip().lower().startswith("<!doctype"):
        return roh
    return KOPF + roh + FUSS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefen", action="store_true", help="nur vergleichen, nichts schreiben")
    args = ap.parse_args()

    neu = bauen()
    alt = ZIEL.read_text(encoding="utf-8") if ZIEL.exists() else ""

    if alt == neu:
        print("Auslieferung ist schon auf dem Stand der Quelle.")
        return

    print("Quelle      : %6d Zeichen" % len(QUELLE.read_text(encoding="utf-8")))
    print("Auslieferung: %6d Zeichen (bisher)" % len(alt))
    print("Neu         : %6d Zeichen" % len(neu))
    bsp_alt, bsp_neu = alt.count('beispiel:"'), neu.count('beispiel:"')
    print("Beispiele   : %d -> %d" % (bsp_alt, bsp_neu))

    if args.pruefen:
        print("\nNur geprüft — nichts geschrieben.")
        return

    ZIEL.write_text(neu, encoding="utf-8")
    print("\nGeschrieben: %s" % ZIEL)
    print("Jetzt noch hochladen:")
    print("  cd scripts/startklar-service && npx vercel --prod")


if __name__ == "__main__":
    main()
