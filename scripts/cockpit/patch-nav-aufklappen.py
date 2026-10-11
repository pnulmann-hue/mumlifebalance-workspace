"""Macht aus den Navigations-Gruppen aufklappbare Bereiche.

Patricia am 24.09.2026: *„kannst du es nicht so machen, dass ich content als
eigenen reiter habe und erst wenn ich ihn anklicke, kommen die unterpunkte?"*

Vorher standen alle 24 Reiter untereinander, die Gruppenüberschriften waren nur
Beschriftung. Jetzt ist **eine** Gruppe offen und der Rest zugeklappt — aus
24 sichtbaren Zeilen werden sechs plus die Punkte der offenen Gruppe.

🚨 **Die Gruppe des aktiven Reiters ist immer offen.** Sonst klickt man sich
auf «Planen», die Gruppe klappt zu, und man sieht nicht mehr, wo man ist.
Deshalb entscheidet nicht nur der Klick, sondern auch `activeTab`.

🚨 **Nur eine Gruppe offen.** Zwei offene Gruppen sind fast so lang wie die
alte Liste, und dann hat das Aufklappen nichts gebracht.

🚨 **Die Wahl überlebt das Neuladen** (`localStorage`), aber die Seite muss
auch ohne funktionieren — im privaten Fenster oder bei gesperrtem Speicher
wirft der Zugriff. Deshalb steht jeder Zugriff in einem try/catch, wie überall
sonst im Cockpit auch.

    python scripts/cockpit/patch-nav-aufklappen.py [--pruefen] [--datei <pfad>]
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

# ---------------------------------------------------------------- 1 · CSS

CSS_ALT = "  .navgroup { padding: 18px 10px 5px; }"

CSS_NEU = r"""  /* Aufklappbare Bereiche (24.09.2026). Eine Gruppe offen, Rest zu. */
  .navgroup {
    display: flex; align-items: center; gap: 8px; width: 100%;
    background: none; border: 0; cursor: pointer; text-align: left;
    font: inherit; font-size: 11px; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--ink-soft);
    padding: 11px 10px; margin-top: 6px; border-radius: 8px;
  }
  .navgroup:hover { background: var(--surface-2); color: var(--ink); }
  .navgroup[aria-expanded="true"] { color: var(--ink); font-weight: bold; }
  .navgroup .pfeil {
    margin-left: auto; font-size: 10px; line-height: 1;
    transition: transform 0.15s ease; opacity: 0.7;
  }
  .navgroup[aria-expanded="true"] .pfeil { transform: rotate(90deg); }
  .navgroup .gcnt {
    font-size: 10px; font-weight: normal; letter-spacing: 0;
    color: var(--ink-soft); background: var(--surface-2);
    border-radius: 999px; padding: 1px 7px;
  }
  .navgroup[aria-expanded="true"] .gcnt { background: var(--teal-soft); }"""

# ------------------------------------------------------------- 2 · renderNav

NAV_NEU = r'''  /* Welche Gruppe aufgeklappt ist. Siehe Kopf von patch-nav-aufklappen.py:
     nur eine, und die des aktiven Reiters immer. */
  var offeneGruppe = null;
  try { offeneGruppe = localStorage.getItem("mlb:navgruppe"); } catch (e) {}

  function navBaum() {
    var baum = [], aktuell = null;
    TABS.forEach(function (t) {
      if (t.g) { aktuell = { g: t.g, items: [] }; baum.push(aktuell); return; }
      if (aktuell) aktuell.items.push(t);
      else baum.push({ solo: t });
    });
    return baum;
  }

  function gruppeVon(id) {
    var g = null;
    navBaum().forEach(function (k) {
      if (k.items && k.items.some(function (t) { return t.id === id; })) g = k.g;
    });
    return g;
  }

  function navZahl(t) {
    // 🚨 Eine 0 an einem Reiter mit Daten ist eine Falschaussage — der
    // Jahresplan zeigte 0, obwohl 54 Einträge drin sind. Deshalb nur
    // positive Zahlen.
    var c = t.id === "fertig" ? fertigAnzahl()
      : t.id === "storys" ? state.storys.length
      : t.id === "reels" ? state.reels.length
      : (Array.isArray(state[t.id]) ? state[t.id].length : "");
    return (c !== "" && c > 0) ? c : "";
  }

  function renderNav() {
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    var aktivGruppe = gruppeVon(activeTab);
    // Die Gruppe des aktiven Reiters ist immer offen — sonst verliert man
    // beim Klicken die Orientierung.
    var offen = aktivGruppe || offeneGruppe;

    function knopf(t) {
      var b = document.createElement("button");
      b.className = t.sub ? "navbtn navsub" : "navbtn";
      b.setAttribute("aria-current", activeTab === t.id ? "true" : "false");
      var c = navZahl(t);
      b.innerHTML = "<span>" + esc(t.label) + "</span>" +
        (c !== "" ? '<span class="cnt">' + c + "</span>" : "");
      b.onclick = function () { activeTab = t.id; render(); };
      return b;
    }

    navBaum().forEach(function (k) {
      if (k.solo) { nav.appendChild(knopf(k.solo)); return; }

      var auf = k.g === offen;
      var kopf = document.createElement("button");
      kopf.className = "navgroup";
      kopf.setAttribute("aria-expanded", auf ? "true" : "false");
      // Summe der Zahlen in der Gruppe, damit man zugeklappt trotzdem sieht,
      // dass dort etwas wartet.
      var summe = k.items.reduce(function (a, t) {
        var c = navZahl(t); return a + (c === "" ? 0 : c);
      }, 0);
      kopf.innerHTML = "<span>" + esc(k.g) + "</span>" +
        (summe ? '<span class="gcnt">' + summe + "</span>" : "") +
        '<span class="pfeil">▶</span>';
      kopf.onclick = function () {
        offeneGruppe = auf ? null : k.g;
        try { localStorage.setItem("mlb:navgruppe", offeneGruppe || ""); } catch (e) {}
        // Beim Zuklappen der aktiven Gruppe zurück auf «Heute», sonst stünde
        // man auf einer Seite, deren Reiter nicht mehr sichtbar ist.
        if (auf && k.g === aktivGruppe) activeTab = "uebersicht";
        render();
      };
      nav.appendChild(kopf);

      if (auf) k.items.forEach(function (t) { nav.appendChild(knopf(t)); });
    });
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
    if "navBaum" in s:
        print("  Schon umgebaut — nichts zu tun.")
        return

    if s.count(CSS_ALT) != 1:
        sys.exit("🚨 CSS-Anker kommt %dx vor." % s.count(CSS_ALT))
    s = s.replace(CSS_ALT, CSS_NEU, 1)

    zeilen = s.split("\n")
    a = next(i for i, z in enumerate(zeilen) if "function renderNav()" in z)
    b = next(i for i in range(a, len(zeilen))
             if zeilen[i] == "  }" or (zeilen[i].startswith("  }")
                                       and not zeilen[i].startswith("  })")))
    alt = "\n".join(zeilen[a:b + 1])
    print("  Alte renderNav: %d Zeilen" % (b - a + 1))
    s = s.replace(alt, NAV_NEU, 1)

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Navigation aufklappbar · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
