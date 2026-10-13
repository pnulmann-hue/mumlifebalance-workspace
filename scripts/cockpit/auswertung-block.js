  /* ---------- „Was die Zahlen sagen“ (seit 13.10.2026, patch-auswertung.py) ----------
     Oben im Reiter „Gepostet & Analyse“. Liest daten/auswertung (zahlen-auswerten.py):
     Umsatz-Kacheln, Erkenntnis, drei Empfehlungen, Wochentage, Formate, Säulen,
     Stichwörter mit Umsatz, Diagnose je Beitrag, Bestenlisten.
     Patricia: „kein neues dashboard. sondern in meinem bestehenden schlau integrieren“. */
  function awChf(x) {
    if (x == null) return "–";
    return "CHF " + Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'");
  }
  function awZahl(x) {
    if (x == null) return "–";
    return Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'");
  }
  function awBalken(zeilen, feld, einheit) {
    var max = Math.max.apply(null, zeilen.map(function (z) { return z[feld] || 0; }).concat([1]));
    return '<div class="aw-balken">' + zeilen.map(function (z) {
      var w = Math.max(2, Math.round(100 * (z[feld] || 0) / max));
      return '<div class="aw-zeile"><span class="aw-name">' + esc(z.name) +
        ' <small>(' + z.beitraege + ')</small></span>' +
        '<span class="aw-spur"><span class="aw-fuell" style="width:' + w + '%"></span></span>' +
        '<span class="aw-wert">' + (feld === "rate" ? (z[feld] || 0).toFixed(1).replace(".", ",") + " %"
                                                   : awZahl(z[feld])) + (einheit || "") + '</span></div>';
    }).join("") + '</div>';
  }
  function awLink(z) {
    var t = esc((z.anfang || "").slice(0, 70)) + ((z.anfang || "").length > 70 ? " …" : "");
    return z.link ? '<a href="' + esc(z.link) + '" target="_blank" rel="noopener">' + t + '</a>' : t;
  }
  function auswertungBlock() {
    var a = zahlenAuswertung;
    if (!a) return '<div class="panel aw"><h2>Was die Zahlen sagen</h2><div class="empty">' +
      'Noch keine Auswertung. Sie entsteht mit <code>python scripts/cockpit/zahlen-auswerten.py</code> ' +
      'und liegt danach in daten/auswertung.</div></div>';
    var u = a.umsatz || {};
    var kacheln = '<div class="aw-kacheln">' +
      '<div class="aw-k"><b>' + awChf(u.umsatz) + '</b><span>Umsatz seit ' + esc(a.umsatz_ab || "") + '</span></div>' +
      '<div class="aw-k"><b>' + awZahl(u.kaeufe) + '</b><span>Käufe</span></div>' +
      '<div class="aw-k"><b>' + awChf(u.bestellwert) + '</b><span>Ø Bestellwert</span></div>' +
      '<div class="aw-k"><b>' + (u.anteil_ohne_stichwort == null ? "–" : Math.round(u.anteil_ohne_stichwort) + " %") +
        '</b><span>ohne Stichwort</span></div></div>';
    var erk = (a.erkenntnis || []).map(function (s) { return '<p>' + esc(s) + '</p>'; }).join("");
    var empf = '<ol class="aw-empf">' + (a.empfehlungen || []).map(function (e) {
      return '<li>' + esc(e.was) + '<br><small>' + esc(e.zahl) + '</small></li>';
    }).join("") + '</ol>';
    var kw = '<table class="aw-tab"><tr><th>Stichwort</th><th>Beiträge</th><th>Reichweite</th>' +
      '<th>Kommentare</th><th>Eingetragen</th><th>Käuferinnen</th><th>Umsatz</th><th>je 1’000</th></tr>' +
      (a.stichwoerter || []).map(function (k) {
        return '<tr' + (k.nie_benutzt ? ' class="aw-leer"' : '') + '><td><b>' + esc(k.stichwort) + '</b>' +
          (k.nie_benutzt ? ' <small>nie gespielt</small>' : '') +
          (k.geteilt_mit && k.geteilt_mit.length ? '<br><small>Käuferin auch bei ' + esc(k.geteilt_mit.join(", ")) + '</small>' : '') +
          '</td><td>' + k.beitraege + '</td><td>' + awZahl(k.reichweite) + '</td><td>' + k.kommentare +
          '</td><td>' + (k.eintragungen == null ? "–" : k.eintragungen) + '</td><td>' +
          (k.kaeuferinnen == null ? "–" : k.kaeuferinnen) + '</td><td>' + (k.umsatz ? awChf(k.umsatz) : "–") +
          '</td><td>' + (k.umsatz_je_1000 ? awChf(k.umsatz_je_1000) : "–") + '</td></tr>';
      }).join("") + '</table><p class="note">' + esc(a.umsatz_misst || "") +
      ' Die Spalte Umsatz darf nicht aufsummiert werden.</p>';
    var farbe = { "läuft": "gut", "Reichweite ohne Reaktion": "warn",
                  "Reaktion ohne Reichweite": "teal", "leise": "grau" };
    var diag = '<table class="aw-tab"><tr><th>Datum</th><th>Beitrag</th><th>Format</th><th>Reichweite</th>' +
      '<th>Rate</th><th>Diagnose</th></tr>' + (a.diagnose || []).slice(0, 20).map(function (d) {
        return '<tr><td>' + esc(d.datum) + '</td><td>' + awLink(d) + '</td><td>' + esc(d.format) +
          '</td><td>' + awZahl(d.reichweite) + '</td><td>' + String(d.rate).replace(".", ",") +
          ' %</td><td><span class="aw-d aw-' + (farbe[d.diagnose] || "grau") + '">' + esc(d.diagnose) +
          '</span></td></tr>';
      }).join("") + '</table>';
    function liste(titel, zs) {
      return '<div><h3>' + titel + '</h3><ol class="aw-top">' + (zs || []).map(function (z) {
        return '<li>' + awLink(z) + ' <small>' + esc(z.datum) + ' · ' + awZahl(z.reichweite) +
          ' erreicht · ' + String(z.rate).replace(".", ",") + ' %</small></li>';
      }).join("") + '</ol></div>';
    }
    var bp = a.bestperformer || null, bpHtml = "";
    if (bp) {
      var namen = { format: "Format", hooktyp: "Hook-Typ", thema: "Thema", laenge: "Caption-Länge", cta: "Aufruf" };
      bpHtml = '<details class="aw-mehr" open><summary>Deine Bestperformer-Formel</summary>' +
        '<p class="aw-formel">' + esc(bp.formel) + '</p>' +
        '<table class="aw-tab"><tr><th></th><th>in den Top 10</th><th>bei allen Beiträgen</th><th>Verteilung Top 10</th></tr>' +
        Object.keys(namen).filter(function (f) { return bp.muster && bp.muster[f]; }).map(function (f) {
          var m = bp.muster[f];
          return '<tr><td><b>' + namen[f] + '</b><br>' + esc(m.wert) + '</td><td>' + m.in_top + ' von ' + m.von +
            '</td><td>' + (m.anteil_gesamt == null ? "–" : m.anteil_gesamt + " %") + '</td><td><small>' +
            esc((m.verteilung || []).map(function (v) { return v[0] + " " + v[1]; }).join(" · ")) + '</small></td></tr>';
        }).join("") + '</table>' +
        '<table class="aw-tab"><tr><th>#</th><th>Beitrag</th><th>Format</th><th>Hook</th><th>Thema</th>' +
        '<th>Länge</th><th>Aufruf</th><th>Erreicht</th><th>Rate</th></tr>' +
        (bp.top || []).map(function (z, i) {
          return '<tr><td>' + (i + 1) + '</td><td>' + awLink(z) + '<br><small>' + esc(z.datum) + '</small></td><td>' +
            esc(z.format) + '</td><td>' + esc(z.hooktyp) + '</td><td>' + esc(z.thema) + '</td><td>' + esc(z.laenge) +
            '</td><td>' + esc(z.cta) + '</td><td>' + awZahl(z.reichweite) + '</td><td>' +
            String(z.rate).replace(".", ",") + ' %</td></tr>';
        }).join("") + '</table><p class="note">' + esc(bp.basis || "") +
        '. Der Gesamtanteil daneben zeigt, ob ein Merkmal in den Top 10 wirklich häufiger ist oder einfach überall.</p></details>';
    }
    var nf = a.nachfrage || [], nfHtml = "";
    if (nf.length) {
      nfHtml = '<details class="aw-mehr"><summary>Wo die Nachfrage liegt — Speichern, Teilen, Kommentieren je Thema</summary>' +
        '<table class="aw-tab"><tr><th>Thema</th><th>Beiträge</th><th>Erreicht</th><th>Gespeichert</th><th>Geteilt</th>' +
        '<th>Kommentare</th><th>je 1’000 erreicht</th></tr>' + nf.map(function (n) {
          return '<tr><td><b>' + esc(n.name) + '</b>' + (n.top || []).slice(0, 2).map(function (t) {
              return '<br><small>' + awLink(t) + ' · ' + t.saves + ' gesp. · ' + t.kommentare + ' Komm.</small>';
            }).join("") + '</td><td>' + n.beitraege + '</td><td>' + awZahl(n.reichweite) + '</td><td>' + n.saves +
            '</td><td>' + n.shares + '</td><td>' + n.kommentare + '</td><td>' +
            String(n.saves_je_1000 + n.shares_je_1000 + n.kommentare_je_1000).replace(".", ",").slice(0, 4) + '</td></tr>';
        }).join("") + '</table><p class="note">Wer speichert oder kommentiert, will das Thema weiterverwenden — das ' +
        'ist näher an „würde dafür zahlen“ als Reichweite. DMs liefert die Schnittstelle nicht, sie fehlen hier.</p></details>';
    }
    var b = a.basis || {};
    return '<div class="panel aw"><div class="aw-kopf"><h2>Was die Zahlen sagen</h2>' +
      '<span class="note">Stand ' + esc(a.stand) + ' · ' + b.beitraege + ' ausgereifte Beiträge seit ' +
      esc(b.ab) + ' · Median ' + awZahl(b.reichweite_median) + ' erreicht · Rate ' +
      String(b.rate_schnitt).replace(".", ",") + ' %</span></div>' + kacheln +
      '<div class="aw-erk">' + erk + '</div><h3>Was du diese Woche tun kannst</h3>' + empf +
      bpHtml + nfHtml +
      '<details class="aw-mehr"><summary>Wochentage · Formate · Säulen</summary><div class="aw-drei">' +
      '<div><h3>Wochentag (Median erreicht)</h3>' + awBalken(a.wochentage || [], "reichweite_median") + '</div>' +
      '<div><h3>Format (Median erreicht · Rate)</h3>' + awBalken(a.formate || [], "reichweite_median") +
      awBalken(a.formate || [], "rate") + '</div>' +
      '<div><h3>Säule (Median erreicht)</h3>' + awBalken(a.saeulen || [], "reichweite_median") + '</div>' +
      '</div></details>' +
      '<details class="aw-mehr"><summary>Stichwörter: Kommentare, Eintragungen, Umsatz</summary>' + kw + '</details>' +
      '<details class="aw-mehr"><summary>Wo springen die Leute ab — Diagnose je Beitrag</summary>' + diag + '</details>' +
      '<details class="aw-mehr"><summary>Bestenlisten</summary><div class="aw-drei">' +
      liste("Beste Rate (über dem Median)", a.top_rate) + liste("Reels mit der grössten Reichweite", a.top_reels) +
      liste("Karussells mit der grössten Reichweite", a.top_karussells) + '</div></details></div>';
  }
  function auswertungEinsetzen(main) {
    var kopf = main.querySelector(".page-head");
    var div = document.createElement("div");
    div.innerHTML = auswertungBlock();
    var el = div.firstChild;
    if (kopf && kopf.parentNode) kopf.parentNode.insertBefore(el, kopf.nextSibling);
    else main.insertBefore(el, main.firstChild);
  }
