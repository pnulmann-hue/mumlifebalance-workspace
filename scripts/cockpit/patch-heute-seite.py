"""Ersetzt die Startseite — von toten Zählern auf das, was heute ansteht.

🚨 **Die alte Übersicht rechnete mit Leichen.** Sie zählte `state.posts`
(5 Einträge) und `state.ideen` (6) — Überbleibsel aus der allerersten Fassung —
und zeigte ein «40/35/25-Verhältnis», das es nicht mehr gibt, dazu eine
«Archetypen-Abdeckung» ohne Daten. Patricia: *„vieles macht jetzt nicht soo viel
sinn. z.B. die übersicht."* Genau deshalb.

**Die neue Seite beantwortet drei Fragen, und nur die:**

| | |
|---|---|
| Was kann heute raus? | fertige Beiträge mit Zeitpunkt in der Zukunft |
| Wer ist dran — du oder ich? | aus `wasFehlt()`, derselben Quelle wie die Wochenkarte |
| Wo stehe ich? | Umsatz zum Jahresziel, überfällige Aufgaben |

🚨 **Dieselbe Quelle wie die Wochen-Vorschau, keine zweite Rechnung.** Wer die
Zahl «du bist dran» hier anders ausrechnet als dort, hat irgendwann zwei
verschiedene Wahrheiten auf zwei Seiten. Deshalb `alleBeitraege()` und
`wasFehlt()` — dieselben Funktionen.

🚨 **Keine Zahl ohne Grundlage.** Fehlt ein Dokument (Aufgaben, Steuer,
Jahresplan), steht dort ein Strich und nicht eine Null. Eine Null heisst
«nichts offen», ein Strich heisst «weiss ich nicht».

    python scripts/cockpit/patch-heute-seite.py [--pruefen] [--datei <pfad>]
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

NEU = r'''  function renderUebersicht(main) {
    var heute = todayISO();
    var jetzt = new Date();

    /* Dieselbe Quelle wie die Wochen-Vorschau - siehe Kopf des Patch-Skripts. */
    var offen = (typeof offeneBeitraege === "function" ? offeneBeitraege() : alleBeitraege())
      .filter(function (b) { return b.art !== "storys"; });

    var meins = [], deins = [];
    offen.forEach(function (b) {
      (wasFehlt(b) || []).forEach(function (f) {
        var e = { b: b, was: f.was, dazu: f.dazu, datum: (blo(b.obj) || {}).datum || "" };
        (f.wer === "du" ? deins : meins).push(e);
      });
    });
    function nachDatum(a, c) { return (a.datum || "9999") < (c.datum || "9999") ? -1 : 1; }
    deins.sort(nachDatum); meins.sort(nachDatum);

    var raus = offen.filter(function (b) {
      return istFertig(b) && !zeitpunktVorbei(b);
    }).sort(function (a, c) {
      return ((blo(a.obj) || {}).datum || "9999") < ((blo(c.obj) || {}).datum || "9999") ? -1 : 1;
    });

    /* Fehlt ein Dokument, steht ein Strich - nicht eine Null. */
    var afOffen = aufgaben && aufgaben.items
      ? aufgaben.items.filter(function (a) { return !a.erledigt; }) : null;
    var afFaellig = afOffen
      ? afOffen.filter(function (a) { return a.datum && a.datum < heute; }) : null;

    var jahr = String(jetzt.getFullYear());
    var st = steuer && steuer.jahre
      ? steuer.jahre.filter(function (x) { return x.jahr === jahr; })[0] : null;
    var ziel = 40000;
    var pct = st ? Math.round(st.einnahmen / ziel * 100) : null;
    var tagImJahr = Math.floor((jetzt - new Date(jetzt.getFullYear(), 0, 0)) / 86400000);
    var jahrPct = Math.round(tagImJahr / 365 * 100);

    var stunde = jetzt.getHours();
    var gruss = stunde < 11 ? "Guten Morgen" : (stunde < 18 ? "Hallo" : "Guten Abend");
    var datum = jetzt.toLocaleDateString("de-CH",
      { weekday: "long", day: "numeric", month: "long" });

    var lage = raus.length
      ? raus.length + (raus.length === 1 ? " Beitrag wartet" : " Beiträge warten") + " auf deine Freigabe."
      : (deins.length ? "Nichts zum Freigeben — aber " + deins.length + " Sachen warten auf dich."
                      : "Nichts offen. Guter Moment für etwas Neues.");

    main.innerHTML =
      '<div class="hero">' +
        '<div class="hero-bild"></div><div class="hero-schleier"></div>' +
        '<div class="hero-text">' +
          '<p class="hero-gruss">' + esc(gruss) + '</p>' +
          '<h1>' + esc(datum) + '</h1>' +
          '<p class="hero-sub">' + esc(lage) + '</p>' +
        '</div>' +
      '</div>' +
      '<div class="tiles">' +
        tile("Kann raus", raus.length, raus.length ? "fertig, Zeitpunkt offen" : "nichts freigabebereit") +
        tile("Du bist dran", deins.length, deins.length ? "drehen, hochladen, entscheiden" : "nichts von dir offen") +
        tile("Ich bin dran", meins.length, meins.length ? "baue ich" : "nichts von mir offen") +
        tile("Überfällige Aufgaben", afFaellig ? afFaellig.length : "—",
             afOffen ? afOffen.length + " offen gesamt" : "keine Aufgaben geladen") +
        tile("Umsatz " + jahr, st ? "CHF " + Math.round(st.einnahmen).toLocaleString("de-CH") : "—",
             pct === null ? "keine Zahlen geladen"
               : pct + " % vom Ziel · Jahr zu " + jahrPct + " % vorbei") +
      '</div>' +
      '<div class="jetzt">' +
        '<div class="karte"><h3>Du bist dran</h3><div id="ov-du"></div></div>' +
        '<div class="karte"><h3>Kann raus</h3><div id="ov-raus"></div></div>' +
        '<div class="karte"><h3>Als Nächstes</h3><div id="ov-next"></div></div>' +
      '</div>';

    function fuelle(id, zeilen, leertext) {
      var el = main.querySelector(id);
      if (!zeilen.length) { el.innerHTML = '<div class="leer">' + esc(leertext) + '</div>'; return; }
      el.innerHTML = zeilen.slice(0, 6).map(function (z) {
        return '<div class="zeile"><span class="wann">' + esc(z.wann) + '</span>' +
               '<span>' + esc(z.text) + '</span></div>';
      }).join("") + (zeilen.length > 6
        ? '<div class="leer" style="margin-top:8px">und ' + (zeilen.length - 6) + ' weitere</div>' : "");
    }

    fuelle("#ov-du", deins.map(function (e) {
      return { wann: fmtDate(e.datum), text: (e.b.titel || e.b.format) + " — " + e.was };
    }), "Nichts, das auf dich wartet.");

    fuelle("#ov-raus", raus.map(function (b) {
      return { wann: fmtDate((blo(b.obj) || {}).datum), text: b.titel || b.format };
    }), "Nichts freigabebereit.");

    var next = [];
    if (jahresplan && jahresplan.eintraege) {
      next = jahresplan.eintraege.filter(function (e) {
        return e.start && e.start >= heute && e.bereich !== "Ferien";
      }).sort(function (a, c) { return a.start < c.start ? -1 : 1; })
        .map(function (e) { return { wann: fmtDate(e.start), text: e.name }; });
    }
    fuelle("#ov-next", next, jahresplan ? "Nichts mehr geplant dieses Jahr."
                                        : "Jahresplan nicht geladen.");
  }'''


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
    if 'id="ov-du"' in s:
        print("  Schon ersetzt — nichts zu tun.")
        return

    zeilen = s.split("\n")
    try:
        a = next(i for i, z in enumerate(zeilen) if "function renderUebersicht" in z)
    except StopIteration:
        sys.exit("🚨 renderUebersicht nicht gefunden.")
    b = next(i for i in range(a, len(zeilen))
             if zeilen[i] == "  }" or (zeilen[i].startswith("  }") and not zeilen[i].startswith("  })")))
    alt = "\n".join(zeilen[a:b + 1])
    print("  Alte Funktion: %d Zeilen, %d Zeichen" % (b - a + 1, len(alt)))

    s = s.replace(alt, NEU, 1)

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Startseite ersetzt · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
