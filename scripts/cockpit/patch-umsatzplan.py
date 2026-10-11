"""
Schritt 3: der Rechner fuer das Monatsziel.

Die Frage, um die es geht: **was muesste im Monat laufen, damit 4'000
zusammenkommen?** Bisher stand im Cockpit nur, was war — die Tabelle unter
„Zahlen & Ziele". Was fehlt, ist die Richtung nach vorne.

Der Rechner nennt bewusst **zwei Zahlen statt einer**:

  vorsichtig       nur das Angebot selbst wird gekauft
  mit ganzer Kette jede Kundin nimmt Bump und Upsell mit

Warum nicht eine einzige Zahl mit einer Annahme dazwischen: eine Bump-Quote von
dreissig Prozent waere geraten. Patricia hat noch keine eigene Statistik dazu,
und eine geratene Zahl sieht in einer Tabelle genauso echt aus wie eine
gemessene. Die Spanne ist ehrlich und trotzdem brauchbar — die Wahrheit liegt
dazwischen, und sobald ThriveCart-Transaktionen angebunden sind, kann daraus ein
echter Wert werden.

Abgelegt in `daten/umsatzplan`. 🚨 Gehoert Patricia, der Abgleich schreibt es nie.

Aufruf:
  python scripts/cockpit/patch-umsatzplan.py [--pruefen]
"""
import io
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ERSETZUNGEN = []


def patch(name, alt, neu):
    ERSETZUNGEN.append((name, alt, neu))


# --------------------------------------------------------------------------
# 1) Speicher
# --------------------------------------------------------------------------
patch("Speicher fuer den Umsatzplan",
      '  var ketten = {};\n  var offeneKette = null;',
      '  var ketten = {};\n'
      '  var offeneKette = null;\n'
      '  /* Der Weg zum Monatsziel: welches Angebot wie oft. Gehoert Patricia. */\n'
      '  var umsatzplan = { zeilen: [], weitere: 0 };')


