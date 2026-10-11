"""Baut den Reiter „Gepostet & Analyse" — Schritt 1 der Notion-Abloesung.

Ersetzt die Notion-Ansicht „Analyse" der Content-Management-Datenbank.
Patricia am 24.09.2026: *„ziel für mich wäre, dass ich notion ablösen kann.
also auch gepostete beiträge sehen würde mit der analyse im anschluss"* — und
zur Abgrenzung: *„ich will nicht alles separat pflegen"*.

🚨 **Sieben von neun Spalten fallen damit als Handarbeit weg.** In Notion trug
sie Reichweite, Gespeichert, Gefaellt mir, Kommentare, neue Follower, URL und
Datum von Hand ein. Alle sieben liefert die Meta Graph API. Ihre Eingabe bleiben
Bewertung und Notiz — plus die vier Einordnungsfelder, die sie genannt hat
(Content-Saeule, Ueberthema, Produkt, Launch-Phase).

🚨 **Zwei Dokumente, nicht eins.** `daten/gepostet` gehoert dem Abgleich und
wird bei jedem Lauf ersetzt; `daten/gepostet-notizen` gehoert Patricia und darf
vom Abgleich **nie** geschrieben werden. Dasselbe Muster wie
`daten/produkt-details` — ein `set` vom Abgleich wuerde ihre Eintraege loeschen.

Aufruf:
  python scripts/cockpit/patch-gepostet.py [--pruefen]
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

# --------------------------------------------------------------------------
# 1) Reiter in die Leiste — direkt nach „Fertig zum Posten".
#    Der Fluss ist: planen -> fertig -> gepostet. Weiter unten waere er
#    ausserhalb des Blicks, in dem Patricia ohnehin arbeitet.
# --------------------------------------------------------------------------
ALT_NAV = '''    { id: "posts", label: "Content-Planung" },'''
NEU_NAV = '''    { id: "gepostet", label: "Gepostet & Analyse" },
    { id: "posts", label: "Content-Planung" },'''

# --------------------------------------------------------------------------
# 2) Speicherplatz
# --------------------------------------------------------------------------
ALT_VAR = "  var igzahlen = null;   // daten/instagram — gemessene Instagram-Werte"
NEU_VAR = """  var igzahlen = null;   // daten/instagram — gemessene Instagram-Werte
  var gepostet = null;        // daten/gepostet — Archiv, gehoert dem Abgleich
  var gepostetNotizen = {};   // daten/gepostet-notizen — gehoert PATRICIA
  var gepostetProfil = "";    // Filter in der Ansicht
  var gepostetOffen = null;   // welcher Beitrag aufgeklappt ist"""

ALT_LS = '  igzahlen = lsGet("ig-zahlen", null);'
NEU_LS = ('  igzahlen = lsGet("ig-zahlen", null);\n'
          '  gepostet = lsGet("gepostet", null);\n'
          '  gepostetNotizen = lsGet("gepostet-notizen", {}) || {};')

# --------------------------------------------------------------------------
# 3) Aus der Datenbank nachladen
# --------------------------------------------------------------------------
ALT_SNAP = '''      db.doc("daten/instagram").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/gepostet").onSnapshot(function (snap) {
        if (!snap.exists) return;
        gepostet = snap.data() || null;
        lsSet("gepostet", gepostet);
        if (activeTab === "gepostet") render();
      }, function () {});
      db.doc("daten/gepostet-notizen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        gepostetNotizen = (snap.data() || {}).werte || {};
        lsSet("gepostet-notizen", gepostetNotizen);
        if (activeTab === "gepostet") render();
      }, function () {});
      db.doc("daten/instagram").onSnapshot(function (snap) {'''

