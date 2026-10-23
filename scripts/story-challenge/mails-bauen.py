"""
Baut die Mailreise der Story-Challenge — von der Bestätigung bis zur Übergabe
an die Engine — als fertige Mail-HTMLs, als Text und als Cockpit-Dokumente.

  python scripts/story-challenge/mails-bauen.py
  # danach: ArtifactData batch set -> Sammlung "mailentwuerfe",
  #         je Datei aus outputs/cockpit/abgleich/mailentwuerfe/story-challenge-*.json

Ausgabe:
  outputs/funnels/story-challenge-nurture/   mail-NN-*.html · index.html (Kopierseite) · story-challenge-mails.md (Text)
  outputs/cockpit/abgleich/mailentwuerfe/    story-challenge-NN.json (automation "45")

Das Gerüst (Kopf, Farben, Fuss, Outlook-Tabellen, Umlaut-Wächter) kommt aus
scripts/startklar/mails-bauen.py und wird importiert, nicht kopiert.

Pitch-Ziel ist die Instagram-Kundenmaschine (333), weil das Workbook sie dreimal
nennt (S. 3, Tag 6, Schlussseite). 🚨 Nicht Startklar pitchen: an dessen Kasse
hängt die Kundenmaschine als Upsell für 97 — wer beides sieht, wartet ab dann
auf den tieferen Preis (Patricia, 21.10.2026: „ist da jetzt startklar in den
mails eine verwirrung?“).

Hormozi ist der Struktur-Layer, Patricias Stimme der Ton: erst helfen (Tag 0–7),
nach dem Gewinn das neue Problem benennen (Tag 8), dann EIN Angebot mit EINEM
Aufruf (Tag 10–15), P.S. als zweiter Einstieg, wer nicht passt, wird
ausgeladen. Ganze Sätze statt Stakkato.
"""
import html
import importlib.util
import json
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

ZIEL = ROOT / "outputs" / "funnels" / "story-challenge-nurture"
COCKPIT = ROOT / "outputs" / "cockpit" / "abgleich" / "mailentwuerfe"

TELEGRAM = "https://t.me/+S-4YWyCtH45mZDE0"
INSTAGRAM = "https://www.instagram.com/mumlifebalance_patricia_ulmann/"
IKM = "https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/"
# 🚨 Wie bekommt sie das PDF? Die bisherige Bestätigung verlinkt nur die
#    Telegram-Gruppe. Leer lassen, wenn das Workbook dort oder auf der
#    ThriveCart-Dankeseite liegt — dann fällt der Knopf weg.
WORKBOOK = ""

absatz, kasten, liste, knopf, h2, ps, gruss, merken = (
    sk.absatz, sk.kasten, sk.liste, sk.knopf, sk.h2, sk.ps, sk.gruss, sk.merken)
P_ENG, PETROL, ORANGE = sk.P_ENG, sk.PETROL, sk.ORANGE


def link(text, ziel):
    return '<a href="%s" style="color:%s;">%s</a>' % (ziel, PETROL, text)


START_PUNKTE = [
    "<strong>1 · Tritt der Telegram-Gruppe bei</strong> und stell dich und dein Business mit "
    "ein paar Worten vor. Dort tauschen wir uns die ganze Woche aus.",
    "<strong>2 · Öffne dein Workbook</strong> und lies die Seite mit den sechs Story-Arten. "
    "Die brauchst du an jedem der sieben Tage.",
    "<strong>3 · Heute ist Tag 1, deine Geschichte.</strong> Du nimmst deine Leute auf eine kleine "
    "Zeitreise durch ein Stück deines Lebens mit und leitest am Schluss zu dem über, was du "
    "anbietest. Auf Seite 7 steht ein ganzes Beispiel mit zehn Storys zum Abschauen.",
]

