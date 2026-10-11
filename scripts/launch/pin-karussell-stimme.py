# -*- coding: utf-8 -*-
"""Baut das 0€-Karussell für den angepinnten Beitrag (Stimm-Check).

Anlass: Patricia am 08.10.2026 — *„kannst du mir das 0€ karussell machen für den
angepinnten beitrag?"* und *„copywriting skill, karussellvorschriften etc. bitte
berücksichtigen und auch, dass das branding passt. ich habe geschaut, dass alle 3
beiträge in einer linie stehen"*.

**Die Linie der drei Pins** (aus ihrem Screenshot): heller Creme-/Naturgrund, viel
Luft, dunkle Serifenschrift zentriert, **Orange als einziger Akzent** — Textbalken
bei „Hey, ich bin Patricia", 0€-Kreis und Knopf „KOSTENLOS SICHERN" bei „Von 0 auf
echt". Kein Petrol als Fläche.

🚨 **Folie 1 ist ein Angebots-Cover, kein Hook** — bewusste Abweichung vom
   Karussell-Skill (dort ist Folie 1 der Hook). Grund: alle drei bestehenden Pins
   tragen Produktname plus Unterzeile, kein Hook. Der Hook steht auf Folie 2.
   Von Patricia am 08.10. freigegeben („passt").

🚨 **Kein Petrol-Cover** — doppelt begründet: Lead-Post mit Keyword
   (`feedback_KRITISCH-petrol-cover-nicht-bei-leadposts`) und die Linie der Pins.

🚨 **Kein Kursname, kein Preis** — Feed bleibt programm-frei
   (`feedback_keine-programme-im-feed`). 0€ ist erlaubt.

Zahlen hinter den Entscheidungen (`outputs/marktrecherche/2026-10-04-hook-gesamtbericht.md`):
Angle Identität 1,16 · Stufe 1 = 1,20 · Frage in Zeile 1 = 1,22 · Form Bekenntnis
1,16 · Liste 0,45. Deshalb Bekenntnis + Identität statt Schmerz, und keine Liste.

Produktangaben wörtlich aus `scripts/stimm-check/public/index.html` geprüft:
sechs Angaben, eine eigene Textprobe, rund 15 Minuten, zurück kommen Stimm-Brief,
Stimm-Prompt und ein erster Text. „Ohne Anmeldung" steht bewusst nirgends — die
Mailadresse wird hinterlegt.

    python scripts/launch/pin-karussell-stimme.py --ziel <ordner> \\
        [--entwuerfe <entwuerfe.json>]
"""
import argparse
import json
import pathlib
import sys

ID = "pin-kar-m-stimme"

FOLIEN = [
    ("STIMM-CHECK",
     "Damit deine KI schreibt, wie du redest"),
    ("Ich hab meine eigenen Texte nicht mehr erkannt",
     "Die KI hat geschrieben, was ich wollte, und trotzdem hab ich jeden Satz "
     "umgebaut, bis er wieder nach mir klang."),
    ("Und am Montag fängst du wieder vorne an",
     "Du erklärst ihr nochmal, wer du bist und für wen du schreibst, "
     "und nächste Woche machst du es wieder."),
    ("Das liegt nicht an der KI",
     "Sie kennt Millionen Texte und klingt deshalb wie der Durchschnitt von "
     "allen. Dich kennt sie nicht, weil ihr das noch nie jemand aufgeschrieben "
     "hat."),
    ("Mehr Prompts helfen hier nicht",
     "Eine gespeicherte Liste weiss nichts über dich, über deine "
     "Sätze und über die Wörter, die bei dir nie vorkommen."),
    ("Was hilft, ist ein Stimm-Brief",
     "Einmal festgehalten, wie du klingst, worauf sie achten soll und was tabu "
     "ist. Danach liest sie das jedes Mal selbst, bevor sie für dich "
     "schreibt."),
    ("Dafür brauchst du keine Technik",
     "Sechs Angaben und ein Text, den du selbst geschrieben hast — eine "
     "alte Caption reicht. Daran erkennt sie deine Sprache besser als an jeder "
     "Selbstbeschreibung."),
    ("Was danach bei dir liegt",
     "Dein Stimm-Brief, dein Stimm-Prompt zum Kopieren und ein erster Text, den "
     "du so posten würdest. In rund 15 Minuten."),
    ("Kommentier STIMME",
     "Dann schick ich dir den Stimm-Check. Kostenlos, und du machst es am "
     "Handy."),
]

CAPTION = """Ich hab monatelang Texte von der KI schreiben lassen und sie danach komplett umgebaut, weil sie nach irgendwem klangen, nur nicht nach mir.

Geändert hat es sich, als ich aufgehört habe, Prompts zu sammeln. Ich hab einmal aufgeschrieben, wie ich klinge: welche Wörter ich benutze, wie lang meine Sätze sind und was bei mir nie vorkommt. Seitdem liest meine KI das jedes Mal selbst, bevor sie für mich schreibt.

Im Karussell steht, was in so einen Stimm-Brief gehört und warum eine alte Caption von dir dafür mehr wert ist als jede Selbstbeschreibung.

Und wenn du deinen in rund 15 Minuten fertig haben willst: Kommentier STIMME, dann schick ich dir den Stimm-Check. Du gibst sechs Angaben und einen eigenen Text ein und bekommst deinen Stimm-Brief, deinen Stimm-Prompt und einen ersten Text zurück.

STIMME ⬇️

Hi, ich bin Patricia, Mama von vier Kindern. 2023 habe ich mein Network im Hybridmodell aufgebaut. Bei mir lernst du, wie du mit deinem Thema auf Instagram sichtbar wirst, wie du digitale Produkte passend zum Network entwickelst und wie du das ganze Business in deinen Mama-Alltag packst.

#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #kifuermamas #mumpreneur"""