# --------------------------------------------------------------------------
# 2) Rechnen und Zeichnen, direkt vor renderZahlen
# --------------------------------------------------------------------------
patch("Der Umsatzplan",
      """  function renderZahlen(main) {""",
      """  function planSpeichern() {
    clearTimeout(saveTimers.umsatzplan);
    saveTimers.umsatzplan = setTimeout(function () {
      lsSet("umsatzplan", umsatzplan);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/umsatzplan")
        .set({ zeilen: umsatzplan.zeilen, weitere: umsatzplan.weitere,
               updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function planRechnen() {
    var vorsichtig = 0, voll = 0;
    (umsatzplan.zeilen || []).forEach(function (z) {
      var a = angebotNach(z.angebot);
      if (!a) return;
      var n = Number(z.anzahl) || 0;
      var w = warenkorb(a);
      vorsichtig += n * (w.grund || 0);
      voll += n * (w.max || 0);
    });
    var extra = Number(umsatzplan.weitere) || 0;
    return { vorsichtig: vorsichtig + extra, voll: voll + extra, extra: extra };
  }

  /* Die Angebotsliste nach Schubladen, damit man nicht in neunundvierzig
     Zeilen am Stueck sucht. */
  function angebotOptionen(sel, gewaehlt) {
    var alle = ((katalog && katalog.angebote) || []).slice()
      .sort(function (x, y) { return (x.name || "") < (y.name || "") ? -1 : 1; });
    var leer = document.createElement("option");
    leer.value = ""; leer.textContent = "\\u2014 Angebot w\\u00e4hlen \\u2014";
    sel.appendChild(leer);
    (((katalog && katalog.kategorien) || [])).forEach(function (kat) {
      var drin = alle.filter(function (x) { return x.kategorie === kat.id; });
      if (!drin.length) return;
      var gruppe = document.createElement("optgroup");
      gruppe.label = kat.name;
      drin.forEach(function (x) {
        var o = document.createElement("option");
        o.value = x.id;
        o.textContent = x.name +
          (x.preis ? "  (" + preisText(x.preis, x.waehrung) + ")" : "");
        if (gewaehlt === x.id) o.selected = true;
        gruppe.appendChild(o);
      });
      sel.appendChild(gruppe);
    });
  }

  function renderPlan(box) {
    if (!katalog) {
      box.innerHTML = '<h2>Weg zum Monatsziel</h2>' +
        '<div class="empty">Daf\\u00fcr braucht es den Angebots-Katalog. ' +
        'Der entsteht aus ThriveCart.</div>';
      return;
    }
    var ziel = Number(settings.monatsziel) || 0;
    var waehrung = settings.waehrung || "CHF";

    box.innerHTML = '<h2>Weg zum Monatsziel</h2>' +
      '<p class="note">Trag ein, wie oft du ein Angebot im Monat verkaufen willst. ' +
      'Links steht, was es bringt, wenn <strong>nur das Angebot selbst</strong> ' +
      'gekauft wird. Rechts, was es bringt, wenn <strong>jede Kundin die ganze ' +
      'Kette mitnimmt</strong>. Die Wahrheit liegt dazwischen \\u2014 wo genau, ' +
      'sagt dir erst deine eigene Statistik. Die Ketten baust du im ' +
      'Angebots-Katalog.</p>' +
      '<div class="plankopf">' +
      '<span>Angebot</span><span>Verk\\u00e4ufe im Monat</span>' +
      '<span>nur das Angebot</span><span>mit ganzer Kette</span><span></span>' +
      '</div><div id="planrows"></div>' +
      '<div class="planextra">' +
      '<label for="planweit">Dazu kommt im Monat, ohne Checkout ' +
      '(zum Beispiel doTERRA)</label>' +
      '<input id="planweit" type="number" min="0" step="1" value="' +
      esc(umsatzplan.weitere || "") + '"></div>' +
      '<div id="plansumme"></div>';

    var rows = box.querySelector("#planrows");

    (umsatzplan.zeilen || []).forEach(function (z, i) {
      var a = angebotNach(z.angebot);
      var w = a ? warenkorb(a) : { grund: 0, max: 0 };

      var zeile = document.createElement("div");
      zeile.className = "planzeile";

      var sel = document.createElement("select");
      angebotOptionen(sel, z.angebot);
      sel.onchange = function () {
        z.angebot = sel.value;
        planSpeichern();
        render();
      };
      zeile.appendChild(sel);

      var anz = document.createElement("input");
      anz.type = "number"; anz.min = "0"; anz.step = "1";
      anz.placeholder = "0";
      anz.value = z.anzahl === null || z.anzahl === undefined ? "" : z.anzahl;
      zeile.appendChild(anz);

      var min = document.createElement("span");
      min.className = "katpreis";
      zeile.appendChild(min);

      var max = document.createElement("span");
      max.className = "katpreis";
      zeile.appendChild(max);

      // Beim Tippen wird nicht neu gezeichnet, sonst springt der Fokus weg.
      // Also muessen die beiden Geldspalten von Hand nachgezogen werden.
      function zeileNeu() {
        var k = Number(z.anzahl) || 0;
        min.textContent = preisText(k * (w.grund || 0), waehrung);
        max.textContent = preisText(k * (w.max || 0), waehrung);
      }
      zeileNeu();
      anz.oninput = function () {
        z.anzahl = anz.value === "" ? null : Number(anz.value);
        zeileNeu();
        planSpeichern();
        planNeu(box);
      };

      var weg = document.createElement("button");
      weg.className = "del";
      weg.textContent = "\\u00d7";
      weg.title = "Zeile entfernen";
      weg.onclick = function () {
        umsatzplan.zeilen.splice(i, 1);
        planSpeichern();
        render();
      };
      zeile.appendChild(weg);
      rows.appendChild(zeile);
    });

    if (!(umsatzplan.zeilen || []).length) {
      var e = document.createElement("div");
      e.className = "empty";
      e.textContent = "Noch nichts geplant. Fang mit dem Angebot an, das du am " +
        "besten verkaufst.";
      rows.appendChild(e);
    }

    var plus = document.createElement("button");
    plus.className = "btn";
    plus.style.marginTop = "8px";
    plus.textContent = "+ Angebot hinzuf\\u00fcgen";
    plus.onclick = function () {
      if (!umsatzplan.zeilen) umsatzplan.zeilen = [];
      umsatzplan.zeilen.push({ angebot: "", anzahl: null });
      planSpeichern();
      render();
    };
    rows.appendChild(plus);

    var weit = box.querySelector("#planweit");
    weit.oninput = function () {
      umsatzplan.weitere = weit.value === "" ? 0 : Number(weit.value);
      planSpeichern();
      planNeu(box);
    };

    planNeu(box);
  }

  /* Nur die Summen neu zeichnen — wer tippt, will den Fokus behalten. */
  function planNeu(box) {
    var kasten = box.querySelector("#plansumme");
    if (!kasten) return;
    var ziel = Number(settings.monatsziel) || 0;
    var waehrung = settings.waehrung || "CHF";
    var r = planRechnen();

    function balken(lab, wert) {
      var pct = ziel ? Math.min(100, Math.round(wert / ziel * 100)) : 0;
      return '<div class="bar-row"><div class="bar-lab"><span>' + esc(lab) +
        '</span><b>' + esc(preisText(wert, waehrung)) + ' \\u00b7 ' + pct +
        '%</b></div><div class="bar-track"><div class="bar-fill" style="width:' +
        pct + '%"></div></div></div>';
    }

    var satz;
    if (!ziel) {
      satz = "Setz oben rechts dein Monatsziel, dann rechne ich mit.";
    } else if (r.vorsichtig >= ziel) {
      satz = "Das geht auf, auch wenn niemand einen Bump oder Upsell mitnimmt.";
    } else if (r.voll >= ziel) {
      satz = "Das geht auf, wenn die Ketten mitlaufen. Ohne sie fehlen " +
        preisText(ziel - r.vorsichtig, waehrung) + " \\u2014 " +
        "an den Ketten h\\u00e4ngt hier also dein Ziel.";
    } else {
      satz = "So fehlen selbst bei voller Kette noch " +
        preisText(ziel - r.voll, waehrung) + ". Da braucht es mehr Verk\\u00e4ufe " +
        "oder ein Angebot mit gr\\u00f6sserem Warenkorb.";
    }

    kasten.innerHTML = '<div class="bars" style="margin-top:14px">' +
      balken("vorsichtig gerechnet", r.vorsichtig) +
      balken("mit ganzer Kette", r.voll) +
      '</div><p class="note" style="margin-top:10px">' + esc(satz) +
      (r.extra ? " Darin stecken " + esc(preisText(r.extra, waehrung)) +
        " an weiteren Einnahmen." : "") + '</p>';
  }

  function renderZahlen(main) {""")


