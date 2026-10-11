"""
Das Cockpit vom Anzeige-Brett zum Arbeitswerkzeug ausbauen.

Fuenf Sachen, die Patricia gefehlt haben:

  1  **Dropdowns, die nach etwas aussehen.** Die Auswahlfelder in den Tabellen
     waren unsichtbar, bis man mit der Maus drueberfuhr — man sah nicht, wo
     ueberhaupt etwas auszuwaehlen ist.

  2  **Angebote mit Substanz.** Pro Angebot klappt jetzt eine Karte auf mit
     Kursinhalt, Order Bump, Upsell und Downsell. Diese Felder gehoeren
     Patricia und werden vom taeglichen Abgleich **nicht** angefasst — sie
     liegen in einem eigenen Dokument `daten/produkt-details`.

  3  **Mailtexte hinter jeder Automation.** Ein Klick auf die Automation
     zeigt, welche Mails darin haengen, mit Betreff und vollem Text. Die
     Mails werden erst beim Aufklappen geholt, damit das Cockpit schnell
     bleibt.

  4  **Suche ueber alles.** Ein Stichwort, und es kommt, wo im ganzen
     Workspace darueber geschrieben wurde — Grundlagen, Produkte, Funnel,
     Recherche. Der Index wird erst beim ersten Suchen geladen.

  5  **Ideenkasten.** Was noch nicht umgesetzt ist, an einem Ort, mit Status
     und Aufwand statt verstreut in Chats.

Aufruf:
  python scripts/cockpit/patch-arbeitswerkzeug.py [--pruefen]
"""
import io
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ERSETZUNGEN = []


def patch(name, alt, neu):
    ERSETZUNGEN.append((name, alt, neu))


# ==========================================================================
# 1 · Dropdowns und Eingabefelder sichtbar machen
# ==========================================================================
patch("Auswahlfelder sehen aus wie Auswahlfelder",
      """  .trow input, .trow select, .trow textarea {
    width: 100%; background: transparent; border: 1px solid transparent;
    border-radius: 6px; padding: 5px 7px; font-size: 13px;
  }""",
      """  .trow input, .trow select, .trow textarea {
    width: 100%; background: transparent; border: 1px solid transparent;
    border-radius: 6px; padding: 5px 7px; font-size: 13px;
  }
  /* Ein Auswahlfeld muss man sehen, bevor man mit der Maus draufkommt:
     eigener Grund, eigener Rand, eigenes Pfeilchen. */
  .trow select {
    -webkit-appearance: none; appearance: none;
    background-color: var(--surface-2);
    border-color: var(--line);
    padding-right: 22px; cursor: pointer;
    background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='7' viewBox='0 0 10 7'%3E%3Cpath d='M1 1l4 4 4-4' fill='none' stroke='%234d6076' stroke-width='1.6' stroke-linecap='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 7px center;
  }
  .trow select:hover { border-color: var(--line-strong); }
  .trow select:focus { outline: 2px solid var(--teal-soft); border-color: var(--teal); }""")

# ==========================================================================
# 2 · Ideenkasten als eigene Liste
# ==========================================================================
patch("Ideenkasten in die Datenschluessel",
      '  var DOC_KEYS = ["posts", "ideen", "leads", "team", "produkte", "funnel", "launches", "zahlen"];',
      '  var DOC_KEYS = ["posts", "ideen", "leads", "team", "produkte", "funnel", "launches", "zahlen", "ideenkasten"];')

patch("Ideenkasten im Startzustand",
      '  var state = { posts: [], ideen: [], leads: [], team: [], produkte: [], funnel: [], launches: [], zahlen: [], karussells: [], storys: [], reels: [] };',
      '  var state = { posts: [], ideen: [], leads: [], team: [], produkte: [], funnel: [], launches: [], zahlen: [], ideenkasten: [], karussells: [], storys: [], reels: [] };\n'
      '  /* Kursinhalt, Bump, Upsell, Downsell je Angebot. Gehoert Patricia,\n'
      '     der taegliche Abgleich fasst dieses Dokument nicht an. */\n'
      '  var produktdetails = {};')

