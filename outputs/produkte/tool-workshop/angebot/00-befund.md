---
tags: [produkt, funnel]
---

# Tool-Workshop gegen die Funnel-Checkliste

Geprüft am 31.10.2026, alle 138 Punkte. Derselbe Befund steht unter jedem Punkt auf der Funnel-Checkliste (Auswahl „Tool-Workshop“).

⚠️ veraltet oder falsch 28 · ❌ fehlt 14 · ❓ nicht prüfbar 27 · ✅ belegt 44 · ➖ trifft nicht zu 25

> Gegenprobe in ActiveCampaign (31.10.): „Tool-Workshop“ (86) enthält 8 Mails, „0€ Nischengenerator“ (87) enthält 5. Die Mail-Liste im Cockpit-Abgleich () ordnet dort mehr Mails zu, als in den Automationen stehen.

## ⚠️ veraltet oder falsch (28)


**Bevor du baust**

- **Das Produkt wurde schon ein- bis dreimal live verkauft** — Workshop ist neu (launched_on 2026-10-29 in active-funnels.json), noch kein Verkauf belegt. Nachfrage ungeprueft, die Kasse ist der Test.
- **Ein Problem, eine Verwandlung — in einem Satz** — 00-bauplan.md hat Schmerz davor und Veraenderung, aber active-funnels.json tool-workshop hat kein Feld problem/transformation.
- **Im Ziel-Checkout nachgesehen, was dort als Upsell hängt** — 03-kasse.md: "Upsell Nr. 7 an Startklar/Storyideen bucht 97, die Seite dort schreibt nur fuer CHF 199" noch offen; gleiche Kundenmaschine, zwei Preise im Umlauf.
- **Der Name nennt das Ziel, nicht den Inhalt** — Name "Tool-Workshop" nennt den Inhalt; nur die Seiten-Ueberschrift nennt das Ziel ("Bau dir ein Gratis-Tool, das dir neue Kontakte bringt").

**Die Kasse**

- **Jedes Zusatzangebot trägt seinen eigenen Streichpreis** — Bump "25 statt 39" und Upsell "333 -> 199" ok; Downsell Startklar 39 ist laut katalog.json auch der Normalpreis (39), also kein Streichpreis moeglich.
- **Bei 0€: alle drei Kassen besetzt** — Nischengenerator: Danke-Seite WP 4442 besetzt, aber nach dem Bestaetigungsklick geht es direkt zum Tool (09-einrichten.md), nicht auf eine Seite mit Angebot.
- **Das grosse Produkt steht im Funnel nie zum Normalpreis** — Mails B5/B7 pitchen Digitale Produktwelt zu 333 ohne Frist und ohne Funnel-Preis; nur die Danke-Seiten haben 199 per Gutschein.

**Die Seiten**

- **Seite nach dem Bestätigungsklick hinterlegt** — Nischengenerator: nach dem Klick geht es direkt zum Tool (09-einrichten.md), keine eigene Seite mit Workshop-Angebot; Workshop selbst braucht keine.
- **Bei einer Frist: eigene Angebotsseite und eine „abgelaufen“-Seite** — Frist "bis Mo 9.11., 23:59" steht in Mails/Storys, nicht auf WP 4436; 03-kasse.md: Kasse bleibt danach offen. Keine Abgelaufen-Seite.
- **Der Produktname steht genau einmal auf der Seite** — WP 4436 nennt "Tool-Workshop" mehrfach: Logo, Eyebrow, Preiskarte, Titel; Ueberschrift selbst nennt zum Glueck das Ziel.
- **Die sechs Blöcke stehen in dieser Reihenfolge** — WP 4436: Reihenfolge Hero, Ablauf, Was ist ein Tool, Warum Tool, Workshop, Warum mit mir, Preis; keine Kundenstimme, Ist-Situation und Soll nicht in der Blockfolge.
- **Der Block „Das brauchst du nicht“ steht drin** — Kein eigener Block "Das brauchst du nicht"; nur Haken "Ganz ohne Code, kein Technik-Wissen" und FAQ "Was brauche ich" auf WP 4436.
- **Ein FAQ beantwortet die Einwände** — FAQ auf WP 4436 hat sechs Fragen, aber nicht Zugriffsdauer, Ratenzahlung oder Erfolgsgarantie.
- **Jede Adresse einmal wirklich aufgerufen** — Nur per REST geprueft (WP 4436/4441/4442/4443/4413 publish, Kassen live); Aufruf per Browser nicht, curl ist durch die Firewall geblockt.

