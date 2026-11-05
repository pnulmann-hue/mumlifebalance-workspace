"""Gepostete Reels: Video aus dem Cockpit raus, Instagram-Link und lokale Kopie bleiben.

Patricia am 04.11.2026: *„dass die videos selber aus dem cockpit verschwinden,
sobald sie gepostet sind und nur noch der link zu instagram dann kommt"*. Anlass: Der
Anhang-Speicher (1 GB) war zu 99,96 % voll, fast nur mit Videos.

Zwei Schritte, dazwischen arbeitet der Task `cockpit-daten-abgleich` (Schritt 4d):

    python scripts/cockpit/videos-archivieren.py --plan
    python scripts/cockpit/videos-archivieren.py --sichern <heruntergeladen.mp4> --reel <id>

`--plan` liest `outputs/cockpit/inhalte-roh/` (reels, freigaben, daten/clips) und
`abgleich/gepostet-zuordnung.json` und schreibt `abgleich/video-archiv-plan.json`.
`--sichern` prüft das heruntergeladene Original gegen `video/`, legt es nach
`video/archiv/`, wenn es dort noch nicht liegt, und schreibt das fertige Beitrags-Dokument
nach `abgleich/video-archiv-updates/<id>.json`.

🚨 **Gepostet heisst: auf Instagram gefunden oder von Patricia als gepostet markiert.**
Der Klick „In der App eingeplant" zählt nicht, der Beitrag kann dann noch offen sein.
Eine unsichere Zuordnung lässt das Video stehen, denn eine falsche löscht es am falschen Beitrag.

🚨 **Testreels bleiben.** Die besten nimmt Patricia später in den Feed, das Video wird
also noch gebraucht.

🚨 **Das Skript löscht nichts.** Löschen macht der Task, und erst nach `--sichern`.
"""

import datetime
import hashlib
import json
import pathlib
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ROH = ROOT / "outputs" / "cockpit" / "inhalte-roh"
ABGLEICH = ROOT / "outputs" / "cockpit" / "abgleich"
VIDEO = ROOT / "video"
ARCHIV = VIDEO / "archiv"
PLAN = ABGLEICH / "video-archiv-plan.json"
UPDATES = ABGLEICH / "video-archiv-updates"

# Unter diesem Wert ist die Zuordnung nur eine Vermutung über gemeinsame Wörter.
UNSCHARF_MIN = 0.6
BLOB = re.compile(r"/_blob/([0-9a-f]{32})")


def lies(pfad):
    return json.loads(pathlib.Path(pfad).read_text(encoding="utf-8"))


def ist_testreel(r, rid):
    return bool(r.get("trial") or r.get("testVon")
                or re.search(r"(^|-)trial(-|$)", rid)
                or rid.startswith("radar-")
                or re.search(r"TRIAL REEL", r.get("hinweis") or "", re.I))