patch("Ideenkasten als Tabelle",
      """    produkte: {
      titel: "Angebote",""",
      """    ideenkasten: {
      titel: "Ideenkasten",
      unter: "Was noch nicht umgesetzt ist. Nicht jede Idee muss gemacht werden — aber keine soll verloren gehen.",
      neu: function () { return { id: uid("ik"), idee: "", bereich: "Funnel", status: "Idee", aufwand: "mittel", notiz: "" }; },
      sort: "status",
      cols: [
        { k: "idee", l: "Idee", t: "text", w: "minmax(260px, 1fr)" },
        { k: "bereich", l: "Bereich", t: "select", opts: ["Funnel", "Produkt", "Content", "Technik", "doTERRA", "Website", "Sonstiges"], w: "145px" },
        { k: "status", l: "Status", t: "pill", opts: ["Idee", "Als nächstes", "In Arbeit", "Erledigt", "Verworfen"], w: "142px" },
        { k: "aufwand", l: "Aufwand", t: "select", opts: ["klein", "mittel", "gross"], w: "115px" },
        { k: "notiz", l: "Notiz", t: "text", w: "minmax(220px, 1fr)" }
      ]
    },
    produkte: {
      titel: "Angebote",""")

patch("Ideenkasten in die Navigation",
      '    { id: "ideen", label: "Ideen & Hooks" },',
      '    { id: "ideen", label: "Ideen & Hooks" },\n'
      '    { id: "ideenkasten", label: "Ideenkasten" },')

patch("Suche in die Navigation",
      '    { g: "Grundlagen" },\n'
      '    { id: "wissen", label: "Mein Wissen" }',
      '    { g: "Grundlagen" },\n'
      '    { id: "wissen", label: "Mein Wissen" },\n'
      '    { id: "suche", label: "Suchen" }')

# „Verworfen" braucht einen zurueckgenommenen Ton — sonst sieht eine
# beerdigte Idee aus wie eine offene.
patch("Blasser Ton fuer Verworfenes",
      '  select.pill[data-tone="new"] { background: var(--teal-soft); color: var(--teal); border-color: transparent !important; }',
      '  select.pill[data-tone="new"] { background: var(--teal-soft); color: var(--teal); border-color: transparent !important; }\n  select.pill[data-tone="aus"] { background: var(--surface-2); color: var(--ink-soft); border-color: transparent !important; opacity: 0.75; }')

patch("Farbton fuer die neuen Status",
      '"Idee": "new", "Neu": "new", "Offen": "new"',
      '"Idee": "new", "Neu": "new", "Offen": "new",\n'
      '    "Als nächstes": "mid", "Erledigt": "go", "Verworfen": "aus"')

