"""Zeigt die echten Instagram-Zahlen im Reiter „Zahlen & Ziele".

Bis zum 24.09.2026 war „Zahlen & Ziele" reine Handarbeit: Patricia trug Umsatz,
Verkaeufe und Listenwachstum von Hand ein. Die **gemessenen** Zahlen —
Reichweite, Speicherungen, Geteilt je Beitrag — holt
`scripts/instagram-insights/holen.py` ueber die Meta Graph API, aber sie endeten
in einer Markdown-Datei, die niemand aufmacht.

Anlass: eine Werbeanzeige vom 24.09.2026, in der jemand genau diese Zahlen im
Dashboard stehen hat, samt roter Warnung „seit 3 Tagen kein Abruf".

Neu: ein Block **„Was Instagram misst"** ueber der Umsatz-Tabelle.

🚨 **Die Warnung ist der eigentliche Wert.** Eine Zahl ohne Datum daneben sieht
immer aktuell aus. Ist der Abzug drei Tage oder aelter, steht der Block rot da
und nennt den Befehl zum Nachholen — sonst trifft sie Entscheidungen auf einem
Stand von letzter Woche.

🚨 **Median UND Mittelwert.** Ein Reel mit 1'328 Aufrufen zieht den Schnitt auf
272, waehrend der Median bei 182 liegt. Wer nur den Schnitt zeigt, behauptet
eine Reichweite, die die normale Woche nie hat.

Aufruf:
  python scripts/cockpit/patch-instagram-zahlen.py [--pruefen]
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
# 1) Speicherplatz fuer das Dokument
# --------------------------------------------------------------------------
ALT_VAR = "  var links = null;"
NEU_VAR = """  var links = null;
  // 🚨 NICHT `zahlen` nennen — `state.zahlen` ist Patricias haendische
  // Umsatz-Tabelle (ein Array). Ein zweites `zahlen` im localStorage hat sie
  // ueberschrieben, und `renderZahlen` stuerzte mit „slice is not a function"
  // ab — der ganze Reiter war tot. Gefunden hat das die lokale Testfassung,
  // bevor es live ging.
  var igzahlen = null;   // daten/instagram — gemessene Instagram-Werte"""


ALT_LS = '  links = lsGet("links", null);'
NEU_LS = '  links = lsGet("links", null);\n  igzahlen = lsGet("ig-zahlen", null);'

# --------------------------------------------------------------------------
# 2) Aus der Datenbank nachladen
# --------------------------------------------------------------------------
ALT_SNAP = '''      db.doc("daten/links").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/instagram").onSnapshot(function (snap) {
        if (!snap.exists) return;
        igzahlen = snap.data() || null;
        lsSet("ig-zahlen", igzahlen);
        if (activeTab === "zahlen") render();
      }, function () {});
      db.doc("daten/links").onSnapshot(function (snap) {'''

# --------------------------------------------------------------------------
# 3) Der Block selbst
# --------------------------------------------------------------------------
ALT_BLOCK = """      '<div class="panel" id="planbox" style="margin-bottom:18px"></div>' +"""
NEU_BLOCK = """      igBlock() +
      '<div class="panel" id="planbox" style="margin-bottom:18px"></div>' +"""

