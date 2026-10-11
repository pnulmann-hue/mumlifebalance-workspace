"""Reiter „Erledigt" unter Mama-CEO (08.10.2026).

Patricia: *„ich möchte wenn die aufgabe abgehakt ist, dass sie dann in einen
reiter erledigt kommt"*.

- Neuer Unterreiter **Mama-CEO → Erledigt** (`activeTab = "erledigt"`): alles
  Abgehakte, nach Erledigt-Datum gruppiert (Heute · Gestern · Datum), mit Filter
  Business/Privat/Alle. Haken weg = zurück zu den offenen Aufgaben.
- **Aufgaben** zeigt nur noch Offenes (die Auswahl „Alle" ist raus).
- **Mein Tisch** zeigt keine erledigten mehr, sondern eine Zeile „N erledigt —
  ansehen".

🚨 Abhaken löscht weiterhin nichts — die Aufgabe bleibt mit `erledigt_am` im
Dokument, nur die Ansicht wechselt. Der Monatsbogen braucht das Datum.

Reihenfolge: patch-mein-tisch → patch-bereiche → patch-offene-chats →
patch-auftauen → patch-erledigt.

    python scripts/cockpit/patch-erledigt.py [--datei <pfad>]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
MARKE = "function renderErledigt(main)"

JS_ANKER = "  function renderAufgaben(main) {"
JS = r"""  /* =========================================================
     Reiter „Erledigt" (08.10.2026) — siehe Kopf von patch-erledigt.py.
     ========================================================= */
  var erlFilter = "alle";

  function renderErledigt(main) {
    var alle = ((aufgaben && aufgaben.items) || []).filter(function (a) { return a.erledigt; });
    var zahl = { alle: alle.length, Business: 0, Privat: 0 };
    alle.forEach(function (a) { zahl[tiBereich(a)]++; });
    var liste = alle.filter(function (a) {
      return erlFilter === "alle" || tiBereich(a) === erlFilter;
    }).sort(function (a, b) {
      return (a.erledigt_am || "") > (b.erledigt_am || "") ? -1 : 1;
    });

    var heute = tiIso(new Date());
    var gestern = new Date(); gestern.setDate(gestern.getDate() - 1);
    var gestIso = tiIso(gestern);
    function wann(iso) {
      if (!iso) return "ohne Datum";
      if (iso === heute) return "Heute";
      if (iso === gestIso) return "Gestern";
      return tiTagLang(iso);
    }

    main.innerHTML =
      '<div class="page-head"><div><h1>Erledigt</h1>' +
      '<p>Was du abgehakt hast, nach Tag. Haken wieder weg nehmen schiebt die ' +
      'Aufgabe zurück zu den offenen.</p></div></div>' +
      '<div class="ti-seg">' + [["alle", "Alle"], ["Business", "Business"], ["Privat", "Privat"]]
        .map(function (k) {
          return '<button data-e="' + k[0] + '" aria-pressed="' + (k[0] === erlFilter) + '">' +
            k[1] + '<span class="n">' + zahl[k[0]] + '</span></button>';
        }).join("") + '</div>' +
      '<div class="panel" id="erl-liste"></div>';
    Array.prototype.forEach.call(main.querySelectorAll("[data-e]"), function (b) {
      b.onclick = function () { erlFilter = b.getAttribute("data-e"); render(); };
    });

    var box = main.querySelector("#erl-liste");
    if (!liste.length) {
      box.innerHTML = '<div class="ti-leer">Hier ist noch nichts. Hak auf dem Tisch oder unter ' +
        'Aufgaben etwas ab, dann landet es hier.</div>';
      return;
    }
    var letzte = null;
    liste.forEach(function (a) {
      var tag = a.erledigt_am || "";
      if (tag !== letzte) {
        letzte = tag;
        var g = document.createElement("div");
        g.className = "ti-gruppe";
        g.innerHTML = "<span>" + esc(wann(tag)) + "</span>";
        box.appendChild(g);
      }
      var z = document.createElement("div");
      z.className = "ti-af fertig";
      var cb = document.createElement("input");
      cb.type = "checkbox"; cb.checked = true; cb.title = "zurück zu den offenen";
      cb.onchange = function () {
        a.erledigt = false; a.erledigt_am = ""; a.erledigt_grund = "";
        tiAfSpeichern();
        toast("Zurück bei den offenen Aufgaben.");
        render();
      };
      var r = document.createElement("div");
      var meta = '<span class="ti-mini">' + esc(tiBereich(a)) + '</span>';
      if (a.fuerClaude) meta += '<span class="ti-mini hoch">für Claude</span>';
      else if (a.quelle === "PIA") meta += '<span class="ti-mini">von PIA</span>';
      if (a.erledigt_grund === "hinfaellig") meta += '<span class="ti-mini">hinfällig</span>';
      r.innerHTML = '<div class="txt">' + esc(a.aufgabe || "(ohne Text)") + '</div>' +
        '<div class="meta">' + meta + '</div>';
      z.appendChild(cb); z.appendChild(r);
      box.appendChild(z);
    });
  }

