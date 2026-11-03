  /* =========================================================
     Tagesrunde (03.11.2026) — die drei täglichen Schritte aus Rise to Lead
     Patricia: „ich möchte bei doTERRA endlich in die umsetzung kommen“.
     Steht oben im Reiter Rising Leaders, auf Mein Tisch als Zähler „x/3“.
     Daten in daten/rising-leaders (gehört Patricia):
       tagesrunde[JJJJ-MM-TT] = { biz, person, kundin, pName, kName, extra }
       abschluss[JJJJ-MM]     = { <kennung>: true }
     Ab dem 24. schaltet die Karte auf den Monatsabschluss um.
     ========================================================= */
  var TR_ZIEL = 100;          // rund 100 Menschen fragen ergibt 2–4 Beraterinnen
  var TR_AB = "2026-10-01";   // Start des Programms, ab hier wird gezählt
  var TR_SCHRITTE = [
    { id: "biz", icon: "🔥", titel: "Übers Business gesprochen", wo: "Story oder Status",
      ideen: [
        "Erzähl einen Moment, den dir das Business möglich gemacht hat. Ein echter Tag, kein Prospekt.",
        "„Ich nehme diesen Monat drei Frauen mit, die neu starten möchten.“ Einfaches Foto, wer antwortet, bekommt die Infos per Nachricht.",
        "Erzähl, wie du deine Öle jeden Monat zum besten Preis bestellst und wie das Weiterempfehlen angefangen hat. Sag „empfehlen und teilen“, nicht „verkaufen“.",
        "Zeig einen Ausschnitt von heute, der ohne dein Business nicht ginge.",
        "Update-Story: wie viele Gespräche gerade laufen und dass noch ein Platz frei ist.",
        "Sag, wo du startest, wenn jemand mitmachen will: „Bei mir kannst du starten, schreib mir einfach.“"
      ] },
    { id: "person", icon: "💖", titel: "Eine Person aufs Business angesprochen", wo: "eine, die du dir im Team vorstellen kannst",
      ideen: [
        "Wer bestellt viel, fragt nach oder teilt die Öle von sich aus? Mit ihr anfangen.",
        "Du musst nicht das ganze Business erklären. Gib nur die Möglichkeit ins Feld und frag, ob sie mehr wissen will.",
        "Säe einen Samen: „Wenn du magst, zeig ich dir, wie du die Öle günstiger bekommst und sie später selbst weitergibst.“",
        "Ein Nein ist kein Urteil über dich. Die nächste Person.",
        "Schau auf Ergebnisse, nicht auf Potenzial: Wer setzt schon etwas um?"
      ] },
    { id: "kundin", icon: "🚀", titel: "Eine Kundin kontaktiert", wo: "aus deiner Organisation oder eine, die jeden Monat viel bestellt",
      ideen: [
        "Back Office → Quick Reports → Inaktivität (6 Monate). Eine Sprachnachricht: „Ich hab an dich gedacht und wollte hören, wie es dir geht …“",
        "Frag eine treue Kundin, ob sie ihre Öle schon mal weiterempfohlen hat. Dann einfach zuhören.",
        "Erzähl der Kundin von der Aktion dieser Woche, persönlich und nur für sie.",
        "Wer ist im Sommer eingeschrieben worden und noch nicht im Treueprogramm? Nachfassen, so wie bei einer Einschreibung.",
        "Bedank dich bei einer Kundin für ihre Treue, ganz ohne Angebot."
      ] }
  ];
  var TR_ABSCHLUSS = [
    { id: "volumen", text: "Back Office und Rang-Tracker anschauen: Wie viel Volumen fehlt je Bein?" },
    { id: "team", text: "Das ganze Team anschreiben: Was ist noch in der Pipeline?" },
    { id: "aktion", text: "Monatsend-Aktionen und BOGOs bis zum Schluss an Kundinnen geben." },
    { id: "frontlines", text: "Frontlines anschieben, sie qualifizieren sich damit auch selbst." },
    { id: "kontakte", text: "Alle offenen Kontakte nachfassen und weiter einschreiben." },
    { id: "platz", text: "Mögliche Umplatzierungen prüfen (Placement per Mail an doTERRA, bei Unklarheit Upline fragen)." }
  ];

  function trHeute() { return tiIso(new Date()); }
  function trTagDaten(iso) {
    var T = dtRising.tagesrunde || (dtRising.tagesrunde = {});
    return T[iso] || (T[iso] = {});
  }
  function trZahl(t) { return t ? (t.biz ? 1 : 0) + (t.person ? 1 : 0) + (t.kundin ? 1 : 0) : 0; }
  function trHeuteZahl() { return trZahl((dtRising.tagesrunde || {})[trHeute()]); }
  function trAnsprachen() {
    var T = dtRising.tagesrunde || {}, n = 0;
    Object.keys(T).forEach(function (k) {
      if (k < TR_AB) return;
      var t = T[k];
      n += (t.person ? 1 : 0) + (t.kundin ? 1 : 0) + (t.extra || 0);
    });
    return n;
  }
  function trVerschoben(iso, tage) {
    var d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + tage); return tiIso(d);
  }
  // Tage in Folge mit allen drei Schritten. Heute zählt mit, sobald er voll ist;
  // ist er noch nicht voll, reisst die Serie dadurch nicht ab.
  function trSerie() {
    var T = dtRising.tagesrunde || {}, iso = trHeute(), n = 0;
    if (trZahl(T[iso]) < 3) iso = trVerschoben(iso, -1);
    while (trZahl(T[iso]) === 3) { n++; iso = trVerschoben(iso, -1); }
    return n;
  }
  function trIdee(schritt, iso) {
    var tagNr = Math.floor(new Date(iso + "T12:00:00").getTime() / 86400000);
    return schritt.ideen[tagNr % schritt.ideen.length];
  }

  function trHtml() {
    var iso = trHeute();
    var t = (dtRising.tagesrunde || {})[iso] || {};
    var tagImMonat = Number(iso.slice(8, 10));
    var gezaehlt = trAnsprachen();
    var anteil = Math.min(100, Math.round(gezaehlt / TR_ZIEL * 100));
    var serie = trSerie();

    var woche = "";
    for (var i = 6; i >= 0; i--) {
      var d = trVerschoben(iso, -i);
      var z = trZahl((dtRising.tagesrunde || {})[d]);
      woche += '<span class="tr-punkt z' + z + (d === iso ? " heute" : "") + '" title="' + esc(dtDatum(d)) + ': ' + z + ' von 3">' +
        esc(["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"][new Date(d + "T12:00:00").getDay()]) + '</span>';
    }

    var h = '<section class="panel tr">' +
      '<div class="tr-kopf"><div><h2>Deine Tagesrunde</h2>' +
      '<p class="note">Drei kleine Schritte, jeden Tag. Mehr braucht es heute nicht.</p></div>' +
      '<div class="tr-heute"><b>' + trZahl(t) + '/3</b><span>heute</span></div></div>';

    TR_SCHRITTE.forEach(function (s) {
      var an = !!t[s.id];
      h += '<div class="tr-schritt' + (an ? " an" : "") + '">' +
        '<label class="tr-haken"><input type="checkbox" data-tr="' + s.id + '"' + (an ? " checked" : "") + '>' +
        '<span class="tr-icon">' + s.icon + '</span><span><b>' + esc(s.titel) + '</b><br><span class="note">' + esc(s.wo) + '</span></span></label>' +
        '<p class="tr-idee">💡 ' + esc(trIdee(s, iso)) + '</p>' +
        (s.id === "person" ? '<input class="tr-name" data-trname="pName" value="' + esc(t.pName || "") + '" placeholder="Wen? (kommt in deine Beraterinnen-Liste)" autocomplete="off">' : "") +
        (s.id === "kundin" ? '<input class="tr-name" data-trname="kName" value="' + esc(t.kName || "") + '" placeholder="Wen? (optional)" autocomplete="off">' : "") +
        '</div>';
    });

    h += '<div class="tr-mehr"><span>Heute noch mehr Menschen angesprochen?</span>' +
      '<button class="btn" type="button" data-trextra="-1" aria-label="eine weniger">−</button>' +
      '<b>' + (t.extra || 0) + '</b>' +
      '<button class="btn" type="button" data-trextra="1" aria-label="eine mehr">+</button></div>';

    h += '<div class="tr-fuss"><div class="tr-woche">' + woche + '</div>' +
      '<div class="tr-zaehler"><div class="tr-zlab"><b>' + gezaehlt + '</b> von ' + TR_ZIEL + ' Menschen angesprochen' +
      (serie > 1 ? ' · <span class="tr-serie">' + serie + ' Tage in Folge</span>' : "") + '</div>' +
      '<div class="tr-spur"><span style="width:' + anteil + '%"></span></div>' +
      '<p class="note">Faustregel: rund 100 Menschen ansprechen ergibt 2 bis 4 Beraterinnen. Jedes Nein bringt dich näher an das Ja.</p></div></div>';

    if (tagImMonat <= 15) {
      h += '<p class="tr-hinweis">📌 Bis zum 15.: Wer neu dabei ist und noch nicht im Treueprogramm, jetzt nachfassen, dann gibt es das Produkt des Monats.</p>';
    }
    h += '</section>';

    if (tagImMonat >= 24) h += trAbschlussHtml(iso);
    return h;
  }

  function trAbschlussHtml(iso) {
    var mon = iso.slice(0, 7);
    var A = (dtRising.abschluss || {})[mon] || {};
    var naechster = new Date(Number(iso.slice(0, 4)), Number(iso.slice(5, 7)), 1);
    var restTage = Math.round((naechster - new Date(iso + "T00:00:00")) / 86400000);
    var erledigt = TR_ABSCHLUSS.filter(function (p) { return A[p.id]; }).length;

    var h = '<section class="panel tr tr-abschluss"><div class="tr-kopf"><div><h2>Monatsabschluss</h2>' +
      '<p class="note">Noch ' + restTage + (restTage === 1 ? " Tag" : " Tage") + ' bis das Volumen am Monatsersten auf null fällt.</p></div>' +
      '<div class="tr-heute"><b>' + erledigt + '/' + TR_ABSCHLUSS.length + '</b><span>erledigt</span></div></div>';
    TR_ABSCHLUSS.forEach(function (p) {
      h += '<label class="tr-ab' + (A[p.id] ? " an" : "") + '"><input type="checkbox" data-trab="' + p.id + '"' + (A[p.id] ? " checked" : "") + '> ' + esc(p.text) + '</label>';
    });

    if (doterra && doterra.beine && doterra.beine.length) {
      h += '<h3 class="tr-unter">Was je Bein fehlt <span class="note">Stand ' + esc(monatKlar(doterra.monat)) + ', neuere Zahlen im Back Office</span></h3>';
      doterra.beine.forEach(function (b, i) {
        var bis = (b.zu_naechstem || []).map(function (x) {
          return x.was === "OV" ? zahlKurz(x.fehlt) + " OV" : x.fehlt + " " + x.was;
        }).join(" · ");
        h += '<div class="tr-bein"><span>Bein ' + (i + 1) + ' · ' + esc(b.name) + '</span>' +
          '<span class="note">' + esc(b.rang) + (b.naechster ? " → " + esc(b.naechster) : "") + '</span>' +
          '<b>' + (bis ? "fehlt " + esc(bis) : "erreicht") + '</b></div>';
      });
    }
    return h + '</section>';
  }

  function trBinden(main) {
    var iso = trHeute();
    main.querySelectorAll("[data-tr]").forEach(function (c) {
      c.onchange = function () {
        var t = trTagDaten(iso);
        t[c.dataset.tr] = c.checked;
        if (c.checked && trZahl(t) === 3) toast("Alle drei für heute. Stark, Patricia! 🔥");
        if (c.dataset.tr === "person" && c.checked) trInListe(t.pName);
        dtRisingSpeichern(); render();
      };
    });
    main.querySelectorAll("[data-trname]").forEach(function (f) {
      f.oninput = function () { trTagDaten(iso)[f.dataset.trname] = f.value; dtRisingSpeichern(); };
      if (f.dataset.trname === "pName") {
        f.onchange = function () { var t = trTagDaten(iso); if (t.person) { trInListe(t.pName); render(); } };
      }
    });
    main.querySelectorAll("[data-trextra]").forEach(function (b) {
      b.onclick = function () {
        var t = trTagDaten(iso);
        t.extra = Math.max(0, (t.extra || 0) + Number(b.dataset.trextra));
        dtRisingSpeichern(); render();
      };
    });
    main.querySelectorAll("[data-trab]").forEach(function (c) {
      c.onchange = function () {
        var A = dtRising.abschluss || (dtRising.abschluss = {});
        var mon = iso.slice(0, 7);
        var m = A[mon] || (A[mon] = {});
        m[c.dataset.trab] = c.checked;
        dtRisingSpeichern(); render();
      };
    });
  }

  // Eine angesprochene Person landet als Idee in der Beraterinnen-Liste — einmal, nicht doppelt.
  function trInListe(name) {
    name = (name || "").trim();
    if (!name) return;
    var B = dtRising.beraterinnen || (dtRising.beraterinnen = []);
    var da = B.some(function (b) { return (b.name || "").trim().toLowerCase() === name.toLowerCase(); });
    if (da) return;
    B.push({ id: "b" + Date.now().toString(36) + Math.random().toString(36).slice(2, 5), name: name,
             notiz: "angesprochen am " + dtDatum(trHeute()), stufe: "idee", naechster: "", datum: "", angelegt: trHeute() });
    toast(name + " steht jetzt in deiner Beraterinnen-Liste");
  }