# --------------------------------------------------------------------------
# 4) Der Reiter selbst
# --------------------------------------------------------------------------
ALT_FUNK = "  function igZeile(k) {"
NEU_FUNK = '''  /* =========================================================
     Gepostet & Analyse — was rausging und was es gebracht hat
     ========================================================= */
  function notizSpeichern() {
    clearTimeout(saveTimers.gepostetNotizen);
    saveTimers.gepostetNotizen = setTimeout(function () {
      lsSet("gepostet-notizen", gepostetNotizen);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      // 🚨 Eigenes Dokument. Der taegliche Abgleich schreibt `daten/gepostet`
      // und darf das hier nie anfassen — sonst sind ihre Notizen weg.
      db.doc("daten/gepostet-notizen")
        .set({ werte: gepostetNotizen, updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function rateTon(r) {
    // Richtwert 1–3 %. Darunter ist es ein Befund, kein Zufall.
    if (r == null) return "";
    if (r >= 3) return "gut";
    if (r >= 1) return "ok";
    return "schwach";
  }

  function gpAngebote() {
    var a = ((katalog && katalog.angebote) || []).map(function (x) { return x.name; });
    return [""].concat(a.sort());
  }

  function gpKarte(b) {
    var n = gepostetNotizen[b.id] || {};
    var auf = gepostetOffen === b.id;
    var karte = document.createElement("div");
    karte.className = "gpkarte" + (auf ? " auf" : "");

    var kopf = document.createElement("button");
    kopf.className = "gpkopf";
    var typ = b.typ === "REELS" ? "Reel" : (b.art || "Beitrag");
    kopf.innerHTML =
      '<span class="gpdatum">' + esc(fmtDate ? fmtDate(b.datum) : b.datum) + '</span>' +
      '<span class="gptyp">' + esc(typ) + '</span>' +
      '<span class="gptext">' + esc(b.anfang || "") + '</span>' +
      '<span class="gprate ' + rateTon(b.rate) + '">' +
        (b.rate == null ? "—" : b.rate + " %") + '</span>' +
      '<span class="gpreach">' + (b.reach || 0).toLocaleString("de-CH") + '</span>';
    kopf.onclick = function () {
      gepostetOffen = auf ? null : b.id;
      render();
    };
    karte.appendChild(kopf);

    var koerper = document.createElement("div");
    koerper.className = "gpkoerper";
    if (!auf) { karte.appendChild(koerper); return karte; }

    // Die gemessenen Zahlen. Reine Anzeige — hier tippt niemand etwas ein.
    var zahlen = document.createElement("div");
    zahlen.className = "gpwerte";
    [["Reichweite", b.reach], ["Gefällt mir", b.likes],
     ["Kommentare", b.kommentare], ["Gespeichert", b.saved],
     ["Geteilt", b.shares]].forEach(function (w) {
      var d = document.createElement("div");
      d.innerHTML = "<b>" + (w[1] || 0).toLocaleString("de-CH") + "</b><span>" +
                    esc(w[0]) + "</span>";
      zahlen.appendChild(d);
    });
    koerper.appendChild(zahlen);

    var her = document.createElement("p");
    her.className = "note";
    her.style.margin = "2px 0 10px";
    her.innerHTML = "Gemessen am " + esc(b.zahlen_vom || "?") + " · kommt von Instagram" +
      (b.geplant_als ? " · geplant als <b>" + esc(b.geplant_als) + "</b>" : "") +
      (b.link ? ' · <a href="' + esc(b.link) + '" target="_blank" rel="noopener">ansehen ↗</a>' : "");
    koerper.appendChild(her);

    if (b.hook) {
      var hk = document.createElement("p");
      hk.className = "gphook";
      hk.textContent = "„" + b.hook + "“";
      koerper.appendChild(hk);
    }

    // Patricias Einordnung. Die Optionen kommen aus den Daten, nicht aus
    // diesem Code — siehe FELDER in gepostet-bauen.py.
    var felder = (gepostet && gepostet.felder) || [];
    var raster = document.createElement("div");
    raster.className = "gpfelder";
    felder.forEach(function (f) {
      var d = document.createElement("div");
      d.className = "field";
      var l = document.createElement("label");
      l.textContent = f.l;
      var sel = document.createElement("select");
      var opts = f.opt === "__angebote__" ? gpAngebote() : f.opt;
      opts.forEach(function (o) {
        var op = document.createElement("option");
        op.value = o; op.textContent = o || "—";
        if ((n[f.k] || "") === o) op.selected = true;
        sel.appendChild(op);
      });
      sel.onchange = function () {
        if (!gepostetNotizen[b.id]) gepostetNotizen[b.id] = {};
        gepostetNotizen[b.id][f.k] = sel.value;
        notizSpeichern();
        render();
      };
      d.appendChild(l); d.appendChild(sel);
      if (f.hinweis) {
        var h = document.createElement("span");
        h.className = "note";
        h.textContent = f.hinweis;
        d.appendChild(h);
      }
      raster.appendChild(d);
    });
    koerper.appendChild(raster);

    var nf = document.createElement("div");
    nf.className = "field";
    nf.style.marginTop = "10px";
    var nl = document.createElement("label");
    nl.textContent = "Was du daraus mitnimmst";
    var ta = document.createElement("textarea");
    ta.className = "gpnotiz";
    ta.rows = 3;
    ta.placeholder = "Warum lief das so? Was machst du beim nächsten Mal anders?";
    ta.value = n.notiz || "";
    ta.oninput = function () {
      if (!gepostetNotizen[b.id]) gepostetNotizen[b.id] = {};
      gepostetNotizen[b.id].notiz = ta.value;
      notizSpeichern();
    };
    nf.appendChild(nl); nf.appendChild(ta);
    koerper.appendChild(nf);

    karte.appendChild(koerper);
    return karte;
  }

  function renderGepostet(main) {
    if (!gepostet || !(gepostet.beitraege || []).length) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Gepostet &amp; Analyse</h1>' +
        '<p>Was rausgegangen ist und was es gebracht hat.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch kein Archiv. Es entsteht aus ' +
        'den Instagram-Zahlen:<br><code>python scripts/instagram-insights/holen.py</code>' +
        '<br><code>python scripts/cockpit/gepostet-bauen.py</code></div></div>';
      return;
    }

    var alle = gepostet.beitraege || [];
    var liste = gepostetProfil
      ? alle.filter(function (b) { return b.handle === gepostetProfil; })
      : alle;

    var mit = liste.filter(function (b) { return b.reach > 0; })
                   .map(function (b) { return b.reach; }).sort(function (x, y) { return x - y; });
    var median = mit.length ? mit[Math.floor(mit.length / 2)] : 0;
    var bester = liste.slice().sort(function (x, y) { return (y.reach || 0) - (x.reach || 0); })[0];
    var eingeordnet = liste.filter(function (b) {
      var n = gepostetNotizen[b.id] || {};
      return n.saeule || n.notiz;
    }).length;

    var handles = [];
    alle.forEach(function (b) {
      if (b.handle && handles.indexOf(b.handle) < 0) handles.push(b.handle);
    });

    var fw = gepostet.follower || {};
    var zuwachs = null, zuSeit = null;
    Object.keys(fw).forEach(function (h) {
      if (!gepostetProfil || h === gepostetProfil) {
        if (fw[h].zuwachs != null) {
          zuwachs = (zuwachs || 0) + fw[h].zuwachs;
          zuSeit = fw[h].seit;
        }
      }
    });

    main.innerHTML =
      '<div class="page-head"><div><h1>Gepostet &amp; Analyse</h1>' +
      '<p>Jeder Beitrag, der draussen war — mit den Zahlen, die Instagram dazu misst. ' +
      'Reichweite, Gespeichert, Geteilt und Kommentare holt der Abgleich selbst. ' +
      'Deine Einordnung und dein Fazit trägst du hier ein, sonst nichts.</p></div>' +
      '<div class="head-actions"><select class="btn" id="gpfilter"></select></div></div>' +
      (gepostet.veraltet
        ? '<p class="igwarn">Diese Zahlen sind ' + gepostet.alter_tage +
          ' Tage alt. Hol sie neu, bevor du danach entscheidest:<br>' +
          '<code>python scripts/instagram-insights/holen.py</code></p>'
        : "") +
      '<div class="tiles">' +
      tile("Im Archiv", liste.length, "Stand " + esc(gepostet.stand || "?")) +
      tile("Reichweite", median, "Median je Beitrag") +
      tile("Bester", bester ? bester.reach : 0,
           bester ? esc((bester.datum || "")) : "—") +
      (zuwachs != null
        ? tile("Follower", (zuwachs >= 0 ? "+" : "") + zuwachs, "seit " + esc(zuSeit || ""))
        : "") +
      tile("Eingeordnet", eingeordnet + " von " + liste.length, "mit Säule oder Fazit") +
      '</div>' +
      '<div class="panel" style="margin-bottom:14px"><div class="gpkopfzeile">' +
        '<span>Datum</span><span>Art</span><span>Anfang</span>' +
        '<span>Rate</span><span>Reichweite</span></div>' +
        '<div id="gpliste"></div></div>' +
      '<p class="note">Die Rate sind Interaktionen je erreichte Person — ' +
      'Richtwert 1 bis 3 Prozent. Auf die Reichweite gerechnet, nicht auf die ' +
      'Followerzahl: sonst wären die beiden Profile nicht vergleichbar. ' +
      'Das Archiv wächst mit jedem Abruf, auch wenn Instagram nur die letzten ' +
      '25 Beiträge herausgibt.</p>';

    var f = main.querySelector("#gpfilter");
    [["", "Beide Profile"]].concat(handles.map(function (h) { return [h, "@" + h]; }))
      .forEach(function (o) {
        var op = document.createElement("option");
        op.value = o[0]; op.textContent = o[1];
        if (gepostetProfil === o[0]) op.selected = true;
        f.appendChild(op);
      });
    f.onchange = function () { gepostetProfil = f.value; render(); };

    var box = main.querySelector("#gpliste");
    liste.forEach(function (b) { box.appendChild(gpKarte(b)); });
  }

  function igZeile(k) {'''

