"""
Baut die komplette Nachkauf-Strecke für „Startklar" als fertige Mail-HTMLs.

Warum ein Skript und nicht acht getippte Dateien: das Gerüst (Kopf, Farben,
Fuss, Tabellen-Layout für Outlook) ist in allen Mails gleich. Wer es achtmal
kopiert, ändert später siebenmal und vergisst die achte.

  python scripts/startklar/mails-bauen.py            # alle Mails + Kopierseite
  python scripts/startklar/mails-bauen.py --liste     # nur die Strecke anzeigen

Ausgabe: outputs/produkte/instagram-startklar/08-funnel/
  mail-00-auslieferung.html · mail-02-bio.html · mail-04-der-tipp.html …
  index.html  (Kopierseite mit Knopf je Mail)

Die Strategie dahinter steht in `bump-upsell-strategie.md` im selben Ordner.

🚨 Hormozi ist der STRUKTUR-Layer, Patricias Stimme der Ton. Wo beide sich
   widersprechen, gewinnt die Stimme: Hormozi will Sätze unter 15 Wörtern,
   Patricia will keine Stakkato-Sätze. Also: Hormozis Reihenfolge (Schmerz →
   Moment → Mechanismus → Angebot → ein CTA → P.S.), aber in ganzen Sätzen
   mit „und", „weil", „aber".

🚨 Keine erfundenen Zahlen und keine erfundenen Kundenstimmen. Wo eine echte
   Stimme fehlt, steht ein sichtbar leerer Platz mit Kommentar — nie ein
   plausibler Name.
"""
import argparse
import html
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "produkte" / "instagram-startklar" / "08-funnel"

WERKSTATT = "https://startklar.mumlifebalance.ch"
IKM = "https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/"

# --- Farben (context/brand-voice.md) ---------------------------------------
PETROL, DUNKEL, NACHT = "#12828c", "#29556d", "#0c1c30"
CREME, ORANGE = "#f1ecdd", "#dc822e"

# --- Bausteine --------------------------------------------------------------
# Alles inline, weil Outlook <style> im <head> grosszügig ignoriert.

P = ('<p style="margin:0 0 18px 0;font-family:Arial,sans-serif;font-size:16px;'
     'color:%s;line-height:1.85;">%%s</p>' % NACHT)
P_ENG = ('<p style="margin:0 0 10px 0;font-family:Arial,sans-serif;font-size:16px;'
         'color:%s;line-height:1.8;">%%s</p>' % NACHT)


def absatz(text, letzter=False):
    return (P_ENG if letzter else P) % text


def kasten(inhalt, hintergrund, rand=None, kopf=None, kopffarbe=PETROL):
    rahmen = ("border-left:4px solid %s;border-radius:0 12px 12px 0;" % rand
              if rand else "border-radius:12px;")
    k = ""
    if kopf:
        k = ('<p style="margin:0 0 10px 0;font-family:Arial,sans-serif;font-size:11px;'
             'font-weight:bold;color:%s;text-transform:uppercase;letter-spacing:2px;">'
             "%s</p>" % (kopffarbe, kopf))
    return (
        '<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 26px 0;">'
        '<tr><td style="background-color:%s;%spadding:22px 26px;">%s%s</td></tr></table>'
        % (hintergrund, rahmen, k, inhalt))


def merken(kopf, gross, klein=None):
    """Der dunkle Kasten — für die eine Zahl oder den einen Satz, der hängen bleibt."""
    t = ('<p style="margin:0 0 %s;font-family:Georgia,serif;font-size:21px;color:%s;'
         'line-height:1.45;">%s</p>' % ("12px 0" if klein else "0", CREME, gross))
    if klein:
        t += ('<p style="margin:0;font-family:Arial,sans-serif;font-size:15px;'
              'color:#a9bcc8;line-height:1.7;">%s</p>' % klein)
    return kasten(t, NACHT, kopf=kopf, kopffarbe=ORANGE)


def liste(kopf, punkte, hintergrund="#e4f3f4", rand=PETROL, farbe=PETROL):
    z = "".join(
        '<p style="margin:0 0 %s;font-family:Arial,sans-serif;font-size:15px;'
        'color:%s;line-height:1.7;">%s</p>' % ("8px 0" if i < len(punkte) - 1 else "0", NACHT, p)
        for i, p in enumerate(punkte))
    return kasten(z, hintergrund, rand=rand, kopf=kopf, kopffarbe=farbe)


def knopf(text, ziel):
    return (
        '<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 30px 0;">'
        '<tr><td align="center"><a href="%s" style="display:inline-block;'
        'background-color:%s;color:#ffffff;font-family:Arial,sans-serif;font-size:17px;'
        'font-weight:bold;text-decoration:none;padding:16px 38px;border-radius:30px;">'
        "%s</a></td></tr></table>" % (ziel, ORANGE, text))


def h2(text):
    return ('<h2 style="margin:0 0 14px 0;font-family:Georgia,serif;font-size:22px;'
            'font-weight:bold;color:%s;line-height:1.35;">%s</h2>' % (NACHT, text))


def dreher(vorher, nachher):
    """Vorher/Nachher-Paar — grau oben, fett unten."""
    return (
        '<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px 0;">'
        '<tr><td style="background-color:#f6f3ea;border-radius:10px;padding:16px 20px;">'
        '<p style="margin:0 0 6px 0;font-family:Arial,sans-serif;font-size:12px;color:#9a8f7c;">so hättest du es geschrieben</p>'
        '<p style="margin:0 0 12px 0;font-family:Arial,sans-serif;font-size:15px;color:#7a6f5d;line-height:1.6;">%s</p>'
        '<p style="margin:0 0 6px 0;font-family:Arial,sans-serif;font-size:12px;color:%s;font-weight:bold;">so bleibt der Daumen stehen</p>'
        '<p style="margin:0;font-family:Arial,sans-serif;font-size:16px;color:%s;line-height:1.6;"><strong>%s</strong></p>'
        "</td></tr></table>" % (vorher, PETROL, NACHT, nachher))


