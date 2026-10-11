"""Baut den Reiter „Monatsbogen" — Ersatz fuer die Notion-Monatsplanung.

Die Notion-Vorlage hat sechs Abschnitte. Der zweite, „Analysen & Kennzahlen",
war bei September **und** Oktober 2026 komplett leer — waehrend die Monatsziele
daneben sorgfaeltig ausformuliert dastanden. Nicht aus Nachlaessigkeit: die
Zahlen dafuer lagen in ThriveCart, in der Meta-API und in zwei Tabellen, und
niemand traegt so etwas von Hand zusammen.

**Hier rechnet sich dieser Abschnitt selbst.** Ihre Eingabe bleibt das, was
nur sie wissen kann: was sie daraus mitnimmt.

🚨 **Zwei Dokumente.** `daten/monatsbogen` gehoert dem Abgleich und wird bei
jedem Lauf ersetzt; `daten/monatsbogen-notizen` gehoert Patricia. Der Abgleich
darf es nie schreiben.

🚨 **Der laufende Monat bekommt kein Urteil.** Er wird gezeigt, aber ohne
Vergleich zum Vormonat — eine Reichweite am 3. des Monats gegen einen vollen
Monat zu stellen erzeugt jedes Mal einen falschen Alarm.

Aufruf:
  python scripts/cockpit/patch-monatsbogen.py [--pruefen]
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

ALT_NAV = '    { id: "launches", label: "Jahresplan" },'
NEU_NAV = ('    { id: "launches", label: "Jahresplan" },\n'
           '    { id: "monatsbogen", label: "Monatsbogen" },')

ALT_VAR = '  var jahresplan = null;      // daten/jahresplan — gehoert PATRICIA'
NEU_VAR = """  var jahresplan = null;      // daten/jahresplan — gehoert PATRICIA
  var monatsbogen = null;        // daten/monatsbogen — Abgleich
  var monatsbogenNotizen = {};   // daten/monatsbogen-notizen — gehoert PATRICIA
  var mbOffen = null;            // welcher Monat aufgeklappt ist"""

ALT_LS = '  jahresplan = lsGet("jahresplan", null);'
NEU_LS = ('  jahresplan = lsGet("jahresplan", null);\n'
          '  monatsbogen = lsGet("monatsbogen", null);\n'
          '  monatsbogenNotizen = lsGet("monatsbogen-notizen", {}) || {};')

ALT_SNAP = '''      db.doc("daten/jahresplan").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/monatsbogen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        monatsbogen = snap.data() || null;
        lsSet("monatsbogen", monatsbogen);
        if (activeTab === "monatsbogen") render();
      }, function () {});
      db.doc("daten/monatsbogen-notizen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        monatsbogenNotizen = (snap.data() || {}).werte || {};
        lsSet("monatsbogen-notizen", monatsbogenNotizen);
        if (activeTab === "monatsbogen") render();
      }, function () {});
      db.doc("daten/jahresplan").onSnapshot(function (snap) {'''

