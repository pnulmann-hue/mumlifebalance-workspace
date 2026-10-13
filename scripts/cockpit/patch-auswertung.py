"""Block „Was die Zahlen sagen“ oben im Reiter „Gepostet & Analyse“ (13.10.2026).

Patricia: *„genau logisch kein neues dashboard. sondern in meinem bestehenden schlau
integrieren“*. Liest `daten/auswertung` (von `zahlen-auswerten.py`). Im Browser liegt
es unter `mlb:zahlen-auswertung` — 🚨 nicht `auswertung` allein und nicht `zahlen`,
weil `state.zahlen` schon Patricias Umsatz-Tabelle ist (Lehre vom 24.09.).

Code und CSS liegen daneben in `auswertung-block.js` / `.css`.
Wiederholbar: ein zweiter Lauf erkennt den Block und frischt ihn auf.

    python scripts/cockpit/patch-auswertung.py [--datei <cockpit.html>]
"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
if "--datei" in sys.argv:
    DATEI = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])

JS_A, JS_E = "  /* @@auswertung-js-anfang */\n", "  /* @@auswertung-js-ende */\n"
CSS_A, CSS_E = "  /* @@auswertung-css-anfang */\n", "  /* @@auswertung-css-ende */\n"

ERSETZ = [
    ('  var ideenExtern = { ideen: [] };',
     '  var ideenExtern = { ideen: [] };\n  var zahlenAuswertung = null;   // daten/auswertung'),
    ('  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };',
     '  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };\n'
     '  zahlenAuswertung = lsGet("zahlen-auswertung", null);'),
    ('      db.doc("daten/ideen-extern").onSnapshot(function (snap) {',
     '      db.doc("daten/auswertung").onSnapshot(function (snap) {\n'
     '        if (!snap.exists) return;\n'
     '        zahlenAuswertung = tief(snap.data()) || null;\n'
     '        lsSet("zahlen-auswertung", zahlenAuswertung);\n'
     '        if (activeTab === "gepostet") render();\n'
     '      }, function () {});\n'
     '      db.doc("daten/ideen-extern").onSnapshot(function (snap) {'),
    ('    else if (activeTab === "gepostet") renderGepostet(main);',
     '    else if (activeTab === "gepostet") { renderGepostet(main); auswertungEinsetzen(main); }'),
]


def main():
    s = DATEI.read_text(encoding="utf-8")
    js = (HIER / "auswertung-block.js").read_text(encoding="utf-8")
    css = (HIER / "auswertung-block.css").read_text(encoding="utf-8")

    if JS_A in s:      # zweiter Lauf: nur die Blöcke auffrischen
        s = re.sub(re.escape(JS_A) + ".*?" + re.escape(JS_E), lambda m: JS_A + js + JS_E, s, flags=re.S)
        s = re.sub(re.escape(CSS_A) + ".*?" + re.escape(CSS_E), lambda m: CSS_A + css + CSS_E, s, flags=re.S)
        print("Blöcke aufgefrischt.")
    else:
        for alt, neu in ERSETZ:
            if s.count(alt) != 1:
                sys.exit("FEHLER: Stelle nicht genau einmal gefunden: %s" % alt[:70])
            s = s.replace(alt, neu)
        anker = "  function renderGepostet(main) {"
        if s.count(anker) != 1:
            sys.exit("FEHLER: renderGepostet nicht gefunden.")
        s = s.replace(anker, JS_A + js + JS_E + anker)
        css_anker = "  .page-head { display: flex;"
        if s.count(css_anker) != 1:
            sys.exit("FEHLER: CSS-Anker nicht gefunden.")
        s = s.replace(css_anker, CSS_A + css + CSS_E + css_anker)

    for muss in ("function auswertungEinsetzen(", "daten/auswertung", "auswertungEinsetzen(main)"):
        if muss not in s:
            sys.exit("FEHLER: Gegenprobe fehlt: " + muss)

    teile = re.findall(r"<script>(.*?)</script>", s, re.S)
    if not teile:
        sys.exit("FEHLER: kein <script>-Block.")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(max(teile, key=len))
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("FEHLER node --check:\n" + r.stderr[:800])
    neu = DATEI.with_suffix(".tmp")
    neu.write_text(s, encoding="utf-8")
    os.replace(neu, DATEI)
    print("node --check: in Ordnung · geschrieben:", DATEI)


if __name__ == "__main__":
    main()