def ps(text):
    """Hormozi Hack 10 — das P.S. wird fast immer gelesen."""
    return ('<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:22px 0 0 0;">'
            '<tr><td style="border-top:1px solid #e8e2d2;padding-top:18px;">'
            '<p style="margin:0;font-family:Arial,sans-serif;font-size:15px;color:#5f5748;'
            'line-height:1.75;">%s</p></td></tr></table>' % text)


def gruss(text="Bis bald,"):
    return ('<p style="margin:26px 0 0 0;font-family:Georgia,serif;font-style:italic;'
            'font-size:17px;color:%s;line-height:1.6;">%s<br>Patricia</p>' % (PETROL, text))


SEITE = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titel}</title>
  <!--[if mso]><xml><w:WordDocument xmlns:w="urn:schemas-microsoft-com:office:word"><w:DontUseAdvancedTypographyReadingMail/></w:WordDocument></xml><![endif]-->
</head>
<!--
  NACHKAUF-STRECKE STARTKLAR · {marke}
  ERZEUGT von scripts/startklar/mails-bauen.py — Änderungen dort, nicht hier.

  Betreff     : {betreff}
  Alternative : {betreff2}
  Versand     : {wann}

{notiz}
-->
<body style="margin:0;padding:0;background-color:{creme};font-family:Arial,sans-serif;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{preheader} &nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;&nbsp;&#8204;</div>
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{creme};">
    <tr>
      <td align="center" style="padding:30px 16px;">
        <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;">
          <tr>
            <td bgcolor="{petrol}" style="background-color:{petrol};background:linear-gradient(135deg,{nacht} 0%,{dunkel} 60%,{petrol} 100%);border-radius:16px 16px 0 0;padding:42px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr><td style="padding-bottom:16px;"><span style="background-color:{orange};color:#ffffff;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;padding:6px 14px;border-radius:20px;">{marke}</span></td></tr>
                <tr><td><h1 style="margin:0;font-family:Georgia,serif;font-size:30px;font-weight:bold;color:{creme};line-height:1.28;">{h1}</h1></td></tr>
                {unterzeile}
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#ffffff;padding:38px 40px 34px 40px;">
              {rumpf}
            </td>
          </tr>
          <tr>
            <td bgcolor="{dunkel}" style="background-color:{dunkel};border-radius:0 0 16px 16px;padding:26px 40px;">
              <p style="margin:0 0 6px 0;font-family:Georgia,serif;font-size:15px;color:{creme};line-height:1.5;">Funktionieren war gestern.</p>
              <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:#a9bcc8;line-height:1.6;">Patricia Ulmann &middot; mumlifebalance.ch</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def bauen(m):
    unter = ""
    if m.get("unterzeile"):
        unter = ('<tr><td style="padding-top:14px;"><p style="margin:0;font-family:Georgia,serif;'
                 'font-style:italic;font-size:16px;color:#dcd5c0;line-height:1.5;">%s</p></td></tr>'
                 % m["unterzeile"])
    notiz = "\n".join("  " + z for z in m["notiz"].strip().splitlines())
    return SEITE.format(
        titel=html.escape(m["betreff"], quote=False),
        marke=m["marke"], betreff=m["betreff"], betreff2=m["betreff2"],
        wann=m["wann"], notiz=notiz, preheader=m["preheader"],
        h1=m["h1"], unterzeile=unter, rumpf="\n              ".join(m["bloecke"]),
        creme=CREME, petrol=PETROL, dunkel=DUNKEL, nacht=NACHT, orange=ORANGE)


# ============================================================================
#  DIE STRECKE
# ============================================================================
#  „wann" ist die Wartezeit AB DER VORIGEN MAIL, nicht ab Kauf — so trägt
#  ActiveCampaign es auch ein (Warte-Schritt zwischen zwei Mails).
# ============================================================================

