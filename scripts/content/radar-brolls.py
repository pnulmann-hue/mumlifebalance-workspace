#!/usr/bin/env python3
"""Die 60 Testreels November 2026 (2.11.-1.12.): je Tag ein Paar A und B, dieselbe Szene und
Caption, nur der Hook ist anders. Die eine Quelle fuer Hooks, Clips und Captions ist
outputs/reels/2026-11-testreels.json — ins Cockpit bringt sie testreels-ins-cockpit.py.

Patricia 31.10.: „bei allen videos bitte ein broll aus meiner sammlung nehmen. normale
alltagszenen ziehen gemäss erfahrung am besten.“ Deshalb nur Clips aus video/input, in
denen sie etwas tut und nicht in die Kamera schaut.

Gebaut wird mit derselben Mechanik wie kw42-brolls.py (Stil, Akzent, Aufruf als Chip am
Schluss) — die Funktion `bauen` kommt von dort, damit es eine Stelle gibt, nicht zwei.
A und B tragen denselben Stil: verglichen wird nur der Hook.

    python scripts/content/radar-brolls.py                     # Konzept-Standbilder
    python scripts/content/radar-brolls.py --rendern [name …]   # rendern, z.B. radar-10-a
    python scripts/content/radar-brolls.py --fehlend            # nur, was noch kein Video hat
"""
import importlib.util
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HIER = pathlib.Path(__file__).resolve().parent
WURZEL = HIER.parents[1]
QUELLE = WURZEL / "outputs" / "reels" / "2026-11-testreels.json"
spec = importlib.util.spec_from_file_location("kw42", HIER / "kw42-brolls.py")
kw42 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw42)

# Die Hook-Sperre (seit 01.11.2026): gebaut wird nur, was hook-sperre.py bestanden hat.
spec = importlib.util.spec_from_file_location("sperre", WURZEL / "scripts" / "hooks" / "hook-sperre.py")
sperre = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sperre)

REELS = []
for p in json.loads(QUELLE.read_text(encoding="utf-8"))["paare"]:
    for teil in ("a", "b"):
        text, betont = p[teil]
        ok, grund = sperre.freigabe(p, teil)
        REELS.append(dict(name="radar-%s-%s" % (p["nr"], teil), clip=p["clip"], ab=p["ab"],
                          dauer=p["dauer"], hoehe=p["hoehe"], stil=p["stil"], akzent=p["akzent"],
                          text=text, betont=betont, wort=p.get("wort_" + teil, ""),
                          zusatz=p["cta"], cta_y=68, frei=ok, sperrgrund=grund))


def hat_video(name):
    return any((kw42.AUS / name / "finish" / "renders").glob("*.mp4"))


def main():
    rendern = "--rendern" in sys.argv or "--fehlend" in sys.argv
    namen = [a for a in sys.argv[1:] if not a.startswith("--")]
    for r in REELS:
        if namen and r["name"] not in namen:
            continue
        if "--fehlend" in sys.argv and hat_video(r["name"]):
            continue
        if not r["frei"]:
            print(f"\n=== {r['name']} GESPERRT ({r['sperrgrund']}) — erst hook-sperre.py ===", flush=True)
            continue
        print(f"\n=== {r['name']} ===", flush=True)
        try:
            kw42.bauen(r, rendern)
        except Exception as e:  # ein kaputter Clip darf die anderen nicht aufhalten
            print(f"!!! {r['name']} gescheitert: {e}", flush=True)


if __name__ == "__main__":
    main()
