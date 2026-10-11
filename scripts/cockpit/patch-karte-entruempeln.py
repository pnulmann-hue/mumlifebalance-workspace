"""Die Wochenkarte zeigt, was man beim Durchgehen braucht — der Rest liegt hinter «⋯».

Zweiter Teil von Patricias *„vor allem die wochenvorschau der beiträge. weil da
einfach alles durcheinander kommt"* (24.09.2026).

**Gemessen an einer einzigen Karte** (lokale Testfassung):

| | |
|---|---:|
| Höhe | 572 px |
| sichtbare Knöpfe | **13** |
| Eingabefelder | **14** |

Bei zehn Plätzen sind das **130 Knöpfe und 140 Felder auf einer Seite**. Nicht
die Zahl der Beiträge macht die Seite unübersichtlich, sondern die Zahl der
Bedienelemente je Beitrag.

🚨 **Die Frage ist nicht «was kann man hier tun», sondern «was tut man hier
jedes Mal».** Beim Durchgehen einer Woche schaut man das Cover an, liest den
Hook, prüft Tag und Profil und gibt frei. *Abgelehnt · Anderes Datum · Löschen ·
Hab ich selbst gepostet · Im Bild-Editor bauen* sind Ausnahmen — jede davon
kommt vielleicht einmal pro Woche vor, und jede kostet auf jeder der zehn Karten
Platz und Aufmerksamkeit.

| bleibt offen | liegt hinter «⋯» |
|---|---|
| Datum · Zeit · Profil | Im Bild-Editor bauen |
| **Freigeben** | Hab ich selbst gepostet |
| Caption kopieren | Abgelehnt · Anderes Datum · Löschen |

🚨 **Die Knöpfe bleiben im DOM, sie werden nur eingeklappt.** Die Ereignisse
werden weiter unten über `karte.querySelector(".wk-ablehnen")` angebunden —
wer die Knöpfe stattdessen erst beim Aufklappen erzeugt, bricht jede dieser
Anbindungen, und zwar lautlos.

    python scripts/cockpit/patch-karte-entruempeln.py [--pruefen] [--datei <pfad>]
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

ALT = """          '<button class="btn wk-kopieren">Caption kopieren</button>' +
          '<a class="btn wk-editorlink" href="' + BILDEDITOR +
            '" target="_blank" rel="noopener">Im Bild-Editor bauen</a>' +
          '<button class="btn wk-frei' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +
          // Nach einem Handy-Post muss der Beitrag aus dem Einplan-Lauf raus,
          // sonst steht er zweimal im Feed.
          (b.obj.textfrei && b.art !== "storys"
            ? '<button class="btn wk-selbst">Hab ich selbst gepostet</button>'
            : "") +
          '<button class="btn wk-ablehnen">Abgelehnt</button>' +
          // Anderes Datum: das Feld links setzt den Tag auch, aber wer einen
          // Beitrag verschiebt, will danach wissen, dass die Freigabe weg ist.
          // Das sagt nur dieser Weg.
          '<button class="btn wk-umplan">Anderes Datum</button>' +
          '<span class="wk-umplanbox" hidden>' +
            '<input type="date" class="wk-neudatum" value="' + esc(b.obj.datum || "") + '">' +
            '<button class="btn primary wk-neuok">\\u00dcbernehmen</button>' +
          '</span>' +
          // 🚨 Zwei Klicks statt confirm(): ein Artifact-Rahmen darf Modals
          // blockieren, und ein lautlos wirkungsloser Loeschknopf waere
          // schlimmer als keiner.
          '<button class="btn wk-loeschen">L\\u00f6schen</button>' +
        '</div>' +"""

NEU = """          '<button class="btn wk-kopieren">Caption kopieren</button>' +
          '<button class="btn wk-frei' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +
          /* Alles ab hier ist Ausnahme, nicht Alltag - siehe Kopf von
             patch-karte-entruempeln.py. Die Knoepfe bleiben im DOM, damit die
             Anbindung weiter unten sie findet; sie sind nur eingeklappt. */
          '<details class="wk-mehr"><summary title="Mehr Aktionen">\\u22ef</summary>' +
            '<div class="wk-mehrbox">' +
              '<a class="btn wk-editorlink" href="' + BILDEDITOR +
                '" target="_blank" rel="noopener">Im Bild-Editor bauen</a>' +
              // Nach einem Handy-Post muss der Beitrag aus dem Einplan-Lauf raus,
              // sonst steht er zweimal im Feed.
              (b.obj.textfrei && b.art !== "storys"
                ? '<button class="btn wk-selbst">Hab ich selbst gepostet</button>'
                : "") +
              // Anderes Datum: das Feld links setzt den Tag auch, aber wer einen
              // Beitrag verschiebt, will danach wissen, dass die Freigabe weg ist.
              // Das sagt nur dieser Weg.
              '<button class="btn wk-umplan">Anderes Datum</button>' +
              '<span class="wk-umplanbox" hidden>' +
                '<input type="date" class="wk-neudatum" value="' + esc(b.obj.datum || "") + '">' +
                '<button class="btn primary wk-neuok">\\u00dcbernehmen</button>' +
              '</span>' +
              '<button class="btn wk-ablehnen">Abgelehnt</button>' +
              // 🚨 Zwei Klicks statt confirm(): ein Artifact-Rahmen darf Modals
              // blockieren, und ein lautlos wirkungsloser Loeschknopf waere
              // schlimmer als keiner.
              '<button class="btn wk-loeschen">L\\u00f6schen</button>' +
            '</div>' +
          '</details>' +
        '</div>' +"""

CSS_ALT = "  .wk-fuss { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }"
CSS_NEU = r'''  .wk-fuss { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  /* Die Ausnahme-Aktionen hinter einem Punkt-Knopf (24.09.2026). */
  .wk-mehr { position: relative; margin-left: auto; }
  .wk-mehr > summary {
    list-style: none; cursor: pointer; user-select: none;
    border: 1px solid var(--line); border-radius: 8px;
    padding: 6px 12px; line-height: 1; font-size: 15px;
    color: var(--ink-soft); background: var(--surface);
  }
  .wk-mehr > summary::-webkit-details-marker { display: none; }
  .wk-mehr > summary:hover { background: var(--surface-2); color: var(--ink); }
  .wk-mehr[open] > summary { background: var(--surface-2); color: var(--ink); }
  .wk-mehrbox {
    position: absolute; right: 0; top: calc(100% + 6px); z-index: 30;
    display: flex; flex-direction: column; gap: 6px; align-items: stretch;
    min-width: 200px; padding: 8px;
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 10px; box-shadow: var(--shadow);
  }
  .wk-mehrbox .btn { text-align: left; white-space: nowrap; }
  .wk-mehrbox .wk-umplanbox { display: flex; gap: 6px; }'''


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
    if "wk-mehrbox" in s:
        print("  Schon entrümpelt — nichts zu tun.")
        return

    s = setze(s, ALT, NEU, "Fusszeile")
    s = setze(s, CSS_ALT, CSS_NEU, "CSS")

    # Gegenprobe: jede Knopf-Klasse muss noch genau so oft vorkommen wie vorher.
    for kl in ["wk-ablehnen", "wk-loeschen", "wk-umplan", "wk-neuok",
               "wk-selbst", "wk-editorlink", "wk-frei", "wk-kopieren"]:
        if ('"' + kl) not in s and ("." + kl) not in s:
            sys.exit("🚨 Knopf-Klasse %s ist verschwunden — die Anbindung "
                     "weiter unten liefe ins Leere." % kl)

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Karte entrümpelt · %d KB" % (len(s) / 1024))
    print("  Offen: Datum · Zeit · Profil · Caption kopieren · Freigeben.")
    print("  Hinter «⋯»: Bild-Editor · selbst gepostet · Datum · Abgelehnt · Löschen.")


if __name__ == "__main__":
    main()
