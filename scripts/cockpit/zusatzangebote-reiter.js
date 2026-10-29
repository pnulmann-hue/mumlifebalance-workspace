  /* ======================================================================
     Reiter "Zusatzangebote" — Produkte -> Upsell-Ersteller
     (seit 29.10.2026, patch-zusatzangebote.py)

     Patricia: „ich brauche im cockpit drin unbedingt auch noch einen upsell,
     downsell, crosssell ersteller“. Sie waehlt ein Produkt, die Seite fragt
     Claude ueber `sample` nach Bump, Upsell, Downsell und Cross-Sell — aus
     dem, was sie schon hat, oder als neues KI-Tool zum Bauen.

     Quellen: daten/katalog (Preise und heutige Kette aus ThriveCart),
     daten/produkt-details (ihre Notizen je Angebot, nur gelesen) und ZA_TOOLS
     (ihre eigenen KI-Tools, die nicht in ThriveCart stehen).

     🚨 Die Preis-Kette wird NACH der Antwort in JS nachgerechnet, nicht dem
     Modell geglaubt: Bump < Hauptprodukt · Bump < Upsell < Hauptprodukt ·
     Downsell < Upsell. Ein Vorschlag, der sie bricht, steht rot da.

     Ergebnisse je Produkt in der Sammlung `zusatzangebote` (gehoert der
     Seite, der Abgleich schreibt dort nie) und lokal unter mlb:za-<id>.
     ====================================================================== */

  /* Julias Regeln, verdichtet aus dem Themenbuch Angebotstreppe, Abschnitt 19-21
     (reference/julia-trost/learnings/themen/angebotstreppe.md). Gekauftes
     Material — das Cockpit ist privat. */
  var ZA_REGELN = [
    "REGELN FÜR BUMP, UPSELL, DOWNSELL UND CROSS-SELL (Julias Methode, auf Patricias Regeln angepasst)",
    "",
    "Warum: Im Moment des Kaufs ist die Käuferin kaufbereit. Wer dort nichts anbietet, lässt Geld liegen. Aus einem Kauf werden zwei, drei, vier — der Kundenwert steigt, ohne neue Reichweite.",
    "",
    "ORDER BUMP (auf der Kasse, vor dem Bezahlen, ein Häkchen):",
    "- Immer günstiger als das Hauptprodukt, und in sich rabattiert: 30 bis 60 Prozent unter seinem normalen Preis, gern 50 bis 60.",
    "- Immer etwas Kleines und Günstiges, nie etwas sehr Hochwertiges. Typisch 15 bis 37, zu einem Kurs für 333 eher 17, bis 49 geht noch.",
    "- Der nächste logische Schritt zum Hauptprodukt ('willst du zu deinem Burger auch Pommes?'). Darf auch konträr sein: 'um dein Ziel zu erreichen, brauchst du auch das'.",
    "- Minikurse lassen sich gegenseitig als Bump verknüpfen.",
    "- Mehrere Bumps plus ein Bundle aus allen Bumps zu einem nochmals günstigeren Preis ist die stärkste Form.",
    "",
    "UPSELL (direkt nach dem Bezahlen, eigene kurze Seite, ein Klick):",
    "- PATRICIAS VERBINDLICHE REGEL: teurer als der Bump, aber günstiger als das Hauptprodukt, stark rabattiert gegenüber seinem normalen Preis ('wenn ich jetzt nicht buche, verpasse ich es'). Julia lässt ihn manchmal teurer als das Hauptprodukt — hier NICHT.",
    "- Gut als Upsell: ein Begleitpaket (WhatsApp-/Telegram-Begleitung, eine Woche bis ein Monat), eine 1:1-Stunde, ein Werkzeug, das das Gelernte sofort anwendet. 1:1 und Begleitung gehen immer, auch ohne weiteres Programm.",
    "- Kleinere Upsells mit wenig Text, grossem Bild und Stimmen verkaufen meist besser als ganz grosse.",
    "",
    "DOWNSELL (wenn das Upsell abgelehnt wird):",
    "- Günstiger als das Upsell: eine kleinere Fassung davon (kürzer, ohne Begleitung, nur das Werkzeug) oder das Upsell in Raten.",
    "",
    "CROSS-SELL (nicht auf der Kasse, sondern danach: im Kurs als 'So geht's weiter', in der Fusszeile jeder Lektion, in der Mail-Strecke nach dem Kauf):",
    "- Ein anderes Angebot, das zum Ziel der Käuferin noch nötig ist — Folgekurs zum selben Thema oder ein anderes Thema. In den Produkten immer wieder auf den nächsten Schritt zeigen.",
    "- Preis: der normale Preis des Angebots oder ein Käuferinnen-Preis 'nur für dich, weil du X hast'. Darf teurer sein als das Hauptprodukt — es ist der nächste Schritt auf der Treppe.",
    "",
    "PATRICIAS FESTE REGELN:",
    "- Minikurse kosten fix 39. Grosse Kurse 333 (nach Gratis-Anmeldung 'nur hier' 199). Story-Generator 17. Mum Business Academy 997.",
    "- Keine Geld-zurück-Garantie. Keine erfundenen Zahlen, keine erfundenen Kundinnen-Ergebnisse.",
    "- Verkauft wird die Veränderung, nie Modul-, Lektions- oder Call-Zahlen.",
    "- Ihre Kundinnen sind Mamas im Network Marketing. Deren eigene Kundschaft heisst nie 'Kundin' (Kundschaft, Leute, Interessenten).",
    "- Schweizer Rechtschreibung mit ss, Freundin-Ton, kein Stakkato, keine KI-Floskeln, kein 'nicht X, sondern Y'."
  ].join("\n");

  /* Ihre eigenen KI-Tools — stehen nicht oder nicht so in ThriveCart. */
  var ZA_TOOLS = [
    { name: "Nischengenerator", preis: 0, link: "https://mlb-nischengenerator.vercel.app",
      was: "Sechs Fragen, dann drei Themen mit Experten-Satz, Produktbrücke und Tool-Ideen. 0-Franken-Freebie, 10 Durchgänge je Mailadresse." },
    { name: "Story-Generator", preis: 17, link: "https://mlb-story-generator.vercel.app",
      was: "Alltagssituation plus Produkt rein, fertige Story-Abfolge raus (Alltag → Learning → Angebot). Zugang per Code. Kasse noch nicht eingerichtet." },
    { name: "Stimm-Check", preis: 0, link: "https://stimm-check.vercel.app/",
      was: "Textprobe rein, Rückmeldung zur eigenen Schreibstimme raus. 0-Franken-Freebie." },
    { name: "Startklar-Werkstatt", preis: null, link: "https://startklar.mumlifebalance.ch",
      was: "Zwölf Stationen fürs Instagram-Grundgerüst mit KI-Rückmeldung. Gehört zum Kauf von Startklar (39)." }
  ];

  var zaWahl = lsGet("za-wahl", "") || "";
  var zaPreisEigen = {};
  var zaErgebnis = {};
  var zaLaeuft = false;
  var zaWunsch = "";

  function zaProdukte() {
    var alle = (katalog && katalog.angebote) || [];
    return alle.filter(function (a) {
      return a.status === "live" && a.preis > 0 &&
        a.kategorie !== "sonstiges" && a.kategorie !== "tipp" && a.kategorie !== "prompt" &&
        !/rabatt|webinar/i.test(a.name);
    });
  }

  function zaPreis(a) {
    if (!a) return null;
    var e = zaPreisEigen[a.id];
    if (e != null && e !== "") return Number(e);
    return a.preis > 0 ? a.preis : null;
  }

  /* Die Notizen haengen an Schluesseln aus dem alten Namen ("a-" + Name,
     Umlaut wird "-", auf 30 Zeichen gekuerzt) oder am Kassen-Slug. Nur exakte
     Treffer: ein Praefix-Vergleich hat der Produktwelt am 29.10. die Notiz
     von „Vom Network-Wissen zum eigenen Produkt“ untergeschoben. */
  function zaNotiz(a) {
    var pd = produktdetails || {};
    var ausName = ("a-" + String(a.name || "").toLowerCase()
      .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")).slice(0, 30).replace(/-$/, "");
    var kandidaten = [ausName, "a-" + (a.slug || "")];
    for (var i = 0; i < kandidaten.length; i++) {
      var e = pd[kandidaten[i]];
      if (e && e.inhalt) return e.inhalt;
    }
    return "";
  }

  function zaKetteText(a) {
    var k = a.kette || {}, raus = [];
    ["bumps", "upsells", "downsells"].forEach(function (f) {
      (k[f] || []).forEach(function (x) {
        raus.push(f.slice(0, -1) + ": " + x.name + (x.preis != null ? " (" + x.preis + ")" : ""));
      });
    });
    return raus.length ? raus.join("; ") : "noch nichts";
  }

  /* Die Preis-Kette nachrechnen — die Antwort des Modells zaehlt hier nicht. */
  function zaPruefen(v, haupt) {
    var bumps = v.filter(function (x) { return x.rolle === "bump" && x.preis != null; });
    var ups = v.filter(function (x) { return x.rolle === "upsell" && x.preis != null; });
    var maxBump = bumps.reduce(function (m, x) { return Math.max(m, x.preis); }, -1);
    var minUp = ups.reduce(function (m, x) { return Math.min(m, x.preis); }, Infinity);
    v.forEach(function (x) {
      x.fehler = [];
      if (x.preis == null || isNaN(x.preis)) { if (x.rolle !== "crosssell") x.fehler.push("kein Preis"); return; }
      if (haupt == null) return;
      if (x.rolle === "bump" && !(x.preis < haupt)) x.fehler.push("Bump muss günstiger sein als das Hauptprodukt (" + haupt + ")");
      if (x.rolle === "upsell") {
        if (!(x.preis < haupt)) x.fehler.push("Upsell muss günstiger sein als das Hauptprodukt (" + haupt + ")");
        if (maxBump >= 0 && !(x.preis > maxBump)) x.fehler.push("Upsell muss teurer sein als der Bump (" + maxBump + ")");
      }
      if (x.rolle === "downsell") {
        /* Ein Downsell gehoert zu EINEM Upsell — gegen dessen Preis pruefen,
           sonst gegen das guenstigste. */
        var zu = ups.filter(function (u) { return x.zu && u.name === x.zu; })[0];
        var grenze = zu ? zu.preis : minUp;
        if (grenze < Infinity && !(x.preis < grenze))
          x.fehler.push("Downsell muss günstiger sein als das Upsell" + (zu ? " „" + zu.name + "“" : "") + " (" + grenze + ")");
      }
    });
    return v;
  }

  function zaFragen(a) {
    if (!sampler) { toast("Hier kann ich gerade nicht schreiben — öffne das Cockpit auf claude.ai."); return; }
    var haupt = zaPreis(a);
    if (haupt == null) { toast("Trag zuerst den Preis des Produkts ein."); return; }
    var liste = zaProdukte().filter(function (x) { return x.id !== a.id; }).map(function (x) {
      return "- " + x.name + " · " + x.preis + " CHF · " + (x.link || "kein Link") + " · id " + x.id;
    }).join("\n");
    var tools = ZA_TOOLS.map(function (t) {
      return "- " + t.name + " · " + (t.preis == null ? "Teil eines Kaufs" : t.preis + " CHF") + " · " + t.link + " · " + t.was;
    }).join("\n");
    var p = "Du hilfst Patricia Ulmann (Mum Life Balance, Schweiz), Zusatzangebote für eines ihrer Produkte zu planen. " +
      "Ihre Kundinnen sind Mamas, die im Network Marketing arbeiten und sich ein eigenes Online-Business daneben aufbauen.\n\n" +
      ZA_REGELN +
      "\n\nDAS HAUPTPRODUKT\n" + a.name + " · " + haupt + " CHF · " + (a.link || "") +
      "\nWas heute schon an der Kasse hängt: " + zaKetteText(a) +
      (zaNotiz(a) ? "\nPatricias Notiz dazu: " + zaNotiz(a) : "") +
      "\n\nIHRE BESTEHENDEN PRODUKTE (nur diese gibt es wirklich)\n" + liste +
      "\n\nIHRE EIGENEN KI-TOOLS\n" + tools +
      (zaWunsch.trim() ? "\n\nPATRICIAS WUNSCH FÜR DIESEN DURCHGANG\n" + zaWunsch.trim() : "") +
      "\n\nAUFTRAG\nMach 7 bis 9 Vorschläge: mindestens 2 Bumps, 2 Upsells, 1 Downsell, 2 Cross-Sells. " +
      "Mische bestehende Produkte und neue Ideen. Neue Ideen sind vor allem KI-Tools, die sie mit Claude bauen kann " +
      "(Rechner, Check, Planer, Generator — so wie Nischengenerator und Story-Generator), dazu Begleitung oder 1:1 wo es passt. " +
      "Ein neues Tool muss ein Problem lösen, das die Käuferin direkt NACH diesem Kauf hat. " +
      "Nenne bei bestehenden Produkten den Link genau so, wie er oben steht, und erfinde keine Links. " +
      "Jeder Downsell nennt im Feld zu den Namen des Upsells, dem er folgt (genau wie dort geschrieben). " +
      "Rechne jeden Preis offen vor (z. B. 'normal 39, als Bump 56 % günstiger = 17'). Halte die Preis-Kette strikt ein." +
      '\n\nAntworte nur als JSON: {"vorschlaege": [{"rolle": "bump|upsell|downsell|crosssell", "name": "...", ' +
      '"art": "bestehend|neu", "tooltyp": "Rechner|Check|Planer|Generator|Begleitung|1:1|Kurs|Bundle|anderes", ' +
      '"preis": Zahl in CHF, "normalpreis": Zahl oder null, "rechnung": "die Rechnung ausgeschrieben", ' +
      '"problem": "welches Problem es nach dem Kauf löst, ein Satz", "kasse": "ein Satz für die Kasse, in ihrer Stimme", ' +
      '"link": "Link oder leer", "zu": "nur beim Downsell: Name des Upsells", "bauen": "bei neu: was gebaut werden muss, ein bis zwei Sätze; bei bestehend leer"}], ' +
      '"hinweis": "ein Satz, worauf sie bei diesem Produkt achten soll"}';
    zaLaeuft = true;
    render();
    sampler.json(p, { modelTier: "complex", cache: false }).then(function (r) {
      var v = (r && r.vorschlaege) || [];
      v.forEach(function (x) { x.preis = x.preis == null || x.preis === "" ? null : Number(x.preis); });
      var erg = { produkt: a.id, name: a.name, preis: haupt, vorschlaege: zaPruefen(v, haupt),
                  hinweis: (r && r.hinweis) || "", stand: new Date().toISOString(), wunsch: zaWunsch.trim() };
      zaErgebnis[a.id] = erg;
      lsSet("za-" + a.id, erg);
      if (db) db.doc("zusatzangebote/" + a.id).set(JSON.parse(JSON.stringify(erg))).catch(function () {});
    }).catch(function (e) {
      zaErgebnis[a.id] = { fehler: (e && (e.code || e.message)) || "Fehler" };
    }).then(function () { zaLaeuft = false; render(); });
  }

  function zaLaden(a) {
    if (zaErgebnis[a.id] !== undefined) return;
    zaErgebnis[a.id] = lsGet("za-" + a.id, null);
    if (!db) return;
    db.doc("zusatzangebote/" + a.id).get().then(function (s) {
      if (!s.exists) return;
      var d = tief(s.data());
      var lokal = zaErgebnis[a.id];
      if (!lokal || !lokal.stand || (d.stand && d.stand > lokal.stand)) {
        zaErgebnis[a.id] = d; lsSet("za-" + a.id, d);
        if (activeTab === "zusatzangebote") render();
      }
    }).catch(function () {});
  }

  var ZA_ROLLEN = [
    { id: "bump", name: "Order Bump", wo: "Häkchen auf der Kasse, vor dem Bezahlen" },
    { id: "upsell", name: "Upsell", wo: "eigene Seite direkt nach dem Bezahlen" },
    { id: "downsell", name: "Downsell", wo: "wenn das Upsell abgelehnt wird" },
    { id: "crosssell", name: "Cross-Sell", wo: "danach: im Kurs, in der Fusszeile, in der Mail-Strecke" }
  ];

  function zaKarte(x) {
    var neu = x.art === "neu";
    return '<div class="za-karte' + (x.fehler && x.fehler.length ? " za-bruch" : "") + '">' +
      '<div class="za-kopf"><b>' + esc(x.name) + '</b>' +
      '<span class="za-preis">' + (x.preis != null ? esc(x.preis) + " CHF" : "–") + '</span></div>' +
      '<div class="za-chips"><span class="chip' + (neu ? " orange" : "") + '">' +
      (neu ? "neu bauen" : "gibt es schon") + '</span>' +
      (x.rolle === "downsell" && x.zu ? ' <span class="chip">nach: ' + esc(x.zu) + '</span>' : "") +
      (x.tooltyp ? ' <span class="chip">' + esc(x.tooltyp) + '</span>' : "") + '</div>' +
      (x.rechnung ? '<p class="za-rech">' + esc(x.rechnung) + '</p>' : "") +
      (x.problem ? '<p><span class="za-lab">Löst nach dem Kauf</span>' + esc(x.problem) + '</p>' : "") +
      (x.kasse ? '<p class="za-kasse">„' + esc(x.kasse) + '“</p>' : "") +
      (neu && x.bauen ? '<p><span class="za-lab">Zu bauen</span>' + esc(x.bauen) + '</p>' : "") +
      (x.link && /^https?:\/\//.test(x.link) ? '<p><a href="' + esc(x.link) + '" target="_blank" rel="noopener">' + esc(x.link) + '</a></p>' : "") +
      (x.fehler && x.fehler.length ? '<p class="za-warn">⚠ ' + esc(x.fehler.join(" · ")) + '</p>' : "") +
      '</div>';
  }

  function zaAlsText(erg) {
    var t = ["Zusatzangebote für " + erg.name + " (" + erg.preis + " CHF)", ""];
    ZA_ROLLEN.forEach(function (r) {
      var v = (erg.vorschlaege || []).filter(function (x) { return x.rolle === r.id; });
      if (!v.length) return;
      t.push(r.name.toUpperCase() + " — " + r.wo);
      v.forEach(function (x) {
        t.push("• " + x.name + " · " + (x.preis != null ? x.preis + " CHF" : "–") + " · " + (x.art === "neu" ? "neu bauen" : "gibt es schon"));
        if (x.rechnung) t.push("  Rechnung: " + x.rechnung);
        if (x.problem) t.push("  Löst: " + x.problem);
        if (x.kasse) t.push("  Kasse: " + x.kasse);
        if (x.art === "neu" && x.bauen) t.push("  Bauen: " + x.bauen);
        if (x.link) t.push("  Link: " + x.link);
        if (x.fehler && x.fehler.length) t.push("  ⚠ " + x.fehler.join(" · "));
      });
      t.push("");
    });
    return t.join("\n");
  }

  function renderZusatzangebote(main) {
    var liste = zaProdukte();
    var a = liste.filter(function (x) { return x.id === zaWahl; })[0] || null;
    if (a) zaLaden(a);
    var erg = a ? zaErgebnis[a.id] : null;
    var haupt = a ? zaPreis(a) : null;

    var opts = '<option value="">— Produkt wählen —</option>' + liste.map(function (x) {
      return '<option value="' + esc(x.id) + '"' + (x.id === zaWahl ? " selected" : "") + '>' +
        esc(x.name) + ' · ' + esc(x.preis) + ' CHF</option>';
    }).join("");

    var h = '<div class="page-head"><div><h1>Upsell-Ersteller</h1>' +
      '<p>Wähl ein Produkt. Du bekommst Vorschläge für Bump, Upsell, Downsell und Cross-Sell nach Julias Methode, ' +
      'aus dem, was du schon hast, oder als neues KI-Tool zum Bauen. Die Preis-Kette rechnet die Seite selbst nach.</p></div></div>' +
      '<div class="panel za-regel"><b>Die Kette:</b> Bump günstiger als das Hauptprodukt · Upsell teurer als der Bump, ' +
      'aber günstiger als das Hauptprodukt · Downsell günstiger als das Upsell · Minikurse fix 39 · keine Geld-zurück-Garantie.</div>' +
      '<div class="panel za-form"><div class="field"><label for="za-wahl">Produkt</label>' +
      '<select id="za-wahl">' + opts + '</select></div>';
    if (a) {
      h += '<div class="field za-klein"><label for="za-preis">Preis (CHF)</label>' +
        '<input id="za-preis" type="number" min="1" value="' + esc(haupt == null ? "" : haupt) + '"></div>' +
        '<div class="field za-breit"><label for="za-wunsch">Wunsch für diesen Durchgang (frei)</label>' +
        '<input id="za-wunsch" placeholder="z. B. nur Tools, die ich in einem Tag bauen kann" value="' + esc(zaWunsch) + '"></div>' +
        '<div class="za-los"><button class="btn primary" id="za-los"' + (zaLaeuft || !sampler ? " disabled" : "") + '>' +
        (zaLaeuft ? "Claude denkt nach …" : (erg && erg.vorschlaege ? "Neue Vorschläge" : "Vorschläge machen")) + '</button></div>';
    }
    h += '</div>';
    if (!sampler) h += '<div class="panel note">Die Vorschläge kommen über Claude und gehen nur im Cockpit auf claude.ai.</div>';

    if (a) {
      h += '<div class="panel za-ist"><b>Heute an der Kasse:</b> ' + esc(zaKetteText(a)) +
        (a.link ? ' · <a href="' + esc(a.link) + '" target="_blank" rel="noopener">Kasse öffnen</a>' : "") + '</div>';
      if (erg && erg.fehler) h += '<div class="panel za-warn">Das hat nicht geklappt (' + esc(erg.fehler) + '). Nochmal versuchen.</div>';
      if (erg && erg.vorschlaege) {
        zaPruefen(erg.vorschlaege, erg.preis);
        var brueche = erg.vorschlaege.filter(function (x) { return x.fehler && x.fehler.length; }).length;
        h += '<div class="za-stand note">Stand ' + esc(String(erg.stand || "").slice(0, 16).replace("T", " ")) +
          (erg.wunsch ? ' · Wunsch: ' + esc(erg.wunsch) : "") +
          (brueche ? ' · <span class="za-warn">' + (brueche === 1 ? "1 Vorschlag bricht" : brueche + " Vorschläge brechen") + ' die Kette</span>' : ' · Kette eingehalten ✓') +
          ' <button class="btn ghost" id="za-kopie">Als Text kopieren</button></div>';
        if (erg.hinweis) h += '<div class="panel za-hinweis">' + esc(erg.hinweis) + '</div>';
        ZA_ROLLEN.forEach(function (r) {
          var v = erg.vorschlaege.filter(function (x) { return x.rolle === r.id; });
          if (!v.length) return;
          h += '<h2 class="za-rolle">' + esc(r.name) + ' <span>' + esc(r.wo) + '</span></h2>' +
            '<div class="za-raster">' + v.map(zaKarte).join("") + '</div>';
        });
      }
    }
    main.innerHTML = h;

    var sel = main.querySelector("#za-wahl");
    if (sel) sel.onchange = function () { zaWahl = sel.value; lsSet("za-wahl", zaWahl); render(); };
    var pr = main.querySelector("#za-preis");
    if (pr) pr.onchange = function () { zaPreisEigen[a.id] = pr.value; };
    var wu = main.querySelector("#za-wunsch");
    if (wu) wu.oninput = function () { zaWunsch = wu.value; };
    var los = main.querySelector("#za-los");
    if (los) los.onclick = function () { if (pr) zaPreisEigen[a.id] = pr.value; zaFragen(a); };
    var ko = main.querySelector("#za-kopie");
    if (ko) ko.onclick = function () {
      var txt = zaAlsText(erg);
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () {
        toast("Kopiert.");
      }).catch(function () { toast("Kopieren ging nicht."); });
    };
  }
