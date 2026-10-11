"""
Holt einen Textblock aus 10-kursplattform-texte.md und macht HTML daraus.

Die Kursplattform (ThriveCart Learn) hat ein eigenes Feld fuer den Titel und
eines fuer den Text. Deshalb gibt dieses Skript den Titel getrennt aus und
baut nur den Textteil als HTML - mit Absaetzen, Fettungen und Links.

Aufruf:
  python scripts/startklar/text-fuer-kursplattform.py --liste
  python scripts/startklar/text-fuer-kursplattform.py "Lektion 1.1"
  python scripts/startklar/text-fuer-kursplattform.py "Lektion 1.1" --mit-titel

Das Ergebnis landet in einer Datei; in die Zwischenablage kommt es danach mit:
  powershell -c "Set-Clipboard -Value ([IO.File]::ReadAllText('<pfad>',[Text.Encoding]::UTF8))"
"""
import argparse
import html as H
import os
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "produkte" / "instagram-startklar" / "10-kursplattform-texte.md"


def bloecke():
    """Alle Abschnitte als {Ueberschrift: Rohtext}."""
    text = QUELLE.read_text(encoding="utf-8")
    teile = re.split(r"^#{2,3} (.+)$", text, flags=re.M)
    raus = {}
    for i in range(1, len(teile), 2):
        raus[teile[i].strip()] = teile[i + 1]
    return raus


def finden(bl, suche):
    s = suche.lower()
    treffer = [k for k in bl if s in k.lower()]
    if not treffer:
        return None, treffer
    # kuerzeste Ueberschrift gewinnt: "Lektion 1.1" vor "Lektion 1.10"
    return min(treffer, key=len), treffer


def auszeichnen(s):
    # quote=False: im Fliesstext bleibt " ein ", sonst steht im Quelltext
    # ueberall &quot; - richtig dargestellt, aber unlesbar beim Nachbearbeiten.
    s = H.escape(s, quote=False)
    # Links vor Fettungen, sonst frisst die Klammer-Regel die Auszeichnung.
    # Die Adresse wird einzeln gesichert, weil sie in ein Attribut geht.
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               lambda m: '<a href="%s">%s</a>' % (H.escape(m.group(2), quote=True), m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def aufbereiten(roh):
    """Zitatzeilen zu Absaetzen buendeln, Titelzeile heraustrennen."""
    titel, zeilen = None, []
    for z in roh.splitlines():
        z = z.strip()
        if z.startswith("**Überschrift:**"):
            titel = z.replace("**Überschrift:**", "").strip()
            continue
        if z.startswith(">"):
            zeilen.append(z[1:].strip())
        elif not z or z.startswith("---"):
            zeilen.append("")
        # alles andere (Fliesstext der Doku) gehoert nicht in den Kurs

    absaetze, puffer = [], []
    for z in zeilen:
        if z:
            puffer.append(z)
        elif puffer:
            absaetze.append(" ".join(puffer))
            puffer = []
    if puffer:
        absaetze.append(" ".join(puffer))
    return titel, absaetze


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("abschnitt", nargs="?", help="z.B. \"Lektion 1.1\" oder \"Begrüssung\"")
    ap.add_argument("--liste", action="store_true", help="alle Abschnitte zeigen")
    ap.add_argument("--mit-titel", action="store_true", help="Titel als <h2> mit ins HTML")
    args = ap.parse_args()

    bl = bloecke()
    if args.liste or not args.abschnitt:
        print("Abschnitte in %s:\n" % QUELLE.name)
        for k in bl:
            print("  " + k)
        return

    name, treffer = finden(bl, args.abschnitt)
    if not name:
        print("Nichts gefunden zu %r. Mit --liste siehst du alle." % args.abschnitt)
        sys.exit(1)
    if len(treffer) > 1:
        print("Mehrdeutig, nehme %r (auch möglich: %s)" % (name, ", ".join(treffer)))

    titel, absaetze = aufbereiten(bl[name])
    teile = []
    if args.mit_titel and (titel or name):
        teile.append("<h2>%s</h2>" % H.escape(titel or name))
    teile += ["<p>%s</p>" % auszeichnen(a) for a in absaetze]
    fragment = "\n".join(teile)

    ziel = pathlib.Path(os.environ.get("TEMP", ".")) / "kurstext.html"
    ziel.write_text(fragment, encoding="utf-8")

    print("Abschnitt:   %s" % name)
    print("Titelfeld:   %s" % (titel or name))
    print("Absätze:     %d  ·  fett: %d  ·  Links: %d"
          % (len(absaetze), fragment.count("<strong>"), fragment.count("<a href")))
    print("Datei:       %s" % ziel)


if __name__ == "__main__":
    main()