ALT_FUNK = "  function renderJahresplan(main) {"
NEU_FUNK = '''  /* =========================================================
     Monatsbogen — der Rueckblick, der sich selbst ausfuellt
     ========================================================= */
  /* Die Felder aus der Notion-Vorlage. Reihenfolge wie dort: erst was war,
     dann was daraus folgt, dann was kommt. */
  var MB_FELDER = [
    { k: "erfolge", l: "Was lief gut", z: 3,
      p: "Woran hast du gemerkt, dass es funktioniert?" },
    { k: "herausforderungen", l: "Was war schwierig", z: 3,
      p: "Was hat dich aufgehalten oder Kraft gekostet?" },
    { k: "learning", l: "Das grösste Learning", z: 2,
      p: "Ein Satz, den du dir fürs nächste Mal merkst." },
    { k: "erkenntnis_zahlen", l: "Was die Zahlen sagen", z: 3,
      p: "Umsatz, Käufe, Reichweite — was liest du daraus?" },
    { k: "erkenntnis_content", l: "Was der Content sagt", z: 3,
      p: "Was kam an, was nicht — und woran lag es?" },
    { k: "ziele", l: "Die drei Ziele für diesen Monat", z: 3,
      p: "1.\\n2.\\n3." },
    { k: "fokus_gratis", l: "🎁 Gratis-Fokus", z: 1, p: "Welches 0€-Angebot?" },
    { k: "fokus_mini", l: "💸 Mini-Fokus", z: 1, p: "Welcher Minikurs?" },
    { k: "fokus_gross", l: "👑 Gross-Fokus", z: 1, p: "Welches grosse Angebot?" },
    { k: "begruendung", l: "Warum dieser Fokus", z: 3,
      p: "Der rote Faden des Monats in ein, zwei Sätzen." }
  ];

  function mbSpeichern() {
    clearTimeout(saveTimers.monatsbogenNotizen);
    saveTimers.monatsbogenNotizen = setTimeout(function () {
      lsSet("monatsbogen-notizen", monatsbogenNotizen);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/monatsbogen-notizen")
        .set({ werte: monatsbogenNotizen, updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function mbName(ym) {
    var MON = ["Januar","Februar","März","April","Mai","Juni","Juli","August",
               "September","Oktober","November","Dezember"];
    var t = String(ym || "").split("-");
    return (MON[Number(t[1]) - 1] || ym) + " " + t[0];
  }

  /* Ein Unterschied wird nur gezeigt, wenn er einer ist. */
  function mbDelta(wert, einheit) {
    if (wert === undefined || wert === null || wert === 0) return "";
    var hoch = wert > 0;
    return '<span class="mbdelta ' + (hoch ? "hoch" : "runter") + '">' +
      (hoch ? "▲ +" : "▼ ") + (einheit === "geld"
        ? Math.abs(wert).toLocaleString("de-CH", { maximumFractionDigits: 0 })
        : Math.abs(wert)) + '</span>';
  }

  function mbKarte(m, waehrung) {
    var n = monatsbogenNotizen[m.monat] || {};
    var auf = mbOffen === m.monat;
    var d = m.vs_vormonat || {};
    var karte = document.createElement("div");
    karte.className = "panel mbkarte" + (auf ? " auf" : "") +
                      (m.laeuft_noch ? " laeuft" : "");

    var kopf = document.createElement("button");
    kopf.className = "mbkopf";
    kopf.innerHTML =
      '<span class="dpfeil">▸</span>' +
      '<span class="mbmonat">' + esc(mbName(m.monat)) + '</span>' +
      (m.laeuft_noch ? '<span class="mblaeuft">läuft noch</span>' : "") +
      '<span class="mbwert"><b>' + esc(waehrung) + " " +
        (m.umsatz || 0).toLocaleString("de-CH", { maximumFractionDigits: 0 }) +
        '</b>' + mbDelta(d.umsatz, "geld") + '</span>' +
      '<span class="mbwert">' + (m.kaeufe || 0) + ' Käufe</span>' +
      '<span class="mbwert">' + (m.beitraege || 0) + ' Beiträge' +
        mbDelta(d.beitraege) + '</span>' +
      '<span class="mbwert">' + (m.reichweite_median || 0) + ' Reichweite' +
        mbDelta(d.reichweite_median) + '</span>';
    kopf.onclick = function () { mbOffen = auf ? null : m.monat; render(); };
    karte.appendChild(kopf);

    if (!auf) return karte;

    var k = document.createElement("div");
    k.className = "mbkoerper";

    // --- Was gerechnet ist. Reine Anzeige.
    var zahlen = document.createElement("div");
    zahlen.className = "mbblock";
    zahlen.innerHTML = '<h3>Was gemessen wurde</h3>' +
      '<div class="gpwerte">' +
        '<div><b>' + esc(waehrung) + " " + (m.umsatz || 0).toLocaleString("de-CH",
          { maximumFractionDigits: 0 }) + '</b><span>Umsatz</span></div>' +
        '<div><b>' + (m.kaeufe || 0) + '</b><span>Käufe</span></div>' +
        '<div><b>' + (m.beitraege || 0) + '</b><span>Beiträge</span></div>' +
        '<div><b>' + (m.reichweite_median || 0) + '</b><span>Reichweite (Median)</span></div>' +
        '<div><b>' + (m.gespeichert || 0) + '</b><span>gespeichert</span></div>' +
        '<div><b>' + (m.geteilt || 0) + '</b><span>geteilt</span></div>' +
        '<div><b>' + (m.kommentare || 0) + '</b><span>Kommentare</span></div>' +
      '</div>' +
      '<p class="note" style="margin-top:6px">Umsatz aus ThriveCart, Content aus ' +
      'der Instagram-API. Nichts davon trägst du ein.</p>';
    k.appendChild(zahlen);

    if (m.bester || m.schwaechster) {
      var b = document.createElement("div");
      b.className = "mbblock";
      var h = '<h3>Was ankam und was nicht</h3>';
      if (m.bester) {
        h += '<p class="mbbest"><span class="mbtag gut">bester</span> ' +
             esc(m.bester.anfang) + ' <b>' + m.bester.reach + '</b>' +
             (m.bester.link ? ' <a href="' + esc(m.bester.link) +
               '" target="_blank" rel="noopener">↗</a>' : "") + '</p>';
      }
      if (m.schwaechster) {
        h += '<p class="mbbest"><span class="mbtag schwach">schwächster</span> ' +
             esc(m.schwaechster.anfang) + ' <b>' + m.schwaechster.reach + '</b>' +
             (m.schwaechster.link ? ' <a href="' + esc(m.schwaechster.link) +
               '" target="_blank" rel="noopener">↗</a>' : "") + '</p>';
      }
      b.innerHTML = h;
      k.appendChild(b);
    }

    if ((m.launches || []).length) {
      var l = document.createElement("div");
      l.className = "mbblock";
      l.innerHTML = '<h3>Was laut Jahresplan lief</h3><ul class="mbliste">' +
        m.launches.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") +
        '</ul>';
      k.appendChild(l);
    }

    // --- Was nur sie wissen kann.
    var eigen = document.createElement("div");
    eigen.className = "mbblock";
    eigen.innerHTML = '<h3>Was du daraus mitnimmst</h3>';
    MB_FELDER.forEach(function (f) {
      var d2 = document.createElement("div");
      d2.className = "field mbfeld";
      var lab = document.createElement("label");
      lab.textContent = f.l;
      var ta = document.createElement("textarea");
      ta.rows = f.z;
      ta.placeholder = f.p;
      ta.value = n[f.k] || "";
      ta.oninput = function () {
        if (!monatsbogenNotizen[m.monat]) monatsbogenNotizen[m.monat] = {};
        monatsbogenNotizen[m.monat][f.k] = ta.value;
        mbSpeichern();
      };
      d2.appendChild(lab); d2.appendChild(ta);
      eigen.appendChild(d2);
    });
    k.appendChild(eigen);

    karte.appendChild(k);
    return karte;
  }

  function renderMonatsbogen(main) {
    if (!monatsbogen || !(monatsbogen.monate || []).length) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Monatsbogen</h1>' +
        '<p>Der Rückblick, der sich selbst ausfüllt.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch nichts gerechnet:<br>' +
        '<code>python scripts/cockpit/monatsbogen-bauen.py</code></div></div>';
      return;
    }
    var w = monatsbogen.waehrung || "CHF";
    var monate = monatsbogen.monate || [];
    var fertig = monate.filter(function (m) { return !m.laeuft_noch; });
    var jahr = new Date().getFullYear().toString();
    var imJahr = monate.filter(function (m) { return m.monat.indexOf(jahr) === 0; });
    var jahresumsatz = imJahr.reduce(function (s, m) { return s + (m.umsatz || 0); }, 0);
    var ziel = Number(settings.monatsziel) || 0;

    var ausgefuellt = monate.filter(function (m) {
      var n = monatsbogenNotizen[m.monat] || {};
      return n.learning || n.erkenntnis_zahlen || n.erkenntnis_content;
    }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Monatsbogen</h1>' +
      '<p>Was war, in Zahlen — und was du daraus mitnimmst. Umsatz, Reichweite ' +
      'und die Beiträge rechnet das Cockpit selbst; du schreibst nur, was du ' +
      'daraus liest.</p></div></div>' +
      '<div class="tiles">' +
      tile("Umsatz " + jahr, w + " " +
           jahresumsatz.toLocaleString("de-CH", { maximumFractionDigits: 0 }),
           imJahr.length + " Monate erfasst") +
      tile("Bester Monat",
           fertig.length
             ? esc(mbName(fertig.slice().sort(function (x, y) {
                 return (y.umsatz || 0) - (x.umsatz || 0); })[0].monat))
             : "—",
           fertig.length
             ? w + " " + Math.round(fertig.slice().sort(function (x, y) {
                 return (y.umsatz || 0) - (x.umsatz || 0); })[0].umsatz)
             : "") +
      (ziel ? tile("Monatsziel", w + " " + ziel.toLocaleString("de-CH"),
                   fertig.filter(function (m) { return (m.umsatz || 0) >= ziel; }).length +
                   " von " + fertig.length + " Monaten erreicht") : "") +
      tile("Ausgefüllt", ausgefuellt + " von " + monate.length, "mit deinem Fazit") +
      '</div>' +
      '<div id="mbliste"></div>' +
      '<p class="note" style="margin-top:14px">Der laufende Monat wird ohne ' +
      'Vergleich gezeigt — eine halbe Monatszahl gegen einen vollen Monat zu ' +
      'stellen ergibt jedes Mal einen falschen Alarm.</p>';

    var box = main.querySelector("#mbliste");
    monate.forEach(function (m) { box.appendChild(mbKarte(m, w)); });
  }

  function renderJahresplan(main) {'''

