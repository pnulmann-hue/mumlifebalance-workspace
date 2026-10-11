"""Erweitert „Kundinnen & Leads" um die Notion-Felder und die Kundenstimmen.

Patricia am 24.09.2026: *„auch das mit den kunden soll rein bitte"* · *„auch
testimonials"*.

🚨 **Kein neuer Reiter.** „Kundinnen & Leads" gab es schon — und `daten/leads`
war leer, genau wie vorher bei den Launches. Ein zweiter Reiter haette zwei
Kundenlisten ergeben.

🚨 **Der Reiter war ein Vertriebs-Trichter, die Notion-Liste eine Kundenliste.**
Im Untertitel stand „Ohne nächsten Schritt kein Eintrag" — 30 bestehende
Kundinnen haben keinen naechsten Schritt und waeren als Verstoss gegen die
eigene Regel dagestanden. Deshalb drei neue Spalten (Art, E-Mail, Notiz) und
ein ehrlicher Untertitel: die Liste ist beides, und die Spalte „Art" trennt es.

🚨 **Telefon, Adresse und Geburtstag kommen nicht mit** — in Notion bei allen
34 Eintraegen leer. Eine Spalte zu bauen, die dauerhaft leer aussieht und
trotzdem nach sensiblen Daten verlangt, waere das Schlechteste aus beidem.

🚨 **Kundenstimmen nur, wo sie oeffentlich stehen.** Die vier stammen aus der
MBA-Salespage, die live ist — damit sind sie freigegeben. Alles, wo eine
Freigabe unklar ist, gehoert hier nicht hinein.

Aufruf:
  python scripts/cockpit/patch-kunden.py [--pruefen]
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
# 1) Spalten und Untertitel
# --------------------------------------------------------------------------
ALT_TAB = '''      unter: "Wer sich gemeldet hat, wo sie steht und was dein nächster Schritt ist. Ohne nächsten Schritt kein Eintrag.",
      neu: function () { return { id: uid("l"), name: "", quelle: "Instagram DM", interesse: "", status: "Neu", schritt: "", datum: todayISO() }; },
      cols: [
        { k: "name", l: "Name", t: "text", w: "170px" },
        { k: "quelle", l: "Quelle", t: "select", opts: ["Instagram DM", "ManyChat Keyword", "E-Mail-Liste", "Empfehlung", "Bootcamp", "Sonstiges"], w: "175px" },
        { k: "interesse", l: "Interesse", t: "text", w: "minmax(200px, 1fr)" },
        { k: "status", l: "Status", t: "pill", opts: ["Neu", "Im Gespräch", "Angebot raus", "Kundin", "Kein Interesse"], w: "150px" },
        { k: "schritt", l: "Nächster Schritt", t: "text", w: "minmax(200px, 1fr)" },
        { k: "datum", l: "Am", t: "date", w: "132px" }
      ]'''
NEU_TAB = '''      unter: "Bestehende Kundinnen und alle, die sich gemeldet haben. Bei allem, was noch offen ist, gehört ein nächster Schritt dazu — sonst passiert nichts.",
      neu: function () { return { id: uid("l"), name: "", kategorie: "Kunde", quelle: "Instagram DM", email: "", interesse: "", status: "Neu", schritt: "", notiz: "", datum: todayISO() }; },
      cols: [
        { k: "name", l: "Name", t: "text", w: "170px" },
        { k: "kategorie", l: "Art", t: "select", opts: ["Kunde", "Kooperation", "Dienstleister"], w: "140px" },
        { k: "status", l: "Status", t: "pill", opts: ["Neu", "Im Gespräch", "Angebot raus", "Kundin", "Kein Interesse"], w: "150px" },
        { k: "interesse", l: "Produkt / Interesse", t: "text", w: "minmax(180px, 1fr)" },
        { k: "email", l: "E-Mail", t: "text", w: "190px" },
        { k: "quelle", l: "Quelle", t: "select", opts: ["Instagram DM", "ManyChat Keyword", "E-Mail-Liste", "Empfehlung", "Bootcamp", "Sonstiges"], w: "165px" },
        { k: "schritt", l: "Nächster Schritt", t: "text", w: "minmax(180px, 1fr)" },
        { k: "notiz", l: "Notiz", t: "text", w: "minmax(160px, 1fr)" },
        { k: "datum", l: "Seit", t: "date", w: "132px" }
      ]'''

# --------------------------------------------------------------------------
# 2) Stimmen: Speicherplatz, laden, Block
# --------------------------------------------------------------------------
ALT_VAR = '  var wochenbogen = null;        // daten/wochenbogen — Abgleich'
NEU_VAR = ('  var wochenbogen = null;        // daten/wochenbogen — Abgleich\n'
           '  var stimmen = null;            // daten/stimmen — Kundenstimmen')

ALT_LS = '  wochenbogen = lsGet("wochenbogen", null);'
NEU_LS = ('  wochenbogen = lsGet("wochenbogen", null);\n'
          '  stimmen = lsGet("stimmen", null);')

ALT_SNAP = '''      db.doc("daten/wochenbogen").onSnapshot(function (snap) {'''
NEU_SNAP = '''      db.doc("daten/stimmen").onSnapshot(function (snap) {
        if (!snap.exists) return;
        stimmen = snap.data() || null;
        lsSet("stimmen", stimmen);
        if (activeTab === "leads") render();
      }, function () {});
      db.doc("daten/wochenbogen").onSnapshot(function (snap) {'''

ALT_DISP = '    else renderTable(main, activeTab);'
NEU_DISP = '''    else if (activeTab === "leads") { renderTable(main, "leads"); stimmenBlock(main); }
    else renderTable(main, activeTab);'''

ALT_FUNK = "  function renderWochenbogen(main) {"
NEU_FUNK = '''  /* Kundenstimmen unter der Kundenliste. Kein eigener Reiter — es sind vier.
     🚨 Nur was oeffentlich auf einer Salespage steht. Eine Stimme ohne
     geklaerte Freigabe gehoert nicht in eine Ablage, die man weitergeben kann. */
  function stimmenBlock(main) {
    var liste = (stimmen && stimmen.items) || [];
    if (!liste.length) return;
    var box = document.createElement("div");
    box.className = "panel";
    box.style.marginTop = "22px";
    box.innerHTML = "<h2>Kundenstimmen <span class=\\"note\\">" + liste.length +
      "</span></h2>" +
      '<p class="note">Aus deinen Salespages — die stehen öffentlich, sind also ' +
      'freigegeben. Zum Kopieren für Ads, Mails und neue Seiten.</p>';
    liste.forEach(function (s) {
      var z = document.createElement("div");
      z.className = "stimme";
      z.innerHTML =
        '<p class="stimmetext">„' + esc(s.text) + '"</p>' +
        '<p class="stimmewer">— ' + esc(s.name || "ohne Namen") +
        (s.handle ? ' <span class="note">' + esc(s.handle) + '</span>' : "") +
        '</p>';
      var k = document.createElement("button");
      k.className = "lzkopie";
      k.textContent = "kopieren";
      k.onclick = function () {
        var t = "„" + s.text + "“ — " + (s.name || "") +
                (s.handle ? " " + s.handle : "");
        // 🚨 Kein navigator.clipboard.writeText allein — im Artifact-Rahmen
        // kann es ohne sichtbaren Fehler abgelehnt werden. Deshalb derselbe
        // Weg wie in der Link-Zentrale, mit Rueckfall auf execCommand.
        var ok = false;
        try {
          var ta = document.createElement("textarea");
          ta.value = t;
          ta.style.position = "fixed"; ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          ok = document.execCommand("copy");
          document.body.removeChild(ta);
        } catch (e) {}
        k.textContent = ok ? "kopiert" : "von Hand markieren";
        k.classList.toggle("fertig", ok);
        setTimeout(function () {
          k.textContent = "kopieren"; k.classList.remove("fertig");
        }, 2500);
      };
      z.appendChild(k);
      box.appendChild(z);
    });
    main.appendChild(box);
  }

  function renderWochenbogen(main) {'''

ALT_CSS = "  .wbfokus { font-size: 13px; flex: 1 1 180px; min-width: 0;"
NEU_CSS = """  .stimme {
    border-top: 1px solid var(--line); padding: 11px 0 9px;
    display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: start;
  }
  .panel .stimme:first-of-type { border-top: 0; }
  .stimmetext { margin: 0; font-size: 14px; line-height: 1.55; grid-column: 1; }
  .stimmewer { margin: 4px 0 0; font-size: 13px; color: var(--ink-soft); grid-column: 1; }
  .stimme .lzkopie { grid-row: 1 / 3; grid-column: 2; align-self: center; }
  .wbfokus { font-size: 13px; flex: 1 1 180px; min-width: 0;"""

ERSETZUNGEN = [
    ("Spalten und Untertitel", ALT_TAB, NEU_TAB),
    ("Speicherplatz", ALT_VAR, NEU_VAR),
    ("Lokal laden", ALT_LS, NEU_LS),
    ("Aus der Datenbank", ALT_SNAP, NEU_SNAP),
    ("Stimmen-Block", ALT_FUNK, NEU_FUNK),
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

    if "function stimmenBlock" in html:
        sys.exit("Die Kundenstimmen sind schon drin — nichts zu tun.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-24s ersetzt" % name)

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
