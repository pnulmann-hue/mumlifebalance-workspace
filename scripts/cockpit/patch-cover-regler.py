# -*- coding: utf-8 -*-
"""Text auf dem Cover frei verschieben und in der Groesse aendern.

**Patricia, 16.09.2026:** *„ich will auch den text auf dem cover verschieben können und
verkleinern oder vergrössern"* — und schon in ihrer ersten Aufzaehlung stand
*„die höhe des Textes"* als eine von vier Zusagen.

**Warum eine feste Position nicht reicht.** Bei der Sichtpruefung mit dem Textfeld ueber
fuenf Shootingbildern lag ihr Gesicht bei **drei von fuenf** mitten im Textblock. Die
drei Vorgaben oben/mittig/unten treffen je nach Foto daneben, und „unten" faellt
ohnehin in die tote Zone, wo Instagram Caption und Knöpfe darueberlegt.

**Zwei neue Felder:**

| Feld | Bedeutung | Vorgabe |
|---|---|---|
| `texty` | Hoehe des Textblocks in Prozent der Bildhoehe | aus `pos` abgeleitet |
| `textskala` | Schriftgroesse in Prozent | 100 |

`pos` bleibt als Rueckfall erhalten, damit bestehende Reels sich nicht veraendern:
`oben` → 16 % · `mitte` → mittig gerechnet · `unten` → 76 %.

🚨 **Der Regler ist bei 82 % begrenzt, nicht bei 100.** Darunter beginnt die tote Zone
(82–100 %), in der Instagram Caption und Bedienknöpfe ueber das Cover legt. Ein Regler,
der dorthin laesst, produziert Cover, die im Feed halb verdeckt sind.

    python scripts/cockpit/patch-cover-regler.py <html> <html>
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

    # --- 1 · Schriftgroesse skalierbar -----------------------------------
    t = ersetze(
        t,
        """      var h = fitLines(ctx, String(coverText).toUpperCase(), maxW, RH * 0.34, b.display, "bold", 104, 44, 1.12);""",
        "\n".join([
            "      // Schriftgroesse als Faktor. `fitLines` verkleinert weiter, wenn der Text",
            "      // sonst nicht in die erlaubte Hoehe passt — der Regler hebt nur die",
            "      // Obergrenze an oder senkt sie.",
            "      var sk = Math.max(0.6, Math.min(1.5, (r.textskala || 100) / 100));",
            "      var h = fitLines(ctx, String(coverText).toUpperCase(), maxW, RH * 0.34 * sk,",
            '                       b.display, "bold", Math.round(104 * sk),'
            " Math.round(44 * sk), 1.12);",
        ]),
        "1 Schriftgroesse")

    t = ersetze(
        t,
        """      if (coverUnter) {
        ctx.font = "40px " + b.body;
        uLines = wrap(ctx, coverUnter, maxW).slice(0, 3);
      }""",
        "\n".join([
            "      var uSize = Math.round(40 * sk);",
            "      if (coverUnter) {",
            '        ctx.font = uSize + "px " + b.body;',
            "        uLines = wrap(ctx, coverUnter, maxW).slice(0, 3);",
            "      }",
        ]),
        "2 Unterzeile skaliert")

    t = ersetze(
        t,
        """      var blockH = h.lines.length * h.size * 1.12 + (uLines.length ? uLines.length * 56 + 34 : 0);
      var y;
      if (r.pos === "oben") y = 300;
      else if (r.pos === "mitte") y = (RH - blockH) / 2;
      else y = RH - 470 - blockH;""",
        "\n".join([
            "      var uZeile = Math.round(56 * sk);",
            "      var blockH = h.lines.length * h.size * 1.12 +",
            "                   (uLines.length ? uLines.length * uZeile + 34 : 0);",
            "      var y;",
            "      if (typeof r.texty === \"number\") {",
            "        // Freie Hoehe in Prozent. \U0001F6A8 Bei 82 % beginnt die tote Zone, in der",
            "        // Instagram Caption und Knöpfe drueberlegt — der Block darf nicht",
            "        // hineinragen, deshalb wird gegen blockH begrenzt.",
            "        var maxY = RH * 0.82 - blockH;",
            "        y = Math.max(RH * 0.13, Math.min(maxY, RH * (r.texty / 100)));",
            '      } else if (r.pos === "oben") y = 300;',
            '      else if (r.pos === "mitte") y = (RH - blockH) / 2;',
            "      else y = RH - 470 - blockH;",
        ]),
        "3 Freie Hoehe")

    t = ersetze(
        t,
        """      if (uLines.length) {
        ctx.font = "40px " + b.body;
        ctx.fillStyle = opts.transparent ? "rgba(255,255,255,0.92)" : b.muted;
        uLines.forEach(function (ln, i) { ctx.fillText(ln, pad, uy + 40 + i * 56); });
      }""",
        "\n".join([
            "      if (uLines.length) {",
            '        ctx.font = uSize + "px " + b.body;',
            '        ctx.fillStyle = opts.transparent ? "rgba(255,255,255,0.92)" : b.muted;',
            "        uLines.forEach(function (ln, i) {",
            "          ctx.fillText(ln, pad, uy + uSize + i * uZeile);",
            "        });",
            "      }",
        ]),
        "4 Unterzeile zeichnen")

    # --- 2 · Die zwei Regler ins Reel-Studio ------------------------------
    t = ersetze(
        t,
        """    posSel.onchange = function () { r.pos = posSel.value; saveReel(r); zeichneVorschau(); };""",
        "\n".join([
            "    posSel.onchange = function () {",
            "      r.pos = posSel.value;",
            "      // Eine Auswahl setzt die freie Hoehe zurueck, sonst haette der Regler",
            "      // immer Vorrang und die drei Vorgaben taeten nichts mehr.",
            "      r.texty = null;",
            "      saveReel(r); zeichneVorschau(); render();",
            "    };",
        ]),
        "5 Vorgabe setzt Regler zurueck")

    t = ersetze(
        t,
        """    var brandSel = document.createElement("select");
    Object.keys(BRANDS).forEach(function (k) {""",
        "\n".join([
            "    // \U0001F6A8 Zwei Regler statt drei fester Positionen: bei drei von fuenf",
            "    // Shootingbildern lag Patricias Gesicht im Textblock, und kein fester Wert",
            "    // passt auf alle Fotos.",
            "    function regler(titel, feldname, min, max, start, einheit) {",
            '      var box = document.createElement("div");',
            '      box.style.cssText = "flex:1 1 200px;min-width:180px";',
            '      var lab = document.createElement("label");',
            '      lab.style.cssText = "font-size:13px;display:block;margin-bottom:2px";',
            '      var sl = document.createElement("input");',
            '      sl.type = "range"; sl.min = min; sl.max = max;',
            "      sl.value = (typeof r[feldname] === \"number\") ? r[feldname] : start;",
            '      sl.style.width = "100%";',
            "      function beschriften() {",
            "        lab.textContent = titel + \": \" + sl.value + einheit;",
            "      }",
            "      beschriften();",
            "      sl.oninput = function () {",
            "        r[feldname] = +sl.value;",
            "        beschriften();",
            "        zeichneVorschau();",
            "      };",
            "      sl.onchange = function () { saveReel(r); render(); };",
            "      box.appendChild(lab); box.appendChild(sl);",
            "      return box;",
            "    }",
            "",
            '    var brandSel = document.createElement("select");',
            "    Object.keys(BRANDS).forEach(function (k) {",
        ]),
        "6 Regler-Baustein")

    # Die Regler unter die Zeile haengen, in der posSel und brandSel sitzen.
    t = ersetze(
        t,
        """    posSel.onchange = function () {
      r.pos = posSel.value;""",
        """    posSel.title = "Grobe Lage. Feiner geht es mit dem Regler darunter.";
    posSel.onchange = function () {
      r.pos = posSel.value;""",
        "7 Hinweis an der Auswahl")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
