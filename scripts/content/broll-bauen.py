#!/usr/bin/env python3
"""B-Roll bauen: ein Clip, ein Hook, sonst nichts.

Seit 19.09.2026 laeuft das ueber denselben Generator wie die Sprechreels
(`scripts/videoschnitt/textebene.py`). Vorher hatte das B-Roll ein eigenes
Textwerk aus ffmpeg-drawtext — schlichter Text ohne Schleier. Patricia am
19.09.: *„auch bei den anderen B-Roll Reels finde ich den Hook halt nicht
schoen"*, und als Referenz: *„das B-Roll vom 3 Wege ohne Namensliste finde
ich absolut super"*. Genau das ist die Textebene. Also gibt es jetzt **ein**
Textwerk statt zwei, und es ist das, das ihr gefaellt.

Mitgekommen sind damit: der weiche Schleier statt harter Kanten, die orange
Akzentzeile, die Zonenpruefung und die langsame Zoomfahrt.

🚨 Es gibt KEINE Vorgabe „mittig" mehr. Die alte Vorgabe war `--y 0 = mittig`,
und bei einem Hochformat-Video ist die Mitte das Gesicht. Genau so sind am
18.09. zehn KW39-B-Rolls mit dem Hook quer ueber Patricias Gesicht entstanden.
Entweder `--hoehe <prozent>` von Hand oder `--auto` — und danach das Standbild
wirklich anschauen.

🚨 Der Bauplan wird gespeichert (`bauplan.json`). Bei den ersten zehn war er
das nicht, und weil der Text eingebrannt ist, musste der Quellclip ueber
Bildvergleich zurueckgesucht werden (`quelle-finden.py`). Eine Korrektur ist
jetzt eine geaenderte Zahl, keine Rekonstruktion.

    python scripts/content/broll-bauen.py --clip 20260521_104644 \
        --ab 1.0 --dauer 7.0 --auto \
        --text "Kann mir mal jemand erklaeren, warum im Network alle so tun," \
        --betont "als waere der Anfang das Schwere?" \
        --name kw39-m-mo-b
    # Standbilder anschauen, dann dasselbe nochmal mit --rendern
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFont

WURZEL = pathlib.Path(__file__).resolve().parents[2]
EIN = WURZEL / "video" / "input"
AUS = WURZEL / "video" / "output" / "broll"
GENERATOR = WURZEL / "scripts" / "videoschnitt" / "textebene.py"
MESSSCHRIFT = WURZEL / "scripts" / "story-render" / "fonts" / "SourceSans3-Regular.ttf"

BREITE, HOEHE = 1080, 1920
# Instagram legt oben den Namen und unten Caption und Knoepfe darueber.
ZONE_OBEN = 12.5
ZONE_UNTEN = 82.0
# So setzt der Generator den Hook: 96 px Rand, 54 px Schrift, Zeilen mal 1.22.
INNEN = 96
SCHRIFT_PX = 54
ZEILE_PX = SCHRIFT_PX * 1.22


def lauf(befehl: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(befehl, check=True, **kw)


def dauer_von(p: pathlib.Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip())


# --- Hoehe des Textblocks schaetzen ----------------------------------------
# Nur eine Schaetzung: gemessen wird mit Source Sans, gesetzt wird in Poppins.
# Fuer die Platzwahl reicht das; die Abnahme bleibt das Standbild.

def zeilen_zahl(text: str, groesse: int = SCHRIFT_PX) -> int:
    if not text.strip():
        return 0
    font = ImageFont.truetype(str(MESSSCHRIFT), groesse)
    platz = BREITE - 2 * INNEN
    zeilen, laufend = 1, ""
    for wort in text.split():
        probe = (laufend + " " + wort).strip()
        if font.getlength(probe) > platz and laufend:
            zeilen += 1
            laufend = wort
        else:
            laufend = probe
    return zeilen


def block_prozent(text: str, betont: str) -> float:
    """Wie viel Prozent der Bildhoehe der ganze Hook einnimmt."""
    px = zeilen_zahl(text) * ZEILE_PX
    px += zeilen_zahl(betont, 62) * 62 * 1.22      # Akzentzeile ist groesser
    return px / HOEHE * 100


# --- Platz suchen ----------------------------------------------------------

def unruhe(clip: pathlib.Path, ab: float, dauer: float, bilder: int = 8) -> np.ndarray:
    """Pro Bildzeile ein Wert: wie unruhig es dort ist.

    Zwei Anteile, beide zeigen auf die Person und weg von der leeren Wand:
    **Struktur** (Helligkeitswechsel innerhalb der Zeile — Gesicht, Haare,
    Muster) und **Bewegung** (wie stark sich die Zeile ueber die Bilder
    veraendert — die Wand steht still, der Mensch nicht).
    """
    with tempfile.TemporaryDirectory() as tmp:
        stapel = []
        for i in range(bilder):
            t = ab + dauer * i / max(1, bilder - 1)
            ziel = pathlib.Path(tmp) / f"{i:02d}.png"
            lauf(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(clip),
                  "-frames:v", "1", "-vf",
                  f"scale={BREITE}:{HOEHE}:force_original_aspect_ratio=increase,"
                  f"crop={BREITE}:{HOEHE},scale=135:240", str(ziel)])
            stapel.append(np.asarray(Image.open(ziel).convert("L"), dtype=np.float64))

    a = np.stack(stapel)
    struktur = np.abs(np.diff(a.mean(axis=0), axis=1)).mean(axis=1)
    bewegung = a.std(axis=0).mean(axis=1)
    # Beide auf 0..1, damit keiner den anderen erschlaegt.
    def norm(v):
        s = v.max() - v.min()
        return (v - v.min()) / s if s else v * 0
    fein = norm(struktur) + norm(bewegung)
    return np.repeat(fein, HOEHE // len(fein))[:HOEHE]


def platz_suchen(clip: pathlib.Path, ab: float, dauer: float,
                 hoch_prozent: float) -> tuple[float, list[tuple[float, float]]]:
    w = unruhe(clip, ab, dauer)
    hoch = int(hoch_prozent / 100 * HOEHE)
    von, bis = int(ZONE_OBEN / 100 * HOEHE), int(ZONE_UNTEN / 100 * HOEHE) - hoch
    if bis <= von:
        sys.exit("Der Hook ist zu lang fuer die erlaubte Flaeche — kuerzen.")
    werte = [(float(w[y:y + hoch].mean()), y / HOEHE * 100) for y in range(von, bis, 8)]
    werte.sort()
    return werte[0][1], [(p, s) for s, p in werte[:3]]


# --- Bauen -----------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--clip", required=True, help="Dateiname in video/input ohne .mp4")
    p.add_argument("--ab", type=float, default=0.0)
    p.add_argument("--dauer", type=float, default=7.0)
    p.add_argument("--text", required=True, help="der Hook, weisse Zeilen")
    p.add_argument("--betont", default="", help="die Wendung, orange Serifenschrift")
    p.add_argument("--name", required=True)
    p.add_argument("--profil", default="mentoring", choices=["mentoring", "doterra"])
    p.add_argument("--hoehe", type=float, default=None,
                   help="Oberkante des Blocks in Prozent der Bildhoehe")
    p.add_argument("--auto", action="store_true",
                   help="ruhigste Stelle suchen statt von Hand setzen")
    p.add_argument("--zoom", type=float, default=1.06, help="1.0 = keine Fahrt")
    p.add_argument("--rendern", action="store_true",
                   help="ohne das gibt es nur Standbilder zum Anschauen")
    a = p.parse_args()

    quelle = EIN / (a.clip + ".mp4")
    if not quelle.exists():
        sys.exit(f"Nicht gefunden: {quelle}")
    if a.hoehe is None and not a.auto:
        sys.exit("Sag, wo der Hook hin soll: --hoehe <prozent> oder --auto.\n"
                 "Eine Vorgabe 'mittig' gibt es nicht mehr — die Mitte ist das Gesicht.")

    hoch = block_prozent(a.text, a.betont)
    if a.auto:
        beste, liste = platz_suchen(quelle, a.ab, a.dauer, hoch)
        a.hoehe = round(beste, 1)
        print("Ruhigste Stellen (Prozent von oben):  "
              + " · ".join(f"{pz:.0f} %" for pz, _ in liste))
        print(f"Gewaehlt: {a.hoehe} %")

    unten = a.hoehe + hoch
    if a.hoehe < ZONE_OBEN:
        sys.exit(f"Oberkante {a.hoehe:.1f} % liegt in der toten Zone (ab {ZONE_OBEN} %).")
    if unten > ZONE_UNTEN:
        sys.exit(f"Unterkante {unten:.1f} % liegt in der toten Zone (bis {ZONE_UNTEN} %).\n"
                 "Hook kuerzen oder hoeher setzen.")
    print(f"Block {a.hoehe:.1f} % bis {unten:.1f} % — tote Zonen frei.")

    ordner = AUS / a.name
    ordner.mkdir(parents=True, exist_ok=True)
    schnitt = ordner / "clip.mp4"
    lauf(["ffmpeg", "-v", "error", "-y", "-ss", f"{a.ab:.3f}", "-i", str(quelle),
          "-t", f"{a.dauer:.3f}", "-vf",
          f"scale={BREITE}:{HOEHE}:force_original_aspect_ratio=increase,"
          f"crop={BREITE}:{HOEHE}", "-r", "30",
          "-c:v", "libx264", "-preset", "medium", "-crf", "18",
          "-pix_fmt", "yuv420p", "-c:a", "aac", str(schnitt)])

    spec = {
        "video": str(schnitt.relative_to(WURZEL)).replace("\\", "/"),
        "profil": a.profil,
        "zoom": ({"modus": "aus"} if a.zoom <= 1.0
                 else {"modus": "auto", "staerke": a.zoom, "fokus": "50% 45%"}),
        # B-Roll hat keinen gesprochenen Text.
        "untertitel": {"an": False},
        "hook": {
            "stil": "serif",
            "akzent": "orange",
            # Weicher Schleier statt Pille — das ist die Optik aus dem
            # 3-Wege-Reel, die Patricia als Referenz genannt hat.
            "grund": "verlauf",
            "position": a.hoehe,
            "oben": a.text,
            "betont": a.betont,
            "klein": "",
            # Der Aufruf steht bei einem B-Roll in der Caption, nicht im Bild.
            "zusatz": "",
            # 🚨 Hook ab Bild null, ohne Einblendung (Patricia, 29.09.2026).
            # Vorher 0.3 s Verzoegerung plus Fade: ganz lesbar erst nach ~1 s.
            "ab_sek": 0.0,
            "sofort": True,
        },
    }
    (ordner / "finish.json").write_text(
        json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
    (ordner / "bauplan.json").write_text(
        json.dumps(vars(a), indent=2, ensure_ascii=False), encoding="utf-8")

    lauf([sys.executable, str(GENERATOR), str(ordner / "finish.json"),
          "--rendern" if a.rendern else "--konzept"])

    if a.rendern:
        fertig = sorted((ordner / "finish" / "renders").glob("*.mp4"))[-1]
        ziel = AUS / (a.name + ".mp4")
        ziel.write_bytes(fertig.read_bytes())
        print(f"\nFertig: {ziel}")
        print("Jetzt noch: python scripts/video-pruefung/kante-suchen.py " + str(ziel))
    else:
        print(f"\nStandbilder: {ordner / 'finish' / 'konzept'}")
        print("Erst anschauen, dann dasselbe nochmal mit --rendern.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
