"""
Schritt 5 des /videoschnitt-Workflows: Finish — Zoom, Untertitel, Textebene.

Baut aus einer Spezifikation ein HyperFrames-Projekt und rendert daraus das
fertige, direkt postbare Video. Damit ist CapCut optional statt Pflicht.

Ebenen (von unten nach oben):
  1  Rohschnitt (dein Video)          — bekommt die Zoom-Bewegung
  2  das GROSSE betonte Wort          — Poppins Bold, durchscheinend, Farbverlauf
  3  du freigestellt (optional)       — dadurch liegt das grosse Wort HINTER dir
  4  die kleine duenne Zeile          — Poppins Light, liegt vor dir
  5  wortgenaue Untertitel (optional) — aktives Wort in Orange

Beide Textzeilen sitzen auf Stoss (line-height 0.84, kein Abstand). Jede
Einblendung startet auf dem Wort, das gerade gesprochen wird — dafuer werden die
Wort-Zeitstempel aus `words-schnitt.json` benutzt. Auftritt wechselt
automatisch durch: von links, von rechts, aufgepoppt.

Aufruf:
  python scripts/videoschnitt/textebene.py video/output/<slug>/textebene.json
  python scripts/videoschnitt/textebene.py <spec> --pruefen
  python scripts/videoschnitt/textebene.py <spec> --rendern

Spezifikation (textebene.json):
{
  "video": "video/output/2026-09-10-reel/rohschnitt.mp4",
  "words": "video/output/2026-09-10-reel/words-schnitt.json",
  "person_alpha": "video/output/2026-09-10-reel/person.webm",   // optional
  "profil": "mentoring",                                        // oder "doterra"
  "position": 46,
  "zoom":       {"modus": "auto", "staerke": 1.07, "fokus": "50% 42%"},
  "untertitel": {"an": true, "position": 74},
  "einblendungen": [
    {"klein": "das ist kein", "gross": "ZEITPROBLEM",
     "ab_wort": "Zeitproblem", "dauer": 2.2, "auftritt": "links"}
  ]
}

Jede Einblendung braucht `ab_wort` (naechstes Vorkommen im Transkript) ODER
`ab_sek`. Fehlt `auftritt`, wird links/rechts/pop abgewechselt.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows-Konsole auf UTF-8 stellen
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[2]
HF_VERSION = "0.8.33"

# Patricias Brand-Farben (context/Farbcodes / brand-stories.css) — kein Gelb.
PETROL = "#12828c"
DUNKELBLAU = "#29556d"
CREME = "#f1ecdd"
ORANGE = "#dc822e"

VERLAUF = {
    "mentoring": "linear-gradient(180deg, %s 0%%, %s 48%%, %s 100%%)" % (CREME, PETROL, DUNKELBLAU),
    "doterra": "linear-gradient(180deg, %s 0%%, %s 55%%, %s 100%%)" % (CREME, ORANGE, DUNKELBLAU),
}

AUFTRITTE = ["links", "rechts", "pop"]

# Sounds werden mit ffmpeg erzeugt, nicht heruntergeladen: keine Lizenzfragen,
# keine fehlenden Dateien, immer identisch. "keiner" = still.
SOUNDS = {
    "klick": "anoisesrc=d=0.06:c=pink:a=0.6,highpass=f=1800,afade=t=out:st=0.005:d=0.055",
    "pop": "sine=frequency=520:duration=0.14,volume=0.8,afade=t=out:st=0.02:d=0.12",
    "whoosh": ("anoisesrc=d=0.45:c=white:a=0.45,bandpass=f=1100:width_type=o:w=2,"
               "afade=t=in:st=0:d=0.18,afade=t=out:st=0.2:d=0.25"),
    "ding": "sine=frequency=1180:duration=0.6,volume=0.5,afade=t=out:st=0.05:d=0.55",
}
SOUND_DAUER = {"klick": 0.06, "pop": 0.14, "whoosh": 0.45, "ding": 0.60}

# Freie Elemente (Kapitel 06 des Guides: Aussehen · Bewegung · Stelle · Sound)
ELEMENT_TYPEN = ["punkt", "chip", "notiz", "bild", "clip"]
ELEMENT_BEWEGUNGEN = ["pulsieren", "links", "rechts", "pop", "hoch", "keine"]

# B-Roll-Hook-Stile (abgeschaut bei jenya_kork, siehe context/videoschnitt-animationen.md)
HOOK_STILE = ["marker", "serif"]

# Akzentfarben, die pro Reel rotieren. Patricias Brand hat KEIN Gelb.
AKZENTE = {"petrol": PETROL, "orange": ORANGE, "dunkelblau": DUNKELBLAU}

# Untertitel-Gruppierung
UT_MAX_WOERTER = 4
UT_MAX_DAUER = 1.8
UT_PAUSE_TRENNT = 0.6


def kopie(quelle, ziel):
    """Kopieren, auch wenn das Ziel schreibgeschuetzt ist.

    Dateien, die vom Handy kommen, tragen das Nur-Lesen-Flag mit. Beim zweiten
    Lauf bricht shutil.copy2 daran ab.
    """
    if ziel.exists():
        try:
            ziel.chmod(0o666)
        except OSError:
            pass
    shutil.copy2(quelle, ziel)
    try:
        ziel.chmod(0o666)
    except OSError:
        pass


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def dauer_von(pfad):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", str(pfad)]
    return float(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip())


def normalisieren(text):
    s = text.lower()
    for a, b in [("ä", "a"), ("ö", "o"), ("ü", "u"), ("ß", "ss")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)


def zeit_fuer_wort(woerter, suchwort, ab_index):
    """Findet das naechste Vorkommen von suchwort ab Position ab_index."""
    ziel = normalisieren(suchwort)
    if not ziel:
        return None, ab_index
    for i in range(ab_index, len(woerter)):
        if normalisieren(woerter[i]["wort"]) == ziel:
            return woerter[i]["start"], i + 1
    # zweiter Versuch: Teiltreffer (Beugung, angehaengte Endung)
    for i in range(ab_index, len(woerter)):
        w = normalisieren(woerter[i]["wort"])
        if w and (w.startswith(ziel[:max(4, len(ziel) - 2)])
                  or ziel.startswith(w[:max(4, len(w) - 2)])):
            return woerter[i]["start"], i + 1
    return None, ab_index


def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def woerter_laden(spec):
    if not spec.get("words"):
        return []
    wpfad = Path(spec["words"])
    if not wpfad.exists():
        wpfad = ROOT / spec["words"]
    if not wpfad.exists():
        log("Hinweis: %s nicht gefunden — 'ab_wort', Auto-Zoom und Untertitel "
            "brauchen diese Datei." % spec["words"])
        return []
    return json.loads(wpfad.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- Einblendungen

def gross_schriftgroesse(wort, maximum=188.0, nutzbreite=960.0):
    """Laesst das grosse Wort so gross wie moeglich, aber im Bild.

    Poppins Bold in Versalien ist im Schnitt rund 0.60 em breit pro Zeichen.
    Ohne das laufen lange Woerter wie ENTSCHEIDUNGSPROBLEM links und rechts raus.
    """
    n = max(1, len(wort.strip()))
    return round(max(64.0, min(maximum, nutzbreite / (n * 0.60))), 1)


def einblendungen_aufloesen(spec, woerter, video_dauer):
    fertig, cursor = [], 0
    for i, e in enumerate(spec.get("einblendungen", [])):
        if e.get("ab_sek") is not None:
            start = float(e["ab_sek"])
        elif e.get("ab_wort") and woerter:
            start, cursor = zeit_fuer_wort(woerter, e["ab_wort"], cursor)
            if start is None:
                log("  ! Wort '%s' nicht im Transkript gefunden — Einblendung uebersprungen."
                    % e["ab_wort"])
                continue
        else:
            log("  ! Einblendung %d hat weder ab_wort (mit Transkript) noch ab_sek "
                "— uebersprungen." % (i + 1))
            continue

        dauer = float(e.get("dauer", 2.2))
        start = max(0.0, min(start, max(0.0, video_dauer - 0.3)))
        dauer = min(dauer, video_dauer - start)
        auftritt = e.get("auftritt") or AUFTRITTE[len(fertig) % len(AUFTRITTE)]
        if auftritt not in AUFTRITTE:
            log("  ! Unbekannter Auftritt '%s' — nehme 'pop'." % auftritt)
            auftritt = "pop"

        fertig.append({
            "id": "tx%02d" % (len(fertig) + 1),
            "klein": e.get("klein", ""),
            "gross": e.get("gross", ""),
            "start": round(start, 3),
            "dauer": round(dauer, 3),
            "auftritt": auftritt,
            "position": float(e.get("position", spec.get("position", 46))),
        })
    return fertig


# ------------------------------------------------------------------------ Zoom

def zoom_abschnitte(spec, woerter, video_dauer):
    """Baut die Zoom-Bewegung.

    'auto' nimmt die Clipgrenzen aus words-schnitt.json: jeder zweite Clip
    bekommt eine langsame Fahrt hinein, dazwischen sitzt ein harter Sprung auf
    eine engere Einstellung. Das ist der Rhythmus, den ein Mensch schneiden
    wuerde — durchgehend zoomen wirkt seekrank, gar nicht zoomen wirkt statisch.
    """
    z = spec.get("zoom") or {}
    modus = z.get("modus", "auto")
    if modus in ("aus", "off", "nein") or z.get("an") is False:
        return []

    staerke = float(z.get("staerke", 1.07))
    staerke = max(1.0, min(1.30, staerke))

    if modus == "manuell":
        abschnitte = []
        cursor = 0
        for e in z.get("abschnitte", []):
            if e.get("ab_sek") is not None:
                start = float(e["ab_sek"])
            elif e.get("ab_wort") and woerter:
                start, cursor = zeit_fuer_wort(woerter, e["ab_wort"], cursor)
                if start is None:
                    continue
            else:
                continue
            dauer = min(float(e.get("dauer", 3.0)), video_dauer - start)
            abschnitte.append({"start": round(start, 3), "dauer": round(dauer, 3),
                               "art": e.get("art", "fahrt"),
                               "staerke": float(e.get("staerke", staerke))})
        return abschnitte

    # auto: Clipgrenzen aus dem Transkript
    grenzen = []
    if woerter and "clip" in woerter[0]:
        aktuell = None
        for w in woerter:
            if w.get("clip") != aktuell:
                aktuell = w.get("clip")
                grenzen.append(w["start"])
    if len(grenzen) < 2:
        # kein Clip-Feld: gleichmaessig alle 4 Sekunden
        grenzen = [t for t in range(0, int(video_dauer), 4)]
    grenzen = [max(0.0, g) for g in grenzen]

    abschnitte = []
    for i, start in enumerate(grenzen):
        ende = grenzen[i + 1] if i + 1 < len(grenzen) else video_dauer
        dauer = ende - start
        if dauer < 0.4:
            continue
        art = "fahrt" if i % 2 == 0 else "sprung"
        abschnitte.append({"start": round(start, 3), "dauer": round(dauer, 3),
                           "art": art, "staerke": staerke})
    return abschnitte


# ------------------------------------------------------------------ Untertitel

def untertitel_gruppen(spec, woerter, video_dauer):
    u = spec.get("untertitel") or {}
    if not u.get("an"):
        return []
    if not woerter:
        log("Hinweis: keine Wort-Zeitstempel — Untertitel werden uebersprungen.")
        return []

    max_w = int(u.get("max_woerter", UT_MAX_WOERTER))
    max_d = float(u.get("max_dauer", UT_MAX_DAUER))

    gruppen, aktuell = [], []
    for w in woerter:
        if aktuell and (len(aktuell) >= max_w
                        or (w["ende"] - aktuell[0]["start"]) > max_d
                        or (w["start"] - aktuell[-1]["ende"]) > UT_PAUSE_TRENNT):
            gruppen.append(aktuell)
            aktuell = []
        aktuell.append(w)
    if aktuell:
        gruppen.append(aktuell)

    fertig = []
    for i, g in enumerate(gruppen):
        start = g[0]["start"]
        ende = min(video_dauer, g[-1]["ende"] + 0.12)
        # Nicht in die naechste Gruppe hineinlaufen — sonst stehen zwei
        # Untertitel-Zeilen uebereinander und beide sind unlesbar.
        if i + 1 < len(gruppen):
            ende = min(ende, gruppen[i + 1][0]["start"] - 0.02)
        if ende - start < 0.15:
            continue
        fertig.append({
            "id": "ut%03d" % (i + 1),
            "start": round(start, 3),
            "dauer": round(ende - start, 3),
            "position": float(u.get("position", 74)),
            "woerter": [{"wort": w["wort"], "start": w["start"], "ende": w["ende"]}
                        for w in g],
        })
    return fertig


def elemente_aufloesen(spec, woerter, video_dauer):
    """Freie Animationselemente nach den vier Angaben aus Kapitel 06.

    Aussehen (typ/farbe/flaeche/stil) · Bewegung · Stelle (ab_wort) · Sound.
    """
    fertig, cursor = [], 0
    for i, e in enumerate(spec.get("elemente", [])):
        if e.get("ab_sek") is not None:
            start = float(e["ab_sek"])
        elif e.get("ab_wort") and woerter:
            start, cursor = zeit_fuer_wort(woerter, e["ab_wort"], cursor)
            if start is None:
                log("  ! Wort '%s' nicht gefunden — Element uebersprungen." % e["ab_wort"])
                continue
        else:
            log("  ! Element %d hat keine Stelle (ab_wort/ab_sek) — uebersprungen." % (i + 1))
            continue

        typ = e.get("typ", "chip")
        if typ not in ELEMENT_TYPEN:
            log("  ! Unbekannter Typ '%s' — nehme 'chip'." % typ)
            typ = "chip"
        bewegung = e.get("bewegung", "pop")
        if bewegung not in ELEMENT_BEWEGUNGEN:
            log("  ! Unbekannte Bewegung '%s' — nehme 'pop'." % bewegung)
            bewegung = "pop"
        sound = e.get("sound", "keiner")
        if sound not in SOUNDS and sound != "keiner":
            log("  ! Unbekannter Sound '%s' — nehme keinen. Moeglich: %s"
                % (sound, ", ".join(SOUNDS)))
            sound = "keiner"

        dauer = float(e.get("dauer", 2.5))
        start = max(0.0, min(start, max(0.0, video_dauer - 0.3)))
        dauer = min(dauer, video_dauer - start)
        wo = e.get("wo") or {}

        fertig.append({
            "id": "el%02d" % (len(fertig) + 1),
            "typ": typ,
            "text": e.get("text", ""),
            "farbe": e.get("farbe", "#ffffff"),
            "flaeche": e.get("flaeche", "glas"),
            "kursiv": bool(e.get("kursiv")),
            "groesse": float(e.get("groesse", 44)),
            "bewegung": bewegung,
            "sound": sound,
            "start": round(start, 3),
            "dauer": round(dauer, 3),
            "x": float(wo.get("x", 50)),
            "y": float(wo.get("y", 18)),
            # Nur fuer typ "bild": Pfad relativ zum Projekt und Breite in
            # Prozent der Videobreite.
            "datei": e.get("datei", ""),
            "breite": float(e.get("breite", 72)),
        })
    return fertig


def hook_aufloesen(spec, video_dauer):
    """Der stehende B-Roll-Hook: ein Clip, ein Hook, Inhalt in der Caption.

    Zwei Stile, beide von jenya_kork:
      marker — zweiteiliger Hook, betonter Teil auf einem Marker-Balken
      serif  — zentrierter Block, ein Wort in Philosopher kursiv
    """
    h = spec.get("hook")
    if not h:
        return None
    stil = h.get("stil", "marker")
    if stil not in HOOK_STILE:
        log("  ! Unbekannter Hook-Stil '%s' — nehme 'marker'. Moeglich: %s"
            % (stil, ", ".join(HOOK_STILE)))
        stil = "marker"

    akzent_name = h.get("akzent", "petrol")
    akzent = AKZENTE.get(akzent_name, PETROL)
    if akzent_name not in AKZENTE:
        log("  ! Unbekannte Akzentfarbe '%s' — nehme Petrol. Moeglich: %s"
            % (akzent_name, ", ".join(AKZENTE)))

    start = float(h.get("ab_sek", 0))
    dauer = float(h.get("dauer", video_dauer - start))
    dauer = max(0.5, min(dauer, video_dauer - start))

    return {
        "stil": stil,
        "akzent": akzent,
        "akzent_name": akzent_name if akzent_name in AKZENTE else "petrol",
        "oben": h.get("oben", ""),
        "betont": h.get("betont", ""),
        "klein": h.get("klein", ""),
        "zusatz": h.get("zusatz", ""),
        "grund": h.get("grund", "pille"),
        # Der CTA soll erst am Schluss kommen und dann allein stehen — vorher
        # lief er die ganze Zeit mit und war nach zwei Sekunden unsichtbar.
        "zusatz_ab": h.get("zusatz_ab"),
        "zusatz_allein": bool(h.get("zusatz_allein", True)),
        # Grosser, zentrierter Schlussblock statt kleiner Zeile unten rechts.
        # Gedacht fuer den Fall, dass der Hook vorher ausblendet und der
        # Aufruf die Flaeche allein bekommt.
        "zusatz_gross": bool(h.get("zusatz_gross", False)),
        # 🚨 B-Roll: Hook ab Bild null. Mit Einblendung (0.3 s Verzoegerung plus
        # Fade) stand der ganze Text erst nach knapp einer Sekunde da — Patricia,
        # 29.09.2026: „mich stoert, dass der text erst spaeter eingeblendet wird".
        "sofort": bool(h.get("sofort", False)),
        "position": float(h.get("position", 52 if stil == "marker" else 12)),
        "start": round(start, 3),
        "dauer": round(dauer, 3),
        "video_dauer": round(float(video_dauer), 3),
    }


def zusatz_zeit(hook):
    """Wann der CTA kommt: standardmaessig erst in den letzten 2,6 Sekunden.

    Vorher lief er ueber die ganze Laenge mit und verschwand im Bild. Als
    eigener Schlussakzent liest ihn man wirklich — so machen es die Profile,
    an denen Patricia sich orientiert.
    """
    # Der Aufruf darf ueber das Hook-Ende hinausgehen — genau dafuer ist er da,
    # wenn der Hook vorher ausblendet. Grenze ist das Video, nicht der Hook.
    ende = hook.get("video_dauer") or (hook["start"] + hook["dauer"])
    ab = hook.get("zusatz_ab")
    ab = float(ab) if ab is not None else max(hook["start"] + 0.6, ende - 2.6)
    ab = min(ab, max(hook["start"], ende - 0.8))
    return round(ab, 3), round(max(0.8, ende - ab), 3)


def hook_html(hook):
    if hook["stil"] == "marker":
        teile = ['      <div id="hook" class="clip hook-marker grund-%s" '
                 'data-start="%.3f" data-duration="%.3f" '
                 'style="top:%.2f%%; z-index:7">'
                 % (hook["grund"], hook["start"], hook["dauer"], hook["position"])]
        if hook["oben"]:
            teile.append('        <span class="hk-oben">%s</span>' % html_escape(hook["oben"]))
        if hook["betont"]:
            teile.append('        <span class="hk-betont">'
                         '<i class="hk-balken" style="background:%s"></i>'
                         '<span class="hk-wort">%s</span></span>'
                         % (hook["akzent"], html_escape(hook["betont"])))
        if hook["klein"]:
            teile.append('        <span class="hk-klein">%s</span>' % html_escape(hook["klein"]))
        teile.append("      </div>")
        return "\n".join(teile)

    # serif
    teile = ['      <div id="hook" class="clip hook-serif grund-%s" '
             'data-start="%.3f" data-duration="%.3f" '
             'style="top:%.2f%%; z-index:7">'
             % (hook["grund"], hook["start"], hook["dauer"], hook["position"])]
    if hook["oben"]:
        teile.append('        <span class="sf-normal">%s</span>' % html_escape(hook["oben"]))
    if hook["betont"]:
        teile.append('        <span class="sf-akzent" style="color:%s">%s</span>'
                     % (hook["akzent"], html_escape(hook["betont"])))
    if hook["klein"]:
        teile.append('        <span class="sf-normal">%s</span>' % html_escape(hook["klein"]))
    teile.append("      </div>")
    if hook["zusatz"]:
        ab, lang = zusatz_zeit(hook)
        klassen = "clip hook-zusatz"
        innen = ""
        if hook["zusatz_gross"]:
            klassen += " gross"
        teile.append('      <div id="hook-zusatz" class="%s" data-start="%.3f" '
                     'data-duration="%.3f" style="z-index:7">%s'
                     '<span class="sf-zusatz">%s</span></div>'
                     % (klassen, ab, lang, innen, html_escape(hook["zusatz"])))
    return "\n".join(teile)


def hook_anims(hook):
    z = []
    s = hook["start"]
    if hook.get("sofort"):
        # Nur der CTA darf spaeter kommen, der Hook selbst steht ab Bild null.
        if hook["zusatz"]:
            ab, _ = zusatz_zeit(hook)
            z.append('      tl.from(".sf-zusatz", {opacity:0, y:12, duration:0.4, '
                     'ease:"power2.out"}, %.3f);' % ab)
        return z
    if hook["stil"] == "marker":
        if hook["oben"]:
            z.append('      tl.from(".hk-oben", {opacity:0, y:18, duration:0.3, '
                     'ease:"power2.out"}, %.3f);' % s)
        if hook["betont"]:
            # Der Balken wischt von links auf — das ist die ganze Bewegung.
            z.append('      tl.fromTo(".hk-balken", {scaleX:0, rotate:-1.2}, '
                     '{scaleX:1, rotate:-1.2, duration:0.35, ease:"power2.out", '
                     'immediateRender:false}, %.3f);' % (s + 0.15))
            z.append('      tl.from(".hk-wort", {opacity:0, duration:0.2}, %.3f);' % (s + 0.32))
        if hook["klein"]:
            z.append('      tl.from(".hk-klein", {opacity:0, duration:0.3}, %.3f);' % (s + 0.5))
    else:
        z.append('      tl.from("#hook", {opacity:0, duration:0.45, ease:"power2.out"}, %.3f);' % s)
        if hook["betont"]:
            z.append('      tl.from(".sf-akzent", {opacity:0, y:14, duration:0.4, '
                     'ease:"power2.out"}, %.3f);' % (s + 0.25))
        if hook["zusatz"]:
            ab, _ = zusatz_zeit(hook)
            z.append('      tl.from(".sf-zusatz", {opacity:0, y:12, duration:0.4, '
                     'ease:"power2.out"}, %.3f);' % ab)
    return z


def sounds_erzeugen(elemente, assets_ordner):
    """Erzeugt die gebrauchten Sounds als WAV im Projekt."""
    gebraucht = sorted({e["sound"] for e in elemente if e["sound"] != "keiner"})
    for name in gebraucht:
        ziel = assets_ordner / ("sound-%s.wav" % name)
        if ziel.exists():
            continue
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", SOUNDS[name], "-ac", "2", "-ar", "48000", str(ziel)],
                       check=True)
    return gebraucht


def untertitel_entzerren(untertitel, einblendungen):
    """Blendet Untertitel aus, solange eine Einblendung steht.

    Sonst steht unten 'Kommentier mir MAMA' waehrend oben gross MAMA liegt —
    zweimal derselbe Satz im Bild. Das grosse Wort IST in dem Moment der Untertitel.
    """
    if not einblendungen:
        return untertitel
    behalten = []
    for g in untertitel:
        g_ende = g["start"] + g["dauer"]
        ueberlappung = 0.0
        for e in einblendungen:
            e_ende = e["start"] + e["dauer"]
            ueberlappung += max(0.0, min(g_ende, e_ende) - max(g["start"], e["start"]))
        if ueberlappung > g["dauer"] * 0.3:
            continue
        behalten.append(g)
    return behalten


# ------------------------------------------------------------------------ HTML

def element_html(e):
    """Ein freies Element: aussen ein Vollbild-Clip, innen die eigentliche Form."""
    flaechen = {
        # Frostglas mit dunkler Basis: rein helles Glas laesst farbige
        # Beschriftungen unter 3:1 Kontrast fallen, sobald das Video hell ist.
        "glas": ("background: linear-gradient(rgba(255,255,255,0.16), "
                 "rgba(255,255,255,0.08)), rgba(10,20,26,0.42); "
                 "backdrop-filter: blur(14px); "
                 "border: 1px solid rgba(255,255,255,0.34); "
                 "box-shadow: 0 8px 30px rgba(0,0,0,0.28);"),
        "voll": "background: %s; border: none;" % DUNKELBLAU,
        "keine": "background: none; border: none;",
    }
    flaeche = flaechen.get(e["flaeche"], flaechen["glas"])
    kursiv = "font-style: italic;" if e["kursiv"] else ""

    if e["typ"] == "punkt":
        polster = "14px 26px 14px 20px"
        radius = "999px"
        inhalt = ('<span class="punkt" style="background:%s"></span>'
                  '<span class="beschriftung" style="color:%s; font-size:%.0fpx; %s">%s</span>'
                  % (e["farbe"], e["farbe"], e["groesse"], kursiv, html_escape(e["text"])))
    elif e["typ"] == "notiz":
        polster = "30px 36px"
        radius = "26px"
        inhalt = ('<span class="beschriftung" style="color:%s; font-size:%.0fpx; %s">%s</span>'
                  % (e["farbe"], e["groesse"], kursiv, html_escape(e["text"])))
    elif e["typ"] == "clip":
        # Zwischenschnitt: ein zweiter Clip legt sich vollflaechig ueber das
        # Hauptbild, waehrend der Ton des Talking Heads weiterlaeuft. Genau so
        # halten die Profile ein langes Sprech-Reel am Leben.
        return (
            '      <video id="%s" class="clip zwischenschnitt" data-start="%.3f" '
            'data-duration="%.3f" src="assets/%s" playsinline muted data-volume="0" '
            'style="z-index:4"></video>'
            % (e["id"], e["start"], e["dauer"], Path(e["datei"]).name))
    elif e["typ"] == "bild":
        # Ein echtes Bild ueber dem Video — Screenshot der Bio, ein Testimonial,
        # ein Beweis. Leicht gekippt und mit Schatten, damit es aufliegt statt
        # eingeklebt zu wirken.
        return (
            '      <div id="%s-feld" class="clip" data-start="%.3f" data-duration="%.3f" '
            'style="z-index:6">\n'
            '        <img id="%s" class="element bild" src="assets/%s" '
            'style="left:%.2f%%; top:%.2f%%; width:%.1f%%;">\n'
            '      </div>'
            % (e["id"], e["start"], e["dauer"], e["id"],
               Path(e["datei"]).name, e["x"], e["y"], e["breite"]))
    else:  # chip
        polster = "16px 30px"
        radius = "999px"
        inhalt = ('<span class="beschriftung" style="color:%s; font-size:%.0fpx; %s">%s</span>'
                  % (e["farbe"], e["groesse"], kursiv, html_escape(e["text"])))

    return (
        '      <div id="%s-feld" class="clip" data-start="%.3f" data-duration="%.3f" '
        'style="z-index:6">\n'
        '        <div id="%s" class="element" style="left:%.2f%%; top:%.2f%%; '
        'padding:%s; border-radius:%s; %s">%s</div>\n'
        '      </div>'
        % (e["id"], e["start"], e["dauer"], e["id"], e["x"], e["y"],
           polster, radius, flaeche, inhalt))


def element_anims(e):
    zeilen = []
    ziel = '"#%s"' % e["id"]
    if e["bewegung"] == "links":
        zeilen.append('      tl.from(%s, {opacity:0, x:-160, duration:0.4, '
                      'ease:"power3.out"}, %.3f);' % (ziel, e["start"]))
    elif e["bewegung"] == "rechts":
        zeilen.append('      tl.from(%s, {opacity:0, x:160, duration:0.4, '
                      'ease:"power3.out"}, %.3f);' % (ziel, e["start"]))
    elif e["bewegung"] == "hoch":
        zeilen.append('      tl.from(%s, {opacity:0, y:70, duration:0.4, '
                      'ease:"power3.out"}, %.3f);' % (ziel, e["start"]))
    elif e["bewegung"] == "pop":
        zeilen.append('      tl.from(%s, {opacity:0, scale:0.6, duration:0.38, '
                      'ease:"back.out(2.4)"}, %.3f);' % (ziel, e["start"]))
    elif e["bewegung"] == "pulsieren":
        zeilen.append('      tl.from(%s, {opacity:0, scale:0.7, duration:0.3, '
                      'ease:"back.out(2)"}, %.3f);' % (ziel, e["start"]))
        # Pulsieren am Punkt selbst, damit die Beschriftung ruhig stehen bleibt.
        # EINE Tween mit yoyo statt vieler aneinandergereihter — sonst stossen
        # die Enden aufeinander und GSAP meldet ueberlappende Tweens.
        takte = max(1, int((e["dauer"] - 0.7) / 0.9))
        zeilen.append('      tl.to("#%s .punkt", {opacity:0.25, scale:0.72, duration:0.45, '
                      'repeat:%d, yoyo:true, ease:"sine.inOut"}, %.3f);'
                      % (e["id"], takte * 2 - 1, e["start"] + 0.35))
    aus = min(0.3, e["dauer"] * 0.2)
    zeilen.append('      tl.to(%s, {opacity:0, duration:%.2f, ease:"power2.in"}, %.3f);'
                  % (ziel, aus, e["start"] + e["dauer"] - aus))
    return zeilen


def baue_html(spec, video_name, person_name, video_dauer,
              einblendungen, zooms, untertitel, elemente=None, hook=None):
    verlauf = VERLAUF.get(spec.get("profil", "mentoring"), VERLAUF["mentoring"])
    fokus = (spec.get("zoom") or {}).get("fokus", "50% 42%")

    # --- Textbausteine (grosses Wort hinten, kleine Zeile vorne)
    bloecke = []
    for e in einblendungen:
        gemeinsam = ('class="clip textzeile" data-start="%.3f" data-duration="%.3f"'
                     % (e["start"], e["dauer"]))
        groesse = gross_schriftgroesse(e["gross"])
        bloecke.append(
            '      <div id="%s-gross" %s style="top:%.2f%%; z-index:2">\n'
            '        <span class="gross" style="font-size:%.1fpx">%s</span>\n'
            '      </div>'
            % (e["id"], gemeinsam, e["position"] + 3.2, groesse, html_escape(e["gross"])))
        bloecke.append(
            '      <div id="%s-klein" %s style="top:%.2f%%; z-index:4">\n'
            '        <span class="klein">%s</span>\n'
            '      </div>'
            % (e["id"], gemeinsam, e["position"], html_escape(e["klein"])))

    # --- Untertitel-Gruppen
    for g in untertitel:
        spans = []
        for j, w in enumerate(g["woerter"]):
            spans.append('<span id="%s-w%02d">%s</span>' % (g["id"], j, html_escape(w["wort"])))
        bloecke.append(
            '      <div id="%s" class="clip untertitel" data-start="%.3f" '
            'data-duration="%.3f" style="top:%.2f%%; z-index:5">\n'
            '        <p>%s</p>\n'
            '      </div>'
            % (g["id"], g["start"], g["dauer"], g["position"], " ".join(spans)))

    # --- Stehender B-Roll-Hook
    if hook:
        bloecke.append(hook_html(hook))

    # --- Freie Elemente + ihre Sounds
    elemente = elemente or []
    for e in elemente:
        bloecke.append(element_html(e))
    for e in elemente:
        if e["sound"] == "keiner":
            continue
        # id ist Pflicht: ohne sie findet der Renderer das Audio nicht und
        # die Stelle ist im fertigen Video stumm.
        bloecke.append(
            '      <audio id="%s-ton" class="clip" data-start="%.3f" data-duration="%.3f"\n'
            '             src="assets/sound-%s.wav" data-volume="%.2f"></audio>'
            % (e["id"], e["start"], SOUND_DAUER.get(e["sound"], 0.3), e["sound"],
               float((spec.get("sound") or {}).get("lautstaerke", 0.55))))

    person_block = ""
    if person_name:
        person_block = (
            '      <video id="person" class="clip" data-start="0" data-duration="%.3f"\n'
            '             src="assets/%s" playsinline muted data-volume="0"\n'
            '             style="z-index:3; object-fit:cover"></video>\n'
            % (video_dauer, person_name))

    # --- Animationen
    anims = []

    # Zoom: Hintergrund und freigestellte Ebene bewegen sich identisch,
    # sonst laufen sie auseinander.
    kamera = '"#hintergrund, #person"' if person_name else '"#hintergrund"'
    if zooms:
        # Ruhezustand bei 0 festnageln. Ohne das uebernimmt GSAP beim Zurueck-
        # springen die From-Werte der zuletzt geschriebenen fromTo-Fahrt.
        anims.append('      tl.set(%s, {scale:1}, 0);' % kamera)
    for z in zooms:
        if z["art"] == "sprung":
            anims.append('      tl.set(%s, {scale:%.4f}, %.3f);'
                         % (kamera, z["staerke"] + 0.02, z["start"]))
        else:
            anims.append('      tl.fromTo(%s, {scale:1}, {scale:%.4f, duration:%.2f, '
                         'ease:"none", immediateRender:false}, %.3f);'
                         % (kamera, z["staerke"], z["dauer"], z["start"]))

    for e in einblendungen:
        s, d = e["start"], e["dauer"]
        aus = max(0.25, min(0.35, d * 0.2))
        ein = 0.45
        if e["auftritt"] == "links":
            von_gross, von_klein, ease = "opacity:0, x:-320", "opacity:0, x:-180", "power3.out"
        elif e["auftritt"] == "rechts":
            von_gross, von_klein, ease = "opacity:0, x:320", "opacity:0, x:180", "power3.out"
        else:
            von_gross, von_klein, ease = "opacity:0, scale:0.72", "opacity:0, scale:0.82", "back.out(2)"
        anims.append(
            '      tl.from("#%s-gross", {%s, duration:%.2f, ease:"%s"}, %.3f);\n'
            '      tl.from("#%s-klein", {%s, duration:%.2f, ease:"%s"}, %.3f);\n'
            '      tl.to("#%s-gross", {opacity:0, duration:%.2f, ease:"power2.in"}, %.3f);\n'
            '      tl.to("#%s-klein", {opacity:0, duration:%.2f, ease:"power2.in"}, %.3f);'
            % (e["id"], von_gross, ein, ease, s,
               e["id"], von_klein, ein, ease, s + 0.08,
               e["id"], aus, s + d - aus,
               e["id"], aus, s + d - aus))

    if hook:
        anims.extend(hook_anims(hook))

    for e in elemente:
        anims.extend(element_anims(e))

    for g in untertitel:
        anims.append('      tl.from("#%s", {opacity:0, y:22, duration:0.16, '
                     'ease:"power2.out"}, %.3f);' % (g["id"], g["start"]))
        for j, w in enumerate(g["woerter"]):
            anims.append('      tl.set("#%s-w%02d", {color:"%s"}, %.3f);'
                         % (g["id"], j, ORANGE, w["start"]))
            anims.append('      tl.set("#%s-w%02d", {color:"#ffffff"}, %.3f);'
                         % (g["id"], j, w["ende"]))

    return """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&family=Philosopher:ital,wght@1,700&display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      body { font-family: "Poppins", sans-serif; }

      .clip { position: absolute; inset: 0; }

      #hintergrund, #person {
        width: 1080px; height: 1920px; object-fit: cover;
        transform-origin: %(fokus)s;
        will-change: transform;
      }

      /* Ein Textbaustein: zwei Zeilen auf Stoss, kein Zeilenabstand. */
      .textzeile {
        inset: auto 0 auto 0;
        display: flex;
        justify-content: center;
        text-align: center;
        padding: 0 60px;
        will-change: transform, opacity;
      }
      .klein {
        font-weight: 300;
        font-size: 46px;
        letter-spacing: 0.06em;
        line-height: 0.84;
        color: #ffffff;
        text-shadow: 0 2px 18px rgba(0, 0, 0, 0.45);
        display: block;
      }
      .gross {
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 0.84;
        display: block;
        background: %(verlauf)s;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        -webkit-text-fill-color: transparent;
        opacity: 0.62;
      }

      /* Freies Element: sitzt an seinem eigenen Punkt im Bild. */
      .element {
        position: absolute;
        transform: translate(-50%%, -50%%);
        display: flex;
        align-items: center;
        gap: 16px;
        white-space: nowrap;
        will-change: transform, opacity;
      }
      .element .punkt {
        display: block;
        width: 22px;
        height: 22px;
        border-radius: 50%%;
      }
      .element .beschriftung {
        font-weight: 700;
        letter-spacing: 0.04em;
        line-height: 1;
      }

      /* --- B-Roll-Hook, Stil "marker" (jenya_kork) --- */
      .hook-marker {
        inset: auto 0 auto 0;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
        padding: 0 76px;
      }
      .hook-marker .hk-oben,
      .hook-marker .hk-wort {
        font-weight: 700;
        font-size: 86px;
        line-height: 1.02;
        letter-spacing: -0.01em;
        color: #ffffff;
        /* dunkle Kontur, damit der Text auf jedem Untergrund steht */
        text-shadow:
          -3px -3px 0 rgba(10,20,26,0.9), 3px -3px 0 rgba(10,20,26,0.9),
          -3px  3px 0 rgba(10,20,26,0.9), 3px  3px 0 rgba(10,20,26,0.9),
           0 6px 22px rgba(0,0,0,0.35);
      }
      .hook-marker .hk-betont {
        position: relative;
        display: inline-block;
        padding: 4px 22px 10px;
      }
      .hook-marker .hk-balken {
        position: absolute;
        inset: 0;
        border-radius: 6px;
        transform-origin: left center;
        display: block;
      }
      .hook-marker .hk-wort {
        position: relative;
        text-shadow: 0 3px 14px rgba(0,0,0,0.35);
      }
      .hook-marker .hk-klein {
        /* Dezenter Grund: die Kontur allein reicht auf sehr hellem Material
           nicht (Schnee, Strand, helle Holzwand kamen auf 2.5:1 statt 3:1).
           Inline + clone, damit sich der Grund an die Zeilen schmiegt statt
           als Balken darunterzuliegen. */
        display: inline;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        background: rgba(10, 20, 32, 0.52);
        padding: 4px 12px;
        border-radius: 10px;
        margin-top: 14px;
        font-weight: 400;
        font-size: 38px;
        line-height: 1.28;
        color: #ffffff;
        /* Dunkle Kontur wie beim grossen Text — ohne die verschwindet die Zeile
           auf hellem Material (auf einem Blatt, auf Schnee, am Strand). */
        text-shadow:
          -2px -2px 0 rgba(10,20,26,0.85), 2px -2px 0 rgba(10,20,26,0.85),
          -2px  2px 0 rgba(10,20,26,0.85), 2px  2px 0 rgba(10,20,26,0.85),
           0 4px 16px rgba(0,0,0,0.6);
        max-width: 82%%;
      }

      /* --- B-Roll-Hook, Stil "serif" (jenya_kork) --- */

      .hook-serif {
        inset: auto 0 auto 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 0 96px;
        gap: 2px;
      }
      .hook-serif .sf-normal {
        /* Dezenter Grund: die Kontur allein reicht auf sehr hellem Material
           nicht (Schnee, Strand, helle Holzwand kamen auf 2.5:1 statt 3:1).
           Inline + clone, damit sich der Grund an die Zeilen schmiegt statt
           als Balken darunterzuliegen. */
        display: inline;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        background: rgba(10, 20, 32, 0.52);
        padding: 4px 12px;
        border-radius: 10px;
        font-weight: 400;
        font-size: 54px;
        line-height: 1.22;
        color: #ffffff;
        text-shadow: 0 3px 18px rgba(0,0,0,0.5);
      }
      .hook-serif .sf-akzent {
        /* Auch das betonte Wort braucht den Grund: Creme auf heller Holzwand
           kam auf 2.4:1. Der Grund liegt eng am Wort, nicht als Balken. */
        display: inline;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        background: rgba(10, 20, 32, 0.46);
        padding: 2px 16px 6px;
        border-radius: 14px;
        font-family: "Philosopher", Georgia, serif;
        font-style: italic;
        font-weight: 700;
        font-size: 104px;
        line-height: 1.05;
        margin: 2px 0 6px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.45);
      }
      .zwischenschnitt {
        width: 1080px; height: 1920px; object-fit: cover;
        inset: 0;
      }
      .element.bild {
        position: absolute;
        transform: translate(-50%%, -50%%);
        border-radius: 22px;
        border: 3px solid rgba(255,255,255,0.85);
        box-shadow: 0 22px 60px rgba(0,0,0,0.45);
        background: #ffffff;
      }
      .hook-zusatz {
        inset: auto 0 12%% 0;
        display: flex;
        justify-content: flex-end;
        padding: 0 86px;
      }
      .hook-zusatz .sf-zusatz {
        /* Dezenter Grund: die Kontur allein reicht auf sehr hellem Material
           nicht (Schnee, Strand, helle Holzwand kamen auf 2.5:1 statt 3:1).
           Inline + clone, damit sich der Grund an die Zeilen schmiegt statt
           als Balken darunterzuliegen. */
        display: inline;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        background: rgba(10, 20, 32, 0.52);
        padding: 4px 12px;
        border-radius: 10px;
        font-family: "Philosopher", Georgia, serif;
        font-style: italic;
        font-size: 46px;
        color: #ffffff;
        text-shadow: 0 3px 16px rgba(0,0,0,0.55);
      }

      /* Grosser Schlussblock: der Hook ist dann schon weg, der Aufruf bekommt
         die Flaeche fuer sich. Zentriert wie eine eigene Tafel. */
      .hook-zusatz.gross {
        inset: 34%% 0 auto 0;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        text-align: center;
        /* Mehr Luft rundum, damit der Verlauf trotz kleinerem Radius weit
           genug reicht. */
        padding: 130px 96px 150px;
        /* 62%% war zu gross: der Verlauf endete erst ausserhalb der Flaeche
           und wurde an deren Kante abgeschnitten. Beide Radien bleiben unter
           50%%, sonst steht am Rand ein sichtbarer Strich. */
        background: radial-gradient(45%% 45%% at 50%% 50%%,
                    rgba(8, 18, 30, 0.90) 0%%,
                    rgba(8, 18, 30, 0.74) 40%%,
                    rgba(8, 18, 30, 0.40) 64%%,
                    rgba(8, 18, 30, 0.12) 84%%,
                    rgba(8, 18, 30, 0) 100%%);
      }
      .hook-zusatz.gross .sf-zusatz {
        font-family: "Philosopher", Georgia, serif;
        font-style: italic;
        font-weight: 700;
        font-size: 58px;
        line-height: 1.22;
        color: #f1ecdd;
        /* Ohne das erbt der Text die durchsichtige Fuellung aus dem
           Verlaufsschrift-Stil und wird gar nicht gezeichnet. */
        -webkit-text-fill-color: #f1ecdd;
        /* Die Pille am Text traegt — Flaechen hinter dem Text zeichnet der
           Renderer in diesem Container nicht. Also die bewaehrte Loesung,
           nur groesser: sie schmiegt sich an die Zeilen statt als Kasten
           darunterzuliegen. */
        display: inline;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        background: rgba(8, 18, 30, 0.66);
        padding: 6px 20px 10px;
        border-radius: 16px;
        text-shadow:
          -2px -2px 0 rgba(8,18,30,0.92), 2px -2px 0 rgba(8,18,30,0.92),
          -2px  2px 0 rgba(8,18,30,0.92), 2px  2px 0 rgba(8,18,30,0.92),
          -3px  0   0 rgba(8,18,30,0.92), 3px  0   0 rgba(8,18,30,0.92),
           0   -3px 0 rgba(8,18,30,0.92), 0    3px 0 rgba(8,18,30,0.92),
           0 6px 26px rgba(0,0,0,0.75);
      }

      /* --- Grund-Variante "verlauf" ---------------------------------------
         Statt einer Pille pro Zeile liegt ein weicher Schleier hinter dem
         ganzen Block. Kein Kasten, keine harte Kante — derselbe Gedanke wie
         beim Cover: der Schleier gehoert ueber die Flaeche, sonst sieht es
         nach Aufkleber aus. */
      .grund-verlauf .hk-klein,
      .grund-verlauf .sf-normal,
      .grund-verlauf .sf-akzent {
        background: none;
        padding: 0;
        border-radius: 0;
      }
      .grund-verlauf::before {
        content: "";
        position: absolute;
        /* Beide Radien MUESSEN unter 50%% bleiben. Ein Radius von 55%% reicht
           weiter als der Weg zur Boxkante (50%%), also wird der Verlauf dort
           abgeschnitten und steht noch bei rund 4%% Deckung — im Video ein
           Strich quer durchs Bild. Am 11.09. lief er Patricia durchs Gesicht.
           Die Box zu vergroessern hilft NICHT: beide Werte sind Prozent
           derselben Box und wachsen mit. Nur der Radius selbst zaehlt.
           Die Reichweite kommt stattdessen aus der groesseren Flaeche. */
        left: -50%%;
        right: -50%%;
        top: -85%%;
        bottom: -85%%;
        background: radial-gradient(45%% 45%% at 50%% 50%%,
                    rgba(8, 18, 30, 0.86) 0%%,
                    rgba(8, 18, 30, 0.66) 38%%,
                    rgba(8, 18, 30, 0.34) 60%%,
                    rgba(8, 18, 30, 0.10) 81%%,
                    rgba(8, 18, 30, 0) 100%%);
        pointer-events: none;
        z-index: -1;
      }

      .untertitel {
        inset: auto 0 auto 0;
        display: flex;
        justify-content: center;
        padding: 0 90px;
      }
      /* Dunkle Unterlage: haelt das orange aktive Wort auch auf hellem
         Videobild lesbar. Ohne sie faellt der Kontrast unter 3:1. */
      .untertitel p {
        font-weight: 700;
        font-size: 62px;
        line-height: 1.12;
        text-align: center;
        color: #ffffff;
        background: rgba(11, 22, 28, 0.72);
        padding: 18px 30px;
        border-radius: 22px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-duration="%(dauer).3f" data-width="1080" data-height="1920">

      <video id="hintergrund" class="clip" data-start="0" data-duration="%(dauer).3f"
             src="assets/%(video)s" playsinline data-has-audio="true"
             style="z-index:1"></video>

%(person)s%(bloecke)s
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
%(anims)s
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""" % {
        "verlauf": verlauf,
        "fokus": fokus,
        "dauer": video_dauer,
        "video": video_name,
        "person": person_block,
        "bloecke": "\n".join(bloecke),
        "anims": "\n".join(anims),
    }


def projekt_anlegen(ordner, name):
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / "assets").mkdir(exist_ok=True)
    (ordner / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"blocks": "compositions", "components": "compositions/components",
                  "assets": "assets"},
        "media": {"autoProxy": True},
    }, indent=2), encoding="utf-8")
    (ordner / "meta.json").write_text(json.dumps(
        {"id": name, "name": name}, indent=2), encoding="utf-8")
    (ordner / "package.json").write_text(json.dumps({
        "name": name, "private": True, "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@%s preview" % HF_VERSION,
            "check": "npx --yes hyperframes@%s check" % HF_VERSION,
            "render": "npx --yes hyperframes@%s render" % HF_VERSION,
        },
    }, indent=2), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Finish bauen: Zoom, Untertitel, Textebene")
    p.add_argument("spec", help="Pfad zur textebene.json")
    p.add_argument("--rendern", action="store_true", help="direkt zu MP4 rendern")
    p.add_argument("--pruefen", action="store_true", help="nur 'hyperframes check' laufen lassen")
    p.add_argument("--konzept", action="store_true",
                   help="Standbilder ueber dem echten Material, bevor gerendert wird")
    args = p.parse_args()

    spfad = Path(args.spec)
    if not spfad.exists():
        sys.exit("Spezifikation nicht gefunden: %s" % spfad)
    spec = json.loads(spfad.read_text(encoding="utf-8"))

    video = Path(spec["video"])
    if not video.exists():
        video = ROOT / spec["video"]
    if not video.exists():
        sys.exit("Video nicht gefunden: %s" % spec["video"])

    person = None
    if spec.get("person_alpha"):
        person = Path(spec["person_alpha"])
        if not person.exists():
            person = ROOT / spec["person_alpha"]
        if not person.exists():
            log("Hinweis: freigestelltes Video nicht gefunden — das grosse Wort liegt "
                "dann VOR dir statt hinter dir.")
            person = None

    dauer = dauer_von(video)
    log("Video: %s (%.2f s)" % (video.name, dauer))

    woerter = woerter_laden(spec)
    einblendungen = einblendungen_aufloesen(spec, woerter, dauer)
    zooms = zoom_abschnitte(spec, woerter, dauer)
    elemente = elemente_aufloesen(spec, woerter, dauer)
    hook = hook_aufloesen(spec, dauer)
    untertitel = untertitel_gruppen(spec, woerter, dauer)
    vorher = len(untertitel)
    untertitel = untertitel_entzerren(untertitel, einblendungen)
    if vorher != len(untertitel):
        log("  %d Untertitel-Gruppen ausgeblendet, weil dort eine Einblendung steht"
            % (vorher - len(untertitel)))

    if not (einblendungen or zooms or untertitel or elemente or hook):
        sys.exit("Nichts zu bauen: weder Hook noch Einblendung noch Zoom noch Untertitel noch Element.")

    projekt = Path(spec.get("projekt") or (video.parent / "finish"))
    if not projekt.is_absolute():
        projekt = ROOT / projekt
    name = re.sub(r"[^a-z0-9-]+", "-", projekt.parent.name.lower()).strip("-") or "finish"
    projekt_anlegen(projekt, name)

    kopie(video, projekt / "assets" / video.name)
    if person:
        kopie(person, projekt / "assets" / person.name)
    for e in elemente:
        if e["typ"] not in ("bild", "clip"):
            continue
        quelle = Path(e["datei"])
        if not quelle.is_absolute():
            quelle = ROOT / quelle
        if not quelle.exists():
            log("  ! Bild fehlt: %s — Element wird leer bleiben." % e["datei"])
            continue
        kopie(quelle, projekt / "assets" / quelle.name)
    klaenge = sounds_erzeugen(elemente, projekt / "assets")

    html = baue_html(spec, video.name, person.name if person else None,
                     dauer, einblendungen, zooms, untertitel, elemente, hook)
    (projekt / "index.html").write_text(html, encoding="utf-8")

    log("Projekt geschrieben → %s" % projekt)
    log("  Zoom: %d Abschnitte (%d Fahrten, %d Spruenge)" % (
        len(zooms), sum(1 for z in zooms if z["art"] == "fahrt"),
        sum(1 for z in zooms if z["art"] == "sprung")))
    log("  Untertitel: %d Gruppen" % len(untertitel))
    if klaenge:
        log("  Sounds erzeugt: %s" % ", ".join(klaenge))
    if hook:
        log("  B-Roll-Hook: Stil %s, Akzent %s — \"%s %s\"" % (
            hook["stil"], hook["akzent_name"], hook["oben"], hook["betont"]))
    for e in einblendungen:
        log("  %s  bei %6.2fs  %-7s  %s / %s" % (
            e["id"], e["start"], e["auftritt"], e["klein"], e["gross"]))
    for e in elemente:
        log("  %s  bei %6.2fs  %-6s %-10s Sound %-7s  %s" % (
            e["id"], e["start"], e["typ"], e["bewegung"], e["sound"], e["text"]))
    if einblendungen and not person:
        log("  (ohne freigestelltes Video: Text liegt vor dir, nicht hinter dir —")
        log("   dafuer zuerst 'npx hyperframes remove-background <video>' laufen lassen)")

    if args.pruefen or args.rendern or args.konzept:
        log("Pruefe Komposition ...")
        r = subprocess.run(["npx", "--yes", "hyperframes@%s" % HF_VERSION, "check"],
                           cwd=projekt, shell=True)
        if r.returncode != 0:
            sys.exit("Check fehlgeschlagen — bitte oben nachlesen.")

    if args.konzept:
        # Standbilder ueber dem ECHTEN Material, bevor Minuten in einen Render gehen.
        zeiten = sorted({round(x["start"] + min(0.6, x["dauer"] * 0.5), 2)
                         for x in list(einblendungen) + list(elemente)})
        if not zeiten:
            zeiten = [round(dauer * f, 2) for f in (0.15, 0.5, 0.85)]
        log("Mache Konzept-Standbilder bei: %s" % ", ".join("%.2fs" % t for t in zeiten))
        subprocess.run(["npx", "--yes", "hyperframes@%s" % HF_VERSION, "snapshot",
                        "--at", ",".join("%.2f" % t for t in zeiten),
                        "--no-end", "--describe", "false", "-o", "konzept"],
                       cwd=projekt, shell=True, check=True)
        log("Konzept-Bilder → %s" % (projekt / "konzept"))
        log("Erst anschauen, dann mit --rendern das ganze Video bauen.")
    if args.rendern:
        log("Rendere ... (dauert je nach Laenge einige Minuten)")
        # --sdr: Handy-Material (S25) ist HDR/10-bit. Ohne --sdr will HyperFrames
        # zig GB Roh-HDR-Frames vorab extrahieren und bricht ab. Fuer Instagram
        # ist SDR ohnehin korrekt.
        subprocess.run(["npx", "--yes", "hyperframes@%s" % HF_VERSION, "render", "--sdr"],
                       cwd=projekt, shell=True, check=True)
        log("FERTIG. Das gerenderte MP4 liegt in %s" % (projekt / "renders"))


if __name__ == "__main__":
    main()
