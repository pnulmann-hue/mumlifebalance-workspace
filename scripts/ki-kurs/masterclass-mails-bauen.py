"""
Baut die Mails rund um die KI-Masterclass (Do 8.10.2026, 09:00) als fertige Mail-HTMLs.

Das Gerüst (Kopf, Farben, Fuss, Outlook-Tabellen, Umlaut-Wächter, Kopierseite)
kommt aus scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert.

  python scripts/ki-kurs/masterclass-mails-bauen.py

Ausgabe: outputs/produkte/ki-treppe/mails/  (je Mail ein HTML + index.html zum Kopieren)

Formular: ActiveCampaign 69 „0€ Anmeldung KI Webinar“, Tag „0€ KI Webinar“ (100),
Double-Opt-in an. Die Opt-in-Mail wird im Formular unter Optionen → Opt-in-Bestätigung
eingefügt; der Bestätigungsknopf muss den AC-Platzhalter %CONFIRMLINK% behalten.
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

ZIEL = ROOT / "outputs" / "produkte" / "ki-treppe" / "mails"
TERMIN = "Donnerstag, 8. Oktober, um 9 Uhr morgens"

absatz, kasten, knopf, ps, gruss = sk.absatz, sk.kasten, sk.knopf, sk.ps, sk.gruss

MAILS = [
    {
        "datei": "masterclass-00-optin.html", "tag": "0", "warten": "sofort nach dem Absenden (Double-Opt-in)",
        "marke": "KI-Masterclass",
        "betreff": "Ein Klick noch, dann bist du am Donnerstag dabei",
        "betreff2": "Bitte kurz bestätigen",
        "wann": "Opt-in-Bestätigung von Formular 69",
        "preheader": "Sonst kommt dein Zoom-Link nicht bei dir an.",
        "h1": "Ein Klick noch",
        "unterzeile": "Dann ist dein Platz am Donnerstagmorgen sicher.",
        "notiz": """In ActiveCampaign: Formular 69 → Optionen → Opt-in-Bestätigung → E-Mail bearbeiten.
