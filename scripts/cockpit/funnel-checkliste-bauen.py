# -*- coding: utf-8 -*-
"""Die Funnel-Checkliste — eine Artifact-Seite, die je Funnel abgehakt wird.

    python scripts/cockpit/funnel-checkliste-bauen.py
    # danach: Artifact publish mit capabilities {"db": {}}

WOHER DIE PUNKTE KOMMEN: Jeder einzelne steht für einen Fehler, der in diesem
Workspace schon passiert ist und in CLAUDE.md dokumentiert wurde. Eine Liste
aus allgemeinen Ratschlägen hakt man nach zwei Wochen blind ab — eine, bei der
neben jedem Punkt steht, was beim letzten Mal schiefging, liest man.

🚨 Die Haken liegen in der Artifact-Datenbank (`db`), nicht im Browser.
   Sie sollen einen Gerätewechsel überleben und von /funnel und /strategie
   lesbar sein. Browser-Speicher könnte das nicht.

🚨 Die Funnel-Liste kommt aus context/active-funnels.json und wird beim Bauen
   eingebettet. Kommt ein Funnel dazu, läuft dieses Skript erneut — sonst
   fehlt er in der Auswahl.

🚨 Keine Personendaten auf der Seite. Aus active-funnels.json kommen nur
   Kennung, Name, Profil und Status — keine Kontakte, keine Zahlen.
"""
import html
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "funnel-checkliste.html"

