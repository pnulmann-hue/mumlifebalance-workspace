"""Macht aus dem leeren Launches-Reiter den Jahresplan.

Patricia am 24.09.2026: *„launches siehst du eigentlich in jahresplanung. da
müssen wir unter umständen dann noch etwas tiefer eintauchen"*.

🚨 **Kein zweiter Reiter.** Der bestehende „Launches"-Reiter war leer —
`daten/launches` gibt es in der Datenbank nicht — waehrend in Notion 54 Eintraege
stehen. Ein neuer Reiter daneben haette zwei Zeitachsen ergeben, die beim
naechsten Umbau auseinanderlaufen. Also wird dieser hier gefuellt.

**Drei Dinge, die der alte Reiter nicht konnte:**

| | |
|---|---|
| **Ferien** | Fuenf Bloecke im Jahr, in denen nichts Grosses starten darf. Kapazitaet ist Planung — auf einer eigenen, gedaempften Spur ganz unten. |
| **Produkttreppe** | 0€ · Mini · Mittel · Hoch je Eintrag. Ohne das sieht man nicht, ob ein Monat vom Freebie oder vom 777er lebt. |
| **Bereich** | Mentoring und doTERRA getrennt, als eigene Spuren. |

🚨 **„Bereich" ist nicht „Phase".** In Notion heisst das Feld „Status" und
enthaelt Mum Life Balance / doTERRa / Ferien — also **wem** etwas gehoert. Die
Phase (Vorbereitung, Warm-up, Verkauf, Cart Close) ist etwas voellig anderes und
bleibt ein eigenes Feld. Wer beides in eine Spalte legt, kann danach keines von
beidem auswerten.

🚨 **`daten/jahresplan` gehoert Patricia.** Der taegliche Abgleich darf es nie
schreiben — wie `daten/ketten` und `daten/produkt-details`. Der Import aus
Notion laeuft **einmal**; danach wird hier gepflegt und dort nicht mehr.

Aufruf:
  python scripts/cockpit/patch-jahresplan.py [--pruefen]
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
# 1) Speicherplatz + laden
# --------------------------------------------------------------------------
ALT_VAR = "  var gepostet = null;        // daten/gepostet — Archiv, gehoert dem Abgleich"
NEU_VAR = """  var gepostet = null;        // daten/gepostet — Archiv, gehoert dem Abgleich
  var jahresplan = null;      // daten/jahresplan — gehoert PATRICIA
  var jpBereich = "";         // Filter"""

ALT_LS = '  gepostet = lsGet("gepostet", null);'
NEU_LS = ('  gepostet = lsGet("gepostet", null);\n'
          '  jahresplan = lsGet("jahresplan", null);')

ALT_SNAP = '''      db.doc("daten/gepostet").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/jahresplan").onSnapshot(function (snap) {
        if (!snap.exists) return;
        jahresplan = snap.data() || null;
        lsSet("jahresplan", jahresplan);
        if (activeTab === "launches") render();
      }, function () {});
      db.doc("daten/gepostet").onSnapshot(function (snap) {'''

