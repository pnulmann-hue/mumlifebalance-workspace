"""
Haengt die Arbeitsblaetter aus Google Drive an die passende Lektion.

Patricia: „ich habe alle Arbeitsblätter aller Kurse in google drive abgelegt …
es würde sicher sinn machen, wenn du dann die verlinkung zum dokument hast in
der entsprechenden lektion."

🚨 **Die Modul- und Lektionsstruktur kommt NICHT aus ThriveCart.** Die
ThriveCart-Schnittstelle kennt Produkte, Bumps, Upsells und Transaktionen — aber
keine Kurse, Module oder Lektionen. Es gibt dort keinen Weg, der das hergibt.
Die Struktur stammt aus `kurse-indexieren.py`, und die Modulnummern der
Produktwelt stehen in der README des Kursordners (Tabelle `MODULE` dort).

Zwei Wege der Zuordnung:

  Mama-CEO      Saeule N  ->  alle Lektionen mit modul = N
                Das Arbeitsblatt gehoert zur ganzen Saeule, nicht zu einer
                einzelnen Lektion.

  Produktwelt   Lektion M.L  ->  die Lektion mit modul = M und lektion = L
                Lektion 3.4 gibt es zweimal (Theorie und Live-Demo), das
                Arbeitsblatt haengt an beiden. Das ist richtig so.

🚨 **Nichts raten.** Die Dateinummer ist NICHT die Kursreihenfolge — Datei 01
ist Lektion 2.3, Datei 07 ist die Willkommens-Lektion 0.1. Wer nach
Dateinummer zuordnet, haengt jedes zweite Arbeitsblatt falsch. Findet sich
keine Lektion, steht das Arbeitsblatt beim Kurs statt bei der Lektion.

Aufruf:
  python scripts/cockpit/arbeitsblaetter-verknuepfen.py [zielordner]
"""
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DOC = "https://docs.google.com/document/d/%s/edit"
DATEI = "https://drive.google.com/file/d/%s/view"

# --------------------------------------------------------------------------
# Die Arbeitsblaetter. (kurs, modul, lektion|None, titel, link)
# lektion = None heisst: gilt fuer das ganze Modul.
# --------------------------------------------------------------------------
PRODUKTWELT = [
    ("0", "1", "Mein Warum", DATEI % "1K0AKBkVXOhkvzp5dONYUOs58KHyVC578"),
    ("1", "1", "", DATEI % "14llmNEHz9PLlCxjgmIJfWLFkktRqfbsS"),
    ("1", "2", "", DATEI % "18s6FmeciyocSVQQnCsyfdZYjZjC-1WPB"),
    ("1", "3", "", DATEI % "1BAtisrpViLfI1PU2VwdjHM7f1b6doNXM"),
    ("2", "1", "", DATEI % "1CiLYfKEtmebHHfhhpmp2PyIsy5HPqE6V"),
    ("2", "2", "", DATEI % "1JFsm6JsgLYZ2k7bYIilsLW5yq7IbknZY"),
    ("2", "3", "", DATEI % "1pKDvDIbOPlEqoKiIWQwMUWTHTF-jdCFo"),
    ("3", "1", "", DATEI % "1jj2RF49M5UZDP3XN9fHg_LtofzamR4f1"),
    ("3", "2", "", DOC % "1BIpDzNPe-AEEsSNLsaNhx0WJuYM7wl8CLI-9C6Hv_F8"),
    ("3", "3", "", DOC % "19qeP1PaRLh8kdC_S96ARcgktgFiPbK_MxOBskhhcMJk"),
    ("3", "4", "", DOC % "1VLvOfd4hW3iAdwIakc-kFu3_MuXsJ9OqIVJvCVJAEoo"),
    ("3", "5", "", DOC % "16AeNBv1eLkBugPq_iOmEj7iOLpO6cHAHA_RKBuIGY4w"),
    ("4", "1", "", DOC % "1Xf3tu5mSmRDWGorYpDFPdRAC2UgaSwu1CqCP4mjwBiw"),
    ("4", "2", "", DOC % "1mV2TrEGiwjLf_G1jFxOjwwoFEMdavo50pgv76MvNGn4"),
    ("4", "3", "", DOC % "1H0AbMbOPVRBiIyhOQe1-HK_mJAUWyEMLlRjheifvA_w"),
    ("4", "4", "", DOC % "183X987SUhik0zKdohZ4Gi5qlnD_wLikiMUDH3S5tqUs"),
    ("5", "1", "", DOC % "13gJMYYZpX4PsPzz8wJCzcGxBI-LyKYjp4zEOBHqAej8"),
    ("5", "2", "", DOC % "1Wgla_kpTwjpX7yLqhfqX_kF01a7TUB-2BA3NlXNpri8"),
    ("5", "3", "", DOC % "1xzdnoPO4eafrk6n5rugjsnrlet72WGasLkrKJRORWJA"),
    ("5", "4", "", DOC % "18hC-zR0s4HNYBxlF_vM7GkBLoRuBA6b9RVIT1pIHAFY"),
    ("6", "1", "", DOC % "1RKy7-3M-RthIdgS5z548er3-0Av8hQblsH-sIXoY49U"),
    ("6", "2", "", DOC % "1g-so9kECckZjbD6PAy1zWch1DHfMVg0CqKdYkLxanxk"),
]

