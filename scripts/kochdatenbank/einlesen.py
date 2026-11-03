"""Kochdatenbank, Schritt 1 — jedes Rezept aus dem OneDrive-Rezeptordner als Eintrag.

    python scripts/kochdatenbank/einlesen.py --probe      # rund 50 Dateien zum Anschauen
    python scripts/kochdatenbank/einlesen.py              # alles, was neu oder geändert ist
    python scripts/kochdatenbank/einlesen.py --trocken    # nur zählen, was neu ist

Quelle: OneDrive/Dokumente/Patricia/Hobby/Rezepte (dort landen auch die fotografierten
Papierrezepte). Der Abgleich läuft über Pfad, Grösse und Änderungszeit in `gesehen.json` —
ein zweiter Lauf liest nur, was dazugekommen oder geändert ist.

Je Datei: Text aus PDF/Word, bei Scans und Fotos das Bild. Claude (Sonnet) macht daraus null,
eine oder mehrere Rezepte mit Kategorie, Unterart, Zutaten, Schritten und Nährwerten je Portion.
Nährwerte, die nicht im Rezept stehen, werden geschätzt und als „geschätzt“ markiert.

Ausgabe: outputs/kochdatenbank/daten/ (gitignored — Rezepte aus Zeitschriften und Kursen).
"""
import base64
import hashlib
import json
import os
import pathlib
import sys
import zipfile
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import anthropic  # noqa: E402
import pymupdf  # noqa: E402
from pydantic import BaseModel  # noqa: E402

WS = pathlib.Path(__file__).resolve().parents[2]
QUELLE = pathlib.Path.home() / "OneDrive/Dokumente/Patricia/Hobby/Rezepte"
ZIEL = WS / "outputs/kochdatenbank/daten"
EINTRAEGE = ZIEL / "eintraege"
GESEHEN = ZIEL / "gesehen.json"
ENDUNGEN = {".pdf", ".jpg", ".jpeg", ".png", ".docx"}
MAX_TEXT = 30_000
MAX_SEITEN_BILD = 4

# Dateien, die sicher keine Rezepte sind (Ernährungslehre, Training, Vorlagen)
KEIN_REZEPT = re.compile(r"(?i)fettsäuren|tiefenmuskulatur|workout|etikett|vitalstoffe|nährstoffe|"
                         r"nahrungsmittel für|wie ernähre ich|mixtabelle|ernährungsplan")

PROBE = {"Frühstück": 13, "Dessert": 14, "Hauptgang": 14, "Hauptgang vegi": 5, "Screenshots": 5}

# Die Coaching-Ernährungspläne (MyBodyAdvice) liegen nicht im Rezeptordner. Sie bekommen das Merkmal
# „Coaching-Plan“; Rezepte, die in mehreren Fassungen vorkommen, nimmt seite-bauen.py nur einmal.
PLAENE = [WS / "kochwissen" / n for n in (
    "Ernährungsplan Coaching 2026-04.pdf", "Ernährungsplan Coaching 2026-06-25.pdf",
    "Ernährungsplan Coaching AKTUELL 2026-08-10.pdf", "Ernährungsplan Coaching NEU 2026-08-31.pdf")]
PLAENE += [QUELLE / n for n in ("Ernährungsplan.pdf", "Ernährungsplan2.pdf", "Ernährungsplan3.pdf")]

# Patricias eigene Rezepte aus der 30-Tage-Energie-Routine (Markdown, je Datei 30 Rezepte)
EIGENE = [WS / "outputs/produkte/doterra-mama-energie" / n for n in (
    "12-30-fruehstuecke.md", "17-mittagessen.md", "18-abendessen.md", "19-zwischenmahlzeiten.md")]

# Patricia: „ich will da kein menu kochen wie mittags mit fleisch … eher was einfaches. aber es darf auch
# mal milchreis sein, gschwellti … optionen für mich, dass ich auf proteine schaue. auch mal falafel“
ZNACHT_REGEL = """true, wenn es als einfacher Znacht unter der Woche taugt (Schweizer Familie, Abendessen
  ohne Menü-Aufwand): Suppen, Eintöpfe, Wähen, Gschwellti mit Käse/Quark, Rösti, Milchreis, Griessbrei,
  Omeletten, Eierspeisen, Toast- und Brotgerichte mit Belag, Salate mit Protein, Bowls, Wraps, Falafel,
  Ofengemüse, Birchermüesli, Pasta- oder Reisgerichte, Quark- und Hüttenkäse-Gerichte, Tortilla, einfache
  Pfannengerichte. false bei Braten, Festtags- und Sonntagsfleisch, aufwendigen Hauptgängen mit Beilagen,
  Kuchen, Guetzli, Desserts ausser Milchreis/Griessbrei, Saucen, Eingemachtem, Getränken, Apéro-Gebäck."""


