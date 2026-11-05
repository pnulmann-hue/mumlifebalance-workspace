  /* =========================================================
     doTERRA → Freigaben (05.11.2026)
     Monats-Newsletter und Saison-Beiträge der Gruppe „Gesund durchs ganze Jahr“.
     Sammlung "doterra-freigaben": Claude legt Entwürfe ab, Patricia gibt frei,
     der Task doterra-freigaben-ausfuehren verschickt über ActiveCampaign bzw. plant in Telegram ein.
     Der Klick setzt nur status = "freigegeben". Eine Mail lässt sich nicht zurückholen,
     deshalb fragt der Newsletter-Knopf in zwei Klicks.
     ========================================================= */
  var dfDocs = null, dfLaeuft = false, dfScharf = null, dfVersuche = 0, dfFehler = false;

  function dfFertig() {
    if (activeTab === "uebersicht" || activeTab === "dtfreigaben") render();
  }

  // 🚨 Das erste render() läuft, bevor window.claude.use("db") fertig ist. Bis zum 05.11. wurde hier
  // die leere Liste gemerkt, und der Reiter meldete „Gerade liegt nichts bereit“, obwohl alles da lag.
  function dfHolen() {
    if (dfLaeuft || dfDocs) return;
    if (!db) {
      var mitDb = !!(window.claude && window.claude.use);
      if (!mitDb || dfVersuche >= 50) {
        dfFehler = mitDb;
        dfDocs = mitDb ? [] : (lsGet("df-docs", []) || []);
        setTimeout(dfFertig, 0);
        return;
      }
      dfVersuche++; dfLaeuft = true;
      setTimeout(function () { dfLaeuft = false; dfHolen(); }, 300);
      return;
    }
    dfLaeuft = true;
    db.collection("doterra-freigaben").limit(200).get().then(function (qs) {
      dfDocs = qs.docs.map(function (d) { var x = tief(d.data()) || {}; x.__id = d.id; return x; });
      dfFehler = false; dfLaeuft = false; dfFertig();
    }).catch(function () { dfFehler = true; dfLaeuft = false; dfDocs = []; dfFertig(); });
  }

  function dfOffen() {
    return (dfDocs || []).filter(function (d) { return (d.status || "entwurf") === "entwurf"; });
  }

  function dfSpeichern(d, felder) {
    Object.keys(felder).forEach(function (k) { d[k] = felder[k]; });
    d.updatedAt = new Date().toISOString();
    if (!db) { render(); return; }
    var sauber = {};
    Object.keys(d).forEach(function (k) { if (k.indexOf("__") !== 0) sauber[k] = d[k]; });
    db.doc("doterra-freigaben/" + d.__id).set(JSON.parse(JSON.stringify(sauber)))
      .then(function () { setSaveState("gespeichert", "on"); })
      .catch(function () { setSaveState("nicht gespeichert", "off"); toast("Das hat nicht geklappt, bitte nochmals"); });
    render();
  }

  var DF_STAND = {
    entwurf: "wartet auf dich",
    freigegeben: "freigegeben, geht beim nächsten Lauf raus",
    verschickt: "verschickt",
    eingeplant: "eingeplant",
    gepostet: "schon gepostet"
  };

  function dfKommentar(d) {
    var offen = d.kommentar && (!d.kommentarErledigt || d.kommentarErledigt < d.kommentarStand);
    return '<div class="df-kommentar"><label>Was soll ich ändern?<textarea data-df-k="' + esc(d.__id) + '" rows="2">' + esc(d.kommentar || "") + '</textarea></label>' +
      '<button class="btn" data-df-ks="' + esc(d.__id) + '">An Claude</button>' +
      (offen ? '<span class="df-hinweis">Liegt bei Claude</span>' : "") +
      (d.kommentarAntwort ? '<p class="df-antwort">' + esc(d.kommentarAntwort) + '</p>' : "") + '</div>';
  }

  function dfNewsletterHtml(d) {
    var st = d.status || "entwurf", offen = st === "entwurf";
    var wahl = d.betreffWahl || 0;
    var h = '<article class="df-karte"><div class="df-kopf"><h3>' + esc(d.titel) + '</h3><span class="df-stand ' + st + '">' + esc(DF_STAND[st] || st) + '</span></div>';
    h += '<fieldset class="df-betreffe"' + (offen ? "" : " disabled") + '><legend>Betreff</legend>' + (d.betreffe || []).map(function (b, i) {
      return '<label><input type="radio" name="df-b-' + esc(d.__id) + '" data-df-b="' + esc(d.__id) + '" value="' + i + '"' + (i === wahl ? " checked" : "") + '> ' + esc(b) + '</label>';
    }).join("") + '</fieldset>';
    h += '<p class="df-klein"><b>Vorschautext:</b> ' + esc(d.preheader || "") + '</p>';
    if (d.notiz) h += '<p class="df-notiz"><b>Vor der Freigabe:</b> ' + esc(d.notiz) + '</p>';
    // Ein Sandbox-Rahmen ohne allow-popups schluckt jeden Klick auf einen Link der Mail. Skripte bleiben gesperrt.
    h += '<details class="df-vorschau" open><summary>Mail ansehen</summary><iframe sandbox="allow-popups allow-popups-to-escape-sandbox" title="Vorschau Newsletter" data-df-mail="' + esc(d.__id) + '"></iframe></details>';
    var dfLinks = [], dfMuster = /href=["'](https?:[^"']+)["']/g, dfTreffer;
    while ((dfTreffer = dfMuster.exec(d.html || ""))) { if (dfLinks.indexOf(dfTreffer[1]) < 0) dfLinks.push(dfTreffer[1]); }
    if (dfLinks.length) h += '<div class="df-knoepfe">' + dfLinks.map(function (u, i) {
      return '<a class="btn" target="_blank" rel="noopener" href="' + esc(u) + '">' + (dfLinks.length > 1 ? "Link " + (i + 1) + " aus der Mail öffnen" : "Link aus der Mail öffnen") + '</a>';
    }).join("") + '</div>';
    if (offen) {
      h += dfKommentar(d) + '<div class="df-knoepfe"><button class="btn primary" data-df-nl="' + esc(d.__id) + '">' +
        (dfScharf === d.__id ? "Wirklich verschicken? Nochmals klicken" : "Freigeben und verschicken") + '</button></div>';
    } else if (st === "freigegeben") {
      h += '<div class="df-knoepfe"><button class="btn" data-df-zurueck="' + esc(d.__id) + '">Freigabe zurücknehmen</button></div>';
    }
    return h + '</article>';
  }

  function dfSaisonHtml(paket, liste) {
    var offen = liste.filter(function (d) { return (d.status || "entwurf") === "entwurf"; }).length;
    var h = '<section class="df-paket"><div class="df-kopf"><h2>' + esc(liste[0].saison) + ' ' + esc(liste[0].jahr) + ' · Gesund durchs ganze Jahr</h2>' +
      (offen ? '<button class="btn primary" data-df-alle="' + esc(paket) + '">Alle ' + offen + ' freigeben</button>' : "") + '</div>';
    if (!offen) h += '<p class="df-klein">Schon eingeplant, hier nur zum Ansehen. Soll sich etwas ändern, sag es Claude im Chat.</p>';
    h += liste.map(function (d) {
      var st = d.status || "entwurf", frei = st === "entwurf";
      return '<article class="df-beitrag">' + (d.bild ? '<img src="' + esc(d.bild) + '" alt="">' : "") +
        '<div class="df-beitragtext"><div class="df-kopf"><h3>' + esc(d.titel) + '</h3><span class="df-stand ' + st + '">' + esc(DF_STAND[st] || st) + '</span></div>' +
        '<label class="df-datum">Wann<input type="datetime-local" data-df-datum="' + esc(d.__id) + '" value="' + esc(d.datum || "") + '"' + (frei ? "" : " disabled") + '></label>' +
        '<details><summary>Text lesen</summary><p class="df-text">' + esc((d.text || "").replace(/\*/g, "")) + '</p></details>' +
        (frei ? dfKommentar(d) + '<div class="df-knoepfe"><button class="btn primary" data-df-frei="' + esc(d.__id) + '">Freigeben</button></div>' : "") +
        (st === "freigegeben" ? '<div class="df-knoepfe"><button class="btn" data-df-zurueck="' + esc(d.__id) + '">Freigabe zurücknehmen</button></div>' : "") +
        '</div></article>';
    }).join("");
    return h + '</section>';
  }

  function renderDtFreigaben(main) {
    if (!dfDocs) {
      main.innerHTML = '<div class="page-head"><div><h1>Freigaben</h1></div></div><p class="df-klein">Einen Moment …</p>';
      dfHolen();
      return;
    }
    function nachDoc(id) { return dfDocs.filter(function (d) { return d.__id === id; })[0]; }
    var nl = dfDocs.filter(function (d) { return d.art === "newsletter"; }).sort(function (a, b) { return a.monat < b.monat ? 1 : -1; });
    var pakete = {};
    dfDocs.filter(function (d) { return d.art === "saison"; }).sort(function (a, b) { return a.nr - b.nr; }).forEach(function (d) {
      (pakete[d.paket] = pakete[d.paket] || []).push(d);
    });
    var h = '<div class="page-head"><div><h1>Freigaben</h1><p>Was du hier freigibst, geht von selbst raus: der Newsletter über ActiveCampaign, die Saison-Beiträge in die Telegram-Gruppe. Der Lauf kommt um 9, 13 und 18 Uhr, solange die App offen ist.</p></div></div>';
    if (dfFehler) h += '<p class="df-klein">Die Freigaben liessen sich gerade nicht laden. Bitte lade das Cockpit neu.</p>';
    else if (!dfDocs.length) h += '<p class="df-klein">Gerade liegt nichts bereit.</p>';
    h += nl.map(dfNewsletterHtml).join("");
    Object.keys(pakete).sort().forEach(function (p) { h += dfSaisonHtml(p, pakete[p]); });
    main.innerHTML = h;

    main.querySelectorAll("[data-df-mail]").forEach(function (f) { var d = nachDoc(f.getAttribute("data-df-mail")); if (d) f.srcdoc = '<base target="_blank">' + (d.html || ""); });
    main.querySelectorAll("[data-df-b]").forEach(function (r) {
      r.addEventListener("change", function () { dfSpeichern(nachDoc(r.getAttribute("data-df-b")), { betreffWahl: +r.value }); });
    });
    main.querySelectorAll("[data-df-nl]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-df-nl");
        if (dfScharf !== id) {
          dfScharf = id; render();
          setTimeout(function () { if (dfScharf === id) { dfScharf = null; if (activeTab === "dtfreigaben") render(); } }, 8000);
          return;
        }
        dfScharf = null;
        dfSpeichern(nachDoc(id), { status: "freigegeben", freigabeAm: new Date().toISOString() });
        toast("Freigegeben, geht beim nächsten Lauf raus");
      });
    });
    main.querySelectorAll("[data-df-frei]").forEach(function (b) {
      b.addEventListener("click", function () { dfSpeichern(nachDoc(b.getAttribute("data-df-frei")), { status: "freigegeben", freigabeAm: new Date().toISOString() }); });
    });
    main.querySelectorAll("[data-df-alle]").forEach(function (b) {
      b.addEventListener("click", function () {
        (pakete[b.getAttribute("data-df-alle")] || []).forEach(function (d) {
          if ((d.status || "entwurf") === "entwurf") dfSpeichern(d, { status: "freigegeben", freigabeAm: new Date().toISOString() });
        });
        toast("Alle freigegeben");
      });
    });
    main.querySelectorAll("[data-df-zurueck]").forEach(function (b) {
      b.addEventListener("click", function () { dfSpeichern(nachDoc(b.getAttribute("data-df-zurueck")), { status: "entwurf" }); });
    });
    main.querySelectorAll("[data-df-datum]").forEach(function (i) {
      i.addEventListener("change", function () { dfSpeichern(nachDoc(i.getAttribute("data-df-datum")), { datum: i.value }); });
    });
    main.querySelectorAll("[data-df-ks]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-df-ks");
        var feld = main.querySelector('[data-df-k="' + id + '"]');
        if (!feld || !feld.value.trim()) return;
        dfSpeichern(nachDoc(id), { kommentar: feld.value.trim(), kommentarStand: new Date().toISOString() });
        toast("Claude schaut es sich beim nächsten Lauf an");
      });
    });
  }
