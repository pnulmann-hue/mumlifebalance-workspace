#!/usr/bin/env python3
"""Findet zu einem fertigen B-Roll den Quellclip und die Stelle darin.

Noetig geworden, weil die Bauparameter der ersten zehn B-Rolls nirgends
gespeichert wurden. Der Text ist eingebrannt, das Rohmaterial aber noch da.
(`broll-bauen.py` legt seit 19.09.2026 einen `bauplan.json` ab — damit ist
dieses Werkzeug fuer neue Reels nicht mehr noetig.)

🚨 Der Textbereich wird beim Vergleich ausgeblendet. Die helle Schrift liegt
auf jedem fertigen B-Roll an derselben Stelle und wuerde sonst alle Clips
gleich aehnlich aussehen lassen.

🚨 Die Miniaturbilder werden **einmal** angelegt und danach wiederverwendet.
Ein ffmpeg-Aufruf je Einzelbild bedeutet bei 184 Clips rund 14 Minuten — pro
gesuchtem Reel. Mit einem Aufruf je Clip und einem Zwischenspeicher ist es
einmal gut eine Minute und danach Sekunden.

    python scripts/content/quelle-finden.py video/output/kw39/*.mp4
    python scripts/content/quelle-finden.py --index-neu <datei>
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

WURZEL = pathlib.Path(__file__).resolve().parents[2]
EIN = WURZEL / "video" / "input"
CACHE = WURZEL / "video" / "output" / "_bildindex"
KLEIN = (48, 85)
PRO_SEK = 0.5          # zwei Miniaturen je Sekunde reichen, um die Stelle zu finden


def dauer_von(p: pathlib.Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip())


def ohne_text(a: np.ndarray) -> np.ndarray:
    """Mittleres Drittel raus — dort steht bei jedem B-Roll der Hook."""
    h = a.shape[-2]
    return np.concatenate([a[..., : int(h * 0.28), :], a[..., int(h * 0.72):, :]], axis=-2)


def index_bauen(neu: bool = False) -> dict[str, np.ndarray]:
    CACHE.mkdir(parents=True, exist_ok=True)
    clips = sorted(EIN.glob("*.mp4"))
    index: dict[str, np.ndarray] = {}
    for i, c in enumerate(clips, 1):
        ziel = CACHE / (c.stem + ".npy")
        if ziel.exists() and not neu:
            index[c.name] = np.load(ziel)
            continue
        print(f"\r  Index {i}/{len(clips)} {c.stem[:28]:28s}", end="", file=sys.stderr)
        # EIN Aufruf je Clip statt einer je Bild — das ist der ganze Trick.
        roh = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(c), "-vf",
             f"fps={PRO_SEK},scale={KLEIN[0]}:{KLEIN[1]}",
             "-pix_fmt", "gray", "-f", "rawvideo", "-"],
            capture_output=True).stdout
        n = len(roh) // (KLEIN[0] * KLEIN[1])
        if n == 0:
            continue
        a = np.frombuffer(roh[: n * KLEIN[0] * KLEIN[1]], dtype=np.uint8)
        a = a.reshape(n, KLEIN[1], KLEIN[0]).astype(np.float32)
        np.save(ziel, a)
        index[c.name] = a
    print("\r" + " " * 64 + "\r", end="", file=sys.stderr)
    return index


def zielbild(p: pathlib.Path) -> np.ndarray:
    roh = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{dauer_von(p) * 0.5:.2f}", "-i", str(p),
         "-frames:v", "1", "-vf", f"scale={KLEIN[0]}:{KLEIN[1]}",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.uint8).reshape(KLEIN[1], KLEIN[0]).astype(np.float32)


def naehe(ziel: np.ndarray, stapel: np.ndarray) -> np.ndarray:
    """Korrelation des Ziels mit jedem Bild des Stapels, Text ausgeblendet."""
    z = ohne_text(ziel[None]).reshape(1, -1)
    s = ohne_text(stapel).reshape(len(stapel), -1)
    z = z - z.mean(axis=1, keepdims=True)
    s = s - s.mean(axis=1, keepdims=True)
    nenner = np.linalg.norm(z) * np.linalg.norm(s, axis=1)
    nenner[nenner == 0] = 1e-9
    return (s @ z.ravel()) / nenner


def verfeinern(clip: pathlib.Path, ziel: np.ndarray, grob: float,
               fenster: float = 3.0, takt: float = 0.2) -> tuple[float, float]:
    """Im gefundenen Clip die Stelle genau bestimmen.

    Der Index tastet nur alle zwei Sekunden ab — das findet den richtigen
    Clip, aber die Startzeit liegt dann bis zu einer Sekunde daneben. Hier
    wird nur noch der eine Gewinnerclip fein abgetastet, das kostet Sekunden.
    """
    von = max(0.0, grob - fenster)
    roh = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{von:.2f}", "-i", str(clip),
         "-t", f"{2 * fenster:.2f}", "-vf",
         f"fps={1 / takt:.2f},scale={KLEIN[0]}:{KLEIN[1]}",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    n = len(roh) // (KLEIN[0] * KLEIN[1])
    if n == 0:
        return grob, 0.0
    a = np.frombuffer(roh[: n * KLEIN[0] * KLEIN[1]], dtype=np.uint8)
    a = a.reshape(n, KLEIN[1], KLEIN[0]).astype(np.float32)
    w = naehe(ziel, a)
    k = int(np.argmax(w))
    return von + k * takt, float(w[k])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("fertig", nargs="+", type=pathlib.Path)
    p.add_argument("--index-neu", action="store_true")
    p.add_argument("--zeige", type=int, default=2)
    a = p.parse_args()

    index = index_bauen(a.index_neu)
    print(f"Bildindex: {len(index)} Clips\n")

    for datei in a.fertig:
        if not datei.exists():
            print(f"{datei} — nicht gefunden")
            continue
        ziel = zielbild(datei)
        treffer = []
        for name, stapel in index.items():
            w = naehe(ziel, stapel)
            k = int(np.argmax(w))
            treffer.append((float(w[k]), name, k / PRO_SEK))
        treffer.sort(reverse=True)
        best = treffer[0]
        genau, guete = verfeinern(EIN / best[1], ziel, best[2])
        # Die Mitte der fertigen Datei wurde verglichen, also liegt der
        # Anfang eine halbe Laenge davor.
        ab = max(0.0, genau - dauer_von(datei) / 2)
        print(f"{datei.name}")
        print(f"  -> {best[1]}  --ab {ab:.1f}   (Naehe {guete:.3f})")
        for s, name, wo in treffer[1: 1 + a.zeige]:
            print(f"     dahinter {s:.3f}  {name}")
        if guete < 0.90:
            print("     ACHTUNG: schwacher Treffer, von Hand nachsehen.")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
