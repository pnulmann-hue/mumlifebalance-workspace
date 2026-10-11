"""
Baut das Inhaltsverzeichnis von Patricias eigenen Kursen.

Ziel ist die Frage, die im Alltag wirklich vorkommt: „In welcher Lektion habe
ich das eigentlich erklaert?" — zum Beispiel, wenn eine Kundin fragt oder
Patricia im Content darauf verweisen will.

Das Skript liest die Kursordner, erkennt Modul und Lektion am Dateinamen und
zieht aus den Transkripten die Woerter, die **diese** Lektion ausmachen: haeufig
hier, selten in allen anderen. Das ist zuverlaessiger als eine Stichwortliste
von Hand, weil sie sich mit dem Material mitbewegt.

Erkannte Benennungen:
  01_Produkte,_die_immer_wieder_gekauft_werden.txt     Nummer + Titel
  12-lektion-3-1-brain-dump-struktur.txt               Nummer + Modul + Lektion
  Expertin statt Verkaeuferin - Modul 1.2.mp4          Modul + Lektion

Aufruf:
  python scripts/cockpit/kurse-indexieren.py [zielordner]
"""
import json
import math
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
KURSE = ROOT / "context" / "Kurse" / "aktuelle kurse"

# Woerter, die in jedem gesprochenen Text vorkommen und nichts unterscheiden.
STOPP = set("""
aber alle allem allen aller alles als also am an andere anderen auch auf aus
bei beim bin bis bist da dabei dadurch dafuer dann daran darauf darin das dass
dein deine deinem deinen deiner deines dem den denen denn der des dich die dies
diese diesem diesen dieser dieses dir doch dort du durch ein eine einem einen
einer eines einfach er es etwas euch euer fuer ganz gar gegen gehen geht gemacht
gibt gleich gut habe haben hast hat hatte hier hin ich ihm ihn ihnen ihr ihre
im immer in ins ist ja jede jeden jeder jetzt kann kannst kein keine koennen
koennt konnte machen macht mal man mehr mein meine mich mir mit muss musst
nach nicht nichts noch nun nur ob oder ohne paar schon sehr sein seine seid
selbst sich sie sind so soll sollte sondern ueber um und uns unsere unter viel
viele vielleicht vom von vor waere war waren was weg weil weiss weiter wenn
wer werden wie wieder wir wird wirklich wirst wo wollen wollte wurde zu zum
zur zwei zwischen
also gerade halt eben einfach quasi sozusagen wirklich echt voll total
okay ok super toll genau richtig klar logisch
thema themen punkt punkte sache sachen ding dinge
video lektion modul kurs teil folge
mama mamas frau frauen
euro franken chf
prozent
""".split())

# Diese Wortpaare lohnen sich als Ganzes — sie sind Patricias Fachbegriffe.
PAARE_MINDEST = 3


def woerter(text):
    text = text.lower()
    text = re.sub(r"[^a-zäöüß\s-]+", " ", text)
    return [w for w in text.split()
            if len(w) > 3 and w not in STOPP and not w.isdigit()]


# Wo die Modulnummer nicht im Dateinamen steckt, steht sie in der README des
# Kursordners. Belegt aus
# „context/Kurse/aktuelle kurse/Digitale Produktwelt/Transkripte/README.md" —
# dort ist jede der 24 Lektionen ihrer Modul-Nummer zugeordnet. Nicht raten:
# die Reihenfolge der Dateien ist NICHT die Reihenfolge im Kurs (Datei 01 ist
# Lektion 2.3, Datei 07 ist die Willkommens-Lektion 0.1).
# Links, die zu einem Kurs gehoeren - Mitmach-Heft, Tool, Kursplattform.
# Sie stehen hier und nicht nur im Artifact, weil ein Abgleich-Lauf das
# Dokument neu schreibt: was nur drueben steht, waere danach weg.
KURS_LINKS = {
    "Startklar": [
        {"titel": "Startklar-Werkstatt (Mitmach-Heft)", "url": "https://startklar.mumlifebalance.ch"},
        {"titel": "Bio-Check (in Lektion 1.3 verlinkt)", "url": "https://mumlifebalance.ch/bio-check/"},
    ],
}

