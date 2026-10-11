# -*- coding: utf-8 -*-
"""Jeder Cover-Entwurf bringt ein vorgeschlagenes Shootingbild mit.

Anlass (Patricia, 19.09.2026): *„ich will, dass du mir für jedes reel ein
standbild aus meinem shooting mit dem hook drauf vorschlägst. und bei bedarf
soll ich das bild ändern können. sowie auch den hooktext anpassen, vergrössern,
verkleinern, verschieben usw."*

Bisher lud „Aus deiner Planung" nur den **Text** in die Folie. Das Bild blieb
auf `lounge.jpg` stehen — dem Vorgabewert der Seite. Es lag also bei jedem Cover
derselbe Hintergrund, und der Vorschlag war in Wahrheit keiner.

**Was dieser Patch macht:**
1. Zwölf weitere Shootingbilder in die Auswahl (`s01`–`s12`). Vorher neun, davon
   vier schwarzweiss — zu wenig, um vierzehn Cover zu unterscheiden.
2. Der Entwurf darf **Bild, Brandfarbe, Verlaufstärke, Schriftgrösse und Höhe**
   mitbringen. Fehlt eine Angabe, bleibt der bisherige Wert.

🚨 **Alles bleibt änderbar.** Der Vorschlag setzt nur den Startwert — Foto über
den Streifen oder „Foto wechseln", Text im Feld, Grösse und Höhe über die
Regler direkt unter dem Bild. Ein Vorschlag, den man nicht überstimmen kann,
ist eine Vorschrift.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "_bild-editor", "index.html")

FOTOS_ALT = """  const PHOTOS = ["lounge.jpg","p1.jpg","p2.jpg","p3.jpg","p4.jpg","p5.jpg","p6.jpg","p7.jpg","p8.jpg"];"""

FOTOS_NEU = """  // s01–s12 kamen am 19.09. aus dem Shooting dazu. Vorher waren es neun, davon
  // vier schwarzweiss — zu wenig, um vierzehn Cover auseinanderzuhalten.
  const PHOTOS = ["s01.jpg","s02.jpg","s03.jpg","s04.jpg","s05.jpg","s06.jpg",
                  "s07.jpg","s08.jpg","s09.jpg","s10.jpg","s11.jpg","s12.jpg",
                  "lounge.jpg","p1.jpg","p2.jpg","p3.jpg","p4.jpg","p5.jpg",
                  "p6.jpg","p7.jpg","p8.jpg"];"""

LADEN_ALT = """    const vorlage = Object.assign({}, state), stil = Object.assign({}, B());
    folien = e.folien.map(f => {
      const bl = [ Object.assign({}, stil, {headline: f.text || "", eyebrow: f.eyebrow || ""}) ];
      // Fliesstext kommt als zweiter, kleinerer Balken darunter
      if (f.unter) bl.push(Object.assign({}, stil, {headline: f.unter, eyebrow: "",
        fs: Math.max(36, Math.round(stil.fs * 0.6)), pos: Math.min(88, stil.pos + 22)}));
      return Object.assign({}, vorlage, {bloecke: bl, blk: 0});
    });
"""

LADEN_NEU = """    const vorlage = Object.assign({}, state), stil = Object.assign({}, B());
    // Der Entwurf darf Bild, Farbe und Verlauf mitbringen — das ist der
    // Vorschlag. 🚨 Nur als Startwert: Foto, Text, Grösse und Höhe bleiben
    // danach über die Regler änderbar.
    if (e.foto){ vorlage.photo = e.foto; vorlage.mode = "foto"; }
    if (e.farbe) vorlage.color = e.farbe;
    if (typeof e.grad === "number") vorlage.grad = e.grad;
    if (typeof e.fs === "number") stil.fs = e.fs;
    if (typeof e.pos === "number") stil.pos = e.pos;
    folien = e.folien.map(f => {
      const bl = [ Object.assign({}, stil, {headline: f.text || "", eyebrow: f.eyebrow || ""}) ];
      // Fliesstext kommt als zweiter, kleinerer Balken darunter
      if (f.unter) bl.push(Object.assign({}, stil, {headline: f.unter, eyebrow: "",
        fs: Math.max(36, Math.round(stil.fs * 0.6)), pos: Math.min(88, stil.pos + 22)}));
      return Object.assign({}, vorlage, {bloecke: bl, blk: 0});
    });
"""

# Die Info-Karte soll sagen, welches Bild vorgeschlagen ist.
INFO_ALT = """    box.innerHTML = `<b>${e.folien ? e.folien.length : 0} Folien</b>`
      + (e.cta ? `<br>CTA: ${esc(e.cta)}` : "")"""

INFO_NEU = """    box.innerHTML = `<b>${e.folien ? e.folien.length : 0} Folien</b>`
      + (e.fotoText ? `<br>Bildvorschlag: ${esc(e.fotoText)} — im Streifen änderbar` : "")
      + (e.cta ? `<br>CTA: ${esc(e.cta)}` : "")"""


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

    tausche(FOTOS_ALT, FOTOS_NEU, "Zwoelf Shootingbilder in die Auswahl")
    tausche(LADEN_ALT, LADEN_NEU, "Entwurf bringt Bild, Farbe und Textmasse mit")
    tausche(INFO_ALT, INFO_NEU, "Info-Karte nennt den Bildvorschlag")

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
