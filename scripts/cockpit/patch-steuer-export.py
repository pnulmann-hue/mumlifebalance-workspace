"""Haengt den Steuer-Block unten in «Zahlen & Ziele» ein.

Patricia am 24.09.2026: *„wäre da richtig geil, wenn wir ende jahr eine option
hätten, dass ich per knopfdruck die daten rauslassen kann für meine
steuererklärung"*.

Der Block zeigt je Jahr Einnahmen, Kosten und **wie viele Posten keinen Beleg
haben** — und gibt auf Knopfdruck die Ausgaben als CSV ab.

🚨 **Der Knopf liefert die Zahlen, nicht die Belegdateien.** Ein Artifact kommt
nicht an den Dateiordner; die PDFs liegen in `context/finanzen/2026/belege/`.
Die CSV nennt je Zeile den Dateinamen, und unter dem Knopf steht der Befehl
fuer das vollstaendige Paket. Ein Knopf, der „Steuer-Export" heisst und die
Haelfte weglaesst, ohne es zu sagen, ist schlimmer als keiner.

🚨 **Kein Gewinn, wo ein Beleg fehlt.** Dieselbe Regel wie im Monatsbogen.
Statt einer Zahl steht dort der Grund.

🚨 **CSV mit Semikolon und BOM.** Excel auf Deutsch legt sonst alles in eine
Spalte, und dann tippt sie es ab.

🚨 **Im eingebetteten JS stehen echte Umlaute, keine \\u-Escapes.** Der Rest der
Seite macht es genauso, und jede Escape-Schreibweise in einem Python-Skript,
das durch eine Shell laeuft, kostet eine Runde Fehlersuche.

    python scripts/cockpit/patch-steuer-export.py [--pruefen]
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

# ---------------------------------------------------------------- Bausteine

VAR_ALT = '  var monatsbogen = null;        // daten/monatsbogen — Abgleich'
VAR_NEU = ('  var monatsbogen = null;        // daten/monatsbogen — Abgleich\n'
           '  var steuer = null;             // daten/steuer — Abgleich')

LS_ALT = '  monatsbogen = lsGet("monatsbogen", null);'
LS_NEU = ('  monatsbogen = lsGet("monatsbogen", null);\n'
          '  steuer = lsGet("steuer", null);')

SNAP_ALT = '''      db.doc("daten/monatsbogen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        monatsbogen = snap.data() || null;
        lsSet("monatsbogen", monatsbogen);
        if (activeTab === "monatsbogen") render();
      }, function () {});'''
SNAP_NEU = SNAP_ALT + '''
      db.doc("daten/steuer").onSnapshot(function (snap) {
        if (!snap.exists) return;
        steuer = snap.data() || null;
        lsSet("steuer", steuer);
        if (activeTab === "zahlen") render();
      }, function () {});'''

AUFRUF_ALT = '''    main.querySelector("#addmonat").onclick = function () {
      state.zahlen.push({ id: uid("z"), monat: jetzt, umsatz: "", verkaeufe: "", liste: "", notiz: "" });
      saveList("zahlen"); render();
    };
  }'''

AUFRUF_NEU = r'''    main.querySelector("#addmonat").onclick = function () {
      state.zahlen.push({ id: uid("z"), monat: jetzt, umsatz: "", verkaeufe: "", liste: "", notiz: "" });
      saveList("zahlen"); render();
    };

    steuerBlock(main);
  }

  /* =========================================================
     Steuer-Unterlage — je Jahr eine Bilanz, auf Knopfdruck als CSV.

     ACHTUNG: Der Knopf gibt die ZAHLEN heraus, nicht die Belegdateien. Die
     liegen im Workspace; ein Artifact kommt nicht an den Dateiordner. Die
     CSV nennt je Zeile den Dateinamen, und unter dem Knopf steht der Befehl
     fuer das vollstaendige Paket.
     ========================================================= */
  function csvFeld(x) {
    x = (x === null || x === undefined) ? "" : String(x);
    return /[";\n]/.test(x) ? '"' + x.replace(/"/g, '""') + '"' : x;
  }

  function csvDatei(kopf, zeilen) {
    var text = [kopf].concat(zeilen).map(function (r) {
      return r.map(csvFeld).join(";");
    }).join("\r\n");
    // BOM, sonst zerlegt Excel auf Deutsch die Umlaute.
    return new Blob(["﻿" + text], { type: "text/csv;charset=utf-8" });
  }

  function steuerAbgeben(jahr) {
    if (!downloads) { toast("Herunterladen ist hier nicht verfügbar."); return; }
    var zeilen = ((steuer && steuer.zeilen) || []).filter(function (z) {
      return z.jahr === jahr;
    });
    if (!zeilen.length) { toast("Für " + jahr + " sind keine Ausgaben erfasst."); return; }

    var aus = csvDatei(
      ["Datum", "Was", "Kategorie", "Betrag", "Waehrung", "Beleg", "Quelle"],
      zeilen.map(function (z) {
        return [z.datum, z.was, z.art, Number(z.betrag).toFixed(2), z.waehrung,
                z.beleg || "FEHLT", z.quelle];
      }));

    downloads.save({ filename: "ausgaben-" + jahr + ".csv", data: aus })
      .then(function () {
        toast("Ausgaben " + jahr + " abgelegt · " + zeilen.length + " Zeilen");
      })
      .catch(function () { toast("Abgabe abgebrochen."); });
  }

  function steuerBlock(main) {
    var jahre = (steuer && steuer.jahre) || [];
    var h = '<h2 style="margin-top:34px">Für die Steuererklärung</h2>';

    if (!jahre.length) {
      main.insertAdjacentHTML("beforeend", h +
        '<div class="card"><p class="muted">Noch nichts gerechnet. Erst bauen:<br>' +
        '<code>python scripts/cockpit/umsatz-bauen.py</code><br>' +
        '<code>python scripts/finanzen/meta-werbekosten.py</code><br>' +
        '<code>python scripts/cockpit/kosten-bauen.py</code><br>' +
        '<code>python scripts/cockpit/steuer-fuer-cockpit.py</code></p></div>');
      return;
    }

    var reihen = jahre.map(function (e) {
      var gew = (e.gewinn === null || e.gewinn === undefined)
        ? '<span class="mbleer">' + esc(e.gewinn_warum_nicht || "noch offen") + '</span>'
        : "<b>" + e.gewinn.toLocaleString("de-CH", { maximumFractionDigits: 0 }) + "</b>";
      var beleglage = e.posten
        ? (e.ohne_beleg
            ? '<span class="warn">' + e.ohne_beleg + " von " + e.posten + " ohne Beleg</span>"
            : '<span class="ok">alle ' + e.posten + " belegt</span>")
        : '<span class="warn">keine Kosten erfasst</span>';
      return "<tr>" +
        "<td><b>" + esc(e.jahr) + "</b></td>" +
        '<td style="text-align:right">' +
          e.einnahmen.toLocaleString("de-CH", { maximumFractionDigits: 0 }) + "</td>" +
        '<td style="text-align:right">' +
          e.kosten_chf.toLocaleString("de-CH", { maximumFractionDigits: 0 }) + "</td>" +
        '<td style="text-align:right">' + (e.kosten_usd
          ? '<span class="mbleer">USD ' +
            e.kosten_usd.toLocaleString("de-CH", { maximumFractionDigits: 0 }) + "</span>"
          : "—") + "</td>" +
        '<td style="text-align:right">' + gew + "</td>" +
        "<td>" + beleglage + "</td>" +
        '<td><button class="btn" data-steuerjahr="' + esc(e.jahr) +
          '">Ausgaben als CSV</button></td></tr>';
    }).join("");

    main.insertAdjacentHTML("beforeend", h +
      '<div class="card"><table class="tbl"><thead><tr>' +
      '<th>Jahr</th><th style="text-align:right">Einnahmen</th>' +
      '<th style="text-align:right">Kosten CHF</th>' +
      '<th style="text-align:right">offen in USD</th>' +
      '<th style="text-align:right">Gewinn</th><th>Belege</th><th></th>' +
      "</tr></thead><tbody>" + reihen + "</tbody></table>" +
      '<p class="muted" style="margin-top:14px">' +
      "Der Knopf gibt die <b>Zahlen</b> ab — die Belegdateien liegen im " +
      "Workspace unter <code>" + esc((steuer && steuer.belegordner) || "") +
      "</code> und kommen über das vollständige Paket dazu:<br>" +
      "<code>" + esc((steuer && steuer.vollexport) || "") + "</code><br>" +
      "Das legt Übersicht, beide CSV, die Lückenliste und Kopien aller " +
      "Belege in einen Ordner.</p>" +
      '<p class="muted">Ein Gewinn wird erst ausgewiesen, wenn jeder Posten ' +
      "einen Beleg hat und keine USD-Beträge mehr offen stehen. Einnahmen " +
      "minus unvollständige Kosten wäre eine Zahl, die zu hoch ist und nach " +
      "einer gerechneten aussieht.</p></div>");

    Array.prototype.forEach.call(
      main.querySelectorAll("[data-steuerjahr]"), function (b) {
        b.onclick = function () { steuerAbgeben(b.getAttribute("data-steuerjahr")); };
      });
  }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    """Das eingebettete Skript durch node --check jagen.

    🚨 Ein deutsches Anfuehrungszeichen in einer JS-Zeichenkette hat schon
    einmal die ganze Seite totgelegt. Deshalb vor jedem Publish hier durch.
    """
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

    if "steuerBlock(main)" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, VAR_ALT, VAR_NEU, "Variable")
    s = setze(s, LS_ALT, LS_NEU, "localStorage-Laden")
    s = setze(s, SNAP_ALT, SNAP_NEU, "Datenbank-Abo")
    s = setze(s, AUFRUF_ALT, AUFRUF_NEU, "renderZahlen-Ende")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)

    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    SEITE.write_text(s, encoding="utf-8")
    print("  Steuer-Block eingebaut · %d KB" % (len(s) / 1024))
    print("  Geprüft mit node --check.")


if __name__ == "__main__":
    main()
