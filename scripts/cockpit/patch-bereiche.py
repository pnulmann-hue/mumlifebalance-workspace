"""Fünf Bereiche oben statt 28 Reiter in der Seitenleiste (08.10.2026).

Patricia am 08.10.2026, mit dem CEO-Table-Screenshot als Vorbild: *„der
screenshot den ich geschickt habe sieht einfach auch viel benutzerfreundlicher
aus — wäre nicht eine aufteilung von instagram, produkte, mama-ceo und ki eine
gute wahl?"* · vorher: *„aufgebaut wie halt meine Mum Business Academy und
darin steckt dann der ganze inhalt plus meine assistenten"*.

| Bereich | Reiter |
|---|---|
| Mein Tisch | Startseite |
| Instagram | Planen · Bauen · Storys · Reels · Freigeben · Ausgewertet · Ideenkasten · Ideen von anderen |
| Produkte | Katalog · Notizen · Links · Funnel · Listen · Kundinnen · Kurs-Inhalte |
| Mama-CEO | Aufgaben · Jahresplan · Monats-/Wochenbogen · Ziele · Zahlen · Rang-Tracker · Team |
| KI | Mein Wissen · Suchen |

Die Seitenleiste wird zur Kopfleiste auf dem Verlauf, jede Ansicht (ausser dem
Tisch) liegt auf einem hellen Blatt. Oben in jedem Bereich stehen die
Helferinnen dieser Säule (`HELFERINNEN` aus patch-mein-tisch.py).

🚨 **Die Reiter-Kennungen bleiben unverändert.** Nur die Navigation ist neu;
`activeTab`, die Render-Funktionen und jeder Sprung (`springeZuBeitrag`,
„Zu Freigeben“) laufen weiter. `renderNav()` leitet auf `renderBereiche()` um,
die alte Fassung bleibt als `renderNavAlt` stehen.

Setzt patch-mein-tisch.py voraus.

    python scripts/cockpit/patch-bereiche.py [--datei <pfad>]
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
MARKE = "---------- Bereiche oben (08.10.2026) ----------"

KOPF_ALT = """  <aside class="side">
    <div class="brandmark">
      <img class="bm-logo" src="assets/logo.svg" alt="Mum Life Balance">
      <div class="bm-sub">Cockpit</div>
    </div>
    <nav id="nav"></nav>
    <div class="side-foot">
      <div id="savestate"><span class="dot"></span>verbinde…</div>
      <div style="margin-top:8px">Alles, was du hier eintippst, bleibt gespeichert und ist beim nächsten Öffnen wieder da.</div>
    </div>
  </aside>
"""
KOPF_NEU = """  <header class="kopfleiste">
    <div class="kl-marke"><span class="kl-name">Mum Life Balance</span><span class="kl-sub">Cockpit</span></div>
    <nav id="nav" class="kl-nav" aria-label="Bereiche"></nav>
    <div class="kl-stand" id="savestate" title="Alles, was du hier eintippst, bleibt gespeichert."><span class="dot"></span>verbinde…</div>
  </header>
