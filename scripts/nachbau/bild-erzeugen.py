"""
Erzeugt ein Bild ueber Google AI Studio (Gemini / Nano Banana) fuer Einblendungen.

Laeuft nur mit GOOGLE_AI_API_KEY aus scripts/nachbau/.env.
Kosten: rund 2 Rappen je Bild.

Aufruf:
  python scripts/nachbau/bild-erzeugen.py "beschreibung" --name abhaengig
  python scripts/nachbau/bild-erzeugen.py "..." --modell gemini-3-pro-image
  python scripts/nachbau/bild-erzeugen.py --modelle          # zeigt verfuegbare

🚨 Marken-Regel: KEINE erfundenen Szenen aus Patricias Leben. Erzeugt werden
nur **erkennbar gestaltete** Elemente — Formen, Flaechen, Grafiken, Metaphern.
Nie ein Foto, das man fuer eine echte Aufnahme halten koennte.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parents[1]
ZIEL = WURZEL / "nachbau" / "_bilder"
BASIS = "https://generativelanguage.googleapis.com/v1beta"

# Patricias Farben — gehen in jeden Auftrag mit
MARKE = (
    "Colour palette strictly limited to: deep teal #12828c, dark navy #0c1c30, "
    "muted teal #29556d, warm cream #f1ecdd, burnt orange #dc822e. "
    "No yellow, no gold, no pink. Flat graphic design, not photographic. "
    "Clean, calm, generous negative space. Vertical 9:16 composition."
)


def schluessel():
    for zeile in (HIER / ".env").read_text(encoding="utf-8").splitlines():
        if zeile.startswith("GOOGLE_AI_API_KEY="):
            wert = zeile.split("=", 1)[1].strip()
            if wert:
                return wert
    sys.exit("GOOGLE_AI_API_KEY fehlt in scripts/nachbau/.env")


def holen(url, daten=None):
    kopf = {"Content-Type": "application/json"}
    rumpf = json.dumps(daten).encode() if daten else None
    anfrage = urllib.request.Request(url, data=rumpf, headers=kopf,
                                     method="POST" if daten else "GET")
    try:
        with urllib.request.urlopen(anfrage, timeout=180) as a:
            return json.loads(a.read())
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
        try:
            f = json.loads(text)["error"]
            sys.exit(f"Google sagt: {f.get('status')} — {f.get('message')}")
        except (KeyError, json.JSONDecodeError):
            sys.exit(f"HTTP {e.code}: {text[:300]}")


def main():
    p = argparse.ArgumentParser(description="Bild fuer Einblendungen erzeugen.")
    p.add_argument("beschreibung", nargs="?", help="was zu sehen sein soll (deutsch oder englisch)")
    p.add_argument("--name", default=None, help="Dateiname ohne Endung")
    p.add_argument("--modell", default="gemini-2.5-flash-image",
                   help="Standard: gemini-2.5-flash-image (guenstig). "
                        "Besser: gemini-3-pro-image")
    p.add_argument("--modelle", action="store_true", help="verfuegbare Bildmodelle zeigen")
    p.add_argument("--ohne-marke", action="store_true",
                   help="Farbvorgabe weglassen (nur fuer Versuche)")
    a = p.parse_args()

    key = schluessel()

    if a.modelle:
        d = holen(f"{BASIS}/models?key={key}")
        for m in d.get("models", []):
            n = m["name"].split("/")[-1]
            if "image" in n:
                print(f"  {n}")
        return

    if not a.beschreibung:
        p.error("Beschreibung fehlt.")

    auftrag = a.beschreibung if a.ohne_marke else f"{a.beschreibung}\n\n{MARKE}"
    print(f"  Modell: {a.modell}")
    print(f"  Auftrag: {a.beschreibung[:70]}…")

    antwort = holen(
        f"{BASIS}/models/{a.modell}:generateContent?key={key}",
        {"contents": [{"parts": [{"text": auftrag}]}]},
    )

    ZIEL.mkdir(parents=True, exist_ok=True)
    name = a.name or f"{datetime.now():%H%M%S}"
    gemacht = []
    for kand in antwort.get("candidates", []):
        for i, teil in enumerate(kand.get("content", {}).get("parts", [])):
            roh = teil.get("inlineData") or teil.get("inline_data")
            if not roh:
                continue
            endung = (roh.get("mimeType") or roh.get("mime_type") or "image/png").split("/")[-1]
            datei = ZIEL / f"{name}{'' if not gemacht else f'-{i}'}.{endung}"
            datei.write_bytes(base64.b64decode(roh["data"]))
            gemacht.append(datei)

    if not gemacht:
        text = json.dumps(antwort)[:400]
        sys.exit(f"Kein Bild in der Antwort. Anfang der Antwort:\n{text}")

    for d in gemacht:
        print(f"\n✅ {d.relative_to(WURZEL)}  ({d.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
