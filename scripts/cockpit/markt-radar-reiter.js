  /* ======================================================================
     Reiter "Markt-Radar" — Instagram -> Markt-Radar
     (seit 30.10.2026, patch-markt-radar.py)

     Warum ein Reel gelaufen ist, je Konto: die 10 staerksten und 5
     schwaechsten gegen den Median des eigenen Kontos, mit Standbild,
     Bericht (Hebel, sofort, vermeiden, Muster) und beim eigenen Konto die
     Uhrzeit. Gebaut von scripts/hooks/radar.py, Sammlung "markt-radar"
     (_index + je Konto ein Dokument). Nur Anzeige — die Seite schreibt nichts.
     ====================================================================== */
  var radarIndex = null;
  var radarKonten = {};

  function radarIndexLaden(fertig) {
    if (radarIndex) { fertig(); return; }
    var lokal = lsGet("markt-radar", null);
    if (lokal) { radarIndex = lokal; fertig(); }
    if (!db) {
      if (!lokal) setTimeout(function () { if (db) radarIndexLaden(fertig); }, 1500);
      return;
    }
    db.doc("markt-radar/_index").get().then(function (snap) {
      if (!snap.exists) { if (!lokal) { radarIndex = { konten: [] }; fertig(); } return; }
      radarIndex = tief(snap.data());
      lsSet("markt-radar", radarIndex);
      fertig();
    }).catch(function () {
      if (!lokal) { radarIndex = { konten: [], fehler: true }; fertig(); }
    });
  }

  function radarKontoLaden(konto, fertig) {
    if (radarKonten[konto]) { fertig(radarKonten[konto]); return; }
    var lokal = lsGet("mr-" + konto, null);
    if (lokal) { radarKonten[konto] = lokal; fertig(lokal); }
    if (!db) return;
    db.doc("markt-radar/" + konto).get().then(function (snap) {
      if (!snap.exists) { if (!lokal) fertig(null); return; }
      var d = tief(snap.data());
      radarKonten[konto] = d;
      try { lsSet("mr-" + konto, d); } catch (e) { /* Speicher voll: nur ohne Zwischenspeicher */ }
      fertig(d);
    }).catch(function () { if (!lokal) fertig(null); });
  }

  function renderMarktRadar(main) {
    main.innerHTML =
      '<div class="page-head"><div><h1>Markt-Radar</h1>' +
      '<p>Warum ein Reel gelaufen ist: je Konto die zehn stärksten und die fünf schwächsten, gemessen am ' +
      'Median des eigenen Kontos, mit Blick ins Video. Vorschläge, die deine Regeln brechen, stehen unter ' +
      '„Passt nicht zu dir“.</p></div></div>' +
      '<div id="mrinhalt"><div class="panel"><div class="empty">Lädt …</div></div></div>';
    radarIndexLaden(function () { radarListe(main.querySelector("#mrinhalt")); });
  }

  function radarListe(box) {
    if (!box) return;
    var konten = (radarIndex && radarIndex.konten) || [];
    if (!konten.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Noch kein Lauf. Bauen mit ' +
        '<code>python scripts/hooks/radar.py</code>, dann in die Sammlung „markt-radar“.</div></div>';
      return;
    }
    var html = '<div class="tiles">' +
      tile("Konten", String(konten.length), "") +
      tile("Stand", radarIndex.stand ? fmtDate(radarIndex.stand) : "—", "") +
      '</div>';
    konten.forEach(function (k) {
      html += '<details class="panel zg-teil mr-konto" data-konto="' + esc(k.konto) + '">' +
        '<summary><span class="zg-titel">@' + esc(k.konto) + (k.eigen ? ' <span class="chip orange">dein Konto</span>' : '') + '</span>' +
        '<span class="zg-kurz">' + esc(k.anzahl + " Reels · Median " + k.masz + " " + k.median +
          " · Daten vom " + fmtDate(k.stand)) + '</span>' +
        (k.zusammenfassung ? '<span class="zg-kurz">' + esc(k.zusammenfassung) + '</span>' : '') +
        '</summary><div class="zg-inhalt mr-inhalt"><div class="empty">Lädt …</div></div></details>';
    });
    box.innerHTML = html;
    Array.prototype.forEach.call(box.querySelectorAll(".mr-konto"), function (el) {
      el.addEventListener("toggle", function () {
        if (!el.open || el.dataset.geladen) return;
        el.dataset.geladen = "1";
        radarKontoLaden(el.dataset.konto, function (d) {
          el.querySelector(".mr-inhalt").innerHTML = d ? radarKonto(d) :
            '<div class="empty">Der Bericht liess sich nicht laden.</div>';
        });
      });
    });
  }

  function radarKonto(d) {
    var b = d.bericht;
    var h = '<p class="mr-meta">' + esc(d.bilder || "") + (d.erstellt ? " · erstellt " + esc(fmtDate(d.erstellt)) : "") + '</p>';
    if (d.funde && d.funde.length) {
      h += '<div class="mr-warn">Noch offene Regelverstösse:<ul>' +
        d.funde.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join("") + '</ul></div>';
    }
    if (b) {
      h += '<h3>Zusammenfassung</h3><p>' + esc(b.zusammenfassung) + '</p>';
      h += '<h3>Die wichtigsten Hebel</h3><ul>' + (b.hebel || []).map(function (x) {
        return '<li><strong>' + esc(x.titel) + '</strong> <span class="mr-klein">Aufwand ' + esc(x.aufwand) +
          ' · Wirkung ' + esc(x.wirkung) + '/10</span><br>' + esc(x.beleg) + '</li>';
      }).join("") + '</ul>';
      h += '<h3>Sofort umsetzbar</h3><ol>' + (b.sofort || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join("") + '</ol>';
      h += '<h3>Das vermeiden</h3><ul>' + (b.vermeiden || []).map(function (x) {
        return '<li>' + esc(x.text) + ' <span class="mr-klein">' + esc(x.beleg) + '</span></li>';
      }).join("") + '</ul>';
      h += '<h3>Muster mit Zahlen</h3><ul>' + (b.muster || []).map(function (x) {
        return '<li><strong>' + esc(x.text) + '</strong><br><span class="mr-klein">' + esc(x.beleg) + '</span></li>';
      }).join("") + '</ul>';
      if (b.passt_nicht && b.passt_nicht.length) {
        h += '<h3>Passt nicht zu dir</h3><ul class="mr-nein">' + b.passt_nicht.map(function (x) {
          return '<li>' + esc(x.text) + ' <span class="mr-klein">' + esc(x.beleg) + '</span></li>';
        }).join("") + '</ul>';
      }
    } else {
      h += '<p class="mr-klein">Für dieses Konto gibt es nur die Auswahl, noch keinen Bericht.</p>';
    }
    if (d.uhrzeit) h += radarUhrzeit(d.uhrzeit);
    h += '<h3>Die Beiträge</h3><div class="mr-grid">';
    (d.beitraege || []).forEach(function (p) {
      h += '<div class="mr-post ' + (p.gruppe === "top" ? "mr-top" : "mr-flop") + '">' +
        (p.bild ? '<img src="' + p.bild + '" alt="" loading="lazy">' : '<div class="mr-ohnebild">kein Bild</div>') +
        '<div class="mr-text"><div class="mr-zahlen">' + (p.gruppe === "top" ? "▲" : "▼") + ' Faktor ' + esc(p.faktor) +
        ' · ' + esc(p.masz) + ' ' + esc(p.wert) + ' · Rate ' + esc(p.rate) + ' %' +
        (p.wiederholt ? ' · ' + esc(p.wiederholt) + '× gepostet' : '') + '</div>' +
        '<div class="mr-hook">' + esc(p.hook || "") + '</div>' +
        (p.warum ? '<div class="mr-warum">' + esc(p.warum) + '</div>' : '') +
        ((p.muster || []).length ? '<div class="mr-klein">' + esc(p.muster.join(" · ")) + '</div>' : '') +
        '<div class="mr-klein">' + esc(fmtDate(p.datum)) + (p.hook_note ? ' · Hook ' + esc(p.hook_note) + '/10 · Bild ' + esc(p.bild_note) + '/10' : '') +
        (p.link ? ' · <a href="' + esc(p.link) + '" target="_blank" rel="noopener">Zum Beitrag</a>' : '') + '</div>' +
        '</div></div>';
    });
    return h + '</div>';
  }

  function radarUhrzeit(u) {
    var h = '<h3>Uhrzeit (aus deinen eigenen Zahlen)</h3><p class="mr-klein">Ein Feld zählt erst ab 5 Beiträgen. ' +
      'Massstab ist der Median der Reichweite. Die Posting-Zeiten im Cockpit ändern sich dadurch nicht von selbst.</p>';
    Object.keys(u).forEach(function (typ) {
      var w = u[typ];
      var max = Math.max.apply(null, w.stunden.map(function (z) { return z.median; }).concat([1]));
      h += '<h4>' + esc(typ) + ' · ' + esc(w.beitraege) + ' Beiträge · Median ' + esc(w.median) + '</h4><div class="mr-balken">';
      w.stunden.forEach(function (z) {
        h += '<div class="mr-b' + (z.genug ? "" : " mr-duenn") + '" title="' + esc(z.feld + ":00 · Median " + z.median + " · " + z.anzahl + " Beiträge") + '">' +
          '<span style="height:' + Math.max(4, Math.round(70 * z.median / max)) + 'px"></span><em>' + esc(z.feld) + '</em></div>';
      });
      h += '</div>';
      if (w.beste_stunde) {
        h += '<p class="mr-klein">Stärkste Stunde ' + esc(w.beste_stunde.feld) + ':00 (Median ' + esc(w.beste_stunde.median) +
          ', ' + esc(w.beste_stunde.anzahl) + ' Beiträge) · schwächste ' + esc(w.schwaechste_stunde.feld) + ':00 (Median ' +
          esc(w.schwaechste_stunde.median) + ', ' + esc(w.schwaechste_stunde.anzahl) + ' Beiträge). Blasse Balken haben zu wenig Beiträge.</p>';
      }
      h += '<p class="mr-klein">' + w.tage.map(function (z) {
        return esc(z.feld) + ' ' + esc(z.median) + (z.genug ? '' : ' (' + esc(z.anzahl) + ')');
      }).join(" · ") + '</p>';
    });
    return h;
  }
