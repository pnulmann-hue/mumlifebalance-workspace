"""
Mama-CEO Modul 1 — Transkription aller 6 Videos (Willkommen + L1.1-L1.5)

Source: C:\\Users\\pnulm\\OneDrive\\Dokumente\\Zoom\\Mama CEO Modul 1
Output: context/Kurse/aktuelle kurse/Mama-CEO/Transkripte/ (txt + srt + json pro Video)

API-Key wird aus dem Julia-Trost-Skript wiederverwendet (Patricia's eigener Key).
"""

import os
import sys
import json
from pathlib import Path
from openai import OpenAI

# OpenAI-Key aus Patricia's .env (aktueller Workspace-Key)
import re
_env_path = Path(__file__).parents[2] / ".env"
_env_text = _env_path.read_text(encoding="utf-8", errors="replace")
_match = re.search(r"OPENAI_API_KEY=(sk-[A-Za-z0-9_-]+)", _env_text)
if not _match:
    print(f"FEHLER: OPENAI_API_KEY nicht gefunden in {_env_path}", file=sys.stderr)
    sys.exit(1)
API_KEY = _match.group(1)
client = OpenAI(api_key=API_KEY)

INPUT_DIR = Path(r"C:\Users\pnulm\OneDrive\Dokumente\Zoom\Mama CEO Modul 1")
OUTPUT_DIR = Path(r"C:\Users\pnulm\Desktop\Mein Business\context\Kurse\aktuelle kurse\Mama-CEO\Transkripte")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapping: Source-Datei -> Output-Basename
FILES = [
    ("Willkommen.mp4", "00-willkommen"),
    ("1,1 Mama-CEO.mp4", "01-lektion-1-1-was-ist-mama-ceo"),
    ("1,2 Deine Realität.mp4", "02-lektion-1-2-deine-realitaet"),
    ("1,3 3, Säulen.mp4", "03-lektion-1-3-die-3-saeulen"),
    ("1,4 4 Rollenwoche.mp4", "04-lektion-1-4-die-4-wochen-rollen"),
    ("1,5 Wochenrhytmus.mp4", "05-lektion-1-5-MASTERY-wochenrhythmus"),
]


def format_time_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(source_path, out_basename):
    """Schickt File an Whisper API, speichert txt/srt/json."""
    size_mb = source_path.stat().st_size / 1024 / 1024
    print(f"  Datei-Grösse: {size_mb:.1f} MB")

    if size_mb > 25:
        print(f"  WARNUNG: über 25 MB Whisper-Limit. Versuche trotzdem...")

    with open(source_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            language="de",
        )

    # TXT (Volltext)
    (OUTPUT_DIR / f"{out_basename}.txt").write_text(transcript.text, encoding="utf-8")

    # SRT (Untertitel mit Zeitstempeln)
    segments = transcript.segments if hasattr(transcript, "segments") else []
    if segments:
        with open(OUTPUT_DIR / f"{out_basename}.srt", "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                start = format_time_srt(seg.start)
                end = format_time_srt(seg.end)
                f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")

        # JSON (komplett mit Segments)
        with open(OUTPUT_DIR / f"{out_basename}.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "text": transcript.text,
                    "segments": [
                        {"start": s.start, "end": s.end, "text": s.text}
                        for s in segments
                    ],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    return len(transcript.text)


def main():
    print(f"=== Mama-CEO Modul 1 Transkription ===")
    print(f"Input:  {INPUT_DIR}")
    print(f"Output: {OUTPUT_DIR}\n")

    erfolg = 0
    fehler = 0

    for src_name, out_basename in FILES:
        src_path = INPUT_DIR / src_name
        print(f"[{src_name}]")

        if not src_path.exists():
            print(f"  FEHLT — überspringe.\n")
            fehler += 1
            continue

        # Skip wenn schon fertig
        out_txt = OUTPUT_DIR / f"{out_basename}.txt"
        if out_txt.exists() and out_txt.stat().st_size > 100:
            print(f"  Bereits transkribiert ({out_txt.stat().st_size} bytes) — skip.\n")
            erfolg += 1
            continue

        try:
            chars = transcribe(src_path, out_basename)
            print(f"  OK — {chars} Zeichen transkribiert\n")
            erfolg += 1
        except Exception as e:
            print(f"  FEHLER: {e}\n")
            fehler += 1

    print(f"=== ERGEBNIS ===")
    print(f"Erfolgreich: {erfolg}")
    print(f"Fehler:      {fehler}")
    print(f"Output:      {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
