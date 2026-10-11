# -*- coding: utf-8 -*-
"""Die Launch-Strecke an die ÜBRIGE Mailliste — KI-Kurs, Oktober 2026.

    python scripts/ki-kurs/liste-mails-bauen.py           # alle Mails
    python scripts/ki-kurs/liste-mails-bauen.py --liste   # nur die Strecke

WER DAS BEKOMMT: alle auf der Liste, die **nicht** im Webinar-Funnel stecken.
Sie waren nicht in der Masterclass, haben keinen Stimm-Check gemacht und wissen
unter Umständen gar nicht, dass es einen Kurs gibt. Deshalb fängt Mail 1 bei
null an und erklärt, statt an etwas anzuknüpfen.

WARUM ÜBERHAUPT: Julia schickt die Pitch-Mails an alle — „wer nicht zugeschaut
hat, bekommt dieselben Pitch-Mails, sie unterscheidet bewusst nicht, weil es
sonst zu kompliziert wird." Dazu ihre Alltagsregel: jede Woche eine Mail an die
Liste, mit Angebot und Link, kein reiner Newsletter. Ihr eigener dokumentierter
Fehler: im Juni null Mails ausserhalb der Funnels.

🚨 KEINE ERFUNDENEN BELEGE. Jede Zahl und jede Szene in diesen Mails steht in
   einer Quelle im Workspace:
     · vier Kinder, 18 Stunden Woche, keine technische Ausbildung
       → outputs/produkte/ki-treppe/04-kursplattform-texte.md (Begrüssung)
     · Kochbot, Cockpit-Bot, Freigabe statt Autopilot, Doppelpost-Fehler
       → dieselbe Datei, Module 6, 7, 9
     · Zugangsschlüssel und 32 Kundinnen offen im Repo
       → dieselbe Datei, Lektion 10.1 (und CLAUDE.md, 13.09.2026)
     · die Kundin, die Claude selbst installiert hat
       → context/kundinnen-geschichten.md, Kundin A
   Was dort nicht steht, steht auch hier nicht.

🚨 KUNDIN A NUR ANONYM UND NUR ALS ZUSAMMENFASSUNG. Ihre Freigabe steht auf
   „offen", und ihr Wortlaut liegt als Sprachnachricht auf dem Handy, nicht
   abgetippt. Also keine Anführungszeichen, kein Name, keine erkennbaren
   Details — sonst wäre es ein erfundenes Zitat.

🚨 SCREENSHOTS GIBT ES NOCH KEINE. Mail 5 trägt deshalb einen vorbereiteten,
   leeren Beweis-Kasten mit Anleitung statt eines erfundenen. Sobald eine
   Kundin freigibt, wird der Kasten gefüllt — nicht vorher.
"""
import argparse
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
ZIEL = ROOT / "outputs" / "produkte" / "ki-treppe" / "liste-mails"

# Das Gerüst wird IMPORTIERT, nicht kopiert — sonst ändert man es später
# an einer Stelle und an drei anderen nicht (Regel aus CLAUDE.md, Magnet-Ich).
_spec = importlib.util.spec_from_file_location(
    "startklar_mails", ROOT / "scripts" / "startklar" / "mails-bauen.py")
_sk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sk)

absatz, kasten, merken, liste = _sk.absatz, _sk.kasten, _sk.merken, _sk.liste
knopf, h2, ps, gruss, bauen = _sk.knopf, _sk.h2, _sk.ps, _sk.gruss, _sk.bauen
PETROL, DUNKEL, NACHT = _sk.PETROL, _sk.DUNKEL, _sk.NACHT
CREME, ORANGE = _sk.CREME, _sk.ORANGE

# --- Die festen Angaben ------------------------------------------------------
KURS = "https://mumlifebalance.ch/ki-kurs/"
AUFZEICHNUNG = "https://vimeo.com/1233995735/e14aa6e93c"
ACADEMY = "https://mumlifebalance.thrivecart.com/mba-webinar/"

PREIS_FRUEH, PREIS_SPAET = "277", "333"
FRUEH_ENDE = "Donnerstag, 15. Oktober, 21 Uhr"
SCHLUSS = "Donnerstag, 23. Oktober, 21 Uhr"


