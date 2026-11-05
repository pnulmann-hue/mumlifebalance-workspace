"""Block „Fürs Team“ im Reiter doTERRA → Rising Leaders (05.11.2026).

Patricia: *„ich würde gerne meine teammitglieder enger begleiten … vielleicht zwei impulse rsp.
aufgaben?“* Montag eine Aufgabe, Donnerstag ein Impuls, aus `doterra-wissen/team-impulse`, das die
Routine `rise-to-lead` schreibt. Ihre Änderungen und „verschickt“ stehen in `daten/rising-leaders`
unter `impulse`. Heute dran zeigt, was wartet. Der Team-Funke meldet sich nicht mehr von selbst
(sonst wären es drei Nachrichten pro Woche), er bleibt zum Aufklappen für Erfolge und persönliche
Nachrichten.

Setzt patch-teamfunke.py und patch-heutedran.py voraus. Code und CSS in `teamimpuls.js` / `.css`.

    python scripts/cockpit/patch-teamimpuls.py [--datei <cockpit.html>]
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
JS_DATEI = HIER / "teamimpuls.js"
CSS_DATEI = HIER / "teamimpuls.css"

A_KOPF = '''    var h = trHtml() + tfHtml() + eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''
N_KOPF = '''    var h = trHtml() + tiImpulsHtml() + tfHtml() + eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +'''

A_BIND = '''    tfBinden(main);'''
N_BIND = '''    tfBinden(main);
    tiImpulsBinden(main);'''

# Der Team-Funke drängt nicht mehr: zwei Nachrichten pro Woche sind genug.
A_FAELLIG = '''  function tfFaellig() {
    var F = dtRising.funke || {};'''
N_FAELLIG = '''  function tfFaellig() {
    return false; // seit 05.11.: ersetzt durch „Fürs Team“ (Mo Aufgabe, Do Impuls)
    var F = dtRising.funke || {};'''

A_FUNKE_TEXT = '''(letzte ? "zuletzt am " + esc(dtDatum(letzte.datum)) : "die Wochennachricht für dein Team")'''
N_FUNKE_TEXT = '''(letzte ? "zuletzt am " + esc(dtDatum(letzte.datum)) : "Erfolge feiern und persönliche Nachrichten")'''
A_FUNKE_NOTIZ = '''Einmal die Woche, am besten sonntags: Du trägst ein, was gelaufen ist, ich schreibe die Nachricht für eure Gruppe. Verschickt wird nichts, das machst du selbst.'''
N_FUNKE_NOTIZ = '''Wenn du etwas feiern oder jemanden persönlich anschreiben willst: Du trägst ein, was gelaufen ist, ich schreibe die Nachricht. Verschickt wird nichts, das machst du selbst.'''

A_HEUTE = '''    if (tfFaellig()) P.push({ art: "doterra", titel: "Team-Funke für diese Woche", klein: "Die Wochennachricht an dein Team ist noch nicht raus.", gehe: "rising" });'''
N_HEUTE = '''    tiImpulsOffen().forEach(function (x) {
      P.push({ art: "doterra", titel: (x.art === "aufgabe" ? "Team-Aufgabe" : "Team-Impuls") + " schicken", klein: x.titel || "", gehe: "rising" });
    });'''

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
    if "function tfHtml(" not in t or "function hdHtml(" not in t:
        sys.exit("🚨 Team-Funke oder Heute dran fehlt — zuerst deren Patches.")
    if "function tiImpulsHtml(" in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    vorher = len(t)

    t = ersetze(t, A_KOPF, N_KOPF, "Rising-Kopf")
    t = ersetze(t, A_BIND, N_BIND, "Binden")
    t = ersetze(t, A_FAELLIG, N_FAELLIG, "tfFaellig")
    t = ersetze(t, A_FUNKE_TEXT, N_FUNKE_TEXT, "Funke-Zeile")
    t = ersetze(t, A_FUNKE_NOTIZ, N_FUNKE_NOTIZ, "Funke-Notiz")
    t = ersetze(t, A_HEUTE, N_HEUTE, "Heute dran")
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
