"""
Baut die Nachkauf-Mails für das 1:1 „Magnet-Ich" als fertige Mail-HTMLs.

Das Gerüst (Kopf, Farben, Fuss, Outlook-Tabellen, Umlaut-Wächter, Kopierseite)
kommt aus scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert:
eine Stelle, an der das Mail-Design gepflegt wird.

  python scripts/magnet-ich/mails-bauen.py

Ausgabe: outputs/produkte/magnet-ich/mails/
  mail-00-willkommen.html · mail-03-vorbereitung.html · index.html (Kopierseite)

Ersetzt in ActiveCampaign die Automation 42 „Magnet-ich" (bisher eine Mail,
„Magnet-ich 1", ID 375, mit dem Drive-PDF und einem kaputten Instagram-Link).

🔁 Die Herbst-Aktion (Start-Calls ab 19.10., dritter Call bei Anmeldung bis
   27.09.) steht jeweils in EINEM Kasten mit Kopf „Herbst 2026". Nach der
   Aktion den Kasten löschen, der Rest der Mail bleibt richtig.
"""
import html
import importlib.util
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)

ZIEL = ROOT / "outputs" / "produkte" / "magnet-ich" / "mails"
ONBOARDING = "https://claude.ai/artifact/MBpprtwLrrgQzenaiPoBny"
WHATSAPP = "https://wa.me/41793591937"
INSTAGRAM = "https://www.instagram.com/mumlifebalance_patricia_ulmann/"

absatz, kasten, liste, knopf, h2, ps, gruss = sk.absatz, sk.kasten, sk.liste, sk.knopf, sk.h2, sk.ps, sk.gruss
merken = sk.merken

HERBST_MAIL0 = kasten(
    sk.P_ENG % ("Weil du dich in der Herbst-Aktion angemeldet hast: Die Start-Calls finden "
                "<strong>ab dem 19. Oktober</strong> statt, direkt nach den Ferien — und du bekommst "
                "<strong>einen dritten Call dazu</strong>, den wir irgendwo in deine drei Wochen legen, "
                "dorthin, wo du ihn am meisten brauchst."),
    "#fdf1e6", rand=sk.ORANGE, kopf="Herbst 2026", kopffarbe=sk.ORANGE)

HERBST_MAIL3 = kasten(
    sk.P_ENG % ("Die Start-Calls finden ab dem <strong>19. Oktober</strong> statt. Wenn du mir "
                "deine Antworten in den Ferien schickst, kann ich mich in Ruhe darauf vorbereiten "
                "und wir sind im ersten Call sofort mittendrin."),
    "#fdf1e6", rand=sk.ORANGE, kopf="Herbst 2026", kopffarbe=sk.ORANGE)

