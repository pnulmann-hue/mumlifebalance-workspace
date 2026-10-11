"""
Schritt 1, zweiter Teil: den Katalog im Cockpit sichtbar machen.

Ein neuer Reiter **Angebots-Katalog** zeigt alle Angebote in Schubladen —
Freebie · Tipp · Prompt · Mini-Kurs · Kurs · Signature · Programm — mit dem
echten Preis aus ThriveCart und der Kette, die daran haengt.

Die bestehende Angebots-Tabelle bleibt, wo sie ist. Sie ist Patricias
Arbeitsliste; der Katalog ist der Befund aus der Quelle. Zusammengelegt werden
sie in Schritt 2, wenn die Ketten anklickbar werden.

Zwei Dinge macht die Ansicht sichtbar, die vorher niemand sehen konnte:
  ↳ was an diesem Checkout haengt (Bump, Upsell, Downsell) mit Preis
  ← wo dieses Angebot selbst als Bump oder Upsell eingesetzt wird, und zu
    welchem — meist anderen — Preis

Aufruf:
  python scripts/cockpit/patch-katalog.py [--pruefen]
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


patch("Speicher fuer den Katalog",
      '  var verknuepfung = null;',
      '  var verknuepfung = null;\n'
      '  /* Angebote in Schubladen, mit echtem Preis und Kette. */\n'
      '  var katalog = null;\n'
      '  var katalogFilter = "";')

patch("Katalog in die Navigation",
      '    { id: "produkte", label: "Angebote" },',
      '    { id: "produkte", label: "Angebote" },\n'
      '    { id: "katalog", label: "Angebots-Katalog" },')

patch("Katalog an den Render-Dispatcher",
      '    else if (activeTab === "kurse") renderKurse(main);',
      '    else if (activeTab === "kurse") renderKurse(main);\n'
      '    else if (activeTab === "katalog") renderKatalog(main);')

patch("Die Katalog-Ansicht",
      """  /* =========================================================
     Kurs-Inhalte — wo habe ich was erklärt
     ========================================================= */""",
      """  /* =========================================================
     Angebots-Katalog — was es ist, was es kostet, was daran hängt
     ========================================================= */
  function preisText(betrag, waehrung) {
    if (betrag === null || betrag === undefined) return "—";
    if (!betrag) return "0";
    return (waehrung || "CHF") + " " +
      Number(betrag).toLocaleString("de-CH", { maximumFractionDigits: 0 });
  }

  function renderKatalog(main) {
    if (!katalog) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Angebots-Katalog</h1>' +
        '<p>Alle Angebote in Schubladen, mit echtem Preis.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch kein Katalog da. ' +
        'Er entsteht aus ThriveCart.</div></div>';
      return;
    }

    var alle = katalog.angebote || [];
    var verkauft = alle.filter(function (a) {
      return a.preis && a.kategorie !== "sonstiges";
    });
    var summe = verkauft.reduce(function (s, a) { return s + (a.preis || 0); }, 0);
    var ketten = alle.filter(function (a) {
      return a.kette && (a.kette.bumps.length || a.kette.upsells.length ||
                         a.kette.downsells.length);
    }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Angebots-Katalog</h1>' +
      '<p>Was du hast, was es kostet und was daran hängt — direkt aus ThriveCart. ' +
      'Das Pfeilchen ↳ zeigt, was an diesem Checkout angeboten wird, ' +
      '← zeigt, wo dieses Angebot selbst eingesetzt wird.</p></div></div>' +
      '<div class="tiles">' +
      tile("Angebote", alle.length, "ohne Karteileichen: " + verkauft.length) +
      tile("Mit Kette", ketten, "haben Bump, Upsell oder Downsell") +
      tile("Treppe", preisText(summe, "CHF"), "alle verkauften zusammen") +
      '</div>' +
      '<div class="suchleiste"><input id="katfeld" type="search" autocomplete="off" ' +
      'placeholder="Angebot suchen — zum Beispiel Storyideen, Content-Box, MBA"></div>' +
      '<div id="katraus"></div>';

    var feld = main.querySelector("#katfeld");
    var raus = main.querySelector("#katraus");
    feld.value = katalogFilter;

    function zeigen() {
      var w = katalogFilter.toLowerCase().trim();
      raus.innerHTML = "";

      (katalog.kategorien || []).forEach(function (kat) {
        var drin = alle.filter(function (a) {
          return a.kategorie === kat.id &&
                 (!w || (a.name || "").toLowerCase().indexOf(w) >= 0);
        });
        if (!drin.length) return;

        var block = document.createElement("div");
        block.className = "panel katblock";
        var h = '<h2>' + esc(kat.name) + ' <span class="note">· ' +
                esc(kat.hinweis) + '</span></h2>';

        drin.forEach(function (a) {
          h += '<div class="katzeile">' +
               '<span class="katpreis">' + esc(preisText(a.preis, a.waehrung)) + '</span>' +
               '<span class="katname">' + esc(a.name) +
               (a.status && a.status !== "live"
                 ? ' <span class="flag bad">' + esc(a.status) + '</span>' : "") +
               '</span></div>';

          [["↳ Order Bump", a.kette.bumps], ["↳ Upsell", a.kette.upsells],
           ["↳ Downsell", a.kette.downsells]].forEach(function (r) {
            r[1].forEach(function (x) {
              h += '<div class="katkette"><span class="katrolle">' + esc(r[0]) +
                   '</span><span>' + esc(x.name) + '</span>' +
                   '<span class="katpreis klein">' + esc(preisText(x.preis, x.waehrung)) +
                   '</span></div>';
            });
          });

          (a.haengt_an || []).forEach(function (x) {
            h += '<div class="katkette rueck"><span class="katrolle">← ' +
                 esc(x.art) + '</span><span>bei ' + esc(x.bei) + '</span>' +
                 '<span class="katpreis klein">' + esc(preisText(x.preis, "CHF")) +
                 '</span></div>';
          });
        });

        block.innerHTML = h;
        raus.appendChild(block);
      });

      if (!raus.children.length) {
        raus.innerHTML = '<div class="panel"><div class="empty">Nichts gefunden.</div></div>';
      }
    }

    var warten;
    feld.oninput = function () {
      katalogFilter = feld.value;
      clearTimeout(warten);
      warten = setTimeout(zeigen, 160);
    };
    zeigen();

    var fuss = document.createElement("p");
    fuss.className = "note";
    fuss.style.marginTop = "14px";
    fuss.textContent = "Stand " + mailDatum(katalog.stand) +
      " · Preise direkt aus ThriveCart. Ein Angebot kann je Einsatzort einen " +
      "anderen Preis haben — das ist keine Panne, sondern die Mechanik.";
    main.appendChild(fuss);
  }

  /* =========================================================
     Kurs-Inhalte — wo habe ich was erklärt
     ========================================================= */""")

patch("Stil fuer den Katalog",
      "  /* ---------- Kurs-Inhalte ---------- */",
      """  /* ---------- Angebots-Katalog ---------- */
  .katblock { margin-bottom: 16px; }
  .katblock h2 { margin-bottom: 10px; }
  .katzeile {
    display: grid; grid-template-columns: 108px 1fr; gap: 12px;
    padding: 9px 0 4px; border-top: 1px solid var(--line); align-items: baseline;
  }
  .katblock .katzeile:first-of-type { border-top: 0; }
  .katpreis {
    font-variant-numeric: tabular-nums; font-size: 14px; font-weight: 600;
    text-align: right; white-space: nowrap;
  }
  .katpreis.klein { font-size: 12px; font-weight: normal; color: var(--ink-soft); }
  .katname { font-size: 14px; }
  .katkette {
    display: grid; grid-template-columns: 108px 1fr 84px; gap: 12px;
    font-size: 12.5px; color: var(--ink-soft); padding: 2px 0 2px 0;
    align-items: baseline;
  }
  .katrolle { text-align: right; color: var(--teal); white-space: nowrap; }
  .katkette.rueck .katrolle { color: var(--orange); }
  @media (max-width: 700px) {
    .katzeile, .katkette { grid-template-columns: 84px 1fr; }
    .katkette .katpreis { grid-column: 2; }
  }

  /* ---------- Kurs-Inhalte ---------- */""")

patch("Katalog aus der Datenbank holen",
      """      db.doc("daten/kurse").onSnapshot(function (snap) {""",
      """      db.doc("daten/katalog").onSnapshot(function (snap) {
        if (!snap.exists) return;
        katalog = snap.data() || null;
        lsSet("katalog", katalog);
        if (activeTab === "katalog") render();
      }, function () {});
      db.doc("daten/kurse").onSnapshot(function (snap) {""")

patch("Katalog beim Start laden",
      '  kurse = lsGet("kurse", null);',
      '  kurse = lsGet("kurse", null);\n'
      '  katalog = lsGet("katalog", null);')


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
