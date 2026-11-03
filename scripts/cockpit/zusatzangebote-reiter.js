  /* ======================================================================
     Reiter "Zusatzangebote" — Produkte -> Upsell-Ersteller
     (seit 29.10.2026, patch-zusatzangebote.py)

     Patricia: „ich brauche im cockpit drin unbedingt auch noch einen upsell,
     downsell, crosssell ersteller“. Sie waehlt ein Produkt, die Seite fragt
     Claude ueber `sample` nach Bump, Upsell, Downsell und Cross-Sell — aus
     dem, was sie schon hat, oder als neues KI-Tool zum Bauen.

     Quellen: daten/katalog (Preise und heutige Kette aus ThriveCart),
     daten/produkt-details (ihre Notizen je Angebot, nur gelesen), ZA_TOOLS
     (ihre eigenen KI-Tools, die nicht in ThriveCart stehen) und seit
     31.10.2026 Julias voller Abschnitt „Verknuepfen I-III“ aus der Sammlung
     `bibliothek` (zaJuliaText).

     🚨 Die Preis-Kette wird NACH der Antwort in JS nachgerechnet, nicht dem
     Modell geglaubt: Bump < Hauptprodukt · Upsell > Bump (darf teurer sein
     als das Hauptprodukt, Patricias Entscheid 31.10.: „darum heisst er ja
     UPsell“) · Downsell < sein Upsell. Wer sie bricht, steht rot da. Der
     Rabatt (Julia: Bump 30-60 %) steht als oranger Hinweis daneben.

     Seit 31.10.2026 zwei Wege weiter:
     - „Tool-Bauplan“ bei jedem KI-Tool: sucht in Patricias eigenen Kursen
       (Sammlung `eigenwissen`, von eigenwissen-bauen.py) und in Julias
       Themenbuechern die passenden Stellen und laesst Claude daraus einen
       fertigen Bauplan fuer Vercel schreiben — System-Prompt mit ihrem
       Wissen, Ablauf, Pruefregeln und den Auftrag fuer Claude Code.
     - „Mit Knopfdruck bauen“: kopiert den Vorschlag als Auftrag, den „Angebot
       auf Knopfdruck“ einliest (Kennung MLB-ZUSATZANGEBOT).

     Ergebnisse je Produkt in der Sammlung `zusatzangebote` (gehoert der
     Seite, der Abgleich schreibt dort nie) und lokal unter mlb:za-<id>.
     ====================================================================== */

  /* Kurzfassung der Regeln. Julias voller Abschnitt kommt zusaetzlich ueber
     zaJuliaText() aus der Datenbank. Der Text steht bewusst NICHT hier im
     Code: mlb-cockpit.html liegt im oeffentlichen Repo, das Themenbuch ist
     gekauftes Material. Laedt er nicht, sagt die Seite das dazu. */
  var ZA_REGELN = [
    "REGELN FÜR BUMP, UPSELL, DOWNSELL UND CROSS-SELL",
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
    "- Teurer als der Bump. Er darf gleich teuer oder teurer sein als das Hauptprodukt (Patricias Entscheid: 'darum heisst er ja UPsell'), ist aber immer stark rabattiert gegenüber seinem normalen Preis ('wenn ich jetzt nicht buche, verpasse ich es').",
    "- Nach einem Minikurs verkaufen sich Upsells unter 200 erfahrungsgemäss am besten.",
    "- Gut als Upsell: ein Begleitpaket (WhatsApp-/Telegram-Begleitung, eine Woche bis ein Monat), eine 1:1-Stunde, ein Werkzeug, das das Gelernte sofort anwendet, ein grösserer Kurs zum Sonderpreis. 1:1 und Begleitung gehen immer.",
    "- Kleinere Upsells mit wenig Text, grossem Bild und Stimmen verkaufen meist besser als ganz grosse.",
    "",
    "DOWNSELL (wenn das Upsell abgelehnt wird):",
    "- Günstiger als das Upsell, dem er folgt: eine kleinere Fassung davon (kürzer, ohne Begleitung, nur das Werkzeug) oder das Upsell in Raten.",
    "",
    "CROSS-SELL (nicht auf der Kasse, sondern danach: im Kurs als 'So geht's weiter', in der Fusszeile jeder Lektion, in der Mail-Strecke nach dem Kauf):",
    "- Ein anderes Angebot, das zum Ziel der Käuferin noch nötig ist — Folgekurs zum selben Thema oder ein anderes Thema. In den Produkten immer wieder auf den nächsten Schritt zeigen.",
    "- Preis: der normale Preis des Angebots oder ein Käuferinnen-Preis 'nur für dich, weil du X hast'.",
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

  /* Die Themenbuecher, aus denen ein Tool-Bauplan Fachwissen holen darf. */
  var ZA_BUECHER = {
    positionierung: "Positionierung, Nische, Thema", angebotstreppe: "Angebote, Preise, Treppe",
    freebie: "Freebies und Leadmagneten", funnel: "Funnel und Mail-Strecken", verkaufsseite: "Verkaufsseiten",
    launch: "Launch", storys: "Instagram-Storys", content: "Content, Säulen, Hooks, Reels, Karussells",
    werbung: "Werbeanzeigen", strategie: "Business-Strategie", jahresplan: "Jahresplanung",
    zeit: "Zeit, Fokus, Mama-CEO", ki: "KI und Automatisierung"
  };

  var zaWahl = lsGet("za-wahl", "") || "";
  var zaPreisEigen = {};
  var zaErgebnis = {};
  var zaLaeuft = false;
  var zaWunsch = "";
  var zaJulia = null;        /* null = noch nicht geladen, "" = nicht verfuegbar */
  var zaEigen = null;        /* Stuecke aus Patricias eigenen Kursen */
  var zaBuchStuecke = {};    /* je Themenbuch die Stichpunkte */
  var zaBauLaeuft = {};      /* "<produkt>:<nr>" -> true */

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

  function zaKopieren(txt, meldung) {
    (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () {
      toast(meldung || "Kopiert.");
    }).catch(function () { toast("Kopieren ging nicht."); });
  }

  /* ---------- Wissen holen ---------- */

  /* Fundstellen am Zeilenende („— Kurs: datei.txt, 00:12:03“) braucht hier niemand. */
  function zaOhneFundstelle(z) {
    return z.replace(/\s+—\s+(?=[^—]*(\.txt|\.pdf|S\.\s?\d|\d:\d\d|Mentoring-Gruppe|Calls?\b))[^—]*$/, "");
  }

  /* Julias Abschnitt „Verknuepfen I-III“ aus dem Themenbuch Angebotstreppe.
     Ueber den Titel, nicht ueber die Nummer — die Nummern aendern sich, wenn
     das Buch waechst. */
  function zaJuliaText(fertig) {
    if (zaJulia !== null) { fertig(zaJulia); return; }
    zaBuchLaden("angebotstreppe", function (md) {
      var raus = [];
      String(md || "").split(/\n(?=## )/).forEach(function (abschnitt) {
        var titel = abschnitt.split("\n")[0];
        if (/^## /.test(titel) && /Verknüpfen/i.test(titel)) raus.push(abschnitt);
      });
      zaJulia = raus.join("\n\n").split("\n").map(zaOhneFundstelle).join("\n").trim();
      fertig(zaJulia);
    });
  }

  function zaBuchLaden(id, fertig) {
    if (typeof bibIndexLaden !== "function" || typeof bibTextLaden !== "function") { fertig(""); return; }
    var einmal = false;
    bibIndexLaden(function () {
      if (einmal) return;
      einmal = true;
      var thema = ((bibIndex && bibIndex.themen) || []).filter(function (x) { return x.id === id; })[0];
      var teile = thema && thema.buch && thema.buch.teile;
      if (!teile) { fertig(""); return; }
      bibTextLaden("t-" + id, teile, function (md) { fertig(md || ""); });
    });
  }

  function zaNorm(s) {
    return String(s || "").toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
  }

  var ZA_FUELL = ("aber alle also auch dabei damit dann dass dein deine deinem deinen deiner diese dieser dieses durch " +
    "eine einem einen einer eines etwas fuer gibt habe haben hast hier immer jetzt kann kannst keine mehr mich mit nach " +
    "nicht noch nur oder ohne schon sein sich sind soll ueber und uns unter viel vom von was weil welche wenn werden wie " +
    "wird wirklich zum zur zwei direkt kauf kaeuferin neue neuen nach patricia produkt produkte tool tools").split(" ");

  function zaWoerter(text) {
    var gesehen = {};
    return zaNorm(text).split(/[^a-z0-9]+/).filter(function (w) {
      if (w.length < 5 || ZA_FUELL.indexOf(w) >= 0 || gesehen[w]) return false;
      gesehen[w] = true;
      return true;
    });
  }

  /* Patricias eigene Kurse aus der Sammlung `eigenwissen`, zerlegt in Stuecke
     von rund 900 Zeichen, je mit der Lektion davor als Herkunft. */
  function zaEigenLaden(fertig) {
    if (zaEigen) { fertig(zaEigen); return; }
    if (!db) { zaEigen = []; fertig(zaEigen); return; }
    db.doc("eigenwissen/_index").get().then(function (snap) {
      if (!snap.exists) { zaEigen = []; fertig(zaEigen); return; }
      var ix = tief(snap.data()) || {};
      var holen = [];
      (ix.kurse || []).forEach(function (k) {
        for (var n = 1; n <= (k.teile || 1); n++) {
          holen.push(db.doc("eigenwissen/" + k.id + "-" + n).get().then(function (kk) {
            return function (s) { return { kurs: kk.name, md: s.exists ? (s.data().md || "") : "" }; };
          }(k)));
        }
      });
      return Promise.all(holen).then(function (teile) {
        var stuecke = [];
        teile.forEach(function (t) {
          var lektion = "", puffer = "";
          t.md.split(/\n\s*\n/).forEach(function (absatz) {
            var kopf = absatz.match(/^#+\s+(.*)$/m);
            if (kopf && absatz.trim().indexOf("#") === 0) lektion = kopf[1].trim();
            puffer += (puffer ? "\n" : "") + absatz.trim();
            if (puffer.length > 900) {
              stuecke.push({ quelle: t.kurs + (lektion ? " · " + lektion : ""), text: puffer });
              puffer = "";
            }
          });
          if (puffer) stuecke.push({ quelle: t.kurs + (lektion ? " · " + lektion : ""), text: puffer });
        });
        zaEigen = stuecke;
        fertig(zaEigen);
      });
    }).catch(function () { zaEigen = []; fertig(zaEigen); });
  }

  function zaBuchStueckeLaden(id, fertig) {
    if (zaBuchStuecke[id]) { fertig(zaBuchStuecke[id]); return; }
    zaBuchLaden(id, function (md) {
      var abschnitt = "";
      var stuecke = [];
      String(md || "").split("\n").forEach(function (z) {
        if (/^##\s/.test(z)) abschnitt = z.replace(/^#+\s*/, "");
        else if (/^\s*-\s/.test(z)) stuecke.push({ quelle: ZA_BUECHER[id] + (abschnitt ? " · " + abschnitt : ""), text: zaOhneFundstelle(z.trim()) });
      });
      zaBuchStuecke[id] = stuecke;
      fertig(stuecke);
    });
  }

  /* Bewertet jedes Stueck danach, wie viele der Suchwoerter darin vorkommen
     (ueber die ersten sechs Buchstaben, damit „Säulen“ auch „Säule“ findet). */
  function zaBeste(stuecke, woerter, grenze) {
    var wurzeln = woerter.map(function (w) { return w.slice(0, 6); });
    var bewertet = stuecke.map(function (s) {
      var n = zaNorm(s.text + " " + s.quelle), punkte = 0;
      wurzeln.forEach(function (w) { if (n.indexOf(w) >= 0) punkte++; });
      return { s: s, p: punkte };
    }).filter(function (x) { return x.p >= 2; });
    bewertet.sort(function (a, b) { return b.p - a.p; });
    var raus = [], laenge = 0, quellen = {};
    for (var i = 0; i < bewertet.length && laenge < grenze; i++) {
      raus.push("[" + bewertet[i].s.quelle + "]\n" + bewertet[i].s.text);
      laenge += bewertet[i].s.text.length;
      quellen[bewertet[i].s.quelle.split(" · ")[0]] = true;
    }
    return { text: raus.join("\n\n"), quellen: Object.keys(quellen), anzahl: raus.length };
  }

  function zaWissenSuchen(woerter, buecher, fertig) {
    zaEigenLaden(function (eigen) {
      var offen = buecher.length, alle = [];
      if (!offen) fertig({ eigen: zaBeste(eigen, woerter, 20000), fach: { text: "", quellen: [], anzahl: 0 } });
      buecher.forEach(function (id) {
        zaBuchStueckeLaden(id, function (st) {
          alle = alle.concat(st);
          if (--offen === 0) fertig({ eigen: zaBeste(eigen, woerter, 20000), fach: zaBeste(alle, woerter, 10000) });
        });
      });
    });
  }

  /* ---------- Vorschlaege ---------- */

  /* Die Preis-Kette nachrechnen — die Antwort des Modells zaehlt hier nicht. */
  function zaPruefen(v, haupt) {
    var bumps = v.filter(function (x) { return x.rolle === "bump" && x.preis != null; });
    var ups = v.filter(function (x) { return x.rolle === "upsell" && x.preis != null; });
    var maxBump = bumps.reduce(function (m, x) { return Math.max(m, x.preis); }, -1);
    var minUp = ups.reduce(function (m, x) { return Math.min(m, x.preis); }, Infinity);
    v.forEach(function (x) {
      x.fehler = [];
      x.hinweise = [];
      var normal = Number(x.normalpreis);
      if (normal > 0 && x.preis != null && x.rolle !== "crosssell") {
        var rabatt = Math.round((1 - x.preis / normal) * 100);
        if (x.rolle === "bump" && (rabatt < 30 || rabatt > 65))
          x.hinweise.push("Bump-Rabatt " + rabatt + " % — Julia: 30 bis 60 % unter dem normalen Preis");
        if (x.rolle === "upsell" && rabatt < 20)
          x.hinweise.push("Upsell kaum rabattiert (" + rabatt + " %) — Julia rabattiert ihn stark");
      }
      if (x.preis == null || isNaN(x.preis)) { if (x.rolle !== "crosssell") x.fehler.push("kein Preis"); return; }
      if (haupt == null) return;
      if (x.rolle === "bump" && !(x.preis < haupt)) x.fehler.push("Bump muss günstiger sein als das Hauptprodukt (" + haupt + ")");
      if (x.rolle === "upsell" && maxBump >= 0 && !(x.preis > maxBump))
        x.fehler.push("Upsell muss teurer sein als der Bump (" + maxBump + ")");
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
    zaLaeuft = true;
    render();
    zaJuliaText(function (julia) { zaFragenMit(a, haupt, julia); });
  }

  function zaFragenMit(a, haupt, julia) {
    var liste = zaProdukte().filter(function (x) { return x.id !== a.id; }).map(function (x) {
      return "- " + x.name + " · " + x.preis + " CHF · " + (x.link || "kein Link") + " · id " + x.id;
    }).join("\n");
    var tools = ZA_TOOLS.map(function (t) {
      return "- " + t.name + " · " + (t.preis == null ? "Teil eines Kaufs" : t.preis + " CHF") + " · " + t.link + " · " + t.was;
    }).join("\n");
    var buecher = Object.keys(ZA_BUECHER).map(function (k) { return k + " (" + ZA_BUECHER[k] + ")"; }).join(", ");
    var p = "Du hilfst Patricia Ulmann (Mum Life Balance, Schweiz), Zusatzangebote für eines ihrer Produkte zu planen. " +
      "Ihre Kundinnen sind Mamas, die im Network Marketing arbeiten und sich ein eigenes Online-Business daneben aufbauen.\n\n" +
      ZA_REGELN +
      (julia ? "\n\nJULIAS VOLLER ABSCHNITT ZU BUMP, UPSELL, DOWNSELL UND VERKNÜPFEN (aus ihren Kursen, nur für Patricia). " +
        "Arbeite danach. Wo die Regeln oben etwas anderes sagen, gelten die Regeln oben. Nenne Julia nie in den Texten für die Kasse.\n\n" + julia : "") +
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
      "Bei jedem neuen KI-Tool nennst du 4 bis 8 Suchwörter, unter denen ihr Kurswissen dazu zu finden ist " +
      "(z. B. für einen Content-Säulen-Planer: Säulen, Themensäule, Contentsäule, Content-Plan, Redaktionsplan), " +
      "und bis zu drei passende Themenbücher aus dieser Liste: " + buecher + ". " +
      "Rechne jeden Preis offen vor (z. B. 'normal 39, als Bump 56 % günstiger = 17'). Halte die Preis-Kette strikt ein." +
      '\n\nAntworte nur als JSON: {"vorschlaege": [{"rolle": "bump|upsell|downsell|crosssell", "name": "...", ' +
      '"art": "bestehend|neu", "tooltyp": "Rechner|Check|Planer|Generator|Begleitung|1:1|Kurs|Bundle|anderes", ' +
      '"preis": Zahl in CHF, "normalpreis": Zahl oder null, "rechnung": "die Rechnung ausgeschrieben", ' +
      '"problem": "welches Problem es nach dem Kauf löst, ein Satz", "kasse": "ein Satz für die Kasse, in ihrer Stimme", ' +
      '"link": "Link oder leer", "zu": "nur beim Downsell: Name des Upsells", ' +
      '"bauen": "bei neu: was gebaut werden muss, ein bis zwei Sätze; bei bestehend leer", ' +
      '"suchwoerter": ["nur bei neuen KI-Tools"], "buecher": ["nur bei neuen KI-Tools, ids aus der Liste"]}], ' +
      '"hinweis": "ein Satz, worauf sie bei diesem Produkt achten soll"}';
    sampler.json(p, { modelTier: "complex", cache: false }).then(function (r) {
      var v = (r && r.vorschlaege) || [];
      v.forEach(function (x) { x.preis = x.preis == null || x.preis === "" ? null : Number(x.preis); });
      var erg = { produkt: a.id, name: a.name, preis: haupt, link: a.link || "", vorschlaege: zaPruefen(v, haupt),
                  hinweis: (r && r.hinweis) || "", stand: new Date().toISOString(), wunsch: zaWunsch.trim(),
                  quelle: julia ? "Julias voller Abschnitt (rund " + Math.round(julia.length / 1000) + "'000 Zeichen)"
                                : "nur Kurzfassung — Julias Abschnitt hat nicht geladen" };
      zaErgebnis[a.id] = erg;
      zaSichern(erg);
    }).catch(function (e) {
      zaErgebnis[a.id] = { fehler: (e && (e.code || e.message)) || "Fehler" };
    }).then(function () { zaLaeuft = false; render(); });
  }

  function zaSichern(erg) {
    lsSet("za-" + erg.produkt, erg);
    if (db) db.doc("zusatzangebote/" + erg.produkt).set(JSON.parse(JSON.stringify(erg))).catch(function () {
      toast("Nur lokal gespeichert — die Datenbank hat nicht geantwortet.");
    });
  }

  function zaLaden(a) {
    if (zaErgebnis[a.id] !== undefined) return;
    zaErgebnis[a.id] = lsGet("za-" + a.id, null);
    if (!db) return;
    db.doc("zusatzangebote/" + a.id).get().then(function (s) {
      if (!s.exists) return;
      var d = tief(s.data());
      var lokal = zaErgebnis[a.id];
      if (!lokal || !lokal.stand || (d.stand && d.stand > lokal.stand) ||
          (d.stand === lokal.stand && JSON.stringify(d).length > JSON.stringify(lokal).length)) {
        zaErgebnis[a.id] = d; lsSet("za-" + a.id, d);
        if (activeTab === "zusatzangebote") render();
      }
    }).catch(function () {});
  }

  /* ---------- Tool-Bauplan ---------- */

  function zaIstTool(x) {
    return x.art === "neu" && /rechner|check|planer|generator|tool|finder|assistent/i.test((x.tooltyp || "") + " " + (x.name || ""));
  }

  function zaBauplan(erg, nr) {
    var x = erg.vorschlaege[nr];
    if (!sampler || !x) return;
    var schluessel = erg.produkt + ":" + nr;
    zaBauLaeuft[schluessel] = true;
    render();
    var woerter = zaWoerter((x.suchwoerter || []).join(" ") + " " + x.name + " " + (x.problem || "") + " " + (x.bauen || ""));
    var buecher = (x.buecher || []).filter(function (b) { return ZA_BUECHER[b]; }).slice(0, 3);
    if (!buecher.length) buecher = ["content", "positionierung"];
    zaWissenSuchen(woerter, buecher, function (w) {
      var p = "Du baust für Patricia Ulmann (Mum Life Balance, Schweiz) den fertigen Bauplan für ein kleines KI-Tool, " +
        "das sie verkauft. Ihre Kundinnen sind Mamas im Network Marketing mit eigenem Business daneben.\n\n" +
        "DAS TOOL\n" + x.name + " · " + (x.tooltyp || "") + " · " + (x.preis != null ? x.preis + " CHF" : "") +
        " · Rolle: " + x.rolle + " zu „" + erg.name + "“ (" + erg.preis + " CHF)" +
        "\nWelches Problem es nach dem Kauf löst: " + (x.problem || "") +
        "\nWas gebaut werden muss: " + (x.bauen || "") +
        "\n\nPATRICIAS EIGENES WISSEN (aus ihren Kursen, hat Vorrang — nimm ihre Begriffe, Modelle und Schritte, " +
        "sinngemäss und in ihrer Sprache):\n" + (w.eigen.text || "(nichts Passendes gefunden)") +
        "\n\nFACHWISSEN AUS GEKAUFTEN KURSEN (nur als Hintergrund: die Mechanik übernehmen, in eigenen Worten. " +
        "Keine Namen, keine Zitate, keine Beispiele daraus. Das Tool wird verkauft):\n" + (w.fach.text || "(nichts)") +
        "\n\nSO BAUT PATRICIA IHRE TOOLS (Muster Story-Generator, liegt in scripts/story-generator/):\n" +
        "- Vercel-Projekt in scripts/<slug>/: public/index.html (eine Seite, Marke Mum Life Balance: Petrol #12828c, " +
        "Dunkelblau #29556d, Creme #f1ecdd, Orange #dc822e, Schriften Philosopher und Source Sans 3, am Handy bedienbar), " +
        "api/<name>.js (ruft Claude mit lib/system-prompt.md auf und prüft die Antwort gegen Floskeln, Stakkato, " +
        "'nicht X, sondern Y' und das Wort 'Kundin' für die Kundschaft der Nutzerin; bis zu zwei Korrekturrunden), " +
        "lib/system-prompt.md (das ganze Wissen), Zugang per Code (Vercel-Variable ZUGANGSCODES).\n" +
        "- Netlify nur, wenn das Tool ohne KI nach festen Regeln rechnet (eine HTML-Datei, Netlify Drop).\n" +
        "- Ausgeliefert unter mlb-<slug>.vercel.app, Deploy: cd scripts/<slug> && npx vercel --prod --yes.\n" +
        "- Nichts dazuerfinden: Wo der Nutzerin eine Angabe fehlt, fragt das Tool nach oder markiert die Stelle mit ✏️.\n\n" +
        "REGELN\n- Schweizer Rechtschreibung mit ss, Freundin-Ton, kein Stakkato, keine KI-Floskeln.\n" +
        "- Keine erfundenen Zahlen, keine Heilversprechen, keine Einkommensversprechen.\n" +
        "- Die Kundschaft der Nutzerin heisst nie 'Kundin' (Kundschaft, Leute, Interessenten).\n" +
        "- Keine fremden Namen (Mentorinnen, gekaufte Kurse) — nirgends, auch nicht als Verbot in Prüfregeln oder Code.\n" +
        "- Auch der System-Prompt selbst ist frei von Gegenüberstellungen „nicht/nie X, sondern Y“ und von ß.\n\n" +
        "AUFTRAG\nSchreib den Bauplan. Der System-Prompt ist vollständig und sofort einsetzbar (4'000 bis 9'000 Zeichen): " +
        "Rolle, für wen, das Wissen aus ihren Kursen ausformuliert, der Ablauf, das Ausgabeformat, die Verbote. " +
        "Der Auftrag für Claude Code ist ein fertiger Text zum Einfügen im Chat: welcher Ordner, welche Dateien, " +
        "welcher Ablauf, welche Prüfungen, lokal testen, dann ausliefern und die Adresse nennen. " +
        "Halte das Tool klein: höchstens fünf Schritte für die Nutzerin." +
        '\n\nAntworte nur als JSON: {"name": "...", "slug": "kleinbuchstaben-mit-strich", "plattform": "Vercel|Netlify", ' +
        '"warum_plattform": "ein Satz", "versprechen": "ein Satz, was die Nutzerin danach hat", ' +
        '"ablauf": [{"schritt": "Titel", "frage": "was die Nutzerin eingibt oder antippt"}], ' +
        '"ergebnis": "was das Tool am Schluss ausgibt", "system_prompt": "der ganze Text in Markdown", ' +
        '"pruefregeln": ["..."], "zugang": "Code und Durchgänge", ' +
        '"wissen_genutzt": ["welche ihrer Kurse und Begriffe drinstecken"], "auftrag": "der Auftrag für Claude Code"}';
      sampler.json(p, { modelTier: "complex", cache: false }).then(function (r) {
        if (!r || !r.system_prompt) throw { message: "leer zurückgekommen" };
        x.bauplan = r;
        x.bauplanStand = new Date().toISOString();
        x.bauplanQuellen = { eigen: w.eigen.quellen, fach: w.fach.quellen, stellen: w.eigen.anzahl + w.fach.anzahl };
        zaSichern(erg);
      }).catch(function (e) {
        x.bauplanFehler = (e && (e.code || e.message)) || "Fehler";
      }).then(function () { delete zaBauLaeuft[schluessel]; render(); });
    });
  }

  function zaBauplanAuftrag(x) {
    var b = x.bauplan || {};
    return (b.auftrag || "") +
      "\n\nAblauf für die Nutzerin:\n" + (b.ablauf || []).map(function (s, i) {
        return (i + 1) + ". " + s.schritt + " — " + s.frage;
      }).join("\n") +
      "\n\nErgebnis: " + (b.ergebnis || "") +
      "\nZugang: " + (b.zugang || "") +
      "\nPrüfregeln:\n" + (b.pruefregeln || []).map(function (r) { return "- " + r; }).join("\n") +
      "\n\nDen System-Prompt bitte wörtlich als lib/system-prompt.md übernehmen:\n\n" + (b.system_prompt || "");
  }

  /* Gegenprobe am fertigen Bauplan: das Tool wird verkauft, fremde Namen und
     Patricias Wortverbote duerfen nicht darin stehen. Am 31.10. stand im
     ersten Bauplan „Der Name Julia kommt nirgends vor“ als Pruefregel — damit
     waere der Name im Code eines verkauften Tools gelandet. */
  function zaBauplanFunde(b) {
    var t = (b.system_prompt || "") + "\n" + (b.auftrag || "") + "\n" + (b.pruefregeln || []).join("\n");
    var funde = [];
    if (/julia|trost|mentorin\s+[A-ZÄÖÜ]/i.test(t)) funde.push("fremder Name");
    /* „nie ß“ / „kein ß“ ist die Regel selbst, kein Fund */
    if (/ß/.test(t.replace(/(nie|kein|statt|ohne)\s+ß/gi, ""))) funde.push("ß statt ss");
    var kontrast = (b.system_prompt || "").replace(/„[^“]*“/g, "").match(/\b(nicht|nie|kein\w*)\b[^.!?\n]{0,80}[,.]\s*sondern\b/gi);
    if (kontrast) funde.push(kontrast.length + "× „nicht/nie X, sondern Y“ im System-Prompt");
    return funde;
  }

  function zaBauplanHtml(x, nr) {
    var b = x.bauplan, q = x.bauplanQuellen || {};
    var funde = zaBauplanFunde(b);
    return '<details class="za-plan" open><summary>Tool-Bauplan: ' + esc(b.name || x.name) +
      ' <span class="note">· ' + esc(b.plattform || "Vercel") + '</span></summary>' +
      (b.versprechen ? '<p><span class="za-lab">Danach hat sie</span>' + esc(b.versprechen) + '</p>' : "") +
      (b.ablauf && b.ablauf.length ? '<ol class="za-ablauf">' + b.ablauf.map(function (s) {
        return '<li><b>' + esc(s.schritt) + '</b> — ' + esc(s.frage) + '</li>';
      }).join("") + '</ol>' : "") +
      (b.ergebnis ? '<p><span class="za-lab">Ergebnis</span>' + esc(b.ergebnis) + '</p>' : "") +
      '<p><span class="za-lab">Wissen darin</span>' +
        esc((b.wissen_genutzt || []).join(" · ") || "–") +
        (q.eigen ? '<br><span class="note">Gefunden in deinen Kursen: ' + esc(q.eigen.join(", ") || "nichts") +
          (q.fach && q.fach.length ? ' · im Fachwissen: ' + esc(q.fach.join(", ")) : "") + '</span>' : "") + '</p>' +
      (b.plattform ? '<p class="note">' + esc(b.warum_plattform || "") + (b.zugang ? " · " + esc(b.zugang) : "") + '</p>' : "") +
      (funde.length ? '<p class="za-warn">⚠ Vor dem Bauen korrigieren: ' + esc(funde.join(" · ")) +
        ' — „Bauplan neu“ oder beim Einfügen Claude Code darauf hinweisen.</p>' : "") +
      '<details class="za-prompt"><summary>System-Prompt ansehen (' + (b.system_prompt || "").length + ' Zeichen)</summary>' +
        '<pre>' + esc(b.system_prompt || "") + '</pre></details>' +
      '<div class="za-fuss"><button class="btn primary" data-za-auftrag="' + nr + '">Auftrag für Claude Code kopieren</button>' +
        '<button class="btn" data-za-prompt="' + nr + '">System-Prompt kopieren</button>' +
        (downloads ? '<button class="btn ghost" data-za-datei="' + nr + '">Als Datei speichern</button>' : "") + '</div>' +
      '<p class="note">Einfügen im Chat mit Claude Code: Claude baut das Tool, testet es lokal und liefert es auf Vercel aus.</p>' +
      '</details>';
  }

  /* ---------- Uebergabe an „Angebot auf Knopfdruck“ ---------- */

  function zaUebergabe(erg, x) {
    var auftrag = {
      v: 1, rolle: x.rolle, name: x.name, preis: x.preis, normalpreis: x.normalpreis || null,
      tooltyp: x.tooltyp || "", problem: x.problem || "", kasse: x.kasse || "", bauen: x.bauen || "",
      rechnung: x.rechnung || "", zu: { name: erg.name, preis: erg.preis, link: erg.link || "" },
      tool: x.bauplan ? { name: x.bauplan.name, versprechen: x.bauplan.versprechen, ablauf: x.bauplan.ablauf,
                          ergebnis: x.bauplan.ergebnis, plattform: x.bauplan.plattform } : null
    };
    return "MLB-ZUSATZANGEBOT\n" + JSON.stringify(auftrag);
  }

  /* ---------- Anzeige ---------- */

  var ZA_ROLLEN = [
    { id: "bump", name: "Order Bump", wo: "Häkchen auf der Kasse, vor dem Bezahlen" },
    { id: "upsell", name: "Upsell", wo: "eigene Seite direkt nach dem Bezahlen" },
    { id: "downsell", name: "Downsell", wo: "wenn das Upsell abgelehnt wird" },
    { id: "crosssell", name: "Cross-Sell", wo: "danach: im Kurs, in der Fusszeile, in der Mail-Strecke" }
  ];

  function zaKarte(erg, x, nr) {
    var neu = x.art === "neu";
    var laeuft = zaBauLaeuft[erg.produkt + ":" + nr];
    return '<div class="za-karte' + (x.fehler && x.fehler.length ? " za-bruch" : "") + (x.bauplan ? " za-breit-karte" : "") + '">' +
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
      (x.hinweise && x.hinweise.length ? '<p class="za-hinw">' + esc(x.hinweise.join(" · ")) + '</p>' : "") +
      (x.bauplan ? zaBauplanHtml(x, nr) : "") +
      (x.bauplanFehler && !x.bauplan ? '<p class="za-warn">Bauplan hat nicht geklappt (' + esc(x.bauplanFehler) + ').</p>' : "") +
      (neu ? '<div class="za-fuss">' +
        (zaIstTool(x) ? '<button class="btn' + (x.bauplan ? "" : " primary") + '" data-za-bauplan="' + nr + '"' +
          (laeuft || !sampler ? " disabled" : "") + '>' +
          (laeuft ? "Claude baut den Plan …" : (x.bauplan ? "Bauplan neu" : "Tool-Bauplan erstellen")) + '</button>' : "") +
        '<button class="btn" data-za-bau="' + nr + '">Mit Knopfdruck bauen</button></div>' +
        '<p class="note">„Mit Knopfdruck bauen“ kopiert den Auftrag für die Seite „Angebot auf Knopfdruck“' +
        (zaIstTool(x) ? ', der Tool-Bauplan liefert System-Prompt und Auftrag für Vercel' : "") + '.</p>' : "") +
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
        if (x.hinweise && x.hinweise.length) t.push("  Hinweis: " + x.hinweise.join(" · "));
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
        esc(x.name) + ' · ' + esc(x.preis) + ' ' + esc(x.waehrung || "CHF") + '</option>';
    }).join("");

    var h = '<div class="page-head"><div><h1>Upsell-Ersteller</h1>' +
      '<p>Wähl ein Produkt. Du bekommst Vorschläge für Bump, Upsell, Downsell und Cross-Sell nach Julias Methode, ' +
      'aus dem, was du schon hast, oder als neues KI-Tool zum Bauen. Die Preis-Kette rechnet die Seite selbst nach.</p></div></div>' +
      '<div class="panel za-regel"><b>Die Kette:</b> Bump günstiger als das Hauptprodukt · Upsell teurer als der Bump ' +
      '(darf auch teurer sein als das Hauptprodukt) · Downsell günstiger als sein Upsell · Bump 30 bis 60 % rabattiert · ' +
      'Minikurse fix 39 · keine Geld-zurück-Garantie.</div>' +
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
          (erg.quelle ? ' · Grundlage: ' + esc(erg.quelle) : "") +
          (erg.wunsch ? ' · Wunsch: ' + esc(erg.wunsch) : "") +
          (brueche ? ' · <span class="za-warn">' + (brueche === 1 ? "1 Vorschlag bricht" : brueche + " Vorschläge brechen") + ' die Kette</span>' : ' · Kette eingehalten ✓') +
          ' <button class="btn ghost" id="za-kopie">Als Text kopieren</button></div>';
        if (erg.hinweis) h += '<div class="panel za-hinweis">' + esc(erg.hinweis) + '</div>';
        ZA_ROLLEN.forEach(function (r) {
          var karten = [];
          erg.vorschlaege.forEach(function (x, nr) { if (x.rolle === r.id) karten.push(zaKarte(erg, x, nr)); });
          if (!karten.length) return;
          h += '<h2 class="za-rolle">' + esc(r.name) + ' <span>' + esc(r.wo) + '</span></h2>' +
            '<div class="za-raster">' + karten.join("") + '</div>';
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
    if (ko) ko.onclick = function () { zaKopieren(zaAlsText(erg)); };

    function knopf(attr, tun) {
      main.querySelectorAll("[" + attr + "]").forEach(function (b) {
        b.onclick = function () { tun(erg.vorschlaege[Number(b.getAttribute(attr))], Number(b.getAttribute(attr))); };
      });
    }
    knopf("data-za-bauplan", function (x, nr) { zaBauplan(erg, nr); });
    knopf("data-za-bau", function (x) {
      zaKopieren(zaUebergabe(erg, x), "Kopiert. In „Angebot auf Knopfdruck“ bei „Aus dem Upsell-Ersteller einfügen“ hineinkleben.");
    });
    knopf("data-za-auftrag", function (x) { zaKopieren(zaBauplanAuftrag(x), "Auftrag kopiert — im Chat mit Claude Code einfügen."); });
    knopf("data-za-prompt", function (x) { zaKopieren((x.bauplan || {}).system_prompt || "", "System-Prompt kopiert."); });
    knopf("data-za-datei", function (x) {
      var slug = (x.bauplan && x.bauplan.slug) || "tool";
      downloads.save({ filename: "bauplan-" + slug + ".md", data: "# " + ((x.bauplan || {}).name || x.name) + "\n\n" + zaBauplanAuftrag(x) })
        .catch(function () { toast("Speichern ging nicht."); });
    });
  }
