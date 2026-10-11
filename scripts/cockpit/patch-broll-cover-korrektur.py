# -*- coding: utf-8 -*-
"""Korrektur: B-Roll braucht doch ein Cover — wegen des Feed-Rasters.

🚨 Ich hatte am 18.09. auf der Karte geschrieben „Kein Cover nötig — der Hook
steht ab Bild null im Video". Das stimmt für das, was **abspielt**, und ist
falsch für das, was im **Profil** steht.

Patricia sofort danach: *„ich will ja einen schönen feed haben."* Genau da
liegt der Fehler: Das Cover bestimmt die Kachel im Profil-Raster, und eine
Kachel aus einem Handyclip mit weisser Schrift drauf hat weder die Markenfarbe
noch den ABAB-Rhythmus aus `feedback_KRITISCH-feed-aesthetic-3-in-folge`.

**Richtig ist:** Der Hook im Video ist für die ersten drei Sekunden da. Das
Cover ist für das Raster. Das sind zwei verschiedene Bilder, und Instagram
lässt beim Posten ein eigenes Titelbild aus der Galerie wählen.

Die Lehre für mich: **„braucht man nicht" ist eine Aussage über einen Zweck.**
Bevor ich sie treffe, muss ich wissen, welchen Zweck die Sache hat — hier waren
es zwei, und ich hatte nur an einen gedacht.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")

ALT = """        (brollOhneCover
          ? '<a class="btn" data-cover="1" href="' + BILDEDITOR +
            '" target="_blank" rel="noopener">Cover trotzdem bauen</a>' +
            '<span class="wk-unter">Kein Cover n\\u00f6tig \\u2014 der Hook steht ' +
            'ab Bild null im Video.</span>'
          : '<a class="btn' + (quelle ? "" : " primary") + '" data-cover="1" href="' +
            BILDEDITOR + '" target="_blank" rel="noopener">' +
            (quelle ? "Cover ändern" : "Cover bauen") + '</a>') +
        '</div>';
"""

NEU = """        '<a class="btn' + (quelle ? "" : " primary") + '" data-cover="1" href="' +
          BILDEDITOR + '" target="_blank" rel="noopener">' +
          (quelle ? "Cover ändern" : "Cover bauen") + '</a>' +
        // 🚨 Auch B-Roll braucht ein Cover. Der Hook im Video ist fuer die
        // ersten drei Sekunden; das Cover ist die Kachel im Profil-Raster,
        // und die traegt den Feed-Rhythmus. Zwei verschiedene Bilder.
        (brollOhneCover
          ? '<span class="wk-unter">Der Hook im Video ist nur, was abspielt. ' +
            'Im Profil steht das Cover \\u2014 und das tr\\u00e4gt den Feed.</span>'
          : "") +
        '</div>';
"""

LEER_ALT = """            (b.art !== "reels" ? "Folien stehen rechts."
              : (b.obj.videoart || "sprech") === "broll"
                ? "Brauchst du nicht — beim B-Roll steht der Hook ab Bild null im Video."
                : "Knopf „Cover bauen“ darunter — "
                  + "Foto aus deinen Shootings, Text und Verlauf im Bild-Editor.") +"""

LEER_NEU = """            (b.art !== "reels" ? "Folien stehen rechts."
              : "Knopf „Cover bauen“ darunter — Foto aus deinen Shootings, "
                + "Text und Verlauf im Bild-Editor. Beim Posten in Instagram "
                + "unter „Cover“ aus der Galerie wählen.") +"""


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

    tausche(ALT, NEU, "Cover-Knopf wieder normal, Hinweis richtiggestellt")
    tausche(LEER_ALT, LEER_NEU, "Platzhaltertext richtiggestellt")

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