MODULE = {
    "Digitale Produktwelt": {
        1: ("2", "3"), 2: ("2", "2"), 3: ("2", "1"),
        4: ("1", "1"), 5: ("1", "2"), 6: ("1", "3"),
        7: ("0", "1"),
        8: ("3", "1"), 9: ("3", "2"), 10: ("3", "3"),
        11: ("3", "4"), 12: ("3", "4"), 13: ("3", "5"),
        14: ("4", "1"), 15: ("4", "2"), 16: ("4", "3"), 17: ("4", "4"),
        18: ("5", "1"), 19: ("5", "2"), 20: ("5", "3"), 21: ("5", "4"),
        22: ("6", "1"), 23: ("6", "2"),
    },
}


def lektionen_finden(kurs):
    """Alle Lektionen eines Kurses, aus den Dateinamen erschlossen."""
    gefunden = {}
    for f in sorted(kurs.rglob("*")):
        if not f.is_file():
            continue
        # Ordner, die mit _ beginnen, sind Archiv — dort liegen alte Aufnahmen,
        # die durch neue ersetzt wurden. Kaemen sie mit, stuende jede Lektion
        # zweimal im Cockpit, und niemand wuesste, welche die gueltige ist.
        if any(t.startswith("_") for t in f.relative_to(kurs).parts[:-1]):
            continue
        name = f.name
        endung = f.suffix.lower()
        if endung not in (".txt", ".mp4", ".md", ".pdf"):
            continue

        modul, lektion, titel, nummer = "", "", "", 0

        # 12-lektion-3-1-brain-dump-struktur.txt
        m = re.match(r"^(\d{1,3})-lektion-(\d+)-(\d+)-(.+?)\.\w+$", name, re.I)
        if m:
            nummer, modul, lektion = int(m.group(1)), m.group(2), m.group(3)
            titel = m.group(4).replace("-", " ").replace("MASTERY", "").strip()
        else:
            # 01_Produkte,_die_immer_wieder_gekauft_werden.txt
            m = re.match(r"^(\d{1,3})[_-](.+?)\.\w+$", name)
            if m and endung in (".txt", ".md"):
                nummer = int(m.group(1))
                titel = m.group(2).replace("_", " ").replace("-", " ").strip()
            else:
                # … - Modul 1.2.mp4
                m = re.search(r"Modul\s+(\d+)\.(\d+)", name, re.I)
                if m:
                    modul, lektion = m.group(1), m.group(2)
                    nummer = int(modul) * 100 + int(lektion)
                    titel = re.sub(r"\s*-\s*Modul.*$", "", f.stem).strip()
                else:
                    continue

        if titel.lower().startswith("willkommen"):
            titel = titel[:40]

        schluessel = (modul, lektion, nummer, titel.lower()[:30])
        eintrag = gefunden.setdefault(schluessel, {
            "nummer": nummer, "modul": modul, "lektion": lektion,
            "titel": titel[:90], "text": "", "dateien": [],
        })
        eintrag["dateien"].append(f.relative_to(ROOT).as_posix())
        if endung in (".txt", ".md") and not eintrag["text"]:
            try:
                eintrag["text"] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

    return sorted(gefunden.values(), key=lambda x: (x["modul"] or "0", x["nummer"]))


