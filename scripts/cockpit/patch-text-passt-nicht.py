"""Text bricht nicht mehr mitten im Wort ab — und sagt, wenn er nicht passt.

Patricia am 25.09.2026: *„oft hast du texte nicht durchgehend geschrieben. es
bricht einfach in einem wort ab"*.

🚨 **In den Daten steht kein abgebrochener Text.** Alle 101 Story-Folien sind
vollständig. Der Abbruch entsteht erst beim **Zeichnen** — und zwar durch zwei
Fehler in derselben Funktion:

**1 · `wrap()` bricht nur an Leerzeichen.**

```js
var words = para.split(/\\s+/).filter(Boolean);
```

Ein einzelnes Wort, das breiter ist als die Fläche — ein langes Kompositum, eine
Adresse, ein Stichwort in Grossbuchstaben — passt nie in eine Zeile und läuft
seitlich hinaus. Das `clip()` schneidet es ab, **mitten im Wort**. Genau das,
was Patricia sieht.

**2 · `fitLines()` gibt bei der kleinsten Schrift auf und zeichnet trotzdem:**

```js
while (size > min) { … size -= 4; }
return { size: min, lines: wrap(ctx, text, maxW) };   // ohne Prüfung
```

Passt der Text auch bei `min` nicht, kommen **alle** Zeilen zurück. Gezeichnet
wird bis zum Rand, der Rest verschwindet — lautlos. Die längste Folie im
Bestand hat **209 Zeichen**, bei einem Median von 88.

**Was sich ändert:**

| | |
|---|---|
| `wrap` | bricht ein zu breites Wort **hart** um, Zeichen für Zeichen |
| `fitLines` | gibt `zuLang: true` zurück, wenn es bei `min` nicht passt |
| Story-Studio und Wochenkarte | zeigen dann einen Hinweis mit der Zeichenzahl |

🚨 **Nicht still kürzen.** Ein automatisch abgeschnittener Text sieht aus wie
ein fertiger — dieselbe Falle wie „Freigegeben und abgelegt", während nichts
passieren konnte. Der Hinweis sagt, welche Folie zu lang ist; **gekürzt wird
von Hand**, weil nur Patricia weiss, welcher Satz weg darf.

🚨 **Der harte Umbruch ist die Notbremse, nicht der Normalfall.** Er greift nur
bei einem Wort, das allein schon zu breit ist. Alles andere bricht weiter an
Leerzeichen.

    python scripts/cockpit/patch-text-passt-nicht.py [--pruefen] [--datei <pfad>]
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

ALT_WRAP = '''  function wrap(ctx, text, maxW) {
    var out = [];
    String(text || "").split("\\n").forEach(function (para) {
      var words = para.split(/\\s+/).filter(Boolean);
      if (!words.length) { out.push(""); return; }
      var line = words[0];
      for (var i = 1; i < words.length; i++) {
        var test = line + " " + words[i];
        if (ctx.measureText(test).width > maxW) { out.push(line); line = words[i]; }
        else { line = test; }
      }
      out.push(line);
    });
    return out;
  }'''

NEU_WRAP = '''  /* 🚨 Ein Wort, das allein schon breiter ist als die Flaeche, passt in keine
     Zeile und laeuft seitlich hinaus — das clip() schneidet es ab, mitten im
     Wort. Genau das hat Patricia am 25.09.2026 gemeldet. Deshalb die
     Notbremse: zu breite Woerter zeichenweise trennen. Alles andere bricht
     weiter an Leerzeichen. */
  function hartTrennen(ctx, wort, maxW) {
    if (ctx.measureText(wort).width <= maxW) return [wort];
    var teile = [], rest = wort;
    while (rest && ctx.measureText(rest).width > maxW) {
      var n = 1;
      while (n < rest.length &&
             ctx.measureText(rest.slice(0, n + 1)).width <= maxW) n++;
      if (n < 1) n = 1;             // eine Zeichenbreite ist das Minimum
      teile.push(rest.slice(0, n));
      rest = rest.slice(n);
    }
    if (rest) teile.push(rest);
    return teile;
  }

  function wrap(ctx, text, maxW) {
    var out = [];
    String(text || "").split("\\n").forEach(function (para) {
      var roh = para.split(/\\s+/).filter(Boolean);
      if (!roh.length) { out.push(""); return; }
      // Zu breite Woerter vorher aufteilen, damit die Zeilenlogik darunter
      // nie ein Wort bekommt, das sie nicht unterbringen kann.
      var words = [];
      roh.forEach(function (w) {
        hartTrennen(ctx, w, maxW).forEach(function (t) { words.push(t); });
      });
      var line = words[0];
      for (var i = 1; i < words.length; i++) {
        var test = line + " " + words[i];
        if (ctx.measureText(test).width > maxW) { out.push(line); line = words[i]; }
        else { line = test; }
      }
      out.push(line);
    });
    return out;
  }'''

ALT_FIT = '''    ctx.font = weight + " " + min + "px " + family;
    return { size: min, lines: wrap(ctx, text, maxW) };
  }'''

NEU_FIT = '''    /* 🚨 Passt es auch bei der kleinsten Schrift nicht, kamen bisher trotzdem
       ALLE Zeilen zurueck — gezeichnet wurde bis zum Rand, der Rest verschwand
       lautlos. Jetzt steht das im Ergebnis, und die Ansicht sagt es.
       Still kuerzen waere falsch: ein abgeschnittener Text sieht aus wie ein
       fertiger, und nur Patricia weiss, welcher Satz weg darf. */
    ctx.font = weight + " " + min + "px " + family;
    var rest = wrap(ctx, text, maxW);
    return { size: min, lines: rest,
             zuLang: rest.length * min * lh > maxH,
             passtNicht: Math.max(0, rest.length - Math.floor(maxH / (min * lh))) };
  }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    for i, block in enumerate(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)):
        if len(block.strip()) < 200:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(block)
            p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        Path(p).unlink(missing_ok=True)
        if r.returncode != 0:
            return "Block %d: %s" % (i, (r.stderr or "")[:700])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit-neu.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "hartTrennen" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_WRAP, NEU_WRAP, "wrap")
    s = setze(s, ALT_FIT, NEU_FIT, "fitLines")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Harter Umbruch + zuLang-Befund · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
