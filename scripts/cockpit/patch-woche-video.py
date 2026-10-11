"""
Das Reel-Video im Cockpit abspielbar machen.

Bisher stand in der Wochen-Vorschau nur ein Standbild und daneben der
Dateiname. Patricia konnte das fertige Reel nirgends anschauen.

Loesung: Die Videos liegen jetzt als Dateien am Artifact selbst
(assets-Faehigkeit). Ihre Adresse steht im Reel-Dokument unter `videourl`.
Die Wochenkarte zeigt dort, wo sie hinterlegt ist, einen echten Player statt
des Standbilds — mit Steuerung, also zum Anschauen vor der Freigabe.

Aufruf:
  python scripts/cockpit/patch-woche-video.py [--pruefen]
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


patch("Video-Adresse speichern",
      '        coverfarbe: r.coverfarbe || "dunkelblau",',
      '        coverfarbe: r.coverfarbe || "dunkelblau",\n'
      '        videourl: r.videourl || "",')

patch("Video-Adresse laden",
      'coverfarbe: d0.coverfarbe || "dunkelblau", scrim: d0.scrim !== false,',
      'coverfarbe: d0.coverfarbe || "dunkelblau", videourl: d0.videourl || "", '
      'scrim: d0.scrim !== false,')

patch("Video an die Wochenkarte durchreichen",
      '      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",\n'
      '                       titel: r.name, hook: r.hook || "", unter: r.unter || "",\n'
      '                       caption: r.caption || "", datei: r.videodatei || "" });',
      '      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",\n'
      '                       titel: r.name, hook: r.hook || "", unter: r.unter || "",\n'
      '                       caption: r.caption || "", datei: r.videodatei || "",\n'
      '                       videourl: r.videourl || "" });')

patch("Player statt Standbild, wenn ein Video da ist",
      """    var quelle = coverBild(b);
    var bild = quelle
      ? '<img class="wk-bild" src="' + quelle + '" alt="">'
      : '<div class="wk-leer">Noch kein Vorschaubild</div>';""",
      """    var quelle = coverBild(b);
    // Wenn ein Video hinterlegt ist, steht hier der Player. Sonst das Cover.
    var bild = b.videourl
      ? '<video class="wk-bild wk-video" src="' + esc(b.videourl) + '" controls ' +
        'playsinline preload="metadata"' + (quelle ? ' poster="' + quelle + '"' : "") + '></video>'
      : (quelle
          ? '<img class="wk-bild" src="' + quelle + '" alt="">'
          : '<div class="wk-leer">Noch kein Vorschaubild</div>');""")

patch("Cover unter dem Player zeigen",
      """    // Farbwaehler nur beim Reel — beim Karussell macht die Farbe der Editor.
    var farbwahl = "";
    if (b.art === "reels") {
      farbwahl = '<div class="wk-farben">' +""",
      """    // Farbwaehler nur beim Reel — beim Karussell macht die Farbe der Editor.
    // Laeuft daneben ein Video, kommt das Cover als kleines Bild dazu, damit
    // beides sichtbar bleibt: was im Feed steht und was abgespielt wird.
    var farbwahl = "";
    if (b.art === "reels") {
      if (b.videourl && quelle) {
        farbwahl += '<img class="wk-covermini" src="' + quelle + '" alt="Cover">';
      }
      farbwahl += '<div class="wk-farben">' +""")

patch("Stil fuer Player und Mini-Cover",
      "  .wk-farben { display: flex; gap: 6px; align-items: center; margin-top: 8px; }",
      """  .wk-video { background: #0c1c30; }
  .wk-covermini {
    width: 78px; border-radius: 6px; border: 1px solid var(--line);
    display: block; margin-top: 8px;
  }
  .wk-farben { display: flex; gap: 6px; align-items: center; margin-top: 8px; }""")


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
