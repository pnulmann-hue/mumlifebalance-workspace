"""Öl-App — ALLES aus den Quellen: jede Aussage zu einem Öl oder Produkt und jedes Rezept, vollständig.

    python scripts/oel-app/wissen-ausziehen.py --trocken   # nur zählen: Pakete, Zeichen, geschätzte Kosten
    python scripts/oel-app/wissen-ausziehen.py             # alle Pakete, die noch fehlen (wiederholbar)

Patricia, 22.10.2026: *„nicht das gesamte buch … aber halt einfach die tipps und texte zu den ölen und
die rezepte. das hätte ich schon gerne vollständig“*. produkte-bauen.py liest je Produkt nur die
passendsten rund 40 Stellen; dieser Durchgang liest JEDEN Abschnitt aus quellen.py, Quelle für Quelle
in Paketen, und zieht heraus, was dort zu Ölen und Produkten steht, plus jedes Rezept mit Mengen.
In eigenen Worten (kein Abschreiben ganzer Passagen), mit Quelle und Seite.

Ausgabe: outputs/oel-app/daten/auszug/<nr>.json je Paket (gitignored) — app-bauen.py ordnet die
Aussagen den Produkten zu und legt die Rezepte zu den übrigen.
🚨 Draussen bleiben Coaching-Unterlagen, Business- und Arbeitsblätter (RAUS) — der Kompass geht an Kundinnen.
"""
import hashlib
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
import quellen  # noqa: E402
from produkte_gemeinsam import env  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
KATALOG = WS / "outputs/oel-app/daten/katalog.json"
ZIEL = WS / "outputs/oel-app/daten/auszug"
PAKET = 45_000
OELBEZUG = re.compile(r"ätherisch|aetherisch|\bÖl\b|\böle\b|doTERRA|Tropfen", re.I)
# bezahlte Coachings, Business-Unterlagen und leere Arbeitsblätter gehören nicht in ein Öl-Nachschlagewerk
RAUS = re.compile(r"coaching|unbox your network|recruitment|claims|business|worksheet|arbeitsblatt|agreement|"
                  r"^mba-|ernaehrungsplan|ohne-coaching|lebensmittel tauschen", re.I)


class Aussage(BaseModel):
    produkte: List[str]   # Öle/Produkte, um die es geht — Namen wie in der Produktliste
    art: Literal["aromatisch", "äusserlich", "innerlich", "Emotion", "Kinder", "Haushalt", "Sicherheit",
                 "Hintergrund"]
    text: str             # die Aussage vollständig, in eigenen Worten, so dass man sie anwenden kann
    quelle: str           # Titel genau wie im Auszug
    wo: str               # Seite/Kapitel genau wie im Auszug


class Rezept(BaseModel):
    titel: str
    zweck: Literal["Diffuser", "Roller", "Haut & Bad", "Küche & Trinken", "Haushalt", "Kinder", "Sonstiges"]
    zutaten: List[str]    # mit Mengen, genau übernommen
    anleitung: str
    quelle: str
    wo: str


class Auszug(BaseModel):
    aussagen: List[Aussage]
    rezepte: List[Rezept]


AUFTRAG = """Du liest Abschnitte aus Patricias Öl-Unterlagen (Bücher, Hefte, Kursunterlagen) für ihr
Nachschlagewerk zu ätherischen Ölen. Zieh VOLLSTÄNDIG heraus:

1. aussagen: jede Aussage, die zu einem bestimmten Öl, einer Mischung oder einem Produkt etwas sagt —
   Anwendung, Wirkung laut Quelle, Dosierung, Verdünnung, Sicherheit, Emotion, Hintergrund (Pflanze,
   Gewinnung, Inhaltsstoffe). Eine Aussage je Gedanke, so vollständig, dass man sie ohne das Buch anwenden
   kann. In eigenen Worten, keine langen Passagen abschreiben. Gilt eine Aussage für mehrere Öle, alle nennen.
2. rezepte: jedes Rezept und jede Mischung mit Mengen, in der mindestens ein ätherisches Öl oder ein
   doTERRA-Produkt vorkommt (Diffuser, Roller, Salben, Bäder, Küche, Putzmittel, Kinder). Kochrezepte ganz
   ohne Öl gehören nicht hinein. Zutaten und Mengen genau übernehmen, Anleitung knapp.

Regeln: nur was in den Abschnitten steht, nichts aus eigenem Wissen. Allgemeines ohne Bezug zu einem Öl
(Biografie, Werbung, Inhaltsverzeichnis) weglassen. Produktnamen wie in der Produktliste; ein Öl, das nicht
in der Liste steht, mit seinem Namen aus dem Text. Quelle und Seite genau wie im Kopf des Abschnitts.
Deutsch, Schweizer Schreibweise (ss statt ß). Steht nichts Brauchbares drin: leere Listen.

"""


