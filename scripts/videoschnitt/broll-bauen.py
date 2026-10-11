# -*- coding: utf-8 -*-
"""Aus vorhandenem Material ein fertiges B-Roll-Reel bauen — Clip, Hook, ab ins Cockpit.

**Patricias Arbeitsteilung, 16.09.2026:**

> *„Bei B-roll sollst du ein video nehmen, schneiden, hook und ggfs. animationen drauf
> wos sinn ergibt und was sinn ergibt und ab ins cockpit. bei sprechreels brauche ich ne
> anleitung, was ich rein sprechen soll. ich lads ins cockpit hoch, du haust den text
> animationen nach kelsy schnitte usw. rein — so wie wirs geübt haben und haust es mir
> überarbeitet wieder ins cockpit"*

Also: **B-Roll ist ganz meine Sache.** Kein Dreh, kein Zuruf — ich nehme einen Clip aus
`video/input/`, schneide ihn, lege den Hook drauf und haenge ihn an den Beitrag.

## Die Form (aus `feedback_broll-ein-clip-ein-textblock`)

- **Ein einziger Clip**, rund sieben Sekunden. Kein Schnitt im Schnitt.
- **Der ganze Hook als EIN Textblock**, ohne Kasten dahinter — nur ein weicher Schatten,
  damit er auf hellem Material lesbar bleibt.
- **Das Video muss den Text nicht illustrieren.** Ein ruhiger Clip traegt einen harten
  Satz besser als eine Bebilderung.
- Text in der **Mitte**: oben 0–12.5 % und unten 82–100 % sind tote Zone, dort legt
  Instagram Caption und Bedienknöpfe drueber.

## Vor dem Schneiden: hinsehen

🚨 **Nie nach Dateinamen auswaehlen.** Am 16.09. habe ich vier Clips aus den
Vorschaubildern gegriffen; beim Vergroessern waren **zwei davon unbrauchbar** — einer
war ein fertiges Reel mit eingebrannten Untertiteln, einer zeigte eine warme
Umarmung statt Erschoepfung. Die Vorschaubilder liegen in
`context/content-assets/vorschau/`, ein Bild je Video. **Erst gross ansehen, dann
schneiden.**

    python scripts/videoschnitt/broll-bauen.py \\
        --quelle video/input/lv_0_20240425085411.mp4 \\
        --ab 2.0 --dauer 7 \\
        --hook "Magnesium, frueher ins Bett, weniger Kaffee. Und trotzdem liegst du um drei wach." \\
        --ziel video/output/broll/magnesium.mp4

Danach als Artifact-Anhang hochladen und `videourl` am Reel setzen.
"""
import argparse
import subprocess
import sys
import textwrap
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WURZEL = Path(__file__).resolve().parents[2]
SCHRIFT = WURZEL / "scripts" / "story-render" / "fonts" / "Philosopher-Bold.ttf"

BREITE, HOEHE = 1080, 1920
# Text in der Mitte: oberhalb 12.5 % und unterhalb 82 % liegt die tote Zone.
OBEN, UNTEN = int(HOEHE * 0.125), int(HOEHE * 0.82)


def umbrechen(text, zeichen=26):
    """Zeilen so brechen, dass ein Wort nie zerrissen wird."""
    return textwrap.wrap(text, width=zeichen, break_long_words=False,
                         break_on_hyphens=False)


def ffmpeg_text(s):
    """Fuer drawtext maskieren. Reihenfolge zaehlt: Backslash zuerst."""
    for a, b in (("\\", "\\\\"), (":", "\\:"), ("'", "’"),
                 ("%", "\\%"), (",", "\\,")):
        s = s.replace(a, b)
    return s