HINWEIS = (
    "ANGEPINNTER BEITRAG — kein Wochenplatz, deshalb ohne Datum. "
    "Nicht über Blotato einplanen, Patricia postet und pinnt selbst. "
    "Gestaltung in der Linie der drei bestehenden Pins: Creme-Grund, "
    "Philosopher dunkelblau, Orange als einziger Akzent, KEIN Petrol. "
    "Folie 1 ist das Angebots-Cover (0€ im orangen Kreis oben links, "
    "Mockup des Stimm-Briefs am Handy, Knopf „KOSTENLOS SICHERN“ wie "
    "beim Pin „Von 0 auf echt“) — der Hook steht auf Folie 2. "
    "Freigegeben von Patricia am 08.10.2026."
)


def cockpit():
    return {
        "name": "Pin · 0€ Stimm-Check",
        "profil": "mentoring",
        "datum": "",
        "typ": "edukativ",
        "funnel": "TOF",
        "handle": "@mumlifebalance_patricia_ulmann",
        "brand": "mlb_light",
        "slides": [
            {"layout": "hook" if i == 0 else ("cta" if i == len(FOLIEN) - 1
                                              else "text"),
             "headline": h, "body": b}
            for i, (h, b) in enumerate(FOLIEN)
        ],
        "caption": CAPTION,
        "hinweis": HINWEIS,
        "launch": "",
        "job": "Lead",
        "angle": "Identität",
        "blotato": {"status": "", "zeit": ""},
        "textfrei": False,
        "kommentar": "",
        "kommentarAntwort": "",
        "kommentarErledigt": "",
        "kommentarStand": "",
        "abgelehnt": False,
        "abgelehntStand": "",
        "updatedAt": "2026-10-08T19:30:00.000Z",
    }


def editor_eintrag():
    return {
        "art": "karussell",
        "format": "slide",
        "cta": "STIMME",
        "datum": "",
        "id": ID,
        # 📌 wie 📦 (Vorrat) und 📡 (Keyword-Karte) — in der Liste
        # „ohne Datum" liegen 17 Entwürfe nebeneinander.
        "name": "📌 Pin · 0€ Stimm-Check",
        # Der Editor zeigt `fotoText` als „Bildvorschlag" im Infokasten an —
        # dort gehoert der Gestaltungs-Hinweis hin, nicht in den Namen. Im
        # Auswahlfeld steht nur `art · name`, und ein langer Name macht
        # die Zeile unlesbar.
        "fotoText": "Folie 1 ist das Angebots-Cover — 0€ im orangen "
                    "Kreis, Knopf KOSTENLOS SICHERN, Creme-Grund, "
                    "Philosopher dunkelblau, kein Petrol",
        "profil": "mentoring",
        "folien": [{"text": h, "unter": b} for h, b in FOLIEN],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ziel", required=True)
    p.add_argument("--entwuerfe", help="entwuerfe.json des Bild-Editors")
    a = p.parse_args()
    z = pathlib.Path(a.ziel)
    (z / "karussells").mkdir(parents=True, exist_ok=True)

    doc = cockpit()
    # Gegenprobe: kein Preis, kein Kursname im Feed.
    text = " ".join([s["headline"] + " " + s["body"] for s in doc["slides"]]) \
        + " " + doc["caption"]
    for wort in ("277", "333", "199", "CHF", "Franken", "Easy KI", "KI-Kurs"):
        if wort in text:
            sys.exit("\U0001f6a8 „%s“ steht im Feed-Text — "
                     "Programme und Preise gehören in Story und Mail"
                     % wort)
    if len(doc["slides"]) > 10:
        sys.exit("\U0001f6a8 mehr als 10 Folien — Blotato nimmt das nicht")

    (z / "karussells" / (ID + ".json")).write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Cockpit-Entwurf: %s  (%d Folien)" % (ID, len(doc["slides"])))

    if a.entwuerfe:
        e = pathlib.Path(a.entwuerfe)
        d = json.loads(e.read_text(encoding="utf-8"))
        d = d.get("data", d)
        liste = [x for x in d["entwuerfe"] if x.get("id") != ID]
        liste.append(editor_eintrag())
        d["entwuerfe"] = liste
        d["stand"] = "2026-10-08"
        d["quelle"] = (d.get("quelle", "") +
                       " | 08.10.: Pin-Karussell 0€ Stimm-Check "
                       "ergänzt (Folie 1 = Cover, kein Petrol).")
        (z / "entwuerfe.json").write_text(
            json.dumps(d, ensure_ascii=False), encoding="utf-8")
        print("Bild-Editor: %d Entwürfe (vorher %d)"
              % (len(liste), len(liste) - 1))


if __name__ == "__main__":
    main()
