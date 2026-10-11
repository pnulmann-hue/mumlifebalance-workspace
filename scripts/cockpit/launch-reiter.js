  /* ======================================================================
     Reiter "Launch" — Produkte -> Launch   (seit 08.10.2026)

     Ein Funnel laeuft von selbst. Ein Launch ist der Start davor, und er hat
     eine feste Form: fuenf Phasen, zwei Tage Secret Offer, rund eine Woche
     aufwaermen. Die Aufgaben je Phase stehen hier fest verdrahtet, weil sie
     sich nicht je Launch aendern — was sich aendert, sind die Daten.

     Herkunft: die Methodik-Durchsicht vom 08.10.2026
     (outputs/marktrecherche/2026-10-08-julia-funnel-durchsicht.md, Befunde
     27-45, 68-76, 110-115). Nur die Mechanik, nie der Wortlaut, keine Namen.
     ====================================================================== */

  var LA_PHASEN = [
    { k: "vorbereitung", l: "Vorbereitung", farbe: "grau",
      was: "Alles bauen, was während des Launches fertig sein muss.",
      todo: [
        "Verkaufsseite oder Kasse steht, Kaufknopf ohne Scrollen sichtbar",
        "Order Bump, Upsell und Downsell hängen dran, jedes mit Streichpreis",
        "Die drei Preisstufen festgelegt: kleiner Schritt vom Secret zum Frühbucher, grosser zum regulären Preis",
        "Mail-Strecke geschrieben: Aufwärmen, Secret Offer, Verkauf",
        "Beiträge vorproduziert, einer davon zum Anpinnen",
        "Storys vorbereitet — je Käufertyp mindestens eine",
        "Highlight angelegt, farbig von den anderen unterscheidbar",
        "Ausgerechnet, wie viele Verkäufe das Ziel braucht"
      ] },
    { k: "aufwaermen", l: "Aufwärmen", farbe: "teal",
      was: "Rund eine Woche. Hier entsteht die Nachfrage — nicht in der Verkaufsphase.",
      todo: [
        "Jeden Tag eine Story zum Thema, aber nicht zum Produkt",
        "Noch nicht sagen, WAS kommt — nur, dass etwas kommt",
        "Making-of zeigen: über Unterlagen schwenken, unscharf",
        "Die Community mitentscheiden lassen: Titel, Gestaltung, Inhalte",
        "Zwei bis vier Aufwärm-Mails",
        "Frühwarnzeichen beobachten: kommen Fragen und „das kenne ich“-Antworten?"
      ] },
    { k: "secret", l: "Secret Offer", farbe: "orange",
      was: "Zwei Tage. Verdecktes Angebot zum tiefsten Preis — keine Preisstufe.",
      todo: [
        "Story: „es gibt etwas, tipp auf den Sticker“ — und NICHT sagen, um was es geht",
        "Wer tippt, bekommt den Link per Nachricht. Sonst nichts",
        "Mail: wer antwortet, bekommt den Link",
        "Der Preis ist hier am tiefsten — belohnt wird das Vertrauen",
        "Nach zwei Tagen ist Schluss, auch wenn es läuft"
      ] },
    { k: "verkauf", l: "Verkaufsphase", farbe: "navy",
      was: "Jetzt wird jeden Tag verkauft. Alles zeigt in dieselbe Richtung.",
      todo: [
        "In der Bio steht nur EIN Link — der zum Produkt",
        "Das Highlight ist vollgepackt: Inhalte, für wen, Stimmen, Link",
        "Jeden Tag teilen, wer schon dabei ist — echte Vornamen",
        "Der Launch-Beitrag ist angepinnt",
        "Jeden Tag Story plus die Mails der Strecke",
        "Einwände einzeln aufgreifen: Zeit, Geld, „schaffe ich das“",
        "Den Preisanstieg ankündigen, bevor er kommt",
        "Ein zweites Angebot höchstens als zweite Story am Abend"
      ] },
    { k: "nach", l: "Nachbereitung", farbe: "grau",
      was: "Der Teil, der immer liegenbleibt — und den nächsten Launch leichter macht.",
      todo: [
        "Preis erhöht oder die Kasse geschlossen",
        "Kundenstimmen eingeholt: jede anschreiben, mit Gegenleistung",
        "Eine eigene Mail an alle, die schon einmal gekauft haben",
        "Zahlen notiert: Eintragungen, Verkäufe je Stufe, was gezogen hat",
        "Entschieden, was als Nächstes beworben wird — keine Lücke"
      ] }
  ];

  /* Sechs Käufertypen, benannt nach dem, was sie brauchen. Keine fremden
     Vornamen auf der Seite — das Cockpit zeigt Patricia auch Kundinnen. */
  var LA_TYPEN = [
    { k: "inspiriert", l: "Die Inspirierte", ico: "✦",
      was: "Kauft, wenn sie mitgerissen wird. Braucht Bilder vom Leben danach, Energie, Vision — keine Zahlen." },
    { k: "beweis", l: "Die Beweis-Sucherin", ico: "✔",
      was: "Kauft, wenn sie sieht, dass es bei anderen funktioniert hat. Braucht Stimmen, Vorher-Nachher, Screenshots." },
    { k: "zahlen", l: "Die Zahlen-Person", ico: "#",
      was: "Kauft, wenn alles dasteht: Preis, Dauer, Inhalt, Raten. Springt ab, wenn der Preis fehlt." },
    { k: "gruppe", l: "Die Mitmacherin", ico: "••",
      was: "Kauft, wenn andere dabei sind. Braucht „wer ist schon drin“ und das Gefühl, nicht allein anzufangen." },
    { k: "zoegernd", l: "Die Zögernde", ico: "…",
      was: "Kauft am letzten Tag. Braucht Einwandbehandlung, eine echte Frist und die Erlaubnis, klein anzufangen." },
    { k: "schnell", l: "Die Entschlossene", ico: "→",
      was: "Kauft sofort, wenn der Weg klar ist. Braucht einen Link ohne Umwege — und keine zweite Erklärung." }
  ];

  /* Kalenderwoche nach ISO (Donnerstag-Regel) — dieselbe Zaehlung wie im
     Rest des Cockpits, damit die Haken zur Wochen-Vorschau passen. */
  function laKw(d) {
    var dt = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    var tag = (dt.getDay() + 6) % 7;
    dt.setDate(dt.getDate() - tag + 3);
    var ersterDo = new Date(dt.getFullYear(), 0, 4);
    var t2 = (ersterDo.getDay() + 6) % 7;
    ersterDo.setDate(ersterDo.getDate() - t2 + 3);
    return "kw" + (1 + Math.round((dt - ersterDo) / 604800000));
  }

  function laSpeichern() {
    launchD.updatedAt = new Date().toISOString();
    lsSet("launch", launchD);
    clearTimeout(saveTimers.launchD);
    saveTimers.launchD = setTimeout(function () {
      if (!db) return;
      db.doc("daten/launch").set({
        launches: launchD.launches, typen: launchD.typen,
        updatedAt: launchD.updatedAt
      }).catch(function () {});
    }, 700);
  }

  /* Welche Phase laeuft heute? */
  function laPhaseHeute(l, heute) {
    var p = l.phasen || {};
    var folge = [];
    LA_PHASEN.forEach(function (ph) { if (p[ph.k]) folge.push({ ph: ph, ab: p[ph.k] }); });
    folge.sort(function (a, b) { return a.ab < b.ab ? -1 : 1; });
    if (!folge.length) return null;
    if (p.ende && p.ende < heute) return { vorbei: true };
    var akt = null;
    for (var i = 0; i < folge.length; i++) { if (folge[i].ab <= heute) akt = folge[i]; }
    if (!akt) return { kuenftig: folge[0] };
    var naechste = null;
    for (var j = 0; j < folge.length; j++) { if (folge[j].ab > heute) { naechste = folge[j]; break; } }
    return { akt: akt, naechste: naechste };
  }

  function laTage(von, bis) {
    var a = new Date(von + "T00:00:00"), b = new Date(bis + "T00:00:00");
    return Math.round((b - a) / 86400000);
  }

  function renderLaunch(main) {
    var heute = todayISO();
    main.innerHTML =
      '<div class="page-head"><div><h1>Launch</h1>' +
      '<p>Ein Funnel l&auml;uft von selbst. Ein Launch ist der Start davor &mdash; ' +
      'f&uuml;nf Phasen, zwei Tage Secret Offer, rund eine Woche aufw&auml;rmen. ' +
      'Die Aufgaben je Phase stehen fest; was sich &auml;ndert, sind die Daten.</p></div>' +
      '<a class="btn" href="https://claude.ai/artifact/YViQzGgPqr3AiufeA35Ev3" ' +
      'target="_blank" rel="noopener">Funnel-Checkliste &rarr;</a></div>' +
      '<div id="la-jetzt"></div><div id="la-typen"></div>' +
      '<div id="la-plan"></div><div id="la-liste"></div>';
    laJetzt(main.querySelector("#la-jetzt"), heute);
    laTypen(main.querySelector("#la-typen"), heute);
    laPlan(main.querySelector("#la-plan"));
    laListe(main.querySelector("#la-liste"));
  }

  /* --- Block 1: Wo stehe ich ------------------------------------------- */
  function laJetzt(el, heute) {
    var laufend = null, kuenftig = null;
    launchD.launches.forEach(function (l) {
      var st = laPhaseHeute(l, heute);
      if (!st) return;
      if (st.akt && !laufend) { laufend = { l: l, st: st }; return; }
      if (st.kuenftig && !kuenftig) kuenftig = { l: l, st: st };
    });

    if (!laufend && !kuenftig) {
      el.innerHTML = '<div class="panel"><p class="la-hint">Noch kein Launch angelegt. ' +
        'Unten eintragen, dann steht hier, welche Phase heute l&auml;uft und was dran ist.</p></div>';
      return;
    }

    if (!laufend) {
      var tg = laTage(heute, kuenftig.st.kuenftig.ab);
      el.innerHTML = '<div class="panel"><h2>' + esc(kuenftig.l.name || "Ohne Namen") +
        '</h2><p class="la-hint">Startet in ' + tg + ' Tag' + (tg === 1 ? "" : "en") +
        ' mit der Phase <b>' + esc(kuenftig.st.kuenftig.ph.l) + '</b> (' +
        esc(kuenftig.st.kuenftig.ab) + ').</p></div>';
      return;
    }

    var l = laufend.l, st = laufend.st, ph = st.akt.ph;
    var h = '<div class="panel la-jetzt la-' + ph.farbe + '">' +
      '<div class="la-kopf"><div><span class="la-chip">' + esc(ph.l) + '</span>' +
      '<h2>' + esc(l.name || "Ohne Namen") + '</h2>' +
      (l.produkt ? '<p class="la-hint">' + esc(l.produkt) + '</p>' : "") +
      '</div><div class="la-rechts">';
    if (st.naechste) {
      var t = laTage(heute, st.naechste.ab);
      h += '<div class="la-zahl">' + t + '</div><div class="la-hint">Tag' +
        (t === 1 ? "" : "e") + ' bis <b>' + esc(st.naechste.ph.l) + '</b></div>';
    } else if ((l.phasen || {}).ende) {
      var te = laTage(heute, l.phasen.ende);
      h += '<div class="la-zahl">' + te + '</div><div class="la-hint">Tag' +
        (te === 1 ? "" : "e") + ' bis Schluss</div>';
    }
    h += '</div></div><p class="la-was">' + esc(ph.was) + '</p><ul class="la-todo">';
    ph.todo.forEach(function (x) { h += '<li>' + esc(x) + '</li>'; });
    h += '</ul>';

    /* Die Preisstufen mit der Gegenprobe auf die Abstaende: vom Secret Offer
       zum Fruehbucher klein, vom Fruehbucher zum regulaeren Preis gross. */
    var p = l.preise || {};
    if (p.secret && p.frueh && p.regulaer) {
      var s = +p.secret, f = +p.frueh, r = +p.regulaer;
      h += '<div class="la-preise"><span>Secret <b>' + s + '</b></span>' +
        '<span>Fr&uuml;hbucher <b>' + f + '</b></span>' +
        '<span>regul&auml;r <b>' + r + '</b></span></div>';
      if (isFinite(s) && isFinite(f) && isFinite(r) && (f - s) >= (r - f)) {
        h += '<div class="la-warn">Der Schritt vom Secret Offer zum Fr&uuml;hbucher ist ' +
          'gr&ouml;sser als der zum regul&auml;ren Preis. Dann lohnt sich das Vertrauen ' +
          'nicht &mdash; vorne klein, hinten gross.</div>';
      }
    }
    h += '</div>';
    el.innerHTML = h;
  }

  /* --- Block 2: Kaeufertypen diese Woche ------------------------------- */
  function laTypen(el, heute) {
    var kw = laKw(new Date(heute + "T12:00:00"));
    var hat = launchD.typen[kw] || [];
    var fehlt = LA_TYPEN.filter(function (t) { return hat.indexOf(t.k) < 0; });
    el.innerHTML = '<div class="panel"><h2>Wen hast du diese Woche angesprochen?</h2>' +
      '<p class="la-hint">Sechs Arten zu kaufen. &Uuml;ber eine Woche sollten alle sechs ' +
      'vorkommen &mdash; wer immer nur inspiriert, verkauft nie an die, die Zahlen brauchen. ' +
      'Antippen, wenn eine Story oder eine Mail diesen Typ bedient hat. (' + kw.toUpperCase() + ')</p>' +
      '<div class="la-typen" id="la-tg"></div>' +
      (fehlt.length
        ? '<div class="la-fehlt">Diese Woche fehlen noch: <b>' +
          fehlt.map(function (t) { return esc(t.l); }).join(", ") + '</b></div>'
        : '<div class="la-voll">Alle sechs bedient. Genau so.</div>') +
      '</div>';
    var g = el.querySelector("#la-tg");
    LA_TYPEN.forEach(function (t) {
      var an = hat.indexOf(t.k) >= 0;
      var k = document.createElement("button");
      k.className = "la-typ" + (an ? " an" : "");
      k.innerHTML = '<span class="la-ico">' + esc(t.ico) + '</span>' +
        '<span class="la-tl">' + esc(t.l) + '</span>' +
        '<span class="la-tw">' + esc(t.was) + '</span>';
      k.onclick = function () {
        var liste = (launchD.typen[kw] || []).slice();
        var i = liste.indexOf(t.k);
        if (i >= 0) liste.splice(i, 1); else liste.push(t.k);
        launchD.typen[kw] = liste;
        laSpeichern();
        laTypen(el, heute);
      };
      g.appendChild(k);
    });
  }

  /* --- Block 3: der Fahrplan ------------------------------------------- */
  function laPlan(el) {
    var h = '<div class="panel"><h2>Der Fahrplan</h2>' +
      '<p class="la-hint">Gilt f&uuml;r Produkte ab rund 99. Darunter wird nicht gelauncht, ' +
      'sondern gedroppt: drei bis f&uuml;nf Tage dar&uuml;ber sprechen, fertig. Eine ' +
      'Begleitung oder ein 1:1 wird gar nicht gelauncht, sondern immer wieder einmal ' +
      'erw&auml;hnt, bis die Pl&auml;tze voll sind.</p>';
    LA_PHASEN.forEach(function (ph) {
      h += '<details class="la-ph la-' + ph.farbe + '"><summary>' + esc(ph.l) +
        '<span class="la-hint">' + esc(ph.was) + '</span></summary><ul>';
      ph.todo.forEach(function (x) { h += '<li>' + esc(x) + '</li>'; });
      h += '</ul></details>';
    });
    el.innerHTML = h + '</div>';
  }

  /* --- Block 4: anlegen und bearbeiten -------------------------------- */
  function laListe(el) {
    el.innerHTML = '<div class="panel"><h2>Deine Launches</h2>' +
      '<p class="la-hint">Je Phase ein Startdatum, dazu der Schluss. Was leer bleibt, ' +
      '&uuml;berspringt die Anzeige.</p><div id="la-ll"></div>' +
      '<button class="btn" id="la-neu">+ Launch anlegen</button></div>';
    var box = el.querySelector("#la-ll");
    launchD.launches.forEach(function (l, idx) {
      var k = document.createElement("div");
      k.className = "la-zeile";
      var f = '<input class="la-i la-breit" data-f="name" value="' +
        esc(l.name || "") + '" placeholder="Name des Launches">' +
        '<input class="la-i la-breit" data-f="produkt" value="' +
        esc(l.produkt || "") + '" placeholder="Produkt">';
      LA_PHASEN.forEach(function (ph) {
        f += '<label class="la-dl">' + esc(ph.l) +
          '<input class="la-i" type="date" data-p="' + ph.k + '" value="' +
          esc((l.phasen || {})[ph.k] || "") + '"></label>';
      });
      f += '<label class="la-dl">Schluss<input class="la-i" type="date" data-p="ende" value="' +
        esc((l.phasen || {}).ende || "") + '"></label>';
      [["secret", "Secret"], ["frueh", "Fr&uuml;hbucher"], ["regulaer", "regul&auml;r"]]
        .forEach(function (pp) {
          f += '<label class="la-dl">' + pp[1] +
            '<input class="la-i la-eng" inputmode="numeric" data-pr="' + pp[0] + '" value="' +
            esc((l.preise || {})[pp[0]] || "") + '"></label>';
        });
      k.innerHTML = f + '<button class="btn la-del" data-del="1">l&ouml;schen</button>';
      Array.prototype.forEach.call(k.querySelectorAll("input"), function (inp) {
        inp.oninput = function () {
          if (inp.dataset.f) l[inp.dataset.f] = inp.value;
          else if (inp.dataset.p) { l.phasen = l.phasen || {}; l.phasen[inp.dataset.p] = inp.value; }
          else if (inp.dataset.pr) { l.preise = l.preise || {}; l.preise[inp.dataset.pr] = inp.value; }
          laSpeichern();
        };
        inp.onchange = function () { render(); };
      });
      /* Loeschen in zwei Klicks — kein confirm(), das kann im Artifact-Rahmen
         lautlos blockiert sein (Lehre vom 19.09.2026). */
      var dk = k.querySelector("[data-del]");
      dk.onclick = function () {
        if (dk.dataset.scharf) {
          launchD.launches.splice(idx, 1); laSpeichern(); render(); return;
        }
        dk.dataset.scharf = "1";
        dk.textContent = "wirklich?";
        setTimeout(function () {
          if (!dk.dataset.scharf) return;
          delete dk.dataset.scharf;
          dk.innerHTML = "l&ouml;schen";
        }, 8000);
      };
      box.appendChild(k);
    });
    el.querySelector("#la-neu").onclick = function () {
      launchD.launches.push({ id: uid("la"), name: "", produkt: "", phasen: {}, preise: {} });
      laSpeichern(); render();
    };
  }
