"""
Raeumt den kompletten Download-Ordner auf — Ziel: die Wurzel ist leer.

Patricia: „ziel ist, dass der downloadordner nachher wieder leer ist und alles
am richtigen platz ist."

🚨 **Es wird nur verschoben, nie geloescht.** Alles bleibt auf der Platte, nur
in einer benannten Schublade. Was weg kann, landet in `_dubletten` und
`_programme` — das loescht Patricia selbst, nachdem sie hineingeschaut hat. Ein
Skript, das im Download-Ordner loescht, kann einen Fehlgriff nicht rueckgaengig
machen.

🚨 **`_zugangsdaten/` enthaelt Sitzungs-Cookies.** Das sind Login-Token: wer die
Datei hat, ist eingeloggt, ohne Passwort zu kennen. Die gehoeren geloescht und
nie in eine Cloud. Sie stammen aus `/nachbau`; das Werkzeug legt sie bei Bedarf
neu an.

🚨 **`_privat/` geht nie nach Drive.** Dort liegen Kontoauszuege,
Scheidungsunterlagen, eine Sorgerechtsverfuegung, VR-Protokolle und
Schulunterlagen. Die Muster sind bewusst weit gefasst — lieber eine
Geschaeftsdatei zu viel im Privat-Ordner als eine private Datei in der Cloud.

Die Reihenfolge der Regeln entscheidet: **erst privat, dann Zugangsdaten, dann
Geschaeft, dann Art der Datei.** Wer zuerst nach Endung sortiert, schiebt eine
Scheidungsurkunde nach `_dokumente`, weil sie halt eine PDF ist.

Aufruf:
  python scripts/cockpit/downloads-aufraeumen.py            Bericht
  python scripts/cockpit/downloads-aufraeumen.py --machen   verschieben
"""
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DOWNLOADS = Path.home() / "Downloads"
INVENTAR = ROOT / "outputs" / "cockpit" / "abgleich" / "drive-dateien.json"
REFERENCE = ROOT / "reference"

# --------------------------------------------------------------------------
# 1) Zugangsdaten — hoechste Prioritaet, das sind Anmeldungen
# --------------------------------------------------------------------------
ZUGANG = re.compile(r"cookies?\.txt$|_cookies|\.pem$|\.key$|credentials", re.I)

# --------------------------------------------------------------------------
# 2) Privat — bleibt lokal, nie in eine Cloud
# --------------------------------------------------------------------------
PRIVAT = [
    # 🚨 Daten anderer Menschen. Namen und Mailadressen von Kundinnen gehoeren
    # nie in eine geteilte Ablage — dieselbe Regel wie fuer den Code.
    # Eng gefasst: „kunden" allein faengt auch Instagram-KUNDENmaschine,
    # flyer_NEUKUNDEN und Kunden-PAKET. Gemeint sind nur echte Listen.
    ("Kundendaten", re.compile(
        r"^patricia-kunden|kundenliste|kontaktliste|teilnehmerliste|"
        r"adressliste|kunden[-_ ]?export|kunden\.(csv|json|xlsx)$", re.I)),
    ("Recht & Familie", re.compile(
        r"scheidung|sorgerecht|vollmacht|testament|ehevertrag|vaterschaft|"
        r"patientenverf", re.I)),
    ("Finanzen", re.compile(
        r"kontoausz|kredit|raiffeisen|earnings|rechnung|receipt|quittung|"
        r"mahnung|csr-\d|msr-\d|steuer|lohn|ac_invoice|abrechnung|salden|"
        r"tickets_\d|booking-details", re.I)),
    ("Versicherung", re.compile(r"versicher|axa|police|factsheet vp|newmf", re.I)),
    ("Wohnen & Bau", re.compile(
        r"kostenvoranschlag|klimatisierung|strichliste|elektrizitaet|"
        r"schlosserei|scheidweghalde|preisliste_|bkp_|schleuderraum|"
        r"gemeinde|e-dokument", re.I)),
    ("Schule & Kinder", re.compile(
        r"elternbrief|schulreise|infobrief|berufsmesse|sporttag|evaluation|"
        r"zeugnis|mettlen", re.I)),
    ("Vereinsarbeit", re.compile(r"\bvr\b|pendenzenliste|beschluss-|ewu ag|protokoll|aktennotiz", re.I)),
    ("Familie & Erinnerungen", re.compile(r"familienfilm|mobile upload|whatsapp", re.I)),
    ("Haushalt", re.compile(r"haushaltsliste|vorabend-\d|wochenplan_kw|wochenplan_aktuell", re.I)),
]

