  /* ======================================================================
     Reiter "Wissensbibliothek" — Produkte -> Wissensbibliothek
     (seit 27.10.2026, patch-bibliothek.py)

     Je Business-Schritt ein Thema: oben die Unterlagen als Link (Drive oeffnet
     PDFs, ein Artifact-Anhang nicht), darunter die Learnings aller Kurse, die
     zum Thema gehoeren. Die Texte sind gross, deshalb holt der Reiter erst das
     Verzeichnis bibliothek/_index und einen Kurs erst beim Aufklappen
     (bibliothek/k-<kurs>-<n>). Gemalt wird mit zgMarkdown aus dem Reiter
     "Zielgruppe & Markt".

     Erzeugt von bibliothek-bauen.py. Gekauftes Kursmaterial — das Cockpit
     muss privat sein.
     ====================================================================== */
  var bibIndex = null;
  var bibTexte = {};
  var bibThema = null;

  function bibIndexLaden(fertig) {
    if (bibIndex) { fertig(); return; }
    var lokal = lsGet("bib-index", null);
    if (lokal) { bibIndex = lokal; fertig(); }
    if (!db) {
      if (!lokal) setTimeout(function () { if (db) bibIndexLaden(fertig); }, 1500);
      return;
    }
    db.doc("bibliothek/_index").get().then(function (snap) {
      if (!snap.exists) { if (!lokal) { bibIndex = { themen: [], kurse: {} }; fertig(); } return; }
      bibIndex = tief(snap.data());
      lsSet("bib-index", bibIndex);
      fertig();
    }).catch(function () {
      if (!lokal) { bibIndex = { themen: [], kurse: {}, fehler: true }; fertig(); }
    });
  }

  function bibKursLaden(slug, fertig) {
    var k = (bibIndex.kurse || {})[slug] || {};
    bibTextLaden("k-" + slug, k.teile || 1, fertig);
  }

  /* schluessel: "k-<kurs>" (Kursdatei) oder "t-<thema>" (Themenbuch) */
  function bibTextLaden(schluessel, n, fertig) {
    var slug = schluessel;
    if (bibTexte[slug] != null) { fertig(bibTexte[slug]); return; }
    var lokal = [];
    for (var i = 1; i <= n; i++) lokal.push(lsGet("bib-" + slug + "-" + i, null));
    if (lokal.every(function (x) { return x != null; })) {
      bibTexte[slug] = lokal.join("");
      fertig(bibTexte[slug]);
      return;
    }
    if (!db) { fertig(null); return; }
    var holen = [];
    for (var j = 1; j <= n; j++) holen.push(db.doc("bibliothek/" + slug + "-" + j).get());
    Promise.all(holen).then(function (snaps) {
      var md = snaps.map(function (s) { return s.exists ? (s.data().md || "") : ""; }).join("");
      bibTexte[slug] = md;
      fertig(md);
    }).catch(function () { fertig(null); });
  }

  function bibMalen(md) {
    var html = zgMarkdown(md);
    return html.replace(/\s*[—–-]\s*Fundstelle:\s*([^<]*)/g,
      ' <span class="bib-fund">$1</span>');
  }

  function renderBibliothek(main) {
    main.innerHTML =
      '<div class="page-head"><div><h1>Wissensbibliothek</h1>' +
      '<p>Was du in den Kursen gelernt hast, nach Thema. Je Thema die Unterlagen ' +
      'zum Öffnen und die Learnings aus allen Kursen, die dazu gehören, vollständig ' +
      'und ohne das Drumherum.</p></div></div>' +
      '<div class="panel bib-hinweis"><strong>Gekauftes Kursmaterial.</strong> ' +
      'Nur für dich: nichts davon wörtlich in Kundentexte, und das Cockpit bleibt privat.</div>' +
      '<div class="panel bib-links"><a class="btn" href="https://kurse.juliatrost.de/" target="_blank" rel="noopener">Zu den Kursen &rarr;</a>' +
      ' <a class="btn" href="https://app.juliatrost.de/" target="_blank" rel="noopener">Claude-Kurse &rarr;</a></div>' +
      '<div id="bibinhalt"><div class="panel"><div class="empty">Lädt …</div></div></div>';

    bibIndexLaden(function () {
      var box = main.querySelector("#bibinhalt");
      if (!box) return;
      if (bibThema) bibThemaZeigen(box, bibThema);
      else bibUebersicht(box);
    });
  }

  function bibUebersicht(box) {
    var themen = (bibIndex && bibIndex.themen) || [];
    if (!themen.length) {
      box.innerHTML = '<div class="panel"><div class="empty">' +
        (bibIndex && bibIndex.fehler ? "Die Bibliothek liess sich nicht laden." : "Noch nichts da.") +
        ' Bauen mit <code>python scripts/cockpit/bibliothek-bauen.py</code>, ' +
        'dann in die Datenbank unter bibliothek/.</div></div>';
      return;
    }
    var gesamt = Object.keys(bibIndex.kurse || {}).length;
    box.innerHTML =
      '<div class="tiles">' +
        tile("Kursdateien", String(gesamt), "alle ausgewertet") +
        tile("Stand", bibIndex.stand ? fmtDate(bibIndex.stand) : "—", "") +
      '</div><div class="bib-grid"></div>';
    var grid = box.querySelector(".bib-grid");
    themen.forEach(function (t) {
      var nk = (t.kurse || []).length + (t.auch || []).length, nu = (t.unterlagen || []).length;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "bib-karte" + (nk || nu ? "" : " leer");
      b.innerHTML =
        '<span class="bib-ktitel">' + esc(t.titel) + '</span>' +
        '<span class="bib-kkurz">' + esc(t.kurz || "") + '</span>' +
        '<span class="bib-kzahl">' +
          (t.buch ? "Themenbuch · " : "") +
          (nk ? nk + (nk === 1 ? " Kurs" : " Kurse") : "noch keine Learnings") +
          (nu ? " · " + nu + (nu === 1 ? " Unterlage" : " Unterlagen") : "") +
        '</span>';
      b.addEventListener("click", function () {
        bibThema = t.id;
        bibThemaZeigen(box, t.id);
        window.scrollTo(0, 0);
      });
      grid.appendChild(b);
    });
  }

  function bibThemaZeigen(box, tid) {
    var t = ((bibIndex && bibIndex.themen) || []).filter(function (x) { return x.id === tid; })[0];
    if (!t) { bibThema = null; bibUebersicht(box); return; }
    var unterlagen = t.unterlagen || [];
    var kurse = t.kurse || [];
    box.innerHTML =
      '<button type="button" class="btn bib-zurueck">&larr; Alle Themen</button>' +
      '<h2 class="bib-ttitel">' + esc(t.titel) + '</h2>' +
      '<p class="bib-tkurz">' + esc(t.kurz || "") + '</p>' +
      '<div class="panel"><h2>Unterlagen</h2><div class="bib-unter"></div></div>' +
      '<div class="bib-buch"></div>' +
      '<h3 class="bib-zwischen">' + (t.buch ? "Nach Kurs, zum Nachschlagen" : "Learnings") + '</h3>' +
      '<div class="bib-kurse"></div>';
    box.querySelector(".bib-zurueck").addEventListener("click", function () {
      bibThema = null;
      bibUebersicht(box);
    });

    var ul = box.querySelector(".bib-unter");
    if (!unterlagen.length) ul.innerHTML = '<div class="empty">Noch keine Unterlagen verknüpft.</div>';
    unterlagen.forEach(function (u) {
      var z = document.createElement("div");
      z.className = "bib-uzeile";
      z.innerHTML =
        '<span class="bib-art">' + esc(u.art || "") + '</span>' +
        '<span class="bib-uname">' + esc(u.name) +
          (u.kurs ? ' <span class="bib-ukurs">' + esc(u.kurs) + '</span>' : '') +
          (u.notiz ? '<span class="bib-unotiz">' + esc(u.notiz) + '</span>' : '') +
        '</span>' +
        (u.link ? '<a class="btn" href="' + esc(u.link) + '" target="_blank" rel="noopener">Öffnen &rarr;</a>'
                : '<span class="bib-ohne">kein Link</span>');
      ul.appendChild(z);
    });

    if (t.buch) {
      var bd = document.createElement("details");
      bd.className = "panel zg-teil";
      bd.open = true;
      bd.innerHTML =
        '<summary><span class="zg-titel">Alles zum Thema, jeder Punkt einmal</span>' +
        '<span class="zg-kurz">' + Math.round((t.buch.zeichen || 0) / 1000) + "'000 Zeichen</span></summary>" +
        '<div class="zg-inhalt bib-inhalt"><div class="empty">Lädt …</div></div>';
      box.querySelector(".bib-buch").appendChild(bd);
      bibTextLaden("t-" + t.id, t.buch.teile || 1, function (md) {
        bd.querySelector(".bib-inhalt").innerHTML = md == null
          ? '<div class="empty">Der Text liess sich nicht laden.</div>'
          : bibMalen(md);
      });
    }

    var kb = box.querySelector(".bib-kurse");
    var auch = t.auch || [];
    if (!kurse.length && !auch.length) {
      kb.innerHTML = '<div class="panel"><div class="empty">Zu diesem Thema ist noch kein Kurs ausgewertet.</div></div>';
      return;
    }
    if (!kurse.length) {
      kb.innerHTML = '<div class="panel"><div class="empty">Noch kein Kurs, der hauptsächlich dieses Thema hat.</div></div>';
    }
    bibKursListe(kb, kurse, kurse.length === 1 && !t.buch);
    if (auch.length) {
      var h = document.createElement("h3");
      h.className = "bib-zwischen";
      h.textContent = "Streift das Thema auch";
      kb.appendChild(h);
      bibKursListe(kb, auch, false);
    }
  }

  function bibKursListe(kb, kurse, erstenOeffnen) {
    kurse.forEach(function (slug, n) {
      var k = (bibIndex.kurse || {})[slug] || {};
      var d = document.createElement("details");
      d.className = "panel zg-teil";
      d.innerHTML =
        '<summary><span class="zg-titel">' + esc(k.titel || slug) + '</span>' +
        '<span class="zg-kurz">' + Math.round((k.zeichen || 0) / 1000) + "'000 Zeichen</span></summary>" +
        '<div class="zg-inhalt bib-inhalt"><div class="empty">Lädt …</div></div>';
      var gemalt = false;
      d.addEventListener("toggle", function () {
        if (gemalt || !d.open) return;
        gemalt = true;
        bibKursLaden(slug, function (md) {
          d.querySelector(".bib-inhalt").innerHTML = md == null
            ? '<div class="empty">Der Text liess sich nicht laden.</div>'
            : bibMalen(md);
        });
      });
      if (n === 0 && erstenOeffnen) d.open = true;
      kb.appendChild(d);
      if (d.open) d.dispatchEvent(new Event("toggle"));
    });
  }