def stichwoerter(alle):
    """Pro Lektion die Woerter, die gerade sie ausmachen.

    Haeufig in dieser Lektion, selten in allen anderen — sonst kaeme in jeder
    Lektion „Produkt" und „Kundin" heraus.
    """
    zaehler = [Counter(woerter(l["text"])) for l in alle]
    gesamt = Counter()
    for z in zaehler:
        gesamt.update(set(z))
    n = max(1, len(alle))

    for lek, z in zip(alle, zaehler):
        if not z:
            lek["stichwoerter"] = []
            continue
        punkte = {}
        for w, h in z.items():
            if h < 2:
                continue
            selten = math.log(n / (1 + gesamt[w]))
            punkte[w] = h * (selten + 0.35)
        lek["stichwoerter"] = [w for w, _ in
                               sorted(punkte.items(), key=lambda x: -x[1])[:12]]
        lek["laenge"] = len(lek["text"].split())
        del lek["text"]
    return alle


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    if not KURSE.exists():
        sys.exit("Kursordner fehlt: %s" % KURSE)

    kurse, register = [], {}
    for ordner in sorted(p for p in KURSE.iterdir() if p.is_dir()):
        lekt = stichwoerter(lektionen_finden(ordner))
        lekt = [l for l in lekt if l["titel"]]
        if not lekt:
            continue
        # Wo nur Videos liegen, wiederholt der Dateiname den Kursnamen. Dann
        # ist „Modul 1.2" ehrlicher als zwoelfmal derselbe Titel.
        zuordnung = MODULE.get(ordner.name, {})
        for l in lekt:
            if l["titel"].lower().strip() == ordner.name.lower().strip():
                l["titel"] = ("Modul %s.%s" % (l["modul"], l["lektion"])
                              if l["modul"] else "Lektion %d" % l["nummer"])
            # Modulnummer aus der Kurs-README nachtragen, wo der Dateiname
            # keine hergibt.
            if not l["modul"] and l["nummer"] in zuordnung:
                l["modul"], l["lektion"] = zuordnung[l["nummer"]]
            l["ohne_transkript"] = not l.get("stichwoerter")
        # Jetzt nach Modul und Lektion sortieren — die Dateinummer ist bei der
        # Produktwelt nicht die Kursreihenfolge.
        if zuordnung:
            lekt.sort(key=lambda l: (int(l["modul"] or 99),
                                     int(l["lektion"] or 99), l["nummer"]))

        eintrag = {
            "name": ordner.name,
            "lektionen": lekt,
            "ohne_transkript": sum(1 for l in lekt if l["ohne_transkript"]),
        }
        if ordner.name in KURS_LINKS:
            eintrag["links"] = KURS_LINKS[ordner.name]
        kurse.append(eintrag)
        for l in lekt:
            wohin = "%s · %s" % (ordner.name, l["titel"])
            # Der Titel ist das zuverlaessigste Stichwort — „Hybridmodell" wird
            # im Video kaum ausgesprochen, steht aber in der Ueberschrift.
            aus_titel = [w for w in woerter(l["titel"]) if w not in STOPP]
            for w in aus_titel:
                if w not in l["stichwoerter"]:
                    l["stichwoerter"].insert(0, w)
            for w in l["stichwoerter"]:
                register.setdefault(w, []).append(wohin)

    # Dateinamen sind mal mit, mal ohne Umlaut geschrieben
    # („huetchenmethode"). Beide Schreibweisen sollen finden.
    for w in list(register):
        andere = (w.replace("ue", "ü").replace("oe", "ö").replace("ae", "ä")
                  if any(x in w for x in ("ue", "oe", "ae"))
                  else w.replace("ü", "ue").replace("ö", "oe").replace("ä", "ae"))
        if andere != w and andere not in register:
            register[andere] = register[w]

    # Das Register: nur Woerter, die nicht in halb allen Lektionen stehen —
    # sonst landet man bei jeder Suche wieder im ganzen Kurs.
    schlank = {w: v for w, v in sorted(register.items()) if len(v) <= 8}

    (ziel / "kurse.json").write_text(json.dumps(
        {"kurse": kurse, "register": schlank, "stand": date.today().isoformat()},
        ensure_ascii=False, indent=2), encoding="utf-8")

    gesamt = sum(len(k["lektionen"]) for k in kurse)
    print("  %d Kurse · %d Lektionen · %d Stichwörter im Register"
          % (len(kurse), gesamt, len(schlank)))
    for k in kurse:
        print("    %-46s %2d Lektionen" % (k["name"][:46], len(k["lektionen"])))
    print("\nAbgelegt in: %s" % (ziel / "kurse.json"))


if __name__ == "__main__":
    main()
