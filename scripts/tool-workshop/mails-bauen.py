"""Mails zum Tool-Workshop (November 2026): drei Launch-Mails an die Liste, vier Nachkauf-Mails.

Texte: outputs/produkte/tool-workshop/angebot/04-mails.md (dort wird geschrieben, hier gesetzt).
Geruest (Kopf, Farben, Bausteine) kommt aus scripts/startklar/mails-bauen.py, importiert, nicht kopiert.

    python scripts/tool-workshop/mails-bauen.py              # HTML nach outputs/produkte/tool-workshop/mails/
    python scripts/tool-workshop/mails-bauen.py --hochladen  # zusaetzlich als Kampagnen-ENTWURF in AC (status 0)

Mit --hochladen wird nichts verschickt. A1-A3 liegen an Liste 2, B0-B3 an Liste 16 (Kunden).
Die Automation „Tool-Workshop“ (Ausloeser Tag 107) baut Patricia in AC von Hand und waehlt dort
die Entwuerfe B0-B3 als Vorlage. Zugang aus 04-projects/activecampaign-mcp/.env.
"""
import importlib.util
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)

ZIEL = ROOT / "outputs" / "produkte" / "tool-workshop" / "mails"
absatz, kasten, liste, knopf, ps, gruss = sk.absatz, sk.kasten, sk.liste, sk.knopf, sk.ps, sk.gruss
P_ENG, ORANGE = sk.P_ENG, sk.ORANGE