"""

CSS_ANKER = "</style>\n\n<div class=\"shell\">"
CSS = r"""
  /* ---------- Bereiche oben (08.10.2026) ----------
     Kopfleiste auf dem Verlauf, Inhalte auf einem hellen Blatt. */
  body {
    background: linear-gradient(140deg, #0c1c30 0%, #173a52 50%, #12828c 100%) fixed;
    background-color: #0c1c30;
  }
  .shell { display: block; min-height: 100vh; }
  .kopfleiste {
    position: sticky; top: 0; z-index: 40;
    display: flex; align-items: center; gap: 18px; flex-wrap: wrap;
    padding: 12px 24px;
    background: rgba(12, 28, 48, 0.6);
    -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(251, 248, 241, 0.12);
  }
  .kl-marke { display: flex; align-items: baseline; gap: 10px; color: #fbf8f1; }
  .kl-name { font-family: var(--display); font-size: 19px; }
  .kl-sub { font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.7; }
  .kl-nav { display: flex; flex-direction: row; gap: 6px; overflow-x: auto; }
  .kl-pill {
    border: 1px solid rgba(251, 248, 241, 0.3); background: rgba(251, 248, 241, 0.08);
    color: #fbf8f1; border-radius: 999px; padding: 7px 16px; font: inherit;
    font-size: 14px; cursor: pointer; white-space: nowrap;
  }
  .kl-pill:hover { background: rgba(251, 248, 241, 0.18); }
  .kl-pill[aria-current="true"] {
    background: #fbf8f1; color: #0c1c30; border-color: #fbf8f1; font-weight: 600;
  }
  .kl-zahl {
    margin-left: 6px; font-size: 11px; background: #dc822e; color: #fff;
    border-radius: 999px; padding: 1px 7px; font-weight: 600;
  }
  .kl-stand { margin-left: auto; color: rgba(251, 248, 241, 0.8); font-size: 12px; }
  main.ti-main { background: none; }
  main.blatt {
    background: var(--ground); border-radius: 22px;
    margin: 18px 20px 28px; padding: 22px 26px 50px;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.25);
  }
  .unterleiste { margin: 0 0 22px; display: flex; flex-direction: column; gap: 12px; }
  .ul-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
  .ul-tab {
    border: 0; background: var(--surface-2); color: var(--ink-soft);
    border-radius: 999px; padding: 6px 14px; font: inherit; font-size: 13px; cursor: pointer;
  }
  .ul-tab:hover { color: var(--ink); }
  .ul-tab[aria-current="true"] { background: var(--ink); color: var(--surface); font-weight: 600; }
  .ul-tab .n { margin-left: 5px; font-size: 11px; color: var(--orange); font-weight: 700; }
  .hilfeleiste { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
  .hl-titel {
    font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--ink-soft); margin-right: 4px;
  }
  .hl-chip {
    display: inline-flex; gap: 6px; align-items: center;
    border: 1px solid var(--line); background: var(--surface); color: var(--ink);
    border-radius: 999px; padding: 3px 11px 3px 3px; font: inherit; font-size: 12.5px; cursor: pointer;
  }
  .hl-chip .ti-ava { flex: 0 0 22px; width: 22px; height: 22px; font-size: 11px; }
  .hl-chip:hover { border-color: var(--teal); }
  .hl-chip[aria-pressed="true"] { border-color: var(--teal); box-shadow: inset 0 0 0 1px var(--teal); }
  .panel, .tile, .tablewrap, .wkarte, .dkarte { border-radius: 14px; }
  .pia-grid { display: grid; gap: 16px; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); align-items: start; }
  @media (max-width: 900px) { .pia-grid { grid-template-columns: 1fr; } }
  main.blatt .ti-karte { box-shadow: 0 4px 18px rgba(12, 28, 48, 0.10); border: 1px solid var(--line); }
  main.blatt .ti-verlauf { max-height: 460px; }
  @media (max-width: 760px) {
    .kopfleiste { padding: 10px 12px; gap: 8px; }
    .kl-stand { display: none; }
    .kl-nav { width: 100%; }
    main.blatt { margin: 10px 8px 20px; padding: 16px 14px 40px; border-radius: 16px; }
    /* Am Handy eine Zeile zum Wischen statt drei Zeilen Pillen. */
    .ul-tabs { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 2px; }
    .ul-tab { white-space: nowrap; }
  }
  /* Breite Tabellen (Projekte, Steuer) wischen statt die Seite zu sprengen. */
  .card { overflow-x: auto; }
