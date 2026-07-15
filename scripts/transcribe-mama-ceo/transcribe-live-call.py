"""
Mama-CEO Live-Call 2026-07-09 — Transkription (faster-whisper, lokal, CPU)

Source: OneDrive Zoom-Ordner (m4a-Audio, ~158 Min)
Output: context/Kurse/aktuelle kurse/Mama-CEO/Transkripte/2026-07-09-mama-ceo-call-live.txt

Schreibt FORTLAUFEND Segment fuer Segment in die .txt (partieller Fortschritt
ueberlebt Abbruch). Am Ende zusaetzlich .srt + .json mit Zeitstempeln.
"""

import json
import time
import os
from pathlib import Path
from faster_whisper import WhisperModel

AUDIO = Path(r"C:\Users\pnulm\OneDrive\Dokumente\Zoom\2026-07-09 09.03.39 Mama-CEO Call\audio1540461730.m4a")
OUT_DIR = Path(r"C:\Users\pnulm\Desktop\Mein Business\context\Kurse\aktuelle kurse\Mama-CEO\Transkripte")
OUT_DIR.mkdir(parents=True, exist_ok=True)
BASE = "2026-07-09-mama-ceo-call-live"

TXT = OUT_DIR / f"{BASE}.txt"
SRT = OUT_DIR / f"{BASE}.srt"
JSN = OUT_DIR / f"{BASE}.json"
PROG = OUT_DIR / f"{BASE}.progress.log"


def srt_time(sec):
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60); ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(PROG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    total_sec = 9499  # ~158 min, aus av-Probe
    log(f"Lade Modell medium (int8, CPU, {os.cpu_count()} Threads)...")
    model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    log("Modell geladen. Starte Transkription...")

    header = (
        "# Mama-CEO - Live-Call 2026-07-09 (Coaching/Strategie)\n"
        "# Transkript (faster-whisper medium, lokal; Roh-Transkript, ~158 Min)\n\n"
    )
    TXT.write_text(header, encoding="utf-8")

    segments, info = model.transcribe(
        str(AUDIO),
        language="de",
        beam_size=1,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    all_segs = []
    t0 = time.time()
    last_log = 0
    with open(TXT, "a", encoding="utf-8") as ftxt:
        for seg in segments:
            text = seg.text.strip()
            ftxt.write(text + " ")
            ftxt.flush()
            all_segs.append({"start": seg.start, "end": seg.end, "text": text})
            # alle ~60s Audiofortschritt loggen
            if seg.end - last_log >= 60:
                last_log = seg.end
                pct = 100 * seg.end / total_sec
                elapsed = time.time() - t0
                log(f"  {seg.end/60:5.1f} min Audio ({pct:4.1f}%) - {elapsed/60:.1f} min gerechnet")

    # SRT + JSON
    with open(SRT, "w", encoding="utf-8") as f:
        for i, s in enumerate(all_segs, 1):
            f.write(f"{i}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n{s['text']}\n\n")
    with open(JSN, "w", encoding="utf-8") as f:
        json.dump({"segments": all_segs}, f, ensure_ascii=False, indent=2)

    full = TXT.read_text(encoding="utf-8")
    log(f"FERTIG. {len(all_segs)} Segmente, {len(full)} Zeichen. Gesamtzeit: {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
