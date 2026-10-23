"""
Baut die HTML-Mails der Produkt-Ideen-Finder-Bruecke (Mail 2a/2b/3/4).

Eine Vorlage, vier Mails — damit Design-Aenderungen an genau einer Stelle
passieren und nicht viermal von Hand nachgezogen werden muessen. Die Vorlage
ist identisch zu `mails/mail-1-auslieferung.html` (Georgia-Headline,
Arial-Body, Brandfarben, Creme-Box mit Petrol-Kante).

Aufruf:
  python scripts/funnels/finder-mails-bauen.py
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "funnels" / "produkt-ideen-finder" / "mails"

DUNKELBLAU = "#0c1c30"
PETROL = "#12828c"
MITTELBLAU = "#29556d"
ORANGE = "#dc822e"
CREME = "#f1ecdd"

TOOL = "https://produkt-ideen-finder-service.vercel.app/"
MINIKURS = "https://mumlifebalance.thrivecart.com/eigene-produkterstellung/"

P = ('<p style="margin:0 0 18px 0;font-family:Arial,sans-serif;font-size:16px;'
     'color:%s;line-height:1.7;">%%s</p>' % DUNKELBLAU)


def absatz(text):
    return P % text


def knopf(text, url):
    return (
        '<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0;">'
        '<tr><td align="center">'
        '<a href="%s" style="display:inline-block;background-color:%s;color:#ffffff;'
        'text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;font-size:16px;'
        'padding:16px 32px;border-radius:12px;">%s</a>'
        '</td></tr></table>' % (url, ORANGE, text)
    )


def kasten(zeilen):
    """Creme-Box mit Petrol-Kante. Erste Zeile gross (Georgia), Rest normal."""
    inhalt = []
    for i, zeile in enumerate(zeilen):
        if i == 0:
            inhalt.append(
                '<p style="margin:0 0 14px 0;font-family:Georgia,serif;font-size:18px;'
                'font-weight:bold;color:%s;line-height:1.45;">%s</p>' % (DUNKELBLAU, zeile))
        else:
            letzte = i == len(zeilen) - 1
            inhalt.append(
                '<p style="margin:0 0 %dpx 0;font-family:Arial,sans-serif;font-size:16px;'
                'color:%s;line-height:1.7;">%s</p>' % (0 if letzte else 14, DUNKELBLAU, zeile))
    return (
        '<table width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin:26px 0;">'
        '<tr><td style="background-color:%s;border-left:4px solid %s;border-radius:0 12px 12px 0;'
        'padding:24px 26px;">%s</td></tr></table>' % (CREME, PETROL, "".join(inhalt))
    )


def seite(titel, preheader, headline, subline, koerper, ps):
    return """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titel}</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f0e6;font-family:Arial,sans-serif;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{preheader} &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f0e6;">
    <tr>
      <td align="center" style="padding:30px 16px;">
        <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;">
          <tr>
            <td style="background-color:{petrol};background:linear-gradient(135deg,{dunkelblau} 0%,{mittelblau} 60%,{petrol} 100%);border-radius:16px 16px 0 0;padding:48px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr><td style="padding-bottom:20px;"><table cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;"><tr><td bgcolor="{orange}" style="background-color:{orange};border-radius:20px;padding:6px 14px;color:#ffffff;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;letter-spacing:2px;line-height:1.5;text-transform:uppercase;">mumlifebalance &middot; deine Idee</td></tr></table></td></tr>
                <tr><td><h1 style="margin:0 0 16px 0;font-family:Georgia,serif;font-size:32px;font-weight:bold;color:{creme};line-height:1.25;">{headline}</h1></td></tr>
                <tr><td><p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:16px;color:rgba(241,236,221,0.72);line-height:1.5;">{subline}</p></td></tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#ffffff;padding:40px;">
{koerper}
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #e6e0d2;">
                <tr><td style="padding-top:22px;">
                  <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;color:rgba(12,28,48,0.62);line-height:1.65;"><strong>P.S.</strong> {ps}</p>
                </td></tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:{dunkelblau};border-radius:0 0 16px 16px;padding:28px 40px;text-align:center;">
              <p style="margin:0 0 6px 0;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:{creme};text-transform:uppercase;letter-spacing:1px;">MUMLIFEBALANCE &middot; PATRICIA ULMANN</p>
              <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:rgba(241,236,221,0.55);">Network + Onlinekurse f&uuml;r Mamas</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