KASSE = "https://mumlifebalance.thrivecart.com/tool-workshop/"
KASSE_DPW = "https://mumlifebalance.thrivecart.com/digitale-produktwelt/"   # Evergreen, 333 oder 2x 166.50
SEITE = "https://mumlifebalance.ch/tool-workshop/"
NISCHE = "https://mlb-nischengenerator.vercel.app"   # KI-Fassung nach dem Kurs „Finde dein Thema“, mit Tool-Ideen
# ✏️ Sobald bekannt eintragen. Leer = es steht ein sichtbarer Platzhalter in der Mail.
UHRZEIT = "19:00 Uhr"
# Zoom- und Gruppenlinks tragen Passwörter: sie stehen in scripts/tool-workshop/.env (gitignored), nie hier.
_ENV = {}
if (pathlib.Path(__file__).parent / ".env").exists():
    for _z in (pathlib.Path(__file__).parent / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in _z and not _z.strip().startswith("#"):
            _k, _v = _z.split("=", 1)
            _ENV[_k.strip()] = _v.strip().strip("\"'")
ZOOM_1 = _ENV.get("ZOOM_1", "")
ZOOM_2 = _ENV.get("ZOOM_2", "")
GRUPPE = _ENV.get("GRUPPE", "")
UHR = UHRZEIT or "✏️ UHRZEIT"


def platz(wert, was):
    return wert or ("✏️ " + was)


MAILS = [
    {"datei": "A1-anmeldung-offen.html", "liste": 2, "name": "Tool-Workshop A1 · Anmeldung offen (Fr 30.10.)",
     "marke": "mumlifebalance · Tool-Workshop",
     "betreff": "Ein PDF wird heruntergeladen, ein Tool wird benutzt",
     "betreff2": "Am 10. November bauen wir dein Gratis-Tool",
     "wann": "sofort, Fr 30.10.2026, an Liste 2",
     "preheader": "Am 10. November bauen wir dein Gratis-Tool, live.",
     "h1": "Dein Gratis-Angebot als Tool", "unterzeile": "Live am 10. und 11. November",
     "notiz": "Launch A1. Kasse offen bis Mo 9.11. 23:59.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("wann hast du das letzte PDF geöffnet, das du dir irgendwo geholt hast?"),
         absatz("Bei vielen liegen sie im Download-Ordner, und die Person, die es verschenkt hat, hört "
                "nichts mehr. Darum baue ich meine Gratis-Angebote seit einiger Zeit als kleine Tools: "
                "einen Bio-Check, einen Stimm-Check, einen Produkt-Ideen-Finder. Wer sie ausfüllt, erlebt "
                "etwas und hat am Schluss ein Ergebnis in der Hand. In deinem Network "
                "verschenken fast alle E-Books und PDFs. Mit einem Tool fällst du auf, und es öffnet den "
                "Kontakt: Wer ein Ergebnis bekommen hat, hört dir zu, wenn du danach von deinem Produkt erzählst."),
         absatz("Gebaut habe ich sie mit Claude, ohne programmieren zu können. Und genau das machen wir "
                "jetzt zusammen."),
         liste("Im Tool-Workshop", [
             "<strong>Dienstag, 10. November, 19:00 Uhr:</strong> du baust live dein eigenes Gratis-Tool zu deiner Nische",
             "<strong>Mittwoch, 11. November, 19:00 Uhr:</strong> die Seite, auf der man sich dafür einträgt",
             "<strong>Danach:</strong> drei Tage Begleitung, bis beides online ist. Die Calls werden aufgezeichnet.",
         ]),
         absatz("Der Workshop kostet 39 Franken oder 39 Euro, die Anmeldung ist offen bis Montag, 9. November."),
         knopf("Ich bin dabei", SEITE),
         absatz("Und wenn du noch nicht weisst, welche Nische zu dir passt: Den Nischengenerator kannst du "
                "gratis vorher ausfüllen.", True),
         knopf("Zum Nischengenerator", NISCHE),
         gruss("Herzlich,"),
     ]},
    {"datei": "A2-nicht-technisch.html", "liste": 2, "name": "Tool-Workshop A2 · Nicht technisch (Fr 6.11.)",
     "marke": "mumlifebalance · Tool-Workshop",
     "betreff": "„Ich bin überhaupt nicht technisch“",
     "betreff2": "Das musst du für den Workshop auch nicht sein",
     "wann": "Fr 6.11.2026, an Liste 2 (Käuferinnen mit Tag 107 ausschliessen)",
     "preheader": "Das musst du für den Workshop auch nicht sein.",
     "h1": "Du musst nicht technisch sein", "unterzeile": "Tool-Workshop am 10. und 11. November",
     "notiz": "Launch A2. Segment: ohne Tag Tool-Workshop (107).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("falls du beim Wort Tool gerade gedacht hast „Ich bin überhaupt nicht technisch“: Das musst du für den Workshop auch nicht sein."),
         absatz("Du beschreibst Claude in deinen eigenen Worten, was dein Tool tun soll: welche Fragen es "
                "stellt, was am Schluss als Ergebnis kommt, wohin der Knopf führt. Den Code schreibt Claude. "
                "Wir machen jeden Schritt zusammen, live, und wer hängen bleibt, bekommt in den drei Tagen "
                "danach Hilfe in der Gruppe."),
         absatz("Was du brauchst: ein Gratis-Konto bei Claude und eins bei Netlify. Die Links dazu "
                "bekommst du in der Willkommens-Mail."),
         absatz("Anmeldung bis Montag, 9. November, 23:59, für 39 Franken oder 39 Euro."),
         knopf("Ich bin dabei", SEITE),
         gruss("Herzlich,"),
     ]},
    {"datei": "A3-letzter-tag.html", "liste": 2, "name": "Tool-Workshop A3 · Letzter Tag (Mo 9.11.)",
     "marke": "mumlifebalance · Tool-Workshop",
     "betreff": "Morgen bauen wir, heute schliesst die Anmeldung",
     "betreff2": "Letzter Tag für den Tool-Workshop",
     "wann": "Mo 9.11.2026 morgens, an Liste 2 (Käuferinnen mit Tag 107 ausschliessen)",
     "preheader": "Letzter Tag für den Tool-Workshop.",
     "h1": "Heute um Mitternacht", "unterzeile": "Morgen fangen wir an",
     "notiz": "Launch A3. Segment: ohne Tag Tool-Workshop (107).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("heute um 23:59 schliesst die Anmeldung für den Tool-Workshop, und morgen fangen wir an."),
         absatz("Er passt zu dir, wenn du an beiden Tagen live dabei bist oder die Aufzeichnung schaust und "
                "danach drei Tage dranbleibst. Er passt nicht, wenn du ein fertiges Tool von mir erwartest: "
                "Das baust du selbst, mit mir an deiner Seite."),
         knopf("Ich bin dabei", SEITE),
         gruss("Bis morgen, hoffentlich,"),
         ps("P.S. Ein PDF wird heruntergeladen, ein Tool wird benutzt. In zwei Tagen hast du deins."),
     ]},
    {"datei": "B0-willkommen.html", "liste": 16, "name": "Tool-Workshop B0 · Willkommen (sofort nach Kauf)",
     "marke": "Tool-Workshop · Willkommen",
     "betreff": "Du bist dabei. So bereitest du dich vor",
     "betreff2": "Willkommen im Tool-Workshop",
     "wann": "Automation Tool-Workshop: sofort, wenn Tag 107 gesetzt wird",
     "preheader": "Zwei Gratis-Konten, eine Frage und dein Wissen, mehr braucht es nicht.",
     "h1": "Willkommen im Tool-Workshop", "unterzeile": "Tool-Workshop am 10. und 11. November",
     "notiz": "Den Kurszugang schickt ThriveCart nicht (Auslieferung = Bestätigung). Zoom- und Gruppenlink hier eintragen.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("schön, dass du dabei bist. Hier steht alles, was du bis zum Dienstag brauchst."),
         liste("Die Termine", [
             "<strong>Dienstag, 10. November, %s:</strong> dein Tool · Zoom: %s" % (UHR, platz(ZOOM_1, "Zoom-Link Tag 1")),
             "<strong>Mittwoch, 11. November, %s:</strong> deine Seite · Zoom: %s" % (UHR, platz(ZOOM_2, "Zoom-Link Tag 2")),
             "<strong>12. bis 14. November:</strong> Begleitung in der Gruppe · %s" % platz(GRUPPE, "Link zur Gruppe"),
         ]),
         liste("Deine Vorbereitung", [
             "Ein Gratis-Konto auf <a href=\"https://claude.ai\" style=\"color:%s;\">claude.ai</a>: mit deiner Mailadresse registrieren" % sk.PETROL,
             "Ein Gratis-Konto auf <a href=\"https://app.netlify.com/signup\" style=\"color:%s;\">netlify.com</a>: ebenfalls mit deiner Mailadresse" % sk.PETROL,
             "Den Nischengenerator ausfüllen und den Satz deiner ersten Nische notieren",
             "Eine Frage aufschreiben, die dir die Leute in deinem Network immer wieder stellen",
             "<strong>Dein Wissen fürs Tool:</strong> Hast du ein Workbook, E-Book oder PDF, bring es mit. "
             "Wenn nicht, schreib in ein paar Sätzen auf, was dein Tool können soll. Das reicht.",
         ]),
         knopf("Zum Nischengenerator", NISCHE),
         absatz("Wenn du vorher eine Frage hast, antworte einfach auf diese Mail.", True),
         gruss("Bis bald,"),
     ]},
    {"datei": "C0-tool-ideen-willkommen.html", "liste": 2, "name": "Nischengenerator C0 · Willkommen (sofort, Tag 0€ Nischengenerator)",
     "marke": "mumlifebalance · Nischengenerator",
     "betreff": "Dein Thema, und was du jetzt damit machst",
     "betreff2": "Ein Thema reicht für den Anfang",
     "wann": "Automation am Tag 0€ Nischengenerator (108): sofort",
     "preheader": "Dein Experten-Satz darf heute schon raus.",
     "h1": "Dein eigenes Thema", "unterzeile": "Vom Experten-Satz zu deinem ersten Gratis-Tool",
     "notiz": "Nach dem 9.11. den Workshop-Teil austauschen (Kasse zu).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("schön, dass du dabei bist. Hier ist dein Zugang zum Nischengenerator. Nimm dir zehn Minuten, "
                "Stichworte reichen bei jeder Frage. Du kannst ihn mit derselben Mailadresse bis zu zehn Mal "
                "benutzen, heb dir diese Mail also auf."),
         knopf("Zum Nischengenerator", NISCHE),
         liste("Wenn du dein Thema hast", [
             "Nimm das Thema, bei dem du beim Lesen gedacht hast: Darüber könnte ich stundenlang reden. "
             "Es muss nicht für immer sein, es ist deine Klarheit für heute.",
             "Schreib deinen Experten-Satz in deine Bio und sag ihn in deiner nächsten Story. "
             "So wissen deine Leute, wobei du ihnen hilfst.",
             "Hol dir die Tool-Ideen zu deinem Thema und fang mit einer an, bei der „Geht im Claude-Chat“ steht. "
             "Die kostet dich nichts, auch wenn sie hundertmal ausgefüllt wird.",
         ]),
         absatz("Fast alle im Network verschenken ein PDF, das kaum jemand liest. Mit einem Tool gibst du "
                "deinen Leuten ein Erlebnis und ein Ergebnis zu ihrem Problem, und danach kannst du ganz "
                "natürlich von deinem Produkt erzählen."),
         absatz("Wenn du dein Tool nicht allein bauen willst: Im Tool-Workshop bauen wir es zusammen, am "
                "<strong>10. November um %s</strong> dein Tool und am <strong>11. November</strong> die Seite, "
                "auf der man sich dafür einträgt. Danach begleite ich dich drei Tage. Bring dein Workbook "
                "mit, falls du eins hast." % UHR),
         knopf("Zum Tool-Workshop, 39 Franken oder 39 Euro", KASSE),
         ps("P.S. Antworte mir gern mit deinem Experten-Satz. Ich lese jede Antwort."),
         gruss("Herzlich,"),
     ]},
    {"datei": "B1-morgen.html", "liste": 16, "name": "Tool-Workshop B1 · Morgen geht's los (Mo 9.11., 18:00)",
     "marke": "Tool-Workshop · Morgen",
     "betreff": "Morgen bauen wir dein Tool",
     "betreff2": "Zoom-Link und deine kleine Vorbereitung",
     "wann": "Automation: warten bis Mo 9.11.2026 18:00",
     "preheader": "Zoom-Link und deine kleine Vorbereitung.",
     "h1": "Morgen geht's los", "unterzeile": "Dienstag, 10. November",
     "notiz": "Wer nach 18:00 am 9.11. kauft, bekommt sie nicht; B0 enthält dieselben Angaben.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("morgen um %s sehen wir uns. Zoom-Link: %s" % (UHR, platz(ZOOM_1, "Zoom-Link Tag 1"))),
         absatz("Bring deinen Nischen-Satz und deine Frage mit, und halte Claude in einem zweiten Fenster "
                "offen. Mehr braucht es nicht.", True),
         gruss("Bis morgen,"),
     ]},
    {"datei": "B2-tag-2.html", "liste": 16, "name": "Tool-Workshop B2 · Heute die Seite (Mi 11.11. morgens)",
     "marke": "Tool-Workshop · Tag 2",
     "betreff": "Heute bekommt dein Tool seine Seite",
     "betreff2": "Und die Aufzeichnung von gestern ist da",
     "wann": "Automation: warten bis Mi 11.11.2026 07:00",
     "preheader": "Und die Aufzeichnung von gestern ist da.",
     "h1": "Heute kommt die Seite", "unterzeile": "Mittwoch, 11. November",
     "notiz": "✏️ Wo die Aufzeichnung liegt (Learn-Kurs fehlt noch).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("die Aufzeichnung von gestern liegt bereit: ✏️ LINK ZUR AUFZEICHNUNG. Heute um %s bauen wir "
                "die Seite dazu. Zoom-Link: %s" % (UHR, platz(ZOOM_2, "Zoom-Link Tag 2"))),
         absatz("Hast du dein Tool schon drei Personen geschickt? Ihre Rückmeldung hilft uns heute beim Text "
                "für die Seite.", True),
         gruss("Bis später,"),
     ]},
    # ---- Nischengenerator → Tool-Workshop: Pitch-Serie (Automation 2 nach C0) ------------------
    # Julias Funnel-Logik: nach dem Freebie mehrere Mails auf EIN Angebot. Den letzten Tag (9.11.)
    # übernimmt die Launch-Mail A3 an Liste 2, deshalb hier keine eigene Letzter-Tag-Mail.
    {"datei": "C1-pdf-oder-tool.html", "liste": 2, "name": "Nischengenerator C1 · PDF oder Tool (+1 Tag)",
     "marke": "mumlifebalance · Nischengenerator",
     "betreff": "Drei Eintragungen aus 27 Beiträgen",
     "betreff2": "Warum ich keine PDFs mehr verschenke",
     "wann": "Automation 2: 1 Tag nach C0",
     "preheader": "Und neun aus elf, als ich etwas anderes verschenkt habe.",
     "h1": "PDF oder Tool", "unterzeile": "Was ich an meinen eigenen Zahlen gesehen habe",
     "notiz": "Zahlen aus dem Funnel-Abgleich 30.09.2026 (BIO 11 Beiträge / 9 in der Liste, ECHT1 27 / 3).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("ich habe im September nachgezählt, was meine Gratis-Angebote wirklich bringen, und das "
                "Ergebnis hat mich selbst überrascht."),
         absatz("Für mein Workbook „Von 0 auf echt“, ein PDF, habe ich 27 Beiträge gemacht. Daraus haben "
                "sich drei Frauen in meine Liste eingetragen. Für meinen Bio-Check, ein kleines Tool, das "
                "deine Instagram-Bio mit dir durchgeht, waren es elf Beiträge und neun Eintragungen."),
         absatz("Dasselbe Profil, dieselben Leute, dieselbe Frau, die es verschenkt. Der Unterschied war nur: "
                "Beim PDF bekommt man eine Datei, beim Tool ein Ergebnis, das sofort mit einem selbst zu tun hat."),
         absatz("Genau so ein Tool baust du dir im Tool-Workshop, zu dem Thema, das du im Nischengenerator "
                "gefunden hast. Am 10. November das Tool, am 11. November die Seite, auf der man sich dafür "
                "einträgt, beide Male um %s, mit Aufzeichnung." % UHR),
         knopf("Ich will mein eigenes Tool", KASSE),
         ps("P.S. Die Zahlen sind klein, weil mein Profil klein ist. Gerade deshalb zählt das Verhältnis: "
            "Mit einem Tool reicht dir eine kleinere Reichweite für dieselbe Zahl an Kontakten."),
         gruss("Herzlich,"),
     ]},
    {"datei": "C2-so-entsteht-es.html", "liste": 2, "name": "Nischengenerator C2 · So entsteht dein Tool (+3 Tage)",
     "marke": "mumlifebalance · Nischengenerator",
     "betreff": "Du beschreibst es, Claude baut es",
     "betreff2": "So entsteht dein Gratis-Tool an einem Abend",
     "wann": "Automation 2: 2 Tage nach C1",
     "preheader": "So entsteht dein Gratis-Tool an einem Abend.",
     "h1": "So entsteht dein Tool", "unterzeile": "Ein Abend, deine Worte, kein Code",
     "notiz": "Energie-Check ist das Beispiel-Tool aus dem Workshop-Mockup, kein Kundinnenfall.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("wenn du „Tool“ liest und an Programmieren denkst, verstehe ich das gut. Bevor ich meinen "
                "ersten Check gebaut habe, ging es mir genauso."),
         absatz("In Wahrheit beschreibst du nur, was du sonst am Küchentisch erklärst, wenn dich jemand nach "
                "deinem Thema fragt: welche Fragen du stellst, worauf du bei den Antworten achtest und was du "
                "am Schluss rätst. Den Rest schreibt Claude."),
         liste("Am Beispiel eines Energie-Checks für den Familienalltag", [
             "<strong>Deine Fragen:</strong> Wie startest du in den Tag? Wann kommt dein Tief? Was machst du dann?",
             "<strong>Deine Auswertung:</strong> drei Typen mit je einem Tipp aus deiner eigenen Erfahrung",
             "<strong>Dein Schluss:</strong> ein Satz zu dir und ein Knopf, über den man mit dir ins Gespräch kommt",
         ]),
         absatz("Im Workshop gehen wir genau diese drei Teile zusammen durch, zu deinem eigenen Thema. "
                "Wer hängen bleibt, bekommt in den drei Tagen danach in der Gruppe Hilfe, bis das Tool online ist."),
         knopf("Zum Tool-Workshop, 39 Franken oder 39 Euro", KASSE),
         ps("P.S. Hast du ein Workbook oder ein PDF zu deinem Thema? Bring es mit. Daraus wird das Wissen "
            "in deinem Tool."),
         gruss("Herzlich,"),
     ]},
    {"datei": "C3-tueroeffner.html", "liste": 2, "name": "Nischengenerator C3 · Der Türöffner (+5 Tage)",
     "marke": "mumlifebalance · Nischengenerator",
     "betreff": "Die Liste, die ich für meinen Mann geschrieben habe",
     "betreff2": "Wie mein Network-Produkt erst über ein anderes Angebot ins Gespräch kam",
     "wann": "Automation 2: 2 Tage nach C2",
     "preheader": "Und warum meine Öle erst danach zur Sprache kamen.",
     "h1": "Der Türöffner", "unterzeile": "Eine Liste, 30 Bestellungen, viele neue Gespräche",
     "notiz": "Patricias Ursprungsgeschichte (Memory reference_hybridmodell-ursprungsgeschichte, 21.09.2026).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("vor der Geburt meiner dritten Tochter habe ich meinem Mann eine Liste geschrieben, mit allem, "
                "was ich als Mama nebenbei erledige. Damit er weiss, was läuft, wenn ich im Spital bin."),
         absatz("Mit dieser Liste habe ich danach meinen Alltag so umgebaut, dass alles aufgeht und Zeit für "
                "mich bleibt. Daraus wurde mein Angebot „Die 3 Schritte, um deine To-do-Liste zu halbieren“, "
                "mit 30 Bestellungen in zwei Tagen."),
         absatz("Das Spannende kam danach. Über dieses Angebot kam ich mit Mamas ins Gespräch, die ich vorher "
                "nicht kannte, und irgendwann haben sie gefragt, was ich sonst noch mache. Erst dann kamen meine "
                "Öle zur Sprache, als Teil der Lösung und nicht als Aufhänger."),
         absatz("Genau diese Rolle bekommt dein Gratis-Tool. Es öffnet die Tür zu Leuten, die dich noch nicht "
                "kennen, und dein Network-Produkt bekommt danach seinen Platz, ohne dass du es jemandem "
                "aufdrängen musst."),
         knopf("Ich baue mir meinen Türöffner", KASSE),
         ps("P.S. Der Workshop ist live am 10. und 11. November um %s. Die Anmeldung ist offen bis "
            "Montag, 9. November, 23:59." % UHR),
         gruss("Herzlich,"),
     ]},
    {"datei": "C4-schon-so-viel.html", "liste": 2, "name": "Nischengenerator C4 · Schon so viel probiert (+7 Tage)",
     "marke": "mumlifebalance · Nischengenerator",
     "betreff": "„Ich hab schon so viel probiert“",
     "betreff2": "Wenn du Angst hast, dass es wieder nichts bringt",
     "wann": "Automation 2: 2 Tage nach C3",
     "preheader": "Wenn du Angst hast, dass es wieder nichts bringt.",
     "h1": "Wenn schon so viel nichts gebracht hat", "unterzeile": "Ein ehrliches Wort vor dem Workshop",
     "notiz": "Einwand aus ZIELGRUPPE.md (D3b: Angst vor dem nächsten Fehlschlag). Patricias eigener Weg.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("vielleicht denkst du gerade: Schon wieder etwas, das ich lernen soll, und am Ende bringt es "
                "doch nichts. Den Gedanken kenne ich von mir selbst."),
         absatz("Ich habe mein erstes Network aufgegeben, und danach habe ich zwei Jahre lang Programme gebaut, "
                "die niemand gekauft hat. Mir hat damals kein Wissen gefehlt. Mir hat gefehlt, dass am Ende "
                "eines Abends etwas fertig ist, das andere benutzen."),
         absatz("Darum ist der Workshop so gebaut: zwei Abende, an denen du mitbaust, statt nur zuzuhören. "
                "Wenn wir am 11. November auflegen, hast du ein Tool und eine Seite. Und in den drei Tagen "
                "danach helfe ich dir in der Gruppe, bis beides online ist."),
         liste("Das bekommst du für 39 Franken oder 39 Euro", [
             "Zwei Live-Abende, 10. und 11. November, %s, mit Aufzeichnung" % UHR,
             "Dein eigenes Gratis-Tool zu deinem Thema und die Seite, auf der man sich dafür einträgt",
             "Drei Tage Begleitung in der Gruppe",
             "Die Auftrags-Vorlage für Claude und die Seitenvorlage",
         ]),
         knopf("Ich bin dabei", KASSE),
         ps("P.S. Wenn du unsicher bist, ob es für dich passt, antworte einfach auf diese Mail. Ich lese "
            "und beantworte jede selbst."),
         gruss("Herzlich,"),
     ]},
    # ---- Nach dem Workshop → Digitale Produktwelt: Pitch-Serie (Automation 1 nach B2) ----------
    # Julia: nach dem kleinen Kauf fünf Mails auf EIN grosses Angebot. Die Produktwelt ist Evergreen
    # (Patricia 29.10.), darum ohne Frist. Pitch erst, wenn der Workshop ein neues Problem geschaffen hat.
    {"datei": "B3-und-jetzt.html", "liste": 16, "name": "Tool-Workshop B3 · Dein Tool läuft (Sa 14.11.)",
     "marke": "Tool-Workshop · Und jetzt?",
     "betreff": "Dein Tool steht. Was gibst du den Leuten danach?",
     "betreff2": "Wenn die ersten Leute dein Tool ausfüllen",
     "wann": "Automation 1: warten bis Sa 14.11.2026 09:00",
     "preheader": "Wenn die ersten Leute dein Tool ausfüllen.",
     "h1": "Dein Tool steht", "unterzeile": "Und jetzt kommt die nächste Frage",
     "notiz": "Startet die Produktwelt-Serie B3–B7 (Patricia 29.10.: Pitch-Mails nach Julia).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("du hast an zwei Abenden an deinem Tool und deiner Seite gebaut, und vielleicht ist beides schon "
                "online. Darauf darfst du stolz sein, das schaffen die wenigsten."),
         absatz("Sobald die ersten Leute dein Tool ausfüllen, kommt meistens eine neue Frage: Was mache ich "
                "jetzt mit den Kontakten? Sie haben ein Ergebnis bekommen, sie kennen dich jetzt ein bisschen, "
                "und manche wollen mehr von dir. Wenn es dann nur dein Network-Produkt gibt, fühlt sich jedes "
                "Gespräch schnell nach Verkauf an."),
         liste("Wie es nach einem Gratis-Tool weitergehen kann", [
             "<strong>Das Tool</strong> bringt die Leute zu dir und gibt ihnen ein erstes Ergebnis",
             "<strong>Ein kleines eigenes Angebot</strong>, zum Beispiel ein Workbook oder ein Minikurs, "
             "löst den nächsten Schritt",
             "<strong>Dein Network-Produkt</strong> kommt dort zur Sprache, wo es wirklich hilft",
         ]),
         absatz("In den nächsten Tagen zeige ich dir, wie das bei mir aussieht und wie du dein erstes "
                "eigenes Angebot baust. Für heute: Schick dein Tool drei Menschen, die dein Thema betrifft, "
                "und frag sie, was sie sich als Nächstes von dir wünschen würden."),
         ps("P.S. Antworte mir gern mit dem Link zu deinem Tool. Ich schaue es mir an."),
         gruss("Herzlich,"),
     ]},
    {"datei": "B4-das-erste-eigene.html", "liste": 16, "name": "Tool-Workshop B4 · Dein erstes eigenes Angebot (Mo 16.11.)",
     "marke": "Tool-Workshop · Und jetzt?",
     "betreff": "„Meine Kunden waren ich und ein paar Bekannte“",
     "betreff2": "Warum ein eigenes Angebot neue Leute bringt",
     "wann": "Automation 1: warten bis Mo 16.11.2026 09:00",
     "preheader": "So hat es eine Networkerin über ihr erstes Jahr geschrieben.",
     "h1": "Das erste eigene Angebot", "unterzeile": "Warum es neue Leute bringt",
     "notiz": "Zitat aus outputs/marktrecherche/2026-10-04-zielgruppe-ausserhalb-instagram.md (schreibfluss.net).",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("eine Networkerin hat in ihrem Blog über ihr erstes Jahr geschrieben: „Die ersten Monate "
                "beschränkten sich meine Kunden auf mich, ein Familienmitglied und ein paar Bekannte.“ "
                "Ich glaube, viele kennen genau diesen Satz."),
         absatz("Mit einem Produkt, das alle in deiner Firma gleich anbieten, erreichst du vor allem die Menschen, "
                "die dich schon kennen. Ein eigenes Angebot zu deinem Thema bringt dich zu Leuten, die nach "
                "einer Lösung suchen und dich noch nie gesehen haben. Dein Tool ist der erste Schritt dahin."),
         absatz("Bei mir war es ein kleines Angebot zum Thema To-do-Liste, und darüber kamen Mamas zu mir, die "
                "ich vorher nicht kannte. Meine Öle kamen erst später im Gespräch dazu."),
         absatz("Wie du so ein Angebot aus deinem Network-Wissen baust, Schritt für Schritt, zeige ich dir in "
                "der Digitalen Produktwelt. Morgen erzähle ich dir mehr darüber, heute nur so viel: Du fängst "
                "dafür nicht bei null an. Das Thema hast du, das erste Tool auch."),
         knopf("Zur Digitalen Produktwelt", KASSE_DPW),
         gruss("Herzlich,"),
     ]},
    {"datei": "B5-produktwelt.html", "liste": 16, "name": "Tool-Workshop B5 · Die Digitale Produktwelt (Mi 18.11.)",
     "marke": "Tool-Workshop · Und jetzt?",
     "betreff": "Vom Tool zu deinem ersten eigenen Produkt",
     "betreff2": "Was du in der Digitalen Produktwelt baust",
     "wann": "Automation 1: warten bis Mi 18.11.2026 09:00",
     "preheader": "Was du in der Digitalen Produktwelt baust, und für wen sie ist.",
     "h1": "Vom Tool zum eigenen Produkt", "unterzeile": "Die Digitale Produktwelt",
     "notiz": "Inhalt nach der Kasse /digitale-produktwelt/ (Stand 29.10.), Preis 333 oder 2× 166.50 CHF. Veränderung statt Modulzahlen.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("heute erzähle ich dir, was nach deinem Tool kommen kann. In der Digitalen Produktwelt baust "
                "du aus deinem Network-Wissen dein erstes eigenes Produkt, und zwar so, dass es neben deinem "
                "Network läuft und dein Network-Produkt darin seinen Platz hat."),
         liste("Was danach bei dir anders ist", [
             "Du weisst, welches Produkt zu deinem Thema und deinem Alltag passt",
             "Du baust es mit KI und Canva, als Kurs, Workbook oder Workshop, in der Stunde nach dem Ins-Bett-Bringen",
             "Du hast eine Treppe vom Gratis-Tool über dein Produkt bis zu deinem Network",
             "Du verkaufst über Storys, Mails und eine Kasse, ohne wie eine Verkäuferin zu klingen",
         ]),
         absatz("Dazu gibt es Vorlagen und Arbeitsblätter, und in der Telegram-Gruppe beantworte ich deine "
                "Fragen jeden Dienstag und Donnerstag. Den Kurs hast du ohne Ablaufdatum."),
         absatz("<strong>Das ist nicht dabei:</strong> Teamaufbau oder Tipps zum Rekrutieren. Es geht um "
                "etwas, das dir gehört, neben deinem Network."),
         absatz("Die Digitale Produktwelt kostet 333 Franken, oder zweimal 166.50 in Raten."),
         knopf("Ich baue mein erstes Produkt", KASSE_DPW),
         ps("P.S. Ich arbeite am liebsten mit Frauen, die umsetzen und mir Rückmeldung geben. Wenn du "
            "unsicher bist, ob du dazugehörst, antworte auf diese Mail."),
         gruss("Herzlich,"),
     ]},
    {"datei": "B6-network-produkt.html", "liste": 16, "name": "Tool-Workshop B6 · Ich hab doch mein Network-Produkt (Fr 20.11.)",
     "marke": "Tool-Workshop · Und jetzt?",
     "betreff": "„Ich hab doch schon ein Produkt“",
     "betreff2": "Warum ein eigenes Produkt dein Network stärkt",
     "wann": "Automation 1: warten bis Fr 20.11.2026 09:00",
     "preheader": "Warum ein eigenes Produkt dein Network stärkt.",
     "h1": "Du hast doch schon ein Produkt", "unterzeile": "Ein Einwand, den ich gut kenne",
     "notiz": "Einwände aus ZIELGRUPPE.md: Network aufgeben, Upline, schon so viel probiert.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("vielleicht denkst du: Wozu ein eigenes Produkt? Ich hab doch schon eins, und das ist richtig gut."),
         absatz("Ja, und genau deshalb. Dein Network-Produkt ist gut, nur bieten es alle in deiner Firma an, "
                "zum selben Preis, mit denselben Bildern. Dein eigenes Angebot gibt es nur bei dir. Es macht "
                "dich zur Ansprechperson für dein Thema, und wer dir vertraut, fragt dich dann auch nach "
                "deinen Ölen, deinen Shakes oder deiner Pflege."),
         absatz("Du musst dafür nichts aufgeben. Dein Network bleibt, und deine Upline verliert nichts, wenn "
                "neue Leute über dein Angebot zu dir finden."),
         absatz("Und falls du denkst, du hättest schon zu viel probiert: Mir ging es genauso. Zwei Jahre lang "
                "habe ich Programme gebaut, die niemand kaufte. Erst als ich wusste, für wen ich baue und wie "
                "die Treppe dahinter aussieht, hat es angefangen zu laufen. Genau diesen Weg zeigt dir die "
                "Digitale Produktwelt."),
         knopf("Zur Digitalen Produktwelt", KASSE_DPW),
         gruss("Herzlich,"),
     ]},
    {"datei": "B7-letzte.html", "liste": 16, "name": "Tool-Workshop B7 · Zum Abschluss (So 22.11.)",
     "marke": "Tool-Workshop · Und jetzt?",
     "betreff": "Ich lass dich jetzt in Ruhe",
     "betreff2": "Ein letztes Wort zur Digitalen Produktwelt",
     "wann": "Automation 1: warten bis So 22.11.2026 18:00, danach Ende der Automation",
     "preheader": "Ein letztes Wort zur Digitalen Produktwelt.",
     "h1": "Ein letztes Wort", "unterzeile": "Danach lasse ich dich in Ruhe",
     "notiz": "Keine Frist: die Produktwelt ist Evergreen. Schreib-mir-Brücke statt Verknappung.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%,"),
         absatz("das ist meine letzte Mail zur Digitalen Produktwelt, danach lasse ich dich damit in Ruhe."),
         absatz("Du kannst dir alles auch selbst beibringen. Das geht, es braucht nur mehr Zeit und mehr "
                "Umwege. Die Produktwelt ist für dich, wenn du den Weg lieber mit einer klaren Reihenfolge "
                "gehst und mit jemandem, der deine Fragen beantwortet."),
         absatz("Du hast an zwei Abenden ein Tool gebaut. Mit deinem ersten Produkt geht das genauso, wenn du "
                "weisst, was zu tun ist."),
         absatz("333 Franken, oder zweimal 166.50 in Raten."),
         knopf("Zur Digitalen Produktwelt", KASSE_DPW),
         ps("P.S. Wenn du eine Frage hast, bevor du dich entscheidest, antworte einfach auf diese Mail. "
            "Ich antworte dir selbst."),
         gruss("Herzlich,"),
     ]},
]


