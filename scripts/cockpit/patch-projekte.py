"""Hängt den Projekte-Block unten in den Reiter «Aufgaben».

24 Projekte aus Notion, mit Zeitraum und den Aufgaben, die daran hängen.

🚨 **Kein eigener Reiter.** Ein Projekt ist eine Klammer um Aufgaben, keine
eigene Welt — und ein zwölfter Reiter macht das Cockpit unübersichtlicher, ohne
etwas zu zeigen, das hier nicht auch passt. Dass es kein Doppel zum Jahresplan
ist, wurde vorher geprüft: nur 2 von 24 stehen dort auch.

🚨 **«Ohne Status» ist eine eigene Anzeige, nicht leer.** In Notion war das
Statusfeld ein E-Mail-Feld, und bei 11 von 24 stand gar nichts drin. Ein leeres
Feld sieht aus wie erledigt; deshalb steht es ausgeschrieben da.

🚨 **Der Widerspruch wird angezeigt, nicht aufgelöst.** Drei Projekte stehen auf
«Läuft», obwohl ihr Zeitraum lange vorbei ist. Das ist kein Datenfehler, den ein
Skript geradebiegen darf — es ist dieselbe Lage wie bei den überfälligen
Aufgaben, und sie gehört Patricia vorgelegt.

    python scripts/cockpit/patch-projekte.py [--pruefen]
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
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

VAR_ALT = '  var steuer = null;             // daten/steuer — Abgleich'
VAR_NEU = ('  var steuer = null;             // daten/steuer — Abgleich\n'
           '  var projekte = null;           // daten/projekte — gehoert PATRICIA')

LS_ALT = '  steuer = lsGet("steuer", null);'
LS_NEU = ('  steuer = lsGet("steuer", null);\n'
          '  projekte = lsGet("projekte", null);')

SNAP_ALT = '''      db.doc("daten/steuer").onSnapshot(function (snap) {
        if (!snap.exists) return;
        steuer = snap.data() || null;
        lsSet("steuer", steuer);
        if (activeTab === "zahlen") render();
      }, function () {});'''
SNAP_NEU = SNAP_ALT + '''
      db.doc("daten/projekte").onSnapshot(function (snap) {
        if (!snap.exists) return;
        projekte = snap.data() || null;
        lsSet("projekte", projekte);
        if (activeTab === "aufgaben") render();
      }, function () {});'''

AUFRUF_ALT = '''    main.querySelector("#afneu").onclick = function () {
      aufgaben.items.unshift({
        id: uid("af"), aufgabe: "", datum: todayISO(), prio: "Mittel",
        status: "Geplant", notiz: "", erledigt: false, quelle: "Cockpit"
      });
      afSpeichern(); render();
    };
  }'''

AUFRUF_NEU = r'''    main.querySelector("#afneu").onclick = function () {
      aufgaben.items.unshift({
        id: uid("af"), aufgabe: "", datum: todayISO(), prio: "Mittel",
        status: "Geplant", notiz: "", erledigt: false, quelle: "Cockpit"
      });
      afSpeichern(); render();
    };

    projekteBlock(main);
  }

  /* =========================================================
     Projekte — die Klammer um die Aufgaben.

     Kein eigener Reiter: ein Projekt ist eine Gruppe von Aufgaben.
     «Ohne Status» steht ausgeschrieben da, weil ein leeres Feld wie
     erledigt aussieht. Wo «Läuft» steht und der Zeitraum vorbei ist,
     wird der Widerspruch gezeigt, nicht stillschweigend korrigiert.
     ========================================================= */
  function projekteBlock(main) {
    var items = (projekte && projekte.items) || [];
    var h = '<h2 style="margin-top:34px">Projekte</h2>';

    if (!items.length) {
      main.insertAdjacentHTML("beforeend", h +
        '<div class="card"><p class="muted">Noch nichts übernommen:<br>' +
        '<code>python scripts/cockpit/projekte-importieren.py</code></p></div>');
      return;
    }

    var heute = todayISO();
    // Widerspruch: steht auf «Läuft», Zeitraum ist aber durch.
    var haengt = items.filter(function (p) {
      return p.zustand === "Läuft" && p.vorbei;
    });
    var ohne = items.filter(function (p) { return p.zustand === "Ohne Status"; });

    function zeile(p) {
      var wann = p.von
        ? esc(p.von.slice(8) + "." + p.von.slice(5, 7) + "." +
              (p.bis ? " – " + p.bis.slice(8) + "." + p.bis.slice(5, 7) + "." + p.bis.slice(2, 4) : ""))
        : "—";
      var fahne = "";
      if (p.zustand === "Läuft" && p.vorbei) {
        fahne = ' <span class="warn" title="Steht auf Läuft, der Zeitraum ist aber vorbei">' +
                "Zeitraum durch</span>";
      }
      return "<tr" + (p.laeuft ? ' style="font-weight:600"' : "") + ">" +
        "<td>" + (p.laeuft ? "▶ " : "") + esc(p.name) + fahne + "</td>" +
        "<td>" + (p.zustand === "Ohne Status"
          ? '<span class="muted">Ohne Status</span>' : esc(p.zustand)) + "</td>" +
        "<td>" + esc(p.prio || "—") + "</td>" +
        "<td>" + wann + "</td>" +
        '<td style="text-align:right">' +
          (p.aufgaben ? p.aufgaben + " Aufgaben" : '<span class="muted">—</span>') +
        "</td></tr>";
    }

    var laeuft = items.filter(function (p) { return p.laeuft; });
    var kommt = items.filter(function (p) { return !p.laeuft && !p.vorbei; });
    var vorbei = items.filter(function (p) { return p.vorbei; });

    function gruppe(titel, ps) {
      if (!ps.length) return "";
      return '<tr><td colspan="5" class="muted" style="padding-top:14px">' +
        esc(titel) + " · " + ps.length + "</td></tr>" + ps.map(zeile).join("");
    }

    main.insertAdjacentHTML("beforeend", h +
      '<div class="card">' +
      '<div class="tiles" style="margin-bottom:14px">' +
      tile("Läuft gerade", laeuft.length, "im Zeitraum") +
      tile("Kommt noch", kommt.length, "Start in der Zukunft") +
      tile("Zeitraum durch", haengt.length, "steht aber auf «Läuft»") +
      tile("Ohne Status", ohne.length, "in Notion war das Feld leer") +
      "</div>" +
      '<table class="tbl"><thead><tr><th>Projekt</th><th>Zustand</th>' +
      "<th>Priorität</th><th>Zeitraum</th>" +
      '<th style="text-align:right">hängt dran</th></tr></thead><tbody>' +
      gruppe("Läuft gerade", laeuft) +
      gruppe("Kommt noch", kommt) +
      gruppe("Vorbei", vorbei) +
      "</tbody></table>" +
      '<p class="muted" style="margin-top:14px">' +
      esc((projekte && projekte.hinweis) || "") + "</p></div>");
  }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    bloecke = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    for i, block in enumerate(bloecke):
        if len(block.strip()) < 200:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(block)
            p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        Path(p).unlink(missing_ok=True)
        if r.returncode != 0:
            return "Block %d: %s" % (i, (r.stderr or "")[:600])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = SEITE.read_text(encoding="utf-8")

    if "projekteBlock(main)" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, VAR_ALT, VAR_NEU, "Variable")
    s = setze(s, LS_ALT, LS_NEU, "localStorage-Laden")
    s = setze(s, SNAP_ALT, SNAP_NEU, "Datenbank-Abo")
    s = setze(s, AUFRUF_ALT, AUFRUF_NEU, "renderAufgaben-Ende")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    SEITE.write_text(s, encoding="utf-8")
    print("  Projekte-Block eingebaut · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
