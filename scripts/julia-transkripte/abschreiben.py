"""Julias Kursvideos ohne Vimeo-Untertitel lokal abschreiben (Ton holen + faster-whisper).

    python scripts/julia-transkripte/abschreiben.py [--modell large-v3-turbo] [--nur <vimeo-id>]

Nimmt alle Videos mit Stand "keine-untertitel" aus reference/julia-trost/transkripte-abgleich.json,
laedt nur die Tonspur ueber den HLS-Stream (ffmpeg), schreibt sie lokal ab und legt
<Titel> - <id>.txt + .vtt in den Kursordner. Die Tondatei wird danach geloescht.
Patricias Erlaubnis zum Herunterladen: 27.10.2026, nur Eigengebrauch.
"""
import importlib.util, json, os, re, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("holen", os.path.join(HIER, "holen.py"))
holen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(holen)

KOPF = ("Quelle: Julia Trost, Kurs „{kurs}“ · Vimeo {id} · Titel „{titel}“ · {min} Min.\n"
        "Lokal abgeschrieben mit faster-whisper ({modell}), weil Vimeo keine Untertitel hat — "
        "bei Fachwörtern und Namen verhört; keine Schreibweise hieraus abschreiben.\n"
        "Gekauftes Fremdmaterial: nur Eigengebrauch, nie in Kundendokumente.\n\n---\n\n")


def zeit(s):
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return "%02d:%02d:%06.3f" % (h, m, s)


def ton_holen(cfg, ziel):
    hls = ((cfg.get("request") or {}).get("files") or {}).get("hls") or {}
    cdn = (hls.get("cdns") or {}).get(hls.get("default_cdn")) or next(iter((hls.get("cdns") or {}).values()), {})
    url = cdn.get("url")
    if not url:
        raise RuntimeError("kein HLS-Stream")
    # Ton getrennt vom Bild (separate_av): nur die Tonspur-Playlist laden, sonst zieht ffmpeg
    # das ganze Video mit (erster Lauf: 9 Min. fuer 7 Min. Video).
    from urllib.parse import urljoin
    master = holen.hole(url)
    ton = re.search(r'#EXT-X-MEDIA:TYPE=AUDIO[^\n]*URI="([^"]+)"', master)
    if ton:
        url = urljoin(url, ton.group(1))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-headers", "Referer: https://kurse.juliatrost.de/\r\n",
                    "-i", url, "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000", ziel], check=True)


def main():
    modell = sys.argv[sys.argv.index("--modell") + 1] if "--modell" in sys.argv else "large-v3-turbo"
    nur = sys.argv[sys.argv.index("--nur") + 1] if "--nur" in sys.argv else None
    bericht = json.load(open(holen.BERICHT, encoding="utf-8"))
    offen = [v for v, e in bericht.items() if e["stand"] == "keine-untertitel" and (not nur or v == nur)]
    from faster_whisper import WhisperModel
    m = WhisperModel(modell, device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    for v in offen:
        e = bericht[v]
        cfg = holen.konfig(v, e.get("schluessel", ""))  # Freigabe-Schlüssel aus der Lektion, falls Vimeo sonst 403
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "ton.wav")
            ton_holen(cfg, wav)
            segs, _ = m.transcribe(wav, language="de", beam_size=5, vad_filter=True)
            segs = list(segs)
        vtt = "WEBVTT\n\n" + "\n\n".join("%s --> %s\n%s" % (zeit(s.start), zeit(s.end), s.text.strip()) for s in segs) + "\n"
        text = "\n".join(s.text.strip() for s in segs)
        kurse = e["kurse"]
        ordner = holen.MEHRFACH if len(kurse) > 1 else holen.KURS.get(kurse[0], str(kurse[0]))
        ziel = os.path.join(holen.SORT, ordner)
        os.makedirs(ziel, exist_ok=True)
        name = re.sub(r'[\\/:*?"<>|]', "-", e["titel"])[:90].strip() + " - " + v
        with open(os.path.join(ziel, name + ".vtt"), "w", encoding="utf-8") as f:
            f.write(vtt)
        kursname = ", ".join(holen.KURS.get(k, str(k)) for k in kurse)
        with open(os.path.join(ziel, name + ".txt"), "w", encoding="utf-8") as f:
            f.write(KOPF.format(kurs=kursname, id=v, titel=e["titel"], min=e["min"], modell=modell) + text + "\n")
        bericht[v] = dict(e, stand="abgeschrieben", ordner=ordner)
        with open(holen.BERICHT, "w", encoding="utf-8") as f:
            json.dump(bericht, f, ensure_ascii=False, indent=1)
        print("abgeschrieben", v, ordner, "|", e["titel"], "|", len(text), "Zeichen", flush=True)
    print("FERTIG", len(offen), flush=True)


if __name__ == "__main__":
    main()
