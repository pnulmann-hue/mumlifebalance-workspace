"""Baut den Reiter „Wochenbogen" — Ersatz fuer die Notion-Wochenplanung.

In Notion war die letzte gepflegte Woche **KW35** (25.–31. August), und
„Erfolge letzte Woche" sowie „Herausforderung letzte Woche" waren in **jeder**
Woche leer — waehrend Fokus, CTA und Sales-Pattern sorgfaeltig ausformuliert
dastanden. Der Rueckblick fehlt, weil die Zahlen dafuer woanders lagen.

🚨 **Der Wochenfokus hat ab jetzt eine Quelle: hier.** Der Bild-Editor liest
seinen Fokus aus seiner eigenen Datenbank; zwei Artifacts sind nie verbunden,
die Bruecke laeuft ueber Claude. Richtung **Cockpit → Bild-Editor**, nie
zurueck — wer drueben tippt, verliert es beim naechsten Uebertrag.

🚨 **Die vier Routine-Haekchen aus Notion kommen mit** (Contentplanung, Mails
durchgesehen, Downloads aufgeraeumt, Tabs zu), aber klein und in einer Zeile.
Sie standen dort in jeder Woche auf Nein. Etwas, das nie angehakt wird, gehoert
nicht in die erste Bildschirmhaelfte.

Aufruf:
  python scripts/cockpit/patch-wochenbogen.py [--pruefen]
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

ALT_NAV = '    { id: "monatsbogen", label: "Monatsbogen" },'
NEU_NAV = ('    { id: "wochenbogen", label: "Wochenbogen" },\n'
           '    { id: "monatsbogen", label: "Monatsbogen" },')

ALT_VAR = '  var monatsbogen = null;        // daten/monatsbogen — Abgleich'
NEU_VAR = """  var monatsbogen = null;        // daten/monatsbogen — Abgleich
  var wochenbogen = null;        // daten/wochenbogen — Abgleich
  var wochenbogenNotizen = {};   // daten/wochenbogen-notizen — gehoert PATRICIA
  var wbOffen = null;"""

ALT_LS = '  monatsbogen = lsGet("monatsbogen", null);'
NEU_LS = ('  monatsbogen = lsGet("monatsbogen", null);\n'
          '  wochenbogen = lsGet("wochenbogen", null);\n'
          '  wochenbogenNotizen = lsGet("wochenbogen-notizen", {}) || {};')

ALT_SNAP = '''      db.doc("daten/monatsbogen").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/wochenbogen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        wochenbogen = snap.data() || null;
        lsSet("wochenbogen", wochenbogen);
        if (activeTab === "wochenbogen") render();
      }, function () {});
      db.doc("daten/wochenbogen-notizen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        wochenbogenNotizen = (snap.data() || {}).werte || {};
        lsSet("wochenbogen-notizen", wochenbogenNotizen);
        if (activeTab === "wochenbogen") render();
      }, function () {});
      db.doc("daten/monatsbogen").onSnapshot(function (snap) {'''

ALT_FUNK = "  function renderMonatsbogen(main) {"
NEU_FUNK = '''  /* =========================================================
     Wochenbogen
     ========================================================= */
  var WB_FELDER = [
    { k: "fokus", l: "Fokus der Woche", z: 2,
      p: "Ein Thema. Woran soll sie diese Woche denken?" },
    { k: "produkt", l: "🎯 Hauptprodukt", z: 1, p: "Worauf zahlt alles ein?" },
    { k: "cta", l: "Wochen-CTA", z: 1, p: "Stichwort oder Link" },
    { k: "pattern", l: "📅 Sales-Pattern", z: 3,
      p: "Wie führen die Stories über die Woche zum Angebot?" },
    { k: "erfolge", l: "Was lief gut", z: 2, p: "" },
    { k: "hindernis", l: "Was war schwierig", z: 2, p: "" }
  ];
  var WB_HAKEN = [
    { k: "contentplanung", l: "Content geplant" },
    { k: "mails", l: "Mails durchgesehen" },
    { k: "downloads", l: "Downloads aufgeräumt" },
    { k: "tabs", l: "Tabs zu" }
  ];

  function wbSpeichern() {
    clearTimeout(saveTimers.wochenbogenNotizen);
    saveTimers.wochenbogenNotizen = setTimeout(function () {
      lsSet("wochenbogen-notizen", wochenbogenNotizen);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/wochenbogen-notizen")
        .set({ werte: wochenbogenNotizen, updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function wbKarte(w, waehrung) {
    var n = wochenbogenNotizen[w.kw] || {};
    var auf = wbOffen === w.kw;
    var d = w.vs_vorwoche || {};
    var karte = document.createElement("div");
    karte.className = "panel mbkarte" + (auf ? " auf" : "") +
                      (w.laeuft_noch ? " laeuft" : "");

    var kopf = document.createElement("button");
    kopf.className = "mbkopf";
    kopf.innerHTML =
      '<span class="dpfeil">▸</span>' +
      '<span class="mbmonat">' + esc(w.kw.replace("-", " ")) + '</span>' +
      '<span class="note">' + esc(fmtDate(w.von)) + '–' + esc(fmtDate(w.bis)) + '</span>' +
      (w.laeuft_noch ? '<span class="mblaeuft">läuft</span>' : "") +
      (n.fokus ? '<span class="wbfokus">' + esc(n.fokus.slice(0, 44)) + '</span>'
               : '<span class="wbleer">kein Fokus gesetzt</span>') +
      '<span class="mbwert"><b>' + esc(waehrung) + " " +
        (w.umsatz || 0).toLocaleString("de-CH", { maximumFractionDigits: 0 }) +
        '</b>' + mbDelta(d.umsatz, "geld") + '</span>' +
      '<span class="mbwert">' + (w.beitraege || 0) + ' Beiträge' +
        mbDelta(d.beitraege) + '</span>' +
      '<span class="mbwert">' + (w.reichweite_median || 0) + ' Reichw.' +
        mbDelta(d.reichweite_median) + '</span>';
    kopf.onclick = function () { wbOffen = auf ? null : w.kw; render(); };
    karte.appendChild(kopf);
    if (!auf) return karte;

    var k = document.createElement("div");
    k.className = "mbkoerper";

    var zahlen = document.createElement("div");
    zahlen.className = "mbblock";
    zahlen.innerHTML = '<h3>Was gemessen wurde</h3><div class="gpwerte">' +
      '<div><b>' + esc(waehrung) + " " + (w.umsatz || 0).toLocaleString("de-CH",
        { maximumFractionDigits: 0 }) + '</b><span>Umsatz</span></div>' +
      '<div><b>' + (w.kaeufe || 0) + '</b><span>Käufe</span></div>' +
      '<div><b>' + (w.beitraege || 0) + '</b><span>Beiträge</span></div>' +
      '<div><b>' + (w.reichweite_median || 0) + '</b><span>Reichweite</span></div>' +
      '<div><b>' + (w.gespeichert || 0) + '</b><span>gespeichert</span></div>' +
      '<div><b>' + (w.geteilt || 0) + '</b><span>geteilt</span></div>' +
      '</div>' +
      (w.bester ? '<p class="mbbest" style="margin-top:7px">' +
        '<span class="mbtag gut">bester</span>' + esc(w.bester.anfang) +
        ' <b>' + w.bester.reach + '</b>' +
        (w.bester.link ? ' <a href="' + esc(w.bester.link) +
          '" target="_blank" rel="noopener">↗</a>' : "") + '</p>' : "");
    k.appendChild(zahlen);

    if ((w.laeuft || []).length) {
      var l = document.createElement("div");
      l.className = "mbblock";
      l.innerHTML = '<h3>Was laut Jahresplan läuft</h3><ul class="mbliste">' +
        w.laeuft.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") +
        '</ul>';
      k.appendChild(l);
    }

    var eigen = document.createElement("div");
    eigen.className = "mbblock";
    eigen.innerHTML = '<h3>Deine Planung und dein Fazit</h3>';
    WB_FELDER.forEach(function (f) {
      var d2 = document.createElement("div");
      d2.className = "field mbfeld";
      var lab = document.createElement("label");
      lab.textContent = f.l;
      var ta = document.createElement("textarea");
      ta.rows = f.z; ta.placeholder = f.p; ta.value = n[f.k] || "";
      ta.oninput = function () {
        if (!wochenbogenNotizen[w.kw]) wochenbogenNotizen[w.kw] = {};
        wochenbogenNotizen[w.kw][f.k] = ta.value;
        wbSpeichern();
      };
      d2.appendChild(lab); d2.appendChild(ta);
      eigen.appendChild(d2);
    });

    // Die vier Routine-Haken, klein und am Schluss.
    var hz = document.createElement("div");
    hz.className = "wbhaken";
    WB_HAKEN.forEach(function (h) {
      var lab = document.createElement("label");
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = !!n[h.k];
      cb.onchange = function () {
        if (!wochenbogenNotizen[w.kw]) wochenbogenNotizen[w.kw] = {};
        wochenbogenNotizen[w.kw][h.k] = cb.checked;
        wbSpeichern();
      };
      lab.appendChild(cb);
      lab.appendChild(document.createTextNode(" " + h.l));
      hz.appendChild(lab);
    });
    eigen.appendChild(hz);
    k.appendChild(eigen);

    karte.appendChild(k);
    return karte;
  }

  function renderWochenbogen(main) {
    if (!wochenbogen || !(wochenbogen.wochen || []).length) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Wochenbogen</h1>' +
        '<p>Fokus, Zahlen und Fazit je Woche.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch nichts gerechnet:<br>' +
        '<code>python scripts/cockpit/wochenbogen-bauen.py</code></div></div>';
      return;
    }
    var w = wochenbogen.waehrung || "CHF";
    var wochen = wochenbogen.wochen || [];
    var fertig = wochen.filter(function (x) { return !x.laeuft_noch; });
    var mitFokus = wochen.filter(function (x) {
      return (wochenbogenNotizen[x.kw] || {}).fokus;
    }).length;
    var beste = fertig.slice().sort(function (a, b) {
      return (b.reichweite_median || 0) - (a.reichweite_median || 0); })[0];

    main.innerHTML =
      '<div class="page-head"><div><h1>Wochenbogen</h1>' +
      '<p>Der Fokus für die Woche und was daraus wurde. Umsatz, Beiträge und ' +
      'Reichweite rechnet das Cockpit; Fokus, CTA und Fazit schreibst du.</p></div></div>' +
      '<div class="tiles">' +
      tile("Diese Woche", esc((wochenbogen.laufende_woche || "").replace("-", " ")),
           (wochenbogenNotizen[wochenbogen.laufende_woche] || {}).fokus
             ? "Fokus gesetzt" : "noch kein Fokus") +
      tile("Beste Woche", beste ? esc(beste.kw.replace("-", " ")) : "—",
           beste ? beste.reichweite_median + " Reichweite" : "") +
      tile("Mit Fokus", mitFokus + " von " + wochen.length, "ausgefüllt") +
      '</div><div id="wbliste"></div>' +
      '<p class="note" style="margin-top:14px">' + esc(wochenbogen.hinweis || "") +
      '</p>';

    var box = main.querySelector("#wbliste");
    wochen.forEach(function (x) { box.appendChild(wbKarte(x, w)); });
  }

  function renderMonatsbogen(main) {'''

ALT_DISP = '    else if (activeTab === "monatsbogen") renderMonatsbogen(main);'
NEU_DISP = ('    else if (activeTab === "monatsbogen") renderMonatsbogen(main);\n'
            '    else if (activeTab === "wochenbogen") renderWochenbogen(main);')

ALT_CSS = "  .mbkarte { margin-bottom: 10px; padding: 0; overflow: hidden; }"
NEU_CSS = """  .wbfokus { font-size: 13px; flex: 1 1 180px; min-width: 0;
             overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .wbleer { font-size: 12px; color: var(--ink-soft); font-style: italic;
            flex: 1 1 180px; }
  .wbhaken { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px;
             padding-top: 10px; border-top: 1px solid var(--line); }
  .wbhaken label { display: flex; align-items: center; gap: 6px;
                   font-size: 12px; color: var(--ink-soft); }
  .mbkarte { margin-bottom: 10px; padding: 0; overflow: hidden; }"""

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

    if "function renderWochenbogen" in html:
        sys.exit("Der Wochenbogen ist schon drin — nichts zu tun.")
    if "function mbDelta" not in html:
        sys.exit("ABBRUCH — erst `patch-monatsbogen.py` (liefert mbDelta).")

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