def beweis_platz():
    """🚨 Ein vorbereiteter, LEERER Beweis-Kasten.

    Hormozi setzt an diese Stelle einen Screenshot — bei Patricia gibt es noch
    keinen freigegebenen. Ein erfundener wäre der schlimmste aller Fehler, ein
    weggelassener verschenkt die Stelle. Also steht der Platz da, sichtbar
    markiert, mit der Anleitung zum Füllen.
    """
    return kasten(
        '<p style="margin:0 0 10px 0;font-family:Arial,sans-serif;font-size:15px;'
        'color:#9a8f7c;line-height:1.7;"><strong>&#9888;&#65039; Hier geh&ouml;rt ein '
        'Screenshot hin &mdash; vor dem Versand einsetzen oder diesen Kasten l&ouml;schen.'
        '</strong></p>'
        '<p style="margin:0;font-family:Arial,sans-serif;font-size:14px;color:#9a8f7c;'
        'line-height:1.7;">Ein abfotografierter Chat oder eine abgetippte Sprachnachricht '
        'wirkt st&auml;rker als jeder Satz von mir. Frag die Kundin vorher, ob du es zeigen '
        'darfst. Ohne ihr Ja bleibt der Kasten leer.</p>',
        "#f6f3ea", rand="#d8d0bd")


# ============================================================================
#  DIE STRECKE — acht Mails, 10. bis 23. Oktober
# ============================================================================
#  Taktung nach Julias Muster: regelmässig bis zum Frühbucher-Ende, dann eine
#  ruhigere Woche, dann am Schlusstag zwei Mails (morgens und abends).
# ============================================================================

