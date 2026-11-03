"""Heute dran ganz oben auf Mein Tisch (03.11.2026, Version 123).

Patricia: *„wie können wir gewährleisten, dass mir die dinge aufploppen? … irgendwie habe
ich das gefühl ich könnte die dinge übersehen oder nicht bemerken bei der jetzigen
darstellung“*. Eine Liste statt verteilter Zähler: Termine · Tagesfokus (morgens) ·
Learning und Blick auf Morgen (abends) · Fokus der Woche · doTERRA-Tagesrunde ·
Team-Funke · Monatsabschluss · Beiträge, die auf sie warten · Aufgaben.
Die Zähler „doTERRA heute“ und „Team-Funke“ oben im Kopf fallen dafür weg.

Neues Dokument `daten/tagebuch` = `{ tage: { JJJJ-MM-TT: { fokus, learning, morgen } } }`,
gehört Patricia. Setzt patch-tagesrunde.py und patch-teamfunke.py voraus.

    python scripts/cockpit/patch-heutedran.py [--datei <cockpit.html>]
"""

import os
import pathlib
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
JS_DATEI = HIER / "heutedran.js"
CSS_DATEI = HIER / "heutedran.css"

A_ZAHLEN = '''          '<button class="ti-zahl" data-gehe="rising"><b>' + trHeuteZahl() + '/3</b>doTERRA heute</button>' +
          (tfFaellig() ? '<button class="ti-zahl du" data-gehe="rising"><b>✨</b>Team-Funke</button>' : "") +
'''
N_ZAHLEN = ""

A_GRID = '''        '</div></header>' +
        '<div class="ti-grid">' +'''
N_GRID = '''        '</div></header>' +
        hdHtml(heute, beitraege) +
        '<div class="ti-grid">' +'''

A_BIND = '''    tiPia(main.querySelector("#ti-pia"), heute, beitraege);'''
N_BIND = '''    hdBinden(main, heute);
''' + A_BIND

EINHAENGEN = '''  /* ---------- Rising Leaders: Aufträge + Beraterinnen ---------- */'''


def ersetze(t, alt, neu, name):
    n = t.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert." % (name, n))
    return t.replace(alt, neu, 1)


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    else:
        ziel = ROOT / "outputs/cockpit/mlb-cockpit.html"
    js = JS_DATEI.read_text(encoding="utf-8")
    css = CSS_DATEI.read_text(encoding="utf-8")
    pruefe_js("(function(){" + js + "})();", JS_DATEI.name)

    t = ziel.read_text(encoding="utf-8")
    if "function tfHtml(" not in t:
        sys.exit("🚨 Team-Funke fehlt — zuerst patch-tagesrunde.py und patch-teamfunke.py.")
    for name in ("hdHtml", "hdPunkte", "hdKw", "hdTag", "hdBinden", "hdSpeichern", "hdTagebuchHolen", "hdZahl", "hdPunktHtml"):
        if "function %s(" % name in t:
            sys.exit("Steht schon drin (%s) — nichts zu tun." % name)
    if "daten/tagebuch" in t or "var hdTagebuch" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

    t = ersetze(t, A_ZAHLEN, N_ZAHLEN, "Zähler im Kopf")
    t = ersetze(t, A_GRID, N_GRID, "Mein Tisch")
    t = ersetze(t, A_BIND, N_BIND, "Binden")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "Code")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
