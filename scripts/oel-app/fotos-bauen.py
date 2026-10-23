"""Öl-App — Produktfotos für den Öl-Kompass zuschneiden (quadratisch um die Flasche, klein fürs Handy).

    python scripts/oel-app/fotos-bauen.py

Quelle: Patricias Produktfotos in context/doTERRA/Produktwissen/. Die meisten sind gestylte Bilder (Flasche
mit Zweigen, Ingwer, Zitronenscheiben) — deshalb je Foto die Stelle der Flasche als Anteil von Breite und
Höhe; am Kontaktbogen kontrollieren, nicht raten. Ausgabe: outputs/oel-app/app/bilder/<kennung>.jpg
(gitignored), app-bauen.py setzt dann am Produkt das Feld „foto“.
Neues Foto: Datei in Produktwissen ablegen, Zeile in FOTOS ergänzen, Skript laufen lassen.
"""
import pathlib
import sys

from PIL import Image, ImageOps

WS = pathlib.Path(__file__).resolve().parents[2]
QUELLE = WS / "context/doTERRA/Produktwissen"
ZIEL = WS / "outputs/oel-app/app/bilder"
ROH = WS / "outputs/oel-app/roh/fotos"   # Originale aus dem doTERRA Marketing-Kit (fotos-holen.py)
GROESSE = 480

# Kennung: (Datei, Mitte der Flasche x, y als Anteil, Anteil der kürzeren Seite für den Ausschnitt)
FOTOS = {
    "air": ("Air 15 ml.jpg", .50, .62, .62),
    "deep-blue": ("Deep Blue 5 ml 2.jpg", .55, .42, .9),
    "frankincense": ("Frankincense 15 ml 1.jpg", .50, .52, .85),
    "lavender": ("Lavender 15 ml 4.jpg", .58, .50, .9),
    "lemon": ("Lemon 15 ml.jpg", .50, .48, .8),
    "on-guard": ("On Guard.JPG", .62, .45, .95),
    "oregano": ("Oregano-15ml_CMYK.jpg", .50, .50, 0),   # freigestellt: auf Weiss gesetzt statt beschnitten
    "peppermint": ("Peppermint 15 ml 2.jpg", .48, .50, .8),
    "tea-tree": ("Tea Tree 10 & 15 ml.jpg", .55, .48, .9),
    "zengest": ("ZenGest 15 ml 1.jpg", .45, .58, .7),
}


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for kennung, (datei, x, y, anteil) in FOTOS.items():
        im = ImageOps.exif_transpose(Image.open(QUELLE / datei)).convert("RGB")
        w, h = im.size
        if anteil == 0:  # schmale freigestellte Flasche: mittig auf Weiss
            im.thumbnail((GROESSE, int(GROESSE * .86)))
            grund = Image.new("RGB", (GROESSE, GROESSE), (255, 255, 255))  # Foto hat weissen Grund
            grund.paste(im, ((GROESSE - im.width) // 2, (GROESSE - im.height) // 2))
            im = grund
        else:
            s = int(min(w, h) * anteil)
            l = min(max(int(w * x - s / 2), 0), w - s)
            o = min(max(int(h * y - s / 2), 0), h - s)
            im = im.crop((l, o, l + s, o + s)).resize((GROESSE, GROESSE), Image.LANCZOS)
        ziel = ZIEL / f"{kennung}.jpg"
        im.save(ziel, quality=82, optimize=True, progressive=True)
        print(f"  {kennung:14} {ziel.stat().st_size // 1024} KB")

    # Alle übrigen Produkte: die freigestellte Flasche aus dem Marketing-Kit (fotos-holen.py),
    # zugeschnitten auf den sichtbaren Teil und mittig auf Weiss. Die zehn gestylten oben gehen vor.
    alle = list(FOTOS)
    for png in sorted(ROH.glob("*.png")):
        kennung = png.stem
        if kennung in FOTOS:
            continue
        try:
            im = ImageOps.exif_transpose(Image.open(png)).convert("RGBA")
        except Exception as e:
            print(f"  ⚠️  {kennung}: {e}")
            continue
        kasten = im.getchannel("A").getbbox()  # durchsichtigen Rand weg, sonst steht die Flasche winzig da
        if kasten:
            im = im.crop(kasten)
        im.thumbnail((int(GROESSE * .8), int(GROESSE * .86)), Image.LANCZOS)
        grund = Image.new("RGBA", (GROESSE, GROESSE), (255, 255, 255, 255))
        grund.alpha_composite(im, ((GROESSE - im.width) // 2, (GROESSE - im.height) // 2))
        grund.convert("RGB").save(ZIEL / f"{kennung}.jpg", quality=82, optimize=True, progressive=True)
        alle.append(kennung)
    print(f"→ {len(alle)} Produktfotos in {ZIEL.relative_to(WS)}")

    # Kontaktbogen zum Ansehen — alle Fotos, 10 je Zeile
    spalten, kachel = 10, 120
    bogen = Image.new("RGB", (spalten * kachel, ((len(alle) + spalten - 1) // spalten) * kachel), "white")
    for i, k in enumerate(alle):
        bogen.paste(Image.open(ZIEL / f"{k}.jpg").resize((kachel, kachel)), ((i % spalten) * kachel, (i // spalten) * kachel))
    bogen.save(ZIEL.parent.parent / "fotos-kontaktbogen.jpg", quality=80)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
