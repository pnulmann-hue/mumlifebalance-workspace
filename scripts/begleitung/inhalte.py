# -*- coding: utf-8 -*-
"""Die Inhalte der Begleit-Seite — getrennt vom Bauskript, damit Texte ohne
Code-Aenderung angepasst werden koennen.

🚨 **Nur gruenes Material.** Patricias eigene Rezepte, ihr eigener Plan, und Fakten
aus ihren Buechern mit Quellenangabe. Nichts aus den bezahlten Coachings — die Seite
geht an Kundinnen. Sachverhalte (Blutzucker, Ballaststoffe, resistente Staerke) sind
Allgemeinwissen und hier in eigenen Worten geschrieben; fremde Formulierungen,
Schaubilder und Gliederungen bleiben draussen.

🚨 **Keine Heilversprechen.** Nichts heilt, lindert oder behandelt. Erlaubt ist
„bei mir war das so" und die Einordnung, dass Abklaerungen zur Aerztin gehoeren.
"""

WOCHEN = [
    dict(nr=1, tage="Tag 1–7", titel="Essen", ton="petrol",
         ziel="Morgens so essen, dass du mittags nicht einbrichst. Mehr nicht.",
         text=["Auf jedem Teller alle drei: Protein, Ballaststoffe, Kohlenhydrate. "
               "Kein Rechnen, kein Zählen — Teller anschauen, sind alle drei drauf?",
               "Jeden Morgen eines der Frühstücke. Und die Nährstoffe dazu, immer zur "
               "selben Gelegenheit, damit es nicht vergessen geht."],
         merkst="Meistens schon in der ersten Woche, dass der Vormittag anders läuft. "
                "Der Nachmittag braucht länger.",
         lies=["achterbahn", "gipfeli", "dreissig-gramm"]),
    dict(nr=2, tage="Tag 8–14", titel="Bewegen", ton="orange",
         ziel="8000 Schritte am Tag, und dreimal die Woche eine halbe Stunde Kraft.",
         text=["Die Schritte sind das Tägliche, das Krafttraining der Aufbau.",
               "Und gleich die Entlastung dazu: <b>Es ist egal, wann.</b> Nicht um 5:15, "
               "nicht vor den Kindern — mittags, abends, in der Mittagspause. Hauptsache "
               "dreimal.",
               "Schritte sammelst du im Alltag: Kinder zu Fuss bringen, telefonieren im "
               "Gehen, eine Runde nach dem Abendessen. Den ersten Krafttermin schreibst "
               "du in den Kalender — als Termin, nicht als Vorsatz."],
         merkst="Dass die Schritte leichter zusammenkommen, als du denkst. Und dass der "
                "erste Krafttermin der schwerste ist.",
         lies=["sarkopenie", "steigern", "alltagsbewegung"]),
    dict(nr=3, tage="Tag 15–21", titel="Schlafen", ton="blau",
         ziel="Abends runterfahren. Und verstehen, was da eigentlich passiert.",
         text=["Handy dreissig Minuten vor dem Bett weg. Etwas, das den Tag beendet — "
               "bei mir ein Öl in der Lotion oder im Diffuser, es geht ums Ritual und "
               "nicht ums Produkt. Kurz durchatmen.",
               "Und jetzt, wo du zwei Wochen dabei bist und den ersten Unterschied "
               "gespürt hast, reden wir darüber, warum das alles zusammenhängt. Diese "
               "Woche gehört der Bibliothek — fang bei „Warum sich alles gegenseitig "
               "zieht“ an."],
         merkst="Die meisten merken in dieser Woche zum ersten Mal etwas am Schlaf.",
         lies=["cortisol", "faden", "perimenopause"]),
    dict(nr=4, tage="Tag 22–30", titel="Zusammensetzen", ton="petrol",
         ziel="Aus vier Einzelteilen wird eine Routine.",
         text=["Alles läuft jetzt parallel, kein neues Thema mehr.",
               "Am Ende soll sich dein Tag anders anfühlen und nicht wie ein Programm, "
               "das du durchziehst."],
         merkst="Am Tag 25 frage ich dich: Was ist anders geworden in den letzten Wochen? "
                "Ganz egal wie klein. Fang jetzt schon an, darauf zu achten.",
         lies=["dranbleiben", "achtzig-zwanzig"]),
]

