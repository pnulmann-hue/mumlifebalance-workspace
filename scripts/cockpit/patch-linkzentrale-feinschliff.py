"""
Drei Dinge, die die Sichtpruefung der Link-Zentrale gefunden hat (16.09.2026).

1) **Die Auslieferungs-Adresse war unlesbar.** Ein hinterlegtes PDF steht als
   `claude.ai/code/artifact/eeee48d5-…/_blob/45f60d98…` in der Zeile — 95
   Zeichen, die auf dem Handy drei Zeilen fuellen und nichts sagen. Jetzt steht
   dort der Dateiname („Workbook: Von 0 auf echt · 25 Seiten"), **kopiert wird
   weiterhin die volle Adresse**. Anzeige und Inhalt duerfen auseinandergehen,
   solange das Kopieren stimmt — genau deswegen gibt es den Knopf.

2) **Die Datei-Zeile doppelte die Auslieferung.** Beides zeigte dasselbe PDF,
   einmal als Link zum Antippen, einmal als Adresse zum Kopieren. Jetzt faellt
   die Datei-Zeile weg, wenn dieselbe Adresse schon als Auslieferung dasteht.

3) **„Stichwort: fehlt" hatte einen Kopier-Knopf.** In der Uebersicht steht bei
   der Mini-Notfallapotheke „🔴 fehlt" — das ist eine Luecke, kein Stichwort.
   Wer da auf kopieren tippt, hat das Wort „fehlt" in der Zwischenablage.
   Jetzt wird es als Luecke gezeigt, ohne Knopf.

🚨 Anker-Pruefung wie immer: fehlt oder doppelt sich eine Fundstelle, bricht das
Skript ab. Danach prueft Node die Syntax.

Aufruf:
  python scripts/cockpit/patch-linkzentrale-feinschliff.py [--pruefen]
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
# 1) kopierZeile bekommt einen optionalen Anzeigetext.
# --------------------------------------------------------------------------
ALT_ZEILE = """  function kopierZeile(lab, wert, istLink) {"""
NEU_ZEILE = """  function kopierZeile(lab, wert, istLink, anzeige) {"""

ALT_TEXT = """      a.textContent = wert.replace(/^https?:\\/\\//, "");"""
NEU_TEXT = """      // Anzeige und kopierter Wert duerfen auseinandergehen: eine
      // Blob-Adresse ist 95 Zeichen lang und sagt nichts.
      a.textContent = anzeige || wert.replace(/^https?:\\/\\//, "");"""

# --------------------------------------------------------------------------
# 2) Beim Zeichnen: Dateiname als Anzeige, Doppelung merken.
# --------------------------------------------------------------------------
ALT_SCHLEIFE = """          var hatWas = false;
          arten.forEach(function (art) {
            var urls = e[art.id] || [];
            urls.forEach(function (u) {
              karte.appendChild(kopierZeile(art.kurz, u, true));
              hatWas = true;
            });"""

NEU_SCHLEIFE = """          var hatWas = false;
          var gezeigt = {};
          // Zu einer Blob-Adresse kennen wir meist den Dateinamen — der ist
          // als Anzeige brauchbar, die Adresse selbst nicht.
          var namen = {};
          (e.dateien || []).forEach(function (d) {
            if (d.blob) {
              namen[d.blob] = d.name + (d.seiten ? " · " + d.seiten + " Seiten" : "");
            }
          });
          arten.forEach(function (art) {
            var urls = e[art.id] || [];
            urls.forEach(function (u) {
              // verknuepfung.json speichert „/_blob/…" relativ, die
              // Link-Zentrale absolut. Darum ueber das Endstueck abgleichen.
              var kurzname = namen[u];
              if (!kurzname) {
                var ab = u.indexOf("/_blob/");
                if (ab >= 0) kurzname = namen[u.slice(ab)] || "hinterlegte Datei";
              }
              karte.appendChild(kopierZeile(art.kurz, u, true, kurzname));
              // Beide Schreibweisen merken, sonst zeichnet die Datei-Zeile
              // unten dasselbe PDF ein zweites Mal.
              gezeigt[u] = true;
              var ab2 = u.indexOf("/_blob/");
              if (ab2 >= 0) gezeigt[u.slice(ab2)] = true;
              hatWas = true;
            });"""

# --------------------------------------------------------------------------
# 3) Datei-Zeilen nur, wenn sie nicht schon als Auslieferung dastehen.
# --------------------------------------------------------------------------
ALT_DATEI = """          (e.dateien || []).forEach(function (d) {
            var zeile = document.createElement("div");"""
NEU_DATEI = """          (e.dateien || []).forEach(function (d) {
            if (gezeigt[d.blob]) return;   // steht schon als Auslieferung da
            var zeile = document.createElement("div");"""

# --------------------------------------------------------------------------
# 4) „fehlt" ist kein Stichwort, sondern eine Luecke.
# --------------------------------------------------------------------------
ALT_KEYWORD = """          if (e.keyword) {
            karte.appendChild(kopierZeile("Stichwort", e.keyword, false));
          }"""
NEU_KEYWORD = """          // In der Uebersicht steht bei einer Luecke „🔴 fehlt" in der
          // Stichwort-Spalte. Das ist keine Ansage, die man kopiert.
          var kwLeer = /^(fehlt|keins?|noch offen|—|-)$/i.test(e.keyword || "");
          if (e.keyword && !kwLeer) {
            karte.appendChild(kopierZeile("Stichwort", e.keyword, false));
          } else if (kwLeer) {
            var kw = document.createElement("div");
            kw.className = "lzzeile";
            kw.innerHTML = '<span class="lzlab">Stichwort</span>' +
              '<span class="lzwert lzfehlt">noch keins angelegt</span>';
            karte.appendChild(kw);
          }"""

ERSETZUNGEN = [
    ("kopierZeile-Kopf", ALT_ZEILE, NEU_ZEILE),
    ("Anzeigetext", ALT_TEXT, NEU_TEXT),
    ("Linkschleife", ALT_SCHLEIFE, NEU_SCHLEIFE),
    ("Datei-Doppelung", ALT_DATEI, NEU_DATEI),
    ("Stichwort-Lücke", ALT_KEYWORD, NEU_KEYWORD),
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
