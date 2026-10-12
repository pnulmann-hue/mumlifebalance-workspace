"""Fertige Folienbilder wirklich an die Freigabe geben (12.10.2026).

`fertigeFolien()` sollte die fertigen Bilder unter karussells/<id>/bilder/slide-NN
einsammeln, damit die Freigabe sie statt einer eigenen Zeichnung an Blotato gibt.
Sie rief aber `snap.forEach(...)` auf — die Artifact-Datenbank liefert ein Ergebnis
mit `snap.docs`, ohne `forEach`. Der Aufruf warf, der `.catch` gab ein leeres
Verzeichnis zurueck, und die Freigabe zeichnete still selbst (Georgia, Versalien).
Gefunden, weil Patricia am 12.10. das Karussell vom 15.10. freigab und in
freigaben/… die Cockpit-Zeichnung lag statt der gerenderten Folien.

Dieselbe Stelle beim Laden (Zeile ~14440) benutzt `bs.docs.forEach` — das ist die
Form, die funktioniert.

    python scripts/cockpit/patch-fertige-folien-docs.py [--datei <cockpit.html>]   (nach patch-fertige-folien.py)
"""
import os
import pathlib
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]

ALT = '''    db.doc("karussells/" + id).collection("bilder").limit(30).get()
      .then(function (snap) {
        var gefunden = {};
        snap.forEach(function (d) {'''
NEU = '''    db.doc("karussells/" + id).collection("bilder").limit(30).get()
      .then(function (snap) {
        var gefunden = {};
        // 🚨 snap.docs, nicht snap.forEach — das gibt es hier nicht (12.10.2026).
        (snap.docs || []).forEach(function (d) {'''


def main():
    ziel = ROOT / "outputs/cockpit/mlb-cockpit.html"
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    t = ziel.read_text(encoding="utf-8")
    if NEU in t:
        sys.exit("Steht schon drin — nichts zu tun.")
    n = t.count(ALT)
    if n != 1:
        sys.exit("🚨 Suchtext %dx gefunden, erwartet 1x. Nichts geaendert." % n)
    t = t.replace(ALT, NEU, 1)
    js = t[t.rfind("<script>") + 8:t.rfind("</script>")]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check: " + (r.stderr or r.stdout))
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: fertigeFolien liest jetzt snap.docs · node --check gruen" % ziel.name)


if __name__ == "__main__":
    main()