MAILS = [

# --------------------------------------------------------------------- Tag 0
{
 "datei": "mail-00-auslieferung.html", "tag": 0, "warten": "sofort nach dem Kauf",
 "marke": "mumlifebalance · Startklar",
 "betreff": "Startklar — dein Zugang steht",
 "betreff2": "Dein Profil in einer Woche — los geht es",
 "wann": "sofort nach dem Kauf (Auslieferung)",
 "preheader": "Drei Module, zwölf Lektionen und ein Mitmach-Heft, das mittippt",
 "h1": "Dein Zugang steht",
 "unterzeile": "In einer Woche steht dein Profil &mdash; und du weisst, wo du hindrücken musst.",
 "notiz": """
🚨 KEIN Kurslink in dieser Mail. Die Zugangsdaten verschickt ThriveCart in
   einer eigenen Mail. Zwei Wege zum selben Kurs stiften nur Verwirrung.
🚨 Der Zugangscode STARTKLAR_KUNDE wird absichtlich nicht erwähnt — er steht
   im Kurs in der Lektion „Deine Werkstatt".
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("schön, dass du da bist. Startklar liegt ab jetzt für dich bereit, und du "
          "kannst sofort loslegen &mdash; vorbereiten musst du nichts, dein Handy reicht."),
   absatz("Der Kurs besteht aus <strong>drei Modulen mit zwölf Lektionen</strong>, "
          "zusammen rund 80 Minuten. Die einzelnen Lektionen sind bewusst kurz, damit "
          "du auch dann eine schaffst, wenn nur zwanzig Minuten übrig sind."),
   kasten("<p style=\"margin:0;font-family:Arial,sans-serif;font-size:15px;color:%s;"
          "line-height:1.75;\">Deine Zugangsdaten zum Kurs hast du in einer <strong>separaten "
          "Mail von ThriveCart</strong> bekommen &mdash; dort stehen dein Login und der Link "
          "zur Kursplattform. Falls du sie nicht findest, schau kurz im Spam-Ordner nach, "
          "manchmal landet sie dort.</p>" % NACHT,
          "#fdf4e9", rand=ORANGE, kopf="Wo du reinkommst", kopffarbe="#b4661f"),
   h2("Das Mitmach-Heft ist der halbe Kurs"),
   absatz("Zu jeder Lektion gehört eine Station in der <strong>Startklar-Werkstatt</strong>. "
          "Dort tippst du direkt hinein, was nachher wirklich auf deinem Profil stehen soll, "
          "und du bekommst sofort zurück, was schon sitzt und was noch zu schwammig ist "
          "&mdash; also nicht erst, wenn alles online steht und du dich fragst, warum "
          "niemand reagiert."),
   liste("Am Ende hast du", [
       "&#128205; Namensfeld und Bio, die sagen, für wen du da bist",
       "&#128193; Fünf Highlight-Ordner, die wie ein Schaufenster wirken",
       "&#127916; Dein erstes Reel, dein erstes Karussell und deine erste Story &mdash; fertig getippt",
       "&#128197; Einen Plan für Woche eins, damit du am Montag nicht ratlos dastehst"]),
   knopf("Zur Startklar-Werkstatt &rarr;", WERKSTATT),
   h2("Wie du am besten startest"),
   absatz('<strong style="color:%s;">1.</strong> &nbsp;Öffne die Werkstatt in einem zweiten '
          "Tab und leg sie dir als Lesezeichen ab." % PETROL, letzter=True),
   absatz('<strong style="color:%s;">2.</strong> &nbsp;Schau Modul 1 und tipp dabei mit, '
          "statt danach." % PETROL, letzter=True),
   absatz('<strong style="color:%s;">3.</strong> &nbsp;Lass nach jeder Station einmal prüfen '
          "und schärf den Satz nach, bevor du weitergehst." % PETROL),
   absatz("Und eines noch, weil ich es selbst lange falsch gemacht habe: <strong>fertig "
          "schlägt perfekt.</strong> Deine Bio darf beim ersten Mal holprig sein, du kannst "
          "sie jederzeit ändern. Was du nicht ändern kannst, ist die Zeit, die vergeht, "
          "während du auf die perfekte Formulierung wartest."),
   absatz("Ich hab diesen Kurs neben vier Kindern gebaut, und genau so ist er auch gedacht "
          "&mdash; in Stücken, die zwischen zwei Türen passen."),
   absatz("Wenn irgendwo etwas klemmt, schreib mir einfach auf Instagram. Ich lese alles selbst.",
          letzter=True),
   gruss("Ich freu mich auf dein Profil,"),
 ]},

# --------------------------------------------------------------------- Tag 2
{
 "datei": "mail-02-bio.html", "tag": 2, "warten": "2 Tage warten",
 "marke": "Startklar · Tag 2",
 "betreff": "Liegt der Kurs noch offen in einem Tab?",
 "betreff2": "Steht deine Bio schon?",
 "wann": "2 Tage nach der Auslieferung",
 "preheader": "Eine Station. Nicht der ganze Kurs. Nur eine.",
 "h1": "Eine Station reicht für heute",
 "notiz": """
Job: sie bleibt dran. Kein Verkauf.
Hormozi: Flaunt your flaws (ich hab meine Bio dreimal umgeschrieben) ·
Repel bad fits (wer schon durch ist, darf weglesen) · genau EIN CTA.
Der Schmerz ist ein Moment, keine Eigenschaft: der offene Tab.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("ich rate mal, wie es gerade bei dir aussieht: Der Kurs ist offen in einem Tab, "
          "du hast Lektion 1.1 geschaut, und dann kam der Abend, an dem noch Wäsche lag."),
   absatz("Falls du längst durch bist &mdash; super, dann lies hier gar nicht weiter. "
          "Der Rest ist für die anderen."),
   h2("Nimm dir heute nur die Bio vor"),
   absatz("Nicht den ganzen Kurs, nicht Modul 1 am Stück. Nur die eine Station, in der "
          "vier Zeilen stehen. Das dauert zehn Minuten, und danach steht der Teil deines "
          "Profils, den jede zuerst liest."),
   absatz("Ich sag dir gleich dazu: Ich hab meine eigene Bio dreimal komplett "
          "umgeschrieben, bevor sie gesessen hat. Beim ersten Mal stand da, was ich mache. "
          "Heute steht da, für wen ich da bin, und das ist ein ziemlicher Unterschied."),
   liste("Woran du merkst, dass sie sitzt", [
       "Eine Fremde könnte nach dem Lesen sagen, für wen du da bist &mdash; ohne zu raten.",
       "Es steht ein Grund drin, dir zu folgen, und nicht nur, wer du bist.",
       "Du kommst mit allem zusammen unter 150 Zeichen, weil Instagram bei 150 abschneidet."]),
   knopf("Zur Station „Bio“ &rarr;", WERKSTATT),
   absatz("In der Werkstatt liegt bei jedem Feld ein fertiges Beispiel, das du als Start "
          "übernehmen und dann auf dich umschreiben kannst. Damit du nicht vor einem "
          "leeren Feld sitzt, was der eigentliche Grund ist, warum Bios wochenlang "
          "unfertig bleiben.", letzter=True),
   gruss(),
   ps("<strong>P.S.</strong> Zehn Minuten. Wirklich. Wenn du danach aufhörst, hast du "
      "trotzdem den wichtigsten Teil erledigt."),
 ]},

