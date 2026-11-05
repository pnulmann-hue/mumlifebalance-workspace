  /* =========================================================
     Fürs Team (05.11.2026) — zwei Nachrichten pro Woche an ihr doTERRA-Team
     Patricia: „es kommen täglich so viele nachrichten in der gruppe, dass ich und mein team
     die übersicht verloren haben was relevant ist … ich würde gerne meine teammitglieder
     enger begleiten … vielleicht zwei impulse rsp. aufgaben?“
     Montag eine Aufgabe, Donnerstag ein Impuls. Die Routine rise-to-lead legt sie in
     doterra-wissen/team-impulse (items) und schickt sie Patricia per Telegram. Verschickt
     wird nichts ans Team: sie liest, passt an, schickt selbst.
     Ihre Änderungen und „verschickt“ stehen in daten/rising-leaders (gehört ihr):
     impulse = { <id>: { text, verschickt } }
     ========================================================= */
  var tiImpulse = null, tiImpulsGeholt = false;

  // Nur dieses eine Dokument: Mein Tisch soll nicht die ganze Öl-Sammlung laden.
  function tiImpulsHolen() {
    if (tiImpulsGeholt) return;
    tiImpulsGeholt = true;
    tiImpulse = lsGet("dt-impulse", null);
    if (!db) return;
    db.doc("doterra-wissen/team-impulse").get().then(function (d) {
      if (!d.exists) return;
      tiImpulse = tief(d.data()) || null;
      lsSet("dt-impulse", tiImpulse);
      if (activeTab === "uebersicht" || activeTab === "rising") render();
    }).catch(function () {});
  }

  function tiImpulsStand(id) {
    var I = dtRising.impulse || (dtRising.impulse = {});
    return I[id] || (I[id] = {});
  }
  function tiImpulsListe() {
    tiImpulsHolen();
    return (tiImpulse && tiImpulse.items) ? tiImpulse.items.slice().sort(function (a, b) { return a.datum < b.datum ? 1 : -1; }) : [];
  }
  // Was gerade wartet: Tag erreicht, noch nicht verschickt, höchstens drei Tage alt.
  function tiImpulsOffen() {
    var heute = trHeute(), grenze = trVerschoben(heute, -3);
    return tiImpulsListe().filter(function (x) {
      return x.datum <= heute && x.datum >= grenze && !tiImpulsStand(x.id).verschickt;
    });
  }
  function tiImpulsText(x) {
    var s = tiImpulsStand(x.id);
    return s.text != null ? s.text : (x.text || "");
  }

  function tiImpulsKarte(x) {
    var s = tiImpulsStand(x.id);
    return '<div class="tm-karte' + (s.verschickt ? " raus" : "") + '" id="impuls-' + esc(x.id) + '">' +
      '<div class="tm-kopf"><span class="tm-art">' + (x.art === "aufgabe" ? "Aufgabe" : "Impuls") + '</span>' +
      '<b>' + esc(x.titel || "") + '</b><span class="note">' + esc(dtDatum(x.datum)) + '</span></div>' +
      (x.fuerDich ? '<p class="note tm-dich">Für dich: ' + esc(x.fuerDich) + '</p>' : "") +
      (s.verschickt
        ? '<details class="tm-text"><summary>Verschickt am ' + esc(dtDatum(s.verschickt)) + '</summary><p class="tm-alt">' + esc(tiImpulsText(x)) + '</p></details>'
        : '<textarea data-tmtext="' + esc(x.id) + '" rows="9">' + esc(tiImpulsText(x)) + '</textarea>' +
          '<div class="dt-knoepfe"><button class="btn primary" type="button" data-tmkopie="' + esc(x.id) + '">Kopieren</button>' +
          '<button class="btn" type="button" data-tmraus="' + esc(x.id) + '">Hab ich verschickt</button></div>') +
      '</div>';
  }

  function tiImpulsHtml() {
    var L = tiImpulsListe();
    if (!L.length) return "";
    var offen = tiImpulsOffen();
    var heute = trHeute();
    var aktuell = L.filter(function (x) { return x.datum >= trVerschoben(heute, -3) && x.datum <= heute; });
    var aelter = L.filter(function (x) { return aktuell.indexOf(x) < 0 && x.datum <= heute; });
    var h = '<section class="panel tm"><div class="tm-titel"><h2>Fürs Team</h2>' +
      '<span class="note">' + (offen.length ? "liegt bereit zum Schicken" : "alles verschickt") + '</span></div>' +
      '<p class="note">Montag eine Aufgabe, Donnerstag ein Impuls, aus allem, was in den Rise-to-Lead-Gruppen wichtig war. Du schickst sie selbst.</p>' +
      aktuell.map(tiImpulsKarte).join("");
    if (aelter.length) {
      h += '<details class="tm-aelter"><summary>' + aelter.length + ' frühere</summary>' + aelter.slice(0, 12).map(tiImpulsKarte).join("") + '</details>';
    }
    return h + '</section>';
  }

  function tiImpulsBinden(main) {
    function finde(id) { return tiImpulsListe().filter(function (x) { return x.id === id; })[0]; }
    main.querySelectorAll("[data-tmtext]").forEach(function (f) {
      f.oninput = function () { tiImpulsStand(f.dataset.tmtext).text = f.value; dtRisingSpeichern(); };
    });
    main.querySelectorAll("[data-tmkopie]").forEach(function (b) {
      b.onclick = function () { var x = finde(b.dataset.tmkopie); if (x) dtKopieren(tiImpulsText(x), b); };
    });
    main.querySelectorAll("[data-tmraus]").forEach(function (b) {
      b.onclick = function () {
        tiImpulsStand(b.dataset.tmraus).verschickt = trHeute();
        dtRisingSpeichern(); render();
        toast("Vermerkt. Der nächste kommt von selbst.");
      };
    });
  }