def env(name):
    for z in (WS / ".env").read_text(encoding="utf-8").splitlines():
        if z.startswith(name + "="):
            return z.split("=", 1)[1].strip().strip('"')
    sys.exit(f"❌ {name} fehlt in .env")


class Rezept(BaseModel):
    titel: str
    kurz: str                     # ein Satz, was es ist
    kategorie: Literal["Frühstück", "Fleisch", "Fisch", "Vegetarisch", "Suppe", "Salat", "Beilage",
                       "Snack & Apéro", "Brot & Gebäck", "Dessert", "Getränk", "Eingemachtes & Vorrat",
                       "Sauce & Basis"]
    unterart: str                 # siehe Auftrag; "" wenn keine passt
    portionen: int                # 0 = steht nicht da
    zeit_min: int                 # gesamte aktive Zeit, 0 = unbekannt
    zutaten: List[str]            # je Zeile Menge + Zutat, wie im Rezept
    schritte: List[str]
    kcal: int                     # je Portion
    protein: int                  # g je Portion
    kohlenhydrate: int
    fett: int
    naehrwerte: Literal["angegeben", "geschätzt"]
    thermomix: bool
    znacht: bool                  # taugt als einfacher Znacht, siehe ZNACHT_REGEL
    merkmale: List[Literal["vegetarisch", "vegan", "glutenfrei", "laktosefrei", "low carb", "zuckerfrei",
                           "kinderfreundlich", "einfrierbar", "Meal Prep", "schnell", "Ofen", "Grill",
                           "Festtag", "Weihnachten"]]
    saison: List[Literal["Frühling", "Sommer", "Herbst", "Winter"]]   # leer = ganzjährig
    link: str                     # Webadresse, wenn im Dokument sichtbar, sonst ""
    herkunft: str                 # Zeitschrift/Website/Kurs, wenn erkennbar, sonst ""


class Datei(BaseModel):
    rezepte: List[Rezept]


AUFTRAG = """Du liest eine Datei aus Patricias privatem Rezeptordner (Schweiz, Familie mit 4 Kindern) und
machst daraus Einträge für ihre Kochdatenbank. Eine Datei kann kein, ein oder mehrere Rezepte enthalten.
Ist es kein Rezept (Ernährungslehre, Einkaufsliste, Plan ohne Rezepte), gib eine leere Liste zurück.

Regeln:
- Zutaten und Schritte vollständig und in der Reihenfolge des Rezepts, Mengen wie dort. Schweizer
  Schreibweise mit ss, nichts erfinden. Unleserliches weglassen statt raten.
- kategorie: Hauptgang mit Fleisch → "Fleisch", mit Fisch/Meeresfrüchten → "Fisch", Hauptgang ohne
  Fleisch → "Vegetarisch". Kuchen, Torten, Guetzli gehören zu "Dessert"; Brot, Zopf, salzige Wähen zu
  "Brot & Gebäck"; Eintöpfe zu "Suppe" nur wenn es eine Suppe ist.
- unterart:
  Fleisch → genau eins von: Rind, Kalb, Schwein, Poulet, Hackfleisch, Lamm, Wild, Wurst & Speck, Gemischt
  Fisch → Lachs, Thunfisch, Weissfisch, Meeresfrüchte, Anderer Fisch
  Dessert → Kuchen & Torten, Cremen & Mousse, Glace & Parfait, Guetzli & Kleingebäck, Früchte, Warme Desserts, Proteinreich
  Frühstück → Süss, Herzhaft, Porridge & Müesli, Pancakes & Waffeln, Eier, Smoothie & Bowl
  Vegetarisch → Pasta, Kartoffeln, Hülsenfrüchte, Gemüse, Reis & Getreide, Eier & Käse, Wähe & Auflauf
  sonst: eine kurze sinnvolle Unterart oder "".
- Nährwerte je Portion. Stehen sie im Rezept, übernimm sie und setze naehrwerte="angegeben".
  Sonst schätze sie realistisch aus Zutaten und Portionenzahl (bei fehlender Portionenzahl eine übliche
  annehmen und in portionen eintragen) und setze "geschätzt".
- thermomix: true, wenn das Rezept für den Thermomix geschrieben ist (Stufe, Varoma, Linkslauf, Mixtopf).
- merkmale nur, wenn sie wirklich zutreffen. "schnell" = höchstens 30 Minuten.
- link: nur eine Adresse, die im Dokument steht.
- znacht: """ + ZNACHT_REGEL + """

Dateiname: {name}
Ordner: {ordner}
"""


