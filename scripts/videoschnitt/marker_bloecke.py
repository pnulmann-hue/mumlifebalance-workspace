#!/usr/bin/env python3
"""Mehrere Textbloecke nacheinander im Marker-Hook-Look (Stil 4, Jenya-B-Roll).

Anders als marker_hook.py, wo ein Hook das ganze Reel steht: hier loesen sich
mehrere Bloecke zeitlich ab. Patricias Text wird dabei NICHT umgeschrieben -
der Zeilenumbruch und die markierte Zeile werden im Briefing vorgegeben.

Aussehen   Linksbuendiger Block, weiss/fett mit dunkler Kontur. Genau eine
           Zeile pro Block liegt auf einem schiefen Marker-Balken in der
           Akzentfarbe.
Bewegung   Der Balken wischt beim Blockwechsel von links nach rechts auf
           (~0,35 s), danach steht alles still.
Sound      keiner - Trending-Audio waehlt Patricia beim Posten in der App.

Doku: context/videoschnitt-animationen.md, Stil 4.
"""
import argparse
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = "/home/user/mumlifebalance-workspace/scripts/story-render/fonts"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
AKZENT = {"orange": (220, 130, 46), "petrol": (18, 130, 140), "dunkelblau": (41, 85, 109)}

WISCH_S = 0.35
NEIGUNG = -1.6


def emoji_bild(zeichen, hoehe):
    """NotoColorEmoji ist eine Bitmap-Schrift und kann nur 109 px - also gross
    rendern und runterrechnen."""
    f = ImageFont.truetype(EMOJI, 109)
    roh = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(roh).text((4, 4), zeichen, font=f, embedded_color=True)
    roh = roh.crop(roh.getbbox() or (0, 0, 140, 140))
    faktor = hoehe / roh.height
    return roh.resize((max(1, int(roh.width * faktor)), hoehe), Image.LANCZOS)


def trenne_emoji(zeile):
    """Zerlegt in (text, emoji) - Emojis stehen bei Patricia immer am Zeilenende."""
    i = len(zeile)
    while i > 0 and ord(zeile[i - 1]) > 0x2100:
        i -= 1
    return zeile[:i].rstrip(), zeile[i:].strip()


def schriftgroesse(zeilen, w, platz):
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    g = int(w * 0.072)
    while g > int(w * 0.032):
        f = ImageFont.truetype(f"{FONTS}/Philosopher-Bold.ttf", g)
        breit = max(d.textlength(trenne_emoji(z)[0], font=f) for z in zeilen)
        if breit + int(w * 0.05) <= platz:
            return f
        g -= 2
    return ImageFont.truetype(f"{FONTS}/Philosopher-Bold.ttf", g)


def block_ebenen(w, h, zeilen, markiert, akzent, mitte_frac):
    """Liefert (basis_ohne_balken, balkenkasten) - der Balken wird animiert."""
    f = schriftgroesse(zeilen, w, w - 2 * int(w * 0.075))
    zh = int(f.size * 1.2)
    links = int(w * 0.075)
    oben = int(h * mitte_frac - (len(zeilen) * zh) / 2)

    basis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(basis)
    kasten = None
    for i, zeile in enumerate(zeilen):
        y = oben + i * zh
        text, emo = trenne_emoji(zeile)
        if i == markiert:
            kasten = d.textbbox((links, y), text, font=f)
        else:
            d.text((links, y), text, font=f, fill=(255, 255, 255, 255),
                   stroke_width=max(2, int(w * 0.0042)), stroke_fill=(20, 28, 34, 215))
        if emo:
            bild = emoji_bild(emo, int(f.size * 0.9))
            x = links + int(d.textlength(text + " ", font=f))
            basis.alpha_composite(bild, (x, y + int(f.size * 0.12)))
    return basis, kasten, (links, oben + markiert * zh), zeilen[markiert], f


def balken_ebene(w, h, kasten, pos, text, f, akzent, fortschritt):
    pad_x, pad_y = int(w * 0.022), int(w * 0.013)
    x0, y0, x1, y1 = kasten
    x0, y0, x1, y1 = x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if fortschritt > 0:
        bal = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(bal).rounded_rectangle(
            [x0, y0, x0 + int((x1 - x0) * fortschritt), y1],
            radius=int(h * 0.006), fill=(*akzent, 255))
        lay = Image.alpha_composite(
            lay, bal.rotate(NEIGUNG, resample=Image.BICUBIC, center=(x0, (y0 + y1) / 2)))
    if fortschritt >= 1.0:
        ImageDraw.Draw(lay).text(pos, trenne_emoji(text)[0], font=f,
                                 fill=(255, 255, 255, 255))
    return lay


def als_array(pil):
    a = np.array(pil)
    alpha = a[:, :, 3:4].astype(np.float32) / 255.0
    return a[:, :, :3][:, :, ::-1].astype(np.float32), alpha


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--briefing", required=True, help="JSON mit den Bloecken")
    p.add_argument("--akzent", default="orange", choices=list(AKZENT))
    a = p.parse_args()

    bloecke = json.load(open(a.briefing))
    cap = cv2.VideoCapture(a.input)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    akzent = AKZENT[a.akzent]

    vorbereitet = []
    for b in bloecke:
        basis, kasten, pos, mtext, f = block_ebenen(
            w, h, b["zeilen"], b["markiert"], akzent, b.get("mitte", 0.42))
        fertig = als_array(Image.alpha_composite(
            balken_ebene(w, h, kasten, pos, mtext, f, akzent, 1.0), basis))
        vorbereitet.append(dict(b=b, basis=basis, kasten=kasten, pos=pos,
                                mtext=mtext, f=f, fertig=fertig))

    out = cv2.VideoWriter(a.output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = i / fps
        akt = None
        for v in vorbereitet:
            if v["b"]["ab"] <= t < v["b"]["bis"]:
                akt = v
                break
        if akt is None:
            out.write(frame)
            i += 1
            continue

        fortschritt = min(1.0, (t - akt["b"]["ab"]) / WISCH_S)
        if fortschritt >= 1.0:
            vorder, alpha = akt["fertig"]
        else:
            vorder, alpha = als_array(Image.alpha_composite(
                balken_ebene(w, h, akt["kasten"], akt["pos"], akt["mtext"],
                             akt["f"], akzent, fortschritt), akt["basis"]))
        out.write((frame.astype(np.float32) * (1 - alpha) + vorder * alpha).astype(np.uint8))
        i += 1

    cap.release()
    out.release()
    print(f"{a.output} - {i} Frames, {i/fps:.1f}s, {w}x{h}")


if __name__ == "__main__":
    main()
