"""
Schritt 1 des /nachbau-Workflows: fremdes Reel -> zerlegte Analyse.

Nimmt einen Instagram-/TikTok-/YouTube-Link (oder eine lokale Datei) und zerlegt
das Video in seine Bausteine, damit Claude erkennen kann, WARUM es funktioniert:

  - Transkript mit Wort-Zeitstempeln  (faster-whisper, lokal)
  - Hook = was in den ersten 3 Sekunden gesagt wird
  - Schnittrhythmus  (Szenenwechsel ueber ffmpeg-Szenenerkennung)
  - Standbilder je Szene  -> Claude SIEHT das Video, statt zu raten
  - Laenge, Aufloesung, Sprechtempo

Laeuft komplett lokal. Kein API-Schluessel, keine Kosten.

Erzeugt in nachbau/<slug>/:
  video.mp4        das heruntergeladene Video (gitignored)
  meta.json        Dauer, Aufloesung, FPS, Quelle, Beschreibung
  words.json       jedes Wort mit Start-/End-Zeit
  analyse.json     maschinenlesbar: Hook, Szenen, Tempo
  analyse.md       <- das liest Claude
  bilder/          Standbild je Szene + Titelbild

Aufruf:
  python scripts/nachbau/zerlegen.py "https://www.instagram.com/reel/XXXX/"
  python scripts/nachbau/zerlegen.py video/input/fremd.mp4 --slug beispiel
  python scripts/nachbau/zerlegen.py <url> --schwelle 0.25   # feiner schneiden
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Windows-Konsole auf UTF-8 stellen (sonst brechen Umlaute den Lauf ab)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "nachbau"


def lauf(befehl, **kw):
    """Fuehrt einen Befehl aus und gibt (returncode, stdout+stderr) zurueck."""
    p = subprocess.run(befehl, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def schlanker_name(text, grenze=50):
    text = re.sub(r"[^\w\s-]", "", (text or "").lower())
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text[:grenze] or "ohne-namen"


# --------------------------------------------------------------------------
# 1 — Video besorgen
# --------------------------------------------------------------------------

def holen(quelle, ordner, cookies=None, browser=None):
    """Laedt das Video per yt-dlp oder kopiert eine lokale Datei."""
    ordner.mkdir(parents=True, exist_ok=True)
    ziel = ordner / "video.mp4"

    if not quelle.startswith("http"):
        pfad = Path(quelle)
        if not pfad.is_absolute():
            pfad = WURZEL / quelle
        if not pfad.exists():
            sys.exit(f"Datei nicht gefunden: {pfad}")
        if ziel.exists():
            ziel.unlink()
        import shutil
        shutil.copy2(pfad, ziel)
        return {"quelle": str(pfad), "art": "lokale Datei"}

    befehl = [
        "yt-dlp", quelle,
        "-o", str(ordner / "video.%(ext)s"),
        "--merge-output-format", "mp4",
        "--write-info-json",
        "--no-playlist", "--no-update",
        "--quiet", "--no-warnings", "--progress",
    ]
    # Standard-Cookie-Datei, falls vorhanden — dann laeuft Instagram ohne Zusatzangabe
    if not cookies and not browser:
        vorgabe = Path(__file__).parent / "cookies.txt"
        if vorgabe.exists():
            cookies = str(vorgabe)
    if cookies:
        befehl += ["--cookies", str(cookies)]
        print(f"  Nutze Cookies aus {cookies}")
    elif browser:
        befehl += ["--cookies-from-browser", browser]
        print(f"  Nutze Cookies aus {browser}")

    print(f"  Lade herunter: {quelle}")
    code, aus = lauf(befehl)
    if code != 0 or not ziel.exists():
        # Instagram verlangt Login. Ehrlich sagen statt still scheitern.
        print("\n  yt-dlp kam nicht durch. Ausgabe:")
        print("  " + "\n  ".join(aus.strip().splitlines()[-6:]))
        sys.exit(
            "\nAbbruch. Drei Auswege:\n\n"
            "  1. VON HAND LADEN (geht immer, dauert 20 Sekunden)\n"
            "     Link auf cobalt.tools einfuegen, Datei speichern, dann:\n"
            "     python scripts/nachbau/zerlegen.py <pfad-zur-datei> --slug name\n\n"
            "  2. COOKIES EINMALIG EXPORTIEREN (danach laeuft es automatisch)\n"
            "     Browser-Erweiterung \"Get cookies.txt LOCALLY\" installieren,\n"
            "     auf instagram.com exportieren, Datei ablegen als:\n"
            "     scripts/nachbau/cookies.txt\n"
            "     Das Skript findet sie dann von selbst.\n\n"
            "  3. ANDEREN BROWSER PROBIEREN\n"
            "     --browser edge   (Edge muss dabei geschlossen sein)\n"
            "     Chrome geht seit Version 127 nicht mehr, der verschluesselt anders.\n"
        )

    info = {"quelle": quelle, "art": "heruntergeladen"}
    infodatei = next(ordner.glob("*.info.json"), None)
    if infodatei:
        try:
            roh = json.loads(infodatei.read_text(encoding="utf-8"))
            info.update({
                "titel": roh.get("title"),
                "kanal": roh.get("uploader") or roh.get("channel"),
                "beschreibung": (roh.get("description") or "")[:2000],
                "aufrufe": roh.get("view_count"),
                "likes": roh.get("like_count"),
                "kommentare": roh.get("comment_count"),
                "hochgeladen": roh.get("upload_date"),
            })
        except Exception:
            pass
        infodatei.unlink()
    return info


# --------------------------------------------------------------------------
# 2 — Technische Eckdaten
# --------------------------------------------------------------------------

def eckdaten(video):
    code, aus = lauf([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate:format=duration",
        "-of", "json", str(video),
    ])
    if code != 0:
        sys.exit("ffprobe konnte das Video nicht lesen.")
    d = json.loads(aus)
    s = (d.get("streams") or [{}])[0]
    fps = s.get("r_frame_rate", "0/1")
    try:
        z, n = fps.split("/")
        fps = round(int(z) / int(n), 2) if int(n) else 0
    except Exception:
        fps = 0
    return {
        "breite": s.get("width"),
        "hoehe": s.get("height"),
        "fps": fps,
        "dauer": round(float(d.get("format", {}).get("duration", 0)), 2),
    }


# --------------------------------------------------------------------------
# 3 — Schnittrhythmus
# --------------------------------------------------------------------------

def szenen(video, dauer, schwelle=0.30):
    """Findet Szenenwechsel. Gibt eine Liste von Sekunden zurueck, 0.0 immer dabei."""
    code, aus = lauf([
        "ffmpeg", "-i", str(video),
        "-filter:v", f"select='gt(scene,{schwelle})',showinfo",
        "-f", "null", "-",
    ])
    zeiten = [0.0]
    for treffer in re.finditer(r"pts_time:([0-9.]+)", aus):
        t = round(float(treffer.group(1)), 2)
        # Schnitte unter 0.25 s auseinander sind meist Bildrauschen, nicht Schnitt
        if t - zeiten[-1] >= 0.25:
            zeiten.append(t)
    return zeiten


# --------------------------------------------------------------------------
# 4 — Standbilder
# --------------------------------------------------------------------------

def standbilder(video, zeiten, ordner, hoechstens=12):
    ordner.mkdir(parents=True, exist_ok=True)
    for alt in ordner.glob("*.jpg"):
        alt.unlink()

    # Bei vielen Szenen gleichmaessig ausduennen, damit Claude nicht 60 Bilder liest
    auswahl = zeiten
    if len(zeiten) > hoechstens:
        schritt = len(zeiten) / hoechstens
        auswahl = [zeiten[int(i * schritt)] for i in range(hoechstens)]

    gemacht = []
    for i, t in enumerate(auswahl, 1):
        ziel = ordner / f"{i:02d}_{t:06.2f}s.jpg"
        code, _ = lauf([
            "ffmpeg", "-ss", str(t), "-i", str(video),
            "-frames:v", "1", "-q:v", "3", "-y", str(ziel),
        ])
        if code == 0 and ziel.exists():
            gemacht.append({"nr": i, "sekunde": t, "datei": ziel.name})
    return gemacht


def raster_bilder(video, dauer, ordner, takt=1.0):
    """Standbilder im festen Takt — fuer Jenyas Methode „Sekunde 2 bis 5".

    Die Szenen-Standbilder reichen nicht, wenn ein Reel in einer Einstellung
    laeuft und die Bewegung nur im Text steckt. Hier kommt alle `takt` Sekunden
    ein Bild, damit eine Animation zeitgenau beschrieben werden kann.
    """
    ordner.mkdir(parents=True, exist_ok=True)
    for alt_bild in ordner.glob("*.jpg"):
        alt_bild.unlink()
    gemacht = []
    t = 0.0
    while t < dauer:
        ziel = ordner / f"s{t:06.2f}.jpg"
        code, _ = lauf([
            "ffmpeg", "-ss", f"{t}", "-i", str(video),
            "-frames:v", "1", "-q:v", "4", "-y", str(ziel),
        ])
        if code == 0 and ziel.exists():
            gemacht.append({"sekunde": round(t, 2), "datei": ziel.name})
        t += takt
    return gemacht


# --------------------------------------------------------------------------
# 5 — Transkript
# --------------------------------------------------------------------------

def transkribieren(video, modell="small"):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  faster-whisper fehlt -> ohne Transkript weiter.")
        print("  Nachinstallieren: pip install faster-whisper")
        return [], ""

    print(f"  Transkribiere lokal (Modell {modell}) …")
    m = WhisperModel(modell, device="cpu", compute_type="int8")
    segmente, _ = m.transcribe(str(video), language="de", word_timestamps=True)

    woerter, text = [], []
    for seg in segmente:
        text.append(seg.text.strip())
        for w in (seg.words or []):
            woerter.append({
                "wort": w.word.strip(),
                "start": round(w.start, 2),
                "ende": round(w.end, 2),
            })
    return woerter, " ".join(text).strip()


def hook_text(woerter, bis=3.0):
    return " ".join(w["wort"] for w in woerter if w["start"] < bis).strip()


# --------------------------------------------------------------------------
# Bericht
# --------------------------------------------------------------------------

def bericht(a, ordner):
    m, s = a["meta"], a["szenen"]
    z = [x["sekunde"] for x in s]
    laengen = [round(z[i + 1] - z[i], 2) for i in range(len(z) - 1)]
    if m["dauer"] and z:
        laengen.append(round(m["dauer"] - z[-1], 2))

    zeilen = []
    zeilen.append("---")
    zeilen.append("tags: [research, content, nachbau]")
    zeilen.append("---")
    zeilen.append("")
    zeilen.append(f"# Zerlegt: {a['slug']}")
    zeilen.append("")
    zeilen.append(f"**Zerlegt am:** {a['stand']}  ")
    zeilen.append(f"**Quelle:** {a['herkunft'].get('quelle')}")
    for feld, name in [("kanal", "Kanal"), ("hochgeladen", "Hochgeladen"),
                       ("aufrufe", "Aufrufe"), ("likes", "Likes"),
                       ("kommentare", "Kommentare")]:
        if a["herkunft"].get(feld):
            zeilen.append(f"**{name}:** {a['herkunft'][feld]}  ")
    zeilen.append("")
    zeilen.append("---")
    zeilen.append("")
    zeilen.append("## Eckdaten")
    zeilen.append("")
    zeilen.append(f"- **Laenge:** {m['dauer']} s")
    zeilen.append(f"- **Format:** {m['breite']}×{m['hoehe']} ({m['fps']} fps)")
    zeilen.append(f"- **Schnitte:** {len(z)} Einstellungen")
    if laengen:
        schnitt = round(sum(laengen) / len(laengen), 2)
        zeilen.append(f"- **Schnittrhythmus:** im Mittel {schnitt} s je Einstellung "
                      f"(kuerzeste {min(laengen)} s, laengste {max(laengen)} s)")
    if a.get("tempo"):
        zeilen.append(f"- **Sprechtempo:** {a['tempo']} Woerter pro Minute")
    zeilen.append("")

    if a.get("hook"):
        zeilen.append("## Der Hook — was in den ersten 3 Sekunden gesagt wird")
        zeilen.append("")
        zeilen.append(f"> {a['hook']}")
        zeilen.append("")

    if a.get("text"):
        zeilen.append("## Gesprochener Text")
        zeilen.append("")
        zeilen.append(a["text"])
        zeilen.append("")

    zeilen.append("## Einstellungen mit Standbild")
    zeilen.append("")
    zeilen.append("| # | ab Sekunde | Dauer | Standbild | was dort gesagt wird |")
    zeilen.append("|---|---|---|---|---|")
    for i, e in enumerate(s):
        d = laengen[i] if i < len(laengen) else ""
        gesagt = " ".join(
            w["wort"] for w in a.get("woerter", [])
            if e["sekunde"] <= w["start"] < e["sekunde"] + (d or 99)
        )[:70]
        zeilen.append(f"| {e['nr']} | {e['sekunde']} s | {d} s | "
                      f"`bilder/{e['datei']}` | {gesagt} |")
    zeilen.append("")

    if a["herkunft"].get("beschreibung"):
        zeilen.append("## Caption / Beschreibung")
        zeilen.append("")
        zeilen.append("```text")
        zeilen.append(a["herkunft"]["beschreibung"])
        zeilen.append("```")
        zeilen.append("")

    if a.get("raster"):
        zeilen.append(f"## Raster-Bilder ({len(a['raster'])} Stueck)")
        zeilen.append("")
        zeilen.append("Fuer zeitgenaues Nachbauen von Animationen — „Sekunde 2 bis 5, "
                      "hier springt der Text rein\".")
        zeilen.append("")
        zeilen.append("Liegen in `raster/`, benannt nach der Sekunde: "
                      + ", ".join(f"`{x['datei']}`" for x in a["raster"][:6])
                      + (" …" if len(a["raster"]) > 6 else ""))
        zeilen.append("")

    zeilen.append("---")
    zeilen.append("")
    zeilen.append("## 🔎 Was Claude jetzt macht")
    zeilen.append("")
    zeilen.append("1. **Standbilder in `bilder/` wirklich anschauen** — nicht aus den")
    zeilen.append("   Dateinamen schliessen, was zu sehen ist.")
    zeilen.append("2. Den **Mechanismus** benennen: Hook-Familie, Kommentar-Ausloeser,")
    zeilen.append("   Share-Trigger, wo die Pointe sitzt, wie die Spannung gehalten wird.")
    zeilen.append("3. Ein **Nachbau-Briefing fuer Patricias eigenes Material** schreiben —")
    zeilen.append("   nie den Text uebernehmen, nur die Bauweise. Szene, Zahlen und Stimme")
    zeilen.append("   kommen aus ihrem Leben.")
    zeilen.append("")
    zeilen.append("🚨 **Das fremde Video bleibt lokal.** `nachbau/` ist gitignored —")
    zeilen.append("das Repo ist oeffentlich, und das ist fremdes Material.")
    return "\n".join(zeilen)


# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Fremdes Reel in seine Bausteine zerlegen.")
    p.add_argument("quelle", help="URL (Instagram/TikTok/YouTube) oder lokale Videodatei")
    p.add_argument("--slug", help="Ordnername (sonst automatisch)")
    p.add_argument("--modell", default="small", help="faster-whisper Modell (default: small)")
    p.add_argument("--schwelle", type=float, default=0.30,
                   help="Empfindlichkeit der Szenenerkennung, 0.15 = fein, 0.45 = grob")
    p.add_argument("--ohne-text", action="store_true", help="Transkript ueberspringen")
    p.add_argument("--raster", nargs="?", type=float, const=1.0, default=None,
                   help="Zusaetzlich Standbilder im festen Takt, z.B. --raster 0.5 "
                        "(fuer zeitgenaues Nachbauen von Animationen)")
    p.add_argument("--cookies", help="Pfad zu einer cookies.txt (fuer Instagram)")
    p.add_argument("--browser", help="Cookies direkt aus diesem Browser holen: edge / firefox")
    args = p.parse_args()

    slug = args.slug or schlanker_name(
        Path(args.quelle).stem if not args.quelle.startswith("http")
        else args.quelle.rstrip("/").split("/")[-1]
    )
    slug = f"{datetime.now():%Y-%m-%d}-{slug}"
    ordner = ZIEL / slug

    print(f"\n▶ Zerlege nach nachbau/{slug}/\n")

    herkunft = holen(args.quelle, ordner, args.cookies, args.browser)
    video = ordner / "video.mp4"

    print("  Lese Eckdaten …")
    meta = eckdaten(video)
    print(f"    {meta['dauer']} s · {meta['breite']}×{meta['hoehe']} · {meta['fps']} fps")

    print("  Suche Szenenwechsel …")
    zeiten = szenen(video, meta["dauer"], args.schwelle)
    print(f"    {len(zeiten)} Einstellungen")

    print("  Ziehe Standbilder …")
    bilder = standbilder(video, zeiten, ordner / "bilder")
    print(f"    {len(bilder)} Bilder")

    raster = []
    if args.raster:
        print(f"  Ziehe Raster-Bilder alle {args.raster} s …")
        raster = raster_bilder(video, meta["dauer"], ordner / "raster", args.raster)
        print(f"    {len(raster)} Bilder")

    woerter, text = ([], "")
    if not args.ohne_text:
        woerter, text = transkribieren(video, args.modell)
        print(f"    {len(woerter)} Woerter")

    tempo = None
    if woerter and meta["dauer"]:
        tempo = round(len(woerter) / meta["dauer"] * 60)

    analyse = {
        "slug": slug,
        "stand": f"{datetime.now():%Y-%m-%d %H:%M}",
        "herkunft": herkunft,
        "meta": meta,
        "szenen": bilder,
        "alle_schnitte": zeiten,
        "woerter": woerter,
        "text": text,
        "hook": hook_text(woerter) if woerter else "",
        "tempo": tempo,
        "raster": raster,
    }

    (ordner / "meta.json").write_text(
        json.dumps({"herkunft": herkunft, "meta": meta}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    (ordner / "words.json").write_text(
        json.dumps(woerter, ensure_ascii=False, indent=2), encoding="utf-8")
    (ordner / "analyse.json").write_text(
        json.dumps(analyse, ensure_ascii=False, indent=2), encoding="utf-8")
    (ordner / "analyse.md").write_text(bericht(analyse, ordner), encoding="utf-8")

    print(f"\n✅ Fertig: nachbau/{slug}/analyse.md")
    print(f"   Standbilder: nachbau/{slug}/bilder/ ({len(bilder)} Stueck)")
    if analyse["hook"]:
        print(f"\n   Hook: „{analyse['hook']}\"")
    print()


if __name__ == "__main__":
    main()
