"""Reel-Karte für archivierte Videos (04.11.2026, Version 124).

Patricia: *„dass die videos selber aus dem cockpit verschwinden, sobald sie gepostet sind
und nur noch der link zu instagram dann kommt"*. Das Entfernen macht der tägliche Abgleich
(`videos-archivieren.py`, Schritt 4d im Task). Hier steht nur, was die Karte dazu braucht:
die Felder `videoArchiv` und `igLink` beim Speichern und Lesen, der Hinweis mit dem
Instagram-Link statt des Upload-Knopfs, und kein „Video fehlt“ mehr.

🚨 Ohne die zwei Felder in der festen Liste von `saveReel` löscht das nächste Speichern den Vermerk.

    python scripts/cockpit/patch-video-archiv.py [--datei <cockpit.html>]
"""

import os
import pathlib
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]

HILFE = '''  /* Archiviertes Video: Hinweis auf der Karte statt Upload-Knopf (patch-video-archiv.py). */
  function videoArchivHinweis(o) {
    var a = o.videoArchiv || {};
    return '<span class="wk-unter">Video archiviert: ' + esc(a.pfad || "") +
      '. F\\u00fcr einen Repost sag es mir, dann lade ich es wieder hoch.</span>' +
      (o.igLink ? '<a class="btn" href="' + esc(o.igLink) +
        '" target="_blank" rel="noopener">Auf Instagram ansehen</a>' : "");
  }

'''

STELLEN = [
    ("Fehlt", '''    if (b.art === "reels" && !b.videourl) {
      if ((o.videoart || "sprech") === "broll") {''',
     '''    if (b.art === "reels" && !b.videourl && !o.videoArchiv) {
      if ((o.videoart || "sprech") === "broll") {'''),
    ("Upload", '''        (assetsAPI
          ? '<label class="btn filebtn wk-hochladen' + (b.videourl ? "" : " primary") + '">' +''',
     '''        (b.obj.videoArchiv ? videoArchivHinweis(b.obj) : assetsAPI
          ? '<label class="btn filebtn wk-hochladen' + (b.videourl ? "" : " primary") + '">' +'''),
    ("Sprechtext", '''(b.art === "reels" && !b.videourl && (b.obj.videoart || "sprech") !== "broll"''',
     '''(b.art === "reels" && !b.videourl && !b.obj.videoArchiv && (b.obj.videoart || "sprech") !== "broll"'''),
    ("Testreel-Kopie", '''neu.blotato = null; neu.videourl = ""; neu.videodatei = "";''',
     '''neu.blotato = null; neu.videourl = ""; neu.videodatei = ""; neu.videoArchiv = null; neu.igLink = "";'''),
    ("Speichern", '''        untertitel: r.untertitel || "", videodatei: r.videodatei || "",
        blotato: r.blotato || null,''',
     '''        untertitel: r.untertitel || "", videodatei: r.videodatei || "",
        videoArchiv: r.videoArchiv || null, igLink: r.igLink || "",
        blotato: r.blotato || null,'''),
    ("Lesen", '''videodatei: d0.videodatei || "", blotato: d0.blotato || null, rolle:''',
     '''videodatei: d0.videodatei || "", videoArchiv: d0.videoArchiv || null, igLink: d0.igLink || "", blotato: d0.blotato || null, rolle:'''),
    ("Hilfsfunktion", '''  /* Was an einem Beitrag fehlt, und wer dafuer zustaendig ist.''',
     HILFE + '''  /* Was an einem Beitrag fehlt, und wer dafuer zustaendig ist.'''),
]


def pruefe_js(js):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check: %s" % (r.stderr or r.stdout))


def main():
    ziel = ROOT / "outputs/cockpit/mlb-cockpit.html"
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    t = ziel.read_text(encoding="utf-8")
    if "function videoArchivHinweis(" in t:
        sys.exit("Steht schon drin, nichts zu tun.")
    vorher = len(t)
    for name, alt, neu in STELLEN:
        n = t.count(alt)
        if n != 1:
            sys.exit("🚨 «%s» kommt %dx vor, erwartet genau 1x. Nichts geändert." % (name, n))
        t = t.replace(alt, neu, 1)
    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")])
    tmp = ziel.with_suffix(".tmp")
    tmp.write_text(t, encoding="utf-8")
    os.replace(tmp, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
