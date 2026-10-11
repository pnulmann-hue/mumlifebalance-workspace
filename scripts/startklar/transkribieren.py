"""
Transkribiert die fertigen Startklar-Videos ins Kurs-Wissensarchiv.

Die Aufnahmen liegen in OneDrive, die Transkripte gehoeren zu den anderen
Kursen unter context/Kurse/aktuelle kurse/Startklar/Transkripte/ - im selben
Format wie dort: eine .txt mit Fliesstext und eine .vtt mit Zeitmarken.

Aufruf:
  python scripts/startklar/transkribieren.py
  python scripts/startklar/transkribieren.py --modell medium   # genauer, langsamer
  python scripts/startklar/transkribieren.py --neu             # auch schon Fertiges
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = pathlib.Path(r"C:\Users\pnulm\OneDrive\Dokumente\Patricia\Arbeit&Politik\Business\Kurse\Startklar")
ZIEL = ROOT / "context" / "Kurse" / "aktuelle kurse" / "Startklar" / "Transkripte"


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def zeitmarke(s):
    st, rest = divmod(s, 3600)
    mi, se = divmod(rest, 60)
    return "%02d:%02d:%06.3f" % (st, mi, se)


# Die Titel stehen in den Briefings unter 03-canva-briefing/. Sie muessen hier
# stehen, weil das Cockpit Modul, Lektion und Titel aus dem DATEINAMEN liest
# (scripts/cockpit/kurse-indexieren.py, Muster "NN-lektion-M-L-titel").
TITEL = {
    "1.1": (1, "konto-anlegen-oder-umstellen"),
    "1.2": (2, "username-name-feld-profilbild"),
    "1.3": (3, "deine-bio-in-vier-zeilen"),
    "1.4": (4, "highlights-und-dein-link"),
    "1.5": (5, "konto-absichern"),
    "2.1": (6, "reel-beitrag-story-was-ist-was"),
    "2.2": (7, "dein-erstes-reel"),
    "2.3": (8, "dein-erstes-karussell"),
    "2.4": (9, "deine-erste-story"),
    "2.5": (10, "caption-hashtags-musik-cover"),
    "3.1": (11, "die-fuenf-network-fallen"),
    "3.2": (12, "dein-startplan-fuer-woche-eins"),
}
ABSCHLUSS = (13, "so-gehts-weiter")


def name_normalisieren(p):
    """'Startklar 1.3_2.mp4' -> '1.3'  ·  'So gehts weiter.mp4' -> 'abschluss'"""
    n = p.stem
    m = re.search(r"(\d)\.(\d)", n)
    if m:
        return "%s.%s" % (m.group(1), m.group(2))
    return "abschluss"


def dateiname(kurz):
    """'1.3' -> '03-lektion-1-3-deine-bio-in-vier-zeilen'"""
    if kurz in TITEL:
        nr, slug = TITEL[kurz]
        modul, lektion = kurz.split(".")
        return "%02d-lektion-%s-%s-%s" % (nr, modul, lektion, slug)
    nr, slug = ABSCHLUSS
    return "%02d-%s" % (nr, slug)


def umbenennen():
    """Bereits erzeugte Transkripte auf die Cockpit-Benennung bringen."""
    umgestellt = 0
    for alt in sorted(ZIEL.glob("*")):
        if alt.suffix.lower() not in (".txt", ".vtt"):
            continue
        kurz = alt.stem
        neu_stamm = dateiname(kurz) if (kurz in TITEL or kurz == "abschluss") else None
        if not neu_stamm:
            continue
        neu = alt.with_name(neu_stamm + alt.suffix)
        if neu == alt:
            continue
        alt.rename(neu)
        log("%s -> %s" % (alt.name, neu.name))
        umgestellt += 1
    log("%d Dateien umbenannt" % umgestellt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modell", default="small", help="small (Standard) oder medium")
    ap.add_argument("--neu", action="store_true", help="auch schon vorhandene neu machen")
    ap.add_argument("--umbenennen", action="store_true",
                    help="nur vorhandene Transkripte auf die Cockpit-Benennung bringen")
    args = ap.parse_args()

    if args.umbenennen:
        umbenennen()
        return

    videos = sorted(QUELLE.glob("*.mp4"))
    if not videos:
        log("Keine Videos in %s" % QUELLE)
        sys.exit(1)

    ZIEL.mkdir(parents=True, exist_ok=True)
    log("%d Videos, Modell %s -> %s" % (len(videos), args.modell, ZIEL))

    from faster_whisper import WhisperModel
    modell = WhisperModel(args.modell, device="cpu", compute_type="int8")

    for v in videos:
        kurz = name_normalisieren(v)
        stamm = dateiname(kurz)
        txt = ZIEL / ("%s.txt" % stamm)
        vtt = ZIEL / ("%s.vtt" % stamm)
        if txt.exists() and not args.neu:
            log("%s: schon da, uebersprungen" % kurz)
            continue

        log("%s: Ton holen (%s)" % (kurz, v.name))
        wav = pathlib.Path(tempfile.gettempdir()) / ("startklar-%s.wav" % kurz)
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-vn",
                        "-ar", "16000", "-ac", "1", "-y", str(wav)], check=True)

        log("%s: transkribieren" % kurz)
        segmente, info = modell.transcribe(str(wav), language="de", beam_size=1,
                                           vad_filter=True)

        zeilen_txt, zeilen_vtt = [], ["WEBVTT", ""]
        for s in segmente:
            text = s.text.strip()
            if not text:
                continue
            # Whisper liefert das deutsche ss - Patricia schreibt Schweizer ss
            text = text.replace("ß", "ss")
            zeilen_txt.append(text)
            zeilen_vtt.append("%s --> %s" % (zeitmarke(s.start), zeitmarke(s.end)))
            zeilen_vtt.append(text)
            zeilen_vtt.append("")

        kopf = "# Startklar %s\n\nQuelle: %s\nTranskribiert: %s (faster-whisper %s)\n\n---\n\n" % (
            kurz, v.name, time.strftime("%d.%m.%Y"), args.modell)
        txt.write_text(kopf + "\n".join(zeilen_txt) + "\n", encoding="utf-8")
        vtt.write_text("\n".join(zeilen_vtt), encoding="utf-8")
        try:
            wav.unlink()
        except Exception:
            pass
        log("%s: fertig, %d Abschnitte, %d Zeichen" % (kurz, len(zeilen_txt), len(" ".join(zeilen_txt))))

    log("Alles fertig. %d Dateien in %s" % (len(list(ZIEL.glob('*.txt'))), ZIEL))


if __name__ == "__main__":
    main()