# --------------------------------------------------------------------------
# 2) Der Reiter
# --------------------------------------------------------------------------
ALT_FUNK = "  function renderLaunches(main) {"
NEU_FUNK = '''  /* =========================================================
     Jahresplan — was wann laeuft, inklusive Ferien
     ========================================================= */
  var JP_BEREICHE = [
    { k: "mentoring", l: "Mentoring" },
    { k: "doterra", l: "doTERRA" },
    { k: "ferien", l: "Ferien & Termine" },
    { k: "", l: "ohne Zuordnung" }
  ];
  var JP_STUFEN = ["", "0€", "Mini", "Mittel", "Hoch"];

  function jpSpeichern() {
    clearTimeout(saveTimers.jahresplan);
    saveTimers.jahresplan = setTimeout(function () {
      lsSet("jahresplan", jahresplan);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      // 🚨 Gehoert Patricia. Der Abgleich fasst dieses Dokument nie an.
      db.doc("daten/jahresplan")
        .set(Object.assign({}, jahresplan, { updatedAt: new Date().toISOString() }))
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function jpTag(iso) {
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d)) return null;
    return { jahr: d.getFullYear(),
             tag: Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 86400000) };
  }

  function renderJahresplan(main) {
    var jahr = new Date().getFullYear();
    var alle = (jahresplan && jahresplan.eintraege) || [];

    main.innerHTML =
      '<div class="page-head"><div><h1>Jahresplan</h1>' +
      '<p>Was wann läuft — Launches, Freebies und die Ferien, in denen nichts ' +
      'Grosses starten sollte. Hier gepflegt, nicht mehr in Notion.</p></div>' +
      '<div class="head-actions"><select class="btn" id="jpfilter"></select>' +
      '<button class="btn primary" id="jpneu">Eintrag anlegen</button></div></div>' +
      '<div id="jpkacheln" class="tiles"></div>' +
      '<div class="timeline"><div class="tl-track">' +
        '<div class="tl-months">' +
        ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"]
          .map(function (m) { return "<span>" + m + "</span>"; }).join("") +
        '</div><div class="tl-rows" id="jprows">' +
        '<div class="tl-grid">' + new Array(12).fill("<i></i>").join("") + '</div>' +
        '</div></div></div>' +
      '<div id="jpliste"></div>';

    if (!alle.length) {
      main.querySelector("#jpliste").innerHTML =
        '<div class="panel"><div class="empty">Noch nichts übernommen. ' +
        'Der Import aus Notion läuft einmalig über ' +
        '<code>python scripts/cockpit/jahresplan-importieren.py</code>.</div></div>';
      return;
    }

    var f = main.querySelector("#jpfilter");
    [{ k: "", l: "Alle Bereiche" }].concat(JP_BEREICHE).forEach(function (o) {
      var op = document.createElement("option");
      op.value = o.k; op.textContent = o.l;
      if (jpBereich === o.k && !(o.k === "" && jpBereich === "")) op.selected = true;
      f.appendChild(op);
    });
    f.value = jpBereich;
    f.onchange = function () { jpBereich = f.value; render(); };

    var sicht = jpBereich
      ? alle.filter(function (e) { return e.bereich === jpBereich; })
      : alle;

    // --- Kacheln
    var heute = todayISO();
    var laeuft = alle.filter(function (e) {
      return e.start <= heute && (e.ende || e.start) >= heute && e.bereich !== "ferien";
    });
    var naechste = alle.filter(function (e) { return e.start > heute; })
      .sort(function (x, y) { return x.start < y.start ? -1 : 1; })[0];
    var ferienNaechst = alle.filter(function (e) {
      return e.bereich === "ferien" && (e.ende || e.start) >= heute;
    }).sort(function (x, y) { return x.start < y.start ? -1 : 1; })[0];
    var z = (jahresplan && jahresplan.zahlen) || {};

    main.querySelector("#jpkacheln").innerHTML =
      tile("Läuft gerade", laeuft.length,
           laeuft.length ? esc(laeuft[0].name.slice(0, 34)) : "nichts offen") +
      tile("Als Nächstes", naechste ? esc(fmtDate(naechste.start)) : "—",
           naechste ? esc(naechste.name.slice(0, 34)) : "nichts geplant") +
      tile("Nächste Ferien", ferienNaechst ? esc(fmtDate(ferienNaechst.start)) : "—",
           ferienNaechst ? esc(ferienNaechst.name) : "—") +
      tile("Im Jahr " + jahr, z.im_jahr || sicht.length,
           Object.keys(z.nach_stufe || {}).map(function (k) {
             return k + " " + z.nach_stufe[k];
           }).join(" · ") || "Einträge");

    // --- Zeitachse: je Bereich eine Spur, Ferien zuletzt und gedaempft
    var rows = main.querySelector("#jprows");
    JP_BEREICHE.forEach(function (ber) {
      var drin = sicht.filter(function (e) {
        var a = jpTag(e.start);
        return e.bereich === ber.k && a && a.jahr === jahr;
      });
      if (!drin.length) return;
      var spur = document.createElement("div");
      spur.className = "tl-row jp-" + (ber.k || "leer");
      drin.forEach(function (e) {
        var a = jpTag(e.start), b = jpTag(e.ende || e.start) || a;
        if (!a) return;
        var links = (a.tag - 1) / 365 * 100;
        var breite = Math.max(1.6, ((b.tag - a.tag + 1) / 365) * 100);
        var bar = document.createElement("div");
        bar.className = "tl-bar jpbar jp-" + (ber.k || "leer") +
                        (e.vorbei ? " past" : "");
        bar.style.left = links + "%";
        bar.style.width = Math.min(100 - links, breite) + "%";
        bar.title = e.name + " · " + e.start + " bis " + (e.ende || e.start) +
                    (e.stufe ? " · " + e.stufe : "");
        bar.textContent = e.name;
        spur.appendChild(bar);
      });
      rows.appendChild(spur);
    });
    var hTag = jpTag(heute);
    if (hTag) {
      var marker = document.createElement("div");
      marker.className = "tl-today";
      marker.style.left = ((hTag.tag - 1) / 365 * 100) + "%";
      marker.title = "heute";
      rows.appendChild(marker);
    }

    // --- Liste, nach Monat gruppiert
    var liste = main.querySelector("#jpliste");
    var MON = ["Januar","Februar","März","April","Mai","Juni","Juli","August",
               "September","Oktober","November","Dezember"];
    var letzterMonat = "";
    sicht.slice().sort(function (x, y) { return x.start < y.start ? -1 : 1; })
      .forEach(function (e) {
        var mon = (e.start || "").slice(0, 7);
        if (mon !== letzterMonat) {
          letzterMonat = mon;
          var h = document.createElement("h2");
          h.className = "jpmonat";
          var t = mon.split("-");
          h.textContent = (MON[Number(t[1]) - 1] || mon) + " " + t[0];
          liste.appendChild(h);
        }
        liste.appendChild(jpZeile(e));
      });

    main.querySelector("#jpneu").onclick = function () {
      jahresplan.eintraege.push({
        id: uid("jp"), name: "Neuer Eintrag", start: heute, ende: heute,
        bereich: jpBereich || "mentoring", stufe: ""
      });
      jpSpeichern(); render();
    };
  }

  function jpZeile(e) {
    var z = document.createElement("div");
    z.className = "jpzeile" + (e.vorbei ? " vorbei" : "") +
                  (e.bereich === "ferien" ? " ferien" : "");

    function feld(typ, schluessel, breite, opts) {
      var el;
      if (opts) {
        el = document.createElement("select");
        opts.forEach(function (o) {
          var op = document.createElement("option");
          op.value = typeof o === "string" ? o : o.k;
          op.textContent = (typeof o === "string" ? o : o.l) || "—";
          if ((e[schluessel] || "") === op.value) op.selected = true;
          el.appendChild(op);
        });
      } else {
        el = document.createElement("input");
        el.type = typ;
        el.value = e[schluessel] || "";
      }
      el.style.width = breite;
      el.oninput = el.onchange = function () {
        e[schluessel] = el.value;
        jpSpeichern();
      };
      return el;
    }

    z.appendChild(feld("date", "start", "130px"));
    z.appendChild(feld("date", "ende", "130px"));
    z.appendChild(feld("text", "name", "100%"));
    z.appendChild(feld(null, "bereich", "150px", JP_BEREICHE));
    z.appendChild(feld(null, "stufe", "96px", JP_STUFEN));

    var weg = document.createElement("button");
    weg.className = "del";
    weg.textContent = "×";
    var scharf = false;
    weg.onclick = function () {
      // 🚨 Kein confirm() — im Artifact-Rahmen kann ein Modal lautlos
      // blockiert sein. Zwei Klicks, der zweite verfaellt.
      if (!scharf) {
        scharf = true;
        weg.classList.add("scharf");
        weg.textContent = "sicher?";
        setTimeout(function () {
          scharf = false; weg.classList.remove("scharf"); weg.textContent = "×";
        }, 6000);
        return;
      }
      jahresplan.eintraege = jahresplan.eintraege.filter(function (x) {
        return x.id !== e.id;
      });
      jpSpeichern(); render();
    };
    z.appendChild(weg);
    return z;
  }

  /* 🗃 Abgeloest am 24.09.2026 durch renderJahresplan. Blieb stehen, weil
     PHASEN und dayOfYear noch anderswo gebraucht werden; die Funktion selbst
     ruft niemand mehr auf und darf beim naechsten Umbau raus. */
  function renderLaunches(main) {'''

