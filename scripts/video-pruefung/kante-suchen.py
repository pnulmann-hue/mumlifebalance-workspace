#!/usr/bin/env python3
"""Sucht waagrechte Kanten, die ueber die ganze Bildbreite laufen.

Das sind die Kanten, die von einer hinterlegten Flaeche stammen — ein
Schleier, der nicht bis auf null auslaeuft, sondern an seiner eigenen
Box abgeschnitten wird. Im fertigen Video sieht das aus wie ein Strich
quer durchs Bild, und wenn Patricia dort sitzt, laeuft er durch ihr
Gesicht.

Warum gemittelt wird: in einem einzelnen Bild verschwindet so ein Strich
zwischen Haaren, Regalkanten und Bildrauschen. Ueber viele Bilder gemittelt
loescht sich alles Bewegte aus, und was stehen bleibt, ist genau das
Aufgelegte.

Erkannt wird eine Kante nur, wenn der Helligkeitssprung ueber fast die
ganze Breite dasselbe Vorzeichen hat. Eine Textkante ist oertlich und
faellt damit raus.

    python scripts/video-pruefung/kante-suchen.py <video.mp4>
"""
import argparse, pathlib, subprocess, sys, tempfile
import numpy as np
from PIL import Image

# Ueber die ganze Breite gleiches Vorzeichen — darunter ist es kein
# durchlaufender Strich, sondern Text oder ein Gegenstand im Bild.
MIN_EINIG = 0.92
# Ab hier faellt es im Video auf. Bei 2.9 hat Patricia es gesehen.
SCHWELLE = 1.2


def bilder(video: pathlib.Path, anzahl: int, ordner: pathlib.Path) -> list[np.ndarray]:
    dauer = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(video)],
        capture_output=True, text=True, check=True).stdout.strip())
    raus = []
    for i in range(anzahl):
        # Rand aussparen: am Anfang blendet der Hook ein, am Ende aus.
        t = dauer * (0.15 + 0.70 * i / max(1, anzahl - 1))
        ziel = ordner / f"{i:02d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}",
                        "-i", str(video), "-frames:v", "1", str(ziel)], check=True)
        raus.append(np.asarray(Image.open(ziel).convert("L"), dtype=np.float64))
    return raus


def kanten(mittel: np.ndarray) -> list[tuple[int, float, float]]:
    d = np.diff(mittel, axis=0)                  # Zeile y minus Zeile y-1
    pos = (d > 0).mean(axis=1)
    einig = np.maximum(pos, 1.0 - pos)           # wie einheitlich das Vorzeichen ist
    staerke = np.abs(np.median(d, axis=1))
    treffer = [(int(y) + 1, float(staerke[y]), float(einig[y]))
               for y in range(len(staerke))
               if einig[y] >= MIN_EINIG and staerke[y] >= SCHWELLE]
    return sorted(treffer, key=lambda t: -t[1])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("video", type=pathlib.Path)
    p.add_argument("--bilder", type=int, default=12)
    a = p.parse_args()
    if not a.video.exists():
        print(f"Nicht gefunden: {a.video}")
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        stapel = bilder(a.video, a.bilder, pathlib.Path(tmp))
    mittel = np.mean(stapel, axis=0)
    hoehe = mittel.shape[0]
    gefunden = kanten(mittel)

    print(f"{a.video.name} · {mittel.shape[1]}x{hoehe} · {len(stapel)} Bilder gemittelt")
    if not gefunden:
        print("Keine durchlaufende Kante. Sauber.")
        return 0
    print(f"{len(gefunden)} Kante(n):")
    for y, s, e in gefunden[:8]:
        print(f"  y={y:4d} ({y / hoehe * 100:5.1f} %)  Sprung {s:5.2f}  einheitlich {e * 100:.0f} %")
    return 1


if __name__ == "__main__":
    sys.exit(main())
