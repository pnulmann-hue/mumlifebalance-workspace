"""
Einen eigenen doTERRA-Bereich ins Cockpit bauen.

Getrennt vom Mentoring, weil es zwei Profile mit zwei Logiken sind. Der
Bereich ist als Rang-Tracker aufgebaut: oben, wo Patricia steht, darunter
die drei Qualifikations-Beine mit genau der Zahl, die noch fehlt — und in
jedem Bein die Leute, die etwas bewegen.

Die Zahlen kommen aus `scripts/cockpit/doterra-tracker-bauen.py`, das den
Schlagdistanz-Bericht aus dem Back Office liest.

Aufruf:
  python scripts/cockpit/patch-doterra.py [--pruefen]
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


patch("Speicher fuer die doTERRA-Zahlen",
      '  var mailings = { listen: [], automationen: [], stand: "" };',
      '  var mailings = { listen: [], automationen: [], stand: "" };\n'
      '  /* Rang-Tracker: kommt aus dem Schlagdistanz-Bericht im Back Office. */\n'
      '  var doterra = null;')

patch("doTERRA in die Navigation",
      '    { id: "zahlen", label: "Zahlen & Ziele" },',
      '    { id: "zahlen", label: "Zahlen & Ziele" },\n'
      '    { g: "doTERRA" },\n'
      '    { id: "rangtracker", label: "Rang-Tracker" },')

patch("doTERRA an den Render-Dispatcher",
      '    else if (activeTab === "suche") renderSuche(main);',
      '    else if (activeTab === "suche") renderSuche(main);\n'
      '    else if (activeTab === "rangtracker") renderRangtracker(main);')

patch("Die Rang-Tracker-Ansicht",
      """  /* =========================================================
     Launches
     ========================================================= */""",
      """  /* =========================================================
     doTERRA Rang-Tracker — was fehlt wo, Bein für Bein
     ========================================================= */
  /* „202609" ist eine Datenbank-Schreibweise, keine, die man liest. */
  function monatKlar(m) {
    m = String(m || "");
    return /^\d{6}$/.test(m) ? m.slice(4) + "/" + m.slice(0, 4) : m;
  }

  function zahlKurz(n) {
    return (Math.round(n * 10) / 10).toLocaleString("de-CH",
      { minimumFractionDigits: 0, maximumFractionDigits: 1 });
  }

  function balken(ist, soll) {
    var teil = soll ? Math.min(100, (ist / soll) * 100) : 0;
    var ton = teil >= 100 ? "voll" : (teil >= 75 ? "nah" : "weit");
    return '<div class="dtbalken"><span class="' + ton + '" style="width:' +
           teil.toFixed(1) + '%"></span></div>';
  }

  function luecken(liste) {
    if (!liste || !liste.length) return '<span class="flag ok">erfüllt</span>';
    return liste.map(function (l) {
      return '<span class="flag bad">' + zahlKurz(l.fehlt) + ' ' + esc(l.was) +
             ' fehlen</span>';
    }).join(" ");
  }

  function renderRangtracker(main) {
    if (!doterra) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Rang-Tracker</h1>' +
        '<p>Dein Weg zu Gold, Bein für Bein.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch keine Zahlen da. Sie kommen aus ' +
        'dem Schlagdistanz-Bericht im doTERRA Back Office.</div></div>';
      return;
    }

    var ich = doterra.ich;
    var eliteBeine = doterra.beine.filter(function (b) { return b.ov >= 3000; }).length;
    var premierBeine = doterra.beine.filter(function (b) { return b.rang === "Premier"; }).length;
    var fehltSilver = doterra.beine.reduce(function (s, b) {
      return s + Math.max(0, 3000 - b.ov);
    }, 0);

    main.innerHTML =
      '<div class="page-head"><div><h1>Rang-Tracker</h1>' +
      '<p>Dein Weg zu Gold, Bein für Bein. Gold heisst: drei Beine auf Premier. ' +
      'Der ehrliche nächste Schritt davor ist Silver — drei Beine auf Elite.</p></div></div>' +
      '<div class="tiles">' +
      tile("Dein Rang", esc(ich.rang), "bezahlt im Monat " + esc(monatKlar(doterra.monat))) +
      tile("Dein OV", zahlKurz(ich.ov), "dein PV: " + zahlKurz(ich.pv)) +
      tile("Elite-Beine", eliteBeine + " von 3", "für Silver") +
      tile("Premier-Beine", premierBeine + " von 3", "für Gold") +
      '</div>' +
      '<div class="panel dtleiter"><h2>Die Leiter</h2>' +
      '<p class="note">Executive 2.000 OV · Elite 3.000 OV · Premier 5.000 OV + 2 Executive-Beine · ' +
      'Silver 3 Elite-Beine · Gold 3 Premier-Beine. Überall 100 PV im Monat.</p>' +
      '<p class="dtsumme">Bis Silver fehlen über alle drei Beine zusammen <strong>' +
      zahlKurz(fehltSilver) + ' OV</strong>.</p></div>' +
      '<div id="dtbeine"></div>';

    var box = main.querySelector("#dtbeine");
    doterra.beine.forEach(function (b, i) {
      var karte = document.createElement("div");
      karte.className = "panel dtbein";
      var h =
        '<div class="dtkopf"><span class="dtnr">Bein ' + (i + 1) + '</span>' +
        '<span class="dtname">' + esc(b.name) + '</span>' +
        '<span class="dstufe">' + esc(b.rang) + '</span></div>' +
        '<div class="dtzeile"><span>OV</span>' + balken(b.ov, 3000) +
        '<span class="dtzahl">' + zahlKurz(b.ov) + ' / 3.000</span></div>' +
        '<div class="dtziele">' +
        '<div><strong>zu Elite</strong> ' + luecken(b.zu_elite) + '</div>' +
        '<div><strong>zu Premier</strong> ' + luecken(b.zu_premier) + '</div>' +
        '</div>';

      if (b.leute && b.leute.length) {
        h += '<h3 class="dtunter">Wer in diesem Bein etwas bewegt</h3>' +
             '<div class="tablewrap"><div class="trow head" ' +
             'style="grid-template-columns:minmax(190px,1fr) 120px 92px 92px 130px">' +
             '<span>Name</span><span>Rang</span><span>PV</span><span>OV</span>' +
             '<span>bis Executive</span></div>';
        b.leute.forEach(function (p) {
          var fehlt = (p.zu_executive || []).filter(function (x) { return x.was === "OV"; })[0];
          h += '<div class="trow" style="grid-template-columns:minmax(190px,1fr) 120px 92px 92px 130px">' +
               '<span>' + esc(p.name) + '</span>' +
               '<span class="note">' + esc(p.rang) + '</span>' +
               '<span>' + zahlKurz(p.pv) + '</span>' +
               '<span>' + zahlKurz(p.ov) + '</span>' +
               '<span class="note">' + (fehlt ? zahlKurz(fehlt.fehlt) + " OV" : "erreicht") +
               '</span></div>';
        });
        h += '</div>';
        if (b.weitere) {
          h += '<p class="note">und ' + b.weitere + ' weitere ohne Volumen in diesem Monat</p>';
        }
      } else {
        h += '<p class="note">In diesem Bein hat diesen Monat noch niemand bestellt.</p>';
      }
      karte.innerHTML = h;
      box.appendChild(karte);
    });

    var fuss = document.createElement("p");
    fuss.className = "note";
    fuss.style.marginTop = "14px";
    fuss.textContent = "Stand " + mailDatum(doterra.stand) +
      " · Zahlen aus dem Schlagdistanz-Bericht, Zeitraum " + monatKlar(doterra.monat) +
      ". Der Monat läuft noch, die Zahlen wachsen bis zum Monatsende.";
    main.appendChild(fuss);
  }

  /* =========================================================
     Launches
     ========================================================= */""")

patch("Stil fuer den Rang-Tracker",
      "  /* ---------- Suche ---------- */",
      """  /* ---------- doTERRA Rang-Tracker ---------- */
  .dtleiter { margin-bottom: 18px; }
  .dtsumme { margin: 10px 0 0; font-size: 14px; }
  .dtbein { margin-bottom: 16px; }
  .dtkopf { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
  .dtnr {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--teal); background: var(--teal-soft);
    padding: 3px 9px; border-radius: 999px;
  }
  .dtname { font-family: var(--display); font-size: 18px; }
  .dtzeile { display: grid; grid-template-columns: 32px 1fr 128px; gap: 10px; align-items: center; }
  .dtzeile > span:first-child { font-size: 11px; letter-spacing: 0.08em; color: var(--ink-soft); }
  .dtzahl { font-size: 13px; font-variant-numeric: tabular-nums; text-align: right; }
  .dtbalken { height: 9px; background: var(--surface-2); border-radius: 999px; overflow: hidden; }
  .dtbalken span { display: block; height: 100%; border-radius: 999px; }
  .dtbalken .voll { background: var(--good); }
  .dtbalken .nah { background: var(--orange); }
  .dtbalken .weit { background: var(--navy); }
  .dtziele { display: flex; flex-wrap: wrap; gap: 18px; margin-top: 12px; font-size: 13px; }
  .dtziele strong { font-weight: 600; margin-right: 6px; }
  .dtunter { font-size: 12px; letter-spacing: 0.07em; text-transform: uppercase;
             color: var(--ink-soft); font-weight: normal; margin: 18px 0 8px; }

  /* ---------- Suche ---------- */""")

patch("doTERRA-Zahlen aus der Datenbank holen",
      """      db.doc("daten/mailings").onSnapshot(function (snap) {""",
      """      db.doc("daten/doterra").onSnapshot(function (snap) {
        if (!snap.exists) return;
        doterra = snap.data() || null;
        lsSet("doterra", doterra);
        if (activeTab === "rangtracker") render();
      }, function () {});
      db.doc("daten/mailings").onSnapshot(function (snap) {""")

patch("doTERRA beim Start laden",
      '  produktdetails = lsGet("produkt-details", {}) || {};',
      '  produktdetails = lsGet("produkt-details", {}) || {};\n'
      '  doterra = lsGet("doterra", null);')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:160]))
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
