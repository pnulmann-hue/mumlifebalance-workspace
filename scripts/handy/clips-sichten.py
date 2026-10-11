"""
Sichtet die Videos auf dem Handy, ohne sie zu kopieren.

Zieht pro Video ein Standbild und schreibt Laenge und Format daneben. Damit
kann Claude sehen, was auf dem Material ist, statt aus Dateinamen zu raten —
und dann gezielt die zwei, drei Clips holen, die zum Hook passen.

Es wird auf dem Handy **nichts** geloescht, verschoben oder veraendert.

Aufruf:
  python scripts/handy/clips-sichten.py                    # Reel-Videos + Camera
  python scripts/handy/clips-sichten.py Reel-Videos        # nur ein Album
  python scripts/handy/clips-sichten.py --ab 2026-08-01    # nur neuere
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
HANDY = Path(r"C:\Users\pnulm\CrossDevice\S25 Ultra von Patricia\storage\DCIM")
ZIEL = ROOT / "context" / "content-assets" / "sichtung"
BERICHT = ROOT / "context" / "content-assets-sichtung.md"
ENDUNGEN = {".mp4", ".mov", ".3gp"}
STANDARD_ALBEN = ["Reel-Videos", "Camera"]


def ffprobe(pfad):
    """Laenge, Breite, Hoehe und Drehung — ohne die Datei ganz zu lesen."""
    # Achtung: die Drehung steckt bei Handy-Videos in den side_data der Spur,
    # nicht in width/height. Ohne sie meldet ffprobe Hochformat-Clips als quer.
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_entries",
         "format=duration:stream=width,height:stream_side_data=rotation:stream_tags=rotate",
         "-select_streams", "v:0", str(pfad)],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        d = json.loads(r.stdout)
    except Exception:
        return None
    s = (d.get("streams") or [{}])[0]
    dreh = 0
    for sd in s.get("side_data_list") or []:
        if "rotation" in sd:
            dreh = int(float(sd["rotation"]))
    if not dreh:
        dreh = int(float((s.get("tags") or {}).get("rotate") or 0))
    b, h = s.get("width", 0), s.get("height", 0)
    if dreh in (90, -90, 270, -270):
        b, h = h, b
    return {
        "dauer": round(float((d.get("format") or {}).get("duration") or 0), 1),
        "breite": b, "hoehe": h,
        "hochformat": h > b,
    }


def standbild(quelle, ziel, sekunde):
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.2f" % sekunde,
         "-i", str(quelle), "-frames:v", "1", "-vf", "scale=360:-2", str(ziel)],
        capture_output=True, text=True)
    return r.returncode == 0 and ziel.exists()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    alben = args or STANDARD_ALBEN
    ab = None
    if "--ab" in sys.argv:
        ab = datetime.fromisoformat(sys.argv[sys.argv.index("--ab") + 1])

    ZIEL.mkdir(parents=True, exist_ok=True)
    zeilen = []
    gesamt = 0

    for album in alben:
        ordner = HANDY / album
        if not ordner.is_dir():
            print("  Album fehlt: %s" % album)
            continue
        dateien = sorted(
            [p for p in ordner.iterdir()
             if p.is_file() and p.suffix.lower() in ENDUNGEN],
            key=lambda p: p.stat().st_mtime, reverse=True)
        print("Album %s: %d Videos" % (album, len(dateien)))
        for p in dateien:
            wann = datetime.fromtimestamp(p.stat().st_mtime)
            if ab and wann < ab:
                continue
            info = ffprobe(p)
            if not info:
                print("   ? %s — nicht lesbar" % p.name)
                continue
            # Mitte des Clips zeigt mehr als der erste Frame (oft noch Bewegung/unscharf)
            bild = ZIEL / ("%s__%s.jpg" % (album.lower().replace(" ", "-"), p.stem))
            if not bild.exists():
                if not standbild(p, bild, min(1.5, max(0.3, info["dauer"] / 2))):
                    print("   ? %s — kein Standbild" % p.name)
                    continue
            gesamt += 1
            zeilen.append({
                "album": album, "datei": p.name, "bild": bild.name,
                "dauer": info["dauer"], "hochformat": info["hochformat"],
                "datum": wann.strftime("%Y-%m-%d"),
                "mb": round(p.stat().st_size / 1024 / 1024, 1),
            })
            print("   %-30s %5.1f s  %s  %s" % (
                p.name, info["dauer"],
                "hoch" if info["hochformat"] else "quer", wann.strftime("%Y-%m-%d")))

    zeilen.sort(key=lambda z: (z["album"], z["datei"]))
    text = ["---", "tags: [content]", "---", "",
            "# Sichtung Handy-Videos", "",
            "Erzeugt am %s von `scripts/handy/clips-sichten.py`. Standbilder liegen in "
            "`context/content-assets/sichtung/` (gitignored)." % datetime.now().strftime("%Y-%m-%d %H:%M"),
            "", "Auf dem Handy wurde nichts verändert.", "",
            "| Album | Datei | Länge | Format | Datum | Standbild |",
            "|---|---|---|---|---|---|"]
    for z in zeilen:
        text.append("| %s | `%s` | %.1f s | %s | %s | `%s` |" % (
            z["album"], z["datei"], z["dauer"],
            "hoch" if z["hochformat"] else "quer", z["datum"], z["bild"]))
    BERICHT.write_text("\n".join(text) + "\n", encoding="utf-8")
    print("\n%d Videos gesichtet. Bericht: %s" % (gesamt, BERICHT))


if __name__ == "__main__":
    main()