# ==========================================================================
# 3 · Angebote mit Kursinhalt, Bump, Upsell, Downsell
# ==========================================================================
patch("Angebots-Ansicht mit Detailkarten",
      """  /* =========================================================
     Listen & Automationen — Abbild aus ActiveCampaign
     ========================================================= */""",
      """  /* =========================================================
     Angebote — Tabelle plus das, was im Angebot drinsteckt
     ========================================================= */
  var offenesAngebot = null;

  var DETAILFELDER = [
    { k: "inhalt", l: "Das steckt drin", ph: "Module, Lektionen, Arbeitsblätter — was die Kundin bekommt", hoch: 5 },
    { k: "bump", l: "Order Bump", ph: "Was beim Checkout angehakt werden kann, mit Preis", hoch: 2 },
    { k: "upsell", l: "Upsell danach", ph: "Was direkt nach dem Kauf angeboten wird", hoch: 2 },
    { k: "downsell", l: "Downsell", ph: "Was kommt, wenn der Upsell abgelehnt wird", hoch: 2 },
    { k: "notiz", l: "Notiz", ph: "Alles, was du dir sonst merken willst", hoch: 2 }
  ];

  function detailSpeichern() {
    clearTimeout(saveTimers.produktdetails);
    saveTimers.produktdetails = setTimeout(function () {
      lsSet("produkt-details", produktdetails);
      if (!db) return;
      db.doc("daten/produkt-details")
        .set({ werte: produktdetails, updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function renderProdukte(main) {
    renderTable(main, "produkte");

    var box = document.createElement("div");
    box.className = "detailbox";
    box.innerHTML = '<h2>Was in den Angeboten drinsteckt</h2>' +
      '<p class="note">Kursinhalt, Order Bump und Up-/Downsell trägst du hier selbst ein. ' +
      'Der tägliche Abgleich überschreibt diese Felder nicht — nur Preis, Link und Stand kommen von aussen.</p>';
    main.appendChild(box);

    if (!state.produkte.length) {
      box.innerHTML += '<div class="empty">Noch keine Angebote.</div>';
      return;
    }

    state.produkte.forEach(function (a) {
      var d = produktdetails[a.id] || (produktdetails[a.id] = {});
      var gefuellt = DETAILFELDER.filter(function (f) { return String(d[f.k] || "").trim(); }).length;

      var karte = document.createElement("div");
      karte.className = "dkarte" + (offenesAngebot === a.id ? " auf" : "");
      karte.innerHTML =
        '<button class="dkopf"><span class="dpfeil">▸</span>' +
        '<span class="dname">' + esc(a.name || "Ohne Namen") + '</span>' +
        '<span class="dstufe">' + esc(a.stufe || "") + '</span>' +
        '<span class="note">' + (gefuellt ? gefuellt + " von " + DETAILFELDER.length + " Feldern" : "noch leer") + '</span>' +
        '</button><div class="dkoerper"></div>';

      karte.querySelector(".dkopf").onclick = function () {
        offenesAngebot = (offenesAngebot === a.id) ? null : a.id;
        render();
      };

      if (offenesAngebot === a.id) {
        var koerper = karte.querySelector(".dkoerper");
        DETAILFELDER.forEach(function (f) {
          var feld = document.createElement("div");
          feld.className = "dfeld";
          var lab = document.createElement("label");
          lab.textContent = f.l;
          var ta = document.createElement("textarea");
          ta.rows = f.hoch;
          ta.placeholder = f.ph;
          ta.value = d[f.k] || "";
          ta.oninput = function () { d[f.k] = ta.value; detailSpeichern(); };
          feld.appendChild(lab); feld.appendChild(ta);
          koerper.appendChild(feld);
        });
        // Was ThriveCart wirklich am Checkout haengen hat. Das ist Befund,
        // kein Eingabefeld — deshalb steht es ueber den Notizfeldern.
        var tc = [["Order Bump", a.tc_bumps], ["Upsell", a.tc_upsells],
                  ["Downsell", a.tc_downsells]].filter(function (r) {
          return r[1] && r[1].length;
        });
        if (tc.length) {
          var kasten = document.createElement("div");
          kasten.className = "tcbefund";
          kasten.innerHTML = '<div class="tckopf">Am Checkout hängt</div>' +
            tc.map(function (r) {
              return '<div class="tczeile"><span>' + esc(r[0]) + '</span><span>' +
                     r[1].map(esc).join(" · ") + '</span></div>';
            }).join("");
          koerper.insertBefore(kasten, koerper.firstChild);
        }

        if (a.bumphinweis) {
          var hw = document.createElement("p");
          hw.className = "note";
          hw.textContent = "Aus deiner Linkliste: " + a.bumphinweis;
          koerper.appendChild(hw);
        }
        if (a.link) {
          var lk = document.createElement("p");
          lk.className = "note";
          lk.innerHTML = 'Checkout: <a href="' + esc(a.link) + '" target="_blank" rel="noopener">' + esc(a.link) + '</a>';
          koerper.appendChild(lk);
        }
      }
      box.appendChild(karte);
    });
  }

  /* =========================================================
     Suchen — ein Stichwort, und es kommt, wo es vorkam
     ========================================================= */
  var suchIndex = null;       // null = noch nicht geholt
  var suchLaeuft = false;
  var suchWort = "";

  function suchIndexHolen(fertig) {
    if (suchIndex || suchLaeuft) { fertig(); return; }
    if (!db) { fertig(); return; }
    suchLaeuft = true;
    db.collection("suche").limit(40).get().then(function (qs) {
      var alles = [];
      qs.docs.forEach(function (doc) {
        (doc.data() || {}).items && (alles = alles.concat(doc.data().items));
      });
      suchIndex = alles;
      suchLaeuft = false;
      fertig();
    }).catch(function () { suchLaeuft = false; suchIndex = []; fertig(); });
  }

  function suchTreffer(wort) {
    var w = wort.toLowerCase().trim();
    if (!w || !suchIndex) return [];
    var raus = [];
    for (var i = 0; i < suchIndex.length; i++) {
      var x = suchIndex[i];
      var imTitel = (x.t || "").toLowerCase().indexOf(w) >= 0;
      if (imTitel || (x.a || "").toLowerCase().indexOf(w) >= 0) {
        raus.push({ x: x, rang: imTitel ? 0 : 1 });
      }
      if (raus.length > 400) break;
    }
    raus.sort(function (a, b) { return a.rang - b.rang; });
    return raus.map(function (r) { return r.x; });
  }

  function markiere(text, wort) {
    var w = wort.trim();
    if (!w) return esc(text);
    var i = text.toLowerCase().indexOf(w.toLowerCase());
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + w.length)) +
           '</mark>' + esc(text.slice(i + w.length));
  }

  function renderSuche(main) {
    main.innerHTML =
      '<div class="page-head"><div><h1>Suchen</h1>' +
      '<p>Ein Stichwort, und du siehst, wo im ganzen Workspace darüber geschrieben wurde — Grundlagen, Produkte, Funnel, Recherche.</p></div></div>' +
      '<div class="suchleiste"><input id="suchfeld" type="search" placeholder="zum Beispiel: Keyword, Hybridmodell, Orderbump, Energie" autocomplete="off"></div>' +
      '<div id="suchraus"></div>';

    var feld = main.querySelector("#suchfeld");
    var raus = main.querySelector("#suchraus");
    feld.value = suchWort;

    function zeigen() {
      if (suchIndex === null) {
        raus.innerHTML = '<div class="panel"><div class="empty">Der Suchindex wird geholt …</div></div>';
        suchIndexHolen(function () { if (activeTab === "suche") zeigen(); });
        return;
      }
      if (!suchIndex.length) {
        raus.innerHTML = '<div class="panel"><div class="empty">Kein Suchindex da. Der tägliche Abgleich legt ihn an.</div></div>';
        return;
      }
      if (!suchWort.trim()) {
        raus.innerHTML = '<p class="note">' + suchIndex.length + ' Abschnitte durchsuchbar.</p>';
        return;
      }
      var tr = suchTreffer(suchWort);
      if (!tr.length) {
        raus.innerHTML = '<div class="panel"><div class="empty">Nichts gefunden zu „' + esc(suchWort) + '".</div></div>';
        return;
      }
      var h = '<p class="note">' + tr.length + ' Fundstellen' + (tr.length > 60 ? ' — die ersten 60' : '') + '</p>';
      tr.slice(0, 60).forEach(function (x) {
        // Fremdes Material bekommt eine andere Farbe. Es soll nie aussehen
        // wie Patricias eigenes — was hier steht, ist ein Wegweiser ins
        // Original, kein Text, den man verwenden darf.
        var fremd = /^Fremd/.test(x.b || "");
        h += '<div class="sxtreffer' + (fremd ? " fremd" : "") + '">' +
             '<div class="sxkopf"><span class="sxbereich' + (fremd ? " fremd" : "") +
             '">' + esc(x.b || "") + '</span>' +
             '<span class="sxtitel">' + markiere(x.t || "", suchWort) + '</span></div>' +
             '<p class="sxauszug">' + markiere(x.a || "", suchWort) + '</p>' +
             '<p class="sxpfad">' +
             (/^https?:/.test(x.d || "")
               ? '<a href="' + esc(x.d) + '" target="_blank" rel="noopener">' +
                 esc(x.d.replace(/^https?:\/\//, "").slice(0, 72)) + ' ↗</a>'
               : esc(x.d || "")) + '</p></div>';
      });
      raus.innerHTML = h;
    }

    var warten;
    feld.oninput = function () {
      suchWort = feld.value;
      clearTimeout(warten);
      warten = setTimeout(zeigen, 180);
    };
    zeigen();
    feld.focus();
  }

  /* =========================================================
     Listen & Automationen — Abbild aus ActiveCampaign
     ========================================================= */""")

