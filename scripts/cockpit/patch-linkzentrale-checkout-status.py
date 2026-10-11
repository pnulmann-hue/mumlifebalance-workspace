"""
Die Link-Zentrale zeigt, ob eine Kasse ueberhaupt Geld nimmt.

Patricia am 16.09.2026: *„du siehst auf thrivecart welche angebote gerade online
sind oder entwürfe oder einfach deaktiviert."* Genau — und bis jetzt stand das
nirgends. ThriveCart fuehrt drei Zustaende:

| Zustand | Was der Checkout tut |
|---|---|
| `live` | nimmt echtes Geld |
| `test` | zeigt die Seite, bucht aber **nichts** ab |
| `disabled` | ist abgeschaltet |

🚨 **Der Anlass war ein echter Fehler.** „Dein starkes Mama-Business" (777) steht
auf `test` und ist trotzdem von der Angebots-Seite verlinkt. Wer dort kauft,
bezahlt nichts — und niemand merkt es, weil die Seite normal aussieht.

Deshalb bekommt jede Karte mit `tc_status != "live"` eine rote Fahne neben dem
Preis und einen Satz darunter, der sagt, was das heisst. Der Wert kommt aus
`katalog.json` (Feld `status`) und wird **nie von Hand gepflegt** — sobald
Patricia in ThriveCart umstellt, zieht der naechste Abgleich nach.

Dazu eine Kachel oben: wie viele der verlinkten Kassen wirklich laufen.

Aufruf:
  python scripts/cockpit/patch-linkzentrale-checkout-status.py [--pruefen]
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
# 1) Fahne im Kartenkopf.
# --------------------------------------------------------------------------
ALT_KOPF = """            (e.status === "achtung"
              ? '<span class="flag bad">prüfen</span>' : "");
          karte.appendChild(kopf);"""

NEU_KOPF = """            (e.status === "achtung"
              ? '<span class="flag bad">prüfen</span>' : "") +
            // ThriveCart-Zustand: „test" bucht nichts ab, „disabled" ist aus.
            (e.tc_status && e.tc_status !== "live"
              ? '<span class="flag bad">' +
                (e.tc_status === "test" ? "Testmodus" : "abgeschaltet") +
                '</span>' : "");
          karte.appendChild(kopf);

          if (e.tc_status && e.tc_status !== "live") {
            var warn = document.createElement("p");
            warn.className = "note";
            warn.style.margin = "2px 0 6px";
            warn.style.color = "var(--bad, #b3261e)";
            warn.textContent = e.tc_status === "test"
              ? "Die Kasse steht in ThriveCart auf Testmodus — sie zeigt die "
                + "Seite, bucht aber nichts ab. Nicht verlinken, solange das so ist."
              : "Dieser Checkout ist in ThriveCart abgeschaltet.";
            karte.appendChild(warn);
          }"""

# --------------------------------------------------------------------------
# 2) Kachel: laufen die verlinkten Kassen ueberhaupt?
# --------------------------------------------------------------------------
ALT_ZAEHLER = """    var tot = alle.filter(function (e) { return e.status === "tot"; }).length;"""
NEU_ZAEHLER = """    var tot = alle.filter(function (e) { return e.status === "tot"; }).length;
    var kassen = alle.filter(function (e) { return e.tc_status; });
    var kassenTot = kassen.filter(function (e) {
      return e.tc_status !== "live";
    }).length;"""

ALT_KACHEL = """      tile("Tot", tot, tot ? "nicht verlinken!" : "keiner tot") +"""
NEU_KACHEL = """      tile("Tot", tot, tot ? "nicht verlinken!" : "keiner tot") +
      tile("Kassen offen", kassen.length - kassenTot,
           kassenTot ? kassenTot + " nehmen kein echtes Geld"
                     : "alle verlinkten Kassen laufen") +"""

ERSETZUNGEN = [
    ("Fahne + Warnsatz", ALT_KOPF, NEU_KOPF),
    ("Zähler", ALT_ZAEHLER, NEU_ZAEHLER),
    ("Kachel", ALT_KACHEL, NEU_KACHEL),
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

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-18s ersetzt" % name)

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
