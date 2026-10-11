"""
Schritt 2: die Kette anklickbar machen.

Bis jetzt zeigte der Angebots-Katalog nur den **Befund** aus ThriveCart: was dort
tatsaechlich am Checkout haengt. Jetzt kommt die zweite Ebene dazu — Patricias
**Plan**: was sie an welches Angebot haengen WILL, mit dem Preis, den sie dort
nehmen will.

Warum zwei Ebenen und nicht eine:
  Befund  = was ThriveCart heute ausliefert  (kommt vom Abgleich, nur Anzeige)
  Plan    = was sie bauen will               (gehoert ihr, wird nie ueberschrieben)
Genau die Differenz ist die Arbeitsliste. Wer beides in ein Feld schreibt, sieht
nie, was noch fehlt.

Gerechnet wird der **maximale Warenkorb**: Grundpreis + alle Bumps + alle
Upsells. Der Downsell zaehlt nicht mit — er kommt nur, wenn der Upsell abgelehnt
wurde, also nie zusammen mit ihm. Dazu die Zeile, wie viele Verkaeufe dieser
Kette im Monat das Monatsziel decken.

Abgelegt wird der Plan in `daten/ketten`. 🚨 Dieses Dokument darf der taegliche
Abgleich NIE schreiben — dort stehen Patricias eigene Entscheidungen.

Aufruf:
  python scripts/cockpit/patch-kette-klickbar.py [--pruefen]
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
# 1) Speicher
# --------------------------------------------------------------------------
patch("Speicher fuer Patricias Ketten",
      '  var katalog = null;\n  var katalogFilter = "";',
      '  var katalog = null;\n'
      '  var katalogFilter = "";\n'
      '  /* Patricias Plan: was sie an welches Angebot haengen will. Getrennt vom\n'
      '     ThriveCart-Befund, weil Plan und Wirklichkeit auseinanderlaufen\n'
      '     duerfen — genau das soll man sehen. Gehoert ihr, der Abgleich\n'
      '     fasst dieses Dokument nicht an. */\n'
      '  var ketten = {};\n'
      '  var offeneKette = null;\n'
      '  var ROLLEN = [["bumps", "Order Bump"], ["upsells", "Upsell"],\n'
      '                ["downsells", "Downsell"]];')


# --------------------------------------------------------------------------
# 2) Die Rechen- und Speicherhelfer, direkt vor renderKatalog
# --------------------------------------------------------------------------
patch("Helfer fuer die Kette",
      """  function renderKatalog(main) {""",
      """  function kettenSpeichern() {
    clearTimeout(saveTimers.ketten);
    saveTimers.ketten = setTimeout(function () {
      lsSet("ketten", ketten);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/ketten")
        .set({ werte: ketten, updatedAt: new Date().toISOString() })
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function meineKette(id) {
    var k = ketten[id];
    if (!k) { k = ketten[id] = { bumps: [], upsells: [], downsells: [] }; }
    ROLLEN.forEach(function (r) { if (!k[r[0]]) k[r[0]] = []; });
    return k;
  }

  function hatKette(id) {
    var k = ketten[id];
    if (!k) return false;
    return ROLLEN.some(function (r) { return (k[r[0]] || []).length; });
  }

  function angebotNach(id) {
    var alle = (katalog && katalog.angebote) || [];
    for (var i = 0; i < alle.length; i++) {
      if (alle[i].id === id) return alle[i];
    }
    return null;
  }

  /* Was maximal in den Warenkorb kann: Grundpreis plus alle Bumps plus alle
     Upsells. Der Downsell bleibt draussen — er kommt nur nach einem
     abgelehnten Upsell, also nie zusammen mit ihm. */
  function warenkorb(a) {
    var k = meineKette(a.id);
    var grund = a.preis || 0, bump = 0, up = 0;
    k.bumps.forEach(function (x) { bump += Number(x.preis) || 0; });
    k.upsells.forEach(function (x) { up += Number(x.preis) || 0; });
    return { grund: grund, bump: bump, up: up, max: grund + bump + up };
  }

  function warenkorbText(a) {
    var w = warenkorb(a);
    var teile = [preisText(w.grund, a.waehrung)];
    if (w.bump) teile.push("+ " + preisText(w.bump, a.waehrung) + " Bump");
    if (w.up) teile.push("+ " + preisText(w.up, a.waehrung) + " Upsell");
    var ziel = Number(settings.monatsziel) || 0;
    var noetig = (ziel && w.max) ? Math.ceil(ziel / w.max) : 0;
    return '<strong>' + esc(preisText(w.max, a.waehrung)) +
      '</strong> maximal im Warenkorb<span class="note"> \\u00b7 ' +
      esc(teile.join(" ")) + '</span>' +
      (noetig
        ? '<div class="note">Bei vollem Warenkorb decken <strong>' + noetig +
          '</strong> Verkaeufe im Monat dein Ziel von ' +
          esc(preisText(ziel, settings.waehrung)) + '.</div>'
        : "");
  }

  function summeNeu(a) {
    var el = document.getElementById("kw-" + a.id);
    if (el) el.innerHTML = warenkorbText(a);
  }

  /* Den ThriveCart-Befund als Startpunkt in den Plan kopieren, damit die
     vierzehn bestehenden Ketten nicht von Hand nachgetippt werden muessen. */
  function ausThriveCart(a) {
    var alle = (katalog && katalog.angebote) || [];
    function finde(name) {
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
    }
    var k = { bumps: [], upsells: [], downsells: [] };
    ROLLEN.forEach(function (r) {
      (((a.kette || {})[r[0]]) || []).forEach(function (x) {
        var id = finde(x.name);
        var ziel = id ? angebotNach(id) : null;
        k[r[0]].push({ id: id, name: ziel ? ziel.name : (x.name || ""),
                       preis: (x.preis === null || x.preis === undefined)
                         ? null : Number(x.preis) });
      });
    });
    return k;
  }

  function kettenZeile(a, rolle, eintrag, i, alle) {
    var zeile = document.createElement("div");
    zeile.className = "katedit-zeile";

    var sel = document.createElement("select");
    var leer = document.createElement("option");
    leer.value = ""; leer.textContent = "\\u2014 Angebot w\\u00e4hlen \\u2014";
    sel.appendChild(leer);
    alle.forEach(function (x) {
      if (x.id === a.id) return;          // sich selbst anhaengen geht nicht
      var o = document.createElement("option");
      o.value = x.id;
      o.textContent = x.name +
        (x.preis ? "  (" + preisText(x.preis, x.waehrung) + ")" : "");
      if (eintrag.id === x.id) o.selected = true;
      sel.appendChild(o);
    });
    if (!eintrag.id && eintrag.name) {
      // Kam aus ThriveCart, hat aber keine Entsprechung im Katalog.
      var fremd = document.createElement("option");
      fremd.value = "";
      fremd.textContent = eintrag.name + "  (nicht im Katalog)";
      fremd.selected = true;
      sel.appendChild(fremd);
    }
    sel.onchange = function () {
      var ziel = angebotNach(sel.value);
      eintrag.id = sel.value;
      eintrag.name = ziel ? ziel.name : "";
      if (ziel && (eintrag.preis === null || eintrag.preis === undefined ||
                   eintrag.preis === "")) {
        eintrag.preis = ziel.preis;
      }
      kettenSpeichern();
      render();
    };
    zeile.appendChild(sel);

    var preis = document.createElement("input");
    preis.type = "number"; preis.min = "0"; preis.step = "1";
    preis.placeholder = "Preis hier";
    preis.title = "Der Preis an dieser Stelle \\u2014 er darf vom Einzelpreis abweichen";
    preis.value = (eintrag.preis === null || eintrag.preis === undefined)
      ? "" : eintrag.preis;
    preis.oninput = function () {
      eintrag.preis = preis.value === "" ? null : Number(preis.value);
      kettenSpeichern();
      summeNeu(a);
    };
    zeile.appendChild(preis);

    var weg = document.createElement("button");
    weg.className = "del";
    weg.textContent = "\\u00d7";
    weg.title = "aus der Kette nehmen";
    weg.onclick = function () {
      meineKette(a.id)[rolle].splice(i, 1);
      kettenSpeichern();
      render();
    };
    zeile.appendChild(weg);
    return zeile;
  }

  function katalogEditor(a) {
    var box = document.createElement("div");
    box.className = "katedit";
    var k = meineKette(a.id);
    var alle = ((katalog && katalog.angebote) || []).slice()
      .sort(function (x, y) { return (x.name || "") < (y.name || "") ? -1 : 1; });

    ROLLEN.forEach(function (r) {
      var block = document.createElement("div");
      block.className = "katedit-block";
      var lab = document.createElement("div");
      lab.className = "katedit-lab";
      lab.textContent = r[1];
      block.appendChild(lab);
      k[r[0]].forEach(function (eintrag, i) {
        block.appendChild(kettenZeile(a, r[0], eintrag, i, alle));
      });
      var plus = document.createElement("button");
      plus.className = "btn ghost katplus";
      plus.textContent = "+ " + r[1];
      plus.onclick = function () {
        meineKette(a.id)[r[0]].push({ id: "", name: "", preis: null });
        kettenSpeichern();
        render();
      };
      block.appendChild(plus);
      box.appendChild(block);
    });

    var summe = document.createElement("div");
    summe.className = "katsumme";
    summe.id = "kw-" + a.id;
    summe.innerHTML = warenkorbText(a);
    box.appendChild(summe);

    // Befund gegen Plan. Nur zeigen, wenn ThriveCart ueberhaupt etwas hat.
    var hatBefund = ROLLEN.some(function (r) {
      return (((a.kette || {})[r[0]]) || []).length;
    });
    if (hatBefund) {
      var fuss = document.createElement("div");
      fuss.className = "katbefund";
      fuss.innerHTML = '<span class="note">In ThriveCart h\\u00e4ngt heute: ' +
        esc(ROLLEN.map(function (r) {
          var l = ((a.kette || {})[r[0]]) || [];
          return l.length ? r[1] + " " + l.map(function (x) {
            return x.name + " (" + preisText(x.preis, x.waehrung) + ")";
          }).join(", ") : "";
        }).filter(Boolean).join(" \\u00b7 ")) + '</span>';
      var holen = document.createElement("button");
      holen.className = "btn";
      holen.textContent = hatKette(a.id)
        ? "Stand aus ThriveCart \\u00fcbernehmen (\\u00fcberschreibt)"
        : "Stand aus ThriveCart \\u00fcbernehmen";
      holen.onclick = function () {
        ketten[a.id] = ausThriveCart(a);
        kettenSpeichern();
        render();
        toast("Aus ThriveCart \\u00fcbernommen. Jetzt kannst du es anpassen.");
      };
      fuss.appendChild(holen);
      box.appendChild(fuss);
    }
    return box;
  }

  function renderKatalog(main) {""")


# --------------------------------------------------------------------------
# 3) Die Angebots-Zeilen gruppieren und anklickbar machen
# --------------------------------------------------------------------------
patch("Angebot als anklickbare Gruppe",
      """        drin.forEach(function (a) {
          h += '<div class="katzeile">' +
               '<span class="katpreis">' + esc(preisText(a.preis, a.waehrung)) + '</span>' +
               '<span class="katname">' + esc(a.name) +
               (a.status && a.status !== "live"
                 ? ' <span class="flag bad">' + esc(a.status) + '</span>' : "") +
               '</span></div>';
""",
      """        drin.forEach(function (a) {
          var w = warenkorb(a);
          h += '<div class="katgruppe' + (offeneKette === a.id ? " auf" : "") +
               '" data-ang="' + esc(a.id) + '">' +
               '<div class="katzeile">' +
               '<span class="katpreis">' + esc(preisText(a.preis, a.waehrung)) + '</span>' +
               '<span class="katname">' + esc(a.name) +
               (a.status && a.status !== "live"
                 ? ' <span class="flag bad">' + esc(a.status) + '</span>' : "") +
               (w.max > w.grund
                 ? ' <span class="katkorb">bis ' +
                   esc(preisText(w.max, a.waehrung)) + '</span>' : "") +
               '</span></div>';
""")

patch("Gruppe schliessen und Klick verdrahten",
      """          (a.haengt_an || []).forEach(function (x) {
            h += '<div class="katkette rueck"><span class="katrolle">← ' +
                 esc(x.art) + '</span><span>bei ' + esc(x.bei) + '</span>' +
                 '<span class="katpreis klein">' + esc(preisText(x.preis, "CHF")) +
                 '</span></div>';
          });
        });

        block.innerHTML = h;
        raus.appendChild(block);""",
      """          (a.haengt_an || []).forEach(function (x) {
            h += '<div class="katkette rueck"><span class="katrolle">← ' +
                 esc(x.art) + '</span><span>bei ' + esc(x.bei) + '</span>' +
                 '<span class="katpreis klein">' + esc(preisText(x.preis, "CHF")) +
                 '</span></div>';
          });
          h += '</div>';
        });

        block.innerHTML = h;
        // Ein Klick auf die Zeile klappt den Ketten-Bauer auf.
        block.querySelectorAll(".katgruppe").forEach(function (g) {
          var id = g.getAttribute("data-ang");
          var a = angebotNach(id);
          if (!a) return;
          g.querySelector(".katzeile").onclick = function () {
            offeneKette = (offeneKette === id) ? null : id;
            render();
          };
          if (offeneKette === id) g.appendChild(katalogEditor(a));
        });
        raus.appendChild(block);""")


# --------------------------------------------------------------------------
# 4) Eine Kachel, die den groessten Warenkorb zeigt
# --------------------------------------------------------------------------
patch("Kachel groesster Warenkorb",
      """      tile("Treppe", preisText(summe, "CHF"), "alle verkauften zusammen") +
      '</div>' +""",
      """      tile("Treppe", preisText(summe, "CHF"), "alle verkauften zusammen") +
      tile("Grösster Warenkorb", preisText(groesster.wert, "CHF"),
           groesster.name || "noch keine Kette gebaut") +
      '</div>' +""")

patch("Groessten Warenkorb ausrechnen",
      """    main.innerHTML =
      '<div class="page-head"><div><h1>Angebots-Katalog</h1>' +
      '<p>Was du hast, was es kostet und was daran hängt — direkt aus ThriveCart. ' +""",
      """    var groesster = { wert: 0, name: "" };
    alle.forEach(function (a) {
      var w = warenkorb(a);
      if (w.max > groesster.wert) { groesster = { wert: w.max, name: a.name }; }
    });

    main.innerHTML =
      '<div class="page-head"><div><h1>Angebots-Katalog</h1>' +
      '<p>Was du hast, was es kostet und was daran hängt — direkt aus ThriveCart. ' +""")

patch("Hinweis auf den Klick",
      """      'Das Pfeilchen ↳ zeigt, was an diesem Checkout angeboten wird, ' +
      '← zeigt, wo dieses Angebot selbst eingesetzt wird.</p></div></div>' +""",
      """      'Das Pfeilchen ↳ zeigt, was an diesem Checkout angeboten wird, ' +
      '← zeigt, wo dieses Angebot selbst eingesetzt wird. ' +
      '<strong>Klick ein Angebot an</strong>, dann baust du dort die Kette: ' +
      'Bump, Upsell und Downsell auswählen, Preis setzen, und du siehst sofort, ' +
      'was maximal in den Warenkorb passt.</p></div></div>' +""")


# --------------------------------------------------------------------------
# 5) Stil
# --------------------------------------------------------------------------
patch("Stil fuer den Ketten-Bauer",
      """  .katrolle { text-align: right; color: var(--teal); white-space: nowrap; }
  .katkette.rueck .katrolle { color: var(--orange); }""",
      """  .katrolle { text-align: right; color: var(--teal); white-space: nowrap; }
  .katkette.rueck .katrolle { color: var(--orange); }
  .katgruppe { border-radius: 8px; }
  .katgruppe .katzeile { cursor: pointer; }
  .katgruppe:hover .katzeile { background: var(--surface-2); }
  .katgruppe.auf {
    background: var(--surface-2); padding: 2px 10px 10px;
    margin: 6px -10px; box-shadow: inset 3px 0 0 var(--teal);
  }
  .katkorb {
    font-size: 11px; letter-spacing: 0.04em; color: var(--teal);
    background: var(--teal-soft); padding: 1px 8px; border-radius: 999px;
    white-space: nowrap;
  }
  .katedit {
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 8px; padding: 12px 14px; margin-top: 10px;
  }
  .katedit-block { margin-bottom: 12px; }
  .katedit-lab {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft); margin-bottom: 5px;
  }
  .katedit-zeile {
    display: grid; grid-template-columns: 1fr 110px 30px; gap: 8px;
    margin-bottom: 6px; align-items: center;
  }
  .katedit-zeile select, .katedit-zeile input {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 7px; padding: 6px 9px; font-size: 13px; width: 100%;
  }
  .katedit-zeile select:focus, .katedit-zeile input:focus {
    border-color: var(--teal); outline: none;
  }
  .katedit-zeile .del {
    border: 0; background: none; color: var(--ink-soft); cursor: pointer;
    padding: 4px 6px; border-radius: 6px; font-size: 15px; line-height: 1;
  }
  .katedit-zeile .del:hover { background: var(--orange-soft); color: var(--crit); }
  .katplus { font-size: 12px; padding: 4px 8px; }
  .katsumme {
    border-top: 1px solid var(--line); padding-top: 10px; margin-top: 4px;
    font-size: 14px;
  }
  .katbefund {
    border-top: 1px solid var(--line); margin-top: 10px; padding-top: 10px;
    display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
  }
  .katbefund .btn { font-size: 12px; padding: 5px 10px; }
  @media (max-width: 700px) {
    .katedit-zeile { grid-template-columns: 1fr 84px 30px; }
  }""")

patch("Rand der ersten Zeile",
      "  .katblock .katzeile:first-of-type { border-top: 0; }",
      "  .katblock .katgruppe:first-child .katzeile { border-top: 0; }")


# --------------------------------------------------------------------------
# 6) Laden
# --------------------------------------------------------------------------
patch("Ketten beim Start laden",
      '  katalog = lsGet("katalog", null);',
      '  katalog = lsGet("katalog", null);\n'
      '  ketten = lsGet("ketten", {}) || {};')

patch("Ketten aus der Datenbank",
      '      db.doc("daten/katalog").onSnapshot(function (snap) {',
      '      db.doc("daten/ketten").onSnapshot(function (snap) {\n'
      '        if (!snap.exists) return;\n'
      '        ketten = (snap.data() || {}).werte || {};\n'
      '        lsSet("ketten", ketten);\n'
      '        if (activeTab === "katalog") render();\n'
      '      }, function () {});\n'
      '      db.doc("daten/katalog").onSnapshot(function (snap) {')


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