# --------------------------------------------------------------------------
# 3) Geschaeft — die Ordner heissen wie in Drive
# --------------------------------------------------------------------------
GESCHAEFT = [
    ("doTERRA/Darm-Programm", re.compile(
        r"feel\.gut|darm|histaminarm|blaehbauch|ballaststoff|huelsenfruechte|"
        r"leinsamen|flohsamen|kombucha|verstopfung|magen-guide|leber-und|"
        r"zuckeralternativ|zusatzstoffe|plant-points|antibiotika|"
        r"antientzuendlich|achtsames-essen|haut-guide|anti-stress|"
        r"mentales-training|glaubenssaetze-gedanken|ein-blick-in-die-toilette|"
        r"durchfall|filter-erklaerungen|immunsystem-booster|sibo", re.I)),
    ("doTERRA", re.compile(
        r"^aktionen|bogo|convention|doterra|flyer_neukunden|share-guide|"
        r"the good in you|living magazine|train-guide|mah-meh|product-guide|"
        r"essential-emotions|essential_kit|newsletterjuni", re.I)),
    ("Öl-Wissen", re.compile(
        r"oele_in_der|kochen_mit_oelen|aromatherapie|moringa|"
        r"immunsystem-und-dein-teller", re.I)),
    ("03 - Prompts & KI-Tools", re.compile(
        r"herr-tech|seedance|claudeals|karussellpostsmitclaude|chatgpt|"
        r"agent-lab-bot|notion_dashboard|system-prompt|ki_briefing|"
        r"claude code|meta ads", re.I)),
    ("04 - Angebote, Verkauf & Funnels", re.compile(
        r"funnel|checkout vorlagen|launch liebe|launch queen|leadgewinnung|"
        r"quiz vorlage reeltitelbilder|emails evergreen|produkte erstellen|"
        r"^90-storyideen|content-tresor|"
        r"easy mumlife academy|portfolio|checkliste oba", re.I)),
    ("02 - Content Erstellung & Strategie", re.compile(
        r"hook-bibliothek|hooks-kw|markenhandbuch|instagram_strategie|"
        r"marktrecherche|content plan|content recycling|brand_guide|"
        r"aufbau und cover|instagram profil|businesskalendar", re.I)),
    ("01 - Zielgruppe & Positionierung", re.compile(
        r"nische, positionierung|zielgruppe", re.I)),
    ("Produkte · Mama-CEO", re.compile(
        r"^lektion[_ ]|^lektion \d|mental load detox|mama-zeit|tagesplaner|"
        r"mumpreneur-mastermind|trello", re.I)),
    ("Fremd-Kursmaterial", re.compile(
        r"mindset und leadership|mindset und glaubens|team_call|"
        r"selbstbefreiung|gut-genug-statt-perfekt|onleihe", re.I)),
]

# --------------------------------------------------------------------------
# 4) Nach Art, wenn kein Muster greift
# --------------------------------------------------------------------------
NACH_ENDUNG = [
    ("_programme", {".exe", ".msi", ".msix", ".acsm", ".ini", ".ttf"}),
    ("_buecher", {".epub"}),
    ("_medien/Bilder", {".png", ".jpg", ".jpeg", ".webp", ".svg"}),
    ("_medien/Videos", {".mp4"}),
    ("_archive", {".zip"}),
    ("_mails", {".msg"}),
    ("_notizen", {".txt", ".md", ".json", ".csv", ".vtt", ".html", ".htm"}),
    ("_dokumente", {".pdf", ".docx", ".pptx", ".xlsx"}),
]

# Transkripte mit Nummern-Dateinamen — Rohmaterial, das niemand je wieder sucht.
TRANSKRIPT = re.compile(
    r"^\d{6,}_transcript_|_transcript_\d{8}|^[0-9a-f-]{36}_|"
    r"^GMT\d+.*transcript|^TRANSCR__|VIMEO_TRANSCRIPTS", re.I)
TESTDATEI = re.compile(r"^__TEST|^Unbenannt|^current-data|^shell-aliases|probe", re.I)