ALT_DISP = '    else if (activeTab === "launches") renderJahresplan(main);'
NEU_DISP = ('    else if (activeTab === "launches") renderJahresplan(main);\n'
            '    else if (activeTab === "monatsbogen") renderMonatsbogen(main);')

ALT_CSS = "  .jpbar { font-size: 11px; line-height: 20px; height: 20px; top: 4px; }"
NEU_CSS = """  .mbkarte { margin-bottom: 10px; padding: 0; overflow: hidden; }
  .mbkarte.laeuft { border-left: 3px solid var(--teal); }
  .mbkopf {
    display: flex; align-items: center; gap: 14px; width: 100%;
    background: none; border: 0; padding: 13px 17px; cursor: pointer;
    text-align: left; font: inherit; color: inherit; flex-wrap: wrap;
  }
  .mbkopf:hover { background: var(--surface-2); }
  .mbkarte.auf .dpfeil { transform: rotate(90deg); }
  .mbmonat { font-family: var(--display); font-size: 17px; min-width: 132px; }
  .mblaeuft {
    font-size: 10px; letter-spacing: 0.07em; text-transform: uppercase;
    color: var(--teal); background: var(--teal-soft);
    padding: 2px 9px; border-radius: 999px;
  }
  .mbwert { font-size: 13px; color: var(--ink-soft); white-space: nowrap; }
  .mbwert b { color: var(--ink); font-size: 15px; }
  .mbdelta { font-size: 11px; margin-left: 5px; }
  .mbdelta.hoch { color: var(--good); }
  .mbdelta.runter { color: var(--crit); }
  .mbkoerper { padding: 2px 17px 18px; border-top: 1px solid var(--line); }
  .mbblock { margin-top: 16px; }
  .mbblock h3 {
    font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); font-weight: normal; margin: 0 0 8px;
  }
  .mbbest { font-size: 13px; line-height: 1.5; margin: 5px 0; }
  .mbtag {
    font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
    padding: 1px 8px; border-radius: 999px; margin-right: 7px;
  }
  .mbtag.gut { background: rgba(47,125,91,0.14); color: var(--good); }
  .mbtag.schwach { background: var(--orange-soft); color: var(--orange); }
  .mbbest a { color: var(--teal); text-decoration: none; }
  .mbliste { margin: 0; padding-left: 19px; font-size: 13px; line-height: 1.65; }
  .mbfeld { margin-bottom: 11px; }
  .mbfeld textarea {
    width: 100%; background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 9px 11px; font: inherit; font-size: 13px;
    line-height: 1.55; resize: vertical;
  }
  .mbfeld textarea:focus { border-color: var(--teal); outline: none; }
  @media (max-width: 760px) {
    .mbkopf { gap: 9px; }
    .mbmonat { min-width: 100%; }
  }
  .jpbar { font-size: 11px; line-height: 20px; height: 20px; top: 4px; }"""

