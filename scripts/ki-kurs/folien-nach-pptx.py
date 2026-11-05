# -*- coding: utf-8 -*-
"""Liest die HTML-Folien eines Moduls als Struktur aus — Inhalt plus Sprechnotiz.

    python scripts/ki-kurs/folien-modul-5.py <ordner>    # Folien bauen
    python scripts/ki-kurs/folien-nach-pptx.py <ordner>  # -> project/folien.json

Je Folie: Hintergrund hell oder dunkel, Augenbraue, Titel, Absaetze, Listen,
Karten — und die **Sprechnotiz**. Die HTML-Folie ist die Quelle, hier wird nur
gelesen, nie geschrieben.

**Wofuer das gut ist:** fuer alles, was Folie und Sprechnotiz zusammen braucht.
Gedacht war es als Zwischenschritt zu einer PowerPoint; Patricia nimmt am
04.11.2026 aber mit dem Deck-Artifact auf (*„das deckartefact passt auch"*).
Der naechste Verwender ist deshalb der **Regie-Zettel je Modul**, der im
Drehplan noch offen steht (`plans/2026-11-02-modul-5-aufnehmen.md`): sobald der
Bildschirm geteilt ist, sieht sie die Sprechnotizen nicht mehr — und sechs von
acht Lektionen in Modul 5 haben eine Bildschirm-Demo.

🚨 Hier wird nichts umformuliert. Was in der Folie steht, steht im JSON — sonst
laufen zwei Fassungen desselben Kurses auseinander.

🚨 Eine PowerPoint-Fassung gibt es bewusst **nicht**. Wer sie doch braucht:
`folien.json` traegt alles, was ein Generator braucht, und die Masterclass-PPTX
in `outputs/produkte/ki-treppe/masterclass/` zeigt den Aufbau (echter Text,
Sprechnotiz je Folie — keine Bilder).
"""

import html
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Die Markenfarben, wie sie in folien_basis.py stehen
BLAU, PETROL, CREME, ORANGE, TINTE = "#29556d", "#12828c", "#f1ecdd", "#dc822e", "#0c1c30"
HELL = "#f7f4ec"


def text_von(roh: str) -> str:
    """Markup heraus, Zeichen zurueck. <br> wird ein Zeilenumbruch."""
    t = re.sub(r"<br\s*/?>", "\n", roh)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


def fett_teile(roh: str):
    """Zerlegt in Stuecke mit Markierung, welche fett sind — <strong> und <b>."""
    teile, pos = [], 0
    for m in re.finditer(r"<(?:strong|b)\b[^>]*>(.*?)</(?:strong|b)>", roh, re.S):
        if m.start() > pos:
            vor = text_von(roh[pos:m.start()])
            if vor:
                teile.append({"text": vor, "fett": False})
        innen = text_von(m.group(1))
        if innen:
            teile.append({"text": innen, "fett": True})
        pos = m.end()
    rest = text_von(roh[pos:])
    if rest:
        teile.append({"text": rest, "fett": False})
    return teile or [{"text": text_von(roh), "fett": False}]


def ist_augenbraue(stil: str) -> bool:
    """Die kleine Zeile oben: gesperrt und in Grossbuchstaben."""
    return "letter-spacing" in stil and "uppercase" in stil


def farbe_aus(stil: str) -> str:
    m = re.search(r"(?<!background:)color:\s*(#[0-9a-fA-F]{6})", stil)
    return (m.group(1).lower() if m else "")


def groesse_aus(stil: str) -> int:
    m = re.search(r"font-size:\s*(\d+)px", stil)
    return int(m.group(1)) if m else 0


INTERESSANT = ("h1", "h2", "h3", "p", "ul", "ol", "div")


def oberste_ebene(inhalt: str):
    """Liefert (tag, attribute, innerer Inhalt) je Element der obersten Ebene.

    Zaehlt die Verschachtelungstiefe mit, damit ein <div> im <div> den
    aeusseren Block nicht vorzeitig beendet.
    """
    pos = 0
    while True:
        auf = re.compile(r"<(%s)\b([^>]*)>" % "|".join(INTERESSANT)).search(inhalt, pos)
        if not auf:
            return
        tag, attr = auf.group(1), auf.group(2)
        tiefe, i = 1, auf.end()
        gleiche = re.compile(r"<(/?)%s\b[^>]*>" % tag)
        while tiefe and i < len(inhalt):
            m = gleiche.search(inhalt, i)
            if not m:
                i = len(inhalt)
                break
            tiefe += -1 if m.group(1) else 1
            i = m.end()
        yield tag, attr, inhalt[auf.end():i - len("</%s>" % tag)] if tiefe == 0 else inhalt[auf.end():i]
        pos = i


