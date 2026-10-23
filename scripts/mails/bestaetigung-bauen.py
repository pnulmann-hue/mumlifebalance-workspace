# -*- coding: utf-8 -*-
"""Die Bestätigungsmails (Opt-in) der Mentoring-Freebies — eine je Formular.

    python scripts/mails/bestaetigung-bauen.py              # bauen + prüfen
    python scripts/mails/bestaetigung-bauen.py --hochladen  # zusätzlich in AC einsetzen

Anlass (23.10.2026): Zehn Formulare verschickten als allererste Mail einen Text der
alten Positionierung („Toll, dass du lernen willst, erfolgreich Grenzen zu setzen!“),
die übrigen den AC-Standardbetreff „Bitte bestätigen Sie Ihr Abonnement für %LISTNAME%“.
Prüfbericht: outputs/funnels/2026-10-23-formular-pruefung.md

Regeln für diese Mails (Julia: die Bestätigungsmail hat nur einen Job — den Klick):
- kein Angebot, kein zweiter Link
- nennt das Freebie und sagt, was nach dem Klick kommt
- Knopf auf %CONFIRMLINK% (Platzhalter von AC) und Absenderadresse im Fuss
- keine Anrede mit Vornamen: mehrere Formulare fragen ihn gar nicht ab

Das Gerüst kommt aus scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert.
Die doTERRA-Fassung (Energie-Kickstart) baut scripts/mails/bauen.py.

--hochladen schreibt in die Opt-in-Nachricht, die am Formular hängt (form.options.optin_id),
und legt vorher die bisherige Fassung unter bestaetigungsmails/_alt/ ab.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)

ZIEL = ROOT / "outputs" / "funnels" / "bestaetigungsmails"
absatz, knopf, ps, gruss = sk.absatz, sk.knopf, sk.ps, sk.gruss

FREMD = ("Falls du dich gar nicht selbst eingetragen hast, ignorierst du diese Mail einfach. "
         "Dann hörst du auch nichts weiter von mir.")
SPAM = ("P.S. Damit meine nächste Mail nicht im Spam oder unter „Werbung“ landet, zieh diese "
        "hier am besten gleich in deinen Posteingang.")


def mail(formular, datei, marke, betreff, preheader, h1, unterzeile, was, knopftext, danach):
    """Alle neun folgen demselben Ablauf: was es ist · warum der Klick · Knopf · was danach kommt."""
    return {
        "formular": formular, "datei": datei, "marke": marke + " · Bestätigung",
        "betreff": betreff, "betreff2": "", "wann": "sofort nach dem Formular",
        "notiz": "Opt-in-Mail am AC-Formular %d. Einziger Job: der Klick." % formular,
        "preheader": preheader, "h1": h1, "unterzeile": unterzeile,
        "bloecke": [
            absatz(was),
            absatz("Bevor ich dir die erste Mail schicken darf, brauche ich noch einen Klick "
                   "von dir. Damit bestätigst du, dass wirklich du dich eingetragen hast und "
                   "nicht jemand anderes mit deiner Adresse."),
            knopf(knopftext + " &#8594;", "%CONFIRMLINK%"),
            absatz(danach),
            absatz(FREMD, letzter=True),
            gruss("Bis gleich,"),
            ps(SPAM),
        ],
    }


MAILS = [
    mail(49, "businessfahrplan.html", "Businessfahrplan",
         "Ein Klick noch, dann kommt dein Businessfahrplan",
         "Bestätig kurz deine Adresse, danach schicke ich dir Phase 1.",
         "Ein Klick noch, dann kommt dein Fahrplan",
         "Von Produktposts zu einem Business, das dir gehört.",
         "Hey, schön, dass du dir den Businessfahrplan holst. Er zeigt dir in vier Phasen, "
         "wie du vom Produktposten zu einem eigenen Angebot kommst.",
         "Ja, schick mir den Fahrplan",
         "Sobald du geklickt hast, kommt der Fahrplan in dein Postfach. Mit Phase 1 kannst "
         "du noch heute anfangen."),

    mail(51, "lead-challenge.html", "Lead-Challenge",
         "Ein Klick noch, dann bist du bei der Lead-Challenge dabei",
         "Bestätig kurz deine Adresse, danach bekommst du den Link zur Gruppe.",
         "Ein Klick noch, dann bist du dabei",
         "Drei Tage, in denen du lernst, wie aus Followern Kontakte werden.",
         "Hey, schön, dass du bei der Lead-Challenge mitmachst. Die Challenge läuft in "
         "meiner Telegram-Gruppe, dort bekommst du jeden Tag ein kurzes Video und eine "
         "Aufgabe dazu.",
         "Ja, ich bin dabei",
         "Sobald du geklickt hast, schicke ich dir den Link zur Gruppe. Dort findest du "
         "alles Weitere."),

    mail(53, "starterguide.html", "Instagram-Starterguide",
         "Ein Klick noch, dann kommt dein Instagram-Starterguide",
         "Bestätig kurz deine Adresse, danach schicke ich dir den Guide.",
         "Ein Klick noch, dann kommt dein Starterguide",
         "Für alle, die Follower haben, aber noch keine Kundschaft.",
         "Hey, schön, dass du dir den Instagram-Starterguide holst. Er zeigt dir Schritt "
         "für Schritt, wie dein Profil Anfragen bringt statt nur Likes.",
         "Ja, schick mir den Guide",
         "Sobald du geklickt hast, kommt der Guide in dein Postfach. Mit Schritt 1 kannst "
         "du gleich heute anfangen."),

    mail(45, "story-challenge.html", "Story-Challenge",
         "Ein Klick noch, dann startet deine Story-Challenge",
         "Bestätig kurz deine Adresse, danach schicke ich dir das Workbook.",
         "Ein Klick noch, dann startet deine Story-Challenge",
         "Sieben Tage, bis auf deine Storys wieder jemand antwortet.",
         "Hey, schön, dass du bei der 7-Tage-Story-Challenge mitmachst. Du bekommst ein "
         "Workbook, mit dem du jeden Tag eine Story baust, auf die man antworten will.",
         "Ja, schick mir das Workbook",
         "Sobald du geklickt hast, kommt das Workbook in dein Postfach, und du kannst "
         "direkt mit Tag 1 loslegen."),

    mail(41, "von-0-auf-echt.html", "Von 0 auf echt",
         "Ein Klick noch, dann kommt dein Workbook „Von 0 auf echt“",
         "Bestätig kurz deine Adresse, danach schicke ich dir das Workbook.",
         "Ein Klick noch, dann gehört das Workbook dir",
         "Für ein Network-Business, das sich nach dir anfühlt.",
         "Hey, schön, dass du dir das Workbook „Von 0 auf echt“ holst. Darin findest du "
         "heraus, wofür du stehst, damit dein Profil nach dir klingt und nicht nach "
         "Werbung.",
         "Ja, schick mir das Workbook",
         "Sobald du geklickt hast, kommt das Workbook in dein Postfach."),

    mail(47, "bio-check.html", "Bio-Check",
         "Ein Klick noch, dann ist dein Bio-Check startklar 🌿",
         "Bestätig kurz deine Adresse, danach bekommst du den Link zum Bot.",
         "Ein Klick noch, dann ist dein Bio-Check startklar",
         "In fünf bis zehn Minuten zu einer Bio, in die man reingeht.",
         "Hey, schön, dass du deine Bio anschauen willst. Mein Bio-Check-Bot geht sie mit "
         "dir durch und baut dir Vorschläge, die zu deinem Thema passen.",
         "Ja, schick mir den Link",
         "Sobald du geklickt hast, kommt der Link zum Bot in dein Postfach. Nimm dir die "
         "fünf bis zehn Minuten gleich, solange du an deine Bio denkst."),

    mail(66, "produkt-ideen-finder.html", "Produkt-Ideen-Finder",
         "Ein Klick noch, dann startet dein Produkt-Ideen-Finder ✨",
         "Bestätig kurz deine Adresse, danach geht's los.",
         "Ein Klick noch, dann geht's los",
         "Fünf Minuten, und du hast eine Produktidee statt eines vagen Gefühls.",
         "Hey, schön, dass du rausfinden willst, welche eigene Produktidee zu dir passt. "
         "Der Produkt-Ideen-Finder stellt dir ein paar Fragen und macht aus deinen "
         "Antworten konkrete Ideen.",
         "Ja, ich will meine Idee finden",
         "Sobald du geklickt hast, landest du direkt beim Finder, und den Link bekommst du "
         "zusätzlich per Mail, falls du später weitermachen willst."),

    mail(71, "stimm-check.html", "Stimm-Check",
         "Ein Klick noch, dann gehört dein Stimm-Check dir",
         "Bestätig kurz deine Adresse, danach kannst du sofort loslegen.",
         "Ein Klick noch, dann kannst du loslegen",
         "Fünfzehn Minuten, und deine KI weiss, wie du klingst.",
         "Hey, schön, dass du deinen Stimm-Check machen willst. Er liest aus einem Text von "
         "dir heraus, wie du schreibst, damit deine KI künftig nach dir klingt.",
         "Ja, ich will loslegen",
         "Sobald du geklickt hast, landest du direkt beim Stimm-Check. Hol dir schon mal "
         "einen Text, den du selbst geschrieben hast, eine Caption oder eine Mail reicht."),

    mail(1, "newsletter.html", "Newsletter",
         "Ein Klick noch, dann bist du auf meiner Liste",
         "Bestätig kurz deine Adresse, danach bekommst du meine Mails.",
         "Ein Klick noch, dann bist du dabei",
         "Mails für Mamas, die neben der Familie ihr eigenes Business aufbauen.",
         "Hey, schön, dass du meine Mails bekommen willst. Darin teile ich, was bei mir im "
         "Business gerade funktioniert, was nicht, und was du davon gleich übernehmen kannst.",
         "Ja, ich will deine Mails",
         "Sobald du geklickt hast, schicke ich dir eine kurze Willkommensmail, damit du "
         "weisst, was dich erwartet."),
]

ABSENDER = ('<p style="margin:10px 0 0 0;font-family:Arial,sans-serif;font-size:11px;'
            'color:#a9bcc8;line-height:1.6;">Gesendet an %EMAIL% &middot; %SENDER-INFO-SINGLELINE%</p>')
FUSS = "Patricia Ulmann &middot; mumlifebalance.ch</p>"


def bauen(m):
    h = sk.bauen(m)
    assert h.count(FUSS) == 1, "Fuss im Gerüst nicht gefunden"
    h = h.replace(FUSS, FUSS + "\n              " + ABSENDER)
    for platz in ("%CONFIRMLINK%", "%SENDER-INFO-SINGLELINE%"):
        assert platz in h, "%s fehlt in %s" % (platz, m["datei"])
    return h


def text_fassung(h):
    t = re.sub(r"(?s)<(style|script|title|head)[^>]*>.*?</\1>", "", h)
    t = re.sub(r"(?s)<!--.*?-->", "", t)
    t = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"\2: \1", t)
    t = re.sub(r"</p>|</h1>|</tr>", "\n\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"\n\s*\n+", "\n\n", "\n".join(z.strip() for z in t.splitlines()))
    return t.strip()


def ac_zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        mm = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", z)
        if mm:
            env[mm.group(1)] = mm.group(2).strip("\"'")
    assert env.get("AC_API_KEY"), "AC-Zugang fehlt in der .env"
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


def hochladen(m, h):
    url, key = ac_zugang()

    def ac(pfad, daten=None):
        r = urllib.request.Request(url + "/api/3/" + pfad, method="PUT" if daten else "GET",
                                   data=json.dumps(daten).encode() if daten else None,
                                   headers={"Api-Token": key, "Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(r))

    form = ac("forms/%d" % m["formular"])["form"]
    opt = form.get("options") or {}
    assert opt.get("sendoptin") and opt.get("optin_id"), "Formular %d hat keine Opt-in-Mail" % m["formular"]
    msg_id = ac("campaigns/%s/campaignMessages" % opt["optin_id"])["campaignMessages"][0]["message"]
    alt = ac("messages/%s" % msg_id)["message"]
    (ZIEL / "_alt").mkdir(parents=True, exist_ok=True)
    sicherung = ZIEL / "_alt" / ("formular-%d-%s.json" % (m["formular"], msg_id))
    if not sicherung.exists():   # nur die allererste Fassung sichern, nie überschreiben
        sicherung.write_text(json.dumps({k: alt.get(k) for k in ("subject", "html", "text", "preheader_text")},
                                        ensure_ascii=False, indent=1), encoding="utf-8")
    neu = ac("messages/%s" % msg_id, {"message": {
        "fromname": "Patricia Ulmann", "fromemail": "info@mumlifebalance.ch",
        "reply2": "info@mumlifebalance.ch", "subject": m["betreff"], "name": m["betreff"],
        "preheader_text": m["preheader"], "html": h, "text": text_fassung(h)}})["message"]
    kontrolle = ac("messages/%s" % msg_id)["message"]
    assert kontrolle["subject"] == m["betreff"] and "%CONFIRMLINK%" in kontrolle["html"], "Kontrolle fehlgeschlagen"
    print("   in AC: Formular %d → Nachricht %s ✓" % (m["formular"], msg_id))


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for m in MAILS:
        h = bauen(m)
        (ZIEL / m["datei"]).write_text(h, encoding="utf-8")
        print("%-28s %s" % (m["datei"], m["betreff"]))
        if "--hochladen" in sys.argv:
            hochladen(m, h)
    # Umlaut-Wächter aus dem Gerüst über den sichtbaren Text
    for m in MAILS:
        sk.umlaute_pruefen(ZIEL / m["datei"], (ZIEL / m["datei"]).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
