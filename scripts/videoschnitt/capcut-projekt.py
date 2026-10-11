"""
Rohschnitt als CapCut-Projekt — und die Korrekturen daraus zurücklesen.

Nach Jenya Korks Kurs „Dein Videoeditor ist Claude" (Teil 3, Okt. 2026):
Claude legt den Rohschnitt direkt als CapCut-Projekt an, Patricia zieht die
Kanten nach, und danach liest Claude ihre Änderungen aus der Projektdatei und
schlägt daraus Regeln vor.

Der Unterschied zu clips/01.mp4 …: Jedes Stück im Projekt zeigt auf das
ORIGINAL-Video. Eine Kante lässt sich deshalb in beide Richtungen aufziehen —
bei einem fertig geschnittenen Clip ist hinter der Kante nichts mehr.

Aufruf:
  python scripts/videoschnitt/capcut-projekt.py anlegen video/transkripte/<slug>/cutlist.json
  python scripts/videoschnitt/capcut-projekt.py vergleichen video/transkripte/<slug>/cutlist.json

🚨 CapCut muss beim Anlegen GESCHLOSSEN sein, sonst überschreibt es beim Beenden
   seine Projektliste und das neue Projekt ist weg. Beim Vergleichen ebenfalls,
   sonst liegt der letzte Stand noch nicht in der Datei.

Die Vorlage ist das jüngste eigene CapCut-Projekt mit mindestens einem Video —
sie wird nur gelesen. Im Repo liegt bewusst keine Vorlage: die Projektdateien
tragen Geräte-Kennungen.
"""
import argparse
import copy
import importlib.util
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = Path(__file__).resolve().parent
ROOT = HIER.parents[1]
DRAFTS = Path(os.environ.get("LOCALAPPDATA", "")) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
US = 1_000_000          # CapCut rechnet in Mikrosekunden
KANTE_MIN = 0.04        # kleinere Verschiebungen sind Zittern, keine Korrektur
REGEL_AB = 2            # Jenya: erst ab zwei gleichen Änderungen eine Regel

# schnitt.py wiederverwenden statt die Luft-Logik zu kopieren
_spec = importlib.util.spec_from_file_location("schnitt", HIER / "schnitt.py")
schnitt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(schnitt)


def neu_id():
    return str(uuid.uuid4()).upper()


def capcut_laeuft():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout
        return "capcut.exe" in out.lower()
    except Exception:
        return False