# ==========================================================================
# 4 · Mailtexte hinter den Automationen
# ==========================================================================
patch("Mails hinter der Automation aufklappen",
      """  function renderMailings(main) {""",
      """  var offeneAutomation = null;
  var mailtexte = {};            // Automations-Nummer -> Liste der Mails
  var mailsGeholt = {};

  function mailsHolen(nummer) {
    if (!db || mailsGeholt[nummer]) return;
    mailsGeholt[nummer] = true;
    db.doc("mails/" + nummer).get().then(function (snap) {
      if (!snap.exists) { mailtexte[nummer] = []; }
      else { mailtexte[nummer] = (snap.data() || {}).items || []; }
      if (activeTab === "mailings") render();
    }).catch(function () { mailtexte[nummer] = []; });
  }

  function mailListe(nummer) {
    var mails = mailtexte[nummer];
    if (!mails) { mailsHolen(nummer); return '<div class="empty">Mails werden geholt …</div>'; }
    if (!mails.length) return '<div class="empty">In dieser Automation stecken keine Mails.</div>';
    return mails.map(function (m) {
      return '<div class="mailkarte">' +
        '<div class="mailkopf"><strong>' + esc(m.betreff || m.name || "Ohne Betreff") + '</strong>' +
        (m.gebaut ? '<span class="note">' + esc(mailDatum(m.gebaut)) + '</span>' : "") + '</div>' +
        '<pre class="mailtext">' + esc(m.text || "(kein Text hinterlegt)") + '</pre></div>';
    }).join("");
  }

  function renderMailings(main) {""")

