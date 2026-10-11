"""
Zeigt die Arbeitsblaetter bei der Lektion, zu der sie gehoeren.

Im Reiter „Kurs-Inhalte" stand bisher nur, was in welcher Lektion vorkommt.
Jetzt haengt daneben das Arbeitsblatt aus Google Drive — ein Klick, und es ist
offen. Wer gefragt wird „hast du dazu was zum Ausfuellen?", muss nicht mehr im
Drive suchen.

Zwei Stellen:
  * an der Lektion      die zugeordneten Arbeitsblaetter als Knopf
  * am Kurs             die, bei denen die Zuordnung nicht eindeutig war

Der zweite Kasten ist Absicht und keine Schlamperei: bei vierzehn
Arbeitsblaettern der Produktwelt steht die Lektionsnummer nirgends im
Inhaltsverzeichnis. Raten waere schlimmer als sie einmal beim Kurs zu zeigen.

Aufruf:
  python scripts/cockpit/patch-arbeitsblaetter.py [--pruefen]
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


patch("Arbeitsblatt an der Lektion",
      """            return '<div class="klzeile">' +""",
      """            var ab = (l.arbeitsblaetter || []).map(function (a) {
              return '<a class="abknopf" href="' + esc(a.link) + '" ' +
                     'target="_blank" rel="noopener">' + esc(a.name) + ' ↗</a>';
            }).join("");
            return '<div class="klzeile' + (ab ? " mitab" : "") + '">' +""")

patch("Arbeitsblatt unter die Stichwoerter",
      """              (l.ohne_transkript
                ? '<em>kein Transkript — nur Video</em>'
                : (l.stichwoerter || []).slice(0, 8).map(esc).join(" · ")) +
              '</span></div>';""",
      """              (l.ohne_transkript
                ? '<em>kein Transkript — nur Video</em>'
                : (l.stichwoerter || []).slice(0, 8).map(esc).join(" · ")) +
              (ab ? '<span class="abzeile">' + ab + '</span>' : "") +
              '</span></div>';""")

patch("Arbeitsblaetter ohne Lektion beim Kurs",
      """        if (offenerKurs === k.name) {
          var koerper = karte.querySelector(".dkoerper");
          koerper.innerHTML = k.lektionen.map(function (l) {""",
      """        if (offenerKurs === k.name) {
          var koerper = karte.querySelector(".dkoerper");
          // Wo die Lektionsnummer im Inhaltsverzeichnis fehlt, laesst sich das
          // Arbeitsblatt nicht sauber zuordnen. Dann steht es hier — sichtbar
          // an der falschen Ebene ist besser als unsichtbar.
          var lose = k.arbeitsblaetter_ohne_lektion || [];
          var loseHtml = lose.length
            ? '<div class="abkasten"><div class="abkopf">Arbeitsblätter, die ' +
              'sich keiner Lektion eindeutig zuordnen liessen</div>' +
              lose.map(function (a) {
                return '<a class="abknopf" href="' + esc(a.link) + '" ' +
                       'target="_blank" rel="noopener">' + esc(a.name) + ' ↗</a>';
              }).join("") + '</div>'
            : "";
          koerper.innerHTML = loseHtml + k.lektionen.map(function (l) {""")

patch("Stil fuer die Arbeitsblatt-Knoepfe",
      """  .klworte { font-size: 12px; color: var(--ink-soft); line-height: 1.5; }""",
      """  .klworte { font-size: 12px; color: var(--ink-soft); line-height: 1.5; }
  .klzeile.mitab { background: var(--teal-soft); border-radius: 6px; }
  .abzeile { display: block; margin-top: 6px; }
  .abknopf {
    display: inline-block; background: var(--teal); color: #fbf8f1;
    border-radius: 999px; padding: 3px 11px; font-size: 11.5px;
    text-decoration: none; margin: 0 6px 5px 0;
  }
  .abknopf:hover { background: var(--navy); }
  .abkasten {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 10px 12px; margin: 10px 0 4px;
  }
  .abkopf {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft); margin-bottom: 8px;
  }""")


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
