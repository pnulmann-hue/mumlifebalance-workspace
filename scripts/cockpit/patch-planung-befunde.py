"""Zeigt die Workspace-Befunde bei Jahresplan und Zielen an.

Patricia am 24.09.2026: *„kannst du bitte auch den bereich planung mit den daten
aus dem workspace abgleichen? in notion waren teilweise inhalte veraltet"*.

`planung-abgleichen.py` hat die Befunde gebaut, dieser Patch macht sie sichtbar.

| Befund | heisst |
|---|---|
| **belegt** | es gibt Spuren im Workspace — Produktordner, Funnel, Checkout, Plan |
| **offen** | Spuren da, Termin liegt noch vorn |
| **keine Spur** | nichts gefunden — **eine Frage, kein Urteil** |
| **Termin** | Ferien, Convention — hinterlässt nie eine Spur |
| **abgelaufen** | (Ziele) Quartal vorbei, Status steht noch auf „Aktiv" |

🚨 **Die Befunde liegen in `daten/planung-abgleich`, nicht im Jahresplan.**
Jahresplan und Ziele gehören Patricia und werden nie überschrieben — dasselbe
Muster wie `daten/gepostet` gegenüber `daten/gepostet-notizen`.

🚨 **„Keine Spur" steht nie allein da.** Unter jeder Liste steht, dass ein
Leadmagnet in ManyChat leben kann, ohne je eine Datei zu bekommen. Ein Befund,
der wie ein Vorwurf aussieht, wird entweder geglaubt und ist dann falsch — oder
er wird ignoriert, und dann war die ganze Liste umsonst.

    python scripts/cockpit/patch-planung-befunde.py [--pruefen] [--datei <pfad>]
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

ALT_VAR = '''  var ideenExtern = { ideen: [] };'''
NEU_VAR = '''  var ideenExtern = { ideen: [] };

  /* Befunde aus dem Workspace-Abgleich. 🚨 Sie liegen NEBEN Jahresplan und
     Zielen, nicht darin — die beiden gehoeren Patricia. Siehe Kopf von
     patch-planung-befunde.py. */
  var planungAbgleich = { jahresplan: {}, ziele: {} };
  function befundVon(bereich, id) {
    return ((planungAbgleich[bereich] || {})[id]) || null;
  }
  var BEFUND_TEXT = {
    belegt: "im Workspace belegt",
    offen: "steht noch aus",
    keine_spur: "keine Spur im Workspace",
    termin: "Termin",
    abgelaufen: "Quartal vorbei, Status noch aktiv",
    nicht_messbar: "nicht maschinell prüfbar"
  };
  var BEFUND_ART = {
    belegt: "gut", offen: "info", keine_spur: "warn",
    termin: "info", abgelaufen: "warn", nicht_messbar: "info"
  };
  function befundChip(bereich, id) {
    var b = befundVon(bereich, id);
    if (!b || !b.befund) return "";
    var titel = (b.belege || []).map(function (x) { return x.wo; }).join(" · ");
    return '<span class="tp-stand ' + (BEFUND_ART[b.befund] || "info") + '"' +
      (titel ? ' title="' + esc(titel) + '"' : "") + '>' +
      esc(BEFUND_TEXT[b.befund] || b.befund) + '</span>';
  }
  var ABGLEICH_HINWEIS =
    "„Keine Spur“ heisst NICHT „nicht passiert“ — ein Leadmagnet kann in " +
    "ManyChat leben, ohne je eine Datei zu bekommen. Fahr mit der Maus über " +
    "einen Befund, dann siehst du, worauf er sich stützt.";'''

ALT_LADE = '''      db.doc("daten/ideen-extern").onSnapshot(function (snap) {'''
NEU_LADE = '''      db.doc("daten/planung-abgleich").onSnapshot(function (snap) {
        if (!snap.exists) return;
        planungAbgleich = snap.data() || { jahresplan: {}, ziele: {} };
        lsSet("planung-abgleich", planungAbgleich);
        if (activeTab === "launches" || activeTab === "ziele") render();
      }, function () {});
      db.doc("daten/ideen-extern").onSnapshot(function (snap) {'''

ALT_INIT = '''  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };'''
NEU_INIT = '''  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };
  planungAbgleich = lsGet("planung-abgleich", { jahresplan: {}, ziele: {} })
    || { jahresplan: {}, ziele: {} };'''


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
    if "planungAbgleich" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_VAR, NEU_VAR, "Variable")
    s = setze(s, ALT_LADE, NEU_LADE, "Ladestelle")
    s = setze(s, ALT_INIT, NEU_INIT, "Init")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Befunde geladen · %d KB" % (len(s) / 1024))
    print("  ⚠️ Angezeigt werden sie im zweiten Schritt (Jahresplan + Ziele).")


if __name__ == "__main__":
    main()