ALT_FUNK = "  function renderZahlen(main) {"
NEU_FUNK = '''  function igZeile(k) {
    var b = k.bester, s = k.schwaechster;
    return '<div class="igkonto">' +
      '<div class="igkopf"><strong>@' + esc(k.handle) + '</strong>' +
        '<span class="note">' + (k.follower || 0).toLocaleString("de-CH") +
        ' Follower · ' + (k.beitraege_gezaehlt || 0) + ' Beiträge</span></div>' +
      '<div class="igwerte">' +
        '<div><b>' + (k.reichweite_median || 0) + '</b><span>Reichweite (Median)</span></div>' +
        '<div><b>' + (k.reichweite_schnitt || 0) + '</b><span>Schnitt</span></div>' +
        '<div><b>' + (k.gespeichert || 0) + '</b><span>gespeichert</span></div>' +
        '<div><b>' + (k.geteilt || 0) + '</b><span>geteilt</span></div>' +
      '</div>' +
      (b ? '<p class="note" style="margin:6px 0 0">Bester: ' + esc(b.datum) +
           ' · ' + b.reach + ' — ' + esc(b.anfang) + '</p>' : "") +
      (s && b && s.datum !== b.datum
           ? '<p class="note" style="margin:2px 0 0">Schwächster: ' + esc(s.datum) +
             ' · ' + s.reach + ' — ' + esc(s.anfang) + '</p>' : "") +
    '</div>';
  }

  function igBlock() {
    if (!igzahlen || !(igzahlen.konten || []).length) {
      return '<div class="panel" style="margin-bottom:18px">' +
        '<h2>Was Instagram misst</h2>' +
        '<div class="empty">Noch keine Zahlen geholt.<br>' +
        '<code>python scripts/instagram-insights/holen.py</code></div></div>';
    }
    // 🚨 Eine Zahl ohne Datum daneben sieht immer aktuell aus. Ist der Abzug
    // drei Tage oder aelter, muss das ins Auge springen.
    var alt = igzahlen.veraltet;
    return '<div class="panel' + (alt ? " igalt" : "") + '" style="margin-bottom:18px">' +
      '<h2>Was Instagram misst ' +
        '<span class="note">· Stand ' + esc(igzahlen.stand || "?") +
        (igzahlen.alter_tage != null ? " · " + igzahlen.alter_tage + " Tage alt" : "") +
        '</span></h2>' +
      (alt ? '<p class="igwarn">Diese Zahlen sind ' + igzahlen.alter_tage +
             ' Tage alt. Hol sie neu, bevor du danach entscheidest:<br>' +
             '<code>python scripts/instagram-insights/holen.py</code></p>' : "") +
      (igzahlen.konten || []).map(igZeile).join("") +
      '<p class="note" style="margin:10px 0 0">Median statt Schnitt lesen — ' +
      'ein einzelnes starkes Reel zieht den Schnitt hoch.</p>' +
    '</div>';
  }

  function renderZahlen(main) {'''

# --------------------------------------------------------------------------
# 4) Aussehen
# --------------------------------------------------------------------------
ALT_CSS = "  .lzkarte {"
NEU_CSS = """  .igkonto { border-top: 1px solid var(--line); padding: 10px 0; }
  .igkonto:first-of-type { border-top: 0; }
  .igkopf { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
  .igwerte { display: flex; gap: 18px; flex-wrap: wrap; margin-top: 6px; }
  .igwerte > div { display: flex; flex-direction: column; min-width: 92px; }
  .igwerte b { font-size: 22px; line-height: 1.1; }
  .igwerte span { font-size: 12px; color: var(--ink-soft); }
  .panel.igalt { border-color: var(--bad, #b3261e); }
  .igwarn { color: var(--bad, #b3261e); margin: 4px 0 10px; font-size: 14px; }
  .lzkarte {"""

ERSETZUNGEN = [
    ("Speicherplatz", ALT_VAR, NEU_VAR),
    ("Lokal laden", ALT_LS, NEU_LS),
    ("Aus der Datenbank", ALT_SNAP, NEU_SNAP),
    ("Block einhängen", ALT_BLOCK, NEU_BLOCK),
    ("Block bauen", ALT_FUNK, NEU_FUNK),
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
        r = subprocess.run(["node", "--check", pfad],
                           capture_output=True, text=True)
        return "" if r.returncode == 0 else (r.stderr or "").strip()[:600]
    except FileNotFoundError:
        return ""
    finally:
        Path(pfad).unlink(missing_ok=True)


def main():
    nur_pruefen = "--pruefen" in sys.argv
    html = SEITE.read_text(encoding="utf-8")
    vorher = len(html)

    if "function igBlock" in html:
        sys.exit("Der Zahlen-Block ist schon drin — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-20s ersetzt" % name)

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
