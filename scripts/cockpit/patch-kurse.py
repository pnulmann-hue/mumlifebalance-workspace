"""
Den Reiter „Kurs-Inhalte" ins Cockpit bauen.

Beantwortet die Frage, die im Alltag wirklich kommt: „In welcher Lektion habe
ich das erklaert?" Man tippt ein Stichwort und sieht Kurs, Modul und Lektion —
statt sich durch ThriveCart, Drive und Canva zu klicken.

Zwei Ansichten in einem Reiter:
  Suchen       Stichwort → Fundstellen in den Lektionen
  Durchblaettern   Kurs aufklappen, alle Lektionen mit ihren Stichwoertern

Die Daten kommen aus `scripts/cockpit/kurse-indexieren.py`.

Aufruf:
  python scripts/cockpit/patch-kurse.py [--pruefen]
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


patch("Speicher fuer die Kurs-Inhalte",
      '  var doterra = null;',
      '  var doterra = null;\n'
      '  /* Kurse, Lektionen und das Stichwort-Register. */\n'
      '  var kurse = null;\n'
      '  var kursWort = "";\n'
      '  var offenerKurs = null;')

patch("Kurs-Inhalte in die Navigation",
      '    { id: "produkte", label: "Angebote" },',
      '    { id: "produkte", label: "Angebote" },\n'
      '    { id: "kurse", label: "Kurs-Inhalte" },')

patch("Kurs-Inhalte an den Render-Dispatcher",
      '    else if (activeTab === "suche") renderSuche(main);',
      '    else if (activeTab === "suche") renderSuche(main);\n'
      '    else if (activeTab === "kurse") renderKurse(main);')

patch("Die Kurs-Ansicht",
      """  /* =========================================================
     Suchen — ein Stichwort, und es kommt, wo es vorkam
     ========================================================= */""",
      """  /* =========================================================
     Kurs-Inhalte — wo habe ich was erklärt
     ========================================================= */
  function ohneUmlaut(w) {
    return String(w || "").toLowerCase()
      .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
  }

  function lektionTreffer(wort) {
    /* Erst das Register fragen, dann alle Lektionen — so findet auch ein
       Wortanfang wie „hütch" etwas. */
    var w = ohneUmlaut(wort).trim();
    if (!w || !kurse) return [];
    var raus = [];
    kurse.kurse.forEach(function (k) {
      k.lektionen.forEach(function (l) {
        var imTitel = ohneUmlaut(l.titel).indexOf(w) >= 0;
        var treffer = (l.stichwoerter || []).filter(function (s) {
          return ohneUmlaut(s).indexOf(w) >= 0;
        });
        if (imTitel || treffer.length) {
          raus.push({ kurs: k.name, lektion: l, worte: treffer, imTitel: imTitel });
        }
      });
    });
    raus.sort(function (a, b) { return (b.imTitel ? 1 : 0) - (a.imTitel ? 1 : 0); });
    return raus;
  }

  function lektionNummer(l) {
    if (l.modul) return l.modul + "." + l.lektion;
    return l.nummer ? String(l.nummer) : "—";
  }

  function renderKurse(main) {
    if (!kurse) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Kurs-Inhalte</h1>' +
        '<p>Wo habe ich was erklärt?</p></div></div>' +
        '<div class="panel"><div class="empty">Noch kein Inhaltsverzeichnis da.</div></div>';
      return;
    }

    var anzahl = kurse.kurse.reduce(function (s, k) { return s + k.lektionen.length; }, 0);
    main.innerHTML =
      '<div class="page-head"><div><h1>Kurs-Inhalte</h1>' +
      '<p>Deine ' + kurse.kurse.length + ' Kurse mit ' + anzahl + ' Lektionen. ' +
      'Tipp ein Stichwort ein, und du siehst, in welcher Lektion du es erklärt hast — ' +
      'zum Beispiel wenn jemand fragt.</p></div></div>' +
      '<div class="suchleiste"><input id="kursfeld" type="search" autocomplete="off" ' +
      'placeholder="zum Beispiel: Hütchenmethode, Käufertypen, Orderbump, Schaufenster"></div>' +
      '<div id="kursraus"></div>';

    var feld = main.querySelector("#kursfeld");
    var raus = main.querySelector("#kursraus");
    feld.value = kursWort;

    function zeigen() {
      if (kursWort.trim()) {
        var tr = lektionTreffer(kursWort);
        if (!tr.length) {
          raus.innerHTML = '<div class="panel"><div class="empty">Zu „' +
            esc(kursWort) + '" ist in deinen Kursen nichts hinterlegt.</div></div>';
          return;
        }
        var h = '<p class="note">' + tr.length +
                (tr.length === 1 ? ' Lektion' : ' Lektionen') + '</p>';
        tr.forEach(function (t) {
          h += '<div class="sxtreffer">' +
               '<div class="sxkopf"><span class="sxbereich">' + esc(t.kurs) + '</span>' +
               '<span class="klnr">' + esc(lektionNummer(t.lektion)) + '</span>' +
               '<span class="sxtitel">' + markiere(t.lektion.titel, kursWort) + '</span></div>' +
               (t.worte.length
                 ? '<p class="sxauszug">' + t.worte.map(esc).join(" · ") + '</p>' : "") +
               '</div>';
        });
        raus.innerHTML = h;
        return;
      }

      // Kein Stichwort: alle Kurse zum Aufklappen
      raus.innerHTML = "";
      kurse.kurse.forEach(function (k) {
        var karte = document.createElement("div");
        karte.className = "dkarte" + (offenerKurs === k.name ? " auf" : "");
        karte.innerHTML =
          '<button class="dkopf"><span class="dpfeil">▸</span>' +
          '<span class="dname">' + esc(k.name) + '</span>' +
          '<span class="note">' + k.lektionen.length + ' Lektionen' +
          (k.ohne_transkript ? ' · ' + k.ohne_transkript + ' ohne Transkript' : "") +
          '</span></button><div class="dkoerper"></div>';
        karte.querySelector(".dkopf").onclick = function () {
          offenerKurs = (offenerKurs === k.name) ? null : k.name;
          render();
        };
        if (offenerKurs === k.name) {
          var koerper = karte.querySelector(".dkoerper");
          koerper.innerHTML = k.lektionen.map(function (l) {
            return '<div class="klzeile">' +
              '<span class="klnr">' + esc(lektionNummer(l)) + '</span>' +
              '<span class="kltitel">' + esc(l.titel) + '</span>' +
              '<span class="klworte">' +
              (l.ohne_transkript
                ? '<em>kein Transkript — nur Video</em>'
                : (l.stichwoerter || []).slice(0, 8).map(esc).join(" · ")) +
              '</span></div>';
          }).join("");
        }
        raus.appendChild(karte);
      });
    }

    var warten;
    feld.oninput = function () {
      kursWort = feld.value;
      clearTimeout(warten);
      warten = setTimeout(zeigen, 160);
    };
    zeigen();
  }

  /* =========================================================
     Suchen — ein Stichwort, und es kommt, wo es vorkam
     ========================================================= */""")

patch("Stil fuer die Kurs-Liste",
      "  /* ---------- Suche ---------- */",
      """  /* ---------- Kurs-Inhalte ---------- */
  .klzeile {
    display: grid; grid-template-columns: 58px minmax(170px, 1fr) minmax(200px, 1.5fr);
    gap: 12px; padding: 8px 0; border-top: 1px solid var(--line); align-items: baseline;
  }
  .klzeile:first-child { border-top: 0; }
  .klnr {
    font-size: 11px; font-variant-numeric: tabular-nums; color: var(--teal);
    background: var(--teal-soft); border-radius: 999px; padding: 2px 8px;
    text-align: center; flex: none;
  }
  .kltitel { font-size: 13px; font-weight: 600; }
  .klworte { font-size: 12px; color: var(--ink-soft); line-height: 1.5; }
  @media (max-width: 760px) { .klzeile { grid-template-columns: 58px 1fr; } .klworte { grid-column: 2; } }

  /* ---------- Suche ---------- */""")

patch("Kurs-Inhalte aus der Datenbank holen",
      """      db.doc("daten/doterra").onSnapshot(function (snap) {""",
      """      db.doc("daten/kurse").onSnapshot(function (snap) {
        if (!snap.exists) return;
        kurse = snap.data() || null;
        lsSet("kurse", kurse);
        if (activeTab === "kurse") render();
      }, function () {});
      db.doc("daten/doterra").onSnapshot(function (snap) {""")

patch("Kurs-Inhalte beim Start laden",
      '  doterra = lsGet("doterra", null);',
      '  doterra = lsGet("doterra", null);\n'
      '  kurse = lsGet("kurse", null);')


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
