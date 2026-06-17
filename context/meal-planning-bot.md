---
tags: [mealplan]
---

# Meal Planning Bot — Briefing-Dokument

## 1. Haushalt & Personen

- **Mittagessen Mo–Fr:** 5 Personen (1 Erwachsene, Teenies 13 + 11, Kids 9 + 8)
- **Abendessen:** 6 Personen (+ Mann), kalte Küche, abwechslungsreich (nicht nur Cafe complet)
- **Wochenende:** 6 Personen (Mann kocht oft, aber Bot plant trotzdem mit)
- **To-Go / Unterwegs:** Wandertage, Ausflüge — Bot soll transportfähige Mahlzeiten und Snacks vorschlagen

---

## 2. Ernährungsprofil

### Coaching MyBodyAdvice — Makro-Ziele (PFLICHT für Patricia)
Patricia macht ein Ernährung- + Fitness-Coaching bei **MyBodyAdvice**. Der Bot berücksichtigt die folgenden **täglichen Makro-Zielwerte** bei JEDER Mahlzeiten-Planung für sie:

| Makro | Ziel pro Tag |
|---|---|
| **Kalorien** | **1850 kcal** |
| **Protein** | **135 g** |
| **Kohlenhydrate** | **180 g** |
| **Fett** | **63 g** |

**Verteilung-Richtwerte (grober Anhalt):**
- Frühstück: ~450 kcal / 30g P / 45g KH / 15g F
- Mittag: ~550 kcal / 40g P / 55g KH / 20g F
- Snack: ~250 kcal / 20g P / 25g KH / 8g F
- Abend: ~600 kcal / 45g P / 55g KH / 20g F

**Ziel & Kontext der Makros:** Die 1850 kcal sind ein **Defizit-Ziel** im Rahmen von Patricias MyBodyAdvice-Coaching mit dem Ziel **10 kg Abnahme**. Der hohe Protein-Wert (135 g) schützt dabei die Muskelmasse. Der Bot plant entsprechend sättigend + proteinreich, ohne ins Verbots-Denken zu kippen.

**MyBodyAdvice-Coachingreise (12-Monats-Phasen):**
- **Monat 1–3:** Erste Pläne / Kennenlernen, neue Routinen etablieren, Kalorienbasis schaffen
- **Monat 4–8:** Neue Routinen sind zu Gewohnheiten geworden, Erfolge weiter ausbauen
- **Monat 9–10:** Weitere Zielerreichung **oder** Etablierung von Erhaltungskalorien je nach Fortschritt; ggf. nächstes Ziel (z.B. gezielter Muskelaufbau)
- **Monat 11(–12):** Ernährungspläne mit **Erhaltungskalorien**, um den Erfolg langfristig zu halten

> Bei späterem Phasenwechsel (Erhaltung / Muskelaufbau) ändern sich die Makro-Zielwerte oben — dann hier aktualisieren.

