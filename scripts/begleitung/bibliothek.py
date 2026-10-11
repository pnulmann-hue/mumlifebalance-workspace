# -*- coding: utf-8 -*-
"""Die Wissensbibliothek und die Tagesimpulse der 30-Tage-Energie-Routine.

**Getrennt von `inhalte.py`**, weil das hier der grosse Teil ist und beides sonst
in einer 100-KB-Datei laege, in der niemand mehr etwas findet.

🚨 **Jeder Artikel hat einen `tag`** — den Tag, an dem er freigeschaltet wird.
Vorher steht er als verschlossene Zeile da (Titel plus „ab Tag N“), damit sichtbar
ist, dass noch etwas kommt, ohne dass am Tag 1 fuenfzig Artikel erschlagen.

🚨 **Nur gruenes Material.** Fakten aus Patricias eigenen Buechern mit Autor und
Titel, aus ihrer Immunwoche, oder Allgemeinwissen in eigenen Worten. Kein Satz aus
einem bezahlten Coaching.

🚨 **Keine Heilversprechen, keine Diagnosen.** Wo es medizinisch wird — Blutwerte,
Schilddruese, Hormontherapie, anhaltende Beschwerden — steht der Verweis auf die
Aerztin im Text, nicht im Kleingedruckten. Hormonersatztherapie kommt bewusst
NICHT vor, obwohl das Buch ein Kapitel dazu hat: das ist aerztliches Gebiet.
"""

# ---------------------------------------------------------------------------
# Die Tagesimpulse — einer je Tag, kurz gehalten
# ---------------------------------------------------------------------------

IMPULSE = {
 1:  ("Heute nur eins: das Frühstück",
      "Such dir aus der Rezeptbibliothek ein Frühstück aus, von dem du denkst, du "
      "würdest es zweimal machen. Nicht das gesündeste — das, worauf du Lust hast. "
      "Und nimm heute deine Nährstoffe zum ersten Mal, zu einer Gelegenheit, die du "
      "sowieso jeden Tag hast."),
 2:  ("Dasselbe nochmal",
      "Heute kein neues Thema. Wenn dir das Frühstück von gestern geschmeckt hat, mach "
      "es nochmal. Wiederholung ist hier keine Langeweile, sondern der ganze Trick."),
 3:  ("Wie war dein Vormittag?",
      "Schreib heute unten ins Feld, wie sich dein Vormittag angefühlt hat. Noch muss "
      "sich nichts verändert haben — es geht darum, dass du anfängst hinzuschauen."),
 4:  ("Der Teller, nicht die Waage",
      "Heute schaust du einmal auf deinen Mittagsteller. Die Hälfte Gemüse, ein Viertel "
      "Protein, ein Viertel Kohlenhydrate. Kein Abwiegen. Nur hinschauen, und beim "
      "nächsten Mal ein bisschen verschieben."),
 5:  ("Rechne deinen Nachmittag aus",
      "Wann isst du zu Mittag, wann zu Abend? Wenn mehr als fünf Stunden dazwischen "
      "liegen — und bei zwölf Uhr und halb sieben sind es sechseinhalb —, dann nimm "
      "dir heute etwas für dazwischen mit. Mit echtem Protein, nicht einen Riegel."),
 6:  ("Zwei Esslöffel",
      "Leinsamen auf dein Frühstück. Zwei Esslöffel, geschrotet. Das schliesst den "
      "grössten Teil deiner Ballaststoff-Lücke, und du schmeckst sie kaum."),
 7:  ("Eine Woche ist rum",
      "Schau dir im Reiter „Dein Plan“ dein Gitter an. Sieben Tage. Was davon ging "
      "leicht, was war mühsam? Schreib es unten rein — das ist dein erster Rückblick."),
 8:  ("Ab heute kommen die Schritte dazu",
      "8000 am Tag. Nicht als Sporttermin, sondern verteilt: Kinder zu Fuss bringen, "
      "das nächste Telefonat im Gehen, abends eine Runde. Schau heute einfach mal "
      "nach, wo du überhaupt stehst."),
 9:  ("Schreib den Termin auf",
      "Dein erstes Krafttraining diese Woche. In den Kalender, mit Uhrzeit. Als Termin, "
      "nicht als Vorsatz — das ist der ganze Unterschied."),
 10: ("Egal wann",
      "Falls du gerade denkst, du müsstest um sechs Uhr aufstehen: musst du nicht. Ich "
      "habe mich jahrelang damit gestresst und dabei übersehen, dass es völlig egal "
      "ist, wann. Hauptsache dreimal die Woche."),
 11: ("Drei Spalten",
      "Schreib nach dem Training auf, was du gemacht hast: Übung, Gewicht, "
      "Wiederholungen. Handy oder Zettel. Ohne Notiz erinnerst du dich falsch, und "
      "dann trainierst du in drei Monaten noch mit demselben Gewicht."),
 12: ("Ruhetag ist Teil des Plans",
      "Wenn du gestern trainiert hast, ist heute frei für diese Muskelgruppe. Gewachsen "
      "wird nicht im Training, sondern dazwischen."),
 13: ("Wie fühlt sich der Nachmittag an?",
      "Zwei Wochen sind fast rum. Vergleich mal mit dem, was du am Tag 3 "
      "aufgeschrieben hast. Bei den meisten ist der Vormittag zuerst anders, der "
      "Nachmittag braucht länger."),
 14: ("Halbzeit steht bevor",
      "Nächste Woche reden wir darüber, warum das alles zusammenhängt — und was sich "
      "ab Mitte dreissig ohnehin verändert. Heute nur weitermachen."),
 15: ("Der Abend beginnt früher, als du denkst",
      "Ab heute: Handy dreissig Minuten vor dem Bett weg. Ich weiss. Probier es drei "
      "Tage, bevor du entscheidest, ob es etwas bringt."),
 16: ("Ein Duft, der den Tag beendet",
      "Such dir eins deiner Öle aus — in der Lotion, auf den Handgelenken, im "
      "Diffuser. Es geht nicht um das bestimmte Öl. Es geht darum, dass immer dasselbe "
      "kommt, wenn der Tag vorbei ist."),
 17: ("Wie hast du geschlafen?",
      "Die meisten merken in dieser Woche zum ersten Mal etwas am Schlaf. Schreib "
      "heute auf, wie du aufgewacht bist — auch wenn sich noch nichts verändert hat."),
 18: ("Heute wird es persönlich",
      "In der Bibliothek stehen ab heute die Stücke über das, worüber mit uns selten "
      "jemand spricht. Nimm dir dafür zehn Minuten in Ruhe, nicht zwischen Tür und "
      "Angel."),
 19: ("Nicht du bist das Problem",
      "Falls dich gestern etwas getroffen hat: das ist normal, und es ist der Grund, "
      "warum das Thema erst jetzt kommt und nicht am Tag 1. Heute steht in der "
      "Bibliothek, wohin du gehen kannst, wenn du es genauer wissen willst — Blutbild "
      "und Hormontest, und was ich selber nehme."),
 20: ("Erholung ist keine Belohnung",
      "Sie ist Teil der Arbeit. Wenn du diese Woche einen Trainingstag ausfallen lässt, "
      "weil du erschöpft bist, ist das kein Versagen — das ist die richtige "
      "Entscheidung."),
 21: ("Drei Wochen",
      "Schau nochmal ins Gitter. Und lies, was du in Woche 1 aufgeschrieben hast. "
      "Meistens ist der Unterschied dort besser zu sehen als im Spiegel."),
 22: ("Jetzt läuft alles parallel",
      "Kein neues Thema mehr. Ab hier geht es nur noch darum, dass sich das Ganze "
      "normal anfühlt statt nach Programm."),
 23: ("Was würdest du behalten?",
      "Wenn du morgen aufhören müsstest — welche eine Sache würdest du weitermachen? "
      "Schreib sie auf. Das ist die, die bleibt."),
 24: ("Deine Dose wird leer",
      "Schau heute nach, wie weit deine Nährstoffe noch reichen. Nicht wegen des "
      "Nachschubs — sondern damit dich der Tag nicht überrascht."),
 25: ("Die wichtigste Frage",
      "Was ist in den letzten Wochen anders geworden? Ganz egal wie klein. Lies dir "
      "unten deine Einträge von Anfang an durch, bevor du antwortest. Das ist "
      "eindrücklicher als jede Waage."),
 26: ("Sag es jemandem",
      "Erzähl heute einer Person, was sich verändert hat. Nicht als Werbung — sondern "
      "weil etwas, das man ausspricht, plötzlich wahr wird."),
 27: ("Was war am schwersten?",
      "Schreib auf, woran du diesen Monat fast gescheitert wärst. Das ist die Stelle, "
      "an der du beim nächsten Mal vorbereitet bist."),
 28: ("Dein Satz von Tag 1",
      "Im Start-Gespräch hast du gesagt, woran du merken würdest, dass es sich gelohnt "
      "hat. Erinnerst du dich? Schau, wie es damit aussieht."),
 29: ("Was bleibt, gehört dir",
      "Die Frühstücke, die Bibliothek, die Erfahrung, wie sich ein Vormittag ohne Loch "
      "anfühlt. Das nimmt dir niemand mehr weg, egal wie es weitergeht."),
 30: ("Letzter Tag",
      "Du hast dreissig Tage lang vier Sachen gemacht, während der Alltag weiterlief. "
      "Das ist mehr, als die meisten schaffen. Lies deine Einträge nochmal durch — und "
      "dann entscheide in Ruhe, was davon bleibt."),
}

