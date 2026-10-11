"""Beiträge, die draussen sind, zählen nicht mehr als offen.

Patricia am 24.09.2026: *„mir ist wichtig, dass die reels und beiträge, die im
feed sind, dass die nach freigegeben oder so wandern."*

🚨 **Sie hat einen echten Fehler gefunden.** `tpBelegung()` — die Funktion, die
die zehn Wochenplätze füllt — nimmt `offeneBeitraege()`, und das filtert nur
**abgelehnte** heraus. Ein freigegebener oder längst geposteter Beitrag blieb
damit auf seinem Platz stehen, als wäre er noch zu tun. Die Information war da
(`blotato.status`), sie wurde nur nirgends gelesen.

**Fünf Zustände kennt ein Beitrag heute:**

| `blotato.status` | heisst |
|---|---|
| *(leer)* | noch nicht freigegeben |
| `wartet` | freigegeben, der 20:00-Lauf holt ihn |
| `geplant` | bei Blotato eingeplant — **ist durch** |
| `gepostet-von-hand` | selbst gepostet — **ist durch** |
| `selber-posten` | B-Roll, sie postet selbst — **ist durch** |
| `zeitpunkt-vorbei` | Zeitpunkt war schon vorbei, nichts passiert |

🚨 **Ausblenden wäre falsch.** Ein Beitrag, der aus der Woche verschwindet,
lässt den Platz leer aussehen — und dann baut man denselben Tag nochmal.
Deshalb bleibt er stehen und wird **abgehakt**: gedämpft, mit Vermerk, und aus
den Zählern raus.

    python scripts/cockpit/patch-ist-draussen.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------------------- 1 · Funktion

FN_ALT = '''  /* Abgelehnt heisst: aus allen Arbeitsansichten raus, aber nicht geloescht.
     Das Feld bleibt am Beitrag, und „Zurueckholen" macht es rueckgaengig. */
  function istAbgelehnt(b) { return !!(b.obj || b).abgelehnt; }'''

FN_NEU = '''  /* Abgelehnt heisst: aus allen Arbeitsansichten raus, aber nicht geloescht.
     Das Feld bleibt am Beitrag, und „Zurueckholen" macht es rueckgaengig. */
  function istAbgelehnt(b) { return !!(b.obj || b).abgelehnt; }

  /* 🚨 Ist der Beitrag durch? Bis 24.09.2026 wurde das nirgends gefragt —
     ein geposteter Beitrag stand weiter als offener Platz in der Woche.
     „selber-posten" zaehlt dazu: bei einem B-Roll postet Patricia selbst,
     das Cockpit erfaehrt es nie, und wartend stehenbleiben waere falscher
     als abgehakt. */
  var DRAUSSEN = ["geplant", "gepostet-von-hand", "selber-posten"];
  function istDraussen(b) {
    var o = (b.obj || b), bl = o.blotato || {};
    return DRAUSSEN.indexOf(bl.status) >= 0;
  }
  function draussenGrund(b) {
    var bl = ((b.obj || b).blotato) || {};
    return bl.status === "geplant" ? "bei Blotato eingeplant"
      : bl.status === "gepostet-von-hand" ? "von dir gepostet"
      : bl.status === "selber-posten" ? "B-Roll — postest du selbst"
      : "";
  }'''

# ---------------------------------------------- 2 · Wochenplatz kennzeichnen

SLOT_ALT = '''    var box = document.createElement("div");
    box.className = "wslot" + (drauf ? "" : " leer");'''
SLOT_NEU = '''    var box = document.createElement("div");
    box.className = "wslot" + (drauf ? "" : " leer") +
      (drauf && istDraussen(drauf) ? " durch" : "");'''

# ------------------------------------------------------ 3 · Zaehler bereinigen

# „Kann raus" darf nichts zaehlen, was schon draussen ist.
FERTIG_ALT = '''  function fertigAnzahl() {
    return offeneBeitraege().filter(function (b) {
      return b.art !== "storys" && istFertig(b) && !zeitpunktVorbei(b);
    }).length;
  }'''
FERTIG_NEU = '''  function fertigAnzahl() {
    return offeneBeitraege().filter(function (b) {
      return b.art !== "storys" && !istDraussen(b) &&
             istFertig(b) && !zeitpunktVorbei(b);
    }).length;
  }'''

# „Du bist dran" / „Ich bin dran": was draussen ist, fehlt nicht mehr.
FEHLT_ALT = '''  function wasFehlt(b) {
    var o = b.obj, raus = [];'''
FEHLT_NEU = '''  function wasFehlt(b) {
    var o = b.obj, raus = [];
    // Was draussen ist, kann nichts mehr fehlen — sonst steht ein geposteter
    // Beitrag bis in alle Ewigkeit unter „du bist dran".
    if (istDraussen(b)) return raus;'''

# ------------------------------------------------------------------ 4 · CSS

CSS_ALT = "  .jetzt .zeile.klick:hover span { color: var(--ink); }"
CSS_NEU = '''  .jetzt .zeile.klick:hover span { color: var(--ink); }
  /* Abgehakt statt ausgeblendet - ein verschwundener Beitrag laesst den
     Platz leer aussehen, und dann baut man denselben Tag nochmal. */
  .wslot.durch { opacity: 0.62; }
  .wslot.durch .wkarte { border-style: dashed; }
  .wslot.durch::after {
    content: "\\2713 ist raus";
    display: block; margin-top: 8px; font-size: 11px;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--good);
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
    if "istDraussen" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, FN_ALT, FN_NEU, "istAbgelehnt")
    s = setze(s, SLOT_ALT, SLOT_NEU, "Wochenplatz")
    s = setze(s, FERTIG_ALT, FERTIG_NEU, "fertigAnzahl")
    s = setze(s, FEHLT_ALT, FEHLT_NEU, "wasFehlt")
    s = setze(s, CSS_ALT, CSS_NEU, "CSS")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  «Ist raus» eingebaut · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