MAILS = [

# ------------------------------------------------------------------ Fr 10.10.
{
 "datei": "liste-01-aufzeichnung.html", "tag": "Fr 10.10.", "warten": "Start der Strecke",
 "marke": "mumlifebalance",
 "betreff": "Falls du die Masterclass verpasst hast",
 "betreff2": "Die Aufzeichnung — 45 Minuten, und der eine Satz daraus",
 "wann": "Freitag, 10. Oktober, 08:00",
 "preheader": "Der eine Satz, der erklärt, warum KI dich bisher Zeit gekostet hat",
 "h1": "Die Aufzeichnung für dich",
 "unterzeile": "45 Minuten. Und ein Satz, der reicht, falls du sie nicht schaust.",
 "notiz": """
Mehrwert-Mail, kein harter Pitch. Diese Leute waren nicht dabei und wissen
vielleicht nicht einmal, dass es eine Masterclass gab — also kein Vorwurf,
kein „du hast verpasst", sondern einfach aufmachen.
Der Kurs kommt am Schluss als Angebot, nicht als Hauptsache.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("am Donnerstag habe ich eine Masterclass gehalten und dabei gezeigt, "
          "wie ich mit KI arbeite. Sie nimmt mir tats&auml;chlich Arbeit ab, statt "
          "dass ich hinterher die H&auml;lfte umschreibe."),
   absatz("Falls du nicht dabei warst: hier ist die Aufzeichnung."),
   knopf("Zur Aufzeichnung", AUFZEICHNUNG),
   absatz("Und falls du die 45 Minuten gerade nicht hast, nimm diesen einen Satz "
          "mit, weil er das Wichtigste ist:"),
   merken("Der Kern", "Deine KI muss dich kennen. Und sie muss wissen, was zu tun ist.",
          "Solange eins von beidem fehlt, f&auml;ngst du jede Woche wieder bei null an "
          "&mdash; und genau das kostet dich die Zeit, die sie dir eigentlich sparen sollte."),
   absatz("Das klingt banal, ist es aber nicht. Die meisten arbeiten mit KI wie mit "
          "einer Suchmaschine: Frage rein, Antwort raus, n&auml;chste Woche dasselbe "
          "nochmal. Dabei k&ouml;nnte dort dein ganzes Wissen liegen &mdash; deine "
          "Sprache, deine Angebote, deine Kundin &mdash; und jeder Auftrag w&uuml;rde "
          "darauf aufbauen."),
   h2("Wenn du das bei dir einrichten willst"),
   absatz("Daf&uuml;r habe ich einen Kurs gebaut: <strong>Easy KI f&uuml;r "
          "Networkerinnen &mdash; vom Chat zur Mitarbeiterin</strong>. Du f&auml;ngst "
          "im Chat an, den du schon kennst, und installierst erst sp&auml;ter etwas. "
          "Die Kapitel kommen ab dem 1. November Woche f&uuml;r Woche, am 30. November "
          "ist er komplett."),
   liste("Was du am Ende hast", [
       "Einen <strong>Arbeitsplatz mit deinem Wissen drin</strong>, den deine KI bei "
       "jedem Auftrag liest",
       "Deinen <strong>ersten eigenen Skill</strong> f&uuml;r eine Arbeit, die jede "
       "Woche wiederkommt",
       "Einen <strong>Bot, der von selbst l&auml;uft</strong> &mdash; so wie mein "
       "Kochbot, der mir die Men&uuml;planung abnimmt"]),
   knopf("Alles zum Kurs", KURS),
   # Patricia am 08.10.2026: „da wo ich die aufzeichnung verschicke, will ich
   # einmal die erwähnung der mba. weil ich rede ja im webinar darüber."
   # Einmal, kurz — wer die Aufzeichnung schaut, hört den Pitch ohnehin, und
   # dann soll in der Mail stehen, wo es langgeht.
   absatz("Ganz am Schluss der Aufzeichnung zeige ich noch die <strong>Mum Business "
          "Academy</strong>: alle vier Kurse, der KI-Kurs ab dem 1. November inklusive, "
          "dazu ein Jahr Begleitung in der Gruppe und zweimal im Monat ein Call. Falls "
          "dich das mehr reizt als der einzelne Kurs, findest du sie "
          "<a href=\"" + ACADEMY + "\" style=\"color:" + PETROL + ";\">hier</a>."),
   gruss("Bis bald,"),
   ps("P.S. Der Fr&uuml;hbucherpreis von " + PREIS_FRUEH + " gilt bis " + FRUEH_ENDE +
      ", danach kostet der Kurs " + PREIS_SPAET + "."),
 ]},

# ------------------------------------------------------------------ So 12.10.
{
 "datei": "liste-02-mechanismus.html", "tag": "So 12.10.", "warten": "2 Tage",
 "marke": "mumlifebalance",
 "betreff": "Warum deine KI jede Woche wieder bei null anfängt",
 "betreff2": "Das Problem ist nicht der Prompt",
 "wann": "Sonntag, 12. Oktober, 08:00",
 "preheader": "Und was du heute in zwanzig Minuten dagegen tun kannst",
 "h1": "Das Problem ist nicht dein Prompt",
 "unterzeile": "Sondern dass die KI nach jedem Chat wieder alles vergessen hat.",
 "notiz": """
Mehrwert-Mail mit echtem Tipp (Hormozi: erst liefern, dann fragen).
Der Tipp funktioniert OHNE den Kurs — das ist Absicht. Wer ihn umsetzt, merkt
selbst, dass es mit einem festen Arbeitsplatz besser ginge.
🚨 Der Betreff enthält bewusst KEIN „nicht X, sondern Y" im Fliesstext.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("kennst du das: Du l&auml;sst dir eine Caption schreiben, baust jeden "
          "zweiten Satz um, weil er nach niemandem klingt, und machst n&auml;chste "
          "Woche genau dasselbe nochmal?"),
   absatz("Das liegt nicht daran, dass du den falschen Prompt benutzt. Es liegt "
          "daran, dass die KI dich nach jedem Chat wieder vergessen hat."),
   h2("Was bei mir anders l&auml;uft"),
   absatz("Bei mir liegt mein Wissen an einem festen Ort: wie ich schreibe, welche "
          "W&ouml;rter nie vorkommen d&uuml;rfen, wer meine Kundin ist, was ich "
          "verkaufe. Jeder Auftrag liest das zuerst. Ich erkl&auml;re es kein "
          "zweites Mal."),
   absatz("Deshalb klingt, was herauskommt, nach mir &mdash; und nicht nach einer "
          "KI, die h&ouml;flich alles bejaht."),
   h2("Was du heute tun kannst, ohne irgendetwas zu installieren"),
   liste("Zwanzig Minuten, und es wirkt sofort", [
       "&Ouml;ffne ein leeres Dokument und schreib auf, <strong>wie du klingst</strong>: "
       "drei S&auml;tze, die typisch f&uuml;r dich sind, und f&uuml;nf W&ouml;rter, die "
       "du nie benutzen w&uuml;rdest.",
       "Schreib darunter, <strong>wer deine Kundin ist</strong> &mdash; in einem Satz, "
       "und zwar so, wie du es einer Freundin erz&auml;hlen w&uuml;rdest.",
       "Schreib darunter, <strong>was du verkaufst</strong>, mit Preis.",
       "Kopier das k&uuml;nftig <strong>vor jeden Auftrag</strong> in den Chat."],
      hintergrund="#e4f3f4"),
   absatz("Das ist die einfachste Fassung von dem, was ich meinen Arbeitsplatz nenne. "
          "Es ist umst&auml;ndlich, weil du es jedes Mal einf&uuml;gen musst &mdash; "
          "aber du wirst am Ergebnis sofort merken, was der Unterschied ist."),
   merken("Und genau da f&auml;ngt der Kurs an",
          "Im Kurs liegt diese Datei fest an ihrem Platz, und jeder Auftrag liest sie "
          "von allein.",
          "Dazu kommen die Bausteine, die darauf aufbauen: dein erster eigener Skill "
          "und ein Bot, der morgens von selbst schreibt."),
   knopf("Alles zum Kurs", KURS),
   gruss("Bis bald,"),
   ps("P.S. Wenn du den Zettel wirklich machst, schreib mir, was sich ver&auml;ndert "
      "hat. Ich lese jede Antwort selbst."),
 ]},

