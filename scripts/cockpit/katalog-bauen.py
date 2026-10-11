"""
Schritt 1 des Angebots-Ausbaus: Schubladen und echte Preise.

Bisher stand im Cockpit eine flache Liste mit Preisen aus einer Markdown-Datei.
Jetzt kommt beides aus der Quelle: **Kategorie** (was ein Angebot ist) und
**Preis** (was ThriveCart wirklich dafuer verlangt).

Der Unterschied, auf den es ankommt:

  Kategorie = was das Angebot IST      Minikurs, Signature-Kurs, Freebie …
  Rolle     = wo es EINGESETZT wird    als Bump, als Upsell, als Downsell

Die Content-Box ist ein Minikurs fuer 17 — und gleichzeitig der Order Bump an
drei Checkouts. Beides gehoert festgehalten, sonst steht dasselbe Produkt
dreimal in der Liste und niemand weiss, welcher Preis gilt.

🚨 **Ein Produkt kann je Einsatzort einen anderen Preis haben.** „Finde dein
Thema" kostet einzeln 39, als Bump mal 27 und mal 39, als Upsell 25. Das ist
kein Fehler, das ist die Mechanik — und genau deshalb muss es sichtbar sein.

Quellen:
  outputs/cockpit/abgleich/thrivecart.json   Produkte, Bumps, Upsells, Downsells
                                             mit Preisen (mit `--preise` geholt)
  context/freebies/                          die 0-Euro-Auslieferungen
  outputs/                                   Prompts und Tipps zum Weitergeben

Aufruf:
  python scripts/cockpit/katalog-bauen.py [zielordner]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# Die Schubladen
# --------------------------------------------------------------------------
KATEGORIEN = [
    ("freebie", "Freebie", "0 Franken — der Einstieg"),
    ("tipp", "Tipp zum Verschicken", "eine Seite, die du auf ein Kommentar-Stichwort schickst"),
    ("prompt", "Prompt / Vorlage", "etwas zum Mitnehmen und selbst Anwenden"),
    ("minikurs", "Mini-Kurs", "bis 49"),
    ("kurs", "Kurs", "50 bis 150"),
    ("signature", "Signature-Kurs", "151 bis 500"),
    ("programm", "Programm", "über 500"),
    ("sonstiges", "Sonstiges", "läuft nicht mehr oder gehört zur alten Ausrichtung"),
]

# Was zur alten Mama-Balance-Ausrichtung gehoert und nicht mehr beworben wird.
ALTBESTAND = re.compile(
    r"mama-zeit|grenzen setzen|familienorga|selbstbewusst als mama|"
    r"mama balance|meisterkurs|ordnung im familienchaos|mama-reset|"
    r"easy mumlife", re.I)

# Karteileichen — unbenannt oder Testzustand.
LEICHE = re.compile(r"untitled|^test$|\(copy", re.I)


def preis_von(eintrag):
    """Der erste echte Preis eines Eintrags."""
    for p in (eintrag.get("preise") or []):
        if p.get("betrag"):
            return round(float(p["betrag"]), 2), (p.get("waehrung") or "CHF")
    return None, "CHF"


def alle_preise(eintrag):
    """Alle Preisstufen — bei Ratenzahlung stehen dort mehrere."""
    return [(round(float(p["betrag"]), 2), p.get("waehrung") or "CHF")
            for p in (eintrag.get("preise") or []) if p.get("betrag")]


def kategorie_von(name, preis, status):
    if LEICHE.search(name or ""):
        return "sonstiges"
    if ALTBESTAND.search(name or ""):
        return "sonstiges"
    if status != "live":
        return "sonstiges"
    if preis is None or preis == 0:
        return "freebie"
    if preis <= 49:
        return "minikurs"
    if preis <= 150:
        return "kurs"
    if preis <= 500:
        return "signature"
    return "programm"


def schluessel(name):
    """Namen auf das Wesentliche eindampfen, damit Produkt und Bump derselben
    Sache zusammenfinden."""
    k = (name or "").lower()
    k = re.sub(r"\(.*?\)", " ", k)
    k = re.sub(r"[^a-zäöüß0-9 ]+", " ", k)
    k = re.sub(r"\b(der|die|das|dein|deine|für|fuer|als|in|minuten|mama|network|networking)\b", " ", k)
    return re.sub(r"\s+", " ", k).strip()[:26]


def slug_von(url):
    teile = [t for t in str(url or "").split("/") if t]
    return teile[-1].lower() if teile and "thrivecart" in str(url) else ""


def freebies_lesen():
    """Die 0-Euro-Auslieferungen aus dem Dateibestand."""
    raus = []
    ordner = ROOT / "context" / "freebies"
    if not ordner.exists():
        return raus
    for f in sorted(ordner.rglob("*.pdf")):
        name = f.stem.replace("-", " ").strip().title()
        raus.append({
            "id": "f-" + re.sub(r"[^a-z0-9]+", "-", f.stem.lower())[:28],
            "name": name,
            "kategorie": "freebie",
            "preis": 0, "waehrung": "CHF",
            "status": "live",
            "quelle": "Datei",
            "datei": f.relative_to(ROOT).as_posix(),
            "haengt_an": [], "kette": {"bumps": [], "upsells": [], "downsells": []},
        })
    return raus


# Prompts und Tipps liegen als fertige Dateien im Workspace und sind nirgends
# erfasst — genau die, die Patricia auf ein Stichwort verschicken kann.
ZUM_VERSCHICKEN = [
    ("outputs/freebies/KI-Strategie-Prompts-Patricia-Ulmann.pdf", "prompt",
     "KI-Strategie-Prompts"),
    ("outputs/produkte/customer-prompts/produkttreppe-skill-fuer-network-mamas.pdf",
     "prompt", "Produkttreppe-Skill für Network-Mamas"),
    ("outputs/produkte/claude-als-networkerin/downloads/claude-business-brain-anleitung.pdf",
     "prompt", "Business-Brain-Anleitung"),
    ("outputs/produkte/vom-networkwissen-zur-digitalen-produktwelt/downloads/claude-business-brain-anleitung-produktwelt.pdf",
     "prompt", "Business-Brain für die Produktwelt"),
    ("outputs/hook-bibliothek.pdf", "tipp", "Hook-Bibliothek"),
    ("outputs/content-ki-ablauf-fahrplan.pdf", "tipp", "Content-Fahrplan mit KI"),
    ("outputs/funnels/doterra-hormon-leadmagnet/4-erkenntnisse-hormonchaos.pdf",
     "tipp", "4 Erkenntnisse zum Hormonchaos"),
]


def zum_verschicken_lesen():
    raus = []
    for pfad, art, name in ZUM_VERSCHICKEN:
        p = ROOT / pfad
        if not p.exists():
            continue
        raus.append({
            "id": "v-" + re.sub(r"[^a-z0-9]+", "-", name.lower())[:28],
            "name": name,
            "kategorie": art,
            "preis": 0, "waehrung": "CHF",
            "status": "live",
            "quelle": "Datei",
            "datei": pfad,
            "haengt_an": [], "kette": {"bumps": [], "upsells": [], "downsells": []},
        })
    return raus


# --------------------------------------------------------------------------
# Schritt 5: Vorlagen, die Patricia weitergeben kann und die NUR in Drive
# liegen. Was es lokal auch als PDF gibt, steht schon in ZUM_VERSCHICKEN —
# zweimal dasselbe im Katalog hilft niemandem.
#
# 🚨 Hier stehen nur Vorlagen, die ihr nachweislich gehoeren: die
# Bonus-Vorlagen aus Mama-CEO Saeule 4 (im Workspace gebaut, in CLAUDE.md
# dokumentiert) und die Prompts aus ihrem eigenen Produktwelt-Kurs. Alles
# andere aus Drive ist ueber die Cockpit-Suche findbar, aber nicht als
# „weitergeben" ausgezeichnet — bei einem „Kopie von …"-Dokument weiss
# niemand mehr, aus wessen Kurs es stammt.
# --------------------------------------------------------------------------
DOC = "https://docs.google.com/document/d/%s/edit"
DRIVE_DATEI = "https://drive.google.com/file/d/%s/view"

DRIVE_VORLAGEN = [
    ("tipp", "Haushalts-Helfer-Vorlage", DOC % "1ER51llHy33luKbNw4QwGpXJz-SmN--WHdqQQ9N3PoRw"),
    ("tipp", "Notion-Haushaltsliste-Vorlage", DOC % "1sJSU6YIn1UoyZlyD3rTc2K4jqkBo366HDg1yrgN45XY"),
    ("tipp", "Cockpit-Bot-Vorlage", DOC % "1YBXq8nEpjEQSUob64kLmIv9g8-LkIWE2y7Uh0L88_7w"),
    ("tipp", "Kochassistent-Vorlage", DOC % "1KTC4yTw09rwZWFPOSazNaxtrusuHHaUtMYbkHMphDSo"),
    ("tipp", "Kochassistent-Vorlage (ausführlich)", DOC % "18dq-SjAjwXudfgmh9KU7siGufejpzXieonZ-qUg7Z-8"),
    ("prompt", "Business-Brief erarbeiten — Prompt", DOC % "1nPUh44WM5y8p1NkqypVfIYxyfZpo3GKdovMOtzF3JIU"),
    ("prompt", "Gratis-Chat One-Shot", DOC % "1MmutD69t6hcajTkCuoJvbVQgou4z7XmZdfOB2v8q-ns"),
    ("prompt", "Claude Code aktivieren — Anleitung", DOC % "1osqJy-mCN_AksIl4D9hQBGZgmGdEhknJGOsyiTFrSfs"),
    ("prompt", "Cowork einrichten — Anleitung", DOC % "1b3mHMYT47nO2HqhDFXvXIRxeSI4ED-unqbioRk1yJYE"),
    ("prompt", "Prompt 21: Salespage für mehrere Plattformen",
     DRIVE_DATEI % "18kx0U-bAJI9xu-C71OCL9Ay8b0kmGK6O"),
    ("prompt", "Prompt 22: Upsell, Bumps, Bundle, Downsell",
     DRIVE_DATEI % "1rjhksSvBuiH9UxFq172zzl7w0AugGw3z"),
]


def drive_vorlagen_lesen():
    raus = []
    for art, name, link in DRIVE_VORLAGEN:
        raus.append({
            "id": "g-" + re.sub(r"[^a-z0-9]+", "-", name.lower())[:28],
            "name": name,
            "kategorie": art,
            "preis": 0, "waehrung": "CHF",
            "status": "live",
            "quelle": "Google Drive",
            "link": link,
            "haengt_an": [], "kette": {"bumps": [], "upsells": [], "downsells": []},
        })
    return raus


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    tc_datei = ziel / "thrivecart.json"
    if not tc_datei.exists():
        sys.exit("thrivecart.json fehlt — erst thrivecart-holen.py --preise laufen lassen.")
    tc = json.loads(tc_datei.read_text(encoding="utf-8"))

    # 1) Die verkauften Angebote
    angebote, nach_schluessel = [], {}
    for x in tc.get("products", []):
        preis, waehrung = preis_von(x)
        eintrag = {
            "id": "p-" + str(x["id"]),
            "name": x["name"],
            "kategorie": kategorie_von(x["name"], preis, x.get("status")),
            "preis": preis, "waehrung": waehrung,
            "preisstufen": alle_preise(x),
            "status": x.get("status", ""),
            "quelle": "ThriveCart",
            "link": x.get("url", ""),
            "slug": x.get("slug") or slug_von(x.get("url")),
            "haengt_an": [],
            "kette": {"bumps": [], "upsells": [], "downsells": []},
        }
        angebote.append(eintrag)
        nach_schluessel.setdefault(schluessel(x["name"]), eintrag)

    # 2) Die Ketten: was haengt an welchem Checkout, und zu welchem Preis
    nach_slug = {a["slug"]: a for a in angebote if a["slug"]}

    for b in tc.get("bumps", []):
        preis, waehrung = preis_von(b)
        wo = nach_slug.get(slug_von(b.get("url")))
        if not wo:
            continue
        wo["kette"]["bumps"].append({"name": b["name"], "preis": preis,
                                     "waehrung": waehrung})
        quelle = nach_schluessel.get(schluessel(b["name"]))
        if quelle:
            quelle["haengt_an"].append({"art": "Order Bump", "bei": wo["name"],
                                        "preis": preis})

    for art, feld in (("upsells", "upsells"), ("downsells", "downsells")):
        preise = {schluessel(u["name"]): preis_von(u)[0] for u in tc.get(art, [])}
        for x in tc.get("products", []):
            wo = nach_slug.get(x.get("slug") or slug_von(x.get("url")))
            if not wo:
                continue
            for name in (x.get(feld) or []):
                preis = preise.get(schluessel(name))
                wo["kette"][feld].append({"name": name, "preis": preis,
                                          "waehrung": "CHF"})
                quelle = nach_schluessel.get(schluessel(name))
                if quelle:
                    quelle["haengt_an"].append({
                        "art": "Upsell" if feld == "upsells" else "Downsell",
                        "bei": wo["name"], "preis": preis})

    # 3) Freebies und was zum Verschicken bereitliegt
    angebote += freebies_lesen()
    angebote += zum_verschicken_lesen()
    angebote += drive_vorlagen_lesen()

    reihe = {k: i for i, (k, _, _) in enumerate(KATEGORIEN)}
    angebote.sort(key=lambda a: (reihe.get(a["kategorie"], 9), -(a["preis"] or 0)))

    heute = date.today().isoformat()
    (ziel / "katalog.json").write_text(json.dumps(
        {"angebote": angebote,
         "kategorien": [{"id": k, "name": n, "hinweis": h} for k, n, h in KATEGORIEN],
         "stand": heute}, ensure_ascii=False, indent=2), encoding="utf-8")

    from collections import Counter
    zaehler = Counter(a["kategorie"] for a in angebote)
    print("  %d Angebote im Katalog" % len(angebote))
    for k, n, _ in KATEGORIEN:
        if zaehler[k]:
            print("    %-22s %2d" % (n, zaehler[k]))
    mit_kette = sum(1 for a in angebote
                    if any(a["kette"][x] for x in ("bumps", "upsells", "downsells")))
    print("\n  %d Angebote mit Kette · %d werden woanders eingesetzt"
          % (mit_kette, sum(1 for a in angebote if a["haengt_an"])))
    print("\nAbgelegt in: %s" % (ziel / "katalog.json"))


if __name__ == "__main__":
    main()