def plan():
    for noetig in (ROH / "reels", ROH / "freigaben", ROH / "daten" / "clips.json",
                   ABGLEICH / "gepostet-zuordnung.json"):
        if not noetig.exists():
            sys.exit("🚨 %s fehlt. Erst aus dem Cockpit holen, sonst könnte ein "
                     "benutzter Clip gelöscht werden." % noetig)

    heute = datetime.date.today().isoformat()
    zuordnung = lies(ABGLEICH / "gepostet-zuordnung.json").get("zuordnung", {})
    reels = {p.stem: lies(p) for p in sorted((ROH / "reels").glob("*.json"))}
    freigaben = {p.stem: lies(p) for p in sorted((ROH / "freigaben").glob("*.json"))}

    clips = {c.get("asset") for c in lies(ROH / "daten" / "clips.json").get("clips", [])}
    wer = {}
    for rid, r in reels.items():
        m = BLOB.search(r.get("videourl") or "")
        if m:
            wer.setdefault(m.group(1), []).append(rid)
    ig_nutzung = {}
    for bid, z in zuordnung.items():
        ig_nutzung[z.get("igId")] = ig_nutzung.get(z.get("igId"), 0) + 1

    items, bleibt = [], []
    for rid, r in reels.items():
        m = BLOB.search(r.get("videourl") or "")
        if not m:
            continue
        asset = m.group(1)
        if ist_testreel(r, rid):
            continue
        f = freigaben.get(rid) or {}
        status = f.get("status") or (r.get("blotato") or {}).get("status") or ""
        z = zuordnung.get(rid)
        link, datum, quelle = "", "", ""

        if z:
            grund = None
            if z.get("unsicher"):
                grund = "Zuordnung unsicher: " + z["unsicher"]
            elif z.get("unscharf") and z["unscharf"] < UNSCHARF_MIN:
                grund = "Zuordnung unscharf (%s)" % z["unscharf"]
            elif z.get("typ") != "REELS":
                grund = "Instagram-Post ist kein Reel"
            elif ig_nutzung.get(z.get("igId"), 0) > 1:
                grund = "derselbe Post passt auf mehrere Beiträge"
            elif (z.get("datum") or "9") > heute:
                grund = "Datum liegt in der Zukunft"
            elif status in ("wartet", "zeitpunkt-vorbei", "zurueckgezogen"):
                grund = "Freigabe steht auf " + status
            if grund:
                bleibt.append({"reel": rid, "grund": grund})
                continue
            link, datum, quelle = z.get("link", ""), z.get("datum", ""), "instagram"
        elif status == "gepostet-von-hand":
            datum, quelle = r.get("datum", ""), "von-hand"
        else:
            continue

        andere = [x for x in wer.get(asset, []) if x != rid]
        if asset in clips:
            bleibt.append({"reel": rid, "grund": "Video liegt auch in der Clip-Ablage"})
            continue
        if andere:
            bleibt.append({"reel": rid, "grund": "Video hängt auch an " + ", ".join(andere)})
            continue
        items.append({"reel": rid, "asset": asset, "link": link, "datum": datum,
                      "quelle": quelle, "name": r.get("name", "")})

    ergebnis = {"stand": heute, "items": items, "bleibt": bleibt}
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Zum Archivieren: %d · bleibt vorerst: %d → %s" % (len(items), len(bleibt), PLAN))
    for x in items:
        print("  %s  %-24s %-10s %s" % (x["datum"] or "—", x["reel"], x["quelle"], x["link"]))
    for x in bleibt:
        print("  bleibt %-24s %s" % (x["reel"], x["grund"]))


def summe(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for stueck in iter(lambda: f.read(1 << 20), b""):
            h.update(stueck)
    return h.hexdigest()


def sichern(datei, reel):
    if not re.fullmatch(r"[A-Za-z0-9_.\-]+", reel):
        sys.exit("🚨 Ungültige Beitrags-Kennung: %s" % reel)
    datei = pathlib.Path(datei)
    if not datei.is_file() or datei.stat().st_size == 0:
        sys.exit("🚨 Keine Datei oder leer: %s. Video bleibt im Cockpit." % datei)
    soll = summe(datei)
    groesse = datei.stat().st_size

    gefunden = None
    for p in VIDEO.rglob("*"):
        if p.suffix.lower() in (".mp4", ".mov", ".webm") and p.is_file() \
                and p.stat().st_size == groesse and summe(p) == soll:
            gefunden = p
            break
    neu = False
    if not gefunden:
        ARCHIV.mkdir(parents=True, exist_ok=True)
        gefunden = ARCHIV / (reel + (datei.suffix or ".mp4"))
        if gefunden.exists():
            sys.exit("🚨 %s gibt es schon mit anderem Inhalt. Video bleibt im Cockpit." % gefunden)
        shutil.copyfile(datei, gefunden)
        if summe(gefunden) != soll:
            gefunden.unlink()
            sys.exit("🚨 Kopie stimmt nicht mit dem Original überein. Video bleibt im Cockpit.")
        neu = True

    eintrag = next((x for x in lies(PLAN).get("items", []) if x["reel"] == reel), None)
    if not eintrag:
        sys.exit("🚨 %s steht nicht im Plan. Video bleibt im Cockpit." % reel)

    # 🚨 Das Dokument schreibt das Skript, nie von Hand: Am 04.11. stand nach dem Abtippen
    # eine falsche Prüfsumme im Vermerk.
    jetzt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    daten = {"videourl": "", "igLink": eintrag.get("link", ""), "updatedAt": jetzt,
             "videoArchiv": {"pfad": gefunden.relative_to(ROOT).as_posix(), "sha256": soll,
                             "stand": datetime.date.today().isoformat()}}
    UPDATES.mkdir(parents=True, exist_ok=True)
    (UPDATES / (reel + ".json")).write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    print("%s: %s · %s → %s" % (reel, "neu kopiert" if neu else "lag schon lokal",
                                daten["videoArchiv"]["pfad"], UPDATES / (reel + ".json")))


def main():
    a = sys.argv[1:]
    if "--plan" in a:
        plan()
    elif "--sichern" in a and "--reel" in a:
        sichern(a[a.index("--sichern") + 1], a[a.index("--reel") + 1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