# ---------------------------------------------------------------------------
# Die Bibliothek — Regale, Artikel, Freischalt-Tag
# ---------------------------------------------------------------------------

BIBLIOTHEK = [

 dict(regal="Energie und Blutzucker", ton="orange", stuecke=[

  dict(id="achterbahn", tag=1, titel="Warum du um halb zehn einbrichst",
       kurz="Dein Vormittagstief ist keine Schwäche. Es ist die Folge von dem, was um sieben auf dem Teller lag.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Isst du morgens vor allem schnelle Kohlenhydrate — Brot mit Konfi, süsses "
             "Müesli, ein Gipfeli —, steigt dein Blutzucker rasant. Deine "
             "Bauchspeicheldrüse schüttet dann viel Insulin aus, um den Zucker in die "
             "Zellen zu bringen. Kurz gibt dir das einen Schub.",
             "Und dann fällt der Blutzucker <b>genauso schnell wieder ab</b>. Dein Körper "
             "deutet dieses Abfallen als Notlage, und dein Gehirn tut daraufhin "
             "biochemisch alles, um dich zum Essen zu bringen. Weil der nächste Griff "
             "wieder zu etwas Schnellem geht, folgt der nächste Absturz.",
             "Genau das ist dein Vormittagstief. Der Griff zum Kaffee und zum Süssen "
             "danach ist keine fehlende Disziplin — das ist dein Körper, der eine "
             "Notmeldung abarbeitet."]),

  dict(id="gipfeli", tag=2, titel="Warum ein Gipfeli nicht satt macht",
       kurz="Es liegt nicht an den Kalorien. Das Sättigungssignal fehlt einfach.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Bei eiweissarmen Mahlzeiten bleibt der Ausstoss der Sättigungsbotenstoffe "
             "weitgehend aus. Dein Körper meldet also gar nicht erst „genug“.",
             "Deshalb kannst du morgens zwei Gipfeli essen und um halb elf trotzdem "
             "Hunger haben, während dich ein Quark mit Beeren bis mittags trägt — bei "
             "ähnlicher Kalorienzahl.",
             "Das ist auch der Grund, warum „einfach weniger essen“ bei so vielen nicht "
             "funktioniert. Weniger von etwas, das nicht sättigt, hält nicht länger."]),

  dict(id="teller", tag=4, titel="Die Teller-Regel",
       kurz="Hinschauen statt rechnen. Zwei Regeln, und du brauchst keine App.",
       quelle="wie ich es selber mache",
       text=["<b>Frühstück:</b> ein Drittel Protein, ein Drittel Ballaststoffe, ein "
             "Drittel Kohlenhydrate. Kein Mensch isst morgens einen halben Teller "
             "Gemüse — deshalb gilt hier die Drittel-Regel.",
             "<b>Mittag und Abend:</b> die Hälfte Gemüse, ein Viertel Protein, ein "
             "Viertel Kohlenhydrate.",
             "Und der entscheidende Halbsatz dazu: <b>immer dann, wenn du dir deinen "
             "Teller selber zusammenstellen kannst.</b> Nicht im Restaurant, nicht beim "
             "Sonntagsbraten bei der Schwiegermutter. Es ist eine Richtschnur, kein "
             "Gesetz.",
             "🚨 <b>Stärkehaltiges Gemüse zählt als Kohlenhydrat</b>, nicht als Gemüse: "
             "Kartoffeln, Mais, Pastinaken, Süsskartoffeln, Kürbis und Erbsen. Das ist "
             "der häufigste Denkfehler an dieser Stelle."]),

  dict(id="dreissig-gramm", tag=3, titel="Warum 30 Gramm pro Mahlzeit",
       kurz="Unter einer gewissen Menge pro Mahlzeit passiert nichts. Verteilen schlägt Sammeln.",
       quelle="Grundlagen der Eiweissversorgung",
       text=["Dein Körper baut Muskeln nicht aus der Tagessumme, sondern aus dem, was bei "
             "<b>einer</b> Mahlzeit ankommt. Bleibt die Portion zu klein, springt der "
             "Aufbaureiz nicht an.",
             "Deshalb bringen dir 100 Gramm Eiweiss am Abend weniger als dreimal 30 über "
             "den Tag verteilt.",
             "Und genau deshalb fängt dieses Programm beim <b>Frühstück</b> an: Das ist "
             "bei fast jeder Frau die Mahlzeit mit dem wenigsten Eiweiss. Mittag und "
             "Abend sind meistens schon halbwegs in Ordnung."]),

  dict(id="mahlzeitenpause", tag=5, titel="Vier bis fünf Stunden — und was darüber liegt",
       kurz="Die Faustregel ist nicht „möglichst lange nichts“. Sie ist eine Spanne, und nach oben offen.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i> — und warum es bei uns anders liegt",
       text=["Über Esspausen wird viel Unsinn erzählt, und meistens läuft er darauf "
             "hinaus, dass länger immer besser sei. Das stimmt so nicht.",
             "Riedl nennt <b>vier, besser fünf Stunden</b> zwischen den Mahlzeiten als "
             "sinnvolle Pause. Gute Spanne — dein Blutzucker kommt zur Ruhe, und du "
             "isst nicht ständig nebenher.",
             "<b>Jetzt rechne deinen Tag durch.</b> Mittagessen um zwölf, Abendessen um "
             "halb sieben: Das sind <b>sechseinhalb Stunden</b>. Bei vielen wird es noch "
             "später, weil jemand vom Training kommt oder das Kind noch Hausaufgaben "
             "hat.",
             "Damit bist du nicht mehr in der guten Spanne, sondern deutlich darüber. Und "
             "das ist der Punkt, an dem dein Körper anfängt gegenzusteuern: Der "
             "Blutzucker fällt, und was dann kommt, sind <b>Stresshormone</b> — genau "
             "die, die du abends eigentlich runterfahren willst.",
             "<b>Warum das gerade bei uns ins Gewicht fällt:</b> Zu wenig essen ist für "
             "den Körper selbst schon Stress, unregelmässig essen auch. Und mit "
             "sinkendem Östrogen nimmt die Belastbarkeit für Stress zusätzlich ab. Da "
             "stapelt sich also etwas, was mit fünfundzwanzig noch niemandem aufgefallen "
             "wäre.",
             "<b>Die Regel, die daraus folgt, ist einfach:</b> Liegen zwischen zwei "
             "Mahlzeiten mehr als fünf Stunden, kommt eine Zwischenmahlzeit dazwischen. "
             "Liegen weniger als fünf dazwischen, brauchst du keine.",
             "Bei einem Mittagessen um zwölf und einem Abendessen um halb sieben heisst "
             "das: etwas gegen vier. Eine Zwischenmahlzeit mit <b>echtem Protein</b>, "
             "nicht ein Riegel — sonst ist es die nächste Zuckerwelle und du hast nichts "
             "gewonnen.",
             "Und genau deshalb steht in diesem Programm nirgends, dass du weniger essen "
             "sollst."]),

  dict(id="abgekuehlt", tag=7, titel="Der Trick mit der abgekühlten Stärke",
       kurz="Kartoffeln, Reis und Nudeln über Nacht kühlen. Kostet nichts, wirkt doppelt.",
       quelle="allgemein bekannt, völlig unterschätzt",
       text=["Wenn du Kartoffeln, Reis oder Nudeln kochst und sie danach <b>12 bis 24 "
             "Stunden im Kühlschrank</b> stehen lässt, verändert sich ein Teil der "
             "Stärke. Sie wird zu sogenannter resistenter Stärke.",
             "Die kann dein Dünndarm nicht mehr aufspalten. Zwei Dinge passieren dadurch: "
             "Dein Blutzucker steigt weniger stark an, und deine Darmbakterien bekommen "
             "Futter, das sonst nie bei ihnen ankommt.",
             "<b>Aufwärmen darfst du das Ganze trotzdem</b> — der Effekt bleibt weitgehend "
             "erhalten. Das ist der einfachste Kniff im ganzen Programm: Kartoffelsalat "
             "vom Vortag statt frischer Kartoffeln, Nudelsalat statt frischer Nudeln."]),

  dict(id="essig", tag=12, titel="Ein Löffel Essig vor dem Essen",
       kurz="Ein alter Hausmittel-Trick, der beim Blutzucker tatsächlich etwas tut.",
       quelle="Hausmittel, kein Wundermittel",
       text=["Ein Esslöffel Apfelessig in einem Glas Wasser vor einer "
             "kohlenhydratreichen Mahlzeit bremst, wie schnell der Zucker ins Blut geht.",
             "Das ersetzt kein Frühstück mit Protein und ist kein Freifahrtschein für "
             "alles andere. Aber es ist ein kleiner Hebel, der nichts kostet.",
             "🚨 <b>Wenn du Magenprobleme hast, lass es.</b> Und wer Medikamente nimmt, "
             "spricht das vorher in der Arztpraxis ab — es gibt Wechselwirkungen."]),

  dict(id="wasser", tag=6, titel="Das Glas am Morgen",
       kurz="Über Nacht verlierst du rund einen halben Liter, ohne etwas dafür zu tun.",
       quelle="warum das erste Glas den Unterschied macht",
       text=["Über die Nacht verliert dein Körper allein durchs Atmen und Schwitzen etwa "
             "einen <b>halben Liter</b> Wasser. Du wachst also mit einem Defizit auf, "
             "bevor der Tag überhaupt angefangen hat.",
             "Deshalb steht in diesem Programm ein grosses Glas Wasser direkt nach dem "
             "Aufstehen — noch vor dem Kaffee.",
             "Wenn du magst, mit einem Schuss Zitrone oder Apfelessig. Muss aber nicht. "
             "Das Wasser ist der Punkt, nicht das Zusatzding.",
             "<b>Nebenbei:</b> Wer mehr Eiweiss isst, hat oft mehr Durst. Das ist normal "
             "und liegt daran, dass beim Eiweissabbau Harnstoff entsteht, den deine Niere "
             "mit Wasser ausscheidet."]),
 ]),

 dict(regal="Eiweiss und Muskeln", ton="petrol", stuecke=[

  dict(id="sarkopenie", tag=8, titel="Was sich ab dreissig verändert",
       kurz="Bis zu ein Prozent Muskelmasse pro Jahr. Und einer der Gründe ist zu wenig Eiweiss.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Etwa ab einem Alter von 30 verlieren Menschen <b>pro Jahr bis zu 1 Prozent "
             "ihrer Muskelmasse</b>, und mit jedem weiteren Jahr geht es schneller.",
             "Drei Gründe werden dafür genannt: die Abnahme von Geschlechts- und "
             "Wachstumshormonen, Bewegungsmangel — und <b>zu wenig Eiweiss</b>.",
             "Deshalb gehören Krafttraining und Protein in diesem Programm zusammen und "
             "sind nicht zwei verschiedene Themen. Wer ab dreissig nichts tut, verliert "
             "jedes Jahr ein Prozent. Mit vierzig sind das zehn."]),

  dict(id="muskel-motor", tag=14, titel="Muskeln sind kein Schönheitsthema",
       kurz="Sie sind der Ort, an dem dein Körper Energie verbrennt. Auch auf dem Sofa.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Riedl vergleicht den Stoffwechsel mit einem Motor: je grösser, desto höher "
             "der Verbrauch — <b>auch im Leerlauf</b>.",
             "Mehr Muskelmasse heisst also, dass dein Körper auch dann mehr verbrennt, "
             "wenn du gar nichts tust. Und weniger Muskelmasse heisst das Gegenteil.",
             "Das erklärt eine Erfahrung, die viele Frauen ab Mitte dreissig machen: "
             "gleich viel gegessen wie immer, gleich viel bewegt wie immer, und trotzdem "
             "sitzt alles enger. Nicht weil du dich gehen lässt — sondern weil der Motor "
             "kleiner geworden ist.",
             "Die gute Nachricht daran: Daran kann man etwas ändern. Und zwar in jedem "
             "Alter."]),

  dict(id="anabole-resistenz", tag=11, titel="Warum es jetzt mehr braucht als früher",
       kurz="Dein Muskel reagiert weniger empfindlich auf Protein und Training. Das hat einen Namen.",
       quelle="Dr. Mariza Snyder, <i>Perimenopause-Power</i>",
       text=["Es gibt einen Fachbegriff für das, was viele Frauen ab Mitte dreissig "
             "spüren: <b>anabole Resistenz</b>. Das Muskelgewebe reagiert bei sinkenden "
             "Hormonspiegeln weniger empfindlich auf Proteinzufuhr und auf "
             "Trainingsreize.",
             "Im Klartext: Dasselbe Training und dasselbe Essen bringen weniger als mit "
             "fünfundzwanzig. Das ist keine Einbildung und kein Zeichen von Faulheit.",
             "Snyder nennt dazu eine deutliche Zahl: <b>allein während der Perimenopause "
             "kann man rund 10 Prozent der Muskelmasse verlieren.</b>",
             "Und daraus folgt genau das Gegenteil von dem, was die meisten machen. Nicht "
             "weniger essen und mehr Ausdauer — sondern <b>mehr Protein und Kraft</b>."]),

  dict(id="wieviel", tag=13, titel="Wie viel Eiweiss denn nun?",
       kurz="Die Empfehlungen gehen weit auseinander. Hier ist, warum — und was das für dich heisst.",
       quelle="drei Quellen, drei Antworten",
       text=["Wenn du danach suchst, findest du Zahlen zwischen 0,8 und 2,2 Gramm pro "
             "Kilogramm Körpergewicht. Das ist verwirrend, bis man sieht, dass die Frage "
             "unterschiedlich gemeint ist.",
             "<b>Dr. Matthias Riedl</b> nennt für gesunde Erwachsene <b>0,8 bis 1,0 g je "
             "kg</b>. Das ist die Menge, bei der nichts fehlt. Bei 65 kg wären das rund "
             "52 bis 65 Gramm am Tag.",
             "<b>Dr. Mariza Snyder</b> empfiehlt Frauen in der Perimenopause <b>2,2 g je "
             "kg Idealgewicht</b>, also bei einem Zielgewicht von 65 kg etwa 132 Gramm — "
             "gleichmässig auf Frühstück, Mittag und Abend verteilt. Ihr Ziel ist nicht "
             "„nichts fehlt“, sondern <b>Muskeln erhalten trotz anaboler Resistenz</b>.",
             "<b>Mein eigener Richtwert</b> liegt dazwischen: rund 30 Gramm pro "
             "Hauptmahlzeit. Das sind etwa 90 Gramm am Tag, und damit bin ich gut "
             "gefahren.",
             "🚨 <b>Was du daraus mitnimmst:</b> Es gibt keine eine richtige Zahl. Wenn du "
             "bisher bei 40 oder 50 Gramm warst, ist jeder Schritt nach oben ein "
             "Fortschritt. Fang bei den dreissig Gramm am Frühstück an — das ist die "
             "Mahlzeit, an der es fast immer fehlt.",
             "Und wenn du eine Nierenerkrankung hast oder Medikamente nimmst: Die Menge "
             "besprichst du mit deinem Arzt oder deiner Ärztin, nicht mit einem Buch."]),

  dict(id="ohne-shakes", tag=9, titel="Warum du dafür keinen Shake brauchst",
       kurz="Die Pulver-Industrie hat ein Interesse daran, dass du das anders siehst.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Riedl wird in seinem Buch ungewöhnlich deutlich: Die Verwirrung um den "
             "Eiweissbedarf stiften vor allem Unternehmen, die <b>industrielle "
             "Proteinpulver</b> und angereicherte Produkte herstellen. Sie argumentieren "
             "mit gesponserten, meist sehr kleinen Studien und lassen bezahlte Influencer "
             "dafür werben.",
             "Du kommst mit normalem Essen auf deine Menge. Skyr, Quark, Hüttenkäse, "
             "Eier, Linsen, Bohnen, Käse — alles in den Rezepten hier drin.",
             "<b>Deshalb gibt es in diesem Programm keine Shakes.</b> Nicht aus Prinzip, "
             "sondern weil du sie nicht brauchst."]),

  dict(id="quellen", tag=10, titel="Wo Eiweiss wirklich drinsteckt",
       kurz="Nicht nur Fleisch. Und nicht nur tierisch.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["Die üblichen Verdächtigen kennst du: Fleisch, Fisch, Eier, Milchprodukte. "
             "Was viele unterschätzen, sind die anderen.",
             "<b>Haferflocken</b> zum Beispiel gehören unter den Getreideprodukten zu den "
             "eiweissreichsten überhaupt — deshalb tauchen sie in den Frühstücken hier so "
             "oft auf.",
             "Dazu <b>Hülsenfrüchte</b>: Linsen, Kichererbsen, Bohnen, Edamame. Sie "
             "bringen Protein und Ballaststoffe in einem Lebensmittel, und das kann "
             "Fleisch nicht.",
             "<b>Zur biologischen Wertigkeit:</b> Tierisches Eiweiss kann dein Körper "
             "etwas besser verwerten als pflanzliches. Das Konzept wird aber gerne von "
             "denen ins Feld geführt, die Fleisch oder Pulver verkaufen. In der Praxis "
             "gleicht sich das aus, sobald du <b>kombinierst</b> — Getreide mit "
             "Hülsenfrüchten, Kartoffeln mit Ei, Bohnen mit Käse."]),

  dict(id="satt-effekte", tag=16, titel="Drei Nebenwirkungen von mehr Eiweiss",
       kurz="Du wirst satter, verbrennst beim Verdauen mehr, und bekommst mehr Durst.",
       quelle="Dr. Matthias Riedl, <i>Gamechanger Protein</i>",
       text=["<b>Du bist länger satt.</b> Eiweiss löst die Sättigungssignale aus, die bei "
             "einer Kohlenhydrat-Mahlzeit ausbleiben. Dadurch fallen längere Pausen "
             "zwischen den Mahlzeiten leichter.",
             "<b>Dein Körper verbrennt beim Verdauen mehr.</b> Um Nährstoffe "
             "aufzuspalten und zu verarbeiten, muss er Energie aufwenden — dabei entsteht "
             "Wärme. Bei Eiweiss ist dieser Aufwand deutlich höher als bei Fett oder "
             "Kohlenhydraten.",
             "<b>Du bekommst mehr Durst.</b> Beim Eiweissabbau entsteht Harnstoff, den "
             "die Niere mit Wasser ausscheidet. Das ist normal — trink einfach mehr."]),
 ]),

 dict(regal="Bewegen", ton="orange", stuecke=[

  dict(id="steigern", tag=9, titel="Wie du steigerst, ohne Trainerin",
       kurz="Im Training setzt du den Reiz. Gewachsen wird in den Ruhetagen.",
       quelle="das Prinzip hinter jedem Trainingsplan",
       text=["Im Training setzt du einen Reiz. Dein Muskel merkt, dass er dieser "
             "Belastung kaum standhalten konnte — und wächst <b>in den Ruhetagen</b>, "
             "damit er es beim nächsten Mal besser kann.",
             "Heisst: Es darf anstrengend sein. Wenn du mit demselben Gewicht dieselben "
             "Wiederholungen machst wie vor drei Monaten, passiert nichts mehr.",
             "<b>Vier Wege zu steigern</b> — und drei davon brauchen keine neuen Hanteln:",
             "① langsamere Ausführung · ② mehr Wiederholungen · ③ länger unter Spannung "
             "bleiben · ④ mehr Gewicht",
             "<b>Schreib auf, was du gemacht hast.</b> Drei Spalten reichen: Übung, "
             "Gewicht, Wiederholungen. Ohne Notiz erinnerst du dich falsch, und das "
             "Gefühl sagt bei Müdigkeit immer „dasselbe wie letztes Mal“."]),

  dict(id="alltagsbewegung", tag=8, titel="Warum 8000 Schritte mehr bringen als ein Kurs",
       kurz="Das Tägliche schlägt das Gelegentliche. Auch für Herz und Kreislauf.",
       quelle="warum die Schritte in diesem Programm stehen",
       text=["Alltagsbewegung ist für Herz und Kreislauf genauso wertvoll wie ein "
             "Cardio-Training — nur dass du sie jeden Tag hast und nicht zweimal die "
             "Woche.",
             "Dazu kommt das Tageslicht. Wer draussen geht, bringt nebenbei seinen "
             "Tag-Nacht-Rhythmus in Gang, und das zahlt abends auf den Schlaf ein.",
             "Kinder zu Fuss bringen oder abholen · das nächste Telefonat im Gehen · "
             "abends eine Runde ums Quartier. Das sind keine Sport-Termine, das ist "
             "derselbe Tag, nur anders gelaufen."]),

  dict(id="wann-egal", tag=10, titel="Es ist egal, wann du trainierst",
       kurz="Ich habe mich jahrelang mit 5:15 Uhr gestresst. Völlig umsonst.",
       quelle="aus Erfahrung, und das war eine teure",
       text=["Irgendwo steht immer, dass man morgens trainieren soll. Vor den Kindern, "
             "vor der Arbeit, auf nüchternen Magen.",
             "Ich habe das jahrelang versucht und mich damit vor allem gestresst. Und "
             "dabei übersehen, dass für das Ergebnis vor allem eins zählt: <b>dass es "
             "überhaupt stattfindet.</b>",
             "Dreimal die Woche eine halbe Stunde. Mittags, abends, in der Mittagspause, "
             "am Sonntagmorgen. Die Zeit, zu der du es <b>wirklich machst</b>, ist die "
             "richtige.",
             "Und wenn du wie ich in einer Phase mit wenig Schlaf bist: Um fünf Uhr "
             "aufzustehen, um zu trainieren, ist keine gute Idee. Schlaf ist der "
             "Baustein, aus dem die Erholung kommt."]),

  dict(id="pause", tag=12, titel="Muskelkater und Pausen",
       kurz="48 Stunden für dieselbe Muskelgruppe. Und was passiert, wenn du zwei Wochen aussetzt.",
       quelle="Grundregeln, die selten jemand sagt",
       text=["<b>Muskelkater:</b> Warte 48 Stunden, bevor dieselbe Muskelgruppe wieder "
             "dran ist. Erst reizen, wenn sie sich erholt hat — sonst arbeitest du gegen "
             "dich.",
             "<b>Längere Pause:</b> Ab etwa 14 Tagen ohne Training baut Muskulatur ab, "
             "weil dein Körper nicht erhält, was er nicht braucht. Das ist normal und "
             "kein Drama.",
             "Danach steigst du langsam wieder ein und reduzierst das Gewicht. Wer nach "
             "drei Wochen Ferien dort weitermacht, wo er aufgehört hat, holt sich "
             "meistens eine Zerrung statt eines Fortschritts."]),

  dict(id="essen-training", tag=17, titel="Essen rund ums Training",
       kurz="Nüchtern trainieren klingt nach mehr Wirkung. Ist es meistens nicht.",
       quelle="was bei mir funktioniert",
       text=["Wenn du vor dem Training seit fünf Stunden nichts gegessen hast, ist dein "
             "Körper bereits im Sparmodus — und dann kommt noch eine Belastung obendrauf.",
             "Bei mir funktioniert es so: eine Kleinigkeit ein bis zwei Stunden vorher, "
             "und danach eine richtige Mahlzeit mit Protein. Nicht kompliziert, nicht "
             "abgemessen.",
             "Wenn du morgens direkt nach dem Aufstehen trainierst und dich dabei gut "
             "fühlst, ist das auch in Ordnung. <b>Du bist der Massstab, nicht die "
             "Regel.</b>"]),
 ]),

 dict(regal="Schlaf und Stress", ton="blau", stuecke=[

  dict(id="cortisol", tag=15, titel="Warum du nachts um drei wach wirst",
       kurz="Cortisol und Melatonin hängen zusammen. Und zu wenig essen ist auch Stress.",
       quelle="Zusammenhänge, die selten jemand erklärt",
       text=["Cortisol ist dein Stresshormon, Melatonin dein Schlafhormon — und die "
             "beiden hängen zusammen. Ist zu viel vom einen da, kommt zu wenig vom "
             "anderen.",
             "Bei Dauerbelastung kann dein Körper in eine Art Überlebensmodus rutschen: "
             "Er hält fest, was er hat, und fährt nachts nicht mehr richtig runter.",
             "<b>Und das Unerwartete daran:</b> Zu wenig essen ist für deinen Körper "
             "ebenfalls Stress. Unregelmässig essen auch. Wer also gleichzeitig wenig "
             "isst, viel leistet und schlecht schläft, dreht an drei Schrauben in "
             "dieselbe Richtung.",
             "Deshalb steht in diesem Programm nirgends, dass du weniger essen sollst.",
             "🚨 Wenn du regelmässig schweissgebadet aufwachst oder seit Monaten nicht "
             "durchschläfst, gehört das abgeklärt. Das ist kein Fall für ein Ritual."]),

  dict(id="faden", tag=16, titel="Warum sich alles gegenseitig zieht",
       kurz="Essen, Schlaf und Bewegung sind nicht drei Tipps. Es ist eine Sache.",
       quelle="der rote Faden hinter den vier Bausteinen",
       text=["Was du isst — und ob regelmässig — wirkt über den Blutzucker und über "
             "Cortisol auf deinen Schlaf.",
             "Dein Schlaf entscheidet, wie gut du dich erholst.",
             "Deine Erholung entscheidet, was dein Krafttraining überhaupt bringt, denn "
             "Muskeln wachsen nicht im Training, sondern <b>in den Ruhetagen</b>.",
             "Und deine Muskeln entscheiden mit, wie stabil dein Blutzucker bleibt.",
             "<b>Das ist ein Kreis, kein Stapel.</b> Deshalb wirkt es so stark, wenn man "
             "an vier Stellen gleichzeitig ein bisschen etwas ändert — und so wenig, wenn "
             "man eine Sache perfekt macht und die anderen drei ignoriert."]),

  dict(id="abendritual", tag=16, titel="Dein Abend-Ritual",
       kurz="Dreissig Minuten ohne Handy, ein Duft, einmal durchatmen.",
       quelle="was bei mir funktioniert",
       text=["<b>Handy dreissig Minuten vor dem Bett weg.</b> Ich weiss, ich weiss.",
             "<b>Ein Öl, das dir guttut</b> — in der Lotion, auf den Handgelenken oder im "
             "Diffuser. Ich nehme da ehrlich gesagt, worauf ich gerade Lust habe. Es muss "
             "nichts Bestimmtes sein, es geht ums Ritual.",
             "<b>Kurz durchatmen</b> und den Tag hinter dir lassen.",
             "Der Sinn dahinter ist nicht der Duft an sich, sondern die Wiederholung. "
             "Dein Körper lernt: Wenn das kommt, ist der Tag vorbei.",
             "Melatonin ist übrigens das Hormon, das tagsüber ruht und abends mit der "
             "Dunkelheit aktiv wird. Helles Licht und ein Bildschirm kurz vorher arbeiten "
             "also gegen genau den Vorgang, auf den du wartest."]),

  dict(id="nicht-allein", tag=21, titel="Du bist damit nicht allein",
       kurz="Jeder zweite klagt über dasselbe. Das macht es nicht besser — aber es ordnet ein.",
       quelle="Prof. Dr. Elmar Wienecke, <i>Mikronährstoffe</i>",
       text=["Wienecke beschreibt, was in seinen Untersuchungen immer wieder auftaucht: "
             "<b>Jeder zweite</b> klagt über Befindlichkeitsstörungen — chronisch müde, "
             "häufige Infekte, Konzentrationsprobleme, Antriebsschwäche, Kopfschmerzen, "
             "Erschöpfung.",
             "Sein Punkt dabei ist keiner der Beruhigung, sondern einer der Ursache: Sehr "
             "häufig werde am Symptom gearbeitet und nicht an dem, was darunter liegt.",
             "Für dich heisst das vor allem eins: <b>Dass du erschöpft bist, ist kein "
             "Charakterfehler.</b> Es ist extrem verbreitet, und es hat Gründe, an denen "
             "man etwas ändern kann.",
             "🚨 Und es heisst auch: Anhaltende Erschöpfung gehört abgeklärt. "
             "Schilddrüse, Eisen, Vitamin D, Blutbild — das ersetzt kein Programm der "
             "Welt. Wohin ich dafür gehen würde, steht unter „Wenn du es wirklich wissen "
             "willst“."]),
 ]),

 dict(regal="Hormone ab Mitte dreissig", ton="orange", stuecke=[

  dict(id="perimenopause", tag=18, titel="Es fängt früher an, als alle denken",
       kurz="In der Regel zwischen 39 und 44. Die meisten rechnen frühestens mit fünfzig.",
       quelle="Dr. Mariza Snyder, <i>Perimenopause-Power</i>",
       text=["Die Perimenopause — also die Jahre <b>vor</b> den Wechseljahren — beginnt "
             "in der Regel im Alter zwischen <b>39 und 44 Jahren</b>. Bei manchen Frauen "
             "früher.",
             "Und das erklärt eine Menge. Es erklärt, warum sich etwas verändert, ohne "
             "dass irgendetwas kaputt wäre. Und warum das, was mit dreissig funktioniert "
             "hat, heute nicht mehr reicht.",
             "Snyder beschreibt die Lebensphase so, wie sie meistens aussieht: Frauen sind "
             "in dieser Zeit privat und beruflich stark eingespannt. Man sucht die "
             "Ursache dann bei sich — zu wenig Disziplin, zu wenig zusammengerissen.",
             "🚨 <b>Das hier ist Einordnung, keine Diagnose.</b> Was bei dir los ist, kann "
             "dir nur ein Arzt oder eine Ärztin sagen. Aber zu wissen, dass es diese Phase "
             "gibt, nimmt schon einiges an Druck raus."]),

  dict(id="was-passiert", tag=19, titel="Was dabei im Körper passiert",
       kurz="Drei Dinge hängen direkt an diesen Hormonen: Muskeln, Kopf und Blutzucker.",
       quelle="Dr. Mariza Snyder, <i>Perimenopause-Power</i>",
       text=["Ausgelöst wird die Perimenopause durch den Rückgang der Eibläschen und "
             "durch <b>Schwankungen</b> der Hormonspiegel — vor allem Östrogen und "
             "Progesteron. Schwankungen, nicht einfach ein gleichmässiges Absinken. "
             "Deshalb ist auch mal ein Monat völlig unauffällig und der nächste nicht.",
             "Und jetzt kommt der Teil, der dieses ganze Programm erklärt: An diesen "
             "Hormonen hängen unter anderem <b>Muskelwachstum, der Schutz deines Gehirns "
             "und dein Blutzuckerhaushalt</b>.",
             "Das sind genau die drei Dinge, um die es hier geht. Müdigkeit, "
             "Konzentration, Heisshunger, und dass Muskeln schwerer zu halten sind — das "
             "ist kein Zufall und keine Einbildung.",
             "Snyder macht auch auf ein sprachliches Detail aufmerksam: Wir reden von "
             "„Wechseljahrbeschwerden“, obwohl das meiste davon schon <b>vorher</b> "
             "passiert. Genauer wäre <b>perimenopausal</b> — und genau deshalb erkennt "
             "man sich mit vierzig nicht in dem wieder, was über Fünfzigjährige "
             "geschrieben wird."]),

  dict(id="abklaeren", tag=19, titel="Wenn du es wirklich wissen willst",
       kurz="Blutbild und Hormontest — und was du machst, wenn dir der Arzt das Blutbild ausredet.",
       quelle="aus meiner eigenen Erfahrung — keine medizinische Empfehlung",
       text=["Irgendwann kommt der Punkt, an dem Ausprobieren nicht mehr weiterhilft und "
             "du wissen willst, was eigentlich los ist. Bei mir war das so, und ich "
             "hätte mir gewünscht, dass mir das früher jemand sagt.",
             "<b>Zwei Dinge lohnen sich:</b> ein richtiges Blutbild und ein Hormontest. "
             "Zusammen, nicht einzeln — die beiden erklären sich gegenseitig.",
             "<b>Für den Hormontest</b> nehme ich <b>CENSA</b>, das Centrum für "
             "Speichelanalyse. Das läuft über Speichel statt Blut, du machst es zuhause "
             "und schickst die Probe ein; den Befund schreibt eine Fachperson. Es gibt "
             "verschiedene Profile — eines zum Beispiel mit Cortisol als Tagesprofil, "
             "DHEA, Estradiol, Estriol, Progesteron und Testosteron. Zu finden unter "
             "<b>censa.de</b>, in der Schweiz auch über florentia.ch.",
             "Gerade das <b>Cortisol-Tagesprofil</b> ist interessant, wenn du müde "
             "aufwachst und abends nicht runterkommst — eine einzelne Blutentnahme am "
             "Morgen zeigt davon nämlich nur einen einzigen Moment.",
             "<b>Für das Blutbild</b> gilt: Wenn dein Arzt oder deine Ärztin dafür offen "
             "ist, geh diesen Weg. Dann hast du jemanden, der die Werte einordnet, und die Kasse "
             "beteiligt sich meistens.",
             "<b>Meiner war es nicht.</b> Mein Hausarzt hat mir ein allgemeines Blutbild "
             "ausgeredet — sinngemäss, dafür gebe es keinen Anlass. Und aus ärztlicher Sicht "
             "stimmt das sogar: In einer Praxis wird normalerweise auf einen konkreten "
             "Verdacht hin getestet, und „ich bin ständig müde“ ist keiner. Nur stehst du "
             "danach genauso da wie vorher.",
             "Deshalb würde ich mich aus eigener Erfahrung sonst <b>direkt an ein Labor "
             "wenden</b> und das Blut dort testen lassen. Das geht schneller, und du "
             "bekommst die Werte, die dich interessieren, statt nur die, die gerade im "
             "Standardpaket stecken. Bezahlen musst du es dann allerdings selber.",
             "<b>Und wenn du nicht weisst, was du wo testen lassen sollst:</b> Such dir "
             "jemanden in der Naturheilkunde, dem du vertraust. Das "
             "ist genau die Person, die dir sagen kann, welche Werte bei deinen "
             "Beschwerden überhaupt Sinn ergeben — und die danach etwas mit dem Ergebnis "
             "anfangen kann.",
             "🚨 <b>Ein Test ist kein Programm und keine Behandlung.</b> Er sagt dir, wo "
             "du stehst. Was daraus folgt, besprichst du mit einer Fachperson — das kann "
             "ich dir hier nicht abnehmen und will es auch nicht.",
             "Und wenn etwas wirklich weh tut oder dir Angst macht: Dann ist das kein "
             "Fall für einen Selbsttest, sondern für einen Termin in der Arztpraxis."]),

  dict(id="regeneration", tag=20, titel="Warum du mehr Erholung brauchst als früher",
       kurz="Viel hilft hier nicht viel. Das ist keine Ausrede, das ist Physiologie.",
       quelle="Zusammenhänge, die selten jemand erklärt",
       text=["Mit sinkendem Östrogen erholt sich dein Körper langsamer, und die "
             "Belastbarkeit für Stress nimmt zusätzlich ab.",
             "Deshalb ist extremer Ausdauersport in dieser Phase für viele Frauen genau "
             "der falsche Weg: Er ist eine weitere Belastung obendrauf.",
             "<b>Krafttraining plus Alltagsbewegung plus echte Ruhetage</b> bringt hier "
             "mehr als sechsmal die Woche laufen gehen. Das ist einer der Gründe, warum "
             "in diesem Programm dreimal dreissig Minuten stehen und nicht mehr.",
             "Wenn du also eine Woche hast, in der du nach zwei Trainings platt bist: "
             "Dann waren zwei richtig."]),

  dict(id="zeichen", tag=20, titel="Woran man es merken kann",
       kurz="Nicht jede hat alles. Aber vieles davon wird selten zusammen gedacht.",
       quelle="Dr. Mariza Snyder, <i>Perimenopause-Power</i>",
       text=["Snyder sortiert die möglichen Zeichen in Gruppen — psychische, "
             "körperliche, den Zyklus betreffende, den Schlaf betreffende.",
             "Beim Schlaf fragt sie zum Beispiel: Wachst du mitten in der Nacht "
             "schweissgebadet auf? Fühlst du dich müde, obwohl du durchgeschlafen hast? "
             "Kannst du schlecht einschlafen?",
             "<b>Warum das nützlich ist:</b> Die meisten Frauen tragen diese Dinge "
             "einzeln mit sich herum und ordnen jedes für sich ein — der Schlaf ist "
             "halt schlecht, die Konzentration halt weg, die Laune halt kurz. Dass "
             "vieles davon zusammengehören könnte, denkt kaum jemand.",
             "🚨 <b>Das ist kein Test und keine Diagnose</b>, und du sollst dir jetzt "
             "nichts anlesen. Wenn dich mehrere dieser Punkte betreffen, ist das ein "
             "guter Grund für ein ärztliches Gespräch — mehr nicht und nicht "
             "weniger."]),
 ]),

 dict(regal="Der Darm", ton="petrol", stuecke=[

  dict(id="siebzig-prozent", tag=22, titel="70 Prozent sitzen im Darm",
       kurz="Dein Immunsystem wohnt zum grössten Teil dort, wo dein Essen vorbeikommt.",
       quelle="aus meiner Immunwoche",
       text=["In der Darmwand sitzt der grösste Teil deiner Immunzellen — rund <b>70 "
             "Prozent</b>. Und die Bakterien, die dort leben, bringen ihnen bei, wann sie "
             "reagieren sollen und wann nicht.",
             "Dazwischen steht ein einziger Stoff: Ballaststoffe kommen unverdaut im "
             "Dickdarm an, deine Bakterien vergären sie, und daraus entsteht etwas, das "
             "gleich zwei Dinge tut. Es ernährt deine Darmschleimhaut, und es beruhigt "
             "die Immunzellen, wenn sie überreagieren.",
             "Dein Teller ist deshalb keine Kosmetik. Er ist die Zutatenliste dafür."]),

  dict(id="bewohner", tag=23, titel="Wer da eigentlich wohnt",
       kurz="Zwischen 40 und 100 Billionen Mitbewohner. Und sie wollen gefüttert werden.",
       quelle="Prof. Dr. Elmar Wienecke, <i>Mikronährstoffe</i>",
       text=["Geschätzt <b>40 bis 100 Billionen</b> Kleinstlebewesen besiedeln einen "
             "Menschen — Bakterien, Viren, Pilze. Die meisten davon leben im "
             "Verdauungstrakt.",
             "Diese Bewohner wollen gefüttert werden. Bekommen sie nicht das nötige "
             "Futter, sterben die anspruchsvollen ab — und übrig bleiben die, die mit "
             "allem zufrieden sind. Genau die will man meistens nicht in der Überzahl "
             "haben.",
             "Gute und weniger gute gibt es immer. Worauf es ankommt, ist das "
             "<b>Gleichgewicht</b> und die <b>Artenvielfalt</b>.",
             "🚨 <b>Eine Antibiotikabehandlung trifft auch die guten.</b> Das heisst "
             "nicht, dass man sie nicht nehmen soll, wenn sie nötig ist — aber danach "
             "lohnt es sich besonders, auf Ballaststoffe und Vielfalt zu achten."]),

  dict(id="luecke", tag=23, titel="Die Lücke von zehn Gramm",
       kurz="Zwei Esslöffel Leinsamen und eine Portion Linsen. Mehr ist es nicht.",
       quelle="aus meiner Immunwoche",
       text=["Empfohlen wären <b>30 Gramm Ballaststoffe am Tag</b>. Frauen kommen im "
             "Schnitt auf 18 bis 23.",
             "Es fehlen also rund <b>10 Gramm</b> — jeden Tag. Und das klingt nach viel, "
             "bis man es umrechnet: zwei Esslöffel Leinsamen und eine Portion Linsen. "
             "Das war's.",
             "In vielen Frühstücken hier stecken die Leinsamen schon drin. Du musst dafür "
             "nichts extra tun."]),

  dict(id="vielfalt", tag=24, titel="Vielfalt schlägt Menge",
       kurz="30 verschiedene Pflanzen pro Woche. Basilikum zählt. Zimt zählt.",
       quelle="aus meiner Immunwoche",
       text=["Verschiedene Bakterien wollen verschiedenes Futter. Deshalb bringt dir "
             "<b>anderes</b> Gemüse mehr als <b>mehr</b> Gemüse.",
             "Die einfachste Regel dazu: <b>30 verschiedene Pflanzen pro Woche.</b> "
             "Kräuter, Gewürze, Nüsse und Samen zählen voll mit. Basilikum zählt. Zimt "
             "zählt. Kürbiskerne zählen.",
             "Wer glaubt, das nie zu schaffen, kommt mit einer Handvoll Kräutern und "
             "einem gemischten Salat schnell auf zwölf an einem einzigen Tag.",
             "<b>Und Farbe ist Bakterienfutter.</b> Von den Farbstoffen in Beeren, "
             "Rotkohl, Zwiebeln, Kräutern und Kakao werden nur etwa fünf bis zehn Prozent "
             "überhaupt aufgenommen. Der ganze Rest landet im Dickdarm und füttert dort "
             "die guten Bakterien."]),

  dict(id="fett-salat", tag=24, titel="Fettarmer Salat ist der teuerste Salat",
       kurz="Ohne Öl zahlst du fürs Gemüse und lässt das meiste ungenutzt liegen.",
       quelle="aus meiner Immunwoche",
       text=["Die orangen, roten und dunkelgrünen Farbstoffe im Gemüse kann dein Körper "
             "<b>nur mit Fett</b> aufnehmen. In einer Untersuchung nahmen Menschen aus "
             "demselben Salat ein Vielfaches davon auf, sobald Avocado oder Öl dabei war.",
             "Ein Esslöffel Olivenöl ist also kein Luxus. Das ist die Eintrittskarte.",
             "Dasselbe gilt für die Vitamine A, D, E und K — die kommen ohne Fett gar "
             "nicht erst in dein Blut."]),

  dict(id="blaehungen", tag=6, titel="Wenn es am Anfang zwickt",
       kurz="Blähungen beim Umstellen sind normal. Deine Darmflora braucht ein paar Tage.",
       quelle="was du wissen solltest, bevor du aufgibst",
       text=["Wenn du plötzlich mehr Ballaststoffe isst, reagiert dein Darm oft mit "
             "Blähungen oder Druck. <b>Das ist normal</b> — deine Darmflora braucht Zeit, "
             "sich auf das neue Futter einzustellen.",
             "Der häufigste Fehler an dieser Stelle ist, es als Unverträglichkeit zu "
             "deuten und wieder aufzuhören. Gib deinem Körper ein bis zwei Wochen.",
             "Wenn du sehr empfindlich bist: nicht alles auf einmal. Fang mit einem "
             "Löffel Leinsamen an statt mit zweien, und steigere langsam.",
             "🚨 <b>Bei starken oder anhaltenden Beschwerden gehört das abgeklärt</b> — "
             "nicht in eine Gruppe und nicht zu mir."]),
 ]),

 dict(regal="Die Nährstoffe", ton="petrol", stuecke=[

  # Tag 1 = schon vor dem Start offen (vor dem 10. zaehlt die Seite Tag 1).
  # Nur doTERRA-Produktblaetter + eine Studie. Nichts aus bezahlten Kursen.
  dict(id="einnahme", tag=1, titel="So nimmst du deine Nährstoffe",
       kurz="Alle drei zur selben Gelegenheit, jeden Tag. Mehr musst du dir nicht merken.",
       quelle="Angaben von doTERRA auf den Produktblättern · Tompkins u. a., "
              "<i>Beneficial Microbes</i>, 2011",
       text=["Das Wichtigste zuerst: Nimm alle drei zur selben Gelegenheit, jeden Tag. "
             "Das Frühstück bietet sich an, weil du dort ohnehin sitzt und weil auf dem "
             "Teller etwas Fett ist — das brauchen zwei der drei.",
             "<b>VMG+</b> — ein Sachet am Tag. Rühr es in 150 bis 240 ml kaltes Wasser "
             "oder ein anderes kaltes Getränk und schüttle es gut. Nicht in Tee oder "
             "Kaffee, nichts Heisses.",
             "<b>EO Mega+</b> — drei Softgels am Tag, zusammen mit einer Mahlzeit. "
             "So steht es auf dem Produktblatt.",
             "<b>PB Restore</b> — eine Kapsel am Tag, vor einer Mahlzeit. So steht es auf "
             "dem Produktblatt, und am einfachsten ist es gleich vor dem Frühstück. Die "
             "Kapsel hat zwei Schichten und ist so gebaut, dass die Kulturen den Magen "
             "überstehen. <b>Nüchtern musst du sie nicht nehmen.</b> Eine Laborstudie hat "
             "sogar gezeigt, dass "
             "Probiotika am besten durchkommen, wenn sie kurz vor oder zu Beginn einer "
             "Mahlzeit mit etwas Fett genommen werden, und am schlechtesten eine halbe "
             "Stunde danach.",
             "<b>Nach dem Öffnen gehört die Dose in den Kühlschrank.</b> Stell sie neben "
             "den Skyr, dann siehst du sie jeden Morgen.",
             "Manche merken in den ersten Tagen, dass die Verdauung etwas anders läuft, "
             "wenn Probiotika neu dazukommen. Wenn dich das beschäftigt, sag es mir in "
             "der Gruppe.",
             "<b>Bitte vorher mit deiner Ärztin sprechen</b>, wenn du schwanger bist oder "
             "stillst, Medikamente nimmst oder in Behandlung bist. Bei VMG+ nennt doTERRA "
             "ausdrücklich eine Schilddrüsenunterfunktion, Blutverdünner und Diabetes. "
             "EO Mega+ enthält Fisch.",
             "Und: Die Nährstoffe sind für dich. VMG+ ist laut doTERRA nicht für Kinder "
             "gedacht."]),

  dict(id="omega", tag=26, titel="Warum Leinöl allein nicht reicht",
       kurz="Dein Körper wandelt pflanzliches Omega 3 nur zu einem Bruchteil um.",
       quelle="Falk Hofmann, <i>OMEGA-3</i>",
       text=["Pflanzliches Omega 3 aus Leinöl oder Walnüssen heisst ALA. Damit dein "
             "Körper etwas damit anfangen kann, muss er es erst in zwei andere Formen "
             "umwandeln — EPA und DHA.",
             "Und das gelingt schlecht: Nur etwa <b>5 bis 10 Prozent</b> werden zu EPA, "
             "<b>unter 1 bis 4 Prozent</b> zu DHA.",
             "Die Folgerung im Buch: ALA ist notwendig, aber die direkte Zufuhr von EPA "
             "und DHA ist praktisch unerlässlich, wenn wirksame Mengen zusammenkommen "
             "sollen.",
             "Das ist der Grund, warum Omega 3 in deinem Paket ist — und nicht ein "
             "Fläschchen Leinöl."]),

  dict(id="verhaeltnis", tag=27, titel="Das Verhältnis, über das niemand redet",
       kurz="Nicht nur, wie viel Omega 3 du isst. Sondern wie viel Omega 6 daneben steht.",
       quelle="Falk Hofmann, <i>OMEGA-3</i>",
       text=["Omega 6 ist nicht der Böse — dein Körper braucht es. Entscheidend ist das "
             "<b>Verhältnis</b> zwischen Omega 6 und Omega 3.",
             "In der modernen Ernährung liegt dieses Verhältnis weit auf der Omega-6-"
             "Seite: Sonnenblumenöl, Distelöl, viele Fertigprodukte und die meisten "
             "Snacks bringen es reichlich mit.",
             "Ein ungünstiges Verhältnis kann nach den Angaben im Buch sogar die "
             "positiven Effekte einer Omega-3-Ergänzung abschwächen — unter anderem auf "
             "die Vielfalt im Darm.",
             "<b>Praktisch heisst das:</b> Olivenöl und Rapsöl statt Sonnenblumenöl, "
             "fetter Fisch einmal die Woche, und Omega 3 dazu. Nicht kompliziert."]),

  dict(id="bedarf", tag=27, titel="Was deinen Bedarf erhöht",
       kurz="Zeitmangel steht auf der Liste. Kaffee auch. Und unregelmässiges Essen.",
       quelle="Sascha Widemann, <i>Mikronährstoffe für ein stärkeres Immunsystem</i>",
       text=["Dass man Nährstoffe braucht, ist klar. Weniger bekannt ist, was den Bedarf "
             "nach oben treibt. Widemann listet unter anderem auf:",
             "<b>Zeitmangel · Nikotin, Alkohol und Kaffee · Medikamenteneinnahme · "
             "unregelmässiges Essen · körperliche Belastung im Beruf · Sport · einseitige "
             "Ernährung · Schwangerschaft · chronische Erkrankungen.</b>",
             "Lies die Liste nochmal langsam. Wie viele Punkte treffen auf dich zu?",
             "Bei den meisten Müttern mit Job sind es drei bis fünf gleichzeitig. Das "
             "heisst nicht automatisch, dass dir etwas fehlt — aber es erklärt, warum "
             "„ich ernähre mich doch normal“ nicht dasselbe ist wie „ich bin gut "
             "versorgt“.",
             "🚨 <b>Was dir tatsächlich fehlt, zeigt nur ein Bluttest.</b> Raten hilft "
             "hier niemandem."]),

  dict(id="magnesium", tag=28, titel="Magnesium und die unruhigen Nächte",
       kurz="Ein normaler Bluttest misst nicht das, worauf es hier ankommt.",
       quelle="Prof. Dr. Elmar Wienecke, <i>Mikronährstoffe</i>",
       text=["Wienecke berichtet aus seinen Untersuchungen: Über <b>85 Prozent</b> der "
             "untersuchten Personen zeigten deutliche Defizite in der <b>zellulären</b> "
             "Magnesiumkonzentration — und schliefen nachts sehr unruhig.",
             "In einer seiner Untersuchungen nahm eine Gruppe täglich abends <b>400 mg "
             "Magnesium, eine Stunde vor dem Schlafen</b>. Die Herzratenvariabilität "
             "verbesserte sich deutlich in Richtung Erholung.",
             "🚨 <b>„Zellulär“ ist der entscheidende Halbsatz.</b> Ein üblicher Bluttest "
             "misst Magnesium im Serum, nicht in der Zelle. Ein unauffälliger Wert sagt "
             "deshalb wenig darüber aus, wie es in deinen Zellen aussieht.",
             "Ob Magnesium für dich sinnvoll ist, besprichst du mit deinem Arzt oder einer "
             "Fachperson. Es ist nicht Teil deines Pakets, und ich verkaufe es dir hier "
             "auch nicht — es steht hier, weil du es wissen solltest."]),

  dict(id="paket", tag=28, titel="Was in deinem Paket steckt",
       kurz="Vier Bausteine, und warum es genau diese sind.",
       quelle="dein Nährstoff-Paket",
       text=["<b>Das Multi</b> deckt die Grundversorgung ab — die Basis, auf der alles "
             "andere aufbaut.",
             "<b>Das Probiotikum</b> arbeitet dort, wo rund 70 Prozent deiner Immunzellen "
             "sitzen.",
             "<b>Omega 3</b> liefert EPA und DHA direkt, weil dein Körper sie aus "
             "pflanzlichen Quellen kaum herstellt.",
             "<b>Der vierte Baustein</b> kommt dazu, wenn die Basis läuft — das "
             "besprechen wir im Start-Gespräch, weil es davon abhängt, wo du stehst.",
             "🚨 <b>Nimm sie immer zur selben Gelegenheit.</b> Nicht zu einer bestimmten "
             "Uhrzeit, sondern an eine bestehende Gewohnheit gekoppelt: zum Frühstück, "
             "zum Kaffee, beim Zähneputzen. Das ist der einzige Grund, warum Menschen "
             "Nahrungsergänzung durchhalten oder eben nicht."]),

  dict(id="was-nicht", tag=29, titel="Was die Nährstoffe nicht tun",
       kurz="Sie ersetzen kein Essen, keinen Schlaf und keine Abklärung.",
       quelle="damit du nicht falsch startest",
       text=["Sie machen aus einem Frühstück aus Weissbrot und Konfi kein gutes "
             "Frühstück. Der Teller kommt zuerst, das Paket kommt dazu.",
             "Sie wirken nicht über Nacht. Bei mir hat es gut ein Jahr gebraucht, bis "
             "alles zusammen da war — der erste spürbare Unterschied kam aber deutlich "
             "früher, und zwar aus dem Frühstück.",
             "🚨 <b>Und sie ersetzen keine Abklärung.</b> Blutwerte, Schilddrüse, Eisen, "
             "anhaltende Erschöpfung — das gehört abgeklärt, und zwar unabhängig davon, "
             "was du sonst noch machst."]),
 ]),

 dict(regal="Dranbleiben", ton="blau", stuecke=[

  dict(id="achtzig-zwanzig", tag=22, titel="Die 80 Prozent entscheiden",
       kurz="Was du regelmässig machst, zählt. Der Rest darf in Leichtigkeit stattfinden.",
       quelle="die wichtigste Regel von allen",
       text=["Entscheidend für das Ergebnis ist das, was du <b>im Alltag regelmässig</b> "
             "machst — nicht das, was du an einem einzelnen Tag machst.",
             "Die anderen zwanzig Prozent dürfen ganz bewusst in Leichtigkeit "
             "stattfinden. Ohne schlechtes Gewissen, ohne Druck.",
             "Du musst nicht ab sofort nie wieder Kuchen essen. Ein Geburtstag ist ein "
             "Geburtstag. Wer versucht, dreissig Tage lang alles richtig zu machen, hört "
             "am Tag neun auf — und wer achtzig Prozent macht, ist nach einem Jahr noch "
             "dabei."]),

  dict(id="dranbleiben", tag=11, titel="Wenn ein Tag danebengeht",
       kurz="Einer geht immer daneben. Entscheidend ist nur der nächste.",
       quelle="aus Erfahrung",
       text=["Es wird Tage geben, an denen nichts davon passiert. Ein krankes Kind, eine "
             "durchwachte Nacht, ein Tag, an dem alles gleichzeitig ist.",
             "<b>Das ist eingeplant.</b> Ein ausgelassener Tag macht nichts kaputt — was "
             "Programme kaputt macht, ist der Gedanke „jetzt ist es eh egal“ am Tag "
             "danach.",
             "Mein Vorschlag: Wenn ein Tag danebengeht, mach am nächsten Morgen nur eine "
             "Sache. Das Frühstück. Damit steht der Faden wieder, und der Rest kommt von "
             "allein zurück."]),

  dict(id="waage", tag=13, titel="Warum die Waage dich anlügt",
       kurz="Wenn Muskeln dazukommen und Fett weggeht, steht die Zahl still.",
       quelle="warum ich nicht nach Gewicht gehe",
       text=["Muskeln sind dichter als Fett. Wenn du also gleichzeitig Muskeln aufbaust "
             "und Fett abbaust, kann die Waage <b>wochenlang dieselbe Zahl zeigen</b>, "
             "während sich unter der Haut einiges verändert.",
             "Und stillstehende Zahlen sind der häufigste Grund, warum Menschen "
             "aufhören — nicht fehlende Motivation.",
             "<b>Vier Zahlen, alle vier Wochen, statt jeden Morgen eine:</b> Taille, "
             "Hüfte, dein schwerstes Gewicht bei einer Übung, und wie oft du in vier "
             "Wochen trainiert hast.",
             "Und dazu das, was du hier unten aufschreibst. Wie du aufwachst, wie der "
             "Nachmittag läuft, ob du um vier noch Geduld hast — das misst keine Waage, "
             "und genau das ist es, was du eigentlich wolltest."]),

  dict(id="was-anders", tag=25, titel="Die Frage am Tag 25",
       kurz="Nicht „hast du durchgehalten“. Sondern: Was ist anders geworden?",
       quelle="der wichtigste Moment der dreissig Tage",
       text=["Am Tag 25 frage ich dich nicht, ob du alles gemacht hast. Ich frage dich:",
             "<b>Was ist in den letzten Wochen anders geworden? Ganz egal wie klein.</b>",
             "Und weil einem das am Tag 25 selten spontan einfällt, gibt es hier das Feld "
             "„Was ist dir heute aufgefallen?“. Alles, was du dort einträgst, sammelt "
             "sich darunter — auch Kleinigkeiten. Dass du die Treppe genommen hast. Dass "
             "du um vier noch Geduld hattest. Dass die Hose anders sitzt.",
             "Am Tag 25 liest du das zusammen durch. Das ist eindrücklicher als jede "
             "Waage."]),

  dict(id="danach", tag=30, titel="Was bleibt, wenn es vorbei ist",
       kurz="Die Rezepte, das Wissen, und eine Erfahrung, die dir niemand mehr nimmt.",
       quelle="zum Schluss",
       text=["Du hast dreissig Tage lang vier Sachen gemacht, während der Alltag "
             "weiterlief. Mit Kindern, mit Job, mit allem, was dazwischenkam.",
             "Was du behältst, egal wie es weitergeht: <b>die Rezepte</b>, <b>diese "
             "Bibliothek</b>, und die Erfahrung, wie sich ein Vormittag ohne Loch "
             "anfühlt. Das ist kein kleines Ding — bevor man es einmal gespürt hat, hält "
             "man es nämlich für normal, dass man um halb zehn einbricht.",
             "Und wenn du magst, machen wir weiter. Aber das entscheidest du, wenn du "
             "deine Einträge gelesen hast — nicht vorher."]),
 ]),
]