# --------------------------------------------------------------------- Tag 4
{
 "datei": "mail-04-der-tipp.html", "tag": 4, "warten": "2 Tage warten",
 "marke": "Startklar · Tag 4",
 "betreff": "Ich habs bei mir nachgemessen: 2,6-mal",
 "betreff2": "Deine erste Zeile macht fast alles",
 "wann": "2 Tage nach der Bio-Mail",
 "preheader": "Und warum „Folge mir, wenn du…\" bei mir gar nichts gebracht hat",
 "h1": "Deine erste Zeile macht fast alles",
 "notiz": """
🚨 IN DIESER MAIL WIRD NICHTS VERKAUFT. Kein Knopf, kein Produkt, kein
   „übrigens". Der Pitch kommt an Tag 12 und funktioniert nur, wenn diese
   hier geschenkt war.
Die 2,6 stammen aus Patricias eigenen Instagram-Zahlen vom 17.09.2026.
Aendert sich die Zahl, gehört sie hier nachgezogen — nie schätzen.
Hormozi: Schock-Zahl als Hook · Promise+Proof · Specificity als Beweis.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("ich hab letzte Woche meine eigenen Zahlen durchgeschaut, und zwar nicht so "
          "nebenbei, sondern Beitrag für Beitrag. Dabei ist mir etwas aufgefallen, das "
          "ich vorher so nicht auf dem Schirm hatte."),
   merken("Was in meinen Zahlen stand",
          "Beiträge, deren erste Zeile eine <strong>Frage</strong> war, hatten "
          "<strong>2,6-mal so viel Reichweite</strong> wie die anderen.",
          "Und der Satz, den einem alle empfehlen &mdash; „Folge mir, wenn…\" &mdash; "
          "hat bei mir praktisch nichts gebracht."),
   absatz("Der Grund dafür ist ziemlich unspektakulär: Eine Aussage kann man "
          "überscrollen, ohne dass etwas offen bleibt. Eine Frage nicht, denn die will "
          "beantwortet werden, und dafür bleibt der Daumen kurz stehen. Diese eine "
          "Sekunde ist alles, was du brauchst."),
   absatz("So sieht das aus, wenn du eine Zeile umdrehst:"),
   dreher("Ich zeig dir, wie du endlich sichtbar wirst.",
          "Wie oft hast du schon einen Beitrag getippt und dann doch nicht gepostet?"),
   dreher("5 Tipps für mehr Reichweite.",
          "Warum sieht deinen Beitrag niemand, obwohl du 400 Leute in deiner Liste hast?"),
   dreher("Folge mir, wenn du im Network durchstarten willst.",
          "Kennst du das, wenn du abends noch was posten willst und dann zwanzig Minuten "
          "auf ein leeres Feld starrst?"),
   kasten("<p style=\"margin:0;font-family:Arial,sans-serif;font-size:15px;color:%s;"
          "line-height:1.75;\">Es muss <strong>ihre</strong> Frage sein, nicht irgendeine. "
          "„Willst du mehr Reichweite?\" ist zwar eine Frage, aber niemand fühlt sich davon "
          "gemeint &mdash; das ist eine Verkaufsfrage. Die Frage muss so klingen, als "
          "hättest du ihr beim Denken zugehört.</p>" % NACHT,
          "#fdf4e9", rand=ORANGE, kopf="Wichtig, sonst geht es nach hinten los",
          kopffarbe="#b4661f"),
   absatz("<strong>Deine Aufgabe für heute:</strong> Nimm den Beitrag, den du als Nächstes "
          "posten willst, und dreh nur die erste Zeile um. Sonst nichts. Der Rest darf "
          "bleiben, wie er ist."),
   absatz("Wenn du magst, antworte mir mit deiner ersten Zeile. Ich lese alles selbst.",
          letzter=True),
   gruss(),
 ]},

# --------------------------------------------------------------------- Tag 6
{
 "datei": "mail-06-erstes-reel.html", "tag": 6, "warten": "2 Tage warten",
 "marke": "Startklar · Tag 6",
 "betreff": "Dein erstes Reel wird schlecht. Poste es trotzdem.",
 "betreff2": "Sieben Sekunden, ein Satz, fertig",
 "wann": "2 Tage nach dem Tipp",
 "preheader": "Sieben Sekunden Video, ein Satz drauf, der Rest in die Caption",
 "h1": "Sieben Sekunden reichen",
 "notiz": """
Job: sie postet zum ersten Mal.
Hormozi: Konträre Meinung als Hook · Value Equation (Aufwand runter statt
Ergebnis hoch) · Flaunt your flaws · ein CTA.
Das B-Roll-Format ist Patricias eigenes: ein Clip, ein Textblock, Inhalt in
der Caption. Nichts dazuerfinden.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("die häufigste Stelle, an der es stecken bleibt, ist nicht die Bio. Es ist das "
          "erste Video. Man nimmt sich vor, eins zu machen, und dann kommt die Rechnung im "
          "Kopf: Licht, Text, Schnitt, Musik, und wie sehe ich eigentlich aus."),
   absatz("Deshalb machen wir es heute so klein, dass die Rechnung gar nicht erst aufgeht."),
   merken("Das Format für dein erstes Mal",
          "<strong>Ein Clip. Sieben Sekunden. Ein Satz drauf. Der Rest in die Caption.</strong>",
          "Kein Sprechen vor der Kamera, kein Schnitt, keine Musik-Recherche."),
   h2("So geht es konkret"),
   absatz('<strong style="color:%s;">1.</strong> &nbsp;Film sieben Sekunden von etwas, das '
          "heute sowieso passiert: Kaffee eingiessen, Schuhe im Flur, Laptop auf dem "
          "Küchentisch." % PETROL, letzter=True),
   absatz('<strong style="color:%s;">2.</strong> &nbsp;Leg deinen Hook als Text darüber, den '
          "ganzen Satz, ohne Kasten drumherum." % PETROL, letzter=True),
   absatz('<strong style="color:%s;">3.</strong> &nbsp;Schreib den Inhalt in die Caption. '
          "Da gehört er hin, nicht ins Video." % PETROL),
   absatz("Das Video muss nicht zeigen, wovon der Satz handelt. Es muss nur dafür sorgen, "
          "dass der Satz gelesen wird, und dafür reicht ein völlig normales Bild aus "
          "deinem Tag."),
   knopf("Zur Station „Reel“ &rarr;", WERKSTATT),
   absatz("Und weil ich weiss, was jetzt kommt: Ja, es wird nicht das beste Reel deines "
          "Lebens. Meins war es auch nicht, und ich hab es trotzdem drin gelassen. Das "
          "erste ist dafür da, dass es das zweite gibt.", letzter=True),
   gruss(),
   ps("<strong>P.S.</strong> Nimm den Hook, dessen erste Zeile eine Frage ist. Du weisst "
      "ja seit vorgestern, was das bei mir gebracht hat."),
 ]},

