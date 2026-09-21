#!/usr/bin/env python3
"""Marker-Hook (Stil 4, der Jenya-B-Roll-Stil) auf einen B-Roll-Clip brennen.

Aussehen   Hook in zwei Teilen, mittig-links. Teil 1 weiss/fett mit dunkler
           Kontur, Teil 2 mit schiefem Marker-Balken in der Akzentfarbe
           dahinter. Darunter eine kleine duenne Zeile in Weiss.
Bewegung   Der Marker-Balken wischt von links nach rechts auf (~0,35 s),
           danach steht alles still.
Stelle     Ab Sekunde 0, der Hook steht das ganze Reel.
Sound      keiner - Trending-Audio waehlt Patricia beim Posten in der App.

Doku: context/videoschnitt-animationen.md, Stil 4.
"""
import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = "/home/user/mumlifebalance-workspace/scripts/story-render/fonts"
AKZENT = {"orange": (220, 130, 46), "petrol": (18, 130, 140), "dunkelblau": (41, 85, 109)}

WISCH_S = 0.35          # Dauer des Marker-Aufwischens
NEIGUNG = -1.6          # Balken leicht schief, wie mit dem Textmarker gezogen


def textbild(w, h, teil1, teil2, unterzeile, akzent, oben_frac):
    """Baut die Textebene einmal als RGBA - ohne den Balken, der wird animiert."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    links = int(w * 0.075)
    # Der Balken braucht rechts Luft, sonst laeuft die zweite Zeile ins Bild hinaus.
    platz = w - links - int(w * 0.075)
    groesse = int(w * 0.105)
    while groesse > int(w * 0.05):
        f_hook = ImageFont.truetype(f"{FONTS}/Philosopher-Bold.ttf", groesse)
        breit = max(d.textlength(t, font=f_hook) for t in (teil1, teil2))
        if breit + int(w * 0.044) <= platz:
            break
        groesse -= 2
    f_hook = ImageFont.truetype(f"{FONTS}/Philosopher-Bold.ttf", groesse)
    f_klein = ImageFont.truetype(f"{FONTS}/SourceSans3-Regular.ttf", int(w * 0.047))

    y = int(h * oben_frac)

    # Teil 1 - weiss, fett, dunkle Kontur
    d.text((links, y), teil1, font=f_hook, fill=(255, 255, 255, 255),
           stroke_width=max(2, int(w * 0.004)), stroke_fill=(20, 28, 34, 210))

    zeilenhoehe = int(f_hook.size * 1.12)
    y2 = y + zeilenhoehe

    # Teil 2 - Text kommt spaeter ueber den Balken, Position hier merken
    kasten2 = d.textbbox((links, y2), teil2, font=f_hook)

    # Unterzeile
    y3 = y2 + int(zeilenhoehe * 1.28)
    d.text((links + int(w * 0.006), y3), unterzeile, font=f_klein,
           fill=(255, 255, 255, 255),
           stroke_width=max(2, int(w * 0.0035)), stroke_fill=(20, 28, 34, 225))

    return img, (links, y2), kasten2, f_hook


def balken_und_text(w, h, teil2, pos2, kasten2, f_hook, akzent, fortschritt):
    """Marker-Balken (bis fortschritt aufgewischt) plus der Text darauf."""
    pad_x, pad_y = int(w * 0.022), int(w * 0.012)
    x0, y0, x1, y1 = kasten2
    x0, y0, x1, y1 = x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y

    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if fortschritt > 0:
        breite = int((x1 - x0) * fortschritt)
        bal = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(bal).rounded_rectangle(
            [x0, y0, x0 + breite, y1], radius=int(h * 0.006), fill=(*akzent, 255))
        bal = bal.rotate(NEIGUNG, resample=Image.BICUBIC,
                         center=(x0, (y0 + y1) / 2))
        lay = Image.alpha_composite(lay, bal)

    if fortschritt >= 1.0:
        ImageDraw.Draw(lay).text(pos2, teil2, font=f_hook, fill=(255, 255, 255, 255))
    return lay


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--teil1", required=True)
    p.add_argument("--teil2", required=True)
    p.add_argument("--unterzeile", default="")
    p.add_argument("--akzent", default="orange", choices=list(AKZENT))
    p.add_argument("--oben", type=float, default=0.36,
                   help="Oberkante des Hooks als Anteil der Hoehe")
    a = p.parse_args()

    cap = cv2.VideoCapture(a.input)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    akzent = AKZENT[a.akzent]

    basis, pos2, kasten2, f_hook = textbild(
        w, h, a.teil1, a.teil2, a.unterzeile, akzent, a.oben)

    out = cv2.VideoWriter(a.output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        fortschritt = min(1.0, (i / fps) / WISCH_S)
        lay = balken_und_text(w, h, a.teil2, pos2, kasten2, f_hook, akzent, fortschritt)
        ebene = Image.alpha_composite(lay, basis)

        rgba = np.array(ebene)
        alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
        vorder = rgba[:, :, :3][:, :, ::-1].astype(np.float32)   # RGB -> BGR
        frame = (frame.astype(np.float32) * (1 - alpha) + vorder * alpha)
        out.write(frame.astype(np.uint8))
        i += 1

    cap.release()
    out.release()
    print(f"{a.output} - {i} Frames, {i/fps:.1f}s, {w}x{h}")


if __name__ == "__main__":
    main()
