"""
Zwei Kleinigkeiten, die nach Schritt 4 und 5 noethig wurden.

1) **Vorlagen anklickbar.** Der Katalog fuehrt jetzt auch Vorlagen, die in
   Google Drive liegen (Mama-CEO Bonus-Vorlagen, Produktwelt-Prompts). Ohne
   Link ist so ein Eintrag nur eine Behauptung. Neben dem Namen steht deshalb
   ein „oeffnen"-Pfeil, der die Datei in einem neuen Tab aufmacht. Er stoppt
   das Klick-Ereignis, sonst klappt gleichzeitig der Ketten-Bauer auf.

2) **Suchindex-Grenze hoch.** Die Suche holte `suche` mit `limit(40)`. Mit dem
   Drive-Inventar (`suche/x01`) kommen laufend Dokumente dazu; bei 40 faellt
   irgendwann still etwas hinten runter, ohne dass es jemand merkt. Jetzt 80.

Aufruf:
  python scripts/cockpit/patch-katalog-links.py [--pruefen]
"""
import io
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ERSETZUNGEN = []


def patch(name, alt, neu):
    ERSETZUNGEN.append((name, alt, neu))


patch("Oeffnen-Link am Angebot",
      """               (w.max > w.grund
                 ? ' <span class="katkorb">bis ' +
                   esc(preisText(w.max, a.waehrung)) + '</span>' : "") +
               '</span></div>';""",
      """               (w.max > w.grund
                 ? ' <span class="katkorb">bis ' +
                   esc(preisText(w.max, a.waehrung)) + '</span>' : "") +
               (a.link
                 ? ' <a class="katauf" href="' + esc(a.link) + '" target="_blank" ' +
                   'rel="noopener" title="' + esc(a.quelle || "") + '">öffnen ↗</a>'
                 : "") +
               '</span></div>';""")

patch("Der Link darf die Karte nicht aufklappen",
      """          g.querySelector(".katzeile").onclick = function () {
            offeneKette = (offeneKette === id) ? null : id;
            render();
          };""",
      """          g.querySelector(".katzeile").onclick = function (ev) {
            // Der Öffnen-Pfeil ist ein Link, kein Schalter — sonst klappt
            // beim Anklicken gleichzeitig der Ketten-Bauer auf.
            if (ev.target && ev.target.classList.contains("katauf")) return;
            offeneKette = (offeneKette === id) ? null : id;
            render();
          };""")

patch("Stil fuer den Oeffnen-Link",
      """  .katkorb {""",
      """  .katauf {
    font-size: 11px; color: var(--teal); text-decoration: none;
    white-space: nowrap; margin-left: 4px;
  }
  .katauf:hover { text-decoration: underline; }
  .katkorb {""")

patch("Suchindex-Grenze",
      '    db.collection("suche").limit(40).get().then(function (qs) {',
      '    db.collection("suche").limit(80).get().then(function (qs) {')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:200]))
        if s.count(alt) > 1:
            sys.exit("Anker mehrdeutig (%dx) fuer: %s" % (s.count(alt), name))
        s = s.replace(alt, neu, 1)
        print("  OK  %s" % name)
    print("\nLaenge %d -> %d (%+d)" % (vorher, len(s), len(s) - vorher))
    if nur_pruefen:
        print("PRUEFLAUF — nichts geschrieben.")
        return
    io.open(DATEI, "w", encoding="utf-8").write(s)
    print("Geschrieben: %s" % DATEI)


if __name__ == "__main__":
    main()
