"""
Die Verknüpfung in die Angebots-Karte einbauen.

Bisher stand in einer Angebots-Karte nur, was Patricia selbst eingetragen hat.
Jetzt steht darueber, was das Cockpit ueber dieses Angebot weiss: die Datei zum
Anklicken, der Funnel, die Mails, die es ausliefern, die Beitraege, in denen es
vorkommt, und der Kurs, wenn es einer ist.

Das ist der Teil, der Zeit spart: keine Suche mehr durch ThriveCart, Drive und
Canva, um herauszufinden, wo etwas haengt.

Daten aus `scripts/cockpit/verknuepfen.py`.

Aufruf:
  python scripts/cockpit/patch-verknuepfung.py [--pruefen]
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


patch("Speicher fuer die Verknuepfung",
      '  var kurse = null;',
      '  var kurse = null;\n'
      '  /* Was ein Angebot alles beruehrt: Datei, Funnel, Mails, Beiträge. */\n'
      '  var verknuepfung = null;')

patch("Die Verknüpfung in die Angebots-Karte",
      """        // Was ThriveCart wirklich am Checkout haengen hat. Das ist Befund,
        // kein Eingabefeld — deshalb steht es ueber den Notizfeldern.""",
      """        // Alles, was dieses Angebot beruehrt — zuoberst, weil man deshalb
        // die Karte aufmacht.
        var v = (verknuepfung && verknuepfung.werte) ? verknuepfung.werte[a.id] : null;
        if (v) {
          var kasten = document.createElement("div");
          kasten.className = "vkbox";
          var h = "";

          if (v.dateien && v.dateien.length) {
            h += '<div class="vkzeile"><span>Datei</span><span>' +
              v.dateien.map(function (d) {
                return '<a class="vkdatei" href="' + esc(d.blob) + '" target="_blank" ' +
                       'rel="noopener">' + esc(d.name) +
                       (d.seiten ? ' · ' + d.seiten + ' Seiten' : "") + '</a>';
              }).join(" ") + '</span></div>';
          }
          if (v.funnel) {
            var f = v.funnel, teile = [];
            if (f.keyword) teile.push("Keyword <strong>" + esc(f.keyword) + "</strong>");
            if (f.liste) teile.push("Liste " + esc(String(f.liste)));
            if (f.automation) teile.push("Automation " + esc(String(f.automation)));
            if (teile.length) {
              h += '<div class="vkzeile"><span>Funnel</span><span>' +
                   teile.join(" · ") + '</span></div>';
            }
            if (f.anschluss) {
              h += '<div class="vkzeile"><span>Danach</span><span>' +
                   esc(f.anschluss) + '</span></div>';
            }
          }
          if (v.mails && v.mails.length) {
            h += '<div class="vkzeile"><span>Liefert aus</span><span>' +
              v.mails.map(function (m) { return esc(m.betreff); }).join("<br>") +
              '</span></div>';
          }
          if (v.kurs) {
            h += '<div class="vkzeile"><span>Kurs</span><span>' +
                 esc(v.kurs.kurs) + ' · ' + v.kurs.anzahl + ' Lektionen</span></div>';
          }
          if (v.erwaehnt && v.erwaehnt.length) {
            h += '<div class="vkzeile"><span>Erwähnt in</span><span>' +
              '<button class="vkmehr" type="button">' + v.erwaehnt.length +
              ' Dokumenten anzeigen</button>' +
              '<div class="vkliste" hidden>' +
              v.erwaehnt.map(function (e) {
                return '<div class="vkfund"><strong>' + esc(e.titel) + '</strong>' +
                       '<span>' + esc(e.datei) + '</span></div>';
              }).join("") + '</div></span></div>';
          }

          if (h) {
            kasten.innerHTML = '<div class="vkkopf">Was dazugehört</div>' + h;
            koerper.appendChild(kasten);
            var knopf = kasten.querySelector(".vkmehr");
            if (knopf) {
              knopf.onclick = function () {
                var liste = kasten.querySelector(".vkliste");
                liste.hidden = !liste.hidden;
                knopf.textContent = liste.hidden
                  ? v.erwaehnt.length + " Dokumenten anzeigen"
                  : "wieder zuklappen";
              };
            }
          }
        }

        // Was ThriveCart wirklich am Checkout haengen hat. Das ist Befund,
        // kein Eingabefeld — deshalb steht es ueber den Notizfeldern.""")

patch("Die Verknüpfung zuoberst einsortieren",
      """          koerper.insertBefore(kasten, koerper.firstChild);
        }

        if (a.bumphinweis) {""",
      """          koerper.insertBefore(kasten, koerper.firstChild);
        }

        if (a.bumphinweis) {""")

patch("Stil fuer die Verknüpfung",
      "  /* ---------- Befund aus ThriveCart ---------- */",
      """  /* ---------- Was zu einem Angebot gehört ---------- */
  .vkbox {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 11px 13px; margin-top: 12px;
  }
  .vkkopf {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft); margin-bottom: 8px;
  }
  .vkzeile {
    display: grid; grid-template-columns: 96px 1fr; gap: 10px;
    font-size: 13px; padding: 4px 0; align-items: baseline;
  }
  .vkzeile > span:first-child { color: var(--ink-soft); font-size: 12px; }
  .vkdatei {
    display: inline-block; background: var(--teal); color: #fbf8f1;
    border-radius: 999px; padding: 4px 12px; font-size: 12px;
    text-decoration: none; margin-right: 6px;
  }
  .vkdatei:hover { background: var(--navy); }
  .vkmehr {
    background: none; border: 0; padding: 0; font: inherit; font-size: 13px;
    color: var(--teal); cursor: pointer; text-decoration: underline;
  }
  .vkliste { margin-top: 8px; }
  .vkfund { padding: 5px 0; border-top: 1px solid var(--line); }
  .vkfund strong { display: block; font-size: 13px; font-weight: 600; }
  .vkfund span { font-size: 11px; color: var(--ink-soft); }
  @media (max-width: 700px) { .vkzeile { grid-template-columns: 1fr; gap: 2px; } }

  /* ---------- Befund aus ThriveCart ---------- */""")

patch("Verknüpfung aus der Datenbank holen",
      """      db.doc("daten/kurse").onSnapshot(function (snap) {""",
      """      db.doc("daten/verknuepfung").onSnapshot(function (snap) {
        if (!snap.exists) return;
        verknuepfung = snap.data() || null;
        lsSet("verknuepfung", verknuepfung);
        if (activeTab === "produkte") render();
      }, function () {});
      db.doc("daten/kurse").onSnapshot(function (snap) {""")

patch("Verknüpfung beim Start laden",
      '  kurse = lsGet("kurse", null);',
      '  kurse = lsGet("kurse", null);\n'
      '  verknuepfung = lsGet("verknuepfung", null);')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt == neu:
            print("  --  %s (nichts zu tun)" % name)
            continue
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
