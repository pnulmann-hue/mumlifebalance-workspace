"""
Grafik-Ebene fuer ein Reel: erst Varianten als Standbild, dann bewegt bauen.

Nach Jenya Korks Kurs, Teil 4: „Lass dir immer zuerst Standbilder zeigen. Ein Bild
dauert Sekunden, ein fertiges Video Minuten." Und: Varianten zeigen, eine waehlen,
erst dann bewegt bauen.

Ein Reel-Projekt ist ein Ordner mit `grafik.json` (Props fuer src/Reel.tsx) und
dem Material, auf das `clips[].datei` zeigt. Der Ordner wird Remotions public-dir.

  python scripts/grafik/vorschau.py <projekt>              # A|B|C fuer Hook und Untertitel
  python scripts/grafik/vorschau.py <projekt> --stellen    # gewaehlter Stil an jeder Einblendung
  python scripts/grafik/vorschau.py <projekt> --pruefen    # Text am Bildrand? (laeuft vor jedem Render mit)
  python scripts/grafik/vorschau.py <projekt> --rendern    # fertiges MP4 nach <projekt>/renders/

Die Wahl steht in grafik.json unter `stil` ({"hook": "B", "untertitel": "A"}).
Danach Pflicht: scripts/video-pruefung/kante-suchen.py auf das MP4 und Standbilder anschauen.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = Path(__file__).resolve().parent
FPS = 30
VARIANTEN = ["A", "B", "C"]
NAMEN = {
    "hook": {"A": "Zwei Schriften", "B": "Kelsie, Wort fuer Wort", "C": "Balken"},
    "untertitel": {"A": "Zwei Schriften", "B": "Aktives Wort", "C": "Balken"},
}
# dieselben Rezepte wie scripts/videoschnitt/textebene.py — ein Klang klingt ueberall gleich
SOUNDS = {
    "klick": "anoisesrc=d=0.06:c=pink:a=0.6,highpass=f=1800,afade=t=out:st=0.005:d=0.055",
    "pop": "sine=frequency=520:duration=0.14,volume=0.8,afade=t=out:st=0.02:d=0.12",
    "whoosh": ("anoisesrc=d=0.45:c=white:a=0.45,bandpass=f=1100:width_type=o:w=2,"
               "afade=t=in:st=0:d=0.18,afade=t=out:st=0.2:d=0.25"),
    "ding": "sine=frequency=1180:duration=0.6,volume=0.5,afade=t=out:st=0.05:d=0.55",
}
NPX = "npx.cmd" if sys.platform == "win32" else "npx"


EIGENE_SOUNDS = HIER.parents[1] / "video" / "sounds"
# Rolle → Woerter im Dateinamen. Patricia legt Downloads einfach in video/sounds/ ab,
# umbenennen muss sie nichts (06.10.2026: pop · dramatic-youtube-intro · keyboard-typing · short-woosh).
ROLLEN = {
    "pop": ["pop"],
    "whoosh": ["whoosh", "woosh", "swoosh"],
    "typing": ["typing", "keyboard", "tipp", "tastatur"],
    "intro": ["intro"],
    "klick": ["klick", "click"],
    "ding": ["ding"],
}


def sounds_bereitstellen(projekt):
    """Je Rolle die passende Datei aus video/sounds/ nach <projekt>/sfx/<rolle>.wav.
    Fehlt eine, gibt es fuer klick/pop/whoosh/ding den ffmpeg-Ersatz; intro und typing
    gibt es nur als echte Datei. Rueckgabe: Liste der verfuegbaren Rollen."""
    ziel = projekt / "sfx"
    ziel.mkdir(exist_ok=True)
    dateien = sorted(EIGENE_SOUNDS.iterdir()) if EIGENE_SOUNDS.exists() else []
    da = []
    for rolle, woerter in ROLLEN.items():
        f = ziel / ("%s.wav" % rolle)
        eigen = [d for d in dateien if d.is_file() and any(w in d.name.lower() for w in woerter)]
        if eigen:
            q = eigen[0]
            if not f.exists() or f.stat().st_mtime < q.stat().st_mtime:
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(q), "-ac", "2", "-ar", "48000",
                                str(f)], check=True)
        elif rolle in SOUNDS:
            if not f.exists():
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", SOUNDS[rolle], "-ac", "2",
                                "-ar", "48000", str(f)], check=True)
        else:
            continue
        da.append(rolle)
    return da


def remotion(args, projekt, props):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as t:
        json.dump(props, t, ensure_ascii=False)
    cmd = [NPX, "remotion"] + args + ["--props=%s" % t.name, "--public-dir=%s" % projekt, "--log=error"]
    r = subprocess.run(cmd, cwd=HIER, capture_output=True, text=True, encoding="utf-8", errors="replace")
    Path(t.name).unlink(missing_ok=True)
    if r.returncode:
        sys.exit("Remotion-Fehler:\n%s" % (r.stderr or r.stdout)[-2500:])


def still(projekt, props, frame, ziel):
    remotion(["still", "src/index.ts", "Reel", str(ziel), "--frame=%d" % frame, "--scale=0.5",
              "--image-format=jpeg"], projekt, props)


def blatt(bilder, beschriftung, ziel):
    """Bilder nebeneinander mit Beschriftung darueber."""
    from PIL import Image, ImageDraw, ImageFont
    ims = [Image.open(b).convert("RGB") for b in bilder]
    w, h = ims[0].size
    kopf = 70
    out = Image.new("RGB", (w * len(ims) + 20 * (len(ims) - 1), h + kopf), (241, 236, 221))
    zeichne = ImageDraw.Draw(out)
    try:
        schrift = ImageFont.truetype("arialbd.ttf", 34)
    except Exception:
        schrift = ImageFont.load_default()
    for i, (im, txt) in enumerate(zip(ims, beschriftung)):
        x = i * (w + 20)
        out.paste(im, (x, kopf))
        zeichne.text((x + 14, 16), txt, fill=(12, 28, 48), font=schrift)
    out.save(ziel, quality=88)


def erste_untertitel_sek(p):
    hook = p.get("hookDauer", 4.2)
    for w in p["woerter"]:
        s = w["startMs"] / 1000
        if s >= hook + 0.2 and not any(e["abSek"] <= s <= e["abSek"] + e["dauer"] for e in p["einblendungen"]):
            return s + 0.25
    return hook + 0.5


def varianten(projekt, p):
    aus = projekt / "vorschau"
    aus.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    stil = dict(p.get("stil") or {})
    stellen = {"hook": int(1.6 * FPS), "untertitel": int(erste_untertitel_sek(p) * FPS)}
    for teil, frame in stellen.items():
        bilder = []
        for v in VARIANTEN:
            q = dict(p, stil=dict(stil, **{teil: v}))
            b = tmp / ("%s-%s.jpg" % (teil, v))
            still(projekt, q, frame, b)
            bilder.append(b)
        ziel = aus / ("%s-varianten.jpg" % teil)
        blatt(bilder, ["%s · %s" % (v, NAMEN[teil][v]) for v in VARIANTEN], ziel)
        print("✓ %s  (Sekunde %.1f)" % (ziel, frame / FPS))
    shutil.rmtree(tmp, ignore_errors=True)


def stellen(projekt, p):
    aus = projekt / "vorschau"
    aus.mkdir(exist_ok=True)
    punkte = [("hook", 1.6), ("untertitel", erste_untertitel_sek(p))]
    punkte += [("einblendung-%d" % (i + 1), e["abSek"] + 0.7) for i, e in enumerate(p["einblendungen"])]
    punkte.append(("schluss", p["dauer"] - 1.0))
    for name, sek in punkte:
        ziel = aus / ("%s.jpg" % name)
        still(projekt, p, int(sek * FPS), ziel)
        print("✓ %s  (Sekunde %.1f)" % (ziel, sek))


def rendern(projekt, p):
    # 🚨 Nie direkt in den Projektordner rendern: er ist Remotions public-dir, und eine
    # waehrend des Renders wachsende Datei darin bricht den Lauf ab (gefunden 06.10.2026).
    (projekt / "renders").mkdir(exist_ok=True)
    ziel = projekt / "renders" / "reel.mp4"
    tmp = Path(tempfile.mkdtemp()) / "reel.mp4"
    remotion(["render", "src/index.ts", "Reel", str(tmp), "--codec=h264", "--crf=17"], projekt, p)
    shutil.move(str(tmp), ziel)
    print("✓ %s" % ziel)
    print("→ jetzt: python scripts/video-pruefung/kante-suchen.py %s  und Standbilder anschauen" % ziel)


def videobild(projekt, p, sek, b=540, h=960):
    """Das Videobild zur Sekunde `sek` als Graustufen-Bytes (b×h), ohne Text."""
    for c in p["clips"]:
        if c["abSek"] <= sek < c["abSek"] + c["dauer"]:
            quelle = (c.get("abDatei") or 0) + (sek - c["abSek"])
            r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % quelle, "-i", str(projekt / c["datei"]),
                                "-frames:v", "1", "-vf",
                                "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,format=gray" % (b, h, b, h),
                                "-f", "rawvideo", "-"], capture_output=True)
            return r.stdout if len(r.stdout) == b * h else None
    return None


def gesicht_pruefen(projekt, p, textvideo, takt=0.4, b=540, h=960):
    """Liegt Text auf dem Gesicht? Gesicht per OpenCV im Videobild suchen, nach unten bis
    unters Kinn erweitern, und zaehlen, wie viele Textpixel (aus der nurText-Spur) darin liegen.
    Patricia 06.10.2026: „geht es, dass du das immer selber pruefst?" — ja, hiermit."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("⚠ Gesichts-Pruefung uebersprungen: pip install opencv-python-headless")
        return True
    erkenner = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(textvideo), "-vf",
                        "fps=%s,scale=%d:%d,format=gray" % (1 / takt, b, h), "-f", "rawvideo", "-"],
                       capture_output=True)
    n = b * h
    funde, ohne = [], []
    for i in range(len(r.stdout) // n):
        sek = i * takt
        text = np.frombuffer(r.stdout[i * n:(i + 1) * n], np.uint8).reshape(h, b)
        if (text > 60).sum() < 50:
            continue                       # gerade kein Text im Bild
        roh = videobild(projekt, p, sek, b, h)
        if roh is None:
            continue
        bild = np.frombuffer(roh, np.uint8).reshape(h, b)
        gesichter = erkenner.detectMultiScale(bild, 1.1, 5, minSize=(60, 60))
        if len(gesichter) == 0:
            ohne.append(sek)
            continue
        # Das Gesicht ist das OBERSTE Feld in der oberen Bildhaelfte — Haende vor dem Bauch
        # hielt der Erkenner am 06.10. fuer ein zweites Gesicht.
        oben = [g for g in gesichter if g[1] + g[3] / 2 < 0.6 * h]
        if not oben:
            ohne.append(sek)
            continue
        x, y, w, hh = min(oben, key=lambda g: g[1])
        # Das Erkennungsfeld endet etwa am Kinn; +12 % deckt das Kinn sicher ab.
        # (+38 % reichte bis zur Brust und meldete Text, der sauber darunter stand.)
        x0, x1 = max(0, int(x - 0.08 * w)), min(b, int(x + 1.08 * w))
        y0, y1 = max(0, int(y - 0.15 * hh)), min(h, int(y + 1.12 * hh))
        treffer = int((text[y0:y1, x0:x1] > 60).sum())
        if treffer > 40:
            funde.append((sek, treffer, round(y1 / h * 100)))
    ok = True
    if funde:
        ok = False
        print("✗ Text auf dem Gesicht an %d Stellen:" % len(funde))
        for sek, tr, kinn in funde[:15]:
            print("   Sekunde %5.1f  %d Textpixel im Gesicht (Kinn endet bei %d %% Bildhoehe)" % (sek, tr, kinn))
        print("   → Text tiefer setzen: stil.hoehe in grafik.json (Kinn-Wert + 2)")
    else:
        print("✓ kein Text auf dem Gesicht")
    if ohne:
        print("⚠ An %d Stellen mit Text kein Gesicht erkannt (abgewandt, Bewegung) — Sekunden %s: "
              "dort Standbild anschauen." % (len(ohne), ", ".join("%.1f" % s for s in ohne[:8])))
    return ok


def pruefen(projekt, p, takt=0.4, rand=24, schwelle=60):
    """Text am Bildrand? Rendert NUR die Textebene (nurText, schwarzer Grund) einmal als
    Video und misst je Stelle den hellsten Punkt in den aeusseren Pixeln — ueber Rohbytes,
    nie ueber geparste Werkzeug-Ausgaben (die alte signalstats-Pruefung meldete immer OK)."""
    tmp = Path(tempfile.mkdtemp()) / "nurtext.mp4"
    q = dict(p, nurText=True)
    remotion(["render", "src/index.ts", "Reel", str(tmp), "--codec=h264", "--crf=28", "--muted"], projekt, q)
    funde = []
    for seite, x in (("links", 0), ("rechts", 1080 - rand)):
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(tmp), "-vf",
                            "fps=%s,crop=%d:1920:%d:0,format=gray" % (1 / takt, rand, x),
                            "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
        roh, n = r.stdout, rand * 1920
        if not roh:
            sys.exit("Rand-Messung fehlgeschlagen: %s" % r.stderr.decode("utf-8", "replace")[:200])
        for i in range(len(roh) // n):
            m = max(roh[i * n:(i + 1) * n])
            if m > schwelle:
                funde.append((i * takt, seite, m))
    gesicht_ok = gesicht_pruefen(projekt, p, tmp, takt) if p.get("clips") else True
    shutil.rmtree(tmp.parent, ignore_errors=True)
    if funde:
        print("✗ Text am Rand an %d Stellen:" % len(funde))
        for sek, seite, m in sorted(funde)[:20]:
            print("   Sekunde %5.1f  %-6s  Helligkeit %d" % (sek, seite, m))
        return False
    print("✓ kein Text am Rand (alle %.1f s geprueft, Schwelle %d)" % (takt, schwelle))
    return gesicht_ok


def main():
    ap = argparse.ArgumentParser(description="Grafik-Ebene: Varianten, Stellen, Render")
    ap.add_argument("projekt")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--stellen", action="store_true")
    g.add_argument("--rendern", action="store_true")
    g.add_argument("--pruefen", action="store_true", help="Text am Bildrand? (vor jedem Render)")
    a = ap.parse_args()
    projekt = Path(a.projekt).resolve()
    p = json.loads((projekt / "grafik.json").read_text(encoding="utf-8"))
    if not (HIER / "node_modules").exists():
        sys.exit("Erst einmalig: cd scripts/grafik && npm install")
    p["toene"] = sounds_bereitstellen(projekt)
    # Intro zum Hook (Patricia 06.10.2026). Leise abgemischt (LAUT.intro), damit es ihre
    # ersten Worte nicht uebertoent. Abschalten je Reel: hook.intro = false in grafik.json.
    print("Intro: %s" % ("nein" if p["hook"].get("intro") is False else "ja"))
    print("Toene: %s" % ", ".join(p["toene"]))
    if a.pruefen:
        sys.exit(0 if pruefen(projekt, p) else 1)
    if a.rendern:
        if not pruefen(projekt, p):
            sys.exit("Erst Rand bzw. Gesicht korrigieren, dann rendern.")
        rendern(projekt, p)
    elif a.stellen:
        stellen(projekt, p)
    else:
        varianten(projekt, p)


if __name__ == "__main__":
    main()