def stempel(p):
    s = p.stat()
    return f"{s.st_size}:{int(s.st_mtime)}"


def kennung(rel):
    return hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12]


PLAN_ZUSATZ = """
Das ist ein persönlicher Ernährungsplan aus einem Coaching (Tageskalorien oben, je Kategorie mehrere
Mahlzeiten zur Wahl). Nimm JEDE Mahlzeit als eigenes Rezept auf. Der Text ist beim Auslesen zerstückelt
(„Mager quar k“ = Magerquark), setz die Wörter richtig zusammen. Die Mahlzeiten haben keinen Namen —
gib jeder einen kurzen, treffenden Titel aus den Hauptzutaten (z.B. „Dinkel-Quark-Pancakes“).
Nährwerte stehen je Mahlzeit da: naehrwerte="angegeben", portionen=1.
Kategorie nach Art der Mahlzeit (Frühstück, Hauptgericht mit Fleisch/Fisch/vegetarisch, Snack & Apéro).
"""


EIGEN_ZUSATZ = """
Das sind Patricias eigene Rezepte aus ihrer 30-Tage-Energie-Routine (Markdown, rund 30 Rezepte je Datei).
Nimm JEDES Rezept einzeln auf, Zutaten für die Familienmenge, Nährwerte so, wie sie dastehen.
"""
MERKMAL = {"plan": "Coaching-Plan", "eigen": "Energie-Routine"}


def inhalt(p, max_text=MAX_TEXT):
    """Liefert die Inhaltsblöcke für Claude: Text, sonst Bilder."""
    endung = p.suffix.lower()
    if endung in (".jpg", ".jpeg", ".png"):
        return [bild(p.read_bytes(), endung)]
    if endung == ".md":
        return [{"type": "text", "text": p.read_text(encoding="utf-8")[:max_text]}]
    if endung == ".docx":
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
        text = re.sub(r"<w:p[ >]", "\n<w:p ", xml)
        text = re.sub(r"<[^>]+>", "", text)
        return [{"type": "text", "text": text[:MAX_TEXT]}]
    doc = pymupdf.open(p)
    text = "\n".join(seite.get_text() for seite in doc)
    if len(text.strip()) > 150 * max(1, min(len(doc), 3)):
        return [{"type": "text", "text": text[:max_text]}]
    bloecke = []
    for seite in list(doc)[:MAX_SEITEN_BILD]:
        pix = seite.get_pixmap(dpi=110)
        bloecke.append(bild(pix.tobytes("jpeg"), ".jpg"))
    return bloecke