ALT_DISP = '    else if (activeTab === "launches") renderLaunches(main);'
NEU_DISP = '    else if (activeTab === "launches") renderJahresplan(main);'

ALT_NAV = '    { id: "launches", label: "Launches" },'
NEU_NAV = '    { id: "launches", label: "Jahresplan" },'

# --------------------------------------------------------------------------
# 3) Aussehen
# --------------------------------------------------------------------------
ALT_CSS = "  .gpein { border-left: 3px solid var(--orange); }"
NEU_CSS = """  .jpbar { font-size: 11px; line-height: 20px; height: 20px; top: 4px; }
  .tl-row.jp-mentoring .jpbar { background: var(--teal); }
  .tl-row.jp-doterra .jpbar { background: var(--orange); }
  .tl-row.jp-ferien .jpbar { background: var(--surface-2); color: var(--ink-soft);
                             border: 1px dashed var(--line-strong); }
  .tl-row.jp-leer .jpbar { background: var(--navy); }
  .jpbar.past { opacity: 0.45; }
  .jpmonat {
    font-family: var(--display); font-size: 16px; font-weight: normal;
    margin: 20px 0 6px; padding-bottom: 5px; border-bottom: 1px solid var(--line);
  }
  .jpzeile {
    display: grid; grid-template-columns: 130px 130px 1fr 150px 96px 34px;
    gap: 9px; align-items: center; padding: 5px 0;
  }
  .jpzeile.vorbei { opacity: 0.55; }
  .jpzeile.ferien input[type="text"] { font-style: italic; }
  .jpzeile input, .jpzeile select {
    background: var(--ground); border: 1px solid transparent; border-radius: 7px;
    padding: 6px 8px; font-size: 13px;
  }
  .jpzeile input:hover, .jpzeile select:hover { border-color: var(--line); }
  .jpzeile input:focus, .jpzeile select:focus {
    border-color: var(--teal); outline: none;
  }
  .jpzeile .del {
    border: 0; background: none; color: var(--ink-soft); cursor: pointer;
    padding: 4px 6px; border-radius: 6px; font-size: 15px; line-height: 1;
  }
  .jpzeile .del:hover { background: var(--orange-soft); color: var(--crit); }
  .jpzeile .del.scharf {
    background: var(--crit); color: #fbf8f1; font-size: 11px; padding: 4px 7px;
  }
  @media (max-width: 860px) {
    .jpzeile { grid-template-columns: 1fr 1fr 34px; }
    .jpzeile input[type="text"] { grid-column: 1 / -1; }
  }
  .gpein { border-left: 3px solid var(--orange); }"""

