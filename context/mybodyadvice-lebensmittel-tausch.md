---
tags: [mealplan]
---

# MyBodyAdvice — Lebensmittel tauschen & Baukastenprinzip (Referenz)

Detail-Referenz zum Meal-Planning-Bot (`context/meal-planning-bot.md`). Enthält die vollständigen Makro-Tabellen und Tausch-Verhältnisse aus dem MyBodyAdvice-E-Book „Lebensmittel tauschen" + den Übersichten „Produkttausch" und „Swapping Ingredients Guide". Der `/mealplan`-Bot liest diese Datei, wenn er genaue Eiweiss-/kcal-Werte oder Tausch-Verhältnisse braucht.

---

## 1. Grundlagen & Baukastenprinzip

**Makroverteilung einer Hauptmahlzeit (Richtwert):** ~30 % Protein · ~40 % komplexe Kohlenhydrate · ~30 % Fett (mindestens immer Eiweiss + Fett).

**Energiewerte:** 1 g Eiweiss = 4 kcal · 1 g Kohlenhydrate = 4 kcal · 1 g Fett = 9 kcal · (1 g Alkohol = 7 kcal).

**Kriterien an jede Hauptmahlzeit:**
- **Mind. 30 g Eiweiss** pro Hauptmahlzeit (regt die Muskelproteinsynthese an, wichtig im Defizit).
- Viel Gemüse als Sättigungs-/Nährstoffbasis; beim Frühstück etwas Obst.
- Gesunde Fette für Vitaminaufnahme + Hormonhaushalt.
- Komplexe Kohlenhydrate bevorzugen (länger satt, stabiler Blutzucker).

**Bowl-/Mahlzeit-Baureihenfolge:** 1. Protein → 2. viel Gemüse → 3. komplexe Kohlenhydrate → 4. gesunde Fette. (Mit Schritt 1+2 beginnen sichert die 30 g Eiweiss.)

> Hinweis: Die meisten Lebensmittel sind **Hybridlebensmittel** (mehrere Makros) — immer die Gesamtmahlzeit betrachten, nicht ein einzelnes Lebensmittel.

---

## 2. Kategorie 1: Proteinquellen (Eiweiss / kcal pro 100 g · Menge für 30 g Eiweiss)

