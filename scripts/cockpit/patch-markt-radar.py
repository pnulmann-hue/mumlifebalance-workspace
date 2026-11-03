"""Reiter «Instagram → Markt-Radar» (30.10.2026).

Patricia über Content Radar: *„übernehme und analysiere bitte das system. vielleicht können
wir das für mich auch bauen?“* Plan: `plans/2026-10-30-markt-radar.md`.

Liest die Sammlung `markt-radar` (`_index` + je Konto ein Dokument), gebaut von
`scripts/hooks/radar.py`. Code und CSS liegen daneben in `markt-radar-reiter.js` / `.css`.

    python scripts/cockpit/patch-markt-radar.py [--datei <cockpit.html>]
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
JS_DATEI = HIER / "markt-radar-reiter.js"
CSS_DATEI = HIER / "markt-radar-reiter.css"

A_TABS = '''    { id: "markt", label: "Zielgruppe & Markt" },'''
N_TABS = A_TABS + '''
    { id: "radar", label: "Markt-Radar" },'''

A_BER = '''tabs: ["woche", "studio", "storys", "fertig", "gepostet", "markt"] },'''
N_BER = '''tabs: ["woche", "studio", "storys", "fertig", "gepostet", "markt", "radar"] },'''

A_DISP = '''    else if (activeTab === "markt") renderZielgruppe(main);'''
N_DISP = A_DISP + '''
    else if (activeTab === "radar") renderMarktRadar(main);'''

EINHAENGEN = '''  /* Reiter „Ideen von anderen": was bei den beobachteten Profilen deutlich'''


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
    pruefe_js(js, JS_DATEI.name)

    t = ziel.read_text(encoding="utf-8")
    if "function renderMarktRadar(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    if "function renderZielgruppe(" not in t:
        sys.exit("🚨 Zielgruppe-Reiter fehlt — zuerst patch-zielgruppe.py.")
    vorher = len(t)

    t = ersetze(t, A_TABS, N_TABS, "TABS")
    t = ersetze(t, A_BER, N_BER, "BEREICHE")
    t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "renderMarktRadar")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    # Erst in eine Nebendatei, dann umbenennen — ein Fehler beim Schreiben
    # darf das Cockpit nicht leeren.
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
