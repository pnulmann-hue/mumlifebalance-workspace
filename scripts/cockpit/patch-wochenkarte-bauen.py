# -*- coding: utf-8 -*-
"""Repariert die drei Dinge, an denen die Wochen-Vorschau haengenblieb (16.09.2026).

Patricias Befund: *„wenn ich auf im editor bauen gehe, passiert nichts … coverbild
ist immer integriert im video nicht wie vereinbart separat … kann texte anpassen,
farbe aber nicht"*

| # | Was kaputt war | Was jetzt passiert |
|---|---|---|
| A | „Im Bild-Editor bauen" war ein `window.open` — in einem Artifact-Rahmen blockiert, wortlos | echter Link (`<a target="_blank">`), und die Adresse wandert zusaetzlich in die Zwischenablage |
| B | Kein Weg zum separaten Cover, wenn ein Video dranhaengt | Knopf **Cover bauen** springt INNERHALB des Cockpits ins Reel-Studio mit genau diesem Reel |
| C | Beim Karussell liess sich Text aendern, Farbe nicht | Auswahl **Marken-Look** direkt auf der Wochenkarte |

🚨 **Warum B intern springt statt in den Bild-Editor:** Zwei Artifacts koennen nicht
miteinander reden, und ein Sprung nach drueben verliert den Beitrag. Das Reel-Studio
im Cockpit kann alles, was fuers Cover noetig ist — Video laden, Standbild vorschlagen,
Hook drauf, PNG speichern. Der kurze Weg ist der, der nicht ueber die Grenze geht.

Quelle ist die LIVE-Fassung des Artifacts, nicht `outputs/cockpit/mlb-cockpit.html` —
die beiden sind ab Zeile 3126 auseinandergelaufen. Das Skript schreibt die reparierte
Fassung in beide.

    python scripts/cockpit/patch-wochenkarte-bauen.py <live-html> <ziel-html>
"""
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def ersetze(text, alt, neu, was):
    n = text.count(alt)
    if n != 1:
        sys.exit(f"ABBRUCH bei {was}: {n} Treffer statt 1.")
    print(f"  ok  {was}")
    return text.replace(alt, neu)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    quelle, ziel = Path(sys.argv[1]), Path(sys.argv[2])
    zeilen = quelle.read_text(encoding="utf-8").splitlines()

    # Die Huelle, die beim Veroeffentlichen selbst dazukommt, muss raus —
    # sonst steht sie nach dem naechsten Publish zweimal da.
    if zeilen[0].startswith("<!doctype"):
        zeilen = zeilen[1:]
    if zeilen[-1].strip() == "</body></html>":
        zeilen = zeilen[:-1]
    t = "\n".join(zeilen)

    # --- A0 · Ein Link, der wie ein Knopf aussehen soll ------------------
    t = ersetze(
        t,
        "  .btn[disabled] { opacity: 0.45; cursor: not-allowed; }",
        "\n".join([
            "  .btn[disabled] { opacity: 0.45; cursor: not-allowed; }",
            "  /* Ein Link, der als Knopf auftritt: ohne das ist er unterstrichen",
            "     und sitzt als Inline-Element schief in der Fusszeile. */",
            "  a.btn { display: inline-block; text-decoration: none;"
            " line-height: normal; }",
        ]),
        "A0 Knopf-Optik fuer Links")

    # --- A · Der Knopf wird ein Link -------------------------------------
    t = ersetze(
        t,
        """          '<button class="btn">Im Bild-Editor bauen</button>' +""",
        """          '<a class="btn wk-editorlink" href="' + BILDEDITOR +
            '" target="_blank" rel="noopener">Im Bild-Editor bauen</a>' +""",
        "A1 Knopf zu Link")

    t = ersetze(
        t,
        """    felder[2].onclick = function () {
      // Gebaut wird im Bild-Editor — hier wird nur geprüft und freigegeben.
      if (b.art === "karussells") activeCarousel = b.obj.id;
      window.open(BILDEDITOR, "_blank", "noopener");
    };""",
        """    // 🚨 Frueher stand hier window.open(). In einem Artifact-Rahmen ist das
    // blockiert, und zwar lautlos — Patricia hat geklickt und nichts passierte.
    // Ein echter Link mit target="_blank" geht durch, weil die Person ihn selbst
    // anklickt. Zusaetzlich wandert die Adresse in die Zwischenablage, damit sie
    // sie notfalls von Hand einsetzen kann.
    var editorLink = karte.querySelector(".wk-editorlink");
    if (editorLink) {
      editorLink.onclick = function () {
        if (b.art === "karussells") activeCarousel = b.obj.id;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(BILDEDITOR).catch(function () {});
        }
        toast("Bild-Editor wird geöffnet. Falls nichts aufgeht: der Link ist kopiert.");
      };
    }""",
        "A2 Klick-Verdrahtung")

    # --- B · Cover bauen, intern ins Reel-Studio --------------------------
    t = ersetze(
        t,
        """      farbwahl += '<div class="wk-holen">' +
        (b.videourl ? '<button class="btn" data-holen="video">Video speichern</button>' : "") +
        (quelle ? '<button class="btn" data-holen="cover">Cover speichern</button>' : "") +
        '</div>';""",
        """      farbwahl += '<div class="wk-holen">' +
        (b.videourl ? '<button class="btn" data-holen="video">Video speichern</button>' : "") +
        (quelle ? '<button class="btn" data-holen="cover">Cover speichern</button>' : "") +
        // Das Cover ist ein eigenes Bild, nicht das erste Videobild. Dieser Knopf
        // fuehrt dorthin, wo es gebaut wird — im selben Fenster.
        '<button class="btn' + (quelle ? "" : " primary") + '" data-cover="1">' +
          (quelle ? "Cover ändern" : "Cover bauen") + '</button>' +
        '</div>';""",
        "B1 Cover-Knopf")

    t = ersetze(
        t,
        """    karte.querySelectorAll(".farbknopf").forEach(function (kn) {""",
        """    // 🚨 Bleibt INNERHALB des Cockpits. Das Reel-Studio kann alles, was fuers
    // Cover gebraucht wird: Video laden, Standbild vorschlagen, Hook drauflegen,
    // als PNG speichern. Ein Sprung ins andere Artifact wuerde den Beitrag
    // verlieren — die beiden Datenbanken sind nicht verbunden.
    karte.querySelectorAll("[data-cover]").forEach(function (kn) {
      kn.onclick = function () {
        activeReel = b.obj.id;
        reelFrames = [];
        reelVideo = null;
        activeTab = "reels";
        render();
        toast("Reel-Studio offen. Video reinziehen, Standbild wählen, Cover speichern.");
      };
    });

    karte.querySelectorAll(".farbknopf").forEach(function (kn) {""",
        "B2 Cover-Verdrahtung")

    # --- C · Marken-Look beim Karussell ----------------------------------
    t = ersetze(
        t,
        """    var farbwahl = "";
    if (b.art === "reels") {""",
        """    var farbwahl = "";
    // Beim Karussell entscheidet der Marken-Look ueber die Farbe aller Folien.
    // Bisher liess sich auf der Wochenkarte der Text aendern, die Farbe nicht —
    // also musste Patricia fuer eine Farbe in ein anderes Werkzeug wechseln.
    if (b.art === "karussells") {
      farbwahl += '<div class="wk-holen"><select class="btn wk-marke">' +
        Object.keys(BRANDS).map(function (k) {
          return '<option value="' + k + '"' +
            ((b.obj.brand || "mlb_dark") === k ? " selected" : "") + '>' +
            esc(BRANDS[k].label) + '</option>';
        }).join("") + '</select>' +
        '<span class="wk-unter">Marken-Look</span></div>';
    }
    if (b.art === "reels") {""",
        "C1 Marken-Auswahl")

    t = ersetze(
        t,
        """    var profilWahl = karte.querySelector(".wk-profil");""",
        """    var markeWahl = karte.querySelector(".wk-marke");
    if (markeWahl) {
      markeWahl.onchange = function () {
        b.obj.brand = this.value;
        b.obj.handle = BRANDS[this.value].handle;
        saveCarousel(b.obj);
        render();
      };
    }

    var profilWahl = karte.querySelector(".wk-profil");""",
        "C2 Marken-Verdrahtung")

    # --- D · Der leere Platzhalter sagt, was zu tun ist -------------------
    t = ersetze(
        t,
        """          : '<div class="wk-leer">Noch kein Vorschaubild</div>');""",
        """          : '<div class="wk-leer">Noch kein Cover.<br>' +
            (b.art === "reels" ? "Knopf „Cover bauen“ darunter." : "Folien stehen rechts.") +
            '</div>');""",
        "D Platzhalter-Text")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
