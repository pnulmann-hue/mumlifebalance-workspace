"""Nimmt den Oele-Block aus dem Rang-Tracker wieder heraus.

Patricia am 24.09.2026: *„eigentlich ist das gar nicht so wichtig. weil im
doterra bot habe ich alle oel infos drin..."* — und sie hat recht.

| | |
|---|---|
| doTERRA Business Companion | rund 39'000 Chunks Oel-Wissen in Supabase, Chat auf bot.mumlifebalance.ch |
| Der Block hier | 21 Oele, davon 13 ohne Wirkbereich |

Ein halbleeres Duplikat neben einer vollstaendigen Wissensbasis. Wer im Cockpit
nachschlaegt und nichts findet, schliesst daraus, es gebe nichts — dabei steht
die Antwort im Bot.

**Der Fehler war, nicht gegen den Bot zu pruefen.** Bei «Projekte» wurde vorher
gegen den Jahresplan geprueft (nur 2 von 24 doppelt, also gebaut). Hier wurde
diese Frage nicht gestellt. Eine neue Ansicht braucht immer zuerst die Frage:
**gibt es das schon woanders, und ist es dort besser?**

Daten und Importskript bleiben liegen (`doterra-produkte-importieren.py`,
`daten/doterra-produkte`) — falls die Wirkbereich-Zuordnung einmal wirklich
gepflegt wird, ist sie da. Nur die Anzeige geht weg.

    python scripts/cockpit/patch-doterra-produkte-zurueck.py [--pruefen]
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"


def js_pruefen(html):
    for i, block in enumerate(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)):
        if len(block.strip()) < 200:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(block)
            p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        Path(p).unlink(missing_ok=True)
        if r.returncode != 0:
            return "Block %d: %s" % (i, (r.stderr or "")[:600])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = SEITE.read_text(encoding="utf-8")

    if "oeleBlock(main)" not in s:
        print("  Schon draussen — nichts zu tun.")
        return

    # 1) Aufruf raus
    ruf = "\n\n    oeleBlock(main);"
    if s.count(ruf) != 1:
        sys.exit("🚨 Aufruf kommt %dx vor — erwartet 1x." % s.count(ruf))
    s = s.replace(ruf, "", 1)

    # 2) Funktion samt Kommentarblock raus: vom Kommentar bis zur
    #    schliessenden Klammer der Funktion.
    start_marke = "  /* =========================================================\n" \
                  "     \u00d6le und Wirkbereiche"
    i = s.find(start_marke)
    if i < 0:
        sys.exit("🚨 Anfang des Bloecke nicht gefunden.")
    # Ende: die naechste Zeile, die genau "  }" ist, NACH dem Funktionsbeginn.
    j = s.find("\n  function oeleBlock(main) {", i)
    if j < 0:
        sys.exit("🚨 Funktionsbeginn nicht gefunden.")
    k = s.find("\n  }\n", j)
    if k < 0:
        sys.exit("🚨 Funktionsende nicht gefunden.")
    entfernt = k + len("\n  }\n") - i
    s = s[:i] + s[k + len("\n  }\n"):]

    # 3) Variable, Laden und Abo raus
    for weg in [
        "\n  var dtProdukte = null;         // daten/doterra-produkte — gehoert PATRICIA",
        '\n  dtProdukte = lsGet("doterra-produkte", null);',
        '\n      db.doc("daten/doterra-produkte").onSnapshot(function (snap) {\n'
        "        if (!snap.exists) return;\n"
        "        dtProdukte = snap.data() || null;\n"
        '        lsSet("doterra-produkte", dtProdukte);\n'
        '        if (activeTab === "rangtracker") render();\n'
        "      }, function () {});",
    ]:
        if s.count(weg) != 1:
            sys.exit("🚨 Ein Baustein kommt %dx vor — erwartet 1x:\n  %s"
                     % (s.count(weg), weg[:70]))
        s = s.replace(weg, "", 1)

    # Gegenprobe: kein Rest.
    rest = [w for w in ("oeleBlock", "dtProdukte", "oelSuche", "doterra-produkte")
            if w in s]
    if rest:
        sys.exit("🚨 Reste im Code: %s" % ", ".join(rest))

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung, keine Reste. Mit --pruefen wird nicht geschrieben.")
        print("  Es wuerden %d Zeichen entfernt." % entfernt)
        return

    SEITE.write_text(s, encoding="utf-8")
    print("  Öle-Block entfernt · %d Zeichen weg · Seite jetzt %d KB"
          % (entfernt, len(s) / 1024))


if __name__ == "__main__":
    main()