MAILS = [
    {
        "datei": "mail-00-willkommen.html", "tag": "0", "warten": "sofort nach dem Kauf",
        "marke": "Magnet-Ich",
        "betreff": "Willkommen im Magnet-Ich — so geht es jetzt weiter",
        "betreff2": "Dein erster Schritt ist getan",
        "wann": "sofort nach dem Kauf (ersetzt „Magnet-ich 1“, ID 375, in Automation 42)",
        "preheader": "Deine neun Vorbereitungsfragen und wie wir deinen Start-Call abmachen.",
        "h1": "Schön, dass du dabei bist!",
        "unterzeile": "Drei Wochen, in denen wir zusammen klären, wofür man dich kennen soll.",
        "notiz": """Ersetzt die bisherige Mail mit dem Drive-PDF. Das PDF hat auf Seite 14 noch
Platzhaltertext und war nicht ausfüllbar ohne Drucker — die Fragen stehen jetzt
auf der Onboarding-Seite und kommen per WhatsApp zurück.
Herbst-Kasten entfernt am 28.09.2026 (Aktion ohne Verkauf beendet).
🚨 Die Onboarding-Seite muss öffentlich geteilt sein, sonst sieht die Kundin eine Anmeldemaske.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("wie schön, dass du dich für das <strong>Magnet-Ich</strong> entschieden hast. "
                   "Ich freue mich richtig darauf, dich in den nächsten drei Wochen zu begleiten — "
                   "bis du in einem Satz sagen kannst, wofür man dich kennen soll, und eine Bio und "
                   "erste Beiträge hast, die sich nach dir anfühlen."),
            h2("Zwei Dinge für jetzt"),
            liste("So geht es weiter", [
                "<strong>1 · Deine Vorbereitung.</strong> Auf deiner Onboarding-Seite stehen neun Fragen "
                "zu deinem Business, deinem Umfeld und dem, was dich bremst. Du beantwortest sie in Ruhe "
                "auf dem Handy, und mit einem Tipp kommen sie per WhatsApp bei mir an.",
                "<strong>2 · Dein Start-Call.</strong> Schreib mir kurz auf WhatsApp, wann es dir passt, "
                "dann machen wir den Termin für unseren ersten Call ab. Er dauert 60 bis 75 Minuten und "
                "läuft über Zoom — den Link bekommst du von mir.",
            ]),
            knopf("Zu meinen Vorbereitungsfragen", ONBOARDING),
            absatz("Es gibt dort keine falschen Antworten. Wenn etwas chaotisch oder unscharf ist, "
                   "schreib es genau so hin, denn genau damit arbeiten wir."),
            kasten(sk.P_ENG % ('Meine WhatsApp-Nummer: <strong>+41 79 359 19 37</strong><br>'
                               '<a href="%s" style="color:%s;">Direkt eine Nachricht schreiben</a>'
                               % (WHATSAPP, sk.PETROL)),
                   "#e4f3f4", rand=sk.PETROL, kopf="Für den Termin"),
            absatz("Montag bis Freitag hörst du in der Regel am gleichen Tag von mir. Und falls ein "
                   "Termin einmal nicht passt, sag es mir einfach vorher — dann verschieben wir ihn.", True),
            gruss("Ich freu mich auf dich,"),
            ps('P.S. Du musst nicht perfekt vorbereitet sein, du musst nur bereit sein. '
               'Und wenn du mir zwischendurch folgen magst: <a href="%s" style="color:%s;">'
               'hier bin ich auf Instagram</a>.' % (INSTAGRAM, sk.PETROL)),
        ],
    },
    {
        "datei": "mail-03-vorbereitung.html", "tag": "3", "warten": "+3 Tage",
        "marke": "Magnet-Ich",
        "betreff": "Hast du deine neun Fragen schon beantwortet?",
        "betreff2": "Deine Vorbereitung fürs Magnet-Ich",
        "wann": "3 Tage nach dem Kauf (neu in Automation 42)",
        "preheader": "Eine Viertelstunde, und wir sind im Start-Call sofort mittendrin.",
        "h1": "Eine Viertelstunde für dich",
        "unterzeile": "Damit dein Start-Call nicht bei null beginnt.",
        "notiz": """Kurze Erinnerung. ActiveCampaign weiss nicht, ob die Antworten per WhatsApp
schon da sind — deshalb der Satz „wenn du sie mir schon geschickt hast, ignorier
diese Mail einfach“.
Herbst-Kasten entfernt am 28.09.2026 (Aktion ohne Verkauf beendet).""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("ich wollte dir nur kurz deine Vorbereitungsfragen nochmal hinlegen. Die meisten "
                   "brauchen dafür eine Viertelstunde, und oft ist es genau die Frage, bei der man am "
                   "längsten zögert, die uns im Start-Call am weitesten bringt."),
            merken("Die Frage, bei der die meisten hängen bleiben",
                   "„Welche Idee oder welches Thema kommt immer wieder zu dir zurück, auch wenn du es wegschiebst?“",
                   "Schreib einfach auf, was dir als Erstes einfällt — auch wenn es dir zu klein oder zu verrückt vorkommt."),
            knopf("Jetzt meine Fragen beantworten", ONBOARDING),
            absatz("Wenn du sie mir schon geschickt hast: danke dir, dann ignorier diese Mail einfach. "
                   "Und falls unser Termin für den Start-Call noch nicht steht, schreib mir kurz auf "
                   'WhatsApp — <a href="%s" style="color:%s;">+41 79 359 19 37</a>.' % (WHATSAPP, sk.PETROL), True),
            gruss("Bis ganz bald,"),
        ],
    },
]