""".replace("{titel}", titel).replace("{preheader}", preheader) \
   .replace("{headline}", headline).replace("{subline}", subline) \
   .replace("{koerper}", koerper).replace("{ps}", ps) \
   .replace("{petrol}", PETROL).replace("{dunkelblau}", DUNKELBLAU) \
   .replace("{mittelblau}", MITTELBLAU).replace("{orange}", ORANGE) \
   .replace("{creme}", CREME)


GRUSS = absatz("Liebe Grüsse<br>Patricia")

# --------------------------------------------------------------------------
# Mail 2a — Tag 1, Link nicht geklickt
# --------------------------------------------------------------------------
mail_2a = seite(
    titel="Der Finder liegt noch bei dir rum",
    preheader="Eine Frage daraus kannst du auch ohne Tool beantworten.",
    headline="Der Finder liegt noch bei dir rum",
    subline="Zwischen Znacht und Zähneputzen geht so ein Link einfach unter.",
    koerper="\n".join([
        absatz("Hey,"),
        absatz("gestern hab ich dir den Produkt-Ideen-Finder geschickt, und ich hab so eine "
               "Ahnung, wie dein Abend danach aussah. Zwischen Znacht, Znüni-Böxli für morgen "
               "und dem Kind, das um halb neun nochmal Durst hat, ist so ein Link einfach weg."),
        absatz("Deshalb heute nochmal, ganz in Ruhe:"),
        knopf("Zum Produkt-Ideen-Finder", TOOL),
        absatz("Und falls du gerade wieder keine fünf Minuten hast, dann nimm wenigstens die "
               "eine Frage mit, um die sich im Finder am Ende alles dreht:"),
        kasten([
            "Wofür fragen dich Leute schon heute — ohne dass du dafür wirbst?",
            "Das ist meistens näher an deinem eigenen Produkt als alles, was du dir am "
            "Schreibtisch ausdenken würdest. Die Sachen, für die man dich einfach fragt, "
            "fühlen sich für dich nach nichts an. Für die andere sind sie genau der Grund, "
            "warum sie dich fragt.",
        ]),
        absatz("Und falls du jetzt denkst „mich fragt doch niemand was“ — das denken sehr "
               "viele Frauen ungefähr zwei Minuten, bevor ihnen drei Sachen einfallen."),
        GRUSS,
    ]),
    ps="Der Link läuft nicht ab. Ich schreib dir trotzdem nochmal, weil ich weiss, wie so ein "
       "Postfach aussieht.",
)

# --------------------------------------------------------------------------
# Mail 2b — Tag 1, Link geklickt
# --------------------------------------------------------------------------
mail_2b = seite(
    titel="Was ist bei dir rausgekommen?",
    preheader="Ich lese das wirklich selbst.",
    headline="Was ist bei dir rausgekommen?",
    subline="Ein Satz reicht. Auch wenn er sich noch wackelig anfühlt.",
    koerper="\n".join([
        absatz("Hey,"),
        absatz("du warst gestern im Produkt-Ideen-Finder. Und jetzt bin ich ehrlich neugierig:"),
        kasten([
            "Was ist bei dir rausgekommen?",
            "Antworte einfach auf diese Mail. Ein Satz reicht. „Irgendwas mit Meal-Prep für "
            "Schichtarbeiterinnen“ reicht auch, wenn es sich noch wackelig anfühlt.",
        ]),
        absatz("Ich frag aus zwei Gründen."),
        absatz("Der erste ist eigennützig: ich hab das Ding selbst gebaut und will sehen, was "
               "es bei echten Frauen ausspuckt. Was gut trifft und was danebenliegt."),
        absatz("Der zweite ist für dich. Eine Idee, die du einmal aufgeschrieben und einem "
               "anderen Menschen geschickt hast, verhält sich anders als eine, die in deinem "
               "Kopf wohnt. Im Kopf wird sie über Nacht grösser, komplizierter und irgendwie "
               "peinlich. Auf dem Bildschirm steht sie einfach da und lässt sich anschauen."),
        absatz("Und genau da bleibt es bei vielen liegen."),
        absatz("Also: schreib mir, was rausgekommen ist. Häng gern gleich dran, was dich daran "
               "am meisten nervt oder unsicher macht — darauf antworte ich dir."),
        GRUSS,
    ]),
    ps="Falls beim Finder etwas schräg gelaufen ist, eine Frage doppelt kam oder die Antwort "
       "komisch war: schreib mir das auch. Ich bau daran weiter.",
)

# --------------------------------------------------------------------------
# Mail 3 — Tag 3
# --------------------------------------------------------------------------
mail_3 = seite(
    titel="Deine Idee ist noch kein Produkt",
    preheader="Eine Übung für heute Abend, dauert zwei Minuten.",
    headline="Deine Idee ist noch kein Produkt",
    subline="Ein Zettel, zwei Minuten, ein Satz.",
    koerper="\n".join([
        absatz("Hey,"),
        absatz("jetzt liegt da also eine Idee. Und vermutlich passiert gerade genau das: du "
               "drehst sie ein paar Tage im Kopf, sie wird dabei immer grösser, und irgendwann "
               "kommt der Gedanke „dafür müsste ich ja erst mal richtig was aufbauen“. Danach "
               "wandert sie zu den anderen Ideen in die Schublade."),
        absatz("Ganz ehrlich? Das hat nichts mit Disziplin zu tun."),
        absatz("Eine Idee ist ein Thema. Ein Produkt ist ein Ende. Solange du das Ende nicht "
               "benennen kannst, bleibt es etwas, worüber du reden kannst. Kaufen kann es noch "
               "niemand."),
        absatz("Deshalb die Übung für heute Abend:"),
        kasten([
            "„Am Ende hat sie ______ — und zwar in ______.“",
            "So einer könnte heissen: „Am Ende hat sie ihren Vorratsschrank so sortiert, dass "
            "sie unter der Woche ohne Nachdenken kocht — und zwar an einem Samstagvormittag.“ "
            "Oder: „Am Ende hat sie ein Profil, bei dem man in drei Sekunden versteht, wofür "
            "sie da ist — und zwar an einem Abend.“",
        ]),
        absatz("Spürst du den Unterschied? „Ich mach was mit Ernährung“ ist ein Interesse. Der "
               "Satz oben ist ein Angebot. Und der zweite Teil, das „und zwar in“, macht die "
               "halbe Arbeit: er sagt der Frau, dass sie dafür kein halbes Jahr braucht."),
        absatz("Der Satz muss heute nicht schön sein. Er muss existieren."),
        absatz("Schick ihn mir, wenn du magst — antworte einfach auf diese Mail, ich schau "
               "drüber. Und falls du beim Aufschreiben merkst, dass dir für den zweiten Teil "
               "das Handwerk fehlt: dafür hab ich was. Dazu in ein paar Tagen mehr, heute "
               "reicht der Zettel."),
        GRUSS,
    ]),
    ps="Wenn dir gar nichts einfällt, ist das auch eine Antwort. Dann ist die Idee noch zu "
       "gross. Nimm den kleinsten Teil davon, den du an einem Nachmittag erklären könntest, "
       "und schreib den Satz nochmal.",
)

# --------------------------------------------------------------------------
# Mail 4 — Tag 6
# --------------------------------------------------------------------------
mail_4 = seite(
    titel="Von der Idee zu etwas, das man kaufen kann",
    preheader="39 Franken, weniger als ein Familien-Znacht auswärts.",
    headline="Von der Idee zu etwas, das man kaufen kann",
    subline="Der Teil, an dem fast alle aufhören.",
    koerper="\n".join([
        absatz("Hey,"),
        absatz("vor ein paar Tagen hast du eine Idee bekommen. Vielleicht liegt sie noch da, "
               "vielleicht steht der Satz auf einem Zettel."),
        absatz("Und jetzt kommt der Teil, den keine von uns mag: aus der Idee muss etwas "
               "werden, das man anklicken und bezahlen kann."),
        absatz("Da stolpern fast alle über dieselben drei Sachen."),
        absatz("<strong style=\"color:%s;\">Erstens: es soll perfekt sein.</strong> Dein erstes "
               "Produkt ist kein Lebenswerk. Es ist der erste Beweis, dass jemand für dein "
               "Wissen Geld ausgibt. Klein und fertig schlägt gross und irgendwann." % PETROL),
        absatz("<strong style=\"color:%s;\">Zweitens: die Technik.</strong> Die ist heute "
               "wirklich das kleinste Problem, auch wenn sie sich als grösstes anfühlt. Ein "
               "Verkaufslink, eine Datei, eine Mail — viel mehr braucht ein erstes Produkt "
               "nicht." % PETROL),
        absatz("<strong style=\"color:%s;\">Drittens: „wer bin ich denn“.</strong> Du musst "
               "nicht die Beste auf dem Thema sein. Du musst ein paar Schritte weiter sein als "
               "die Frau, der du hilfst. Genau dafür fragt sie dich ja." % PETROL),
        absatz("Den ganzen Weg dazwischen — von der Idee bis zu dem Ding, das online steht und "
               "für dich arbeitet — hab ich in einen kleinen Kurs gepackt: "
               "<strong>Vom Network-Wissen zum eigenen Produkt.</strong> 39 Franken, weniger "
               "als ein Familien-Znacht auswärts."),
        knopf("Ich will mein eigenes Produkt bauen", MINIKURS),
        absatz("Und falls du gerade denkst, du hättest zu wenig Wissen für etwas Eigenes: du "
               "beantwortest seit Monaten oder Jahren die Fragen von Leuten, die genau da "
               "stehen, wo du mal warst. Das ist das Wissen. Es hat nur noch keinen Preis."),
        GRUSS,
    ]),
    ps="Du gibst dabei nichts auf. Dein Network bleibt, wo es ist. Du stellst nur etwas "
       "daneben, das dir gehört.",
)


DATEIEN = {
    "mail-2a-nachfassen.html": mail_2a,
    "mail-2b-was-kam-raus.html": mail_2b,
    "mail-3-idee-ist-kein-produkt.html": mail_3,
    "mail-4-minikurs.html": mail_4,
}


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, inhalt in DATEIEN.items():
        pfad = ZIEL / name
        pfad.write_text(inhalt, encoding="utf-8")
        print("  %-34s %6d Zeichen" % (name, len(inhalt)))
    print("\nAbgelegt in: %s" % ZIEL)


if __name__ == "__main__":
    main()
