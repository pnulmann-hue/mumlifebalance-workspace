# -*- coding: utf-8 -*-
"""Unterscheidet im Cockpit Entwürfe von Live-Mails.

    python scripts/cockpit/patch-entwurf-quelle.py

Bis heute stand über jeder Mail-Karte derselbe Satz:

    „Neue Fassung von mir, noch nicht in ActiveCampaign. Schau dir die Vorschau
     an, kopier das HTML und setz es in der Automation ein."

Das stimmte für die Magnet-Ich-Mails, die als Entwurf gebaut und dann von Hand
eingesetzt werden. Für die Launch-Mails stimmt es nicht: die sind **aus**
ActiveCampaign geholt und stehen dort längst. Wer den Satz befolgt, baut etwas
ein, was schon drin ist.

Deshalb entscheidet jetzt das Feld `quelle` am Dokument, was dasteht:
    quelle = "activecampaign"  → „So steht sie heute in ActiveCampaign."
    sonst (Entwurf)            → der alte Satz

🚨 Wiederholbar. Prüft vorher mit assert, dass der Suchtext genau einmal
   vorkommt, und danach mit `node --check`, dass das eingebettete Skript noch
   läuft — ein kaputtes Anführungszeichen legt die ganze Seite lahm.
"""
import io
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ALT = ('''    return '<div class="mentwuerfe"><p class="note">Neue Fassung von mir, noch nicht in ' +
      'ActiveCampaign. Schau dir die Vorschau an, kopier das HTML und setz es in der ' +
      'Automation ein.</p>' +''')

NEU = ('''    /* Entwurf oder Live-Stand? Das Feld `quelle` entscheidet, was dasteht —
       die Launch-Mails kommen AUS ActiveCampaign, die Magnet-Ich-Mails gehen
       erst hinein. Derselbe Satz für beide wäre für eine der beiden falsch. */
    var ausAC = neu.every(function (e) { return e.quelle === "activecampaign"; });
    return '<div class="mentwuerfe"><p class="note">' +
      (ausAC
        ? 'So stehen diese Mails heute in ActiveCampaign. Vorschau anschauen, '
          + 'HTML kopieren, wenn du sie woanders brauchst.'
        : 'Neue Fassung von mir, noch nicht in ActiveCampaign. Schau dir die '
          + 'Vorschau an, kopier das HTML und setz es in der Automation ein.') +
      '</p>' +''')

# Der Schlusssatz unter den Entwürfen passt dann auch nicht mehr
ALT2 = """      '<p class="note" style="margin-top:16px">Und das steckt heute in ActiveCampaign:</p></div>' +"""
NEU2 = ("""      (ausAC ? '</div>'
             : '<p class="note" style="margin-top:16px">Und das steckt heute in """
        """ActiveCampaign:</p></div>') +""")


def main():
    t = io.open(SEITE, encoding="utf-8").read()
    for alt, neu, name in ((ALT, NEU, "Einleitungssatz"), (ALT2, NEU2, "Schlusssatz")):
        n = t.count(alt)
        assert n == 1, "%s: Suchtext kommt %dx vor (erwartet 1)" % (name, n)
        t = t.replace(alt, neu)
        print("  ✓ %s" % name)

    # Gegenprobe: das eingebettete Skript muss noch laufen
    i = t.find("<script")
    j = t.rfind("</script>")
    js = t[t.find(">", i) + 1:j]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js); pfad = f.name
    r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
    if r.returncode:
        print("🚨 node --check: %s" % r.stderr[:300]); sys.exit(1)
    print("  ✓ node --check")

    io.open(SEITE, "w", encoding="utf-8", newline="\n").write(t)
    print("\nGeschrieben: %s" % SEITE.relative_to(ROOT))
    print("Danach: Artifact publish mit dieser Datei.")


if __name__ == "__main__":
    main()
