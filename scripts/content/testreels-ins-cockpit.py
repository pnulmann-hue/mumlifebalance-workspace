#!/usr/bin/env python3
"""Testreels November 2026 als Cockpit-Dokumente (Sammlung reels).

Liest outputs/reels/2026-11-testreels.json (die eine Quelle, dieselbe wie radar-brolls.py)
und schreibt je neues Paar zwei JSON-Dateien: radar-m-NN (A) und radar-m-NN-test-b (B,
testVon = A). Danach im Chat: ArtifactData batch set (neu) bzw. update (bestehend).

Mit --videos <map.json> traegt es videourl ein ({"radar-10-a": "/_blob/…", …}).

    python scripts/content/testreels-ins-cockpit.py --ziel <ordner> [--videos map.json]
"""
import datetime
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WURZEL = pathlib.Path(__file__).resolve().parents[2]
QUELLE = WURZEL / "outputs" / "reels" / "2026-11-testreels.json"
TAGS = "#mamabusiness #networkmarketingmama #mamaunternehmerin #mumlifebalance"
PRUEF = "Hook geprüft von hook-sperre.py (Prüfvermerk auf der Karte)"
# Die Hook-Sperre (seit 01.11.2026): ins Cockpit kommt nur, was bestanden hat.
import importlib.util
_spec = importlib.util.spec_from_file_location("sperre", WURZEL / "scripts" / "hooks" / "hook-sperre.py")
sperre = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sperre)


def main():
    ziel = pathlib.Path(sys.argv[sys.argv.index("--ziel") + 1])
    ziel.mkdir(parents=True, exist_ok=True)
    videos = {}
    if "--videos" in sys.argv:
        videos = json.loads(pathlib.Path(sys.argv[sys.argv.index("--videos") + 1]).read_text(encoding="utf-8"))
    jetzt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
    n, gesperrt = 0, []
    for p in json.loads(QUELLE.read_text(encoding="utf-8"))["paare"]:
        if not p.get("neu") and "--alle" not in sys.argv:
            continue
        a_id = "radar-m-%s" % p["nr"]
        for teil in ("a", "b"):
            hook = " ".join(p[teil])
            rid = a_id if teil == "a" else a_id + "-test-b"
            ok, grund = sperre.freigabe(p, teil)
            if not ok:
                gesperrt.append("%s (%s)" % (rid, grund))
                continue
            d = dict(id=rid, name="🧪 Radar %s %s · %s" % (p["nr"], teil.upper(), p.get("rolle", "")),
                     profil="mentoring", videoart="broll", datum=p["datum"], hook=hook, unter="",
                     coverhook=hook, coverunter="", coverfarbe="dunkelblau" if teil == "a" else "orange",
                     caption=p["caption"] + "\n\n" + TAGS,
                     skript="Im Bild (ab Bild null): " + hook + "\nClip: " + p["clip"],
                     hinweis="🧪 TRIAL REEL — beim Posten in der App „Testreel“ einschalten. Rolle: %s · "
                             "gibt ihr mit: %s · Aufruf: %s · %s" % (p.get("rolle", ""), p.get("mit", ""), p["cta"], PRUEF),
                     rolle=p.get("rolle", ""), quelle="testreels-november", trial=True,
                     testVon="" if teil == "a" else a_id, testStand="offen", testGepostetAm="",
                     testReichweite=None, testKommentare=None, testNotiz="", testGewinner=False,
                     testInFeed=False, textfrei=False, abgelehnt=False, kommentar="", brand="mlb_dark",
                     scrim=True, pos="unten", texty=29, textskala=100, untertitel="", updatedAt=jetzt,
                     pruefung=p["pruefung"][teil])
            if not p.get("neu"):
                # bestehendes Dokument: nur Text, Prüfvermerk und Zeitstempel ändern (ArtifactData update)
                d = {k: d[k] for k in ("hook", "coverhook", "caption", "skript", "hinweis", "rolle",
                                         "pruefung", "updatedAt")}
            v = videos.get("radar-%s-%s" % (p["nr"], teil))
            if v:
                d["videourl"] = v
                d["videodatei"] = "radar-%s-%s.mp4" % (p["nr"], teil)
            (ziel / (rid + ".json")).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            n += 1
    print(n, "Dokumente nach", ziel)
    if gesperrt:
        print("GESPERRT, nicht geschrieben:")
        for g in gesperrt:
            print("  " + g)


if __name__ == "__main__":
    main()
