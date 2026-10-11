"""Ergaenzt den doTERRA-Rang-Tracker im Cockpit um zwei Bloecke:

  1. "Was ausbezahlt wurde"  — Provisionsverlauf aus dem Back Office
  2. "Der Vormonat im Vergleich" — August-Endstand neben dem laufenden Monat

Quelle der Daten ist das Cockpit-Dokument daten/doterra, Felder `provisionen`
und `vormonat`. Fehlen die Felder, rendert das Cockpit wie bisher — der Patch
ist also gefahrlos, auch wenn das Dokument noch alt ist.

Mehrfaches Laufen schadet nicht: das Skript prueft auf die Markierung und
bricht ab, wenn der Block schon drin ist.

    python scripts/cockpit/patch-doterra-provisionen.py
"""

import pathlib
import sys

COCKPIT = pathlib.Path(__file__).resolve().parents[2] / "outputs" / "cockpit" / "mlb-cockpit.html"

MARKE = "/* doTERRA-Provisionen */"

# Der Anker steht am Ende der Rang-Tracker-Funktion, direkt vor dem Fuss-Text.
ANKER = """    var fuss = document.createElement("p");
    fuss.className = "note";
    fuss.style.marginTop = "14px";
    fuss.textContent = "Stand " + mailDatum(doterra.stand) +"""

BLOCK = """    /* doTERRA-Provisionen */
    if (doterra.provisionen && doterra.provisionen.monate && doterra.provisionen.monate.length) {
      var prov = doterra.provisionen;
      var pk = document.createElement("div");
      pk.className = "panel";
      var ph = '<h2>Was ausbezahlt wurde</h2>' +
        '<div class="tablewrap"><div class="trow head" ' +
        'style="grid-template-columns:130px 140px 1fr">' +
        '<span>Zeitraum</span><span>Auszahlung</span><span>Verdienst</span></div>';
      prov.monate.forEach(function (m) {
        ph += '<div class="trow" style="grid-template-columns:130px 140px 1fr">' +
          '<span>' + esc(m.monat) + '</span>' +
          '<span><strong>' + zahlKurz(m.auszahlung) + '</strong></span>' +
          '<span class="note">' + zahlKurz(m.verdienst) + '</span></div>';
      });
      ph += '</div>';
      if (prov.summe_jan_jul) {
        ph += '<p class="dtsumme">Zusammen bisher <strong>' +
          zahlKurz(prov.summe_jan_jul) + ' ' + esc(prov.waehrung || "CHF") +
          '</strong>.</p>';
      }
      if (prov.sekundaerbonus_2026) {
        ph += '<p class="note">Sekundaerbonus ' +
          zahlKurz(prov.sekundaerbonus_2026.summe_verdienst) +
          ' verdient, davon ausbezahlt ' +
          zahlKurz(prov.sekundaerbonus_2026.ausbezahlt) + ' \\u2014 ' +
          esc(prov.sekundaerbonus_2026.hinweis || "") + '.</p>';
      }
      if (prov.hinweis) {
        ph += '<p class="note">' + esc(prov.hinweis) + '</p>';
      }
      if (prov.quelle) {
        ph += '<p class="note">' + esc(prov.quelle) + '</p>';
      }
      pk.innerHTML = ph;
      main.appendChild(pk);
    }

    if (doterra.vormonat && doterra.vormonat.ich) {
      var vm = doterra.vormonat;
      var vk = document.createElement("div");
      vk.className = "panel";
      var vh = '<h2>Der Vormonat im Vergleich</h2>' +
        '<div class="tablewrap"><div class="trow head" ' +
        'style="grid-template-columns:minmax(190px,1fr) 110px 110px 120px">' +
        '<span>Wer</span><span>Rang</span><span>PV</span><span>OV</span></div>' +
        '<div class="trow" style="grid-template-columns:minmax(190px,1fr) 110px 110px 120px">' +
        '<span><strong>' + esc(vm.ich.name) + '</strong></span>' +
        '<span class="note">' + esc(vm.ich.rang) + '</span>' +
        '<span>' + zahlKurz(vm.ich.pv) + '</span>' +
        '<span><strong>' + zahlKurz(vm.ich.ov) + '</strong></span></div>';
      (vm.beine || []).forEach(function (b) {
        vh += '<div class="trow" style="grid-template-columns:minmax(190px,1fr) 110px 110px 120px">' +
          '<span>' + esc(b.name) + '</span>' +
          '<span class="note">' + esc(b.rang) + '</span>' +
          '<span>' + zahlKurz(b.pv) + '</span>' +
          '<span>' + zahlKurz(b.ov) + '</span></div>';
      });
      vh += '</div>';
      if (vm.notiz) {
        vh += '<p class="note">' + esc(vm.notiz) + '</p>';
      }
      vk.innerHTML = vh;
      main.appendChild(vk);
    }

"""


def main():
    if not COCKPIT.exists():
        sys.exit("Cockpit-Datei nicht gefunden: %s" % COCKPIT)

    text = COCKPIT.read_text(encoding="utf-8")

    if MARKE in text:
        print("Block ist schon drin — nichts zu tun.")
        return

    if text.count(ANKER) != 1:
        sys.exit(
            "Anker %d mal gefunden, erwartet genau 1. "
            "Das Cockpit hat sich geaendert — Anker im Skript nachziehen."
            % text.count(ANKER)
        )

    COCKPIT.with_suffix(".html.vor-provisionen").write_text(text, encoding="utf-8")
    text = text.replace(ANKER, BLOCK + ANKER, 1)
    COCKPIT.write_text(text, encoding="utf-8")
    print("Eingefuegt. Sicherung liegt als mlb-cockpit.html.vor-provisionen daneben.")


if __name__ == "__main__":
    main()
