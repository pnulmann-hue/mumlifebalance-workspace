"""
Schritt 1 des /videoschnitt-Workflows: Rohvideo -> Transkript mit Wort-Zeitstempeln.

Laeuft komplett lokal (faster-whisper, CPU). Kein Upload, keine Kosten.

Erzeugt in video/transkripte/<slug>/:
  meta.json              Dauer, Aufloesung, FPS des Rohvideos
  words.json             jedes Wort mit Start-/End-Zeit
  transkript.srt         Untertitel-Datei (fuer CapCut-Import)
  transkript.txt         Fliesstext
  saetze.md              <- das liest Claude: nummerierte Saetze, Pausen, Take-Gruppen
  cutlist-vorschlag.json Vorschlag nach Regel "letzter vollstaendiger Take gewinnt"

Aufruf:
  python scripts/videoschnitt/transkribieren.py                      # neuestes Video in video/input/
  python scripts/videoschnitt/transkribieren.py video/input/reel.mp4
  python scripts/videoschnitt/transkribieren.py reel.mp4 --modell small
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Windows-Konsole auf UTF-8 stellen (sonst brechen Umlaute und Pfeile den Lauf ab)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "video" / "input"
TRANS_DIR = ROOT / "video" / "transkripte"

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mp3", ".m4a", ".wav"}

# Pause (Sekunden), ab der ein neuer Satz beginnt, auch ohne Satzzeichen
PAUSE_GRENZE = 0.45
# Aehnlichkeit, ab der zwei Saetze als derselbe Take gelten
AEHNLICHKEIT = 0.72
# Wie weit nach vorne wird nach Wiederholungen gesucht
LOOKAHEAD_SAETZE = 8
LOOKAHEAD_SEK = 120.0


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def zeit(sec, ms=True):
    m = int(sec // 60)
    s = sec % 60
    return "%02d:%05.2f" % (m, s) if ms else "%02d:%02d" % (m, int(s))


def srt_zeit(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    msec = int(round((sec % 1) * 1000))
    if msec >= 1000:
        msec, s = 0, s + 1
    return "%02d:%02d:%02d,%03d" % (h, m, s, msec)


def slugify(name):
    s = name.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "video"


def neustes_input():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    kandidaten = [p for p in INPUT_DIR.iterdir()
                  if p.is_file() and p.suffix.lower() in VIDEO_EXT]
    if not kandidaten:
        return None
    return max(kandidaten, key=lambda p: p.stat().st_mtime)


def video_meta(pfad):
    cmd = ["ffprobe", "-v", "error", "-print_format", "json",
           "-show_format", "-show_streams", str(pfad)]
    roh = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    meta = {"datei": str(pfad), "dauer": float(roh["format"].get("duration", 0))}
    for st in roh.get("streams", []):
        if st.get("codec_type") == "video" and "breite" not in meta:
            meta["breite"] = st.get("width")
            meta["hoehe"] = st.get("height")
            fr = st.get("r_frame_rate", "0/1")
            try:
                a, b = fr.split("/")
                meta["fps"] = round(float(a) / float(b), 3) if float(b) else None
            except Exception:
                meta["fps"] = None
        if st.get("codec_type") == "audio" and "audio_rate" not in meta:
            meta["audio_rate"] = st.get("sample_rate")
            meta["audio_kanaele"] = st.get("channels")
    return meta


def audio_extrahieren(video, ziel_wav):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
           "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(ziel_wav)]
    subprocess.run(cmd, check=True)


def transkribieren(wav, modell, sprache):
    from faster_whisper import WhisperModel
    log("Lade Whisper-Modell '%s' (CPU, int8, %d Threads) ..." % (modell, os.cpu_count()))
    m = WhisperModel(modell, device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    log("Modell geladen. Transkribiere mit Wort-Zeitstempeln ...")
    segments, info = m.transcribe(
        str(wav), language=sprache, beam_size=5, word_timestamps=True,
        vad_filter=True, vad_parameters=dict(min_silence_duration_ms=300),
        condition_on_previous_text=False,
    )
    woerter = []
    letzte_meldung = 0.0
    for seg in segments:
        for w in (seg.words or []):
            text = w.word.strip()
            if not text:
                continue
            woerter.append({"wort": text, "start": round(w.start, 3), "ende": round(w.end, 3)})
        if seg.end - letzte_meldung >= 30:
            letzte_meldung = seg.end
            log("  ... %s Audio verarbeitet" % zeit(seg.end, ms=False))
    return woerter


def normalisieren(text):
    s = text.lower()
    for a, b in [("ä", "a"), ("ö", "o"), ("ü", "u"), ("ß", "ss")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def neuanlauf_splitten(gruppe):
    """Trennt Neuanlaeufe: 'Aber du hast keine ... Aber du hast kein Thema ...'

    Wenn der Satzanfang mitten im Satz noch einmal auftaucht, hat Patricia neu
    angesetzt. Ohne diese Trennung landen Fehlversuch und guter Take in einem
    Block und die Doppel-Erkennung sieht sie nie.
    """
    if len(gruppe) < 5:
        return [gruppe]
    klein = [normalisieren(w["wort"]) for w in gruppe]
    anfang = [x for x in klein[:2] if x]
    if len(anfang) < 2:
        return [gruppe]
    n = len(anfang)
    for i in range(2, len(klein) - n + 1):
        if klein[i:i + n] == anfang:
            return [gruppe[:i]] + neuanlauf_splitten(gruppe[i:])
    return [gruppe]


def saetze_bauen(woerter):
    roh, aktuell = [], []
    for w in woerter:
        if aktuell and (w["start"] - aktuell[-1]["ende"]) > PAUSE_GRENZE:
            roh.append(aktuell)
            aktuell = []
        aktuell.append(w)
        if re.search(r"[.!?]$", w["wort"]) or len(aktuell) >= 30:
            roh.append(aktuell)
            aktuell = []
    if aktuell:
        roh.append(aktuell)

    saetze = []
    for gruppe in roh:
        saetze.extend(neuanlauf_splitten(gruppe))

    ergebnis = []
    for idx, gruppe in enumerate(saetze):
        text = " ".join(x["wort"] for x in gruppe)
        text = re.sub(r"\s+([,.!?;:])", r"\1", text)
        start, ende = gruppe[0]["start"], gruppe[-1]["ende"]
        pause_davor = round(start - ergebnis[-1]["ende"], 2) if ergebnis else round(start, 2)
        ergebnis.append({
            "nr": idx + 1,
            "start": start,
            "ende": ende,
            "dauer": round(ende - start, 2),
            "pause_davor": pause_davor,
            "text": text,
            "norm": normalisieren(text),
            "woerter": len(gruppe),
            "vollstaendig": bool(re.search(r"[.!?]$", text)),
        })
    return ergebnis


def take_gruppen(saetze):
    """Findet wiederholte Saetze (mehrere Takes desselben Satzes) per Union-Find."""
    eltern = list(range(len(saetze)))

    def find(x):
        while eltern[x] != x:
            eltern[x] = eltern[eltern[x]]
            x = eltern[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            eltern[max(ra, rb)] = min(ra, rb)

    for i, s in enumerate(saetze):
        if len(s["norm"].split()) < 3:
            continue
        for j in range(i + 1, min(i + 1 + LOOKAHEAD_SAETZE, len(saetze))):
            t = saetze[j]
            if t["start"] - s["ende"] > LOOKAHEAD_SEK:
                break
            if len(t["norm"].split()) < 3:
                continue
            quote = difflib.SequenceMatcher(None, s["norm"], t["norm"]).ratio()
            # Auch Teil-Takes: abgebrochener Anfang steckt im spaeteren, laengeren Satz
            praefix = s["norm"][:max(12, len(s["norm"]) // 2)]
            teil = len(s["norm"]) >= 12 and t["norm"].startswith(praefix)
            if quote >= AEHNLICHKEIT or teil:
                union(i, j)

    gruppen = {}
    for i in range(len(saetze)):
        gruppen.setdefault(find(i), []).append(i)

    nummer = 0
    for wurzel in sorted(gruppen):
        mitglieder = gruppen[wurzel]
        if len(mitglieder) < 2:
            continue
        label = chr(ord("A") + nummer % 26)
        if nummer >= 26:
            label += str(nummer // 26)
        nummer += 1
        # Regel: der LETZTE vollstaendige Take gewinnt
        vollstaendige = [i for i in mitglieder if saetze[i]["vollstaendig"]]
        gewinner = (vollstaendige or mitglieder)[-1]
        for pos, i in enumerate(mitglieder, start=1):
            saetze[i]["gruppe"] = label
            saetze[i]["take"] = "%d/%d" % (pos, len(mitglieder))
            saetze[i]["behalten"] = (i == gewinner)

    for s in saetze:
        s.setdefault("gruppe", None)
        s.setdefault("take", None)
        s.setdefault("behalten", True)
    return saetze


def schreibe_srt(pfad, saetze):
    zeilen = []
    for i, s in enumerate(saetze, start=1):
        zeilen += [str(i), "%s --> %s" % (srt_zeit(s["start"]), srt_zeit(s["ende"])), s["text"], ""]
    pfad.write_text("\n".join(zeilen), encoding="utf-8")


def schreibe_saetze_md(pfad, saetze, meta, quelle):
    raus = [s for s in saetze if not s["behalten"]]
    zeilen = [
        "---",
        "tags: [videoschnitt, transkript]",
        "---",
        "",
        "# Transkript-Saetze — %s" % Path(quelle).name,
        "",
        "- Dauer Rohmaterial: **%s min** (%sx%s, %s fps)" % (
            zeit(meta.get("dauer", 0), ms=False), meta.get("breite"),
            meta.get("hoehe"), meta.get("fps")),
        "- Saetze erkannt: **%d**" % len(saetze),
        "- Davon als Doppel-Take markiert: **%d**" % len(raus),
        "",
        "Legende: `WEG` = Doppelung, ein spaeterer vollstaendiger Take desselben Satzes existiert.",
        "`?` = Satz endet ohne Satzzeichen, moeglicherweise abgebrochen.",
        "",
        "---",
        "",
    ]
    for s in saetze:
        marker = []
        if s["gruppe"]:
            marker.append("Take-Gruppe %s (%s)" % (s["gruppe"], s["take"]))
        if not s["behalten"]:
            marker.append("**WEG**")
        if not s["vollstaendig"]:
            marker.append("?")
        m = ("  ·  " + " · ".join(marker)) if marker else ""
        zeilen.append("**%03d**  `%s → %s`  (%.2fs, Pause davor %.2fs)%s" % (
            s["nr"], zeit(s["start"]), zeit(s["ende"]), s["dauer"], s["pause_davor"], m))
        zeilen.append("> " + s["text"])
        zeilen.append("")
    pfad.write_text("\n".join(zeilen), encoding="utf-8")


def schreibe_cutlist(pfad, saetze, quelle, meta):
    segmente = []
    for i, s in enumerate([x for x in saetze if x["behalten"]], start=1):
        segmente.append({
            "nr": i,
            "von_satz": s["nr"],
            "start": s["start"],
            "ende": s["ende"],
            "text": s["text"],
        })
    data = {
        "quelle": str(quelle),
        "dauer_quelle": meta.get("dauer"),
        "padding_vor": 0.12,
        "padding_nach": 0.35,
        "pause_max": 0.3,
        "regel": "letzter vollstaendiger Take gewinnt",
        "hinweis": ("Automatischer Vorschlag. Claude prueft ihn gegen "
                    "context/videoschnitt-regeln.md, bevor geschnitten wird."),
        "segmente": segmente,
    }
    pfad.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Rohvideo transkribieren (lokal, mit Wort-Zeitstempeln)")
    p.add_argument("video", nargs="?", help="Pfad zum Rohvideo (Standard: neuestes in video/input/)")
    p.add_argument("--modell", default="large-v3-turbo",
                   choices=["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"],
                   help="large-v3-turbo: Jenyas Empfehlung (Kurs Okt. 2026) — fast so genau wie "
                        "large-v3, ungefaehr so schnell wie medium; erster Lauf laedt ~1.6 GB")
    p.add_argument("--sprache", default="de")
    p.add_argument("--slug", help="Name des Transkript-Ordners (Standard: aus Dateiname)")
    args = p.parse_args()

    if args.video:
        video = Path(args.video)
        if not video.exists():
            video = INPUT_DIR / args.video
    else:
        video = neustes_input()
        if not video:
            sys.exit("Kein Video in %s gefunden. Leg dein Rohmaterial dort ab." % INPUT_DIR)
        log("Kein Pfad angegeben — nehme das neueste: %s" % video.name)

    if not video.exists():
        sys.exit("Datei nicht gefunden: %s" % video)

    slug = args.slug or slugify(video.stem)
    out = TRANS_DIR / slug
    out.mkdir(parents=True, exist_ok=True)

    log("Rohmaterial: %s" % video)
    meta = video_meta(video)
    log("Dauer %s min · %sx%s · %s fps" % (
        zeit(meta["dauer"], ms=False), meta.get("breite"), meta.get("hoehe"), meta.get("fps")))
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        log("Extrahiere Audio ...")
        audio_extrahieren(video, wav)
        t0 = time.time()
        woerter = transkribieren(wav, args.modell, args.sprache)
    log("%d Woerter in %.1f min transkribiert." % (len(woerter), (time.time() - t0) / 60))

    (out / "words.json").write_text(json.dumps(woerter, ensure_ascii=False, indent=1), encoding="utf-8")

    saetze = take_gruppen(saetze_bauen(woerter))
    schreibe_srt(out / "transkript.srt", saetze)
    (out / "transkript.txt").write_text(" ".join(s["text"] for s in saetze), encoding="utf-8")
    schreibe_saetze_md(out / "saetze.md", saetze, meta, video)
    schreibe_cutlist(out / "cutlist-vorschlag.json", saetze, video, meta)

    doppel = sum(1 for s in saetze if not s["behalten"])
    netto = sum(s["dauer"] for s in saetze if s["behalten"])
    log("")
    log("FERTIG → %s" % out)
    log("  %d Saetze, davon %d als Doppel-Take markiert" % (len(saetze), doppel))
    log("  Rohmaterial %s min → Vorschlag ca. %s min" % (
        zeit(meta["dauer"], ms=False), zeit(netto, ms=False)))
    log("  Naechster Schritt: saetze.md lesen, Schnittliste freigeben, dann schnitt.py")


if __name__ == "__main__":
    main()
