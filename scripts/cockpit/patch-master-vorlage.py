"""Karussell-Master-Vorlage im Cockpit (04.11.2026).

Patricia: *„kann man es wieder so machen, dass ich die farbe und evt das foto anpassen kann
wie jetzt schon im cockpit?“* Der Zeichner `scripts/karussell-render/master-zeichner.js`
läuft dadurch im Cockpit und in folien.mjs. Farbe über den bestehenden Marken-Look, Foto über
den Streifen auf der Cover-Folie, Texte über die Felder je Folie.
Beim Freigeben entsteht das Bild aus demselben Zeichner.

Wiederholbar: Ein zweiter Lauf ersetzt nur den Zeichner-Block.

    python scripts/cockpit/patch-master-vorlage.py [--datei <cockpit.html>]
"""

import os
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
ZEICHNER = ROOT / "scripts" / "karussell-render" / "master-zeichner.js"
ANFANG, ENDE = "/* MASTER-VORLAGE-ANFANG", "/* MASTER-VORLAGE-ENDE */"

ERSETZUNGEN = [
    # Zeichner vor renderSlide, und renderSlide leitet Vorlagen-Folien dorthin
    ('''  function renderSlide(canvas, slide, car, index, total) {
    var b = BRANDS[car.brand] || BRANDS.mlb_dark;
''', '''  @@ZEICHNER@@
  function renderSlide(canvas, slide, car, index, total, fertig) {
    if (MASTER.ist(slide)) {
      if (canvas.width !== W) { canvas.width = W; canvas.height = H; }
      getImageObj(slide.fotoEigen ? slide.id : "", function (eigen) {
        MASTER.bereit(slide, function (foto) {
          MASTER.zeichne(canvas, slide, car, index, total, slide.layout === "m-titel" ? (eigen || foto) : null);
          if (fertig) fertig();
        });
      });
      return;
    }
    var b = BRANDS[car.brand] || BRANDS.mlb_dark;
'''),
    # Die Auswahl im Cockpit kennt die Vorlagen-Layouts
    ('''    cta:   "CTA (Keyword-Slide)"
  };
''', '''    cta:   "CTA (Keyword-Slide)",
    "m-titel": "Vorlage: Cover",
    "m-liste": "Vorlage: Karten-Liste",
    "m-text": "Vorlage: ein Gedanke",
    "m-auftrag": "Vorlage: zum Abtippen",
    "m-aufruf": "Vorlage: letzte Folie"
  };
'''),
    # Freigabe wartet bei Vorlagen-Folien auf Schrift und Foto
    ('''    var cv = document.createElement("canvas");
    renderSlide(cv, slide, car, i, car.slides.length);
    setTimeout(function () {
      var q = 0.92;
      var out = cv.toDataURL("image/jpeg", q);
      while (out.length > 700000 && q > 0.45) { q -= 0.08; out = cv.toDataURL("image/jpeg", q); }
      cb(out);
    }, 320);
''', '''    var cv = document.createElement("canvas");
    function abnehmen() {
      var q = 0.92;
      var out = cv.toDataURL("image/jpeg", q);
      while (out.length > 700000 && q > 0.45) { q -= 0.08; out = cv.toDataURL("image/jpeg", q); }
      cb(out);
    }
    if (MASTER.ist(slide)) { renderSlide(cv, slide, car, i, car.slides.length, abnehmen); return; }
    renderSlide(cv, slide, car, i, car.slides.length);
    setTimeout(abnehmen, 320);
'''),
    # Farbe: derselbe Marken-Look, bei der Vorlage mit klaren Namen und Petrol-Warnung
    ('''    if (b.art === "karussells") {
      farbwahl += '<div class="wk-holen"><select class="btn wk-marke">' +
        Object.keys(BRANDS).map(function (k) {
          return '<option value="' + k + '"' +
            ((b.obj.brand || "mlb_dark") === k ? " selected" : "") + '>' +
            esc(BRANDS[k].label) + '</option>';
        }).join("") + '</select>' +
        '<span class="wk-unter">Marken-Look</span></div>';
    }
''', '''    if (b.art === "karussells") {
      var mVorlage = MASTER.istKarussell(b.obj);
      farbwahl += '<div class="wk-holen"><select class="btn wk-marke">' +
        Object.keys(BRANDS).map(function (k) {
          return '<option value="' + k + '"' +
            ((b.obj.brand || "mlb_dark") === k ? " selected" : "") + '>' +
            esc(mVorlage ? MASTER.FARBNAME[k] : BRANDS[k].label) + '</option>';
        }).join("") + '</select>' +
        '<span class="wk-unter">' + (mVorlage ? "Farbe von Cover und letzter Folie" : "Marken-Look") + '</span>' +
        (mVorlage ? "" : '<button class="btn wk-zumaster">Auf Master-Vorlage umstellen</button>') +
        (mVorlage && b.obj.brand === "mlb_teal" && MASTER.istLead(b.obj)
          ? '<span class="wk-mwarn">Dieser Beitrag hat ein Stichwort. Petrol-Cover sind bei Lead-Posts eingebrochen, nimm besser Dunkelblau oder Beige.</span>'
          : "") +
        '</div>';
    }
'''),
    ('''    var markeWahl = karte.querySelector(".wk-marke");
''', '''    var zumaster = karte.querySelector(".wk-zumaster");
    if (zumaster) {
      zumaster.onclick = function () {
        MASTER.umstellen(b.obj);
        saveCarousel(b.obj);
        render();
        toast("Umgestellt. Setz auf dem Cover das grosse Wort in *Sternchen*.");
      };
    }

    var markeWahl = karte.querySelector(".wk-marke");
'''),
    # Felder je Folie
    ('''        feld("headline", "Headline", 2);
        if (sl.layout !== "hook" && sl.layout !== "zitat") feld("body", "Text", 3);
''', '''        var mFelder = MASTER.felder(sl.layout);
        if (mFelder) mFelder.forEach(function (f) { feld(f[0], f[1], f[2]); });
        else {
          feld("headline", "Headline", 2);
          if (sl.layout !== "hook" && sl.layout !== "zitat") feld("body", "Text", 3);
        }
'''),
    # Foto auf der Cover-Folie: Streifen aus dem Shooting, eigenes Foto, ohne Foto
    ('''        // Hintergrundbild und Bildausschnitt — nur bei Layouts mit Bild
        if (sl.layout === "bild" || sl.layout === "split") {
          var wahl = document.createElement("label");
''', '''        function folieNeu() { renderSlide(c, sl, b.obj, i, b.obj.slides.length); }
        if (sl.layout === "m-titel") {
          var streifen = document.createElement("div");
          streifen.className = "wk-fotos";
          var ohne = document.createElement("button");
          ohne.className = "btn wk-ohnefoto" + (!sl.foto && !sl.fotoEigen ? " sel" : "");
          ohne.textContent = "Ohne Foto";
          ohne.onclick = function () {
            sl.foto = ""; sl.fotoEigen = false;
            saveCarousel(b.obj); render();
          };
          streifen.appendChild(ohne);
          COVERFOTOS.forEach(function (name) {
            var t = document.createElement("img");
            t.src = "assets/" + name;
            t.loading = "lazy";
            t.className = sl.foto === name && !sl.fotoEigen ? "sel" : "";
            t.onerror = function () { t.remove(); };
            t.onclick = function () {
              sl.foto = name; sl.fotoEigen = false;
              saveCarousel(b.obj); render();
            };
            streifen.appendChild(t);
          });
          sp.appendChild(streifen);
        }

        // Hintergrundbild und Bildausschnitt — nur bei Layouts mit Bild
        if (sl.layout === "bild" || sl.layout === "split" || sl.layout === "m-titel") {
          var wahl = document.createElement("label");
'''),
    ('''          wahl.innerHTML = '<span>' + (images[sl.id] ? "Bild ersetzen" : "Bild wählen") +
''', '''          wahl.innerHTML = '<span>' + (sl.layout === "m-titel" ? "Eigenes Foto" : images[sl.id] ? "Bild ersetzen" : "Bild wählen") +
'''),
    ('''              saveImage("karussells/" + b.obj.id, sl.id, dataUrl);
              renderSlide(c, sl, b.obj, i, b.obj.slides.length);
              toast("Bild gesetzt");
''', '''              saveImage("karussells/" + b.obj.id, sl.id, dataUrl);
              if (sl.layout === "m-titel") { sl.fotoEigen = true; saveCarousel(b.obj); render(); }
              else renderSlide(c, sl, b.obj, i, b.obj.slides.length);
              toast("Bild gesetzt");
'''),
    ('''          if (images[sl.id]) {
            [["zoom", "Zoom", 1, 2.4, 0.02, 1],
''', '''          if (images[sl.id] || (sl.layout === "m-titel" && sl.foto)) {
            [["zoom", "Zoom", 1, 2.4, 0.02, 1],
'''),
    # Aussehen
    ('''  .wk-fotos img.sel { border-color: var(--teal); }
''', '''  .wk-fotos img.sel { border-color: var(--teal); }
  /* In der schmalen Folien-Spalte umbrechen, sonst dehnt der Streifen die ganze Spalte */
  .wk-folienkarte { min-width: 0; }
  .wk-folienkarte .wk-fotos { flex-wrap: wrap; overflow: visible; padding: 2px 0; }
  .wk-folienkarte .wk-fotos img { width: 37px; height: 50px; object-fit: cover; flex: 0 0 auto; }
  .wk-ohnefoto { flex: 0 0 100%; font-size: 12px; }
  .wk-ohnefoto.sel { border-color: var(--teal); }
  .wk-mwarn { display: block; font-size: 12px; line-height: 1.35; color: #a84a12; margin-top: 4px; }
'''),
]


