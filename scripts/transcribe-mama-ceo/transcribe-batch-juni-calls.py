"""
Mama-CEO Calls 15.6. + 30.6. — Batch-Transkription (faster-whisper, lokal, CPU).
Laeuft sequenziell. Output je Call: .txt (fortlaufend) + .srt + .json in
context/Kurse/aktuelle kurse/Mama-CEO/Transkripte/
"""
import json, time, os, glob
from pathlib import Path
from faster_whisper import WhisperModel

OUT_DIR = Path(r"C:\Users\pnulm\Desktop\Mein Business\context\Kurse\aktuelle kurse\Mama-CEO\Transkripte")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CALLS = [
    (r"C:\Users\pnulm\OneDrive\Dokumente\Zoom\2026-06-15 09.03.17 Mama-CEO Call", "2026-06-15-mama-ceo-call", 3240),
    (r"C:\Users\pnulm\OneDrive\Dokumente\Zoom\2026-06-30 20.02.32 Mama-CEO Call", "2026-06-30-mama-ceo-call", 5268),
]


def srt_time(sec):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int((sec%1)*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def log(prog, m):
    line=f"[{time.strftime('%H:%M:%S')}] {m}"; print(line, flush=True)
    with open(prog,"a",encoding="utf-8") as f: f.write(line+"\n")


def main():
    print(f"Lade Modell medium (int8, CPU, {os.cpu_count()} Threads)...", flush=True)
    model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    for folder, base, total in CALLS:
        m4as = glob.glob(os.path.join(folder, "*.m4a"))
        if not m4as:
            print(f"KEIN m4a in {folder} — skip", flush=True); continue
        audio = m4as[0]
        TXT=OUT_DIR/f"{base}.txt"; SRT=OUT_DIR/f"{base}.srt"; JSN=OUT_DIR/f"{base}.json"; PROG=OUT_DIR/f"{base}.progress.log"
        if TXT.exists() and TXT.stat().st_size > 500:
            log(PROG, f"{base} existiert bereits — skip"); continue
        log(PROG, f"=== START {base} ({audio}) ===")
        TXT.write_text(f"# Mama-CEO - Call {base[:10]}\n# Transkript (faster-whisper medium, lokal; Roh-Transkript)\n\n", encoding="utf-8")
        segments, info = model.transcribe(audio, language="de", beam_size=1, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
        all_segs=[]; t0=time.time(); last=0
        with open(TXT,"a",encoding="utf-8") as ftxt:
            for seg in segments:
                text=seg.text.strip(); ftxt.write(text+" "); ftxt.flush()
                all_segs.append({"start":seg.start,"end":seg.end,"text":text})
                if seg.end-last>=120:
                    last=seg.end; log(PROG, f"  {seg.end/60:5.1f} min ({100*seg.end/total:4.1f}%) - {(time.time()-t0)/60:.1f} min gerechnet")
        with open(SRT,"w",encoding="utf-8") as f:
            for i,s in enumerate(all_segs,1): f.write(f"{i}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n{s['text']}\n\n")
        with open(JSN,"w",encoding="utf-8") as f: json.dump({"segments":all_segs}, f, ensure_ascii=False, indent=2)
        log(PROG, f"FERTIG {base}. {len(all_segs)} Segmente, {(time.time()-t0)/60:.1f} min gerechnet")
    print("ALLE BATCH-CALLS FERTIG", flush=True)


if __name__ == "__main__":
    main()