ERSETZUNGEN = [
    ("Speicherplatz", ALT_VAR, NEU_VAR),
    ("Lokal laden", ALT_LS, NEU_LS),
    ("Aus der Datenbank", ALT_SNAP, NEU_SNAP),
    ("Der Reiter", ALT_FUNK, NEU_FUNK),
    ("Dispatcher", ALT_DISP, NEU_DISP),
    ("Beschriftung", ALT_NAV, NEU_NAV),
    ("Aussehen", ALT_CSS, NEU_CSS),
]


def node_pruefen(html):
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(max(bloecke, key=len))
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
        return "" if r.returncode == 0 else (r.stderr or "").strip()[:600]
    except FileNotFoundError:
        return ""
    finally:
        Path(pfad).unlink(missing_ok=True)


def main():
    nur_pruefen = "--pruefen" in sys.argv
    html = SEITE.read_text(encoding="utf-8")
    vorher = len(html)

    if "function renderJahresplan" in html:
        sys.exit("Der Jahresplan ist schon drin — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-20s ersetzt" % name)

    # Gegenprobe: der alte Reiter darf nirgends mehr aufgerufen werden.
    if "renderLaunches(main)" in html.replace("function renderLaunches(main) {", ""):
        sys.exit("ABBRUCH — renderLaunches wird noch aufgerufen.")
    print("  Gegenprobe          : renderLaunches wird nicht mehr aufgerufen")

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