# ------------------------------------------------------------------ Di 14.10.
{
 "datei": "liste-03-einwand-technik.html", "tag": "Di 14.10.", "warten": "2 Tage",
 "marke": "mumlifebalance",
 "betreff": "„Ich bin da echt nicht die Technische“",
 "betreff2": "Der Satz, den ich am häufigsten höre",
 "wann": "Dienstag, 14. Oktober, 08:00",
 "preheader": "Vier Kinder, achtzehn Stunden Woche, keine technische Ausbildung",
 "h1": "„Ich bin da echt nicht die Technische“",
 "unterzeile": "Den Satz höre ich öfter als jeden anderen. Also reden wir darüber.",
 "notiz": """
Einwand-Mail. Der stärkste Beweis ist nicht Patricia selbst, sondern eine
normale Kundin (Podcast-Notiz: „die ist wie ich, und die hat es geschafft").
🚨 Die Kundin steht ANONYM und als ZUSAMMENFASSUNG drin — ihre Freigabe ist
   offen, ihr Wortlaut liegt unabgetippt auf dem Handy. Keine Anführungszeichen.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("wenn ich erz&auml;hle, dass ich mir Bots baue, die mir morgens aufs Handy "
          "schreiben, kommt fast immer derselbe Satz zur&uuml;ck. Ich bin da echt "
          "nicht die Technische."),
   absatz("Verstehe ich. Ich war es auch nicht."),
   kasten(
     '<p style="margin:0;font-family:Arial,sans-serif;font-size:16px;color:%s;'
     'line-height:1.8;">Ich habe das <strong>neben vier Kindern</strong> gelernt, mit '
     'einer <strong>Achtzehn-Stunden-Woche</strong> und <strong>ohne technische '
     'Ausbildung</strong>. Programmiert habe ich dabei nichts. Ich schreibe Deutsch, '
     'so wie hier.</p>' % NACHT,
     "#e4f3f4", rand=PETROL),
   h2("Und eine Kundin war schneller als ich"),
   absatz("Ende September habe ich einer Kundin per Sprachnachricht erz&auml;hlt, was "
          "ich alles mit Claude mache. Sie hat es sich daraufhin mit meiner Anleitung "
          "<strong>selbst eingerichtet</strong> &mdash; ohne Kurs, ohne dass ich "
          "danebensass."),
   absatz("Was sie mir danach zur&uuml;ckgeschrieben hat, lief darauf hinaus: Sie war "
          "krass schnell mit ihrem Zeug fertig und hatte danach tausend Ideen, was sie "
          "damit noch machen k&ouml;nnte. <em>(Das ist meine Zusammenfassung ihrer "
          "Sprachnachricht, nicht ihr Wortlaut.)</em>"),
   absatz("Sie ist keine Entwicklerin. Sie ist Networkerin, so wie du."),
   h2("Warum das geht"),
   liste("Der Kurs ist daf&uuml;r gebaut", [
       "<strong>Du musst nichts programmieren.</strong> Du schreibst Deutsch.",
       "<strong>Drei Stufen, auf jeder ein Ergebnis.</strong> Erst der normale Chat, "
       "dann eine Zwischenstufe, dann der eigene Arbeitsplatz. Wer nach Stufe eins "
       "aufh&ouml;rt, hat trotzdem etwas, das sie beh&auml;lt.",
       "<strong>Alles mitgefilmt.</strong> Vom ersten Klick bis zur ersten Nachricht "
       "auf deinem Handy &mdash; und wenn der Bot schweigt, zeige ich dir die drei "
       "Stellen, an denen es normalerweise liegt."]),
   knopf("Alles zum Kurs", KURS),
   gruss("Bis bald,"),
   ps("P.S. Morgen Abend um 21 Uhr endet der Fr&uuml;hbucherpreis von " + PREIS_FRUEH +
      ". Danach kostet der Kurs " + PREIS_SPAET + "."),
 ]},

# ------------------------------------------------------------------ Mi 15.10.
{
 "datei": "liste-04-fruehbucher-endet.html", "tag": "Mi 15.10.", "warten": "1 Tag",
 "marke": "mumlifebalance",
 "betreff": "Heute Abend um 21 Uhr steigt der Preis",
 "betreff2": "Letzter Tag zum Frühbucherpreis",
 "wann": "Mittwoch, 15. Oktober, 08:00",
 "preheader": "277 bis heute Abend, danach 333",
 "h1": "Heute Abend um 21 Uhr",
 "unterzeile": "Danach kostet der Kurs 333 statt 277.",
 "notiz": """
Kurze Frist-Mail. Ein Gedanke, ein Knopf, kein neuer Inhalt.
🚨 Nichts aufbauschen: der Kurs ist danach weiter da, nur teurer. Genau das
   steht auch so drin — eine Frist, die mehr behauptet, als sie ist, zerstört
   die nächste.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("nur kurz, weil heute der letzte Tag ist: Der Fr&uuml;hbucherpreis f&uuml;r "
          "<strong>Easy KI f&uuml;r Networkerinnen</strong> gilt bis heute Abend um "
          "21 Uhr. Danach kostet der Kurs " + PREIS_SPAET + " statt " + PREIS_FRUEH + "."),
   merken("Worum es geht",
          "Am Ende hast du einen Arbeitsplatz mit deinem Wissen, deinen ersten eigenen "
          "Skill und einen Bot, der von selbst l&auml;uft.",
          "Start ist der 1. November, die Kapitel kommen Woche f&uuml;r Woche, am "
          "30. November ist der Kurs komplett."),
   knopf("Jetzt zu " + PREIS_FRUEH + " sichern", KURS),
   absatz("Falls du noch &uuml;berlegst: Der Kurs ist auch danach da. Es wird nur "
          "teurer, und das f&auml;nde ich schade, wenn du ohnehin einsteigen wolltest."),
   gruss("Bis bald,"),
   ps("P.S. Die Anmeldung bleibt bis zum " + SCHLUSS + " offen, danach schliesst sie "
      "ganz &mdash; weil ich die Gruppe w&auml;hrend der vier Wochen begleite."),
 ]},

