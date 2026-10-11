"""Launch-Storys abwechslungsreich gestalten (08.10.2026).

Patricia: *„könntest du mir die storys für den launch nun durchgehend alle so
vorbereiten? immer schön abwechselnd wie die von heute 8.10. dann möchte ich aber
dass du mir vorher das datum schreibst z.B. 9.10. - freitag"*.

Liest die Story-Dokumente, wie sie im Cockpit liegen (Ordner mit JSON je Dokument,
geholt per `ArtifactData list … out_dir`), und schreibt je Dokument eine Datei mit
neuer Gestaltung und neuem Namen „9.10. · Freitag · KI-Launch · …“ nach --ziel.

🚨 Die WÖRTER bleiben unverändert. Zerlegt wird nur in Felder (Zeile oben ·
Haupttext · Nachsatz · Haken-Liste) — die Gegenprobe am Schluss bricht ab, wenn
ein Wort fehlt oder dazukommt. Einzige Formatierung: führendes „1. “ einer
Aufzählung fällt weg, weil die Haken-Liste selbst zählt.
🚨 Keine zwei Folien hintereinander mit gleichem Hintergrund.

    python scripts/launch/storys-gestalten.py <quelle> --ziel <ordner> [--ab 2026-10-09] [--bis 2026-10-23]
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

WOCHENTAG = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
FOTOS = ["s04.jpg", "s03.jpg", "s01.jpg", "s05.jpg", "s02.jpg", "s06.jpg"]   # Mentoring-Vorrat

# Gestaltungen für reine Textfolien — der Zyklus sorgt für Abwechslung
TEXTSTILE = [
    {"hg": "creme", "schrift": "philo", "align": "left", "balken": "aus", "farbe": "dunkel", "pos": 42},
    {"hg": "dunkel", "schrift": "philo-k", "align": "right", "balken": "aus", "pos": 46},
    {"hg": "creme", "schrift": "sans-b", "align": "left", "balken": "zeilen", "farbe": "orange", "pos": 38},
    {"hg": "petrol", "schrift": "philo", "align": "center", "balken": "aus", "pos": 44},
    {"hg": "orange", "schrift": "sans-b", "align": "left", "balken": "aus", "pos": 42},
    {"hg": "creme", "schrift": "philo-k", "align": "center", "balken": "zeilen", "farbe": "petrol", "pos": 44},
    {"hg": "dunkel", "schrift": "sans-b", "align": "left", "balken": "zeilen", "farbe": "creme", "pos": 40},
]
FOTOSTILE = [
    {"schrift": "sans-b", "align": "center", "balken": "zeilen", "farbe": "creme", "pos": 70},
    {"schrift": "philo", "align": "left", "balken": "zeilen", "farbe": "dunkel", "pos": 72},
    {"schrift": "sans-b", "align": "right", "balken": "zeilen", "farbe": "weiss", "pos": 70},
    {"schrift": "philo-k", "align": "left", "balken": "zeilen", "farbe": "orange", "pos": 72},
]
KURS_HG = ["dunkel", "creme", "petrol"]
CTA_HG = ["dunkel", "orange", "petrol"]
STILFELDER = ["hg", "schrift", "align", "balken", "farbe", "pos", "groesse", "dreh", "foto",
              "eyebrow", "punkte", "klein", "pille", "sticker", "stickerText", "stickerPos", "notiz"]


def ist_kopf(p):
    """Kurze Zwischenüberschrift wie „Morgens“, „Modul 1–3“, „Eure Worte, nicht meine 😄“."""
    p = p.strip()
    return 0 < len(p) <= 42 and "\n" not in p and not p.endswith(".") and not p.endswith("?")


def zerlegen(fr):
    text = (fr.get("text") or "").strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    teil = {"eyebrow": "", "text": "", "klein": "", "punkte": []}
    if len(paras) >= 2 and ist_kopf(paras[0]):
        teil["eyebrow"] = paras.pop(0)
    rest = []
    for p in paras:
        zeilen = [z.strip() for z in p.split("\n") if z.strip()]
        nummeriert = [z for z in zeilen if re.match(r"^\d\.\s", z)]
        if len(nummeriert) >= 2 and len(nummeriert) == len(zeilen):
            teil["punkte"] = [re.sub(r"^\d\.\s+", "", z) for z in zeilen]
        else:
            rest.append(p)
    if rest:
        teil["text"] = rest[0]
        teil["klein"] = "\n\n".join(rest[1:])
    elif teil["punkte"] and teil["eyebrow"]:
        teil["text"], teil["eyebrow"] = teil["eyebrow"], ""
    return teil


def woerter(s):
    s = re.sub(r"(?m)^\d\.\s+", "", s or "")
    return re.findall(r"\w+|[^\w\s]", s)


def gestalten(doc, tag_nr):
    frames = doc["frames"]
    zyklus = tag_nr * 3          # jeder Tag beginnt woanders im Zyklus
    foto_nr = tag_nr
    vorher_hg = None
    neu = []
    for i, fr in enumerate(frames):
        f = {k: v for k, v in fr.items() if k not in STILFELDER}
        lay = fr.get("layout") or "text"
        teil = zerlegen(fr)
        stil = {}
        zitat = teil["eyebrow"].lower().startswith(("eure worte", "warum frauen", "aus meinen dms"))
        if lay in ("frage", "umfrage"):
            f["layout"] = lay
            f["text"] = teil["text"] if not teil["eyebrow"] else teil["eyebrow"]
            klein = "\n\n".join(x for x in [teil["text"] if teil["eyebrow"] else "", teil["klein"]] if x)
            if klein: f["klein"] = klein
            hg = "petrol" if vorher_hg == "creme" else "creme"
            stil = {"hg": hg, "schrift": "philo", "align": "center", "balken": "aus", "pos": 30,
                    "sticker": lay, "stickerPos": 66}
            if lay == "umfrage" and (fr.get("optA") or fr.get("optB")):
                stil["stickerText"] = (fr.get("optA") or "") + " / " + (fr.get("optB") or "")
        elif lay == "cta":
            f["layout"] = "cta"
            f["text"] = teil["eyebrow"] or teil["text"]
            klein = "\n\n".join(x for x in [teil["text"] if teil["eyebrow"] else "", teil["klein"]] if x)
            if klein: f["klein"] = klein
            hg = [h for h in CTA_HG if h != vorher_hg][tag_nr % 2]
            stil = {"hg": hg, "schrift": "philo", "align": "center", "balken": "aus", "pos": 36,
                    "sticker": "link", "stickerText": "mumlifebalance.ch/ki-kurs/"}
        elif teil["punkte"]:
            f["layout"] = "kurs"
            f["text"] = teil["text"]
            f["punkte"] = teil["punkte"]
            if teil["eyebrow"]: f["eyebrow"] = teil["eyebrow"]
            if teil["klein"]: f["klein"] = teil["klein"]
            hg = [h for h in KURS_HG if h != vorher_hg][tag_nr % 2]
            stil = {"hg": hg, "balken": "karte", "farbe": "weiss" if hg != "creme" else "", "pos": 46}
        elif i == 0:
            # Einstieg: immer Foto, persönlich — Selfie von heute ist noch besser
            f["layout"] = "bild"
            f["text"] = teil["text"]
            if teil["eyebrow"]: f["eyebrow"] = teil["eyebrow"]
            if teil["klein"]: f["klein"] = teil["klein"]
            stil = dict(FOTOSTILE[foto_nr % len(FOTOSTILE)], hg="foto", foto=FOTOS[foto_nr % len(FOTOS)],
                        notiz="Am stärksten mit einem Foto oder Selfie von heute — unter „Hintergrund, Foto & Sticker“ tauschen.")
            foto_nr += 1
        elif zitat:
            f["layout"] = "learning"
            f["eyebrow"] = teil["eyebrow"]
            f["text"] = teil["text"]
            if teil["klein"]: f["klein"] = teil["klein"]
            hg = "petrol" if vorher_hg != "petrol" else "creme"
            stil = {"hg": hg, "schrift": "philo-k", "align": "center", "balken": "aus", "pos": 44, "groesse": 0.9}
        else:
            f["layout"] = "text"
            f["text"] = teil["text"]
            if teil["eyebrow"]: f["eyebrow"] = teil["eyebrow"]
            if teil["klein"]: f["klein"] = teil["klein"]
            # Jede dritte Textfolie als Foto, damit die Sequenz nicht nur aus Flächen besteht
            if i % 3 == 2 and len(teil["text"]) < 130:
                f["layout"] = "bild"
                stil = dict(FOTOSTILE[foto_nr % len(FOTOSTILE)], hg="foto", foto=FOTOS[foto_nr % len(FOTOS)])
                foto_nr += 1
            else:
                for _ in range(len(TEXTSTILE)):
                    s = TEXTSTILE[zyklus % len(TEXTSTILE)]
                    zyklus += 1
                    if s["hg"] != vorher_hg:
                        stil = dict(s)
                        break
        # Langer Nachsatz: etwas kleiner, damit nichts über den Rand läuft
        if len(f.get("klein", "")) > 220 or len(f.get("text", "")) > 170:
            stil["groesse"] = min(stil.get("groesse", 1), 0.85)
        f.update({k: v for k, v in stil.items() if v != ""})
        vorher_hg = f.get("hg")
        neu.append(f)

    # 🚨 Gegenprobe: dieselben Wörter vorher und nachher
    for alt, n in zip(frames, neu):
        vorher = woerter(alt.get("text", ""))
        nachher = woerter("\n".join([n.get("eyebrow", ""), n.get("text", ""), "\n".join(n.get("punkte", [])), n.get("klein", "")]))
        if sorted(vorher) != sorted(nachher):
            raise SystemExit("Wörter verändert in %s: %s" % (doc.get("name"), set(vorher) ^ set(nachher)))
    return neu


def neuer_name(doc):
    d = datetime.date.fromisoformat(doc["datum"])
    alt = doc.get("name", "")
    rest = re.sub(r"^(\d{1,2}\.\d{1,2}\.\s*·\s*\w+( abends)?\s*·\s*|[A-Z][a-z]([ -]Abend)?\s*·\s*)", "", alt)
    abends = " abends" if re.match(r"^[A-Z][a-z][ -]Abend", alt) or " abends ·" in alt else ""
    return "%d.%d. · %s%s · %s" % (d.day, d.month, WOCHENTAG[d.weekday()], abends, rest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quelle")
    ap.add_argument("--ziel", required=True)
    ap.add_argument("--ab", default="2026-10-09")
    ap.add_argument("--bis", default="2026-10-23")
    ap.add_argument("--nur-name", default="", help="Kennungen, bei denen nur der Name gesetzt wird (Komma)")
    a = ap.parse_args()
    ziel = pathlib.Path(a.ziel); ziel.mkdir(parents=True, exist_ok=True)
    nur_name = set(x for x in a.nur_name.split(",") if x)
    jetzt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    tage = sorted({json.load(open(p, encoding="utf-8")).get("datum", "")
                   for p in pathlib.Path(a.quelle).glob("*-ki-*.json")})
    for p in sorted(pathlib.Path(a.quelle).glob("*-ki-*.json")):
        doc = json.load(open(p, encoding="utf-8"))
        if not doc.get("datum"):
            continue
        aus = {"name": neuer_name(doc)}
        if p.stem not in nur_name and a.ab <= doc["datum"] <= a.bis:
            aus["frames"] = gestalten(doc, tage.index(doc["datum"]))
            aus["updatedAt"] = jetzt
        (ziel / p.name).write_text(json.dumps(aus, ensure_ascii=False), encoding="utf-8")
        print(p.stem, "·", aus["name"], "·", "neu gestaltet" if "frames" in aus else "nur Name")


if __name__ == "__main__":
    main()
