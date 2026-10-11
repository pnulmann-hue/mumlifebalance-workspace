"""Schnittliste zum SELBER Nachjustieren — lesen, aendern, neu bauen.

🚨 Warum es das gibt (15.09.2026): Patricia — „das ist jetzt scheisse. hoerst du
dir die dinge ueberhaupt selber an? oder habe ich eine moeglichkeit, dass ich das
nachjustieren kann?" — Claude kann den Ton nicht hoeren. Also muss sie selbst
ran koennen, ohne durch Code zu steigen.

Zwei Schritte:

  1. LISTE SCHREIBEN (einmal, aus dem Transkript)
       python scripts/videoschnitt/kurzfassung.py liste \\
           --transkript nachbau/<slug>/words.json \\
           --ziel video/output/<projekt>/schnittliste.md

  2. LISTE AENDERN und BAUEN (beliebig oft)
       python scripts/videoschnitt/kurzfassung.py bauen \\
           --projekt video/output/<projekt> \\
           --roh video/input/<datei>.mp4

Die Liste ist eine schlichte Tabelle. Patricia aendert nur Zahlen und Zeilen:

  | an | Winkel | von | bis | was gesagt wird |
  |----|--------|-----|-----|-----------------|
  | ja | A      | 0.00 | 6.15 | In meinem ersten Network war ... |
  | nein | B    | 65.25 | 66.85 | Mehr Stunden, mehr Abende, |

  · `an` auf `nein` -> Abschnitt fliegt raus
  · `von`/`bis` in Sekunden aendern -> Schnitt verschiebt sich
  · Zeilen umsortieren -> Reihenfolge aendert sich

**Luft vor dem Satz** wird NICHT fest gerechnet, sondern gesucht: das Skript geht
vom Satzanfang rueckwaerts bis zur naechsten Stille, hoechstens 0.6 s. Eine feste
Zahl schnitt Patricia sonst mitten ins Einatmen.
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from array import array
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BLENDE = 0.04         # Sekunden Ton-Blende an jeder Schnittkante
STILL_DB = -38.0      # darunter gilt als Stille
LUFT_MAX = 0.60       # hoechstens so weit zurueck suchen
LUFT_MIN = 0.12       # aber mindestens so viel Luft lassen


def pegel(datei, ab, dauer):
    """Spitzenpegel in dB. Liest Rohbytes — nie Werkzeug-Ausgaben parsen."""
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{ab}", "-t", f"{dauer}", "-i", str(datei),
         "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-acodec", "pcm_s16le", "-"],
        capture_output=True)
    if not p.stdout or len(p.stdout) < 4:
        return None
    w = array("h")
    w.frombytes(p.stdout[: len(p.stdout) // 2 * 2])
    s = max(abs(x) for x in w) if w else 0
    return -99.0 if s == 0 else round(20 * math.log10(s / 32768), 1)


def luft_suchen(roh, satzanfang):
    """Geht vom Satzanfang rueckwaerts bis zur Stille, hoechstens LUFT_MAX.

    Zweiter Rueckgabewert sagt, ob wirklich Stille gefunden wurde. Wenn nicht,
    redet Patricia dort ohne Pause weiter — es gibt nichts zum Mitnehmen, und die
    Kante laesst sich nur von Hand entschaerfen. Das muss DASTEHEN, statt still
    auf LUFT_MIN zurueckzufallen und so zu tun, als sei alles in Ordnung.
    """
    schritt = 0.06
    zurueck = LUFT_MIN
    while zurueck <= LUFT_MAX:
        p = pegel(roh, max(0.0, satzanfang - zurueck), schritt)
        if p is not None and p < STILL_DB:
            return round(zurueck, 2), True
        zurueck += schritt
    return LUFT_MIN, False


# ---------------------------------------------------------------- Liste

def liste_schreiben(transkript, ziel, grenze):
    w = json.loads(Path(transkript).read_text(encoding="utf-8"))
    saetze, akt = [], []
    for x in w:
        akt.append(x)
        if re.search(r"[.!?]$", x["wort"]):
            saetze.append(akt); akt = []
    if akt:
        saetze.append(akt)

    zeilen = [
        "# Schnittliste — hier aenderst du den Schnitt",
        "",
        "`an` auf **nein** setzen laesst einen Abschnitt weg.",
        "`von` und `bis` sind Sekunden im Rohmaterial — Zahlen aendern verschiebt den Schnitt.",
        "Zeilen umsortieren aendert die Reihenfolge.",
        "**Winkel:** A = nah · B = weit.",
        "",
        "Danach neu bauen:",
        "",
        "```bash",
        "python scripts/videoschnitt/kurzfassung.py bauen --projekt <projektordner> --roh <rohvideo>",
        "```",
        "",
        "| an | Winkel | von | bis | was gesagt wird |",
        "|---|---|---|---|---|",
    ]
    for s in saetze:
        winkel = "A" if s[0]["start"] < grenze else "B"
        text = " ".join(x["wort"] for x in s).replace("|", "/")
        zeilen.append(f"| ja | {winkel} | {s[0]['start']:.2f} | {s[-1]['ende']:.2f} | {text} |")

    Path(ziel).write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"Geschrieben: {ziel}  ({len(saetze)} Abschnitte)")


# ---------------------------------------------------------------- Bauen

def liste_lesen(datei):
    abschnitte = []
    for z in Path(datei).read_text(encoding="utf-8").splitlines():
        if not z.startswith("|"):
            continue
        s = [x.strip() for x in z.strip("|").split("|")]
        if len(s) < 5 or s[0].lower() in ("an", "---"):
            continue
        if s[0].lower() not in ("ja", "j", "x"):
            continue
        try:
            abschnitte.append({"winkel": s[1].upper(), "von": float(s[2]),
                               "bis": float(s[3]), "text": s[4]})
        except ValueError:
            print(f"  Zeile uebersprungen (keine Zahl): {z[:60]}")
    return abschnitte


def bauen(projekt, roh, transkript):
    # 🚨 .resolve() ist Pflicht: ffmpegs concat-Liste loest relative Pfade
    # gegen den Ordner der LISTE auf, nicht gegen das Arbeitsverzeichnis.
    projekt, roh = Path(projekt).resolve(), Path(roh).resolve()
    abschnitte = liste_lesen(projekt / "schnittliste.md")
    if not abschnitte:
        sys.exit("Keine aktiven Abschnitte in schnittliste.md — steht ueberall 'nein'?")

    clips = projekt / "clips"
    public = projekt / "remotion/public"
    clips.mkdir(parents=True, exist_ok=True)
    public.mkdir(parents=True, exist_ok=True)
    for alt in list(clips.glob("*.mp4")) + list(public.glob("*.mp4")):
        alt.unlink()

    woerter = json.loads(Path(transkript).read_text(encoding="utf-8"))
    teile, captions, ohne_luft, jetzt = [], [], [], 0.0

    for i, a in enumerate(abschnitte, 1):
        luft, gefunden = luft_suchen(roh, a["von"])
        if not gefunden:
            ohne_luft.append(i)
        start = max(0.0, a["von"] - luft)
        ziel = clips / f"{i:02d}_{a['winkel']}.mp4"
        subprocess.run([
            "ffmpeg", "-loglevel", "error",
            "-i", str(roh), "-ss", f"{start}", "-t", f"{a['bis'] - start}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-force_key_frames", "expr:gte(t,0)",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
            # 🚨 Ton-Blende an BEIDEN Enden, 40 ms. Ein harter Schnitt setzt die
            # Wellenform mitten in der Schwingung ab — das knackt hoerbar, egal wie
            # sauber die Wortgrenze liegt. Zu kurz, um eine Silbe zu schlucken.
            #
            # 🚨 Warum ueber areverse und nicht afade=t=out: `-ss` steht hinter `-i`
            # (genaue Suche, sonst findet Remotion keine Bilder), und dabei behaelt
            # der Tonstrom seine ORIGINAL-Zeitstempel. `afade=t=out:st=1.7` auf einem
            # Strom, der bei Sekunde 65 beginnt, ist laengst vorbei — das Ergebnis
            # waren zehn KOMPLETT STUMME Dateien. `asetpts=PTS-STARTPTS` davor hat
            # nicht geholfen. Umdrehen, einblenden, zurueckdrehen rechnet in Samples
            # statt in Zeitstempeln und ist damit immun. Gemessen, nicht vermutet.
            "-af", f"afade=t=in:st=0:d={BLENDE},areverse,"
                   f"afade=t=in:st=0:d={BLENDE},areverse",
            "-vf", "scale=1080:1920", "-r", "30",
            "-avoid_negative_ts", "make_zero", "-reset_timestamps", "1",
            "-movflags", "+faststart", "-y", str(ziel),
        ], check=True)

        ist = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(ziel)], capture_output=True, text=True).stdout.strip())

        for w in woerter:
            if start <= w["start"] < a["bis"]:
                captions.append({
                    "text": w["wort"].replace("ß", "ss"),   # Schweizer ss
                    "startMs": round((jetzt + (w["start"] - start)) * 1000),
                    "endMs": round((jetzt + (w["ende"] - start)) * 1000),
                })

        teile.append({"datei": ziel.name, "winkel": a["winkel"],
                      "dauer": round(ist, 3), "abSek": round(jetzt, 3)})
        marke = "Luft" if gefunden else "KEINE Pause"
        print(f"  {i:2d}. {a['winkel']}  {ist:5.2f}s  ({marke} {luft:.2f}s)  {a['text'][:48]}")
        jetzt += ist

    for t in teile:
        shutil.copy2(clips / t["datei"], public / t["datei"])

    # --- EINE Datei zum Reinhoeren -----------------------------------------
    # 🚨 Zehn Dateien einzeln anzuhoeren ist der Grund, warum eine Runde 40 Minuten
    # dauert. Es gibt genau eine Datei: die hoert Patricia einmal durch und sagt,
    # welche Nummer klemmt. Dieselbe Datei zieht sie in CapCut, wenn sie selbst
    # ziehen will — ein Objekt statt zehn.
    liste = projekt / "_teile.txt"
    liste.write_text(
        "".join("file '" + (clips / x["datei"]).as_posix() + "'" + chr(10)
                for x in teile),
        encoding="utf-8")
    roh = projekt / "rohschnitt.mp4"
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", str(liste),
        "-c:v", "copy",
        # Pegel ueber das GANZE Stueck angleichen, nicht je Abschnitt: sonst hebt
        # ffmpeg einen leisen Abschnitt auf dasselbe Niveau wie einen lauten, und
        # genau dann springt es beim Schnitt.
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-movflags", "+faststart", "-y", str(roh),
    ], check=True)
    liste.unlink(missing_ok=True)

    src = projekt / "remotion/src"
    (src / "clips.json").write_text(json.dumps(teile, ensure_ascii=False, indent=1), encoding="utf-8")
    (src / "captions.json").write_text(json.dumps(captions, ensure_ascii=False, indent=1), encoding="utf-8")

    root = src / "Root.tsx"
    if root.exists():
        t = root.read_text(encoding="utf-8")
        root.write_text(re.sub(r"const DURATION_S = [\d.]+;",
                               f"const DURATION_S = {jetzt:.3f};", t), encoding="utf-8")

    print(f"\nGesamt {jetzt:.1f}s · {len(teile)} Abschnitte · {len(captions)} Woerter")
    if ohne_luft:
        nr = ", ".join(str(x) for x in ohne_luft)
        print()
        print(f"🚨 Abschnitt {nr}: vor dem Satz ist keine Pause im Rohmaterial.")
        print("   Das Skript kann dort nichts mitnehmen — die Kante klingt hart.")
        print("   Diese Abschnitte in CapCut von Hand ziehen (siehe CAPCUT.md).")
    print()
    print(f"Zum Reinhoeren (EINE Datei): {roh}")
    print()
    print("Jetzt pruefen:")
    print("  python scripts/video-pruefung/schnittkanten-pruefen.py      (Ton)")
    print("  python scripts/video-pruefung/rand-pruefen.py --takt 0.4    (Bild, im remotion/-Ordner)")


def main():
    p = argparse.ArgumentParser(description="Schnittliste schreiben und daraus bauen.")
    u = p.add_subparsers(dest="was", required=True)

    a = u.add_parser("liste", help="Schnittliste aus dem Transkript schreiben")
    a.add_argument("--transkript", required=True)
    a.add_argument("--ziel", required=True)
    a.add_argument("--grenze", type=float, required=True,
                   help="Sekunde, ab der Winkel B beginnt")

    b = u.add_parser("bauen", help="Clips aus der geaenderten Liste bauen")
    b.add_argument("--projekt", required=True)
    b.add_argument("--roh", required=True)
    b.add_argument("--transkript", required=True)

    args = p.parse_args()
    if args.was == "liste":
        liste_schreiben(args.transkript, args.ziel, args.grenze)
    else:
        bauen(args.projekt, args.roh, args.transkript)


if __name__ == "__main__":
    main()