# ------------------------------------------------------------------ So 19.10.
{
 "datei": "liste-05-mein-freitag.html", "tag": "So 19.10.", "warten": "4 Tage",
 "marke": "mumlifebalance",
 "betreff": "Was bei mir am Freitagmorgen passiert, während ich noch schlafe",
 "betreff2": "Ein ganz normaler Freitag",
 "wann": "Sonntag, 19. Oktober, 08:00",
 "preheader": "Kein Hochglanz, nur was tatsächlich läuft — inklusive dem, was schiefging",
 "h1": "Ein ganz normaler Freitag bei mir",
 "unterzeile": "Ohne Hochglanz. Mit dem Fehler, der mich fast einen Doppelpost gekostet hat.",
 "notiz": """
Beweis-Mail. Konkreter Alltag statt Versprechen — und bewusst MIT Panne,
weil eine Geschichte ohne Reibung wie Werbung klingt.
🚨 Alle Beispiele sind belegt: Kochbot (Modul 6.2), Freitags-Content (Modul 7),
   Freigabe statt Autopilot (7.5), Doppelpost (9.4), Sicherheitsvorfall (10.1).
🚨 Der leere Beweis-Kasten steht bewusst drin. Vor dem Versand füllen oder raus.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("ich erz&auml;hle dir heute keinen Nutzen, sondern einen Freitag."),
   liste("Was l&auml;uft, bevor ich am Rechner sitze", [
       "<strong>Morgens</strong> liegt der Content f&uuml;r die ganze Woche fertig da "
       "&mdash; Reels, Karussells, Captions, je zwei Varianten zum Aussuchen.",
       "<strong>Der Kochbot</strong> hat den Men&uuml;plan und die Einkaufsliste "
       "geschickt, sortiert nach dem Laden, in dem ich einkaufe.",
       "<strong>Im Cockpit</strong> steht, was heute ansteht, was noch fehlt und wer "
       "daf&uuml;r dran ist."],
      hintergrund="#e4f3f4"),
   absatz("Meine Arbeit daran ist: durchlesen, aussuchen, freigeben. Das dauert keine "
          "Stunde."),
   h2("Und jetzt der Teil, den sonst niemand erz&auml;hlt"),
   absatz("Bei mir geht nichts ungepr&uuml;ft raus. Das ist eine bewusste Entscheidung, "
          "weil mein Konto an meinem Partnerunternehmen h&auml;ngt und ein unbedachter "
          "Satz mich mehr kostet, als eine automatisierte Woche mir spart."),
   absatz("Trotzdem ist mir genau das passiert: Ich hatte ein Reel von Hand &uuml;ber "
          "die App gepostet, im Cockpit stand es aber weiter auf <em>wartet</em> "
          "&mdash; abends w&auml;re es ein zweites Mal eingeplant worden. Den Fehler "
          "sieht man nicht, bevor er passiert."),
   merken("Warum ich dir das erz&auml;hle",
          "Genau dieser Fehler steht als eigene Lektion im Kurs.",
          "Sch&ouml;n sieht er nicht aus. Er steht drin, weil du ihn sonst selbst "
          "herausfindest &mdash; und zwar in dem Moment, in dem er schon passiert ist."),
   beweis_platz(),
   knopf("Alles zum Kurs", KURS),
   gruss("Bis bald,"),
   ps("P.S. Die Anmeldung ist noch bis " + SCHLUSS + " offen."),
 ]},

# ------------------------------------------------------------------ Di 21.10.
{
 "datei": "liste-06-fuer-wen-nicht.html", "tag": "Di 21.10.", "warten": "2 Tage",
 "marke": "mumlifebalance",
 "betreff": "Für wen der Kurs nichts ist",
 "betreff2": "Lies das, bevor du buchst",
 "wann": "Dienstag, 21. Oktober, 08:00",
 "preheader": "Drei Gründe, es sein zu lassen — und einer, es zu tun",
 "h1": "Für wen der Kurs nichts ist",
 "unterzeile": "Mir ist lieber, du steigst nicht ein, als dass er bei dir liegen bleibt.",
 "notiz": """
Disqualifikations-Mail (Hormozi: wer aussortiert, erhöht den Wert für die
Richtigen). Patricias eigene Haltung steht in brand-voice.md: sie will keine
Frauen, die Tipps sammeln und nichts umsetzen, und niemanden, der auf ein
Wunder hofft.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("am Donnerstag schliesst die Anmeldung. Bevor du dich entscheidest, "
          "schreibe ich dir lieber auf, wann du es <strong>sein lassen</strong> "
          "solltest."),
   liste("Lass es, wenn", [
       "du <strong>Kurse sammelst und nichts umsetzt</strong>. Dieser hier verlangt, "
       "dass du zwischendurch etwas anklickst. Sonst hast du am 30. November zehn "
       "Module gesehen und nichts gebaut.",
       "du dir davon erhoffst, dass <strong>dein Business von allein l&auml;uft</strong>. "
       "Es nimmt dir Arbeit ab, die sich wiederholt. Es nimmt dir nicht ab, zu "
       "entscheiden, was du eigentlich willst.",
       "du <strong>im November keine zwei Stunden pro Woche</strong> hast. Dann warte "
       "auf den n&auml;chsten Durchgang, das ist ehrlicher zu dir selbst."],
      hintergrund="#faf2ea", rand=ORANGE, farbe="#b56a24"),
   h2("Und jetzt die andere Seite"),
   absatz("Steig ein, wenn du jede Woche dieselben Arbeiten machst und merkst, dass "
          "sie dich auffressen. Content, Mails, Planung, Antworten &mdash; genau das "
          "ist der Teil, den du abgeben kannst."),
   absatz("Du f&auml;ngst im Chat an, den du schon kennst. Die erste Stufe ist nach "
          "einem Abend erledigt, und schon die tr&auml;gt."),
   knopf("Alles zum Kurs", KURS),
   gruss("Bis bald,"),
   ps("P.S. Noch bis " + SCHLUSS + ", danach schliesst die Anmeldung."),
 ]},