def lies(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def schreib(p, daten):
    """Erst in eine Nebendatei, dann tauschen — ein Fehler leert nie die echte Datei."""
    p = Path(p)
    tmp = p.with_suffix(p.suffix + ".neu")
    tmp.write_text(json.dumps(daten, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, p)


def vorlage_finden():
    beste = None
    for d in DRAFTS.iterdir() if DRAFTS.exists() else []:
        f = d / "draft_content.json"
        if not f.is_file():
            continue
        try:
            c = lies(f)
        except Exception:
            continue
        if any(t.get("type") == "video" and t.get("segments") for t in c.get("tracks", [])):
            if beste is None or f.stat().st_mtime > beste[1]:
                beste = (d, f.stat().st_mtime)
    if not beste:
        sys.exit("Keine Vorlage gefunden. Leg in CapCut einmal ein Projekt mit irgendeinem Video an, "
                 "schliess CapCut und starte nochmal.")
    return beste[0]


def segmente_mit_luft(cut_pfad):
    cutlist = lies(cut_pfad)
    haupt = cutlist.get("quelle")
    quellen = {}
    for s in cutlist["segmente"]:
        roh = s.get("quelle") or haupt
        q = Path(roh) if Path(roh).exists() else ROOT / roh
        if not q.exists():
            sys.exit("Video nicht gefunden: %s" % roh)
        if roh not in quellen:
            quellen[roh] = (q.resolve(), schnitt.quelle_parameter(q))
        s["_quelle"], s["_dauer_quelle"] = quellen[roh][0], quellen[roh][1]["dauer"]
    seg = schnitt.segmente_pruefen(
        cutlist["segmente"],
        float(cutlist.get("padding_vor", schnitt.PADDING_VOR)),
        float(cutlist.get("padding_nach", schnitt.PADDING_NACH)))
    wp = Path(cutlist.get("words") or Path(cut_pfad).with_name("words.json"))
    if len(quellen) == 1 and wp.exists():
        seg = schnitt.pausen_kappen(seg, lies(wp), cutlist.get("pause_max", schnitt.PAUSE_MAX))
    return seg, {str(v[0]): v[1] for v in quellen.values()}


# ---------------------------------------------------------------- anlegen

def anlegen(cut_pfad, name):
    if capcut_laeuft():
        sys.exit("CapCut läuft noch. Bitte ganz schliessen (auch im Infobereich unten rechts) und nochmal starten.")
    segmente, par = segmente_mit_luft(cut_pfad)
    vorlage = vorlage_finden()
    ziel = DRAFTS / name
    if ziel.exists():
        sys.exit("Ein CapCut-Projekt „%s“ gibt es schon. Anderen Namen mit --name wählen." % name)

    print("Vorlage: %s" % vorlage.name)
    shutil.copytree(vorlage, ziel, ignore=shutil.ignore_patterns(
        ".locked", "*.bak", "*.tmp", "draft_cover.jpg", "subdraft", "qr_upload", "smart_crop", "matting"))

    c = lies(vorlage / "draft_content.json")
    spur = next(t for t in c["tracks"] if t.get("type") == "video" and t.get("segments"))
    seg0 = spur["segments"][0]
    mats = c["materials"]
    nach_id = {x["id"]: (k, x) for k, v in mats.items() if isinstance(v, list)
               for x in v if isinstance(x, dict) and "id" in x}
    video0 = nach_id[seg0["material_id"]][1]
    extras0 = [nach_id[r] for r in seg0.get("extra_material_refs", []) if r in nach_id]

    neu_mats = {k: ([] if isinstance(v, list) else v) for k, v in mats.items()}
    neue_segmente = []
    pos = 0
    for s in segmente:
        q = str(Path(s["_quelle"]).resolve())
        p = par[q]
        v = copy.deepcopy(video0)
        v.update({"id": neu_id(), "path": q.replace("\\", "/"), "material_name": Path(q).name,
                  "duration": int(p["dauer"] * US), "width": p["breite"], "height": p["hoehe"],
                  "has_audio": p["hat_audio"]})
        neu_mats["videos"].append(v)
        refs = []
        for art, x in extras0:
            x = copy.deepcopy(x)
            x["id"] = neu_id()
            neu_mats[art].append(x)
            refs.append(x["id"])
        dauer = int(round((s["ende"] - s["start"]) * US))
        sg = copy.deepcopy(seg0)
        sg.update({"id": neu_id(), "material_id": v["id"], "extra_material_refs": refs,
                   "source_timerange": {"start": int(round(s["start"] * US)), "duration": dauer},
                   "target_timerange": {"start": pos, "duration": dauer},
                   "keyframe_refs": [], "common_keyframes": []})
        neue_segmente.append(sg)
        pos += dauer

    spur = copy.deepcopy(spur)
    spur["id"] = neu_id()
    spur["segments"] = neue_segmente
    erst = par[str(Path(segmente[0]["_quelle"]).resolve())]
    c.update({"id": neu_id(), "duration": pos, "tracks": [spur], "materials": neu_mats,
              "keyframes": {k: [] for k in c.get("keyframes", {})}})
    c["canvas_config"] = dict(c.get("canvas_config") or {}, ratio="original",
                              width=erst["breite"], height=erst["hoehe"])

    # Zeitleisten-Ordner (CapCut 9 hält eine Kopie je Zeitleiste)
    tl_ordner = ziel / "Timelines"
    tl_id = c["id"]
    if (tl_ordner / "project.json").exists():
        pj = lies(tl_ordner / "project.json")
        alt = pj.get("main_timeline_id")
        if alt and (tl_ordner / alt).exists():
            (tl_ordner / alt).rename(tl_ordner / tl_id)
        for t in pj.get("timelines", []):
            if t.get("id") == alt:
                t["id"] = tl_id
        pj["timelines"] = [t for t in pj.get("timelines", []) if t.get("id") == tl_id]
        pj.update({"id": neu_id(), "main_timeline_id": tl_id})
        schreib(tl_ordner / "project.json", pj)
        for unter in tl_ordner.iterdir():
            if unter.is_dir() and unter.name != tl_id:
                shutil.rmtree(unter)
        (tl_ordner / tl_id).mkdir(exist_ok=True)
        schreib(tl_ordner / tl_id / "draft_content.json", c)
    schreib(ziel / "draft_content.json", c)

    # Titelbild aus dem ersten Stück
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % (segmente[0]["start"] + 0.3),
                    "-i", str(segmente[0]["_quelle"]), "-frames:v", "1", "-vf", "scale=360:-2",
                    str(ziel / "draft_cover.jpg")], check=False)

    jetzt_us = int(time.time() * US)
    fold = str(ziel).replace("\\", "/")
    m = lies(vorlage / "draft_meta_info.json")
    eintrag0 = ((m.get("draft_materials") or [{}])[0].get("value") or [{}])[0]
    medien = []
    for q, p in par.items():
        e = copy.deepcopy(eintrag0)
        e.update({"id": str(uuid.uuid4()), "file_Path": q.replace("\\", "/"), "extra_info": Path(q).name,
                  "duration": int(p["dauer"] * US), "width": p["breite"], "height": p["hoehe"],
                  "roughcut_time_range": {"start": 0, "duration": int(p["dauer"] * US)},
                  "create_time": int(time.time()), "import_time": int(time.time()), "import_time_ms": jetzt_us})
        medien.append(e)
    draft_id = neu_id()
    m.update({"draft_fold_path": fold, "draft_id": draft_id, "draft_name": name,
              "draft_materials": [{"type": 0, "value": medien}],
              "tm_duration": pos, "tm_draft_create": jetzt_us, "tm_draft_modified": jetzt_us,
              "draft_timeline_materials_size_": 0, "draft_segment_extra_info": [],
              "draft_materials_copied_info": []})
    schreib(ziel / "draft_meta_info.json", m)

    # In CapCuts Projektliste eintragen (vorher sichern)
    root = DRAFTS / "root_meta_info.json"
    shutil.copy2(root, root.with_suffix(".json.vor-claude"))
    r = lies(root)
    vor = next((e for e in r["all_draft_store"] if Path(e["draft_fold_path"]).name == vorlage.name),
               r["all_draft_store"][0])
    e = copy.deepcopy(vor)
    e.update({"draft_fold_path": fold, "draft_id": draft_id, "draft_name": name,
              "draft_cover": fold + "\\draft_cover.jpg", "draft_json_file": fold + "\\draft_content.json",
              "tm_duration": pos, "tm_draft_create": jetzt_us, "tm_draft_modified": jetzt_us,
              "draft_timeline_materials_size": 0})
    r["all_draft_store"].insert(0, e)
    r["draft_ids"] = len(r["all_draft_store"])
    schreib(root, r)

    # Merkzettel für den späteren Vergleich
    merk = Path(cut_pfad).with_name("capcut-schnitt.json")
    merk.write_text(json.dumps({
        "projekt": name, "ordner": fold, "angelegt": time.strftime("%Y-%m-%d %H:%M"),
        "segmente": [{"nr": s["nr"], "quelle": str(s["_quelle"]), "start": round(s["start"], 3),
                      "ende": round(s["ende"], 3), "text": s["text"]} for s in segmente]},
        ensure_ascii=False, indent=1), encoding="utf-8")

    print("✓ CapCut-Projekt „%s“ angelegt: %d Stücke, %.1f s" % (name, len(segmente), pos / US))
    print("  Merkzettel: %s" % merk)
    print("  Jedes Stück zeigt aufs Original — Kanten lassen sich in beide Richtungen aufziehen.")


