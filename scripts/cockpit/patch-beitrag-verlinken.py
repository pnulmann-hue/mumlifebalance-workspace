"""Zum Beitrag springen — von überall, und erstmals überhaupt funktionierend.

Patricia am 25.09.2026: *„kannst du die verlinkung machen zu den beiträgen
bitte"* — im Funnel-Reiter, bei den Beiträgen, die ein Stichwort spielen.

**Drei Fehler mussten dafür weg, und zwei davon waren still:**

🚨 **`springeZuBeitrag` stand INNERHALB von `renderUebersicht`.** In „Was wann
rausgeht" ruft `unterBlock` sie auf — eine andere Funktion im selben Modul, die
eine verschachtelte Funktion nie sehen kann. Die Zeile dort lautet
`if (typeof springeZuBeitrag === "function") …`, und genau diese Abfrage war
**immer falsch**. Der Klick auf einen Hook hat seit dem 24.09. nichts getan, und
weil die Prüfung den Fehler abfing, kam nicht einmal eine Meldung in der Konsole.
**Ein `typeof`-Schutz um einen Aufruf macht einen kaputten Aufruf unsichtbar.**

🚨 **Das Datum wurde an der falschen Stelle gelesen.** `blo(b.obj).datum` ist das
alte Blotato-Feld aus dem Karussell-Editor und bei fast allen Beiträgen leer; das
echte Datum steht in `b.obj.datum`, dort setzt es die Wochenkarte. Gemessen an der
Testfassung: von 16 Zeilen auf der Übersicht trugen **6** ein Datum, die anderen
zehn standen ohne — und der Sprung landete in der falschen Woche, weil
`wochenAbstand("")` null ergibt. Dieselbe Stelle sortiert auch die Übersicht.

**Was der Patch macht:**

| | |
|---|---|
| `datumVon(b)` | ein Ort für „wann geht der Beitrag raus" — `obj.datum`, dann Blotato |
| `wochenAbstand` · `springeZuBeitrag` | aus `renderUebersicht` heraus in den Modul-Scope |
| `beitragNach(id)` | Beitrag über seine Kennung finden — die Brücke für jeden Link |
| Funnel-Reiter | geplante Beiträge sind anklickbar und springen in ihre Woche |

🚨 **Keine `typeof`-Prüfung mehr um `springeZuBeitrag`.** Die Funktion steht jetzt
im selben Sichtbereich; eine Abfrage würde nur den nächsten Umbau wieder verdecken.

    python scripts/cockpit/patch-beitrag-verlinken.py [--pruefen] [--datei <pfad>]
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

# ---------------------------------------------- 1 · die drei Helfer nach oben

ANKER = "  /* Was in den Arbeitsansichten auftaucht. Abgelehntes nie. */"

HELFER = '''  /* Wann geht dieser Beitrag raus?
     🚨 EINE Stelle dafuer. Vorher stand an vier Stellen `blo(b.obj).datum` —
     das ist das alte Blotato-Feld aus dem Karussell-Editor und bei fast allen
     Beitraegen leer. Das echte Datum setzt die Wochenkarte in `obj.datum`.
     Folge: von 16 Zeilen auf der Uebersicht trugen 6 ein Datum. */
  function datumVon(b) {
    var o = (b && b.obj) || b || {};
    return o.datum || ((o.blotato || {}).datum) || "";
  }

  /* Einen Beitrag ueber seine Kennung finden — die Bruecke fuer jede
     Verlinkung, egal aus welchem Reiter. */
  function beitragNach(id) {
    if (!id) return null;
    var alle = alleBeitraege();
    for (var i = 0; i < alle.length; i++) {
      if (alle[i].id === id) return alle[i];
    }
    return null;
  }

  /* Wie viele Wochen liegt ein Datum von der laufenden Woche entfernt?
     Ueber den Montag beider Wochen gerechnet — die Tages-Differenz durch
     sieben springt daneben. */
  function wochenAbstand(iso) {
    function montag(d) {
      var x = new Date(d + "T00:00:00");
      if (isNaN(x)) return null;
      x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
      x.setHours(0, 0, 0, 0);
      return x;
    }
    var a = montag(todayISO()), b = montag(iso);
    if (!a || !b) return null;
    return Math.round((b - a) / 604800000);
  }

  /* 🚨 Stand bis 25.09.2026 INNERHALB von renderUebersicht und war damit fuer
     `unterBlock` unsichtbar — der Klick auf einen Hook in „Was wann rausgeht"
     hat nie etwas getan. Gefangen hat das eine `typeof`-Abfrage, und genau
     deshalb ist es niemandem aufgefallen. */
  function springeZuBeitrag(b) {
    if (!b) { toast("Diesen Beitrag gibt es im Cockpit nicht mehr."); return; }
    var d = datumVon(b);
    activeTab = "woche";
    var ab = d ? wochenAbstand(d) : null;
    if (ab !== null) {
      wochenOffset = ab;
      // Ohne Datum kein aufgeklappter Platz — sonst oeffnet sich ein
      // beliebiger und man haelt den falschen Beitrag fuer den gesuchten.
      slotOffen = d + "|" + kartenProfil(b.obj);
    } else {
      // Liegt ohne Datum im Vorrat: die laufende Woche zeigen und sagen,
      // wo er steht. Eine stumme Ansicht sieht aus wie ein toter Klick.
      wochenOffset = 0;
      slotOffen = null;
      toast("„" + (b.titel || "Der Beitrag") + "“ hat noch kein Datum — " +
            "er steht unten in der Ideenliste.");
    }
    render();
  }

'''

# -------------------------------------------- 2 · die verschachtelten weg

ALT_NESTED = '''    /* Wie viele Wochen liegt ein Datum von der laufenden Woche entfernt?
       Ueber den Montag beider Wochen gerechnet - siehe Kopf des
       Patch-Skripts, die Tages-Differenz durch sieben springt daneben. */
    function wochenAbstand(iso) {
      function montag(d) {
        var x = new Date(d + "T00:00:00");
        if (isNaN(x)) return null;
        x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
        x.setHours(0, 0, 0, 0);
        return x;
      }
      var a = montag(todayISO()), b = montag(iso);
      if (!a || !b) return null;
      return Math.round((b - a) / 604800000);
    }

    function springeZuBeitrag(b) {
      var d = (blo(b.obj) || {}).datum || "";
      activeTab = "woche";
      var ab = d ? wochenAbstand(d) : null;
      if (ab !== null) {
        wochenOffset = ab;
        // Ohne Datum kein aufgeklappter Platz - sonst oeffnet sich ein
        // beliebiger und man haelt den falschen Beitrag fuer den gesuchten.
        slotOffen = d + "|" + (typeof kartenProfil === "function"
          ? kartenProfil(b.obj) : "mentoring");
      }
      render();
    }

'''

# ------------------------------------------- 3 · die Datumsstellen richten

DATUM = [
    ('        var e = { b: b, was: f.was, dazu: f.dazu, datum: (blo(b.obj) || {}).datum || "" };',
     '        var e = { b: b, was: f.was, dazu: f.dazu, datum: datumVon(b) };'),
    ('      return ((blo(a.obj) || {}).datum || "9999") < ((blo(c.obj) || {}).datum || "9999") ? -1 : 1;',
     '      return (datumVon(a) || "9999") < (datumVon(c) || "9999") ? -1 : 1;'),
    ('      return { wann: fmtDate((blo(b.obj) || {}).datum), text: b.titel || b.format,',
     '      return { wann: fmtDate(datumVon(b)), text: b.titel || b.format,'),
]

# ---------------------------------- 4 · die tote typeof-Abfrage entfernen

ALT_TYPEOF = '''        z.querySelector(".uehook").onclick = function () {
          if (typeof springeZuBeitrag === "function") springeZuBeitrag(b);
        };'''
NEU_TYPEOF = '''        // 🚨 Ohne typeof-Abfrage. Die hat bis 25.09.2026 verdeckt, dass die
        // Funktion hier gar nicht sichtbar war — der Klick tat nichts, und
        // niemand bekam es mit.
        z.querySelector(".uehook").onclick = function () { springeZuBeitrag(b); };'''

# ------------------------------------ 5 · Funnel: geplante Posts verlinken

ALT_GPL = '''      if (gpl.length) {
        block("Geplant (" + gpl.length + ")",
          gpl.map(function (p) {
            return '<div class="fnpost"><span class="fnpdat">' +
              (p.datum ? esc(fmtDate(p.datum)) : "ohne Datum") + '</span>' +
              '<span class="fnptext">' + esc(p.name || p.id) + '</span>' +
              '<span class="fnpreach">' + esc(p.art || "") + '</span></div>';
          }).join(""));
      }'''
NEU_GPL = '''      if (gpl.length) {
        /* Anklickbar: springt in die Woche des Beitrags und klappt den Platz
           auf. Nicht als Link gebaut, weil das Ziel ein Reiter ist und keine
           Adresse. */
        block("Geplant (" + gpl.length + ")",
          gpl.map(function (p) {
            return '<div class="fnpost fnklick" data-bid="' + esc(p.id) + '" ' +
              'title="Beitrag in der Wochen-Vorschau öffnen">' +
              '<span class="fnpdat">' +
              (p.datum ? esc(fmtDate(p.datum)) : "ohne Datum") + '</span>' +
              '<span class="fnptext">' + esc(p.name || p.id) + '</span>' +
              '<span class="fnpreach">' + esc(p.art || "") + '</span></div>';
          }).join(""));
      }'''

ALT_ENDE = '''      box.appendChild(k);
    });
  }

  function funnelStand() {'''
NEU_ENDE = '''      /* Erst anhaengen, dann verdrahten — vorher gibt es die Knoten nicht. */
      [].forEach.call(k.querySelectorAll(".fnklick"), function (z) {
        z.onclick = function () {
          springeZuBeitrag(beitragNach(z.getAttribute("data-bid")));
        };
      });
      box.appendChild(k);
    });
  }

  function funnelStand() {'''

CSS_ALT = "  .fnpost:first-child { border-top: 0; }"
CSS_NEU = '''  .fnpost:first-child { border-top: 0; }
  .fnpost.fnklick { cursor: pointer; }
  .fnpost.fnklick:hover { background: var(--surface-2); }
  .fnpost.fnklick .fnptext { color: var(--teal); }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet 1x. Nichts geändert." % (name, n))
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
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "function datumVon(" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER, HELFER + ANKER, "Helfer einsetzen")
    s = setze(s, ALT_NESTED, "", "verschachtelte Fassung entfernen")
    for i, (a, n) in enumerate(DATUM):
        s = setze(s, a, n, "Datum %d" % (i + 1))
    s = setze(s, ALT_TYPEOF, NEU_TYPEOF, "typeof-Abfrage")
    s = setze(s, ALT_GPL, NEU_GPL, "Funnel geplant")
    s = setze(s, ALT_ENDE, NEU_ENDE, "Funnel verdrahten")
    s = setze(s, CSS_ALT, CSS_NEU, "CSS")

    # Gegenprobe: es darf keine zweite Definition mehr geben.
    if s.count("function springeZuBeitrag(") != 1:
        sys.exit("🚨 springeZuBeitrag kommt %dx vor — erwartet genau 1x."
                 % s.count("function springeZuBeitrag("))
    if "(blo(b.obj) || {}).datum" in s or "(blo(a.obj) || {}).datum" in s:
        sys.exit("🚨 Es steht noch ein blo()-Datum drin.")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if "--pruefen" in sys.argv:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Verlinkung eingebaut · %d KB" % (len(s) / 1024))
    print("  springeZuBeitrag ist jetzt erreichbar · Datum aus obj.datum · "
          "geplante Beiträge im Funnel klickbar.")


if __name__ == "__main__":
    main()