# --------------------------------------------------------------------- Tag 9
{
 "datei": "mail-09-rueckmeldung.html", "tag": 9, "warten": "3 Tage warten",
 "marke": "Startklar · Tag 9",
 "betreff": "Eine Frage an dich (dauert zwei Minuten)",
 "betreff2": "Was ging nachher, was vorher nicht ging?",
 "wann": "3 Tage nach der Reel-Mail",
 "preheader": "Kein Verkauf, keine Aufgabe — nur eine Frage",
 "h1": "Was ging nachher, was vorher nicht ging?",
 "notiz": """
Job: Kundenstimme einsammeln UND Antworten erzeugen (Antworten auf eine Mail
sind das beste Zustellbarkeits-Signal, das es gibt).
🚨 Die Frage ist bewusst nicht „wie hat es dir gefallen?" — darauf kommt
   „super, danke", und damit kann niemand etwas anfangen. Die Vorher/Nachher-
   Frage erzwingt eine brauchbare Antwort.
Diese Mail wärmt den Pitch an Tag 12 vor: wer selbst formuliert, was jetzt
geht, spürt im selben Moment, was noch nicht geht.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("heute keine Aufgabe und nichts zu lesen, sondern eine Frage. Und zwar eine, "
          "die mir wirklich weiterhilft."),
   merken("Die Frage",
          "Was konntest du nach Startklar, was vorher nicht ging?"),
   absatz("Antworte einfach auf diese Mail. Zwei, drei Sätze reichen völlig, und es darf "
          "ruhig unfertig klingen &mdash; ich will nicht das Lob, ich will den Unterschied."),
   absatz("Falls du gerade nicht weiterkommst, ist das genauso eine gültige Antwort. "
          "Schreib mir, an welcher Stelle du hängst. Ich lese alles selbst und antworte, "
          "wenn ich etwas beitragen kann."),
   liste("Was mir am meisten hilft", [
       "Wie dein Profil vorher ausgesehen hat und was jetzt anders ist",
       "Welche Station am meisten gebracht hat &mdash; und welche gar nichts",
       "Ob du seitdem etwas gepostet hast, und was dabei passiert ist"]),
   absatz("Wenn du magst und ich deine Antwort später mal zeigen darf, schreib einfach "
          "dazu, dass das für dich in Ordnung ist. Ohne diesen Satz bleibt sie bei mir.",
          letzter=True),
   gruss("Danke dir,"),
 ]},

# -------------------------------------------------------------------- Tag 12
{
 "datei": "mail-12-kundenmaschine.html", "tag": 12, "warten": "3 Tage warten",
 "marke": "Startklar · Tag 12",
 "betreff": "Dein Profil steht. Und jetzt passiert nichts.",
 "betreff2": "Warum ein gutes Profil noch keine Kundin bringt",
 "wann": "3 Tage nach der Rückfrage &mdash; der wichtigste Verkaufsmoment der Strecke",
 "preheader": "Der Teil, den Startklar bewusst nicht abdeckt",
 "h1": "Dein Profil steht. Und jetzt?",
 "notiz": """
🚨 DER PITCH. Instagram-Kundenmaschine, 333 CHF, voller Preis, kein Rabatt.

Hormozi „PAIN IS THE PITCH" plus die Ausnahme: nach einem Gewinn verkauft man
nur, wenn der gelieferte Wert ein NEUES Problem geschaffen hat. Genau das ist
hier der Fall — das Profil steht, und deshalb kommen jetzt Reaktionen, mit
denen sie nichts anfangen kann.
Aufbau: Gewinn spiegeln → neuer Schmerz als MOMENT → Reframe → Angebot →
Beweis → EIN CTA → P.S.

🚨 Startklar deckt Profil, Thema und Schaufenster ab — das steht in der
   Kundenmaschine auch drin. Das wird hier offen gesagt, statt es zu
   verschweigen. Wer es verschweigt, verliert sie beim ersten Modul.

🚨 KUNDENSTIMME FEHLT. In den Unterlagen steht nur „Super Kurs!", und damit
   kann man nicht arbeiten. Der Platz unten ist absichtlich leer gelassen —
   nie einen Namen erfinden.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("wenn du die letzten zwei Wochen mitgemacht hast, steht jetzt etwas da, "
          "was vorher nicht da war: ein Profil, das sagt, für wen du da bist, und ein "
          "erster Beitrag, den du wirklich gepostet hast. Das ist mehr, als die meisten "
          "in einem halben Jahr schaffen."),
   absatz("Und genau deshalb schreibe ich dir heute. Denn ein Profil, das steht, erzeugt "
          "ein Problem, das du vorher nicht hattest."),
   h2("Der Moment, den ich meine"),
   absatz("Jemand kommentiert unter deinem Beitrag. Du freust dich, antwortest mit einem "
          "Herz und einem „Danke dir!\", und dann ist es still. Zwei Tage später weisst du "
          "nicht mehr, wer das war. Drei Wochen später hast du vierzig solche Kommentare "
          "und keine einzige Unterhaltung."),
   absatz("Das ist kein Profil-Problem mehr. Dein Profil hat seine Arbeit gemacht, es hat "
          "den Blick geholt. Was fehlt, ist der Weg vom Blick zum Gespräch und vom "
          "Gespräch zur Kundin, und der passiert nicht von allein."),
   merken("Die ehrliche Grenze von Startklar",
          "Startklar bringt dich <strong>gesehen</strong>. Es bringt dich nicht "
          "<strong>gekauft</strong>.",
          "Das war nie der Anspruch, und für 39 Franken wäre es auch eine Frechheit, "
          "das zu behaupten."),
   h2("Was danach kommt"),
   absatz("Dafür gibt es die <strong>Instagram-Kundenmaschine</strong>. Da geht es nicht "
          "mehr darum, wie dein Profil aussieht, sondern darum, was danach passiert."),
   liste("Was drinsteckt", [
       "<strong>Keywords, die Entscheidungen auslösen</strong> &mdash; damit aus einem Kommentar ein Gespräch wird, ohne dass du hinterherlaufen musst",
       "<strong>Von Reaktionen zu Gesprächen</strong> &mdash; was du antwortest, wenn jemand reagiert, und was du besser nicht antwortest",
       "<strong>Deine Instagram-Routine</strong> &mdash; ein Ablauf, der auch in einer Woche funktioniert, in der zwei Kinder krank sind",
       "<strong>Content-Säulen und Ideen</strong> &mdash; damit du nie wieder überlegst, was du heute posten sollst",
       "<strong>ChatGPT sinnvoll nutzen</strong> &mdash; nicht Texte generieren lassen, sondern schneller zu deinen eigenen kommen",
       "<strong>Dranbleiben ohne Motivation</strong> &mdash; weil Motivation nicht der Teil ist, auf den man bauen kann",
       "Dazu die Aufzeichnungen der Zoom-Calls, in denen echte Profile auseinandergenommen wurden"]),
   kasten("<p style=\"margin:0;font-family:Arial,sans-serif;font-size:15px;color:%s;"
          "line-height:1.75;\">Damit du es von mir hörst und nicht selbst merkst: In der "
          "Kundenmaschine gibt es auch Lektionen zu Profil, Thema und Highlights. Das ist "
          "genau der Teil, den du mit Startklar schon gemacht hast, und den kannst du "
          "überspringen. Ich sag es lieber vorher, als dass du im ersten Modul denkst, du "
          "hättest etwas doppelt gekauft.</p>" % NACHT,
          "#fdf4e9", rand=ORANGE, kopf="Was du schon hast", kopffarbe="#b4661f"),
   h2("Warum ausgerechnet jetzt"),
   absatz("Nicht, weil ein Preis steigt oder irgendein Zähler abläuft &mdash; beides wäre "
          "erfunden. Sondern weil dein Profil gerade frisch ist und du noch keine "
          "Gewohnheiten hast, die du dir wieder abtrainieren musst. In sechs Monaten hast "
          "du zweihundert Beiträge ohne System und einen Haufen Kommentare, aus denen nie "
          "etwas geworden ist. Das lässt sich reparieren, aber es ist deutlich mehr Arbeit, "
          "als es jetzt gleich richtig anzufangen."),
   absatz("Die Instagram-Kundenmaschine kostet <strong>333 Franken</strong>, einmalig, "
          "mit Zugang zu allem, was drin ist."),
   knopf("Die Kundenmaschine ansehen &rarr;", IKM),
   # 🚨 Echte Kundenstimme fehlt — siehe Notiz oben. Nichts erfinden.
   # <!-- HIER ECHTE STIMME EINSETZEN, sobald eine brauchbare vorliegt -->
   absatz("Wenn du dir nicht sicher bist, ob es gerade passt, schreib mir einfach zurück "
          "und sag, wo du stehst. Ich sag dir ehrlich, ob es der richtige Schritt ist oder "
          "ob du noch vier Wochen einfach posten solltest.", letzter=True),
   gruss(),
   ps("<strong>P.S.</strong> Falls du nur eine Sache mitnimmst aus dieser Mail: Ein "
      "Kommentar, auf den du mit einem Herz antwortest, ist verschenkt. Das ist die "
      "Stelle, an der bei den meisten das Geld liegen bleibt."),
 ]},

