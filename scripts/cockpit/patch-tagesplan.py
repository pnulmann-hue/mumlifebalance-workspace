#!/usr/bin/env python3
"""Reiter „Tagesplan": ein Platz pro Tag und Profil, mit Alternativen.

Patricia am 19.09.2026: *„bitte liste mir pro tag einen beitrag auf und mach
einen reiter wo ich zwischen den verschiedenen vorschlaegen umschalten kann.
heisst fuer montag: einmal doterra (mit alternativen zum umstellen), einmal
mumlifebalance (mit alternativen zum umstellen), 3 reels und 2 karussells
pro woche"*

Die Wochen-Vorschau zeigt alles nebeneinander — wer wissen will, was am
Montag laeuft, scrollt. Hier gibt es **zehn Plaetze** (5 Tage x 2 Profile),
je Platz einen Beitrag und darunter, was sonst dafuer in Frage kaeme.

🚨 Der Platz wird NICHT getrennt gespeichert. Umschalten setzt das `datum`
am neuen Beitrag und leert es am alten — der Beitrag selbst bleibt die
einzige Wahrheit. Ein zweites Verzeichnis daneben waere beim naechsten Umbau
auseinandergelaufen, und Freigabe, Aufgabenliste und „Fertig zum Posten"
lesen alle `datum`.

🚨 Beim Umschalten wird `profil` **hart gesetzt**. Ein leeres `profil` gilt
ueber `kartenProfil()` stillschweigend als Mentoring — so lagen am 16.09.
sechs Beitraege im falschen Profil. Wer einen Beitrag auf den doTERRA-Platz
legt, meint doTERRA.

Wiederholbar: das Skript bricht ab, wenn ein Anker nicht genau einmal
vorkommt, und schreibt erst nach `<datei>.neu`.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

WURZEL = pathlib.Path(__file__).resolve().parents[2]
STANDARD = WURZEL / "outputs" / "cockpit" / "mlb-cockpit.html"


# --------------------------------------------------------------------------
# 1 · Reiter in die Liste
# --------------------------------------------------------------------------
ANKER_TABS = '''    { g: "Planen" },
    { id: "woche", label: "Wochen-Vorschau" },'''
NEU_TABS = '''    { g: "Planen" },
    { id: "tagesplan", label: "Tagesplan" },
    { id: "woche", label: "Wochen-Vorschau" },'''


# --------------------------------------------------------------------------
# 2 · Zahl am Reiter
# --------------------------------------------------------------------------
ANKER_CNT = '''      var cnt = t.id === "fertig" ? fertigAnzahl()'''
NEU_CNT = '''      var cnt = t.id === "tagesplan" ? tagesplanZahl()
        : t.id === "fertig" ? fertigAnzahl()'''


# --------------------------------------------------------------------------
# 3 · Verteiler
# --------------------------------------------------------------------------
ANKER_DISPATCH = '''    else if (activeTab === "woche") renderWoche(main);'''
NEU_DISPATCH = '''    else if (activeTab === "tagesplan") renderTagesplan(main);
    else if (activeTab === "woche") renderWoche(main);'''


# --------------------------------------------------------------------------
# 4 · Der Code selbst, vor renderNav
# --------------------------------------------------------------------------
ANKER_CODE = '''  function renderNav() {'''

NEU_CODE = r'''  /* =========================================================
     Tagesplan: ein Platz je Tag und Profil
     ========================================================= */

  /* Fuenf Tage, zwei Profile — zehn Plaetze in der Woche. Das Soll je Profil
     ist Patricias Entscheid vom 19.09.2026: 3 Reels, 2 Karussells. */
  var TP_SOLL = { reels: 3, karussells: 2 };
  var TP_PROFILE = [
    { id: "mentoring", label: "Mum Life Balance" },
    { id: "doterra", label: "doTERRA" }
  ];
  var tagesplanOffset = null;   // null = noch nicht bestimmt, 0 = diese Woche
  var tagesplanOffen = null;    // "iso|profil" — welcher Platz seine Liste zeigt

  /* Welche Woche beim Oeffnen steht. Normalerweise diese — aber am Freitag
     ist diese Woche durch und geplant wird die naechste. Ein neuer Reiter,
     der eine leere Woche zeigt, sieht kaputt aus, obwohl er stimmt. Deshalb:
     diese Woche, ausser sie ist leer und die naechste nicht. Die Kopfzeile
     nennt immer die KW, und „Diese Woche" holt zurueck. */
  function tpOffset() {
    if (tagesplanOffset === null) {
      tagesplanOffset = (!tpBelegteTage(0) && tpBelegteTage(1)) ? 1 : 0;
    }
    return tagesplanOffset;
  }

  function tpBelegteTage(offset) {
    var belegt = tpBelegung(), n = 0;
    tpTage(offset).forEach(function (t) {
      TP_PROFILE.forEach(function (p) {
        if ((belegt[t.iso + "|" + p.id] || []).length) n++;
      });
    });
    return n;
  }

  /* 🚨 Nie toISOString() fuer ein Datum: das rechnet nach UTC um und macht in
     der Schweiz aus dem 22. abends den 21. Also von Hand aus den lokalen
     Bestandteilen zusammensetzen. */
  function tpIso(d) {
    return d.getFullYear() + "-" +
      String(d.getMonth() + 1).padStart(2, "0") + "-" +
      String(d.getDate()).padStart(2, "0");
  }

  function tpMontag(offset) {
    var t = new Date();
    t.setHours(12, 0, 0, 0);
    t.setDate(t.getDate() - ((t.getDay() + 6) % 7) + offset * 7);
    return t;
  }

  function tpKw(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    t.setUTCDate(t.getUTCDate() + 4 - (t.getUTCDay() || 7));
    var jan = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil(((t - jan) / 86400000 + 1) / 7);
  }

  function tpTage(offset) {
    var m = tpMontag(offset), raus = [];
    for (var i = 0; i < 5; i++) {
      var d = new Date(m);
      d.setDate(m.getDate() + i);
      raus.push({ iso: tpIso(d), datum: d });
    }
    return raus;
  }

  /* Was auf welchem Platz liegt. Mehrere am selben Tag und Profil sind
     erlaubt — der erste ist der Platzhalter, die anderen stehen unten in
     der Liste. Sie zu verstecken waere derselbe Fehler wie am 18.09. bei
     den zwei Generationen im Bild-Editor. */
  function tpBelegung() {
    var karte = {};
    offeneBeitraege().forEach(function (b) {
      if (!b.obj.datum || istLeer(b)) return;
      var k = b.obj.datum + "|" + kartenProfil(b.obj);
      (karte[k] = karte[k] || []).push(b);
    });
    return karte;
  }

  /* Der Vorrat: alles ohne Datum, das zum Profil passt. Genau dort landen
     Beitraege, die von einem Platz verdraengt werden. */
  function tpVorrat(profil) {
    return offeneBeitraege().filter(function (b) {
      return !b.obj.datum && !istLeer(b) && kartenProfil(b.obj) === profil;
    });
  }

  function tpSpeichern(b) {
    if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
  }

  /* Umschalten. Der alte Beitrag faellt in den Vorrat zurueck statt
     verloren zu gehen. */
  function tpBelegen(neu, alt, iso, profil) {
    if (alt && alt.id !== neu.id) {
      alt.obj.datum = "";
      tpSpeichern(alt);
    }
    neu.obj.datum = iso;
    // 🚨 hart setzen, nicht nur wenn leer — sonst bleibt ein Beitrag ohne
    // Profil stillschweigend Mentoring, auch auf dem doTERRA-Platz.
    neu.obj.profil = profil;
    tpSpeichern(neu);
    tagesplanOffen = null;
    toast(neu.titel + " liegt jetzt auf " + tagName(iso) + ".");
    render();
  }

  function tpFreiRaeumen(b) {
    b.obj.datum = "";
    tpSpeichern(b);
    toast(b.titel + " ist zurueck im Vorrat.");
    render();
  }

  /* Wie viele der zehn Plaetze belegt sind — die Zahl am Reiter. */
  function tagesplanZahl() {
    return tpBelegteTage(tpOffset()) + "/10";
  }

  /* Ein Satz zum Zustand — dasselbe Urteil wie in der Wochen-Vorschau,
     nur auf eine Zeile eingedampft. */
  function tpStand(b) {
    if (b.obj.textfrei) return { text: "Freigegeben", art: "gut" };
    var fehlt = wasFehlt(b);
    if (!fehlt.length) {
      return zeitpunktVorbei(b)
        ? { text: "Fertig, aber der Zeitpunkt ist durch", art: "warn" }
        : { text: "Fertig — kann raus", art: "gut" };
    }
    var e = fehlt[0];
    return { text: e.was + (e.wer === "du" ? " (du)" : " (ich)"),
             art: e.wer === "du" ? "warn" : "info" };
  }

  function tpMini(b) {
    var q = coverBild(b);
    return q ? '<img class="tp-mini" src="' + q + '" alt="">'
             : '<div class="tp-mini tp-minileer"></div>';
  }

  function tpZeile(b) {
    var s = tpStand(b);
    return '<span class="tp-format">' + esc(b.format) + '</span>' +
           '<div class="tp-hook">' + esc(b.hook || b.titel || "ohne Hook") + '</div>' +
           '<div class="tp-stand ' + s.art + '">' + esc(s.text) + '</div>';
  }

  function renderTagesplan(main) {
    var tage = tpTage(tpOffset());
    var belegt = tpBelegung();
    var montag = tage[0].datum, freitag = tage[4].datum;

    // Cover nachladen, sonst bleibt der Platz grau.
    offeneBeitraege().forEach(function (b) {
      if (b.obj.datum) wochenBildHolen(b.art, b.id);
    });

    var kurz = function (d) {
      return String(d.getDate()).padStart(2, "0") + "." +
             String(d.getMonth() + 1).padStart(2, "0") + ".";
    };

    // --- Soll/Ist je Profil ------------------------------------------------
    var bilanz = TP_PROFILE.map(function (p) {
      var n = { reels: 0, karussells: 0 };
      tage.forEach(function (t) {
        var liste = belegt[t.iso + "|" + p.id] || [];
        if (liste.length) n[liste[0].art]++;
      });
      var stimmt = n.reels === TP_SOLL.reels && n.karussells === TP_SOLL.karussells;
      return '<div class="tp-bilanz' + (stimmt ? " ok" : "") + '">' +
        '<b>' + esc(p.label) + '</b>' +
        '<span>' + n.reels + ' von ' + TP_SOLL.reels + ' Reels</span>' +
        '<span>' + n.karussells + ' von ' + TP_SOLL.karussells + ' Karussells</span>' +
        (stimmt ? '<span class="tp-haken">passt</span>' : '') +
        '</div>';
    }).join("");

    // --- die fuenf Tage ----------------------------------------------------
    var tageHtml = tage.map(function (t) {
      var spalten = TP_PROFILE.map(function (p) {
        var schluessel = t.iso + "|" + p.id;
        var liste = belegt[schluessel] || [];
        var drauf = liste[0] || null;
        var weitere = liste.slice(1);
        var vorrat = tpVorrat(p.id);
        var offen = tagesplanOffen === schluessel;

        var inhalt = drauf
          ? '<div class="tp-karte">' + tpMini(drauf) +
            '<div class="tp-text">' + tpZeile(drauf) + '</div></div>'
          : '<div class="tp-karte tp-frei">Noch nichts geplant.</div>';

        var anzahl = weitere.length + vorrat.length;
        var knopf = '<button class="btn ghost tp-auf" data-slot="' + schluessel + '">' +
          (offen ? "Liste zu" : (drauf ? "Wechseln" : "Auswählen")) +
          (anzahl ? ' <span class="tp-anz">' + anzahl + '</span>' : "") + '</button>' +
          (drauf ? '<button class="btn ghost tp-weg" data-id="' + drauf.art + ":" + drauf.id +
                   '">Platz leeren</button>' : "");

        var auswahl = "";
        if (offen) {
          var eintraege = weitere.map(function (b) {
            return { b: b, hinweis: "liegt auch an diesem Tag" };
          }).concat(vorrat.map(function (b) {
            return { b: b, hinweis: "" };
          }));
          auswahl = '<div class="tp-alts">' + (eintraege.length
            ? eintraege.map(function (e) {
                return '<button class="tp-alt" data-slot="' + schluessel +
                  '" data-neu="' + e.b.art + ":" + e.b.id + '">' +
                  '<span class="tp-format">' + esc(e.b.format) + '</span>' +
                  '<span class="tp-althook">' + esc(e.b.hook || e.b.titel) + '</span>' +
                  (e.hinweis ? '<span class="tp-hinweis">' + esc(e.hinweis) + '</span>' : "") +
                  '</button>';
              }).join("")
            : '<div class="tp-keine">Nichts im Vorrat für dieses Profil. ' +
              'Im Reiter „Wochen-Vorschau" stehen die Beiträge ohne Datum.</div>') +
            '</div>';
        }

        return '<div class="tp-slot' + (drauf ? "" : " leer") + '">' +
          '<div class="tp-slotkopf">' + esc(p.label) + '</div>' +
          inhalt +
          '<div class="tp-knoepfe">' + knopf + '</div>' +
          auswahl + '</div>';
      }).join("");

      return '<div class="tp-tag"><div class="tp-tagkopf">' +
        '<span class="tp-tagname">' + esc(tagName(t.iso)) + '</span>' +
        '<span class="tp-tagdatum">' + kurz(t.datum) + '</span></div>' +
        '<div class="tp-slots">' + spalten + '</div></div>';
    }).join("");

    main.innerHTML =
      '<div class="page-head"><div><h1>Tagesplan</h1>' +
      '<p>Ein Platz pro Tag und Profil. Darunter steht, was sonst dafür in ' +
      'Frage käme — umschalten legt den bisherigen Beitrag zurück in den Vorrat.</p>' +
      '</div><div class="head-actions">' +
      '<button class="btn" id="tp-zurueck">← Woche</button>' +
      '<span class="tp-kw">KW ' + tpKw(montag) + ' · ' + kurz(montag) + '–' + kurz(freitag) + '</span>' +
      '<button class="btn" id="tp-vor">Woche →</button>' +
      (tpOffset() ? '<button class="btn ghost" id="tp-heute">Diese Woche</button>' : "") +
      '</div></div>' +
      '<div class="tp-bilanzen">' + bilanz + '</div>' +
      tageHtml;

    main.querySelector("#tp-zurueck").onclick = function () {
      tagesplanOffset = tpOffset() - 1; tagesplanOffen = null; render();
    };
    main.querySelector("#tp-vor").onclick = function () {
      tagesplanOffset = tpOffset() + 1; tagesplanOffen = null; render();
    };
    var heuteBtn = main.querySelector("#tp-heute");
    if (heuteBtn) heuteBtn.onclick = function () {
      tagesplanOffset = 0; tagesplanOffen = null; render();
    };

    var finde = function (marke) {
      var teile = String(marke).split(":");
      return alleBeitraege().filter(function (b) {
        return b.art === teile[0] && b.id === teile.slice(1).join(":");
      })[0];
    };

    main.querySelectorAll(".tp-auf").forEach(function (k) {
      k.onclick = function () {
        var s = k.getAttribute("data-slot");
        tagesplanOffen = tagesplanOffen === s ? null : s;
        render();
      };
    });
    main.querySelectorAll(".tp-weg").forEach(function (k) {
      k.onclick = function () {
        var b = finde(k.getAttribute("data-id"));
        if (b) tpFreiRaeumen(b);
      };
    });
    main.querySelectorAll(".tp-alt").forEach(function (k) {
      k.onclick = function () {
        var teile = k.getAttribute("data-slot").split("|");
        var neu = finde(k.getAttribute("data-neu"));
        if (!neu) return;
        var alt = (tpBelegung()[k.getAttribute("data-slot")] || [])[0] || null;
        tpBelegen(neu, alt, teile[0], teile[1]);
      };
    });
  }

  function renderNav() {'''


# --------------------------------------------------------------------------
# 5 · CSS
# --------------------------------------------------------------------------
ANKER_CSS = """  /* ---------- Wochen-Vorschau ---------- */"""

NEU_CSS = """  /* ---------- Tagesplan ---------- */
  .tp-kw { font-family: var(--display); font-size: 15px; align-self: center;
           font-variant-numeric: tabular-nums; }
  .tp-bilanzen { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
  .tp-bilanz {
    display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap;
    background: var(--surface); border: 1px solid var(--line);
    border-left: 3px solid var(--orange);
    border-radius: var(--r); padding: 9px 14px; font-size: 13px;
  }
  .tp-bilanz.ok { border-left-color: var(--good); }
  .tp-bilanz b { font-weight: 600; }
  .tp-bilanz span { color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .tp-bilanz .tp-haken { color: var(--good); }

  .tp-tag { margin-bottom: 18px; }
  .tp-tagkopf { display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px; }
  .tp-tagname { font-family: var(--display); font-size: 18px; }
  .tp-tagdatum { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .tp-slots { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 760px) { .tp-slots { grid-template-columns: 1fr; } }
  .tp-slot {
    background: var(--surface); border: 1px solid var(--line);
    border-radius: var(--r); padding: 12px 14px; box-shadow: var(--shadow);
  }
  .tp-slot.leer { box-shadow: none; background: transparent;
                  border-style: dashed; }
  .tp-slotkopf {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft); margin-bottom: 8px;
  }
  .tp-karte { display: grid; grid-template-columns: 54px 1fr; gap: 11px; align-items: start; }
  .tp-karte.tp-frei {
    display: block; color: var(--ink-soft); font-style: italic; font-size: 13px;
    padding: 6px 0 2px;
  }
  .tp-mini { width: 54px; border-radius: 6px; display: block; background: var(--surface-2); }
  .tp-minileer { aspect-ratio: 9/16; border: 1px dashed var(--line-strong); }
  .tp-text { min-width: 0; }
  .tp-format {
    display: inline-block; font-size: 10px; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--teal); background: var(--teal-soft);
    padding: 1px 8px; border-radius: 999px;
  }
  .tp-hook { font-family: var(--display); font-size: 15px; line-height: 1.3; margin: 4px 0 3px; }
  .tp-stand { font-size: 12px; }
  .tp-stand.gut { color: var(--good); }
  .tp-stand.warn { color: var(--orange); }
  .tp-stand.info { color: var(--teal); }
  .tp-knoepfe { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 9px; }
  .tp-knoepfe .btn { font-size: 12px; padding: 5px 9px; }
  .tp-anz {
    font-size: 10px; background: var(--surface-2); color: var(--ink-soft);
    border-radius: 999px; padding: 0 6px; margin-left: 2px;
  }
  .tp-alts {
    margin-top: 10px; border-top: 1px solid var(--line); padding-top: 8px;
    display: flex; flex-direction: column; gap: 4px;
    max-height: 290px; overflow-y: auto;
  }
  .tp-alt {
    display: flex; align-items: baseline; gap: 8px; width: 100%;
    text-align: left; background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 7px 10px; cursor: pointer; font: inherit; font-size: 13px;
  }
  .tp-alt:hover { border-color: var(--teal); }
  .tp-althook { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .tp-hinweis { font-size: 11px; color: var(--orange); white-space: nowrap; }
  .tp-keine { font-size: 12px; color: var(--ink-soft); font-style: italic; padding: 4px 0; }

  /* ---------- Wochen-Vorschau ---------- */"""


ERSETZUNGEN = [
    ("Reiter in der Liste", ANKER_TABS, NEU_TABS),
    ("Zahl am Reiter", ANKER_CNT, NEU_CNT),
    ("Verteiler", ANKER_DISPATCH, NEU_DISPATCH),
    ("Code", ANKER_CODE, NEU_CODE),
    ("CSS", ANKER_CSS, NEU_CSS),
]


def js_pruefen(html: str) -> None:
    """node --check ueber das eingebettete Skript.

    🚨 Pflicht vor jedem Publish: ein deutsches Anfuehrungszeichen in einer
    JS-Zeichenkette hat schon einmal die ganze Seite totgelegt.
    """
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        sys.exit("Kein <script>-Block gefunden — das kann nicht stimmen.")
    grosse = max(bloecke, key=len)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(grosse)
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
        if r.returncode:
            sys.exit("node --check schlaegt fehl:\n" + (r.stderr or r.stdout))
    finally:
        os.unlink(pfad)
    print("  node --check: in Ordnung")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("datei", nargs="?", type=pathlib.Path, default=STANDARD)
    a = p.parse_args()
    if not a.datei.exists():
        sys.exit(f"Nicht gefunden: {a.datei}")

    html = a.datei.read_text(encoding="utf-8")
    if "renderTagesplan" in html:
        print("Der Tagesplan steckt schon drin — nichts zu tun.")
        return 0

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n != 1:
            sys.exit(f"Anker „{name}“ kommt {n}x vor (erwartet: 1) — nichts geaendert.")
        html = html.replace(alt, neu)
        print(f"  gesetzt: {name}")

    js_pruefen(html)

    # 🚨 Nie in die Zieldatei schreiben, solange etwas schiefgehen kann:
    # open(pfad, "w") leert sie sofort, und ein Fehler danach laesst nichts
    # uebrig. Erst daneben schreiben, dann umbenennen.
    neben = a.datei.with_suffix(a.datei.suffix + ".neu")
    neben.write_text(html, encoding="utf-8")
    os.replace(neben, a.datei)
    print(f"\nFertig: {a.datei}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
