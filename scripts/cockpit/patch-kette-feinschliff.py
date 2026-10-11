"""
Schritt 2, Feinschliff — drei Befunde aus der Sichtpruefung.

1) Die Kachel „Groesster Warenkorb" zeigte 1'350 fuer die 1:1-Begleitung, an der
   gar keine Kette haengt. Ohne Kette ist der Warenkorb nur der Einzelpreis, und
   dann sagt die Kachel bloss, was am teuersten ist. Sie zaehlt jetzt nur noch
   Angebote, an denen wirklich etwas haengt.

2) Der ThriveCart-Upsell heisst „Finde dein Thema als Network-Mama", das Produkt
   heisst „Finde dein Thema als Networking-Mama in 60 Minuten". Weder gleich noch
   Wortanfang — also blieb er beim Uebernehmen als „nicht im Katalog" liegen.
   Der Abgleich laeuft jetzt ueber gemeinsame Woerter; bei mehreren Treffern
   entscheidet der Preis.

3) Die Auswahlliste war eine Wand aus neunundvierzig Zeilen, Altbestand mitten
   drin. Jetzt nach Schubladen gruppiert, „Sonstiges" zuletzt.

Aufruf:
  python scripts/cockpit/patch-kette-feinschliff.py [--pruefen]
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


# --------------------------------------------------------------------------
# 1) Die Kachel zaehlt nur Angebote mit Kette
# --------------------------------------------------------------------------
patch("Groesster Warenkorb nur mit Kette",
      """    var groesster = { wert: 0, name: "" };
    alle.forEach(function (a) {
      var w = warenkorb(a);
      if (w.max > groesster.wert) { groesster = { wert: w.max, name: a.name }; }
    });""",
      """    // Ohne Kette ist der Warenkorb nur der Einzelpreis — das waere bloss
    // die Antwort auf „was ist am teuersten", nicht auf „was traegt am meisten".
    var groesster = { wert: 0, name: "" };
    alle.forEach(function (a) {
      var w = warenkorb(a);
      if (w.max > w.grund && w.max > groesster.wert) {
        groesster = { wert: w.max, name: a.name };
      }
    });""")


# --------------------------------------------------------------------------
# 2) Namen ueber gemeinsame Woerter zusammenfuehren
# --------------------------------------------------------------------------
patch("Namensabgleich ueber Woerter",
      """    function finde(name) {
      var n = String(name || "").toLowerCase().trim();
      if (!n) return "";
      var i;
      for (i = 0; i < alle.length; i++) {
        if ((alle[i].name || "").toLowerCase().trim() === n) return alle[i].id;
      }
      for (i = 0; i < alle.length; i++) {
        var m = (alle[i].name || "").toLowerCase().trim();
        if (m && (m.indexOf(n) === 0 || n.indexOf(m) === 0)) return alle[i].id;
      }
      return "";
    }""",
      """    function finde(name, preis) {
      var n = String(name || "").toLowerCase().trim();
      if (!n) return "";
      var i;
      for (i = 0; i < alle.length; i++) {
        if ((alle[i].name || "").toLowerCase().trim() === n) return alle[i].id;
      }
      for (i = 0; i < alle.length; i++) {
        var m = (alle[i].name || "").toLowerCase().trim();
        if (m && (m.indexOf(n) === 0 || n.indexOf(m) === 0)) return alle[i].id;
      }
      // Dritter Anlauf ueber gemeinsame Woerter: in ThriveCart heisst derselbe
      // Kurs mal „Network-Mama", mal „Networking-Mama in 60 Minuten".
      var gesucht = wortMenge(n);
      if (!gesucht.length) return "";
      var bester = "", bestwert = 0;
      for (i = 0; i < alle.length; i++) {
        var hier = wortMenge(alle[i].name);
        if (!hier.length) continue;
        var gleich = 0;
        gesucht.forEach(function (w) { if (hier.indexOf(w) >= 0) gleich++; });
        var wert = gleich / Math.min(gesucht.length, hier.length);
        // Bei gleichem Wortbild entscheidet der Preis.
        if (preis && alle[i].preis === Number(preis)) wert += 0.05;
        if (wert > bestwert) { bestwert = wert; bester = alle[i].id; }
      }
      return bestwert >= 0.6 ? bester : "";
    }""")

patch("Preis an finde uebergeben",
      "        var id = finde(x.name);",
      "        var id = finde(x.name, x.preis);")

patch("Wortmenge-Helfer",
      """  /* Den ThriveCart-Befund als Startpunkt in den Plan kopieren, damit die
     vierzehn bestehenden Ketten nicht von Hand nachgetippt werden muessen. */""",
      """  /* Ein Name auf seine tragenden Woerter eingedampft. Umlaute sind egal,
     Fuellwoerter fliegen raus — sonst findet „Finde dein Thema als
     Network-Mama" seinen eigenen Kurs nicht wieder. */
  var FUELLWORT = /^(der|die|das|dein|deine|den|dem|fuer|als|und|mit|von|zum|zur|ein|eine|einen|ist|auf|aus|minuten|stunden)$/;

  function wortMenge(s) {
    return String(s || "").toLowerCase()
      .replace(/\\u00e4/g, "ae").replace(/\\u00f6/g, "oe")
      .replace(/\\u00fc/g, "ue").replace(/\\u00df/g, "ss")
      .replace(/[^a-z0-9]+/g, " ").trim().split(" ")
      .filter(function (w) { return w.length > 2 && !FUELLWORT.test(w); });
  }

  /* Den ThriveCart-Befund als Startpunkt in den Plan kopieren, damit die
     vierzehn bestehenden Ketten nicht von Hand nachgetippt werden muessen. */""")


# --------------------------------------------------------------------------
# 3) Auswahlliste nach Schubladen gruppieren
# --------------------------------------------------------------------------
patch("Auswahlliste nach Schubladen",
      r"""    alle.forEach(function (x) {
      if (x.id === a.id) return;          // sich selbst anhaengen geht nicht
      var o = document.createElement("option");
      o.value = x.id;
      o.textContent = x.name +
        (x.preis ? "  (" + preisText(x.preis, x.waehrung) + ")" : "");
      if (eintrag.id === x.id) o.selected = true;
      sel.appendChild(o);
    });""",
      r"""    // Nach Schubladen gruppiert — neunundvierzig Zeilen am Stueck findet
    // niemand. „Sonstiges" steht zuletzt, weil dort der Altbestand liegt.
    (((katalog && katalog.kategorien) || [])).forEach(function (kat) {
      var drin = alle.filter(function (x) {
        return x.kategorie === kat.id && x.id !== a.id;
      });
      if (!drin.length) return;
      var gruppe = document.createElement("optgroup");
      gruppe.label = kat.name;
      drin.forEach(function (x) {
        var o = document.createElement("option");
        o.value = x.id;
        o.textContent = x.name +
          (x.preis ? "  (" + preisText(x.preis, x.waehrung) + ")" : "");
        if (eintrag.id === x.id) o.selected = true;
        gruppe.appendChild(o);
      });
      sel.appendChild(gruppe);
    });""")


# --------------------------------------------------------------------------
# 4) Rechtschreibung
# --------------------------------------------------------------------------
patch("Verkaeufe mit Umlaut",
      "'</strong> Verkaeufe im Monat dein Ziel von ' +",
      "'</strong> Verk\\u00e4ufe im Monat dein Ziel von ' +")


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
