  /* ======================================================================
     Reiter "Testreels" — Instagram -> Testreels
     (seit 31.10.2026, patch-testreels.py)

     Patricia: „die idee ist, dass ich für jeden tag die fixfertigen testreels
     nach datum sehe, die ich zum testen posten kann. die besten nehme ich
     selber in den feed. paralell machen wir aber auch beiträge die so oder so
     gepostet werden.“ Ein Testreel zeigt Instagram nur Leuten, die ihr noch
     nicht folgen. Zwei Hooks, gleiche Szene, gleicher Tag — sonst deuten wir
     Zufall: dasselbe Reel lief einmal mit 1'948 und einmal mit 277 Konten.

     Ein Testreel ist ein normales Reel (Sammlung "reels") mit
       trial: true · testVon: <Kennung des Partners, gegen den es antritt> ·
       testStand: offen | gepostet | ausgewertet · testGepostetAm ·
       testReichweite · testKommentare · testNotiz · testGewinner · testInFeed
     🚨 Diese Felder stehen auch in der festen Feldliste von saveReel und
     beim Lesen — sonst waeren sie nach dem naechsten Speichern weg.
     🚨 Testreels stehen NICHT in alleBeitraege(): sie belegen keinen
     Feed-Platz in der Woche, gehen nicht in Freigeben und nicht in den
     Content-Kalender. Die Feed-Beitraege laufen daneben weiter.
     Alte Testreels (KW42) tragen nur „trial“ in der Kennung oder
     „TRIAL REEL“ im Hinweis; die werden ueber istTestreel() mitgefunden.
     ====================================================================== */
  var trZweiterKlick = {};
  var TR_TAG = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];

  function istTestreel(r) {
    if (!r) return false;
    return !!(r.trial || /(^|-)trial(-|$)/.test(r.id || "") ||
              /TRIAL REEL/i.test(r.hinweis || ""));
  }

  function trStand(r) {
    if (r.testStand) return r.testStand;
    // Alte Testreels: wer sie in der App eingeplant hat, hat sie gepostet.
    var s = (r.blotato || {}).status || "";
    if (s === "selber-posten" || s === "gepostet-von-hand") return "gepostet";
    return "offen";
  }

  function trWoerter(t) {
    return String(t || "").replace(/[„“"«»]/g, "").trim().split(/\s+/).filter(Boolean).length;
  }

  function trReelNach(id) {
    for (var i = 0; i < state.reels.length; i++) if (state.reels[i].id === id) return state.reels[i];
    return null;
  }

  function trTageSeit(iso) {
    if (!iso) return null;
    var a = new Date(iso + "T12:00:00"), b = new Date(todayISO() + "T12:00:00");
    if (isNaN(a) || isNaN(b)) return null;
    return Math.round((b - a) / 86400000);
  }

  function trTagName(iso) {
    var d = new Date(iso + "T12:00:00");
    if (isNaN(d)) return iso;
    var vor = iso === todayISO() ? "Heute · " : "";
    return vor + TR_TAG[d.getDay()] + " " + d.getDate() + "." + (d.getMonth() + 1) + ".";
  }

  // Ein Paar bleibt zusammen: Partner A und B stehen nebeneinander.
  function trPaar(r) { return r.testVon || r.id; }

  /* Besser ist, wer mehr Kommentare holt — Reichweite erst danach.
     Ein Reel mit 1'900 Konten und null Kommentaren ist kein Gewinner. */
  function trBesser(a, b) {
    var ka = a.testKommentare || 0, kb = b.testKommentare || 0;
    if (ka !== kb) return kb - ka;
    return (b.testReichweite || 0) - (a.testReichweite || 0);
  }

  function renderTestreels(main) {
    var tests = state.reels.filter(function (r) { return istTestreel(r) && !r.abgelehnt; });
    var offen = [], laeuft = [], fertig = [];
    tests.forEach(function (r) {
      var s = trStand(r);
      (s === "gepostet" ? laeuft : s === "ausgewertet" ? fertig : offen).push(r);
    });
    var mitTag = {}, ohne = [];
    offen.forEach(function (r) { if (r.datum) (mitTag[r.datum] = mitTag[r.datum] || []).push(r); else ohne.push(r); });
    var tage = Object.keys(mitTag).sort();
    var bereit = offen.filter(function (r) { return !!r.videourl; }).length;
    laeuft.sort(function (a, b) { return (a.testGepostetAm || "") < (b.testGepostetAm || "") ? -1 : 1; });

    main.innerHTML =
      '<div class="page-head"><div><h1>Testreels</h1>' +
      '<p>Je Tag die Testreels, die du posten kannst. Instagram zeigt sie nur Leuten, die dir noch nicht ' +
      'folgen. Beim Posten in der App den Schalter <b>Testreel</b> einschalten. Die besten nimmst du danach ' +
      'selbst in den Feed, deine normalen Beiträge laufen daneben weiter.</p></div></div>' +
      '<div class="tr-stand"><span><b>' + offen.length + '</b> zum Posten</span><span><b>' + bereit +
      '</b> davon fertig</span><span><b>' + laeuft.length + '</b> laufen</span><span><b>' + fertig.length +
      '</b> ausgewertet</span></div>' +
      (tage.length ? tage.map(function (t) { return trTag(t, mitTag[t]); }).join("")
                   : '<div class="panel"><div class="empty">Für die nächsten Tage ist noch kein Testreel eingeplant.</div></div>') +
      (ohne.length ? trTag("", ohne) : "") +
      trGruppe("Läuft", "Nach drei Tagen die Zahlen aus der App eintragen: Konten erreicht und Kommentare.", laeuft, "gepostet") +
      trAusgewertet(fertig) +
      '<details class="panel tr-neu"><summary>Neues Testreel: zweiter Hook zu einem Reel</summary>' +
      '<label class="field"><span>Gegen welches Reel tritt es an?</span><select id="trbasis"></select></label>' +
      '<label class="field"><span>Der andere Hook (10 bis 14 Wörter, ohne Lösung, ohne Werkzeug)</span>' +
      '<textarea id="trhook" rows="2"></textarea></label>' +
      '<div class="tr-neufuss"><span class="note" id="trzahl"></span>' +
      '<button class="btn primary" id="tranlegen">Testreel anlegen</button></div></details>';

    var sel = main.querySelector("#trbasis");
    var basis = state.reels.filter(function (r) { return !r.abgelehnt; })
      .sort(function (a, b) { return (a.datum || "9") < (b.datum || "9") ? -1 : 1; });
    sel.innerHTML = '<option value="">– Reel wählen –</option>' + basis.map(function (r) {
      return '<option value="' + esc(r.id) + '">' + (istTestreel(r) ? "🧪 " : "") +
        esc((r.datum ? r.datum.slice(8, 10) + "." + r.datum.slice(5, 7) + ". · " : "ohne Datum · ") + (r.name || r.hook || r.id)) + '</option>';
    }).join("");
    var hookFeld = main.querySelector("#trhook"), zahl = main.querySelector("#trzahl");
    hookFeld.addEventListener("input", function () {
      var n = trWoerter(hookFeld.value);
      zahl.textContent = n ? n + " Wörter" + (n < 10 || n > 14 ? " · Bild-Hook sollte 10 bis 14 haben" : "") : "";
      zahl.className = "note" + (n && (n < 10 || n > 14) ? " tr-warn" : "");
    });
    main.querySelector("#tranlegen").onclick = function () {
      var b = trReelNach(sel.value), hook = hookFeld.value.trim();
      if (!b) { toast("Zuerst das Reel wählen."); return; }
      if (!hook) { toast("Den anderen Hook eintragen."); return; }
      if (hook === (b.hook || "").trim()) { toast("Das ist derselbe Hook wie im Reel."); return; }
      var neu = JSON.parse(JSON.stringify(b));
      neu.id = b.id + "-test-" + Date.now().toString(36);
      neu.name = "🧪 Test · " + String(b.name || "Reel").replace(/^🧪 Test · /, "");
      neu.hook = hook; neu.coverhook = hook; neu.unter = "";
      // Ein Paar postet am selben Tag, sonst vergleicht man zwei Tage statt zwei Hooks.
      neu.datum = istTestreel(b) ? (b.datum || "") : "";
      neu.textfrei = false; neu.blotato = null; neu.videourl = ""; neu.videodatei = "";
      neu.kommentar = ""; neu.kommentarStand = ""; neu.kommentarErledigt = ""; neu.kommentarAntwort = "";
      neu.trial = true; neu.testVon = b.id; neu.testStand = "offen";
      neu.testGepostetAm = ""; neu.testReichweite = null; neu.testKommentare = null;
      neu.testNotiz = ""; neu.testGewinner = false; neu.testInFeed = false;
      neu.hinweis = "🧪 TRIAL REEL — beim Posten in der App „Testreel“ einschalten. Tritt gegen „" +
                    (b.name || b.id) + "“ an, mit derselben Szene. 🎬 Video baut Claude.";
      state.reels.unshift(neu);
      saveReel(neu);
      toast("Testreel angelegt.");
      render();
    };

    trKnoepfeVerdrahten(main);
  }

  function trTag(iso, liste) {
    liste.sort(function (a, b) {
      var pa = trPaar(a), pb = trPaar(b);
      if (pa !== pb) return pa < pb ? -1 : 1;
      return a.testVon ? 1 : -1;
    });
    var fertig = liste.filter(function (r) { return !!r.videourl; }).length;
    var vorbei = iso && iso < todayISO();
    return '<h2 class="tr-gtitel' + (iso === todayISO() ? ' tr-heute' : '') + '">' +
      esc(iso ? trTagName(iso) : "Noch ohne Tag") +
      ' <span class="tr-zahl">' + fertig + ' von ' + liste.length + ' fertig</span>' +
      (vorbei ? ' <span class="chip orange">Tag ist vorbei</span>' : '') + '</h2>' +
      '<div class="tr-liste">' + liste.map(function (r) { return trKarte(r, "offen"); }).join("") + '</div>';
  }

  function trGruppe(titel, satz, liste, stand) {
    return '<h2 class="tr-gtitel">' + esc(titel) + ' <span class="tr-zahl">' + liste.length + '</span></h2>' +
      '<p class="note tr-gsatz">' + esc(satz) + '</p>' +
      (liste.length ? '<div class="tr-liste">' + liste.map(function (r) { return trKarte(r, stand); }).join("") + '</div>'
                    : '<div class="panel"><div class="empty">Gerade keins.</div></div>');
  }

  function trAusgewertet(liste) {
    var kopf = '<h2 class="tr-gtitel">Ausgewertet <span class="tr-zahl">' + liste.length + '</span></h2>' +
      '<p class="note tr-gsatz">Je Paar nebeneinander. Besser ist, was mehr Kommentare geholt hat, bei Gleichstand ' +
      'die Reichweite. Ein einzelner Test ist ein Hinweis, noch keine Regel.</p>';
    if (!liste.length) return kopf + '<div class="panel"><div class="empty">Noch nichts ausgewertet.</div></div>';
    var nach = {};
    liste.forEach(function (r) { (nach[trPaar(r)] = nach[trPaar(r)] || []).push(r); });
    return kopf + Object.keys(nach).map(function (k) {
      var reihe = nach[k].sort(trBesser), b = trReelNach(k);
      var feed = b && !istTestreel(b);
      return '<div class="panel tr-vergleich"><div class="tr-vkopf">' +
        (feed ? 'Feed-Beitrag: <b>' + esc(b.name || b.id) + '</b><div class="tr-vhook">Hook dort: „' + esc(b.hook || "") + '“</div>'
              : '<b>' + esc(reihe.length > 1 ? "Testpaar" : "Einzeltest") + '</b>') + '</div>' +
        reihe.map(function (r, i) { return trKarte(r, "ausgewertet", i === 0 && reihe.length > 1); }).join("") + '</div>';
    }).join("");
  }

  // Prüfvermerk der Hook-Sperre (scripts/hooks/hook-sperre.py, seit 01.11.2026):
  // ein zweiter, unabhängiger Blick beantwortet je Hook die Prüffragen.
  var TR_FRAGEN = {
    schmerz: "Trifft einen Schmerz", gedanke_gelesen: "„Wieso weiss die, was ich denke?“",
    kuechentisch: "So sagt man es einer Freundin", bezug_der_zeilen: "Bezug der Satzteile stimmt",
    loesung_draussen: "Lösung bleibt draussen", in_drei_sekunden_klar: "In drei Sekunden klar",
    mikro_szene: "Konkreter Moment (Mikro)", gegner_gestaendnis_oder_zitat: "Gegner, Geständnis oder Zitat",
    nische_network_mama: "Passt zur Network-Mama", passt_zur_rolle: "Passt zur Rolle im Garten"
  };
  function trPruefung(r) {
    var p = r.pruefung;
    if (!p) return '<div class="note tr-warn">Hook nicht geprüft</div>';
    var zeilen = Object.keys(TR_FRAGEN).map(function (k) {
      var a = (p.antworten || {})[k];
      if (!a) return "";
      return '<li class="' + (a.ja ? "tr-ja" : "tr-nein") + '"><b>' + (a.ja ? "✓ " : "✗ ") + esc(TR_FRAGEN[k]) +
        '</b> · ' + esc(a.warum || "") + '</li>';
    }).join("");
    return '<details class="tr-cap"><summary>' + (p.bestanden ? "✓ Hook geprüft" : "✗ Hook durchgefallen") +
      '</summary><ul class="tr-pruef">' + zeilen + '</ul></details>';
  }

  function trKarte(r, stand, vorne) {
    var b = r.testVon ? trReelNach(r.testVon) : null;
    var feedBasis = b && !istTestreel(b);
    var n = trWoerter(r.hook);
    var tage = trTageSeit(r.testGepostetAm);
    var h = '<div class="tr-karte' + (vorne ? ' tr-vorne' : '') + (r.videourl ? ' tr-bereit' : '') + '" data-id="' + esc(r.id) + '">' +
      '<div class="tr-kname">' + esc(r.name || r.id) +
      (stand === "offen" ? (r.videourl ? ' <span class="chip">fertig</span>' : ' <span class="chip orange">Video fehlt' +
        (r.videoart === "broll" ? ' · baut Claude' : '') + '</span>') : '') +
      (vorne ? ' <span class="chip">mehr Kommentare</span>' : '') +
      (r.testGewinner ? ' <span class="chip orange">in den Beitrag übernommen</span>' : '') +
      (r.testInFeed ? ' <span class="chip">im Feed</span>' : '') + '</div>' +
      (r.videourl ? '<video class="tr-video" src="' + esc(r.videourl) + '" controls playsinline preload="metadata"></video>' : '') +
      '<div class="tr-hook">' + esc(r.hook || "– noch kein Hook –") + '</div>' +
      '<div class="note">' + n + ' Wörter' + (b ? ' · tritt an gegen „' + esc(b.name || b.id) + '“' : '') + '</div>' +
      trPruefung(r) +
      (r.caption ? '<details class="tr-cap"><summary>Caption lesen</summary><div class="tr-captext">' + esc(r.caption) + '</div></details>' : '') +
      '<div class="tr-knoepfe">' +
      (r.videourl ? '<button class="btn" data-tr="video">Video speichern</button>' : '') +
      '<button class="btn" data-tr="hook">Hook kopieren</button>' +
      (r.caption ? '<button class="btn" data-tr="caption">Caption kopieren</button>' : '') +
      (feedBasis ? '<button class="btn ghost" data-tr="beitrag">Feed-Beitrag öffnen</button>' : '') +
      '</div>';
    if (stand === "offen") {
      h += '<div class="tr-fuss"><label class="tr-datum">Tag <input type="date" data-trf="datum" value="' + esc(r.datum || "") + '"></label>' +
        '<button class="btn primary" data-tr="gepostet">Als Testreel gepostet</button></div>';
    } else if (stand === "gepostet") {
      h += '<div class="tr-fuss"><span class="note">' + (tage === null ? 'gepostet' : 'gepostet vor ' + tage + (tage === 1 ? ' Tag' : ' Tagen')) +
        (tage !== null && tage < 3 ? ' · Zahlen erst nach drei Tagen eintragen' : '') + '</span></div>' +
        '<div class="tr-zahlen">' +
        '<label class="field"><span>Konten erreicht</span><input type="number" min="0" data-trf="testReichweite" value="' + (r.testReichweite == null ? "" : r.testReichweite) + '"></label>' +
        '<label class="field"><span>Kommentare</span><input type="number" min="0" data-trf="testKommentare" value="' + (r.testKommentare == null ? "" : r.testKommentare) + '"></label>' +
        '<label class="field tr-notiz"><span>Was ist dir aufgefallen?</span><input type="text" data-trf="testNotiz" value="' + esc(r.testNotiz || "") + '"></label>' +
        '</div><div class="tr-fuss"><button class="btn primary" data-tr="auswerten">Auswerten</button>' +
        '<button class="btn ghost" data-tr="zurueck">doch noch nicht gepostet</button></div>';
    } else {
      h += '<div class="tr-ergebnis"><b>' + (r.testReichweite == null ? "–" : Number(r.testReichweite).toLocaleString("de-CH")) + '</b> erreicht · <b>' +
        (r.testKommentare == null ? "–" : r.testKommentare) + '</b> Kommentare' + (r.testNotiz ? ' · ' + esc(r.testNotiz) : '') + '</div>' +
        '<div class="tr-fuss">' +
        '<button class="btn' + (r.testInFeed ? '' : ' primary') + '" data-tr="feed">' + (r.testInFeed ? 'doch nicht im Feed' : 'Hab ich in den Feed genommen') + '</button>' +
        (feedBasis && !r.testGewinner ? '<button class="btn" data-tr="uebernehmen">Hook in den Feed-Beitrag übernehmen</button>' : '') +
        '<button class="btn ghost" data-tr="zurueck">Zahlen ändern</button></div>';
    }
    return h + '</div>';
  }

  function trKnoepfeVerdrahten(main) {
    Array.prototype.forEach.call(main.querySelectorAll(".tr-karte"), function (karte) {
      var r = trReelNach(karte.getAttribute("data-id"));
      if (!r) return;
      Array.prototype.forEach.call(karte.querySelectorAll("[data-trf]"), function (feld) {
        // Gespeichert wird beim Verlassen des Feldes, nicht bei jedem Tippen —
        // sonst zeichnet die Seite neu und der Cursor springt raus.
        feld.addEventListener("change", function () {
          var k = feld.getAttribute("data-trf");
          if (feld.type === "number") r[k] = feld.value === "" ? null : Math.max(0, parseInt(feld.value, 10) || 0);
          else r[k] = feld.value;
          saveReel(r);
          if (k === "datum") render();
        });
      });
      Array.prototype.forEach.call(karte.querySelectorAll("[data-tr]"), function (knopf) {
        knopf.onclick = function () {
          var was = knopf.getAttribute("data-tr");
          /* Ein Download-Link wird im Viewer gesperrt (Patricia 02.11.: „ich kann die videos nicht runterladen“),
             deshalb über die downloads-Fähigkeit wie überall sonst im Cockpit. */
          if (was === "video") { dateiSpeichern(r.videourl, (r.id || "testreel") + ".mp4"); return; }
          if (was === "hook") { inDieZwischenablage(r.hook || "", knopf); return; }
          if (was === "caption") { inDieZwischenablage(r.caption || "", knopf); return; }
          if (was === "beitrag") { springeZuBeitrag(beitragNach(r.testVon)); return; }
          if (was === "gepostet") {
            r.testStand = "gepostet"; r.testGepostetAm = todayISO();
            saveReel(r); toast("Abgehakt. In drei Tagen die Zahlen eintragen."); render(); return;
          }
          if (was === "auswerten") {
            if (r.testReichweite == null || r.testKommentare == null) {
              toast("Zuerst Konten erreicht und Kommentare eintragen (auch 0)."); return;
            }
            r.testStand = "ausgewertet"; saveReel(r); render(); return;
          }
          if (was === "zurueck") {
            r.testStand = trStand(r) === "ausgewertet" ? "gepostet" : "offen";
            saveReel(r); render(); return;
          }
          if (was === "feed") {
            r.testInFeed = !r.testInFeed; saveReel(r); render(); return;
          }
          if (was === "uebernehmen") {
            // Zwei Klicks statt confirm() — ein Modal kann im Artifact-Rahmen
            // lautlos blockiert sein, und dann taete der Knopf scheinbar nichts.
            if (!trZweiterKlick[r.id]) {
              trZweiterKlick[r.id] = true;
              knopf.textContent = "Wirklich? Nochmal tippen";
              knopf.classList.add("primary");
              setTimeout(function () { delete trZweiterKlick[r.id]; if (knopf.isConnected) { knopf.textContent = "Hook in den Feed-Beitrag übernehmen"; knopf.classList.remove("primary"); } }, 8000);
              return;
            }
            delete trZweiterKlick[r.id];
            var b = trReelNach(r.testVon);
            if (!b) { toast("Den Beitrag gibt es nicht mehr."); return; }
            // Ein freigegebener Beitrag geht so raus, wie er freigegeben wurde.
            // Ihn hier still umzuschreiben, waere eine Aenderung ohne ihr Go.
            if (b.textfrei) { toast("Der Beitrag ist schon freigegeben. Erst dort die Freigabe zurücknehmen."); return; }
            // Der alte Hook bleibt als Notiz am Testreel stehen, damit man zurueck kann.
            r.testNotiz = (r.testNotiz ? r.testNotiz + " · " : "") + "alter Hook im Beitrag: „" + (b.hook || "") + "“";
            r.testGewinner = true;
            b.hook = r.hook; b.coverhook = r.hook;
            saveReel(b); saveReel(r);
            toast("Übernommen. Der Beitrag trägt jetzt den neuen Hook, das Video baut Claude neu.");
            render();
          }
        };
      });
    });
  }