# -------------------------------------------------------------------- Tag 15
{
 "datei": "mail-15-einwand.html", "tag": 15, "warten": "3 Tage warten",
 "marke": "Startklar · Tag 15",
 "betreff": "„Ich bin doch noch gar nicht so weit\"",
 "betreff2": "Der Satz, den ich am häufigsten höre",
 "wann": "3 Tage nach dem Pitch",
 "preheader": "Warum genau das der Grund ist, jetzt anzufangen",
 "h1": "„Ich bin noch nicht so weit\"",
 "notiz": """
Job: den einen Einwand auflösen, der am häufigsten hält.
Hormozi: Reframe (den Einwand in den Grund verwandeln) · Flaunt your flaws ·
derselbe EINE CTA wie an Tag 12, kein neues Angebot.
🚨 Kein Rabatt, keine erfundene Frist. Wenn hier ein Sonderpreis auftaucht,
   ist der 333er dauerhaft undicht.
""",
 "bloecke": [
   absatz("Hey %FIRSTNAME%,"),
   absatz("auf die Mail von vorgestern kam ein Satz mehrfach zurück, in verschiedenen "
          "Varianten, aber im Kern immer derselbe: <em>Ich hab doch gerade erst "
          "angefangen. Ich bin noch nicht so weit für sowas.</em>"),
   absatz("Ich versteh das gut, weil ich genauso gedacht habe. Also lass mich das einmal "
          "umdrehen."),
   merken("Der Punkt",
          "„Noch nicht so weit\" ist kein Grund zu warten. Es ist der Grund, jetzt "
          "anzufangen.",
          "Du baust die Routine, solange du noch keine falsche hast."),
   absatz("Wer seit zwei Jahren postet, hat sich Gewohnheiten angewöhnt, die sich zäh "
          "wieder abgewöhnen lassen. Du hast die noch nicht. Bei dir ist das Blatt gerade "
          "leer, und es ist viel leichter, gleich den richtigen Ablauf zu lernen, als "
          "später den eingespielten umzubauen."),
   h2("Der zweite Satz, der kommt"),
   absatz("<em>Ich hab keine Zeit dafür.</em> Und ja, das stimmt sogar &mdash; du hast sie "
          "wirklich nicht. Nur ist eine Routine nicht das, was Zeit frisst. Was Zeit "
          "frisst, ist das Überlegen: was poste ich heute, wie antworte ich darauf, "
          "sollte ich nochmal nachfassen oder wirkt das aufdringlich."),
   absatz("Genau dieses Überlegen fällt weg, wenn der Ablauf steht. Es geht nicht darum, "
          "mehr zu machen, sondern darum, dass das, was du sowieso machst, irgendwo ankommt."),
   absatz("Falls du es trotzdem gerade nicht willst, ist das völlig in Ordnung &mdash; "
          "dann poste die nächsten vier Wochen einfach weiter und schau, was passiert. "
          "Das ist kein schlechter Plan, es dauert nur länger."),
   knopf("Die Kundenmaschine ansehen &rarr;", IKM),
   absatz("Und wenn dich etwas anderes hält als diese zwei Sätze, schreib es mir. Ich "
          "beiss nicht und ich rede dir auch nichts ein.", letzter=True),
   gruss(),
   ps("<strong>P.S.</strong> Es gibt keinen Rabatt und keine Frist. 333 kostet sie heute, "
      "und 333 kostet sie in vier Wochen. Du sollst dich nicht wegen eines Countdowns "
      "entscheiden, sondern weil es passt."),
 ]},

]


# ============================================================================
#  Kopierseite — eine Karte je Mail
# ============================================================================