def szenenwechsel(pfad):
    """Sekunden, an denen das Bild umspringt. Schwelle 0.2 — bei 0.3 wurden am
    16.09. beide echten Wechsel uebersehen."""
    lauf = subprocess.run(
        ["ffmpeg", "-nostats", "-loglevel", "info", "-i", str(pfad),
         "-vf", "select='gt(scene,0.2)',metadata=print", "-f", "null", "-"],
        capture_output=True, text=True, errors="replace")
    import re as _re
    return [float(x) for x in _re.findall(r"pts_time:([0-9.]+)", lauf.stderr)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quelle", required=True)
    ap.add_argument("--ziel", required=True)
    ap.add_argument("--hook", required=True)
    ap.add_argument("--ab", type=float, default=0.0)
    ap.add_argument("--dauer", type=float, default=7.0)
    ap.add_argument("--groesse", type=int, default=74)
    args = ap.parse_args()

    if not SCHRIFT.is_file():
        sys.exit(f"Schrift fehlt: {SCHRIFT}")

    zeilen = umbrechen(args.hook)
    if len(zeilen) > 5:
        sys.exit(f"{len(zeilen)} Zeilen — der Hook ist fuer ein B-Roll zu lang. "
                 "Kuerzen oder Schrift kleiner.")

    zh = int(args.groesse * 1.32)
    block = len(zeilen) * zh
    start_y = (OBEN + UNTEN) // 2 - block // 2

    schrift = str(SCHRIFT).replace("\\", "/").replace(":", "\\:")
    filter_teile = [
        f"scale={BREITE}:{HOEHE}:force_original_aspect_ratio=increase",
        f"crop={BREITE}:{HOEHE}",
        # Leichte Abdunklung, damit heller Text auf hellem Material steht.
        "eq=brightness=-0.06:saturation=1.04",
    ]
    for i, zeile in enumerate(zeilen):
        y = start_y + i * zh
        filter_teile.append(
            f"drawtext=fontfile='{schrift}':text='{ffmpeg_text(zeile)}':"
            f"fontcolor=white:fontsize={args.groesse}:x=(w-text_w)/2:y={y}:"
            # Kein Kasten — nur Schatten. Ein Kasten wirkt wie eine Vorlage.
            f"shadowcolor=black@0.55:shadowx=3:shadowy=4"
        )

    # 🚨 Im Fenster darf KEIN Szenenwechsel liegen. Beim ersten Lauf am 16.09.
    # sassen in beiden Clips Schnitte mitten im Ausschnitt — aus „Diffusor“ wurden
    # nach vier Sekunden Oelflaeschchen, aus „Laptop“ eine Ruestszene in der Kueche.
    # Gesehen habe ich das erst am Standbild. Also prueft das Skript es selbst.
    wechsel = szenenwechsel(args.quelle)
    drin = [w for w in wechsel if args.ab < w < args.ab + args.dauer]
    if drin:
        sys.exit(
            "ABBRUCH: im Fenster %.1f–%.1f s liegt ein Szenenwechsel bei %s s.\n"
            "Ein B-Roll ist EIN Clip. Waehle ein Fenster dazwischen — "
            "Wechsel in dieser Datei: %s"
            % (args.ab, args.ab + args.dauer,
               ", ".join("%.1f" % w for w in drin),
               ", ".join("%.1f" % w for w in wechsel) or "keine"))

    ziel = Path(args.ziel)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    befehl = [
        "ffmpeg", "-loglevel", "error", "-y",
        "-ss", str(args.ab), "-i", args.quelle, "-t", str(args.dauer),
        "-vf", ",".join(filter_teile),
        "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-pix_fmt", "yuv420p", "-an",       # ohne Ton: die Musik kommt in der App
        str(ziel),
    ]
    subprocess.run(befehl, check=True)
    mb = ziel.stat().st_size / 1_048_576
    print(f"  {ziel}  ({mb:.1f} MB, {args.dauer:.0f} s, {len(zeilen)} Textzeilen)")
    for z in zeilen:
        print(f"     {z}")


if __name__ == "__main__":
    main()
