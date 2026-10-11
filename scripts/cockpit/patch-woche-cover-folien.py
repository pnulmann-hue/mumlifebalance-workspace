"""
Zweiter Ausbau der Wochen-Vorschau.

  1  Farbwaehler am Reel-Cover — Patricia will die Schleierfarbe selbst
     umstellen koennen, statt dass ich sie festlege. Die drei Varianten
     liegen als Bilder in der Sammlung (cover-petrol / -dunkelblau / -orange).
  2  Karussell Folie fuer Folie statt nur der ersten — als Streifen aus
     denselben Canvas-Slides, die auch der Editor zeichnet.

Aufruf:
  python scripts/cockpit/patch-woche-cover-folien.py [--pruefen]
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


# --------------------------------------------------------------------------
# 1 · Coverfarbe am Reel speichern und laden
# --------------------------------------------------------------------------
patch("Reel speichern: Coverfarbe mit",
      '        datum: r.datum || "", textfrei: !!r.textfrei,',
      '        datum: r.datum || "", textfrei: !!r.textfrei,\n'
      '        coverfarbe: r.coverfarbe || "dunkelblau",')

patch("Reel laden: Coverfarbe uebernehmen",
      'datum: d0.datum || "", textfrei: !!d0.textfrei, scrim: d0.scrim !== false,',
      'datum: d0.datum || "", textfrei: !!d0.textfrei, '
      'coverfarbe: d0.coverfarbe || "dunkelblau", scrim: d0.scrim !== false,')

# --------------------------------------------------------------------------
# 2 · Bilder: alle Farbvarianten laden, nicht nur "cover"
# --------------------------------------------------------------------------
patch("Cover in allen Farben holen",
      """  function wochenBildHolen(art, id) {
    if (!db || wochenbilderGeholt[id]) return;
    wochenbilderGeholt[id] = true;
    db.doc(art + "/" + id).collection("bilder").doc("cover").get()
      .then(function (d) {
        var u = d && d.data && (d.data() || {}).dataUrl;
        if (!u) return;
        wochenbilder[id] = u;
        if (activeTab === "woche") render();
      }).catch(function () {});
  }""",
      """  function wochenBildHolen(art, id) {
    if (!db || wochenbilderGeholt[id]) return;
    wochenbilderGeholt[id] = true;
    // Alle Cover-Dokumente auf einmal: "cover" plus die Farbvarianten
    // cover-petrol / cover-dunkelblau / cover-orange.
    db.doc(art + "/" + id).collection("bilder").limit(12).get()
      .then(function (qs) {
        var neu = false;
        qs.docs.forEach(function (d) {
          var u = (d.data() || {}).dataUrl;
          if (!u || d.id.indexOf("cover") !== 0) return;
          wochenbilder[id + "/" + d.id] = u;
          neu = true;
        });
        if (neu && activeTab === "woche") render();
      }).catch(function () {});
  }

  var COVERFARBEN = [
    { k: "petrol", l: "Petrol" },
    { k: "dunkelblau", l: "Dunkelblau" },
    { k: "orange", l: "Orange" }
  ];

  function coverBild(b) {
    if (b.art !== "reels") return wochenbilder[b.id + "/cover"] || "";
    var f = b.obj.coverfarbe || "dunkelblau";
    return wochenbilder[b.id + "/cover-" + f]
        || wochenbilder[b.id + "/cover"] || "";
  }""")

# --------------------------------------------------------------------------
# 3 · Karte: Farbknoepfe beim Reel, Folienstreifen beim Karussell
# --------------------------------------------------------------------------
patch("Wochenkarte neu aufbauen",
      """    var bild = wochenbilder[b.id]
      ? '<img class="wk-bild" src="' + wochenbilder[b.id] + '" alt="">'
      : '<div class="wk-leer">Noch kein Vorschaubild</div>';""",
      """    var quelle = coverBild(b);
    var bild = quelle
      ? '<img class="wk-bild" src="' + quelle + '" alt="">'
      : '<div class="wk-leer">Noch kein Vorschaubild</div>';

    // Farbwaehler nur beim Reel — beim Karussell macht die Farbe der Editor.
    var farbwahl = "";
    if (b.art === "reels") {
      farbwahl = '<div class="wk-farben">' +
        COVERFARBEN.map(function (f) {
          var an = (b.obj.coverfarbe || "dunkelblau") === f.k;
          return '<button class="farbknopf f-' + f.k + '" data-farbe="' + f.k + '"' +
                 (an ? ' aria-pressed="true"' : '') + ' title="' + f.l + '"></button>';
        }).join("") +
        '<span class="wk-unter">Coverfarbe</span></div>';
    }""")

patch("Karte zusammensetzen",
      """    karte.innerHTML =
      '<div>' + bild + '</div>' +""",
      """    karte.innerHTML =
      '<div>' + bild + farbwahl + '</div>' +""")

patch("Folienstreifen beim Karussell",
      """        (b.datei ? '<div class="wk-datei">Datei: ' + esc(b.datei) + '</div>' : "") +""",
      """        (b.datei ? '<div class="wk-datei">Datei: ' + esc(b.datei) + '</div>' : "") +
        (b.art === "karussells" ? '<div class="wk-folien"></div>' : "") +""")

patch("Farbknoepfe und Folien verdrahten",
      """    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");""",
      """    // Folien des Karussells zeichnen — dieselben Canvas-Slides wie im Editor
    var folienbox = karte.querySelector(".wk-folien");
    if (folienbox && b.obj.slides) {
      b.obj.slides.forEach(function (sl, i) {
        var c = document.createElement("canvas");
        c.className = "wk-folie";
        c.title = "Folie " + (i + 1);
        folienbox.appendChild(c);
        renderSlide(c, sl, b.obj, i, b.obj.slides.length);
      });
    }

    karte.querySelectorAll(".farbknopf").forEach(function (kn) {
      kn.onclick = function () {
        b.obj.coverfarbe = this.getAttribute("data-farbe");
        saveReel(b.obj);
        render();
      };
    });

    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");""")

# --------------------------------------------------------------------------
# 4 · Stil
# --------------------------------------------------------------------------
patch("Stil fuer Farbknoepfe und Folien",
      "  /* Text-Freigabe */",
      """  .wk-farben { display: flex; gap: 6px; align-items: center; margin-top: 8px; }
  .farbknopf {
    width: 22px; height: 22px; border-radius: 50%; cursor: pointer;
    border: 2px solid transparent; padding: 0;
  }
  .farbknopf:hover { border-color: var(--line-strong); }
  .farbknopf[aria-pressed="true"] { border-color: var(--ink); }
  .farbknopf.f-petrol { background: #12828c; }
  .farbknopf.f-dunkelblau { background: #29556d; }
  .farbknopf.f-orange { background: #dc822e; }
  .wk-folien { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px; }
  .wk-folie {
    flex: 0 0 118px; width: 118px; height: auto; border-radius: 6px;
    border: 1px solid var(--line); background: #0c1c30;
  }

  /* Text-Freigabe */""")


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:120]))
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