| Lebensmittel | Kategorie | Eiweiss/100g | kcal/100g | für 30 g Eiweiss |
|---|---|---|---|---|
| Hähnchenbrust | Fleisch | 24 g | 109 | 124 g / 136 kcal |
| Putenbrust | Fleisch | 24 g | 107 | 122 g / 133 kcal |
| Geflügelhackfleisch | Fleisch | 24 g | 142 | 124 g / 177 kcal |
| Rindfleisch | Fleisch | 20–22 g | 250 | 150 g / 375 kcal |
| Rinderhackfleisch | Fleisch | 21–22 g | 332 | 136 g / 452 kcal |
| Rinderhack leicht / Tartar | Fleisch | 20 g | 129 | 149 g / 193 kcal |
| Schweinefilet | Fleisch | 21 g | 143 | 142 g / 204 kcal |
| Magerer Schinken | Fleisch | 20 g | 107 | 142 g / 160 kcal |
| Katenschinken mager | Fleisch | 24 g | 122 | 124 g / 152 kcal |
| Lachs | Fisch | 20–23 g | 200 | 130 g / 260 kcal |
| Stremellachs | Fisch | 20 g | 207 | 150 g / 310 kcal |
| Räucherlachs | Fisch | 21 g | 138 | 143 g / 197 kcal |
| Saibling | Fisch | 19 g | 96 | 155 g / 151 kcal |
| Kabeljau | Fisch | 17 g | 90 | 176 g / 159 kcal |
| Garnelen | Fisch | 24 g | 99 | 125 g / 124 kcal |
| Thunfisch (frisch/in Wasser) | Fisch | 24–25 g | 130 | 120 g / 156 kcal |
| Magerquark | Milchprodukte | 12 g | 72 | 250 g / 180 kcal |
| Speisequark (40 % Fett) | Milchprodukte | 11 g | 100 | 273 g / 273 kcal |
| Speisequark (20 % Fett) | Milchprodukte | 9 g | 143 | 333 g / 476 kcal |
| Skyr | Milchprodukte | 12 g | 72 | 250 g / 180 kcal |
| Griech. Joghurt (2 % Fett) | Milchprodukte | 5 g | 174 | 600 g / 1044 kcal |
| Griech. Joghurt (10 % Fett) | Milchprodukte | 9 g | 54 | 333 g / 180 kcal |
| Hüttenkäse | Milchprodukte | 11 g | 100 | 273 g / 273 kcal |
| Hüttenkäse fettarm | Milchprodukte | 14 g | 75 | 214 g / 161 kcal |
| Feta | Milchprodukte | 15 g | 270 | 200 g / 540 kcal |
| Feta leicht | Milchprodukte | 19 g | 167 | 157 g / 264 kcal |
| Geramont | Milchprodukte | 19 g | 214 | 158 g / 338 kcal |
| Camembert | Milchprodukte | 20 g | 299 | 150 g / 449 kcal |
| Camembert leicht | Milchprodukte | 25 g | 224 | 107 g / 240 kcal |
| Harzer Käse | Milchprodukte | 28 g | 230 | 106 g / 246 kcal |
| Mozzarella | Milchprodukte | 22 g | 300 | 136 g / 409 kcal |
| Mozzarella leicht | Milchprodukte | 20 g | 165 | 150 g / 248 kcal |
| Parmesan | Milchprodukte | 35–38 g | 431 | 85 g / 369 kcal |
| Emmentaler | Milchprodukte | 29 g | 395 | 103 g / 409 kcal |
| Gouda | Milchprodukte | 25 g | 356 | 120 g / 427 kcal |
| Cheddar | Milchprodukte | 25 g | 415 | 120 g / 498 kcal |
| Ei (1 Ei = 60 g) | Ei | 12 g | 143 | 250 g / 358 kcal |
| Eiklar | Ei | 11 g | 47 | 272 g / 128 kcal |
| Linsen (roh) | Hülsenfrüchte | 24 g | 360 | 125 g / 450 kcal |
| Linsen Dose / vorgekocht | Hülsenfrüchte | 8 g | 96 | 375 g / 360 kcal |
| Linsennudeln | Hülsenfrüchte | 26 g | 336 | 115 g / 387 kcal |
| Kichererbsen-Couscous | Hülsenfrüchte | 21 g | 367 | 143 g / 524 kcal |
| Kichererbsen Glas | Hülsenfrüchte | 7 g | 127 | 428 g / 544 kcal |
| Kichererbsennudeln | Hülsenfrüchte | 22 g | 360 | 136 g / 491 kcal |
| Schwarze Bohnen Glas | Hülsenfrüchte | 8 g | 92 | 375 g / 345 kcal |
| Kidney Bohnen Glas | Hülsenfrüchte | 7 g | 101 | 428 g / 433 kcal |
| Edamame | Hülsenfrüchte | 11 g | 121 | 273 g / 330 kcal |
| Tofu | Sojaprodukte | 12 g | 124 | 250 g / 310 kcal |
| Tempeh | Sojaprodukte | 19 g | 193 | 158 g / 305 kcal |
| Sojaquark | Sojaprodukte | 5 g | 53 | 600 g / 318 kcal |
| Sojajoghurt | Sojaprodukte | 4 g | 46 | 750 g / 345 kcal |
| Quinoa | Pseudogetreide | 15 g | 368 | 200 g / 736 kcal |
| Amaranth | Pseudogetreide | 15 g | 374 | 200 g / 748 kcal |
| Hirse | Pseudogetreide | 10 g | 357 | 300 g / 1071 kcal |
| Buchweizen / -mehl | Pseudogetreide | 12 g | 365 | 250 g / 913 kcal |
| Chiasamen | Samen & Nüsse | 21 g | 446 | 143 g / 637 kcal |
| Hanfsamen | Samen & Nüsse | 31 g | 619 | 97 g / 599 kcal |
| Mandeln / -mus | Samen & Nüsse | 24 g | 624 | 125 g / 780 kcal |
| Erdnüsse / -mus | Samen & Nüsse | 25 g | 623 | 120 g / 748 kcal |
| Walnüsse | Samen & Nüsse | 17 g | 696 | 162 g / 1128 kcal |
| Cashewnüsse | Samen & Nüsse | 17 g | 576 | 176 g / 1016 kcal |
| Kürbiskerne | Samen & Nüsse | 35 g | 581 | 85 g / 498 kcal |
| Mandelmehl (teilentölt) | Samen & Nüsse | 53 g | 380 | 57 g / 215 kcal |
| Kuhmilch | Milch & -alternativen | 3,5 g | 47–64 | 858 g / 549 kcal |
| Sojamilch | Milch & -alternativen | 3 g | 33 | 1000 g / 330 kcal |
| Erbsenmilch | Milch & -alternativen | 2,5 g | 37 | 1200 g / 444 kcal |
| Wheyprotein | Proteinpulver | 53–84 g | 350–400 | 42 g / 163 kcal |
| Erbsenprotein | Proteinpulver | 82 g | 393 | 37 g / 144 kcal |
| Sojaprotein | Proteinpulver | 90 g | 360 | 33 g / 120 kcal |
| Hanfprotein | Proteinpulver | 50 g | 356 | 60 g / 214 kcal |
| Reisprotein | Proteinpulver | 80 g | 404 | 38 g / 152 kcal |

