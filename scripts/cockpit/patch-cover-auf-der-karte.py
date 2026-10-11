# -*- coding: utf-8 -*-
"""Cover direkt auf der Wochenkarte bauen — dort, wo auch das Video liegt.

Anlass (Patricia, 19.09.2026): *„kann ich die cover bitte nicht direkt in der
wochenvorschau machen? da lade ich ja auch das video runter"*

Sie hat recht: Video holen, Cover holen und freigeben gehoeren zu einem
Beitrag. Der Sprung in den Bild-Editor war ein Werkzeugwechsel mitten in
einem Handgriff.

**Das meiste war schon da** — nur nie auf der Karte sichtbar:
`renderReelCanvas()` zeichnet das Cover bereits (Reel-Studio), und die Felder
`coverhook`, `coverunter`, `texty`, `textskala`, `scrim` und `coverfarbe`
haengen laengst am Reel. Gefehlt haben **die Fotos** und **die Bedienung**.

Neu auf jeder Reel-Karte, aufklappbar unter „Cover bauen":
  · Vorschau, die sofort mitzeichnet
  · Hook und Unterzeile als Textfelder (vorbelegt aus `coverhook`)
  · Regler fuer Hoehe und Schriftgroesse
  · Streifen mit den zwoelf Shootingbildern, plus eigenes Foto
  · Schalter „Abdunkeln"
  · Knopf „Cover speichern" (laedt das PNG herunter)

🚨 **Das Cover wird beim Waehlen sofort abgelegt** (`saveImage`), nicht erst
beim Herunterladen. Sonst haette die Karte weiter „Noch kein Cover" gezeigt
und die Blotato-Freigabe haette ohne Titelbild abgelegt.

Der Link in den Bild-Editor bleibt — dort gibt es den Folien-Streifen und die
Story-Formate. Fuer ein einzelnes Reel-Cover braucht es ihn nicht mehr.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")


# ---------------------------------------------------------------- 1. CSS

CSS_ANKER = "  .wk-tagsfeld:focus { border-color: var(--teal); outline: none; }\n"

CSS_NEU = CSS_ANKER + """
  /* Cover direkt auf der Karte — dieselbe Zeichnung wie im Reel-Studio,
     nur mit Bedienung daneben. */
  .wk-cover { margin: 2px 0; }
  .wk-cover > summary {
    cursor: pointer; font-size: 13px; color: var(--teal); font-weight: 600;
    padding: 6px 0;
  }
  .wk-coverbox {
    display: grid; grid-template-columns: 190px 1fr; gap: 14px;
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 12px 14px; margin-top: 6px;
  }
  @media (max-width: 720px) { .wk-coverbox { grid-template-columns: 1fr; } }
  .wk-covercv {
    width: 100%; height: auto; border-radius: 8px; background: #0c1c30;
    border: 1px solid var(--line); display: block;
  }
  .wk-coversteuer { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
  .wk-coversteuer label {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); margin-top: 6px;
  }
  .wk-coversteuer textarea, .wk-coversteuer input[type="text"] {
    width: 100%; font: inherit; font-size: 13px; line-height: 1.4;
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 7px; padding: 7px 9px; resize: vertical;
  }
  .wk-coversteuer textarea:focus, .wk-coversteuer input[type="text"]:focus {
    border-color: var(--teal); outline: none;
  }
  .wk-fotos { display: flex; gap: 6px; overflow-x: auto; padding: 4px 0 6px; }
  .wk-fotos img {
    flex: 0 0 auto; width: 46px; height: 82px; object-fit: cover;
    border-radius: 6px; cursor: pointer; border: 3px solid transparent;
  }
  .wk-fotos img.sel { border-color: var(--teal); }
  .wk-chk { display: flex; align-items: center; gap: 7px; font-size: 13px;
            text-transform: none; letter-spacing: 0; color: var(--ink); }
  .wk-coverknoepfe { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
  .wk-coverknoepfe .btn { font-size: 12px; padding: 6px 12px; }
"""


# ------------------------------------------------- 2. Fotoliste + Markup

FOTOS_ANKER = """  var COVERFARBEN = ["""

FOTOS_NEU = """  /* Die Shootingbilder fuers Cover. Liegen als veroeffentlichte Dateien am
     Artifact — dieselben zwoelf wie im Bild-Editor. */
  var COVERFOTOS = ["s01.jpg", "s02.jpg", "s03.jpg", "s04.jpg", "s05.jpg",
                    "s06.jpg", "s07.jpg", "s08.jpg", "s09.jpg", "s10.jpg",
                    "s11.jpg", "s12.jpg"];

  var COVERFARBEN = ["""

MARKUP_ANKER = """        auftragsZeile(b.obj) +
        '<div class="wk-fuss">' +
"""

MARKUP_NEU = """        // Cover bauen, ohne die Karte zu verlassen. Aufgeklappt nur bei Bedarf,
        // sonst waere die Karte doppelt so lang.
        (b.art === "reels"
          ? '<details class="wk-cover"><summary>\\u25b8 Cover bauen</summary>' +
            '<div class="wk-coverbox">' +
              '<canvas class="wk-covercv"></canvas>' +
              '<div class="wk-coversteuer">' +
                '<label>Hook auf dem Cover</label>' +
                '<textarea class="wk-ch" rows="2">' +
                  esc(b.obj.coverhook || b.obj.hook || "") + '</textarea>' +
                '<label>Unterzeile (darf leer bleiben)</label>' +
                '<input type="text" class="wk-cu" value="' +
                  esc(b.obj.coverunter || "") + '">' +
                '<label>H\\u00f6he <span class="wk-cyv"></span></label>' +
                '<input type="range" class="wk-cy" min="13" max="78">' +
                '<label>Schriftgr\\u00f6sse <span class="wk-csv"></span></label>' +
                '<input type="range" class="wk-cs" min="60" max="150">' +
                '<label class="wk-chk"><input type="checkbox" class="wk-scrim">' +
                  'Hinter dem Text abdunkeln</label>' +
                '<label>Foto aus deinem Shooting</label>' +
                '<div class="wk-fotos"></div>' +
                '<div class="wk-coverknoepfe">' +
                  '<label class="btn filebtn"><span>Eigenes Foto</span>' +
                    '<input type="file" accept="image/*"></label>' +
                  '<button class="btn primary wk-covdl">Cover speichern</button>' +
                '</div>' +
              '</div>' +
            '</div></details>'
          : "") +
        auftragsZeile(b.obj) +
        '<div class="wk-fuss">' +
"""


# ---------------------------------------------------------- 3. Handler

HANDLER_ANKER = """    karte.querySelectorAll(".farbknopf").forEach(function (kn) {
"""

HANDLER_NEU = '''    /* ---------- Cover auf der Karte ----------
       Gezeichnet wird mit renderReelCanvas — genau derselben Funktion wie im
       Reel-Studio. Zwei Zeichnungen desselben Covers waeren beim naechsten
       Umbau auseinandergelaufen. */
    var covBox = karte.querySelector(".wk-cover");
    if (covBox) {
      var cv = covBox.querySelector(".wk-covercv");
      var chFeld = covBox.querySelector(".wk-ch");
      var cuFeld = covBox.querySelector(".wk-cu");
      var cyReg = covBox.querySelector(".wk-cy");
      var csReg = covBox.querySelector(".wk-cs");
      var scrimBox = covBox.querySelector(".wk-scrim");
      var fotoBox = covBox.querySelector(".wk-fotos");

      // 🚨 Vorgabe 68 statt der Mitte: bei einem Hochformat-Portraet sitzt das
      // Gesicht im oberen Drittel, und ein Textblock in der Mitte legt sich
      // genau darueber. Die Zeichnung begrenzt nach unten ohnehin gegen die
      // Caption-Zone, tiefer als erlaubt kann es also nicht rutschen.
      if (typeof b.obj.texty !== "number") b.obj.texty = 68;
      cyReg.value = b.obj.texty;
      csReg.value = b.obj.textskala || 100;
      scrimBox.checked = b.obj.scrim !== false;

      function covZeichnen() {
        covBox.querySelector(".wk-cyv").textContent = cyReg.value + " %";
        covBox.querySelector(".wk-csv").textContent = csReg.value + " %";
        renderReelCanvas(cv, b.obj, {});
      }
      function covMerken() { saveReel(b.obj); }

      chFeld.oninput = function () { b.obj.coverhook = this.value; covZeichnen(); covMerken(); };
      cuFeld.oninput = function () { b.obj.coverunter = this.value; covZeichnen(); covMerken(); };
      cyReg.oninput  = function () { b.obj.texty = +this.value; covZeichnen(); };
      csReg.oninput  = function () { b.obj.textskala = +this.value; covZeichnen(); };
      cyReg.onchange = csReg.onchange = covMerken;
      scrimBox.onchange = function () { b.obj.scrim = this.checked; covZeichnen(); covMerken(); };

      // 🚨 Das gewaehlte Foto wird sofort abgelegt, nicht erst beim
      // Herunterladen. Sonst stuende auf der Karte weiter „Noch kein Cover“
      // und die Freigabe ginge ohne Titelbild raus.
      function fotoSetzen(quelle, fertig) {
        var im = new Image();
        im.onload = function () {
          var c = document.createElement("canvas");
          var f = Math.min(1, 1350 / im.height);
          c.width = Math.round(im.width * f); c.height = Math.round(im.height * f);
          c.getContext("2d").drawImage(im, 0, 0, c.width, c.height);
          komprimiereDataUrl(c.toDataURL("image/jpeg", 0.9), function (klein) {
            saveImage("reels/" + b.obj.id, b.obj.id, klein);
            wochenbilder[b.id + "/cover-" + (b.obj.coverfarbe || "dunkelblau")] = klein;
            covZeichnen();
            if (fertig) fertig();
          });
        };
        im.onerror = function () { toast("Das Bild liess sich nicht laden."); };
        im.src = quelle;
      }

      COVERFOTOS.forEach(function (name) {
        var t = document.createElement("img");
        t.src = "assets/" + name;
        t.loading = "lazy";
        t.title = name;
        t.onerror = function () { t.remove(); };
        t.onclick = function () {
          [].forEach.call(fotoBox.children, function (x) { x.classList.remove("sel"); });
          t.classList.add("sel");
          fotoSetzen("assets/" + name, function () { toast("Foto gesetzt."); });
        };
        fotoBox.appendChild(t);
      });

      var eigen = covBox.querySelector(".filebtn input");
      eigen.onchange = function () {
        var f = this.files && this.files[0];
        if (!f) return;
        var leser = new FileReader();
        leser.onload = function () { fotoSetzen(leser.result, function () { toast("Foto gesetzt."); }); };
        leser.readAsDataURL(f);
        this.value = "";
      };

      covBox.querySelector(".wk-covdl").onclick = function () {
        if (!downloads) { toast("Herunterladen ist hier nicht verf\\u00fcgbar."); return; }
        var kn = this, alt = kn.textContent;
        kn.disabled = true; kn.textContent = "bereite vor \\u2026";
        var gross = document.createElement("canvas");
        renderReelCanvas(gross, b.obj, {});
        setTimeout(function () {
          gross.toBlob(function (blob) {
            var name = (b.obj.datum ? b.obj.datum + "-" : "") +
              (b.titel || "cover").replace(/[^\\w\\u00e4\\u00f6\\u00fc\\u00c4\\u00d6\\u00dc]+/g, "-")
              .toLowerCase() + "-cover.png";
            downloads.save({ filename: name, data: blob })
              .then(function () { toast("Gespeichert: " + name); })
              .catch(function (e) {
                if (e && e.code !== "declined") toast("Hat nicht geklappt.");
              })
              .then(function () { kn.disabled = false; kn.textContent = alt; });
          }, "image/png");
        }, 300);
      };

      // Erst zeichnen, wenn aufgeklappt wird — sonst rechnet jede Karte mit.
      covBox.addEventListener("toggle", function () {
        if (covBox.open) covZeichnen();
      });
      if (covBox.open) covZeichnen();
    }

    karte.querySelectorAll(".farbknopf").forEach(function (kn) {
'''


def main():
    if not os.path.isfile(ZIEL):
        sys.exit("Nicht gefunden: " + ZIEL)
    with io.open(ZIEL, encoding="utf-8") as f:
        text = f.read()

    getan, offen = [], []

    def tausche(alt, neu, name):
        nonlocal text
        if neu in text:
            getan.append(name + " (war schon gesetzt)")
            return
        if text.count(alt) != 1:
            offen.append("%s — Anker %dx gefunden" % (name, text.count(alt)))
            return
        text = text.replace(alt, neu)
        getan.append(name)

    tausche(CSS_ANKER, CSS_NEU, "CSS fuer den Cover-Block")
    tausche(FOTOS_ANKER, FOTOS_NEU, "Liste der Shootingbilder")
    tausche(MARKUP_ANKER, MARKUP_NEU, "Cover-Block auf der Karte")
    tausche(HANDLER_ANKER, HANDLER_NEU, "Bedienung und Herunterladen")

    for z in getan:
        print("  ok    " + z)
    for z in offen:
        print("  OFFEN " + z)
    if offen:
        sys.exit("\nAbgebrochen — nichts geschrieben.")

    tmp = ZIEL + ".neu"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, ZIEL)
    print("\nGeschrieben: %s (%d Zeichen)" % (ZIEL, len(text)))


if __name__ == "__main__":
    main()