def zaehle(roh: str) -> dict:
    """Wie viele sichtbare Elemente stehen in der Folie — fuer die Gegenprobe."""
    ohne = re.sub(r"<aside>.*?</aside>", "", roh, flags=re.S)
    z = {}
    for tag in ("h1", "h2", "h3", "li"):
        z[tag] = len(re.findall(r"<%s\b" % tag, ohne))
    # leere <p> zaehlen nicht mit, die traegt auch das JSON nicht
    z["p"] = sum(1 for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", ohne, re.S)
                 if text_von(m.group(1)))
    return z


def lies_folie(pfad: Path) -> dict:
    roh = pfad.read_text(encoding="utf-8")

    sid = re.search(r'id="([^"]+)"', roh).group(1)
    m = re.search(r"<aside>(.*?)</aside>", roh, re.S)
    notiz = text_von(m.group(1)) if m else ""
    koerper = re.sub(r"<aside>.*?</aside>", "", roh, flags=re.S)

    kopf = re.search(r"<section[^>]*>", koerper).group(0)
    hg = re.search(r"background:\s*(#[0-9a-fA-F]{6})", kopf)
    dunkel = (hg.group(1).lower() == BLAU) if hg else False

    inhalt = koerper[koerper.index(">", koerper.index("<section")) + 1:]
    inhalt = re.sub(r"</section>\s*$", "", inhalt)

    bloecke = []
    # 🚨 Nicht per Muster: `<div …>(.*?)</div>` endet beim ERSTEN schliessenden
    # Tag, also mitten in einer verschachtelten Karte. Beim ersten Lauf am
    # 04.11.2026 sind so 16 Zwischentitel und 24 Karten still verschwunden -
    # das JSON sah trotzdem vollstaendig aus. Darum zaehlt oberste_ebene() die
    # Tiefe mit, und unten prueft eine Gegenprobe die Vollstaendigkeit.
    for tag, attr, innen in oberste_ebene(inhalt):
        stil = (re.search(r'style="([^"]*)"', attr) or re.match("", "")).group(1) \
            if re.search(r'style="([^"]*)"', attr) else ""

        if tag in ("h1", "h2"):
            bloecke.append({"art": "titel", "text": text_von(innen),
                            "px": groesse_aus(stil)})
        elif tag == "h3":
            bloecke.append({"art": "zwischentitel", "text": text_von(innen)})
        elif tag == "p":
            if not text_von(innen):
                continue
            art = "augenbraue" if ist_augenbraue(stil) else "absatz"
            bloecke.append({"art": art, "teile": fett_teile(innen),
                            "px": groesse_aus(stil), "farbe": farbe_aus(stil)})
        elif tag in ("ul", "ol"):
            punkte = [fett_teile(li.group(1))
                      for li in re.finditer(r"<li\b[^>]*>(.*?)</li>", innen, re.S)]
            if punkte:
                bloecke.append({"art": "liste", "punkte": punkte,
                                "nummeriert": tag == "ol"})
        elif tag == "div":
            # Karten und Spalten: je Kind-div ein Kasten mit Titel und Zeilen.
            # Auch hier tiefenbewusst lesen, die Kaesten sind selbst verschachtelt.
            kaesten = []
            for ktag, _kattr, inneres in oberste_ebene(innen):
                if ktag != "div":
                    continue
                tt = re.search(r"<h3\b[^>]*>(.*?)</h3>", inneres, re.S)
                zeilen = [text_von(x.group(1)) for x in
                          re.finditer(r"<(?:p|li)\b[^>]*>(.*?)</(?:p|li)>", inneres, re.S)]
                zeilen = [z for z in zeilen if z]
                if tt or zeilen:
                    kaesten.append({"titel": text_von(tt.group(1)) if tt else "",
                                    "zeilen": zeilen})
            if kaesten:
                bloecke.append({"art": "karten", "kaesten": kaesten})
            else:
                # kein Kasten darin: alles, was Text traegt, der Reihe nach
                for itag, _ia, ii in oberste_ebene(innen):
                    txt = text_von(ii)
                    if not txt:
                        continue
                    if itag == "h3":
                        bloecke.append({"art": "zwischentitel", "text": txt})
                    elif itag in ("ul", "ol"):
                        punkte = [fett_teile(li.group(1)) for li in
                                  re.finditer(r"<li\b[^>]*>(.*?)</li>", ii, re.S)]
                        if punkte:
                            bloecke.append({"art": "liste", "punkte": punkte,
                                            "nummeriert": itag == "ol"})
                    else:
                        bloecke.append({"art": "absatz", "teile": fett_teile(ii),
                                        "px": 0, "farbe": ""})
                if not any(text_von(ii) for _t, _a, ii in oberste_ebene(innen)):
                    rest = text_von(innen)
                    if rest:
                        bloecke.append({"art": "absatz",
                                        "teile": [{"text": rest, "fett": False}],
                                        "px": 0, "farbe": ""})

    return {"id": sid, "dunkel": dunkel, "notiz": notiz, "bloecke": bloecke}