patch("Automations-Zeile aufklappbar machen",
      """    main.querySelector("#mailbody").innerHTML =
      mailTabelle("Deine Listen",
        [{ k: "name", l: "Liste", w: "minmax(240px, 1fr)" },
         { k: "kontakte", l: "Kontakte", w: "110px" },
         { k: "nummer", l: "Nr.", w: "70px" },
         { k: "seit", l: "Angelegt", w: "130px", f: function (r) { return esc(mailDatum(r.seit)); } }],
        listen, "Noch nichts abgeglichen.") +
      mailTabelle("Deine Automationen",
        [{ k: "name", l: "Automation", w: "minmax(280px, 1fr)" },
         { k: "status", l: "Status", w: "110px",
           f: function (r) { return '<span class="flag ' + (r.status === "aktiv" ? "ok" : "bad") + '">' + esc(r.status) + '</span>'; } },
         { k: "nummer", l: "Nr.", w: "70px" },
         { k: "seit", l: "Gebaut", w: "130px", f: function (r) { return esc(mailDatum(r.seit)); } }],
        autos, "Noch nichts abgeglichen.");
  }""",
      """    var koerper = main.querySelector("#mailbody");
    koerper.innerHTML =
      mailTabelle("Deine Listen",
        [{ k: "name", l: "Liste", w: "minmax(240px, 1fr)" },
         { k: "kontakte", l: "Kontakte", w: "110px" },
         { k: "nummer", l: "Nr.", w: "70px" },
         { k: "seit", l: "Angelegt", w: "130px", f: function (r) { return esc(mailDatum(r.seit)); } }],
        listen, "Noch nichts abgeglichen.");

    // Automationen als aufklappbare Karten — darin stehen die Mailtexte.
    var ab = document.createElement("div");
    ab.className = "panel";
    ab.innerHTML = '<h2>Deine Automationen</h2>' +
      '<p class="note">Klick auf eine Automation, dann siehst du die Mails, die darin hängen — mit vollem Text.</p>';
    koerper.appendChild(ab);

    if (!autos.length) {
      ab.innerHTML += '<div class="empty">Noch nichts abgeglichen.</div>';
      return;
    }

    autos.forEach(function (a) {
      var karte = document.createElement("div");
      karte.className = "dkarte" + (offeneAutomation === a.nummer ? " auf" : "");
      karte.innerHTML =
        '<button class="dkopf"><span class="dpfeil">▸</span>' +
        '<span class="dname">' + esc(a.name) + '</span>' +
        '<span class="flag ' + (a.status === "aktiv" ? "ok" : "bad") + '">' + esc(a.status) + '</span>' +
        '<span class="note">' + (a.mails ? a.mails + (a.mails === 1 ? " Mail" : " Mails") : "keine Mails") +
        ' · Nr. ' + esc(String(a.nummer)) + '</span></button>' +
        '<div class="dkoerper"></div>';

      karte.querySelector(".dkopf").onclick = function () {
        offeneAutomation = (offeneAutomation === a.nummer) ? null : a.nummer;
        render();
      };
      if (offeneAutomation === a.nummer) {
        karte.querySelector(".dkoerper").innerHTML = mailListe(a.nummer);
      }
      ab.appendChild(karte);
    });
  }""")

