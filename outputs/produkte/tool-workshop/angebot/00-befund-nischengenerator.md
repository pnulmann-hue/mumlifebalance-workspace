---
tags: [produkt, funnel]
---

# Nischengenerator gegen die Funnel-Checkliste

Geprüft am 31.10.2026, alle 138 Punkte. Derselbe Befund steht unter jedem Punkt auf der Funnel-Checkliste (Auswahl „Nischengenerator“).

⚠️ veraltet oder falsch 11 · ❌ fehlt 13 · ❓ nicht prüfbar 20 · ✅ belegt 45 · ➖ trifft nicht zu 49

## ⚠️ veraltet oder falsch (11)


**ActiveCampaign**

- **Zwischen Kauf und Pitch liegt eine Wartezeit** — C0 (sofort) enthält schon den Knopf „Zum Tool-Workshop“, C1 folgt nur 1 Tag danach (mails-bauen.py: „1 Tag nach C0“)
- **ManyChat reagiert auf alle drei Wege** — angebot/07-automation.md: nur Kommentar NISCHE → DM; ManyChat gar nicht im Einsatz, Antwort von Hand gespeichert, Story-Antwort und DM-Auslöser fehlen

**Die Seiten**

- **Bei einer Frist: eigene Angebotsseite und eine „abgelaufen“-Seite** — Frist 9.11. nur im Text: 4442 nennt „Live am 10. und 11. November“, keine Abgelaufen-Seite; Umstellung nach 11.11. nur als To-do (09-einrichten.md Z. 57)
- **Die sechs Blöcke stehen in dieser Reihenfolge** — 4441: Hero · Wo du stehst · So läuft es · Anmelden · Wer dahintersteht · FAQ; es fehlen Kundenstimme und Soll-Situation, Reihenfolge anders

**Die Mails**

- **Genau ein Aufruf je Mail** — C0-tool-ideen-willkommen.html hat zwei Knöpfe: „Zum Nischengenerator“ und „Zum Tool-Workshop, 39 Franken oder 39 Euro“
- **Der Abstand ist nicht täglich und nicht zu lang** — mails-bauen.py: C1 „1 Tag nach C0“, danach je 2 Tage; erster Abstand täglich
- **Die Willkommensmail zeigt die ganze Welt** — C0 nennt nur den Tool-Workshop, nicht drei Angebote mit je einem Satz Pitch
- **Irgendwo in der Strecke steht ein 48-Stunden-Angebot** — Echte Frist 9.11. in C3 (P.S.) und A3, aber kein Rabatt, 39 CHF bleibt gleich
- **Keine festen Datumsangaben in einer Dauer-Automation** — C3: „Die Anmeldung ist offen bis Montag, 9. November, 23:59“; C1/C4 „10. November“, „11. November“: in Dauer-Automation 87 ab 12.11. falsch

**Der Zulauf**

- **ManyChat-Flow eingerichtet** — NISCHE fehlt in context/manychat-keywords.md; Antwort laut 07-automation.md von Hand gespeichert, 09-einrichten.md Z. 27 erledigt, Z. 56 offen (widersprüchlich)
- **Das Stichwort löst nur beim gemeinten Wort aus** — NISCHE ist ein Alltagswort („in meiner Nische“): bei Handantwort kein Auto-Auslöser, bei einem späteren Dienst braucht es eine Regel

## ❌ fehlt (13)


**Bevor du baust**

- **Ein Problem, eine Verwandlung — in einem Satz** — active-funnels.json, Eintrag nischengenerator: keine Felder problem und transformation, nur typ und Anschluss
- **Die Produkt-Tabelle ist ausgefüllt** — angebot/00-bauplan.md hat die Tabelle nur für den Tool-Workshop; für den Nischengenerator keine elf Spalten (Pitch, Story, Glaubenssätze …)
- **Die Ist-Situation über vier Fragen gefunden** — Seite 4441 hat Block „Wo du gerade stehst“ mit drei Aussagen, aber nirgends die vier Fragen (nachts wach, morgens, Angst, Aufschieben)
- **Ausgerechnet, wie viele Verkäufe das Ziel braucht** — Nirgends gerechnet, wie viele Eintragungen nötig sind, damit der Workshop (39) sein Ziel erreicht; gehört in angebot/00-bauplan.md
- **Erste Kundenstimmen beschafft, bevor die Seite steht** — Seite 4441 und Mails ohne Kundenstimme zum Nischengenerator; nur Patricias eigene Zahlen in C1

