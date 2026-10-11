# -*- coding: utf-8 -*-
"""Traegt die Befunde der Methodik-Durchsicht vom 08.10.2026 in die
Funnel-Checkliste ein.

Quelle der Befunde: outputs/marktrecherche/2026-10-08-julia-funnel-durchsicht.md
(117 Punkte aus den Transkripten und Vorlagen-PDFs der gekauften Kursunterlagen).

🚨 Aus den Kursunterlagen kommt nur die MECHANIK, nie der Wortlaut und nie ein
   fremder Name — dieselbe Grenze wie in wissen-bauen.py. Die Seite ist teilbar.

🚨 EIN PUNKT WAR FALSCH und wird hier korrigiert: ich hatte geschrieben, das
   Upsell sei "teurer als das Gekaufte". In den Unterlagen steht an zwei Stellen
   das Gegenteil: das Upsell ist teurer als der Bump, aber immer noch
   guenstiger als das Hauptprodukt. Befund 46.

Wiederholbar: jede Ersetzung prueft vorher, dass sie genau einmal passt, und
bricht sonst ab. Danach einmal funnel-checkliste-bauen.py laufen lassen.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "scripts" / "cockpit" / "funnel-checkliste-bauen.py"


def ersetze(t, alt, neu, name):
    if alt not in t:
        sys.exit("🚨 Ankertext nicht gefunden (%s) — schon gepatcht?" % name)
    if t.count(alt) != 1:
        sys.exit("🚨 Ankertext %sx gefunden (%s), erwartet 1x" % (t.count(alt), name))
    return t.replace(alt, neu)


# ===========================================================================
#  1 · Die falsche Angabe beim Upsell korrigieren (Befund 46)
# ===========================================================================
ALT_UPSELL = '''   ("Ein Upsell kommt direkt nach dem Kauf", "methodik",
    "Eigene Seite, teurer als das Gekaufte. Das ist der Platz für das grosse "
    "Programm, stark rabattiert. Aufbau: Kauf feiern, warum das Gekaufte allein "
    "nicht reicht, ein Satz Pitch, Preisvergleich, Knopf."),'''

NEU_UPSELL = '''   ("Ein Upsell kommt direkt nach dem Kauf", "methodik",
    "Eigene Seite nach der Kaufbestätigung. Die Reihenfolge der Preise: der Bump "
    "ist günstiger als das Hauptprodukt, das Upsell teurer als der Bump — aber "
    "<b>immer noch günstiger als das Hauptprodukt</b>, und in sich stark "
    "rabattiert (333 → 49). Aufbau: Kauf feiern, warum das Gekaufte allein nicht "
    "reicht, ein Satz Pitch, Preisvergleich, Knopf. 🚨 Hier stand bis zum "
    "08.10.2026 „teurer als das Gekaufte“ — das war falsch."),
   ("Jedes Zusatzangebot trägt seinen eigenen Streichpreis", "methodik",
    "Bump, Upsell und Downsell wirken nur, wenn daneben steht, was sie sonst "
    "kosten: „nur 37 statt 99“. Ohne Streichpreis ist es kein Angebot, sondern "
    "nur ein weiterer Posten auf der Rechnung."),
   ("Der Bump ergänzt das Hauptprodukt, das Upsell darf etwas Neues sein", "methodik",
    "Ein Bump ist die Vorlage, die Checkliste, das Workbook zum Gekauften — nie "
    "ein fremdes Thema. Das Upsell dagegen darf ein anderer Kurs sein, eine "
    "Begleitung oder die Mitgliedschaft."),
   ("Mehrere Bumps plus ein Bundle aus allen", "methodik",
    "Drei oder vier Bumps nebeneinander, und darunter alle zusammen zu einem "
    "Preis, der unter zwei Einzelpreisen liegt. Der Gedanke beim Lesen ist "
    "„das will ich, das auch, und zusammen ist es billiger als zwei“ — damit "
    "nimmt rund jede Zweite etwas mit."),
   ("Bump-Preis im Fenster 17 bis 37", "methodik",
    "Darunter wirkt es wertlos, darüber wird überlegt. Ein Bump soll ein "
    "Häkchen sein, keine zweite Kaufentscheidung."),
   ("Upsell vor dem Downsell angelegt", "methodik",
    "Die Kasse zeigt den Downsell nur, wenn das Upsell abgelehnt wurde — ohne "
    "angelegtes Upsell gibt es den Downsell technisch nicht."),
   ("Je Upsell und Downsell ein eigener Tag im Mailprogramm", "methodik",
    "Sonst bekommt die Kundin weiter Werbung für etwas, das sie gerade gekauft "
    "hat. Das ist der peinlichste Fehler im ganzen Funnel und der leiseste."),
   ("Die Auslieferungstexte der Kasse sind übersetzt", "methodik",
    "„You purchased …“ und „Download link“ stehen sonst auf Englisch mitten in "
    "einer deutschen Strecke. Einmal eine Upsell-Seite bauen und danach immer "
    "kopieren, statt sie je Produkt neu zu gestalten."),
   ("Der Kauf löst die Mail automatisch aus", "methodik",
    "Kasse und Mailprogramm sind verbunden, und die erste Mail geht ohne "
    "Handgriff raus. Eine Auslieferung, die jemand von Hand verschickt, "
    "verschickt irgendwann niemand."),
   ("Bump-Text nach der passenden Bauart", "methodik",
    "Drei Fälle, drei Aufbauten. <b>Zwei Kurse kombiniert:</b> erst das "
    "Hauptprodukt in zwei Sätzen, dann warum beide zusammen Sinn machen, dann "
    "die wichtigsten Punkte des Bumps, zuletzt die Ersparnis. <b>1:1 als Bump:</b> "
    "warum schon eine Stunde wertvoll ist, was dich auszeichnet, "
    "Preisunterschied — und ein Blick auf die eigene Kapazität. "
    "<b>Mini-Programm:</b> eine Liste der Vorteile reicht, bei 15 bis 37 gibt es "
    "nichts zu erklären."),'''

# ===========================================================================
#  2 · Neue Punkte in bestehende Phasen
# ===========================================================================
ANKER_PLAN = '''   ("Der Funnel steht in <code>active-funnels.json</code>", "erfahrung",
    "Was dort fehlt, kennen die Content-Skills nicht. Dann schreibt niemand "
    "Beiträge darauf."),
  ]),'''

NEU_PLAN = '''   ("Der Funnel steht in <code>active-funnels.json</code>", "erfahrung",
    "Was dort fehlt, kennen die Content-Skills nicht. Dann schreibt niemand "
    "Beiträge darauf."),
   ("Die Produkt-Tabelle ist ausgefüllt", "methodik",
    "Elf Spalten je Produkt, und sie sind die Vorarbeit für Seite, Mails und "
    "Storys: Name · Pitch · deine Story dazu (warum ist es wichtig) · Inhalte · "
    "wo steht sie heute · wo will sie hin · die Verwandlung · was bringt es ihr · "
    "<b>was passiert, wenn sie bleibt, wo sie ist</b> · wie sieht es aus, wenn "
    "es läuft · Glaubenssätze und Blockaden. Wer sie ausfüllt, muss später "
    "nichts mehr erfinden."),
   ("Die Ist-Situation über vier Fragen gefunden", "methodik",
    "Was hält sie nachts wach · welcher Gedanke kommt morgens zuerst · wovor hat "
    "sie Angst · wovor schiebt sie auf, und was kommt dabei heraus. Antworten "
    "darauf sind die Sätze für Seite und Hook — Vermutungen sind es nicht."),
   ("Der Preis nach den eigenen Stufen gesetzt", "methodik",
    "Der Preis gehört zur Positionierung: ein 7er-Produkt zieht andere Leute an "
    "als ein 333er. Deshalb mehrere Stufen nebeneinander und das 1:1 immer als "
    "teuerstes Angebot — es hängt an deiner Zeit und lässt sich nicht "
    "vervielfachen."),
   ("Preis endet auf 7, 9 oder ist eine Schnapszahl", "methodik",
    "49 statt 50, 111 statt 100, 37 statt 35. Und zweistellig schlägt "
    "dreistellig: eher 99 und später erhöhen als von Anfang an 111."),
   ("Die Prüffrage zum Preis beantwortet", "methodik",
    "„Ist das Ergebnis dieses Produkts für sie mindestens so viel wert?“ Wenn "
    "ja, ist der Preis gerechtfertigt. Bezahlt wird das Ergebnis, nie die Länge "
    "— ein Video von 20 Minuten darf dasselbe kosten wie fünf Stunden."),
   ("Der Return on Invest steht irgendwo als Satz", "methodik",
    "Was holt sie sich zurück, in Geld, Zeit oder Nerven. Das ist der stärkste "
    "Einwand-Löser und fehlt fast immer."),
   ("Ausgerechnet, wie viele Verkäufe das Ziel braucht", "methodik",
    "(Monatsziel minus Bestand) geteilt durch den Preis. Dann die ehrliche "
    "Gegenfrage: geht diese Zahl mit der Reichweite, die du heute hast? Bei "
    "einem 37er-Produkt und 5000 im Monat sind es 122 Verkäufe — dann fehlt "
    "nicht der Funnel, sondern ein zweites, teureres Angebot."),
   ("Erste Kundenstimmen beschafft, bevor die Seite steht", "methodik",
    "Zwei bis drei Leuten das Produkt gratis geben gegen ehrliches Feedback. "
    "Lieber klein anfangen und zehn echte Stimmen sammeln, als mit einem hohen "
    "Preis und null Belegen zu starten."),
  ]),'''

ANKER_AC = '''  ]),

 ("Die Seiten", "seiten",'''

NEU_AC = '''   ("ManyChat reagiert auf alle drei Wege", "methodik",
    "Kommentar unter Beitrag oder Reel · <b>Antwort auf eine Story</b> · "
    "<b>Direktnachricht</b>. Wer nur den Kommentar auslöst, verliert die "
    "beiden Wege, auf denen die Interessiertesten schreiben."),
   ("Ein Zähltag unterscheidet das erste vom zweiten Mal", "methodik",
    "Beim ersten Kommentar den Tag setzen, beim zweiten einen zusätzlichen "
    "„2x“-Tag. Wer zweimal kommentiert, ist deutlich wärmer und bekommt die "
    "längere Nachricht — dieselbe Antwort an beide verschenkt genau die Leute, "
    "die schon fast kaufen."),
   ("In der Nachricht stehen zwei Links, nicht einer", "methodik",
    "Das Freebie — und daneben „so arbeitest du mit mir“. Gemessen klicken rund "
    "60 Prozent auf das erste und 30 Prozent auf das zweite. Nie mehr als zwei, "
    "sonst klickt niemand."),
   ("Je Link ein eigener Klick-Tag", "methodik",
    "Der Klick ist das stärkste Signal im ganzen Funnel und darf nicht "
    "verfallen: er gehört als Tag festgehalten und löst die nächste Strecke aus."),
   ("Nachgefasst, wenn 23 Stunden nichts passiert", "methodik",
    "Das Fenster für eine Nachricht schliesst nach 24 Stunden. Wer nicht "
    "geklickt hat, bekommt vorher eine zweite Zeile — danach geht es nicht mehr."),
   ("Bei einer Umfrage per Nachricht nur positive Antworten", "methodik",
    "„Ja“ und „ja, unbedingt“ — kein „nein“. Auf ein Nein gibt es keine "
    "sinnvolle Antwort, und wer nicht will, schreibt ohnehin nicht."),
  ]),

 ("Die Seiten", "seiten",'''

ANKER_SEITEN = '''   ("Jede Adresse einmal wirklich aufgerufen", "erfahrung",'''

NEU_SEITEN = '''   ("Entschieden: eigene Verkaufsseite oder nur die Kasse", "methodik",
    "Es geht auch ohne Landingpage — die Kasse allein trägt den Verkauf, auch "
    "für Anzeigen, und spart jede Pflege an zwei Stellen. Wenn es eine eigene "
    "Seite gibt, muss klar sein, warum."),
   ("Der Produktname steht genau einmal auf der Seite", "methodik",
    "Im Bild, sonst nirgends. Dreimal derselbe Name oben heisst: man weiss, "
    "wie es heisst, und immer noch nicht, worum es geht. Die Überschrift nennt "
    "das <b>Ziel</b>, nicht den Kurs."),
   ("Der Kaufknopf ist ohne Scrollen zu sehen", "methodik",
    "Oben: Ziel-Überschrift, Bild, Knopf. Wer erst eine Minute scrollen muss, "
    "entscheidet sich vorher — meistens dagegen."),
   ("Die sechs Blöcke stehen in dieser Reihenfolge", "methodik",
    "Name und Pitch mit Knopf → <b>drei</b> Vorteile → Kundenstimme → "
    "Ist-Situation → Storytelling (wie es dir damals ging) → Soll-Situation mit "
    "Knopf. Ausser im Storytelling gilt: wenig Text, keine Blöcke."),
   ("Jeder Abschnitt hat seine eigene Hintergrundfarbe", "methodik",
    "Eine Seite in einem Ton wirkt wie ein Dokument. Der Farbwechsel je "
    "Abschnitt ist der Grund, weiterzuscrollen."),
   ("Der Block „Das brauchst du nicht“ steht drin", "methodik",
    "Drei Dinge, die es <b>nicht</b> braucht: keine Vorkenntnisse, keine Technik, "
    "kein Budget. Das räumt die Glaubenssätze weg, bevor sie auftauchen."),
   ("Ein FAQ beantwortet die Einwände", "methodik",
    "Die immer gleichen vier: wie lange habe ich Zugriff · was, wenn ich keine "
    "Zeit habe · kann ich in Raten zahlen · garantierst du Erfolg. Die letzte "
    "wird ehrlich beantwortet: nein, es hängt an der Umsetzung."),
   ("Bei einer langen Kundenstimme ist ein Satz hervorgehoben", "methodik",
    "Sonst liest sie niemand, und der Beleg verpufft."),
   ("Jemand ohne Vorwissen hat die Seite gelesen", "methodik",
    "Und konnte in einem Satz sagen, worum es geht. Bei einem Fragezeichen "
    "werden Wörter gestrichen, nicht ergänzt."),
   ("Füllwörter gestrichen", "methodik",
    "Jedes Wort raus, ohne das der Satz steht. Danach ist die Seite kürzer und "
    "klarer — das ist derselbe Handgriff wie bei jeder Caption."),
   ("Jede Adresse einmal wirklich aufgerufen", "erfahrung",'''

ANKER_MAILS = '''   ("Keine einzige Mail ohne Link", "methodik",'''

NEU_MAILS = '''   ("Die Betreffzeile ist ein Hook", "methodik",
    "Keine Ankündigung („Newsletter Oktober“), sondern derselbe Anspruch wie "
    "bei einer ersten Reelzeile. Und der Einstieg geht direkt in die Geschichte "
    "— keine Begrüssung, keine Einleitung."),
   ("Genau ein Aufruf je Mail", "methodik",
    "Der am häufigsten vergessene Punkt. Zwei Aufrufe in einer Mail heissen "
    "null Aufrufe."),
   ("Der Abstand ist nicht täglich und nicht zu lang", "methodik",
    "Zwei bis drei Tage in einer Strecke. Täglich nervt, wochenlang Pause und "
    "sie weiss nicht mehr, wer schreibt."),
   ("Der Link steht weit oben", "methodik",
    "Nicht erst im Schlussabsatz. Wer überzeugt ist, soll nicht suchen müssen."),
   ("Die Willkommensmail zeigt die ganze Welt", "methodik",
    "Nach einem 0€-Produkt: drei Angebote, je mit einem Satz Pitch und „für "
    "mehr …“. Der 0€-Funnel macht keinen Umsatz, er baut Vertrauen — und das "
    "erste, was sie danach braucht, ist ein Überblick, wohin es weitergeht."),
   ("Der Baustein „… und das ohne …“ ist drin", "methodik",
    "Drei Dinge, die es bringt, und drei, die es nicht braucht. Löst Einwand und "
    "Nutzen in einem Atemzug."),
   ("Der Einwand gegen das Format vorweggenommen", "methodik",
    "„Wenn du beim Wort Mini denkst, da lerne ich eh nichts“ — und direkt eine "
    "Kundenstimme dagegen. Wer den Satz selbst ausspricht, nimmt ihm die Kraft."),
   ("Irgendwo in der Strecke steht ein 48-Stunden-Angebot", "methodik",
    "Ein echter Rabatt auf einen kleinen Kurs, mit kurzer Frist. Das ist die "
    "Stelle, an der ein 0€-Funnel zum ersten Mal Geld bringt."),
   ("Für die, die nicht gekauft haben, läuft eine eigene Strecke", "methodik",
    "Nicht abbrechen, wenn der Pitch nicht gezogen hat: eine zweite Runde mit "
    "mehr Mehrwert und einem deutlicheren Angebot. Wer kauft, steigt über das "
    "Ziel von selbst aus."),
   ("Der Kurskäuferin wird das 0€-Webinar angeboten", "methodik",
    "Drei Mails nach dem Kauf eines kleinen Produkts: Einladung ins Webinar. So "
    "hängt der kleine Funnel am grossen, ohne dass jemand etwas tun muss."),
   ("Keine einzige Mail ohne Link", "methodik",'''

ANKER_ZULAUF = '''   ("Telegram-Gruppe verlinkt, falls es eine gibt", "erfahrung",'''

NEU_ZULAUF = '''   ("Selbst Nachrichten geschrieben, nicht nur gewartet", "methodik",
    "Interaktion kommt nicht von allein. Neue Followerinnen begrüssen, auf "
    "fremde Profile gehen, in den Austausch kommen — und dort <b>nicht</b> "
    "verkaufen. Höchstens einmal „hast du das schon gesehen?“ mit einem 0€- oder "
    "Minikurs-Link."),
   ("Der Preis steht in der Story", "methodik",
    "Ein Teil der Leute entscheidet über Zahlen und springt ab, wenn der Preis "
    "fehlt. „Schreib mir für den Preis“ kostet mehr Verkäufe, als es Gespräche "
    "bringt."),
   ("90 Prozent geht kostenlos raus", "methodik",
    "Der Mehrwert ist das Pfand: wer viel bekommt, will etwas zurückgeben. "
    "Deshalb ist ein zu dünnes Freebie teurer als keines."),
   ("Telegram-Gruppe verlinkt, falls es eine gibt", "erfahrung",'''

ANKER_MESSEN = '''   ("Entschieden: weiterlaufen lassen, nachschärfen oder abstellen", "erfahrung",'''

NEU_MESSEN = '''   ("Kundenstimmen aktiv eingeholt", "methodik",
    "Jede anschreiben, die durchgearbeitet hat — auch die, die nie etwas gesagt "
    "haben. Mit einer Gegenleistung: ein Minikurs gratis für eine Stimme. Von "
    "zehn antworten zwei, und das reicht."),
   ("Ein Video-Testimonial gefragt", "methodik",
    "Text ist gut, ein Video ist unschlagbar — man sieht, dass ein echter "
    "Mensch dahintersteht. Bei einem heiklen Thema reicht der Vorname."),
   ("Die Stimmen liegen an einer Stelle", "methodik",
    "Ein Ordner, aus dem Seite, Mails und Storys bedient werden. Sonst sucht "
    "man bei jeder neuen Seite in alten Nachrichten."),
   ("Die Stimmen sind freigegeben", "erfahrung",
    "Bild und voller Name nur mit ausdrücklicher Erlaubnis — fragen, bevor es "
    "auf eine Seite geht. Ohne Freigabe anonym und als Zusammenfassung, nie "
    "als Zitat."),
   ("Den Bestandskundinnen ein eigenes Angebot geschickt", "methodik",
    "Der schnellste Umsatz überhaupt: eine eigene Mail oder Nachricht an alle, "
    "die schon einmal gekauft haben, mit einem Dank-Vorteil. Neue zu gewinnen "
    "kostet ein Vielfaches. 🚨 Das wird in jedem Launch vergessen."),
   ("Entschieden: weiterlaufen lassen, nachschärfen oder abstellen", "erfahrung",'''

# ===========================================================================
#  3 · Zwei neue Phasen vor "Nach dem Start"
# ===========================================================================
ANKER_NEUE_PHASEN = ''' ("Nach dem Start", "messen",'''

NEU_PHASEN = ''' ("Der Launch", "launch",
  "Ein Funnel läuft von selbst. Ein Launch ist der Start davor — und er hat "
  "eine feste Form.", [
   ("Entschieden: launchen oder droppen", "methodik",
    "Ab rund 99 wird gelauncht, darunter gedroppt. Ein kleines Produkt wirft "
    "man auf den Markt und spricht drei bis fünf Tage darüber; eine Begleitung "
    "oder ein 1:1 wird gar nicht gelauncht, sondern immer wieder einmal "
    "erwähnt, bis die Plätze voll sind. Wochenlang über 37 zu reden bringt den "
    "Umsatz nicht und langweilt alle."),
   ("Die fünf Phasen stehen im Kalender", "methodik",
    "Vorbereitung · Aufwärmen · Secret Offer · Verkauf · Nachbereitung. Jede "
    "mit Datum, rückwärts vom Verkaufsstart gerechnet: Seite, Kasse und "
    "Beiträge entstehen im Monat davor, nicht in der Woche davor."),
   ("Die Aufwärmphase dauert rund eine Woche", "methodik",
    "Nicht drei — sonst redet man sechs Wochen über dasselbe Produkt und "
    "niemand hört mehr hin. Aber auch nicht null: ohne Aufwärmen ist es kein "
    "Launch, sondern ein Produkt, das plötzlich dasteht. Je weniger Kundinnen "
    "du hast, desto wichtiger ist diese Woche."),
   ("In der Aufwärmphase wird nicht gesagt, was kommt", "methodik",
    "Nur dass etwas kommt. Making-of zeigen, bewusst unscharf über Unterlagen "
    "schwenken, und die Community mitentscheiden lassen: Titel, Gestaltung, "
    "welche Inhalte hinein sollen. Wer mitgebaut hat, kauft lieber."),
   ("Das Secret Offer sagt nicht, um was es geht", "methodik",
    "Das ist der ganze Trick und wird fast immer falsch gebaut: es ist <b>keine "
    "Preisstufe</b>, sondern ein verdecktes Angebot. „Es gibt etwas, tipp auf "
    "den Sticker“ — und wer tippt, bekommt den Link per Nachricht. In der Mail: "
    "wer antwortet, bekommt ihn. Belohnt wird das Vertrauen, nicht die "
    "Schnelligkeit. Dauer: zwei Tage."),
   ("Die Preisstufen haben die richtigen Abstände", "methodik",
    "Vom Secret Offer zum Frühbucher ein <b>kleiner</b> Schritt, vom Frühbucher "
    "zum regulären Preis ein <b>grosser</b>. Wer die Abstände vertauscht, "
    "bestraft die Treuen und belohnt die Zögerlichen."),
   ("In der Bio steht während des Launches nur ein Link", "methodik",
    "Der zum Produkt. Keine Linkliste, keine Webseite. Wer zwischen fünf "
    "Möglichkeiten wählen muss, wählt keine."),
   ("Ein Highlight ist farbig markiert und vollgepackt", "methodik",
    "Zwischen allen anderen muss man sehen: hier läuft gerade etwas. Darin die "
    "ganze Sequenz — Inhalte, für wen es ist, Stimmen, Link."),
   ("Jeden Tag wird geteilt, wer schon dabei ist", "methodik",
    "Echte Vornamen, nie erfundene. Eine Person ist auch eine Person — dann "
    "wird die eine gefeiert."),
   ("Ein Beitrag zum Launch ist angepinnt", "methodik",
    "Für die Verkaufswochen oben im Profil. Dazu ein Inhalt, der zum Thema "
    "gehört, nicht nur eine Ankündigung."),
   ("Alles zeigt in dieselbe Richtung", "methodik",
    "Story, Feed, Mail, Bio — ein Produkt. Ein zweites darf höchstens abends "
    "als zweite Story auftauchen. Zwei Angebote gleichzeitig heissen für die "
    "Leserin: keins ist wichtig."),
   ("Die Verknappung stimmt wirklich", "methodik",
    "Plätze, Fristen und Zahlen nur, wenn sie zutreffen. Und die Preisspanne "
    "bleibt im Rahmen: ein Sprung, der Panik macht, verkauft einmal und "
    "verbrennt das Vertrauen. Nie zu einer Finanzierung raten."),
   ("Rabattiert wird über die Leistung, nicht über den Preis", "methodik",
    "Statt Prozent auf das Bestehende: dasselbe Angebot kleiner schneiden — "
    "vier Wochen statt zwölf, nur Begleitung per Nachricht, fünf Plätze. Der "
    "Stundenlohn bleibt, das Angebot ist neu, und es lässt sich beliebig oft "
    "wiederholen."),
   ("Bei Flaute die sechs Fragen durchgegangen", "methodik",
    "Ist das Angebot in einem Satz klar · trägt die Kaufseite · war die eigene "
    "Energie da · war es emotional oder nur eine Inhaltsliste · sind alle sechs "
    "Käufertypen vorgekommen · wurde genug aufgewärmt. Das Frühwarnzeichen "
    "steht schon vorher fest: kommen in der Aufwärmphase Fragen und „das kenne "
    "ich“-Antworten, wird die Verkaufsphase laufen. Kommt dort nichts, ändert "
    "sich das durch mehr Verkaufsstorys nicht."),
   ("Keine Lücke bis zum nächsten Launch", "methodik",
    "Nach der Nachbereitung steht fest, was als Nächstes beworben wird. Wer "
    "nichts verkauft, verkauft nichts — und eine leere Woche kostet den ganzen "
    "aufgebauten Schwung."),
  ]),

 ("Das Webinar", "webinar",
  "Nur ausfüllen, wenn der Funnel über eine Masterclass läuft.", [
   ("Das Thema ist breiter als das Produkt", "methodik",
    "Das beworbene Produkt ist die Lösung; das Webinar ist das Mini-Thema "
    "davor. Lieber allgemeiner als zu spezifisch — ein Webinar soll viele "
    "erreichen und Lust auf mehr machen, nicht alles abschliessen."),
   ("Der Titel folgt einer der drei Formeln", "methodik",
    "„Wie du X erreichst, ohne Y“ · „In drei Schritten zu X“ · „Mein "
    "<i>Name</i>-System: mit X zu Y“. Spezifisch, mit Zahlen, ohne Leerfloskeln."),
   ("Die neun Blöcke stehen im Skript", "methodik",
    "Willkommen · warum das Thema wichtig ist · eine Frage an die Zuschauenden "
    "· warum ich · Inhalt · Zusammenfassung · Kundenstimmen · Pitch · Fragen. "
    "Die Reihenfolge darf sich ändern, fehlen darf keiner."),
   ("Die Agenda dauert höchstens zwanzig Sekunden", "methodik",
    "Sie dient nur der Orientierung. Wer lange erklärt, was kommt, verliert "
    "die, die etwas lernen wollten."),
   ("Frei gesprochen, mit Stichpunkten", "methodik",
    "Nie ablesen — man hört es sofort. Kapitelüberschriften reichen, das "
    "Wissen ist ohnehin da. Und: die Energie entscheidet mehr als die Folien."),
   ("Zwischendurch immer wieder auf den Pitch gezeigt", "methodik",
    "„Das ist nur die Spitze, dazu gibt es viel mehr.“ Je öfter das vorkommt, "
    "desto selbstverständlicher ist das Angebot am Ende."),
   ("Die Zusammenfassung sagt, wie viel schon gegeben wurde", "methodik",
    "„So viel Inhalt passt gar nicht in ein Webinar“ — das ist die Brücke zum "
    "Pitch und zugleich der Beweis, dass es sich gelohnt hat zuzusehen."),
   ("Drei bis fünf Kundenstimmen, mit Bild und Namen", "methodik",
    "Mehr wird langatmig, weniger wirkt dünn. Vorher um Erlaubnis fragen."),
   ("Der Preisanker steht im Pitch", "methodik",
    "Ein Bonus mit genanntem Gegenwert, nur bei Buchung jetzt. Dazu der "
    "Vergleichspreis — ohne Anker ist der Preis nur eine Zahl."),
   ("Die drei Standardfragen am Schluss beantwortet", "methodik",
    "Kann ich in Raten zahlen · wie lange habe ich Zugriff · erreiche ich dich "
    "bei Fragen. Sie kommen immer, und sie zu beantworten kostet zwei Minuten."),
   ("Die Erinnerungen stehen", "methodik",
    "18 Stunden, 12 Stunden, 1 Stunde und 15 Minuten vorher. Dazu die "
    "Spät-Anmeldung: wer fünf Minuten vor dem Start kommt, soll noch hinein."),
   ("Nach dem Webinar läuft eine Strecke mit Frist", "methodik",
    "Aufzeichnung, dann drei bis vier Mails. 🚨 Eine Frist in der Mail ist "
    "keine Frist in der Kasse — wenn der Preis nach Ablauf gelten soll, muss "
    "die Kasse ihn ändern, sonst steht das Versprechen nur im Text."),
  ]),

 ("Nach dem Start", "messen",'''


def main():
    t = QUELLE.read_text(encoding="utf-8")
    vorher = len(t)

    t = ersetze(t, ALT_UPSELL, NEU_UPSELL, "Upsell-Korrektur + Kasse")
    t = ersetze(t, ANKER_PLAN, NEU_PLAN, "Bevor du baust")
    t = ersetze(t, ANKER_AC, NEU_AC, "ActiveCampaign/ManyChat")
    t = ersetze(t, ANKER_SEITEN, NEU_SEITEN, "Die Seiten")
    t = ersetze(t, ANKER_MAILS, NEU_MAILS, "Die Mails")
    t = ersetze(t, ANKER_ZULAUF, NEU_ZULAUF, "Der Zulauf")
    t = ersetze(t, ANKER_MESSEN, NEU_MESSEN, "Nach dem Start")
    t = ersetze(t, ANKER_NEUE_PHASEN, NEU_PHASEN, "Launch + Webinar")

    # Gegenprobe: der falsche Satz darf nicht mehr drinstehen
    if "teurer als das Gekaufte" in t.replace(
            "„teurer als das Gekaufte“", ""):
        sys.exit("🚨 Der falsche Upsell-Satz steht noch drin")

    QUELLE.write_text(t, encoding="utf-8")
    print("funnel-checkliste-bauen.py: %d -> %d Zeichen" % (vorher, len(t)))
    print("Jetzt: python scripts/cockpit/funnel-checkliste-bauen.py")


if __name__ == "__main__":
    main()
