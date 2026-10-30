  /* ======================================================================
     Reiter "Gekaufte Kurse" — Produkte -> Gekaufte Kurse
     (seit 30.10.2026, patch-gekauft.py)

     Alle Kurse, die Patricia selbst gekauft hat, mit Link zum Login, dem
     Postfach, in dem die Zugangsmail liegt, und der Mail zum Wiederfinden.
     Daten: daten/gekauft (Quelle outputs/cockpit/abgleich/gekaufte-kurse.json,
     zusammengestellt aus Gmail, GMX und info@). Passwoerter stehen bewusst
     nicht drin, nur der Hinweis, in welcher Mail sie liegen.
     ====================================================================== */
  var gekauft = null;
  var gekauftSuche = "";

  function gekauftLaden(fertig) {
    if (gekauft) { fertig(); return; }
    var lokal = lsGet("gekauft", null);
    if (lokal) { gekauft = lokal; fertig(); }
    if (!db) {
      if (!lokal) setTimeout(function () { if (db) gekauftLaden(fertig); }, 1500);
      return;
    }
    db.doc("daten/gekauft").get().then(function (snap) {
      if (!snap.exists) { if (!lokal) { gekauft = { items: [] }; fertig(); } return; }
      gekauft = tief(snap.data());
      lsSet("gekauft", gekauft);
      fertig();
    }).catch(function () {
      if (!lokal) { gekauft = { items: [], fehler: true }; fertig(); }
    });
  }

  function renderGekauft(main) {
    main.innerHTML =
      '<div class="page-head"><div><h1>Gekaufte Kurse</h1>' +
      '<p>Alles, was du dir selbst gekauft hast, mit dem Weg hinein: Login, Postfach ' +
      'und die Mail, in der der Zugang steht.</p></div></div>' +
      '<div class="panel gk-suche"><input type="search" placeholder="Suchen: Name, Mentorin, Thema …" ' +
      'value="' + esc(gekauftSuche) + '"></div>' +
      '<div id="gkinhalt"><div class="panel"><div class="empty">Lädt …</div></div></div>';
    var feld = main.querySelector(".gk-suche input");
    feld.addEventListener("input", function () {
      gekauftSuche = feld.value;
      gekauftListe(main.querySelector("#gkinhalt"));
    });
    gekauftLaden(function () { gekauftListe(main.querySelector("#gkinhalt")); });
  }

  function gekauftListe(box) {
    if (!box) return;
    var alle = (gekauft && gekauft.items) || [];
    if (!alle.length) {
      box.innerHTML = '<div class="panel"><div class="empty">' +
        (gekauft && gekauft.fehler ? "Die Liste liess sich nicht laden." : "Noch nichts da.") +
        '</div></div>';
      return;
    }
    var s = gekauftSuche.trim().toLowerCase();
    var liste = alle.filter(function (k) {
      if (!s) return true;
      return [k.titel, k.von, k.bereich, k.plattform, k.notiz].join(" ").toLowerCase().indexOf(s) >= 0;
    });
    var abos = alle.filter(function (k) { return k.abo && !k.beendet; }).length;
    var html = '<div class="tiles">' +
      tile("Kurse", String(alle.length), "aus deinen Postfächern") +
      tile("Laufende Abos", String(abos), abos ? "kosten weiter" : "") +
      tile("Stand", gekauft.stand ? fmtDate(gekauft.stand) : "—", "") +
      '</div>';
    var bereiche = [];
    liste.forEach(function (k) { if (bereiche.indexOf(k.bereich) < 0) bereiche.push(k.bereich); });
    if (!liste.length) html += '<div class="panel"><div class="empty">Nichts gefunden.</div></div>';
    bereiche.forEach(function (b) {
      var teil = liste.filter(function (k) { return k.bereich === b; })
        .sort(function (x, y) { return String(y.datum).localeCompare(String(x.datum)); });
      html += '<h2 class="gk-bereich">' + esc(b) + ' <span>' + teil.length + '</span></h2><div class="gk-grid">';
      teil.forEach(function (k) {
        var mailLink = /^https?:/.test(k.mail || "");
        html += '<div class="panel gk-karte' + (k.beendet ? " gk-aus" : "") + '">' +
          '<div class="gk-kopf"><span class="gk-von">' + esc(k.von) + '</span>' +
          (k.abo ? '<span class="chip' + (k.beendet ? "" : " orange") + '">' + (k.beendet ? "Abo beendet" : "Abo") + '</span>' : "") +
          '</div>' +
          '<div class="gk-titel">' + esc(k.titel) + '</div>' +
          '<div class="gk-meta">' + esc(fmtDate(k.datum)) +
            (k.preis ? ' · ' + esc(k.preis) : "") + ' · ' + esc(k.plattform || "") + '</div>' +
          '<div class="gk-meta">Konto: ' + esc(k.konto || "—") + '</div>' +
          (mailLink ? "" : '<div class="gk-meta">Mail: ' + esc(k.mail || "—") + '</div>') +
          (k.notiz ? '<div class="gk-notiz">' + esc(k.notiz) + '</div>' : "") +
          '<div class="gk-fuss">' +
            (k.link && !/mail\.google\.com/.test(k.link)
              ? '<a class="btn primary" href="' + esc(k.link) + '" target="_blank" rel="noopener">Zum Kurs &rarr;</a>' : "") +
            (mailLink || /mail\.google\.com/.test(k.link || "")
              ? '<a class="btn" href="' + esc(mailLink ? k.mail : k.link) + '" target="_blank" rel="noopener">Zugangsmail &rarr;</a>' : "") +
          '</div></div>';
      });
      html += '</div>';
    });
    box.innerHTML = html;
  }
