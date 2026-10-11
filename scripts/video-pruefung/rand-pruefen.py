"""Prueft ein Remotion-Reel maschinell auf Text, der aus dem Bild laeuft.

Rendert die Textebene OHNE Video (Prop `nurText: true`) und misst den hellsten
Punkt in den aeusseren Pixeln links und rechts. Text ist cremeweiss, der Grund
ist dunkelblau — jeder helle Punkt im Randstreifen ist also Text am Rand.

🚨 Gelernt am 15.09.2026: Die erste Fassung nutzte ffmpeg `signalstats` und hat
NICHTS zurueckgegeben — die Pruefung meldete immer "OK", obwohl Text sichtbar
rauslief. Deshalb hier: Rohbytes lesen und selbst das Maximum bilden. Eine
Pruefung, die nicht fehlschlagen KANN, ist schlimmer als keine.

Aufruf im Remotion-Projekt:
  python <repo>/scripts/video-pruefung/rand-pruefen.py
  python ... --takt 0.4 --rand 26 --komposition Reel
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BREITE, HOEHE, FPS = 1080, 1920, 30


def hellster(png, x, breite):
    """Maximale Helligkeit im Streifen ab x. Liest Rohbytes, kein signalstats."""
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(png),
         "-vf", f"crop={breite}:{HOEHE}:{x}:0,format=gray",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True)
    if p.returncode != 0 or not p.stdout:
        sys.exit(f"Messung fehlgeschlagen: {p.stderr.decode('utf-8','replace')[:200]}")
    return max(p.stdout)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--komposition", default="Reel")
    a.add_argument("--takt", type=float, default=0.5, help="Sekunden zwischen Pruefpunkten")
    a.add_argument("--rand", type=int, default=24, help="Breite des Randstreifens in px")
    a.add_argument("--schwelle", type=int, default=60)
    args = a.parse_args()

    caps = json.loads(Path("src/captions.json").read_text(encoding="utf-8"))
    ende = caps[-1]["endMs"] / 1000
    ordner = Path("out/pruef"); ordner.mkdir(parents=True, exist_ok=True)

    punkte, s = [], 0.3
    while s < ende:
        punkte.append(round(s * FPS)); s += args.takt

    print(f"Pruefe {len(punkte)} Stellen (Randstreifen {args.rand} px, Schwelle {args.schwelle}) …")
    treffer = []
    for i, fr in enumerate(punkte, 1):
        png = ordner / f"p{fr:05d}.png"
        r = subprocess.run(
            ["npx", "remotion", "still", "src/index.ts", args.komposition, str(png),
             "--frame", str(fr), "--overwrite", "--props", '{"nurText":true}'],
            capture_output=True, shell=(sys.platform == "win32"))
        if not png.exists():
            sys.exit(f"Render fehlgeschlagen bei Frame {fr}:\n"
                     f"{r.stderr.decode('utf-8','replace')[-400:]}")
        for seite, x in (("links", 0), ("rechts", BREITE - args.rand)):
            h = hellster(png, x, args.rand)
            if h > args.schwelle:
                treffer.append((fr, round(fr / FPS, 1), seite, h))
        if i % 20 == 0:
            print(f"  … {i}/{len(punkte)}")

    print()
    if not treffer:
        print(f"OK — {len(punkte)} Stellen, kein Text am Rand.")
        return 0
    print(f"🚨 TEXT AM RAND an {len(treffer)} Stellen:")
    for fr, sek, seite, h in treffer[:15]:
        print(f"   Frame {fr:5d}  ({sek:5.1f} s)  {seite:7s}  Helligkeit {h}")
    if len(treffer) > 15:
        print(f"   … und {len(treffer)-15} weitere")
    return 1


if __name__ == "__main__":
    sys.exit(main())
