"""Die Auswertungstabelle über den Funnel-Karten — für die 5k-Rechnung.

Patricia am 25.09.2026: *„ich will eine analyse machen können, wieviele keywords
wie oft geteilt wurden und auch sicherstellen, dass die keywords verwendet
werden. bin gerade in einem anderen chat mit dem strategieskill am erarbeiten,
wie ich es auf 5k schaffe. und dafür ist es wichtig."*

**Eine Tabelle, sieben Spalten, sortiert nach dem, was am meisten gespielt wurde:**

| Stichwort | gespielt | davon 90 Tage | zuletzt | Reichweite (Median) | im Tag | je Beitrag |

**`je Beitrag` ist die Zahl für die 5k-Rechnung** — Kontakte im Tag geteilt durch
die Beiträge, die das Wort gespielt haben. Damit lässt sich rückwärts rechnen:
wie viele Beiträge braucht es für X Eintragungen.

🚨 **Und genau diese Zahl muss ihre Grenze mitsagen.** Der Tag füllt sich auch
über Landingpage, Story und Mail, und er ist kumulativ über die ganze Zeit. Sie
ist ein **Anhaltspunkt**, keine gemessene Konversion — das steht unter der
Tabelle, nicht im Kleingedruckten. Eine Quote, die sauberer aussieht, als sie
ist, führt eine Strategie in die Irre.

🚨 **Zwei Befunde, die nur diese Ansicht zeigt:**
- **Dasselbe Stichwort für zwei Angebote.** `STIMME` gehört dem Stimm-Check
  **und** „Easy KI für Networkerinnen". ManyChat löst je Keyword genau eine
  Automation aus — der zweite Funnel läuft ins Leere, ohne dass es auffällt.
- **Kontakte ohne einen einzigen Beitrag.** `ENERGIE` hat 31 im Tag und wurde
  auf Instagram **nie** gespielt. Die kommen von woanders her — Landingpage,
  doTERRA-Kanäle. Wer das nicht trennt, schreibt dem Content eine Wirkung zu,
  die er nicht hatte.

    python scripts/cockpit/patch-keyword-analyse.py [--pruefen] [--datei <pfad>]
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

ANKER = "      '<div id=\"fnliste\"></div>';"

NEU = """      analyseBlock(items) +
      '<div id=\"fnliste\"></div>';"""

FUNKTION_ANKER = "  function funnelStand() {"

FUNKTION = '''  /* Die Auswertung: wie oft gespielt, wann zuletzt, was es gebracht hat.
     Siehe Kopf von patch-keyword-analyse.py. */
  function analyseBlock(items) {
    var mit = items.filter(function (f) { return f.gespielt; });
    if (!mit.length) return "";

    var brach = mit.filter(function (f) {
      return f.tage_her != null && f.tage_her > 30;
    }).sort(function (a, b) { return b.tage_her - a.tage_her; });

    /* 🚨 Kontakte ohne einen einzigen Beitrag: die kommen von woanders. */
    var fremd = items.filter(function (f) {
      return !f.gespielt && f.tag_kontakte;
    });

    var doppelt = items.filter(function (f) {
      return (f.doppelt_mit || []).length;
    });
    var gesehen = {};
    var dopp = [];
    doppelt.forEach(function (f) {
      if (gesehen[f.keyword]) return;
      gesehen[f.keyword] = true;
      dopp.push(f);
    });

    var zeilen = items.slice().sort(function (a, b) {
      return (b.gespielt || 0) - (a.gespielt || 0);
    }).map(function (f) {
      var alt = f.tage_her == null ? "nie"
        : (f.tage_her === 0 ? "heute" : "vor " + f.tage_her + " Tagen");
      return '<div class="kazeile' + (f.gespielt ? "" : " kaleer") + '">' +
        '<span class="kakw">' + esc(f.keyword) + '</span>' +
        '<span class="kaz">' + (f.gespielt || "—") + '</span>' +
        '<span class="kaz">' + (f.gespielt_90 || "—") + '</span>' +
        '<span class="kaalt' + (f.tage_her != null && f.tage_her > 30 ? " kabrach" : "") +
          '">' + esc(alt) + '</span>' +
        '<span class="kaz">' + (f.reichweite_median || "—") + '</span>' +
        '<span class="kaz">' +
          (f.tag_kontakte == null ? "—" : f.tag_kontakte) + '</span>' +
        '<span class="kaz kastark">' +
          (f.kontakte_je_beitrag == null ? "—" : f.kontakte_je_beitrag) + '</span>' +
        '</div>';
    }).join("");

    return '<details class="panel kabox" open><summary><span class="ka-titel">' +
      'Was die Stichwörter bringen</span>' +
      '<span class="note">' + mit.length + ' von ' + items.length +
      ' wurden schon gespielt</span></summary>' +
      (dopp.length
        ? '<div class="kawarn"><strong>Dasselbe Stichwort für zwei Angebote:</strong> ' +
          dopp.map(function (f) {
            return esc(f.keyword) + ' (' + esc(f.freebie) + ' und ' +
                   esc((f.doppelt_mit || []).join(", ")) + ')';
          }).join(" · ") +
          '. ManyChat löst je Stichwort genau eine Automation aus — der zweite ' +
          'Funnel läuft ins Leere.</div>'
        : "") +
      '<div class="kakopf">' +
        '<span>Stichwort</span><span>gespielt</span><span>90 Tage</span>' +
        '<span>zuletzt</span><span>Reichw.</span><span>im Tag</span>' +
        '<span>je Beitrag</span>' +
      '</div>' + zeilen +
      '<p class="note kahinweis"><strong>„je Beitrag"</strong> sind die Kontakte ' +
      'im Tag geteilt durch die Beiträge, die das Wort gespielt haben — die Zahl, ' +
      'mit der du rückwärts rechnest, wie viele Beiträge es für X Eintragungen ' +
      'braucht. <strong>Sie ist ein Anhaltspunkt, keine gemessene Quote:</strong> ' +
      'der Tag füllt sich auch über Landingpage, Story und Mail, und er zählt ' +
      'über die ganze Zeit.</p>' +
      (fremd.length
        ? '<p class="note">' + fremd.map(function (f) {
            return '<strong>' + esc(f.keyword) + '</strong> hat ' + f.tag_kontakte +
                   ' im Tag und wurde auf Instagram nie gespielt';
          }).join(" · ") + ' — die Eintragungen kommen von woanders. Dem Content ' +
          'zuschreiben wäre falsch.</p>'
        : "") +
      (brach.length
        ? '<p class="note kabrachzeile">💤 Über einen Monat nicht gespielt: ' +
          brach.map(function (f) {
            return '<strong>' + esc(f.keyword) + '</strong> (vor ' + f.tage_her + ' Tagen)';
          }).join(" · ") + '</p>'
        : "") +
      '</details>';
  }

  function funnelStand() {'''

CSS_ANKER = "  /* ---------- Funnel-Uebersicht je Keyword (25.09.2026) ---------- */"
CSS_NEU = '''  /* ---------- Auswertung je Stichwort ---------- */
  .kabox { margin-bottom: 16px; }
  .kabox > summary {
    display: flex; align-items: baseline; gap: 12px; cursor: pointer;
    list-style: none;
  }
  .kabox > summary::-webkit-details-marker { display: none; }
  .ka-titel { font-family: var(--display); font-size: 17px; }
  .kakopf, .kazeile {
    display: grid; grid-template-columns: 1fr 70px 70px 112px 76px 70px 84px;
    gap: 8px; align-items: baseline;
  }
  .kakopf {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--ink-soft); padding: 12px 0 6px;
    border-bottom: 1px solid var(--line);
  }
  .kakopf span:not(:first-child), .kazeile .kaz, .kazeile .kaalt {
    text-align: right;
  }
  .kazeile {
    padding: 6px 0; border-bottom: 1px solid var(--line); font-size: 13px;
  }
  .kazeile.kaleer { opacity: 0.55; }
  .kakw {
    font-family: var(--display); letter-spacing: 0.04em; font-size: 14px;
  }
  .kaz { font-variant-numeric: tabular-nums; }
  .kastark { font-weight: 600; color: var(--teal); }
  .kaalt { font-size: 12px; color: var(--ink-soft); }
  .kaalt.kabrach { color: var(--crit); }
  .kahinweis { margin-top: 12px; }
  .kawarn {
    background: var(--orange-soft); border-radius: 8px; padding: 9px 12px;
    font-size: 13px; line-height: 1.55; margin-top: 10px;
  }
  @media (max-width: 760px) {
    .kakopf { display: none; }
    .kazeile { grid-template-columns: 1fr 54px 92px 66px; }
    .kazeile .kaz:nth-of-type(2), .kazeile .kaz:nth-of-type(4) { display: none; }
  }

  /* ---------- Funnel-Uebersicht je Keyword (25.09.2026) ---------- */'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet 1x. Nichts geändert." % (name, n))
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
    if "function analyseBlock(" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER, NEU, "Einhängen")
    s = setze(s, FUNKTION_ANKER, FUNKTION, "analyseBlock")
    s = setze(s, CSS_ANKER, CSS_NEU, "CSS")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if "--pruefen" in sys.argv:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Auswertungstabelle eingebaut · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
