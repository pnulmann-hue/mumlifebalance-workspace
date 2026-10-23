"""Öl-App, Schritt 5 — Tipps und Rezepte aus den Telegram-Gruppen.

    powershell -ExecutionPolicy Bypass -File scripts/doterra/ocr-windows.ps1 outputs/oel-app/roh/telegram/bilder -Filter *.jpg
    python scripts/oel-app/tipps-bauen.py              # nur Chats, die neu sind oder gewachsen
    python scripts/oel-app/tipps-bauen.py --neu

Liest outputs/oel-app/roh/telegram/<chatId>.json (aus scripts/telegram-userbot/src/oel-gruppen-holen.ts)
samt erkanntem Text der Bildkarten, teilt jeden Chat in Pakete und lässt Claude daraus herausziehen,
was als Tipp, Rezept oder Wissen taugt. Plaudern, Grüsse, Bestellfragen, Business fallen weg.

Ausgabe: outputs/oel-app/daten/tipps/<chatId>.json (je Chat, mit Stand) und tipps.json (alle).
🚨 NUR FÜR PATRICIA — Nachrichten anderer Menschen. Keine Personennamen in den Tipps.
"""
import json
import pathlib
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import anthropic  # noqa: E402
from pydantic import BaseModel  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from produkte_gemeinsam import env  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
ROH = WS / "outputs/oel-app/roh/telegram"
ZIEL = WS / "outputs/oel-app/daten/tipps"
ANLIEGEN = WS / "context/doTERRA/Produktwissen/anliegen.json"
KATALOG = WS / "outputs/oel-app/daten/katalog.json"
PAKET = 60_000
LEER = re.compile(r"^(danke|merci|super|toll|cool|ja|nein|ok|hihi|haha|❤️|🙏|👍|😍|🥰|🙌)[\s!.❤️🙏👍😍🥰🙌]*$", re.I)


class Tipp(BaseModel):
    titel: str
    art: Literal["Rezept", "Anwendung", "Wissen", "Erfahrung", "Haushalt", "Kinder", "Emotion", "Ernährung"]
    text: str                 # der Tipp in eigenen Worten, vollständig genug zum Nachmachen
    zutaten: List[str]        # bei Rezepten mit Mengen, sonst leer
    produkte: List[str]       # Produktnamen wie in der Produktliste
    themen: List[str]         # Themen-Kennungen aus der Themenliste, die passen
    nachrichten: List[int]    # Nummern der Nachrichten, aus denen der Tipp stammt


class Paket(BaseModel):
    tipps: List[Tipp]


AUFTRAG = """Hier ist ein Ausschnitt aus einer Telegram-Gruppe rund um doTERRA-Öle. Zieh alles heraus, was
Patricia in ihrer privaten Öl-App nachschlagen möchte: Rezepte (Roller, Diffuser, Küche, Kosmetik,
Putzmittel), Anwendungstipps, Hintergrundwissen zu Ölen und Nahrungsergänzungen, Erfahrungen mit
Produkten, Tipps für Kinder, Emotionen, Ernährung.

Regeln:
- Weglassen: Plaudern, Grüsse, Bestell- und Lieferfragen, Aktionen und Preise, Business, Teamaufbau,
  Termine, Werbung für Calls.
- Keine Personennamen. Erfahrungen anonym („eine Teilnehmerin …“).
- Zusammengehöriges (Frage + Antworten) wird EIN Tipp. Dasselbe zweimal → einmal.
- Nur was im Chat steht; nichts aus eigenem Wissen dazu. Mengen genau übernehmen.
- „[Bildtext …]“ ist per Texterkennung gelesen und kann Fehler haben — offensichtliche Lesefehler
  stillschweigend korrigieren, Unklares weglassen.
- Produktnamen wie in der Produktliste, Themen nur aus der Themenliste (Kennung).
- Deutsch, Schweizer Schreibweise (ss statt ß). Steht nichts Brauchbares drin: leere Liste.

"""


def bildtext(b):
    t = (ROH / "bilder" / b).with_suffix(".txt")
    return t.read_text(encoding="utf-8-sig", errors="ignore").strip() if b and t.exists() else ""


