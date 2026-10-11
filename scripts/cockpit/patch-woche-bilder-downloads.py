"""
Zwei Luecken in der Wochen-Vorschau schliessen.

  1  Folien-Bilder und Bildausschnitt direkt in der Wochenkarte aendern.
     Bisher gingen dort nur Headline und Text — fuer Hintergrundbild und
     Verschieben musste man in den Editor wechseln.

  2  Video und Cover einzeln herunterladen. Bisher war das Cover nur ein
     kleines Bild neben dem Player und liess sich gar nicht speichern.
     Der Artifact-Viewer sperrt eigene Download-Links, deshalb laeuft beides
     ueber die downloads-Faehigkeit der Seite.

Aufruf:
  python scripts/cockpit/patch-woche-bilder-downloads.py [--pruefen]
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
# 1 · Bild und Ausschnitt pro Folie
# --------------------------------------------------------------------------
patch("Bild und Regler an die Folienkarte",
      """        feld("headline", "Headline", 2);
        if (sl.layout !== "hook" && sl.layout !== "zitat") feld("body", "Text", 3);

        folienbox.appendChild(sp);""",
      """        feld("headline", "Headline", 2);
        if (sl.layout !== "hook" && sl.layout !== "zitat") feld("body", "Text", 3);

        // Layout umstellen — entscheidet, ob die Folie ueberhaupt ein Bild hat
        var lay = document.createElement("select");
        lay.className = "wk-folienfeld";
        Object.keys(LAYOUTS).forEach(function (k) {
          var o = document.createElement("option");
          o.value = k; o.textContent = LAYOUTS[k];
          if ((sl.layout || "text") === k) o.selected = true;
          lay.appendChild(o);
        });
        lay.onchange = function () {
          sl.layout = this.value;
          saveCarousel(b.obj);
          render();
        };
        sp.appendChild(lay);

        // Hintergrundbild und Bildausschnitt — nur bei Layouts mit Bild
        if (sl.layout === "bild" || sl.layout === "split") {
          var wahl = document.createElement("label");
          wahl.className = "btn filebtn wk-folienbtn";
          wahl.innerHTML = '<span>' + (images[sl.id] ? "Bild ersetzen" : "Bild wählen") +
                           '</span><input type="file" accept="image/*">';
          wahl.querySelector("input").onchange = function () {
            var f = this.files && this.files[0];
            if (!f) return;
            compressImage(f, function (dataUrl) {
              saveImage("karussells/" + b.obj.id, sl.id, dataUrl);
              renderSlide(c, sl, b.obj, i, b.obj.slides.length);
              toast("Bild gesetzt");
            });
          };
          sp.appendChild(wahl);

          if (images[sl.id]) {
            [["zoom", "Zoom", 1, 2.4, 0.02, 1],
             ["ox", "Links/Rechts", -50, 50, 1, 0],
             ["oy", "Hoch/Runter", -50, 50, 1, 0]].forEach(function (r) {
              var zeile = document.createElement("div");
              zeile.className = "wk-regler";
              var lab = document.createElement("span");
              lab.textContent = r[1];
              var s = document.createElement("input");
              s.type = "range";
              s.min = r[2]; s.max = r[3]; s.step = r[4];
              s.value = sl[r[0]] == null ? r[5] : sl[r[0]];
              s.oninput = function () {
                sl[r[0]] = parseFloat(this.value);
                renderSlide(c, sl, b.obj, i, b.obj.slides.length);
              };
              s.onchange = function () { saveCarousel(b.obj); };
              zeile.appendChild(lab); zeile.appendChild(s);
              sp.appendChild(zeile);
            });
          }
        }

        folienbox.appendChild(sp);""")

# --------------------------------------------------------------------------
# 2 · Video und Cover einzeln herunterladen
# --------------------------------------------------------------------------
patch("Download-Hilfe",
      "  function renderWoche(main) {",
      """  /* Der Viewer sperrt Download-Links, die die Seite selbst oeffnet.
     Deshalb laeuft das Speichern ueber die downloads-Faehigkeit: Datei holen,
     in Bytes wandeln, der Seite zum Speichern geben. */
  function dateiSpeichern(quelle, dateiname) {
    if (!downloads) { toast("Herunterladen ist hier nicht verfügbar"); return; }
    toast("wird vorbereitet …");
    fetch(quelle)
      .then(function (a) { return a.arrayBuffer(); })
      .then(function (puffer) {
        return downloads.save({ filename: dateiname, data: new Uint8Array(puffer) });
      })
      .then(function () { toast("Gespeichert: " + dateiname); })
      .catch(function () { toast("Das Speichern hat nicht geklappt"); });
  }

  function renderWoche(main) {""")

patch("Zwei getrennte Knoepfe statt Mini-Cover",
      """      if (b.videourl && quelle) {
        farbwahl += '<img class="wk-covermini" src="' + quelle + '" alt="Cover">';
      }""",
      """      if (b.videourl && quelle) {
        farbwahl += '<img class="wk-covermini" src="' + quelle + '" alt="Cover">';
      }
      farbwahl += '<div class="wk-holen">' +
        (b.videourl ? '<button class="btn" data-holen="video">Video speichern</button>' : "") +
        (quelle ? '<button class="btn" data-holen="cover">Cover speichern</button>' : "") +
        '</div>';""")

patch("Download-Knoepfe verdrahten",
      """    karte.querySelectorAll(".farbknopf").forEach(function (kn) {""",
      """    karte.querySelectorAll("[data-holen]").forEach(function (kn) {
      kn.onclick = function () {
        var was = this.getAttribute("data-holen");
        var name = (b.obj.datum ? b.obj.datum + "-" : "") +
                   (b.titel || "beitrag").replace(/[^\\wäöüÄÖÜ]+/g, "-").toLowerCase();
        if (was === "video") dateiSpeichern(b.videourl, name + ".mp4");
        else dateiSpeichern(coverBild(b), name + "-cover.jpg");
      };
    });

    karte.querySelectorAll(".farbknopf").forEach(function (kn) {""")

patch("Stil fuer Regler und Knoepfe",
      "  .wk-farben { display: flex; gap: 6px; align-items: center; margin-top: 8px; }",
      """  .wk-regler { display: grid; grid-template-columns: 78px 1fr; gap: 6px; align-items: center; }
  .wk-regler span { font-size: 10px; color: var(--ink-soft); }
  .wk-folienbtn { font-size: 11px; padding: 5px 9px; text-align: center; }
  .wk-holen { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }
  .wk-holen .btn { font-size: 12px; padding: 6px 10px; }
  .wk-farben { display: flex; gap: 6px; align-items: center; margin-top: 8px; }""")


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:140]))
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
