# -*- coding: utf-8 -*-
"""Verlinkt die Seite „Kursproduktion Easy KI" aus dem Cockpit.

Patricia am 19.10.2026: *„aber verlinkung waere schon geil. weil dann kann ich
von meinem cockpit aus direkt rein"*.

Der Knopf steht im Reiter **Produkte -> Launch**, neben dem zur
Funnel-Checkliste. Dort schaut sie waehrend eines Launches ohnehin hin.

🚨 Ein echter Link, kein Knopf mit JavaScript. `window.open()` ist im
   Artifact-Rahmen blockiert, und zwar lautlos (gefunden 16.09.2026).

Wiederholbar: laeuft ein zweites Mal ins Leere.
"""
import pathlib
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
URL = "https://claude.ai/artifact/JYSuhqEdSCja4Gn8V2Xj88"

ALT = ("      '<a class=\"btn\" href=\"https://claude.ai/artifact/YViQzGgPqr3AiufeA35Ev3\" ' +\n"
       "      'target=\"_blank\" rel=\"noopener\">Funnel-Checkliste &rarr;</a></div>' +")
NEU = ("      '<a class=\"btn\" href=\"https://claude.ai/artifact/YViQzGgPqr3AiufeA35Ev3\" ' +\n"
       "      'target=\"_blank\" rel=\"noopener\">Funnel-Checkliste &rarr;</a>' +\n"
       "      '<a class=\"btn\" href=\"" + URL + "\" ' +\n"
       "      'target=\"_blank\" rel=\"noopener\">Kursproduktion KI-Kurs &rarr;</a></div>' +")


def main():
    t = ZIEL.read_text(encoding="utf-8")
    if URL in t:
        sys.exit("\U0001f6a8 schon verlinkt")
    if t.count(ALT) != 1:
        sys.exit("\U0001f6a8 Anker %dx gefunden, erwartet 1x" % t.count(ALT))
    t = t.replace(ALT, NEU)

    skript = t[t.rfind("<script>") + 8:t.rfind("</script>")]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(skript)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("\U0001f6a8 node --check: %s" % (r.stderr or r.stdout))

    ZIEL.write_text(t, encoding="utf-8")
    print("Knopf „Kursproduktion KI-Kurs\u201c steht jetzt im Reiter Produkte \u2192 Launch.")
    print("node --check gruen \u00b7 Links im Launch-Kopf: %d" % t.count('class="btn" href="https://claude.ai/artifact/'))


if __name__ == "__main__":
    main()
