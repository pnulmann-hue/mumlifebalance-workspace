"""Die Wochen-Vorschau zeigt wieder die Woche.

Patricia am 24.09.2026: *„jetzt ist mir zu unübersichtlich…"* — und auf die
Rückfrage: *„vor allem die wochenvorschau der beiträge. weil da einfach alles
durcheinander kommt"*.

**Gemessen statt geraten** (lokale Testfassung, 24.09.2026):

| | |
|---|---:|
| Zeilen in „Was zu tun ist" | 85 |
| davon **ohne Datum** | **67** |
| Seitenhöhe | 13'250 px |
| Bildschirm, ab dem die Woche beginnt | der **siebte** |

🚨 **Ohne Datum ist nichts eine Aufgabe.** Die 67 datumslosen Zeilen sind die
A/B-Varianten aus der Freitagsproduktion, die nie ausgewählt wurden — für jede
stand „Video fehlt" oder „Kein Datum" da. Die Regel steht seit dem 24.09. im
Auftrag des Cockpit-Bots, im Cockpit selbst stand sie nie. Eine Aufgabe, die
keine ist, kostet Vertrauen in die ganze Liste; siebzig davon kosten die Liste.
**Verloren geht nichts** — was kein Datum hat, steht unten in der Ideenliste,
und dort gehört es hin.

🚨 **Die Woche kommt zuerst.** Der Aufgabenblock stand über der Liste und war
damit das Erste, was die Seite zeigte — auf einer Seite, die „Wochen-Vorschau"
heisst. Jetzt steht er darunter.

🚨 **Zugeklappt, mit der Zahl dran.** Als `<details>`, nicht über einen eigenen
Zustand: kein JS, kein `localStorage`, und beim Neuzeichnen kann nichts
auseinanderlaufen. Die Zahl im Kopf sagt, wie viel dahintersteckt — ein
zugeklappter Block ohne Zahl verschweigt, dass dort etwas wartet.

    python scripts/cockpit/patch-woche-aufraeumen.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------- 1 · Reihenfolge + Kopftext

KOPF_ALT = """      '<div class="page-head"><div><h1>Wochen-Vorschau</h1>' +
      '<p>Pro Tag und Profil ein Platz. \\u00dcber \\u201eWechseln\\u201c legst du die ' +
      'Variante drauf, die rausgehen soll \\u2014 die andere f\\u00e4llt zur\\u00fcck in die ' +
      'Ideenliste ganz unten. Storys stehen im Bild-Editor unter ' +
      '\\u201eAus deiner Planung\\u201c.</p></div>' +"""

KOPF_NEU = """      '<div class="page-head"><div><h1>Wochen-Vorschau</h1>' +
      '<p>Pro Tag und Profil ein Platz. \\u201eWechseln\\u201c legt eine andere ' +
      'Variante drauf.</p></div>' +"""

# Der Aufgabenblock wandert unter die Liste.
ORDER_ALT = """      bilanzBlock(tage, belegt) +
      aufgabenBlock(beitraege) +
      '<div id="wliste"></div>' +
      '<div id="wunten"></div>';"""

ORDER_NEU = """      bilanzBlock(tage, belegt) +
      // Erst die Woche, dann die Liste - siehe Kopf von
      // patch-woche-aufraeumen.py.
      '<div id="wliste"></div>' +
      aufgabenBlock(beitraege) +
      '<div id="wunten"></div>';"""

# --------------------------------------------------------- 2 · aufgabenBlock

BLOCK_ALT_ANFANG = "  function aufgabenBlock(beitraege) {"
BLOCK_ALT_ENDE = """    });
    return h + '</div>';
  }"""

BLOCK_NEU = r'''  function aufgabenBlock(beitraege) {
    var offen = [], ohneDatum = 0;
    beitraege.forEach(function (b) {
      if (istLeer(b)) return;   // ein leerer Entwurf ist keine Aufgabe
      var f = wasFehlt(b);
      if (!f.length) return;
      // 🚨 Ohne Datum ist nichts eine Aufgabe. Das sind die A/B-Varianten aus
      // der Freitagsproduktion, die nie ausgewaehlt wurden - 67 von 85 Zeilen
      // am 24.09.2026. Sie stehen unten in der Ideenliste, und dort gehoeren
      // sie hin.
      if (!b.obj.datum) { ohneDatum++; return; }
      f.forEach(function (x) { offen.push({ b: b, f: x }); });
    });

    var rest = ohneDatum
      ? '<p class="note">' + ohneDatum + ' weitere Entwürfe haben noch kein ' +
        'Datum. Die stehen unten in der Ideenliste — solange dort kein Tag ' +
        'dransteht, ist es keine Aufgabe.</p>'
      : "";

    if (!offen.length) {
      return '<div class="panel tuliste"><h2>Was zu tun ist</h2>' +
             '<div class="empty">Nichts offen — jeder eingeplante Beitrag hat ' +
             'Video, Caption und Datum.</div>' + rest + '</div>';
    }

    offen.sort(function (x, y) {
      var a = x.b.obj.datum, c = y.b.obj.datum;
      return a < c ? -1 : (a > c ? 1 : 0);
    });
    var vonDir = offen.filter(function (x) { return x.f.wer === "du"; }).length;
    var vonMir = offen.length - vonDir;

    /* <details> statt eigener Zustand: kein JS, kein localStorage, und beim
       Neuzeichnen kann nichts auseinanderlaufen. Die Zahl steht im Kopf -
       ein zugeklappter Block ohne Zahl verschweigt, dass etwas wartet. */
    var h = '<details class="panel tuliste tuklapp"><summary>' +
      '<span class="tu-titel">Was zu tun ist</span>' +
      (vonDir ? '<span class="tu-zahl du">' + vonDir + ' von dir</span>' : "") +
      (vonMir ? '<span class="tu-zahl ich">' + vonMir + ' von mir</span>' : "") +
      '</summary>' +
      '<p class="note">Was bei dir steht, hält den Beitrag auf — alles ' +
      'andere läuft auch ohne dich weiter.</p>';
    offen.forEach(function (x) {
      h += '<div class="tuzeile">' +
        '<span class="tudatum">' +
          esc(tagName(x.b.obj.datum).slice(0, 2) + " " + fmtDate(x.b.obj.datum)) +
        '</span>' +
        '<span class="tuwas"><strong>' + esc(x.f.was) + '</strong> — ' +
          esc(x.b.titel) + '</span>' +
        '<span class="tuwer ' + x.f.wer + '">' +
          (x.f.wer === "du" ? "von dir" : "von mir") + '</span>' +
        '</div>';
    });
    return h + rest + '</details>';
  }'''

# ------------------------------------------------------------------ 3 · CSS

CSS_ALT = "  .wslot.durch { opacity: 0.62; }"
CSS_NEU = r'''  /* Aufgabenliste zugeklappt (24.09.2026). */
  .tuklapp > summary {
    display: flex; align-items: center; gap: 10px; cursor: pointer;
    list-style: none; padding: 2px 0;
  }
  .tuklapp > summary::-webkit-details-marker { display: none; }
  .tuklapp > summary::before {
    content: "\25b6"; font-size: 10px; color: var(--ink-soft);
    transition: transform 0.15s ease;
  }
  .tuklapp[open] > summary::before { transform: rotate(90deg); }
  .tuklapp .tu-titel {
    font-family: var(--display); font-size: 17px; color: var(--ink);
  }
  .tuklapp .tu-zahl {
    font-size: 12px; border-radius: 999px; padding: 2px 9px;
    background: var(--surface-2); color: var(--ink-soft);
  }
  .tuklapp .tu-zahl.du { background: var(--warn-soft, #fbe7d8); color: #8a4b1c; }
  .tuklapp[open] > summary { margin-bottom: 10px; }
  .wslot.durch { opacity: 0.62; }'''


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
    if "tuklapp" in s:
        print("  Schon aufgeräumt — nichts zu tun.")
        return

    s = setze(s, KOPF_ALT, KOPF_NEU, "Kopftext")
    s = setze(s, ORDER_ALT, ORDER_NEU, "Reihenfolge")
    s = setze(s, CSS_ALT, CSS_NEU, "CSS")

    # aufgabenBlock als Ganzes ersetzen
    a = s.find(BLOCK_ALT_ANFANG)
    if a < 0:
        sys.exit("🚨 aufgabenBlock nicht gefunden.")
    b = s.find(BLOCK_ALT_ENDE, a)
    if b < 0:
        sys.exit("🚨 Ende von aufgabenBlock nicht gefunden.")
    print("  Alte Funktion: %d Zeichen" % (b + len(BLOCK_ALT_ENDE) - a))
    s = s[:a] + BLOCK_NEU + s[b + len(BLOCK_ALT_ENDE):]

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Wochen-Vorschau aufgeräumt · %d KB" % (len(s) / 1024))
    print("  Woche zuerst · Liste zugeklappt · nur Beiträge mit Datum.")


if __name__ == "__main__":
    main()
