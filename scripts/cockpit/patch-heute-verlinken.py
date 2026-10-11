"""Macht die Zeilen auf «Heute» anklickbar — direkt zum Beitrag.

Patricia am 24.09.2026: *„und ich brauche direkt verlinkungen"*.

Vorher war die Startseite eine Anzeigetafel: Sie sagte, dass fünf Beiträge
warten, aber man musste den Reiter selbst suchen und dort nochmal blättern.

| Zeile in | Klick führt zu |
|---|---|
| Du bist dran | **Planen**, richtige Woche, Platz aufgeklappt |
| Kann raus | **Freigeben** |
| Als Nächstes | **Jahresplan** |

🚨 **Die Woche wird gerechnet, nicht geraten.** `wochenOffset` zählt Wochen ab
der laufenden; wer einen Beitrag vom 6. Oktober anklickt, landet sonst in der
aktuellen Woche und sieht ihn nicht. Gerechnet wird über den **Montag** beider
Wochen — nicht über die Differenz in Tagen geteilt durch sieben, denn die
springt je nach Wochentag um eins daneben.

🚨 **Kein Deep-Link ohne Datum.** Beiträge ohne Datum landen im Reiter, aber
ohne aufgeklappten Platz — sonst klappt ein beliebiger Platz auf, und man hält
den falschen Beitrag für den gesuchten.

    python scripts/cockpit/patch-heute-verlinken.py [--pruefen] [--datei <pfad>]
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

CSS_ALT = '  .jetzt .zeile:last-child { border-bottom: 0; }'
CSS_NEU = r'''  .jetzt .zeile:last-child { border-bottom: 0; }
  /* Anklickbare Zeilen muessen auch danach aussehen. */
  .jetzt .zeile.klick { cursor: pointer; margin: 0 -8px; padding-left: 8px; padding-right: 8px; border-radius: 6px; }
  .jetzt .zeile.klick:hover { background: var(--teal-soft); }
  .jetzt .zeile.klick:hover span { color: var(--ink); }'''

# Der Block, der die Zeilen baut — wird ganz ersetzt.
ALT = r'''    function fuelle(id, zeilen, leertext) {
      var el = main.querySelector(id);
      if (!zeilen.length) { el.innerHTML = '<div class="leer">' + esc(leertext) + '</div>'; return; }
      el.innerHTML = zeilen.slice(0, 6).map(function (z) {
        var w = (z.wann && z.wann !== "—") ? '<span class="wann">' + esc(z.wann) + '</span>' : "";
        return '<div class="zeile">' + w + '<span>' + esc(z.text) + '</span></div>';
      }).join("") + (zeilen.length > 6
        ? '<div class="leer" style="margin-top:8px">und ' + (zeilen.length - 6) + ' weitere</div>' : "");
    }'''

NEU = r'''    /* Wie viele Wochen liegt ein Datum von der laufenden Woche entfernt?
       Ueber den Montag beider Wochen gerechnet - siehe Kopf des
       Patch-Skripts, die Tages-Differenz durch sieben springt daneben. */
    function wochenAbstand(iso) {
      function montag(d) {
        var x = new Date(d + "T00:00:00");
        if (isNaN(x)) return null;
        x.setDate(x.getDate() - ((x.getDay() + 6) % 7));
        x.setHours(0, 0, 0, 0);
        return x;
      }
      var a = montag(todayISO()), b = montag(iso);
      if (!a || !b) return null;
      return Math.round((b - a) / 604800000);
    }

    function springeZuBeitrag(b) {
      var d = (blo(b.obj) || {}).datum || "";
      activeTab = "woche";
      var ab = d ? wochenAbstand(d) : null;
      if (ab !== null) {
        wochenOffset = ab;
        // Ohne Datum kein aufgeklappter Platz - sonst oeffnet sich ein
        // beliebiger und man haelt den falschen Beitrag fuer den gesuchten.
        slotOffen = d + "|" + (typeof kartenProfil === "function"
          ? kartenProfil(b.obj) : "mentoring");
      }
      render();
    }

    function fuelle(id, zeilen, leertext) {
      var el = main.querySelector(id);
      if (!zeilen.length) { el.innerHTML = '<div class="leer">' + esc(leertext) + '</div>'; return; }
      el.innerHTML = "";
      zeilen.slice(0, 6).forEach(function (z) {
        var d = document.createElement("div");
        d.className = "zeile" + (z.gehe ? " klick" : "");
        var w = (z.wann && z.wann !== "—")
          ? '<span class="wann">' + esc(z.wann) + '</span>' : "";
        d.innerHTML = w + "<span>" + esc(z.text) + "</span>";
        if (z.gehe) {
          d.title = z.hinweis || "Hinbringen";
          d.onclick = z.gehe;
        }
        el.appendChild(d);
      });
      if (zeilen.length > 6) {
        var r = document.createElement("div");
        r.className = "leer";
        r.style.marginTop = "8px";
        r.textContent = "und " + (zeilen.length - 6) + " weitere";
        el.appendChild(r);
      }
    }'''

# Die drei Aufrufe bekommen ihr Sprungziel.
RUF_ALT_DU = r'''    fuelle("#ov-du", deins.map(function (e) {
      return { wann: fmtDate(e.datum), text: (e.b.titel || e.b.format) + " — " + e.was };
    }), "Nichts, das auf dich wartet.");'''
RUF_NEU_DU = r'''    fuelle("#ov-du", deins.map(function (e) {
      return { wann: fmtDate(e.datum),
               text: (e.b.titel || e.b.format) + " — " + e.was,
               hinweis: "Öffnet die Woche und klappt den Platz auf",
               gehe: function () { springeZuBeitrag(e.b); } };
    }), "Nichts, das auf dich wartet.");'''

RUF_ALT_RAUS = r'''    fuelle("#ov-raus", raus.map(function (b) {
      return { wann: fmtDate((blo(b.obj) || {}).datum), text: b.titel || b.format };
    }), "Nichts freigabebereit.");'''
RUF_NEU_RAUS = r'''    fuelle("#ov-raus", raus.map(function (b) {
      return { wann: fmtDate((blo(b.obj) || {}).datum), text: b.titel || b.format,
               hinweis: "Zu „Freigeben“",
               gehe: function () { activeTab = "fertig"; render(); } };
    }), "Nichts freigabebereit.");'''

RUF_ALT_NEXT = r'''        .map(function (e) { return { wann: fmtDate(e.start), text: e.name }; });'''
RUF_NEU_NEXT = r'''        .map(function (e) {
          return { wann: fmtDate(e.start), text: e.name,
                   hinweis: "Zum Jahresplan",
                   gehe: function () { activeTab = "launches"; render(); } };
        });'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
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
    nur_pruefen = "--pruefen" in sys.argv
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit-neu.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "springeZuBeitrag" in s:
        print("  Schon verlinkt — nichts zu tun.")
        return

    s = setze(s, CSS_ALT, CSS_NEU, "CSS-Anker")
    s = setze(s, ALT, NEU, "Zeilen-Bau")
    s = setze(s, RUF_ALT_DU, RUF_NEU_DU, "Du bist dran")
    s = setze(s, RUF_ALT_RAUS, RUF_NEU_RAUS, "Kann raus")
    s = setze(s, RUF_ALT_NEXT, RUF_NEU_NEXT, "Als Nächstes")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Zeilen verlinkt · %d KB" % (len(s) / 1024))


if __name__ == "__main__":
    main()
