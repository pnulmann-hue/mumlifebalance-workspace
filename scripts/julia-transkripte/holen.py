"""Fehlende Transkripte aus Julias Kursen holen (Vimeo-Untertitel).

    python scripts/julia-transkripte/holen.py <fehl.txt> [--trocken]

<fehl.txt> enthaelt Paare "<kurs-id>:<vimeo-id>", gesammelt im eingeloggten Browser
ueber /api/courses/<c>/lessons/<l>/viewer (siehe README daneben). Jedes Video wird nur
einmal geholt. Hat es lokal schon ein Transkript (Vimeo-Nummer im Dateinamen oder
gleicher Titel), wird es uebersprungen.

Ablage: reference/julia-trost/Transkripte Videocalls/_sortiert/<Kurs>/<Titel> - <id>.txt + .vtt
Alles unter reference/julia-trost/ ist gitignored (gekauftes Fremdmaterial, Repo oeffentlich).
"""
import json, os, re, sys, time, urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SORT = os.path.join(WURZEL, "reference", "julia-trost", "Transkripte Videocalls", "_sortiert")
BERICHT = os.path.join(WURZEL, "reference", "julia-trost", "transkripte-abgleich.json")
MEHRFACH = "Bonus-Lektionen (in mehreren Kursen)"

KURS = {
    60337: "16 Kurse für 15€", 60342: "10k Verkaufs-Strategie", 60923: "Instagram Story Strategie 2.0",
    63916: "IG Reichweiten Booster", 64688: "Verkaufen mit Liebe", 64880: "Glasklare Produktkommunikation",
    65818: "20k Strategie", 67073: "Automatisiere deine Angebote", 70675: "Minikurse als Umsatzbooster",
    74289: "Digitale Produktwelt", 74356: "04 - Erfolgreiche Werbeanzeigen", 76505: "31 Verkaufsstrategien",
    79527: "Erfolgreich ins neue Jahr", 79638: "Das ultimative Verkaufs-Workbook", 84315: "Launch Queen",
    87620: "Content Recycling", 99907: "Reels to Cash", 108913: "Forever Fans",
    108992: "Leadgewinnung leicht gemacht", 112946: "Online Business Academy (OBA)", 116612: "Road to 50K",
    116613: "Mentoring Gruppe", 120840: "Manychat Automation Vorlagen", 127499: "ChatGPT",
    133269: "Content Kalender", 147998: "Story Bibliothek", 154216: "Die Minikurs Strategie",
    164570: "Test Reels", 165653: "Content (der verkauft)", 165654: "Launchen", 165655: "Automationen",
    165656: "Magnetisch Verkaufen", 165657: "Werbeanzeigen", 175690: "Interaktions-Booster-Challenge",
    189960: "ARIA", 190934: "Prompt Bibliothek", 197805: "KI Kurs", 213147: "100k Blueprint",
}

KOPF = ("Quelle: Julia Trost, Kurs „{kurs}“ · Vimeo {id} · Titel „{titel}“ · {min} Min.\n"
        "Untertitel automatisch von Vimeo erzeugt (de-x-autogen) — bei Fachwörtern und Namen "
        "verhört; keine Schreibweise hieraus abschreiben.\n"
        "Gekauftes Fremdmaterial: nur Eigengebrauch, nie in Kundendokumente.\n\n---\n\n")


def norm(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)


def hole(url):
    bitte = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0", "Referer": "https://kurse.juliatrost.de/", "Accept": "*/*"})
    with urllib.request.urlopen(bitte, timeout=60) as antwort:
        return antwort.read().decode("utf-8")


def konfig(nummer, schluessel=""):
    """Wie scripts/ki-kurs/vimeo-transkripte.py: Einbettungsseite statt /config (403).
    Die meisten Videos brauchen nur den Referer ihrer Kursseite; einzelne antworten ohne
    Freigabe-Schluessel (h) mit 403. Den Schluessel liest man aus der Einbettung in der Lektion
    (Paar dann als "<kurs>:<vimeo>:<schluessel>" in die Liste)."""
    seite = hole("https://player.vimeo.com/video/%s" % nummer + ("?h=%s" % schluessel if schluessel else ""))
    m = re.search(r"window\.playerConfig\s*=\s*", seite)
    if not m:
        return None
    cfg, _ = json.JSONDecoder().raw_decode(seite, m.end())
    return cfg


