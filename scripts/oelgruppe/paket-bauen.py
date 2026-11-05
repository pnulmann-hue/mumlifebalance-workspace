"""Saison-Impulse der Gruppe „Gesund durchs ganze Jahr": Markdown -> paket.json + Cockpit-Dokumente.

    python scripts/oelgruppe/paket-bauen.py outputs/telegram-posts/winter-2026 --start 2026-12-05 [--cockpit <ordner>]

Liest <ordner>/<saison>-<jahr>-alle-beitraege.md und <ordner>/kacheln.json.
Rhythmus: Di · Do · Sa · So, Uhrzeiten wechseln. Der Abschluss-Post bekommt die höchste Nummer.
Die Kacheln rendert scripts/karussell-render/saison-kacheln.js, eingeplant wird über
scripts/telegram-userbot/src/saison-einplanen.ts. Mit --cockpit entsteht je Beitrag ein Dokument
für die Sammlung „doterra-freigaben“ (Bild verkleinert als dataUrl).
"""
import argparse
import base64
import datetime as dt
import io
import json
import pathlib
import re
import sys

CHAT = -1002221396127  # der Channel, nicht die alte gleichnamige Gruppe -4518699226
TAGE = {1, 3, 5, 6}  # Di, Do, Sa, So
ZEITEN = ["11:15", "19:45", "09:15", "16:30", "08:30", "14:15", "20:10", "07:45",
          "17:30", "10:20", "13:40", "18:15", "09:45", "15:50", "08:15", "20:30"]


def teile(md):
    posts = []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        kopf, _, rest = block.partition("\n")
        if "Eröffnungspost" in kopf:
            nr = 0
        elif re.search(r"Abschluss-Post", kopf):
            nr = 999
        else:
            m = re.search(r"Beitrag\s+(\d+)", kopf)
            if not m:
                continue
            nr = int(m.group(1))
        titel = re.split(r"\s[—-]\s", kopf, maxsplit=1)[-1].strip()
        text = rest.split("\n---", 1)[0].strip()
        posts.append({"nr": nr, "titel": titel, "text": text})
    posts.sort(key=lambda p: p["nr"])
    letzte = len(posts) - 1
    if posts[-1]["nr"] == 999:
        posts[-1]["nr"] = letzte
    return posts


def termine(start, n):
    tag, raus = start, []
    while len(raus) < n:
        if tag.weekday() in TAGE or not raus:
            raus.append(f"{tag.isoformat()}T{ZEITEN[len(raus) % len(ZEITEN)]}")
        tag += dt.timedelta(days=1)
    return raus


def bild_daten(pfad):
    from PIL import Image
    im = Image.open(pfad).convert("RGB")
    im.thumbnail((320, 320))
    puffer = io.BytesIO()
    im.save(puffer, "JPEG", quality=70)
    return "data:image/jpeg;base64," + base64.b64encode(puffer.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ordner")
    ap.add_argument("--start", required=True)
    ap.add_argument("--cockpit")
    a = ap.parse_args()
    ordner = pathlib.Path(a.ordner)
    saison, jahr = ordner.name.rsplit("-", 1)
    md = (ordner / f"{ordner.name}-alle-beitraege.md").read_text(encoding="utf-8")
    kacheln = json.loads((ordner / "kacheln.json").read_text(encoding="utf-8"))
    posts = teile(md)
    daten = termine(dt.date.fromisoformat(a.start), len(posts))
    for p, d in zip(posts, daten):
        p["datum"] = d
        if str(p["nr"]) not in kacheln:
            sys.exit(f"Keine Kachel für Beitrag {p['nr']}")
        p["kachel"] = kacheln[str(p["nr"])]
    paket = {"saison": saison, "jahr": int(jahr), "chat": CHAT, "beitraege": posts}
    (ordner / "paket.json").write_text(json.dumps(paket, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(posts), "Beiträge,", daten[0], "bis", daten[-1], "· längster Text", max(len(p["text"]) for p in posts))

    if a.cockpit:
        ziel = pathlib.Path(a.cockpit)
        ziel.mkdir(parents=True, exist_ok=True)
        for p in posts:
            kachel = ordner / "tiles" / f"post-{p['nr']}.png"
            doc = {"art": "saison", "paket": ordner.name, "saison": saison.capitalize(), "jahr": int(jahr),
                   "nr": p["nr"], "titel": p["titel"], "text": p["text"], "datum": p["datum"], "status": "entwurf",
                   "bild": bild_daten(kachel) if kachel.exists() else ""}
            (ziel / f"saison-{ordner.name}-{p['nr']:02d}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        print("Cockpit-Dokumente ->", ziel)


if __name__ == "__main__":
    main()