# 🚨 `abWoche` ist der Kern der Fuehrung: In Woche 1 stehen DREI Haken da, nicht
# fuenf. Wer am Tag 1 eine Liste sieht, die sie schon jetzt nicht schafft, hat
# verloren, bevor sie angefangen hat. Am ersten Tag einer neuen Woche wird der
# neue Haken als „neu“ markiert.
TAGLICH = [
    dict(id="fruehstueck", abWoche=1, txt="Frühstück mit Protein",
         hint="eines aus der Rezeptbibliothek"),
    dict(id="naehrstoffe", abWoche=1, txt="Nährstoffe genommen",
         hint="immer zur selben Gelegenheit"),
    dict(id="wasser", abWoche=1, txt="Grosses Glas Wasser am Morgen",
         hint="gleich nach dem Aufstehen, vor dem Kaffee"),
    dict(id="schritte", abWoche=2, txt="8000 Schritte",
         hint="im Alltag gesammelt, nicht als Sporttermin"),
    dict(id="abend", abWoche=3, txt="Abends runtergefahren",
         hint="Handy weg, ein Duft, einmal durchatmen"),
]

KRAFT = dict(id="kraft", abWoche=2, txt="Krafttraining", ziel=3,
             hint="dreimal die Woche, egal wann")

ABSCHLUSS = dict(
    kopf="Wie es nach den dreissig Tagen weitergeht",
    text=["Am Tag 25 wird deine Dose langsam leer. Dann frage ich dich nicht, ob du "
          "weitermachen willst, sondern <b>was in den letzten Wochen anders geworden ist "
          "— ganz egal wie klein.</b>",
          "Wer darauf eine Antwort hat, weiss auch selber, ob sie weitermachen will. Und "
          "wer keine hat, für die war es nicht das Richtige. Das ist völlig in Ordnung, "
          "und ich nehme es niemandem übel.",
          "Was bleibt, gehört dir sowieso: die Frühstücke, das Wissen hier drin, und die "
          "Erfahrung, wie sich ein Vormittag ohne Loch anfühlt."])

# Patricias Telegram-Benutzername OHNE @. Leer = kein „An Patricia schicken"-Knopf.
# Link-Form t.me/<name>?text=… oeffnet ihren Chat mit dem Text schon im Eingabefeld.
TELEGRAM = "mumlifebalance_patricia"

HINWEIS = ("Ich bin weder Ärztin noch Ernährungsberaterin. Ich zeige dir, was bei "
           "mir und meiner Familie funktioniert hat, und ordne ein, was ich darüber "
           "gelesen habe. Alles, was nach Abklärung aussieht — Blutwerte, Schilddrüse, "
           "anhaltende Beschwerden — gehört in ärztliche Hände. Die Nährwerte in den "
           "Rezepten sind Richtwerte; je nach Marke schwanken Skyr, Quark und Knäckebrot "
           "spürbar.")


# ---------------------------------------------------------------------------
# Die Vorratsliste — was zu Hause stehen sollte
# ---------------------------------------------------------------------------

