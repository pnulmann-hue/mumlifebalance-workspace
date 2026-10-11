"""
Macht aus einem Foto ein Dokument, das direkt als Slide-Hintergrund
ins Cockpit geschrieben werden kann.

Das Cockpit legt Bilder als dataUrl in der Datenbank ab. Damit ein Dokument
nicht zu gross wird, verkleinert dieses Skript das Foto und dreht die
JPEG-Qualitaet so weit herunter, bis es unter die Grenze passt — genau wie
das Cockpit es beim Hochladen im Browser auch macht.

Aufruf:
  python scripts/cockpit/foto-ins-cockpit.py <foto> --slide s-1
  python scripts/cockpit/foto-ins-cockpit.py <foto> --slide s-1 --ausschnitt 4:5
  python scripts/cockpit/foto-ins-cockpit.py --liste            # was liegt bereit

Danach mit dem Ergebnis:
  Artifact write_db
    collection: karussells/<carId>/bilder
    doc_id:     <slideId>
    file_path:  <die erzeugte .json>
"""
import argparse
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
AUSGABE = ROOT / "outputs" / "cockpit" / "bilder"
QUELLEN = [
    ROOT / "context" / "Shootingbilder",
    ROOT / "context" / "content-assets" / "inbox",
]
# Das Cockpit haelt seine eigenen Bilder unter 180 KB dataUrl.
GRENZE = 180000


def log(msg):
    print(msg, flush=True)


def masse(pfad):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(pfad)],
        capture_output=True, text=True, check=True)
    b, h = r.stdout.strip().split("x")[:2]
    return int(b), int(h)


def erzeugen(quelle, ziel_jpg, breite, qualitaet, ausschnitt=None):
    """qualitaet: 2 (beste) bis 31 (schlechteste) — ffmpeg-Skala."""
    filter_kette = []
    if ausschnitt:
        w, h = (int(x) for x in ausschnitt.split(":"))
        # mittigen Ausschnitt im gewuenschten Verhaeltnis nehmen
        filter_kette.append(
            "crop='min(iw,ih*%d/%d)':'min(ih,iw*%d/%d)'" % (w, h, h, w))
    filter_kette.append("scale=%d:-2" % breite)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(quelle),
         "-vf", ",".join(filter_kette), "-q:v", str(qualitaet), str(ziel_jpg)],
        check=True)


def main():
    p = argparse.ArgumentParser(description="Foto als Cockpit-Slide-Hintergrund aufbereiten")
    p.add_argument("foto", nargs="?", help="Pfad zum Foto")
    p.add_argument("--slide", help="Slide-ID im Karussell (wird der Dateiname)")
    p.add_argument("--ausschnitt", default="4:5",
                   help="Seitenverhaeltnis des Ausschnitts, z.B. 4:5 (Standard) oder 1:1, 'nein' fuer keinen")
    p.add_argument("--breite", type=int, default=1200)
    p.add_argument("--liste", action="store_true", help="verfuegbare Fotos zeigen")
    args = p.parse_args()

    if args.liste:
        for q in QUELLEN:
            if not q.exists():
                continue
            bilder = sorted([f for f in q.rglob("*")
                             if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
            log("%s — %d Fotos" % (q.relative_to(ROOT), len(bilder)))
            for b in bilder[:8]:
                log("   %s" % b.relative_to(ROOT))
            if len(bilder) > 8:
                log("   … und %d weitere" % (len(bilder) - 8))
        return

    if not args.foto:
        sys.exit("Bitte ein Foto angeben (oder --liste).")
    quelle = Path(args.foto)
    if not quelle.exists():
        quelle = ROOT / args.foto
    if not quelle.exists():
        sys.exit("Foto nicht gefunden: %s" % args.foto)
    if not args.slide:
        sys.exit("Bitte --slide <slideId> angeben, sonst weiss das Cockpit nicht, wohin damit.")

    b, h = masse(quelle)
    log("Foto: %s (%dx%d)" % (quelle.name, b, h))

    ausschnitt = None if str(args.ausschnitt).lower() in ("nein", "no", "") else args.ausschnitt
    breite = args.breite
    with tempfile.TemporaryDirectory() as tmp:
        ziel = Path(tmp) / "bild.jpg"
        daten = None
        for qual in (3, 5, 7, 9, 12, 16, 20):
            erzeugen(quelle, ziel, breite, qual, ausschnitt)
            roh = ziel.read_bytes()
            dataurl = "data:image/jpeg;base64," + base64.b64encode(roh).decode()
            if len(dataurl) <= GRENZE:
                daten = dataurl
                log("  Qualitaet %d, Breite %d → %.0f KB" % (qual, breite, len(dataurl) / 1024))
                break
            if qual >= 20 and breite > 700:
                breite = int(breite * 0.75)
                log("  noch zu gross, verkleinere auf %d px" % breite)
                for qual2 in (5, 9, 14, 20):
                    erzeugen(quelle, ziel, breite, qual2, ausschnitt)
                    roh = ziel.read_bytes()
                    dataurl = "data:image/jpeg;base64," + base64.b64encode(roh).decode()
                    if len(dataurl) <= GRENZE:
                        daten = dataurl
                        log("  Qualitaet %d, Breite %d → %.0f KB" % (qual2, breite, len(dataurl) / 1024))
                        break
                break
        if not daten:
            sys.exit("Das Foto liess sich nicht klein genug bekommen. Probier ein anderes.")

    AUSGABE.mkdir(parents=True, exist_ok=True)
    ziel_json = AUSGABE / ("%s.json" % args.slide)
    ziel_json.write_text(json.dumps({"dataUrl": daten}, ensure_ascii=False), encoding="utf-8")

    log("")
    log("Fertig → %s" % ziel_json.relative_to(ROOT))
    log("Jetzt ins Cockpit schreiben:")
    log("  Artifact write_db · collection karussells/<carId>/bilder · doc_id %s" % args.slide)
    log("  file_path: %s" % ziel_json)


if __name__ == "__main__":
    main()