> Eiweissreich ≠ automatisch kalorienarm. Bsp. Hanfsamen (31 g/100 g, aber 619 kcal) → nur als Topping/Ergänzung.

---

## 3. Kategorie 2: Kohlenhydratquellen (KH / kcal pro 100 g)

| Lebensmittel | Kategorie | KH/100g | kcal/100g |
|---|---|---|---|
| Quinoa (glutenfrei) | Pseudogetreide | 64 g | 368 |
| Amaranth (glutenfrei) | Pseudogetreide | 56 g | 374 |
| Hirse (glutenfrei) | Pseudogetreide | 69 g | 357 |
| Buchweizen / -mehl (glutenfrei) | Pseudogetreide | 71 g | 365 |
| Buchweizengrütze | Pseudogetreide | 63 g | 347 |
| Basmatireis (glutenfrei) | Reis | 78 g | 363 |
| Naturreis (glutenfrei) | Reis | 77 g | 355 |
| Weißer Reis (glutenfrei) | Reis | 80 g | 365 |
| Haferflocken | Getreide | 60 g | 370 |
| Haferkleie | Getreide | 55 g | 330 |
| Reismehl / -brei / -flocken | Getreide | 80 g | 366 |
| Buchweizenflocken | Getreide | 71 g | 365 |
| Quinoaflocken | Getreide | 58 g | 367 |
| Bulgur (Weizen) | Getreide | 76 g | 351 |
| Couscous (Weizen) | Getreide | 70 g | 362 |
| Dinkelgrieß | Getreide | 71 g | 341 |
| Kartoffeln | Gemüse | 14 g | 70 |
| Kartoffelgnocchi | Gemüse | 34 g | 167 |
| Süßkartoffeln | Gemüse | 24 g | 117 |
| Hokkaido-Kürbis | Gemüse | 5 g | 90 |
| Spaghettikürbis | Gemüse | 6 g | 27 |
| Linsen (roh) | Hülsenfrüchte | 57 g | 360 |
| Linsen Dose / vorgekocht | Hülsenfrüchte | 13 g | 96 |
| Linsennudeln | Hülsenfrüchte | 50 g | 336 |
| Kichererbsen Glas | Hülsenfrüchte | 14 g | 127 |
| Kichererbsennudeln | Hülsenfrüchte | 51 g | 360 |
| Schwarze Bohnen Glas | Hülsenfrüchte | 12 g | 92 |
| Kidney Bohnen Glas | Hülsenfrüchte | 13 g | 101 |
| Datteln | Trockenfrüchte | 65 g | 265 |
| Rosinen | Trockenfrüchte | 22 g | 95 |
| Bananen | Obst | 23 g | 89 |
| Weintrauben | Obst | 17 g | 70 |
| Reiswaffeln | Sonstiges | 78 g | 386 |
| Linsenwaffeln | Sonstiges | 58 g | 360 |
| Knäckebrot | Brot | 56 g | 346 |
| Vollkornbrot (Dinkel, Roggen) | Brot | 47 g | 249 |
| Weizen- / Dinkelnudeln | Nudeln | 72 g | 358 |
| Vollkornnudeln (Weizen) | Nudeln | 67 g | 360 |
| Dinkelvollkornnudeln | Nudeln | 62 g | 344 |
| Tortellini | Nudeln | 55 g | 301 |
| Spätzle | Nudeln | 26 g | 169 |
| Reisnudeln | Nudeln | 72 g | 350 |
| Dinkel(vollkorn)mehl | Mehl | 71 g | 350 |
| Weizenmehl | Mehl | 72 g | 352 |
| Reismehl | Mehl | 80 g | 366 |
| Mehlmischung (glutenfrei) | Mehl | 82 g | 345 |