**ActiveCampaign**

- **Entschieden, was mit denen passiert, die nicht kaufen** — mails-bauen.py: nach C4 (+7 Tage) endet Automation 2, kein Folgeweg für Nicht-Käuferinnen; ab 12.11. müsste C1–C4 auf Aufzeichnung
- **In der Nachricht stehen zwei Links, nicht einer** — angebot/07-automation.md: DM-Text „Hallo du! Hier ist dein Nischengenerator: …“ nennt nur einen Link, kein „arbeite mit mir“

**Die Seiten**

- **Der Block „Das brauchst du nicht“ steht drin** — 4441 hat keinen Block „Das brauchst du nicht“, nur FAQ „Brauche ich ein Konto bei Claude …? Nein“

**Die Mails**

- **Der Baustein „… und das ohne …“ ist drin** — C4 hat „Das bekommst du“, aber kein „… und das ohne …“ (kein Code, keine Vorkenntnisse); gehört in C2 oder C4

**Nach dem Start**

- **Eintragungen je Beitrag ausgerechnet** — outputs/cockpit/abgleich/funnel.json und katalog.json enthalten keine Zeile NISCHE; Auswertung Eintragungen je Beitrag nicht eingerichtet
- **Kundenstimmen aktiv eingeholt** — Keine Stimmen zum Nischengenerator gesammelt; Antworten auf das P.S. in C0 („Antworte mit deinem Experten-Satz“) als Quelle nutzen
- **Ein Video-Testimonial gefragt** — Kein Video-Testimonial zum Nischengenerator
- **Entschieden: weiterlaufen lassen, nachschärfen oder abstellen** — Nur To-do „nach dem 11.11. Workshop-Kasten umstellen“ (09-einrichten.md Z. 57), keine Entscheidung weiterlaufen/nachschärfen/abstellen mit Datum

## ❓ nicht prüfbar (20)


**ActiveCampaign**

- **Kopiertes Formular ganz durchgegangen: Liste, Tag, Bestätigung, Weiterleitung** — Formular 75 ist laut CLAUDE.md Kopie von 71; Einstellungen in AC nicht lesbar. angebot/09-einrichten.md nennt Tag, Liste 2 und Mail 718 gesetzt
- **Kette Formular → Tag → Automation von vorn nachgeprüft** — AC nicht lesbar. active-funnels.json nennt konsistent Formular 75, Tag 108, Automation 87; nicht gegen AC verglichen
- **multientry geprüft, bevor ein Tag nachträglich gesetzt wird** — Automation 87 in AC nicht lesbar; das Tool setzt den Tag 108 bei jedem Durchgang erneut (api/ideen.js eintragen), ob Mehrfacheintritt greift, unklar
- **Beim Eintritt wird geprüft, ob sie schon in einer anderen Automation steckt** — Automation 87 nicht lesbar; Mehrfachlauf mit Workshop-Automation 86 nicht prüfbar
- **Ein Ziel „hat gekauft“ in der Automation** — CLAUDE.md: Automation 87 hat Ziel „Tool-Workshop gekauft“; ob es ganz unten steht, ist laut CLAUDE.md über die API nicht lesbar
- **Auslieferung selbst getestet — mit einer echten Adresse eingetragen** — Echter Durchlauf mit Adresse nicht prüfbar (kein Eintrag erlaubt)

**Die Seiten**

- **Jeder Abschnitt hat seine eigene Hintergrundfarbe** — nischengenerator-body.html: Abschnitte wechseln bg/bg2 laut Quelltext, gerendertes Bild nicht gesehen
- **Jemand ohne Vorwissen hat die Seite gelesen** — Kein Gegenleser nachweisbar
- **Füllwörter gestrichen** — texte-pruefen.py meldet „sauber“, Füllwörter-Streichung nicht belegbar
- **Jede Adresse einmal wirklich aufgerufen** — Tool-Adresse antwortet 200; WordPress-Seiten per REST gelesen (publish), Links der Seite (f/75, thrivecart, Impressum, AGB) nicht per Browser aufgerufen

