# -*- coding: utf-8 -*-
"""Schickt „Cover bauen" dorthin, wo Shootingbilder liegen — in den Bild-Editor.

**Korrektur meines eigenen Patches vom selben Tag.** `patch-wochenkarte-bauen.py` hat
den Knopf ins **Reel-Studio** im Cockpit gelegt. Das war falsch: das Reel-Studio zieht
ein **Standbild aus dem Video**. Patricia will aber ein Cover aus ihren Shootingbildern,
mit wechselbarem Bild, freiem Text, verschiebbarer Texthöhe und wahlweise Verlauf,
Unifarbe oder gar keinem Verlauf — und das kann nur der Bild-Editor.

Ihr Wortlaut vom 16.09.2026: *„ich will aber ein Cover aus meinen Shootingbildern. wir
haben das mal definiert. dass ich das Bild ändern kann, den Text auch, die höhe des
Textes und der Verlauf. ob es kein Verlauf drin hat oder in einer meiner
Brandingfarben"* — Punkt für Punkt das, was der Bild-Editor seit dem 14.09. kann.

**Der Beitrag geht beim Sprung nicht verloren.** Das war der Grund für den internen
Sprung, und er ist ausgeräumt: alle Reels und Karussells stehen seit dem 16.09. als
`daten/entwuerfe` in der Bild-Editor-Datenbank (`reel-cover-entwuerfe.py`). Drüben
erscheinen sie unter **„Aus deiner Planung"** — Beitrag antippen, Titelzeile und
Unterzeile stehen auf einem 9:16-Cover, Shootingbild dazu, fertig.

**Das Reel-Studio bleibt**, es hat weiter seinen Zweck: ein Standbild aus einem
gedrehten Video, wenn genau das gewollt ist.

    python scripts/cockpit/patch-cover-bildeditor.py <html> <html>
"""
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
    if zeilen and zeilen[0].startswith("<!doctype"):
        zeilen = zeilen[1:]
    if zeilen and zeilen[-1].strip() == "</body></html>":
        zeilen = zeilen[:-1]
    t = "\n".join(zeilen)

    # --- 1 · Aus dem Knopf wird ein Link ---------------------------------
    t = ersetze(
        t,
        """        // Das Cover ist ein eigenes Bild, nicht das erste Videobild. Dieser Knopf
        // fuehrt dorthin, wo es gebaut wird — im selben Fenster.
        '<button class="btn' + (quelle ? "" : " primary") + '" data-cover="1">' +
          (quelle ? "Cover ändern" : "Cover bauen") + '</button>' +""",
        """        // Das Cover ist ein eigenes Bild, nicht das erste Videobild. Gebaut wird
        // es im Bild-Editor — dort liegen die Shootingbilder, der Verlauf-Regler
        // und die verschiebbare Texthöhe. Muss ein Link sein: window.open() ist
        // im Artifact-Rahmen blockiert.
        '<a class="btn' + (quelle ? "" : " primary") + '" data-cover="1" href="' +
          BILDEDITOR + '" target="_blank" rel="noopener">' +
          (quelle ? "Cover ändern" : "Cover bauen") + '</a>' +""",
        "1 Cover-Knopf wird Link")

    # --- 2 · Neuer Klick-Text statt Sprung ins Reel-Studio ----------------
    t = ersetze(
        t,
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
    });""",
        """    // 🚨 Fuehrt in den Bild-Editor, nicht ins Reel-Studio. Das Reel-Studio zieht
    // ein Standbild aus dem Video — ein Cover aus den Shootingbildern gibt es nur
    // drueben. Der Beitrag geht dabei nicht verloren: alle Reels stehen als
    // `daten/entwuerfe` in der Bild-Editor-Datenbank und erscheinen dort unter
    // „Aus deiner Planung“.
    karte.querySelectorAll("[data-cover]").forEach(function (kn) {
      kn.onclick = function () {
        if (navigator.clipboard) {
          navigator.clipboard.writeText(BILDEDITOR).catch(function () {});
        }
        toast("Bild-Editor: oben „Reel-Cover 9:16“ wählen, dann unter " +
              "„Aus deiner Planung“ „" + (b.obj.name || "diesen Beitrag") +
              "“ antippen.");
      };
    });""",
        "2 Klick-Verdrahtung")

    # --- 3 · Der leere Platzhalter nennt den richtigen Ort ----------------
    t = ersetze(
        t,
        """            (b.art === "reels" ? "Knopf „Cover bauen“ darunter." : "Folien stehen rechts.") +""",
        """            (b.art === "reels" ? "Knopf „Cover bauen“ darunter — "
                + "Foto aus deinen Shootings, Text und Verlauf im Bild-Editor."
              : "Folien stehen rechts.") +""",
        "3 Platzhalter-Text")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