---

## 4. Kategorie 3: Fettquellen (Fett / kcal pro 100 g)

| Lebensmittel | Fett/100g | kcal/100g |
|---|---|---|
| Olivenöl | 92 g | 824 |
| Leinöl | 99 g | 819 |
| Kokosöl | 92 g | 827 |
| Avocadoöl | 91 g | 824 |
| Rapsöl | 100 g | 884 |
| Butter | 83 g | 741 |
| Ghee | 99 g | 898 |
| Schwarzkümmelöl | 100 g | 887 |
| Avocado | 15 g | 160 |
| Kokosflocken | 65 g | 660 |
| Kakaonibs | 58 g | 635 |
| Zartbitterschokolade | 47 g | 582 |
| Hanfsamen | 51 g | 619 |
| Mandeln / -mus | 52 g | 624 |
| Erdnüsse / -mus | 49 g | 623 |
| Walnüsse | 70 g | 696 |
| Cashewnüsse / -mus | 44 g | 576 |
| Kürbiskerne | 48 g | 581 |
| Haselnusskerne / -mus | 60 g | 661 |
| Macadamianüsse | 74 g | 771 |
| Leinsamen | 37 g | 494 |

---

## 5. Tausch-Verhältnisse (gleiche Makro-Funktion ersetzen)

Berechnung: Wenn Verhältnis nicht 1:1, dann angegebene Menge × Faktor. Bsp. statt Dinkelnudeln Kartoffeln (5,11:1) → Nudelmenge × 5,11.

**Kohlenhydrate — statt Haferflocken (alle 1:1):** Haferkleie, Reismehl/-flocken, Buchweizenflocken, Quinoaflocken, Dinkelgrieß, Quinoa, Amaranth, Hirse, Buchweizen(-mehl), Buchweizengrütze, Dinkelmehl.

**Statt Dinkelmehl (1:1):** Dinkel(vollkorn)mehl, Weizenmehl, Buchweizenmehl, Reismehl, Mehlmischung (glutenfrei).

**Statt Roggenvollkornbrot:** Dinkelvollkornbrot 1:1 · Saatenbrot 0,85:1 · Knäckebrot 0,7:1 · Linsenwaffeln 0,7:1.

**Statt Dinkelnudeln:** Vollkorn-/Dinkelvollkorn-/Linsen-/Kichererbsennudeln 1:1 · Tortellini 1:1 · Reisnudeln 1:1 · Reis 1:1 · Linsen 1:1 · Spätzle 2:1 · Kartoffeln (ungekocht) 5,11:1.

**Proteine — statt Skyr (1:1):** Magerquark, Hüttenkäse leicht.
**Statt Feta light:** Mozzarella leicht 1:1 · Tofu 1:1 · Hähnchenbrust 0,8:1 + 4 ml Öl · Garnelen 0,8:1 + 4 ml Öl · (Räucher)Lachs 0,84:1 · Thunfisch 0,6:1 + 8 ml Öl · Hüttenkäse 1,6:1.
**Statt Kichererbsennudeln:** Linsennudeln 1:1 · Linsen 1:1 · Kichererbsen aus dem Glas 2,83:1 · Linsen aus dem Glas 3,75:1.

**Fette — statt Mandelmus (Backen):** Butter 1:1 · Kokosöl 1:1.
**Statt Avocado:** Olivenöl/Leinöl 0,2:1 · Walnusskerne 0,23:1 · Hanfsamen 0,26:1 · Kürbiskerne/Cashewkerne 0,28:1.
**Statt Pesto:** Parmesan 1:1 · Olivenöl 0,5:1 + Essig.

