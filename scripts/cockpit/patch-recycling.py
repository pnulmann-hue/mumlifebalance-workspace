"""Zeigt im Reiter „Gepostet & Analyse", was sich wiederverwenden laesst.

Patricia am 24.09.2026: *„es geht ja irgendwann auch darum, dass wir recyceln
können und nicht immer alles neu produzieren müssen"*.

Ein Beitrag taugt zum Wiederverwenden, wenn er **ueberdurchschnittlich** lief
und **lange genug** her ist. Beide Schwellen stehen in `gepostet-bauen.py` und
reisen mit den Daten mit — nicht hier im Seitencode, sonst muessten sie an zwei
Stellen gepflegt werden.

🚨 **Gemessen wird gegen den eigenen Median, nicht gegen eine feste Zahl.** Bei
rund 2'000 gegen rund 60 Follower waere jede absolute Schwelle fuer eines der
beiden Profile sinnlos: auf dem doTERRA-Konto waere nie etwas „gut", auf dem
Mentoring-Konto fast alles.

🚨 **Erst ab sieben Tagen zaehlt ein Beitrag mit.** Die Zahlen wachsen die
ersten Tage noch. Wer am Tag nach dem Posten bewertet, bewertet den Start.
Deshalb bleiben junge Beitraege aus dem Median **und** aus der Kandidatenliste
draussen — sie stehen in der Liste, aber ohne Urteil.

Der Knopf legt den Beitrag als Idee in den Vorrat. Von dort geht er den
normalen Weg ueber die Wochen-Vorschau — **nichts wird automatisch neu
eingeplant**, das bleibt ihr Klick.

Aufruf:
  python scripts/cockpit/patch-recycling.py [--pruefen]
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
# 1) Der Block + der Knopf
# --------------------------------------------------------------------------
ALT_FUNK = "  function renderGepostet(main) {"
NEU_FUNK = '''  /* Einen gelaufenen Beitrag zurueck in die Planung holen.
     🚨 Nur in den Ideenvorrat — nie direkt auf einen Wochenplatz. Was wann
     rausgeht, bleibt Patricias Entscheidung. */
  function recycelnAlsIdee(b, knopf) {
    var text = (b.hook || b.anfang || "").slice(0, 200);
    state.ideen.unshift({
      id: uid("i"),
      typ: "Recycling",
      saeule: (gepostetNotizen[b.id] || {}).saeule || SAEULEN[0],
      text: text,
      quelle: "lief am " + b.datum + " gut (" + b.reach + " Reichweite" +
              (b.rate != null ? ", " + b.rate + " %" : "") + ")",
      status: "Offen"
    });
    saveList("ideen");
    if (!gepostetNotizen[b.id]) gepostetNotizen[b.id] = {};
    gepostetNotizen[b.id].recycelt = todayISO();
    notizSpeichern();
    knopf.disabled = true;
    knopf.textContent = "in der Ideenliste";
    toast("In den Ideenvorrat gelegt. Einplanen machst du in der Wochen-Vorschau.");
  }

  function gpRecyclingBlock(liste) {
    var r = (gepostet && gepostet.regeln) || {};
    var kandidaten = liste.filter(function (b) {
      return b.recycling && !(gepostetNotizen[b.id] || {}).recycelt;
    }).sort(function (x, y) { return (y.reach || 0) - (x.reach || 0); });

    var box = document.createElement("div");
    box.className = "panel gprec";
    box.style.marginBottom = "18px";

    if (!kandidaten.length) {
      box.innerHTML = "<h2>Kann wieder raus</h2>" +
        '<div class="empty">Gerade nichts. Ein Beitrag kommt hier rein, wenn er ' +
        'überdurchschnittlich lief und mindestens ' + (r.recycling_ab_tagen || 28) +
        ' Tage her ist.</div>';
      return box;
    }

    box.innerHTML = "<h2>Kann wieder raus <span class=\\"gpzahl\\">" +
      kandidaten.length + "</span></h2>" +
      '<p class="note">Lief besser als dein Schnitt und ist mindestens ' +
      (r.recycling_ab_tagen || 28) + ' Tage her. Der Knopf legt es in den ' +
      'Ideenvorrat — eingeplant wird es wie immer in der Wochen-Vorschau.</p>';

    kandidaten.slice(0, 8).forEach(function (b) {
      var z = document.createElement("div");
      z.className = "gpreczeile";
      z.innerHTML =
        '<span class="gpdatum">' + esc(b.datum) + '</span>' +
        '<span class="gpalter">vor ' + b.alter_tage + ' Tagen</span>' +
        '<span class="gptext">' + esc(b.hook || b.anfang || "") + '</span>' +
        '<span class="gpreach">' + (b.reach || 0).toLocaleString("de-CH") + '</span>';
      var k = document.createElement("button");
      k.className = "btn";
      k.textContent = "Nochmal bringen";
      k.onclick = function () { recycelnAlsIdee(b, k); };
      z.appendChild(k);
      box.appendChild(z);
    });

    if (kandidaten.length > 8) {
      var m = document.createElement("p");
      m.className = "note";
      m.style.marginTop = "8px";
      m.textContent = "und " + (kandidaten.length - 8) + " weitere weiter unten in der Liste.";
      box.appendChild(m);
    }
    return box;
  }

  function renderGepostet(main) {'''

# --------------------------------------------------------------------------
# 2) Block einhaengen + Kachel
# --------------------------------------------------------------------------
ALT_EIN = '''    var box = main.querySelector("#gpliste");
    liste.forEach(function (b) { box.appendChild(gpKarte(b)); });'''
NEU_EIN = '''    var recBox = gpRecyclingBlock(liste);
    var listenPanel = main.querySelector("#gpliste").parentNode;
    listenPanel.parentNode.insertBefore(recBox, listenPanel);

    var box = main.querySelector("#gpliste");
    liste.forEach(function (b) { box.appendChild(gpKarte(b)); });'''

ALT_KACHEL = '''      tile("Eingeordnet", eingeordnet + " von " + liste.length, "mit Säule oder Fazit") +'''
NEU_KACHEL = '''      tile("Kann wieder raus",
           liste.filter(function (b) {
             return b.recycling && !(gepostetNotizen[b.id] || {}).recycelt;
           }).length,
           "überdurchschnittlich gelaufen") +
      tile("Eingeordnet", eingeordnet + " von " + liste.length, "mit Säule oder Fazit") +'''

# --------------------------------------------------------------------------
# 3) Marker auf der Karte
# --------------------------------------------------------------------------
ALT_KOPF = '''      '<span class="gprate ' + rateTon(b.rate) + '">' +'''
NEU_KOPF = '''      (b.gut_gelaufen ? '<span class="gpstern" title="lief besser als dein Schnitt">★</span>' : "") +
      (b.reif === false ? '<span class="gpjung" title="noch keine sieben Tage — die Zahlen wachsen noch">jung</span>' : "") +
      '<span class="gprate ' + rateTon(b.rate) + '">' +'''

# --------------------------------------------------------------------------
# 4) Aussehen
# --------------------------------------------------------------------------
ALT_CSS = "  .gpkopfzeile, .gpkopf {"
NEU_CSS = """  .gprec { border-left: 3px solid var(--teal); }
  .gpzahl {
    font-size: 12px; background: var(--teal); color: #fbf8f1;
    border-radius: 999px; padding: 1px 9px; vertical-align: middle;
    margin-left: 6px;
  }
  .gpreczeile {
    display: grid; grid-template-columns: 88px 96px 1fr 76px auto;
    gap: 10px; align-items: center; padding: 8px 0;
    border-top: 1px solid var(--line);
  }
  .gpreczeile .btn { font-size: 12px; padding: 5px 11px; }
  .gpalter { font-size: 12px; color: var(--ink-soft); }
  .gpstern { color: var(--warn); font-size: 14px; }
  .gpjung {
    font-size: 10px; letter-spacing: 0.05em; color: var(--ink-soft);
    background: var(--surface-2); border-radius: 999px; padding: 1px 7px;
  }
  @media (max-width: 720px) {
    .gpreczeile { grid-template-columns: 1fr auto; }
    .gpreczeile .gpalter, .gpreczeile .gpreach { display: none; }
    .gpreczeile .gptext { grid-column: 1 / -1; white-space: normal; }
  }
  .gpkopfzeile, .gpkopf {"""

ERSETZUNGEN = [
    ("Block und Knopf", ALT_FUNK, NEU_FUNK),
    ("Block einhängen", ALT_EIN, NEU_EIN),
    ("Kachel", ALT_KACHEL, NEU_KACHEL),
    ("Marker auf der Karte", ALT_KOPF, NEU_KOPF),
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

    if "function gpRecyclingBlock" in html:
        sys.exit("Der Recycling-Block ist schon drin — nichts zu tun.")
    if "function renderGepostet" not in html:
        sys.exit("ABBRUCH — erst `patch-gepostet.py` laufen lassen.")

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
