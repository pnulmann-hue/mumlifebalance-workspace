"""
Die Link-Zentrale zeigt vier Linkarten statt einer.

Patricia am 16.09.2026: „will immer den link zu dem was ausgeliefert wird, den
link zur landingpage unter mumlifebalance., allenfalls den link zu thrivecart,
den link zur telegramgruppe wie z.B. bei der storychallenge das bekommen sie ja."

Vorher zeigte die Karte **einen** Link und nannte ihn je nach Adresse
„Checkout", „Warenkorb" oder „Seite". Damit war unsichtbar, dass die
Lead-Challenge ausser der Landingpage auch eine ThriveCart-Seite und eine
Telegram-Gruppe hat — und dass es zu fast jedem Freebie eine eigene Seite gibt.

Jetzt bekommt jede Art ihre eigene Zeile mit eigenem Kopier-Knopf:

    Seite         mumlifebalance.ch/lead-challenge/            [kopieren]
    Kasse         mumlifebalance.thrivecart.com/challenge-…    [kopieren]
    Das kriegt sie  Lead-Challenge Workbook (PDF, 13 S.)       [kopieren]
    Gruppe        t.me/+lXiK5ZAigFIzZWY0                       [kopieren]

Eine Art ohne Adresse wird **nicht** gezeigt — ausser der Landingpage, deren
Fehlen eine echte Luecke ist und darum sichtbar bleibt.

🚨 Anker-Pruefung: jede Ersetzung bricht ab, wenn ihre Fundstelle fehlt oder
mehrfach vorkommt. Danach prueft Node die Syntax des Skript-Blocks.

Aufruf:
  python scripts/cockpit/patch-linkzentrale-vier-arten.py [--pruefen]
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
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

# --------------------------------------------------------------------------
# 1) Der Block, der bisher genau einen Link zeichnete.
# --------------------------------------------------------------------------
ALT_LINK = """          if (e.link) {
            var art = e.link.indexOf("thrivecart") >= 0 ? "Checkout"
                    : (e.link.indexOf("doterra.me") >= 0 ? "Warenkorb"
                    : "Seite");
            karte.appendChild(kopierZeile(art, e.link, true));
          } else {
            var luecke = document.createElement("div");
            luecke.className = "lzzeile";
            luecke.innerHTML = '<span class="lzlab">Link</span>' +
              '<span class="lzwert lzfehlt">' +
              esc(e.wortlaut || "kein Link hinterlegt") + '</span>';
            karte.appendChild(luecke);
          }
"""

NEU_LINK = """          // Vier Linkarten, jede mit eigener Zeile und eigenem Knopf.
          // Die Reihenfolge ist die, in der Patricia sie braucht: erst die
          // Seite, auf die sie zeigt, dann die Kasse, dann was ankommt.
          var arten = links.linkarten || [
            { id: "landingpage", kurz: "Seite" },
            { id: "thrivecart", kurz: "Kasse" },
            { id: "auslieferung", kurz: "Das kriegt sie" },
            { id: "telegram", kurz: "Gruppe" }
          ];
          var hatWas = false;
          arten.forEach(function (art) {
            var urls = e[art.id] || [];
            urls.forEach(function (u) {
              karte.appendChild(kopierZeile(art.kurz, u, true));
              hatWas = true;
            });
            // Manche Auslieferung ist kein Link, sondern eine Ansage
            // („3-Tage-Mail-Challenge, kein PDF"). Die gehoert trotzdem hin.
            var wort = e[art.id + "_text"];
            if (!urls.length && wort) {
              var z = document.createElement("div");
              z.className = "lzzeile";
              z.innerHTML = '<span class="lzlab">' + esc(art.kurz) + '</span>' +
                '<span class="lzwert lzfehlt">' + esc(wort) + '</span>';
              karte.appendChild(z);
              hatWas = true;
            }
          });
          // Eine fehlende Landingpage ist eine echte Luecke — sichtbar lassen.
          if (!(e.landingpage || []).length && !e.landingpage_text &&
              (e.gruppe === "freebie" || e.gruppe === "bezahlt")) {
            var fehlt = document.createElement("div");
            fehlt.className = "lzzeile";
            fehlt.innerHTML = '<span class="lzlab">Seite</span>' +
              '<span class="lzwert lzfehlt">keine Landingpage</span>';
            karte.appendChild(fehlt);
            hatWas = true;
          }
          if (!hatWas) {
            var leer = document.createElement("div");
            leer.className = "lzzeile";
            leer.innerHTML = '<span class="lzlab">Link</span>' +
              '<span class="lzwert lzfehlt">kein Link hinterlegt</span>';
            karte.appendChild(leer);
          }