# ==========================================================================
# 5 · Stil fuer Detailkarten, Mails und Suche
# ==========================================================================
patch("Stil fuer die neuen Bausteine",
      "  .wk-regler { display: grid; grid-template-columns: 78px 1fr; gap: 6px; align-items: center; }",
      """  /* ---------- aufklappbare Karten (Angebote, Automationen) ---------- */
  .detailbox { margin-top: 26px; }
  .detailbox h2 { font-family: var(--display); font-size: 17px; margin: 0 0 4px; font-weight: normal; }
  .dkarte { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); margin-top: 8px; overflow: hidden; }
  .dkarte.auf { border-color: var(--line-strong); box-shadow: var(--shadow); }
  .dkopf {
    display: flex; align-items: center; gap: 10px; width: 100%;
    background: none; border: 0; padding: 11px 14px; cursor: pointer;
    text-align: left; font: inherit; color: inherit;
  }
  .dkopf:hover { background: var(--surface-2); }
  .dpfeil { color: var(--ink-soft); transition: transform 0.14s; flex: none; }
  .dkarte.auf .dpfeil { transform: rotate(90deg); }
  .dname { font-weight: 600; font-size: 14px; }
  .dstufe {
    font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--ink-soft); background: var(--surface-2);
    padding: 2px 8px; border-radius: 999px; flex: none;
  }
  .dkopf .note { margin-left: auto; flex: none; }
  .dkoerper:not(:empty) { padding: 4px 14px 16px; border-top: 1px solid var(--line); }
  .dfeld { margin-top: 12px; }
  .dfeld label { display: block; font-size: 11px; letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: 4px; }
  .dfeld textarea {
    width: 100%; background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 8px 10px; font: inherit; font-size: 13px;
    line-height: 1.5; resize: vertical;
  }
  .dfeld textarea:focus { outline: 2px solid var(--teal-soft); border-color: var(--teal); }

  /* ---------- Befund aus ThriveCart ---------- */
  .tcbefund {
    background: var(--teal-soft); border-radius: 8px;
    padding: 10px 12px; margin-top: 12px;
  }
  .tckopf {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--teal); margin-bottom: 6px;
  }
  .tczeile { display: grid; grid-template-columns: 96px 1fr; gap: 8px; font-size: 13px; padding: 2px 0; }
  .tczeile > span:first-child { color: var(--ink-soft); }

  /* ---------- Mailtexte ---------- */
  .mailkarte { border: 1px solid var(--line); border-radius: 8px; margin-top: 10px; background: var(--ground); }
  .mailkopf { display: flex; gap: 10px; align-items: baseline; padding: 9px 12px; border-bottom: 1px solid var(--line); }
  .mailkopf .note { margin-left: auto; }
  .mailtext {
    margin: 0; padding: 12px; font: inherit; font-size: 13px; line-height: 1.6;
    white-space: pre-wrap; word-break: break-word; max-height: 340px; overflow: auto;
  }

  /* ---------- Suche ---------- */
  .suchleiste { margin-bottom: 16px; }
  .suchleiste input {
    width: 100%; max-width: 560px; background: var(--surface);
    border: 1px solid var(--line-strong); border-radius: 999px;
    padding: 11px 18px; font: inherit; font-size: 15px;
  }
  .suchleiste input:focus { outline: 2px solid var(--teal-soft); border-color: var(--teal); }
  .sxtreffer { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 11px 14px; margin-top: 8px; }
  .sxkopf { display: flex; gap: 9px; align-items: baseline; flex-wrap: wrap; }
  .sxbereich {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--teal); background: var(--teal-soft); padding: 2px 8px; border-radius: 999px; flex: none;
  }
  .sxtitel { font-weight: 600; font-size: 14px; }
  .sxauszug { margin: 6px 0 4px; font-size: 13px; line-height: 1.55; color: var(--ink-soft); }
  .sxpfad { margin: 0; font-size: 11px; color: var(--ink-soft); opacity: 0.75; }
  .sxpfad a { color: var(--teal); opacity: 1; }
  .sxtreffer.fremd { border-left: 3px solid var(--orange); }
  .sxbereich.fremd { color: var(--orange); background: var(--orange-soft); }
  mark { background: var(--orange-soft); color: inherit; border-radius: 3px; padding: 0 2px; }

  .wk-regler { display: grid; grid-template-columns: 78px 1fr; gap: 6px; align-items: center; }""")