**Die Mails**

- **Genau ein Aufruf je Mail** — A1 hat Knopf zum Workshop plus zweiten Link zum Nischengenerator; C0 hat Nischengenerator-Knopf und Workshop-Knopf; B0 drei Links.
- **Die Willkommensmail zeigt die ganze Welt** — Willkommen B0 und C0 zeigen keine drei Angebote mit Pitch; B0 nur Vorbereitung, C0 nur Workshop.
- **Irgendwo in der Strecke steht ein 48-Stunden-Angebot** — A3 hat Frist Mo 9.11., aber keinen Rabatt auf einen kleinen Kurs; der Preis bleibt 39. Echtes 48-Stunden-Angebot fehlt.
- **Für die, die nicht gekauft haben, läuft eine eigene Strecke** — C0–C4 laufen für Nicht-Käuferinnen, nennen aber feste Termine (10./11.11., Kasse 9.11.). Ab 10.11. auf die Aufzeichnung umschreiben oder pausieren.
- **Der Kurskäuferin wird das 0€-Webinar angeboten** — Webinar nur als Block auf der Danke-Seite 4460, keine der Mails B0-B7 laedt dazu ein.
- **Keine einzige Mail ohne Link** — B1, B2 und B3 haben keinen Link (B1/B2 nur Zoom-Text, B3 nur Fliesstext).
- **Jeder Knopf führt irgendwohin** — B2-tag-2.html: Platzhalter "LINK ZUR AUFZEICHNUNG" statt Link; alle Knoepfe sonst auf echte Adressen.
- **Keine festen Datumsangaben in einer Dauer-Automation** — Automation 86: B1 Mo 9.11., B2 Mi 11.11., B3 Sa 14.11. als feste Warte-Daten, B0-B2 nennen 10./11.11.; C1-C4 ebenso. Kasse bleibt offen (03-kasse.md): spaete Kaeuferinnen bekommen alles auf einmal.

**Der Zulauf**

- **ManyChat-Flow eingerichtet** — NISCHE steht weder in context/manychat-keywords.md noch in active-funnels.json/funnel.json; Antwort laeuft von Hand (07-automation.md). Content-Skills kennen das Stichwort nicht.
- **Der Preis steht in der Story** — Nur Storys 30.10. und 5.11. nennen 39 CHF; Samstag-, Sonntag- und Montag-Storys (kw45/46) zeigen Link ohne Preis.

**Der Launch**

- **Die fünf Phasen stehen im Kalender** — 05-storys.md kennt Phasen Kasse offen, letzter Tag, Workshop, Begleitung, danach; Aufwaermen, Secret Offer und Nachbereitung als Phasen fehlen.
- **Die Aufwärmphase dauert rund eine Woche** — Aufwaerm-Storys kw44 (26.-29.10.) nur vier Tage, dann Kasse offen seit 29.10. (kw44-story-m-nov-mo bis do).
- **Die Verknappung stimmt wirklich** — Mails A3/Storys: "heute schliesst die Anmeldung", aber 03-kasse.md: "Danach bleibt die Kasse offen" (Aufzeichnung); active-funnels sagt Kasse bis 9.11. 23:59.

**Nach dem Start**

- **Entschieden: weiterlaufen lassen, nachschärfen oder abstellen** — 01-aufbau.md: "Offen: Preis der Aufzeichnung, ob die Begleitung wegfaellt"; Entscheid widerspruechlich: 03-kasse.md Kasse bleibt offen, 09-einrichten.md Kasse disabled.

## ❌ fehlt (14)


**Bevor du baust**