**Die Mails**

- **Jede Mail einmal am Handy geöffnet** — Mails nur als HTML-Datei gelesen, nicht im Postfach am Handy

**Der Zulauf**

- **Anzeigen laufen aufs kleine Produkt, nicht auf den grossen Kurs** — angebot/08-anzeigen.md erwähnt den Nischengenerator nicht; kein Werbebudget auf das Freebie belegt
- **Selbst Nachrichten geschrieben, nicht nur gewartet** — Persönliche Nachrichten sind in keiner Datei belegt
- **Der Preis steht in der Story** — Storys liegen im Cockpit; 05-storys.md nennt keinen Preis je Story

**Der Launch**

- **In der Bio steht während des Launches nur ein Link** — Instagram-Bio nicht lesbar
- **Ein Highlight ist farbig markiert und vollgepackt** — Instagram-Highlights nicht lesbar
- **Ein Beitrag zum Launch ist angepinnt** — Pin-Karussell pin-nische ist gebaut, ob es angepinnt ist, im Cockpit/Instagram nicht lesbar

**Nach dem Start**

- **Verstanden, was die Zahl misst** — Tag 108 zählt Formular- und Tool-Eintragungen; Bedeutung für NISCHE nirgends festgehalten
- **Bei Flaute unterschieden: zu wenig Klicks oder zu wenig Käufe** — Noch keine Zahlen (seit 30.10. live), keine Klick-/Kaufauswertung
- **Die Stimmen liegen an einer Stelle** — context/kundinnen-geschichten.md existiert, enthält nichts zum Nischengenerator (nicht geprüft im Detail)

## ✅ belegt (45)


**Bevor du baust**

- **Aufgeschrieben, wo die Treppe heute endet** — active-funnels.json: produkttreppe_anschluss „→ Tool-Workshop 39 (bis 9.11.), danach Aufzeichnung“; danach B3–B7 zur Digitalen Produktwelt
- **Das Ziel ist das grosse Produkt, nicht dieser Funnel** — Mails C1–C4 und Danke-Seite 4442 führen auf den Tool-Workshop, die Evergreen-Strecke B3–B7 auf die Digitale Produktwelt
- **Das Anschluss-Angebot steht fest** — active-funnels.json: produkttreppe_anschluss „→ Tool-Workshop 39 (bis 9.11.), danach Aufzeichnung“
- **Das Thema ist breit genug für oben im Trichter** — Anmeldeseite 4441: „Finde dein eigenes Thema, das zu dir passt“, für alle Frauen im Network, kein Spezialthema
- **Im Ziel-Checkout nachgesehen, was dort als Upsell hängt** — katalog.json p-54: am Workshop-Checkout hängen Bump (Finde dein Thema) und Upsell; Stand in angebot/03-kasse.md. Euro-Kasse zeigt Upsell-Preis in CHF (prüfen)
- **Das 0€-Produkt ist stark genug, um Vertrauen zu erzeugen** — public/index.html + lib/thema-prompt.md: drei Themen, Experten-Satz, Produktbrücke, Tool-Ideen (KI, 10 Durchgänge). Kein Video, aber ein Ergebnis
- **Der Name nennt das Ziel, nicht den Inhalt** — Seite 4441: Titel „Nischengenerator — finde dein eigenes Thema“, H1 nennt das Ziel; Produktname nur als Marke
- **Der Funnel steht in active-funnels.json** — context/active-funnels.json, id nischengenerator: Landingpage, Tool, Danke-Seite, Tag 108, Formular 75, Automation 87

**Die Kasse**

- **Bei 0€: alle drei Kassen besetzt** — Danke-Seite 4442 (nach Formular), Bestätigungsmail führt direkt ins Tool, das Tool trägt den Workshop-Kasten (public/index.html workshopKasten)
- **Die Auslieferung führt auf eine Seite, nicht direkt aufs PDF** — Mail-Knopf führt auf die Tool-Seite mlb-nischengenerator.vercel.app (Antwort 200) mit Workshop-Angebot, nicht auf ein PDF