"""

JS_ANKER = "  function renderNav() {"
JS = r"""  /* =========================================================
     Bereiche oben (08.10.2026) — siehe Kopf von patch-bereiche.py.
     ========================================================= */
  var BEREICHE = [
    { id: "tisch", label: "Mein Tisch", tabs: ["uebersicht"] },
    { id: "instagram", label: "Instagram", saeule: "Instagram",
      tabs: ["woche", "studio", "storys", "reels", "fertig", "gepostet", "ideenkasten", "ideenextern"] },
    { id: "produkte", label: "Produkte", saeule: "Produkte",
      tabs: ["katalog", "produkte", "links", "funnel", "mailings", "leads", "kurse"] },
    { id: "mamaceo", label: "Mama-CEO", saeule: "Mama-CEO",
      tabs: ["aufgaben", "launches", "monatsbogen", "wochenbogen", "ziele", "zahlen", "rangtracker", "team"] },
    { id: "ki", label: "KI", saeule: "KI", tabs: ["pia", "wissen", "suche"] }
  ];
  /* Kuerzere Namen fuer die Unterleiste — die Bereichs-Pille sagt schon,
     wo man ist. */
  var UNTERNAME = { pia: "PIA & Team", produkte: "Meine Notizen", rangtracker: "doTERRA-Rang", team: "doTERRA-Team",
                    launches: "Jahresplan", mailings: "Listen & Automationen" };
  var bereichLetzter = {};
  try { bereichLetzter = JSON.parse(localStorage.getItem("mlb:bereich-letzter") || "{}") || {}; } catch (e) {}

  function bereichVon(id) {
    for (var i = 0; i < BEREICHE.length; i++) {
      if (BEREICHE[i].tabs.indexOf(id) >= 0) return BEREICHE[i];
    }
    return null;
  }
  function tabName(id) {
    if (UNTERNAME[id]) return UNTERNAME[id];
    var t = TABS.filter(function (x) { return x.id === id; })[0];
    return t ? t.label : id;
  }

  function renderBereiche() {
    var nav = document.getElementById("nav");
    if (!nav) return;
    nav.innerHTML = "";
    var akt = bereichVon(activeTab);
    BEREICHE.forEach(function (b) {
      var k = document.createElement("button");
      k.className = "kl-pill";
      k.setAttribute("aria-current", akt && akt.id === b.id ? "true" : "false");
      // 🚨 Nur EINE Zahl an der Pille: was zum Freigeben bereitliegt. Die
      // Laengen der Listen (38 Reels) sind keine Arbeit und gehoeren nicht hin.
      var n = b.id === "instagram" ? fertigAnzahl() : 0;
      k.innerHTML = esc(b.label) + (n ? '<span class="kl-zahl" title="kann raus">' + n + '</span>' : "");
      k.onclick = function () {
        var ziel = bereichLetzter[b.id];
        activeTab = (ziel && b.tabs.indexOf(ziel) >= 0) ? ziel : b.tabs[0];
        tiHelfer = null;
        render();
        try { window.scrollTo(0, 0); } catch (e) {}
      };
      nav.appendChild(k);
    });
  }

  /* KI → „PIA & Team“: oben mit PIA sprechen, daneben was am Tisch liegt,
     unten alle Helferinnen (Patricia, 08.10.2026). */
  function renderPiaSeite(main) {
    var heute = tiIso(new Date());
    var beitraege = offeneBeitraege();
    main.innerHTML =
      '<div class="page-head"><div><h1>PIA &amp; dein Team</h1>' +
      '<p>Du sprichst nur mit PIA. Sie trägt ein, was ansteht, und gibt Aufträge an Claude weiter — ' +
      'die siehst du rechts und Claude beim nächsten Start in Claude Code.</p></div></div>' +
      '<div class="pia-grid"><div class="ti-karte" id="ps-pia"></div><div class="ti-karte" id="ps-auf"></div></div>' +
      '<div class="ti-karte ti-voll" id="ps-helfer"></div>';
    tiPia(main.querySelector("#ps-pia"), heute, beitraege);
    piaAuftraege(main.querySelector("#ps-auf"));
    tiHelferinnen(main.querySelector("#ps-helfer"));
  }

  /* „Am Tisch – Aufträge“: was PIA an Claude weitergegeben hat. */
  function piaAuftraege(el) {
    var alle = ((aufgaben && aufgaben.items) || []).filter(function (a) { return a.fuerClaude; });
    var offen = alle.filter(function (a) { return !a.erledigt; });
    var fertig = alle.filter(function (a) { return a.erledigt; }).sort(function (a, b) {
      return (a.erledigt_am || "") > (b.erledigt_am || "") ? -1 : 1; }).slice(0, 5);
    el.innerHTML = '<span class="ti-chip o">Am Tisch – Aufträge</span><div id="pa-l"></div>';
    var box = el.querySelector("#pa-l");
    if (!alle.length) {
      box.innerHTML = '<div class="ti-leer">Noch nichts. Sag PIA zum Beispiel: ' +
        '„Claude soll mir ein Karussell zum Stimm-Check bauen.“</div>';
      return;
    }
    function zeile(a, stand, art) {
      var z = document.createElement("div");
      z.className = "ti-zeile";
      z.innerHTML = '<span class="ti-zeit">' + esc(a.datum ? fmtDate(a.datum) : "") + '</span>' +
        '<span class="ti-was">' + esc(a.aufgabe) + '</span>' +
        '<span class="ti-mini' + art + '">' + esc(stand) + '</span>';
      box.appendChild(z);
    }
    offen.forEach(function (a) { zeile(a, "wartet auf Claude", " hoch"); });
    fertig.forEach(function (a) { zeile(a, "fertig", ""); });
  }

  /* Unterreiter plus die Helferinnen der Saeule, oben auf jedes Blatt. */
  function unterleisteEinfuegen(main) {
    main.classList.toggle("blatt", activeTab !== "uebersicht");
    var b = bereichVon(activeTab);
    if (!b || b.id === "tisch") return;
    bereichLetzter[b.id] = activeTab;
    try { localStorage.setItem("mlb:bereich-letzter", JSON.stringify(bereichLetzter)); } catch (e) {}

    var leiste = document.createElement("div");
    leiste.className = "unterleiste";
    var tabs = document.createElement("div");
    tabs.className = "ul-tabs";
    b.tabs.forEach(function (id) {
      var t = document.createElement("button");
      t.className = "ul-tab";
      t.setAttribute("aria-current", id === activeTab ? "true" : "false");
      var n = id === "fertig" ? fertigAnzahl() : 0;
      t.innerHTML = esc(tabName(id)) + (n ? '<span class="n">' + n + '</span>' : "");
      t.onclick = function () { activeTab = id; render(); };
      tabs.appendChild(t);
    });
    leiste.appendChild(tabs);

    // Auf „PIA & Team“ stehen alle Helferinnen ohnehin unten - nicht doppelt.
    var hs = activeTab === "pia" ? [] : HELFERINNEN.filter(function (h) { return h.s === b.saeule; });
    if (hs.length) {
      var hz = document.createElement("div");
      hz.className = "hilfeleiste";
      hz.innerHTML = '<span class="hl-titel">Deine Helferinnen hier</span>';
      hs.forEach(function (h, i) {
        var c = document.createElement("button");
        c.className = "hl-chip";
        c.setAttribute("aria-pressed", tiHelfer === h.id ? "true" : "false");
        c.innerHTML = '<span class="ti-ava' + (h.link ? " n" : (i % 2 ? " o" : "")) + '">' +
          esc(h.name.charAt(0)) + '</span>' + esc(h.name);
        c.onclick = function () { tiHelfer = tiHelfer === h.id ? null : h.id; render(); };
        hz.appendChild(c);
      });
      leiste.appendChild(hz);
      var offen = activeTab === "pia" ? null
        : hs.filter(function (x) { return x.id === tiHelfer; })[0];
      if (offen) {
        var box = document.createElement("div");
        tiHelferDetail(box, offen);
        leiste.appendChild(box);
      }
    }
    main.insertBefore(leiste, main.firstChild);
  }

