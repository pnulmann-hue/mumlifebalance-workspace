"""
Stellt die Kurs-Unterlagen aus dem Workspace fuer Google Drive bereit.

Patricia hat ihre Sachen an vier Orten: Drive (was sie selbst erstellt hat),
diesen Workspace (was Claude gebaut hat), den Download-Ordner und OneDrive.
Dieses Skript holt den Workspace-Teil ans selbe Ufer wie den Rest.

🚨 **Hochladen kann Claude nicht** — der Drive-Connector nimmt Dateien nur als
eingebetteten Inhalt. Deshalb landet alles in
`Downloads/_fuer-drive/<Ordnername>/`, und Patricia zieht je Ordner einmal.

🚨 **Kopieren, nicht verschieben.** Im Workspace bleibt jede Datei liegen; sie
gehoert dort hin und wird von Skripten gelesen.

**Die Ablage folgt dem Kurs, nicht dem Dateisystem.** Im Workspace liegen die
Praesentationen der Saeule 1 lose im Ordner, die der Saeulen 2 bis 5 in
Unterordnern — gewachsen, nicht geplant. Hier bekommt jede Saeule ihren eigenen
Ordner, damit man in Drive findet, was man sucht.

Was bewusst wegbleibt:
  * `~$…`             Word- und PowerPoint-Sperrdateien
  * alte Fassungen    wo es eine `-NEU`-Version gibt, geht nur die mit
  * Dubletten         was schon in Drive liegt (Abgleich ueber drive-dateien.json)

Aufruf:
  python scripts/cockpit/praesentationen-bereitstellen.py [--kopieren]
"""
import json
import re
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ZIEL = Path.home() / "Downloads" / "_fuer-drive"
INVENTAR = ROOT / "outputs" / "cockpit" / "abgleich" / "drive-dateien.json"

# --------------------------------------------------------------------------
# Quelle -> Zielordner. Reihenfolge zaehlt, das erste Muster gewinnt.
# --------------------------------------------------------------------------
REGELN = [
    (re.compile(r"mama-ceo/03-praesentationen/saeule-(\d)/"),
     "Produkte · Mama-CEO/Säule %s"),
    (re.compile(r"mama-ceo/03-praesentationen/(?:saeule-1-)?\d*-?lektion-1-"),
     "Produkte · Mama-CEO/Säule 1"),
    (re.compile(r"mama-ceo/04-arbeitsblaetter/"),
     "Produkte · Mama-CEO/Arbeitsblätter"),
    (re.compile(r"mama-ceo/bonus-vorlagen-saeule-4/"),
     "Produkte · Mama-CEO/Bonus-Vorlagen Säule 4"),
    (re.compile(r"mama-ceo/0[68]-"),
     "Produkte · Mama-CEO/Webinar"),
    (re.compile(r"mba-launch/|mba/praesentationen/"),
     "Produkte · MBA"),
    (re.compile(r"instagram-startklar/"),
     "Produkte · Instagram-Startklar"),
    (re.compile(r"produkte/"),
     "Produkte · Weitere"),
]

ENDUNGEN = {".pptx", ".docx", ".pdf"}


def umschrift(text):
    """Umlaute umschreiben statt wegwerfen. Sonst wird aus „für" ein „fr" und
    der Abgleich erkennt „…-fuer-…" im Dateinamen nicht als dieselbe Sache."""
    return (text.lower().replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))


def schluessel(name):
    name = re.sub(r"\s*\(\d+\)", "", umschrift(name))
    return re.sub(r"[^a-z0-9]", "", name.rsplit(".", 1)[0])


def main():
    kopieren = "--kopieren" in sys.argv

    schon_in_drive = set()
    if INVENTAR.exists():
        daten = json.loads(INVENTAR.read_text(encoding="utf-8"))
        schon_in_drive = {re.sub(r"[^a-z0-9]", "", umschrift(x["t"]))
                          for x in daten["items"]}
        schon_in_drive = {t for t in schon_in_drive if len(t) > 8}

    quellen = []
    for basis in ("outputs/produkte", "outputs/freebies"):
        ordner = ROOT / basis
        if ordner.exists():
            quellen.extend(f for f in ordner.rglob("*")
                           if f.is_file() and f.suffix.lower() in ENDUNGEN)

    # „-NEU" schlaegt die alte Fassung.
    neuere = {f.name.lower().replace("-neu", "") for f in quellen
              if "-neu." in f.name.lower()}

    plan, uebersprungen = {}, []
    for f in sorted(quellen):
        pfad = f.relative_to(ROOT).as_posix()
        if f.name.startswith("~$"):
            continue
        if f.name.lower() in neuere:
            uebersprungen.append((f.name, "es gibt eine -NEU-Fassung"))
            continue
        k = schluessel(f.name)
        if any(k in t or t in k for t in schon_in_drive):
            uebersprungen.append((f.name, "liegt schon in Drive"))
            continue

        for muster, ziel in REGELN:
            m = muster.search(pfad)
            if m:
                ordner = ziel % m.groups() if m.groups() else ziel
                plan.setdefault(ordner, []).append(f)
                break

    # Saeule 1 liegt im Workspace doppelt: einmal mit und einmal ohne Praefix.
    for ordner, dateien in plan.items():
        gesehen, sauber = {}, []
        for f in dateien:
            kern = re.sub(r"^(?:saeule-\d-|\d+-)", "", f.name.lower())
            if kern in gesehen:
                uebersprungen.append((f.name, "gleiche Datei wie " + gesehen[kern]))
                continue
            gesehen[kern] = f.name
            sauber.append(f)
        plan[ordner] = sauber

    gesamt = sum(len(v) for v in plan.values())
    print("  %d Dateien bereitgestellt · %d übersprungen\n"
          % (gesamt, len(uebersprungen)))
    for ordner in sorted(plan):
        mb = sum(f.stat().st_size for f in plan[ordner]) / 1048576
        print("  %-42s %2d · %6.1f MB" % (ordner, len(plan[ordner]), mb))

    if uebersprungen:
        print("\n  Übersprungen:")
        for name, grund in uebersprungen:
            print("      %-52s %s" % (name[:52], grund))

    if not kopieren:
        print("\nBERICHT — nichts kopiert. Mit --kopieren ausführen.")
        return

    for ordner, dateien in plan.items():
        (ZIEL / ordner).mkdir(parents=True, exist_ok=True)
        for f in dateien:
            zieldatei = ZIEL / ordner / f.name
            if not zieldatei.exists():
                shutil.copy2(f, zieldatei)
    print("\nKopiert nach: %s" % ZIEL)
    print("Im Workspace bleibt alles liegen.")


if __name__ == "__main__":
    main()
