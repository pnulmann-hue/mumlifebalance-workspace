"""Hängt das Öl-Nachschlagewerk unten in den Reiter «Rang-Tracker».

21 Öle und 22 Wirkbereiche aus Notion, in beide Richtungen durchsuchbar.

🚨 **Die Compliance-Warnung steht ganz oben im Block, nicht im Kleingedruckten.**
Eine Tabelle «Beschwerde → Öl» ist genau das, was doTERRA als Heilversprechen
verbietet. Sie liegt hier, weil Patricia sie zum Nachschlagen braucht — und
genau deshalb ist die Gefahr gross, dass eine Zeile daraus in eine Caption
wandert. Eine Warnung unten im Fuss hätte den Zweck verfehlt.

🚨 **Kein eigener Reiter.** Der doTERRA-Bereich hat einen; ein zweiter für 21
Zeilen macht die Leiste länger, ohne etwas zu gewinnen.

🚨 **Die Lücken stehen als Zahl da.** 13 der 21 Öle haben keinen Wirkbereich.
Wer das nicht sieht, sucht einen Bereich, findet nichts und schliesst daraus,
es gebe kein Öl dafür.

    python scripts/cockpit/patch-doterra-produkte.py [--pruefen]
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

VAR_ALT = '  var projekte = null;           // daten/projekte — gehoert PATRICIA'
VAR_NEU = ('  var projekte = null;           // daten/projekte — gehoert PATRICIA\n'
           '  var dtProdukte = null;         // daten/doterra-produkte — gehoert PATRICIA')

LS_ALT = '  projekte = lsGet("projekte", null);'
LS_NEU = ('  projekte = lsGet("projekte", null);\n'
          '  dtProdukte = lsGet("doterra-produkte", null);')

SNAP_ALT = '''      db.doc("daten/projekte").onSnapshot(function (snap) {
        if (!snap.exists) return;
        projekte = snap.data() || null;
        lsSet("projekte", projekte);
        if (activeTab === "aufgaben") render();
      }, function () {});'''
SNAP_NEU = SNAP_ALT + '''
      db.doc("daten/doterra-produkte").onSnapshot(function (snap) {
        if (!snap.exists) return;
        dtProdukte = snap.data() || null;
        lsSet("doterra-produkte", dtProdukte);
        if (activeTab === "rangtracker") render();
      }, function () {});'''

# 🚨 `main.appendChild(fuss);` steht DREIMAL im Cockpit — der Waechter in
# setze() hat das gemeldet, statt die falsche Stelle zu treffen. Eindeutig wird
# der Anker erst mit der Fuss-Zeile darueber, die den Schlagdistanz-Bericht
# nennt. Ein Anker, der mehrfach passt, ist kein Anker.
FUSS = ('      ". Der Monat läuft noch, die Zahlen wachsen bis zum '
        'Monatsende.";\n')

AUFRUF_ALT = FUSS + '    main.appendChild(fuss);\n  }'

AUFRUF_NEU = FUSS + r'''    main.appendChild(fuss);

    oeleBlock(main);
  }

  /* =========================================================
     Öle und Wirkbereiche — internes Nachschlagen.

     ACHTUNG: Diese Zuordnung darf nie in Content. Die Warnung steht
     deshalb als erstes im Block und nicht im Fuss.
     ========================================================= */
  var oelSuche = "";

  function oeleBlock(main) {
    var d = dtProdukte;
    var h = document.createElement("h2");
    h.style.marginTop = "34px";
    h.textContent = "Öle und Wirkbereiche";
    main.appendChild(h);

    var karte = document.createElement("div");
    karte.className = "card";

    if (!d || !(d.produkte || []).length) {
      karte.innerHTML = '<p class="muted">Noch nichts übernommen:<br>' +
        '<code>python scripts/cockpit/doterra-produkte-importieren.py</code></p>';
      main.appendChild(karte);
      return;
    }

    var q = (oelSuche || "").trim().toLowerCase();
    function passt(name, liste) {
      if (!q) return true;
      if (name.toLowerCase().indexOf(q) >= 0) return true;
      return (liste || []).some(function (x) {
        return x.toLowerCase().indexOf(q) >= 0;
      });
    }

    var oele = (d.produkte || []).filter(function (p) {
      return passt(p.name, p.bereiche);
    });
    var bereiche = (d.bereiche || []).filter(function (b) {
      return passt(b.name, b.oele);
    });

    function spalte(titel, zeilen) {
      return '<div style="flex:1;min-width:280px">' +
        "<h3>" + esc(titel) + "</h3>" + zeilen + "</div>";
    }

    var oelZeilen = oele.map(function (p) {
      return '<div style="margin-bottom:10px">' +
        "<b>" + esc(p.name) + "</b>" +
        (p.anzahl
          ? '<br><span class="muted">' + esc(p.bereiche.join(" · ")) + "</span>"
          : '<br><span class="warn">kein Wirkbereich hinterlegt</span>') +
        "</div>";
    }).join("") || '<p class="muted">Nichts gefunden.</p>';

    var berZeilen = bereiche.map(function (b) {
      return '<div style="margin-bottom:10px">' +
        "<b>" + esc(b.name) + "</b>" +
        (b.anzahl
          ? '<br><span class="muted">' + esc(b.oele.join(" · ")) + "</span>"
          : '<br><span class="warn">kein Öl hinterlegt</span>') +
        "</div>";
    }).join("") || '<p class="muted">Nichts gefunden.</p>';

    karte.innerHTML =
      '<div class="warnbox" style="border:2px solid var(--orange);' +
      'border-radius:10px;padding:14px;margin-bottom:18px">' +
      '<b>Nur zum Nachschlagen — nie in Content.</b><br>' +
      '<span class="muted">' + esc(d.warnung || "") + "</span></div>" +
      '<div class="field" style="max-width:340px;margin-bottom:16px">' +
      '<label for="oelsuche">Öl oder Bereich suchen</label>' +
      '<input id="oelsuche" type="search" placeholder="z.B. Schlaf oder Serenity" value="' +
      esc(oelSuche) + '"></div>' +
      '<div style="display:flex;gap:28px;flex-wrap:wrap">' +
      spalte("Vom Öl aus (" + oele.length + ")", oelZeilen) +
      spalte("Vom Bereich aus (" + bereiche.length + ")", berZeilen) +
      "</div>" +
      '<p class="muted" style="margin-top:14px">' + esc(d.hinweis || "") + "</p>";

    main.appendChild(karte);

    var feld = karte.querySelector("#oelsuche");
    feld.oninput = function () {
      oelSuche = feld.value;
      // Nur diesen Block neu zeichnen, damit der Rang-Tracker daruber
      // nicht bei jedem Tastendruck neu aufgebaut wird.
      var neu = document.createElement("div");
      oeleBlock(neu);
      karte.innerHTML = neu.querySelector(".card").innerHTML;
      var f2 = karte.querySelector("#oelsuche");
      f2.oninput = feld.oninput;
      f2.focus();
      f2.setSelectionRange(f2.value.length, f2.value.length);
    };
  }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    bloecke = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
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

    if "oeleBlock(main)" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, VAR_ALT, VAR_NEU, "Variable")
    s = setze(s, LS_ALT, LS_NEU, "localStorage-Laden")
    s = setze(s, SNAP_ALT, SNAP_NEU, "Datenbank-Abo")
    s = setze(s, AUFRUF_ALT, AUFRUF_NEU, "renderRangtracker-Ende")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    SEITE.write_text(s, encoding="utf-8")
    print("  Öle-Block eingebaut · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