MAMA_CEO = [
    ("1", None, "Säule 1", DATEI % "1fjDR8QRrGpGZdW-r5Daice4k209GeYFW"),
    ("2", None, "Säule 2", DATEI % "1z8kEQeqffBLuHOS8L_AgH1SyL6cqZsex"),
    ("3", None, "Säule 3", DATEI % "1c8GXeI6GOR2L1FvUZ5M5YDATwrbkCioD"),
    ("4", None, "Säule 4", DATEI % "1e3VvD2VSQRSoT2z5QhaSbT9AsJgKvboq"),
    ("5", None, "Säule 5", DATEI % "12xWSSYQ0sHQI0gvZDhp6QxaNh6VdRjr9"),
]

# Kursname im Index -> Liste der Arbeitsblaetter
ZUORDNUNG = {
    "Digitale Produktwelt": PRODUKTWELT,
    "Mama-CEO": MAMA_CEO,
}

# „… Lekt 3.1 3.3" oder „… Lekt 3.2" im Lektionstitel
LEKT = re.compile(r"\bLekt\.?\s+((?:\d+\.\d+\s*)+)", re.I)


def nummern_im_titel(titel):
    """Alle „M.L"-Angaben, die im Lektionstitel stehen."""
    m = LEKT.search(titel or "")
    if not m:
        return []
    return [tuple(x.split(".")) for x in m.group(1).split()]


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    datei = ziel / "kurse.json"
    if not datei.exists():
        sys.exit("kurse.json fehlt — erst kurse-indexieren.py laufen lassen.")
    daten = json.loads(datei.read_text(encoding="utf-8"))

    gesetzt, offen = 0, []

    for kurs in daten.get("kurse", []):
        blaetter = ZUORDNUNG.get(kurs["name"])
        if not blaetter:
            continue
        untergebracht = set()

        for modul, lektion, zusatz, link in blaetter:
            treffer = []
            for l in kurs["lektionen"]:
                # Weg 1: das Inhaltsverzeichnis kennt Modul und Lektion
                if str(l.get("modul") or "") == modul:
                    if lektion is None or str(l.get("lektion") or "") == lektion:
                        treffer.append(l)
                        continue
                # Weg 2: die Nummer steht im Titel („… Lekt 3.2")
                if lektion is not None and \
                        (modul, lektion) in nummern_im_titel(l.get("titel")):
                    treffer.append(l)

            name = "Arbeitsblatt " + (
                zusatz if lektion is None
                else ("%s.%s" % (modul, lektion) + (" — " + zusatz if zusatz else "")))

            if not treffer:
                offen.append((kurs["name"], name, link))
                continue
            for l in treffer:
                l.setdefault("arbeitsblaetter", [])
                if not any(a["link"] == link for a in l["arbeitsblaetter"]):
                    l["arbeitsblaetter"].append({"name": name, "link": link})
                    gesetzt += 1
            untergebracht.add(link)

        # Was sich nicht sauber zuordnen liess, haengt am Kurs statt an der
        # Lektion. Lieber sichtbar an der falschen Ebene als unsichtbar.
        rest = [(n, l) for k, n, l in offen if k == kurs["name"]]
        if rest:
            kurs["arbeitsblaetter_ohne_lektion"] = [
                {"name": n, "link": l} for n, l in rest]

    datei.write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")

    print("  %d Arbeitsblätter an eine Lektion gehängt" % gesetzt)
    if offen:
        print("  %d ohne eindeutige Lektion — stehen jetzt beim Kurs:" % len(offen))
        for kursname, name, _ in offen:
            print("      %-24s %s" % (kursname, name))
    print("\nAktualisiert: %s" % datei)


if __name__ == "__main__":
    main()