def main():
    if len(sys.argv) < 2:
        sys.exit("Aufruf: folien-nach-pptx.py <folien-ordner>")
    basis = Path(sys.argv[1])
    projekt = basis / "project" if (basis / "project").exists() else basis
    deck = json.loads((projekt / "deck.json").read_text(encoding="utf-8"))

    folien = []
    for sid in deck["order"]:
        p = projekt / "slides" / (sid + ".html")
        if not p.exists():
            print("  ⚠️ fehlt: %s" % p.name)
            continue
        folien.append(lies_folie(p))

    # --- Gegenproben, bevor etwas weitergegeben wird
    ohne_notiz = [f["id"] for f in folien if not f["notiz"]]
    assert not ohne_notiz, "Folien ohne Sprechnotiz: %s" % ohne_notiz
    leer = [f["id"] for f in folien if not f["bloecke"]]
    assert not leer, "Folien ohne Inhalt gelesen: %s" % leer
    assert len(folien) == len(deck["order"]), "Folienzahl weicht ab"

    # 🚨 Vollstaendigkeit: jede Ueberschrift, jeder Absatz, jeder Listenpunkt der
    # HTML-Folie muss im JSON wieder auftauchen. Ohne diese Probe hat der erste
    # Lauf 16 Zwischentitel verschluckt und trotzdem Erfolg gemeldet.
    fehlend = []
    for f in folien:
        soll = zaehle((projekt / "slides" / (f["id"] + ".html")).read_text(encoding="utf-8"))
        ist = {"h1": 0, "h2": 0, "h3": 0, "p": 0, "li": 0}
        for b in f["bloecke"]:
            if b["art"] == "titel":
                ist["h2"] += 1
            elif b["art"] == "zwischentitel":
                ist["h3"] += 1
            elif b["art"] in ("absatz", "augenbraue"):
                ist["p"] += 1
            elif b["art"] == "liste":
                ist["li"] += len(b["punkte"])
            elif b["art"] == "karten":
                for k in b["kaesten"]:
                    if k["titel"]:
                        ist["h3"] += 1
                    ist["p"] += len(k["zeilen"])
        titel_soll = soll["h1"] + soll["h2"]
        if ist["h2"] != titel_soll or ist["h3"] != soll["h3"]:
            fehlend.append("%s: Titel %d/%d, Zwischentitel %d/%d"
                           % (f["id"], ist["h2"], titel_soll, ist["h3"], soll["h3"]))
        # Absaetze und Listenpunkte stecken teils in Karten — zusammen pruefen
        if ist["p"] + ist["li"] < soll["p"] + soll["li"]:
            fehlend.append("%s: Text %d von %d gelesen"
                           % (f["id"], ist["p"] + ist["li"], soll["p"] + soll["li"]))
    assert not fehlend, "unvollstaendig gelesen:\n   " + "\n   ".join(fehlend)

    ziel = projekt / "folien.json"
    ziel.write_text(json.dumps(
        {"titel": deck["title"], "abschnitte": deck.get("sections", {}),
         "folien": folien}, ensure_ascii=False, indent=1), encoding="utf-8")

    arten = {}
    for f in folien:
        for b in f["bloecke"]:
            arten[b["art"]] = arten.get(b["art"], 0) + 1
    print("  %s" % deck["title"])
    print("  %d Folien, alle mit Sprechnotiz" % len(folien))
    print("  Bausteine: %s" % ", ".join("%s %d" % (k, v) for k, v in sorted(arten.items())))
    print("  -> %s" % ziel)


if __name__ == "__main__":
    main()
