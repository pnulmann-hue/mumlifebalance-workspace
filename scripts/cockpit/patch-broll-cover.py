# -*- coding: utf-8 -*-
"""B-Roll braucht kein eigenes Cover — das sagt die Karte jetzt auch.

Anlass (Patricia, 18.09.2026): *„und die Reelcover.. für die B-Roll-Reels..
muss ich die hier selber holen? auch im bildgenerator generieren? oder geht das
in der wochenvorschau"*

**Die Antwort ist: gar nicht.** Bei einem B-Roll steht der ganze Hook ab Bild
null im Video. Das erste Bild IST also schon das Cover — Instagram lässt beim
Posten ein Videobild als Titelbild wählen, und das trägt den Text bereits.

🚨 **Die Karte hat trotzdem „Cover bauen" in Petrol angeboten**, gleich
auffällig wie bei einem Sprechreel. Also sah es nach einer offenen Aufgabe aus,
die keine ist. Ein Knopf, der nach Pflicht aussieht, erzeugt Arbeit.

Beim Sprechreel bleibt alles wie es war: dort ist das Cover ein eigenes Bild
aus den Shootings und wird im Bild-Editor gebaut.

Wiederholbar.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")

ALT = """        '<a class="btn' + (quelle ? "" : " primary") + '" data-cover="1" href="' +
          BILDEDITOR + '" target="_blank" rel="noopener">' +
          (quelle ? "Cover ändern" : "Cover bauen") + '</a>' +
        '</div>';
"""

NEU = """        // 🚨 Bei B-Roll steht der ganze Hook ab Bild null im Video — das erste
        // Videobild ist damit schon das Cover. Der Knopf bleibt, aber unauffaellig
        // und mit Ansage, sonst sieht er aus wie eine offene Aufgabe.
        (brollOhneCover
          ? '<a class="btn" data-cover="1" href="' + BILDEDITOR +
            '" target="_blank" rel="noopener">Cover trotzdem bauen</a>' +
            '<span class="wk-unter">Kein Cover n\\u00f6tig \\u2014 der Hook steht ' +
            'ab Bild null im Video.</span>'
          : '<a class="btn' + (quelle ? "" : " primary") + '" data-cover="1" href="' +
            BILDEDITOR + '" target="_blank" rel="noopener">' +
            (quelle ? "Cover ändern" : "Cover bauen") + '</a>') +
        '</div>';
"""

# Die Variable muss oben in der Funktion stehen, bevor `farbwahl` gebaut wird.
VAR_ALT = """    if (b.art === "reels") {
      if (b.videourl && quelle) {
        farbwahl += '<img class="wk-covermini" src="' + quelle + '" alt="Cover">';
      }
"""

VAR_NEU = """    var brollOhneCover = (b.art === "reels" &&
                          (b.obj.videoart || "sprech") === "broll" && !quelle);
    if (b.art === "reels") {
      if (b.videourl && quelle) {
        farbwahl += '<img class="wk-covermini" src="' + quelle + '" alt="Cover">';
      }
"""

# Und der leere Platzhalter soll bei B-Roll nichts von „Cover bauen" erzaehlen.
LEER_ALT = """            (b.art === "reels" ? "Knopf „Cover bauen“ darunter — "
                + "Foto aus deinen Shootings, Text und Verlauf im Bild-Editor."
              : "Folien stehen rechts.") +"""

LEER_NEU = """            (b.art !== "reels" ? "Folien stehen rechts."
              : (b.obj.videoart || "sprech") === "broll"
                ? "Brauchst du nicht — beim B-Roll steht der Hook ab Bild null im Video."
                : "Knopf „Cover bauen“ darunter — "
                  + "Foto aus deinen Shootings, Text und Verlauf im Bild-Editor.") +"""


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

    tausche(VAR_ALT, VAR_NEU, "brollOhneCover bestimmen")
    tausche(ALT, NEU, "Cover-Knopf bei B-Roll zurueckstufen")
    tausche(LEER_ALT, LEER_NEU, "Platzhaltertext bei B-Roll")

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
