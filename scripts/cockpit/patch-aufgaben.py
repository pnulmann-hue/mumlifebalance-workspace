"""Baut den Reiter „Aufgaben" — Ersatz fuer die Notion-Aufgabenliste.

🚨 **Ueberfaellig steht oben und ist rot.** Von 53 offenen Aufgaben waren beim
Import **37 ueberfaellig**, die aelteste seit dem 16. Juni. In Notion standen
sie in derselben Liste wie alles andere, nach Datum sortiert — eine ueberfaellige
Aufgabe sah genauso aus wie eine, die naechste Woche dran ist.

🚨 **`daten/aufgaben` gehoert Patricia.** Der taegliche Abgleich darf es nie mit
`set` ueberschreiben — sonst sind abgehakte Aufgaben am naechsten Morgen wieder
da. Neue Eintraege aus dem Bot-Eingangskorb kommen per `update` dazu.

🚨 **Abhaken loescht nicht.** Eine erledigte Aufgabe bleibt mit Datum stehen und
rutscht nach unten. Wer loescht, verliert die Antwort auf „was habe ich diesen
Monat eigentlich geschafft" — und genau die braucht der Monatsbogen.

Aufruf:
  python scripts/cockpit/patch-aufgaben.py [--pruefen]
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

ALT_NAV = '    { id: "wochenbogen", label: "Wochenbogen" },'
NEU_NAV = ('    { id: "aufgaben", label: "Aufgaben" },\n'
           '    { id: "wochenbogen", label: "Wochenbogen" },')

ALT_VAR = '  var stimmen = null;            // daten/stimmen — Kundenstimmen'
NEU_VAR = """  var stimmen = null;            // daten/stimmen — Kundenstimmen
  var aufgaben = null;           // daten/aufgaben — gehoert PATRICIA
  var afFilter = "offen";"""

ALT_LS = '  stimmen = lsGet("stimmen", null);'
NEU_LS = ('  stimmen = lsGet("stimmen", null);\n'
          '  aufgaben = lsGet("aufgaben", null);')

ALT_SNAP = '''      db.doc("daten/stimmen").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/aufgaben").onSnapshot(function (snap) {
        if (!snap.exists) return;
        aufgaben = snap.data() || null;
        lsSet("aufgaben", aufgaben);
        if (activeTab === "aufgaben") render();
      }, function () {});
      db.doc("daten/stimmen").onSnapshot(function (snap) {'''

ALT_FUNK = "  function stimmenBlock(main) {"
NEU_FUNK = '''  /* =========================================================
     Aufgaben
     ========================================================= */
  var AF_PRIO = ["Hoch", "Mittel", "Tief", "Quick Win"];

  function afSpeichern() {
    clearTimeout(saveTimers.aufgaben);
    saveTimers.aufgaben = setTimeout(function () {
      lsSet("aufgaben", aufgaben);
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/aufgaben")
        .set(Object.assign({}, aufgaben, { updatedAt: new Date().toISOString() }))
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 700);
  }

  function afZeile(a) {
    var z = document.createElement("div");
    var faellig = a.datum && a.datum < todayISO() && !a.erledigt;
    z.className = "afzeile" + (a.erledigt ? " fertig" : "") +
                  (faellig ? " faellig" : "");

    var cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = !!a.erledigt;
    cb.title = "erledigt";
    cb.onchange = function () {
      // 🚨 Nicht loeschen, nur markieren — mit Datum, damit der Monatsbogen
      // spaeter sagen kann, was in dem Monat fertig geworden ist.
      a.erledigt = cb.checked;
      a.erledigt_am = cb.checked ? todayISO() : "";
      afSpeichern(); render();
    };
    z.appendChild(cb);

    var t = document.createElement("input");
    t.type = "text"; t.value = a.aufgabe || "";
    t.className = "aftext";
    t.oninput = function () { a.aufgabe = t.value; afSpeichern(); };
    z.appendChild(t);

    var p = document.createElement("select");
    AF_PRIO.forEach(function (o) {
      var op = document.createElement("option");
      op.value = o; op.textContent = o;
      if ((a.prio || "Mittel") === o) op.selected = true;
      p.appendChild(op);
    });
    p.onchange = function () { a.prio = p.value; afSpeichern(); render(); };
    z.appendChild(p);

    var d = document.createElement("input");
    d.type = "date"; d.value = a.datum || "";
    d.onchange = function () { a.datum = d.value; afSpeichern(); render(); };
    z.appendChild(d);

    var tage = document.createElement("span");
    tage.className = "aftage";
    if (faellig) {
      var diff = Math.round(
        (new Date(todayISO()) - new Date(a.datum)) / 86400000);
      tage.textContent = diff + " Tage";
    } else if (a.erledigt && a.erledigt_am) {
      tage.textContent = "erledigt";
    }
    z.appendChild(tage);

    var weg = document.createElement("button");
    weg.className = "del";
    weg.textContent = "×";
    var scharf = false;
    weg.onclick = function () {
      if (!scharf) {
        scharf = true; weg.classList.add("scharf"); weg.textContent = "sicher?";
        setTimeout(function () {
          scharf = false; weg.classList.remove("scharf"); weg.textContent = "×";
        }, 6000);
        return;
      }
      aufgaben.items = aufgaben.items.filter(function (x) { return x.id !== a.id; });
      afSpeichern(); render();
    };
    z.appendChild(weg);

    if (a.notiz) {
      var n = document.createElement("p");
      n.className = "afnotiz";
      n.textContent = a.notiz;
      z.appendChild(n);
    }
    return z;
  }

  function renderAufgaben(main) {
    if (!aufgaben || !(aufgaben.items || []).length) {
      main.innerHTML =
        '<div class="page-head"><div><h1>Aufgaben</h1>' +
        '<p>Was ansteht — überfällig zuerst.</p></div></div>' +
        '<div class="panel"><div class="empty">Noch nichts übernommen:<br>' +
        '<code>python scripts/cockpit/aufgaben-bauen.py</code></div></div>';
      return;
    }
    var alle = aufgaben.items;
    var heute = todayISO();
    var offen = alle.filter(function (a) { return !a.erledigt; });
    var faellig = offen.filter(function (a) { return a.datum && a.datum < heute; });
    var heuteF = offen.filter(function (a) { return a.datum === heute; });
    var fertig = alle.filter(function (a) { return a.erledigt; });

    main.innerHTML =
      '<div class="page-head"><div><h1>Aufgaben</h1>' +
      '<p>Überfällig steht oben. Abhaken löscht nicht — eine erledigte Aufgabe ' +
      'bleibt mit Datum stehen, sonst weiss am Monatsende niemand mehr, was ' +
      'geschafft wurde.</p></div>' +
      '<div class="head-actions"><select class="btn" id="affilter">' +
        '<option value="offen">Nur offene</option>' +
        '<option value="faellig">Nur überfällige</option>' +
        '<option value="alle">Alle</option>' +
      '</select><button class="btn primary" id="afneu">Aufgabe anlegen</button>' +
      '</div></div>' +
      '<div class="tiles">' +
      tile("Überfällig", faellig.length,
           faellig.length ? "älteste " + esc(faellig[0].datum || "") : "nichts offen") +
      tile("Heute", heuteF.length, "fällig") +
      tile("Offen gesamt", offen.length,
           (aufgaben.nach_prio ? Object.keys(aufgaben.nach_prio).map(function (k) {
             return k + " " + aufgaben.nach_prio[k]; }).join(" · ") : "")) +
      tile("Erledigt", fertig.length, "bleiben stehen") +
      '</div>' +
      '<div class="panel"><div class="afkopf">' +
        '<span></span><span>Aufgabe</span><span>Priorität</span>' +
        '<span>Fällig</span><span></span><span></span></div>' +
        '<div id="afliste"></div></div>' +
      '<p class="note" style="margin-top:12px">' + esc(aufgaben.hinweis || "") + '</p>';

    var f = main.querySelector("#affilter");
    f.value = afFilter;
    f.onchange = function () { afFilter = f.value; render(); };

    var zeigen = afFilter === "alle" ? alle
      : (afFilter === "faellig" ? faellig : offen);
    // Überfällig zuerst, dann nach Datum. Erledigte ganz unten.
    zeigen = zeigen.slice().sort(function (x, y) {
      if (!!x.erledigt !== !!y.erledigt) return x.erledigt ? 1 : -1;
      var xf = x.datum && x.datum < heute, yf = y.datum && y.datum < heute;
      if (xf !== yf) return xf ? -1 : 1;
      return (x.datum || "9999") < (y.datum || "9999") ? -1 : 1;
    });

    var box = main.querySelector("#afliste");
    if (!zeigen.length) {
      box.innerHTML = '<div class="empty">Nichts in dieser Ansicht.</div>';
    }
    zeigen.forEach(function (a) { box.appendChild(afZeile(a)); });

    main.querySelector("#afneu").onclick = function () {
      aufgaben.items.unshift({
        id: uid("af"), aufgabe: "", datum: todayISO(), prio: "Mittel",
        status: "Geplant", notiz: "", erledigt: false, quelle: "Cockpit"
      });
      afSpeichern(); render();
    };
  }

  function stimmenBlock(main) {'''

ALT_DISP = '    else if (activeTab === "wochenbogen") renderWochenbogen(main);'
NEU_DISP = ('    else if (activeTab === "wochenbogen") renderWochenbogen(main);\n'
            '    else if (activeTab === "aufgaben") renderAufgaben(main);')

ALT_CSS = "  .stimme {"
NEU_CSS = """  .afkopf, .afzeile {
    display: grid; grid-template-columns: 26px 1fr 120px 140px 74px 34px;
    gap: 9px; align-items: center;
  }
  .afkopf {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); padding-bottom: 8px; border-bottom: 1px solid var(--line);
  }
  .afzeile { padding: 5px 0; border-bottom: 1px solid var(--line); }
  .afzeile.faellig { box-shadow: inset 3px 0 0 var(--crit); padding-left: 9px; }
  .afzeile.fertig { opacity: 0.5; }
  .afzeile.fertig .aftext { text-decoration: line-through; }
  .afzeile input[type="text"], .afzeile input[type="date"], .afzeile select {
    background: var(--ground); border: 1px solid transparent; border-radius: 7px;
    padding: 6px 8px; font-size: 13px; width: 100%;
  }
  .afzeile input:hover, .afzeile select:hover { border-color: var(--line); }
  .afzeile input:focus, .afzeile select:focus {
    border-color: var(--teal); outline: none;
  }
  .aftage { font-size: 11px; color: var(--crit); text-align: right; }
  .afzeile.fertig .aftage { color: var(--ink-soft); }
  .afnotiz {
    grid-column: 2 / -1; margin: 0 0 6px; font-size: 12px;
    color: var(--ink-soft); line-height: 1.5;
  }
  .afzeile .del {
    border: 0; background: none; color: var(--ink-soft); cursor: pointer;
    padding: 4px 6px; border-radius: 6px; font-size: 15px; line-height: 1;
  }
  .afzeile .del:hover { background: var(--orange-soft); color: var(--crit); }
  .afzeile .del.scharf {
    background: var(--crit); color: #fbf8f1; font-size: 11px; padding: 4px 7px;
  }
  @media (max-width: 800px) {
    .afkopf { display: none; }
    .afzeile { grid-template-columns: 26px 1fr 34px; }
    .afzeile select, .afzeile input[type="date"] { grid-column: 2; }
    .aftage { grid-column: 2; text-align: left; }
  }
  .stimme {"""

ERSETZUNGEN = [
    ("Reiter in der Leiste", ALT_NAV, NEU_NAV),
    ("Speicherplatz", ALT_VAR, NEU_VAR),
    ("Lokal laden", ALT_LS, NEU_LS),
    ("Aus der Datenbank", ALT_SNAP, NEU_SNAP),
    ("Der Reiter", ALT_FUNK, NEU_FUNK),
    ("Dispatcher", ALT_DISP, NEU_DISP),
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

    if "function renderAufgaben" in html:
        sys.exit("Der Aufgaben-Reiter ist schon drin — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-22s ersetzt" % name)

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
