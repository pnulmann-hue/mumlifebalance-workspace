"""
Der Reiter „Links & Material" — der wichtigste im ganzen Cockpit.

Patricia: „ich muss z.B. auch immer die links suchen wenn ich in der story was
verlinken will. das nervt übelst."

Genau dafuer ist diese Ansicht gebaut, und sie ist auf **einen einzigen
Handgriff** ausgelegt: Stichwort tippen, auf „kopieren" tippen, in die Story
einsetzen. Deshalb steht der Reiter ganz oben unter „Übersicht" und nicht
irgendwo unter Business — er wird taeglich gebraucht, die anderen nicht.

Was je Angebot zusammensteht:
  Checkout-Link · Landingpage · Kommentar-Stichwort · Preis · hinterlegte PDFs

🚨 **Fehlt ein Link, steht das da** — als sichtbare Luecke, nicht als geratene
Adresse. Ein toter Link in einer Story kostet mehr als eine ehrliche Luecke.

🚨 **Die Quelle ist `context/link-uebersicht.md`**, nicht das Cockpit. Wer hier
einen Link falsch findet, korrigiert ihn dort und laesst
`linkzentrale-bauen.py` laufen.

Aufruf:
  python scripts/cockpit/patch-linkzentrale.py [--pruefen]
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


patch("Speicher fuer die Links",
      '  var katalog = null;\n  var katalogFilter = "";',
      '  var katalog = null;\n'
      '  var katalogFilter = "";\n'
      '  /* Alle Links gebuendelt — die meistgebrauchte Ansicht. */\n'
      '  var links = null;\n'
      '  var linkFilter = "";')

patch("Reiter ganz oben",
      '    { id: "uebersicht", label: "Übersicht" },',
      '    { id: "uebersicht", label: "Übersicht" },\n'
      '    { id: "links", label: "Links & Material" },')

patch("Render-Dispatcher",
      '    else if (activeTab === "katalog") renderKatalog(main);',
      '    else if (activeTab === "katalog") renderKatalog(main);\n'
      '    else if (activeTab === "links") renderLinks(main);')

patch("Die Link-Ansicht",
      """  function kettenSpeichern() {""",
      """  /* Kopieren muss ueberall gleich funktionieren — auch dort, wo die
     Zwischenablage gesperrt ist. Deshalb erst der moderne Weg, dann der alte
     ueber ein verstecktes Feld. */
  function inDieZwischenablage(text, knopf) {
    function geschafft() {
      var alt = knopf.textContent;
      knopf.textContent = "kopiert ✓";
      knopf.classList.add("fertig");
      setTimeout(function () {
        knopf.textContent = alt;
        knopf.classList.remove("fertig");
      }, 1400);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      // Wenn der Browser die Freigabe still verschluckt, kommt die Zusage nie
      // zurueck — und Patricia steht ohne jede Rueckmeldung da. Deshalb ein
      // Zeitlimit daneben, nach dem der alte Weg uebernimmt.
      var erledigt = false;
      var wecker = setTimeout(function () {
        if (!erledigt) { erledigt = true; altKopieren(text, geschafft); }
      }, 700);
      navigator.clipboard.writeText(text).then(function () {
        if (erledigt) return;
        erledigt = true; clearTimeout(wecker); geschafft();
      }, function () {
        if (erledigt) return;
        erledigt = true; clearTimeout(wecker); altKopieren(text, geschafft);
      });
      return;
    }
    altKopieren(text, geschafft);
  }

  function altKopieren(text, fertig) {
    var feld = document.createElement("textarea");
    feld.value = text;
    feld.style.position = "fixed";
    feld.style.opacity = "0";
    document.body.appendChild(feld);
    feld.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) {}
    feld.remove();
    if (ok) fertig(); else toast("Kopieren ging nicht — Link von Hand markieren.");
  }

  function kopierZeile(lab, wert, istLink) {
    var zeile = document.createElement("div");
    zeile.className = "lzzeile";

    var marke = document.createElement("span");
    marke.className = "lzlab";
    marke.textContent = lab;
    zeile.appendChild(marke);

    var wertfeld = document.createElement("span");
    wertfeld.className = "lzwert";
    if (istLink) {
      var a = document.createElement("a");
      a.href = wert;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = wert.replace(/^https?:\\/\\//, "");
      wertfeld.appendChild(a);
    } else {
      wertfeld.textContent = wert;
      wertfeld.classList.add("stichwort");
    }
    zeile.appendChild(wertfeld);

    var knopf = document.createElement("button");
    knopf.className = "lzkopie";
    knopf.textContent = "kopieren";
    knopf.onclick = function () { inDieZwischenablage(wert, knopf); };
    zeile.appendChild(knopf);
    return zeile;
  }

  function renderLinks(main) {
    if (!links) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Links & Material</h1>' +
        '<p>Alle Links gebündelt, zum Kopieren.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch nichts da. Die Liste ' +
        'entsteht aus deiner Link-Übersicht.</div></div>';
      return;
    }

    var alle = links.eintraege || [];
    var mitLink = alle.filter(function (e) { return e.link; }).length;
    var luecken = alle.filter(function (e) { return !e.link; }).length;
    var tot = alle.filter(function (e) { return e.status === "tot"; }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Links & Material</h1>' +
      '<p>Stichwort tippen, auf <strong>kopieren</strong> tippen, in die Story ' +
      'einsetzen. Checkout-Links, Landingpages, Kommentar-Stichwörter und die ' +
      'hinterlegten PDFs — alles an einer Stelle.</p></div></div>' +
      '<div class="tiles">' +
      tile("Links", mitLink, "geprüft und live") +
      tile("Lücken", luecken, luecken ? "laufen über ManyChat oder fehlen" : "alles hat einen Link") +
      tile("Tot", tot, tot ? "nicht verlinken!" : "keiner tot") +
      '</div>' +
      '<div class="suchleiste"><input id="lzfeld" type="search" autocomplete="off" ' +
      'placeholder="Suchen — zum Beispiel Storyideen, ENERGIE, Starterguide, MBA"></div>' +
      '<div id="lzraus"></div>';

    var feld = main.querySelector("#lzfeld");
    var raus = main.querySelector("#lzraus");
    feld.value = linkFilter;

    function zeigen() {
      var w = linkFilter.toLowerCase().trim();
      raus.innerHTML = "";

      (links.gruppen || []).forEach(function (g) {
        var drin = alle.filter(function (e) {
          if (e.gruppe !== g.id) return false;
          if (!w) return true;
          return (e.name + " " + e.keyword + " " + e.link).toLowerCase()
            .indexOf(w) >= 0;
        });
        if (!drin.length) return;

        var block = document.createElement("div");
        block.className = "panel lzblock";
        block.innerHTML = '<h2>' + esc(g.name) +
          ' <span class="note">· ' + esc(g.hinweis) + '</span></h2>';

        drin.forEach(function (e) {
          var karte = document.createElement("div");
          karte.className = "lzkarte" + (e.status === "tot" ? " tot" : "");

          var kopf = document.createElement("div");
          kopf.className = "lzkopf";
          var preis = e.tc_preis ? preisText(e.tc_preis, e.waehrung)
                                 : (e.preis || "");
          kopf.innerHTML = '<span class="lzname">' + esc(e.name) + '</span>' +
            (preis ? '<span class="lzpreis">' + esc(preis) + '</span>' : "") +
            (e.status === "tot"
              ? '<span class="flag bad">existiert nicht</span>' : "") +
            (e.status === "achtung"
              ? '<span class="flag bad">prüfen</span>' : "");
          karte.appendChild(kopf);

          if (e.keyword) {
            karte.appendChild(kopierZeile("Stichwort", e.keyword, false));
          }
          if (e.link) {
            var art = e.link.indexOf("thrivecart") >= 0 ? "Checkout"
                    : (e.link.indexOf("doterra.me") >= 0 ? "Warenkorb"
                    : "Seite");
            karte.appendChild(kopierZeile(art, e.link, true));
          } else {
            var luecke = document.createElement("div");
            luecke.className = "lzzeile";
            luecke.innerHTML = '<span class="lzlab">Link</span>' +
              '<span class="lzwert lzfehlt">' +
              esc(e.wortlaut || "kein Link hinterlegt") + '</span>';
            karte.appendChild(luecke);
          }

          (e.dateien || []).forEach(function (d) {
            var zeile = document.createElement("div");
            zeile.className = "lzzeile";
            zeile.innerHTML = '<span class="lzlab">Datei</span>' +
              '<span class="lzwert"><a class="vkdatei" href="' + esc(d.blob) +
              '" target="_blank" rel="noopener">' + esc(d.name) +
              (d.seiten ? " · " + d.seiten + " Seiten" : "") + '</a></span>';
            karte.appendChild(zeile);
          });

          if (e.hinweis && (e.status === "achtung" || e.status === "tot")) {
            var h = document.createElement("p");
            h.className = "note";
            h.style.margin = "6px 0 0";
            h.textContent = e.hinweis;
            karte.appendChild(h);
          }

          block.appendChild(karte);
        });
        raus.appendChild(block);
      });

      if (!raus.children.length) {
        raus.innerHTML = '<div class="panel"><div class="empty">Nichts gefunden.</div></div>';
      }
    }

    var warten;
    feld.oninput = function () {
      linkFilter = feld.value;
      clearTimeout(warten);
      warten = setTimeout(zeigen, 140);
    };
    zeigen();
    feld.focus();

    var fuss = document.createElement("p");
    fuss.className = "note";
    fuss.style.marginTop = "14px";
    fuss.textContent = "Stand " + mailDatum(links.stand) +
      " · Quelle ist " + (links.quelle || "die Link-Übersicht") +
      ". Stimmt ein Link nicht, wird er dort korrigiert — nicht hier.";
    main.appendChild(fuss);
  }

  function kettenSpeichern() {""")

patch("Stil fuer die Link-Zentrale",
      "  /* ---------- Angebots-Katalog ---------- */",
      """  /* ---------- Links & Material ---------- */
  .lzblock { margin-bottom: 16px; }
  .lzkarte {
    border-top: 1px solid var(--line); padding: 11px 0 9px;
  }
  .lzblock .lzkarte:first-of-type { border-top: 0; }
  .lzkarte.tot { opacity: 0.6; }
  .lzkopf { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; margin-bottom: 6px; }
  .lzname { font-size: 14px; font-weight: 600; }
  .lzpreis {
    font-size: 12px; font-variant-numeric: tabular-nums; color: var(--teal);
    background: var(--teal-soft); padding: 1px 9px; border-radius: 999px;
  }
  .lzzeile {
    display: grid; grid-template-columns: 82px 1fr 84px; gap: 10px;
    align-items: center; padding: 3px 0;
  }
  .lzlab {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); text-align: right;
  }
  .lzwert { font-size: 13px; min-width: 0; overflow-wrap: anywhere; }
  /* Nicht den Datei-Knopf mitfaerben: .lzwert a ist spezifischer als
     .vkdatei und machte den Text teal auf teal — also unsichtbar. */
  .lzwert a:not(.vkdatei) { color: var(--teal); text-decoration: none; }
  .lzwert a:not(.vkdatei):hover { text-decoration: underline; }
  .lzwert.stichwort {
    font-weight: 600; letter-spacing: 0.06em;
  }
  .lzwert.lzfehlt { color: var(--ink-soft); font-style: italic; }
  .lzkopie {
    border: 1px solid var(--line-strong); background: var(--surface);
    border-radius: 999px; padding: 4px 10px; font-size: 11.5px;
    cursor: pointer; white-space: nowrap;
  }
  .lzkopie:hover { border-color: var(--teal); color: var(--teal); }
  .lzkopie.fertig {
    background: var(--good); border-color: var(--good); color: #fbf8f1;
  }
  @media (max-width: 640px) {
    .lzzeile { grid-template-columns: 70px 1fr; }
    .lzkopie { grid-column: 2; justify-self: start; margin-top: 2px; }
  }

  /* ---------- Angebots-Katalog ---------- */""")

patch("Links beim Start laden",
      '  katalog = lsGet("katalog", null);',
      '  katalog = lsGet("katalog", null);\n'
      '  links = lsGet("links", null);')

patch("Links aus der Datenbank",
      '      db.doc("daten/katalog").onSnapshot(function (snap) {',
      '      db.doc("daten/links").onSnapshot(function (snap) {\n'
      '        if (!snap.exists) return;\n'
      '        links = snap.data() || null;\n'
      '        lsSet("links", links);\n'
      '        if (activeTab === "links") render();\n'
      '      }, function () {});\n'
      '      db.doc("daten/katalog").onSnapshot(function (snap) {')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:200]))
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