"""

ERSETZUNGEN = [
    # Unterreiter
    ('tabs: ["aufgaben", "launches", "monatsbogen", "wochenbogen", "ziele", "zahlen", "rangtracker", "team"] },',
     'tabs: ["aufgaben", "erledigt", "launches", "monatsbogen", "wochenbogen", "ziele", "zahlen", "rangtracker", "team"] },'),
    ('  var UNTERNAME = { pia: "PIA & Team", ',
     '  var UNTERNAME = { erledigt: "Erledigt", pia: "PIA & Team", '),
    ('    else if (activeTab === "pia") renderPiaSeite(main);\n',
     '    else if (activeTab === "pia") renderPiaSeite(main);\n'
     '    else if (activeTab === "erledigt") renderErledigt(main);\n'),
    # Tisch: keine erledigten mehr in der Liste, nur der Hinweis
    ('    gruppe("Zuletzt erledigt", fertig, false);\n'
     '    if (!offen.length && !fertig.length) box.innerHTML = \'<div class="ti-leer">Nichts offen.</div>\';\n',
     '    if (!offen.length) box.innerHTML = \'<div class="ti-leer">Nichts offen.</div>\';\n'
     '    var nErl = hier.filter(function (a) { return a.erledigt; }).length;\n'
     '    if (nErl) {\n'
     '      var zuErl = document.createElement("button");\n'
     '      zuErl.className = "ti-btn"; zuErl.style.marginTop = "10px";\n'
     '      zuErl.textContent = nErl + " erledigt — ansehen";\n'
     '      zuErl.onclick = function () { activeTab = "erledigt"; erlFilter = tiAfBereich; render(); };\n'
     '      box.appendChild(zuErl);\n'
     '    }\n'),
    # Aufgaben-Reiter: nur Offenes
    ("        '<option value=\"alle\">Alle</option>' +\n", ""),
    ('      tile("Erledigt", fertig.length, "bleiben stehen") +\n',
     '      tile("Erledigt", fertig.length, "stehen im Reiter Erledigt") +\n'),
    ('    var zeigen = afFilter === "alle" ? alle\n      : (afFilter === "faellig" ? faellig : offen);\n',
     '    var zeigen = afFilter === "faellig" ? faellig : offen;\n'),
]


def patchen(t: str) -> str:
    if MARKE in t:
        print("Schon gepatcht — nichts zu tun.")
        return t
    assert "function tief(x)" in t, "Erst die anderen Patches laufen lassen (bis patch-auftauen)."

    def eins(alt, neu):
        nonlocal t
        assert t.count(alt) == 1, "Anker fehlt oder ist mehrdeutig: " + alt[:70]
        t = t.replace(alt, neu)
    eins(JS_ANKER, JS + JS_ANKER)
    for alt, neu in ERSETZUNGEN:
        eins(alt, neu)
    return t


def main():
    spec = importlib.util.spec_from_file_location(
        "tisch", Path(__file__).with_name("patch-mein-tisch.py"))
    tisch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tisch)

    ap = argparse.ArgumentParser()
    ap.add_argument("--datei", default=str(ROOT / "outputs/cockpit/mlb-cockpit.html"))
    args = ap.parse_args()
    pfad = Path(args.datei)
    roh = pfad.read_bytes().decode("utf-8")
    crlf = "\r\n" in roh
    t = roh.replace("\r\n", "\n")
    neu = patchen(t)
    if neu == t:
        return
    tisch.node_check(neu)
    pfad.write_bytes((neu.replace("\n", "\r\n") if crlf else neu).encode("utf-8"))
    print("Erledigt-Reiter eingebaut:", pfad)


if __name__ == "__main__":
    main()
