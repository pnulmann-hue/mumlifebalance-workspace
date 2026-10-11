"""
Einen Reiter „Listen & Automationen" ins Cockpit einbauen.

Bisher stand im Cockpit nur, was Patricia von Hand eingetragen hat. Die
E-Mail-Seite des Business — welche Listen es gibt, wie viele Leute drauf
sind, welche Automationen laufen — lag ausschliesslich in ActiveCampaign.

Der Reiter zeigt genau das, und zwar als Abbild: geschrieben wird hier
nichts, die Daten kommen aus `scripts/cockpit/daten-abgleich.py`. Deshalb
sind die Felder nicht editierbar — was man hier aendern wuerde, waere beim
naechsten Abgleich wieder weg.

Aufruf:
  python scripts/cockpit/patch-mailings-tab.py [--pruefen]
"""
import io
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ERSETZUNGEN = []


def patch(name, alt, neu):
    ERSETZUNGEN.append((name, alt, neu))


# --------------------------------------------------------------------------
# 1 · Ablage fuer die Daten
# --------------------------------------------------------------------------
patch("Speicher fuer Listen und Automationen",
      '  var DOC_KEYS = ["posts", "ideen", "leads", "team", "produkte", "funnel", "launches", "zahlen"];',
      '  var DOC_KEYS = ["posts", "ideen", "leads", "team", "produkte", "funnel", "launches", "zahlen"];\n'
      '  /* Kommt aus ActiveCampaign und wird nur angezeigt, nie hier bearbeitet. */\n'
      '  var mailings = { listen: [], automationen: [], stand: "" };')

# --------------------------------------------------------------------------
# 2 · Stufen der Produktleiter: die echten Namen zulassen
# --------------------------------------------------------------------------
patch("Stufen an die echte Produktleiter angleichen",
      '{ k: "stufe", l: "Stufe", t: "select", opts: ["Freebie", "Mini-Kurs", "Signature-Kurs", "1:1", "Öle"], w: "155px" },',
      '{ k: "stufe", l: "Stufe", t: "select", opts: ["Freebie", "Mini-Kurs", "Kurs", "Signature-Kurs", "Programm", "1:1", "Öle", "Angebot"], w: "155px" },')

# --------------------------------------------------------------------------
# 3 · Reiter
# --------------------------------------------------------------------------
patch("Reiter in die Navigation",
      '    { id: "funnel", label: "Funnel & Keywords" },',
      '    { id: "funnel", label: "Funnel & Keywords" },\n'
      '    { id: "mailings", label: "Listen & Automationen" },')

patch("Reiter an den Render-Dispatcher",
      '    else if (activeTab === "funnel") renderFunnel(main);',
      '    else if (activeTab === "funnel") renderFunnel(main);\n'
      '    else if (activeTab === "mailings") renderMailings(main);')

