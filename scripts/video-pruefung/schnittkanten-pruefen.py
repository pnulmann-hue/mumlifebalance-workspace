"""Prueft die TONSPUR an jeder Schnittkante eines Remotion-Clip-Projekts.

🚨 Warum es das gibt (15.09.2026): Der Schnitt wurde nur nach Wort-Zeitstempeln
gebaut und nur visuell geprueft. Patricia: „das ist jetzt scheisse. hoerst du dir
die dinge ueberhaupt selber an?" — Nein, Claude kann nicht hoeren. Also wird
gemessen statt gehoert.

Was gemessen wird, je Clip:
  · Pegel in den ersten und letzten 120 ms
    laut am Rand = mitten im Wort oder Atemzug geschnitten -> klingt abgehackt
  · Stille am Anfang (die 250 ms Luft, die Patricias Regel verlangt)
  · Pegelsprung zwischen Clip-Ende und naechstem Clip-Anfang

Aufruf im Remotion-Projekt-Elternordner (dort, wo `clips/` liegt):
  python <repo>/scripts/video-pruefung/schnittkanten-pruefen.py
"""
import json
import math
import subprocess
import sys
from array import array
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ab hier gilt eine Schnittkante als „mitten im Wort"
LAUT = -14.0
# Darunter gilt es als Stille
STILL = -45.0


def pegel(datei, ab, dauer):
    """Spitzenpegel in dB fuer ein Stueck Tonspur.

    🚨 Liest ROHE Audio-Bytes und rechnet selbst. Die erste Fassung parste
    ffmpegs `volumedetect`-Ausgabe — die kam nie an, und die Pruefung meldete
    deshalb IMMER "sauber". Genau derselbe Fehler wie bei der Rand-Pruefung.
    Nie wieder Werkzeug-Ausgaben parsen, wenn man die Daten haben kann.
    """
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{ab}", "-t", f"{dauer}",
         "-i", str(datei), "-vn", "-ac", "1", "-ar", "16000",
         "-f", "s16le", "-acodec", "pcm_s16le", "-"],
        capture_output=True)
    roh = p.stdout
    if not roh or len(roh) < 4:
        return None
    werte = array("h")
    werte.frombytes(roh[: len(roh) // 2 * 2])
    spitze = max(abs(x) for x in werte) if werte else 0
    if spitze == 0:
        return -99.0
    return round(20 * math.log10(spitze / 32768), 1)


def d(x):
    return "  –  " if x is None else f"{x:5.1f}"


def main():
    clipdatei = Path("remotion/src/clips.json")
    if not clipdatei.exists():
        sys.exit("remotion/src/clips.json nicht gefunden — im Projektordner aufrufen.")
    clips = json.loads(clipdatei.read_text(encoding="utf-8"))
    ordner = Path("clips")

    print(f"{'#':>2}  {'Clip':12} {'Dauer':>6} {'Anf.':>6} {'Ende':>6} {'Luft':>6}  Befund")
    print("-" * 74)

    befunde = []
    letztes_ende = None
    for i, c in enumerate(clips, 1):
        f = ordner / c["datei"]
        if not f.exists():
            print(f"{i:2d}  {c['datei']:12}  FEHLT")
            continue
        anf = pegel(f, 0, 0.12)
        ende = pegel(f, max(0, c["dauer"] - 0.12), 0.12)
        luft = pegel(f, 0, 0.25)          # die 250 ms Vorlauf

        warn = []
        if anf is not None and anf > LAUT:
            warn.append("Anfang mitten im Wort")
        if ende is not None and ende > LAUT:
            warn.append("Ende abgeschnitten")
        if luft is not None and luft > -20:
            warn.append("keine Luft vor dem Satz")
        if letztes_ende is not None and anf is not None and abs(anf - letztes_ende) > 20:
            warn.append("harter Pegelsprung zum Vorclip")
        letztes_ende = ende

        if warn:
            befunde.append((i, c["datei"], warn))
        print(f"{i:2d}  {c['datei']:12} {c['dauer']:6.2f} {d(anf)} {d(ende)} {d(luft)}  "
              f"{' · '.join(warn) if warn else 'ok'}")

    print()
    if not befunde:
        print("OK — alle Schnittkanten sauber.")
        return 0
    print(f"🚨 {len(befunde)} von {len(clips)} Schnittkanten sind problematisch:")
    for i, name, warn in befunde:
        print(f"   Abschnitt {i} ({name}): {' · '.join(warn)}")
    print()
    print("Zum Nachjustieren: schnittliste.md aendern und den Schnitt neu bauen.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