KOPIERSEITE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Startklar · Mailstrecke kopieren</title>
<style>
  :root{{--petrol:#12828c;--dunkel:#29556d;--nacht:#0c1c30;--creme:#f1ecdd;
        --orange:#dc822e;--linie:#e2dccb}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--creme);color:var(--nacht);
       font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
       padding:28px 16px 60px}}
  .huelle{{max-width:920px;margin:0 auto}}
  h1{{font-family:Georgia,serif;font-size:27px;margin:0 0 6px;color:var(--dunkel)}}
  .unter{{margin:0 0 24px;color:#6d6455}}
  .karte{{background:#fff;border:1px solid var(--linie);border-radius:14px;
         padding:20px 22px;margin-bottom:16px}}
  .kopf{{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin-bottom:8px}}
  .tag{{background:var(--petrol);color:#fff;font-size:12px;font-weight:700;
       letter-spacing:1px;text-transform:uppercase;padding:4px 12px;border-radius:14px}}
  .warten{{font-size:13px;color:#8a8070}}
  h2{{font-family:Georgia,serif;font-size:19px;margin:0;color:var(--dunkel)}}
  .betreff{{margin:2px 0 14px;font-size:15px;color:#6d6455}}
  .betreff b{{color:var(--nacht)}}
  .knoepfe{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
  button,a.knopf{{font:inherit;font-size:14px;font-weight:700;border:0;border-radius:22px;
         padding:9px 18px;cursor:pointer;background:var(--orange);color:#fff;
         text-decoration:none;display:inline-block}}
  button.still,a.knopf.still{{background:#fff;color:var(--petrol);
         border:2px solid var(--petrol);padding:7px 16px}}
  .meldung{{font-size:13px;color:var(--petrol);font-weight:700;min-height:1.3em}}
  .warnung{{background:#fdf4e9;border-left:4px solid var(--orange);
           border-radius:0 10px 10px 0;padding:14px 18px;margin:0 0 22px;font-size:15px}}
  details{{margin-top:16px}}
  summary{{cursor:pointer;font-size:13px;font-weight:700;color:var(--petrol);
          letter-spacing:1px;text-transform:uppercase;padding:6px 0;
          list-style:none;user-select:none}}
  summary::-webkit-details-marker{{display:none}}
  summary::before{{content:"▾  ";font-size:11px}}
  details:not([open]) summary::before{{content:"▸  "}}
  iframe{{width:100%;height:600px;border:1px solid var(--linie);border-radius:12px;
         background:#fff;margin-top:8px;display:block}}
  @media (max-width:700px){{ iframe{{height:460px}} }}
</style>
</head>
<body>
<div class="huelle">
  <h1>Mailstrecke · Startklar</h1>
  <p class="unter">Sieben Mails vom Kauf bis zur Übergabe an die Engine. Kopieren, in ActiveCampaign einen HTML-Block einfügen, einsetzen. Die Vorschau unter jeder Karte ist genau das, was ankommt &mdash; %FIRSTNAME% füllt dein Mailprogramm beim Versand.</p>

  <div class="warnung">
    <b>Beim Einrichten:</b> Die Wartezeit steht bei jeder Mail und zählt
    <b>ab der vorigen Mail</b>, nicht ab Kauf. Wer an Tag 12 oder 15 kauft, soll aussteigen —
    dafür in ActiveCampaign ein Ziel auf den Kauf-Tag der Kundenmaschine setzen.
  </div>

{karten}

  <div class="karte">
    <h2>Und danach: ab in die Engine</h2>
    <p class="betreff">Fünf Tage nach der letzten Mail den Tag setzen, der <b>Automation 72</b>
    („Automation 0€ Produkt", Loop 1) auslöst. Dort bekommt sie „Finde dein Thema" für 39
    angeboten, und danach läuft die Kaskade weiter.</p>
    <p class="betreff"><b>Loop 6 bleibt an.</b> Das ist der Kundenmaschinen-Pitch für 333,
    den sie an Tag 12 schon bekommen hat — er kommt aber erst nach den Loops 1 bis 5, also
    <b>gut zwei Monate später</b>, mit fünf Mehrwert-Mails davor und einem anderen Einstieg.
    Das ist kein Doppel-Pitch, sondern ein zweiter Anlauf in einer anderen Lebenslage.
    Wer inzwischen gekauft hat, steigt über das Ziel „Instagram-Kundenmaschine schon da"
    von selbst aus.</p>
  </div>
</div>

<script>
"use strict";
var geladen = {{}};

function sagen(id, text){{
  var m = document.getElementById("meldung-" + id);
  m.textContent = text;
  clearTimeout(m.uhr);
  m.uhr = setTimeout(function(){{ m.textContent = ""; }}, 2600);
}}

function ohneKommentar(t){{
  return t.replace(/<!--\\s*\\n\\s*NACHKAUF-STRECKE[\\s\\S]*?-->\\s*/, "");
}}
function nurInhalt(t){{
  var von = t.indexOf("<body"), bis = t.lastIndexOf("</body>");
  if (von === -1 || bis === -1) return t;
  return t.slice(t.indexOf(">", von) + 1, bis).trim();
}}

async function holen(datei){{
  if (!geladen[datei]) geladen[datei] = await (await fetch(datei)).text();
  return geladen[datei];
}}

async function kopieren(text, id, was){{
  try {{
    await navigator.clipboard.writeText(text);
    sagen(id, "\\u2713 " + was + " kopiert");
  }} catch (e) {{
    var f = document.createElement("textarea");
    f.value = text; f.style.position = "fixed"; f.style.opacity = "0";
    document.body.appendChild(f); f.select();
    var ok = false;
    try {{ ok = document.execCommand("copy"); }} catch (e2) {{}}
    f.remove();
    sagen(id, ok ? "\\u2713 " + was + " kopiert" : "Ging nicht — markier den Text von Hand.");
  }}
}}

document.querySelectorAll("[data-tun]").forEach(function(b){{
  b.addEventListener("click", async function(){{
    var id = b.dataset.id, datei = b.dataset.datei, tun = b.dataset.tun;
    if (tun === "betreff") return kopieren(b.dataset.wert, id, "Betreff");
    var roh = ohneKommentar(await holen(datei));
    kopieren(tun === "ganz" ? roh : nurInhalt(roh), id,
             tun === "ganz" ? "Ganzes HTML" : "Inhalt");
  }});
}});
</script>
</body>
</html>
"""

KARTE = """  <div class="karte">
    <div class="kopf">
      <span class="tag">Tag {tag}</span>
      <h2>{h1}</h2>
      <span class="warten">{warten}</span>
    </div>
    <p class="betreff"><b>Betreff:</b> {betreff}</p>
    <div class="knoepfe">
      <button data-tun="ganz" data-id="{id}" data-datei="{datei}">Ganzes HTML</button>
      <button class="still" data-tun="teil" data-id="{id}" data-datei="{datei}">Nur Inhalt</button>
      <button class="still" data-tun="betreff" data-id="{id}" data-wert="{betreff_roh}">Betreff</button>
      <a class="knopf still" href="{datei}" target="_blank" rel="noopener">Gross ansehen</a>
      <span class="meldung" id="meldung-{id}"></span>
    </div>
    <details open>
      <summary>So sieht sie aus</summary>
      <iframe loading="lazy" src="{datei}" title="Vorschau: {betreff_roh}"></iframe>
    </details>
  </div>
"""


# ----------------------------------------------------------------------------
#  Waechter: umschriebene Umlaute im sichtbaren Text
# ----------------------------------------------------------------------------
# 🚨 Am 18.09.2026 stand „so haettest du es geschrieben" dreimal in Mail 4 —
#    im Text, den die Käuferin liest. Aufgefallen ist es Patricia, nicht mir.
#    Eine Prüfung aus dem Gedächtnis prüft das, woran man gerade denkt, deshalb
#    steht sie jetzt als Code und läuft bei jedem Bau mit.
#
# 🚨 Echte ae/oe/ue-Wörter (bauen, dauert, neues, zuerst) dürfen NICHT
#    anschlagen — nach dem dritten Fehlalarm liest niemand mehr hin. Darum eine
#    Liste bekannter Umschreibungen statt eines Musters über alle Wörter.

UMSCHRIEBEN = re.compile(
    r"\b(?:fuer|ueber|uebrigens|waere|waeren|haette|haettest|haetten"
    r"|koennte|koennten|koennen|moechte|moechten|muesste|muessten|muessen"
    r"|wuerde|wuerden|laesst|laengst|haelt|haengt|haengen|gehoert|erwaehnt"
    r"|schoen|schoene\w*|groesser|groesste\w*|spaeter|naechste\w*|taeglich"
    r"|haeufig\w*|ueblich\w*|Kaeufer\w*|Saetze\w*|Woerter\w*|Geruest"
    r"|Aenderung\w*|Moeglichkeit\w*|Loesung\w*|Gespraech\w*|Erklaerung\w*"
    r"|waehrend|waehlen|zurueck|fuenf|ueberall|natuerlich|wuenschen"
    r")\b", re.IGNORECASE)


def sichtbarer_text(html_text):
    """Nur was die Leserin sieht — ohne Kommentar-Block und ohne Tags."""
    ohne = re.sub(r"<!--[\s\S]*?-->", " ", html_text)
    ohne = re.sub(r"<[^>]+>", " ", ohne)
    return re.sub(r"\s+", " ", ohne)


def umlaute_pruefen(datei, html_text):
    sicht = sichtbarer_text(html_text)
    treffer = sorted(set(UMSCHRIEBEN.findall(sicht)))
    if treffer:
        print("  \u26a0 %s: ae/oe/ue statt Umlaut -> %s" % (datei, ", ".join(treffer)))

    # Schweizer ss: das deutsche Eszett gehoert in keinen Text. Es muss nach
    # html.unescape geprueft werden \u2014 als &szlig; geschrieben steht es sonst
    # unsichtbar im Quelltext und rutscht durch (so passiert am 06.10.2026).
    klar = html.unescape(sicht)
    scharf = sorted({w for w in re.findall(r"\b\w*\u00df\w*\b", klar)})
    if scharf:
        print("  \u26a0 %s: deutsches \u00df statt ss -> %s" % (datei, ", ".join(scharf)))
        treffer = treffer + scharf

    return treffer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--liste", action="store_true", help="nur die Strecke zeigen")
    args = ap.parse_args()

    print("Die Strecke:\n")
    print("  %-5s %-22s %s" % ("Tag", "Wartezeit", "Betreff"))
    print("  " + "-" * 78)
    for m in MAILS:
        print("  %-5s %-22s %s" % (m["tag"], m["warten"], m["betreff"]))
    print("")
    print("  +5 Tage  ->  Tag setzen, Automation 72 (Engine, Loop 1)"
          "  ->  Finde dein Thema 39.")
    print("               Loop 6 abklemmen (IKM war schon Tag 12),"
          " Skip-Goal Thema pruefen.")
    print("")

    if args.liste:
        return

    ZIEL.mkdir(parents=True, exist_ok=True)
    karten = []
    beanstandet = 0
    for m in MAILS:
        fertig = bauen(m)
        beanstandet += len(umlaute_pruefen(m["datei"], fertig))
        (ZIEL / m["datei"]).write_text(fertig, encoding="utf-8")
        kennung = re.sub(r"[^a-z0-9]+", "", m["datei"].lower())
        karten.append(KARTE.format(
            tag=m["tag"], h1=m["h1"], warten=m["warten"],
            betreff=html.escape(m["betreff"], quote=False),
            betreff_roh=html.escape(m["betreff"], quote=True),
            datei=m["datei"], id=kennung))
        print("  geschrieben: %s" % m["datei"])

    (ZIEL / "index.html").write_text(
        KOPIERSEITE.format(karten="\n".join(karten)), encoding="utf-8")
    print("  geschrieben: index.html (Kopierseite)")
    if beanstandet:
        print("\n  \u26a0 %d Stelle(n) mit ae/oe/ue statt Umlaut."
              % beanstandet)
    else:
        print("\n  \u2713 Keine umschriebenen Umlaute im sichtbaren Text.")
    print('\nAnsehen:  preview_start {"name": "startklar-mail"}  ->  Port 4386')


if __name__ == "__main__":
    main()