> **Achtung — schlecht tauschbar:** Hülsenfrucht-Nudeln (Kichererbsen-/Linsennudeln) **nicht** einfach gegen Getreidenudeln (Dinkel/Weizen) tauschen — sonst fehlt der Proteingehalt der Mahlzeit.

---

## 6. Produkttausch — Milchprodukte & vegane Alternativen

**Milch:** Vollmilch, fettarme Milch, Erbsenmilch (Vly), Ziegenmilch, Schafmilch.
**Käse (untereinander):** Gouda, Leerdammer, Butterkäse, Maasdammer, Edamer, Parmesan, Gruyère, Halloumi.
**Mozzarella ↔ Feta** (auch jeweils Light-Variante; alternativ Tofu).
**Quarkprodukte:** Magerquark, Skyr, Hüttenkäse, Sojaquark.
**Joghurt →** Quark, Skyr, Hüttenkäse oder Sojaquark in **doppelter Menge**.
**Milchalternativen (untereinander):** Soja-, Erbsen-, Haselnuss-, Kokos-, Reis-, Mandelmilch.
**Tofu →** Tempeh, Sojagranulat, Seitan (nicht-vegan: Hähnchenbrust, Rindertatar, Feta Light, Mozzarella Light).
**Sojaquark →** Vly-Joghurt aus Ackerbohnenprotein.
**Pflanzliche Drinks:** jeder gegen jeden tauschbar — aber **Sojaprodukte haben den höchsten Proteingehalt**. High-Protein: Erbsendrink, Sojadrink. Low-Calorie: Hafer-, Reis-, Mandel-, Kokosdrink.

---

## 7. Swapping Ingredients — Obst/Gemüse nach Carb-Level

Zutaten aus **demselben Abschnitt** sind untereinander tauschbar (für nicht verfügbare Zutaten).

- **Low-Carb-Obst:** Himbeeren, Erdbeeren, Brombeeren, schwarze Johannisbeere, Stachelbeeren, Wassermelone, Preiselbeeren, Aprikose, Melone, pinke Grapefruit, Granatapfel, Blaubeeren, Kirschen.
- **High-Carb-Obst:** Birne, Klementine, Ananas, Mango, Nektarine, Pfirsich, Orange, Pflaume, Weintrauben, Apfel, Banane.
- **Low-Carb-Gemüse:** Champignons, Chicorée, Radieschen, Gurke, Sellerie, Spargel, Grünkohl, grüne Bohnen, Zucchini, Aubergine, Brokkoli, Kohlrabi, Rosenkohl, Blumenkohl, Rotkohl, Salat, Fenchel, Paprika, Tomate, Erbsen, Zuckerschote.
- **Medium-/High-Carb-Gemüse:** Kürbis, Steckrübe, Butternusskürbis, Karotten, Zuckermais, Jerusalem-Artischocke, Pastinake, Kartoffel, Süßkartoffel.
- **Zwiebeln (untereinander):** Schalotte, Frühlingszwiebel, gelbe/rote Zwiebel, Silberzwiebeln.

**Fleisch nach Fettgehalt (untereinander tauschbar):**
- *< 4 % Fett:* Hähnchenbrust, Putenbrust, Schweinefilet, mageres Geflügel-Hack, Kalbsfilet, Rinderfilet.
- *4–7 % Fett:* Hähnchenschenkel (ohne Haut), Schweinerücken, Lamm, Rinderbraten, Steak, mageres Rinder-Entrecôte, Hackfleisch (4–7 %).
- *10–15 % Fett:* Rumpsteak, Hackfleisch (10–15 %).
**Hülsenfrüchte (untereinander):** weiße/schwarze Bohnen, Puy-/grüne/rote Linsen, Kichererbsen, Kidney-/Wachtelbohnen.
**Getreide (untereinander):** Gerste, Bulgur, Nudeln, Couscous, Reis, Quinoa, Amaranth.
**Pflanzl. Joghurt (untereinander):** Mandel-, Kokos-, Sojajoghurt (Soja = mehr Protein).

---

## 🔗 Verwandte Notizen

- [[meal-planning-bot]]