# ==========================================================================
# 6 · Anschliessen
# ==========================================================================
patch("Neue Ansichten an den Render-Dispatcher",
      '    else if (activeTab === "mailings") renderMailings(main);',
      '    else if (activeTab === "mailings") renderMailings(main);\n'
      '    else if (activeTab === "produkte") renderProdukte(main);\n'
      '    else if (activeTab === "suche") renderSuche(main);')

patch("Angebots-Details aus der Datenbank holen",
      """      db.doc("daten/mailings").onSnapshot(function (snap) {""",
      """      db.doc("daten/produkt-details").onSnapshot(function (snap) {
        if (!snap.exists) return;
        produktdetails = (snap.data() || {}).werte || {};
        lsSet("produkt-details", produktdetails);
        if (activeTab === "produkte") render();
      }, function () {});
      db.doc("daten/mailings").onSnapshot(function (snap) {""")

patch("Angebots-Details beim Start laden",
      '  Object.assign(mailings, lsGet("mailings", {}) || {});',
      '  Object.assign(mailings, lsGet("mailings", {}) || {});\n'
      '  produktdetails = lsGet("produkt-details", {}) || {};')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:160]))
        if s.count(alt) > 1:
            sys.exit("Anker mehrdeutig (%dx) fuer: %s" % (s.count(alt), name))
        s = s.replace(alt, neu, 1)
        print("  OK  %s" % name)
    print("\nLaenge %d -> %d (%+d)" % (vorher, len(s), len(s) - vorher))
    if nur_pruefen:
        print("PRUEFLAUF — nichts geschrieben.")
        return
    io.open(DATEI, "w", encoding="utf-8").write(s)
    print("Geschrieben: %s" % DATEI)


if __name__ == "__main__":
    main()