def prosa(vtt):
    raus = []
    for z in vtt.splitlines():
        z = z.strip()
        if not z or z == "WEBVTT" or z.isdigit() or "-->" in z:
            continue
        if z.startswith(("NOTE", "Kind:", "Language:")):
            continue
        raus.append(z)
    return "\n".join(raus)


def lokal():
    ids, titel = set(), set()
    for d, _, fs in os.walk(os.path.join(WURZEL, "reference", "julia-trost")):
        for f in fs:
            if not f.lower().endswith((".txt", ".vtt", ".md", ".srt")):
                continue
            ids.update(re.findall(r"\d{8,10}", f))
            st = re.sub(r"\.(txt|vtt|md|srt)$", "", f, flags=re.I)
            st = re.sub(r"\s*-\s*\d{8,10}$", "", st)
            st = re.sub(r"^\d{1,3}[\s._-]+", "", st)
            n = norm(st)
            if len(n) >= 6 and not n.isdigit():
                titel.add(n)
    return ids, titel


def main():
    paare = open(sys.argv[1], encoding="utf-8").read().split()
    trocken = "--trocken" in sys.argv
    kurse_je_video, schluessel = {}, {}
    for p in paare:
        c, v, *k = p.split(":")
        if k and k[0]:
            schluessel[v] = k[0]
        kurse_je_video.setdefault(v, [])
        if int(c) not in kurse_je_video[v]:
            kurse_je_video[v].append(int(c))
    ids, titel = lokal()
    bericht = json.load(open(BERICHT, encoding="utf-8")) if os.path.exists(BERICHT) else {}
    for v, kurse in kurse_je_video.items():
        if v in ids or bericht.get(v, {}).get("stand") in ("geholt", "vorhanden-titel"):
            bericht.setdefault(v, {"stand": "vorhanden-id", "kurse": kurse})
            continue
        try:
            cfg = konfig(v, schluessel.get(v, ""))
        except Exception as e:
            bericht[v] = {"stand": "fehler", "grund": str(e)[:120], "kurse": kurse}
            print("FEHLER", v, e, flush=True)
            continue
        if not cfg:
            bericht[v] = {"stand": "fehler", "grund": "keine Konfiguration", "kurse": kurse}
            continue
        video = cfg.get("video") or {}
        t = (video.get("title") or "").strip() or ("video%s" % v)
        minuten = round((video.get("duration") or 0) / 60)
        eintrag = {"titel": t, "min": minuten, "kurse": kurse}
        if norm(re.sub(r"^\d{1,3}[\s._-]+", "", t)) in titel:
            bericht[v] = dict(eintrag, stand="vorhanden-titel")
            print("vorhanden", v, t, flush=True)
            continue
        spuren = (cfg.get("request") or {}).get("text_tracks") or []
        if not spuren:
            bericht[v] = dict(eintrag, stand="keine-untertitel")
            print("ohne Untertitel", v, t, flush=True)
            continue
        if trocken:
            bericht[v] = dict(eintrag, stand="wuerde-holen")
            continue
        adresse = spuren[0].get("url", "")
        if adresse.startswith("/"):
            adresse = "https://player.vimeo.com" + adresse
        vtt = hole(adresse)
        ordner = MEHRFACH if len(kurse) > 1 else KURS.get(kurse[0], str(kurse[0]))
        ziel = os.path.join(SORT, ordner)
        os.makedirs(ziel, exist_ok=True)
        name = re.sub(r'[\\/:*?"<>|]', "-", t)[:90].strip() + " - " + v
        kursname = ", ".join(KURS.get(k, str(k)) for k in kurse)
        with open(os.path.join(ziel, name + ".vtt"), "w", encoding="utf-8") as f:
            f.write(vtt)
        with open(os.path.join(ziel, name + ".txt"), "w", encoding="utf-8") as f:
            f.write(KOPF.format(kurs=kursname, id=v, titel=t, min=minuten) + prosa(vtt) + "\n")
        bericht[v] = dict(eintrag, stand="geholt", ordner=ordner)
        print("geholt", v, ordner, "|", t, flush=True)
        time.sleep(0.4)
    with open(BERICHT, "w", encoding="utf-8") as f:
        json.dump(bericht, f, ensure_ascii=False, indent=1)
    zaehl = {}
    for e in bericht.values():
        zaehl[e["stand"]] = zaehl.get(e["stand"], 0) + 1
    print("FERTIG", zaehl, flush=True)


if __name__ == "__main__":
    main()