def als_text(html_text):
    t = re.sub(r"<!--.*?-->|<style.*?</style>", "", html_text, flags=re.S)
    t = re.sub(r"<br\s*/?>|</p>|</li>|</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    import html as h
    t = h.unescape(t)
    return re.sub(r"\n\s*\n+", "\n\n", re.sub(r"[ \t]+", " ", t)).strip()


def ac_zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        if "=" in z and not z.startswith("#"):
            k, v = z.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


def ac_v1(basis, schluessel, aktion, werte):
    url = "%s/admin/api.php?api_action=%s&api_key=%s&api_output=json" % (basis, aktion, schluessel)
    daten = urllib.parse.urlencode(werte).encode()
    antwort = json.load(urllib.request.urlopen(urllib.request.Request(url, data=daten, method="POST")))
    if antwort.get("result_code") != 1:
        raise RuntimeError("%s: %s" % (aktion, antwort.get("result_message")))
    return antwort


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    stand_datei = ZIEL / "ac-entwuerfe.json"
    stand = json.loads(stand_datei.read_text(encoding="utf-8")) if stand_datei.exists() else {}
    for m in MAILS:
        seite = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "TOOL-WORKSHOP").replace(
            "scripts/startklar/mails-bauen.py", "scripts/tool-workshop/mails-bauen.py")
        (ZIEL / m["datei"]).write_text(seite, encoding="utf-8")
        sk.umlaute_pruefen(m["datei"], seite)
        print("✓", m["datei"])
        if "--hochladen" in sys.argv:
            basis, schluessel = ac_zugang()
            if m["datei"] in stand:   # Entwurf gibt es schon: nur die Nachricht ersetzen, nichts doppelt anlegen
                nid = stand[m["datei"]]["nachricht"]
                daten = json.dumps({"message": {"html": seite, "text": als_text(seite), "subject": m["betreff"]}}).encode()
                urllib.request.urlopen(urllib.request.Request("%s/api/3/messages/%s" % (basis, nid), data=daten, method="PUT",
                                       headers={"Api-Token": schluessel, "Content-Type": "application/json"})).read()
                zurueck = json.load(urllib.request.urlopen(urllib.request.Request(
                    "%s/api/3/messages/%s" % (basis, nid), headers={"Api-Token": schluessel})))["message"]
                assert (zurueck["html"] or "").strip() == seite.strip(), "AC hat Nachricht %s anders gespeichert" % nid
                print("   in AC aktualisiert: Nachricht", nid)
                continue
            absender = {"fromname": "Patricia Ulmann", "fromemail": "patricia@mumlifebalance.ch",
                        "reply2": "patricia@mumlifebalance.ch", "subject": m["betreff"]}
            msg = ac_v1(basis, schluessel, "message_add", dict(absender, format="html", htmlconstructor="external",
                        textconstructor="external", html=seite, text=als_text(seite), **{"p[%d]" % m["liste"]: m["liste"]}))
            kamp = ac_v1(basis, schluessel, "campaign_create", dict(absender, type="single", name=m["name"], sdate="",
                         status=0, public=0, tracklinks="all", **{"p[%d]" % m["liste"]: m["liste"], "m[%s]" % msg["id"]: 100}))
            stand[m["datei"]] = {"kampagne": kamp["id"], "nachricht": msg["id"], "name": m["name"]}
            stand_datei.write_text(json.dumps(stand, ensure_ascii=False, indent=1), encoding="utf-8")
            print("   AC-Entwurf: Kampagne", kamp["id"], "· Nachricht", msg["id"])


if __name__ == "__main__":
    main()
