"""Gepostete Beiträge rutschen aus «Freigegeben» heraus.

Patricia am 24.09.2026: *„Ich prüfe, gebe frei und sie rutschen dann weiter in
den nächsten Reiter freigegeben und sobald sie auf insta gepostet sind, rutschen
sie auf gepostet."*

**Vier Stationen, ein Beitrag wandert durch:**

| Station | Reiter | Bedingung |
|---|---|---|
| Planen | Wochen-Vorschau | noch nicht freigegeben |
| Freigegeben | Freigeben | `textfrei`, aber kein Instagram-Post gefunden |
| **Gepostet** | Gepostet & Analyse | in `daten/gepostet-zuordnung` |
| Recycling | derselbe Reiter | gut gelaufen und ≥28 Tage her |

🚨 **Die Zuordnung ist die neue Zutat**, gebaut von `gepostet-zuordnen.py`
über den Caption-Anfang. Ohne sie weiss das Cockpit nicht, dass Beitrag X und
Instagram-Post Y dasselbe sind — deshalb rutschte bisher nichts weiter.

🚨 **Eine fehlende Zuordnung heisst nicht „nicht gepostet".** Das
doTERRA-Konto hängt nicht an der Graph API; für dessen sieben Beiträge kann es
nie eine geben. Sie bleiben unter „Ist durch" stehen und tragen den Vermerk
„nicht prüfbar" — nie „wartet noch".

🚨 **Was gepostet ist, trägt seine Zahl.** Auf der Zeile steht die Reichweite,
sonst ist „gepostet" nur ein Wort. Die vier Beiträge im Bestand: 234 · 207 ·
184 · **54** — der mit 54 ist das Dienstags-Karussell, und das ist der Befund,
der wirklich zählt.

    python scripts/cockpit/patch-fliessband.py [--pruefen] [--datei <pfad>]
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

# --------------------------------------------------- 1 · Zuordnung laden

ALT_VAR = '''  var freigaben = {};'''
NEU_VAR = '''  var freigaben = {};

  /* 🚨 Welcher Beitrag ist als Instagram-Post wiedergefunden worden?
     Gebaut von gepostet-zuordnen.py ueber den Caption-Anfang. Ohne das weiss
     das Cockpit nicht, dass Beitrag X und Post Y dasselbe sind. */
  var igZuordnung = { zuordnung: {}, nicht_pruefbar: [] };
  function igPost(b) {
    return (igZuordnung.zuordnung || {})[(b && b.id) || ""] || null;
  }
  function istGepostet(b) { return !!igPost(b); }
  function nichtPruefbar(b) {
    // Das doTERRA-Konto haengt nicht an der Graph API. Fehlende Zuordnung
    // heisst dort NICHT „nicht gepostet".
    return (kartenProfil(b.obj) === "doterra") && !igPost(b);
  }'''

ALT_LADE = '''      db.collection("freigaben").limit(300).get().then(function (qs) {'''
NEU_LADE = '''      db.doc("daten/gepostet-zuordnung").onSnapshot(function (snap) {
        if (!snap.exists) return;
        igZuordnung = snap.data() || { zuordnung: {} };
        lsSet("ig-zuordnung", igZuordnung);
        render();
      }, function () {});
      db.collection("freigaben").limit(300).get().then(function (qs) {'''

ALT_INIT = '''  freigaben = lsGet("freigaben", {}) || {};'''
NEU_INIT = '''  freigaben = lsGet("freigaben", {}) || {};
  igZuordnung = lsGet("ig-zuordnung", { zuordnung: {} }) || { zuordnung: {} };'''

# ------------------------------------------------- 2 · Gruppen im Reiter

ALT_GRUPPEN = '''    var laeuft = frei.filter(function (b) { return haengt.indexOf(b) < 0; });'''
NEU_GRUPPEN = '''    // Was auf Instagram wiedergefunden wurde, ist durch und gehoert in den
    // Reiter „Gepostet & Analyse" — nicht mehr hierher.
    var gepostet = frei.filter(istGepostet);
    var laeuft = frei.filter(function (b) {
      return haengt.indexOf(b) < 0 && !istGepostet(b);
    });'''

ALT_KACHEL = '''      tile("Ist durch", laeuft.length,
           selbst.length ? selbst.length + " davon in deiner App"
                         : "eingeplant oder schon raus") +'''
NEU_KACHEL = '''      tile("Unterwegs", laeuft.length,
           selbst.length ? selbst.length + " davon in deiner App"
                         : "eingeplant, noch nicht raus") +
      tile("Gepostet", gepostet.length,
           gepostet.length ? "steht unter „Gepostet & Analyse“" : "noch keiner") +'''

ALT_AUFRUF = '''    liste("Ist durch", selbst.length
      ? "Liegt bei Blotato oder ist schon raus. " + selbst.length + " davon hast "
        + "du selbst in der App eingeplant \\u2014 B-Roll und Storys gehen nie "
        + "\\u00fcber Blotato, weil die Musik nur dort w\\u00e4hlbar ist."
      : "Liegt bei Blotato oder ist schon raus. Hier musst du nichts mehr tun.",
      laeuft, "ich");'''

NEU_AUFRUF = '''    liste("Unterwegs", selbst.length
      ? "Eingeplant, aber noch nicht im Feed. " + selbst.length + " davon hast "
        + "du selbst in der App eingeplant \\u2014 B-Roll und Storys gehen nie "
        + "\\u00fcber Blotato, weil die Musik nur dort w\\u00e4hlbar ist."
      : "Eingeplant, aber noch nicht im Feed. Hier musst du nichts mehr tun.",
      laeuft, "ich");

    liste("Gepostet", "Auf Instagram wiedergefunden. Die Auswertung steht unter "
      + "\\u201eGepostet & Analyse\\u201c \\u2014 dort liegt auch der Knopf, um "
      + "einen gut gelaufenen Beitrag nach vier Wochen nochmal zu bringen.",
      gepostet, "ich");'''

# ---------------------------------------- 3 · Reichweite auf der Zeile

ALT_STAND = '''        var stand = s === "gepostet-von-hand" ? "selbst gepostet"
                  : s === "geplant" ? "eingeplant"
                  : b.art === "storys" ? "Story"
                  : s === "selber-posten" ? "in deiner App"
                  : "wartet";'''
NEU_STAND = '''        // 🚨 Was gepostet ist, traegt seine Zahl — sonst ist „gepostet"
        // nur ein Wort.
        var ig = igPost(b);
        var stand = ig ? (ig.reach != null ? ig.reach + " erreicht" : "gepostet")
                  : nichtPruefbar(b) ? "in deiner App · nicht prüfbar"
                  : s === "gepostet-von-hand" ? "selbst gepostet"
                  : s === "geplant" ? "eingeplant"
                  : b.art === "storys" ? "Story"
                  : s === "selber-posten" ? "in deiner App"
                  : "wartet";'''

# Ist-raus-Vermerk auf der Wochenkarte soll die Zahl auch zeigen.
ALT_GRUND = '''  function draussenGrund(b) {
    var s = draussenStatus(b);'''
NEU_GRUND = '''  function draussenGrund(b) {
    var ig = (typeof igPost === "function") && igPost(b);
    if (ig) return ig.reach != null ? "gepostet · " + ig.reach + " erreicht"
                                    : "gepostet";
    var s = draussenStatus(b);'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


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
    if "igZuordnung" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_VAR, NEU_VAR, "Zuordnung")
    s = setze(s, ALT_LADE, NEU_LADE, "Ladestelle")
    s = setze(s, ALT_INIT, NEU_INIT, "Init")
    s = setze(s, ALT_GRUPPEN, NEU_GRUPPEN, "Gruppen")
    s = setze(s, ALT_KACHEL, NEU_KACHEL, "Kachel")
    s = setze(s, ALT_AUFRUF, NEU_AUFRUF, "Aufruf")
    s = setze(s, ALT_STAND, NEU_STAND, "Stand")
    s = setze(s, ALT_GRUND, NEU_GRUND, "draussenGrund")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Fliessband eingebaut · %d KB" % (len(s) / 1024))
    print("  Planen → Freigegeben → Unterwegs → Gepostet (mit Reichweite).")


if __name__ == "__main__":
    main()