**ActiveCampaign**

- **0€ läuft über ein Formular im Mailtool, nicht über die Kasse** — active-funnels.json: formular 75, Liste 2, Tag 108; Anmeldeseite bettet activehosted.com/f/75 ein
- **Die Liste passt zum Profil** — active-funnels.json: liste 2 (Mentoring-Interessenten); api/ideen.js AC_LISTE ebenfalls Liste 2
- **Genau EIN Eintrags-Tag, benannt „0€ &lt;Name&gt;“** — active-funnels.json: eintrag_tag_name „0€ Nischengenerator“, ein Tag (108); api/ideen.js setzt denselben Tag
- **Der Tag ist über die ID eingetragen, nicht über den Namen** — active-funnels.json: eintrag_tag_id 108; api/ideen.js TAG = '108'
- **Die drei Listen sind sauber getrennt** — Liste 2 = Interessenten für die Anmeldung (active-funnels.json); Workshop-Käuferinnen via Tag 107, A1–A3 schliessen sie aus (mails-bauen.py wann)
- **Einwilligung, eigene Bestätigungsmail, Ränder am Handy** — scripts/mails/bestaetigung-bauen.py: Mail 75 „Ein Klick noch …“; Tool hat Einwilligungs-Häkchen (public/index.html #ja). Handy-Ränder nicht gesehen
- **Bestätigungsmail in deiner Stimme und ohne Angebot** — bestaetigung-bauen.py: Du-Form, Knopf %CONFIRMLINK%, %SENDER-INFO-SINGLELINE% im Fuss, kein Angebot

**Die Seiten**

- **Landingpage ist erreichbar** — WordPress REST: Seite 4441 status publish, /nischengenerator/; Tool mlb-nischengenerator.vercel.app antwortet 200
- **Danke-Seite steht und führt weiter** — WordPress REST: Seite 4442 publish, Workshop-Angebot 39 CHF · 39 € mit Knopf auf thrivecart.com/tool-workshop/
- **Die Danke-Seite passt zur Bestätigung** — 4442: „Mail mit dem Betreff ‚Ein Klick noch, dann findest du dein eigenes Thema‘“ = Betreff in bestaetigung-bauen.py (Formular 75)
- **Seite nach dem Bestätigungsklick hinterlegt** — 09-einrichten.md: „nach dem Klick weiter zum Tool“; das Tool zeigt Workshop-Kasten. Einstellung im Formular selbst nicht lesbar
- **Entschieden: eigene Verkaufsseite oder nur die Kasse** — Eigene Anmeldeseite 4441 für Formular-Eintrag und Bestätigung; Grund: Opt-in mit Bestätigung (angebot/07-automation.md)
- **Der Produktname steht genau einmal auf der Seite** — 4441: Logo „NISCHEN·GENERATOR“, H1 nennt das Ziel, Name danach nur im Anmeldeblock
- **Der Kaufknopf ist ohne Scrollen zu sehen** — 4441: Hero mit Knopf „→ Gratis loslegen“ (Anker #anmelden) direkt unter dem Pitch
- **Ein FAQ beantwortet die Einwände** — 4441: sechs Fragen (kostet es, Network verlassen, festlegen, keine Ausbildung, KI-Konto, Mailadresse)

**Die Mails**

- **Die Betreffzeile ist ein Hook** — mails-bauen.py: C1 „Drei Eintragungen aus 27 Beiträgen“, C3 „Die Liste, die ich für meinen Mann geschrieben habe“, Bestätigung „Ein Klick noch …“
- **Der Link steht weit oben** — C0: Knopf zum Tool vor dem Fliesstext; C1–C4 Knopf nach 2–4 Absätzen
- **Der Einwand gegen das Format vorweggenommen** — C2: „wenn du ‚Tool‘ liest und an Programmieren denkst, verstehe ich das gut“, mit Beispiel
- **Für die, die nicht gekauft haben, läuft eine eigene Strecke** — C1–C4 sind die Strecke für Nicht-Käuferinnen, Ausstieg über das Ziel „Tool-Workshop gekauft“ (CLAUDE.md)
- **Keine einzige Mail ohne Link** — C0–C4 und Bestätigungsmail tragen je mindestens einen Link (vercel.app, thrivecart.com/tool-workshop, %CONFIRMLINK%)
- **Jeder Knopf führt irgendwohin** — Hrefs in C0–C4: mlb-nischengenerator.vercel.app (200) und mumlifebalance.thrivecart.com/tool-workshop/, keine Platzhalter
- **Im Verkaufs-Funnel wird verkauft, im Newsletter nicht** — C1–C4 reine Pitch-Serie auf den Workshop (Problem, Geschichte, Angebot, P.S.), kein Newsletter-Mix
- **Der Pitch nennt das Ziel hinter dem Ziel** — C1: „Mit einem Tool reicht dir eine kleinere Reichweite für dieselbe Zahl an Kontakten“; C3: Tür zu neuen Leuten
- **Blacklisten-Prüfung gelaufen** — texte-pruefen.py --datei auf C0–C4, beide Seiten-Bodys und Pin-Caption: 8 Dateien, 0 Funde
- **Umlaute und Schweizer ss geprüft** — grep ß in C0–C4 und Seiten-Bodys: 0 Treffer; echte Umlaute
- **Zwei Zielgruppen-Ebenen beachtet** — grep „Kundin“ in C0–C4 und Seiten-Bodys: nur ein HTML-Kommentar in C2, im Text „deine Leute“; Tool-Prompt verbietet es

**Der Zulauf**

- **Mindestens ein geplanter Beitrag nennt das Stichwort** — outputs/karussells/pin-nische/caption.txt „Kommentier NISCHE“, angebot/06-feed.md zwei Lead-Posts mit NISCHE; Termine im Cockpit nicht lesbar
- **Der Funnel ist dauerhaft sichtbar, nicht nur in einer Story** — Gratis-Übersicht 4443 verlinkt den Nischengenerator; Pin-Karussell pin-nische gebaut. Bio-Link und Pin-Status nicht lesbar
- **90 Prozent geht kostenlos raus** — Tool liefert 3 Themen, Experten-Satz, Produktbrücke, Tool-Ideen gratis, 10 Durchgänge je Adresse (api/ideen.js MAX)

**Der Launch**

- **Alles zeigt in dieselbe Richtung** — 05-storys.md, 06-feed.md, Pin, Mails C0–C4: alles auf Nischengenerator → Workshop
- **Die Verknappung stimmt wirklich** — Frist 9.11. 23:59 und Termine 10./11.11. in 4442, C3, A3, Tool (LIVE_BIS 12.11.) einheitlich; keine erfundenen Plätze
- **Keine Lücke bis zum nächsten Launch** — angebot/05-storys.md plant 14.–30.11. mit Nischengenerator; Evergreen B3–B7 zur Digitalen Produktwelt ab 14.11.

**Nach dem Start**

- **Geteilte Tags nicht doppelt gezählt** — Tag 108 gehört nur dem Nischengenerator (active-funnels.json), kein geteilter Tag
- **Weiter über das Angebot reden, auch wenn der Funnel läuft** — angebot/05-storys.md: Nischengenerator in Storys 31.10.–30.11.; 06-feed.md drei Beiträge
- **Den Bestandskundinnen ein eigenes Angebot geschickt** — mails-bauen.py: A1–A3 an Liste 2 (Käuferinnen ausgeschlossen) bewerben den Workshop bei Bestandskontakten

## ➖ trifft nicht zu (49)


**Bevor du baust**

- **Das Produkt wurde schon ein- bis dreimal live verkauft** — 0-€-Freebie, wird nicht verkauft
- **Der Preis nach den eigenen Stufen gesetzt** — 0-€-Freebie, kein Preis
- **Preis endet auf 7, 9 oder ist eine Schnapszahl** — 0-€-Freebie, kein Preis
- **Die Prüffrage zum Preis beantwortet** — 0-€-Freebie, kein Preis
- **Der Return on Invest steht irgendwo als Satz** — 0-€-Freebie, kein Preis

**Die Kasse**

- **Ein Order Bump hängt am Checkout** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Ein Upsell kommt direkt nach dem Kauf** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Jedes Zusatzangebot trägt seinen eigenen Streichpreis** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Der Bump ergänzt das Hauptprodukt, das Upsell darf etwas Neues sein** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Mehrere Bumps plus ein Bundle aus allen** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Bump-Preis im Fenster 17 bis 37** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Upsell vor dem Downsell angelegt** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Je Upsell und Downsell ein eigener Tag im Mailprogramm** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Die Auslieferungstexte der Kasse sind übersetzt** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Der Kauf löst die Mail automatisch aus** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Bump-Text nach der passenden Bauart** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Ein Downsell fängt die Ablehnung auf** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)
- **Das grosse Produkt steht im Funnel nie zum Normalpreis** — Funnel führt auf Workshop 39, nicht aufs grosse Produkt
- **Checkout und Upsell-Seite am Handy angesehen** — Freebie für 0 €, keine eigene Kasse (Workshop-Kasse ist ein anderer Funnel)

**ActiveCampaign**

- **Ein Zähltag unterscheidet das erste vom zweiten Mal** — Stichwort läuft ohne ManyChat über gespeicherte Antwort (07-automation.md), kein Zähltag möglich
- **Je Link ein eigener Klick-Tag** — Gespeicherte Antwort in Instagram, ohne ManyChat kein Klick-Tag
- **Nachgefasst, wenn 23 Stunden nichts passiert** — Ohne ManyChat-Flow kein 24-Stunden-Fenster steuerbar
- **Bei einer Umfrage per Nachricht nur positive Antworten** — Keine Umfrage per Nachricht im Funnel

**Die Seiten**

- **Checkout-Status geprüft: live, nicht test oder disabled** — Freebie ohne Kasse; Workshop-Kasse (Produkt 53/54) steht laut katalog.json auf live
- **Bei einer langen Kundenstimme ist ein Satz hervorgehoben** — Keine Kundenstimme auf der Seite

**Die Mails**

- **Der Kurskäuferin wird das 0€-Webinar angeboten** — Kein Kauf, Freebie-Funnel

**Der Zulauf**

- **Telegram-Gruppe verlinkt, falls es eine gibt** — Für den Nischengenerator gibt es keine Gruppe (Workshop-Gruppe ist WhatsApp)

**Der Launch**

- **Entschieden: launchen oder droppen** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Die fünf Phasen stehen im Kalender** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Die Aufwärmphase dauert rund eine Woche** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **In der Aufwärmphase wird nicht gesagt, was kommt** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Das Secret Offer sagt nicht, um was es geht** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Die Preisstufen haben die richtigen Abstände** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Jeden Tag wird geteilt, wer schon dabei ist** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Rabattiert wird über die Leistung, nicht über den Preis** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie
- **Bei Flaute die sechs Fragen durchgegangen** — Launch-Punkt gehört zum Tool-Workshop, nicht zum Freebie

**Das Webinar**

- **Das Thema ist breiter als das Produkt** — Workshop, kein Webinar-Funnel
- **Der Titel folgt einer der drei Formeln** — Workshop, kein Webinar-Funnel
- **Die neun Blöcke stehen im Skript** — Workshop, kein Webinar-Funnel
- **Die Agenda dauert höchstens zwanzig Sekunden** — Workshop, kein Webinar-Funnel
- **Frei gesprochen, mit Stichpunkten** — Workshop, kein Webinar-Funnel
- **Zwischendurch immer wieder auf den Pitch gezeigt** — Workshop, kein Webinar-Funnel
- **Die Zusammenfassung sagt, wie viel schon gegeben wurde** — Workshop, kein Webinar-Funnel
- **Drei bis fünf Kundenstimmen, mit Bild und Namen** — Workshop, kein Webinar-Funnel
- **Der Preisanker steht im Pitch** — Workshop, kein Webinar-Funnel
- **Die drei Standardfragen am Schluss beantwortet** — Workshop, kein Webinar-Funnel
- **Die Erinnerungen stehen** — Workshop, kein Webinar-Funnel
- **Nach dem Webinar läuft eine Strecke mit Frist** — Workshop, kein Webinar-Funnel

**Nach dem Start**

- **Die Stimmen sind freigegeben** — Keine Stimmen vorhanden