🚨 Der Knopf zeigt auf %CONFIRMLINK% — das ist der Bestätigungslink von ActiveCampaign.
Steht im AC-Editor ein anderer Platzhalter im Standardtext, DEN nehmen.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("schön, dass du am <strong>%s</strong> dabei sein willst. Damit ich dir den "
                   "Zoom-Link und später die Aufzeichnung schicken darf, brauche ich noch einen "
                   "Klick von dir." % TERMIN),
            knopf("Ja, ich bin dabei", "%CONFIRMLINK%"),
            absatz("Sobald du geklickt hast, kommt die Mail mit dem Link, und am Mittwochabend "
                   "erinnere ich dich nochmal. Wenn du am Morgen nicht live dabei sein kannst, "
                   "bekommst du die Aufzeichnung am Donnerstag trotzdem noch."),
            gruss("Bis Donnerstag,"),
            ps("P.S. Falls du dich gar nicht angemeldet hast, kannst du diese Mail einfach "
               "ignorieren, dann passiert nichts."),
        ],
    },
    # ---------------------------------------------------------------- Stimm-Check
    {
        "datei": "stimm-00-optin.html", "tag": "0", "warten": "sofort nach dem Absenden (Double-Opt-in)",
        "marke": "Der Stimm-Check",
        "betreff": "Ein Klick noch, dann gehört dein Stimm-Check dir",
        "betreff2": "Bitte kurz bestätigen",
        "wann": "Opt-in-Bestätigung des Stimm-Check-Formulars",
        "preheader": "Danach kannst du sofort loslegen.",
        "h1": "Ein Klick noch",
        "unterzeile": "Dann kannst du mit deinem Stimm-Check loslegen.",
        "notiz": """In ActiveCampaign: Stimm-Check-Formular → Optionen → Opt-in-Bestätigung → E-Mail bearbeiten.
🚨 Der Knopf zeigt auf %CONFIRMLINK% — Bestätigungslink von ActiveCampaign.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("schön, dass du deinen Stimm-Check machen willst. Damit ich dir den Link und "
                   "ab und zu eine Mail mit Ideen rund um KI und dein Business schicken darf, "
                   "brauche ich noch einen Klick von dir."),
            knopf("Ja, ich will meinen Stimm-Check", "%CONFIRMLINK%"),
            absatz("Danach landest du direkt auf der Seite, auf der du loslegen kannst, und den "
                   "Link bekommst du zusätzlich per Mail, damit du ihn wiederfindest."),
            gruss("Bis gleich,"),
            ps("P.S. Falls du dich gar nicht angemeldet hast, kannst du diese Mail einfach "
               "ignorieren, dann passiert nichts."),
        ],
    },
    {
        "datei": "stimm-01-auslieferung.html", "tag": "0", "warten": "sofort nach der Bestätigung (Automation, Tag 0€ Stimmcheck)",
        "marke": "Der Stimm-Check",
        "betreff": "Dein Stimm-Check ist da",
        "betreff2": "Damit deine KI klingt wie du",
        "wann": "Automation „Stimm-Check“, Auslöser Tag „0€ Stimmcheck“ (105)",
        "preheader": "15 Minuten, und deine KI kennt dich.",
        "h1": "Dein Stimm-Check ist da",
        "unterzeile": "15 Minuten, und deine KI weiss, wer du bist und wie du klingst.",
        "notiz": """🚨 TOOL_URL steht noch auf Platzhalter, bis das Tool auf Vercel liegt.
Der Link trägt ?e=%EMAIL%&n=%FIRSTNAME% — damit begrüsst das Tool sie mit Namen.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("hier ist dein Stimm-Check. Hol dir vorher einen Text, den du selbst geschrieben "
                   "hast, eine Caption, eine Mail oder eine Sprachnachricht, die du abtippst. Daraus "
                   "liest der Stimm-Check, wie du wirklich klingst."),
            knopf("Stimm-Check starten", "{{TOOL_URL}}?e=%EMAIL%&n=%FIRSTNAME%"),
            absatz("Am Ende hast du deinen Stimm-Brief, den du ab jetzt vor jeden Auftrag an deine "
                   "KI kopierst, und einen ersten Text, den du so posten würdest."),
            kasten(sk.P_ENG % ("Am <strong>%s</strong> zeige ich dir live, was möglich ist, wenn deine "
                               "KI dich kennt und genau weiss, was zu tun ist: mein Cockpit, meine "
                               "Assistenten und wie ein Skill entsteht. Kostenlos, 45 Minuten über Zoom, "
                               "mit Aufzeichnung am selben Tag.<br>"
                               '<a href="%s" style="color:%s;font-weight:bold;">Platz für die Masterclass sichern</a>'
                               % (TERMIN, "https://mumlifebalance.activehosted.com/f/69", sk.PETROL)),
                   "#e4f3f4", rand=sk.PETROL, kopf="Live-Masterclass"),
            gruss("Viel Spass beim Ausprobieren,"),
            ps("P.S. Schreib mir gern, wie dein erster Text geworden ist. Ich lese jede Antwort."),
        ],
    },
    {
        # Wer ab dem 8.10. kommt, bekommt keine Einladung zu einem Termin, der vorbei ist.
        "datei": "stimm-01b-auslieferung.html", "tag": "0b",
        "warten": "sofort nach der Bestätigung · Zweig „ab dem 8.10.“",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "Dein Stimm-Check ist da",
        "betreff2": "Damit deine KI klingt wie du",
        "wann": "Automation „Stimm-Check“, gleich nach dem Auslöser Wenn/Dann: Datum ab 8.10. → diese Mail statt S1",
        "preheader": "15 Minuten, und deine KI kennt dich.",
        "h1": "Dein Stimm-Check ist da",
        "unterzeile": "15 Minuten, und deine KI weiss, wer du bist und wie du klingst.",
        "notiz": """Gleiche Auslieferung wie S1, nur ohne Einladung zur Live-Masterclass (der Termin ist vorbei).
Die Aufzeichnung kommt am nächsten Tag mit S2b.
🚨 TOOL_URL steht noch auf Platzhalter, bis das Tool auf Vercel liegt.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("hier ist dein Stimm-Check. Hol dir vorher einen Text, den du selbst geschrieben "
                   "hast, eine Caption, eine Mail oder eine Sprachnachricht, die du abtippst. Daraus "
                   "liest der Stimm-Check, wie du wirklich klingst."),
            knopf("Stimm-Check starten", "{{TOOL_URL}}?e=%EMAIL%&n=%FIRSTNAME%"),
            absatz("Am Ende hast du deinen Stimm-Brief, den du ab jetzt vor jeden Auftrag an deine "
                   "KI kopierst, und einen ersten Text, den du so posten würdest."),
            absatz("Morgen schicke ich dir noch die Aufzeichnung meiner Masterclass. Darin siehst du, "
                   "was möglich wird, wenn deine KI dich kennt und dazu weiss, was zu tun ist: mein "
                   "Cockpit, meine Assistenten und wie ein Skill entsteht."),
            gruss("Viel Spass beim Ausprobieren,"),
            ps("P.S. Schreib mir gern, wie dein erster Text geworden ist. Ich lese jede Antwort."),
        ],
    },
]

TOOL_URL = "https://stimm-check.vercel.app/"   # Stimm-Check-Tool auf Vercel (live seit 26.09.2026)

# 🚨 Offene Adressen — bis sie stehen, zeigen die Knöpfe auf einen Platzhalter mit '#'
KURS_URL = "https://mumlifebalance.ch/ki-kurs/"   # Verkaufsseite KI-Kurs (WP 4286, bis zum Launch Entwurf)
ZOOM_URL = "https://us06web.zoom.us/j/89774712326?pwd=biw9afsJ0tCnuj3b2NKa71u4yMr0c2.1"   # Zoom-Raum Masterclass 8.10.
AUFZEICHNUNG_URL = "#aufzeichnung-folgt"
MC_SEITE = "https://mumlifebalance.ch/ki-masterclass/"
MBA_PS = ("Bist du in der Mum Business Academy? Dann hast du den Kurs schon, er kommt ab dem "
          "1. November in deinen Bereich, ohne dass du etwas zahlst.")
h2, liste, merken = sk.h2, sk.liste, sk.merken

# ======================================================================
# Newsletter an die ganze Liste — Einladung 1 (Di 29.9. 07:00)
# ======================================================================
MAILS += [
    {
        "datei": "newsletter-01-einladung.html", "tag": "N1", "warten": "Kampagne an die ganze Newsletter-Liste",
        "strecke": "newsletter", "marke": "Mum Life Balance",
        "betreff": "Warum deine KI-Texte nach niemandem klingen",
        "betreff2": "Wie oft hast du deiner KI dieses Jahr schon erklärt, wer du bist?",
        "wann": "Di 29.9. 07:00 · Newsletter + Interessenten (Liste 2), Käuferinnen des KI-Kurses ausschliessen",
        "preheader": "Und was ich dir am Donnerstag, 8. Oktober, live zeige.",
        "h1": "Warum deine KI-Texte nach niemandem klingen",
        "unterzeile": "Es liegt nicht an dir, und es liegt auch nicht an der KI.",
        "notiz": "Einladung 1 von 3 (drei Einladungen vor dem Live-Termin). Link auf /ki-masterclass/, P.S. Stimm-Check.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("kennst du das? Du tippst in ChatGPT oder Claude, worum es geht und für wen der Text ist, "
                   "und zurück kommt etwas, das glatt klingt und nach irgendwem, nur nicht nach dir. Also baust "
                   "du ihn um, Satz für Satz, und hättest ihn fast schneller selbst geschrieben."),
            absatz("Das liegt weder an dir noch an der KI. Ihr fehlen zwei Dinge."),
            liste("Was deine KI braucht", [
                "<strong>Sie muss dich kennen.</strong> Wer du bist, für wen du schreibst, was du anbietest und "
                "wie du klingst, einmal sauber festgehalten statt jedes Mal neu erklärt.",
                "<strong>Sie muss wissen, was zu tun ist.</strong> Die Arbeit, die du jede Woche wieder machst, "
                "steht einmal als Auftrag da, und dann sagst du nur noch „mach die Caption für Mittwoch“.",
            ]),
            absatz("Genau das zeige ich dir live am <strong>%s</strong>: mein Cockpit, in dem meine ganze "
                   "Content-Woche vorbereitet liegt, meine Assistenten, wie ein Skill entsteht, und den Bot, "
                   "der mir die Menüplanung abnimmt. Für die habe ich früher ein, zwei Stunden gebraucht, heute "
                   "sind es fünf Minuten." % TERMIN),
            knopf("Platz für die Masterclass sichern", MC_SEITE),
            absatz("Die Masterclass ist kostenlos, dauert rund 45 Minuten, und die Aufzeichnung bekommst du am "
                   "selben Tag, auch wenn du am Morgen nicht kannst.", True),
            gruss("Ich freu mich auf dich,"),
            ps('P.S. Wenn du bis dahin schon anfangen willst: Im <a href="https://mumlifebalance.ch/stimm-check/" '
               'style="color:%s;">Stimm-Check</a> sammelst du in rund 15 Minuten die sechs Angaben, die deine KI '
               'von dir braucht. Kostenlos, und du bringst am Donnerstag schon deinen eigenen Brief mit.' % sk.PETROL),
        ],
    },
    {
        # Einladung 2: anderer Angle als N1 (dort Schmerz „klingt nach niemandem“) —
        # hier Beweis aus dem Alltag, mit dem Kochbot als Szene, die jede Mama kennt.
        "datei": "newsletter-02-einladung.html", "tag": "N2", "warten": "Kampagne an die ganze Newsletter-Liste",
        "strecke": "newsletter", "marke": "Mum Life Balance",
        # Überarbeitet 02.10.2026 mit /copywriting + Patricias eigenem Absatz (Menüplanung →
        # Haushalt → CEO der Familie). Vorher: 37 von 172 geöffnet, 2 Klicks bei N1.
        "betreff": "Was würdest du als Erstes abgeben?",
        "betreff2": "Menüplanung in fünf Minuten, und was sonst noch geht",
        "wann": "Mo 5.10. 07:00 · Newsletter + Interessenten (Liste 2) + Kunden (Liste 16), "
                "ohne Tag „0€ KI Webinar“ (100), ohne KI-Käuferinnen, ohne doTERRA-Listen",
        "preheader": "Und warum meine KI auch an die Bügelstation denkt.",
        "h1": "Was würdest du als Erstes abgeben?",
        "unterzeile": "Bei mir war es die Menüplanung.",
        "notiz": "Einladung 2 von 3. 🚨 Wer sich schon angemeldet hat (Tag 100), bekommt sie nicht — "
                 "im Kampagnen-Segment ausschliessen.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%,"),
            absatz("was würdest du als Erstes abgeben, wenn jemand die Arbeit übernimmt, die jede Woche "
                   "gleich aussieht? Bei mir war es die Menüplanung."),
            absatz("Früher habe ich dafür ein, zwei Stunden gebraucht, mit Überlegen, Rezepte "
                   "zusammensuchen und Einkaufsliste schreiben. Heute beantworte ich drei Fragen – ist "
                   "nächste Woche etwas Besonderes, kommt Besuch, muss im Kühlschrank etwas weg – und ein "
                   "paar Minuten später liegen Menü und Einkaufsliste aus meinen eigenen Rezepten auf dem "
                   "Handy. Kochen muss ich allerdings immer noch selbst."),
            absatz("Wenn du jetzt denkst „häää, was hat meine Menüplanung mit meinem Business zu tun?“, "
                   "dann: ganz viel. Du bist ja auch Mama, und als Mama musst du irgendwie alles "
                   "gleichzeitig unter einen Hut kriegen. Deshalb habe ich mich irgendwann gefragt, warum "
                   "ich die KI eigentlich nur für Businessthemen nutzen soll."),
            absatz("So kam der Koch-Helfer dazu, und danach eine Übersicht für den Haushalt, die ich mir "
                   "mit Claude gebaut habe. Da steht jeden Tag drin, was zu erledigen ist, damit nichts "
                   "vergessen geht, bis hin zum Entkalken meiner Bügelstation. Das würde ich mit meinen "
                   "1000 offenen Tabs im Kopf garantiert vergessen 😃"),
            absatz("Du bist CEO deines Business, aber auch CEO deiner Familie, und Planung gehört für "
                   "mich zu beidem."),
            absatz("Natürlich helfen mir meine KI-Helfer auch im Business. Sie sortieren meine Mails, "
                   "machen jede Woche automatisch eine Marktanalyse, planen meinen Content mit, und so "
                   "weiter und so fort. Ich arbeite rund 18 Stunden die Woche, neben vier Kindern und "
                   "zwei Instagram-Kanälen. Ich prüfe, gebe frei, und der Rest läuft."),
            absatz("Am <strong>%s</strong> zeige ich dir das live, und zwar so, dass du danach weisst, "
                   "wo du bei dir anfangen würdest." % TERMIN),
            liste("Was du am Donnerstag mitnimmst", [
                "welche zwei Dinge deine KI von dir braucht, damit ihre Texte nach dir klingen",
                "wie aus einer Arbeit, die du jede Woche machst, ein fester Auftrag wird, den du nie "
                "mehr neu erklären musst",
                "meinen Koch-Helfer in Aktion, damit du siehst, dass das ohne Technik-Kenntnisse geht",
            ]),
            knopf("Platz für Donnerstag sichern", MC_SEITE),
            absatz("Kostenlos, rund 45 Minuten über Zoom. Und falls bei dir gerade Ferien sind und der "
                   "Morgen nicht passt: Die Aufzeichnung kommt am Donnerstagnachmittag zu allen, die sich "
                   "angemeldet haben.", True),
            gruss("Ich freu mich auf dich,"),
            ps("P.S. Schreib mir gern zurück, welche Arbeit du am liebsten als Erstes abgeben würdest. "
               "Ich lese jede Antwort, und vielleicht zeige ich genau die am Donnerstag."),
        ],
    },
    {
        # Einladung 3: letzte vor dem Termin. Angle Identität und Einwand „ich bin
        # keine Technikerin“ — der häufigste Grund, sich nicht anzumelden.
        "datei": "newsletter-03-einladung.html", "tag": "N3", "warten": "Kampagne an die ganze Newsletter-Liste",
        "strecke": "newsletter", "marke": "Mum Life Balance",
        "betreff": "Welcher Prompt war das nochmal?",
        # Überarbeitet 02.10.2026: Einstieg ist Patricias eigene Szene (altes ChatGPT durchgescrollt).
        "betreff2": "Wo war nochmal diese geniale Idee?",
        "wann": "Mi 7.10. 07:00 · Newsletter + Interessenten (Liste 2) + Kunden (Liste 16), "
                "ohne Tag „0€ KI Webinar“ (100), ohne KI-Käuferinnen, ohne doTERRA-Listen",
        "preheader": "Morgen um neun zeige ich dir, wie du nie mehr danach suchst.",
        "h1": "Welcher Prompt war das nochmal?",
        "unterzeile": "Morgen um neun zeige ich dir, wie du nie mehr danach suchst.",
        "notiz": "Einladung 3 von 3, am Tag vor dem Termin. 🚨 Angemeldete (Tag 100) ausschliessen.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%,"),
            absatz("letztens habe ich mein altes ChatGPT geöffnet und aus Neugier durch die Chats gescrollt. "
                   "Mann, war DAS ein Chaos. Unendlich viele Chats mit unendlich vielen Anfragen und "
                   "unendlich langen Prompts, weil ich der KI jedes Mal wieder sagen musste, wer ich bin, "
                   "was ich mache und für wen."),
            absatz("Und ich weiss noch, als wäre es gestern gewesen: Da war dieser Gedanke „letztens habe "
                   "ich doch mit ChatGPT so eine geile Idee ausgearbeitet“. Kopiert hast du sie natürlich "
                   "nicht, also suchst du, suchst und suchst und ärgerst dich. Kennst du bestimmt auch."),
            absatz("Irgendwann habe ich es anders gemacht. Ich habe einmal sauber aufgeschrieben, wer ich "
                   "bin, für wen ich schreibe und wie ich klinge, und jede Arbeit, die immer wiederkommt, "
                   "als festen Auftrag abgelegt. Seitdem fange ich nicht mehr bei null an. Ein Satz wie "
                   "„mach mir die Caption für Mittwoch“ reicht, und die KI weiss, was das bei mir heisst."),
            absatz("Genau das zeige ich dir <strong>morgen, am %s</strong>, live." % TERMIN),
            absatz("Falls du gerade denkst, das sei nur etwas für Technik-Leute: Ich komme aus dem "
                   "Sozialbereich, und am Donnerstag wird nichts programmiert. Du musst nichts installieren "
                   "und nichts mitschreiben, du schaust einfach zu. Ob du heute mit ChatGPT oder mit Claude "
                   "arbeitest, spielt keine Rolle (ich arbeite hauptsächlich mit Claude, das Prinzip ist "
                   "dasselbe). Und falls der Morgen nicht passt, kommt die Aufzeichnung am "
                   "Donnerstagnachmittag."),
            knopf("Ich bin morgen dabei", MC_SEITE),
            absatz("Kostenlos und rund 45 Minuten. Am Ende erzähle ich, wie du dir das selbst aufbauen "
                   "kannst, wenn du willst. Wer nur zuschauen will, schaut nur zu.", True),
            gruss("Bis morgen, hoffe ich,"),
            ps("P.S. Das ist meine letzte Einladung. Heute Abend kommt für alle Angemeldeten die "
               "Erinnerung mit dem Zoom-Link, und morgen um neun geht's los."),
        ],
    },
]

# ======================================================================
# Strecke „0€ KI Webinar“ — nach der Anmeldung zur Masterclass
# ======================================================================
MAILS += [
    {
        "datei": "masterclass-01-bestaetigung.html", "tag": "M1", "warten": "sofort nach der Bestätigung",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Du bist dabei: Donnerstag, 8. Oktober, 9 Uhr",
        "betreff2": "Dein Zoom-Link für die Masterclass",
        "wann": "Automation „0€ KI Webinar“, Schritt 1, sofort",
        "preheader": "Hier ist dein Zoom-Link, und eine kleine Vorbereitung, wenn du magst.",
        "h1": "Du bist dabei!",
        "unterzeile": "Donnerstag, 8. Oktober, um 9 Uhr, rund 45 Minuten über Zoom.",
        "notiz": "🚨 ZOOM_URL eintragen, bevor die Automation aktiv wird.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("schön, dass du dabei bist. Am <strong>%s</strong> zeig ich dir live, wie meine KI "
                   "mitarbeitet, ohne dass ich ihr jede Woche wieder alles erklären muss." % TERMIN),
            knopf("Zum Zoom-Raum", ZOOM_URL),
            absatz("Speicher dir den Link am besten gleich ab oder trag ihn in deinen Kalender ein. Am Mittwochabend "
                   "schicke ich ihn dir nochmal, und am Donnerstag kurz vor neun auch."),
            kasten(sk.P_ENG % ('Wenn du magst, mach vorher den <a href="https://mumlifebalance.ch/stimm-check/" '
                               'style="color:%s;font-weight:bold;">Stimm-Check</a>. In rund 15 Minuten hast du die '
                               'sechs Angaben, die deine KI von dir braucht, und am Donnerstag siehst du, was man '
                               'damit alles machen kann.' % sk.PETROL),
                   "#e4f3f4", rand=sk.PETROL, kopf="Kleine Vorbereitung"),
            gruss("Bis Donnerstag,"),
            ps("P.S. Du kannst am Morgen nicht? Kein Problem, die Aufzeichnung bekommst du am Donnerstagnachmittag."),
        ],
    },
    {
        "datei": "masterclass-02-erinnerung.html", "tag": "M2", "warten": "warten bis Mi 7.10. 19:00",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Morgen um neun",
        "betreff2": "Morgen zeig ich dir mein Cockpit",
        "wann": "Automation „0€ KI Webinar“, warten bis Mi 7.10. 19:00",
        "preheader": "Der Zoom-Link für morgen früh, und was du sehen wirst.",
        "h1": "Morgen um neun",
        "unterzeile": "Du schaust einfach zu, mitschreiben musst du nichts.",
        "notiz": "",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("morgen um neun ist es so weit. Ich zeige dir, was in meinen rund 18 Stunden pro Woche "
                   "alles drinsteckt: jeden Tag Story und Feed auf zwei Kanälen, jeden Monat ein kostenloses und "
                   "ein bezahltes Produkt, mein Network und die ganze Administration, mit vier Kindern daneben. "
                   "Das geht nur, weil meine KI-Assistenten mitarbeiten, und genau die schauen wir uns an."),
            knopf("Zum Zoom-Raum", ZOOM_URL),
            absatz("Kamera an oder aus, wie es dir passt. Und wenn dir heute Abend eine Frage einfällt, "
                   "antworte mir einfach auf diese Mail, dann nehme ich sie morgen mit."),
            gruss("Bis morgen,"),
            ps("P.S. Wenn es morgen früh nicht klappt, bekommst du die Aufzeichnung am Nachmittag."),
        ],
    },
    {
        "datei": "masterclass-03-live.html", "tag": "M3", "warten": "warten bis Do 8.10. 08:55",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Wir sind gleich live",
        "betreff2": "In fünf Minuten geht's los",
        "wann": "Automation „0€ KI Webinar“, warten bis Do 8.10. 08:55",
        "preheader": "Hier ist dein Link, komm einfach rein.",
        "h1": "In fünf Minuten geht's los",
        "unterzeile": "Hol dir einen Kaffee und komm rein.",
        "notiz": "",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("in fünf Minuten starten wir. Hol dir einen Kaffee, und komm einfach rein, auch wenn du ein "
                   "paar Minuten später dran bist."),
            knopf("Jetzt in den Zoom-Raum", ZOOM_URL),
            gruss("Bis gleich,"),
            ps("P.S. Die Aufzeichnung kommt heute Nachmittag, falls du doch nicht kannst."),
        ],
    },
    {
        "datei": "masterclass-04-aufzeichnung.html", "tag": "M4", "warten": "warten bis Do 8.10. 16:00",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Die Aufzeichnung, und was nur bis Samstagabend gilt",
        "betreff2": "Das Wichtigste von heute Morgen",
        "wann": "Automation „0€ KI Webinar“, warten bis Do 8.10. 16:00 · an alle Angemeldeten, auch wer nicht live war",
        "preheader": "Das Wichtigste von heute Morgen in zwei Sätzen, und mein Angebot.",
        "h1": "Das Wichtigste von heute Morgen",
        "unterzeile": "Mit der Aufzeichnung und meinem Angebot für dich.",
        "notiz": """Pitch 1 von 3: Zusammenfassung + Angebot. 🚨 AUFZEICHNUNG_URL + KURS_URL eintragen.
Bonus bis Sa 10.10. 21:00 (48 h nach dem Live-Termin): dritter Call, Bonus-Call Do 21.1.2027 (derselbe wie beim Secret Offer).""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("danke, dass du heute dabei warst oder dir die Zeit nimmst, es nachzuschauen. Hier ist die "
                   "Aufzeichnung:"),
            knopf("Zur Aufzeichnung", AUFZEICHNUNG_URL),
            absatz("Wenn du nur eine Sache mitnimmst, dann diese: <strong>Deine KI muss dich kennen, und sie muss "
                   "wissen, was zu tun ist.</strong> Solange eins davon fehlt, fängst du jede Woche wieder bei null "
                   "an, und genau das kostet dich die Zeit, die dir die KI eigentlich sparen sollte."),
            h2("Wenn du das bei dir einrichten willst"),
            absatz("Im Kurs <strong>„Easy KI für Networkerinnen — vom Chat zur Mitarbeiterin“</strong> richtest "
                   "du dir genau das Schritt für Schritt ein, in deinem eigenen Tempo:"),
            liste("Was du am Ende hast", [
                "<strong>Einen Arbeitsplatz mit deinem Wissen drin</strong>, den deine KI bei jedem Auftrag liest",
                "<strong>Deinen ersten eigenen Skill</strong> für eine Arbeit, die du jede Woche wieder machst",
                "<strong>Einen Bot, der von selbst läuft</strong>, so wie mein Kochbot oder mein Cockpit-Bot",
            ]),
            absatz("Du fängst im Chat an, den du schon kennst, und installierst erst später etwas. Die Kapitel "
                   "kommen ab dem 1. November Woche für Woche, und am 30. November ist der Kurs komplett."),
            kasten(sk.P_ENG % ("Wenn du bis <strong>Samstag, 10. Oktober, 21 Uhr</strong> einsteigst, bist du "
                               "zusätzlich beim <strong>Bonus-Call am 21. Januar</strong> dabei. Dann hast du alles "
                               "ausprobiert, und wir gehen zusammen durch, was bei dir läuft und was noch hakt. Das ist "
                               "ein dritter Live-Call zu den zwei, die ohnehin im Kurs sind. Der Frühbucherpreis von 277 "
                               "gilt bis Donnerstag, 15. Oktober."),
                   "#fdf1e6", rand=sk.ORANGE, kopf="Nur für dich als Teilnehmerin", kopffarbe=sk.ORANGE),
            knopf("Alles zum Kurs", KURS_URL),
            gruss("Danke, dass du dabei warst,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "masterclass-05-beweis.html", "tag": "M5", "warten": "warten bis Fr 9.10. 07:00",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Was in meinen 18 Stunden drinsteckt",
        "betreff2": "Ehrlich: so sieht meine Woche aus",
        "wann": "Automation „0€ KI Webinar“, warten bis Fr 9.10. 07:00 · nur wer noch nicht gekauft hat",
        "preheader": "Und warum das ohne KI nie gegangen wäre.",
        "h1": "Was in meinen 18 Stunden drinsteckt",
        "unterzeile": "Mit vier Kindern daneben, und ohne dass ich abends noch am Handy sitze.",
        "notiz": """Pitch 2 von 3: Beweis (Kundenstimmen gibt es noch keine, deshalb Patricias eigene Zahlen).
✏️ Absatz mit der Frage aus dem Live: nur mit einer Frage, die wirklich gestellt wurde, sonst streichen.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("für mein ganzes Business bleiben mir rund 18 Stunden in der Woche. Darin stecken jeden Tag "
                   "Story und Feed auf zwei Kanälen, jeden Monat ein kostenloses und ein bezahltes Produkt, mein "
                   "Network mit der Betreuung meiner Kundinnen und meines Teams, und die ganze Administration."),
            absatz("Ohne meine 13 KI-Assistenten ginge das nicht. Jeder davon nimmt mir eine Arbeit ab, die ich früher jede Woche von "
                   "Hand gemacht habe, und der kleinste ist der Kochbot: drei Fragen am Sonntag, und Menüplan und "
                   "Einkaufsliste kommen fertig aufs Handy."),
            absatz("✏️ <em>[Eine Frage aus der Masterclass und deine Antwort, nur wenn sie wirklich gestellt "
                   "wurde, sonst diesen Absatz löschen.]</em>"),
            absatz("Im Kurs baust du dir deinen eigenen Anfang davon. Du musst nicht gleich 13 Assistenten "
                   "haben, einer für die Arbeit, die dich am meisten nervt, verändert deine Woche schon."),
            knopf("Zum Kurs", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. Wer bis Samstagabend, 21 Uhr, einsteigt, ist beim Bonus-Call am 21. Januar dabei. " + MBA_PS),
        ],
    },
    {
        "datei": "masterclass-06-letzter-tag-bonus.html", "tag": "M6", "warten": "warten bis Sa 10.10. 07:00",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Bis heute Abend mit dem Bonus-Call im Januar",
        "betreff2": "Drei Fragen, die du dir vielleicht stellst",
        "wann": "Automation „0€ KI Webinar“, warten bis Sa 10.10. 07:00 · nur wer noch nicht gekauft hat",
        "preheader": "Heute um 21 Uhr endet der Bonus aus der Masterclass.",
        "h1": "Heute Abend endet der Bonus",
        "unterzeile": "Und drei Fragen, die dir vielleicht durch den Kopf gehen.",
        "notiz": """Pitch 3 von 3: FAQ + Last Call Bonus. Danach übernehmen die Launch-Mails an die Liste
(15.10. Frühbucher endet · 22./23.10. Kasse zu). Danach → Engine.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("heute um 21 Uhr endet der Bonus aus der Masterclass: Wer bis dann einsteigt, ist zusätzlich beim "
                   "Bonus-Call am 21. Januar dabei, wenn alles ausprobiert ist. Bevor du entscheidest, die drei Fragen, "
                   "die dir vielleicht gerade durch den Kopf gehen."),
            liste("Die drei Fragen", [
                "<strong>„Ist das nicht viel zu technisch für mich?“</strong> Du fängst im Chat an, den du kennst. "
                "Installiert wird erst in Kapitel 4, über die Desktop-App, und ohne schwarzes Fenster.",
                "<strong>„Ich hab keine Zeit für noch einen Kurs.“</strong> Die Lektionen sind kurz, die Kapitel "
                "gehen Woche für Woche auf, und alles, was du einrichtest, nimmt dir danach jede Woche Arbeit ab.",
                "<strong>„Und wenn ich später doch in die MBA will?“</strong> Dann wird dir angerechnet, was du "
                "für den Kurs bezahlt hast.",
            ]),
            knopf("Zum Kurs", KURS_URL),
            absatz("Der Frühbucherpreis von 277 gilt noch bis Donnerstag, 15. Oktober.", True),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
]

# ======================================================================
# Strecke „0€ Stimmcheck“ — nach der Auslieferung (stimm-01)
# In AC als Wenn/Dann: Datum vor 8.10. → Einladung · danach → Aufzeichnung + Pitch
# ======================================================================
MAILS += [
    {
        "datei": "stimm-02-einladung.html", "tag": "S2", "warten": "+1 Tag · Zweig „vor dem 8.10.“",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "Was deine KI jetzt noch nicht weiss",
        "betreff2": "Dein Stimm-Brief ist die eine Hälfte",
        "wann": "Automation „0€ Stimmcheck“, 1 Tag nach der Auslieferung, nur solange das Datum vor dem 8.10. liegt",
        "preheader": "Die andere Hälfte zeige ich dir am Donnerstag, 8. Oktober, live.",
        "h1": "Die eine Hälfte hast du jetzt",
        "unterzeile": "Deine KI weiss, wer du bist. Die andere Hälfte zeige ich dir live.",
        "notiz": "",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("mit deinem Stimm-Brief weiss deine KI jetzt, wer du bist, für wen du schreibst und wie du "
                   "klingst. Das ist die eine Hälfte, und bei den meisten fehlt schon die."),
            absatz("Die andere Hälfte ist, dass sie weiss, <strong>was zu tun ist</strong>, ohne dass du es ihr "
                   "jede Woche neu erklärst. Bei mir heisst das: Am Freitagmorgen liegt meine ganze Content-Woche "
                   "vorbereitet im Cockpit, und ich schaue nur noch drüber und gebe frei."),
            absatz("Wie das aussieht, zeige ich dir live am <strong>%s</strong>, kostenlos und mit Aufzeichnung "
                   "am selben Tag." % TERMIN),
            knopf("Platz für die Masterclass sichern", MC_SEITE),
            gruss("Herzlich,"),
            ps("P.S. Hast du deinen Brief schon ausprobiert? Antworte mir gern, wie dein erster Text geworden ist."),
        ],
    },
    {
        "datei": "stimm-03-einladung-kochbot.html", "tag": "S3", "warten": "+2 Tage · Zweig „vor dem 8.10.“",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "Früher zwei Stunden, heute fünf Minuten",
        "betreff2": "Mein kleinster Assistent",
        "wann": "Automation „0€ Stimmcheck“, 2 Tage nach S2, nur solange das Datum vor dem 8.10. liegt",
        "preheader": "Was mein Kochbot mit deinem Business zu tun hat.",
        "h1": "Früher zwei Stunden, heute fünf Minuten",
        "unterzeile": "Mein kleinster Assistent, und warum er dasselbe Prinzip hat wie dein Stimm-Brief.",
        "notiz": "",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("für eine saubere Menüplanung habe ich früher gut ein, zwei Stunden gebraucht, mit Überlegen "
                   "und Einkaufsliste schreiben. Heute beantworte ich drei Fragen: Ist nächste Woche etwas "
                   "Besonderes, habe ich wenig Zeit oder kommt Besuch, und muss etwas weg? Daraus stellt mir mein "
                   "Kochbot aus meinen eigenen Rezepten die Menüliste samt Einkaufsliste zusammen, fix fertig aufs "
                   "Handy. Kochen muss ich allerdings immer noch selbst."),
            absatz("Das Prinzip ist dasselbe wie bei deinem Stimm-Brief: Die KI kennt mich, meine Rezepte und "
                   "meine Familie, und sie weiss genau, was zu tun ist. Genau so laufen bei mir auch Captions, "
                   "Storys und Mails."),
            absatz("Am <strong>%s</strong> zeige ich dir das live, vom Kochbot bis zum Cockpit." % TERMIN),
            knopf("Platz für die Masterclass sichern", MC_SEITE),
            gruss("Herzlich,"),
            ps("P.S. Die Masterclass ist kostenlos, und die Aufzeichnung bekommst du am selben Tag."),
        ],
    },
    {
        "datei": "stimm-02b-aufzeichnung.html", "tag": "S2b", "warten": "+1 Tag · Zweig „ab dem 8.10.“",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "Wie es nach dem Stimm-Brief weitergeht",
        "betreff2": "Die Aufzeichnung für dich",
        "wann": "Automation „0€ Stimmcheck“, 1 Tag nach der Auslieferung, wenn das Datum ab dem 8.10. liegt",
        "preheader": "Die Aufzeichnung meiner Masterclass, 45 Minuten.",
        "h1": "Wie es weitergeht",
        "unterzeile": "Die Aufzeichnung meiner Masterclass, für dich zum Nachschauen.",
        "notiz": "🚨 AUFZEICHNUNG_URL eintragen. Das Webinar als Aufzeichnung für alle, die später kommen.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("mit deinem Stimm-Brief weiss deine KI jetzt, wer du bist. Die andere Hälfte ist, dass sie "
                   "weiss, was zu tun ist, ohne dass du es jede Woche neu erklärst."),
            absatz("Wie das bei mir aussieht, habe ich in einer Masterclass gezeigt: mein Cockpit, meine "
                   "Assistenten, wie ein Skill entsteht und den Bot, der mir die Menüplanung abnimmt. Hier ist "
                   "die Aufzeichnung für dich, rund 45 Minuten:"),
            knopf("Zur Aufzeichnung", AUFZEICHNUNG_URL),
            gruss("Viel Spass beim Anschauen,"),
            ps("P.S. Am Ende erzähle ich, wie du dir das selbst aufbauen kannst. Schau es dir an, bevor du "
               "entscheidest, ob das etwas für dich ist."),
        ],
    },
    {
        "datei": "stimm-03b-kurs.html", "tag": "S3b", "warten": "+2 Tage · Zweig „ab dem 8.10.“ · solange die Kasse offen ist",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "Vom Chat zur Mitarbeiterin",
        "betreff2": "Wenn du das bei dir einrichten willst",
        "wann": "Automation „0€ Stimmcheck“, 2 Tage nach S2b, nur bis Fr 23.10. (Kasse zu)",
        "preheader": "Was du im Kurs einrichtest, und bis wann die Kasse offen ist.",
        "h1": "Vom Chat zur Mitarbeiterin",
        "unterzeile": "Was du im Kurs einrichtest, Schritt für Schritt.",
        "notiz": "🚨 KURS_URL eintragen. Preisfrei formuliert, weil die Mail je nach Tag in eine andere Preisstufe fällt.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("jede Woche dieselben Captions, dieselben Storys, dieselben Antworten auf dieselben Fragen, "
                   "und jedes Mal erklärst du deiner KI wieder von vorne, was du willst. Genau diese Arbeit kann "
                   "sie dir abnehmen, wenn sie einmal weiss, wie du arbeitest."),
            absatz("Im Kurs <strong>„Easy KI für Networkerinnen — vom Chat zur Mitarbeiterin“</strong> richtest "
                   "du dir das ein:"),
            liste("Was du am Ende hast", [
                "<strong>Einen Arbeitsplatz mit deinem Wissen drin</strong>, dein Stimm-Brief ist schon der Anfang davon",
                "<strong>Deinen ersten eigenen Skill</strong> für eine Arbeit, die du jede Woche wieder machst",
                "<strong>Einen Bot, der von selbst läuft</strong>",
            ]),
            absatz("Du fängst im Chat an, den du kennst, und die Kapitel kommen ab dem 1. November Woche für "
                   "Woche. Die Kasse ist bis Freitag, 23. Oktober, offen, danach mache ich sie erst wieder auf, "
                   "wenn der Kurs komplett ist."),
            knopf("Alles zum Kurs", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "stimm-04b-einwand.html", "tag": "S4b", "warten": "+2 Tage · Zweig „ab dem 8.10.“ · solange die Kasse offen ist",
        "strecke": "stimm-check", "marke": "Der Stimm-Check",
        "betreff": "„Ist das nicht viel zu technisch für mich?“",
        "betreff2": "Die ehrliche Antwort auf deine grösste Sorge",
        "wann": "Automation „0€ Stimmcheck“, 2 Tage nach S3b, nur bis Fr 23.10. · danach → Engine",
        "preheader": "Die ehrliche Antwort, und warum du trotzdem im Chat anfängst.",
        "h1": "„Ist das nicht viel zu technisch?“",
        "unterzeile": "Eine berechtigte Frage, und meine ehrliche Antwort.",
        "notiz": "Letzte Mail der Strecke. Danach → Engine (Patricia hängt sie an).",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("vielleicht denkst du gerade genau das, und die Frage ist berechtigt. Bei „Arbeitsplatz "
                   "einrichten“ denken die meisten zuerst an Programmieren."),
            absatz("Deshalb fängt der Kurs genau dort an, wo du heute schon bist: im Chat, den du kennst. Du "
                   "lernst zuerst, wie ein guter Auftrag aussieht, dann kommt ein erster Bot ganz ohne Code, und "
                   "erst in Kapitel 4 installierst du etwas, über die Desktop-App, ohne schwarzes Fenster."),
            absatz("Die Lektionen sind kurz, Klick für Klick mitgefilmt, und du machst jeden Schritt direkt mit."),
            knopf("Zum Kurs", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
]

# ======================================================================
# M7 + Launch-Mails bis Kasse zu (Plan 26.09.2026)
# M7 hängt an der Masterclass-Strecke (Automation 84). Die sechs Launch-Mails gehen als
# Kampagne an die ganze Liste OHNE Käuferinnen (Kauf-Tag aus ThriveCart, Produkt 52).
# ======================================================================
MAILS += [
    {
        "datei": "masterclass-07-noch-3-stunden.html", "tag": "M7", "warten": "warten bis Sa 10.10. 18:00",
        "strecke": "masterclass", "marke": "KI-Masterclass",
        "betreff": "Noch 3 Stunden bis zum Bonus-Call",
        "betreff2": "Um 21 Uhr ist der Bonus weg",
        "wann": "Automation „0€ KI Webinar“ (84), warten bis Sa 10.10. 18:00 · nur wer noch nicht gekauft hat",
        "preheader": "Wer bis 21 Uhr einsteigt, ist am 21. Januar beim Bonus-Call dabei.",
        "h1": "Noch 3 Stunden",
        "unterzeile": "Dann endet der Bonus aus der Masterclass.",
        "notiz": "Letzte Mail der Masterclass-Strecke, kurz halten. Danach Pause bis Do 15.10.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("nur kurz, weil es heute um 21 Uhr endet: Wer bis dann in den Kurs <strong>„Easy KI für "
                   "Networkerinnen“</strong> einsteigt, ist zusätzlich beim <strong>Bonus-Call am 21. Januar</strong> "
                   "dabei. Bis dann hast du alles ausprobiert, und wir schauen zusammen an, was bei dir läuft und "
                   "wo es noch hakt."),
            absatz("Die zwei Live-Calls im November und Dezember und die Telegram-Gruppe gehören sowieso dazu. "
                   "Der Bonus-Call ist der dritte, und den gibt es nur bis heute Abend."),
            knopf("Jetzt einsteigen", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-01-preis-steigt.html", "tag": "L1", "warten": "Kampagne Do 15.10. 07:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Heute um Mitternacht steigt der Preis",
        "betreff2": "Letzter Tag zum Frühbucherpreis",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Do 15.10. 07:00",
        "preheader": "Bis heute Nacht 277, ab morgen 333.",
        "h1": "Heute ist der letzte Tag zu 277",
        "unterzeile": "Ab morgen kostet der Kurs 333.",
        "notiz": "Launch-Mail 1 von 6. Preisfrist 15.10. 23:59.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("heute ist der letzte Tag, an dem du den Kurs <strong>„Easy KI für Networkerinnen — vom Chat zur "
                   "Mitarbeiterin“</strong> zum Frühbucherpreis von <strong>277</strong> bekommst. Ab morgen kostet "
                   "er 333, und dann bleibt es dabei."),
            absatz("Falls du noch überlegst, was du davon eigentlich hast: Am Ende hast du eine KI, die dich kennt "
                   "und weiss, was zu tun ist. Dann erklärst du ihr nicht jeden Montag wieder von vorne, wer du bist "
                   "und was du brauchst."),
            liste("Was du am Ende hast", [
                "<strong>Einen Arbeitsplatz mit deinem Wissen drin</strong>, den deine KI bei jedem Auftrag liest",
                "<strong>Deinen ersten eigenen Skill</strong> für eine Arbeit, die du jede Woche wieder machst",
                "<strong>Einen Bot, der von selbst läuft</strong> und sich auf deinem Handy meldet",
            ]),
            absatz("Die Kapitel gehen ab dem 1. November Woche für Woche auf, dazu kommen zwei Live-Calls und eine "
                   "Telegram-Gruppe, in der ich dienstags und donnerstags alle Fragen beantworte."),
            knopf("Zum Frühbucherpreis einsteigen", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-02-fragen.html", "tag": "L2", "warten": "Kampagne Fr 16.10. 07:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Die Fragen, die mir zum Kurs gestellt werden",
        "betreff2": "Muss ich dafür programmieren können?",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Fr 16.10. 07:00",
        "preheader": "Programmieren, Kosten, keine Zeit: meine ehrlichen Antworten.",
        "h1": "Deine Fragen, meine Antworten",
        "unterzeile": "Die drei, die am häufigsten kommen.",
        "notiz": """Launch-Mail 2 von 6. ✏️ Die drei Fragen durch echte aus Patricias DMs ersetzen, sobald sie
da sind. Bis dahin stehen Fragen, die der Kurs wirklich beantwortet (Antworten aus den Folien).
🚨 Betreff sagt „werden gestellt“ — nur so lassen, wenn es echte Fragen sind, sonst Betreff 2 nehmen.""",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("seit der Masterclass kommen immer wieder dieselben Fragen zum Kurs. Hier sind meine ehrlichen "
                   "Antworten, damit du in Ruhe entscheiden kannst."),
            liste("Die drei Fragen", [
                "<strong>„Muss ich programmieren können?“</strong> Nein. Du fängst im Chat an, den du kennst. "
                "Installiert wird erst in Kapitel 4, über die Desktop-App und ohne schwarzes Fenster. Wenn du weisst, "
                "was ein Ordner ist, reicht das.",
                "<strong>„Was kostet Claude neben dem Kurs?“</strong> Zum Anfangen reicht das Gratis-Konto. Für die "
                "späteren Stufen brauchst du ein Abo, rund 20 bis 23 Franken im Monat, und für einen Bot, der auch "
                "bei ausgeschaltetem Rechner läuft, rund 5 Franken dazu.",
                "<strong>„Und wenn ich hängen bleibe?“</strong> Dann schreibst du in die Telegram-Gruppe. Dienstags "
                "und donnerstags beantworte ich dort alles, und die Gruppe bleibt auch nach den zwei Live-Calls offen.",
            ]),
            absatz("Der Kurs kostet ab heute 333, und diesen Preis kannst du auch in Raten zahlen. Die Kasse ist bis "
                   "Freitag, 23. Oktober, offen."),
            knopf("Alles zum Kurs", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-03-ergebnis.html", "tag": "L3", "warten": "Kampagne Di 20.10. 07:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Was du am 30. November in der Hand hast",
        "betreff2": "Dein Montag im Dezember",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Di 20.10. 07:00",
        "preheader": "Drei Dinge, die es bei dir vorher nicht gab.",
        "h1": "Am 30. November",
        "unterzeile": "Dann ist der Kurs komplett, und das hast du in der Hand.",
        "notiz": "Launch-Mail 3 von 6: das Ergebnis konkret.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("am 30. November geht das letzte Kapitel auf. Wenn du bis dann mitgemacht hast, sieht dein Montag "
                   "anders aus: Du öffnest deine KI, sagst ihr, welche Caption du für Mittwoch brauchst, und sie weiss, "
                   "für wen du schreibst, wie du klingst und was in deinen Texten nie vorkommt."),
            liste("Das hast du dann", [
                "<strong>Deinen Arbeitsplatz</strong>, in dem dein Business-Brief und deine Inhalte liegen",
                "<strong>Deinen ersten eigenen Skill</strong>, der eine Arbeit übernimmt, die du bisher jede Woche von Hand machst",
                "<strong>Einen Bot</strong>, der sich von selbst auf deinem Handy meldet",
            ]),
            absatz("Du musst dafür nicht bis ganz nach oben. Schon nach den ersten Kapiteln klingen deine Texte nach "
                   "dir, und alles Weitere baut darauf auf."),
            knopf("Zum Kurs", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. Die Kasse ist noch bis Freitag offen. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-04-morgen-zu.html", "tag": "L4", "warten": "Kampagne Do 22.10. 07:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Morgen geht die Kasse zu",
        "betreff2": "Danach erst wieder, wenn der Kurs komplett ist",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Do 22.10. 07:00",
        "preheader": "Und danach mache ich sie erst wieder auf, wenn alles fertig ist.",
        "h1": "Morgen um Mitternacht",
        "unterzeile": "Dann schliesse ich die Kasse.",
        "notiz": "Launch-Mail 4 von 6. 🚨 Die Kasse muss am 24.10. wirklich zu sein (Entscheid 24.09.).",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("morgen, am Freitag um Mitternacht, schliesse ich die Kasse für den Kurs <strong>„Easy KI für "
                   "Networkerinnen“</strong>. Danach mache ich sie erst wieder auf, wenn alle zehn Kapitel online sind."),
            absatz("Wenn du also schon eine Weile denkst, dass deine KI mehr können müsste, und jede Woche wieder "
                   "dieselben Texte selbst schreibst, ist jetzt der Moment. Ab dem 1. November fangen wir gemeinsam an."),
            knopf("Jetzt einsteigen", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. Die 333 kannst du auch in Raten zahlen. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-05-letzter-tag.html", "tag": "L5", "warten": "Kampagne Fr 23.10. 07:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Heute um Mitternacht",
        "betreff2": "Letzter Tag",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Fr 23.10. 07:00",
        "preheader": "Heute ist die Kasse zum letzten Mal offen.",
        "h1": "Heute ist der letzte Tag",
        "unterzeile": "Um Mitternacht schliesst die Kasse.",
        "notiz": "Launch-Mail 5 von 6, letzter Tag morgens.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("heute um Mitternacht schliesst die Kasse für den Kurs. Ich will dich nicht drängen, aber ich will "
                   "auch nicht, dass du es morgen verpasst hast und dich ärgerst."),
            absatz("Im Kurs richtest du dir Schritt für Schritt eine KI ein, die dich kennt und weiss, was zu tun ist. "
                   "Du fängst im Chat an, die Kapitel gehen ab dem 1. November Woche für Woche auf, und du bist dabei "
                   "nicht allein: zwei Live-Calls und eine Telegram-Gruppe, in der ich dienstags und donnerstags "
                   "alles beantworte."),
            knopf("Noch heute einsteigen", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
    {
        "datei": "launch-06-noch-5-stunden.html", "tag": "L6", "warten": "Kampagne Fr 23.10. 19:00",
        "strecke": "launch", "marke": "Easy KI für Networkerinnen",
        "betreff": "Noch 5 Stunden",
        "betreff2": "Dann ist die Kasse zu",
        "wann": "Kampagne an die ganze Liste ohne Käuferinnen · Fr 23.10. 19:00",
        "preheader": "Um Mitternacht schliesse ich die Kasse.",
        "h1": "Noch 5 Stunden",
        "unterzeile": "Dann ist die Kasse zu.",
        "notiz": "Letzte Launch-Mail. Kurz halten. Danach → Engine.",
        "bloecke": [
            absatz("Hallo %FIRSTNAME%"),
            absatz("in fünf Stunden schliesse ich die Kasse. Wenn du dabei sein willst, wenn wir am 1. November "
                   "anfangen, ist das jetzt die letzte Gelegenheit."),
            knopf("Jetzt noch einsteigen", KURS_URL),
            gruss("Herzlich,"),
            ps("P.S. " + MBA_PS),
        ],
    },
]


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    karten, beanstandet = [], 0
    for m in MAILS:
        fertig = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "KI-MASTERCLASS").replace(
            "ERZEUGT von scripts/startklar/mails-bauen.py", "ERZEUGT von scripts/ki-kurs/masterclass-mails-bauen.py").replace("{{TOOL_URL}}", TOOL_URL)
        beanstandet += len(sk.umlaute_pruefen(m["datei"], fertig))
        (ZIEL / m["datei"]).write_text(fertig, encoding="utf-8")
        kennung = re.sub(r"[^a-z0-9]+", "", m["datei"].lower())
        karten.append(sk.KARTE.format(
            tag=m["tag"], h1=m["h1"], warten=m["warten"],
            betreff=html.escape(m["betreff"], quote=False),
            betreff_roh=html.escape(m["betreff"], quote=True),
            datei=m["datei"], id=kennung))
        print("  geschrieben:", m["datei"])
    seite = sk.KOPIERSEITE.format(karten="\n".join(karten)).replace("Startklar", "KI-Masterclass")
    # Einleitung und Warnkasten der Vorlage gehören zu Startklar, hier eigene
    seite = re.sub(r'<p class="unter">.*?</p>',
                   '<p class="unter">Die Mails im KI-Launch: Masterclass (Do 8. Oktober, 9 Uhr) und Stimm-Check. '
                   'Knopf „Ganzes HTML“ tippen, in ActiveCampaign einfügen. Die Vorschau unter jeder Karte '
                   'ist genau das, was ankommt.</p>', seite, count=1, flags=re.S)
    seite = re.sub(r'<div class="warnung">.*?</div>',
                   '<div class="warnung"><b>Opt-in-Mails:</b> im jeweiligen Formular → Optionen → Opt-in-Bestätigung → '
                   'E-Mail bearbeiten → HTML. Der Knopf zeigt auf <code>%CONFIRMLINK%</code>, den '
                   'Bestätigungslink von ActiveCampaign. Die Auslieferung des Stimm-Checks kommt in eine '
                   'Automation mit Auslöser Tag <code>0€ Stimmcheck</code>.</div>', seite, count=1, flags=re.S)
    seite = re.sub(r'<div class="karte">\s*<h2>Und danach: ab in die Engine</h2>.*?</div>', '',
                   seite, count=1, flags=re.S)
    assert "Sieben Mails" not in seite and "Tag 12" not in seite and "ab in die Engine" not in seite
    (ZIEL / "index.html").write_text(seite, encoding="utf-8")
    print("  geschrieben: index.html (Kopierseite)")
    print("  ✓ Keine umschriebenen Umlaute." if not beanstandet else "  ⚠ %d Umlaut-Funde" % beanstandet)


if __name__ == "__main__":
    main()