# ============================================================================
#  DIE PUNKTE — je Punkt: was zu tun ist, und der Fall dahinter
# ============================================================================
#  ZWEI QUELLEN, bewusst gemischt:
#   · die Fehler, die in diesem Workspace passiert sind (CLAUDE.md)
#   · die Funnel-Methodik aus den gekauften Kursunterlagen
#     (.claude/skills/strategie/wissen/julia-evergreen.md, reference/julia-trost/)
#
#  🚨 Aus den Kursunterlagen kommt nur die MECHANIK, nie der Wortlaut und nie
#     ein fremder Name. Die Seite ist teilbar, und fremdes Material gehört
#     nicht weiterverteilt — dieselbe Grenze wie in wissen-bauen.py.
#     Wo ein Punkt von dort stammt, steht `q: "methodik"`; die eigenen Fälle
#     tragen `q: "erfahrung"`. Die Seite zeigt das als kleine Marke, damit
#     man beim Abhaken weiss, worauf der Punkt beruht.
# ============================================================================
PHASEN = [
 ("Bevor du baust", "plan",
  "Fragen, die später teuer werden, wenn sie offenbleiben.", [
   ("Das Produkt wurde schon ein- bis dreimal live verkauft", "methodik",
    "Ein Funnel verstärkt, was funktioniert — und verstärkt nichts, wenn das "
    "Angebot noch nie jemand gekauft hat. Zu früh evergreen zu gehen ist der "
    "Klassiker: Dann baut man wochenlang Technik um ein Produkt, dessen "
    "Nachfrage ungeprüft ist."),
   ("Aufgeschrieben, wo die Treppe heute endet", "methodik",
    "Alle Angebote, alle Wege, und an welcher Stelle nach dem Kauf Schluss ist. "
    "Genau dort kann niemand weiterkaufen — und genau dort hängt der Umsatz, "
    "der am leichtesten zu holen wäre."),
   ("Ein Problem, eine Verwandlung — in einem Satz", "erfahrung",
    "Wenn du es nicht in einem Satz sagen kannst, steht es auch auf der Seite "
    "nicht klar da. Gehört in <code>active-funnels.json</code> unter "
    "<code>problem</code> und <code>transformation</code>."),
   ("Das Ziel ist das grosse Produkt, nicht dieser Funnel", "methodik",
    "Ein Freebie oder Minikurs ist der Eintritt in den Trichter, nie das Ziel. "
    "Wenn du beim Bauen nicht sagen kannst, worauf er zuläuft, verkauft er "
    "einmal 37 und danach nichts mehr."),
   ("Das Anschluss-Angebot steht fest", "methodik",
    "„Dieser Minikurs führt zu jenem Kurs“ gehört aufgeschrieben, bevor gebaut "
    "wird. Von 16 Funnels hatten 6 kein <code>produkttreppe_anschluss</code> — "
    "die enden in einer Sackgasse."),
   ("Das Thema ist breit genug für oben im Trichter", "methodik",
    "Ein 0€-Produkt ist bewusst breit, damit viele hineinpassen; ein Minikurs "
    "ist spezifisch. Wer das vertauscht, baut ein Freebie, das kaum jemand "
    "will — oder einen Minikurs, der alles verspricht."),
   ("Im Ziel-Checkout nachgesehen, was dort als Upsell hängt", "erfahrung",
    "Bei den 90 Storyideen lag ein Upsell auf die Instagram-Kundenmaschine für 97 "
    "— acht Tage nach einem 333er-Pitch hätte die Kundin denselben Kurs billiger "
    "gesehen und ab dann auf den nächsten Preis gewartet."),
   ("Das 0€-Produkt ist stark genug, um Vertrauen zu erzeugen", "methodik",
    "Ein schwaches Freebie erzeugt Misstrauen, und danach kauft niemand mehr "
    "etwas. Der Anspruch: es soll besser sein als das, was andere verkaufen. "
    "Am besten mit Video, weil Persönlichkeit nur darüber ankommt."),
   ("Der Name nennt das Ziel, nicht den Inhalt", "methodik",
    "„für“ oder „um zu“ dranhängen: nicht „Vorlagen-Sammlung“, sondern wofür "
    "sie die Vorlagen will. Und keine Erwartung wecken, die drinnen nicht "
    "eingelöst wird."),
   ("Der Funnel steht in <code>active-funnels.json</code>", "erfahrung",
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
  ]),

 ("Die Kasse", "kasse",
  "Der Umsatz liegt selten im ersten Verkauf. Hier wird er liegengelassen.", [
   ("Ein Order Bump hängt am Checkout", "methodik",
    "Ein Häkchen vor dem Bezahlen, deutlich günstiger als das Hauptprodukt und "
    "spürbar rabattiert. Ohne Bump lässt du bei jedem einzelnen Verkauf Geld "
    "liegen — er ist der billigste Zusatzumsatz, den es gibt."),
   ("Ein Upsell kommt direkt nach dem Kauf", "methodik",
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
    "nichts zu erklären."),
   ("Ein Downsell fängt die Ablehnung auf", "methodik",
    "Nur wenn der Upsell abgelehnt wird, und dann günstiger. Lieber ein "
    "unpassendes Angebot als eine leere Seite."),
   ("Bei 0€: alle drei Kassen besetzt", "methodik",
    "Danke-Seite nach dem Formular · die Seite nach der Bestätigung · die "
    "Auslieferungsseite. Drei Stellen, an denen ohnehin jemand hinschaut."),
   ("Die Auslieferung führt auf eine Seite, nicht direkt aufs PDF", "methodik",
    "Ein direkter Dateilink verschenkt die Stelle und gewöhnt niemanden daran, "
    "deine Mails zu öffnen. Die Seite trägt das Produkt und daneben ein "
    "weiteres Angebot."),
   ("Das grosse Produkt steht im Funnel nie zum Normalpreis", "methodik",
    "Wer im Funnel denselben Preis sieht wie auf der Verkaufsseite, hat keinen "
    "Grund, hier zu kaufen. Der Funnel-Preis ist der Grund — und er braucht "
    "eine echte Frist, sonst ist er nur ein Preisschild."),
   ("Checkout und Upsell-Seite am Handy angesehen", "methodik",
    "Dort kauft die Mehrheit. Ein Knopf, der am Handy unter der Falz liegt, "
    "kostet mehr als jeder Textfehler."),
  ]),

 ("ActiveCampaign", "ac",
  "Hier entstehen die Fehler, die man erst Wochen später an einer Null sieht.", [
   ("0€ läuft über ein Formular im Mailtool, nicht über die Kasse", "methodik",
    "Für 0 € lässt sich über die Verkaufsplattform nichts verkaufen. Formular → "
    "Liste „Interessenten“ → eigener Tag → Automation."),
   ("Kopiertes Formular ganz durchgegangen: Liste, Tag, Bestätigung, Weiterleitung", "erfahrung",
    "Wer ein Formular kopiert, kopiert alle vier Einstellungen mit. Das Formular "
    "„0€ doTERRA Energie-Kickstart“ war eine Kopie von Freischaufeln: es setzte den "
    "Tag „Freischaufeln Lead“ und trug in die Mentoring-Liste ein. Die erste "
    "Anmeldung bekam die Freischaufeln-Mail statt Tag 1 und dazu den "
    "Business-Newsletter. Gefunden am 23.10.2026, drei Wochen später."),
   ("Die Liste passt zum Profil", "erfahrung",
    "doTERRA-Anmeldungen gehören in „doTERRA Interessenten“, Mentoring-Anmeldungen "
    "in „Regulärer Newsletter/Interessenten“. Sonst bekommt eine erschöpfte Mama "
    "deinen Business-Newsletter — und in der Standard-Bestätigungsmail steht der "
    "Listenname sogar im Betreff."),
   ("Kette Formular → Tag → Automation von vorn nachgeprüft", "erfahrung",
    "Der Tag, den das Formular setzt, muss genau der Auslöser der Automation sein. "
    "Verglichen über die Schnittstelle (Formular-Aktion gegen Automation-Auslöser), "
    "nicht nach Namen geraten. Und der Eintrag in <code>active-funnels.json</code> "
    "nennt dieselbe Formular-Nummer, dieselbe Liste und denselben Tag."),
   ("Genau EIN Eintrags-Tag, benannt „0€ &lt;Name&gt;“", "erfahrung",
    "Beim Bio-Check sind im April acht Tags auf einen Schlag entstanden, fünf "
    "davon blieben für immer leer. Ein Funnel, ein Tag."),
   ("Der Tag ist über die ID eingetragen, nicht über den Namen", "erfahrung",
    "Ein Tag lässt sich umbenennen. Die Funnel-Definition nannte einmal "
    "„Bio-Check Lead“ (0 Kontakte), während der echte Eintrags-Tag längst anders "
    "hiess — in der Auswertung stand überall eine Null."),
   ("<code>multientry</code> geprüft, bevor ein Tag nachträglich gesetzt wird", "erfahrung",
    "Alle geprüften Automationen haben <code>multientry=1</code>: dieselbe Person "
    "darf mehrfach durchlaufen. Bei der Story-Challenge ist das passiert — "
    "<code>entered=10</code> bei 8 Kontakten. Wer fünf Leuten einen Tag "
    "nachträglich gibt, schickt ihnen die ganze Strecke ein zweites Mal."),
   ("Beim Eintritt wird geprüft, ob sie schon in einer anderen Automation steckt", "methodik",
    "Sonst bekommt dieselbe Person aus zwei Funneln gleichzeitig Post. Übliche "
    "Lösung: je Automation ein Tag „läuft gerade in NN“, der am Ende wieder weg "
    "ist. Automationen durchnummerieren und lang benennen hilft dabei."),
   ("Ein Ziel „hat gekauft“ in der Automation", "erfahrung",
    "Ohne das wird jemand weiter beworben, der schon gekauft hat. Das ist die "
    "ärgerlichste Mail, die ein Funnel verschicken kann."),
   ("Die drei Listen sind sauber getrennt", "methodik",
    "Newsletter · Interessenten (0 €) · Kundinnen. Gesteuert wird über Tags, "
    "aber die Trennung muss stehen, sonst bewirbst du Kundinnen wie Fremde."),
   ("Einwilligung, eigene Bestätigungsmail, Ränder am Handy", "methodik",
    "Das Häkchen ist Pflicht, und der Standardtext der Bestätigungsmail ist "
    "die erste Mail, die sie von dir sieht."),
   ("Bestätigungsmail in deiner Stimme und ohne Angebot", "erfahrung",
    "Die AC-Vorlage siezt und nennt den internen Listennamen im Betreff („Bitte "
    "bestätigen Sie Ihr Abonnement für Regulärer Newsletter/Interessenten“). Die "
    "eigene Fassung nennt das Freebie, hat einen Knopf auf <code>%CONFIRMLINK%</code> "
    "und die Absenderadresse im Fuss. Kein Angebot: ihr einziger Job ist der Klick, "
    "erst danach setzt AC Tag und Liste. Muster: "
    "<code>outputs/produkte/doterra-mama-energie/mails/kickstart-mail-0.html</code>."),
   ("Zwischen Kauf und Pitch liegt eine Wartezeit", "methodik",
    "Wer gerade gekauft hat, soll erst einmal hineinschauen. Direkt "
    "hinterherzupitchen wirkt, als wäre das Gekaufte nur der Köder gewesen. "
    "Üblich: ein paar Tage, dann die Verkaufsstrecke."),
   ("Entschieden, was mit denen passiert, die nicht kaufen", "methodik",
    "Sie fallen sonst hinten aus dem Funnel und hören nie wieder etwas. Zwei "
    "Wege: gleich in die nächste Automation, oder nach ein paar Monaten noch "
    "einmal von vorn."),
   ("Auslieferung selbst getestet — mit einer echten Adresse eingetragen", "erfahrung",
    "Nicht die Automation ansehen, sondern sich eintragen und warten, ob die "
    "Mail kommt. Alles andere ist eine Vermutung."),
   ("ManyChat reagiert auf alle drei Wege", "methodik",
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

 ("Die Seiten", "seiten",
  "Vier Adressen, und jede kann still kaputt sein.", [
   ("Landingpage ist erreichbar", "erfahrung",
    "Kein eigener Slug heisst nicht: keine Seite. Die Einzelkurse liegen alle auf "
    "<code>/angebote/</code> mit Sprungmarken. Vor „hat keine Landingpage“ immer "
    "die Sammelseite durchsehen."),
   ("Checkout-Status geprüft: live, nicht <code>test</code> oder <code>disabled</code>", "erfahrung",
    "„Dein starkes Mama-Business“ stand auf <code>test</code> und war trotzdem "
    "von <code>/angebote/</code> verlinkt. Wer dort kaufte, bezahlte nichts — und "
    "die Seite sah dabei völlig normal aus. Ein 200er sagt nichts darüber, ob die "
    "Kasse Geld nimmt."),
   ("Danke-Seite steht und führt weiter", "methodik",
    "Die Danke-Seite ist der Platz für den Tripwire. Leer gelassen ist sie eine "
    "Sackgasse direkt nach dem Ja."),
   ("Die Danke-Seite passt zur Bestätigung", "erfahrung",
    "„Fast geschafft — klick den Link in der Mail“ stimmt nur, wenn das Formular "
    "eine Bestätigungsmail verschickt. Beim Freischaufeln-Formular ist sie "
    "ausgeschaltet; die Seite schickt sie auf die Suche nach einer Mail, die nie "
    "kommt."),
   ("Seite nach dem Bestätigungsklick hinterlegt", "erfahrung",
    "Ohne eigene Adresse zeigt AC seine Standardseite, und die zweite "
    "Verkaufsstelle bleibt leer. Dort steht „bestätigt, Tag 1 ist unterwegs“ und "
    "darunter das grosse Angebot. Beim Energie-Kickstart: "
    "<code>/energie-kickstart-bestaetigt/</code> mit der 30-Tage-Energie-Routine."),
   ("Bei einer Frist: eigene Angebotsseite und eine „abgelaufen“-Seite", "methodik",
    "Eine Frist, die nur im Text behauptet wird, ist keine. Wer nach Ablauf "
    "klickt, landet sonst auf demselben Preis und merkt, dass die Frist nichts "
    "bedeutet. Auf der Abgelaufen-Seite steht ein kleineres Angebot, damit der "
    "Klick nicht ins Leere geht."),
   ("Entschieden: eigene Verkaufsseite oder nur die Kasse", "methodik",
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
   ("Jede Adresse einmal wirklich aufgerufen", "erfahrung",
    "<code>bio-check.mumlifebalance.ch</code> löst gar nicht auf — der lebende "
    "Bot liegt woanders. Gemerkt hat das niemand, weil niemand draufgeklickt hat."),
  ]),

 ("Die Mails", "mails",
  "Was hier steht, liest sie als Erstes — oder nie wieder.", [
   ("Jede Mail einmal am Handy geöffnet", "erfahrung",
    "Der orange Balken im Mailkopf war ein Inline-Span. Bricht er am Handy um, "
    "zeichnet die Mail-App zwei lose Hälften — so in der KI-Kurs-Mail vom "
    "23.10.2026. Seitdem ist er eine Tabellenzelle in allen Mail-Generatoren. "
    "Die Outlook-App vergrössert die Schrift, also im echten Postfach schauen, "
    "nicht nur in der Vorschau."),
   ("Die Betreffzeile ist ein Hook", "methodik",
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
   ("Keine einzige Mail ohne Link", "methodik",
    "Jede Mail hat ein Angebot und einen Weg dorthin. Eine Mail ohne Link ist "
    "ein Newsletter, der sich in einen Verkaufs-Funnel verirrt hat."),
   ("Jeder Knopf führt irgendwohin", "erfahrung",
    "In „1 Mail Stimcheck nach Masterclass“ zeigte der einzige Knopf auf "
    "<code>#aufzeichnung-folgt</code>, einen Platzhalter. Wer klickte, blieb "
    "stehen. Die Mail war damit funktionslos."),
   ("Im Verkaufs-Funnel wird verkauft, im Newsletter nicht", "methodik",
    "Der Newsletter ist fast ganz Beziehung, mit einem Link im P.S. Der "
    "Verkaufs-Funnel ist fast ganz Verkauf: Problem → was es kostet, nichts zu "
    "ändern → Lösung als Geschichte → Angebot → Frist. Wer beides mischt, "
    "macht keins von beidem."),
   ("Der Pitch nennt das Ziel hinter dem Ziel", "methodik",
    "Nicht das Merkmal, sondern wofür sie es will: „damit“, „um zu“, „für“. "
    "Niemand will einen Skill, alle wollen den Freitagmorgen zurück."),
   ("Keine festen Datumsangaben in einer Dauer-Automation", "erfahrung",
    "„Bis Donnerstag, 23. Oktober“ stimmt drei Wochen später nicht mehr. In einer "
    "Automation, die evergreen läuft, gehört eine relative Frist hin — oder der "
    "Block kommt nach dem Launch wieder raus."),
   ("Blacklisten-Prüfung gelaufen", "erfahrung",
    "<code>python scripts/cockpit/texte-pruefen.py</code>. Eine Prüfung aus dem "
    "Gedächtnis fand 1 von 4 Treffern — „Nicht weil etwas war. Sondern weil …“ "
    "steht über zwei Sätze."),
   ("Umlaute und Schweizer ss geprüft", "erfahrung",
    "„so haettest du es geschrieben“ stand dreimal in einer fertigen Mail. "
    "Gefunden hat es Patricia, nicht die Selbstprüfung."),
   ("Zwei Zielgruppen-Ebenen beachtet", "erfahrung",
    "„Deine Kundin“ ist fast immer die zweite Ebene — die Kundschaft deiner "
    "Kundin, und die ist nicht weiblich. Richtig: Kundschaft, Leute, "
    "Interessenten."),
  ]),

 ("Der Zulauf", "zulauf",
  "Der häufigste Grund, warum ein fertiger Funnel bei null bleibt.", [
   ("Mindestens ein geplanter Beitrag nennt das Stichwort", "erfahrung",
    "Vier Stichwörter liefen völlig leer: Automation gebaut, Tag angelegt, und "
    "kein einziger Beitrag nannte das Wort. Das ist kein Funnel-Problem, das ist "
    "ein Content-Problem — und es sieht von aussen gleich aus."),
   ("Der Funnel ist dauerhaft sichtbar, nicht nur in einer Story", "methodik",
    "Story-Highlight mit sichtbarem Preis, Link in der Bio, ein angepinnter "
    "Beitrag. Wer auf dein Profil kommt, soll jederzeit kaufen können — nicht "
    "nur an dem Tag, an dem du darüber sprichst."),
   ("ManyChat-Flow eingerichtet", "erfahrung",
    "ManyChat hat eigene Tags, und sie heissen anders als in ActiveCampaign. Für "
    "sechs Freebies gibt es dort gar keinen. Prüfen statt annehmen."),
   ("Das Stichwort löst nur beim gemeinten Wort aus", "erfahrung",
    "ManyChat löst bei jedem Kommentar aus, in dem das Wort vorkommt — auch bei "
    "„ich STIMME dir zu“. Bei kurzen Alltagswörtern vorher überlegen."),
   ("Anzeigen laufen aufs kleine Produkt, nicht auf den grossen Kurs", "methodik",
    "Kalte Leute kaufen keinen Tausender. Die Anzeige holt sie ins Freebie oder "
    "in einen Minikurs, verkauft wird danach im Funnel."),
   ("Selbst Nachrichten geschrieben, nicht nur gewartet", "methodik",
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
   ("Telegram-Gruppe verlinkt, falls es eine gibt", "erfahrung",
    "Neun Angebote haben eine eigene Gruppe. Die Einladungslinks standen nirgends "
    "in der Doku, nur in den AC-Mails."),
  ]),

 ("Der Launch", "launch",
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

 ("Nach dem Start", "messen",
  "Zwei Wochen später, mit Zahlen statt Gefühl.", [
   ("Eintragungen je Beitrag ausgerechnet", "erfahrung",
    "BIO brachte 0,8 Eintragungen je Beitrag, ECHT1 bei dreimal so vielen "
    "Beiträgen nur 0,1. Ohne diese Zahl hält man den fleissigeren für den "
    "besseren."),
   ("Verstanden, was die Zahl misst", "erfahrung",
    "Sie misst Eintragungen in die Mailliste, nicht Reaktionen im Messenger. Wer "
    "im DM antwortet und keine Adresse hinterlässt, fehlt. Die Zahl ist eine "
    "Untergrenze."),
   ("Geteilte Tags nicht doppelt gezählt", "erfahrung",
    "SICHTBAR und ANLEITUNG zeigen beide auf den Starterguide, FAHRPLAN und "
    "SYSTEM beide auf den Fahrplan. Die Zahl gehört dem Freebie, nicht dem "
    "Stichwort."),
   ("Weiter über das Angebot reden, auch wenn der Funnel läuft", "methodik",
    "Ein Funnel ist nicht selbstlaufend. Wer aufhört, in Story und Feed darüber "
    "zu sprechen, sieht die Verkäufe einbrechen — und sucht den Fehler dann in "
    "der Technik."),
   ("Bei Flaute unterschieden: zu wenig Klicks oder zu wenig Käufe", "methodik",
    "Wenige Klicks heisst, der Hook oder das Bild zieht nicht. Viele Klicks "
    "ohne Kauf heisst, die Seite dahinter überzeugt nicht. Zwei verschiedene "
    "Probleme, und wer sie verwechselt, repariert das Falsche."),
   ("Kundenstimmen aktiv eingeholt", "methodik",
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
   ("Entschieden: weiterlaufen lassen, nachschärfen oder abstellen", "erfahrung",
    "Ein Funnel, der nach vier Wochen null bringt und trotzdem stehenbleibt, "
    "kostet jede Woche Aufmerksamkeit und bringt nichts zurück."),
  ]),
]


def schluessel(text):
    """Stabile Kennung aus dem Punkt-Text.

    Umlaute werden umgeschrieben, Markup und Satzzeichen fallen weg. Dieselbe
    Umschrift wie ueberall im Workspace: erst ae/oe/ue/ss, dann filtern — wer
    direkt filtert, macht aus „fuer" ein „fr" und bekommt Kollisionen.
    """
    s = re.sub(r"<[^>]+>", " ", text).lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                 ("ß", "ss"), ("&lt;", ""), ("&gt;", ""), ("&amp;", "")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return "-".join(s.split("-")[:5])[:38]


def funnels():
    """Kennung, Name, Profil, Status — mehr geht nicht auf die Seite."""
    d = json.loads((ROOT / "context" / "active-funnels.json").read_text(encoding="utf-8"))
    roh = d.get("funnels") or d
    items = list(roh.values()) if isinstance(roh, dict) else roh
    raus = []
    for x in items:
        if not isinstance(x, dict) or not x.get("id"):
            continue
        raus.append({"id": x["id"], "name": x.get("name") or x["id"],
                     "profil": x.get("profile") or "", "status": x.get("status") or ""})
    raus.sort(key=lambda x: (x["profil"], x["name"].lower()))
    return raus


CSS = """
/* Eine Spalte, Phase für Phase. Die Reihenfolge IST die Information:
   so läuft ein Funnel von der Idee bis zur Auswertung. */
:root{
  --grund:#f3efe4; --blatt:#fbf8f1; --blatt2:#ebe4d3;
  --tinte:#0c1c30; --weich:#5f6f80; --linie:rgba(12,28,48,.14);
  --petrol:#12828c; --petrol-w:rgba(18,130,140,.12);
  --orange:#dc822e; --orange-w:rgba(220,130,46,.15);
  --gut:#2f7d5b;
  --display:"Philosopher",Georgia,serif;
  --body:"Source Sans 3","Segoe UI",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --grund:#0c1c30; --blatt:#12283f; --blatt2:#1a3450;
  --tinte:#f1ecdd; --weich:#a8bccb; --linie:rgba(241,236,221,.16);
  --petrol:#35a8b2; --petrol-w:rgba(53,168,178,.16);
  --orange:#eb9a4f; --orange-w:rgba(235,154,79,.18);
  --gut:#5fb98d; color-scheme:dark;
}}
:root[data-theme="dark"]{
  --grund:#0c1c30; --blatt:#12283f; --blatt2:#1a3450;
  --tinte:#f1ecdd; --weich:#a8bccb; --linie:rgba(241,236,221,.16);
  --petrol:#35a8b2; --petrol-w:rgba(53,168,178,.16);
  --orange:#eb9a4f; --orange-w:rgba(235,154,79,.18);
  --gut:#5fb98d; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--grund);color:var(--tinte);font-family:var(--body);
     font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.huelle{max-width:840px;margin:0 auto;padding-block:26px 80px;padding-left:16px;padding-right:16px}
h1{font-family:var(--display);font-weight:400;font-size:clamp(26px,6vw,36px);
   line-height:1.14;margin:0 0 8px;text-wrap:balance}
.unter{margin:0;color:var(--weich);font-size:15px;max-width:62ch}

.leiste{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--grund);
        padding:14px 0 12px;margin:22px 0 0;border-bottom:1px solid var(--linie);
        display:flex;gap:12px;align-items:center;flex-wrap:wrap}
select{font:inherit;font-size:15px;background:var(--blatt);color:var(--tinte);
       border:1px solid var(--linie);border-radius:10px;padding:9px 12px;max-width:100%}
select:focus-visible{outline:2px solid var(--petrol);outline-offset:1px}
.stand{margin-left:auto;font-size:14px;color:var(--weich);font-variant-numeric:tabular-nums}
.stand b{font-family:var(--display);font-size:19px;color:var(--tinte)}
.balken{height:6px;border-radius:99px;background:var(--blatt2);overflow:hidden;
        flex:1 1 140px;min-width:120px}
.balken i{display:block;height:100%;background:var(--petrol);width:0;
          transition:width .25s ease}
@media (prefers-reduced-motion:reduce){.balken i{transition:none}}

.phase{margin:26px 0 0;background:var(--blatt);border:1px solid var(--linie);
       border-radius:16px;overflow:hidden}
.phase>summary{cursor:pointer;list-style:none;padding:16px 20px;display:flex;
               gap:12px;align-items:baseline;flex-wrap:wrap}
.phase>summary::-webkit-details-marker{display:none}
.phase>summary::before{content:"\\25b6";font-size:10px;color:var(--weich);
                       transition:transform .15s ease}
.phase[open]>summary::before{transform:rotate(90deg)}
.phase h2{font-family:var(--display);font-weight:400;font-size:21px;margin:0;
          line-height:1.25}
.phase .zahl{margin-left:auto;font-size:13px;color:var(--weich);
             font-variant-numeric:tabular-nums;white-space:nowrap}
.phase .zahl.voll{color:var(--gut);font-weight:600}
.phase .was{flex:1 1 100%;margin:2px 0 0;font-size:14px;color:var(--weich)}
.punkte{padding:0 20px 18px;display:flex;flex-direction:column;gap:2px}

.punkt{display:grid;grid-template-columns:26px minmax(0,1fr);gap:10px;
       padding:12px 0;border-top:1px solid var(--linie)}
.punkt:first-child{border-top:0}
.punkt input{width:19px;height:19px;margin-top:3px;accent-color:var(--petrol);cursor:pointer}
.punkt label{cursor:pointer;font-size:15.5px;line-height:1.55}
.punkt.ab label{color:var(--weich);text-decoration:line-through}
.warum{margin:6px 0 0;font-size:13.5px;line-height:1.65;color:var(--weich);
       border-left:2px solid var(--orange);padding-left:11px}
.warum code{background:var(--orange-w);border-radius:4px;padding:1px 5px;
            font-size:12.5px;word-break:break-word}
.q{display:inline-block;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
   padding:1px 7px;border-radius:999px;margin-right:7px;vertical-align:1px;white-space:nowrap}
.q.erf{background:var(--orange-w);color:var(--orange)}
.q.met{background:var(--petrol-w);color:var(--petrol)}

.fuss{margin:34px 0 0;padding-top:18px;border-top:1px solid var(--linie);
      font-size:13.5px;color:var(--weich);line-height:1.7}
.hinweis{background:var(--petrol-w);border-radius:12px;padding:12px 16px;
         font-size:14px;margin:18px 0 0}
"""


def js(funnel_json):
    return """
var FUNNELS = %s;
var gewaehlt = null, haken = {}, db = null, doc = null, schreibt = false;

function alleFelder(){ return Array.prototype.slice.call(document.querySelectorAll(".punkt input")); }

function zeichnen(){
  var f = alleFelder(), fertig = 0;
  f.forEach(function(e){
    var an = !!haken[e.dataset.k];
    e.checked = an;
    e.closest(".punkt").classList.toggle("ab", an);
    if (an) fertig++;
  });
  document.querySelectorAll(".phase").forEach(function(p){
    var ein = Array.prototype.slice.call(p.querySelectorAll(".punkt input"));
    var n = ein.filter(function(e){ return haken[e.dataset.k]; }).length;
    var z = p.querySelector(".zahl");
    z.textContent = n + " von " + ein.length;
    z.classList.toggle("voll", n === ein.length && ein.length > 0);
  });
  var s = document.getElementById("stand");
  s.innerHTML = "<b>" + fertig + "</b> von " + f.length;
  document.getElementById("fuell").style.width =
    (f.length ? Math.round(fertig / f.length * 100) : 0) + "%%";
}

function sichern(){
  if (!doc || schreibt) return;
  schreibt = true;
  doc.set({ funnel: gewaehlt, haken: haken, stand: new Date().toISOString() })
     .catch(function(){ /* beim nächsten Haken erneut */ })
     .then(function(){ schreibt = false; });
}

function laden(id){
  gewaehlt = id; haken = {}; zeichnen();
  if (!db) return;
  doc = db.doc("funnelcheck/" + id);
  doc.get().then(function(s){
    if (gewaehlt !== id) return;            // inzwischen umgeschaltet
    haken = (s.exists && s.data().haken) || {};
    zeichnen();
  }).catch(function(){});
}

document.addEventListener("change", function(e){
  var i = e.target.closest(".punkt input");
  if (!i) return;
  if (i.checked) haken[i.dataset.k] = true; else delete haken[i.dataset.k];
  zeichnen(); sichern();
});

var wahl = document.getElementById("wahl");
FUNNELS.forEach(function(f){
  var o = document.createElement("option");
  o.value = f.id;
  o.textContent = f.name + (f.status && f.status !== "live" ? "  \\u00b7 " + f.status : "");
  wahl.appendChild(o);
});
wahl.addEventListener("change", function(){ laden(this.value); });

zeichnen();
if (FUNNELS.length) laden(FUNNELS[0].id);

// 🚨 Über window.claude, nicht über das nackte `claude`: in der lokalen
//    Vorschau gibt es den Viewer nicht, und ein ReferenceError würde das
//    Skript an dieser Stelle abbrechen. Die Liste muss auch ohne Datenbank
//    durchgehbar sein.
// 🚨 Kein Umlaut in einem Bezeichner. Mit `brücke` war die Seite beim ersten
//    Test tot: ohne charset las der Browser UTF-8 als Latin-1, der Name wurde
//    unlesbar und das ganze Skript brach mit einem SyntaxError ab — Auswahl
//    leer, Haken ohne Wirkung. `node --check` sieht das nicht, weil es die
//    Datei korrekt als UTF-8 liest.
var bruecke = (window.claude && window.claude.use)
  ? window.claude.use("db")
  : Promise.resolve(null);
bruecke.then(function(d){
  db = d;
  var hin = document.getElementById("speicherhinweis");
  if (!d) {
    hin.textContent = "Die Haken lassen sich hier gerade nicht speichern \\u2014 "
      + "die Liste funktioniert trotzdem zum Durchgehen.";
    return;
  }
  hin.textContent = "Die Haken werden gespeichert, je Funnel getrennt.";
  if (gewaehlt) laden(gewaehlt);
}).catch(function(){});
""" % funnel_json


def main():
    fs = funnels()
    assert fs, "keine Funnels in active-funnels.json gefunden"

    # 🚨 Gegenprobe: nichts Persönliches auf die Seite. Die Felder sind fest
    #    gewählt, aber ein Name könnte theoretisch eine Adresse enthalten.
    roh = json.dumps(fs, ensure_ascii=False)
    for muster, was in [(r"[\w.+-]+@[\w-]+\.\w+", "Mailadresse"),
                        (r"\+41\s?\d", "Telefonnummer")]:
        assert not re.search(muster, roh), "🚨 %s in der Funnel-Liste" % was

    # Woher ein Punkt stammt — als kleine Marke neben der Begründung, damit
    # beim Abhaken sichtbar ist, ob dahinter ein eigener Fehler steht oder die
    # Methodik aus den Kursunterlagen.
    MARKE = {"erfahrung": ("hier passiert", "erf"),
             "methodik":  ("Methodik", "met")}

    phasen = ""
    gesamt = 0
    zaehlung = {"erfahrung": 0, "methodik": 0}
    for titel, kuerzel, was, punkte in PHASEN:
        zeilen = ""
        for i, (text, quelle, warum) in enumerate(punkte, 1):
            assert quelle in MARKE, "unbekannte Quelle %r bei %r" % (quelle, text)
            zaehlung[quelle] += 1
            lab, kurz = MARKE[quelle]
            # 🚨 Die Kennung kommt aus dem TEXT, nicht aus der Position.
            #    Mit `kuerzel-1`, `kuerzel-2` … hätte ein später eingefügter
            #    Punkt alle Haken danach um eins verschoben: gesetzte Haken
            #    stünden plötzlich beim falschen Punkt, und niemand sähe es.
            #    Ein Punkt, dessen Text sich ändert, bekommt bewusst eine neue
            #    Kennung — dann ist es inhaltlich auch ein neuer Punkt.
            k = "%s-%s" % (kuerzel, schluessel(text))
            zeilen += (
              '<div class="punkt">'
              '<input type="checkbox" id="%s" data-k="%s">'
              '<div><label for="%s">%s</label>'
              '<p class="warum"><span class="q %s">%s</span>%s</p></div>'
              '</div>' % (k, k, k, text, kurz, html.escape(lab, quote=False), warum))
            gesamt += 1
        phasen += (
          '<details class="phase" open>'
          '<summary><h2>%s</h2><span class="zahl">0 von %d</span>'
          '<p class="was">%s</p></summary>'
          '<div class="punkte">%s</div>'
          '</details>' % (html.escape(titel, quote=False), len(punkte),
                          html.escape(was, quote=False), zeilen))

    seite = (
      '<title>Funnel-Checkliste</title>'
      '<link rel="preconnect" href="https://fonts.googleapis.com">'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700'
      '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">'
      '<style>%s</style>'
      '<div class="huelle">'
      '<h1>Funnel-Checkliste</h1>'
      '<p class="unter">%d Punkte in sechs Phasen. Neben jedem steht, was beim '
      'letzten Mal schiefging &mdash; deshalb ist die Liste so lang und deshalb '
      'lohnt sie sich.</p>'
      '<div class="leiste">'
      '<select id="wahl" aria-label="Funnel ausw&auml;hlen"></select>'
      '<div class="balken"><i id="fuell"></i></div>'
      '<span class="stand" id="stand"><b>0</b> von %d</span>'
      '</div>'
      '%s'
      '<p class="hinweis" id="speicherhinweis">Haken werden geladen &hellip;</p>'
      '<div class="fuss">'
      '<p><span class="q erf">hier passiert</span> steht f&uuml;r einen Fehler, der in diesem Workspace wirklich vorkam: '
      'der tote Knopf, der nirgendwohin f&uuml;hrte &middot; die acht Tags, von denen '
      'f&uuml;nf leer blieben &middot; der Checkout auf <code>test</code>, der kein Geld '
      'nahm &middot; die vier Stichw&ouml;rter, die kein einziger Beitrag nannte.</p>'
      '<p>Neuer Funnel in <code>active-funnels.json</code>? Dann l&auml;uft '
      '<code>scripts/cockpit/funnel-checkliste-bauen.py</code> noch einmal, sonst '
      'fehlt er in der Auswahl.</p>'
      '</div></div>'
      '<script>%s</script>'
    ) % (CSS, gesamt, gesamt, phasen, js(json.dumps(fs, ensure_ascii=False)))

    # 🚨 Kein Umlaut in einem JS-Bezeichner — siehe Kommentar im Skript.
    #    Geprueft wird nur der Code: Zeichenketten UND beide Kommentararten
    #    fallen vorher raus. Ohne die Block-Kommentare meldete die Regel beim
    #    ersten Lauf „naechsten" aus einem /* … */ — ein Fehlalarm, und nach
    #    dem dritten liest niemand mehr hin.
    skript = seite[seite.rfind("<script>") + 8:seite.rfind("</script>")]
    AP, HO, BS = chr(34), chr(39), chr(92)
    muster = "|".join([
        AP + "[^" + AP + "]*" + AP,          # "…"
        HO + "[^" + HO + "]*" + HO,          # '…'
        r"/\*.*?\*/",                        # /* … */
        "//[^" + BS + "n]*",                 # // …
    ])
    ohne_text = re.sub(muster, " ", skript, flags=re.S)
    umlaute = "äöüÄÖÜß"
    schlecht = sorted(set(re.findall(r"\w*[" + umlaute + r"]\w*", ohne_text)))
    assert not schlecht, "🚨 Umlaut in einem JS-Bezeichner: %s" % schlecht

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(seite, encoding="utf-8")
    print("%d Punkte in %d Phasen · %d Funnels zur Auswahl" % (gesamt, len(PHASEN), len(fs)))
    print("   %d aus eigenen Fehlern · %d aus der Methodik\n"
          % (zaehlung["erfahrung"], zaehlung["methodik"]))
    for t, _, _, p in PHASEN:
        erf = sum(1 for x in p if x[1] == "erfahrung")
        print("   %-22s %2d   (%d erf · %d met)" % (t, len(p), erf, len(p) - erf))
    print("\nGeschrieben: %s  (%d KB)" % (ZIEL.relative_to(ROOT), len(seite) // 1024))
    print('Danach: Artifact publish, capabilities {"db": {}}')


def punkte_als_markdown():
    """Alle Punkte als Prüfliste für `/angebot trichter` — dieselbe Liste wie
    auf der Seite, damit Prüfung und Abhaken nie auseinanderlaufen."""
    zeilen = []
    for titel, _, was, punkte in PHASEN:
        zeilen.append("\n## %s\n\n_%s_\n" % (titel, re.sub(r"<[^>]+>", "", was)))
        for text, quelle, warum in punkte:
            warum = re.sub(r"<[^>]+>", "", warum).replace("&lt;", "<").replace("&gt;", ">")
            zeilen.append("- [ ] **%s** `%s` · %s  \n  %s"
                          % (re.sub(r"<[^>]+>", "", text), schluessel(text), quelle, warum))
    return "\n".join(zeilen)


if __name__ == "__main__":
    if "--punkte" in sys.argv:
        print(punkte_als_markdown())
    else:
        main()
