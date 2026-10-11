# -*- coding: utf-8 -*-
"""Nimmt Patricias CapCut-Export und legt die Remotion-Textebene exakt darueber.

🚨 Warum es das gibt (16.09.2026): Patricia — „machst du das ueber capcut? weil
dann muss ich nicht wegen jedem pups wieder schreiben, sondern kann die
schnittbalken selber nachjustieren." Genau richtig: Claude kann den Ton nicht
hoeren, also gehoert der Feinschnitt dorthin, wo jemand hoert. Claude macht die
Textebene, sie macht den Schnitt.

Der Weg:

  1. Die Abschnitte aus `clips/` in CapCut ziehen, der Reihe nach (01, 02, 03 …).
  2. Schnittbalken ziehen, bis es sich richtig anhoert. Nichts anderes aendern —
     KEINE Untertitel, KEINE Effekte, KEIN Text. Das kommt hier drueber.
  3. Exportieren: 1080×1920, 30 fps, nach `video/input/`.
  4. Dieses Skript laufen lassen:

       python scripts/videoschnitt/aus-capcut.py \
           --export video/input/<dein-capcut-export>.mp4 \
           --projekt video/output/2026-09-15-remotion-test

Was es tut: transkribiert den Export neu (lokal, faster-whisper) und baut die
Untertitel aus DIESEN Zeitstempeln. Dadurch sitzt die Textebene immer richtig,
egal wie weit Patricia die Balken verschoben hat.

**Darum wird neu transkribiert statt umgerechnet:** verschiebt sie einen Balken,
stimmen die alten Zeitstempel nicht mehr. Umrechnen hiesse raten, wo sie was
gezogen hat. Eine Minute Transkription ist billiger als eine falsche Textebene.

Die Zoom-Abschnitte findet ffmpeg selbst ueber die Szenenwechsel — Winkel A und B
sehen unterschiedlich genug aus. `--abschnitte fest` schaltet das ab und teilt in
gleich lange Stuecke.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transkribieren import audio_extrahieren, transkribieren, video_meta  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Ab diesem Unterschied gilt ein Bildwechsel als Schnitt.
SZENE = 0.30
# Kuerzer als das ist kein eigener Zoom-Abschnitt, sondern ein Flackern.
MIN_ABSCHNITT = 0.8


def szenen_finden(video, dauer):
    """Schnittstellen ueber ffmpeg-Szenenerkennung. Liest showinfo, nicht geraten."""
    p = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(video),
         "-vf", f"select='gt(scene,{SZENE})',showinfo", "-an", "-f", "null", "-"],
        capture_output=True, text=True, errors="replace")
    zeiten = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", p.stderr)]
    grenzen = [0.0]
    for z in sorted(zeiten):
        if z - grenzen[-1] >= MIN_ABSCHNITT and dauer - z >= MIN_ABSCHNITT:
            grenzen.append(round(z, 3))
    return grenzen


def feste_grenzen(dauer, laenge=3.5):
    g, t = [0.0], laenge
    while dauer - t >= MIN_ABSCHNITT:
        g.append(round(t, 3))
        t += laenge
    return g


def main():
    ap = argparse.ArgumentParser(description="CapCut-Export -> Remotion-Textebene")
    ap.add_argument("--export", required=True, help="Das aus CapCut exportierte MP4")
    ap.add_argument("--projekt", required=True, help="Ordner mit remotion/")
    ap.add_argument("--modell", default="small", help="faster-whisper-Modell")
    ap.add_argument("--abschnitte", choices=["szenen", "fest"], default="szenen",
                    help="Zoom-Abschnitte aus Szenenwechseln oder fest geteilt")
    a = ap.parse_args()

    export, projekt = Path(a.export).resolve(), Path(a.projekt).resolve()
    if not export.exists():
        sys.exit(f"Nicht gefunden: {export}")
    src = projekt / "remotion/src"
    public = projekt / "remotion/public"
    if not src.exists():
        sys.exit(f"Kein Remotion-Projekt unter {projekt}")
    public.mkdir(parents=True, exist_ok=True)

    meta = video_meta(export)
    dauer = float(meta["dauer"])
    print(f"Export: {export.name} · {dauer:.1f}s · {meta.get('breite')}×{meta.get('hoehe')}")
    if int(meta.get("breite", 0)) != 1080 or int(meta.get("hoehe", 0)) != 1920:
        print("  ⚠ Nicht 1080×1920 — in CapCut das Seitenverhaeltnis auf 9:16 stellen.")

    # --- Ton neu lesen -----------------------------------------------------
    print("Transkribiere (lokal, dauert etwa so lang wie das Video) …")
    wav = projekt / "_capcut.wav"
    audio_extrahieren(export, wav)
    woerter = transkribieren(wav, a.modell, "de")
    wav.unlink(missing_ok=True)

    captions = [{
        "text": w["wort"].replace("\u00df", "ss"),      # Schweizer ss
        "startMs": round(w["start"] * 1000),
        "endMs": round(w["ende"] * 1000),
    } for w in woerter]

    # --- Zoom-Abschnitte ---------------------------------------------------
    grenzen = (szenen_finden(export, dauer) if a.abschnitte == "szenen"
               else feste_grenzen(dauer))
    if len(grenzen) < 2:
        print("  Keine Szenenwechsel gefunden — teile fest.")
        grenzen = feste_grenzen(dauer)

    ziel_datei = "schnitt.mp4"
    shutil.copy2(export, public / ziel_datei)

    clips = []
    for i, g in enumerate(grenzen):
        bis = grenzen[i + 1] if i + 1 < len(grenzen) else dauer
        clips.append({
            "datei": ziel_datei,
            "winkel": "A" if i % 2 == 0 else "B",
            "dauer": round(bis - g, 3),
            "abSek": round(g, 3),
            "abDatei": round(g, 3),      # gleiche Stelle — es ist EIN Video
        })

    (src / "clips.json").write_text(
        json.dumps(clips, ensure_ascii=False, indent=1), encoding="utf-8")
    (src / "captions.json").write_text(
        json.dumps(captions, ensure_ascii=False, indent=1), encoding="utf-8")

    root = src / "Root.tsx"
    t = root.read_text(encoding="utf-8")
    # 🚨 Nicht auf "hat sich was geaendert" pruefen — steht dort schon dieselbe
    # Zahl, waere das ein falscher Alarm. Es zaehlt, ob die Zeile ueberhaupt da ist.
    if not re.search(r"const DURATION_S = [\d.]+;", t):
        sys.exit("DURATION_S in Root.tsx nicht gefunden — Projekt passt nicht.")
    root.write_text(
        re.sub(r"const DURATION_S = [\d.]+;", f"const DURATION_S = {dauer:.3f};", t),
        encoding="utf-8")

    print(f"\n{len(clips)} Zoom-Abschnitte · {len(captions)} Woerter · {dauer:.1f}s")
    print("\nText gegenlesen (die ersten Zeilen):")
    for c in captions[:14]:
        print(f"   {c['startMs']/1000:6.2f}  {c['text']}")
    print("\nJetzt:")
    print("  1. Rand pruefen:  python scripts/video-pruefung/rand-pruefen.py --takt 0.4")
    print("  2. Rendern:       npx remotion render Reel out/reel.mp4   (im remotion/-Ordner)")


if __name__ == "__main__":
    main()
