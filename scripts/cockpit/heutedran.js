  /* =========================================================
     Heute dran (03.11.2026) — eine Liste ganz oben auf Mein Tisch
     Patricia: „wie können wir gewährleisten, dass mir die dinge aufploppen? …
     irgendwie habe ich das gefühl ich könnte die dinge übersehen“.
     Vorher stand jeder Hinweis als kleine Zahl in seinem eigenen Reiter.
     Jetzt: eine Liste, das Dringendste oben, jeder Punkt führt dorthin, wo er
     erledigt wird, und verschwindet danach. Fragen werden direkt hier beantwortet
     (Tagesfokus, Learning, Blick auf Morgen, Fokus der Woche) statt in einem Formular.
     Quellen: termine · aufgaben (nur Business, Mein Tisch sehen auch Kundinnen) ·
     wochenbogen-notizen · rising-leaders (Tagesrunde, Team-Funke, Monatsabschluss) ·
     Beiträge, die auf sie warten · daten/tagebuch (neu, gehört Patricia).
     🚨 Dieselbe Logik steckt in scripts/cockpit/heute-dran.py (Telegram am Morgen).
        Wer hier eine Quelle ändert, zieht sie dort nach.
     ========================================================= */
  var hdTagebuch = { tage: {}, updatedAt: "" };   // daten/tagebuch — gehoert PATRICIA
  var hdGeholt = false;

  function hdTagebuchHolen() {
    if (hdGeholt) return;
    hdGeholt = true;
    hdTagebuch = lsGet("tagebuch", null) || { tage: {}, updatedAt: "" };
    if (!hdTagebuch.tage) hdTagebuch.tage = {};
    if (!db) return;
    db.doc("daten/tagebuch").get().then(function (snap) {
      var d = tief(snap && snap.exists ? snap.data() : null);
      if (!d || !d.tage) return;
      // Neuerer Stand gewinnt — fehlt updatedAt, bleibt der lokale (Lehre vom 24.09.).
      if (!hdTagebuch.updatedAt || (d.updatedAt && d.updatedAt > hdTagebuch.updatedAt)) {
        hdTagebuch = d;
        lsSet("tagebuch", hdTagebuch);
        if (activeTab === "uebersicht") render();
      }
    }).catch(function () {});
  }

  function hdSpeichern() {
    hdTagebuch.updatedAt = new Date().toISOString();
    lsSet("tagebuch", hdTagebuch);
    clearTimeout(saveTimers.tagebuch);
    saveTimers.tagebuch = setTimeout(function () {
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/tagebuch").set(hdTagebuch)
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function hdTag(iso) {
    return hdTagebuch.tage[iso] || (hdTagebuch.tage[iso] = {});
  }

  // ISO-Kalenderwoche im Format der Wochenbögen: „2026-KW45“.
  function hdKw(iso) {
    var d = new Date(iso + "T12:00:00");
    var tag = (d.getDay() + 6) % 7;            // Montag = 0
    d.setDate(d.getDate() - tag + 3);          // Donnerstag derselben Woche
    var jahr = d.getFullYear();
    var erster = new Date(jahr, 0, 4, 12);
    var kw = 1 + Math.round(((d - erster) / 86400000 - 3 + ((erster.getDay() + 6) % 7)) / 7);
    return jahr + "-KW" + (kw < 10 ? "0" + kw : kw);
  }

  // Die Punkte. Jeder: { art, titel, klein, gehe, frage:[{k,l,p,ziel}], dringend }
  function hdPunkte(heute, beitraege) {
    var jetzt = new Date();
    var stunde = jetzt.getHours();
    var wochentag = jetzt.getDay();
    var P = [];

    // 1 · Termine heute — nur zum Sehen, sie verschwinden nicht durch Abhaken.
    var tm = ((termine && termine.items) || []).filter(function (t) { return t.datum === heute; })
      .sort(function (a, b) { return (a.zeit || "99") < (b.zeit || "99") ? -1 : 1; });
    if (tm.length) {
      P.push({ art: "termin", titel: tm.length === 1 ? "Ein Termin heute" : tm.length + " Termine heute",
               klein: tm.map(function (t) { return (t.zeit ? t.zeit + " " : "") + (t.titel || ""); }).join(" · ") });
    }

    // 2 · Tagesplaner — morgens der Fokus, abends Learning und Blick auf Morgen.
    var T = hdTag(heute);
    if ((T.fokus || "").trim() && T.fokus === T.ausGestern && stunde < 17) {
      P.push({ art: "info", titel: "Dein Fokus heute", klein: T.fokus });
    } else if (stunde < 15 && !(T.fokus || "").trim()) {
      P.push({ art: "frage", titel: "Was ist heute dein Fokus?", dringend: true,
               frage: [{ k: "fokus", ziel: "tag", p: "Ein Satz. Woran merkst du heute Abend, dass der Tag gut war?" }] });
    }
    if (stunde >= 17 && (!(T.learning || "").trim() || !(T.morgen || "").trim())) {
      P.push({ art: "frage", titel: "Dein Tag in zwei Sätzen",
               klein: T.fokus ? "Heute war dein Fokus: " + T.fokus : "",
               frage: [{ k: "learning", ziel: "tag", l: "Was hast du heute gelernt oder geschafft?", p: "Daraus wird am Sonntag dein Wochenrückblick." },
                       { k: "morgen", ziel: "tag", l: "Was ist morgen das Wichtigste?", p: "Das steht dir morgen früh als Fokus da." }] });
    }

    // 3 · Wochenfragen — Sonntag ab 15 Uhr für die neue Woche, sonst für die laufende.
    var wIso = heute;
    if (wochentag === 0 && stunde >= 15) wIso = trVerschoben(heute, 1);
    var kw = hdKw(wIso);
    var WN = wochenbogenNotizen[kw] || {};
    if (!(WN.fokus || "").trim() && (wochentag !== 0 || stunde >= 15)) {
      P.push({ art: "frage", titel: "Fokus der Woche (KW " + Number(kw.slice(7)) + ")",
               klein: wochentag >= 3 ? "Steht seit Montag offen." : "Ein Satz für die ganze Woche.",
               dringend: wochentag === 0 || wochentag === 1,
               frage: [{ k: "fokus", ziel: "woche", kw: kw, p: "Woran merkst du am Sonntag, dass die Woche gut war?" }] });
    }

    // 4 · doTERRA: Tagesrunde, Team-Funke, Monatsabschluss.
    var tr = trHeuteZahl();
    if (tr < 3) {
      P.push({ art: "doterra", titel: "doTERRA-Tagesrunde " + tr + "/3",
               klein: tr === 0 ? "Ein Business-Gedanke, eine neue Person, eine Kundin." : "Noch " + (3 - tr) + (3 - tr === 1 ? " Schritt" : " Schritte") + ".",
               gehe: "rising" });
    }
    if (tfFaellig()) P.push({ art: "doterra", titel: "Team-Funke für diese Woche", klein: "Die Wochennachricht an dein Team ist noch nicht raus.", gehe: "rising" });
    if (Number(heute.slice(8, 10)) >= 24) {
      var A = (dtRising.abschluss || {})[heute.slice(0, 7)] || {};
      var fertigAb = TR_ABSCHLUSS.filter(function (p) { return A[p.id]; }).length;
      if (fertigAb < TR_ABSCHLUSS.length) {
        P.push({ art: "doterra", titel: "Monatsabschluss " + fertigAb + "/" + TR_ABSCHLUSS.length,
                 klein: "Am Monatsersten fällt das Volumen auf null.", gehe: "rising", dringend: true });
      }
    }

    // 5 · Beiträge, die heute oder morgen auf sie warten.
    var morgen = trVerschoben(heute, 1);
    var warten = [];
    beitraege.forEach(function (b) {
      var d = datumVon(b);
      if (!d || d > morgen || d < heute || istDraussen(b)) return;
      if ((wasFehlt(b) || []).some(function (f) { return f.wer === "du"; })) warten.push(b);
    });
    if (warten.length) {
      P.push({ art: "beitrag", titel: warten.length === 1 ? "Ein Beitrag wartet auf dich" : warten.length + " Beiträge warten auf dich",
               klein: warten.slice(0, 3).map(function (b) { return (datumVon(b) === heute ? "heute: " : "morgen: ") + (b.titel || b.format); }).join(" · "),
               gehe: "woche", dringend: warten.some(function (b) { return datumVon(b) === heute; }) });
    }

    // 6 · Aufgaben (nur Business): heute fällig einzeln, überfällige als ein Punkt.
    var af = ((aufgaben && aufgaben.items) || []).filter(function (a) { return !a.erledigt && tiBereich(a) === "Business"; });
    af.filter(function (a) { return a.datum === heute; }).slice(0, 3).forEach(function (a) {
      P.push({ art: "aufgabe", titel: a.aufgabe || "Aufgabe", klein: "heute fällig", aufgabe: a.id });
    });
    var ueber = af.filter(function (a) { return a.datum && a.datum < heute; });
    if (ueber.length) {
      P.push({ art: "aufgabe", titel: ueber.length + (ueber.length === 1 ? " Aufgabe ist" : " Aufgaben sind") + " überfällig",
               klein: "Neu terminieren oder streichen, sonst gehen die wichtigen darin unter.", gehe: "aufgaben" });
    }

    // Dringendes nach oben, sonst bleibt die Reihenfolge oben.
    return P.map(function (p, i) { p.i = i; return p; })
      .sort(function (a, b) { return (b.dringend ? 1 : 0) - (a.dringend ? 1 : 0) || a.i - b.i; });
  }

  function hdZahl(heute, beitraege) {
    return hdPunkte(heute, beitraege).filter(function (p) { return p.art !== "termin" && p.art !== "info"; }).length;
  }

  var HD_ICON = { info: "🎯", termin: "📅", frage: "✍️", doterra: "🌿", beitrag: "📸", aufgabe: "☑️" };

  function hdHtml(heute, beitraege) {
    hdTagebuchHolen();
    var P = hdPunkte(heute, beitraege);
    var offen = P.filter(function (p) { return p.art !== "termin" && p.art !== "info"; }).length;
    var h = '<section class="ti-karte hd' + (offen ? " offen" : "") + '" id="hd">' +
      '<div class="hd-kopf"><span class="ti-chip' + (offen ? " o" : "") + '">Heute dran</span>' +
      '<span class="hd-zahl">' + (offen ? offen + (offen === 1 ? " Punkt offen" : " Punkte offen") : "alles erledigt") + '</span></div>';
    P.forEach(function (p) { h += hdPunktHtml(p, heute); });
    if (!offen) h += '<p class="hd-leer">Für heute ist alles erledigt. Was jetzt noch kommt, ist freiwillig.</p>';
    return h + '</section>';
  }

  function hdPunktHtml(p, heute) {
    var h = '<div class="hd-punkt' + (p.dringend ? " dringend" : "") + ' hd-' + p.art + '">' +
      '<span class="hd-icon" aria-hidden="true">' + (HD_ICON[p.art] || "•") + '</span><div class="hd-text">' +
      '<b>' + esc(p.titel) + '</b>' + (p.klein ? '<span>' + esc(p.klein) + '</span>' : "");
    (p.frage || []).forEach(function (f) {
      var wert = f.ziel === "woche" ? ((wochenbogenNotizen[f.kw] || {})[f.k] || "") : (hdTag(heute)[f.k] || "");
      h += (f.l ? '<label class="hd-l">' + esc(f.l) + '</label>' : "") +
        '<textarea class="ti-feld hd-feld" rows="1" data-hdk="' + esc(f.k) + '" data-hdziel="' + esc(f.ziel) + '"' +
        (f.kw ? ' data-hdkw="' + esc(f.kw) + '"' : "") + ' placeholder="' + esc(f.p || "") + '">' + esc(wert) + '</textarea>';
    });
    if (p.frage) h += '<button class="ti-btn hd-fertig" type="button" data-hdfertig="1">Fertig</button>';
    h += '</div>';
    if (p.gehe) h += '<button class="ti-btn hd-los" type="button" data-gehe="' + esc(p.gehe) + '">Hin</button>';
    if (p.aufgabe) h += '<button class="ti-btn hd-los" type="button" data-hdaf="' + esc(p.aufgabe) + '">Erledigt</button>';
    return h + '</div>';
  }

  function hdBinden(el, heute) {
    Array.prototype.forEach.call(el.querySelectorAll("[data-hdk]"), function (f) {
      f.oninput = function () {
        var k = f.getAttribute("data-hdk");
        if (f.getAttribute("data-hdziel") === "woche") {
          var kw = f.getAttribute("data-hdkw");
          if (!wochenbogenNotizen[kw]) wochenbogenNotizen[kw] = {};
          wochenbogenNotizen[kw][k] = f.value;
          wbSpeichern();
        } else {
          hdTag(heute)[k] = f.value;
          // „Blick auf Morgen“ wird morgen früh der Tagesfokus — nie einen getippten überschreiben.
          if (k === "morgen") {
            var m = hdTag(trVerschoben(heute, 1));
            if (!m.fokus || m.fokus === m.ausGestern) { m.fokus = f.value; m.ausGestern = f.value; }
          }
          hdSpeichern();
        }
      };
    });
    // Fertig = neu zeichnen, dann verschwindet der beantwortete Punkt.
    Array.prototype.forEach.call(el.querySelectorAll("[data-hdfertig]"), function (b) {
      b.onclick = function () { render(); };
    });
    Array.prototype.forEach.call(el.querySelectorAll("[data-hdaf]"), function (b) {
      b.onclick = function () {
        var id = b.getAttribute("data-hdaf");
        ((aufgaben && aufgaben.items) || []).forEach(function (a) {
          if (a.id === id) { a.erledigt = true; a.erledigt_am = heute; }
        });
        afSpeichern(); render(); toast("Abgehakt ✓");
      };
    });
  }