"""

ERSETZUNGEN = [
    (KOPF_ALT, KOPF_NEU),
    ('    else if (activeTab === "studio") renderStudio(main);\n',
     '    else if (activeTab === "pia") renderPiaSeite(main);\n'
     '    else if (activeTab === "studio") renderStudio(main);\n'),
    ("  function renderNav() {\n",
     "  function renderNav() { return renderBereiche(); }\n"
     "  /* 🗃 Die Seitenleiste bis 08.10.2026 - laeuft nicht mehr. */\n"
     "  function renderNavAlt() {\n"),
    ('    else renderTable(main, activeTab);\n  }\n',
     '    else renderTable(main, activeTab);\n'
     '    unterleisteEinfuegen(main);\n  }\n'),
]


def patchen(t: str) -> str:
    if MARKE in t:
        print("Schon gepatcht — nichts zu tun.")
        return t
    assert "renderTisch" in t, "Erst patch-mein-tisch.py laufen lassen."

    def eins(alt, neu):
        nonlocal t
        assert t.count(alt) == 1, "Anker fehlt oder ist mehrdeutig: " + alt[:70]
        t = t.replace(alt, neu)
    eins(CSS_ANKER, CSS.rstrip("\n") + "\n" + CSS_ANKER)
    eins(JS_ANKER, JS + JS_ANKER)
    for alt, neu in ERSETZUNGEN:
        eins(alt, neu)
    return t


def main():
    # node --check aus dem ersten Patch wiederverwenden.
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
    print("Bereiche eingebaut:", pfad)


if __name__ == "__main__":
    main()
