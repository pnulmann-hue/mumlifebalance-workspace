"""Sprachnachrichten und Videos aus den Rise-to-Lead-Gruppen abtippen (05.11.2026).

Holt nichts selbst: `npm --prefix scripts/telegram-userbot run rise-to-lead-audio` legt die Dateien
nach `video/telegram-calls/rise-to-lead/`. Dieses Skript tippt ab, was noch kein Transkript hat, und
schreibt es nach `video/telegram-calls/rise-to-lead/transkripte/` (alles gitignored, fremde Stimmen).
Whisper verhört sich bei Fachwörtern („Bogus“ = BOGO, „LAP“ = LRP) — nie eine Schreibweise daraus übernehmen.

    python scripts/doterra/rtl-abtippen.py
"""

import pathlib
import sys

from faster_whisper import WhisperModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORDNER = ROOT / "video/telegram-calls/rise-to-lead"
ZIEL = ORDNER / "transkripte"


def zeit(s):
    return "%02d:%02d" % (int(s) // 60, int(s) % 60)


def main():
    offen = [p for p in sorted(ORDNER.glob("*.*"))
             if p.suffix in (".m4a", ".mp4") and not (ZIEL / (p.stem + ".txt")).exists()]
    if not offen:
        print("Nichts abzutippen.")
        return
    ZIEL.mkdir(parents=True, exist_ok=True)
    # Ist der Arbeitsspeicher knapp, scheitert das grosse Modell schon beim Laden (05.11.: 400 MB frei).
    try:
        modell = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    except RuntimeError as e:
        print("Grosses Modell geht nicht (%s), nehme small." % e)
        modell = WhisperModel("small", device="cpu", compute_type="int8")
    for p in offen:
        teile, _ = modell.transcribe(str(p), language="de", vad_filter=True)
        zeilen = ["[%s] %s" % (zeit(t.start), t.text.strip()) for t in teile]
        (ZIEL / (p.stem + ".txt")).write_text("\n".join(zeilen) + "\n", encoding="utf-8")
        print("✓", p.name, len(zeilen), "Zeilen")


if __name__ == "__main__":
    main()
