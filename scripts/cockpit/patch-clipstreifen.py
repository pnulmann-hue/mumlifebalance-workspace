# -*- coding: utf-8 -*-
"""Ein Clip-Streifen im Reel-Studio — auswaehlen, rauswerfen, eigene dazulegen.

**Patricia, 17.09.2026:** *„ich will die clips ändern können, wie ich auch die bilder
ändern kann"* — und direkt danach: *„kann ich sie auch selber rauswerfen und ersetzen
wenn ich mal was anpassen will?"*

Also dasselbe wie beim Foto-Streifen, nur fuer Video: antippen setzt den Clip ans Reel,
✕ wirft ihn aus der Ablage, und ein eigener laesst sich dazulegen.

## Wie die Ablage aufgebaut ist

| | |
|---|---|
| **Die Datei** | liegt im Anhang des Artifacts (`assets`), erreichbar unter `/_blob/<id>` |
| **Die Liste** | liegt in `daten/clips` (`db`) und ist das Verzeichnis |

🚨 **Die Liste ist der Index, nicht die Anhang-Ablage.** `assets.list()` liefert nur
Groesse und Typ, keine Namen — wer daraus eine Auswahl baut, zeigt ihr eine Wand aus
Kennungen. Der Name steht in `daten/clips`, und nur dort.

🚨 **Loeschen ist endgueltig und gilt fuer alle Ansichten.** Deshalb prueft der Knopf
vorher, ob ein Beitrag diesen Clip benutzt, und sagt es. Erst danach wird
`assets.delete` gerufen und die Zeile aus der Liste genommen — in derselben Handlung,
sonst zeigt die Liste auf eine Datei, die es nicht mehr gibt.

🚨 **20 MiB je Datei.** Ein Handy-Video von 40 Sekunden reisst das. Der Uploader sagt
das vorher, statt den Fehler erst von der Schnittstelle zu holen.

**Das Vorschaubild kommt aus dem Video selbst** (`<video preload="metadata">` zeigt das
erste Bild). Kein zweites Bild je Clip, kein zusaetzlicher Anhang.

    python scripts/cockpit/patch-clipstreifen.py <html> <html>
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

    # --- A · Aussehen -----------------------------------------------------
    t = ersetze(
        t,
        "  .wk-auftrag { display: flex; gap: 8px; align-items: center;",
        "\n".join([
            "  /* Clip-Ablage im Reel-Studio — gebaut wie der Foto-Streifen im",
            "     Bild-Editor: Miniaturen in einer Reihe, antippen waehlt aus. */",
            "  .clipstreifen { display: flex; gap: 10px; overflow-x: auto;"
            " padding: 4px 2px 10px; }",
            "  .clipkachel { position: relative; flex: 0 0 auto; width: 92px; }",
            "  .clipkachel video { width: 92px; height: 164px; object-fit: cover;"
            " border-radius: 8px; border: 3px solid transparent; cursor: pointer;"
            " background: #0c1c30; display: block; }",
            "  .clipkachel.aktiv video { border-color: var(--petrol); }",
            "  .clipkachel .clipname { font-size: 11px; color: var(--ink-soft);"
            " margin-top: 3px; line-height: 1.25;"
            " display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;"
            " overflow: hidden; }",
            "  .clipweg { position: absolute; top: 4px; right: 4px; width: 22px;"
            " height: 22px; border-radius: 50%; border: 0; cursor: pointer;"
            " background: rgba(12,28,48,0.72); color: #fff; font-size: 13px;"
            " line-height: 22px; padding: 0; }",
            "  .clipweg:hover { background: #c0392b; }",
            "",
            "  .wk-auftrag { display: flex; gap: 8px; align-items: center;",
        ]),
        "A Aussehen")

    # --- B · Zustand und Laden -------------------------------------------
    t = ersetze(
        t,
        "  function kartenProfil(o) {",
        "\n".join([
            "  /* ---------- Clip-Ablage ----------",
            "     `clips` ist das Verzeichnis: je Eintrag {id, name, asset}. Die Datei",
            "     selbst haengt als Anhang am Artifact und wird ueber /_blob/<asset>",
            "     ausgeliefert. \U0001F6A8 assets.list() taugt NICHT als Quelle — dort stehen",
            "     keine Namen. */",
            "  var clips = [];",
            "  var assetsAPI = null;",
            "",
            "  function clipsLaden() {",
            "    clips = lsGet(\"clips\", []) || [];",
            "    if (!db) return;",
            "    db.doc(\"daten/clips\").get().then(function (snap) {",
            "      if (snap.exists) {",
            "        clips = (snap.data() || {}).clips || [];",
            "        lsSet(\"clips\", clips);",
            "        if (activeTab === \"reels\") render();",
            "      }",
            "    }).catch(function () {});",
            "  }",
            "  function clipsSichern() {",
            "    lsSet(\"clips\", clips);",
            "    if (!db) return;",
            "    db.doc(\"daten/clips\").set({ clips: clips, stand: new Date().toISOString() })",
            "      .catch(function () { toast(\"Die Clip-Liste liess sich nicht sichern.\"); });",
            "  }",
            "",
            "  function kartenProfil(o) {",
        ]),
        "B Zustand")

    # --- C · Beim Start laden --------------------------------------------
    t = ersetze(
        t,
        """  (lsGet("reelliste", []) || []).forEach(function (id) {""",
        "\n".join([
            "  clipsLaden();",
            "  if (window.claude && window.claude.use) {",
            "    // Nur Schreibende bekommen `assets`; bei einer Lese-Ansicht bleibt es",
            "    // null, und der Uploader wird gar nicht erst angezeigt.",
            "    window.claude.use(\"assets\").then(function (a) {",
            "      assetsAPI = a;",
            "      if (activeTab === \"reels\") render();",
            "    }).catch(function () {});",
            "  }",
            "",
            """  (lsGet("reelliste", []) || []).forEach(function (id) {""",
        ]),
        "C Beim Start")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
