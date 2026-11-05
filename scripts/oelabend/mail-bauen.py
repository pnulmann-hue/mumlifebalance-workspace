"""Öl-Abend: die sechs Nachfass-Mails und die Kopierseite dazu.

Bestellt (3) · Überschlafen (2) · Eigener Öl-Abend (1). Das Gerüst (Outlook-Tabellen, Farben, Fuss)
kommt aus scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert. Dieses Skript ist die
Quelle des Wortlauts.

    python scripts/oelabend/mail-bauen.py
-> outputs/doterra-strategie/oelabend/mail-*.html · oelabend-mails.html (Artifact, privat)

Die Ausgabe trägt Gruppen-Einladungen und das Video mit Unlisted-Hash und ist deshalb gitignored.
Wer noch nicht Kundin ist, braucht Patricias persönlichen Einstieg (/startersets/), der allgemeine
Shop-Link taugt nur für Kundinnen mit eigenem Login.
"""
import html
import importlib.util
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)
absatz, kasten, knopf, h2, ps, gruss = sk.absatz, sk.kasten, sk.knopf, sk.h2, sk.ps, sk.gruss

ZIEL = ROOT / "outputs" / "doterra-strategie" / "oelabend"

BEGLEITUNG = "https://claude.ai/artifact/WQAE68X16K6CvY8DUuLHa7"
SHOP = "https://shop.doterra.com/CH/de_CH/shop/home/"        # für Kundinnen mit eigenem Login
EINSTIEG = "https://mumlifebalance.ch/startersets/"          # für Neue: Patricias persönliche Links
OILACADEMY = "https://oil-academy.ch/"

# Gruppen-Einladungen und der Unlisted-Link stehen in scripts/oelabend/.env (gitignored, Repo public)
_ENV = {}
for _z in (ROOT / "scripts/oelabend/.env").read_text(encoding="utf-8").splitlines():
    if "=" in _z and not _z.startswith("#"):
        _k, _v = _z.split("=", 1)
        _ENV[_k.strip()] = _v.strip()
KUNDENGRUPPE, JAHRESGRUPPE = _ENV["KUNDENGRUPPE"], _ENV["JAHRESGRUPPE"]
MAMA_KIND, VIDEO_TREUE = _ENV["MAMA_KIND"], _ENV["VIDEO_TREUE"]

MARKE = "Mum Life Balance · Öl-Abend"


def link(text, ziel):
    return '<a href="%s" style="color:%s;font-weight:bold;">%s</a>' % (ziel, sk.PETROL, text)


