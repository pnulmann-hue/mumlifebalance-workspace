# -*- coding: utf-8 -*-
"""Baut den Reiter „Launch" unter Produkte ins Cockpit.

Anlass: Patricia am 08.10.2026 — *„da frage ich mich, ob es gut wäre, wenn wir
das im cockpit unter instagram z.B. bei funnel reinnehmen? … überlege dir,
inwiefern wir das im cockpit einbauen könnten"*.

Antwort: nicht unter Instagram, sondern unter **Produkte**. Dort liegen Katalog,
Links, Funnel und Listen — ein Launch gehört zum Angebot, nicht zum Kanal. Unter
Instagram stünde er neben der Wochenplanung und würde mit ihr verwechselt.

Vier Blöcke:
  1 Wo stehe ich — welcher Launch läuft, welche Phase, was heute dran ist
  2 Käufertypen diese Woche — sechs Kacheln zum Abhaken
  3 Der Fahrplan — die fünf Phasen mit ihren Aufgaben
  4 Launch anlegen und bearbeiten

🚨 `daten/launch` gehört PATRICIA. Der tägliche Abgleich darf es nie mit `set`
   überschreiben — dieselbe Regel wie bei `daten/produkt-details`,
   `daten/ideenkasten`, `daten/doterra`, `daten/ketten`, `daten/umsatzplan`,
   `suche/x00` und `daten/termine`.

🚨 Der Code liegt bewusst in zwei eigenen Dateien daneben
   (`launch-reiter.js`, `launch-reiter.css`) statt als Zeichenkette im Skript.
   Grund: beim ersten Anlauf am 08.10. waren die Anführungszeichen des JS-Codes
   und die der HTML-Attribute nicht mehr auseinanderzuhalten, und `node --check`
   brach ab. Als eigene Datei lässt sich das JS direkt prüfen.

Wiederholbar: jede Ersetzung prüft vorher, dass sie genau einmal passt.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
JS_DATEI = pathlib.Path(__file__).with_name("launch-reiter.js")
CSS_DATEI = pathlib.Path(__file__).with_name("launch-reiter.css")

AP = chr(34)
HO = chr(39)
BS = chr(92)


def ersetze(t, alt, neu, name):
    if alt not in t:
        sys.exit("🚨 Anker nicht gefunden (%s) — schon gepatcht?" % name)
    if t.count(alt) != 1:
        sys.exit("🚨 Anker %sx gefunden (%s), erwartet 1x" % (t.count(alt), name))
    return t.replace(alt, neu)


# --- Reiter anmelden -------------------------------------------------------
A_TABS = '''    { id: "funnel", label: "Funnel & Keywords" },'''
N_TABS = '''    { id: "launch", label: "Launch" },
    { id: "funnel", label: "Funnel & Keywords" },'''

A_BER = '''      tabs: ["katalog", "produkte", "links", "funnel", "mailings", "leads", "kurse"] },'''
N_BER = '''      tabs: ["katalog", "produkte", "links", "launch", "funnel", "mailings", "leads", "kurse"] },'''

A_DISP = '''    else if (activeTab === "funnel") renderFunnel(main);'''
N_DISP = '''    else if (activeTab === "launch") renderLaunch(main);
    else if (activeTab === "funnel") renderFunnel(main);'''

# --- Laden und Speichern ---------------------------------------------------
A_VAR = '''  var gepostetNotizen = {};   // daten/gepostet-notizen — gehoert PATRICIA'''
N_VAR = '''  var gepostetNotizen = {};   // daten/gepostet-notizen — gehoert PATRICIA
  /* daten/launch — gehoert PATRICIA. Der Abgleich schreibt hier NIE hinein. */
  var launchD = { launches: [], typen: {} };'''

A_LOAD = '''  umsatzplan = lsGet("umsatzplan", { zeilen: [], weitere: 0 }) ||
               { zeilen: [], weitere: 0 };'''
N_LOAD = '''  umsatzplan = lsGet("umsatzplan", { zeilen: [], weitere: 0 }) ||
               { zeilen: [], weitere: 0 };
  launchD = lsGet("launch", { launches: [], typen: {} }) || { launches: [], typen: {} };
  if (!launchD.launches) launchD.launches = [];
  if (!launchD.typen) launchD.typen = {};'''

A_SNAP = '''      db.doc("daten/ketten").onSnapshot(function (snap) {'''
N_SNAP = '''      db.doc("daten/launch").onSnapshot(function (snap) {
        if (!snap.exists) return;
        var d0 = snap.data() || {};
        /* Lokal neuer gewinnt — die Lehre vom 24.09.2026: Arbeit zurueckholen
           ist unmoeglich, einen alten Anzeigestand erneuern ein Klick. */
        if (launchD && launchD.updatedAt && (!d0.updatedAt || d0.updatedAt < launchD.updatedAt)) return;
        launchD = { launches: d0.launches || [], typen: d0.typen || {}, updatedAt: d0.updatedAt };
        lsSet("launch", launchD);
        if (activeTab === "launch") render();
      }, function () {});
      db.doc("daten/ketten").onSnapshot(function (snap) {'''

EINHAENGEN = '  function renderBereiche() {'


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("🚨 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    js = JS_DATEI.read_text(encoding="utf-8")
    css = CSS_DATEI.read_text(encoding="utf-8")

    pruefe_js(js, "launch-reiter.js")

    # Kein Umlaut in einem JS-Bezeichner (Lehre: `bruecke` statt `br<ue>cke`).
    # Texte, Kommentare und Zeichenketten werden vorher herausgefiltert.
    muster = "|".join([AP + "[^" + AP + "]*" + AP,
                       HO + "[^" + HO + "]*" + HO,
                       r"/\*.*?\*/",
                       "//[^" + BS + "n]*"])
    ohne = re.sub(muster, " ", js, flags=re.S)
    schlecht = sorted(set(re.findall(
        r"\w*[äöüÄÖÜß]\w*", ohne)))
    if schlecht:
        sys.exit("🚨 Umlaut in einem JS-Bezeichner: %s" % schlecht)

    t = ZIEL.read_text(encoding="utf-8")
    vorher = len(t)
    if "function renderLaunch(" in t:
        sys.exit("🚨 renderLaunch steht schon drin — erst zurueckbauen")

    t = ersetze(t, A_TABS, N_TABS, "TABS")
    t = ersetze(t, A_BER, N_BER, "BEREICHE")
    t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
    t = ersetze(t, A_VAR, N_VAR, "Variable")
    t = ersetze(t, A_LOAD, N_LOAD, "Laden")
    t = ersetze(t, A_SNAP, N_SNAP, "onSnapshot")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "renderLaunch")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    # Gegenprobe ueber das ganze eingebettete Skript
    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    ZIEL.write_text(t, encoding="utf-8")
    print("mlb-cockpit.html: %d -> %d Zeichen" % (vorher, len(t)))
    print("node --check gruen (JS einzeln und ganze Seite)")
    print("Reiter: Produkte -> Launch · 5 Phasen · 6 Kaeufertypen")
    print("🚨 Noch nicht veroeffentlicht — "
          "siehe outputs/cockpit/OFFEN-noch-nicht-veroeffentlicht.md")


if __name__ == "__main__":
    main()