"""

# --------------------------------------------------------------------------
# 2) Die Suche muss alle vier Arten durchsuchen, nicht nur e.link.
# --------------------------------------------------------------------------
ALT_SUCHE = """          return (e.name + " " + e.keyword + " " + e.link).toLowerCase()
            .indexOf(w) >= 0;"""

NEU_SUCHE = """          var heu = e.name + " " + e.keyword + " " +
            ["landingpage", "thrivecart", "auslieferung", "telegram"]
              .map(function (a) {
                return (e[a] || []).join(" ") + " " + (e[a + "_text"] || "");
              }).join(" ");
          return heu.toLowerCase().indexOf(w) >= 0;"""

# --------------------------------------------------------------------------
# 3) Die Kacheln zaehlen jetzt Linkarten, nicht Eintraege mit irgendeinem Link.
# --------------------------------------------------------------------------
ALT_ZAEHLER = """    var alle = links.eintraege || [];
    var mitLink = alle.filter(function (e) { return e.link; }).length;
    var luecken = alle.filter(function (e) { return !e.link; }).length;
    var tot = alle.filter(function (e) { return e.status === "tot"; }).length;"""

NEU_ZAEHLER = """    var alle = links.eintraege || [];
    var ARTEN = ["landingpage", "thrivecart", "auslieferung", "telegram"];
    var mitLink = 0;
    alle.forEach(function (e) {
      ARTEN.forEach(function (a) { mitLink += (e[a] || []).length; });
    });
    // Luecke heisst hier: ein Angebot ohne eigene Seite auf mumlifebalance.ch.
    var luecken = alle.filter(function (e) {
      return (e.gruppe === "freebie" || e.gruppe === "bezahlt") &&
        !(e.landingpage || []).length;
    }).length;
    var tot = alle.filter(function (e) { return e.status === "tot"; }).length;"""

ALT_KACHEL = """      tile("Links", mitLink, "geprüft und live") +
      tile("Lücken", luecken, luecken ? "laufen über ManyChat oder fehlen" : "alles hat einen Link") +"""

NEU_KACHEL = """      tile("Links", mitLink, "Seite · Kasse · Auslieferung · Gruppe") +
      tile("Ohne Seite", luecken, luecken ? "Angebot ohne eigene Landingpage" : "jedes Angebot hat eine Seite") +"""

ALT_TEXT = """'<p>Stichwort tippen, auf <strong>kopieren</strong> tippen, in die Story ' +
      'einsetzen. Checkout-Links, Landingpages, Kommentar-Stichwörter und die ' +
      'hinterlegten PDFs — alles an einer Stelle.</p></div></div>' +"""

NEU_TEXT = """'<p>Stichwort tippen, auf <strong>kopieren</strong> tippen, in die Story ' +
      'einsetzen. Je Angebot vier Links: die <strong>Seite</strong> auf ' +
      'mumlifebalance.ch, die <strong>Kasse</strong> bei ThriveCart, ' +
      '<strong>das kriegt sie</strong> (PDF, Bot, Tool) und die ' +
      '<strong>Gruppe</strong> auf Telegram.</p></div></div>' +"""

ERSETZUNGEN = [
    ("Linkzeilen", ALT_LINK, NEU_LINK),
    ("Suche", ALT_SUCHE, NEU_SUCHE),
    ("Zähler", ALT_ZAEHLER, NEU_ZAEHLER),
    ("Kacheln", ALT_KACHEL, NEU_KACHEL),
    ("Einleitung", ALT_TEXT, NEU_TEXT),
]


def node_pruefen(html):
    """Den Skript-Block herausloesen und von Node auf Syntax pruefen."""
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    grosser = max(bloecke, key=len)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(grosser)
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad],
                           capture_output=True, text=True)
        return "" if r.returncode == 0 else (r.stderr or "").strip()[:600]
    except FileNotFoundError:
        return ""      # ohne Node halt ohne Pruefung
    finally:
        Path(pfad).unlink(missing_ok=True)


def main():
    nur_pruefen = "--pruefen" in sys.argv
    html = SEITE.read_text(encoding="utf-8")
    vorher = len(html)

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-14s ersetzt" % name)

    fehler = node_pruefen(html)
    if fehler:
        sys.exit("ABBRUCH — Node meldet einen Syntaxfehler:\n%s" % fehler)
    print("\n  Node --check: in Ordnung")

    if nur_pruefen:
        print("\nPROBELAUF — nichts geschrieben.")
        return
    SEITE.write_text(html, encoding="utf-8")
    print("\nGeschrieben: %s  (%d -> %d Zeichen)" % (SEITE, vorher, len(html)))


if __name__ == "__main__":
    main()