# ---------------------------------------------------------------- vergleichen

def aktueller_stand(ordner):
    kandidaten = [ordner / "draft_content.json"] + list((ordner / "Timelines").glob("*/draft_content.json"))
    kandidaten = [k for k in kandidaten if k.is_file()]
    return lies(max(kandidaten, key=lambda k: k.stat().st_mtime))


def woerter_zwischen(words, von, bis):
    return " ".join(w["wort"] for w in words if w["start"] >= von - 0.02 and w["ende"] <= bis + 0.02)


def vergleichen(cut_pfad):
    if capcut_laeuft():
        sys.exit("CapCut läuft noch. Erst ganz beenden, sonst liegt dein letzter Stand nicht in der Datei.")
    merk = lies(Path(cut_pfad).with_name("capcut-schnitt.json"))
    ordner = Path(merk["ordner"])
    c = aktueller_stand(ordner)
    words_pfad = Path(cut_pfad).with_name("words.json")
    words = lies(words_pfad) if words_pfad.exists() else []

    nach_id = {x["id"]: x for v in c["materials"].values() if isinstance(v, list)
               for x in v if isinstance(x, dict) and "id" in x}
    ist = []
    for t in c["tracks"]:
        if t.get("type") != "video":
            continue
        for s in t["segments"]:
            st, tt = s["source_timerange"], s["target_timerange"]
            ist.append({"quelle": nach_id.get(s["material_id"], {}).get("path", ""),
                        "start": st["start"] / US, "ende": (st["start"] + st["duration"]) / US,
                        "pos": tt["start"] / US, "pos_ende": (tt["start"] + tt["duration"]) / US})
    ist.sort(key=lambda x: x["pos"])
    plan = merk["segmente"]

    def ueberlapp(a, b):
        if Path(a["quelle"]).name != Path(b["quelle"]).name:
            return 0
        return max(0.0, min(a["ende"], b["ende"]) - max(a["start"], b["start"]))

    for i in ist:
        kand = [(ueberlapp(i, p), p["nr"]) for p in plan]
        best = max(kand) if kand else (0, None)
        i["plan"] = best[1] if best[0] > 0 else None

    befunde, arten = [], {}

    def merke(art, wert, satz):
        befunde.append("- **%s** — %s" % (art, satz))
        arten.setdefault(art, []).append(wert)

    for p in plan:
        stuecke = [i for i in ist if i["plan"] == p["nr"]]
        kurz = p["text"][:50]
        if not stuecke:
            merke("Stück gelöscht", p["ende"] - p["start"], "Nr. %d „%s“ ganz raus" % (p["nr"], kurz))
            continue
        a, z = stuecke[0], stuecke[-1]
        d_anf = a["start"] - p["start"]
        d_end = z["ende"] - p["ende"]
        if abs(d_anf) >= KANTE_MIN:
            art = "Anfang später (weniger Luft vorne)" if d_anf > 0 else "Anfang früher (mehr Luft vorne)"
            merke(art, abs(d_anf), "Nr. %d um %d ms" % (p["nr"], abs(d_anf) * 1000))
        if abs(d_end) >= KANTE_MIN:
            art = "Ende verlängert (mehr Luft hinten)" if d_end > 0 else "Ende gekürzt"
            merke(art, abs(d_end), "Nr. %d um %d ms" % (p["nr"], abs(d_end) * 1000))
        for x, y in zip(stuecke, stuecke[1:]):
            if y["start"] - x["ende"] >= KANTE_MIN:
                raus = woerter_zwischen(words, x["ende"], y["start"])
                merke("Stelle mitten im Stück rausgeschnitten", y["start"] - x["ende"],
                      "Nr. %d: %.2f s%s" % (p["nr"], y["start"] - x["ende"], " — „%s“" % raus if raus else ""))
    for i in ist:
        if i["plan"] is None:
            merke("Neues Stück eingefügt", i["ende"] - i["start"],
                  "%s %.2f–%.2f s" % (Path(i["quelle"]).name, i["start"], i["ende"]))
    reihe = [i["plan"] for i in ist if i["plan"] is not None]
    if any(b < a for a, b in zip(reihe, reihe[1:])):
        merke("Reihenfolge geändert", 0, "neue Folge: %s" % ", ".join(map(str, reihe)))
    for x, y in zip(ist, ist[1:]):
        if y["pos"] - x["pos_ende"] >= KANTE_MIN:
            merke("Pause eingefügt", y["pos"] - x["pos_ende"], "%.2f s vor Stück bei %.1f s" % (y["pos"] - x["pos_ende"], y["pos"]))

    zeilen = ["---", "tags: [videoschnitt]", "---", "",
              "# CapCut-Korrekturen — %s" % merk["projekt"], "",
              "Geplant %d Stücke · in CapCut %d Stücke · verglichen %s" % (len(plan), len(ist), time.strftime("%Y-%m-%d %H:%M")),
              "", "## Was du geändert hast", ""]
    zeilen += befunde or ["- nichts — der Rohschnitt stand so, wie er war."]
    zeilen += ["", "## Regelvorschläge (erst ab %d gleichen Änderungen)" % REGEL_AB, ""]
    vorschlaege = 0
    for art, werte in arten.items():
        if len(werte) >= REGEL_AB and art != "Reihenfolge geändert":
            vorschlaege += 1
            zeilen.append("- **%s** kam %d× vor, Median %d ms → als Regel in `context/videoschnitt-regeln.md`?"
                          % (art, len(werte), statistics.median(werte) * 1000))
    if not vorschlaege:
        zeilen.append("- keine — was nur einmal vorkommt, ist Geschmack bei diesem Video, keine Regel.")
    zeilen += ["", "🛑 Eingetragen wird erst, wenn Patricia den Vorschlag bestätigt hat."]
    ziel = Path(cut_pfad).with_name("capcut-korrekturen.md")
    ziel.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print("\n".join(zeilen[4:]))
    print("\n→ %s" % ziel)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("anlegen")
    a.add_argument("cutlist")
    a.add_argument("--name", help="Projektname in CapCut (Standard: Rohschnitt <Datum> <Ordner>)")
    v = sub.add_parser("vergleichen")
    v.add_argument("cutlist")
    args = ap.parse_args()
    if args.cmd == "anlegen":
        name = args.name or "Rohschnitt %s %s" % (time.strftime("%m-%d"), Path(args.cutlist).parent.name)
        anlegen(args.cutlist, name)
    else:
        vergleichen(args.cutlist)


if __name__ == "__main__":
    main()