# --------------------------------------------------------------------------
# 4 · Die Ansicht
# --------------------------------------------------------------------------
patch("Ansicht Listen und Automationen",
      """  /* =========================================================
     Launches
     ========================================================= */""",
      """  /* =========================================================
     Listen & Automationen — Abbild aus ActiveCampaign
     ========================================================= */
  /* fmtDate laesst das Jahr weg — hier stehen Listen von 2023, da muss es mit. */
  function mailDatum(iso) {
    if (!iso) return "—";
    var p = String(iso).split("-");
    return p.length === 3 ? p[2] + "." + p[1] + "." + p[0] : iso;
  }

  function mailTabelle(titel, spalten, reihen, leer) {
    var breiten = spalten.map(function (s) { return s.w; }).join(" ");
    var h = '<h2>' + esc(titel) + '</h2>';
    if (!reihen.length) return '<div class="panel">' + h + '<div class="empty">' + esc(leer) + '</div></div>';
    h += '<div class="tablewrap"><div class="trow head" style="grid-template-columns:' + breiten + '">' +
         spalten.map(function (s) { return '<span>' + esc(s.l) + '</span>'; }).join("") + '</div>';
    reihen.forEach(function (r) {
      h += '<div class="trow" style="grid-template-columns:' + breiten + '">' +
           spalten.map(function (s) { return '<span>' + (s.f ? s.f(r) : esc(r[s.k] == null ? "" : String(r[s.k]))) + '</span>'; }).join("") +
           '</div>';
    });
    return '<div class="panel" style="margin-bottom:18px">' + h + '</div></div>';
  }

  function renderMailings(main) {
    var listen = mailings.listen || [];
    var autos = mailings.automationen || [];
    var kontakte = listen.reduce(function (s, l) { return s + (parseInt(l.kontakte, 10) || 0); }, 0);
    var aktiv = autos.filter(function (a) { return a.status === "aktiv"; }).length;
    var leere = listen.filter(function (l) { return !parseInt(l.kontakte, 10); }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Listen & Automationen</h1>' +
      '<p>So sieht deine E-Mail-Seite gerade aus. Die Zahlen kommen direkt aus ActiveCampaign und werden beim täglichen Abgleich neu geholt — hier wird nichts eingetragen.</p></div></div>' +
      '<div class="tiles">' +
      tile("Kontakte", kontakte, "auf allen Listen zusammen") +
      tile("Listen", listen.length, leere ? leere + " davon noch leer" : "alle mit Kontakten") +
      tile("Automationen", autos.length, aktiv + " laufen") +
      '</div>' +
      '<div id="mailbody"></div>' +
      '<p class="note" style="margin-top:14px">' +
      (mailings.stand ? "Stand: " + esc(mailDatum(mailings.stand)) : "Noch kein Abgleich gelaufen.") +
      '</p>';

    main.querySelector("#mailbody").innerHTML =
      mailTabelle("Deine Listen",
        [{ k: "name", l: "Liste", w: "minmax(240px, 1fr)" },
         { k: "kontakte", l: "Kontakte", w: "110px" },
         { k: "nummer", l: "Nr.", w: "70px" },
         { k: "seit", l: "Angelegt", w: "130px", f: function (r) { return esc(mailDatum(r.seit)); } }],
        listen, "Noch nichts abgeglichen.") +
      mailTabelle("Deine Automationen",
        [{ k: "name", l: "Automation", w: "minmax(280px, 1fr)" },
         { k: "status", l: "Status", w: "110px",
           f: function (r) { return '<span class="flag ' + (r.status === "aktiv" ? "ok" : "bad") + '">' + esc(r.status) + '</span>'; } },
         { k: "nummer", l: "Nr.", w: "70px" },
         { k: "seit", l: "Gebaut", w: "130px", f: function (r) { return esc(mailDatum(r.seit)); } }],
        autos, "Noch nichts abgeglichen.");
  }

  /* =========================================================
     Launches
     ========================================================= */""")

# --------------------------------------------------------------------------
# 5 · Daten laden
# --------------------------------------------------------------------------
patch("Listen und Automationen aus der Datenbank holen",
      """      db.doc("daten/einstellungen").onSnapshot(function (snap) {""",
      """      db.doc("daten/mailings").onSnapshot(function (snap) {
        if (!snap.exists) return;
        var d0 = snap.data() || {};
        mailings = { listen: d0.listen || [], automationen: d0.automationen || [],
                     stand: d0.stand || "" };
        lsSet("mailings", mailings);
        if (activeTab === "mailings") render();
      }, function () {});
      db.doc("daten/einstellungen").onSnapshot(function (snap) {""")

patch("Beim Start den letzten Stand zeigen",
      '  Object.assign(settings, lsGet("einstellungen", {}) || {});',
      '  Object.assign(settings, lsGet("einstellungen", {}) || {});\n'
      '  Object.assign(mailings, lsGet("mailings", {}) || {});')


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:140]))
        if s.count(alt) > 1:
            sys.exit("Anker mehrdeutig (%dx) fuer: %s" % (s.count(alt), name))
        s = s.replace(alt, neu, 1)
        print("  OK  %s" % name)
    print("\nLaenge %d -> %d (%+d)" % (vorher, len(s), len(s) - vorher))
    if nur_pruefen:
        print("PRUEFLAUF — nichts geschrieben.")
        return
    io.open(DATEI, "w", encoding="utf-8").write(s)
    print("Geschrieben: %s" % DATEI)


if __name__ == "__main__":
    main()
