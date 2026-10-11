"""Der Funnel-Reiter zeigt je Keyword die ganze Kette — bis zu den Posts.

Patricia am 25.09.2026: *„vor allem die verknüpften posts müssten dran. ich will
eine klare übersicht mit allen keywords rsp. die zu einem 0€ produkt führen mit
dem verlinkten produkt, wieviele da in der liste sind in active campaign rsp.
wieviele den TAG haben und dem „Manychat" keyword das eine automatische antwort
generiert auf instagram."*

**Eine Tabelle, sechs Spalten, je Zeile ein Keyword:**

| Stichwort | Freebie | Tag (Kontakte) | Angebot danach | Posts | Reichweite |
|---|---|---|---|---|---|

Aufgeklappt kommen dazu: **alle Tag-Stufen** des Freebies, die Automation mit
Status, der Checkout-Link, und die **Posts einzeln** — geplante mit Datum,
gepostete mit Reichweite und Link zum Beitrag.

🚨 **Die Zeile mit null Posts ist der Befund.** Beim ersten Lauf liefen vier
Keywords komplett leer — `STORY`, `QUIZ`, `SYSTEM`, `FAHRPLAN`: Automation
gebaut, Tag angelegt, und kein einziger Beitrag nennt das Wort. Das sieht man
sonst nirgends, weil niemand rückwärts von der Automation zum Content schaut.

🚨 **Ein Freebie hat mehrere Tags, nicht einen.** Bei „Bio-Check" sind es sechs
Stufen — vom Eintrag über „abgeschlossen" bis „→ Thema-Interesse". Die Zeile
zeigt den grössten, aufgeklappt stehen alle. Nur so sieht man, wo die Leute
hängenbleiben.

🚨 **Die Listen-Spalte bleibt meist leer, und das ist kein Fehler.** Patricias
Freebies hängen an Tags, nicht an eigenen Listen. Eine Spalte, die immer leer
ist, wäre irreführend — deshalb steht sie nur dort, wo es wirklich eine Liste
gibt.

    python scripts/cockpit/patch-funnel-uebersicht.py [--pruefen] [--datei <pfad>]
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

ANKER = "  function renderFunnel(main) {"

NEU = '''  /* Der Funnel-Reiter: je Keyword die ganze Kette vom Instagram-Stichwort bis
     zu den Beitraegen, die es spielen. Siehe Kopf von
     patch-funnel-uebersicht.py. */
  function renderFunnelUebersicht(main) {
    var items = (state.funnel || []).slice();
    var stand = funnelStand();
    var leer = items.filter(function (f) {
      return !(f.posts_geplant || []).length && !(f.posts_gepostet || []).length;
    });
    var ohneTag = items.filter(function (f) { return !f.tag_kontakte; });

    main.innerHTML =
      '<div class="page-head"><div><h1>Funnel &amp; Keywords</h1>' +
      '<p>Je Zeile ein Instagram-Stichwort: was sie dafür bekommt, wie viele den ' +
      'Tag tragen, was danach kommt — und welche Beiträge das Wort überhaupt ' +
      'spielen.</p></div>' +
      (stand ? '<div class="head-actions"><span class="note">Stand ' +
        esc(fmtDate(stand)) + '</span></div>' : "") + '</div>' +
      '<div class="tiles">' +
      tile("Stichwörter", items.length, "mit Automation dahinter") +
      tile("Läuft leer", leer.length,
           leer.length ? "kein Beitrag nennt das Wort" : "jedes wird gespielt") +
      tile("Ohne Eintrag", ohneTag.length, "Tag hat null Kontakte") +
      '</div>' +
      (leer.length ? '<div class="panel warn"><strong>' + leer.length +
        ' Stichwörter laufen leer:</strong> ' +
        esc(leer.map(function (f) { return f.keyword; }).join(" · ")) +
        '. Die Automation steht, der Tag ist angelegt — aber kein einziger ' +
        'Beitrag nennt das Wort. Solange das so ist, kommt dort niemand rein.' +
        '</div>' : "") +
      '<div id="fnliste"></div>';

    var box = main.querySelector("#fnliste");
    if (!items.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Noch nichts da. ' +
        '<code>python scripts/cockpit/funnel-uebersicht-bauen.py</code></div></div>';
      return;
    }

    items.forEach(function (f) {
      var gpl = f.posts_geplant || [], gps = f.posts_gepostet || [];
      var k = document.createElement("details");
      k.className = "panel fnkarte" + (!gpl.length && !gps.length ? " fnleer" : "");
      var kontakte = f.tag_kontakte;

      k.innerHTML =
        '<summary class="fnkopf">' +
          '<span class="fnkw">' + esc(f.keyword || "—") + '</span>' +
          '<span class="fnfreebie">' + esc(f.freebie || "—") + '</span>' +
          '<span class="fnzahl" title="Kontakte mit diesem Tag">' +
            (kontakte == null ? "kein Tag" : kontakte + " im Tag") + '</span>' +
          (f.angebot ? '<span class="fnangebot">→ ' + esc(f.angebot) +
            (f.preis ? " · " + f.preis : "") + '</span>' : "") +
          '<span class="fnposts' + (!gpl.length && !gps.length ? " keine" : "") + '">' +
            gps.length + ' raus · ' + gpl.length + ' geplant</span>' +
          (f.reichweite_summe ? '<span class="fnreich">' + f.reichweite_summe +
            ' erreicht</span>' : "") +
        '</summary>' +
        '<div class="fnkoerper"></div>';

      var kb = k.querySelector(".fnkoerper");
      function block(titel, inhalt) {
        if (!inhalt) return;
        var d = document.createElement("div");
        d.className = "fnblock";
        d.innerHTML = '<h4>' + esc(titel) + '</h4>' + inhalt;
        kb.appendChild(d);
      }

      /* 🚨 Alle Tag-Stufen, nicht nur die groesste — sonst sieht man nicht,
         wo die Leute haengenbleiben. */
      if ((f.alle_tags || []).length) {
        block("Tags in ActiveCampaign", '<div class="fntags">' +
          f.alle_tags.map(function (t) {
            return '<span class="fntag' + (t.kontakte ? "" : " null") + '">' +
              esc(t.tag) + ' <b>' + t.kontakte + '</b></span>';
          }).join("") + '</div>');
      }
      if (f.liste) {
        block("Liste", '<p class="note">' + esc(f.liste) + ' · ' +
          (f.liste_kontakte == null ? "?" : f.liste_kontakte) + ' Kontakte</p>');
      }
      if (f.automation) {
        block("Automation", '<p class="note">' + esc(f.automation) +
          (f.automation_status ? ' · ' + esc(f.automation_status) : "") + '</p>');
      }
      if (f.checkout) {
        block("Checkout", '<p class="note"><a href="' + esc(f.checkout) +
          '" target="_blank" rel="noopener">' + esc(f.checkout) + '</a></p>');
      }
      if (gps.length) {
        block("Schon draussen (" + gps.length + ")",
          gps.map(function (p) {
            return '<div class="fnpost"><span class="fnpdat">' +
              esc(fmtDate(p.datum)) + '</span>' +
              '<span class="fnptext">' + esc(p.anfang || "") + '</span>' +
              '<span class="fnpreach">' + (p.reach == null ? "—" : p.reach) +
              (p.rate != null ? ' · ' + p.rate + ' %' : "") + '</span>' +
              (p.link ? '<a class="btn ghost" href="' + esc(p.link) +
                '" target="_blank" rel="noopener">ansehen</a>' : "") + '</div>';
          }).join(""));
      }
      if (gpl.length) {
        block("Geplant (" + gpl.length + ")",
          gpl.map(function (p) {
            return '<div class="fnpost"><span class="fnpdat">' +
              (p.datum ? esc(fmtDate(p.datum)) : "ohne Datum") + '</span>' +
              '<span class="fnptext">' + esc(p.name || p.id) + '</span>' +
              '<span class="fnpreach">' + esc(p.art || "") + '</span></div>';
          }).join(""));
      }
      if (!gpl.length && !gps.length) {
        block("Posts", '<p class="note">Kein Beitrag nennt „' +
          esc(f.keyword) + '". Die Automation läuft leer — hier kommt niemand ' +
          'rein, egal wie gut sie gebaut ist.</p>');
      }
      box.appendChild(k);
    });
  }

  function funnelStand() {
    // Das Stand-Datum liegt am Dokument, nicht an den Zeilen.
    try { return (lsGet("funnel-stand", "") || ""); } catch (e) { return ""; }
  }

  function renderFunnel(main) {
    // 🚨 Neue Ansicht, sobald die Daten aus funnel-uebersicht-bauen.py
    // kommen (erkennbar am Feld `posts_geplant`). Sonst die alte Ketten-
    // Ansicht, damit ein alter Datenstand nicht in eine leere Seite laeuft.
    if ((state.funnel || []).some(function (f) { return f.posts_geplant; })) {
      return renderFunnelUebersicht(main);
    }
    return renderFunnelKetten(main);
  }

  function renderFunnelKetten(main) {'''

CSS_ANKER = "  /* ---------- Funnel-Ketten ---------- */"
CSS_NEU = '''  /* ---------- Funnel-Uebersicht je Keyword (25.09.2026) ---------- */
  .fnkarte { margin-bottom: 10px; padding: 0; }
  .fnkarte > summary {
    display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
    padding: 13px 16px; cursor: pointer; list-style: none;
  }
  .fnkarte > summary::-webkit-details-marker { display: none; }
  .fnkarte > summary::before {
    content: "\\25b6"; font-size: 9px; color: var(--ink-soft);
    transition: transform 0.15s ease;
  }
  .fnkarte[open] > summary::before { transform: rotate(90deg); }
  .fnkw {
    font-family: var(--display); font-size: 16px; letter-spacing: 0.04em;
    background: var(--teal-soft); color: var(--teal);
    padding: 2px 11px; border-radius: 999px;
  }
  .fnfreebie { font-size: 14px; }
  .fnzahl { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .fnangebot { font-size: 12px; color: var(--ink-soft); }
  .fnposts { margin-left: auto; font-size: 12px; color: var(--ink-soft); }
  .fnposts.keine { color: var(--crit); font-weight: 600; }
  .fnreich { font-size: 12px; color: var(--good); font-variant-numeric: tabular-nums; }
  .fnleer { border-left: 3px solid var(--crit); }
  .fnkoerper { padding: 0 16px 14px; border-top: 1px solid var(--line); }
  .fnblock { margin-top: 13px; }
  .fnblock h4 {
    margin: 0 0 6px; font-size: 10px; letter-spacing: 0.09em;
    text-transform: uppercase; color: var(--ink-soft); font-weight: normal;
  }
  .fntags { display: flex; flex-wrap: wrap; gap: 6px; }
  .fntag {
    font-size: 12px; background: var(--surface-2); border-radius: 999px;
    padding: 3px 10px;
  }
  .fntag b { font-variant-numeric: tabular-nums; }
  .fntag.null { opacity: 0.5; }
  .fnpost {
    display: grid; grid-template-columns: 86px 1fr 110px auto; gap: 10px;
    align-items: baseline; padding: 5px 0; border-top: 1px solid var(--line);
    font-size: 13px;
  }
  .fnpost:first-child { border-top: 0; }
  .fnpdat { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .fnptext { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .fnpreach { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  @media (max-width: 760px) {
    .fnpost { grid-template-columns: 1fr auto; }
    .fnptext { grid-column: 1 / -1; white-space: normal; }
  }

  /* ---------- Funnel-Ketten ---------- */'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet 1x." % (name, n))
    return text.replace(alt, neu, 1)


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
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "renderFunnelUebersicht" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER, NEU, "renderFunnel")
    s = setze(s, CSS_ANKER, CSS_NEU, "CSS")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if "--pruefen" in sys.argv:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Funnel-Übersicht eingebaut · %d KB" % (len(s) / 1024))
    print("  Je Keyword: Freebie · Tag-Stufen · Automation · Angebot · Posts mit Reichweite.")


if __name__ == "__main__":
    main()
