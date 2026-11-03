"""Tagesrunde im Reiter doTERRA → Rising Leaders (03.11.2026, Version 121).

Patricia: *„ich möchte bei doTERRa endlich in die umsetzung kommen und zum erfolg“*.
Die drei täglichen Schritte aus Rise to Lead (Business erwähnen · eine Person ansprechen ·
eine Kundin kontaktieren) zum Abhaken, je mit einer Idee für heute, dazu der Zähler auf 100
Ansprachen, die Woche als Punkte und ab dem 24. der Monatsabschluss mit dem, was je Bein fehlt.
Auf Mein Tisch steht oben „x/3 doTERRA heute“ und springt in den Reiter.

Daten in `daten/rising-leaders` (gehört Patricia): `tagesrunde`, `abschluss`.
🚨 Die onSnapshot-Zeile kannte bisher nur fünf Felder und hätte die neuen beim Laden verworfen —
sie übernimmt jetzt das ganze Dokument.

Setzt patch-doterra-bereich.py voraus. Code und CSS daneben in `tagesrunde.js` / `.css`.

    python scripts/cockpit/patch-tagesrunde.py [--datei <cockpit.html>]
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
JS_DATEI = HIER / "tagesrunde.js"
CSS_DATEI = HIER / "tagesrunde.css"

A_SNAP = '''        dtRising = { auftraege: r.auftraege || [], beraterinnen: r.beraterinnen || [], haken: r.haken || {},
                     eingang: r.eingang || {}, updatedAt: r.updatedAt || "" };'''
N_SNAP = '''        dtRising = Object.assign({}, r, { auftraege: r.auftraege || [], beraterinnen: r.beraterinnen || [], haken: r.haken || {},
                     eingang: r.eingang || {}, tagesrunde: r.tagesrunde || {}, abschluss: r.abschluss || {},
                     updatedAt: r.updatedAt || "" });'''

A_SNAP_RENDER = '''        if (activeTab === "rising" || activeTab === "bizwege") render();'''
N_SNAP_RENDER = '''        if (activeTab === "rising" || activeTab === "bizwege" || activeTab === "uebersicht") render();'''

A_KOPF = '''    var h = eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''
N_KOPF = '''    var h = trHtml() + eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''

A_BIND = '''    main.innerHTML = h;

    function neuId(p) { return p + Date.now().toString(36) + Math.random().toString(36).slice(2, 5); }'''
N_BIND = '''    main.innerHTML = h;
    trBinden(main);

    function neuId(p) { return p + Date.now().toString(36) + Math.random().toString(36).slice(2, 5); }'''

A_TISCH = '''          '<button class="ti-zahl" data-gehe="aufgaben"><b>' + faellig + '</b>überfällig</button>' +'''
N_TISCH = A_TISCH + '''
          '<button class="ti-zahl" data-gehe="rising"><b>' + trHeuteZahl() + '/3</b>doTERRA heute</button>' +'''

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
    if "function renderRising(" not in t:
        sys.exit("🚨 Rising-Leaders-Reiter fehlt — zuerst patch-doterra-bereich.py.")
    if "function trHtml(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

    t = ersetze(t, A_SNAP, N_SNAP, "onSnapshot")
    t = ersetze(t, A_SNAP_RENDER, N_SNAP_RENDER, "onSnapshot render")
    t = ersetze(t, A_KOPF, N_KOPF, "Rising-Kopf")
    t = ersetze(t, A_BIND, N_BIND, "Rising-Binden")
    t = ersetze(t, A_TISCH, N_TISCH, "Mein Tisch")
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