def pakete(alle):
    """Je Quelle eigene Pakete — nie zwei Quellen in einem.

    🚨 Erst lief alles in einem Strom: Kam ein neues Heft dazu, verschoben sich alle Paketgrenzen dahinter,
    jedes Paket bekam eine neue Kennung, und der nächste Lauf hätte fast alles neu gelesen und bezahlt.
    So kostet eine neue Quelle nur sich selbst."""
    je_quelle = {}
    for a in alle:
        je_quelle.setdefault(a["p"], []).append(f"[{a['q']} · {a['w']}]\n{a['t']}")
    for pfad in sorted(je_quelle):
        paket, n = [], 0
        for z in je_quelle[pfad]:
            if n + len(z) > PAKET and paket:
                yield pfad, paket
                paket, n = [], 0
            paket.append(z)
            n += len(z)
        if paket:
            yield pfad, paket


def datei(paket):
    """Name nur aus dem Inhalt: gleiches Paket = gleiche Datei, egal an welcher Stelle es steht."""
    return ZIEL / f"{hashlib.sha1(chr(10).join(paket).encode()).hexdigest()[:16]}.json"


def ausziehen(client, nr, paket, kopf):
    text = "\n\n".join(paket)
    ziel = datei(paket)
    if ziel.exists():
        return "da"
    try:
        with client.messages.stream(
            model="claude-opus-5-5", max_tokens=48000, output_config={"effort": "low"},
            messages=[{"role": "user", "content": AUFTRAG + kopf + "\n\nABSCHNITTE:\n\n" + text}],
            output_format=Auszug,
        ) as s:
            fertig = s.get_final_message()
        a = Auszug.model_validate_json("".join(b.text for b in fertig.content if b.type == "text"))
    except Exception as e:
        print(f"  ❌ Paket {nr}: {str(e)[:200]}")
        if "usage limits" in str(e):
            raise SystemExit("API-Limit erreicht — Lauf abgebrochen, fertige Pakete bleiben.")
        return "fehler"
    ziel.write_text(a.model_dump_json(), encoding="utf-8")
    print(f"  ✓ Paket {nr:4}: {len(a.aussagen):3} Aussagen · {len(a.rezepte):3} Rezepte")
    return "neu"


def main():
    alle = [a for a in quellen.abschnitte() if not RAUS.search(a["q"]) and not RAUS.search(a["p"])]
    # Ernährungsbücher nur dort, wo sie Öle überhaupt erwähnen (482 von 2'405 Abschnitten am 22.10.)
    alle = [a for a in alle if a["k"] != "Ernährung" or OELBEZUG.search(a["t"])]
    # dasselbe Buch unter zwei Dateinamen nur einmal (Praxis-Aromatherapie, Jahn, Duft Medizin für Kinder)
    gesehen, eindeutig = set(), []
    for a in alle:
        fp = quellen.A.norm(a["t"])[:160]
        if fp not in gesehen:
            gesehen.add(fp)
            eindeutig.append(a)
    liste = [p for _, p in pakete(eindeutig)]
    offen = [p for p in liste if not datei(p).exists()]   # nur die kosten Geld
    zeichen = sum(len(z) for p in offen for z in p)
    print(f"{len(eindeutig)} Abschnitte (ohne Dubletten und Coaching) aus "
          f"{len({a['q'] for a in eindeutig})} Quellen → {len(liste)} Pakete, davon {len(offen)} noch offen "
          f"({zeichen / 1e6:.1f} Mio. Zeichen)")
    if "--trocken" in sys.argv:
        ein = zeichen / 3.3 / 1e6 + len(offen) * 0.004   # Mio. Token Eingang, mit Produktliste je Paket
        aus = len(offen) * 4000 / 1e6                      # kleine Pakete liefern weniger
        print(f"geschätzt: Eingang ~{ein:.1f} Mio. Token, Ausgabe ~{aus:.1f} Mio. Token → rund {ein * 4 + aus * 20:.0f} USD")
        return
    namen = [p["name"] for p in json.loads(KATALOG.read_text(encoding="utf-8"))["produkte"]]
    kopf = "PRODUKTLISTE: " + ", ".join(namen)
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))
    ZIEL.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(8) as ex:
        ergebnis = list(ex.map(lambda x: ausziehen(client, x[0], x[1], kopf), enumerate(liste)))
    print(f"→ neu {ergebnis.count('neu')} · schon da {ergebnis.count('da')} · Fehler {ergebnis.count('fehler')}")


if __name__ == "__main__":
    main()