MAILS = [
 {"datei": "mail-bestellt-1.html", "strecke": "Ich bestelle heute", "marke": MARKE,
  "warten": "am Tag nach dem Öl-Abend",
  "bedingung": "„Ich bestelle heute und bekomme das Buch …“ angekreuzt",
  "betreff": "Bevor du dein erstes Fläschchen aufmachst",
  "betreff2": "Das liegt für dich bereit, sobald dein Paket da ist",
  "preheader": "Ein Link, den du dir für den Tag aufheben solltest, an dem dein Paket kommt.",
  "h1": "Bevor du dein erstes Fläschchen aufmachst",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("danke dir nochmals für den Öl-Abend, und schön, bist du jetzt dabei. Das Buch „Kraft der Natur“ ist mein Geschenk an dich, darin kannst du jederzeit nachschlagen."),
    absatz("Wenn dein Paket kommt, stehst du erst mal vor einer Menge Fläschchen. Damit die nicht einfach schön im Regal stehen bleiben, begleite ich dich: Du wählst dein Set, und ab dann wartet jeden Tag ein kleiner Schritt auf dich, dazu meine Videos, Rezepte und Rollerideen."),
    knopf("Meine Begleitung öffnen", BEGLEITUNG),
    absatz("Pass auf: Öffne sie erst, wenn dein Paket da ist. Mit dem ersten Öffnen beginnt dein Tag 1. Und leg dir den Link auf den Startbildschirm, dann findest du ihn auch mit einem müden Kind auf dem Arm.", letzter=True),
    gruss("Herzlich,"),
    ps("Hast du eine Frage zu deiner Bestellung? Antworte einfach auf diese Mail."),
  ]},
 {"datei": "mail-bestellt-2.html", "strecke": "Ich bestelle heute", "marke": MARKE,
  "warten": "1 Woche nach der ersten Mail",
  "bedingung": "wie oben",
  "betreff": "Welches Fläschchen war schon offen?",
  "betreff2": "Eine Woche später: Was war schon offen?",
  "preheader": "Falls noch keines: Heute reicht ein einziger Tropfen.",
  "h1": "Welches Fläschchen war schon offen?",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("falls du jetzt ein bisschen ertappt nickst: Es ist völlig okay, wenn das Paket noch halb verpackt dasteht. Für heute reicht ein einziger Griff."),
    kasten(sk.P_ENG % "<strong>Mit der Hausapotheke oder dem Family Essentials Kit:</strong> 1 Tropfen Lemon in ein Glas Wasser, immer Glas oder Edelstahl, kein Plastik."
           + sk.P_ENG % "<strong>Mit der Kids Collection:</strong> heute Abend Calmer auf die Fusssohlen deines Kindes, kurz bevor das Licht ausgeht.",
           "#fdf1e6", rand=sk.ORANGE, kopf="Dein Griff für heute", kopffarbe=sk.ORANGE),
    h2("Du musst das nicht allein herausfinden"),
    absatz("In meiner " + link("Kundengruppe", KUNDENGRUPPE) + " teile ich Infos und das Unboxing meiner Bestellung. In " + link("Gesund durchs ganze Jahr", JAHRESGRUPPE) + " bekommst du Tipps, Rezepte und Ideen passend zur Jahreszeit. Für Fragen rund um die Kinder gibt es die Telegram-Gruppe " + link("dōTERRA Mama & Kind", MAMA_KIND) + "."),
    absatz("In der " + link("Oilacademy", OILACADEMY) + " warten ein Einsteigerkurs, Kundenwebinare und eine ganze Themenbibliothek auf dich, den Zugang hast du per Mail bekommen. Und einmal im Monat treffen wir uns zum Teamcall. Den Termin bekommst du von mir.", letzter=True),
    gruss("Herzlich,"),
    ps("Dein heutiger Schritt wartet schon in deiner " + link("Begleitung", BEGLEITUNG) + "."),
  ]},
 {"datei": "mail-bestellt-3.html", "strecke": "Ich bestelle heute", "marke": MARKE,
  "warten": "2 Wochen nach der zweiten Mail (3 Wochen nach dem Abend)",
  "bedingung": "wie oben",
  "betreff": "Bevor dein Lieblingsöl leer ist",
  "betreff2": "Wie Cumulus, nur für deine Öle",
  "preheader": "So bekommst du regelmässig Produkte gratis, und so richtest du es selbst ein.",
  "h1": "Bevor dein Lieblingsöl leer ist",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("nach drei Wochen weisst du langsam, welches Fläschchen bei euch am meisten unterwegs ist. Genau das ist der richtige Moment für die Treuebestellung. Sie funktioniert ähnlich wie Cumulus bei der Migros: Jedes Produkt hat einen PV-Wert, und für jede monatliche Bestellung bekommst du Punkte geschenkt, mit denen du später Produkte gratis holst."),
    kasten(sk.P_ENG % "<strong>Im 1. bis 3. Monat</strong> bekommst du 10 % als Punkte, danach steigt es Stufe für Stufe bis 30 %."
           + sk.P_ENG % "<strong>Für die nächste Stufe</strong> bestellst du 3 Monate lang für mindestens 50 PV. Ein Monat darunter ist nicht schlimm, er zählt einfach nicht mit."
           + sk.P_ENG % "<strong>Auch das Porto</strong> bekommst du als Punkte zurück."
           + sk.P_ENG % "<strong>Ab 125 PV</strong> im Monat gibt es das Produkt des Monats gratis dazu.",
           "#e4f3f4", rand=sk.PETROL, kopf="So kommst du zu den Punkten", kopffarbe=sk.PETROL),
    absatz("Deine Bestellung läuft dann mit einem festen Datum von selbst, und du kannst sie jeden Monat anpassen. Mein Tipp: Lass Alltägliches wie Zahnpasta, Shampoo oder Waschmittel laufen, auch wenn es nur 10 oder 20 PV sind. So bleibst du drin. Gut zu wissen: Wenn du kündigst, sind die Punkte und deine Stufe weg, und die Punkte verfallen nach 12 Monaten."),
    absatz("Was als Nächstes dazukommen soll, kannst du dir in deiner " + link("Begleitung", BEGLEITUNG) + " unter „Treue & Plan“ auf den Wunschzettel setzen. " + link("Im Video ab Minute 5:37", VIDEO_TREUE) + " erkläre ich dir alles nochmals."),
    knopf("Im Shop selbst einrichten", SHOP),
    gruss("Herzlich,"),
    ps("Hängst du beim Einrichten fest? Antworte einfach auf diese Mail, dann schauen wir es uns an."),
  ]},
 {"datei": "mail-ueberschlafen-1.html", "strecke": "Ich schlafe darüber", "marke": MARKE,
  "warten": "2 Tage nach dem Öl-Abend",
  "bedingung": "„Ich schlafe noch eine Nacht darüber“ angekreuzt",
  "betreff": "Hast du gut darüber geschlafen?",
  "betreff2": "Das wird die grosse Frage, wenn die Öle bei dir stehen",
  "preheader": "Die grosse Frage ist meistens, wann du im Alltag überhaupt daran denkst.",
  "h1": "Hast du gut darüber geschlafen?",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("danke dir nochmals für den Öl-Abend. Du hast angekreuzt, dass du noch eine Nacht darüber schlafen willst, und das finde ich ganz ganz gut so. Wer sich Zeit lässt, kauft am Ende das, was sie dann auch wirklich benutzt."),
    absatz("Angenommen, die Fläschchen stehen nächste Woche bei dir im Regal: Dann ist die grosse Frage meistens, wann du im Alltag überhaupt daran denkst. Sonst wird aus der Hausapotheke einfach ein sehr hübsches Regal."),
    absatz("Darum bekommst du von mir zu deinem Set meine Begleitung dazu: jeden Tag ein kleiner Schritt, dazu Videos, Rezepte und dein eigener Plan für morgens und abends, damit die Öle ihren festen Platz in deinem Tag finden."),
    knopf("Die Sets ansehen und bestellen", EINSTIEG),
    absatz("Und falls dir der Abend so gefallen hat, dass du ihn deinen Freundinnen gönnen magst: Ich komme auch zu dir, und als Dankeschön bekommst du von mir ein Gastgeberinnen-Geschenk. Antworte dafür einfach mit ABEND.", letzter=True),
    gruss("Herzlich,"),
    ps("Falls du lieber klein anfangen magst oder eine Frage hast: Antworte auf diese Mail. Und wenn es gerade nicht passt, ist das völlig okay. Kein Druck."),
  ]},
 {"datei": "mail-ueberschlafen-2.html", "strecke": "Ich schlafe darüber", "marke": MARKE,
  "warten": "4 Tage nach der ersten Mail (6 Tage nach dem Abend)",
  "bedingung": "wie oben, und bisher nicht bestellt",
  "betreff": "Welches Set passt zu euch?",
  "betreff2": "Falls es nur noch an dieser einen Frage hängt",
  "preheader": "Ein kurzer Vergleich, falls es nur noch an dieser Frage hängt.",
  "h1": "Welches Set passt zu euch?",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("falls es nur noch an dieser einen Frage hängt, hier ist die kurze Antwort."),
    kasten(sk.P_ENG % "<strong>Hausapotheke oder Family Essentials Kit:</strong> Die 10 Basisöle für die ganze Familie. Du setzt sie ganz individuell ein, zum Einatmen, auf der Haut oder ausgewählte auch innerlich, und mischst dir daraus eigene Roller und Sprays."
           + sk.P_ENG % "<strong>Kids Collection:</strong> 7 Roller, die bereits mit Kokosöl verdünnt sind. Du kannst sie sofort benutzen, zum Beispiel Calmer beim Zubettgehen oder Thinker bei den Hausaufgaben. doTERRA empfiehlt sie ab 3 Jahren.",
           "#e4f3f4", rand=sk.PETROL, kopf="Die zwei Wege", kopffarbe=sk.PETROL),
    absatz("Beide kommen mit meiner Begleitung, und du bekommst jeden Tag einen kleinen Schritt, bis es Gewohnheit ist."),
    knopf("Die Sets ansehen und bestellen", EINSTIEG),
    absatz("Das war meine letzte Mail zum Öl-Abend. Wenn du unsicher bist, welches Set zu euch passt, antworte einfach, dann schauen wir es zusammen an.", letzter=True),
    gruss("Herzlich,"),
  ]},
 {"datei": "mail-oelabend-1.html", "strecke": "Ich mache einen Öl-Abend", "marke": MARKE,
  "warten": "am Tag nach dem Öl-Abend",
  "bedingung": "„Ich möchte selbst einen Öl-Abend machen …“ angekreuzt",
  "betreff": "Dein Öl-Abend: Das ist alles, was du tun musst",
  "betreff2": "Wie geil, du machst einen Öl-Abend",
  "preheader": "Du lädst ein, ich bringe die Öle mit. Fehlen nur noch zwei Termine von dir.",
  "h1": "Dein Öl-Abend: Das ist alles, was du tun musst",
  "bloecke": [
    absatz("Hallo %FIRSTNAME%,"),
    absatz("wie geil ist das denn, dass du selbst einen Öl-Abend machen möchtest. Du musst dafür keine Expertin sein, das bin ich an dem Abend für dich."),
    kasten(sk.P_ENG % "<strong>Du:</strong> lädst deine Freundinnen ein und stellst den Raum, ein paar Stühle und etwas zu trinken für danach."
           + sk.P_ENG % "<strong>Ich:</strong> bringe die Öle, den Diffuser und die Unterlagen mit und führe durch den Abend, rund 45 bis 60 Minuten."
           + sk.P_ENG % "<strong>Dein Dankeschön:</strong> dein Gastgeberinnen-Geschenk von mir.",
           "#fdf1e6", rand=sk.ORANGE, kopf="So teilen wir uns das auf", kopffarbe=sk.ORANGE),
    h2("So lädst du am besten ein"),
    absatz("Lade ein bis zwei Wochen vorher ein, persönlich und mit Vornamen. Lade ruhig ein paar mehr ein, als Platz haben, denn es kommen nie alle. Das kannst du zum Beispiel schreiben:"),
    kasten(sk.P_ENG % "Ich mache am [Tag] um [Uhrzeit] einen kurzen Abend zu ätherischen Ölen, bei mir zu Hause, etwa eine Stunde. Ich hab grad an dich gedacht, weil du [Bezug]. Ich würde mich freuen, wenn du mein Gast bist. Und bring gern eine Freundin mit.",
           "#f6f2e7", kopf="Zum Kopieren", kopffarbe=sk.DUNKEL),
    absatz("Antworte mir einfach mit zwei Terminen, die dir passen, dann fixieren wir einen davon.", letzter=True),
    gruss("Ich freu mich,"),
  ]},
]


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    daten = []
    for m in MAILS:
        m = dict(m, wann=m["warten"], notiz="Bedingung: " + m["bedingung"])
        seite = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "ÖL-ABEND").replace(
            "scripts/startklar/mails-bauen.py", "scripts/oelabend/mail-bauen.py")
        (ZIEL / m["datei"]).write_text(seite, encoding="utf-8")
        sk.umlaute_pruefen(m["datei"], seite)
        daten.append({k: m[k] for k in ("datei", "strecke", "warten", "bedingung", "betreff", "betreff2", "preheader")} | {"html": seite})
    alt = ZIEL / "mail-ueberschlafen.html"
    if alt.exists():
        alt.unlink()   # abgelöst durch mail-ueberschlafen-1.html

    vorlage = (pathlib.Path(__file__).with_name("mails-vorlage.html")).read_text(encoding="utf-8")
    json_daten = json.dumps(daten, ensure_ascii=False).replace("</", "<\\/")
    (ZIEL / "oelabend-mails.html").write_text(vorlage.replace("/*DATEN*/[]", json_daten), encoding="utf-8")

    # Lesefassung für die Text-Prüfung (ohne Gerüst), wird nicht ausgeliefert
    import re
    teile = ["---\ntags: [doterra, mail]\n---\n\n# Öl-Abend · Nachfass-Mails\n\nQuelle: `scripts/oelabend/mail-bauen.py`, dort ändern.\n"]
    for m in MAILS:
        roh = "\n\n".join(re.sub(r"<[^>]+>", " ", b) for b in m["bloecke"])
        teile.append("## %s\n\n**Strecke:** %s · **Wann:** %s\n\n**Betreff:** %s\n\n%s\n" % (
            m["h1"], m["strecke"], m["warten"], m["betreff"], html.unescape(re.sub(r"[ \t]+", " ", roh)).strip()))
    (ZIEL / "2026-11-03-mail-ueberschlafen.md").write_text("\n".join(teile), encoding="utf-8")
    print(len(MAILS), "Mails ->", ZIEL / "oelabend-mails.html")


if __name__ == "__main__":
    main()
