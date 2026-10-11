"""
Fuellt die beiden neuen Cockpit-Bereiche mit echtem Inhalt.

  produkt-details.json   Was in den Kursen drinsteckt — aus
                         `context/patricia-expertise.md` zusammengezogen.
  ideenkasten.json       Die offenen Punkte, die bisher in Chats und READMEs
                         verstreut lagen.

Das laeuft **einmal** zum Befuellen. Danach gehoeren beide Bereiche Patricia;
der taegliche Abgleich fasst sie nicht an. Ein zweiter Lauf wuerde ihre
Aenderungen ueberschreiben — deshalb weigert sich das Skript, wenn die Dateien
schon da sind (ausser mit `--ueberschreiben`).

Aufruf:
  python scripts/cockpit/startinhalt-bauen.py [zielordner] [--ueberschreiben]
"""
import json
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# Was in den Angeboten drinsteckt
# --------------------------------------------------------------------------
DETAILS = {
    "a-digitale-produktwelt": {
        "inhalt":
            "7 Lektionen. Kern-Versprechen: ein Einkommen, das nicht jeden "
            "Monat bei null anfängt.\n"
            "• Hybridmodell — Network-Provisionen und eigene Kurse verstärken "
            "sich gegenseitig\n"
            "• Produkttreppe — 0€ → Minikurs → Signature-Kurs → Membership/1:1\n"
            "• Evergreen-Automationen — Mail-Funnel, die ohne tägliches "
            "Nachschieben laufen\n"
            "• Dringlichkeit, die stimmt — Secret Offer, Early Bird, nur wenn wahr\n"
            "• Transformation statt Produkt\n\n"
            "Kernsatz: Network-Abhängigkeit von Upline, Teamboni und Firma "
            "durch eigene digitale Assets brechen.",
    },
    "a-finde-dein-thema-als-network": {
        "inhalt":
            "60-Minuten-Kurs. Ergebnis: der eigene Experten-Satz.\n"
            "• Formel: „Ich helfe [Zielgruppe] dabei [Problem], damit [Gefühl].“\n"
            "• Themenlandkarte mit 5 Feldern statt einengender Nische — Alltag · "
            "Körperwohlbefinden · Mindset · Sichtbarkeit · Mama- und Businessleben\n"
            "• Die 4 Quellen der Expertise: Erfahrung · Ergebnisse · Perspektive · "
            "Fragen von früher",
    },
    "a-instagram-kundenmaschine": {
        "inhalt":
            "Kern-Versprechen: Instagram ist kein Stressfaktor, wenn du Struktur hast.\n"
            "• Schaufenster-Strategie — Bio, Highlights und 3 gepinnte Beiträge "
            "zeigen sofort, wofür du stehst\n"
            "• Content-Säulen-System — jede Säule beantwortet EINE Frage\n"
            "• Keyword-/Kommentar-System als Lead-Weg\n"
            "• Content-Recycling und Mail-Funnel-Anschluss\n\n"
            "Abgrenzung: Content-Strategie und Akquise gehören hierher, nicht in Mama-CEO.",
    },
    "a-vom-network-wissen-zum-eigen": {
        "inhalt":
            "Minikurs, 39 CHF. Aus Network-Wissen wird ein verkaufbares Produkt.\n"
            "• Transformation statt Format — nicht „5 Videos + 2 PDFs“, sondern "
            "der Weg von A nach Z\n"
            "• Mini (A→C, ein Problem) gegen Signature (A→Z, Komplettlösung)\n"
            "• MVP-Prinzip: fertig schlägt perfekt, Updates nach Kundenfeedback\n"
            "• Kürzer ist besser — die 10-Minuten-Lösung schlägt das "
            "3-Stunden-Herumschrauben\n"
            "• Jede Lektion braucht Mehrwert und ein Ergebnis",
    },
    "a-mama-ceo": {
        "inhalt":
            "8-Wochen-Programm, 5 Säulen. Mama-CEO heisst nicht mehr arbeiten, "
            "sondern anders — von der Macherin zur Entscheiderin.\n\n"
            "Säule 1 · Du erschaffst dir die Zeit (L1.1–1.5)\n"
            "3 Business-Säulen · 5 CEO-Aufgaben · Power-Slots und Erschöpfungs-Wand · "
            "Wochenrhythmus mit 4 Rollen und 3 Zonen · CEO-Tag-Fokus\n\n"
            "Säule 2 · Du brichst aus dem Hamsterrad aus (L2.1–2.6)\n"
            "Hütchenmethode (Rollen auf max. 7 reduzieren) · 4-Filter Behalten/"
            "Delegieren/Automatisieren/Weg · Sonntag-Reset · Familienorga\n\n"
            "Säule 3 · Du baust die Struktur (L3.1–3.6)\n"
            "Jahr → Monat → Woche → Tag · Notion als Business-Brain · Monats-Trio "
            "(1 Gratis + 1 Mini + 1 gross) · 50%-Plan für Kranktage\n\n"
            "Säule 4 · Deine KI-Mitarbeiter (L4.1–4.6)\n"
            "KI als Praktikantin · 3-Stufen-Modell (nur Notion / Cowork / Claude "
            "Code) · Business-Brief mit 6 Bausteinen · Cockpit-Bot · "
            "Haushalts-Helfer-Bot\n\n"
            "Säule 5 · Skalieren mit der Mama-CEO-Matrix (L5.1–5.4)\n"
            "4 Felder: ich / KI / System / raus · 25 Tasks sortieren · innerer "
            "Kreis schützen · 90-Tage-Plan mit Nicht-Liste",
        "upsell":
            "Am Kursende verweist du auf Instagram-Kundenmaschine, Digitale "
            "Produktwelt und MBA mit Teilnehmerinnen-Rabatt. Das ist bisher ein "
            "Video im Kurs, kein Checkout-Upsell.",
    },
    "a-storyideen-f-r-networkerinne": {
        "inhalt":
            "Workbook mit 90 Storyideen für Networkerinnen, 19 CHF. "
            "Einstiegsprodukt aus der Meta-Anzeige.\n"
            "Nächster Schritt in der Treppe: „Finde dein Thema“ für 39.",
        "bump": "Content-Box (30 Hook-Vorlagen) für 17 CHF.",
    },
    "a-mba": {
        "inhalt":
            "Bundle aus 3 Kursen plus Umsetzerinnen-Calls, auf der ThriveCart "
            "Academy: Instagram-Kundenmaschine · Mama-CEO · Digitale Produktwelt.\n"
            "Pioneer-Preis 997, Listenpreis 1347.\n\n"
            "Achtung: aus Evergreen-Produkten nie direkt zum 1347 verlinken — das "
            "widerspricht dem 997-Event-Preis.",
    },
    "a-expertin-statt-verk-uferin": {
        "inhalt":
            "97-CHF-Kurs. Weg vom Produkt-Posten hin zur erkennbaren Expertin.",
    },
    "a-1-1-aus-nebenbei-wird-busine": {
        "inhalt":
            "1:1-Begleitung, Beta-Preis 777 statt 1500.",
    },
}