ERSETZUNGEN = [
    ("Reiter in der Leiste", ALT_NAV, NEU_NAV),
    ("Speicherplatz", ALT_VAR, NEU_VAR),
    ("Lokal laden", ALT_LS, NEU_LS),
    ("Aus der Datenbank", ALT_SNAP, NEU_SNAP),
    ("Der Reiter", ALT_FUNK, NEU_FUNK),
    ("Dispatcher", ALT_DISP, NEU_DISP),
    ("Aussehen", ALT_CSS, NEU_CSS),
]


def node_pruefen(html):
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(max(bloecke, key=len))
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
        return "" if r.returncode == 0 else (r.stderr or "").strip()[:600]
    except FileNotFoundError:
        return ""
    finally:
        Path(pfad).unlink(missing_ok=True)


def main():
    nur_pruefen = "--pruefen" in sys.argv
    html = SEITE.read_text(encoding="utf-8")
    vorher = len(html)

    if "function renderMonatsbogen" in html:
        sys.exit("Der Monatsbogen ist schon drin — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-22s ersetzt" % name)

    fehler = node_pruefen(html)
    if fehler:
        sys.exit("ABBRUCH — Node meldet einen Syntaxfehler:\n%s" % fehler)
    print("\n  Node --check: in Ordnung")

    if nur_pruefen:
        print("\nPROBELAUF — nichts geschrieben.")
        return
    SEITE.write_text(html, encoding="utf-8")
    print("\nGeschrieben: %s  (%d -> %d Zeichen)" % (SEITE, vorher, len(html)))


if __name__ == "__main__":
    main()
