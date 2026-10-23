# -*- coding: utf-8 -*-
"""Traegt alles zusammen, was zum KI-Kurs gehoert — als eine JSON-Datei.

    python scripts/ki-kurs/produktion-daten.py

Ausgabe: outputs/produkte/ki-treppe/produktion.json

Quellen (alle im Workspace, nichts von Hand gepflegt):
  03-inhaltsverzeichnis.md   Kapitel und Lektionen mit den Dreh-Notizen
  04-kursplattform-texte.md  welche Beilage an welcher Lektion haengt
  05-praesentationen.md      die zehn Foliensaetze mit Link, Folien, Lektionen
  kopierseite-bauen.py       welche Lektionstexte in ThriveCart schon stehen
  beilagen/pdf/              welche Beilage es wirklich als PDF gibt

🚨 Der Status kommt aus den Quellen, nicht aus dem Gedaechtnis. Ein Haken, den
   ein Skript setzt, weil er plausibel aussieht, ist derselbe Fehler wie ein
   fehlender (siehe `aufgaben-abgleichen.py`, 24.09.2026). Hier gilt deshalb:
   - Lektionstext: steht in der Menge ERLEDIGT der Kopierseite
   - Beilage: die PDF-Datei liegt da oder nicht
   - Video: weiss das Skript NICHT. Das hakt Patricia selbst ab (`db`).
"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
KURS = ROOT / "outputs" / "produkte" / "ki-treppe"
BEILAGEN = KURS / "beilagen"


def lies(name):
    return (KURS / name).read_text(encoding="utf-8")


def kapitel_und_lektionen():
    t = lies("03-inhaltsverzeichnis.md").split("# Teil B")[1]
    kap = []
    for m in re.finditer(r"^## Kapitel (\d+) · (.+?)$(.*?)(?=^## Kapitel |\Z)",
                         t, re.M | re.S):
        nr, titel, block = m.group(1), m.group(2).strip(), m.group(3)
        lek = []
        # 🚨 Die Notiz-Spalte darf LEER sein. Mit " (.*?) \|$" (Leerzeichen vor
        #    dem Schlussstrich) fielen genau die sieben Lektionen
        #    „Zusammenfassung und Checkliste" heraus — also die, die niemand
        #    vermisst hätte, weil sie nichts Besonderes enthalten.
        for z in re.finditer(r"^\| (\d+\.\d+\w?) \| \*\*(.+?)\*\* \|(.*)\|\s*$",
                             block, re.M):
            notiz = z.group(3).strip()
            lek.append({"nr": z.group(1), "titel": z.group(2),
                        "notiz": notiz,
                        "zeigen": "Zeigen:" in notiz,
                        "neu": "Vorschlag" in notiz})
        kap.append({"nr": int(nr), "titel": titel, "lektionen": lek})
    return kap


def folien():
    """Die Tabelle aus 05-praesentationen.md: Modul, Folien, Lektionen, Link."""
    raus = {}
    for m in re.finditer(r"^\| (\d+) · (.+?) \| (\d+) \| (\d+) \| (https://\S+) \|$",
                         lies("05-praesentationen.md"), re.M):
        # 🚨 NICHT "lektionen" nennen — so heisst schon die Liste der Lektionen
        #    am Kapitel. Ein update() damit hat sie beim ersten Lauf durch eine
        #    Zahl ersetzt (dieselbe Falle wie daten/zahlen im Cockpit, 24.09.).
        raus[int(m.group(1))] = {"folien_titel": m.group(2).strip(),
                                 "folien": int(m.group(3)),
                                 "folien_lektionen": int(m.group(4)),
                                 "link": m.group(5)}
    if len(raus) != 10:
        sys.exit("🚨 Nur %d von 10 Foliensätzen in 05-praesentationen.md gelesen"
                 % len(raus))
    return raus


def begruessung():
    """Die erste Seite im Kursbereich — Überschrift und Text.

    🚨 Die stand bis zum 22.10.2026 nirgends in den Daten, obwohl sie der erste
       Text ist, den eine Käuferin im Kurs liest. Auf der Produktionsseite war
       deshalb alles zum Kopieren da ausser dem Anfang."""
    t = lies("04-kursplattform-texte.md")
    m = re.search(r"^## Begrüssung .+?$(.*?)(?=^## Modul )", t, re.M | re.S)
    if not m:
        sys.exit("🚨 Abschnitt „Begrüssung“ in 04-kursplattform-texte.md nicht gefunden")
    block = m.group(1)
    kopf = re.search(r"\*\*Überschrift:\*\*\s*(.+)", block)
    zeilen = [z[2:] if z.startswith("> ") else "" for z in block.splitlines()
              if z.startswith(">")]
    return {"titel": kopf.group(1).strip() if kopf else "",
            "text": absaetze(zeilen)}


def absaetze(zeilen):
    """Blockzitat-Zeilen zu Absätzen — eine Leerzeile trennt, sonst fliesst es.

    🚨 Zeile für Zeile zusammenkleben ergibt eine Wand; jede Zeile als eigenen
       Absatz nehmen zerreisst die Sätze mitten im Satz. Beides fällt erst beim
       Einfügen in ThriveCart auf, also nach dem Kopieren."""
    raus, lauf = [], []
    for z in zeilen:
        if z.strip():
            lauf.append(z.strip())
        elif lauf:
            raus.append(" ".join(lauf))
            lauf = []
    if lauf:
        raus.append(" ".join(lauf))
    return "\n\n".join(raus)


def kasse():
    """Die Textblöcke der ThriveCart-Kasse — je Block der Text zum Kopieren.

    Quelle ist `outputs/salespages/ki-kurs-checkout/textbloecke.md`: dort steht
    je Block eine Überschrift `## N · Was`, der Text als Blockzitat und darunter
    die Begründung. Zum Kopieren taugt nur das Zitat.

    🚨 Es gibt eine zweite Fassung (`ki-kurs-checkout-texte.md`, mit BLOCK-Kästen).
       Beide sind von Hand geschrieben, kein Generator. Gelesen wird die
       gegliederte — die andere bleibt als Herkunft liegen."""
    p = ROOT / "outputs" / "salespages" / "ki-kurs-checkout" / "textbloecke.md"
    t = p.read_text(encoding="utf-8")
    raus = []
    for m in re.finditer(r"^## (\d+) · (.+?)$(.*?)(?=^## |\Z)", t, re.M | re.S):
        block = m.group(3)
        zitat = absaetze([z[1:].strip() if z.startswith(">") else ""
                          for z in block.splitlines() if not z.startswith(">>")
                          and (z.startswith(">") or not z.strip())])
        # 🚨 Ein Hinweis geht über mehrere Zeilen. Nur die erste zu nehmen hat am
        #    22.10. den Satz „Nie wieder steht auf deiner Blackliste" mitten im
        #    Wort abgeschnitten — und ein halber Warnsatz warnt vor nichts.
        hinweise, rest, sammelt = [], [], None
        for z in block.splitlines():
            if z.startswith("🚨") or z.startswith("🔁"):
                sammelt = hinweise
            elif not z.strip():
                sammelt = None
            elif z.startswith(">") or z.strip() == "---":
                continue
            elif sammelt is None:
                sammelt = rest
            if sammelt is not None and z.strip():
                sammelt.append(z.strip())
        raus.append({"nr": int(m.group(1)), "was": m.group(2).strip(),
                     "text": zitat, "hinweis": " ".join(hinweise),
                     "notiz": " ".join(rest)})
    if len(raus) < 10:
        sys.exit("🚨 Nur %d Kassen-Blöcke gelesen — Quelle hat sich geändert" % len(raus))
    return raus


def texte_erledigt():
    """Die Menge ERLEDIGT aus der Kopierseite — die eine Wahrheit dazu."""
    t = (ROOT / "scripts" / "ki-treppe" / "kopierseite-bauen.py").read_text(encoding="utf-8")
    m = re.search(r"^ERLEDIGT = \{(.+?)\}", t, re.M | re.S)
    if not m:
        sys.exit("\U0001f6a8 ERLEDIGT in kopierseite-bauen.py nicht gefunden")
    return set(re.findall(r'"([\d.]+\w?)"', m.group(1)))


def beilagen_je_lektion():
    """Die Download-Tabelle aus 04-kursplattform-texte.md.
    Eine Zeile kann mehrere Lektionen nennen (die Modul-Checklisten)."""
    t = lies("04-kursplattform-texte.md")
    # 🚨 NICHT mit split("---") abschneiden: die Trennzeile der Markdown-Tabelle
    #    heisst |---|---| und enthält genau das. Der Block endete dadurch direkt
    #    nach der Kopfzeile, und die Zuordnung blieb still leer — in der Seite
    #    fehlten nur ein paar Chips, einen Fehler hat nie jemand gesehen.
    block = t.split("## \U0001f4ce Welche Downloads wo hingehören")[1]
    block = re.split(r"^---\s*$", block, maxsplit=1, flags=re.M)[0]
    raus = {}
    for m in re.finditer(r"^\| (.+?) \| (.+?) \|$", block, re.M):
        links, datei = m.group(1), m.group(2).strip()
        if links.startswith("---") or "Lektion" in links:
            continue
        for nr in re.findall(r"\d+\.\d+\w?", links):
            raus.setdefault(nr, []).append(datei)
    return raus


def plattform_texte():
    """Modultext und Lektionstext — das, was in ThriveCart unter dem Video steht.

    🚨 Die Quelle ist `04-kursplattform-texte.md`, nicht die Plattform. Was dort
       schon eingetragen ist, sagt die Menge ERLEDIGT der Kopierseite."""
    t = lies("04-kursplattform-texte.md")
    lek, mod = {}, {}
    for m in re.finditer(r"^## Modul (\d+) · (.+?)$(.*?)(?=^## |\Z)", t, re.M | re.S):
        nr, block = int(m.group(1)), m.group(3)
        mt = re.search(r"\*\*Modultext:\*\*\s*\n\n((?:> .*\n)+)", block)
        if mt:
            mod[nr] = " ".join(z[2:].strip() for z in mt.group(1).strip().splitlines())
        # Fassung A (seit 22.10.2026): je Lektion ein eigener Abschnitt
        #   ### 4.3 · Dein Arbeitsplatz
        #   **In dieser Lektion:** …
        # 🚨 Beim Aufwerten der Texte am 22.10. ist genau dieser Leser blind
        #    geworden: er kannte nur Fassung B und meldete danach ALLE 64
        #    Lektionen als „ohne Plattformtext". Die Zahl sah wie ein
        #    Arbeitsstand aus und war ein Lesefehler. Darum beide Fassungen.
        for z in re.finditer(r"^### (\d+\.\d+\w?) · (.+?)$(.*?)(?=^### |\Z)",
                             block, re.M | re.S):
            inhalt = z.group(3).strip()
            inhalt = re.split(r"^---\s*$", inhalt, maxsplit=1, flags=re.M)[0].strip()
            if inhalt:
                lek[z.group(1)] = inhalt

        # Fassung B (Altbestand): eine Tabellenzeile je Lektion
        for z in re.finditer(r"^\| \*\*(\d+\.\d+\w?) (.+?)\*\* \| (.+?) \|$", block, re.M):
            lek.setdefault(z.group(1), z.group(3).strip())
    return mod, lek


def videos():
    """Die Kursvideos bei Vimeo, je Lektion eines.

    Quelle ist `context/Kurse/aktuelle kurse/Easy-KI/videos-roh.json` — die
    Zuordnung Vimeo-Name → Lektion steht in `vimeo-transkripte.py` und ist dort
    am Schlusssatz jedes Videos belegt, nicht geraten.

    🚨 Der Hash im Link ist der Unlisted-Schlüssel: wer den Link hat, sieht den
       bezahlten Kurs ohne zu zahlen. Darum liegt die Quelle unter
       `context/Kurse/` (gitignored) und `produktion.json` ist seit dem
       22.10.2026 ebenfalls ausgeschlossen. **Nie in eine getrackte Datei.**"""
    quelle = (ROOT / "context" / "Kurse" / "aktuelle kurse" / "Easy-KI"
              / "videos-roh.json")
    if not quelle.exists():
        print("  ⚠ keine videos-roh.json — die Seite zeigt dann keine Videos")
        return {}
    # 🚨 `vimeo-transkripte.py` hat einen Bindestrich im Namen und lässt sich
    #    nicht importieren. Die Tabelle wird deshalb aus der Datei gelesen —
    #    eine zweite Kopie hier würde beim nächsten Video auseinanderlaufen.
    t = (pathlib.Path(__file__).resolve().parent / "vimeo-transkripte.py") \
        .read_text(encoding="utf-8")
    m = re.search(r"^LEKTION = \{(.+?)^\}", t, re.M | re.S)
    if not m:
        sys.exit("🚨 LEKTION in vimeo-transkripte.py nicht gefunden")
    zuordnung = dict(re.findall(r'"([^"]+)":\s*"([\d.]+\w?)"', m.group(1)))

    daten = json.loads(quelle.read_text(encoding="utf-8"))
    raus = {}
    for nummer, hash_, name, dauer in daten["videos"]:
        lek = zuordnung.get(name)
        if not lek:
            print("  ⚠ Video „%s“ hat keine Lektion — in LEKTION nachtragen" % name)
            continue
        raus[lek] = {
            "nummer": nummer,
            "dauer": "%d:%02d" % (dauer // 60, dauer % 60),
            "link": "https://vimeo.com/%s/%s" % (nummer, hash_),
            # Das ist, was in ThriveCart ins HTML-Feld kommt.
            "einbettung": ('<iframe src="https://player.vimeo.com/video/%s'
                           '?h=%s" width="640" height="360" frameborder="0" '
                           'allow="autoplay; fullscreen; picture-in-picture" '
                           'allowfullscreen></iframe>' % (nummer, hash_)),
        }
    return raus


# Beilagen, die es nur in Drive gibt (kein lokales Markdown, kein PDF).
# 🚨 Patricias eigene Blackliste, von ihr selbst gepflegt. Sie wird NICHT aus
#    `context/ki-phrasen-blackliste.md` abgeleitet: die Arbeitsfassung hier
#    nennt eine fremde Mentorin und interne Befehle, die Drive-Fassung nicht.
NUR_IN_DRIVE = [
    ("ki-blackliste", "Meine KI-Blackliste",
     "Google Doc · die gefüllte Liste aus Modul 2.2"),
]


# Welche Beilage als Google Doc ausgeliefert wird statt als PDF — und was auf
# der Seite dabeistehen soll.
#
# 🚨 Patricia am 22.10.2026: „es hat anhänge wo sie was reinschreiben sollten.
#    da können wir keine pdfs machen." Sie hat recht, und es betraf 17 von 21:
#    vier zum Ausfüllen, neun zum Abhaken, vier zum Kopieren. Ein PDF kann
#    beides nicht. Jedes Doc trägt oben „Datei → Kopie erstellen", damit das
#    Original stehen bleibt.
# 🚨 Die neun Modul-Checklisten sind EIN Dokument. Jede Modul-Lektion verlinkt
#    dasselbe — einmal kopieren, durch den ganzen Kurs abhaken. Die Quelle dazu
#    ist `checklisten-alle.md`; die neun Einzeldateien liegen in `_abgeloest/`.
# 🚨 Die Markdown-Dateien hier sind die INHALTS-Quelle, nicht das Ausgeliefeste.
#    Wer eine ändert, muss das Doc in Drive nachziehen — eine geänderte .md
#    ändert nichts an dem, was die Teilnehmerin öffnet.
ALS_DOC = {
    "business-brief-vorlage": "Google Doc · zum Ausfüllen",
    "claude-md-vorlage": "Google Doc · zum Ausfüllen",
    "floskel-liste-vorlage": "Google Doc · zum Ausfüllen",
    "skill-geruest": "Google Doc · zum Ausfüllen",
    "checklisten-alle": "Google Doc · zum Abhaken, alle 9 Module",
    "prompt-bibliothek": "Google Doc · zum Kopieren und Ausfüllen",
    "buch-technik-auftrag": "Google Doc · zum Kopieren",
    "cowork-erster-bot": "Google Doc · zum Kopieren",
    "cowork-projekt-kochassistent": "Google Doc · zum Kopieren",
}


def beilagen_dateien():
    """Was wirklich als PDF daliegt, mit Groesse."""
    raus = []
    for md in sorted(BEILAGEN.glob("*.md")):
        pdf = BEILAGEN / "pdf" / (md.stem + ".pdf")
        # Ein Doc hat kein PDF und soll trotzdem nicht als „fehlt" dastehen.
        istdoc = md.stem in ALS_DOC
        eintrag = {"name": md.stem,
                   "titel": titel_von(md),
                   "pdf": istdoc or pdf.exists(),
                   "link": ANHAENGE.get(md.stem, ""),
                   "kb": round(pdf.stat().st_size / 1024) if pdf.exists() else 0}
        if istdoc:
            eintrag["notiz"] = ALS_DOC[md.stem]
        raus.append(eintrag)
    for name, titel, notiz in NUR_IN_DRIVE:
        raus.append({"name": name, "titel": titel, "pdf": True,
                     "link": ANHAENGE.get(name, ""), "kb": 0, "notiz": notiz})
    return raus


# 🚨 Bei einer Vorlage zum Ausfüllen ist die erste Überschrift ein PLATZHALTER,
#    kein Titel. Das Skill-Gerüst stand in der Liste als „[Name des Skills]" —
#    im PDF ist das richtig (sie trägt ihn ein), in einer Übersicht liest es
#    sich wie ein Fehler. Darum hier der Name der Datei, nicht der im Text.
TITEL = {"skill-geruest": "Dein Skill-Gerüst — die Vorlage zum Ausfüllen"}


def titel_von(md):
    if md.stem in TITEL:
        return TITEL[md.stem]
    for z in md.read_text(encoding="utf-8").splitlines():
        if z.startswith("# ") and "[" not in z:
            return z[2:].strip()
    return md.stem


# Die Beilagen liegen in Google Drive, Ordner „KI-Kurs — Deine KI-Mitarbeiterin".
#
# 🚨 Vorher hingen sie als Artifact-Anhang, und das taugt für PDF nicht: der
#    Anhang-Speicher liefert sie als `text/plain` aus. Die Datei kommt an, der
#    Browser zeigt sie aber nicht — eine weisse Seite mit den rohen PDF-Bytes.
#    Davor zeigten die Adressen sogar ganz ins Leere, weil sie dem COCKPIT
#    gehörten statt dieser Seite. Patricia: „die beilagen sind nicht aufrufbar".
# 🚨 Drive nimmt nichts über den Browser an (weder Ablegen noch das Neu-Menü),
#    und die Schnittstelle will die Datei kodiert im Aufruf — 2,3 MB müssten
#    zweimal durch den Kontext. Darum lädt Patricia sie selbst hoch; bereit
#    liegen sie in `outputs/produkte/ki-treppe/beilagen/fuer-drive/`.
# 🚨 Die Kennungen stehen in `context/Kurse/aktuelle kurse/Easy-KI/
#    beilagen-drive.json` (gitignored). Heute geben sie nichts preis — Drive
#    verlangt eine Berechtigung. Sobald der Ordner aber auf „jeder mit dem
#    Link" steht, IST die Kennung der Zugang, und das Repo ist öffentlich.
def anhaenge_aus_drive():
    quelle = (ROOT / "context" / "Kurse" / "aktuelle kurse" / "Easy-KI"
              / "beilagen-drive.json")
    if not quelle.exists():
        print("  ⚠ keine beilagen-drive.json — die Seite zeigt keine Beilagen-Links")
        return {}, ""
    d = json.loads(quelle.read_text(encoding="utf-8"))
    # 🚨 Ein Google Doc hat eine andere Adresse als eine hochgeladene Datei.
    #    Mit `/file/d/<id>/view` antwortet Drive bei einem Doc mit einer
    #    Fehlerseite — sieht aus wie ein kaputter Link, ist der falsche Weg.
    docs = set(d.get("_google_docs", []))
    adr = {k: ("https://docs.google.com/document/d/%s/edit" % v if k in docs
               else "https://drive.google.com/file/d/%s/view" % v)
           for k, v in d["dateien"].items()}
    zip_link = ("https://drive.google.com/file/d/%s/view" % d["grundgeruest_zip"]
                if d.get("grundgeruest_zip") else "")
    return adr, zip_link


ANHAENGE, GRUNDGERUEST_LINK = anhaenge_aus_drive()
DRIVE_ORDNER = "https://drive.google.com/drive/folders/1FzEiDo-R-qi9KXuN4tYRqydd9SkpZQXq"

# Welcher Beilagen-Dateiname steckt hinter welchem Text der Download-Tabelle.
# Nur was eindeutig ist — geraten wird nichts.
ZUORDNUNG = [
    ("Roadmap", "roadmap-drei-stufen"), ("Begriffe", "begriffe-cheatsheet"),
    ("Checkliste je Modul", "checklisten-alle"),
    ("Floskel", "floskel-liste-vorlage"), ("Business-Brief", "business-brief-vorlage"),
    ("Buch-Technik", "buch-technik-auftrag"), ("Skill-Gerüst", "skill-geruest"),
    ("Sicherheits", "sicherheits-checkliste"), ("Prompt-Bibliothek", "prompt-bibliothek"),
    # 22.10.2026 dazu — diese drei lagen als PDF da und standen trotzdem als
    # „fehlt" auf der Seite, weil kein Stichwort passte.
    ("Setup-FAQ", "setup-faq"), ("CLAUDE.md`-Anleitung", "claude-md-vorlage"),
    # 22.10.2026: die gefuellte Liste aus Drive, nicht die leere Vorlage.
    ("KI-Blackliste", "ki-blackliste"),
    ("Cowork-Bot", "cowork-erster-bot"),
]


def anhang_zu(text, lektion):
    """Findet den Anhang zu einer Zeile der Download-Tabelle."""
    for stueck, name in ZUORDNUNG:
        if name and stueck.lower() in text.lower():
            return ANHAENGE.get(name)
    return None


# Was es sonst noch gibt — im Workspace, nicht im Netz. Pfade, weil Patricia
# mit Claude Code arbeitet und ein Pfad dort mehr wert ist als eine Beschreibung.
DOKUMENTE = [
    # 🚨 Das Grundgerüst steht als Erstes, weil es der einzige Download ist, der
    #    nicht als PDF an dieser Seite hängen kann — ein ZIP nimmt der
    #    Anhang-Speicher nicht. Es muss aus dem Download-Ordner an ThriveCart.
    ("Arbeitsplatz-Grundgerüst (ZIP für Lektion 4.3)",
     GRUNDGERUEST_LINK or "Downloads/Mein-Business-Grundgeruest.zip",
     "Fünf Ordner mit je einer Liesmich, CLAUDE.md, vier Befehle. "
     "Liegt in Drive. Neu bauen: python scripts/ki-kurs/grundgeruest-bauen.py --zip"),
    ("Inhaltsverzeichnis", "outputs/produkte/ki-treppe/03-inhaltsverzeichnis.md",
     "Alle Kapitel und Lektionen mit den Dreh-Notizen — die Quelle dieser Seite"),
    ("Lektionstexte für die Plattform", "outputs/produkte/ki-treppe/04-kursplattform-texte.md",
     "Begrüssung, zehn Modultexte, 63 Lektionen · Kopierseite mit Knopf je Feld"),
    ("Kurs-Konzept", "outputs/produkte/ki-treppe/02-kurs-konzept.md",
     "Maschine gegen Treibstoff — warum dieser Kurs die Skills leer ausliefert"),
    ("Preis-Validierung", "outputs/produkte/ki-treppe/06-preis-validierung.md",
     "Die Staffel 199 / 277 / 333 und warum"),
    ("Launch-Kalender", "outputs/produkte/ki-treppe/07-launch-kalender.md",
     "Phasen, Mails, Storys, Feed"),
    ("Funnel-Gerüst", "outputs/produkte/ki-treppe/09-funnel-geruest.md",
     "Stimm-Check → Masterclass → Kurs, mit allem Offenen"),
    ("Texte für den Checkout", "outputs/salespages/ki-kurs-checkout-texte.md",
     "Die 13 Blöcke · gebaut mit ki-kurs-checkout-bauen.py"),
    ("Willkommens-Mail", "outputs/produkte/ki-kurs/mails/mail-00-willkommen.html",
     "🚨 Muss in ActiveCampaign von Hand ersetzt werden"),
    ("Käufertypen in den Storys", "outputs/produkte/ki-treppe/11-kaeufertypen-in-den-storys.md",
     "Welcher Typ an welchem Launch-Tag vorkommt"),
    ("Der Content-Kreislauf", "outputs/produkte/ki-treppe/12-content-kreislauf-kursmaterial.md",
     "Kursfassung mit eigenen Prompts — gehört zu Lektion 7.0"),
]

# Links und Abläufe stehen hier, weil sie nirgends sonst maschinenlesbar sind.
# 🚨 Keine Zugangsdaten, keine Schlüssel — die Seite ist teilbar, auch wenn sie
#    privat bleiben soll.
LINKS = [
    ("Verkaufsseite", "https://mumlifebalance.ch/ki-kurs/", "WP-Seite 4286"),
    ("Kasse", "https://mumlifebalance.thrivecart.com/ki-network/", "ThriveCart-Produkt 52"),
    ("Kursbereich", "https://thrivecart.com/mumlifebalance/", "Projekt Online-Kurse, Kurs 232070"),
    ("Beilagen in Drive", DRIVE_ORDNER,
     "alle 21 PDFs plus das Grundgerüst-ZIP"),
    ("Masterclass", "https://mumlifebalance.ch/ki-masterclass/", "gelaufen am 8.10."),
    ("Stimm-Check (0€)", "https://stimm-check.vercel.app/", "Einstieg in den Funnel"),
]

# Der Freischaltplan steht wörtlich auf der Verkaufsseite (Block „Die Kapitel
# gehen nacheinander auf"). 🚨 Nicht aus dem Gedächtnis ändern — was hier steht,
# haben die Käuferinnen gelesen.
# 🚨 Die Seite widerspricht sich: der Zeitplan sagt „So 1. November: Kapitel 1
#    bis 3", die Kapitel-Liste darunter sagt bei Kapitel 1-3 „ab 2.11.".
#    Gilt der frühere Termin, bis Patricia entscheidet.
ETAPPEN = [
    ("So 1.11.2026", "2026-11-01", [1, 2, 3],
     "alles ohne Installation, damit der erste Gewinn sofort da ist"),
    ("Mo 9.11.2026", "2026-11-09", [4, 5],
     "dein Arbeitsplatz und deine festen Aufträge"),
    ("Mo 16.11.2026", "2026-11-16", [6, 7],
     "deine Helfer und Social Media"),
    ("Mo 23.11.2026", "2026-11-23", [8, 9],
     "Seiten, Mails, deine Übersicht und deine Plattform für die Kundschaft"),
    ("Mo 30.11.2026", "2026-11-30", [10],
     "und der Kurs ist komplett"),
]

TERMINE = [
    ("Fr 23.10.2026", "Kasse schliesst", "ab dann niemand mehr neu dazu"),
    ("So 1.11.2026", "Kursstart", "die ersten Kapitel liegen im Bereich"),
    ("Mi 18.11.2026", "Erster Live-Call", "Arbeitsplatz und erster fester Auftrag"),
    ("Do 10.12.2026", "Zweiter Live-Call", "alles, was bis dahin aufgetaucht ist"),
]

ABLAEUFE = [
    ("Folien eines Moduls neu bauen",
     ["python scripts/ki-kurs/folien-modul-N.py <ordner>",
      "python scripts/ki-kurs/folien-pruefen.py <ordner>   # muss SAUBER melden"],
     "Danach den Foliensatz neu veröffentlichen — der Link bleibt gleich."),
    ("Eine Beilage ändern",
     ["# Text in outputs/produkte/ki-treppe/beilagen/<name>.md ändern",
      "cd scripts/karussell-render",
      "cp ../ki-treppe/beilagen-bauen.mjs ./_t.mjs && node ./_t.mjs <name> ; rm -f ./_t.mjs"],
     "Das PDF landet in beilagen/pdf/. Danach in den Drive-Ordner ziehen."),
    ("Lektionstexte in ThriveCart eintragen",
     ["python scripts/ki-treppe/kopierseite-bauen.py",
      "# dann: preview_start ki-kurs-texte   ->  http://localhost:4387"],
     "Je Karte ein Knopf für Titel und einen für die Beschreibung. "
     "Was eingetragen ist, gehört in ERLEDIGT im Skript nachgeführt."),
    ("Verkaufsseite neu ausspielen",
     ["cd scripts/wordpress",
      "node --env-file=.env deploy-ki-kurs-lp.mjs"],
     "\U0001f501 Preisstufe steht als PHASE in scripts/salespage-design/ki-kurs-bauen.py."),
    ("Die Willkommens-Mail bauen",
     ["python scripts/ki-kurs/mails-bauen.py"],
     "\U0001f6a8 Der Text muss danach in ActiveCampaign von Hand ersetzt werden — "
     "eine Datei im Workspace ändert nichts an dem, was verschickt wird."),
]

# Was offen ist. 🚨 Nur was belegt ist — keine Vermutungen.
OFFEN = [
    ("Die Setup-FAQ aus Lektion 4.2", "fehlt",
     "Am 04.10. geplant, nie gebaut. 4.2 ist laut eigener Notiz die Lektion, "
     "an der die Leute aussteigen."),
    ("Lektion 2.3b — Umzug von ChatGPT", "zu entscheiden",
     "Prompt 3 der Bibliothek ist fertig, die Lektion noch nicht beschlossen."),
    ("Verkaufsseite: 1.11. oder 2.11.?", "widerspricht sich",
     "Der Zeitplan sagt „So 1. November: Kapitel 1 bis 3“, die Kapitel-Liste "
     "darunter sagt bei 1 bis 3 „ab 2.11.“. Die Käuferinnen haben beides gelesen."),
    ("MBA-Upsell am Checkout", "falscher Preis",
     "Steht auf 997 statt 720. Zusammen mit dem Kurs sollen es 997 sein."),
]


def main():
    kap = kapitel_und_lektionen()
    fol = folien()
    fertig = texte_erledigt()
    beil = beilagen_je_lektion()
    modultexte, lektionstexte = plattform_texte()
    vids = videos()

    for k in kap:
        k.update(fol.get(k["nr"], {"folien": 0, "folien_lektionen": 0,
                                   "folien_titel": "", "link": ""}))
        if k["folien_lektionen"] and k["folien_lektionen"] != len(k["lektionen"]):
            print("  ⚠ Kapitel %d: Foliensatz deckt %d Lektionen ab, "
                  "im Inhaltsverzeichnis stehen %d"
                  % (k["nr"], k["folien_lektionen"], len(k["lektionen"])))
        k["modultext"] = modultexte.get(k["nr"], "")
        for l in k["lektionen"]:
            l["text_drin"] = l["nr"] in fertig
            l["video"] = vids.get(l["nr"]) or None
            l["plattformtext"] = lektionstexte.get(l["nr"], "")
            l["beilagen"] = [{"was": b, "link": anhang_zu(b, l["nr"]) or ""}
                             for b in beil.get(l["nr"], [])]
            # 🚨 Julias Lektionen nennen unter jedem Video die Anhänge. Hier wird
            #    geprüft, ob Patricias Text die Beilage auch erwähnt — sonst
            #    verspricht die Lektion nichts und die Datei bleibt ungesehen.
            l["beilage_im_text"] = bool(l["beilagen"]) and any(
                w in l["plattformtext"].lower()
                for w in ("herunterlad", "vorlage", "checkliste", "cheatsheet",
                          "ausdruck", "bibliothek", "gerüst", "pdf", "liegt",
                          "bekommst", "mitgeben", "dabei", "kopieren"))

    fehlt_text = [l["nr"] for k in kap for l in k["lektionen"] if not l["plattformtext"]]
    ohne_hinweis = [l["nr"] for k in kap for l in k["lektionen"]
                    if l["beilagen"] and not l["beilage_im_text"]]
    if fehlt_text:
        print("  ⚠ ohne Plattformtext: %s" % ", ".join(fehlt_text))
    if ohne_hinweis:
        print("  ⚠ Beilage nicht im Lektionstext erwähnt: %s" % ", ".join(ohne_hinweis))

    for k in kap:
        k["etappe"] = ""
        k["frei_ab"] = ""
        for wann, iso, nummern, _ in ETAPPEN:
            if k["nr"] in nummern:
                k["etappe"] = wann
                k["frei_ab"] = iso
    ohne_etappe = [k["nr"] for k in kap if not k["etappe"]]
    if ohne_etappe:
        sys.exit("🚨 Kapitel ohne Freischalt-Termin: %s" % ohne_etappe)

    anz = sum(len(k["lektionen"]) for k in kap)
    daten = {
        "stand": "2026-10-19",
        "kurs": "Easy KI für Networkerinnen — vom Chat zur Mitarbeiterin",
        "preis": 333,
        "kapitel": kap,
        "begruessung": begruessung(),
        "kasse": kasse(),
        "praesentationen": [{"nr": n, "titel": f["folien_titel"],
                             "folien": f["folien"],
                             "lektionen": f["folien_lektionen"],
                             "link": f["link"]}
                            for n, f in sorted(fol.items())],
        "beilagen": beilagen_dateien(),
        "links": [{"was": a, "url": b, "notiz": c} for a, b, c in LINKS],
        "termine": [{"wann": a, "was": b, "notiz": c} for a, b, c in TERMINE],
        "etappen": [{"wann": a, "iso": b, "kapitel": c, "notiz": d}
                    for a, b, c, d in ETAPPEN],
        "ablaeufe": [{"was": a, "befehle": b, "notiz": c} for a, b, c in ABLAEUFE],
        "offen": [{"was": a, "stand": b, "warum": c} for a, b, c in OFFEN],
        "dokumente": [{"was": a, "pfad": b, "notiz": c} for a, b, c in DOKUMENTE],
        "zahlen": {"kapitel": len(kap), "lektionen": anz,
                   "texte_drin": sum(1 for k in kap for l in k["lektionen"] if l["text_drin"]),
                   # 🚨 Diese Zahl ist GEMESSEN — so viele Lektionen haben ein
                   #    Video bei Vimeo. Der Haken auf der Seite ist etwas
                   #    anderes: den setzt Patricia selbst, wenn sie fertig ist.
                   "videos": sum(1 for k in kap for l in k["lektionen"] if l["video"]),
                   "folien": sum(k["folien"] for k in kap),
                   "beilagen": len(beilagen_dateien())},
    }
    ziel = KURS / "produktion.json"
    ziel.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    z = daten["zahlen"]
    print("%s" % daten["kurs"])
    print("  %d Kapitel · %d Lektionen · %d Folien · %d Beilagen"
          % (z["kapitel"], z["lektionen"], z["folien"], z["beilagen"]))
    print("  Lektionstexte in ThriveCart: %d von %d" % (z["texte_drin"], z["lektionen"]))
    print("  Videos bei Vimeo: %d von %d" % (z["videos"], z["lektionen"]))
    ohne_video = [l["nr"] for k in kap for l in k["lektionen"]
                  if not l["video"] and k["nr"] <= 4]
    if ohne_video:
        print("  ⚠ Kapitel 1–4 ohne Video: %s" % ", ".join(ohne_video))
    ohne = [b["name"] for b in daten["beilagen"] if not b["pdf"]]
    if ohne:
        print("  ⚠ ohne PDF: %s" % ", ".join(ohne))
    print("-> %s" % ziel)


if __name__ == "__main__":
    main()
