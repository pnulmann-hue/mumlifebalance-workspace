"""
Karussell-Folien in der Wochen-Vorschau bearbeitbar machen.

Bisher waren die Folien dort nur Bilder. Patricia will sie an derselben Stelle
aendern koennen, an der sie den Beitrag abnimmt — ohne in den Editor zu wechseln.

  1  pro Folie ein Feld fuer Headline und eins fuer den Text
  2  Aenderung zeichnet die Folie sofort neu und speichert
  3  Knopf „Im Editor oeffnen" fuer alles Weitere (Bilder, Reihenfolge, Layout)

Aufruf:
  python scripts/cockpit/patch-woche-folien-bearbeiten.py [--pruefen]
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


patch("Folien mit Feldern statt nur Bild",
      """    var folienbox = karte.querySelector(".wk-folien");
    if (folienbox && b.obj.slides) {
      b.obj.slides.forEach(function (sl, i) {
        var c = document.createElement("canvas");
        c.className = "wk-folie";
        c.title = "Folie " + (i + 1);
        folienbox.appendChild(c);
        renderSlide(c, sl, b.obj, i, b.obj.slides.length);
      });
    }""",
      """    var folienbox = karte.querySelector(".wk-folien");
    if (folienbox && b.obj.slides) {
      b.obj.slides.forEach(function (sl, i) {
        var sp = document.createElement("div");
        sp.className = "wk-folienkarte";

        var c = document.createElement("canvas");
        c.className = "wk-folie";
        sp.appendChild(c);
        renderSlide(c, sl, b.obj, i, b.obj.slides.length);

        var nr = document.createElement("div");
        nr.className = "wk-folienr";
        nr.textContent = "Folie " + (i + 1);
        sp.appendChild(nr);

        // Beide Felder schreiben direkt in die Folie, zeichnen sie neu und
        // speichern. Kein Umweg ueber den Editor.
        function feld(schluessel, platzhalter, zeilen) {
          var t = document.createElement("textarea");
          t.className = "wk-folienfeld";
          t.rows = zeilen;
          t.placeholder = platzhalter;
          t.value = sl[schluessel] || "";
          t.oninput = function () {
            sl[schluessel] = this.value;
            renderSlide(c, sl, b.obj, i, b.obj.slides.length);
            saveCarousel(b.obj);
          };
          sp.appendChild(t);
        }
        feld("headline", "Headline", 2);
        if (sl.layout !== "hook" && sl.layout !== "zitat") feld("body", "Text", 3);

        folienbox.appendChild(sp);
      });
    }""")

patch("Knopf in den Editor",
      """          '<button class="btn">Caption kopieren</button>' +""",
      """          '<button class="btn">Caption kopieren</button>' +
          (b.art === "karussells" ? '<button class="btn">Im Editor öffnen</button>' : "") +""")

patch("Knopf verdrahten",
      """    felder[2].onclick = function () {
      b.obj.textfrei = !b.obj.textfrei;""",
      """    if (b.art === "karussells") {
      felder[2].onclick = function () {
        activeCarousel = b.obj.id;
        activeTab = "karussell";
        render();
      };
    }
    var freigabeKnopf = felder[felder.length - 1];
    freigabeKnopf.onclick = function () {
      b.obj.textfrei = !b.obj.textfrei;""")

patch("Freigabe-Knopf sauber abschliessen",
      """      toast(b.obj.textfrei ? "Freigegeben" : "Freigabe zurückgenommen");
      render();
    };
    return karte;""",
      """      toast(b.obj.textfrei ? "Freigegeben" : "Freigabe zurückgenommen");
      render();
    };
    return karte;""")

patch("Stil fuer die Folienkarten",
      """  .wk-folien { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px; }
  .wk-folie {
    flex: 0 0 118px; width: 118px; height: auto; border-radius: 6px;
    border: 1px solid var(--line); background: #0c1c30;
  }""",
      """  .wk-folien { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 8px; }
  .wk-folienkarte {
    flex: 0 0 168px; display: flex; flex-direction: column; gap: 5px;
  }
  .wk-folie {
    width: 168px; height: auto; border-radius: 6px;
    border: 1px solid var(--line); background: #0c1c30;
  }
  .wk-folienr { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-soft); }
  .wk-folienfeld {
    width: 100%; resize: vertical; font-size: 12px; line-height: 1.4;
    background: var(--ground); border: 1px solid var(--line); border-radius: 6px;
    padding: 6px 8px; font-family: var(--body);
  }
  .wk-folienfeld:focus { border-color: var(--teal); outline: none; }""")


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:130]))
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
