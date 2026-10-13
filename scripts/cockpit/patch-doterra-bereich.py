"""Bereich «doTERRA» im Cockpit (13.10.2026): Öl-Wissen · Anliegen · Business-Wege · Rising Leaders · Rang · Team.

Patricia: *„das ölwissen würde ich gerne vorerst in mein cockpit integrieren"* · Symptomcheck als
*„umfassende nachschlagebibliothek … in ALLEN Unterlagen. büchern, zeitschriften usw."* mit Hinweisen zu
Ernährung und Hormonen · *„gleiches auch fürs business. mit steps was zu tun ist"* · Rising-Leaders-Gruppe
*„mit vielen aufträgen unter anderem neue berater anzuziehen"*.

Eigener Bereich oben statt Unterreiter bei Mama-CEO — Rang-Tracker und Team ziehen mit um.

Daten:
- Sammlung `doterra-wissen` (gehört dem Abgleich): `produkte` (aus produkt-wissensbasis.json),
  `wege` (aus business-wege.json), `anliegen-NN` (aus scripts/doterra/anliegen-bauen.py).
- `daten/rising-leaders` (gehört Patricia): Aufträge, Beraterinnen, Haken der Business-Wege.
  🚨 Der Abgleich schreibt dort NIE hinein. Beim Laden gewinnt der neuere Stand (updatedAt).

Code und CSS daneben in `doterra-bereich.js` / `.css`.

    python scripts/cockpit/patch-doterra-bereich.py [--datei <cockpit.html>]
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
JS_DATEI = HIER / "doterra-bereich.js"
CSS_DATEI = HIER / "doterra-bereich.css"

A_TABS = '''    { id: "team", label: "Team", sub: true },'''
N_TABS = A_TABS + '''
    { id: "oelwissen", label: "Öl-Wissen" },
    { id: "anliegen", label: "Anliegen" },
    { id: "bizwege", label: "Business-Wege" },
    { id: "rising", label: "Rising Leaders" },'''

A_BER = '''      tabs: ["aufgaben", "erledigt", "launches", "monatsbogen", "wochenbogen", "ziele", "zahlen", "rangtracker", "team"] },'''
N_BER = '''      tabs: ["aufgaben", "erledigt", "launches", "monatsbogen", "wochenbogen", "ziele", "zahlen"] },
    { id: "doterra", label: "doTERRA", saeule: "doTERRA",
      tabs: ["oelwissen", "anliegen", "bizwege", "rising", "rangtracker", "team"] },'''

A_NAME = '''rangtracker: "doTERRA-Rang", team: "doTERRA-Team",'''
N_NAME = '''rangtracker: "Rang", team: "Team",'''

A_LOAD = '''  zgDaten = lsGet("zg-markt", null);'''
N_LOAD = A_LOAD + '''
  dtProdukte = lsGet("dt-produkte", null);
  dtWege = lsGet("dt-wege", null);
  dtRising = lsGet("dt-rising", null) || dtRising;'''

A_SNAP = '''      db.doc("daten/ideen-extern").onSnapshot(function (snap) {'''
N_SNAP = '''      db.doc("daten/rising-leaders").onSnapshot(function (snap) {
        if (!snap.exists) return;
        var r = tief(snap.data()) || {};
        // Der neuere Stand gewinnt — sonst legt sich beim Laden ein alter Stand über Getipptes.
        if ((r.updatedAt || "") < (dtRising.updatedAt || "")) return;
        dtRising = { auftraege: r.auftraege || [], beraterinnen: r.beraterinnen || [], haken: r.haken || {},
                     eingang: r.eingang || {}, updatedAt: r.updatedAt || "" };
        lsSet("dt-rising", dtRising);
        if (activeTab === "rising" || activeTab === "bizwege") render();
      }, function () {});
''' + A_SNAP

A_DISP = '''    else if (activeTab === "markt") renderZielgruppe(main);'''
N_DISP = A_DISP + '''
    else if (activeTab === "oelwissen") renderOelwissen(main);
    else if (activeTab === "anliegen") renderAnliegen(main);
    else if (activeTab === "bizwege") renderBizwege(main);
    else if (activeTab === "rising") renderRising(main);'''

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
    pruefe_js("(function(){" + js + "})();", JS_DATEI.name)

    t = ziel.read_text(encoding="utf-8")
    if "function renderOelwissen(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

    t = ersetze(t, A_TABS, N_TABS, "TABS")
    t = ersetze(t, A_BER, N_BER, "BEREICHE")
    t = ersetze(t, A_NAME, N_NAME, "UNTERNAME")
    t = ersetze(t, A_LOAD, N_LOAD, "Laden")
    t = ersetze(t, A_SNAP, N_SNAP, "onSnapshot")
    t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "Code")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    # Erst in eine Nebendatei, dann umbenennen — ein Fehler beim Schreiben darf das Cockpit nicht leeren.
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