# --------------------------------------------------------------------------
# 5) Dispatcher
# --------------------------------------------------------------------------
ALT_DISP = '    else if (activeTab === "zahlen") renderZahlen(main);'
NEU_DISP = ('    else if (activeTab === "gepostet") renderGepostet(main);\n'
            '    else if (activeTab === "zahlen") renderZahlen(main);')

# --------------------------------------------------------------------------
# 6) Aussehen
# --------------------------------------------------------------------------
ALT_CSS = "  .igkonto {"
NEU_CSS = """  .gpkopfzeile, .gpkopf {
    display: grid; grid-template-columns: 92px 74px 1fr 74px 92px;
    gap: 10px; align-items: center;
  }
  .gpkopfzeile {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); padding: 0 0 8px; border-bottom: 1px solid var(--line);
  }
  .gpkopfzeile span:nth-child(4), .gpkopfzeile span:nth-child(5) { text-align: right; }
  .gpkarte { border-bottom: 1px solid var(--line); }
  .gpkopf {
    width: 100%; background: none; border: 0; padding: 9px 0;
    cursor: pointer; text-align: left; font: inherit; color: inherit;
  }
  .gpkopf:hover { background: var(--surface-2); }
  .gpkarte.auf { background: var(--surface-2); border-radius: 8px;
                 margin: 4px -10px; padding: 0 10px; }
  .gpdatum { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .gptyp {
    font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--teal); background: var(--teal-soft);
    padding: 1px 7px; border-radius: 999px; text-align: center;
  }
  .gptext { min-width: 0; overflow: hidden; text-overflow: ellipsis;
            white-space: nowrap; font-size: 13px; }
  .gprate { text-align: right; font-size: 13px; font-variant-numeric: tabular-nums; }
  .gprate.gut { color: var(--good); font-weight: 600; }
  .gprate.ok { color: var(--ink); }
  .gprate.schwach { color: var(--crit); }
  .gpreach { text-align: right; font-variant-numeric: tabular-nums; font-size: 14px; }
  .gpkoerper:not(:empty) { padding: 4px 0 16px; }
  .gpwerte { display: flex; gap: 22px; flex-wrap: wrap; margin: 8px 0 2px; }
  .gpwerte > div { display: flex; flex-direction: column; min-width: 84px; }
  .gpwerte b { font-size: 20px; line-height: 1.1; }
  .gpwerte span { font-size: 11px; color: var(--ink-soft); }
  .gphook {
    font-family: var(--display); font-size: 15px; line-height: 1.35;
    border-left: 3px solid var(--teal); padding: 4px 0 4px 11px; margin: 8px 0;
  }
  .gpfelder {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 10px; margin-top: 10px;
  }
  .gpnotiz {
    width: 100%; background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 9px 11px; font: inherit; font-size: 13px;
    line-height: 1.55; resize: vertical;
  }
  .gpnotiz:focus { border-color: var(--teal); outline: none; }
  @media (max-width: 720px) {
    .gpkopfzeile { display: none; }
    .gpkopf { grid-template-columns: 80px 1fr 62px; }
    .gpkopf .gptyp { display: none; }
    .gpkopf .gptext { grid-column: 1 / -1; white-space: normal; }
  }
  .igkonto {"""

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

    if "function renderGepostet" in html:
        sys.exit("Der Reiter ist schon drin — nichts zu tun.")

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
