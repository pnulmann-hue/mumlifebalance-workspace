"""Den Hook vom Titelbild lesen — für die Konten, die ihn nicht in die Caption schreiben.

Patricia hat am 04.10.2026 ihre Nische benannt: reichweitenherz, karriere.mum,
juliatrost (Feld `nische: kern` in `context/competitor-watchlist.json`). Bei
reichweitenherz ist die Caption oft leer — der Hook steht nur auf dem Bild.
Wer nur die Caption liest, sieht dort nichts oder die falsche Zeile.

Holt die Titelbilder aus dem jüngsten Scrape (die Bild-Adressen von Instagram
laufen nach ein paar Tagen ab, darum nur die letzten Läufe), lässt Claude den
Text auf dem Bild lesen und legt ihn in `outputs/marktrecherche/bild-hooks.json`
ab. Schon gelesene Beiträge werden übersprungen. Die Bilder selbst werden nicht
gespeichert (fremdes Material, Repo ist öffentlich).

    python scripts/hooks/bild-hooks.py             # Kern-Konten
    python scripts/hooks/bild-hooks.py --laeufe 5  # wie viele jüngste Scrapes durchsuchen
"""

import argparse
import base64
import glob
import json
import os
import sys
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "outputs" / "apify-runs"
WATCH = ROOT / "context" / "competitor-watchlist.json"
ZIEL = ROOT / "outputs" / "marktrecherche" / "bild-hooks.json"
MODELL = "claude-opus-5-5"

AUFTRAG = """Das ist das Titelbild (erste Folie oder Reel-Cover) eines Instagram-Beitrags.
Gib nur den Text wieder, der als Überschrift/Hook auf dem Bild steht — wörtlich, in einer Zeile,
ohne Anführungszeichen. Kleingedrucktes, Namen, Handles und Logos weglassen.
Steht kein lesbarer Text auf dem Bild, antworte genau: KEIN TEXT"""


def lies(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--laeufe", type=int, default=4)
    a = ap.parse_args()

    import anthropic
    if not os.environ.get("ANTHROPIC_API_KEY"):
        for z in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if z.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = z.split("=", 1)[1].strip().strip('"')

    kern = {k["handle"] for k in (lies(WATCH) or {}).get("accounts", []) if k.get("nische") == "kern"}
    cache = lies(ZIEL) or {}
    offen = {}
    for f in sorted(glob.glob(str(RUNS / "competitors-*.json")))[-a.laeufe:]:
        for k in (lies(f) or {}).get("results", []):
            if k.get("username") not in kern:
                continue
            for p in k.get("latestPosts") or []:
                sc = p.get("shortCode")
                if sc and sc not in cache and p.get("displayUrl"):
                    offen[sc] = (k["username"], p["displayUrl"])
    for f in sorted(glob.glob(str(RUNS / "tiefe-*.json")))[-2:]:
        for p in (lies(f) or {}).get("posts", []):
            sc = p.get("shortCode")
            if p.get("ownerUsername") in kern and sc and sc not in cache and p.get("displayUrl"):
                offen[sc] = (p["ownerUsername"], p["displayUrl"])
    print(f"Kern-Konten: {', '.join(sorted(kern))} · neu zu lesen: {len(offen)}")

    client = anthropic.Anthropic()
    for i, (sc, (konto, url)) in enumerate(offen.items(), 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            daten = urllib.request.urlopen(req, timeout=30).read()
        except Exception as e:
            print(f"  {sc}: Bild nicht abrufbar ({e.__class__.__name__}) — Adresse vermutlich abgelaufen")
            continue
        try:
            r = client.messages.create(
                model=MODELL, max_tokens=2000, output_config={"effort": "low"},
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                 "data": base64.b64encode(daten).decode()}},
                    {"type": "text", "text": AUFTRAG}]}],
            )
        except anthropic.APIStatusError as e:
            print(f"  {sc}: Fehler {e.status_code}")
            continue
        if r.stop_reason == "refusal":
            continue
        text = "".join(b.text for b in r.content if b.type == "text").strip()
        cache[sc] = {"konto": konto, "text": "" if text.upper().startswith("KEIN TEXT") else text[:220]}
        ZIEL.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {i}/{len(offen)} {konto}: {cache[sc]['text'][:80] or '— kein Text —'}")


if __name__ == "__main__":
    main()
