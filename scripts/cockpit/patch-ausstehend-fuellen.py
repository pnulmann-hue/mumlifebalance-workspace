"""Der Merkzettel für Ausstehendes wird auch befüllt, nicht nur geleert.

🚨 **Fehler im eigenen Patch von vorhin** (24.09.2026): `patch-kein-datenverlust.py`
hat `sofortSichern()` eingebaut und in jeder Speicherfunktion ein
`delete ausstehend[key]` — aber **nirgends ein `ausstehend[key] = …`**. Der
Merkzettel war also immer leer, und der Schutz beim Schliessen der Seite tat
nichts. Ein Sicherheitsnetz, das nicht gespannt ist, ist schlimmer als keins:
man verlässt sich darauf.

**Der Umbau:** der Inhalt des Zeitgebers wird zur benannten Funktion `tun`, die
sowohl im Merkzettel liegt als auch nach 700 ms läuft. `sofortSichern()` ruft
dann wirklich etwas auf.

🚨 **Die lokale Arbeit ist auch ohne das sicher** — `lsSet` läuft seit dem
vorigen Patch sofort. Der Merkzettel betrifft nur das Schreiben in die
Datenbank, also den Abgleich zwischen Geräten.

    python scripts/cockpit/patch-ausstehend-fuellen.py [--pruefen] [--datei <pfad>]
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

# Je Format: (Name, Schluessel-Ausdruck) — der Zeitgeber-Kopf wird umgebaut.
UMBAU = [
    ("saveStory", 'st-" + st.id'),
    ("saveCarousel", 'kar-" + car.id'),
    ("saveReel", 'rl-" + r.id'),
]


def kopf_alt(schl):
    return ('    clearTimeout(saveTimers["%s]);\n'
            '    saveTimers["%s] = setTimeout(function () {\n'
            '      delete ausstehend["%s];\n' % (schl, schl, schl))


def kopf_neu(schl):
    return ('    clearTimeout(saveTimers["%s]);\n'
            '    /* Der Zeitgeber-Inhalt als benannte Funktion: sie liegt im\n'
            '       Merkzettel UND laeuft nach 700 ms. Ohne den Eintrag war\n'
            '       sofortSichern() wirkungslos. */\n'
            '    var tun = function () {\n'
            '      delete ausstehend["%s];\n' % (schl, schl))


def schwanz_alt():
    return ('        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });\n'
            '    }, 700);\n'
            '  }')


def schwanz_neu(schl):
    return ('        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });\n'
            '    };\n'
            '    ausstehend["%s] = tun;\n'
            '    saveTimers["%s] = setTimeout(tun, 700);\n'
            '  }' % (schl, schl))


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
            return "Block %d: %s" % (i, (r.stderr or "")[:700])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit-neu.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "ausstehend[\"st-\" + st.id] = tun" in s:
        print("  Schon gefüllt — nichts zu tun.")
        return

    for name, schl in UMBAU:
        a, n = kopf_alt(schl), kopf_neu(schl)
        if s.count(a) != 1:
            sys.exit("🚨 Kopf von %s kommt %dx vor." % (name, s.count(a)))
        s = s.replace(a, n, 1)

        # Der Schwanz steht dreimal gleich — je Funktion den ersten nach dem
        # Kopf ersetzen, sonst trifft es die falsche.
        start = s.index(n)
        ende = s.index(schwanz_alt(), start)
        s = s[:ende] + schwanz_neu(schl) + s[ende + len(schwanz_alt()):]

    # 🚨 Gegenprobe: drei Eintraege, drei Loeschungen.
    if s.count("ausstehend[") != 7:   # 3× setzen, 3× loeschen, 1× in sofortSichern
        sys.exit("🚨 `ausstehend[` kommt %dx vor — erwartet 7." % s.count("ausstehend["))

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Merkzettel wird gefüllt · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