def main():
    ziel = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    t = ziel.read_text(encoding="utf-8")
    block = ZEICHNER.read_text(encoding="utf-8").strip()

    if ANFANG in t:
        a = t.index(ANFANG)
        e = t.index(ENDE, a) + len(ENDE)
        t = t[:a] + block + t[e:]
        print("Zeichner ersetzt")
    else:
        for alt, neu in ERSETZUNGEN:
            if t.count(alt) != 1:
                sys.exit("Stelle nicht eindeutig (" + str(t.count(alt)) + "x):\n" + alt[:120])
            t = t.replace(alt, neu.replace("@@ZEICHNER@@", block))
        print(len(ERSETZUNGEN), "Stellen gesetzt")

    # Syntaxpruefung, bevor irgendetwas geschrieben wird
    skript = max(re.findall(r"<script>(.*?)</script>", t, re.S), key=len)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(skript)
    erg = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if erg.returncode:
        sys.exit("Syntaxfehler, nichts geschrieben:\n" + erg.stderr[:800])

    # Erst vollstaendig schreiben, dann tauschen: ein Fehler beim Schreiben darf die Datei nicht leeren
    tmp = ziel.with_suffix(".tmp")
    tmp.write_text(t, encoding="utf-8", newline="")
    os.replace(tmp, ziel)
    print("OK", ziel)


main()