VORRAT = dict(
    kopf="Was bei dir zu Hause stehen sollte",
    einleitung=[
        "Das Meiste in diesem Programm scheitert nicht am Willen, sondern daran, dass "
        "um halb vier nichts Passendes da ist.",
        "Diese Liste ist deshalb keine Einkaufsliste für ein bestimmtes Rezept, sondern "
        "ein <b>Grundvorrat</b>. Wenn das da ist, kommst du mit fast allem aus der "
        "Rezeptbibliothek durch, ohne nochmal einkaufen zu gehen.",
        "Du musst nicht alles auf einmal kaufen. Fang mit dem an, was du sowieso magst.",
    ],
    gruppen=[
        dict(titel="Der Kühlschrank", abWoche=1, ton="petrol", hinweis="Das hier ist die Basis — ohne diese vier Sachen wird es schwierig.",
             zeilen=[
                 ("Skyr oder Magerquark", "grosse Packung, hält lange — das Rückgrat von Frühstück und Znüni"),
                 ("Hüttenkäse", "zwei Becher; ersetzt Sauce, Aufstrich und halben Snack"),
                 ("Eier", "zwölf bis achtzehn. Hart gekocht sind sie eine Woche haltbar"),
                 ("Halbhartkäse am Stück", "zum Würfeln, für Salat und Snacks"),
                 ("Frischkäse", "für die, die Hüttenkäse nicht mögen"),
                 ("Milch", "für Porridge und Overnight Oats"),
             ]),
        dict(titel="Proteinquellen zum Kochen", abWoche=1, ton="orange", hinweis="Einmal einkaufen, portionsweise einfrieren — dann hast du immer etwas.",
             zeilen=[
                 ("Pouletbrust", "geht in fast jedes Mittagessen"),
                 ("Hackfleisch", "die Grundform, die immer funktioniert"),
                 ("Lachsfilet", "einmal die Woche reicht — bringt EPA und DHA direkt"),
                 ("Thunfisch in Dosen", "für den Tag, an dem nichts geplant war"),
                 ("Feta oder Mozzarella", "macht aus Gemüse eine Mahlzeit"),
             ]),
        dict(titel="Der Vorratsschrank", abWoche=2, ton="petrol", hinweis="Alles lange haltbar. Das ist dein Netz für die Tage, an denen der Kühlschrank leer ist.",
             zeilen=[
                 ("Linsen — rot und braun", "Dosen für sofort, trocken für Suppe und Bolognese"),
                 ("Kichererbsen in Dosen", "drei bis vier; Curry, Salat, Hummus"),
                 ("Weisse Bohnen in Dosen", "für den Zehn-Minuten-Salat"),
                 ("Haferflocken", "grosse Packung"),
                 ("Leinsamen — geschrotet", "zwei Esslöffel am Tag schliessen deine Ballaststoff-Lücke"),
                 ("Quinoa", "mehr Protein als Reis, gleiche Kochzeit"),
                 ("Reis und Vollkornnudeln", "Basis, und am Vortag gekocht wird daraus resistente Stärke"),
                 ("Vollkornbrot und Knäckebrot", "Knäckebrot hält monatelang"),
                 ("Nussmischung", "in kleine Dosen portionieren, sonst ist die Packung am Mittwoch leer"),
                 ("Dosentomaten", "vier Stück, für alles mit Sauce"),
                 ("Kokosmilch", "zwei, für Curry"),
                 ("Olivenöl", "kein Sparposten — ohne Fett nimmst du die Farbstoffe aus dem Gemüse kaum auf"),
                 ("Apfelessig", "ein Esslöffel im Wasser vor kohlenhydratreichen Mahlzeiten"),
             ]),
        dict(titel="Gemüse und Früchte", abWoche=2, ton="petrol", hinweis="Ziel sind 30 verschiedene Pflanzen pro Woche. Kräuter und Gewürze zählen voll mit.",
             zeilen=[
                 ("Rüebli, Gurke, Peperoni", "die Rohkost-Basis — sonntags schneiden, in Wasser lagern"),
                 ("Zucchetti, Broccoli, Tomaten", "für Pfanne und Blech"),
                 ("Salat", "ein Kopf hält eine Woche"),
                 ("Zwiebeln und Knoblauch", "Grundlage von fast allem"),
                 ("Äpfel", "der Snack, der immer geht — mit Nüssen zusammen"),
                 ("Beeren, auch tiefgekühlt", "für Skyr und Porridge; gefroren sind sie günstiger"),
                 ("Frische Kräuter", "Petersilie, Schnittlauch, Basilikum — jedes zählt als eigene Pflanze"),
             ]),
        dict(titel="Tiefkühler", abWoche=3, ton="blau", hinweis="Dein Netz für die Tage, an denen gar nichts geht.",
             zeilen=[
                 ("Edamame", "sechs Minuten, elf Gramm Protein, fertig"),
                 ("Beeren", "direkt in den Skyr, taut bis zum Znüni auf"),
                 ("Spinat", "für Omelett und Rührei"),
                 ("Portionierte Suppe", "was du doppelt gekocht hast"),
             ]),
    ],
    schluss=["🚨 <b>Kauf nicht alles auf einmal.</b> Nimm beim nächsten Einkauf die erste "
             "Gruppe mit und ergänze dann jede Woche eine. Ein voller Schrank, aus dem du "
             "nichts benutzt, hilft niemandem.",
             "Und wenn du eine Sache zuerst kaufst: <b>Skyr, Eier und geschrotete "
             "Leinsamen.</b> Damit stehen Frühstück, Znüni und deine Ballaststoffe."])


# ---------------------------------------------------------------------------
# Protein-Tabelle — wie viel steckt wo drin
# ---------------------------------------------------------------------------
# 🚨 Richtwerte, keine Messwerte. Je nach Marke schwanken vor allem Skyr, Quark,
# Huettenkaese und Knaeckebrot spuerbar — das steht auch so auf der Seite.
# 🚨 Roh oder gekocht ist bei Huelsenfruechten und Getreide ein Faktor von rund
# drei. Wer das verwechselt, rechnet sich um das Dreifache reich.

