"""Storys und Reels erscheinen erst, wenn «Bauen» dran ist.

Patricia am 24.09.2026: *„storys und reels will ich unter bauen haben"*.

Sie standen schon eingerückt (`sub: true`), aber **immer** — auch beim Planen,
beim Freigeben und beim Auswerten. Eingerückt heisst nur *sieht dazugehörig
aus*; dazugehören heisst, dass sie mit ihrem Elternpunkt kommen und gehen.

**Die Regel:** ein Unterpunkt wird nur gezeigt, wenn sein Elternpunkt der
aktive Reiter ist — oder er selbst. Sonst hätte man keinen Weg zurück: wer auf
„Reels" steht und die Unterpunkte verschwinden sieht, sobald er dort ist, kann
nicht mehr wechseln.

🚨 **Der Elternpunkt ist der letzte Nicht-Unterpunkt davor**, nicht ein neues
Feld. Ein `parent`-Eintrag in `TABS` wäre sauberer und würde beim nächsten
Einfügen vergessen — die Reihenfolge in der Liste ist die Zugehörigkeit, und
die sieht man beim Lesen.

    python scripts/cockpit/patch-nav-unterpunkte.py [--pruefen] [--datei <pfad>]
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

ALT = '''      if (auf) k.items.forEach(function (t) { nav.appendChild(knopf(t)); });'''

NEU = '''      /* 🚨 Ein Unterpunkt kommt und geht mit seinem Elternpunkt — dem letzten
         Nicht-Unterpunkt davor. Sonst stehen Storys und Reels auch dann da,
         wenn man gerade plant oder auswertet. Siehe Kopf von
         patch-nav-unterpunkte.py. */
      if (auf) {
        var elter = null;
        k.items.forEach(function (t) {
          if (!t.sub) { elter = t.id; nav.appendChild(knopf(t)); return; }
          // Ohne diese zweite Bedingung verschwindet die Leiste unter den
          // Fuessen, sobald man den Unterpunkt selbst anklickt.
          if (activeTab === elter || activeTab === t.id ||
              geschwisterAktiv(k.items, elter))
            nav.appendChild(knopf(t));
        });
      }'''

ANKER_HELFER = '''  function renderNav() {'''
NEU_HELFER = '''  /* Steht der aktive Reiter unter demselben Elternpunkt? Dann bleiben alle
     Geschwister sichtbar, damit man zwischen ihnen wechseln kann. */
  function geschwisterAktiv(items, elter) {
    var e = null, treffer = false;
    items.forEach(function (t) {
      if (!t.sub) { e = t.id; return; }
      if (t.id === activeTab && e === elter) treffer = true;
    });
    return treffer;
  }

  function renderNav() {'''


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
    if "geschwisterAktiv" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER_HELFER, NEU_HELFER, "Helfer")
    s = setze(s, ALT, NEU, "Unterpunkte")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Unterpunkte hängen an ihrem Elternpunkt · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
