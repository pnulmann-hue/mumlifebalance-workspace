"""Mails zum Jahresplanungs-Workshop „Neustart 2027“ (Do 17.12.2026, 09:00, gratis).

Texte: outputs/produkte/jahresplanung/angebot/04-mails.md (dort wird geschrieben, hier gesetzt).
Geruest kommt aus scripts/startklar/mails-bauen.py, importiert, nicht kopiert.
Die Bestaetigungsmail (Opt-in am Formular 76) baut scripts/mails/bestaetigung-bauen.py.

    python scripts/jahresplanung/mails-bauen.py              # HTML nach outputs/produkte/jahresplanung/mails/
    python scripts/jahresplanung/mails-bauen.py --hochladen  # zusaetzlich als Kampagnen-ENTWURF in AC (status 0)

Mit --hochladen wird nichts verschickt. Alle Entwuerfe haengen an Liste 2.
A1-A3 sind Kampagnen (beim Einplanen Tag „0€ Jahresplanung“ 109 und MBA-Kaeuferinnen ausschliessen).
E1-E5 sind Vorlagen fuer die Automation „0€ Jahresplanung“, die Patricia in AC baut.
Zoom- und Aufzeichnungs-Link stehen in scripts/jahresplanung/.env (ZOOM, AUFZEICHNUNG), nie hier.
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

ZIEL = ROOT / "outputs" / "produkte" / "jahresplanung" / "mails"
absatz, liste, knopf, ps, gruss = sk.absatz, sk.liste, sk.knopf, sk.ps, sk.gruss

SEITE = "https://mumlifebalance.ch/neustart-2027/"
MBA = "https://mumlifebalance.ch/mba/"
PLANER = "https://claude.ai/artifact/72vifh23HRaBDoVjqcgx4t"   # „Mein Jahresplan“, vorher öffentlich teilen

_ENV = {}
_env = ROOT / "scripts/jahresplanung/.env"
if _env.exists():
    for z in _env.read_text(encoding="utf-8").splitlines():
        if "=" in z and not z.startswith("#"):
            k, v = z.split("=", 1)
            _ENV[k.strip()] = v.strip().strip('"')
ZOOM = _ENV.get("ZOOM") or "#ZOOM-LINK-FEHLT"
AUFZEICHNUNG = _ENV.get("AUFZEICHNUNG") or "#AUFZEICHNUNG-FEHLT"

MARKE = "mumlifebalance · Neustart 2027"

MAILS = [
    {"datei": "A1-einladung.html", "name": "Neustart 2027 A1 · Einladung (Mo 30.11.)",
     "marke": MARKE, "betreff": "Planst du 2027 schon, oder erst im Januar?", "betreff2": "",
     "wann": "Mo 30.11.2026, Kampagne an Liste 2",
     "preheader": "Am 17. Dezember mache ich das mit dir zusammen, gratis.",
     "h1": "Neustart 2027", "unterzeile": "Jahresplanungs-Workshop · Do 17. Dezember, 09:00 Uhr",
     "notiz": "Kampagne A1. Ausschliessen: Tag 0€ Jahresplanung (109), MBA-Käuferinnen.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("im Dezember passiert bei vielen von uns dasselbe: Der Kopf ist schon im neuen Jahr, und der "
                "Kalender ist noch leer. Im Januar fängt dann die Schule wieder an, und das Business läuft wieder "
                "von Monat zu Monat."),
         absatz("Deshalb öffne ich einen Call aus meiner Mum Business Academy für alle: <strong>Neustart 2027</strong>, "
                "den Jahresplanungs-Workshop, am <strong>Donnerstag, 17. Dezember, um 09:00 Uhr</strong>, gratis und "
                "mit Aufzeichnung."),
         knopf("Ich plane mit", SEITE),
         absatz("Wir planen dein Jahr in der Reihenfolge, die neben Kindern funktioniert: zuerst Ferien, Familie und "
                "deine eigene Zeit, danach deine Angebote. Wenn du nur dein Network hast, rechnen wir mit den Zahlen "
                "aus deiner eigenen Abrechnung. Du gehst mit deinem Jahr auf einem Blatt raus und weisst, was du im "
                "Januar als Erstes tust.", True),
         gruss("Herzlich,"),
         ps("P.S. Du kannst am Donnerstagmorgen nicht? Trag dich trotzdem ein, die Aufzeichnung bleibt offen."),
     ]},
    {"datei": "A2-leben-zuerst.html", "name": "Neustart 2027 A2 · Leben zuerst (Mo 7.12.)",
     "marke": MARKE, "betreff": "Was zuerst in meinen Kalender kommt", "betreff2": "",
     "wann": "Mo 7.12.2026, Kampagne an Liste 2 ohne Angemeldete",
     "preheader": "Und warum das die halbe Planung ist.",
     "h1": "Leben zuerst", "unterzeile": "Neustart 2027 · Do 17. Dezember, 09:00 Uhr",
     "notiz": "Kampagne A2. Ausschliessen: Tag 109, MBA-Käuferinnen. Erster Absatz von Patricia bestätigen lassen.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("bevor bei mir ein Angebot einen Monat bekommt, stehen die Schulferien meiner vier Kinder im "
                "Kalender. Dann die Geburtstage, dann meine eigene Zeit. Erst danach schaue ich, was wann Platz hat."),
         absatz("Genau in dieser Reihenfolge planen wir am 17. Dezember zusammen. So rutscht dein Launch nicht in die "
                "Sportferien, und nach einem Angebot kommt kein Loch, weil du schon weisst, was danach dran ist.", True),
         knopf("Ich bin am 17. Dezember dabei", SEITE),
         gruss("Herzlich,"),
     ]},
    {"datei": "A3-uebermorgen.html", "name": "Neustart 2027 A3 · Übermorgen (Di 15.12.)",
     "marke": MARKE, "betreff": "Übermorgen um 09:00 planen wir 2027", "betreff2": "",
     "wann": "Di 15.12.2026, Kampagne an Liste 2 ohne Angemeldete",
     "preheader": "Ein Klick, und du bist dabei.",
     "h1": "Übermorgen", "unterzeile": "Neustart 2027 · Do 17. Dezember, 09:00 Uhr",
     "notiz": "Kampagne A3. Ausschliessen: Tag 109, MBA-Käuferinnen.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("am Donnerstag um 09:00 Uhr ist der Jahresplanungs-Workshop. Danach gehen bei uns die "
                "Weihnachtsferien los, und ich vermute, bei dir auch."),
         absatz("Wenn du 2027 nicht wieder jeden Morgen neu entscheiden willst, was du anbietest, nimm dir diesen "
                "Donnerstagmorgen. Du brauchst nur deinen Laptop, den Ferienplan deiner Kinder und deine Angebote "
                "mit Preis.", True),
         knopf("Ich plane mit", SEITE),
         gruss("Herzlich,"),
     ]},
    {"datei": "E1-vorbereitung.html", "name": "Neustart 2027 E1 · Vorbereitung (Mi 16.12. 18:00)",
     "marke": MARKE, "betreff": "Morgen um 09:00: das kannst du bereitlegen", "betreff2": "",
     "wann": "Automation, Mi 16.12.2026 18:00",
     "preheader": "Drei Dinge, dann bist du startklar.",
     "h1": "Morgen planen wir 2027", "unterzeile": "Donnerstag, 17. Dezember, 09:00 Uhr",
     "notiz": "Automation 0€ Jahresplanung. Zoom-Link aus scripts/jahresplanung/.env.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("morgen um 09:00 Uhr planen wir dein Jahr 2027. Leg dir bitte bereit:"),
         liste("Was du brauchst", [
             "den Ferienplan deiner Kinder für 2027 und eure festen Familientermine",
             "deine Angebote mit Preis, und wenn du im Network bist, deine letzte Monatsabrechnung",
             "ein paar Stichworte: Was lief 2026 gut, was war schwer?",
         ]),
         absatz("Wir arbeiten mit meinem Jahresplaner, einer Seite im Browser ohne Anmeldung. Am besten auf dem "
                "Laptop, damit du Zoom und den Planer nebeneinander hast."),
         knopf("Zum Jahresplaner", PLANER),
         absatz("Und hier ist schon der Link zum Workshop, damit du ihn morgen nicht suchen musst:", True),
         knopf("Zum Zoom am 17. Dezember", ZOOM),
         gruss("Bis morgen,"),
     ]},
    {"datei": "E2-in-einer-stunde.html", "name": "Neustart 2027 E2 · In einer Stunde (Do 17.12. 08:00)",
     "marke": MARKE, "betreff": "In einer Stunde geht's los", "betreff2": "",
     "wann": "Automation, Do 17.12.2026 08:00",
     "preheader": "Hier ist dein Zoom-Link.",
     "h1": "Um 09:00 starten wir", "unterzeile": "Neustart 2027",
     "notiz": "Automation 0€ Jahresplanung.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("um 09:00 Uhr starten wir. Hol dir einen Kaffee, öffne den Jahresplaner und komm rein."),
         knopf("Zum Workshop", ZOOM),
         absatz('Den Jahresplaner findest du <a href="%s" style="color:#12828c;">hier</a>.' % PLANER, True),
         gruss("Bis gleich,"),
     ]},
    {"datei": "E3-aufzeichnung-mba.html", "name": "Neustart 2027 E3 · Aufzeichnung + MBA (Do 17.12. abends)",
     "marke": MARKE, "betreff": "Deine Aufzeichnung, und was du jetzt mit dem Plan machst", "betreff2": "",
     "wann": "Automation, Do 17.12.2026 abends",
     "preheader": "Der Plan steht. Jetzt kommt der Teil, an dem es meistens hängt.",
     "h1": "Dein Plan steht", "unterzeile": "Neustart 2027 · die Aufzeichnung",
     "notiz": "Automation 0€ Jahresplanung. Aufzeichnungs-Link aus scripts/jahresplanung/.env.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("danke, dass du dabei warst. Hier ist die Aufzeichnung, sie bleibt offen:"),
         knopf("Zur Aufzeichnung", AUFZEICHNUNG),
         absatz("Wenn du jetzt auf dein Jahr schaust, hast du wahrscheinlich ein, zwei Monate, bei denen du denkst: "
                "Wie mache ich das eigentlich? Ein Launch im März, ein eigenes Angebot neben dem Network, ein "
                "Instagram, das dir Kontakte bringt."),
         absatz("Genau dafür ist meine <strong>Mum Business Academy</strong>. Dort setzen wir den Plan zusammen um, "
                "das ganze Jahr: dein Instagram, dein eigenes digitales Produkt und eine Woche, die neben der Familie "
                "Platz hat. Und du bist dabei nicht allein, wir treffen uns regelmässig live.", True),
         knopf("Die Academy ansehen", MBA),
         gruss("Herzlich,"),
         ps("P.S. Du hast schon einen meiner Kurse? Schreib mir, er wird angerechnet."),
     ]},
    {"datei": "E4-erst-mal-allein.html", "name": "Neustart 2027 E4 · Erst mal allein (Fr 18.12.)",
     "marke": MARKE, "betreff": "„Ich schau erst mal, wie weit ich allein komme“", "betreff2": "",
     "wann": "Automation, Fr 18.12.2026",
     "preheader": "Der Satz ist ehrlich. Und er kostet meistens ein halbes Jahr.",
     "h1": "Allein umsetzen?", "unterzeile": "Neustart 2027",
     "notiz": "Automation 0€ Jahresplanung. Ziel „MBA gekauft“ ganz unten.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("„Ich schau erst mal, wie weit ich allein komme.“ Diesen Satz höre ich von Frauen im Network immer "
                "wieder, und ich verstehe ihn gut. Dahinter steckt oft die Angst, dass es bei dir wieder nicht klappt."),
         absatz("Seit gestern hast du einen Plan. Allein umsetzen heisst jetzt: jeden Monat selbst herausfinden, wie "
                "ein Launch geht, wie dein eigenes Produkt entsteht und was du dafür postest. In der Academy machen "
                "wir aus deinem Plan Woche für Woche das, was zu tun ist, und du arbeitest an dem Monat, in dem du "
                "gerade bist.", True),
         knopf("Die Academy ansehen", MBA),
         gruss("Herzlich,"),
     ]},
    {"datei": "E5-vor-den-ferien.html", "name": "Neustart 2027 E5 · Vor den Ferien (So 20.12.)",
     "marke": MARKE, "betreff": "Bevor bei uns die Ferien anfangen", "betreff2": "",
     "wann": "Automation, So 20.12.2026",
     "preheader": "Eine letzte Mail zum Plan, dann ist Familienzeit.",
     "h1": "Bevor die Ferien anfangen", "unterzeile": "Neustart 2027",
     "notiz": "Automation 0€ Jahresplanung. Danach Ende der Strecke.",
     "bloecke": [
         absatz("Hallo %FIRSTNAME%"),
         absatz("morgen beginnen bei uns die Weihnachtsferien, und ich bin dann mit der Familie beschäftigt."),
         absatz("Wenn du im Januar mit deinem Plan nicht allein starten willst, schau dir die Academy vor den Ferien "
                "noch an. Dann steigst du im Januar direkt mit uns ein.", True),
         knopf("Die Academy ansehen", MBA),
         gruss("Ich wünsche dir schöne Festtage,"),
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
        seite = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "NEUSTART 2027").replace(
            "scripts/startklar/mails-bauen.py", "scripts/jahresplanung/mails-bauen.py")
        (ZIEL / m["datei"]).write_text(seite, encoding="utf-8")
        sk.umlaute_pruefen(m["datei"], seite)
        fehlt = [p for p in ("#ZOOM-LINK-FEHLT", "#AUFZEICHNUNG-FEHLT") if p in seite]
        print("✓", m["datei"], ("· fehlt: " + ", ".join(fehlt)) if fehlt else "")
        if "--hochladen" in sys.argv:
            basis, schluessel = ac_zugang()
            if m["datei"] in stand:   # Entwurf gibt es schon: nur die Nachricht ersetzen
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
                        textconstructor="external", html=seite, text=als_text(seite), **{"p[2]": 2}))
            kamp = ac_v1(basis, schluessel, "campaign_create", dict(absender, type="single", name=m["name"], sdate="",
                         status=0, public=0, tracklinks="all", **{"p[2]": 2, "m[%s]" % msg["id"]: 100}))
            stand[m["datei"]] = {"kampagne": kamp["id"], "nachricht": msg["id"], "name": m["name"]}
            stand_datei.write_text(json.dumps(stand, ensure_ascii=False, indent=1), encoding="utf-8")
            print("   AC-Entwurf: Kampagne", kamp["id"], "· Nachricht", msg["id"])


if __name__ == "__main__":
    main()