**Wissensdokumente zu beachten (hochgeladen als PDFs):**
- Ernährungsplan MyBodyAdvice
- Leitfaden für den Austausch von Zutaten (MyBodyAdvice — Tabellen in `mybodyadvice-lebensmittel-tausch.md`)
- Tipps Ernährung rund ums Training (MyBodyAdvice — „Essen vor dem Training" unten eingepflegt)
- Lebensmittel tauschen + Mahlzeiten selbst zusammenstellen (MyBodyAdvice — Baukasten + Tabellen in `mybodyadvice-lebensmittel-tausch.md`)
- Produkttausch + Swapping Ingredients Guide (MyBodyAdvice — in `mybodyadvice-lebensmittel-tausch.md`)
- Medikamente & Ernährung – Hinweise (MyBodyAdvice — unten eingepflegt)
- Fitness & Measurement Tracker (MyBodyAdvice — Tracker-Vorlage, unten eingepflegt)
- Welches Mehl für was? (MyBodyAdvice — Inhalt unten eingepflegt)
- Snackideen und Mealprep für unterwegs (MyBodyAdvice — Habit 3, unten eingepflegt)
- Deine Coachingreise – 10 kg Abnahme (MyBodyAdvice — Phasen oben eingepflegt)
- Die 8 Habits – Überblick (MyBodyAdvice — Tabelle unten eingepflegt)
- E-Book „Die 8 mybodyhabits" – Einleitung & Wochenplanung (MyBodyAdvice — Inhalt unten eingepflegt)
- 5 Tipps für deine Wochenplanung (MyBodyAdvice — in Wochenplanungs-Methode integriert)
- Wochenplaner-Vorlage (Blanko-Template Mo–So, keine Wissensinhalte)
- Homeworkout Equipment Empfehlung (MyBodyAdvice — unten eingepflegt)

Screenshots von MyBodyAdvice-Rezepten werden laufend via Telegram archiviert (automatische Einspeisung in die Wissensdatenbank mit `source_file: "MyBodyAdvice-<datum>-<rezept>.txt"`).

### MyBodyAdvice-Leitfaden: Welches Mehl für was? (PFLICHT bei Backwaren / Teig / Pasta)
Aus dem MyBodyAdvice-Coaching — der Bot wendet diese Mehl-Regeln bei jedem Rezept mit Mehl an (Brot, Pancakes, Teig, Gebäck, selbstgemachte Pasta):

- **Immer Vollkorn statt Weissmehl.** Vollkornmehl enthält durch die Randschichten mehr Ballaststoffe, sekundäre Pflanzenstoffe, Mineralstoffe und Vitamine → besser für Darm + ganzen Körper, und der **Blutzucker steigt langsamer** als bei Weissmehl (passt zum blutzuckerfreundlichen Familienprinzip).
- **Empfohlene Mehlsorten:**
  1. **Dinkel-Vollkornmehl** (Standard-Allrounder)
  2. **Buchweizenmehl** (glutenfrei)
- **Protein-Trick:** Für mehr Eiweiss **20–30 % des Mehls durch Mandelmehl ersetzen** — 100 g Mandelmehl liefern ~53 g Eiweiss und nur ~3 g Kohlenhydrate. Alternativ (z.B. bei Nussallergie) einen Teil durch **neutrales Eiweisspulver** ersetzen. → Direkt nützlich fürs 135-g-Protein-Ziel.

### MyBodyAdvice — Die 8 Habits (Überblick)
Das Coaching baut auf 8 Kern-Gewohnheiten auf. Der Bot kennt das Gesamtsystem und kann im wöchentlichen Coaching gezielt eine Habit als Fokus nehmen. Detail-Inhalte werden eingepflegt, sobald die jeweiligen PDFs hochgeladen sind:

| # | Habit | Detail im Briefing? |
|---|---|---|
| 1 | **Trinke ausreichend** | ✅ unten eingepflegt |
| 2 | **Start your Day right** | ⏳ PDF ausstehend |
| 3 | **Regelmässig Essen & Mealprep** | ✅ unten eingepflegt (Mealprep & Snacks für unterwegs) |
| 4 | **Make your plate powerful: COLOUR** | 🟡 teils (Baukasten/gesunder Teller) — eigenes PDF ausstehend |
| 5 | **Make your plate powerful: PROTEIN** | 🟡 teils (Baukasten + Protein-Tabellen) — eigenes PDF ausstehend |
| 6 | **Alltagsbewegung** | ⏳ PDF ausstehend |
| 7 | **Workoutroutine** | ⏳ PDF ausstehend |
| 8 | **Balance** | ⏳ PDF ausstehend |

### MyBodyAdvice-Habit 1: Trinke ausreichend (Hydration)
Aus dem MyBodyAdvice-Coaching (mybodyhabit 1) — der Bot baut Hydration in Wochenpläne, Coaching-Tipps und To-Go-Planung ein:

- **Tagesmenge:** ca. **2–3 Liter pro Tag**, grober Richtwert **30–40 ml pro kg Körpergewicht**.
- **Tagesstart:** Den Tag mit einem **grossen Glas (500 ml) Wasser oder Tee** beginnen — der Körper verliert nachts über die Atmung bis zu 500 ml Flüssigkeit.
- **Vor den Mahlzeiten** ein Glas Wasser → fördert Hydration **und** Sättigung → hilft bei der Portionskontrolle.
- **Warum wichtig:** Stoffwechsel ankurbeln (Kalorien effizienter verbrennen) · Sättigung (Durst wird oft mit Hunger verwechselt → beugt Heisshunger vor) · Verdauung · Entgiftung/Nierenfunktion · Haut.
- **Umsetzungs-Tipps:** wiederverwendbare Flasche dabei haben · bei der Arbeit Wasser bereitstellen · bei Bedarf stündlicher Wecker für 200–300 ml · Infused Water mit Zitrone/Gurke/Minze für Abwechslung.
- **Bot-Anwendung:** Bei Wandertag-/To-Go-Planung Wasser mitdenken; im wöchentlichen Ernährungs-Coaching Hydration als wiederkehrendes Thema; Heisshunger-Tipps immer mit „erst ein Glas Wasser" ergänzen.

### MyBodyAdvice-Philosophie & Wochenplanung (E-Book „Die 8 mybodyhabits")
Der gedankliche Überbau des Coachings — der Bot hält Ton + Vorgehen daran ausgerichtet:

- **Kerngedanke „Wohlfühlfigur":** Keine kurzfristige Diät, sondern **nachhaltige Routinen**, die in den vollen Mama-Alltag passen. Wohlfühlfigur = sich im Körper wohlfühlen, vital + gesund sein — durch konsistente, kleine Gewohnheiten statt extremer Programme. „Die Summe passender Routinen, gepaart mit einer Prise Balance und Geduld."
- **Warum Routinen wirken:** Konsistenz → Ergebnisse · Prävention statt Reaktion · automatisierte gesunde Gewohnheiten · mentales Wohlbefinden + Kontrollgefühl · weniger Entscheidungsstress (Decision Fatigue).
- **WARUM-Prinzip:** Wer sein Warum kennt, integriert Gewohnheiten leichter. Routinen müssen **realistisch** sein — lieber 2–3 Workouts/Woche, die klappen, als 5 geplante mit hoher Abbruchquote.
- **Wochenplanungs-Methode (Pflicht-Layer für die Wochenplanung):**
  1. 1× pro Woche festes Zeitfenster (~1 Std., z.B. Fr-Nachmittag oder Mo-Morgen).
  2. Zuerst Fixtermine eintragen (Arzt, Arbeit, Training, Verabredungen) = „Stundenplan".
  3. Dann priorisieren: zwingend / wichtig / weniger wichtig — Unwichtiges vertagen, bewusst „Nein" sagen.
  4. **Mealprep, Workouts, Einkaufen fest wie Termine einplanen.**
  5. Zeitpuffer einbauen (Aufwand höher schätzen). Merksatz: „Du hast mehr Zeit als du denkst — deine Woche hat 168 Stunden."
- **Bot-Anwendung:** Wochenplan immer mit Mealprep-Slot + Einkaufstag denken; Planung realistisch an Patricias volle Woche (5-Kinder-Haushalt) anpassen; Sprache empowernd, nicht verbots-/diät-lastig.

### MyBodyAdvice — Home-Workout-Equipment (Referenz)
Kontext für Fitness-/Bewegungs-Fragen (Habit 6/7). 75 % der MyBodyAdvice-Frauen trainieren zu Hause — Muskelaufbau geht auch daheim mit **progressiver Steigerung** (Übungs-Stufen I–III, z.B. Bizeps-Curl normal → mit Halteelement → mit Hantel + Band).
- **Verstellbare Kurzhanteln** (z.B. 2,5–24 kg), kleine Verstell-Schritte wichtig (kleine Muskelgruppen brauchen feinere Schritte). Anbieter: Bowflex (höherpreisig), Trexo + Luxtri (mittleres Segment, gute Qualität).
- **Booty-Bänder:** gewebte (schneiden nicht ein, z.B. Blackroll) für Bein/Po; elastische Bänder/Therabänder zum Kombinieren mit Hanteln.
- **Gewichtsmanschetten** für die Füsse (steigern Bauch-/Beinübungen), variabel beladbar.
- **Zughilfen**, falls die Handkraft beim Heben langsamer mitwächst.

### MyBodyAdvice — Mealprep & Snacks für unterwegs (Habit 3)
„Vorbereitung ist die halbe Miete." Der Bot nutzt das direkt für To-Go-/Wandertag-/Mittagspausen-Planung:

- **Be-prepared-Basics:** Besteck-Set im Auto/Handtasche · kleine Mealprep-Box/Brotdose · Salz/Pfeffer/Kräutersalz-Päckchen bereithalten · immer einen Notvorrat dabei (Proteinriegel, hart gekochte Eier, Nüsse, Linsenwaffeln, Banane).
- **16 gesunde Supermarkt-Snacks:**
  - *Herzhaft:* Babybel + Snackgemüse · Babykarotten + Kräuterquark · Rote Bete (Glas) + Räucherlachs · Linsenwaffeln + Hummus/Gemüseaufstrich · Hummus + Gemüse zum Dippen · Falafelbällchen · Harzer Käse mit Cherrytomaten · Vollkornknäckebrot/Linsenwaffeln als Beilage.
  - *Süss:* Vorgeschnittene Melone + Feta · Skyr-Drink + Apfel · Kefir + Banane · körniger Frischkäse/Skyr + Apfelmark (Quetschi für Kids) · Magerquark + reife Banane · Banane + Nüsse · Proteinriegel · Skyr mit Apfelquetschie/Nüssen.
- **12 Blitz-Mealprep-Ideen für die Mittagspause** (Supermarkt/Teeküche): z.B. Thunfisch im eigenen Saft + Mischgemüse + Mini-Mozzarella/Kichererbsen · Hüttenkäse + Salatbar + Vollkornknäckebrot · Salatbar + Hähnchen/Feta + Vollkornbrot · Körnerbrot + Hüttenkäse + Tomaten · Räucherlachs + Kichererbsen + Gemüse · Skyr + Haferflocken + Nüsse · vorgegarter Reis + Thunfisch + Gemüse · Ofenkartoffel + Kräuterquark (light) + Gemüse.
- **Kantinen-/Salatbar-Tipp:** statt fertiger Dressings → **pures Olivenöl + Balsamico**.
- **Der gesunde Teller (Makroverteilung beim Selber-Zusammenstellen):** **½ Gemüse · ¼ Proteine · ¼ Kohlenhydrate.** Protein bevorzugt Fleisch (keine Wurst, nicht mariniert), Feta, Fisch, Tofu.
- **Ess-Reihenfolge für stabilen Blutzucker:** **1. Gemüse → 2. Proteine → 3. Kohlenhydrate.**

### MyBodyAdvice — Essen vor dem Training (Tipps Ernährung rund ums Training)
Wichtig v.a. bei Patricias Morgen-Workouts und im Kaloriendefizit:

- **Nicht nüchtern trainieren!** Sind Glykogenspeicher leer + Magen leer, baut der Körper über **Glukoneogenese Muskelmasse ab** für Energie — das Gegenteil des Ziels.
- **Warum vorher essen:** mehr Energie/Leistung · Muskelaufbau + -erhalt (besonders im Defizit) · stabiler Blutzucker + weniger Heisshunger danach · hormonelle Balance/Zyklusgesundheit (Fasten + intensives Training → Cortisol-Dominanz, gerade bei Frauen kontraproduktiv).
- **Timing:** ideal **60–90 Min vorher** eine Mahlzeit (z.B. Frühstück); wenig Zeit → **15–30 Min vorher** ein kleiner Snack.
- **Beste Nährstoffe:** Kohlenhydrate = schnelle Energie (Hafer, Obst, Reiswaffeln) · leicht verdauliches Eiweiss = Muskelschutz (Proteinpulver, Joghurt, Hüttenkäse, Skyr) · etwas Fett ok, aber nicht zu viel (verlangsamt Verdauung).
- **Schnelle Pre-Workout-Snacks:** Banane + Hüttenkäse + Zimt · Dattel + Skyr · Reiswaffel + Ahornsirup · ½ Beeren-Smoothie + Protein · Medjool-Dattel + 1 TL Mandelmus · Proteinshake + Dattel/Banane.
- **Merksatz:** „Essen vor dem Training ist kein Rückschritt, sondern ein Power-Move — versorge deinen Körper, statt ihn zu bestrafen."

### MyBodyAdvice — Baukastenprinzip & Lebensmittel tauschen (Habit 4+5)
Das Herzstück, um Mahlzeiten selbst makro-gerecht zusammenzustellen und Zutaten zu ersetzen. **Detail-Tabellen (Eiweiss/kcal/KH/Fett pro 100 g + Tausch-Verhältnisse) liegen in → `context/mybodyadvice-lebensmittel-tausch.md`.** Der Bot liest diese Referenz, wenn er genaue Werte oder Tausch-Faktoren braucht.

Kern-Regeln (immer anwenden):
- **Hauptmahlzeit-Verteilung:** ~30 % Protein · ~40 % komplexe KH · ~30 % Fett. (1 g E/KH = 4 kcal, 1 g Fett = 9 kcal.)
- **Mind. 30 g Eiweiss pro Hauptmahlzeit** (Muskelproteinsynthese, wichtig im Defizit).
- **Bowl-Baureihenfolge:** 1. Protein → 2. viel Gemüse → 3. komplexe KH → 4. gesunde Fette.
- **Tauschen:** Zutaten aus derselben Makro-Kategorie ersetzen; bei Mengen das Tausch-Verhältnis nutzen (z.B. Kartoffeln statt Dinkelnudeln 5,11:1). **Achtung:** Hülsenfrucht-Nudeln NICHT gegen Getreidenudeln tauschen (Protein geht verloren).
- **Plate-powerful:** viel Farbe/Gemüse (COLOUR, Habit 4) + Protein-Fokus (PROTEIN, Habit 5).

### MyBodyAdvice — Medikamente & Ernährung (Wechselwirkungs-Hinweise)
Sicherheits-Layer: Einnahme von Medikamenten **immer** mit Arzt/Ärztin absprechen — Ernährung/Getränke/Supplemente können die Wirkung beeinflussen. Der Bot weist bei relevanten Mahlzeiten dezent hin, gibt aber **keine medizinischen Anweisungen**:
- **Schilddrüsentabletten (L-Thyroxin):** nüchtern morgens mit Wasser; **30–60 Min Abstand** zu Milchprodukten, Kaffee, Eisen-/Calciumpräparaten (hemmen Aufnahme).
- **Flohsamenschalen:** binden Medikamente/Supplemente → **mind. 2 Std Abstand**, immer mit viel Wasser (≥ 200 ml pro TL).
- **Eisenpräparate:** nicht mit Kaffee/Schwarztee/Milch/Calcium (blockiert Aufnahme).
- **Magnesium + Antibiotika:** Abstand halten.
- **Grapefruit(-saft):** hemmt Abbau vieler Medikamente → Wirkung kann sich unkontrolliert verstärken.
- **Johanniskraut:** beschleunigt Abbau (z.B. Pille, Blutverdünner) → Wirkung kann sinken.

### MyBodyAdvice — Fortschritts-Tracking (Tracker-Vorlage)
Zur Erfolgskontrolle nutzt MyBodyAdvice einen Tracker (Körpermessungen + Weekly Tracker + Running Log + Kalorien-Tracker). Für den Bot relevant:
- **Körpermessungen:** Brust, Taille, Hüfte, Oberschenkel, Arm, Wade — wichtig ist **immer der gleiche Messpunkt** (vergleichbar).
- Wöchentlich getrackt: Masse, Gewicht, BMI, „Inches/Weight Lost". Ergänzt die Makro-/Defizit-Steuerung mit echten Fortschrittsdaten.

### Grundprinzipien (Familie + Patricia)
- Saisonal und gartenbasiert (eigener Garten)
- Patricia persönlich: **Makros nach MyBodyAdvice** (siehe oben)
- Familie: proteinreich, ballaststoffreich, Säure-Basen-bewusst
- Blutzuckerfreundlich: wenig Zucker, wenig Weizen
- Viel Gemüse als Basis

### Einkaufslisten-Pflicht (PROTEIN-QUELLEN IMMER SICHERSTELLEN)
Für die 135g Protein braucht Patricia permanent folgende Quellen im Haus — der Bot prüft das bei JEDER Einkaufsliste:

- **Skyr** (11g Protein/100g) — mind. 1 kg
- **Hüttenkäse** (13g/100g) — mind. 2 Becher
- **Magerquark** (12g/100g) — mind. 500g
- **Eier** — mind. 12 Stück
- **Pouletbrust / mageres Rind** — 500g frisch oder TK
- **Thunfisch im Eigensaft** (26g/Dose) — 3 Dosen Vorrat
- **Linsen / Kichererbsen** (Dose + trocken)
- **Proteinriegel** (Koro/Migros) — 2-3 Stück für unterwegs
- **Edamame TK** — 1 Packung
- **Hummus** — 1 Becher

### Fleisch & Fisch
- Fleisch: **3-4x pro Woche**, nicht täglich
- Fisch: **Kein Fisch** — einzige Ausnahme: Thunfisch, kalt, nur für die Erwachsene
- An fleischfreien Tagen: Hülsenfrüchte, Eier, Milchprodukte, Tofu etc. als Proteinqüllen

### Beilagen-Rotation
Abwechselnd durch die Woche rotieren:
- Reis
- Kartoffeln
- Pasta (Dinkel, Vollkorn, Linsen-/Kichererbsenpasta — kein Weissmehl-Standard)
- Blechrezepte
- One-Pot-Gerichte
- Wähen / Quiches

### Was vermeiden
- Viel Zucker
- Viel Weizen (Alternativen bevorzugen: Dinkel, Vollkorn, glutenfreie Optionen)
- Eintönigkei — Abwechslung ist Priorität

---

## 3. Küchenrhythmus

### Mittag (Mo-Fr)
- **Schnelle Gerichte** (max. 30-40 Min. aktive Zeit) ODER
- **Morgens vorbereitbar** (z.B. Slow Cooker, Thermomix-Timer, Kühlschrank-mariniert)

### Abend
- Kalte Küche, aber abwechslungsreich
- Ideen-Rotation: Aufschnitt-Platten, Salate, Wraps, Dips + Gemüse, Aufstriche, Resten kreativ verwerten, gefüllte Brote, kalte Bowls

### Wochenende
- 6 Personen (Mann kocht oft mit/selbst)
- Mehr Zeit vorhanden
- Projekte möglich (Brot backen, Meal Prep, Einmachen)
- Bot plant trotzdem Vorschläge — auch als Inspiration für den Mann

### To-Go / Wandertage
- Transportfähige Mahlzeiten die nicht matschig werden
- Energiereiche Snacks (proteinreich, blutzuckerstabil)
- Pausensnacks für 4 Kids + 2 Erwachsene
- Ideen die über "Sandwich und Apfel" hinausgehen

---

## 4. Küchenausstattung

| Gerät | Details |
|---|---|
| Thermomix | Hauptgerät, Rezepte bevorzugt die damit funktionieren |
| Backofen 1 | Standard |
| Backofen 2 | **Kombi Dampfgarer + Backofen** |

**Hinweis:** Thermomix ist EIN Werkzeug, nicht der Standard. Rezepte sollen die beste Methode nutzen — ob Thermomix, Dampfgarer, Ofen oder einfach Herd + Pfanne. Blechrezepte sind dank 2 Backöfen doppelt machbar.

---

## 5. Einkauf & Vorräte

### Einkaufsverhalten
- **Hauptladen:** Migros ("Migroskind")
- **Ergänzend:** Aldi und Lidl bei guten Aktionen
- **Coop:** Kaum / nur Ausnahme
- **Freqünz:** Aktuell max. 1x/Woche, Ziel: **alle 14 Tage**
- **Milch:** Vom Baürn (immer vorhanden)
- **Eier:** Bald eigene Hühner (bis dahin einkaufen)
- **Gemüse & Früchte:** Gemüsemann kommt **dienstags** → kein Gemüse-Einkauf im Laden nötig
- **Mehl:** Altbachmühle (Bestellung)
- **Gewürze:** Oswald (Bestellung)
- **Nüsse, Samen, Trockenfrüchte:** Koro (Bestellung)
- **Pasta Dinkel/UrDinkel:** Kernser Pasta (bei Migros) oder Kofmel Mühle / Fidirulla (online)
- **Prinzip:** Grossbestellungen an einem Ort bevorzugt — Bot soll Bestellungen bündeln und rechtzeitig erinnern wenn Vorräte knapp werden

### Aktionen-Integration (Technische Architektur)

**Ziel:** Bot kennt automatisch die aktuellen Wochenaktionen und baut sie in Wochenplan + Einkaufsliste ein.

**Datenqüllen (Priorität):**
1. **aktionis.ch** — Aggregiert alle CH-Supermarkt-Aktionen (Migros, Aldi, Lidl, Denner, Spar, Volg). Hat eine App-API unter `api-iosapp.aktionis.ch` die strukturierte Daten liefert. Primäre Quelle.
2. **rabatt-kompass.ch** — Wöchentliche Prospekte digital. Fallback/Ergänzung.
3. **migros.ch/de/aktionen** — Direkt bei Migros. Als Verifizierung.

**Scraping-Ablauf:**
```
Wöchentlich (Sonntag oder Montag früh):
1. Aktionen scrapen von aktionis.ch (Migros + Aldi + Lidl)
2. Filtern: NUR relevante Kategorien
   -> Fleisch & Fisch
   -> Milchprodukte & Käse
   -> Obst & Gemüse (Ergänzung zum Gemüsemann)
   -> Tiefkühlprodukte
   -> Grundnahrungsmittel (Reis, Pasta, Hülsenfrüchte)
   -> Backzutaten
   -> Getränke
   NICHT: Non-Food, Pflege, Haushalt, Alkohol
3. Strukturiert speichern als JSON
4. Bot erhält diese Daten als Kontext für Wochenplanung
```

**Intelligente Einbindung in den Wochenplan:**
- Aktionen gegen geplante Mahlzeiten matchen
- Grundvorrat / Immer-Check-Liste abgleichen
- Bulk-Käufe bei starken Rabatten vorschlagen
- Aldi/Lidl-Aktionen nur bei >30% Rabatt UND relevanten Produkten

**Einkaufsliste-Output:**
- Nach Laden sortiert (Migros Haupteinkauf, optional Aldi/Lidl)
- Aktionen markiert mit Preis + Rabatt
- Kategorien: Milch & Käse, Fleisch, Gemüse, Vorratskammer etc.

### Vorratsmanagement
- **Methode:** Patricia sagt dem Bot mündlich/schriftlich was da ist
- Kein automatisches Tracking, kein Foto-Scan
- Bot fragt aktiv: "Was hast du gerade da?" bevor er plant

### Grundvorratsliste
> Das ist IMMER im Haus — damit rechnet der Bot automatisch.

**Kühlschrank / Frisch:**
- Baürnmilch (vom Baürn, immer da)
- Butter
- Eier (bald eigene Hühner, bis dahin kaufen)
- Yoghurt / Naturjoghurt
- Hüttenkäse
- Quark
- Rahm
- Sbrinz
- Käse (diverse — Reibkäse, Sbrinz, weitere Sorten)
- Mozzarella (Immer-Check)
- Feta (Immer-Check)
- Aufschnitt
- Konfi
- Brotaufstrich
- Essiggurken
- Ketchup
- Majo
- Knoblauch
- Zwiebeln

**Tiefkühler:**
- TK Gemüse
- TK Pizza (Notfall-Mahlzeit)
- Pommes
- Büchsengemüse (Vorrat)

**Vorratskammer / Trocken:**
- Reis (Basmati, Milchreis, Risotto)
- Teigwaren (Hörnli, Älplermageronen, Nüdeli, Nudeln, Spaghetti)
- Lasagneblätter
- Pasta Dinkel/Vollkorn
- Haferflocken / Müsli
- Nüsse / Samen (Koro-Bestellung)
- Trockenfrüchte (Koro-Bestellung)
- Hülsenfrüchte (Linsen, Kichererbsen, Bohnen — Dose + trocken)
- Kokosmilch
- Passierte Tomaten
- Bouillon
- Olivenöl
- Rapsöl
- Essig
- Honig
- Nutella (für die Kids)
- Darvida / Blevita
- Knäckebrot
- Farmer-Riegel
- Salziges (Snacks)
- Gewürze (Oswald): Curry, Raclettgewürz, Pomix, Fleischgewürz, Kräuter Meersalz, Bratensauce, Rindsbouillon, Gemüsebouillon, Hühnerbouillon Naturschätze, Pouletgewürz, Pastagewürz
- Mehl (Altbachmühle): Spätzlimehl, Zopfmehl, Dinkel-Rustico, Chnöpflimehl, Pizzamehl, Halbweissmehl, Pastamehl, Baürnmehl, Fitmehlkonzentrat, Roggen und Roggenschrot, Dinkelkorn
- Backutensilien: Vanillezucker, Backpulver, Hefe, Zucker, Rohrzucker

**Garten (saisonal verfügbar):**
- Dienstags kommt der Gemüsemann → Gemüse + Früchte
- Eigener Garten (wird laufend aktualisiert je nach Saison)

### Immer-Check-Liste
> Sachen die der Bot bei JEDER Einkaufsplanung checkt: "Ist noch genug da?"

**Proteinreich / Kühlschrank:**
- Mozzarella, Feta, Hüttenkäse, Eier, Yoghurt/Quark, Skyr, Hummus, Edamame, Hart gekochte Eier (Meal Prep), Proteinriegel (Koro oder Migros)

**Pausensnacks Kids:**
- Farmer-Riegel, Darvida/Blevita, Trockenfrüchte, Nüsse, Reiswaffeln, Fruchtriegel, Gemüsesticks-Zutaten (Karotten, Gurken, Peperoni)

**Haushalt & Pflege (Verbrauchsmaterial):**
- Haushaltspapier, WC Papier, Nastücher, Waschmittel, Reinigung, Zahnpasta, Zahnbürsten, Haarschaum, Rasierschaum, Wattepads, Deo

### Lieferanten & Bezugsqüllen

| Was | Lieferant | Freqünz |
|---|---|---|
| Mehl (12 Sorten) | **Altbachmühle** | Grossbestellung, nach Bedarf |
| Gewürze (11 Produkte) | **Oswald** | Grossbestellung, nach Bedarf |
| Nüsse, Samen, Trockenfrüchte | **Koro** | Grossbestellung, nach Bedarf |
| Gemüse & Früchte | **Gemüsemann** (dienstags) | wöchentlich |
| Milch | **Baür** (lokal) | laufend |
| Pasta (Dinkel/UrDinkel) | Kernser Pasta / Kofmel / Fidirulla | nach Bedarf |
| Lebensmittel allgemein | **Migros** (Hauptladen) | max. 1x/Woche, Ziel 14-tägig |
| Aktionen | **Aldi / Lidl** (wenn lohnend) | gelegentlich |

---

## 6. Rezeptqüllen & Daten-Architektur

### Quellen-Priorität
1. Eigene PDFs / Familienrezepte — ERSTE Anlaufstelle
2. 7hauben Kurshefte (Fokus: Brotbacken) — PDF-Import + Wissensdatenbank
3. Cookidoo (Thermomix-Rezepte) — Direkt-Sync via API
4. Schweizer Rezeptplattformen — Web-Scraping mit Schema.org
5. DACH / Internationale Rezeptseiten — Web-Suche + Schema.org-Parser

### Quelle 1: Eigene PDFs & Familienrezepte
- Bewehrte Rezepte, persönliche Sammlung
- Höchste Priorität — das sind die Gerichte die funktionieren
- Bot durchsucht PDFs nach passenden Rezepten basierend auf verfügbare Zutaten

### Quelle 2: 7hauben Kochkurse (Schwerpunkt Brotbacken)

**Mitgliedschaft:** 7hauben Pass → Zugang zu ALLEN 80+ Kursen inkl. Begleithefte als PDF

**Bisher hochgeladene / priorisierte Kurshefte:**
| Kurs | Kursleiter | Inhalt |
|---|---|---|
| Brotbacken Basics | Lutz Geissler | Grundlagen mit Hefe, ohne Saürteig |
| Saürteig Teil 1 | Lutz Geissler | Saürteig züchten, pflegen, umzüchten, haltbar machen |
| Saürteig Teil 2 | Lutz Geissler | Roggensaürteigbrot, Weizenbrote mit Levain, Croissants, Panettone |
| Vollkornbrote | Dietmar Kappl | Vollkorn mit Dinkel-, Roggen-, Weizenmehl |
| Handgemachte Pasta | Claudio Del Principe | Pastateig von Hand, verschiedene Nudelformen |
| Pasta Essentials | Georg Essig | Perfekter Teig mit Maschine, wichtigste Nudelformen |
| Gesunde Salate | Juliana Lopez May | 6 Vinaigrettes, Panzanella, Blumenkohl-Couscous |

### Quelle 3: Cookidoo (Thermomix)
- Python-Package `cookidoo-api` (inoffiziell, aktiv gepflegt)
- Zugriff auf: Rezepte, Favoriten, eigene Sammlungen, Wochenplaner, Einkaufsliste
- Wöchentlicher Refresh der Favoriten

### Quelle 4: Schweizer Rezeptplattformen
- **Marcel Paa** (marcelpaa.com) — 1'300+ Gratis-Rezepte, Schweizer Bäckermeister
- **Judith Erdin / Streusel** (streusel.ch) — Schweizer Bäckerin-Konditorin
- **Migusto** (migusto.migros.ch) — Migros-Rezepte
- **Betty Bossi** (bettybossi.ch) — Schweizer Klassiker
- **Swissmilk** (swissmilk.ch) — Saisonal, Schweizer Produkte
- **Fooby** (fooby.ch) — Gute Rezepte trotz Coop-Plattform

### Quelle 5: DACH / International
- **Food with Love** (foodwithlove.de) — Thermomix-Rezepte, familientauglich
- **Foodwerk** (foodwerk.de) — Einfache Alltagsrezepte
- **Zaubertopf** (zaubertopf-club.de) — Thermomix-Magazin
- **Chefkoch** (chefkoch.de) — Grösste DACH-Datenbank
- **EatSmarter** (eatsmarter.de) — Nährwertdaten inkl. Protein pro Portion
- **Plötzblog** (plötzblog.de) — Lutz Geisslers Blog, hunderte Brotrezepte

### Quelle 6: Garten, Selbstversorgung & Vorratskammer

**Wurzelwerk — Marie Diederich** (wurzelwerk.net)
- Eigener Gemüsegarten, Selbstversorger-Mindset
- Online-Kurse: Gemüsegarten starten, Wintergarten starten, Vorratskammer starten
- Bot nutzt Wurzelwerk-Wissen für Verarbeitungspläne und Saisonkalender

### Rezept-Pipeline
```
Schritt 1: SUCHE — in eigene PDFs → Cookidoo → Migusto → Chefkoch → EatSmarter
Schritt 2: EXTRAKTION — Schema.org/Recipe Daten auslesen
Schritt 3: FILTER & RANKING
  - Protein pro Portion >= 20g
  - Wenig Zucker / wenig Weizen
  - Zeitaufwand passt
  - Geräte-Match
  - Saisonal passend
  - Familientauglich
Schritt 4: ANPASSUNG — Portionen umrechnen, Protein-Boost, Weizen-Alternative, Aktionen matchen
Schritt 5: OUTPUT — Rezept + Protein/Portion + Quelle + Einkaufsliste-Integration
```

### Rezept-Datenbank (lokal)
- Eigene PDFs (einmalig importiert)
- Cookidoo-Favoriten (regelmässig gesynct)
- Bewehrte Web-Rezepte (nach dem Kochen als "gut" markiert)
- Tags: schnell / vorbereitbar / Thermomix / Dampfgarer / Blech / OnePot / Wähe / proteinreich / kids-approved
- Rating: Familie hat's gemocht? → Bot merkt sich das

---

## 7. Projektmodus

### Saürteig & Brotbacken (Wissensbasis: 7hauben + Plötzblog)
- Schritt-für-Schritt über mehrere Tage
- Erinnerungen (Anstellgut füttern, Teig falten, Stockgare checken)
- Troubleshooting aus Kurswissen
- Levelaufbau: Basics → Saürteig starten → erste Brote → Vollkorn → Croissants/Panettone

### Meal Prep
- Sonntagsplanung: Was kann ich für die Woche vorbereiten?
- Doppelte Mengen vorschlagen wenn sinnvoll
- Komponenten-Prep (Getreide vorkochen, Gemüse schneiden, Saucen vorbereiten)

### Frische Pasta
- Ausrüstung: Betty Bossi Pastamaschine
- Mehl: Altbachmühle (Pastamehl, Halbweissmehl, Dinkelmehl)
- 7hauben-Kurse als Wissensbasis
- Batch-Tag-Planung, Trocknung & Lagerung, Troubleshooting

### Gartenverarbeitung (Wissensbasis: Wurzelwerk Marie Diederich)
- Ernte verarbeiten: Einmachen, Fermentieren, Einfrieren, Dörren
- Saisonale Batch-Verarbeitung
- Aussaatkalender + Erntekalender
- Vorratskammer-Strategie

### Projektablauf
1. Bot fragt: Was willst du starten?
2. Bot erstellt Schritt-für-Schritt-Plan mit Zeitachse
3. Bot erinnert an nächste Schritte
4. Bot passt an wenn sich was ändert

---

## 8. Bot-Verhalten & Ton

### Kommunikationsstil
- Schwyzerdeutsch-kompatibles Hochdeutsch ("ss" statt "ss")
- Direkt, klar, kein Geschwafel
- Darf humorvoll sein und Persönlichkeit zeigen
- Keine generischen Ernährungsratschläge
- Praxisnah: Was kann ich JETZT mit dem was da ist machen?

### Interaktionsmuster
- **Wochenplanung:** "Was hast du da? Was steht diese Woche an?" → Plan + Einkaufsliste
- **Spontan:** "Ich hab Poulet, Brokkoli und Reis — was mach ich?" → 2-3 Vorschläge
- **Projekt starten:** "Ich will Saürteig starten" → Mehrtagesplan
- **Garten-Alarm:** "Die Tomaten sind reif, ALLE" → Verarbeitungsplan
- **Einkaufsoptimierung:** Einkaufsliste nach Laden sortiert, Aktionen integriert
- **Wandertag/Ausflug:** "Wir gehen am Samstag wandern" → To-Go Menü + Snacks für 6
- **Quick-Archiv:** Foto/Screenshot schicken → Bot archiviert Rezept

### Output-Formate
- **Wochenplan:** Mit Rezept-Links, Protein pro Portion, Geräte-Hinweis
- **Einkaufsliste:** Nach Kategorie sortiert, Laden-Zuordnung, Aktionen markiert
- **Rezepte:** Zutaten + Schritte, Portionen für 5-6 Personen, Protein-Info, Zeitangabe, Qüll-Link
- **Projekte:** Zeitachse mit Schritten, Material-/Zutatenliste vorab

---

## 9. Wöchentliches Ernährungs-Coaching

### Konzept: "Wissen, das schmeckt"

**WICHTIG:** Alle Ernährungsprinzipien gelten IMMER und GLEICHZEITIG bei jeder Mahlzeit:
- Proteinreich (100g/Tag)
- Antientzündlich
- Darmfreundlich
- Säure-Basen-balanciert
- Blutzuckerstabil
- Ayurveda-Prinzipien (warme Mahlzeiten, Verdauungsfeür)

Die Themenrotation betrifft nur den wöchentlichen Bildungs-Impuls.

### Themenfelder (Rotation)
1. Vitamine
2. Mineralstoffe
3. Aminosäuren
4. Säure-Basen
5. Blutzucker
6. Darmgesundheit
7. Ayurveda
8. Bedarfsorientiert
9. Selbstheilung
10. Saisonales
→ Dann wieder von vorn, mit neuen Themen

### Protein-Fokus (Daürmodul)
- Täglicher Protein-Tracker im Wochenplan
- Wöchentlicher Protein-Fakt
- Shopping-Tipps für proteinreiche Lebensmittel
- Protein-Boost-Vorschläge wenn Tagesbilanz zu niedrig

### Antientzündliche Ernährung (Daürmodul 2)
- Verknüpft mit doTERRA-Kur "Wohlfühlen leicht gemacht"
- Antientzündlich-Score pro Tag
- Omega-3 zu Omega-6 Verhältnis
- Basische vs. saure Lebensmittel-Balance

### Darm & Ganzheitliche Gesundheit (Daürmodul 3)
- Verknüpft mit feel.gut App, doTERRA-Kur
- Darmfreundliche Rezeptfilter
- Ayurveda-Integration (warme Mahlzeiten, Agni)
- Bedarfsorientierte Ernährung

### Wissensqüllen für Ernährungs-Content
- SGE (sge-ssn.ch) — Offizielle CH-Empfehlungen
- DGE (dge.de) — DACH-Referenzwerte
- EatSmarter (eatsmarter.de) — Nährwertdaten
- Examine.com — Evidenzbasierte Infos
- PubMed / Google Scholar — Für spezifische Fragen

---

## 10. Nächste Schritte

- [x] Grundvorratsliste erarbeiten
- [x] Immer-Check-Liste erarbeiten
- [x] Gewürzliste erstellen (Oswald — 11 Produkte)
- [x] Mehlsorten definieren (Altbachmühle — 12 Sorten)
- [ ] Eigene Rezept-PDFs sammeln und dem Bot zugänglich machen
- [ ] 7hauben-Kurshefte alle runterladen (Brot + weitere Kurse)
- [ ] Saisonkalender Garten definieren (was wächst wann)
- [ ] Erste Testwoche planen
- [ ] Lieblings-Rezepte taggen (Familienklassiker die immer gehen)
- [ ] Koro-Standardbestellung definieren (welche Nüsse, Samen, Trockenfrüchte)