def bild(daten, endung):
    if len(daten) > 3_500_000:  # grosse Handyfotos verkleinern
        pix = pymupdf.Pixmap(daten)
        faktor = max(1, int((pix.width * pix.height / 2_500_000) ** 0.5) + 1)
        pix = pymupdf.Pixmap(pix, pix.width // faktor, pix.height // faktor, None)
        daten, endung = pix.tobytes("jpeg"), ".jpg"
    typ = "image/png" if endung == ".png" else "image/jpeg"
    return {"type": "image", "source": {"type": "base64", "media_type": typ,
                                        "data": base64.b64encode(daten).decode()}}


def lesen(client, p, rel, art="datei"):
    lang = art in ("plan", "eigen")
    try:
        bloecke = inhalt(p, 90_000 if lang else MAX_TEXT)
        bloecke.append({"type": "text", "text": AUFTRAG.format(name=p.name, ordner=str(pathlib.Path(rel).parent))
                        + {"plan": PLAN_ZUSATZ, "eigen": EIGEN_ZUSATZ}.get(art, "")})
        with client.messages.stream(
            model="claude-sonnet-5-5", max_tokens=64000 if lang else 16000, output_config={"effort": "low"},
            messages=[{"role": "user", "content": bloecke}], output_format=Datei,
        ) as s:
            fertig = s.get_final_message()
        roh = "".join(b.text for b in fertig.content if b.type == "text")
        rezepte = Datei.model_validate_json(roh).rezepte
    except Exception as e:
        print(f"  ❌ {rel}: {str(e)[:160]}")
        return None
    k = kennung(rel)
    eintraege = []
    for i, r in enumerate(rezepte):
        e = r.model_dump()
        e.update({"id": f"{k}-{i}", "datei": rel})
        if art in MERKMAL:
            e["merkmale"].append(MERKMAL[art])
        eintraege.append(e)
    (EINTRAEGE / f"{k}.json").write_text(json.dumps(eintraege, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ {len(eintraege)} · {rel}")
    return eintraege


LINKS = ZIEL / "links.txt"   # je Zeile eine Rezeptadresse (Swissmilk, Migusto, Cookidoo …)

LINK_ZUSATZ = """
Das ist der Text einer Rezept-Website. Lies Titel, Art, Portionen, Zeit und Nährwerte heraus. Zutaten
und Schritte brauchst du nur zum Einordnen und Schätzen: das Rezept bleibt auf der Website, gib deshalb
zutaten und schritte als LEERE Listen zurück. Genau ein Rezept.
"""


def seite_text(url):
    import html as h
    import urllib.request
    anfrage = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    roh = urllib.request.urlopen(anfrage, timeout=30).read().decode("utf-8", "replace")
    roh = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", roh)
    return re.sub(r"\s+", " ", h.unescape(re.sub(r"<[^>]+>", " ", roh)))[:MAX_TEXT]


def lesen_link(client, url):
    try:
        text = seite_text(url)
        with client.messages.stream(
            model="claude-sonnet-5-5", max_tokens=8000, output_config={"effort": "low"},
            messages=[{"role": "user", "content": text + "\n\n" + AUFTRAG.format(name=url, ordner="Website") + LINK_ZUSATZ}],
            output_format=Datei,
        ) as s:
            fertig = s.get_final_message()
        rezepte = Datei.model_validate_json("".join(b.text for b in fertig.content if b.type == "text")).rezepte[:1]
    except Exception as e:
        print(f"  ❌ {url}: {str(e)[:160]}")
        return None
    k = kennung("link:" + url)
    eintraege = []
    for r in rezepte:
        e = r.model_dump()
        e.update({"id": f"{k}-0", "datei": "", "link": url, "zutaten": [], "schritte": []})
        e["merkmale"].append("Online")
        eintraege.append(e)
    (EINTRAEGE / f"{k}.json").write_text(json.dumps(eintraege, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  ✓ {len(eintraege)} · {url}")
    return eintraege


def dateien():
    alle = []
    for p in sorted(QUELLE.rglob("*")):
        if p.is_file() and p.suffix.lower() in ENDUNGEN and not KEIN_REZEPT.search(p.name):
            alle.append(p)
    return alle


def main():
    EINTRAEGE.mkdir(parents=True, exist_ok=True)
    gesehen = json.loads(GESEHEN.read_text(encoding="utf-8")) if GESEHEN.exists() else {}
    alle = dateien()
    if "--probe" in sys.argv:
        auswahl = []
        for ordner, n in PROBE.items():
            auswahl += [p for p in alle if p.parent == QUELLE / ordner][:n]
        alle = auswahl
    # Aufgaben: (Schlüssel in gesehen.json, Stempel, Arbeit)
    aufgaben = [(p.relative_to(QUELLE).as_posix(), stempel(p), ("datei", p)) for p in alle]
    if "--probe" not in sys.argv:
        aufgaben += [(f"Coaching/{p.name}", stempel(p), ("plan", p)) for p in PLAENE if p.exists()]
        aufgaben += [(f"Energie-Routine/{p.name}", stempel(p), ("eigen", p)) for p in EIGENE if p.exists()]
        links = [z.strip() for z in LINKS.read_text(encoding="utf-8").splitlines()
                 if z.strip().startswith("http")] if LINKS.exists() else []
        aufgaben += [(f"link:{u}", "1", ("link", u)) for u in links]
    neu = [a for a in aufgaben if gesehen.get(a[0]) != a[1]]
    print(f"{len(aufgaben)} Quellen, davon {len(neu)} neu oder geändert")
    if "--trocken" in sys.argv:
        for a in neu[:40]:
            print("  ·", a[0])
        return
    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))

    def eins(a):
        schluessel, st, (art, ding) = a
        if art == "link":
            ok = lesen_link(client, ding)
        else:
            ok = lesen(client, ding, schluessel, art)
        return (schluessel, st) if ok is not None else None

    with ThreadPoolExecutor(6) as pool:
        for r in pool.map(eins, neu):
            if r:
                gesehen[r[0]] = r[1]
                GESEHEN.write_text(json.dumps(gesehen, ensure_ascii=False, indent=0), encoding="utf-8")
    # gelöschte Dateien aus der Datenbank nehmen (nur bei vollem Lauf)
    if "--probe" not in sys.argv:
        da = {a[0] for a in aufgaben}
        for rel in [r for r in gesehen if r not in da]:
            (EINTRAEGE / f"{kennung(rel)}.json").unlink(missing_ok=True)
            del gesehen[rel]
        GESEHEN.write_text(json.dumps(gesehen, ensure_ascii=False, indent=0), encoding="utf-8")


if __name__ == "__main__":
    main()
