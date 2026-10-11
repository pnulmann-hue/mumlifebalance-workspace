"""
Holt neues Content-Material vom Handy auf den PC.

Patricia wirft auf dem Handy alles, was sie fuer Reels, Karussells oder Stories
verwenden will, in EIN Album: DCIM/Content-Inbox. Dieses Skript holt daraus,
was noch nicht geholt wurde, und legt es dort ab, wo die Skills es finden:

  Videos  ->  video/input/                     (fuer /videoschnitt und /reels)
  Fotos   ->  context/content-assets/inbox/    (fuer /karussell und /story)

Es wird NICHTS auf dem Handy geloescht oder verschoben. Was schon geholt wurde,
steht in einem Merkzettel (context/content-assets-inbox-log.json) und wird beim
naechsten Lauf uebersprungen.

Aufruf:
  python scripts/handy/hol-content.py                 # neues Material holen
  python scripts/handy/hol-content.py --zeigen        # nur auflisten, nichts kopieren
  python scripts/handy/hol-content.py --album Reel-Videos
  python scripts/handy/hol-content.py --alles         # auch schon Geholtes nochmal
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[2]
HANDY = Path(r"C:\Users\pnulm\CrossDevice\S25 Ultra von Patricia\storage")
INBOX_ALBUM = "Content-Inbox"

ZIEL_VIDEO = ROOT / "video" / "input"
ZIEL_FOTO = ROOT / "context" / "content-assets" / "inbox"
LOG = ROOT / "context" / "content-assets-inbox-log.json"
BERICHT = ROOT / "context" / "content-assets-inbox.md"
VORSCHAU = ROOT / "context" / "content-assets" / "vorschau"

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".3gp"}
FOTO_EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp"}


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def ledger_laden():
    if LOG.exists():
        try:
            return json.loads(LOG.read_text(encoding="utf-8"))
        except Exception:
            log("Merkzettel unlesbar — fange neu an.")
    return {"geholt": {}}


def ledger_speichern(daten):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")


def schluessel(pfad):
    """Name + Groesse + Aenderungszeit. Reicht, um dieselbe Datei wiederzuerkennen,
    ohne jede Datei ueber die Handy-Verbindung durchzulesen."""
    s = pfad.stat()
    roh = "%s|%d|%d" % (pfad.name, s.st_size, int(s.st_mtime))
    return hashlib.sha1(roh.encode("utf-8")).hexdigest()[:16]


def medien_info(pfad):
    """Dauer, Aufloesung, Ausrichtung — damit im Bericht steht, was es ueberhaupt ist."""
    try:
        roh = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", str(pfad)],
            capture_output=True, text=True, timeout=120).stdout
        daten = json.loads(roh)
    except Exception:
        return {}
    info = {}
    try:
        info["dauer"] = round(float(daten["format"].get("duration", 0)), 2)
    except Exception:
        pass
    for st in daten.get("streams", []):
        if st.get("codec_type") == "video":
            b, h = st.get("width"), st.get("height")
            # Hochkant-Aufnahmen tragen die Drehung oft nur als Metadatum
            for sd in st.get("side_data_list", []) or []:
                if abs(int(sd.get("rotation", 0) or 0)) in (90, 270):
                    b, h = h, b
            info["breite"], info["hoehe"] = b, h
            if b and h:
                info["format"] = "hochkant" if h > b else ("quadrat" if h == b else "quer")
            break
    return info


def standbild(video, ziel_png, bei=1.0):
    """Ein Standbild, damit Claude sehen kann, was auf dem Clip drauf ist."""
    ziel_png.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.2f" % bei,
                        "-i", str(video), "-frames:v", "1", "-vf", "scale=360:-1",
                        str(ziel_png)], check=True, timeout=180)
        return ziel_png.exists()
    except Exception:
        return False


def datum_aus_name(name):
    """Samsung benennt nach 20260910_132742 — daraus kommt der Monatsordner."""
    ziffern = "".join(c for c in name if c.isdigit())
    if len(ziffern) >= 8:
        try:
            d = datetime.strptime(ziffern[:8], "%Y%m%d")
            return d.strftime("%Y-%m"), d.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m"), datetime.now().strftime("%Y-%m-%d")


def bericht_schreiben(neue, album):
    zeilen = [
        "---",
        "tags: [content, assets]",
        "---",
        "",
        "# Content-Inbox — zuletzt geholt am %s" % time.strftime("%d.%m.%Y um %H:%M"),
        "",
        "Quelle: Handy, Album `DCIM/%s`. Auf dem Handy wurde nichts geloescht." % album,
        "",
    ]
    if not neue:
        zeilen += ["Nichts Neues. Alles aus dem Album ist schon auf dem PC.", ""]
    else:
        videos = [n for n in neue if n["art"] == "video"]
        fotos = [n for n in neue if n["art"] == "foto"]
        zeilen += ["**%d neu geholt** — %d Videos, %d Fotos." % (len(neue), len(videos), len(fotos)), ""]
        if videos:
            zeilen += ["## Videos → `video/input/`", "",
                       "| Datei | aufgenommen | Dauer | Format | Vorschaubild |",
                       "|---|---|---|---|---|"]
            for n in videos:
                zeilen.append("| `%s` | %s | %s | %s | %s |" % (
                    n["name"], n["datum"],
                    ("%.1f s" % n["info"]["dauer"]) if n["info"].get("dauer") else "—",
                    "%s %sx%s" % (n["info"].get("format", "—"),
                                  n["info"].get("breite", "?"), n["info"].get("hoehe", "?")),
                    ("`%s`" % n["vorschau"]) if n.get("vorschau") else "—"))
            zeilen.append("")
        if fotos:
            zeilen += ["## Fotos → `context/content-assets/inbox/`", "",
                       "| Datei | aufgenommen | Format |", "|---|---|---|"]
            for n in fotos:
                zeilen.append("| `%s` | %s | %s %sx%s |" % (
                    n["name"], n["datum"], n["info"].get("format", "—"),
                    n["info"].get("breite", "?"), n["info"].get("hoehe", "?")))
            zeilen.append("")
    zeilen += [
        "## So kommt neues Material her",
        "",
        "Auf dem Handy in der Galerie das Bild oder Video antippen, **Verschieben** oder",
        "**Kopieren** waehlen und das Album **Content-Inbox** nehmen. Danach hier",
        "`python scripts/handy/hol-content.py` laufen lassen — oder einfach im Chat sagen,",
        "dass etwas Neues auf dem Handy liegt.",
        "",
        "## 🔗 Verwandte Notizen",
        "",
        "- [[content-assets-index]] — der grosse Ueberblick, welches Material wo liegt",
        "- [[videoschnitt-regeln]] — was mit den Videos passiert",
        "",
    ]
    BERICHT.write_text("\n".join(zeilen), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Content vom Handy holen")
    uebersprungen = []
    p.add_argument("--album", default=INBOX_ALBUM, help="Album unter DCIM (Standard: Content-Inbox)")
    p.add_argument("--ziel-video", dest="ziel_video", default=None,
                   help="Ziel-Ordner fuer Videos, relativ zum Repo (Standard: video/input). "
                        "Fuer Sprechreels: --album Sprechreels --ziel-video video/sprechreels")
    p.add_argument("--zeigen", action="store_true", help="nur auflisten, nichts kopieren")
    p.add_argument("--alles", action="store_true", help="auch schon Geholtes noch einmal holen")
    args = p.parse_args()

    ziel_video_dir = (ROOT / args.ziel_video) if args.ziel_video else ZIEL_VIDEO

    if not HANDY.exists():
        sys.exit("Handy nicht erreichbar unter %s.\n"
                 "Ist es per CrossDevice/Verbundene Geraete verbunden?" % HANDY)

    quelle = HANDY / "DCIM" / args.album
    if not quelle.exists():
        sys.exit("Album '%s' gibt es nicht. Vorhanden:\n  %s"
                 % (args.album, "\n  ".join(sorted(x.name for x in (HANDY / "DCIM").iterdir()
                                                   if x.is_dir()))))

    ledger = ledger_laden()
    dateien = sorted([f for f in quelle.iterdir() if f.is_file()],
                     key=lambda f: f.stat().st_mtime)
    if not dateien:
        log("Album '%s' ist leer." % args.album)
        bericht_schreiben([], args.album)
        return

    log("Album '%s': %d Dateien" % (args.album, len(dateien)))
    neue = []
    for f in dateien:
        endung = f.suffix.lower()
        if endung in VIDEO_EXT:
            art = "video"
        elif endung in FOTO_EXT:
            art = "foto"
        else:
            log("  uebersprungen (unbekannte Endung): %s" % f.name)
            continue

        sch = schluessel(f)
        if sch in ledger["geholt"] and not args.alles:
            continue

        monat, datum = datum_aus_name(f.stem)
        eintrag = {"name": f.name, "art": art, "datum": datum, "info": {}}

        if args.zeigen:
            neue.append(eintrag)
            log("  NEU  %-6s %s" % (art, f.name))
            continue

        if art == "video":
            ziel = ziel_video_dir / f.name
            ziel.parent.mkdir(parents=True, exist_ok=True)
        else:
            ziel = ZIEL_FOTO / monat / f.name
            ziel.parent.mkdir(parents=True, exist_ok=True)

        log("  hole %-6s %s ..." % (art, f.name))
        try:
            # Schon vorhandene Zieldateien sind schreibgeschuetzt, sobald sie
            # einmal von der Handy-Freigabe kamen — sonst bricht das Kopieren ab.
            if ziel.exists():
                ziel.chmod(0o666)
            shutil.copy2(f, ziel)
        except OSError as fehler:
            # Haeufigster Fall: CrossDevice hat die Datei noch nicht vom Handy
            # geladen ("Der Cloudvorgang war nicht erfolgreich"). Das ist kein
            # Grund, den ganzen Lauf abzubrechen — der Rest wird geholt.
            log("  ! %s uebersprungen: %s" % (f.name, fehler))
            uebersprungen.append(f.name)
            continue
        eintrag["info"] = medien_info(ziel)
        eintrag["ziel"] = str(ziel.relative_to(ROOT))

        if art == "video":
            vp = VORSCHAU / (ziel.stem + ".png")
            bei = min(1.0, (eintrag["info"].get("dauer") or 2) / 3)
            if standbild(ziel, vp, bei):
                eintrag["vorschau"] = str(vp.relative_to(ROOT))

        ledger["geholt"][sch] = {"name": f.name, "art": art,
                                 "geholt_am": datetime.now().isoformat(timespec="seconds"),
                                 "ziel": eintrag.get("ziel", "")}
        neue.append(eintrag)

    if not args.zeigen:
        ledger_speichern(ledger)
    bericht_schreiben(neue, args.album)

    log("")
    if not neue:
        log("Nichts Neues — alles aus dem Album ist schon da.")
    else:
        v = sum(1 for n in neue if n["art"] == "video")
        fo = len(neue) - v
        log("%d neu: %d Videos → %s, %d Fotos → context/content-assets/inbox/"
            % (len(neue), v, ziel_video_dir.relative_to(ROOT), fo))
        log("Bericht: %s" % BERICHT.relative_to(ROOT))
    if uebersprungen:
        log("%d Dateien konnten nicht geholt werden — meist, weil CrossDevice sie noch"
            " nicht vom Handy geladen hat. Handy entsperren, kurz warten, nochmal laufen"
            " lassen: %s" % (len(uebersprungen), ", ".join(uebersprungen[:4])))
    log("Auf dem Handy wurde nichts geloescht oder verschoben.")


if __name__ == "__main__":
    main()