# --------------------------------------------------------------------------
# Was offen ist
# --------------------------------------------------------------------------
IDEEN = [
    ("Automation für die 4 Brücken-Mails im Produkt-Ideen-Finder bauen",
     "Funnel", "Als nächstes", "mittel",
     "Texte stehen in outputs/funnels/produkt-ideen-finder/mails-2-4-bruecke.md, "
     "Wiring in ac-einrichtung.md. Trigger-Tag 98, Ausschluss-Tag 79, Tag 8 → Tag 87."),
    ("Kaufpreis-Tag für eigene-produkterstellung bestätigen",
     "Funnel", "Als nächstes", "klein",
     "Vermutlich Tag 43 — muss geprüft werden, sonst läuft der Ausschluss "
     "in der Brücken-Automation ins Leere."),
    ("Keyword SICHTBAR hat keine Automation",
     "Funnel", "Idee", "mittel",
     "0€ Starterguide wird nur über ManyChat ausgeliefert, danach passiert nichts."),
    ("Keyword STORY hat keine Automation",
     "Funnel", "Idee", "mittel",
     "Story-Challenge liefert aus, aber es gibt keine Nurture-Strecke."),
    ("Keyword ZEITFENSTER hat keine Automation",
     "Funnel", "Idee", "mittel", "Freischaufeln läuft ohne Anschluss."),
    ("Anker #zum-minikurs auf WordPress-Seite 4085 ist tot",
     "Website", "Als nächstes", "klein",
     "Der Link in der Mail zeigt auf eine Sprungmarke, die es auf der Seite nicht gibt."),
    ("Loop 1: Sprungbedingung für ideen-finder-durchlaufen ergänzen",
     "Funnel", "Idee", "klein",
     "In Automation 72 fehlt die Bedingung bei „Springen zu M1“, sonst bekommen "
     "Leute aus dem Ideen-Finder die Strecke doppelt."),
    ("ThriveCart anbinden",
     "Technik", "Idee", "mittel",
     "Offizielle API mit eigenem Schlüssel. Würde Bumps, Up- und Downsells und "
     "echte Umsätze automatisch ins Cockpit holen, statt sie von Hand zu pflegen."),
    ("doTERRA-Zahlen ins Cockpit",
     "doTERRA", "Idee", "gross",
     "Kunden, Treueprogramm, OV, PV, Power of 3 und 9. doTERRA hat keine offene "
     "Schnittstelle — realistisch über den Report-Export aus dem Backoffice."),
    ("Umsatz aus outputs/finanzen in den Abgleich hängen",
     "Technik", "Idee", "mittel",
     "Die Cashflow-Auswertungen liegen als Markdown vor und könnten in "
     "„Zahlen & Ziele“ landen, statt von Hand eingetippt zu werden."),
    ("Drei Listen stehen auf 0 Kontakten",
     "Funnel", "Idee", "klein",
     "Quiz-Kontakte, MBA Webinar und Willkommenssequenz. Entweder ist das "
     "Wiring kaputt oder die Listen sind Karteileichen."),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziel = Path(args[0]) if args else ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)
    ueberschreiben = "--ueberschreiben" in sys.argv

    heute = date.today().isoformat() + "T00:00:00.000Z"
    dateien = {
        "produkt-details.json": {"werte": DETAILS, "updatedAt": heute},
        "ideenkasten.json": {
            "items": [{"id": "ik-%02d" % n, "idee": i[0], "bereich": i[1],
                       "status": i[2], "aufwand": i[3], "notiz": i[4]}
                      for n, i in enumerate(IDEEN)],
            "updatedAt": heute},
    }

    for name, inhalt in dateien.items():
        pfad = ziel / name
        if pfad.exists() and not ueberschreiben:
            print("  ÜBERSPRUNGEN  %s (gibt es schon — mit --ueberschreiben erzwingen)"
                  % name)
            continue
        pfad.write_text(json.dumps(inhalt, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        anzahl = len(inhalt.get("items") or inhalt.get("werte") or [])
        print("  %-22s %2d Einträge" % (name, anzahl))

    print("\nAbgelegt in: %s" % ziel.resolve())


if __name__ == "__main__":
    main()
