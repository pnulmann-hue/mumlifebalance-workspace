# -*- coding: utf-8 -*-
"""Die Ideenliste war am Handy nicht erreichbar.

Patricia am 08.10.2026: *„nochmal unter instagram planen gibt es keine
ideenliste"* und *„auf dem handy fuer mich nicht sichtbar"*.

Sie hatte recht, und es war kein Suchproblem. Im Reiter „Planen" steht die
Ideenliste ganz unten, und davor liegt **„Was wann rausgeht"** mit ALLEN
Terminen ueber ALLE Wochen — am 08.10. waren das **ueber hundert Zeilen**
(75 allein aus Karussells und Storys). Am Rechner scrollt man das, am Handy
gibt man vorher auf. Geprueft: in der ganzen Seite gibt es keine einzige
Handy-Regel mit `display:none`, die Liste war also da und trotzdem nicht
erreichbar.

**Die Aenderung:** „Was wann rausgeht" wird ein aufklappbarer Block, der
**zugeklappt startet**. Die Zahl steht in der Zeile, damit man sieht, was
drin ist. Die Ideenliste rutscht damit direkt unter die Wochen-Uebersicht.

🚨 **Zugeklappt heisst nicht weg.** Die Termine sind die Antwort auf „was geht
   wann raus" und bleiben einen Fingertipp entfernt. Geloescht oder in einen
   anderen Reiter verschoben wird nichts — zwei Ansichten auf dieselben Daten
   laufen beim naechsten Umbau auseinander (Lehre vom 19.09.2026, Tagesplan).

Wiederholbar: die Ersetzung muss genau einmal passen, danach `node --check`.
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ALT = """    var plan = document.createElement("div");
    plan.className = "panel uebersicht";
    plan.innerHTML = '<h2>Was wann rausgeht</h2>' +
      '<p class="note">Alle ' + mitDatum.length + ' Beitr\\u00e4ge mit Datum, ' +
      '\\u00fcber alle Wochen \\u2014 auch die, die oben gerade nicht im Bild sind.</p>';"""

NEU = """    // 🚨 Aufklappbar und ZUGEKLAPPT, seit 08.10.2026. Ueber hundert Zeilen
    //    standen vor der Ideenliste, und am Handy kam dort niemand mehr an.
    var plan = document.createElement("details");
    plan.className = "panel uebersicht uetermine";
    plan.innerHTML = '<summary><h2>Was wann rausgeht</h2>' +
      '<span class="uezahl">' + mitDatum.length + '</span></summary>' +
      '<p class="note">Alle ' + mitDatum.length + ' Beitr\\u00e4ge mit Datum, ' +
      '\\u00fcber alle Wochen \\u2014 auch die, die oben gerade nicht im Bild sind.</p>';"""

CSS_ANKER = "  .la-hint { color: var(--ink-soft); font-size: 13px; margin: 4px 0 0; }"
CSS_NEU = """  /* „Was wann rausgeht" als aufklappbarer Block (08.10.2026) */
  .uetermine > summary { cursor: pointer; display: flex; align-items: center;
                         gap: 10px; list-style: none; }
  .uetermine > summary::-webkit-details-marker { display: none; }
  .uetermine > summary h2 { margin: 0; }
  .uetermine > summary::after { content: "\\25be"; margin-left: auto;
                                color: var(--ink-soft); font-size: 18px; }
  .uetermine[open] > summary::after { content: "\\25b4"; }
  .uezahl { background: var(--surface-2); color: var(--ink-soft);
            border-radius: 99px; padding: 2px 10px; font-size: 13px; }
""" + CSS_ANKER


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("\U0001f6a8 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    t = ZIEL.read_text(encoding="utf-8")
    if "uetermine" in t:
        sys.exit("\U0001f6a8 schon gepatcht")
    for name, alt in (("Markup", ALT), ("CSS", CSS_ANKER)):
        if t.count(alt) != 1:
            sys.exit("\U0001f6a8 %s: Anker %sx gefunden, erwartet 1x"
                     % (name, t.count(alt)))
    t = t.replace(ALT, NEU).replace(CSS_ANKER, CSS_NEU)

    # Gegenprobe: die Ideenliste steht weiterhin danach und wurde nicht
    # angefasst — sie ist der Grund fuer die ganze Aenderung.
    if t.find(">Ideenliste") < t.find("uetermine"):
        sys.exit("\U0001f6a8 Reihenfolge verdreht")
    if t.count(">Ideenliste") != 1:
        sys.exit("\U0001f6a8 Ideenliste %sx" % t.count(">Ideenliste"))

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")
    ZIEL.write_text(t, encoding="utf-8")
    print("„Was wann rausgeht“ ist jetzt aufklappbar und startet zu.")
    print("Die Ideenliste steht damit direkt unter der Wochen-Übersicht.")
    print("node --check gruen")


if __name__ == "__main__":
    main()