# --------------------------------------------------------------------------
# 3) Den Plan in die Seite haengen
# --------------------------------------------------------------------------
patch("Plan-Kasten in Zahlen und Ziele",
      """      '<div class="cols" style="align-items:start">' +
        '<div class="panel" style="grid-column:1/-1"><h2>Umsatz pro Monat</h2>' +
          '<div class="goalline" id="chart"></div></div>' +
      '</div>' +""",
      """      '<div class="panel" id="planbox" style="margin-bottom:18px"></div>' +
      '<div class="cols" style="align-items:start">' +
        '<div class="panel" style="grid-column:1/-1"><h2>Umsatz pro Monat</h2>' +
          '<div class="goalline" id="chart"></div></div>' +
      '</div>' +""")

patch("Plan zeichnen",
      """    var zi = main.querySelector("#zielin");
    zi.oninput = function () { settings.monatsziel = Number(zi.value); saveSettings(); };
    zi.onchange = function () { render(); };""",
      """    var zi = main.querySelector("#zielin");
    zi.oninput = function () { settings.monatsziel = Number(zi.value); saveSettings(); };
    zi.onchange = function () { render(); };

    renderPlan(main.querySelector("#planbox"));""")


# --------------------------------------------------------------------------
# 4) Stil
# --------------------------------------------------------------------------
patch("Stil fuer den Umsatzplan",
      """  .katbefund .btn { font-size: 12px; padding: 5px 10px; }""",
      """  .katbefund .btn { font-size: 12px; padding: 5px 10px; }
  .plankopf, .planzeile {
    display: grid; grid-template-columns: 1fr 120px 118px 128px 30px;
    gap: 10px; align-items: center;
  }
  .plankopf {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); padding: 8px 0 6px; border-bottom: 1px solid var(--line);
  }
  .plankopf span:nth-child(3), .plankopf span:nth-child(4) { text-align: right; }
  .planzeile { padding: 6px 0; border-bottom: 1px solid var(--line); }
  .planzeile select, .planzeile input {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 7px; padding: 6px 9px; font-size: 13px; width: 100%;
  }
  .planzeile select:focus, .planzeile input:focus {
    border-color: var(--teal); outline: none;
  }
  .planzeile .del {
    border: 0; background: none; color: var(--ink-soft); cursor: pointer;
    padding: 4px 6px; border-radius: 6px; font-size: 15px; line-height: 1;
  }
  .planzeile .del:hover { background: var(--orange-soft); color: var(--crit); }
  .planextra { margin-top: 14px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  .planextra label { font-size: 12px; color: var(--ink-soft); }
  .planextra input {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 7px; padding: 6px 9px; font-size: 13px; width: 120px;
  }
  @media (max-width: 760px) {
    .plankopf { display: none; }
    .planzeile { grid-template-columns: 1fr 74px 30px; }
    .planzeile .katpreis:last-of-type { grid-column: 2 / 4; text-align: right; }
  }""")