# ------------------------------------------------- Do 23.10., morgens
{
 "datei": "liste-07-letzter-tag.html", "tag": "Do 23.10. · 08:00", "warten": "2 Tage",
 "marke": "mumlifebalance",
 "betreff": "Heute Abend schliesst die Anmeldung",
 "betreff2": "Letzter Tag für Easy KI",
 "wann": "Donnerstag, 23. Oktober, 08:00",
 "preheader": "Alles auf einen Blick, damit du in zwei Minuten entscheiden kannst",
 "h1": "Heute ist der letzte Tag",
 "unterzeile": "Um 21 Uhr schliesst die Anmeldung, und ich begleite die Gruppe ab dem 1. November.",
 "notiz": """
Zusammenfassungs-Mail. Alles, was sie zum Entscheiden braucht, auf einem Blick.
Kein neues Argument — wer bis hier gelesen hat, kennt sie alle.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("heute Abend um 21 Uhr schliesst die Anmeldung f&uuml;r <strong>Easy KI "
          "f&uuml;r Networkerinnen</strong>. Damit du nicht nochmal suchen musst, hier "
          "alles auf einmal:"),
   liste("Was du bekommst", [
       "<strong>Zehn Module</strong>, ab 1. November Woche f&uuml;r Woche, komplett am "
       "30. November",
       "<strong>Drei Stufen</strong> &mdash; Chat, Zwischenstufe, eigener Arbeitsplatz. "
       "Auf jeder ein Ergebnis, das du beh&auml;ltst",
       "<strong>Dein Arbeitsplatz</strong> mit deinem Wissen, deiner Sprache, deiner "
       "Kundin &mdash; den jeder Auftrag liest",
       "<strong>Dein erster eigener Skill</strong> f&uuml;r eine Arbeit, die jede "
       "Woche wiederkommt",
       "<strong>Ein Bot</strong>, der morgens von selbst schreibt, auch wenn dein "
       "Laptop zu ist",
       "<strong>Zwei Live-Calls</strong> w&auml;hrend des Kurses"]),
   merken("Preis", PREIS_SPAET + " &mdash; oder in Raten",
          "Die Anmeldung schliesst heute um 21 Uhr. Danach gibt es den Kurs erst wieder "
          "im n&auml;chsten Durchgang."),
   knopf("Jetzt einsteigen", KURS),
   absatz("Wenn du Fragen hast, antworte einfach auf diese Mail. Ich lese sie selbst, "
          "und heute bin ich den ganzen Tag erreichbar."),
   gruss("Bis bald,"),
   ps("P.S. Falls du gleich alles willst: In der <a href=\"" + ACADEMY + "\" "
      "style=\"color:" + PETROL + ";\">Mum Business Academy</a> sind alle vier Kurse "
      "drin, der KI-Kurs ab dem 1. November inklusive, dazu ein Jahr Begleitung und "
      "zweimal im Monat ein Call."),
 ]},

# ------------------------------------------------- Do 23.10., abends
{
 "datei": "liste-08-letzte-stunden.html", "tag": "Do 23.10. · 19:00", "warten": "11 Stunden",
 "marke": "mumlifebalance",
 "betreff": "Noch zwei Stunden",
 "betreff2": "Dann schliesst die Anmeldung",
 "wann": "Donnerstag, 23. Oktober, 19:00",
 "preheader": "Kurz und ehrlich: das ist die letzte Mail dazu",
 "h1": "Noch zwei Stunden",
 "unterzeile": "Das ist die letzte Mail zum Kurs.",
 "notiz": """
Die kürzeste Mail der Strecke. Ein Gedanke, ein Knopf.
🚨 Julias Muster: am letzten Tag zwei Mails, morgens und abends. Diese ist
   bewusst knapp — wer jetzt noch liest, braucht kein Argument mehr, sondern
   einen Link.
""",
 "bloecke": [
   absatz("Hallo %FIRSTNAME%,"),
   absatz("um 21 Uhr schliesst die Anmeldung f&uuml;r <strong>Easy KI f&uuml;r "
          "Networkerinnen</strong>. Das ist die letzte Mail dazu, danach habe ich "
          "Ruhe und du auch."),
   absatz("Falls du die ganze Woche &uuml;berlegt hast: Der Kurs f&auml;ngt bei dem "
          "Chat an, den du schon kennst. Du musst heute nichts k&ouml;nnen, du musst "
          "nur anfangen wollen."),
   knopf("Jetzt noch einsteigen", KURS),
   gruss("Bis bald,"),
   ps("P.S. Wenn es dieses Mal nicht passt, ist das v&ouml;llig in Ordnung. Dann "
      "sehen wir uns beim n&auml;chsten Durchgang."),
 ]},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--liste", action="store_true", help="nur die Strecke zeigen")
    args = ap.parse_args()

    print("DIE STRECKE AN DIE ÜBRIGE LISTE — KI-Kurs, Oktober 2026\n")
    print("  %-3s %-16s %-14s %s" % ("#", "wann", "warten", "Betreff"))
    print("  " + "-" * 94)
    for i, m in enumerate(MAILS, 1):
        print("  %-3d %-16s %-14s %s" % (i, m["tag"], m["warten"], m["betreff"]))
    if args.liste:
        return

    ZIEL.mkdir(parents=True, exist_ok=True)
    print()
    fehler = 0
    for m in MAILS:
        h = bauen(m)
        (ZIEL / m["datei"]).write_text(h, encoding="utf-8")
        # 🚨 Der Umlaut-Waechter aus dem Startklar-Skript laeuft mit: er prueft
        #    den SICHTBAREN Text gegen bekannte Umschreibungen (haettest, waere…).
        #    Am 18.09. stand „so haettest du es geschrieben" dreimal in einer
        #    fertigen Mail — gefunden hat es Patricia, nicht die Selbstpruefung.
        try:
            _sk.umlaute_pruefen(m["datei"], h)
        except SystemExit:
            fehler += 1
        print("  ✓ %-34s %6d Zeichen" % (m["datei"], len(h)))

    # Zusaetzliche Pruefung: Blackliste auf dem sichtbaren Text
    print()
    for m in MAILS:
        sicht = _sk.sichtbarer_text((ZIEL / m["datei"]).read_text(encoding="utf-8"))
        klar = html.unescape(sicht)
        schlecht = []
        for muster, name in [
                (r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "Nicht-X-sondern-Y"),
                (r"[Ss]tell(e)? dir[^.!?]{0,40}vor", "Stell dir vor"),
                (r"\bnie wieder\b", "nie wieder"),
                (r"ß", "deutsches Eszett")]:
            if re.search(muster, klar):
                schlecht.append(name)
        if schlecht:
            print("  🚨 %-34s %s" % (m["datei"], " | ".join(schlecht)))
            fehler += 1
    if not fehler:
        print("  Sprachprüfung über alle Mails: sauber ✓")

    print("\n%d Mails → %s" % (len(MAILS), ZIEL.relative_to(ROOT)))
    if fehler:
        print("🚨 %d Mail(s) mit Befund — vor dem Versand ansehen." % fehler)
        sys.exit(1)


if __name__ == "__main__":
    main()
