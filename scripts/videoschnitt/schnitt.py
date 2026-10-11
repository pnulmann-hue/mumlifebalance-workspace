"""
Schritt 3 des /videoschnitt-Workflows: Schnittliste -> Rohschnitt + Einzelclips.

Nimmt eine freigegebene cutlist.json und baut daraus:
  video/output/<slug>/rohschnitt.mp4      alles hintereinander, zum Anschauen
  video/output/<slug>/clips/01.mp4 ...    jede gute Stelle als eigener Clip (fuer CapCut)
  video/output/<slug>/untertitel.srt      Untertitel, auf den Schnitt umgerechnet
  video/output/<slug>/schnittprotokoll.md was drin ist, was rausflog, wie lang

Alle Clips werden mit identischen Parametern neu kodiert (gleiche Aufloesung,
FPS, Pixelformat, Audiorate) — sonst schlaegt das Zusammenfuegen fehl.

Aufruf:
  python scripts/videoschnitt/schnitt.py video/transkripte/<slug>/cutlist.json
  python scripts/videoschnitt/schnitt.py <cutlist> --slug mein-reel --nur-clips
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows-Konsole auf UTF-8 stellen (sonst brechen Umlaute und Pfeile den Lauf ab)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "video" / "output"

PADDING_VOR = 0.12   # Sekunden Luft vor jedem Satzanfang (Jenyas Wert, seit 06.10.2026; vorher 0.25)
PADDING_NACH = 0.35  # Sekunden Luft nach jedem Satzende (Jenya; vorher 0.15 — schnitt Endsilben ab)
PAUSE_MAX = 0.3      # laengere Pausen INNERHALB eines Abschnitts werden auf diesen Wert gekuerzt
CRF = 18             # Qualitaet des Zwischenschnitts (niedriger = besser)


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def zeit(sec, ms=False):
    m = int(sec // 60)
    s = sec % 60
    return "%02d:%05.2f" % (m, s) if ms else "%02d:%02d" % (m, int(s))


def srt_zeit(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    msec = int(round((sec % 1) * 1000))
    if msec >= 1000:
        msec, s = 0, s + 1
    return "%02d:%02d:%02d,%03d" % (h, m, s, msec)


def ffprobe(pfad):
    cmd = ["ffprobe", "-v", "error", "-print_format", "json",
           "-show_format", "-show_streams", str(pfad)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


def quelle_parameter(pfad):
    roh = ffprobe(pfad)
    p = {"dauer": float(roh["format"].get("duration", 0)), "hat_audio": False}
    for st in roh.get("streams", []):
        if st.get("codec_type") == "video" and "breite" not in p:
            # Handy-Videos liegen oft quer gespeichert mit einer Drehung in den
            # Metadaten. ffmpeg dreht beim Dekodieren automatisch — wenn wir hier
            # die rohen width/height nehmen, rechnen wir gegen das echte Bild und
            # zoomen den Clip massiv hinein. Deshalb die Drehung mitlesen.
            breite, hoehe = st.get("width"), st.get("height")
            dreh = 0
            for sd in st.get("side_data_list") or []:
                if "rotation" in sd:
                    dreh = int(float(sd["rotation"]))
            if not dreh:
                dreh = int(float((st.get("tags") or {}).get("rotate") or 0))
            if dreh % 180 != 0:
                breite, hoehe = hoehe, breite
            p["breite"], p["hoehe"] = breite, hoehe
            p["drehung"] = dreh
            try:
                a, b = st.get("r_frame_rate", "30/1").split("/")
                p["fps"] = float(a) / float(b) if float(b) else 30.0
            except Exception:
                p["fps"] = 30.0
        if st.get("codec_type") == "audio":
            p["hat_audio"] = True
    p.setdefault("fps", 30.0)
    return p


def segmente_pruefen(segmente, pad_vor, pad_nach):
    """Padding anwenden, an die Videogrenzen klemmen, Ueberlappungen zusammenfassen.

    Jedes Segment kennt seine eigene Quelle. Dadurch laesst sich aus mehreren
    Clips eine Montage bauen — z.B. erst der Clip vom Auspflanzen, dann der vom
    Ernten, damit die Metapher als Bildfolge dasteht statt als Behauptung.
    Zusammengezogen wird nur innerhalb derselben Quelle und in Reihenfolge.
    """
    fertig = []
    for s in segmente:
        dauer_quelle = s["_dauer_quelle"]
        start = max(0.0, float(s["start"]) - pad_vor)
        ende = min(dauer_quelle, float(s["ende"]) + pad_nach)
        if ende - start < 0.12:
            log("  uebersprungen (zu kurz): %s" % s.get("text", "")[:60])
            continue
        if (fertig
                and fertig[-1]["_quelle"] == s["_quelle"]
                and start <= fertig[-1]["ende"] + 0.02
                and start >= fertig[-1]["start"]):
            # Ueberlappung oder Naht in derselben Quelle: zusammenziehen
            fertig[-1]["ende"] = max(fertig[-1]["ende"], ende)
            fertig[-1]["text"] = (fertig[-1]["text"] + " " + s.get("text", "")).strip()
            continue
        fertig.append({"start": start, "ende": ende, "text": s.get("text", ""),
                       "von_satz": s.get("von_satz"),
                       "_quelle": s["_quelle"], "_dauer_quelle": dauer_quelle})
    for i, s in enumerate(fertig, start=1):
        s["nr"] = i
        s["dauer"] = round(s["ende"] - s["start"], 3)
    return fertig


def pausen_kappen(segmente, woerter, pause_max=PAUSE_MAX):
    """Pausen innerhalb eines Abschnitts auf pause_max kuerzen (Jenyas Regel).

    Laeuft NACH segmente_pruefen: sonst wuerde das Padding die geteilten Stuecke
    sofort wieder zusammenziehen. Getrennt wird mitten in der Stille, sodass genau
    pause_max Ruhe stehen bleibt. Ohne Woerter (Montage) bleibt alles, wie es ist.
    """
    if not woerter or not pause_max:
        return segmente
    neu = []
    for s in segmente:
        drin = [w for w in woerter if w["start"] >= s["start"] - 0.01 and w["ende"] <= s["ende"] + 0.01]
        teil = dict(s)
        for a, b in zip(drin, drin[1:]):
            luecke = b["start"] - a["ende"]
            if luecke > pause_max + 0.05:
                ende = round(a["ende"] + pause_max / 2, 3)
                neu.append(dict(teil, ende=ende))
                teil = dict(s, start=round(b["start"] - pause_max / 2, 3))
        neu.append(teil)
    for i, s in enumerate(neu, start=1):
        s["nr"] = i
        s["dauer"] = round(s["ende"] - s["start"], 3)
    gekappt = len(neu) - len(segmente)
    if gekappt:
        log("  %d Pause(n) innerhalb von Abschnitten auf %.1f s gekuerzt" % (gekappt, pause_max))
    return neu


def clip_schneiden(seg, ziel, p):
    """Ein Segment herausschneiden und auf das Zielformat bringen.

    Clips aus verschiedenen Quellen haben oft verschiedene Aufloesungen. Ohne
    das Skalieren-und-Beschneiden hier scheitert das Zusammenfuegen.
    """
    vf = ("scale=%d:%d:force_original_aspect_ratio=increase,"
          "crop=%d:%d,setsar=1" % (p["breite"], p["hoehe"], p["breite"], p["hoehe"]))
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", "%.3f" % seg["start"], "-t", "%.3f" % seg["dauer"],
        "-i", str(seg["_quelle"]),
        "-map", "0:v:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", str(CRF),
        "-pix_fmt", "yuv420p", "-r", "%.4f" % p["fps"],
        "-vf", vf,
        "-video_track_timescale", "90000",
        # Jede Sekunde ein Keyframe. Ohne das springt der Renderer beim
        # Einzelbild-Aufbau daneben und einzelne Bilder frieren ein.
        "-g", "%d" % max(1, round(p["fps"])),
        "-keyint_min", "%d" % max(1, round(p["fps"])),
        "-sc_threshold", "0",
    ]
    if p["hat_audio"]:
        cmd += ["-map", "0:a:0", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    else:
        cmd += ["-an"]
    cmd += ["-movflags", "+faststart", str(ziel)]
    subprocess.run(cmd, check=True)


def zusammenfuegen(clips, ziel, arbeitsordner):
    liste = arbeitsordner / "concat.txt"
    liste.write_text(
        "\n".join("file '%s'" % c.as_posix().replace("'", "'\\''") for c in clips),
        encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
           "-i", str(liste), "-c", "copy", "-movflags", "+faststart", str(ziel)]
    subprocess.run(cmd, check=True)
    liste.unlink(missing_ok=True)


def schreibe_srt(pfad, segmente):
    zeilen, pos = [], 0.0
    for i, s in enumerate(segmente, start=1):
        if s["text"].strip():
            zeilen += [str(i), "%s --> %s" % (srt_zeit(pos), srt_zeit(pos + s["dauer"])),
                       s["text"].strip(), ""]
        pos += s["dauer"]
    pfad.write_text("\n".join(zeilen), encoding="utf-8")


def woerter_umrechnen(words_pfad, segmente, ziel):
    """Rechnet die Wort-Zeitstempel des Rohmaterials auf den Schnitt um.

    Braucht die Textebene: eine Einblendung soll auf dem Wort erscheinen, das
    im FERTIGEN Video gerade gesprochen wird — nicht dort, wo es im Rohmaterial lag.
    """
    if not words_pfad or not Path(words_pfad).exists():
        return None
    woerter = json.loads(Path(words_pfad).read_text(encoding="utf-8"))
    neu, offset = [], 0.0
    for s in segmente:
        for w in woerter:
            if w["start"] >= s["start"] and w["ende"] <= s["ende"]:
                neu.append({
                    "wort": w["wort"],
                    "start": round(w["start"] - s["start"] + offset, 3),
                    "ende": round(w["ende"] - s["start"] + offset, 3),
                    "clip": s["nr"],
                })
        offset += s["dauer"]
    ziel.write_text(json.dumps(neu, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(neu)


def schreibe_protokoll(pfad, segmente, quelle, p, cutlist, ziel_ordner):
    gesamt = sum(s["dauer"] for s in segmente)
    zeilen = [
        "---",
        "tags: [videoschnitt, schnittprotokoll]",
        "---",
        "",
        "# Schnittprotokoll — %s" % Path(quelle).name,
        "",
        "| | |",
        "|---|---|",
        "| Rohmaterial | %s min |" % zeit(p["dauer"]),
        "| Rohschnitt | **%s min** |" % zeit(gesamt),
        "| Rausgeschnitten | %s min (%.0f %%) |" % (
            zeit(max(0.0, p["dauer"] - gesamt)),
            100 * (1 - gesamt / p["dauer"]) if p["dauer"] else 0),
        "| Clips | %d |" % len(segmente),
        "| Luft vor Satzanfang | %.0f ms |" % (cutlist.get("padding_vor", PADDING_VOR) * 1000),
        "| Luft nach Satzende | %.0f ms |" % (cutlist.get("padding_nach", PADDING_NACH) * 1000),
        "| Regel | %s |" % cutlist.get("regel", "—"),
        "",
        "## Was im Rohschnitt liegt",
        "",
        "| Clip | im Original | Dauer | Text |",
        "|---|---|---|---|",
    ]
    for s in segmente:
        text = s["text"].replace("|", "/")[:110]
        zeilen.append("| `%02d.mp4` | %s → %s | %.2fs | %s |" % (
            s["nr"], zeit(s["start"], ms=True), zeit(s["ende"], ms=True), s["dauer"], text))
    zeilen += [
        "",
        "## So kommt es in CapCut",
        "",
        "1. CapCut öffnen → **Neues Projekt** → Seitenverhältnis 9:16.",
        "2. Alle Dateien aus `%s/clips/` **auf einmal** markieren und ins Projekt ziehen." % ziel_ordner.name,
        "   CapCut sortiert nach Dateiname, also 01, 02, 03 … in der richtigen Reihenfolge.",
        "3. `untertitel.srt` importieren, falls du Untertitel willst (Text → Untertitel importieren).",
        "4. Feinschliff: knappe Clipenden aufziehen, hakelige Übergänge mit einer Mini-Pause entschärfen,",
        "   die ersten zwei Sekunden separat prüfen.",
        "",
    ]
    pfad.write_text("\n".join(zeilen), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Schnittliste in Rohschnitt + Einzelclips umsetzen")
    p.add_argument("cutlist", help="Pfad zur freigegebenen cutlist.json")
    p.add_argument("--slug", help="Name des Ausgabe-Ordners (Standard: aus Quelldateiname)")
    p.add_argument("--nur-clips", action="store_true", help="kein zusammengefuegtes Vorschauvideo")
    p.add_argument("--nur-vorschau", action="store_true", help="keine Einzelclips behalten")
    args = p.parse_args()

    cut_pfad = Path(args.cutlist)
    if not cut_pfad.exists():
        sys.exit("Schnittliste nicht gefunden: %s" % cut_pfad)
    cutlist = json.loads(cut_pfad.read_text(encoding="utf-8"))

    def quelle_finden(roh):
        q = Path(roh)
        if not q.exists():
            q = ROOT / roh
        if not q.exists():
            sys.exit("Video nicht gefunden: %s" % roh)
        return q

    # Jedes Segment darf eine eigene Quelle haben (Montage aus mehreren Clips).
    haupt_roh = cutlist.get("quelle")
    quellen = {}
    for s in cutlist["segmente"]:
        roh = s.get("quelle") or haupt_roh
        if not roh:
            sys.exit("Ein Segment hat keine Quelle und es ist keine Haupt-Quelle gesetzt.")
        if roh not in quellen:
            q = quelle_finden(roh)
            quellen[roh] = (q, quelle_parameter(q))
        s["_quelle"], s["_dauer_quelle"] = quellen[roh][0], quellen[roh][1]["dauer"]

    erste = cutlist["segmente"][0]
    par = dict(quellen[erste.get("quelle") or haupt_roh][1])
    quelle = erste["_quelle"]
    # Zielformat: was in der Schnittliste steht, sonst das des ersten Clips.
    par["breite"] = int(cutlist.get("breite", par.get("breite") or 1080))
    par["hoehe"] = int(cutlist.get("hoehe", par.get("hoehe") or 1920))
    # Audio nur, wenn ALLE Quellen eine Tonspur haben — sonst bricht das Zusammenfuegen.
    par["hat_audio"] = all(v[1]["hat_audio"] for v in quellen.values())
    par["dauer"] = sum(v[1]["dauer"] for v in quellen.values())

    if len(quellen) == 1:
        log("Quelle: %s (%s min, %dx%d, %.2f fps, Audio: %s)" % (
            quelle.name, zeit(par["dauer"]), par["breite"], par["hoehe"],
            par["fps"], "ja" if par["hat_audio"] else "nein"))
    else:
        log("Montage aus %d Clips → %dx%d, %.2f fps, Audio: %s" % (
            len(quellen), par["breite"], par["hoehe"], par["fps"],
            "ja" if par["hat_audio"] else "nein"))
        for roh, (q, qp) in quellen.items():
            log("  %-38s %s min  %sx%s%s" % (
                q.name, zeit(qp["dauer"]), qp.get("breite"), qp.get("hoehe"),
                "" if qp["hat_audio"] else "  (ohne Ton)"))

    segmente = segmente_pruefen(
        cutlist["segmente"],
        float(cutlist.get("padding_vor", PADDING_VOR)),
        float(cutlist.get("padding_nach", PADDING_NACH)))
    if not segmente:
        sys.exit("Die Schnittliste enthaelt keine verwertbaren Segmente.")
    if len(quellen) == 1:
        wp = Path(cutlist.get("words") or (cut_pfad.parent / "words.json"))
        if wp.exists():
            segmente = pausen_kappen(segmente, json.loads(wp.read_text(encoding="utf-8")),
                                     cutlist.get("pause_max", PAUSE_MAX))

    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", quelle.stem.lower()).strip("-")
    ziel = OUT_DIR / ("%s-%s" % (time.strftime("%Y-%m-%d"), slug))
    clips_dir = ziel / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    log("Schneide %d Clips ..." % len(segmente))
    clips = []
    for s in segmente:
        ziel_clip = clips_dir / ("%02d.mp4" % s["nr"])
        clip_schneiden(s, ziel_clip, par)
        clips.append(ziel_clip)
        log("  %02d  %s → %s  (%.2fs)  %s" % (
            s["nr"], zeit(s["start"], ms=True), zeit(s["ende"], ms=True),
            s["dauer"], s["text"][:60]))

    if not args.nur_clips:
        log("Fuege zum Rohschnitt zusammen ...")
        zusammenfuegen(clips, ziel / "rohschnitt.mp4", ziel)

    schreibe_srt(ziel / "untertitel.srt", segmente)
    schreibe_protokoll(ziel / "schnittprotokoll.md", segmente, quelle, par, cutlist, ziel)
    shutil.copy2(cut_pfad, ziel / "cutlist.json")

    # Wort-Zeitstempel auf die geschnittene Zeitachse umrechnen (fuer die Textebene)
    words_pfad = cutlist.get("words") or (cut_pfad.parent / "words.json")
    if len(quellen) > 1:
        words_pfad = None  # bei einer Montage gehoeren die Zeitstempel zu keiner Quelle
    anzahl = woerter_umrechnen(words_pfad, segmente, ziel / "words-schnitt.json")
    if anzahl:
        log("  %d Wort-Zeitstempel auf den Schnitt umgerechnet (words-schnitt.json)" % anzahl)

    if args.nur_vorschau:
        shutil.rmtree(clips_dir)

    gesamt = sum(s["dauer"] for s in segmente)
    log("")
    log("FERTIG → %s" % ziel)
    log("  Rohschnitt: %s min aus %s min Rohmaterial" % (zeit(gesamt), zeit(par["dauer"])))
    if not args.nur_vorschau:
        log("  %d Einzelclips in clips/ — alle markieren und in CapCut ziehen" % len(clips))


if __name__ == "__main__":
    main()