# Die Verkaufsmail an Interessentinnen — eine Kampagne, keine Nachkauf-Mail.
# Steht deshalb NICHT in MAILS (die gehen nach Automation 42 ins Cockpit).
# Text aus outputs/strategie/2026-09-24-magnet-ich-fast-cash.md.
KASSE = "https://mumlifebalance.thrivecart.com/magnet-ich/"
SEITE = "https://mumlifebalance.ch/magnet-ich/"

KAMPAGNE = [
    {
        "datei": "kampagne-herbst-2026.html", "tag": "Fr", "warten": "Kampagne Fr 25.9.",
        "marke": "Magnet-Ich · Herbst",
        "betreff": "Weisst du inzwischen, worüber du reden willst?",
        "betreff2": "Drei Plätze im 1:1, Start nach den Herbstferien",
        "wann": "als Kampagne, Fr 25.9. · an Tags 46, 41, 42, 61, 40/69 · ohne 39 und 79",
        "preheader": "Drei Plätze im 1:1, Start nach den Herbstferien.",
        "h1": "Drei Plätze im 1:1 nach den Herbstferien",
        "unterzeile": "Drei Wochen, in denen wir dein Thema zusammen klären.",
        "notiz": """Kampagne, keine Automation. Einschliessen: Tags 46, 41, 42, 61, 40/69.
Ausschliessen: 39 (Instagram-Kundenmaschine) und 79 (mba-kauf) — für die wäre
Magnet-Ich ein Schritt zurück. Anmeldung bis So 27.9., 20 Uhr.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("egal, ob du schon länger in meiner Welt bist oder erst seit Kurzem dabei, heute "
                   "frag ich dich ganz direkt: Weisst du inzwischen, worüber du auf Instagram eigentlich "
                   "reden willst?"),
            absatz("Wenn du jetzt kurz zögerst, bist du in guter Gesellschaft. Die meisten Frauen, mit "
                   "denen ich arbeite, haben drei, vier Themen im Kopf, posten mal hier und mal da, und am "
                   "Ende fühlt sich keins davon ganz richtig an. Allein dreht man sich dabei oft im Kreis, "
                   "weil einem niemand sagt, welches davon eigentlich trägt."),
            absatz("Genau dafür gibt es das <strong>Magnet-Ich</strong>: drei Wochen, in denen wir das "
                   "zusammen klären."),
            liste("So laufen deine drei Wochen", [
                "<strong>Start-Call</strong> — ein langer Call, in dem wir dein Thema, deine echte "
                "Zielgruppe und deine Kernbotschaft herausarbeiten.",
                "<strong>Drei Wochen WhatsApp</strong> — ich begleite dich, während du deine Bio und "
                "deine ersten Beiträge dazu schreibst.",
                "<strong>Abschluss-Call</strong> — wir setzen uns nochmal zusammen und legen deine "
                "nächsten Schritte fest.",
            ]),
            kasten(sk.P_ENG % ("Nach den Herbstferien nehme ich <strong>drei Frauen</strong> ins 1:1. "
                               "Die Start-Calls finden ab dem <strong>19. Oktober</strong> statt, und ab da "
                               "laufen deine drei Wochen. Wer sich bis Sonntag anmeldet, bekommt "
                               "<strong>einen dritten Call dazu</strong>, den wir irgendwo in deine drei "
                               "Wochen legen, dorthin, wo du ihn am meisten brauchst."),
                   "#fdf1e6", rand=sk.ORANGE, kopf="Herbst 2026", kopffarbe=sk.ORANGE),
            absatz("Die Vorbereitungsfragen schicke ich dir gleich nach der Anmeldung, die kannst du in "
                   "aller Ruhe in den Ferien beantworten. Das Magnet-Ich kostet 333 Franken oder "
                   "zweimal 166.50."),
            knopf("Hier sicherst du dir deinen Platz", KASSE),
            absatz('Die Anmeldung ist bis <strong>Sonntag, 27. September, 20 Uhr</strong> offen, oder bis '
                   'die drei Plätze weg sind. Alles im Detail findest du '
                   '<a href="%s" style="color:%s;">auf meiner Seite zum Magnet-Ich</a>.' % (SEITE, sk.PETROL), True),
            gruss("Herzlich,"),
            ps("P.S. Wenn du unsicher bist, ob das für dich passt, antworte einfach auf diese Mail und "
               "erzähl mir in zwei Sätzen, wo du gerade stehst. Ich sag dir ehrlich, ob das Magnet-Ich "
               "jetzt der richtige Schritt für dich ist."),
        ],
    },
]


def erinnerung(letzter_platz):
    """Sonntags-Erinnerung. Mit letzter_platz=True nur verschicken, wenn wirklich
    zwei der drei Plätze verkauft sind — ein erfundener Engpass geht nie raus."""
    if letzter_platz:
        datei, betreff, h1 = ("kampagne-herbst-2026-erinnerung-letzter-platz.html",
                              "Nur noch ein Platz frei — heute um 20 Uhr ist Schluss",
                              "Nur noch ein Platz frei")
        ps_text = "P.S. Von den drei Plätzen ist noch einer frei. Wenn er weg ist, schliesse ich auch vor 20 Uhr."
    else:
        datei, betreff, h1 = ("kampagne-herbst-2026-erinnerung.html",
                              "Heute um 20 Uhr ist Schluss", "Heute Abend ist Schluss")
        ps_text = "P.S. Es bleiben drei Plätze, weil ich jede Frau persönlich begleite."
    return {
        "datei": datei, "tag": "So", "warten": "Kampagne So 27.9., 10 Uhr",
        "marke": "Magnet-Ich · Herbst",
        "betreff": betreff,
        "betreff2": "Woran du merkst, dass dir dein Thema noch fehlt",
        "wann": "als Kampagne, So 27.9. 10 Uhr · gleiches Segment wie Freitag, Käuferinnen ausschliessen",
        "preheader": "Woran du merkst, dass dir dein Thema noch fehlt, und warum „nächstes Jahr“ nicht kommt.",
        "h1": h1,
        "unterzeile": "Und woran du merkst, dass dir dein Thema noch fehlt.",
        "notiz": ("Erinnerung zur Freitags-Mail. Gleiches Segment, zusätzlich alle ausschliessen, "
                  "die seit Freitag gekauft haben."
                  + (" 🚨 NUR verschicken, wenn wirklich zwei Plätze verkauft sind." if letzter_platz else "")),
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("heute Abend um 20 Uhr schliesse ich die Anmeldung fürs Magnet-Ich. Vorher möchte ich "
                   "dir noch zeigen, woran du erkennst, dass dir dein Thema noch fehlt, denn die meisten "
                   "merken es gar nicht, weil sie ja trotzdem jeden Tag etwas posten."),
            h2("Woran du merkst, dass dein Thema noch fehlt"),
            liste("Wenn du dich hier wiederfindest", [
                "Du sitzt vor dem Handy und überlegst jedes Mal neu, was du heute posten sollst.",
                "Wenn dich jemand fragt, was du machst, erzählst du zuerst von deiner Firma oder deinem Produkt.",
                "Ein Beitrag über dein Produkt, einer über die Kinder, einer über Motivation, und keiner "
                "davon fühlt sich so richtig nach dir an.",
                "Es kommen ein paar Likes, aber kaum jemand fragt nach, und wenn doch, dann eher aus Höflichkeit.",
            ]),
            absatz("Wenn du bei zwei oder mehr Punkten nickst, fehlt dir mit grosser Wahrscheinlichkeit "
                   "dein Thema, und mehr zu posten ändert daran leider wenig."),
            h2("Warum dein Produkt nicht dein Thema ist"),
            absatz("Der naheliegende Gedanke ist: Mein Thema ist doch mein Produkt. Das Schwierige daran "
                   "ist, dass dasselbe Produkt ganz viele andere Frauen auch anbieten, zum selben Preis und "
                   "oft mit denselben Bildern. Wer dir zuschaut, hat dann keinen Grund, ausgerechnet bei dir "
                   "zu kaufen, und dein ganzer Auftritt hängt an einer Firma, die du selbst nicht in der "
                   "Hand hast."),
            merken("Der Satz, um den es geht",
                   "„Das Produkt bekommt sie überall. Das, was sich mit dir verändert, bekommt sie nur bei dir.“",
                   "Dein Thema ist diese Veränderung, und dein Produkt ist ein Werkzeug auf dem Weg dorthin."),
            absatz("Genau diese Verbindung aus deinem Wissen, deiner Geschichte und dem, was du anbietest, "
                   "suchen wir im Magnet-Ich zusammen. Wenn sie steht, weisst du bei jedem Beitrag, warum du "
                   "ihn schreibst, und die richtigen Frauen merken, dass sie bei dir gemeint sind."),
            h2("„Nächstes Jahr, wenn die Kinder in der Schule sind“"),
            absatz("Und dann gibt es noch den Gedanken, den ich selbst gut kenne: Ich mach das dann richtig, "
                   "wenn es ruhiger wird, wenn die Kinder grösser sind oder das neue Schuljahr läuft. Mit vier "
                   "Kindern kann ich dir sagen, dass dieses Dann nicht kommt. Es kommt ein neues Schuljahr, "
                   "ein neuer Infekt, ein neues Hobby, zu dem jemand gefahren werden will, und das Handy liegt "
                   "trotzdem jeden Tag in deiner Hand."),
            absatz("Ein klares Thema macht jeden Beitrag danach leichter, und zwar genau in dem Alltag, den "
                   "du heute schon hast. Dafür sind die drei Wochen da."),
            kasten(sk.P_ENG % ("Wer sich <strong>heute bis 20 Uhr</strong> anmeldet, bekommt den "
                               "<strong>dritten Call dazu</strong>. Die Start-Calls finden ab dem 19. Oktober "
                               "statt, und das Magnet-Ich kostet 333 Franken oder zweimal 166.50."),
                   "#fdf1e6", rand=sk.ORANGE, kopf="Nur noch heute", kopffarbe=sk.ORANGE),
            knopf("Ich bin dabei", KASSE),
            absatz('Und wenn du nicht sicher bist, ob es für dich passt, antworte einfach auf diese Mail. '
                   'Ich schaue heute noch rein und sag dir ehrlich, ob es jetzt der richtige Schritt ist. '
                   'Alles im Detail steht <a href="%s" style="color:%s;">auf meiner Seite zum Magnet-Ich</a>.'
                   % (SEITE, sk.PETROL), True),
            gruss("Herzlich,"),
            ps(ps_text),
        ],
    }


KAMPAGNE += [erinnerung(False), erinnerung(True)]


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    karten, beanstandet = [], 0
    for m in MAILS + KAMPAGNE:
        fertig = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "NACHKAUF-STRECKE MAGNET-ICH").replace(
            "ERZEUGT von scripts/startklar/mails-bauen.py", "ERZEUGT von scripts/magnet-ich/mails-bauen.py")
        beanstandet += len(sk.umlaute_pruefen(m["datei"], fertig))
        (ZIEL / m["datei"]).write_text(fertig, encoding="utf-8")
        kennung = re.sub(r"[^a-z0-9]+", "", m["datei"].lower())
        karten.append(sk.KARTE.format(
            tag=m["tag"], h1=m["h1"], warten=m["warten"],
            betreff=html.escape(m["betreff"], quote=False),
            betreff_roh=html.escape(m["betreff"], quote=True),
            datei=m["datei"], id=kennung))
        print("  geschrieben:", m["datei"])
    seite = sk.KOPIERSEITE.format(karten="\n".join(karten)).replace("Startklar", "Magnet-Ich")
    # Einleitung, Warnkasten und Engine-Karte der Vorlage gehören zu Startklar
    seite = re.sub(r'<p class="unter">.*?</p>',
                   '<p class="unter">Die Nachkauf-Mails und die Herbst-Kampagne fürs Magnet-Ich. '
                   'Knopf „Ganzes HTML“ tippen, in ActiveCampaign einfügen.</p>', seite, count=1, flags=re.S)
    seite = re.sub(r'<div class="warnung">.*?</div>',
                   '<div class="warnung"><b>Beim Einrichten:</b> Die Nachkauf-Mails gehören in Automation 42, '
                   'die Kampagnen-Mails werden einzeln versendet.</div>', seite, count=1, flags=re.S)
    seite = re.sub(r'<div class="karte">\s*<h2>Und danach: ab in die Engine</h2>.*?</div>', '',
                   seite, count=1, flags=re.S)
    assert "Sieben Mails" not in seite and "Engine" not in seite
    (ZIEL / "index.html").write_text(seite, encoding="utf-8")
    print("  geschrieben: index.html (Kopierseite)")
    print("  ✓ Keine umschriebenen Umlaute." if not beanstandet else "  ⚠ %d Umlaut-Funde" % beanstandet)


if __name__ == "__main__":
    main()