- **Die Produkt-Tabelle ist ausgefüllt** — Keine Produkt-Tabelle mit den elf Spalten (Story dazu, was bringt es ihr, Glaubenssaetze ...); 00-bauplan.md hat nur Kurzzeilen. Gehoert in 00-bauplan.md.
- **Die Ist-Situation über vier Fragen gefunden** — Keine Antworten auf die vier Ist-Fragen (nachts wach, morgens zuerst, Angst, aufschieben) dokumentiert; die Seite nutzt nur die Schmerz-Zeile aus 00-bauplan.md.
- **Die Prüffrage zum Preis beantwortet** — Nirgends steht, warum 39 fuer das Ergebnis (Tool + Seite online) gerechtfertigt ist; gehoert in 00-bauplan.md unter Preis.
- **Der Return on Invest steht irgendwo als Satz** — Weder Seite noch Kasse noch Mails nennen den Return (Kontakte, Zeit, Nerven) als Satz; Seite spricht nur von "Weg zu neuen Kontakten".
- **Ausgerechnet, wie viele Verkäufe das Ziel braucht** — Keine Rechnung zu Verkaeufen/Umsatzziel fuer den Workshop in angebot/*.md oder active-funnels.json.
- **Erste Kundenstimmen beschafft, bevor die Seite steht** — 02-salespage.md Block 3 und 10 sind Platzhalter ("Ohne Stimme weglassen"); live WP 4436 hat keine Kundenstimme.

**Die Kasse**

- **Mehrere Bumps plus ein Bundle aus allen** — Nur ein Bump (thrivecart.json), kein zweiter Bump, kein Bundle. Gehoert in die Kasse 53/54, z.B. Story-Generator 17 als zweiter Bump.
- **Je Upsell und Downsell ein eigener Tag im Mailprogramm** — 03-kasse.md: "Offen: AC-Tags fuer Upsell- und Downsell-Kaeuferinnen"; sonst Werbung fuer gekaufte Angebote. In ThriveCart Fulfillment je Upsell/Downsell Tag setzen.

**ActiveCampaign**

- **Entschieden, was mit denen passiert, die nicht kaufen** — Nach B7 ("letzte Mail zur Produktwelt") ist kein Weg fuer Nichtkaeuferinnen dokumentiert; weder zweite Runde noch Uebergabe in eine Automation.

**Die Mails**

- **Der Baustein „… und das ohne …“ ist drin** — Kein Baustein "drei Dinge, die es bringt / drei, die es nicht braucht" in A1-A3 oder C-Mails; nur "Was du brauchst" in A2. Gehoert in A2 und C2.

**Der Launch**

- **Jeden Tag wird geteilt, wer schon dabei ist** — Keine "Wer ist schon dabei"-Folie in den Workshop-Storys kw45/46 (per Dateisuche in den Story-Dateien); gehoert vor die letzte Folie ab Verkaufsphase.

**Nach dem Start**

- **Kundenstimmen aktiv eingeholt** — 09-einrichten.md nennt es erst "nach dem Workshop"; keine Mail B0-B7 fragt nach einer Stimme. Gehoert als Mail nach dem 14.11. in Automation 86.
- **Ein Video-Testimonial gefragt** — Kein Video-Testimonial angefragt oder geplant (angebot/*.md).
- **Den Bestandskundinnen ein eigenes Angebot geschickt** — A1-A3 gehen nur an Liste 2 (Interessenten); keine Mail an Liste 16 (Bestandskundinnen) mit Dank-Vorteil.

## ❓ nicht prüfbar (27)


**Die Kasse**

- **Die Auslieferungstexte der Kasse sind übersetzt** — Auslieferungstexte stehen nur in der ThriveCart-Oberflaeche; ausserhalb nicht lesbar.
- **Checkout und Upsell-Seite am Handy angesehen** — Handy-Ansicht der Kasse nicht ausserhalb ThriveCart pruefbar; 03-kasse.md: Block im Editor nur als CUSTOM HTML sichtbar.

**ActiveCampaign**

- **Kopiertes Formular ganz durchgegangen: Liste, Tag, Bestätigung, Weiterleitung** — Formular 75 ist Kopie von 71; Einstellungen nur im AC-Editor sichtbar, 09-einrichten.md: "einmal selbst durchspielen" offen.
- **Kette Formular → Tag → Automation von vorn nachgeprüft** — „0€ Nischengenerator“ (87) hat in AC 5 Mails (C0–C4) und das Ziel „Tool-Workshop gekauft“. Ob das Ziel ganz unten steht, zeigt nur der AC-Editor.
- **multientry geprüft, bevor ein Tag nachträglich gesetzt wird** — multientry einer Automation nur im AC-Editor einsehbar.
- **Beim Eintritt wird geprüft, ob sie schon in einer anderen Automation steckt** — Eintrittspruefung "laeuft gerade in" nur im AC-Editor sichtbar; mehrere Automationen laufen parallel (86, 87, 72).
- **Ein Ziel „hat gekauft“ in der Automation** — CLAUDE.md nennt Ziele "Produktwelt gekauft" (86) und "Tool-Workshop gekauft" (87); Lage unten nur im AC-Editor pruefbar.
- **Einwilligung, eigene Bestätigungsmail, Ränder am Handy** — Opt-in-Mail Formular 75 (Nachricht 718) nur im AC-Editor pruefbar; laut CLAUDE.md erst nach Speichern der Einstellungen aktiv.
- **Bestätigungsmail in deiner Stimme und ohne Angebot** — Text liegt in scripts/mails/bestaetigung-bauen.py, ob sie im Formular 75 wirklich eingetragen und aktiv ist, nicht ausserhalb AC pruefbar.
- **Auslieferung selbst getestet — mit einer echten Adresse eingetragen** — Testkauf/Eintragung mit echter Adresse ist nirgends dokumentiert und nicht ausserhalb pruefbar.

**Die Seiten**

- **Jeder Abschnitt hat seine eigene Hintergrundfarbe** — Abschnittsfarben nur im gerenderten Bild pruefbar; Live-Seite per curl geblockt, hier nicht per Browser angesehen.
- **Jemand ohne Vorwissen hat die Seite gelesen** — Lesetest durch Aussenstehende nicht dokumentiert.
- **Füllwörter gestrichen** — Lesearbeit am Text; texte-pruefen.py meldet 02-salespage.md sauber, Fuellwoerter prueft das Skript nicht.

**Die Mails**

- **Jede Mail einmal am Handy geöffnet** — Handy-Ansicht der Mails nicht ausserhalb des Postfachs pruefbar.

**Der Zulauf**

- **Mindestens ein geplanter Beitrag nennt das Stichwort** — Cockpit-Feed nicht lesbar; Dateien da: 06-feed.md (Reel + Karussell, NISCHE), pin-nische-Karussell, Storys im Skript.
- **Der Funnel ist dauerhaft sichtbar, nicht nur in einer Story** — Highlight, Bio-Link und Pin liegen auf Instagram bzw. im Cockpit, nicht lesbar; nur pin-nische als Pin-Karussell-Datei vorhanden.
- **Selbst Nachrichten geschrieben, nicht nur gewartet** — Eigene Nachrichten/DMs sind nirgends dokumentiert und nicht pruefbar.
- **90 Prozent geht kostenlos raus** — Verhaeltnis gratis/Verkauf im Feed nicht lesbar (Cockpit).

**Der Launch**

- **In der Aufwärmphase wird nicht gesagt, was kommt** — Inhalt der Storys 26.-29.10. nicht gegen die Regel geprueft; Story-Dateien stehen nur im Cockpit.
- **In der Bio steht während des Launches nur ein Link** — Bio-Link liegt auf Instagram, nicht lesbar.
- **Ein Highlight ist farbig markiert und vollgepackt** — Highlights liegen auf Instagram, nicht lesbar.
- **Ein Beitrag zum Launch ist angepinnt** — Angepinnter Beitrag auf Instagram nicht lesbar; pin-nische bewirbt den Nischengenerator, nicht den Workshop.
- **Alles zeigt in dieselbe Richtung** — Storys verlinken abwechselnd Workshop und Nischengenerator (05-storys.md), Feed/Bio nicht lesbar.

**Nach dem Start**

- **Eintragungen je Beitrag ausgerechnet** — Noch keine Messung: Kasse seit 29.10., Zahlen kommen erst im Funnel-Reiter (funnel.json hat keinen NISCHE-Eintrag).
- **Verstanden, was die Zahl misst** — Auswertung noch nicht gelaufen.
- **Weiter über das Angebot reden, auch wenn der Funnel läuft** — Storys bis 30.11. geplant (05-storys.md), tatsaechliches Posten nicht pruefbar.
- **Bei Flaute unterschieden: zu wenig Klicks oder zu wenig Käufe** — Noch zu frueh, keine Klick- und Kaufzahlen.

## ✅ belegt (44)


**Bevor du baust**

- **Aufgeschrieben, wo die Treppe heute endet** — active-funnels.json tool-workshop: produkttreppe_anschluss "Digitale Produktwelt 333 (Pitch-Serie B3-B7, Evergreen)"; 00-bauplan.md "Naechste Stufe in den Mails".
- **Das Ziel ist das grosse Produkt, nicht dieser Funnel** — active-funnels.json: Anschluss Digitale Produktwelt 333; Mails B3-B7 (mails-bauen.py) pitchen sie.
- **Das Anschluss-Angebot steht fest** — active-funnels.json tool-workshop: produkttreppe_anschluss gesetzt (Digitale Produktwelt 333).
- **Das Thema ist breit genug für oben im Trichter** — 00-bauplan.md: Minikurs 39 mit klarem Ziel (Tool + Seite); Zielgruppe bewusst auch reine Network-Frauen, Nischengenerator als breiter Einstieg.
- **Das 0€-Produkt ist stark genug, um Vertrauen zu erzeugen** — Nischengenerator ist KI-Tool mit Themenlandkarte und Tool-Ideen (09-einrichten.md), Anmeldeseite WP 4441 veroeffentlicht (wp-api get-page).
- **Der Funnel steht in active-funnels.json** — context/active-funnels.json: Eintrag id tool-workshop mit Kasse 53/54, Bump, Upsell, Downsell, Tag 107, Automation 86.
- **Der Preis nach den eigenen Stufen gesetzt** — 00-bauplan.md: "39 CHF (Minikurs-Preis, Patricia 29.10.)", Minikurse fix 39 in der Treppe.
- **Preis endet auf 7, 9 oder ist eine Schnapszahl** — Preis 39 CHF / 39 EUR endet auf 9 (thrivecart.json Produkt 53/54).

**Die Kasse**

- **Ein Order Bump hängt am Checkout** — thrivecart.json: Bump "Finde dein Thema ..." 25 CHF an Produkt 53, 25 EUR an 54.
- **Ein Upsell kommt direkt nach dem Kauf** — thrivecart.json Produkt 53/54: upsells ["Instagram-Kundenmaschine (Copy 1)"], Upsell 8 = 199.
- **Der Bump ergänzt das Hauptprodukt, das Upsell darf etwas Neues sein** — 03-kasse.md Bump-Text: "Finde dein Thema" vor dem Tool-Bau; Upsell Kundenmaschine ist bewusst ein neuer Kurs.
- **Bump-Preis im Fenster 17 bis 37** — Bump 25 CHF / 25 EUR liegt im Fenster 17-37 (thrivecart.json).
- **Upsell vor dem Downsell angelegt** — thrivecart.json: Upsell 8 (199) und Downsell 5 (39) beide an Produkt 53 und 54 verknuepft.
- **Der Kauf löst die Mail automatisch aus** — Automation „Tool-Workshop“ (86) hat in AC genau 8 Mails (B0–B7) und das Ziel „Digitale Produktwelt gekauft“ (über /automations/86/blocks geprüft, 31.10.).
- **Bump-Text nach der passenden Bauart** — 03-kasse.md Stand 30.10.: Bump-Text im Mini-Programm-Aufbau mit Ueberschrift, drei Haken, Preiszeile, Mockup.
- **Ein Downsell fängt die Ablehnung auf** — thrivecart.json: Downsell 5 Startklar 39 an Produkt 53/54, guenstiger als Upsell 199.
- **Die Auslieferung führt auf eine Seite, nicht direkt aufs PDF** — 03-kasse.md: Learn-Kurs 235282 plus Danke-Seite /tool-workshop-danke/ (WP 4460 publish) mit Webinar-Block.

**ActiveCampaign**

- **0€ läuft über ein Formular im Mailtool, nicht über die Kasse** — Nischengenerator (0 Euro): AC-Formular 75, Tag 0 Euro Nischengenerator 108, Liste 2 (09-einrichten.md); Workshop selbst ist bezahlt.
- **Die Liste passt zum Profil** — 09-einrichten.md: Formular 75 an Liste 2 (Mentoring); mails-bauen.py: Workshop-Kaeuferinnen Liste 16 Kunden.
- **Genau EIN Eintrags-Tag, benannt „0€ &lt;Name&gt;“** — Nischengenerator: ein Tag "0 Euro Nischengenerator" (108); Workshop: Tag Tool-Workshop 107 (active-funnels.json).
- **Der Tag ist über die ID eingetragen, nicht über den Namen** — active-funnels.json tool-workshop ac_integration: eintrag_tag_id 107.
- **Die drei Listen sind sauber getrennt** — mails-bauen.py: Launch A1-A3 an Liste 2 (Interessenten), B-Mails an Liste 16 (Kunden), active-funnels.json liste 16.
- **Zwischen Kauf und Pitch liegt eine Wartezeit** — kopierseite-bauen.py: B0 sofort, Pitch Digitale Produktwelt erst B4 ab Mo 16.11., zwei Tage nach B3 (Sa 14.11.).
- **In der Nachricht stehen zwei Links, nicht einer** — 07-automation.md DM: zwei Links, Nischengenerator-Seite und Tool-Workshop-Seite.

**Die Seiten**

- **Landingpage ist erreichbar** — wp-api get-page 4436: status publish, link mumlifebalance.ch/tool-workshop/, Inhalt vom 29.10. (nicht per Browser aufgerufen).
- **Checkout-Status geprüft: live, nicht test oder disabled** — thrivecart.json Stand 2026-10-31: Produkt 53 und 54 status "live", 39 CHF bzw. 39 EUR.
- **Danke-Seite steht und führt weiter** — wp-api get-page 4460 publish: Termine, Vorbereitung, Link Nischengenerator, Block MBA-Webinar-Replay.
- **Die Danke-Seite passt zur Bestätigung** — Danke 4460: "gleich eine Mail mit den Zoom-Links"; Kauf loest B0 aus (Automation 86), keine Bestaetigungsmail noetig.
- **Entschieden: eigene Verkaufsseite oder nur die Kasse** — 00-paket.md: eigene Anmeldeseite WP 4436 plus Kasse 53; Entscheid dokumentiert in 02-salespage.md.
- **Der Kaufknopf ist ohne Scrollen zu sehen** — WP 4436: Hero hat Ueberschrift, Mockup-Bild und Knopf "Ich bin dabei 39 CHF / 39 EUR" (Anker #preis).

**Die Mails**

- **Die Betreffzeile ist ein Hook** — A1 "Ein PDF wird heruntergeladen, ein Tool wird benutzt", B4 Zitat-Betreff, B7 "Ich lass dich jetzt in Ruhe" (mails/*.html); B0/B1 sind Info-Betreffs.
- **Der Abstand ist nicht täglich und nicht zu lang** — kopierseite-bauen.py GRUPPEN: B3 Sa 14.11., B4 Mo 16., B5 Mi 18., B6 Fr 20., B7 So 22.11.; C-Serie 1-2 Tage Warten.
- **Der Link steht weit oben** — A1-A3 und B4-B7: Knopf nach wenigen Absaetzen, nicht erst im Schluss (mails/*.html).
- **Der Einwand gegen das Format vorweggenommen** — A2 "Ich bin ueberhaupt nicht technisch" und C4 "Ich hab schon so viel probiert" nehmen die Einwaende vorweg.
- **Im Verkaufs-Funnel wird verkauft, im Newsletter nicht** — A1-A3, C1-C4 und B4-B7 sind Verkaufsmails mit einem Angebot, B0-B2 reine Organisation (mails/*.html).
- **Der Pitch nennt das Ziel hinter dem Ziel** — B5 "Du baust dein erstes eigenes Produkt neben dem Network"; C3 "Tuer zu Leuten, die dich noch nicht kennen" (mails/*.html).
- **Blacklisten-Prüfung gelaufen** — texte-pruefen.py --datei auf 04-mails.md, 02, 03, 06, 08: 0 muss weg, 1 Hinweis "Superlativ: nie wieder" in 04-mails.md.
- **Umlaute und Schweizer ss geprüft** — grep auf das Zeichen fuer scharfes s: kein Treffer in mails/*.html, angebot/*.md, salespages/tool-workshop/*.html.
- **Zwei Zielgruppen-Ebenen beachtet** — grep "deine Kundin|Kund:in" in mails und angebot: kein Treffer; Texte sprechen von Leuten und Menschen.

**Der Zulauf**

- **Anzeigen laufen aufs kleine Produkt, nicht auf den grossen Kurs** — 08-anzeigen.md: Ziel mumlifebalance.ch/tool-workshop/ (39), Freebie als Einstieg separat; ob die Kampagne laeuft, entscheidet Patricia.
- **Telegram-Gruppe verlinkt, falls es eine gibt** — B0-willkommen.html verlinkt die Begleitungs-Gruppe (WhatsApp) fuer 12.-14.11.

**Der Launch**

- **Entschieden: launchen oder droppen** — 00-bauplan.md: Kasse offen ab 29.10. bis 9.11. (Patricia 29.10.), ein Produkt, zwei Live-Tage; Entscheid dokumentiert.
- **Keine Lücke bis zum nächsten Launch** — Nach dem Workshop laeuft Digitale Produktwelt als Evergreen-Pitch B3-B7 (active-funnels.json), Storys bis 30.11. (05-storys.md).

**Nach dem Start**

- **Die Stimmen liegen an einer Stelle** — context/kundinnen-geschichten.md existiert als zentrale Ablage; 09-einrichten.md verweist darauf.

## ➖ trifft nicht zu (25)


**ActiveCampaign**

- **ManyChat reagiert auf alle drei Wege** — Stichwort NISCHE laeuft bewusst ohne ManyChat (07-automation.md), Antwort von Hand per gespeicherter Instagram-Antwort.
- **Ein Zähltag unterscheidet das erste vom zweiten Mal** — Kein ManyChat-Flow fuer NISCHE (07-automation.md), daher kein Zaehltag.
- **Je Link ein eigener Klick-Tag** — Kein ManyChat-Flow, Klick-Tags dort nicht moeglich (07-automation.md).
- **Nachgefasst, wenn 23 Stunden nichts passiert** — Kein automatischer DM-Flow, Nachfassen nur von Hand.
- **Bei einer Umfrage per Nachricht nur positive Antworten** — Keine Umfrage per Nachricht im Funnel vorgesehen.

**Die Seiten**

- **Bei einer langen Kundenstimme ist ein Satz hervorgehoben** — Keine Kundenstimme auf der Seite.

**Der Zulauf**

- **Das Stichwort löst nur beim gemeinten Wort aus** — Kein automatischer Ausloeser, Antwort von Hand (07-automation.md), daher keine Fehlausloesung.

**Der Launch**

- **Das Secret Offer sagt nicht, um was es geht** — Kein Secret Offer, Minikurs fix 39 (Patricias Regel).
- **Die Preisstufen haben die richtigen Abstände** — Keine Preisstufen, fixer Preis 39.
- **Rabattiert wird über die Leistung, nicht über den Preis** — Kein Rabatt vorgesehen, fixer Minikurs-Preis.
- **Bei Flaute die sechs Fragen durchgegangen** — Noch keine Flaute messbar, Kasse erst seit 29.10. offen.

**Das Webinar**

- **Das Thema ist breiter als das Produkt** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Der Titel folgt einer der drei Formeln** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Die neun Blöcke stehen im Skript** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Die Agenda dauert höchstens zwanzig Sekunden** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Frei gesprochen, mit Stichpunkten** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Zwischendurch immer wieder auf den Pitch gezeigt** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Die Zusammenfassung sagt, wie viel schon gegeben wurde** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Drei bis fünf Kundenstimmen, mit Bild und Namen** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Der Preisanker steht im Pitch** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Die drei Standardfragen am Schluss beantwortet** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Die Erinnerungen stehen** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.
- **Nach dem Webinar läuft eine Strecke mit Frist** — Funnel laeuft nicht ueber eine eigene Masterclass; der Live-Workshop ist das Produkt, das MBA-Webinar nur ein Zusatzblock.

**Nach dem Start**

- **Geteilte Tags nicht doppelt gezählt** — NISCHE und Tool-Workshop haben je einen eigenen Tag (108, 107), keine geteilten Tags.
- **Die Stimmen sind freigegeben** — Noch keine Stimmen vorhanden.

