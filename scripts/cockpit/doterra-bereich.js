  /* =========================================================
     doTERRA-Bereich (13.10.2026) — Öl-Wissen · Anliegen · Business-Wege · Rising Leaders
     Siehe Kopf von patch-doterra-bereich.py.
     Daten: Sammlung "doterra-wissen" (gehört dem Abgleich: produkte, wege, anliegen-NN)
            daten/rising-leaders (gehört Patricia — der Abgleich schreibt dort NIE hinein)
     ========================================================= */
  var dtProdukte = null;      // { produkte: [], workshops: {} }
  var dtWege = null;          // { wege: [] }
  var dtAnliegen = null;      // [ … ] — gross, wird erst beim Öffnen geholt
  var dtEingang = null;       // Vorschläge aus dem Telegram-Abgleich (doterra-wissen/eingang)
  var dtLaeuft = false;
  var dtGeholt = false;       // einmal versucht — verhindert eine Endlosschleife ohne Datenbank
  var dtRising = { auftraege: [], beraterinnen: [], haken: {}, updatedAt: "" };
  var dtSuche = "", dtKat = "Alle", dtAnlWahl = null, dtAnlFilter = "";
  var dtWegOffen = null, dtLoeschScharf = null;
  var DT_STUFEN = [
    { id: "idee", label: "Idee" },
    { id: "gespraech", label: "Gespräch geplant" },
    { id: "infos", label: "Infos geschickt" },
    { id: "eingeschrieben", label: "Eingeschrieben" },
    { id: "eingearbeitet", label: "Eingearbeitet" }
  ];

  function dtHolen(fertig) {
    if (dtLaeuft || dtGeholt) return;
    if (!db) { dtGeholt = true; if (!dtAnliegen) dtAnliegen = lsGet("dt-anliegen", []) || []; dtEingang = lsGet("dt-eingang", null); fertig(); return; }
    dtLaeuft = true;
    db.collection("doterra-wissen").limit(40).get().then(function (qs) {
      var anl = [];
      qs.docs.forEach(function (d) {
        var x = tief(d.data()) || {};
        if (d.id === "produkte") { dtProdukte = x; lsSet("dt-produkte", x); }
        else if (d.id === "wege") { dtWege = x; lsSet("dt-wege", x); }
        else if (d.id === "eingang") { dtEingang = x; }
        else if (/^anliegen-/.test(d.id)) anl.push({ id: d.id, items: x.items || [] });
      });
      anl.sort(function (a, b) { return a.id < b.id ? -1 : 1; });
      dtAnliegen = [];
      anl.forEach(function (a) { dtAnliegen = dtAnliegen.concat(a.items); });
      dtLaeuft = false; dtGeholt = true;
      fertig();
    }).catch(function () { dtLaeuft = false; dtGeholt = true; if (!dtAnliegen) dtAnliegen = []; fertig(); });
  }

  function dtRisingSpeichern() {
    dtRising.updatedAt = new Date().toISOString();
    lsSet("dt-rising", dtRising);
    clearTimeout(saveTimers["dt-rising"]);
    saveTimers["dt-rising"] = setTimeout(function () {
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/rising-leaders").set(JSON.parse(JSON.stringify(dtRising)))
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 500);
  }

  function dtKopieren(text, knopf) {
    function ok() { if (knopf) { var a = knopf.textContent; knopf.textContent = "Kopiert"; setTimeout(function () { knopf.textContent = a; }, 1500); } }
    try {
      navigator.clipboard.writeText(text).then(ok, function () { dtKopierenAlt(text); ok(); });
    } catch (e) { dtKopierenAlt(text); ok(); }
  }
  function dtKopierenAlt(text) {
    var ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) { toast("Bitte von Hand markieren und kopieren"); }
    ta.remove();
  }

  function dtNochNichts(main, titel, satz) {
    if (dtGeholt) {
      main.innerHTML = '<div class="page-head"><div><h1>' + esc(titel) + '</h1><p>' + esc(satz) + '</p></div></div>' +
        '<div class="panel"><div class="empty">Noch nichts da. Der Abgleich legt es in der Sammlung „doterra-wissen“ ab.</div></div>';
      return;
    }
    main.innerHTML = '<div class="page-head"><div><h1>' + esc(titel) + '</h1><p>' + esc(satz) + '</p></div></div>' +
      '<div class="panel"><div class="empty">Wird geholt …</div></div>';
    dtHolen(function () { if (["oelwissen", "anliegen", "bizwege"].indexOf(activeTab) >= 0) render(); });
  }

  function dtDatum(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T12:00:00");
    return ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"][d.getDay()] + " " + d.getDate() + "." + (d.getMonth() + 1) + ".";
  }

  /* ---------- Öl-Wissen ---------- */
  function renderOelwissen(main) {
    if (!dtProdukte) { dtNochNichts(main, "Öl-Wissen", "Produkte, Anwendung und der richtige Satz für Kundinnen."); return; }
    var P = dtProdukte.produkte || [], W = dtProdukte.workshops || null;
    var heute = todayISO();
    var kats = ["Alle"];
    P.forEach(function (p) { if (kats.indexOf(p.kategorie) < 0) kats.push(p.kategorie); });

    var h = '<div class="page-head"><div><h1>Öl-Wissen</h1>' +
      '<p>Was drin ist, wie es riecht, wie man es anwendet, welcher Satz für Kundinnen passt und was du so nicht sagen darfst. ' +
      'Die Suche nach Beschwerden findest du unter „Anliegen“.</p></div></div>';
    if (W) {
      var kommend = (W.termine || []).filter(function (t) { return t >= heute; });
      h += '<div class="panel dt-abende"><h2>' + esc(W.titel) + ' · ' + esc(W.zeit) + '</h2><div class="dt-termine">' +
        (W.termine || []).map(function (t) {
          return '<span class="dt-termin' + (t < heute ? " vorbei" : t === kommend[0] ? " naechster" : "") + '">' + dtDatum(t) + '</span>';
        }).join("") + '</div><p class="note">' + esc(W.text) + '</p><div class="dt-knoepfe">' +
        (W.flyer ? '<a class="btn" href="' + esc(W.flyer) + '" target="_blank" rel="noopener">Flyer öffnen ↗</a>' : "") +
        '<button class="btn" type="button" id="dt-einladung">Einladung kopieren</button></div></div>';
    }
    h += '<div class="dt-werkzeug"><input id="dt-suche" type="search" placeholder="Suchen: Produkt, Duft, Anwendung … z. B. Diffuser oder Haut" autocomplete="off">' +
      '<div class="dt-chips">' + kats.map(function (k) {
        return '<button type="button" class="dt-chip" data-k="' + esc(k) + '" aria-pressed="' + (k === dtKat) + '">' + esc(k) + '</button>';
      }).join("") + '</div></div><div id="dt-liste" class="dt-karten"></div>';
    main.innerHTML = h;

    if (W) {
      var kommend2 = (W.termine || []).filter(function (t) { return t >= heute; });
      main.querySelector("#dt-einladung").onclick = function () {
        dtKopieren("Hey 💛 ich mache wieder meine Öl-Abende bei mir zuhause, jeweils um 20 Uhr: " +
          kommend2.map(dtDatum).join(", ") + ". Gemütlich zusammensitzen, ausprobieren, und du mischst dir deinen eigenen Roller zum Mitnehmen. Magst du kommen?" +
          (W.flyer ? " Hier der Flyer: " + W.flyer : ""), this);
      };
    }
    var feld = main.querySelector("#dt-suche");
    feld.value = dtSuche;
    main.querySelectorAll(".dt-chip").forEach(function (b) {
      b.onclick = function () { dtKat = b.dataset.k; render(); };
    });
    function zeigen() {
      var q = dtSuche.trim().toLowerCase();
      var tr = P.filter(function (p) {
        return (dtKat === "Alle" || p.kategorie === dtKat) && (!q || JSON.stringify(p).toLowerCase().indexOf(q) >= 0);
      });
      var liste = main.querySelector("#dt-liste");
      liste.innerHTML = tr.length ? tr.map(function (p) {
        var meta = [p.duft ? "<b>Duft:</b> " + esc(p.duft) : "", p.inhalt ? "<b>Drin:</b> " + esc(p.inhalt) : "",
                    p.groesse ? "<b>Grösse:</b> " + esc(p.groesse) : ""].filter(Boolean).join(" · ");
        return '<article class="panel dt-karte"><div class="dt-kat">' + esc(p.kategorie) + '</div>' +
          '<div class="dt-kopf"><h3>' + esc(p.name) + '</h3><span class="note">' + esc(p.deutsch || "") + '</span></div>' +
          (p.aktion ? '<div class="dt-aktion">' + esc(p.aktion) + '</div>' : "") +
          '<p class="dt-kurz">' + esc(p.kurz) + '</p>' + (meta ? '<p class="note">' + meta + '</p>' : "") +
          '<ul class="dt-anw">' + (p.anwendung || []).map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("") + '</ul>' +
          (p.hinweis ? '<p class="dt-hinweis">' + esc(p.hinweis) + '</p>' : "") +
          (p.patricia ? '<p class="dt-hinweis"><b>Ich selbst:</b> ' + esc(p.patricia) + '</p>' : "") +
          '<div class="dt-satz"><span class="dt-lab">Satz für Kundinnen</span><p>' + esc(p.kundinnentext) + '</p>' +
          '<button class="btn" type="button" data-kopie="' + esc(p.id) + '">Satz kopieren</button></div>' +
          (p.compliance && p.compliance !== "unkritisch" ? '<p class="dt-verbot"><b>So nicht sagen:</b> ' + esc(p.compliance) + '</p>' : "") +
          '</article>';
      }).join("") : '<div class="panel"><div class="empty">Nichts gefunden. Anderes Wort versuchen oder Filter auf „Alle“.</div></div>';
      liste.querySelectorAll("[data-kopie]").forEach(function (b) {
        b.onclick = function () {
          var p = P.filter(function (x) { return x.id === b.dataset.kopie; })[0];
          if (p) dtKopieren(p.kundinnentext, b);
        };
      });
    }
    var warten;
    feld.oninput = function () { dtSuche = feld.value; clearTimeout(warten); warten = setTimeout(zeigen, 150); };
    zeigen();
  }

  /* ---------- Anliegen (Symptom-Suche über alle Unterlagen) ---------- */
  function renderAnliegen(main) {
    if (!dtAnliegen) { dtNochNichts(main, "Anliegen", "Was deine Bücher und Unterlagen zu einem Thema sagen."); return; }
    if (!dtAnliegen.length) {
      main.innerHTML = '<div class="page-head"><div><h1>Anliegen</h1></div></div><div class="panel"><div class="empty">Noch keine Anliegen-Bibliothek da. ' +
        'Sie entsteht mit <code>python scripts/doterra/anliegen-bauen.py</code>.</div></div>';
      return;
    }
    var gruppen = [];
    dtAnliegen.forEach(function (a) { if (gruppen.indexOf(a.gruppe) < 0) gruppen.push(a.gruppe); });
    var wahl = dtAnliegen.filter(function (a) { return a.id === dtAnlWahl; })[0] || null;

    var h = '<div class="page-head"><div><h1>Anliegen</h1>' +
      '<p>Du tippst ein Thema an und siehst, was deine Bücher, E-Books, Hefte und Ernährungsnotizen dazu sagen, mit Quelle und Seite.</p></div></div>' +
      '<div class="dt-warn">🔒 Nur für dich. Hier stehen Aussagen aus Büchern, auch Heilaussagen. Nach aussen geht nur der Satz im Kasten „So sagst du es Kundinnen“.</div>' +
      '<input id="dt-anlsuche" type="search" class="dt-anlsuche" placeholder="Thema suchen, z. B. Husten, Schlaf, Wechseljahre" autocomplete="off">' +
      '<div id="dt-anlwahl">';
    gruppen.forEach(function (g) {
      h += '<div class="dt-gruppe"><span class="dt-lab">' + esc(g) + '</span><div class="dt-chips">' +
        dtAnliegen.filter(function (a) { return a.gruppe === g; }).map(function (a) {
          return '<button type="button" class="dt-chip" data-anl="' + esc(a.id) + '" aria-pressed="' + (a.id === dtAnlWahl) + '">' + esc(a.name) + '</button>';
        }).join("") + '</div></div>';
    });
    h += '</div><div id="dt-anlinhalt"></div>';
    main.innerHTML = h;

    main.querySelectorAll("[data-anl]").forEach(function (b) {
      b.onclick = function () { dtAnlWahl = dtAnlWahl === b.dataset.anl ? null : b.dataset.anl; render(); };
    });
    var such = main.querySelector("#dt-anlsuche");
    such.value = dtAnlFilter;
    function filtern() {
      var q = dtAnlFilter.trim().toLowerCase();
      main.querySelectorAll("[data-anl]").forEach(function (b) {
        b.hidden = !!q && b.textContent.toLowerCase().indexOf(q) < 0;
      });
      main.querySelectorAll(".dt-gruppe").forEach(function (g) {
        g.hidden = !!q && !g.querySelector("[data-anl]:not([hidden])");
      });
    }
    such.oninput = function () { dtAnlFilter = such.value; filtern(); };
    filtern();

    var ziel = main.querySelector("#dt-anlinhalt");
    if (!wahl) { ziel.innerHTML = '<p class="note">' + dtAnliegen.length + ' Themen. Tipp eins an.</p>'; return; }

    function stelle(s) {
      var lang = s.t.length > 320;
      return '<div class="dt-stelle"><div class="dt-quelle"><b>' + esc(s.q) + '</b>' + (s.w ? ' · ' + esc(s.w) : "") +
        '<span class="dt-qkat">' + esc(s.k) + '</span></div>' +
        (lang ? '<details><summary>' + esc(s.t.slice(0, 300)) + ' …</summary><p>' + esc(s.t) + '</p></details>' : '<p>' + esc(s.t) + '</p>') +
        ((s.o && s.o.length) ? '<div class="dt-oelzeile">' + s.o.map(function (o) { return '<span class="chip">' + esc(o) + '</span>'; }).join(" ") + '</div>' : "") +
        '</div>';
    }
    var oele = (wahl.stellen || []).filter(function (s) { return s.k === "Öle" || s.k === "Gemüt"; });
    var koerper = (wahl.stellen || []).filter(function (s) { return !(s.k === "Öle" || s.k === "Gemüt"); });
    var x = '<div class="panel dt-anlkopf"><h2>' + esc(wahl.name) + '</h2>' +
      '<p class="note">' + wahl.quellen_gesamt + ' deiner Quellen sprechen darüber. Unten die ' + (wahl.stellen || []).length + ' aussagekräftigsten Stellen.</p>' +
      '<div class="dt-satz"><span class="dt-lab">So sagst du es Kundinnen</span><p>' + esc(wahl.kundinnen) + '</p>' +
      '<button class="btn" type="button" id="dt-anlkopie">Satz kopieren</button></div>';
    if ((wahl.oele || []).length) {
      x += '<span class="dt-lab">Öle, die deine Quellen dazu nennen</span><div class="dt-oelrang">' +
        wahl.oele.map(function (o) {
          return '<span class="dt-oel" title="' + esc(o.quellen.join(" · ")) + '"><b>' + esc(o.oel) + '</b> ' + o.n + ' Quellen</span>';
        }).join("") + '</div>';
    }
    x += '</div>';
    if (oele.length) x += '<h3 class="dt-h3">Aus deinen Ölbüchern</h3>' + oele.map(stelle).join("");
    if (koerper.length) x += '<h3 class="dt-h3">Dazu aus Ernährung, Hormonen &amp; Rhythmus</h3>' + koerper.map(stelle).join("");
    ziel.innerHTML = x;
    var k = ziel.querySelector("#dt-anlkopie");
    if (k) k.onclick = function () { dtKopieren(wahl.kundinnen, k); };
  }

  /* ---------- Business-Wege ---------- */
  function renderBizwege(main) {
    if (!dtWege) { dtNochNichts(main, "Business-Wege", "Abläufe Schritt für Schritt."); return; }
    var wege = dtWege.wege || [];
    var haken = dtRising.haken || (dtRising.haken = {});
    var h = '<div class="page-head"><div><h1>Business-Wege</h1>' +
      '<p>Abläufe Schritt für Schritt, zum Abhaken. Nach einer Kundin oder Beraterin setzt du die Haken zurück und fängst beim nächsten Mal wieder oben an.</p></div></div>';
    wege.forEach(function (w) {
      var hk = haken[w.id] || {};
      var n = (w.schritte || []).filter(function (s) { return hk[s.id]; }).length;
      var offen = dtWegOffen === w.id;
      h += '<details class="panel dt-weg"' + (offen ? " open" : "") + ' data-weg="' + esc(w.id) + '"><summary>' +
        '<span class="dt-wegtitel">' + esc(w.titel) + '</span><span class="dt-fort">' + n + ' / ' + (w.schritte || []).length + '</span>' +
        '<span class="note dt-wozu">' + esc(w.wozu || "") + '</span></summary><ol class="dt-schritte">';
      (w.schritte || []).forEach(function (s) {
        h += '<li class="' + (hk[s.id] ? "fertig" : "") + '"><label class="dt-check"><input type="checkbox" data-w="' + esc(w.id) + '" data-s="' + esc(s.id) + '"' +
          (hk[s.id] ? " checked" : "") + '><span>' + esc(s.titel) + '</span></label>' +
          (s.wie ? '<p>' + esc(s.wie) + '</p>' : "") +
          (s.vorlage ? '<div class="dt-satz"><span class="dt-lab">Vorlage</span><p>' + esc(s.vorlage) + '</p>' +
            '<button class="btn" type="button" data-vorlage="' + esc(w.id + "|" + s.id) + '">Vorlage kopieren</button></div>' : "") +
          (s.quelle ? '<p class="dt-q">Quelle: ' + esc(s.quelle) + '</p>' : "") + '</li>';
      });
      h += '</ol><button class="btn ghost" type="button" data-zurueck="' + esc(w.id) + '">Haken zurücksetzen</button></details>';
    });
    main.innerHTML = h;
    main.querySelectorAll(".dt-weg").forEach(function (d) {
      d.addEventListener("toggle", function () { if (d.open) dtWegOffen = d.dataset.weg; else if (dtWegOffen === d.dataset.weg) dtWegOffen = null; });
    });
    main.querySelectorAll("input[data-w]").forEach(function (c) {
      c.onchange = function () {
        var hk = haken[c.dataset.w] || (haken[c.dataset.w] = {});
        if (c.checked) hk[c.dataset.s] = todayISO(); else delete hk[c.dataset.s];
        dtWegOffen = c.dataset.w; dtRisingSpeichern(); render();
      };
    });
    main.querySelectorAll("[data-vorlage]").forEach(function (b) {
      b.onclick = function () {
        var p = b.dataset.vorlage.split("|");
        var w = wege.filter(function (x) { return x.id === p[0]; })[0];
        var s = w && (w.schritte || []).filter(function (x) { return x.id === p[1]; })[0];
        if (s) dtKopieren(s.vorlage, b);
      };
    });
    main.querySelectorAll("[data-zurueck]").forEach(function (b) {
      b.onclick = function () { delete haken[b.dataset.zurueck]; dtWegOffen = b.dataset.zurueck; dtRisingSpeichern(); render(); toast("Haken zurückgesetzt"); };
    });
  }

  /* ---------- Rising Leaders: Aufträge + Beraterinnen ---------- */
  function renderRising(main) {
    var A = dtRising.auftraege || (dtRising.auftraege = []);
    var B = dtRising.beraterinnen || (dtRising.beraterinnen = []);
    var heute = todayISO();
    var offen = A.filter(function (a) { return !a.erledigt; }).sort(function (x, y) { return (x.frist || "9") < (y.frist || "9") ? -1 : 1; });
    var fertig = A.filter(function (a) { return a.erledigt; });

    function auftragZeile(a) {
      var spaet = a.frist && a.frist < heute && !a.erledigt;
      return '<div class="dt-auftrag' + (a.erledigt ? " fertig" : "") + (spaet ? " spaet" : "") + '">' +
        '<input type="checkbox" data-a="' + esc(a.id) + '"' + (a.erledigt ? " checked" : "") + ' aria-label="erledigt">' +
        '<div class="dt-atext"><div>' + esc(a.text) + '</div><div class="note">' +
        (a.frist ? (spaet ? "⚠️ überfällig · " : "bis ") + dtDatum(a.frist) : "ohne Frist") +
        (a.quelle ? " · " + esc(a.quelle) : "") + '</div></div>' +
        '<button class="btn ghost" type="button" data-adel="' + esc(a.id) + '">' + (dtLoeschScharf === a.id ? "Wirklich löschen?" : "✕") + '</button></div>';
    }

    if (!dtGeholt) dtHolen(function () { if (activeTab === "rising") render(); });
    var E = dtRising.eingang || (dtRising.eingang = {});
    var vorschlaege = ((dtEingang && dtEingang.items) || []).filter(function (v) { return !E[v.id]; });
    var ART = { auftrag: "Auftrag", tipp: "Produkt-Tipp", training: "Training" };
    var eh = vorschlaege.length ? '<section class="panel dt-eingang"><h2>Neu aus Telegram <span class="note">' + vorschlaege.length +
      ' Vorschläge · Stand ' + esc((dtEingang.stand || "").slice(0, 10)) + '</span></h2>' +
      vorschlaege.map(function (v) {
        return '<div class="dt-vorschlag"><div><span class="chip' + (v.art === "auftrag" ? " orange" : "") + '">' + esc(ART[v.art] || v.art) + '</span> ' +
          '<b>' + esc(v.titel || "") + '</b>' + (v.frist ? ' <span class="note">bis ' + dtDatum(v.frist) + '</span>' : "") + '</div>' +
          '<p class="note">' + esc(v.chat || "") + (v.datum ? " · " + esc(v.datum.slice(0, 10)) : "") + (v.von ? " · " + esc(v.von) : "") + '</p>' +
          (v.auszug ? '<details><summary>Original</summary><p>' + esc(v.auszug) + '</p></details>' : "") +
          '<div class="dt-knoepfe"><button class="btn primary" type="button" data-ein="' + esc(v.id) + '">Übernehmen</button>' +
          '<button class="btn ghost" type="button" data-weg="' + esc(v.id) + '">Verwerfen</button></div></div>';
      }).join("") + '</section>' : "";

    var h = eh + '<div class="page-head"><div><h1>Rising Leaders</h1>' +
      '<p>Die Aufträge aus der Gruppe mit Frist zum Abhaken, und deine möglichen Beraterinnen vom ersten Gedanken bis eingearbeitet.</p></div></div>' +
      '<div class="cols"><section class="panel"><h2>Aufträge <span class="note">' + offen.length + ' offen</span></h2>' +
      '<div class="dt-neu"><input id="dt-atext" placeholder="Neuer Auftrag, z. B. 3 Gespräche über das Business führen" autocomplete="off">' +
      '<input id="dt-afrist" type="date"><button class="btn primary" type="button" id="dt-aplus">Hinzufügen</button></div>' +
      (offen.length ? offen.map(auftragZeile).join("") : '<div class="empty">Keine offenen Aufträge.</div>') +
      (fertig.length ? '<details class="dt-erledigt"><summary>' + fertig.length + ' erledigt</summary>' + fertig.map(auftragZeile).join("") + '</details>' : "") +
      '<p class="note">Neue Aufträge aus den Telegram-Gruppen erscheinen oben unter „Neu aus Telegram“.</p></section>' +
      '<section class="panel"><h2>Beraterinnen <span class="note">' + B.length + ' im Blick</span></h2>' +
      '<div class="dt-neu"><input id="dt-bname" placeholder="Name" autocomplete="off"><input id="dt-bnotiz" placeholder="Warum sie? (optional)" autocomplete="off">' +
      '<button class="btn primary" type="button" id="dt-bplus">Hinzufügen</button></div>';
    DT_STUFEN.forEach(function (st) {
      var leute = B.filter(function (b) { return (b.stufe || "idee") === st.id; });
      h += '<div class="dt-stufe"><span class="dt-lab">' + esc(st.label) + ' · ' + leute.length + '</span>';
      leute.forEach(function (b) {
        h += '<div class="dt-person"><div class="dt-pkopf"><b>' + esc(b.name) + '</b>' +
          '<select data-bstufe="' + esc(b.id) + '">' + DT_STUFEN.map(function (s) {
            return '<option value="' + s.id + '"' + ((b.stufe || "idee") === s.id ? " selected" : "") + '>' + esc(s.label) + '</option>';
          }).join("") + '</select><button class="btn ghost" type="button" data-bdel="' + esc(b.id) + '">' + (dtLoeschScharf === b.id ? "Wirklich löschen?" : "✕") + '</button></div>' +
          (b.notiz ? '<p class="note">' + esc(b.notiz) + '</p>' : "") +
          '<div class="dt-naechst"><input data-bnext="' + esc(b.id) + '" value="' + esc(b.naechster || "") + '" placeholder="Nächster Schritt">' +
          '<input type="date" data-bdatum="' + esc(b.id) + '" value="' + esc(b.datum || "") + '"></div></div>';
      });
      h += '</div>';
    });
    h += '</section></div>';
    main.innerHTML = h;

    function neuId(p) { return p + Date.now().toString(36) + Math.random().toString(36).slice(2, 5); }
    main.querySelectorAll("[data-ein]").forEach(function (b) {
      b.onclick = function () {
        var v = vorschlaege.filter(function (x) { return x.id === b.dataset.ein; })[0];
        if (!v) return;
        if (v.art === "auftrag") {
          A.push({ id: "tg-" + v.id, text: v.titel, frist: v.frist || "", quelle: v.chat || "Telegram", angelegt: heute, erledigt: false });
          toast("Als Auftrag übernommen");
        } else {
          toast(v.art === "tipp" ? "Kommt beim nächsten Abgleich ins Öl-Wissen" : "Kommt beim nächsten Abgleich in die Business-Wege");
        }
        E[v.id] = "uebernommen"; dtRisingSpeichern(); render();
      };
    });
    main.querySelectorAll("[data-weg]").forEach(function (b) {
      b.onclick = function () { E[b.dataset.weg] = "verworfen"; dtRisingSpeichern(); render(); };
    });
    main.querySelector("#dt-aplus").onclick = function () {
      var t = main.querySelector("#dt-atext").value.trim();
      if (!t) { toast("Erst den Auftrag eintippen"); return; }
      A.push({ id: neuId("a"), text: t, frist: main.querySelector("#dt-afrist").value || "", quelle: "von Hand", angelegt: heute, erledigt: false });
      dtRisingSpeichern(); render();
    };
    main.querySelector("#dt-bplus").onclick = function () {
      var n = main.querySelector("#dt-bname").value.trim();
      if (!n) { toast("Erst einen Namen eintippen"); return; }
      B.push({ id: neuId("b"), name: n, notiz: main.querySelector("#dt-bnotiz").value.trim(), stufe: "idee", naechster: "", datum: "", angelegt: heute });
      dtRisingSpeichern(); render();
    };
    main.querySelectorAll("[data-a]").forEach(function (c) {
      c.onchange = function () {
        var a = A.filter(function (x) { return x.id === c.dataset.a; })[0];
        if (a) { a.erledigt = c.checked; a.erledigt_am = c.checked ? heute : ""; dtRisingSpeichern(); render(); }
      };
    });
    function loeschen(liste, id) {
      if (dtLoeschScharf !== id) {
        dtLoeschScharf = id; render();
        setTimeout(function () { if (dtLoeschScharf === id) { dtLoeschScharf = null; if (activeTab === "rising") render(); } }, 8000);
        return;
      }
      dtLoeschScharf = null;
      for (var i = 0; i < liste.length; i++) if (liste[i].id === id) { liste.splice(i, 1); break; }
      dtRisingSpeichern(); render();
    }
    main.querySelectorAll("[data-adel]").forEach(function (b) { b.onclick = function () { loeschen(A, b.dataset.adel); }; });
    main.querySelectorAll("[data-bdel]").forEach(function (b) { b.onclick = function () { loeschen(B, b.dataset.bdel); }; });
    function person(id) { return B.filter(function (x) { return x.id === id; })[0]; }
    main.querySelectorAll("[data-bstufe]").forEach(function (s) {
      s.onchange = function () { var p = person(s.dataset.bstufe); if (p) { p.stufe = s.value; dtRisingSpeichern(); render(); } };
    });
    main.querySelectorAll("[data-bnext]").forEach(function (f) {
      f.oninput = function () { var p = person(f.dataset.bnext); if (p) { p.naechster = f.value; dtRisingSpeichern(); } };
    });
    main.querySelectorAll("[data-bdatum]").forEach(function (f) {
      f.onchange = function () { var p = person(f.dataset.bdatum); if (p) { p.datum = f.value; dtRisingSpeichern(); } };
    });
  }
