"""
Die geprueften Chat-Ideen in den Ideenkasten uebernehmen.

Der Sammler (`chat-ideen-sammeln.py`) findet Kandidaten, aber viele davon sind
Zitate aus Dokumenten statt echter Einfaelle. Was hier steht, ist von Hand
durchgesehen: nur Saetze, die Patricia selbst gesagt hat, die noch offen sind
und die ins Business gehoeren.

Wichtig: bestehende Eintraege bleiben unberuehrt. Der Ideenkasten gehoert
Patricia — hier wird nur angehaengt und zwei erledigte Punkte abgehakt.

Aufruf:
  python scripts/cockpit/chat-ideen-einpflegen.py <ideenkasten.json> [ziel.json]
"""
import io
import json
import sys
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

AUF = "„"   # „
ZU = "“"    # "


def z(text):
    """Ein Zitat in deutsche Anfuehrungszeichen setzen."""
    return AUF + text + ZU


# Was in diesen Wochen erledigt wurde und im Kasten noch als offen steht.
ERLEDIGT = {
    "ThriveCart anbinden":
        "Am 11.09.2026 angebunden: Produkte, Bumps, Upsells und Downsells "
        "kommen jetzt automatisch.",
    "doTERRA-Zahlen ins Cockpit":
        "Rang-Tracker steht. Die Zahlen kommen aus dem Schlagdistanz-Bericht "
        "und werden monatlich von Hand angestossen.",
}

# Aus 101 Chats gelesen, von Hand geprueft.
AUS_CHATS = [
    ("Storyideen als Order Bump für 19 statt als Einzelprodukt",
     "Produkt", "Idee", "klein",
     "Chat vom 28.08.2026: " + z("storyideen könnte man doch als orderbump für "
     "19 anbieten — wäre ja viel mehr wert") + " Heute hängt es umgekehrt: die "
     "Content-Box ist der Bump am Storyideen-Checkout."),

    ("Zwei MBA-fremde Kurse als Appetitmacher einsetzen",
     "Produkt", "Idee", "mittel",
     "Chat vom 02.08.2026: " + z("Zwei davon sind NICHT in der MBA — wäre cool, "
     "wenn ich sie damit etwas gluschtig machen könnte") + " Am MBA-Checkout "
     "hängt bis heute weder Bump noch Upsell."),

    ("Visuals der einzelnen Kurse im Cockpit zeigen",
     "Technik", "Idee", "mittel",
     "Chat vom 30.06.2026: " + z("vielleicht könnte man bei den einzelnen kursen "
     "noch die visuals rein nehmen?") + " Die Mockups liegen in den Kursordnern."),

    ("Freebie für Block 2 fehlt",
     "Funnel", "Idee", "mittel",
     "In den Chats vom 04. und 07.07.2026 zweimal gefragt: " +
     z("für Block 2 fehlt mir doch aktuell noch ein geeignetes Freebie oder?")),

    ("Powerslot-Finder umbenennen",
     "Produkt", "Idee", "klein",
     "Chat vom 04.07.2026: " + z("Könnte man den Powerslot finder anders benennen?")),

    ("Hütchenmethode in den Content holen",
     "Content", "Idee", "klein",
     "Chat vom 07.07.2026: " + z("vielleicht könnte man die hutmethode etwas "
     "reinnehmen?") + " Steht als Lektion 2.3 in Mama-CEO."),

    ("Hook-Idee: " + z("Nichts für ungut …"),
     "Content", "Idee", "klein",
     "Chat vom 31.07.2026: " + z("hatte gerade eine mega geile hook idee: Nichts "
     "für ungut..") + " — nie ausgebaut."),

    ("Auflockerungs-Foto von dir fehlt in den Designs",
     "Content", "Idee", "klein",
     "Chat vom 05.08.2026: " + z("mir fehlt noch ein foto von mir als auflockerung.")),

    ("Einwand-Content: warum sie nicht mit Instagram anfangen",
     "Content", "Idee", "mittel",
     "Chat vom 24.08.2026: " + z("könnten wir bei dem was sie nicht brauchen auf "
     "konkrete Einwände gehen, warum sie nicht mit Instagram anfangen?")),

    ("Transkripte für " + z("Expertin statt Verkäuferin") + " erzeugen",
     "Technik", "Als nächstes", "klein",
     "Der Kurs hat 13 Videos, aber keine Transkripte — deshalb steht er als "
     "einziger ohne Stichwörter im Kurs-Register. Die Videoschnitt-Pipeline "
     "kann das erledigen."),
]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    quelle = sys.argv[1]
    ziel = sys.argv[2] if len(sys.argv) > 2 else quelle

    d = json.loads(io.open(quelle, encoding="utf-8").read())
    items = d.get("items", [])
    vorher = len(items)

    abgehakt = 0
    for x in items:
        for anfang, notiz in ERLEDIGT.items():
            if x.get("idee", "").startswith(anfang) and x.get("status") != "Erledigt":
                x["status"] = "Erledigt"
                x["notiz"] = notiz
                abgehakt += 1

    vorhanden = {x.get("idee", "") for x in items}
    neu = 0
    for i, (idee, bereich, status, aufwand, notiz) in enumerate(AUS_CHATS):
        if idee in vorhanden:
            continue
        items.append({"id": "ik-c%02d" % i, "idee": idee, "bereich": bereich,
                      "status": status, "aufwand": aufwand, "notiz": notiz})
        neu += 1

    d["items"] = items
    d["updatedAt"] = date.today().isoformat() + "T00:00:00.000Z"
    io.open(ziel, "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, indent=2))

    print("  %d Einträge vorher · %d aus den Chats dazu · %d abgehakt"
          % (vorher, neu, abgehakt))
    print("  %d Einträge jetzt" % len(items))
    print("\nGeschrieben: %s" % ziel)


if __name__ == "__main__":
    main()