def pakete(nachrichten):
    zeilen = []
    for m in nachrichten:
        text, bt = (m.get("text") or "").strip(), bildtext(m.get("bild"))
        if len(text) < 25 and not bt:
            continue
        if LEER.match(text) and not bt:
            continue
        z = f"#{m['id']} {m['datum'][:10]}: {text}"
        if bt and len(bt) > 40:
            z += f"\n[Bildtext: {bt[:3000]}]"
        zeilen.append(z)
    paket, n = [], 0
    for z in zeilen:
        if n + len(z) > PAKET and paket:
            yield "\n\n".join(paket)
            paket, n = [], 0
        paket.append(z)
        n += len(z)
    if paket:
        yield "\n\n".join(paket)


def ausziehen(client, chat, nr, text, kopf):
    try:
        # 🚨 Mit 16'000 Token riss die Antwort bei der Kosmetik-Gruppe ab (zu viele Rezepte in einem
        #    Paket). Mehr Platz verlangt Streaming.
        with client.messages.stream(
            model="claude-opus-5-5", max_tokens=48000, output_config={"effort": "low"},
            messages=[{"role": "user", "content": AUFTRAG + kopf + f"\n\nGRUPPE: {chat}\n\n" + text}],
            output_format=Paket,
        ) as s:
            fertig = s.get_final_message()
        return Paket.model_validate_json("".join(b.text for b in fertig.content if b.type == "text")).tipps
    except Exception as e:
        print(f"  ❌ {chat} Paket {nr}: {e}")
        return None


def main():
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))
    themen = [f"{a['id']} ({a['name']})" for a in json.loads(ANLIEGEN.read_text(encoding="utf-8"))["anliegen"]]
    namen = [p["name"] for p in json.loads(KATALOG.read_text(encoding="utf-8"))["produkte"]]
    kopf = "PRODUKTLISTE: " + ", ".join(namen) + "\n\nTHEMENLISTE: " + ", ".join(themen)
    ZIEL.mkdir(parents=True, exist_ok=True)

    auftraege = []
    for f in sorted(ROH.glob("*.json")):
        nachrichten = json.loads(f.read_text(encoding="utf-8"))
        if not nachrichten:
            continue
        ziel = ZIEL / f.name
        if ziel.exists() and "--neu" not in sys.argv:
            if json.loads(ziel.read_text(encoding="utf-8"))["anzahl"] == len(nachrichten):
                continue
        chat = nachrichten[0]["chat"]
        for nr, text in enumerate(pakete(nachrichten)):
            auftraege.append((f, chat, len(nachrichten), nr, text))
    print(f"{len(auftraege)} Pakete aus {len({a[0] for a in auftraege})} Chats")

    with ThreadPoolExecutor(8) as ex:
        ergebnisse = list(ex.map(lambda a: (a, ausziehen(client, a[1], a[3], a[4], kopf)), auftraege))

    je_chat = {}
    for (f, chat, anzahl, nr, _), tipps in ergebnisse:
        e = je_chat.setdefault(f, {"chat": chat, "anzahl": anzahl, "fehler": 0, "tipps": []})
        if tipps is None:
            e["fehler"] += 1
            continue
        e["tipps"] += [dict(t.model_dump(), chat=chat) for t in tipps]
    for f, e in je_chat.items():
        if e["fehler"]:  # unvollständig: nicht als fertig ablegen, damit der nächste Lauf es nachholt
            e["anzahl"] = -1
        (ZIEL / f.name).write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {len(e['tipps']):4} Tipps  {e['chat']}" + (f"  ⚠️ {e['fehler']} Pakete fehlgeschlagen" if e["fehler"] else ""))

    alle = []
    for f in sorted(ZIEL.glob("-*.json")) + sorted(ZIEL.glob("[0-9]*.json")):
        alle += json.loads(f.read_text(encoding="utf-8"))["tipps"]
    for i, t in enumerate(alle):
        t["id"] = f"t{i + 1}"
    (ZIEL.parent / "tipps.json").write_text(json.dumps(alle, ensure_ascii=False), encoding="utf-8")
    print(f"→ {len(alle)} Tipps in outputs/oel-app/daten/tipps.json")


if __name__ == "__main__":
    main()
