"""Reiter «Instagram → Zielgruppe & Markt» (12.10.2026).

Patricia: *„wäre cool wenn du mir die ergebnisse aus zielgruppe, nische,
wettbewerbsanalyse und den contentsäulen auch im cockpit ablegen könntest?
überlege dir mal, wo es sinn macht"*.

**Warum unter Instagram:** Die Analysen sind Rohstoff für Hooks, Captions und
Säulen, also für die Arbeit im Bereich Instagram. Dort steht der Reiter neben
„Ideen von anderen", das dieselbe Frage von der Beitragsseite her beantwortet.
Für die Kursarbeit (Kundenmaschine, KI-Kurs) verweisen die Aufgaben darauf.

Liest `daten/zielgruppe` (Dokument von `zielgruppe-bauen.py`). Im Browser liegt
es unter `mlb:zg-markt` — 🚨 bewusst nicht `zielgruppe`, weil es im Wissensblock
schon ein Feld mit dem Namen gibt (Lehre vom `state.zahlen`-Zusammenstoss).

Code und CSS liegen daneben in `zielgruppe-reiter.js` / `.css`, damit
`node --check` sie direkt prüft.

    python scripts/cockpit/patch-zielgruppe.py --datei <cockpit.html>
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
JS_DATEI = HIER / "zielgruppe-reiter.js"
CSS_DATEI = HIER / "zielgruppe-reiter.css"

A_TABS = '''    { id: "ideenextern", label: "Ideen von anderen" },'''
N_TABS = A_TABS + '''
    { id: "markt", label: "Zielgruppe & Markt" },'''

A_BER = '''"gepostet", "ideenkasten", "ideenextern"] },'''
N_BER = '''"gepostet", "ideenkasten", "ideenextern", "markt"] },'''

A_VAR = '''  var ideenExtern = { ideen: [] };'''
N_VAR = A_VAR + '''
  var zgDaten = null;'''

A_LOAD = '''  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };'''
N_LOAD = A_LOAD + '''
  zgDaten = lsGet("zg-markt", null);'''

A_SNAP = '''      db.doc("daten/ideen-extern").onSnapshot(function (snap) {'''
N_SNAP = '''      db.doc("daten/zielgruppe").onSnapshot(function (snap) {
        if (!snap.exists) return;
        zgDaten = tief(snap.data()) || null;
        lsSet("zg-markt", zgDaten);
        if (activeTab === "markt") render();
      }, function () {});
''' + A_SNAP

A_DISP = '''    else if (activeTab === "ideenextern") renderIdeenExtern(main);'''
N_DISP = A_DISP + '''
    else if (activeTab === "markt") renderZielgruppe(main);'''

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
    if "function renderZielgruppe(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

    t = ersetze(t, A_TABS, N_TABS, "TABS")
    t = ersetze(t, A_BER, N_BER, "BEREICHE")
    t = ersetze(t, A_VAR, N_VAR, "Variable")
    t = ersetze(t, A_LOAD, N_LOAD, "Laden")
    t = ersetze(t, A_SNAP, N_SNAP, "onSnapshot")
    t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "renderZielgruppe")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    # 🚨 Erst in eine Nebendatei, dann umbenennen — ein Fehler beim Schreiben
    #    darf das Cockpit nicht leeren.
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