# Ganze Ordner, die beim Entpacken entstanden sind — Canva-Exporte,
# Notion-ExportBlocks, Schriftpakete. Die wandern als Ganzes.
ORDNER_ZIEL = "_entpackt"


def umschrift(text):
    """Umlaute umschreiben statt wegwerfen. Sonst wird aus „für" ein „fr" und
    der Abgleich erkennt „…-fuer-…" im Dateinamen nicht als dieselbe Sache."""
    return (text.lower().replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))


def schluessel(name):
    name = re.sub(r"\s*\(\d+\)", "", umschrift(name))
    return re.sub(r"[^a-z0-9]", "", name.rsplit(".", 1)[0])


def bekannte_dateien():
    """Was schon in Drive oder lokal in reference/ liegt."""
    bekannt = set()
    if INVENTAR.exists():
        daten = json.loads(INVENTAR.read_text(encoding="utf-8"))
        bekannt |= {re.sub(r"[^a-z0-9]", "", umschrift(x["t"]))
                    for x in daten["items"]}
    if REFERENCE.exists():
        for f in REFERENCE.rglob("*"):
            if f.is_file():
                bekannt.add(schluessel(f.name))
    return {b for b in bekannt if len(b) > 8}


def einordnen(f, bekannt):
    name = f.name

    if ZUGANG.search(name):
        return "_zugangsdaten", "Sitzungs-Cookie — löschen, nicht ablegen"
    for ordner, muster in PRIVAT:
        if muster.search(name):
            return "_privat/" + ordner, ""
    if TESTDATEI.search(name):
        return "_muell", "Test- oder Restdatei"
    if TRANSKRIPT.search(name):
        return "_notizen/Transkripte-roh", ""

    k = schluessel(name)
    if any(k in b or b in k for b in bekannt):
        return "_dubletten", "liegt schon in Drive oder in reference/"

    for ordner, muster in GESCHAEFT:
        if muster.search(name):
            return "_fuer-drive/" + ordner, ""

    endung = f.suffix.lower()
    for ordner, endungen in NACH_ENDUNG:
        if endung in endungen:
            return ordner, ""
    return "_rest", ""


def main():
    machen = "--machen" in sys.argv
    if not DOWNLOADS.exists():
        sys.exit("Nicht gefunden: %s" % DOWNLOADS)

    bekannt = bekannte_dateien()
    plan = defaultdict(list)
    gruende = {}

    for f in sorted(DOWNLOADS.iterdir()):
        # Die eigenen Schubladen nie wieder einsortieren.
        if f.name.startswith("_"):
            continue
        if f.is_dir():
            plan[ORDNER_ZIEL].append(f)
            gruende[ORDNER_ZIEL] = "entpackte Downloads und Exporte"
            continue
        ordner, grund = einordnen(f, bekannt)
        plan[ordner].append(f)
        if grund:
            gruende[ordner] = grund

    gesamt = sum(len(v) for v in plan.values())
    print("  %d Dateien in der Wurzel · %d Schubladen\n" % (gesamt, len(plan)))
    for ordner in sorted(plan):
        dateien = plan[ordner]
        mb = sum(f.stat().st_size for f in dateien) / 1048576
        hinweis = ("  ← " + gruende[ordner]) if ordner in gruende else ""
        print("  %-38s %3d · %8.1f MB%s" % (ordner, len(dateien), mb, hinweis))

    if "_zugangsdaten" in plan:
        print("\n  🚨 Zugangsdaten gefunden:")
        for f in plan["_zugangsdaten"]:
            print("      %s" % f.name)

    if not machen:
        print("\nBERICHT — nichts verschoben. Mit --machen ausführen.")
        return

    verschoben = 0
    for ordner, dateien in plan.items():
        zielordner = DOWNLOADS / ordner
        zielordner.mkdir(parents=True, exist_ok=True)
        for f in dateien:
            ziel = zielordner / f.name
            nr = 1
            while ziel.exists():
                ziel = zielordner / ("%s~%d%s" % (f.stem, nr, f.suffix))
                nr += 1
            shutil.move(str(f), str(ziel))
            verschoben += 1
    print("\n  %d Dateien verschoben. Die Wurzel ist leer." % verschoben)
    print("  Nichts gelöscht — was weg kann, liegt in _dubletten, _programme "
          "und _muell.")


if __name__ == "__main__":
    main()