PROTEIN = dict(
    kopf="Wie viel Protein steckt wo drin?",
    einleitung="Alles je 100 Gramm, dazu eine übliche Portion. Damit kannst du jedes "
               "Rezept umbauen und trotzdem auf deine Menge kommen.",
    gruppen=[
        dict(titel="Milchprodukte", zeilen=[
            ("Magerquark", 12, "200 g", 24),
            ("Skyr", 11, "180 g", 20),
            ("Hüttenkäse", 13, "130 g", 17),
            ("Griechischer Joghurt, mager", 9, "180 g", 16),
            ("Naturjoghurt", 4, "180 g", 7),
            ("Milch", 3, "200 ml", 7),
            ("Frischkäse", 6, "60 g", 4),
        ]),
        dict(titel="Käse", zeilen=[
            ("Parmesan", 33, "30 g", 10),
            ("Halbhartkäse (Gruyère, Emmentaler)", 28, "60 g", 17),
            ("Halloumi", 22, "120 g", 26),
            ("Mozzarella", 18, "120 g", 22),
            ("Feta", 14, "80 g", 11),
        ]),
        dict(titel="Ei, Fleisch, Fisch", zeilen=[
            ("Ei", 13, "2 Stück (110 g)", 14),
            ("Pouletbrust, roh", 23, "150 g", 35),
            ("Hackfleisch Rind, roh", 20, "150 g", 30),
            ("Lachsfilet, roh", 20, "150 g", 30),
            ("Thunfisch aus der Dose, abgetropft", 25, "1 Dose (110 g)", 28),
            ("Räucherlachs", 20, "60 g", 12),
        ]),
        dict(titel="Hülsenfrüchte", zeilen=[
            ("Linsen, roh", 24, "80 g", 19),
            ("Linsen, gekocht oder aus der Dose", 9, "150 g", 14),
            ("Kichererbsen aus der Dose", 7, "150 g", 11),
            ("Weisse Bohnen aus der Dose", 7, "150 g", 11),
            ("Edamame", 11, "100 g", 11),
            ("Tofu", 13, "130 g", 17),
            ("Hummus", 7, "100 g", 7),
        ]),
        dict(titel="Getreide, Kerne, Nüsse", zeilen=[
            ("Haferflocken", 13, "60 g", 8),
            ("Quinoa, roh", 14, "60 g", 8),
            ("Vollkornbrot", 8, "1 Scheibe (50 g)", 4),
            ("Knäckebrot", 10, "2 Stück (20 g)", 2),
            ("Kürbiskerne", 30, "1 EL (10 g)", 3),
            ("Mandeln und Nüsse", 21, "25 g", 5),
            ("Leinsamen, geschrotet", 24, "2 EL (20 g)", 5),
            ("Erdnussmus ohne Zucker", 25, "1 EL (15 g)", 4),
        ]),
    ],
    schluss=["🚨 <b>Roh oder gekocht macht bei Linsen, Reis, Nudeln und Quinoa rund das "
             "Dreifache aus</b> — sie ziehen beim Kochen Wasser. 80 g rohe Linsen und "
             "80 g gekochte Linsen sind zwei völlig verschiedene Mengen. In den Rezepten "
             "steht deshalb immer dabei, was gemeint ist.",
             "Und ein Blick auf die Tabelle erklärt, warum das Frühstück der Hebel ist: "
             "Brot mit Konfi liegt bei vier bis fünf Gramm. Derselbe Teller mit 200 g "
             "Magerquark dazu liegt bei fast dreissig."])


# ---------------------------------------------------------------------------
# Ein- und Mehrzahl fuer den Portionsrechner
# ---------------------------------------------------------------------------
# 🚨 Aus den echten Rezepten gezogen, nicht geraten — „1 Äpfel" und „2 Dose
# Tomaten" sind sonst das Erste, was auffaellt. Schweizer Woerter wie Zucchetti,
# Peperoni und Rüebli haben dieselbe Form in beiden Zahlen und stehen bewusst
# NICHT in der Tabelle.
MENGENWORT = {
    "Eier": "Ei", "Dosen": "Dose", "Gurken": "Gurke", "Scheiben": "Scheibe",
    "Äpfel": "Apfel", "Avocados": "Avocado", "Zwiebeln": "Zwiebel",
    "Fladenbrote": "Fladenbrot", "Bananen": "Banane", "Nektarinen": "Nektarine",
    "Muffins": "Muffin", "Tacos": "Taco", "Salatköpfe": "Salatkopf",
    "Vollkorn-Wraps": "Vollkorn-Wrap", "Wraps": "Wrap", "Kartoffeln": "Kartoffel",
    "Salatgurken": "Salatgurke",
}
