"""Team-Funke im Reiter doTERRA → Rising Leaders (03.11.2026, Version 122).

Patricia: *„gleichzeitig würde ich gerne damit auch mein Team motivieren. ich muss da wieder mehr
leben reinbringen.“* Die Wochennachricht fürs Team: Erfolge und Aktion eintragen, anhaken, wer kurz
vor dem nächsten Schritt steht (aus `daten/doterra`, Zahlen nur für sie sichtbar), Challenge wählen
(wechselt nach dem Verlauf) — Claude schreibt über `sample` die Gruppennachricht plus je eine
persönliche Nachricht. Verschickt wird nichts, sie kopiert und schickt selbst.
Auf Mein Tisch erscheint ab Sonntag „✨ Team-Funke“, bis eine verschickt ist.

Daten in `daten/rising-leaders` (gehört Patricia): `funke = { entwurf, verlauf }`.
Setzt patch-tagesrunde.py voraus. Code und CSS daneben in `teamfunke.js` / `.css`.

    python scripts/cockpit/patch-teamfunke.py [--datei <cockpit.html>]
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
JS_DATEI = HIER / "teamfunke.js"
CSS_DATEI = HIER / "teamfunke.css"

A_KOPF = '''    var h = trHtml() + eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''
N_KOPF = '''    var h = trHtml() + tfHtml() + eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''

A_BIND = '''    trBinden(main);'''
N_BIND = '''    trBinden(main);
    tfBinden(main);'''

A_TISCH = '''          '<button class="ti-zahl" data-gehe="rising"><b>' + trHeuteZahl() + '/3</b>doTERRA heute</button>' +'''
N_TISCH = A_TISCH + '''
          (tfFaellig() ? '<button class="ti-zahl du" data-gehe="rising"><b>✨</b>Team-Funke</button>' : "") +'''

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
    if "function trHtml(" not in t:
        sys.exit("🚨 Tagesrunde fehlt — zuerst patch-tagesrunde.py.")
    if "function tfHtml(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

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
