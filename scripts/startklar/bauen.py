"""
Legt die Handy-Bildschirmaufnahme in das Zoom-Video des Startklar-Kurses.

Die Zoom-Teile 2 bis 5 haben Ton und Patricias Webcam, aber ein schwarzes
Hauptbild - dort hat sie am Handy gezeigt, ohne den Bildschirm in Zoom zu
teilen. Dieses Skript legt die passende Handyaufnahme gross ins Bild.

Der Zeitpunkt steht als "versatz" in sync.json: ab welcher Sekunde im
Zoom-Teil die Handyaufnahme erscheint. Wer den Wert nicht kennt, findet ihn
im Sync-Editor (video/startklar/sync-editor/index.html) durch Schieben.

Aufruf:
  python scripts/startklar/bauen.py                 # alle Teile mit Handy
  python scripts/startklar/bauen.py --teil 5        # nur einen Teil
  python scripts/startklar/bauen.py --teil 5 --versatz 36.5   # Wert ueberschreiben
  python scripts/startklar/bauen.py --teil 5 --probe          # nur 40 s, schnell
  python scripts/startklar/bauen.py --standbilder   # nur Kontrollbilder, kein Render
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
KONF = Path(__file__).resolve().parent / "sync.json"
ZOOM = ROOT / "video" / "startklar" / "zoom"
HANDY = ROOT / "video" / "startklar" / "roh"
FERTIG = ROOT / "video" / "startklar" / "fertig"
KONTROLLE = ROOT / "video" / "startklar" / "kontrolle"


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def dauer(pfad):
    aus = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(pfad)],
        capture_output=True, text=True, check=True)
    return float(aus.stdout.strip())


def filtergraph(lay, versatz, laenge):
    """Baut den ffmpeg-Filter: Hintergrund, Handy gross, Webcam daneben."""
    hg = lay["hintergrund"].replace("#", "0x")
    # Das Handy wird zeitlich verschoben. Vor dem Versatz existiert einfach
    # kein Bild, also bleibt der Hintergrund stehen - deshalb repeatlast=0.
    # Die Webcam ist im Zoom-Bild nur 224x126 gross. Beim Vergroessern kommt
    # keine Schaerfe dazu - Lanczos plus leichtes Nachschaerfen holt heraus,
    # was ueberhaupt da ist.
    kam = "scale={cb}:-2".format(cb=lay["kamera_breite"])
    if lay.get("kamera_schaerfen"):
        kam = ("scale={cb}:-2:flags=lanczos,unsharp=5:5:1.2:5:5:0.0"
               .format(cb=lay["kamera_breite"]))

    return (
        "color=c={hg}:s={b}x{h}:d={d}[bg];"
        "[0:v]crop={cam}," + kam + "[cam];"
        "[1:v]crop=1080:{ch}:0:{co},scale=-2:{hh},"
        "setpts=PTS-STARTPTS+{v}/TB[handy];"
        "[bg][handy]overlay={hx}:0:eof_action=pass:repeatlast=0[t1];"
        "[t1][cam]overlay={kx}:{ky}[out]"
    ).format(
        hg=hg, b=lay["breite"], h=lay["hoehe"], d=round(laenge, 3),
        cam=lay["kamera_quelle"],
        ch=2340 - lay["handy_crop_oben"], co=lay["handy_crop_oben"],
        hh=lay["handy_hoehe"], v=round(versatz, 3),
        hx=lay["handy_x"], kx=lay["kamera_x"], ky=lay["kamera_y"])


def bauen(teil, lay, versatz, probe=False):
    zoom = ZOOM / teil["zoom"]
    handy = HANDY / teil["handy"]
    for p in (zoom, handy):
        if not p.exists():
            log("FEHLT: %s" % p)
            return None

    laenge = dauer(zoom)
    ziel = FERTIG / ("teil%d%s.mp4" % (teil["teil"], "-probe" if probe else ""))
    FERTIG.mkdir(parents=True, exist_ok=True)

    befehl = ["ffmpeg", "-v", "error", "-stats", "-y",
              "-i", str(zoom), "-i", str(handy),
              "-filter_complex", filtergraph(lay, versatz, laenge),
              "-map", "[out]", "-map", "0:a",
              "-c:v", "libx264", "-preset", "medium", "-crf", "20",
              "-pix_fmt", "yuv420p", "-r", "25",
              "-c:a", "aac", "-b:a", "160k"]
    if probe:
        # 8 Sekunden vor dem Einblenden anfangen, damit man den Uebergang sieht
        befehl += ["-ss", str(max(0, versatz - 8)), "-t", "40"]
    befehl.append(str(ziel))

    log("Teil %d: Handy ab %.1f s  ->  %s" % (teil["teil"], versatz, ziel.name))
    subprocess.run(befehl, check=True)
    return ziel


def standbilder(teil, versatz):
    """Kontrollbilder kurz nach dem Einblenden - zum Selbst-Anschauen."""
    KONTROLLE.mkdir(parents=True, exist_ok=True)
    fertig = FERTIG / ("teil%d.mp4" % teil["teil"])
    if not fertig.exists():
        return []
    raus = []
    for sek in (versatz + 3, versatz + 25):
        ziel = KONTROLLE / ("teil%d-%ds.jpg" % (teil["teil"], int(sek)))
        subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(sek), "-i", str(fertig),
             "-frames:v", "1", "-vf", "scale=760:-1", "-y", str(ziel)],
            check=False)
        if ziel.exists():
            raus.append(ziel)
    return raus


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teil", type=int, help="nur diesen Teil bauen")
    ap.add_argument("--versatz", type=float, help="Versatz in Sekunden ueberschreiben")
    ap.add_argument("--probe", action="store_true", help="nur 40 s rendern")
    ap.add_argument("--standbilder", action="store_true", help="nur Kontrollbilder")
    args = ap.parse_args()

    konf = json.loads(KONF.read_text(encoding="utf-8"))
    lay = konf["layout"]
    teile = [t for t in konf["teile"] if t.get("handy")]
    if args.teil:
        teile = [t for t in teile if t["teil"] == args.teil]
        if not teile:
            log("Teil %d hat keine Handyaufnahme - nichts zu tun." % args.teil)
            return

    for t in teile:
        versatz = args.versatz if args.versatz is not None else t["versatz"]
        if args.standbilder:
            for b in standbilder(t, versatz):
                log("Kontrollbild: %s" % b)
            continue
        if args.versatz is not None and len(teile) == 1:
            t = dict(t)
            t["versatz"] = versatz
        bauen(t, lay, versatz, probe=args.probe)

    if not args.standbilder:
        log("Fertig. Dateien liegen in %s" % FERTIG)


if __name__ == "__main__":
    main()
