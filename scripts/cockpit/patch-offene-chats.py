"""Angefangen, nicht fertig — die offenen Chats als Übersicht (08.10.2026).

Patricia am 08.10.2026: *„ich habe ja jetzt viele chats offen und irgendwie viele
ideen und nie weitergebaut. das hätte ich auch gerne unter aufgaben oder to-dos
einfach in einer übersicht"*.

Quelle ist das Dokument **`daten/offene-chats`** — je Claude-Code-Chat:
worum · was fertig wurde · was offen blieb · nächster Schritt · Bereich ·
Wichtigkeit · Link zurück in den Chat. Erzeugt von Claude aus den Chat-Verläufen
(`mcp__ccd_session_mgmt__list_events`), nicht von einem Skript.

Patricia entscheidet je Eintrag: **Als Aufgabe übernehmen** (legt eine Aufgabe mit
dem nächsten Schritt an) · **Erledigt** · **Verwerfen** · **Zurückholen**.

🚨 **Ihr `status` gehört ihr.** Wer das Dokument neu erzeugt, übernimmt den Status
bestehender Einträge (gleiche `id` = gleiche Session) und ergänzt nur neue Chats —
sonst taucht jeder verworfene Chat beim nächsten Lauf wieder auf.

Setzt patch-mein-tisch.py und patch-bereiche.py voraus.

    python scripts/cockpit/patch-offene-chats.py [--datei <pfad>]
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
MARKE = "---------- Offene Chats (08.10.2026) ----------"

CSS_ANKER = "</style>\n\n<div class=\"shell\">"
CSS = r"""
  /* ---------- Offene Chats (08.10.2026) ---------- */
  .oc-box { margin: 0 0 22px; }
  .oc-kopf { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 6px; }
  .oc-kopf h2 { margin: 0; }
  .oc-kopf .ti-seg { margin: 0 0 0 auto; }
  .oc-karte { border-top: 1px solid var(--line); padding: 12px 0; display: grid; gap: 4px; }
  .oc-karte:first-of-type { border-top: 0; }
  .oc-titel { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
  .oc-titel b { font-family: var(--display); font-weight: 400; font-size: 16px; }
  .oc-text { font-size: 13px; color: var(--ink-soft); margin: 0; }
  .oc-text strong { color: var(--ink); font-weight: 600; }
  .oc-schritt { font-size: 13.5px; margin: 2px 0 0; }
  .oc-schritt::before { content: "\2192  "; color: var(--orange); font-weight: 700; }
  .ti-hinweis {
    display: block; width: 100%; text-align: left; margin: 0 0 10px; cursor: pointer;
    background: var(--orange-soft); color: var(--ink); border: 0; border-radius: 10px;
    padding: 8px 11px; font: inherit; font-size: 12.5px;
  }
  .ti-hinweis b { color: var(--orange); }
"""

JS_ANKER = "  function renderAufgaben(main) {"
JS = r"""  /* =========================================================
     Offene Chats (08.10.2026) — siehe Kopf von patch-offene-chats.py.
     ========================================================= */
  var offeneChats = null;        // daten/offene-chats — Status gehoert PATRICIA
  var ocFilter = "offen";
  var OC_GRUPPEN = [
    { k: "offen", l: "Offen", st: ["offen"] },
    { k: "idee", l: "Nur Idee", st: ["idee"] },
    { k: "aufgabe", l: "Übernommen", st: ["aufgabe"] },
    { k: "weg", l: "Erledigt & verworfen", st: ["erledigt", "verworfen"] }
  ];

  function ocSpeichern() {
    offeneChats.updatedAt = new Date().toISOString();
    lsSet("offene-chats", offeneChats);
    clearTimeout(saveTimers.offeneChats);
    saveTimers.offeneChats = setTimeout(function () {
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/offene-chats").set(offeneChats)
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 500);
  }

  function ocOffenZahl() {
    return ((offeneChats && offeneChats.items) || []).filter(function (c) {
      return c.status === "offen";
    }).length;
  }

  /* Die Zeile auf dem Tisch — ein Hinweis, kein zweiter Ort zum Abarbeiten. */
  function ocHinweis() {
    var n = ocOffenZahl();
    return n ? '<button class="ti-hinweis" data-gehe="aufgaben"><b>' + n +
      ' Chats</b> mit offenen Punkten — unter Aufgaben ansehen</button>' : "";
  }

  function ocBlock(main) {
    var alle = (offeneChats && offeneChats.items) || [];
    if (!alle.length) return;
    var gruppe = OC_GRUPPEN.filter(function (g) { return g.k === ocFilter; })[0] || OC_GRUPPEN[0];
    var RANG = { hoch: 0, mittel: 1, tief: 2 };
    var liste = alle.filter(function (c) { return gruppe.st.indexOf(c.status) >= 0; })
      .sort(function (a, b) {
        var r = (RANG[a.wichtig] || 1) - (RANG[b.wichtig] || 1);
        return r || ((a.zuletzt || "") < (b.zuletzt || "") ? 1 : -1);
      });

    var box = document.createElement("div");
    box.className = "panel oc-box";
    box.innerHTML = '<div class="oc-kopf"><h2>Angefangen, nicht fertig</h2>' +
      '<span class="note">aus deinen Chats · Stand ' + esc(fmtDate(offeneChats.stand || "")) + '</span>' +
      '<div class="ti-seg">' + OC_GRUPPEN.map(function (g) {
        var n = alle.filter(function (c) { return g.st.indexOf(c.status) >= 0; }).length;
        return '<button data-oc="' + g.k + '" aria-pressed="' + (g.k === gruppe.k) + '">' +
          esc(g.l) + '<span class="n">' + n + '</span></button>';
      }).join("") + '</div></div>' +
      '<p class="note" style="margin:0 0 6px">Wichtiges zuerst. „Als Aufgabe übernehmen“ legt den ' +
      'nächsten Schritt in deine Aufgaben — der Chat bleibt hier als „übernommen“ stehen.</p>' +
      '<div class="oc-liste"></div>';
    Array.prototype.forEach.call(box.querySelectorAll("[data-oc]"), function (b) {
      b.onclick = function () { ocFilter = b.getAttribute("data-oc"); render(); };
    });

    var l = box.querySelector(".oc-liste");
    if (!liste.length) l.innerHTML = '<div class="ti-leer">Nichts in dieser Gruppe.</div>';
    liste.forEach(function (c) {
      var k = document.createElement("div");
      k.className = "oc-karte";
      k.innerHTML =
        '<div class="oc-titel"><b>' + esc(c.titel) + '</b>' +
          '<span class="ti-mini">' + esc(c.bereich || "") + '</span>' +
          (c.wichtig === "hoch" ? '<span class="ti-mini hoch">wichtig</span>' : "") +
          '<span class="ti-klein">zuletzt ' + esc(fmtDate(c.zuletzt)) + '</span></div>' +
        (c.worum ? '<p class="oc-text">' + esc(c.worum) + '</p>' : "") +
        (c.stand ? '<p class="oc-text"><strong>Fertig:</strong> ' + esc(c.stand) + '</p>' : "") +
        (c.offen ? '<p class="oc-text"><strong>Offen:</strong> ' + esc(c.offen) + '</p>' : "") +
        (c.naechster ? '<p class="oc-schritt">' + esc(c.naechster) + '</p>' : "") +
        '<div class="ti-knoepfe"></div>';
      var kn = k.querySelector(".ti-knoepfe");
      function knopf(text, art, tun) {
        var b = document.createElement("button");
        b.className = "ti-btn" + (art ? " " + art : "");
        b.textContent = text;
        b.onclick = tun;
        kn.appendChild(b);
      }
      if (c.status === "offen" || c.status === "idee") {
        knopf("Als Aufgabe übernehmen", "voll", function () {
          tiAufgabeNeu({ text: c.naechster || c.titel,
                         bereich: c.bereich === "Privat" ? "Privat" : "Business",
                         notiz: "Aus dem Chat „" + c.titel + "“" + (c.offen ? ": " + c.offen : ""),
                         quelle: "Chat" });
          c.status = "aufgabe"; c.entschieden = todayISO();
          ocSpeichern(); toast("Liegt jetzt in deinen Aufgaben."); render();
        });
        knopf("Ist erledigt", "", function () {
          c.status = "erledigt"; c.entschieden = todayISO(); ocSpeichern(); render();
        });
        knopf("Verwerfen", "orange", function () {
          c.status = "verworfen"; c.entschieden = todayISO(); ocSpeichern(); render();
        });
      } else {
        knopf("Zurückholen", "", function () {
          c.status = "offen"; c.entschieden = ""; ocSpeichern(); render();
        });
      }
      // Zurueck in den Chat. Ein echter Link — window.open() ist im
      // Artifact-Rahmen lautlos blockiert.
      if (c.link) {
        var a = document.createElement("a");
        a.className = "ti-btn"; a.href = c.link; a.target = "_blank"; a.rel = "noopener";
        a.textContent = "Im Chat weitermachen";
        kn.appendChild(a);
      }
      l.appendChild(k);
    });

    var tiles = main.querySelector(".tiles");
    if (tiles && tiles.parentNode) tiles.parentNode.insertBefore(box, tiles.nextSibling);
    else main.appendChild(box);
  }

"""

ERSETZUNGEN = [
    # Laden
    ('  termine = lsGet("termine", null);\n',
     '  termine = lsGet("termine", null);\n'
     '  offeneChats = lsGet("offene-chats", null);\n'),
    # Aus der Datenbank, neuerer Stand gewinnt
    ('      db.doc("daten/termine").onSnapshot(function (snap) {\n',
     '      db.doc("daten/offene-chats").onSnapshot(function (snap) {\n'
     '        if (!snap.exists) return;\n'
     '        var d0 = snap.data() || {};\n'
     '        if (offeneChats && offeneChats.updatedAt && (!d0.updatedAt || d0.updatedAt < offeneChats.updatedAt)) return;\n'
     '        offeneChats = d0;\n'
     '        lsSet("offene-chats", offeneChats);\n'
     '        if (activeTab === "aufgaben" || activeTab === "uebersicht") render();\n'
     '      }, function () {});\n'
     '      db.doc("daten/termine").onSnapshot(function (snap) {\n'),
    # In den Aufgaben-Reiter — auch dann, wenn noch keine Aufgaben da sind
    ('    projekteBlock(main);\n  }\n',
     '    projekteBlock(main);\n    ocBlock(main);\n  }\n'),
    # Hinweis auf dem Tisch, ueber der Aufgabenliste
    ('<div id="ti-afl"></div>\';',
     '<div id="ti-afl"></div>\';\n'
     '    el.querySelector(".ti-kartekopf").insertAdjacentHTML("afterend", ocHinweis());\n'
     '    Array.prototype.forEach.call(el.querySelectorAll("[data-gehe]"), function (b) {\n'
     '      b.onclick = function () { activeTab = b.getAttribute("data-gehe"); render(); };\n'
     '    });'),
]


def patchen(t: str) -> str:
    if MARKE in t:
        print("Schon gepatcht — nichts zu tun.")
        return t
    assert "renderBereiche" in t, "Erst patch-mein-tisch.py und patch-bereiche.py laufen lassen."

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
    print("Offene Chats eingebaut:", pfad)


if __name__ == "__main__":
    main()
