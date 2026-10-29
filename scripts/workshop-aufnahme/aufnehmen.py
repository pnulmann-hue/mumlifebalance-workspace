"""Nimmt auf, was der Rechner gerade abspielt (Zoom, Browser …), ohne Mikrofon.

    python scripts/workshop-aufnahme/aufnehmen.py --name 2026-10-29-business-auf-knopfdruck
    python scripts/workshop-aufnahme/aufnehmen.py --geraete      # Ausgabegeräte zeigen

Stoppen: Strg+C im Fenster — oder die Datei STOP in den Aufnahmeordner legen.
Gespeichert wird alle 5 Minuten ein eigenes Stück (stueck-001.wav …), ein Absturz
kostet also höchstens fünf Minuten. Am Ende fügt ffmpeg alles zu <name>.m4a zusammen.

Ablage AUSSERHALB des Repos (Videos\\Workshop-Aufnahmen) — fremder Ton gehört nie ins
öffentliche Repo. Braucht `pip install pyaudiowpatch` (WASAPI-Loopback).
"""
import argparse
import subprocess
import time
import wave
from pathlib import Path

import pyaudiowpatch as pyaudio

ZIEL = Path.home() / "Videos" / "Workshop-Aufnahmen"
STUECK_SEK = 300


def loopback_geraete(pa):
    return [pa.get_device_info_by_index(i) for i in range(pa.get_device_count())
            if pa.get_device_info_by_index(i).get("isLoopbackDevice")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=time.strftime("%Y-%m-%d-%H%M-aufnahme"))
    ap.add_argument("--geraet", type=int, help="Index aus --geraete (Vorgabe: Standard-Ausgabe)")
    ap.add_argument("--geraete", action="store_true")
    ap.add_argument("--sekunden", type=float, help="nur zum Testen: nach so vielen Sekunden aufhören")
    a = ap.parse_args()

    pa = pyaudio.PyAudio()
    if a.geraete:
        std = pa.get_default_wasapi_loopback()["index"]
        for d in loopback_geraete(pa):
            print(("* " if d["index"] == std else "  ") + f'{d["index"]:3}  {d["name"]}')
        return

    d = pa.get_device_info_by_index(a.geraet) if a.geraet is not None else pa.get_default_wasapi_loopback()
    rate, kan = int(d["defaultSampleRate"]), d["maxInputChannels"]
    ordner = ZIEL / a.name
    ordner.mkdir(parents=True, exist_ok=True)
    stop = ordner / "STOP"
    stop.unlink(missing_ok=True)

    stream = pa.open(format=pyaudio.paInt16, channels=kan, rate=rate, input=True,
                     input_device_index=d["index"], frames_per_buffer=rate // 10)
    print(f"🔴 Aufnahme läuft · {d['name']}\n   {ordner}\n   Stoppen: Strg+C oder Datei STOP in den Ordner legen")

    start, nr, wf, stueck_start = time.time(), 0, None, 0
    try:
        while not stop.exists():
            if a.sekunden and time.time() - start > a.sekunden:
                break
            if wf is None or time.time() - stueck_start > STUECK_SEK:
                if wf:
                    wf.close()
                nr += 1
                wf = wave.open(str(ordner / f"stueck-{nr:03}.wav"), "wb")
                wf.setnchannels(kan); wf.setsampwidth(2); wf.setframerate(rate)
                stueck_start = time.time()
                print(f"   {int((time.time()-start)//60):3} min · Stück {nr}", flush=True)
            # Stille kommt bei Loopback nicht an, wenn nichts spielt — darum nicht blockierend warten
            n = stream.get_read_available()
            if n:
                wf.writeframes(stream.read(n, exception_on_overflow=False))
            else:
                time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        if wf:
            wf.close()
        stream.stop_stream(); stream.close(); pa.terminate()

    stuecke = sorted(ordner.glob("stueck-*.wav"))
    liste = ordner / "liste.txt"
    liste.write_text("".join(f"file '{p.name}'\n" for p in stuecke), encoding="utf-8")
    ausgabe = ordner / f"{a.name}.m4a"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste),
                    "-c:a", "aac", "-b:a", "96k", str(ausgabe)], check=True)
    print(f"⏹ Gestoppt nach {int((time.time()-start)//60)} min → {ausgabe}")


if __name__ == "__main__":
    main()