# --------------------------------------------------------------------------
# 5) Laden
# --------------------------------------------------------------------------
patch("Umsatzplan beim Start laden",
      '  ketten = lsGet("ketten", {}) || {};',
      '  ketten = lsGet("ketten", {}) || {};\n'
      '  umsatzplan = lsGet("umsatzplan", { zeilen: [], weitere: 0 }) ||\n'
      '               { zeilen: [], weitere: 0 };')

patch("Umsatzplan aus der Datenbank",
      '      db.doc("daten/ketten").onSnapshot(function (snap) {',
      '      db.doc("daten/umsatzplan").onSnapshot(function (snap) {\n'
      '        if (!snap.exists) return;\n'
      '        var d0 = snap.data() || {};\n'
      '        umsatzplan = { zeilen: d0.zeilen || [], weitere: d0.weitere || 0 };\n'
      '        lsSet("umsatzplan", umsatzplan);\n'
      '        if (activeTab === "zahlen") render();\n'
      '      }, function () {});\n'
      '      db.doc("daten/ketten").onSnapshot(function (snap) {')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:200]))
        if s.count(alt) > 1:
            sys.exit("Anker mehrdeutig (%dx) fuer: %s" % (s.count(alt), name))
        s = s.replace(alt, neu, 1)
        print("  OK  %s" % name)
    print("\nLaenge %d -> %d (%+d)" % (vorher, len(s), len(s) - vorher))
    if nur_pruefen:
        print("PRUEFLAUF — nichts geschrieben.")
        return
    io.open(DATEI, "w", encoding="utf-8").write(s)
    print("Geschrieben: %s" % DATEI)


if __name__ == "__main__":
    main()