MAILS = [
    # ---------------------------------------------------------------- Tag 0
    {
        "datei": "mail-00-bestaetigung.html", "tag": "0", "warten": "sofort",
        "marke": "mumlifebalance · Story-Challenge",
        "betreff": "Deine Story-Challenge: Heute ist Tag 1",
        "betreff2": "Hier ist dein Start in die 7-Tage-Story-Challenge",
        "wann": "sofort nach der Anmeldung (ersetzt „Story-Challenge Bestätigung“)",
        "preheader": "Telegram-Gruppe, Workbook und deine Aufgabe für heute.",
        "h1": "Schön, bist du dabei",
        "unterzeile": "Sieben Tage, jeden Tag eine kleine Story-Aufgabe.",
        "notiz": """Ersetzt die bisherige Bestätigung. Dort stand „Mein erster Impuls mit dem
Workbook kommt dann am 1.9“ — das Datum ist vorbei, und den Impuls gab es nicht.
Jetzt startet die Challenge am Tag der Anmeldung, die Mails an Tag 2, 4 und 7
begleiten sie. Job: anfangen lassen. Kein Verkauf.
🚨 Workbook-Link fehlt, siehe WORKBOOK im Skript.""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("wie schön, dass du dir die nächsten sieben Tage für deine Storys nimmst. Ich weiss, "
                   "wie es sich anfühlt, wenn man jeden Tag etwas hochlädt und es bleibt einfach still: "
                   "keine Antwort, keine Nachricht, höchstens ein paar Herzchen von Leuten, die man "
                   "sowieso kennt."),
            absatz("Ich sag dir ehrlich, woran es meistens liegt: Leute antworten, wenn sie sich in deiner "
                   "Story wiederfinden und merken, dass du ihren Alltag kennst. Genau das übst du jetzt "
                   "eine Woche lang, jeden Tag mit einer kleinen Aufgabe aus deinem Workbook."),
            liste("Drei Dinge für deinen Start", START_PUNKTE),
            knopf("Zur Telegram-Gruppe", TELEGRAM),
        ] + ([absatz("Und hier liegt dein Workbook, falls du es gleich öffnen möchtest:", True),
              knopf("Mein Workbook öffnen", WORKBOOK)] if WORKBOOK else []) + [
            kasten(P_ENG % ("Die Challenge ist kein Wettlauf. Wenn du einen Tag verpasst, machst du "
                            "einfach am nächsten weiter, und jede Aufgabe funktioniert auch in drei "
                            "Wochen noch."),
                   "#fdf1e6", rand=ORANGE, kopf="Kein Stress", kopffarbe=ORANGE),
            absatz("In zwei Tagen schreib ich dir wieder, mit dem Gedanken, an dem die meisten an Tag 2 "
                   "hängen bleiben. Und wenn du vorher eine Frage hast, antworte einfach auf diese Mail "
                   "oder schreib mir auf Instagram.", True),
            gruss("Ich freu mich auf deine Storys,"),
            ps("P.S. Halt durch bis Tag 7. Viele hören nach drei Tagen auf, und das ist schade, weil die "
               "ersten Antworten oft erst kommen, wenn die Leute dich ein paar Tage hintereinander in "
               "deinen Storys gesehen haben."),
        ],
    },
    # ---------------------------------------------------------------- Tag 2
    {
        "datei": "mail-02-alltag.html", "tag": "2", "warten": "+2 Tage",
        "marke": "Story-Challenge · Tag 2",
        "betreff": "„Ich hab doch nichts Besonderes zu erzählen“",
        "betreff2": "Der Gedanke, an dem Tag 2 meistens hängen bleibt",
        "wann": "2 Tage nach der Bestätigung",
        "preheader": "Warum dein ganz normaler Dienstag die beste Story ist, die du hast.",
        "h1": "Dein Alltag reicht",
        "unterzeile": "Tag 2 der Story-Challenge",
        "notiz": """Job: dranbleiben. Kein Verkauf.
Hormozi: den Einwand aussprechen, bevor sie ihn denkt · ein Aufruf (Antwort auf die Mail),
damit Antworten eingehen — das hilft auch der Zustellbarkeit der Pitch-Mails später.""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("heute ist in deinem Workbook Tag 2 dran, und genau hier höre ich jedes Mal denselben "
                   "Satz: „Aber ich hab doch nichts Besonderes zu erzählen.“ Bei mir war das am Anfang "
                   "auch so. Mit vier Kindern fühlt sich der eigene Tag oft an wie eine Liste, die man "
                   "abarbeitet, und wer will sich schon eine Liste anschauen?"),
            absatz("Was ich erst später verstanden habe: Leute bleiben bei deinen Storys, wenn sie sich "
                   "darin wiederfinden. Dafür reicht ein ganz normaler Moment, den sie selbst auch "
                   "kennen, und davon hattest du heute wahrscheinlich schon ein paar."),
            liste("Fünf Momente, die du heute wahrscheinlich schon hattest", [
                "dein Lieblingsessen nach einem langen Tag",
                "dein Morgen zwischen Brotdosen und Kaffee",
                "ein Satz, den dein Kind heute gesagt hat",
                "eine Situation, die dich genervt oder berührt hat",
                "ein kleiner Aha-Moment zwischendurch",
            ]),
            h2("Und dann kommt die Brücke zu deinem Thema"),
            absatz("Der Trick an Tag 2 ist der zweite Schritt. Du zeigst etwas aus deinem Alltag, setzt "
                   "einen Umfrage-Sticker drauf, und in der nächsten Story erzählst du, was das mit deinem "
                   "Thema zu tun hat. Im Workbook ist das der Proteinriegel, mit dem man bis zum "
                   "Abendessen durchhält, und gleich danach ein Tipp, was am Nachmittag mit dem "
                   "Blutzucker passiert, wenn es stattdessen Chips sind. So bleibt die Story persönlich "
                   "und hat trotzdem mit deinem Business zu tun."),
            merken("Der Satz für heute",
                   "„Wenn du nur dein Produkt zeigst, bleibst du Verkäuferin. Wenn du Einblick gibst, "
                   "wirst du greifbar.“",
                   "Und greifbar ist der erste Schritt zu Vertrauen."),
            absatz("Magst du mir verraten, welchen Moment du heute nimmst? Antworte einfach auf diese "
                   "Mail, ein Satz reicht. Ich lese jede Antwort selbst.", True),
            gruss("Bis übermorgen,"),
        ],
    },
    # ---------------------------------------------------------------- Tag 4
    {
        "datei": "mail-04-halbzeit.html", "tag": "4", "warten": "+2 Tage",
        "marke": "Story-Challenge · Halbzeit",
        "betreff": "Mein erstes Network hab ich nach drei Jahren aufgegeben",
        "betreff2": "Halbzeit — und warum ein Misserfolg deine stärkste Story sein kann",
        "wann": "2 Tage nach Mail Tag 2",
        "preheader": "Warum genau diese Story mehr Vertrauen schafft als jedes Erfolgsbild.",
        "h1": "Halbzeit",
        "unterzeile": "Tag 3 und 4 der Story-Challenge",
        "notiz": """Job: dranbleiben und Nähe. Kein Verkauf.
Hormozi: eigene Schwäche zeigen (erstes Network aufgegeben, belegt in der
Startklar-Salespage, Block 3) · ein Geschenk ohne Gegenleistung (Story-Feedback,
steht so im Workbook auf S. 19).""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("mehr als die Hälfte ist geschafft, und jetzt kommen die zwei Tage, vor denen die "
                   "meisten am meisten Respekt haben. An Tag 3 erzählst du von etwas, das nicht gut "
                   "gelaufen ist, und an Tag 4 zeigst du, was du in deinem Bereich weisst."),
            absatz("Ich fang gleich bei mir an, damit du siehst, wie das aussehen kann. Mein erstes "
                   "Network war ein anderes als heute. Ich war drei Jahre dabei, hab Produktbilder "
                   "gepostet, eins nach dem anderen, und mich jedes Mal gewundert, warum nichts "
                   "zurückkommt. Irgendwann hab ich aufgegeben."),
            absatz("Ganz ehrlich, ich war damals ein wandelnder Katalog, und einem Katalog schreibt "
                   "niemand zurück. Heute bin ich dankbar für diese drei Jahre, weil ich dort gelernt "
                   "habe, dass Leute einem Menschen folgen, bei dem sie merken, dass er ihren Alltag kennt."),
            liste("So baust du deine Story an Tag 3", [
                "Was ist passiert, und was hat dir damals gefehlt?",
                "Welche drei Dinge hätte es gebraucht? Am besten genau die drei, die du heute in "
                "deinem Angebot weitergibst.",
                "Warum bist du heute dankbar dafür?",
                "Und wie hilft dein Angebot anderen, sich diesen Umweg zu sparen?",
            ]),
            kasten(P_ENG % ("Erzähl nur, was du verarbeitet hast. Eine Geschichte mitten aus dem Chaos "
                            "heraus fühlt sich für dich und für die, die zuschauen, schwer an."),
                   "#fdf1e6", rand=ORANGE, kopf="Wichtig", kopffarbe=ORANGE),
            h2("Mein Angebot an dich"),
            absatz("Du möchtest wissen, wie eine deiner Storys ankommt? Dann verlinke mein Profil "
                   "<strong>@mumlifebalance_patricia_ulmann</strong> in deiner Story und schreib mir auf "
                   "Instagram, welche ich mir anschauen soll. Ich schau sie mir an und sag dir, was schon "
                   "gut funktioniert und was ich beim nächsten Mal anders machen würde."),
            knopf("Zu meinem Instagram", INSTAGRAM),
            gruss("Du machst das gut,"),
        ],
    },
    # ---------------------------------------------------------------- Tag 7
    {
        "datei": "mail-07-geschafft.html", "tag": "7", "warten": "+3 Tage",
        "marke": "Story-Challenge · geschafft",
        "betreff": "Welche deiner Storys hat eine Antwort bekommen?",
        "betreff2": "Sieben Tage geschafft",
        "wann": "3 Tage nach Mail Tag 4",
        "preheader": "Eine Frage an dich, bevor ich dir morgen etwas über dein Profil erzähle.",
        "h1": "Sieben Tage geschafft",
        "notiz": """Job: den Gewinn benennen lassen. Kein Verkauf.
Hormozi „Pain is the pitch“ mit Ausnahme: nach einem Gewinn darf man nur
verkaufen, wenn der Gewinn ein NEUES Problem geschaffen hat. Diese Mail holt den
Gewinn, Tag 8 benennt das neue Problem. Antworten hier sind Kundenstimmen —
nur mit Freigabe verwenden (context/kundinnen-geschichten.md).""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("eine Woche ist vorbei, und egal, ob du alle sieben Aufgaben gepostet oder ein paar "
                   "davon erst gelesen und im Kopf behalten hast: beides zählt. Das Wichtigste hast du "
                   "trotzdem gemerkt, nämlich dass Storys anders wirken, sobald du selbst darin vorkommst."),
            absatz("Ich hab heute nur eine Frage an dich, und ich meine sie wirklich als Frage:"),
            merken("Meine Frage an dich",
                   "Welche Story hat dir diese Woche eine Antwort, eine Nachricht oder eine Reaktion "
                   "gebracht?",
                   "Antworte einfach auf diese Mail. Ein Satz reicht, und ich lese jede Antwort selbst."),
            absatz("Mit deiner Antwort kann ich dir viel genauer sagen, wo du als Nächstes ansetzt, als es "
                   "jede Vorlage könnte, weil ich dann weiss, was bei dir schon funktioniert."),
            absatz("Und falls noch nichts zurückgekommen ist, ist das nach einer Woche völlig normal. Viele "
                   "schauen deine Storys zum ersten Mal bewusst an und brauchen ein paar Tage, bis sie "
                   "sich trauen zu schreiben. Mach einfach mit den Fragen von Tag 6 weiter, also mit "
                   "Fragen, die nichts mit deinem Angebot zu tun haben. Die sind am leichtesten zu "
                   "beantworten.", True),
            gruss("Ich bin gespannt,"),
            ps("P.S. Morgen schreib ich dir, warum es bei vielen nach dieser Woche trotzdem wieder still "
               "wird und was das mit deinem Profil zu tun hat."),
        ],
    },
    # ---------------------------------------------------------------- Tag 8
    {
        "datei": "mail-08-profil.html", "tag": "8", "warten": "+1 Tag",
        "marke": "Story-Challenge · danach",
        "betreff": "Warum es nach der Challenge oft wieder still wird",
        "betreff2": "Und dann tippen sie auf dein Profil",
        "wann": "1 Tag nach Mail Tag 7",
        "preheader": "Deine Storys bringen Leute auf dein Profil. Was sehen sie dort?",
        "h1": "Und dann tippen sie auf dein Profil",
        "notiz": """Job: das neue Problem benennen, das der Gewinn geschaffen hat.
Noch kein Angebot, nur die Ankündigung („übermorgen zeig ich dir …“) als offene Schleife.
Die 600 Seiten Canva stehen so im Workbook (Tag 6).""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("nach einer Woche Storys passiert bei vielen genau das, was passieren soll: Es kommen "
                   "die ersten Reaktionen, und ein paar Leute tippen auf dein Profilbild, weil sie wissen "
                   "wollen, wer du eigentlich bist. In diesem Moment entscheidet sich, ob sie bleiben."),
            absatz("Und was sehen sie, wenn sie draufklicken? Bei vielen Network-Mamas ein Profil voller "
                   "Produktbilder, eine Bio mit dem Namen der Firma und ein paar Highlights, die seit "
                   "Monaten niemand mehr angefasst hat. Die Story hat gerade Vertrauen aufgebaut, und das "
                   "Profil fühlt sich dann an wie ein Katalog."),
            h2("Das zweite Problem kommt in Woche zwei"),
            absatz("Solange dir das Workbook jeden Tag eine Aufgabe gibt, läuft es. In der zweiten Woche "
                   "sitzt du dann wieder vor dem Handy und überlegst, was du heute erzählen sollst. "
                   "„Was poste ich jetzt?“ ist die Frage, die ich von Network-Mamas am häufigsten höre."),
            absatz("Ich hab am Anfang über 600 Seiten in Canva mit Story-Ideen gefüllt und trotzdem jeden "
                   "Morgen gesucht. Erst als mein Thema, meine Zielgruppe und meine Rolle klar waren, "
                   "kamen die Ideen fast von allein, weil ich wusste, worüber ich rede und für wen."),
            liste("Drei Fragen zu deinem Profil", [
                "Weiss eine Fremde nach zehn Sekunden auf deinem Profil, wobei du hilfst?",
                "Findet sie dort einen nächsten Schritt, wenn sie nach deiner Story vorbeischaut, "
                "also einen Link, ein kleines Geschenk oder ein Highlight, das sie weiterführt?",
                "Weisst du heute schon, worüber du nächste Woche erzählst, ohne suchen zu müssen?",
            ]),
            absatz("Wenn du bei einer davon zögerst, bist du in guter Gesellschaft, denn genau diesen Teil "
                   "kann eine einzelne Story nicht lösen. Übermorgen zeig ich dir, wie ich das bei mir "
                   "gelöst habe.", True),
            gruss("Liebe Grüsse,"),
        ],
    },
    # ---------------------------------------------------------------- Tag 10
    {
        "datei": "mail-10-pitch.html", "tag": "10", "warten": "+2 Tage",
        "marke": "Instagram-Kundenmaschine",
        "betreff": "Vom Produktkatalog zum Schaufenster",
        "betreff2": "Mein nächster Schritt für dich nach der Story-Challenge",
        "wann": "2 Tage nach Mail Tag 8",
        "preheader": "Wie aus deinen Storys, deinem Profil und deinen Beiträgen ein System wird.",
        "h1": "Dein Instagram als Schaufenster",
        "notiz": """Der Pitch. EIN Angebot, EIN Aufruf.
Inhalt aus der Schlussseite des Workbooks (S. 20) und der Willkommensmail der
Kundenmaschine (Automation 44): alle Module sofort offen, Telegram-Gruppe,
Antworten Di und Do. Bewusst NICHT genannt: „8 Wochen“ und „4 Live Calls“ —
beides steht in älteren Texten, ob es heute so läuft, ist nicht belegt.
Hormozi: wer nicht passt, wird ausgeladen.
Copywriting-Skill (23.10.): Stufe 3–4, Lead = Promise + Differenzierung (Schaufenster).
Beweis = Satz einer Käuferin vor dem Kauf (ZIELGRUPPE.md, Interview D2, anonym).
„Das ist nicht dabei“-Zeile Pflicht, weil eine Kundin nach Teamaufbau-Tipps gefragt hat (D4).
Ratenzahlung bewusst nicht genannt — in ThriveCart nicht geprüft.""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("in deinem Workbook hab ich dir die Instagram-Kundenmaschine schon ein paar Mal "
                   "erwähnt. Heute erzähl ich dir, was drin ist, damit du in Ruhe entscheiden kannst, "
                   "ob sie dein nächster Schritt ist."),
            absatz("Die Story-Challenge hat dir gezeigt, wie Storys Gespräche eröffnen. In der "
                   "Instagram-Kundenmaschine baust du alles darum herum auf: dein Profil, deine Beiträge "
                   "und den Weg, auf dem aus einem Gespräch eine Anfrage wird."),
            liste("Was du in der Instagram-Kundenmaschine aufbaust", [
                "<strong>deine Themen</strong>, über die du immer wieder erzählen kannst, damit du jede "
                "Woche weisst, was dran ist",
                "<strong>Beiträge und Storys</strong>, die so aufgebaut sind, dass Menschen dir vertrauen",
                "ein <strong>Profil</strong>, das vom Produktkatalog zum Schaufenster für dein Wissen wird",
                "ein <strong>kostenloses Geschenk</strong>, mit dem Interessierte auf deine Liste kommen, "
                "und ein Angebot, das im Hintergrund weiterverkauft, auch wenn du gerade bei den Kindern bist",
            ]),
            merken("Was mir eine Teilnehmerin vor dem Kauf geschrieben hat",
                   "„Ich habe es mir lange überlegt, ob es das Richtige für mich ist. Da meine "
                   "Strategien bisher nicht funktioniert haben mit Online-Verkäufen, bin ich jetzt "
                   "auch dabei.“",
                   "Wenn du dich darin wiederfindest, bist du hier richtig."),
            h2("So läuft es"),
            absatz("Alle Module sind ab dem Kauf freigeschaltet, und du gehst in deinem eigenen Tempo "
                   "durch, so wie es in deinen Alltag passt. Deine Fragen stellst du in der "
                   "Telegram-Gruppe, und dort antworte ich dir jeden Dienstag und Donnerstag persönlich."),
            h2("Für wen sie ist"),
            absatz("Sie ist für dich, wenn du im Network bist, Instagram ernsthaft für dein Business "
                   "nutzen willst und bereit bist, ein paar Wochen an deinem Fundament zu arbeiten. Wenn "
                   "du auf den einen Beitrag hoffst, der über Nacht durch die Decke geht, ist sie ehrlich "
                   "nicht das Richtige für dich."),
            absatz("Und damit es keine Missverständnisse gibt: Teamaufbau und Tipps, wie du neue Leute "
                   "für dein Network gewinnst, sind nicht dabei. Dafür hast du in deinem Network ja "
                   "schon deine Upline und dein Team."),
            kasten(P_ENG % ("Die Instagram-Kundenmaschine kostet <strong>333 Franken</strong>, und du "
                            "kannst sofort anfangen."),
                   "#e4f3f4", rand=PETROL, kopf="Preis"),
            knopf("Zur Instagram-Kundenmaschine", IKM),
            gruss("Herzlich,"),
            ps("P.S. Wenn du unsicher bist, ob sie zu dir passt, antworte mir einfach mit zwei Sätzen, wo "
               "du gerade stehst. Ich sag dir ehrlich, ob sie jetzt der richtige Schritt für dich ist."),
        ],
    },
    # ---------------------------------------------------------------- Tag 12
    {
        "datei": "mail-12-einwand.html", "tag": "12", "warten": "+2 Tage",
        "marke": "Instagram-Kundenmaschine",
        "betreff": "„Du bist so strukturiert, ich bin so chaotisch“",
        "betreff2": "Ich bin die, die hundert Sachen gleichzeitig anfängt",
        "wann": "2 Tage nach dem Pitch",
        "preheader": "Was ich einer Teilnehmerin nach der Story-Challenge geantwortet hätte.",
        "h1": "Struktur kann man übernehmen",
        "notiz": """Einwand plus Beweis (Copywriting-Skill, 23.10.).
Der Einwand ist echt und fiel NACH einer Story-Challenge (ZIELGRUPPE.md, Interview D4) —
das ist aber Patricias Nacherzählung, deshalb „sinngemäss“ und nicht als Zitat.
„Hundert Sachen gleichzeitig anfangen“ = Patricias eigene Schwäche (ZIELGRUPPE.md).
Beweis = Wortlaut von Kundin B (MBA nach der Kundenmaschine, schriftlich, anonym).
Bewusst NICHT mehr die Frau, die krank im Bett verkauft hat: die steht live in
„Loop 6 - IKM (333)“ (Automation 78) und käme sonst zweimal.
Wer inzwischen gekauft hat (Tag 39), ist über das Ziel schon draussen.""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("nach einer Story-Challenge hat mir eine Teilnehmerin sinngemäss geschrieben: „Du bist "
                   "so strukturiert, ich bin so chaotisch.“ Und ich musste lachen, weil ich die bin, die "
                   "hundert Sachen gleichzeitig anfängt und die Hälfte davon irgendwo liegen lässt."),
            absatz("Gerade weil ich so bin, hab ich mir meine Struktur Schritt für Schritt als System "
                   "gebaut. Genau dieses System übernimmst du in der Instagram-Kundenmaschine und füllst "
                   "es mit deinem Thema und deinem Alltag, und das Ausdenken hab ich dir damit schon "
                   "abgenommen."),
            merken("Warum eine Frau mit mir weitergegangen ist",
                   "„weil du aus deinen eigenen Erfahrungen sprichst und in einer ähnlichen Situation "
                   "bist, wie ich auch. Mehrere Kinder, Network, eigene Selbständigkeit“",
                   "Das hat sie mir nach der Kundenmaschine geschrieben."),
            h2("Und die Zeit?"),
            absatz("Ich hab mein System neben vier Kindern gebaut, und gerade weil die Zeit knapp ist, "
                   "lohnt es sich, einmal ein Fundament zu legen. Dann musst du nicht mehr jeden Morgen "
                   "neu überlegen, was du heute postest, und die Stunden, die du hast, gehen in das, was "
                   "wirklich etwas bringt."),
            knopf("Ja, ich bau meine Kundenmaschine", IKM),
            gruss("Liebe Grüsse,"),
            ps("P.S. Die Instagram-Kundenmaschine kostet 333 Franken, und alle Module sind sofort offen."),
        ],
    },
    # ---------------------------------------------------------------- Tag 15
    {
        "datei": "mail-15-letzte.html", "tag": "15", "warten": "+3 Tage",
        "marke": "Instagram-Kundenmaschine",
        "betreff": "Was hält dich noch zurück?",
        "betreff2": "Zum Schluss der Story-Challenge",
        "wann": "3 Tage nach Mail Tag 12 · danach Übergabe an die Engine",
        "preheader": "Meine letzte Mail zur Kundenmaschine, danach geht es mit anderen Themen weiter.",
        "h1": "Deine Entscheidung",
        "notiz": """Letzte Mail der Reise, ohne Druck und ohne erfundene Frist.
Danach: 5 Tage warten, dann den Tag setzen, der „Automation 0€ Produkt“ (Loop 1,
Automation 72) auslöst — wie am Ende der Startklar-Strecke. Loop 6 bleibt an:
er kommt erst nach Loop 1 bis 5, gut zwei Monate später.
Antworten auf diese Mail persönlich beantworten.
Copywriting-Skill (23.10.): Einwand „Ich lasse es mal weiterlaufen“ ist echt gehört
(ZIELGRUPPE.md, Interview D3) und wird nach Patricias Linie beantwortet — selbst
lernbar, braucht mehr Zeit, kein Investitionsdruck.""",
        "bloecke": [
            absatz("Hey %FIRSTNAME%,"),
            absatz("vor gut zwei Wochen hast du mit der Story-Challenge angefangen. Das ist heute meine "
                   "letzte Mail zur Instagram-Kundenmaschine, danach schreib ich dir wieder über andere "
                   "Themen rund um dein Business als Network-Mama."),
            absatz("Aufschwatzen möchte ich dir nichts. Die Instagram-Kundenmaschine ist für die Frauen, "
                   "die gemerkt haben, dass ihre Storys etwas auslösen, und die das jetzt nicht wieder "
                   "einschlafen lassen wollen."),
            absatz("Vielleicht denkst du gerade, was mir eine Frau einmal geschrieben hat: „Ich lasse es "
                   "mal so weiterlaufen und schaue, wie weit ich selbst komme.“ Das ist ein ehrlicher Weg, "
                   "und du kannst dir wirklich alles selbst beibringen. Es braucht dann einfach mehr Zeit. "
                   "Die Frage ist nur, wie lange du noch allein dranbleiben willst."),
            liste("Zwei ehrliche Fragen an dich", [
                "Willst du in drei Monaten immer noch jeden Morgen überlegen, was du postest?",
                "Hat dir jemand nach einer deiner Storys geschrieben, und du weisst gerade nicht, wie "
                "es mit dieser Person weitergeht?",
            ]),
            absatz("Wenn du bei einer davon merkst, dass du etwas ändern willst, ist jetzt ein guter "
                   "Moment dafür."),
            knopf("Zur Instagram-Kundenmaschine", IKM),
            absatz("Und wenn es gerade nicht passt, weil das Geld knapp ist oder der Kopf voll, ist das "
                   "völlig in Ordnung. Antworte mir einfach, was dich zurückhält. Manchmal gibt es einen "
                   "kleineren Schritt, der im Moment besser zu dir passt.", True),
            gruss("Danke, dass du dabei warst,"),
        ],
    },
]


# --- Text-Fassung -------------------------------------------------------------

def als_text(m):
    roh = "\n".join(m["bloecke"])
    roh = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                 lambda x: "%s: %s" % (re.sub("<[^>]+>", "", x.group(2)).strip(), x.group(1))
                 if x.group(1) not in x.group(2) else x.group(1), roh, flags=re.S)
    roh = re.sub(r"<br\s*/?>", "\n", roh)
    roh = re.sub(r"</(p|h2|tr|table)>", "\n\n", roh)
    roh = re.sub(r"<[^>]+>", "", roh)
    roh = html.unescape(roh)
    zeilen = [z.strip() for z in roh.splitlines()]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(zeilen)).strip()
    # Knopf erkennbar machen: Zeile „Text: URL“ ohne Satzzeichen davor
    return text.replace("Patricia\n", "Patricia\n", 1)


# --- Prüfung gegen die Blackliste ------------------------------------------------

def blackliste():
    spec2 = importlib.util.spec_from_file_location("tp", ROOT / "scripts/cockpit/texte-pruefen.py")
    tp = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(tp)
    return [(re.compile(m), name) for m, name in tp.KONTRAST + tp.SCHWER + tp.FLOSKELN]


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    COCKPIT.mkdir(parents=True, exist_ok=True)
    for alt in ZIEL.glob("mail-*.html"):
        alt.unlink()
    muster = blackliste()
    karten, beanstandet, funde = [], 0, 0
    md = ["---", "tags: [funnel, mailreise, story-challenge]", "---", "",
          "# Story-Challenge — Mailreise (Textfassung)", "",
          "> Erzeugt von `scripts/story-challenge/mails-bauen.py`. Änderungen dort, nicht hier.",
          "> Automation „0€ Story Challenge“ (45). Pitch: Instagram-Kundenmaschine 333.", ""]
    for i, m in enumerate(MAILS):
        fertig = sk.bauen(m).replace("NACHKAUF-STRECKE STARTKLAR", "MAILREISE STORY-CHALLENGE").replace(
            "ERZEUGT von scripts/startklar/mails-bauen.py", "ERZEUGT von scripts/story-challenge/mails-bauen.py")
        beanstandet += len(sk.umlaute_pruefen(m["datei"], fertig))
        text = als_text(m)
        for rx, name in muster:
            for f in rx.finditer(text):
                funde += 1
                print("  ⚠ %s · %s: „%s“" % (m["datei"], name, f.group(0)[:80]))
        (ZIEL / m["datei"]).write_text(fertig, encoding="utf-8")
        kennung = re.sub(r"[^a-z0-9]+", "", m["datei"].lower())
        karten.append(sk.KARTE.format(
            tag=m["tag"], h1=m["h1"], warten=m["warten"],
            betreff=html.escape(m["betreff"], quote=False),
            betreff_roh=html.escape(m["betreff"], quote=True),
            datei=m["datei"], id=kennung))
        doc = {
            "automation": "45", "automationName": "0€ Story Challenge",
            "quelle": "claude", "reihenfolge": i, "tag": m["tag"], "warten": m["warten"],
            "wann": m["wann"], "betreff": m["betreff"], "betreff2": m["betreff2"],
            "preheader": m["preheader"], "notiz": m["notiz"].strip(),
            "html": fertig, "text": text,
        }
        (COCKPIT / ("story-challenge-%02d.json" % i)).write_text(
            json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        md += ["## Tag %s · %s" % (m["tag"], m["betreff"]), "",
               "- **Wann:** %s" % m["wann"], "- **Zweiter Betreff:** %s" % m["betreff2"],
               "- **Vorschautext:** %s" % m["preheader"], "", "```text", text, "```", ""]
        print("  geschrieben:", m["datei"])

    seite = sk.KOPIERSEITE.format(karten="\n".join(karten)).replace("Startklar", "Story-Challenge")
    seite = re.sub(r'<p class="unter">.*?</p>',
                   '<p class="unter">Acht Mails von der Anmeldung bis zur Übergabe an die Engine. '
                   'Knopf „Ganzes HTML“ tippen, in ActiveCampaign einfügen.</p>', seite, count=1, flags=re.S)
    seite = re.sub(r'<div class="warnung">.*?</div>',
                   '<div class="warnung"><b>Beim Einrichten:</b> Alle Mails gehören in die Automation '
                   '„0€ Story Challenge“ (45). Ziel „Instagram-Kundenmaschine gekauft“ (Tag 39) als Ausstieg '
                   'einbauen.</div>', seite, count=1, flags=re.S)
    (ZIEL / "index.html").write_text(seite, encoding="utf-8")
    (ZIEL / "story-challenge-mails.md").write_text("\n".join(md), encoding="utf-8")
    print("  geschrieben: index.html · story-challenge-mails.md · %d Cockpit-Dokumente" % len(MAILS))
    print("  ✓ Keine umschriebenen Umlaute." if not beanstandet else "  ⚠ %d Umlaut-Funde" % beanstandet)
    print("  ✓ Blackliste sauber." if not funde else "  ⚠ %d Blacklisten-Funde" % funde)
    if not WORKBOOK:
        print("  ⚠ WORKBOOK ist leer — Mail Tag 0 hat keinen Workbook-Knopf.")


if __name__ == "__main__":
    main()
