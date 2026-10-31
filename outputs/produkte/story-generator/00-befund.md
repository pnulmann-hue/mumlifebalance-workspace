---
tags: [produkt, funnel]
---

# Story-Generator gegen die Funnel-Checkliste

Geprüft am 31.10.2026, alle 138 Punkte. Derselbe Befund steht unter jedem Punkt auf der Funnel-Checkliste (Auswahl „Story-Generator“).

⚠️ veraltet oder falsch 12 · ❌ fehlt 55 · ❓ nicht prüfbar 5 · ✅ belegt 12 · ➖ trifft nicht zu 54

## ⚠️ veraltet oder falsch (12)


**Bevor du baust**

- **Aufgeschrieben, wo die Treppe heute endet** — context/active-funnels.json: produkttreppe_anschluss „offen — als Bump am Tool-Workshop vorgeschlagen“. Treppe hinter dem Tool nicht aufgeschrieben.
- **Der Name nennt das Ziel, nicht den Inhalt** — Name „Story-Generator“ nennt das Werkzeug; das Ziel steht nur in der Seitenüberschrift („Aus deinem Alltag wird eine Story, die verkauft“).

**Die Kasse**

- **Bump-Text nach der passenden Bauart** — 03-kasse.md ab Zeile 86: Bump-Text als Entwurf („Dein Tool bringt dir neue Leute…“), 🟠 ENTSCHEID, nicht in ThriveCart; dort läuft aktuell Bump „Finde dein Thema“.
- **Die Auslieferung führt auf eine Seite, nicht direkt aufs PDF** — Auslieferung laut texte.txt FAQ: Mail mit Tool-Link und Code, keine eigene Seite; Kasse fehlt. Tool-Link antwortet 302 auf den Vercel-Login.

**Die Seiten**

- **Landingpage ist erreichbar** — WP 4429 /story-generator/ hat status publish (CLAUDE.md: Entwurf), Knöpfe zeigen auf #CHECKOUT-CHF/#CHECKOUT-EUR; curl auf die Seite gibt 403 (WAF).
- **Der Produktname steht genau einmal auf der Seite** — WP-Inhalt nennt „Story-Generator“ vier Mal plus Logo im Kopf; Regel verlangt genau einmal im Bild.
- **Die sechs Blöcke stehen in dieser Reihenfolge** — Seite hat 11 Abschnitte (Problem, Ablauf, Bauplan, Regeln, Vergleich…), keinen Kundenstimmen-Block; Reihenfolge weicht von den sechs Blöcken ab.
- **Der Block „Das brauchst du nicht“ steht drin** — Kein eigener Block; nur FAQ „Brauche ich ein eigenes KI-Konto? Nein“ und „Muss ich mich mit KI auskennen? Nein“ (texte.txt).
- **Jede Adresse einmal wirklich aufgerufen** — Tool-Link antwortet 302 auf Vercel-SSO (Schutz an); #CHECKOUT-CHF/-EUR sind tot. AGB, Datenschutz, Impressum verlinkt (nicht aufgerufen).

**Die Mails**

- **Blacklisten-Prüfung gelaufen** — Seitentext ohne Treffer bei sondern/Garantie/Kundin (grep texte.txt); texte-pruefen.py-Lauf nicht belegt, Mails fehlen.

**Der Zulauf**

- **Der Preis steht in der Story** — Preis steht in Ads und Seite; in 05-storys.md nur Thema „Du brauchst keine Programmiererin (Story-Generator)“, Preis nicht belegt.

**Der Launch**

- **Entschieden: launchen oder droppen** — Nicht entschieden: laut Bauplan Bump am Tool-Workshop und Einzelverkauf per Ads, ohne Launch-Entscheid (active-funnels: launched_on null).

## ❌ fehlt (55)


**Bevor du baust**

- **Das Produkt wurde schon ein- bis dreimal live verkauft** — Noch nie verkauft: context/active-funnels.json story-generator status in-aufbau, launched_on null. Erst Test mit Tool-Workshop-Teilnehmerinnen oder Ads nötig.
- **Ein Problem, eine Verwandlung — in einem Satz** — Eintrag story-generator in context/active-funnels.json hat kein Feld problem/transformation; nur der Name „Alltag + Produkt → fertige Story“.
- **Das Ziel ist das grosse Produkt, nicht dieser Funnel** — Kein Ziel hinter dem 17er benannt (anschluss „offen“); Bauplan nennt DPW nur als Stufe nach dem Tool-Workshop, nicht nach dem Generator.
- **Das Anschluss-Angebot steht fest** — context/active-funnels.json: produkttreppe_anschluss „offen“. Anschluss festlegen und eintragen.
- **Im Ziel-Checkout nachgesehen, was dort als Upsell hängt** — Es gibt keine Kasse; als Bump im Tool-Workshop-Checkout (53) nicht geprüft, dort hängt laut 03-kasse.md Upsell Kundenmaschine 199 / Downsell 39.
- **Die Produkt-Tabelle ist ausgefüllt** — Keine Produkt-Tabelle mit den elf Spalten gefunden (weder Bauplan noch outputs/produkte). Anlegen.
- **Die Ist-Situation über vier Fragen gefunden** — Keine Vier-Fragen-Antworten dokumentiert; Seite und Ads stützen sich auf Marktzitat und Workbook 90 Storyideen (ads-Datei Zeile 7).
- **Die Prüffrage zum Preis beantwortet** — Nirgends begründet, dass das Ergebnis mindestens 17 wert ist; Seite argumentiert nur mit „weniger als ein Znacht“.
- **Der Return on Invest steht irgendwo als Satz** — Kein ROI-Satz (Zeit, Nerven, Verkäufe) auf Seite oder in Ads; Seite nennt nur „in unter 30 Sekunden“.
- **Ausgerechnet, wie viele Verkäufe das Ziel braucht** — Keine Verkaufsrechnung; ads-Datei Zeile 113: „Mit 17 allein rechnet sich Werbung kaum“, ohne Zahlen zum Ziel.
- **Erste Kundenstimmen beschafft, bevor die Seite steht** — Keine echte Stimme: ads-Datei „Es gibt noch keine echte Stimme zum Generator“; Seite hat keinen Stimmen-Block.

**Die Kasse**

- **Ein Order Bump hängt am Checkout** — Am Generator-Checkout kann noch nichts hängen, es gibt ihn nicht. Ads-Datei schlägt als Bump 90 Storyideen vor.
- **Ein Upsell kommt direkt nach dem Kauf** — Keine ThriveCart-Kasse: thrivecart.json/katalog.json enthalten nur storyideen und story-challenge, nichts zum Generator. Upsell nicht geplant.
- **Jedes Zusatzangebot trägt seinen eigenen Streichpreis** — Bump-Entwurf in 03-kasse.md nennt nur „17 statt einzeln“, keinen Streichpreis für den Generator-Bump.
- **Upsell vor dem Downsell angelegt** — Keine ThriveCart-Kasse: thrivecart.json/katalog.json enthalten nur storyideen und story-challenge, nichts zum Generator.
- **Je Upsell und Downsell ein eigener Tag im Mailprogramm** — Kein Upsell/Downsell geplant, damit auch keine Tags in ActiveCampaign.
- **Die Auslieferungstexte der Kasse sind übersetzt** — Keine ThriveCart-Kasse: thrivecart.json/katalog.json enthalten nur storyideen und story-challenge, nichts zum Generator. Euro-Variante (17 €) laut Seite geplant, nicht angelegt.
- **Der Kauf löst die Mail automatisch aus** — Keine Kasse, keine Automation; Seite verspricht „Mail mit dem Link und deinem Zugangscode“ nach dem Kauf.
- **Checkout und Upsell-Seite am Handy angesehen** — Keine ThriveCart-Kasse: thrivecart.json/katalog.json enthalten nur storyideen und story-challenge, nichts zum Generator.

**ActiveCampaign**

- **Die Liste passt zum Profil** — Keine Liste für Käuferinnen festgelegt; Bauplan nennt für den Workshop Liste Kunden, für den Generator nichts.
- **Kette Formular → Tag → Automation von vorn nachgeprüft** — Kette Kasse → Tag → Automation nicht angelegt (keine Kasse).
- **Genau EIN Eintrags-Tag, benannt „0€ &lt;Name&gt;“** — Kein Tag für den Generator in context/active-funnels.json oder AC; benennen und eintragen.
- **Der Tag ist über die ID eingetragen, nicht über den Namen** — Ohne Tag keine Tag-ID im Funnel-Register.
- **multientry geprüft, bevor ein Tag nachträglich gesetzt wird** — Keine Automation vorhanden, multientry offen.
- **Beim Eintritt wird geprüft, ob sie schon in einer anderen Automation steckt** — Keine Automation, keine Eintrittsprüfung.
- **Ein Ziel „hat gekauft“ in der Automation** — Keine Automation; Ziel „Story-Generator gekauft“ nicht angelegt.
- **Zwischen Kauf und Pitch liegt eine Wartezeit** — Keine Nachkauf-Strecke und kein Anschlussangebot definiert.
- **Entschieden, was mit denen passiert, die nicht kaufen** — Nichts zu Nicht-Käuferinnen entschieden (Ads-Traffic ohne Liste).
- **Auslieferung selbst getestet — mit einer echten Adresse eingetragen** — Nur Tool lokal mit Testcode geprüft (CLAUDE.md); echter Kauf mit Mail, Link und Code nicht möglich, Kasse fehlt.

**Die Seiten**

- **Checkout-Status geprüft: live, nicht test oder disabled** — Es gibt keine Kasse, Status nicht prüfbar; Seitenknöpfe sind Platzhalter.
- **Danke-Seite steht und führt weiter** — Keine Danke-Seite nach dem Kauf; auch im Bauplan nicht angelegt (nur Workshop-Danke WP 4460).
- **Die Danke-Seite passt zur Bestätigung** — Keine Danke-Seite, keine Auslieferungsmail.
- **Jemand ohne Vorwissen hat die Seite gelesen** — Kein Gegenlesen durch eine Person ohne Vorwissen dokumentiert.

**Die Mails**

- **Jede Mail einmal am Handy geöffnet** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Die Betreffzeile ist ein Hook** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Genau ein Aufruf je Mail** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Der Abstand ist nicht täglich und nicht zu lang** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Der Link steht weit oben** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Die Willkommensmail zeigt die ganze Welt** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Der Baustein „… und das ohne …“ ist drin** — Kein Mailtext vorhanden; auf der Seite fehlt der Baustein „… und das ohne …“ als Satz ebenfalls.
- **Der Einwand gegen das Format vorweggenommen** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe). Einwand „Klingt nach KI“ nur im FAQ der Seite.
- **Irgendwo in der Strecke steht ein 48-Stunden-Angebot** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Für die, die nicht gekauft haben, läuft eine eigene Strecke** — Keine Strecke für Nicht-Käuferinnen.
- **Keine einzige Mail ohne Link** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Jeder Knopf führt irgendwohin** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe). Auf der Seite zeigen beide Kaufknöpfe auf #CHECKOUT-…-Platzhalter.
- **Im Verkaufs-Funnel wird verkauft, im Newsletter nicht** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Der Pitch nennt das Ziel hinter dem Ziel** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe).
- **Keine festen Datumsangaben in einer Dauer-Automation** — Keine Mail für den Story-Generator angelegt (kein Eintrag in outputs/produkte/tool-workshop/mails oder ac-entwuerfe). Seite und Ads enthalten keine festen Daten (gut).

**Der Zulauf**

- **Mindestens ein geplanter Beitrag nennt das Stichwort** — Kein Stichwort für den Generator; 05-storys.md erwähnt ihn nur als Story-Thema (6.11., 14.–30.11.). Feed-Beitrag mit Link fehlt.
- **Der Funnel ist dauerhaft sichtbar, nicht nur in einer Story** — Kein Bio-Link, Highlight oder Pin zum Generator geplant; Seite zeigt auf keine Kasse.

**Nach dem Start**

- **Eintragungen je Beitrag ausgerechnet** — Kein Tag, kein Stichwort, keine Zahlen.
- **Kundenstimmen aktiv eingeholt** — Keine Käuferinnen, kein Plan zur Stimmen-Anfrage; ads-Datei bestätigt: keine echte Stimme.
- **Ein Video-Testimonial gefragt** — Nicht gefragt, noch keine Nutzerinnen.
- **Die Stimmen liegen an einer Stelle** — context/kundinnen-geschichten.md enthält keine Stimme zum Generator.
- **Den Bestandskundinnen ein eigenes Angebot geschickt** — Kein Angebot an Bestandskundinnen geplant (Bump nur an Workshop-Käuferinnen).

## ❓ nicht prüfbar (5)


**ActiveCampaign**

- **Die drei Listen sind sauber getrennt** — Listenstruktur ist produktübergreifend, am Generator nicht prüfbar.

**Die Seiten**

- **Jeder Abschnitt hat seine eigene Hintergrundfarbe** — Farbwechsel nur im Browser prüfbar; WP-Seite per curl 403, nicht angesehen.
- **Füllwörter gestrichen** — Nicht belegt; CLAUDE.md nennt Prüfung durch /copywriting, kein Protokoll gefunden.

**Der Zulauf**

- **Selbst Nachrichten geschrieben, nicht nur gewartet** — Persönliche Nachrichten nicht aus Dateien prüfbar.
- **90 Prozent geht kostenlos raus** — Beitragsmix nicht für dieses Produkt prüfbar.

## ✅ belegt (12)


**Bevor du baust**

- **Das Thema ist breit genug für oben im Trichter** — texte.txt: „du ein Network-Produkt, ein Freebie oder einen eigenen Kurs hast“; breit genug für ein 17er-Tool.
- **Der Funnel steht in active-funnels.json** — context/active-funnels.json: id story-generator, 17 CHF, WP-Landing und Tool-URL eingetragen (Eintrag vom 31.10.).
- **Der Preis nach den eigenen Stufen gesetzt** — 00-bauplan.md Zeile 35: Bump 17 < Hauptprodukt 39; passt in die Stufen des Katalogs.
- **Preis endet auf 7, 9 oder ist eine Schnapszahl** — Preis 17 CHF / 17 € endet auf 7 (index.html, texte.txt, Ads).

**Die Kasse**

- **Der Bump ergänzt das Hauptprodukt, das Upsell darf etwas Neues sein** — 00-bauplan.md Zeile 35: Bump Story-Generator ergänzt den Tool-Workshop („nächstes Tool, das sie selbst nutzen kann“), noch 🟠 Entscheid.
- **Bump-Preis im Fenster 17 bis 37** — 17 CHF liegt am unteren Rand des Fensters 17–37 (00-bauplan.md, index.html).

**Die Seiten**

- **Entschieden: eigene Verkaufsseite oder nur die Kasse** — Eigene Verkaufsseite WP 4429 gebaut (outputs/salespages/story-generator/, story-generator-bauen.py).
- **Der Kaufknopf ist ohne Scrollen zu sehen** — WP 4429: Topbar-Knopf „Für 17 CHF / 17 € holen“ oben plus Hero-Knopf; funktioniert erst mit Kasse.
- **Ein FAQ beantwortet die Einwände** — texte.txt: 13 FAQ-Fragen (KI-Kenntnis, ChatGPT-Unterschied, Kamera-Scheu, Datenspeicherung, „Für wen ist das nichts?“).

**Die Mails**

- **Umlaute und Schweizer ss geprüft** — WP-Inhalt ohne ß; texte.txt echte Umlaute; Tool bietet Wahl Schweizer ss oder deutsche Schreibweise.
- **Zwei Zielgruppen-Ebenen beachtet** — system-prompt.md Z.76: „Zielgruppe nicht raten“, neutrale Person; Seite spricht Patricias Kundin als Du an, keine „deine Kundin“.

**Der Zulauf**

- **Anzeigen laufen aufs kleine Produkt, nicht auf den grossen Kurs** — outputs/ads/facebook-ads-story-generator-2026-10-28.md: Ziel Kauf 17 auf /story-generator/, kein grosser Kurs; Link noch nicht live.

## ➖ trifft nicht zu (54)


**Bevor du baust**

- **Das 0€-Produkt ist stark genug, um Vertrauen zu erzeugen** — Kein 0€-Produkt, sondern 17-CHF-Tool (Tripwire).

**Die Kasse**

- **Mehrere Bumps plus ein Bundle aus allen** — Tripwire für 17, Bundle nicht sinnvoll.
- **Ein Downsell fängt die Ablehnung auf** — Bei einem 17er-Tripwire kein Downsell nötig.
- **Bei 0€: alle drei Kassen besetzt** — Kein 0€-Produkt.
- **Das grosse Produkt steht im Funnel nie zum Normalpreis** — Das 17er ist nicht das grosse Produkt.

**ActiveCampaign**

- **0€ läuft über ein Formular im Mailtool, nicht über die Kasse** — Bezahlprodukt, kein 0€-Formular.
- **Kopiertes Formular ganz durchgegangen: Liste, Tag, Bestätigung, Weiterleitung** — Kein Formular im Spiel.
- **Einwilligung, eigene Bestätigungsmail, Ränder am Handy** — Kein Opt-in-Formular, Kauf über Kasse.
- **Bestätigungsmail in deiner Stimme und ohne Angebot** — Keine Opt-in-Bestätigung; Willkommensmail mit Code fehlt, siehe Mails.
- **ManyChat reagiert auf alle drei Wege** — Kein Stichwort-Funnel; kein Eintrag in context/manychat-keywords.md.
- **Ein Zähltag unterscheidet das erste vom zweiten Mal** — Kein ManyChat-Flow.
- **In der Nachricht stehen zwei Links, nicht einer** — Kein ManyChat-Flow.
- **Je Link ein eigener Klick-Tag** — Keine Nachrichtenstrecke mit Links.
- **Nachgefasst, wenn 23 Stunden nichts passiert** — Kein ManyChat-Flow.
- **Bei einer Umfrage per Nachricht nur positive Antworten** — Keine Umfrage per Nachricht.

**Die Seiten**

- **Seite nach dem Bestätigungsklick hinterlegt** — Kein Opt-in mit Bestätigungsklick.
- **Bei einer Frist: eigene Angebotsseite und eine „abgelaufen“-Seite** — Dauerangebot ohne Frist.
- **Bei einer langen Kundenstimme ist ein Satz hervorgehoben** — Keine Kundenstimme vorhanden.

**Die Mails**

- **Der Kurskäuferin wird das 0€-Webinar angeboten** — Kein Kurs, kein Webinar-Bezug.

**Der Zulauf**

- **ManyChat-Flow eingerichtet** — Kein Stichwort-Funnel vorgesehen, Verkauf über Link/Ads.
- **Das Stichwort löst nur beim gemeinten Wort aus** — Kein Stichwort.
- **Telegram-Gruppe verlinkt, falls es eine gibt** — Keine Telegram-Gruppe zum Generator.

**Der Launch**

- **Die fünf Phasen stehen im Kalender** — Dauerangebot (Tripwire), kein Launch geplant.
- **Die Aufwärmphase dauert rund eine Woche** — Dauerangebot (Tripwire), kein Launch geplant.
- **In der Aufwärmphase wird nicht gesagt, was kommt** — Dauerangebot (Tripwire), kein Launch geplant.
- **Das Secret Offer sagt nicht, um was es geht** — Dauerangebot (Tripwire), kein Launch geplant.
- **Die Preisstufen haben die richtigen Abstände** — Dauerangebot (Tripwire), kein Launch geplant.
- **In der Bio steht während des Launches nur ein Link** — Dauerangebot (Tripwire), kein Launch geplant.
- **Ein Highlight ist farbig markiert und vollgepackt** — Dauerangebot (Tripwire), kein Launch geplant.
- **Jeden Tag wird geteilt, wer schon dabei ist** — Dauerangebot (Tripwire), kein Launch geplant.
- **Ein Beitrag zum Launch ist angepinnt** — Dauerangebot (Tripwire), kein Launch geplant.
- **Alles zeigt in dieselbe Richtung** — Dauerangebot (Tripwire), kein Launch geplant.
- **Die Verknappung stimmt wirklich** — Dauerangebot (Tripwire), kein Launch geplant.
- **Rabattiert wird über die Leistung, nicht über den Preis** — Dauerangebot (Tripwire), kein Launch geplant.
- **Bei Flaute die sechs Fragen durchgegangen** — Dauerangebot (Tripwire), kein Launch geplant.
- **Keine Lücke bis zum nächsten Launch** — Dauerangebot (Tripwire), kein Launch geplant.

**Das Webinar**

- **Das Thema ist breiter als das Produkt** — Kein Webinar zum Story-Generator.
- **Der Titel folgt einer der drei Formeln** — Kein Webinar zum Story-Generator.
- **Die neun Blöcke stehen im Skript** — Kein Webinar zum Story-Generator.
- **Die Agenda dauert höchstens zwanzig Sekunden** — Kein Webinar zum Story-Generator.
- **Frei gesprochen, mit Stichpunkten** — Kein Webinar zum Story-Generator.
- **Zwischendurch immer wieder auf den Pitch gezeigt** — Kein Webinar zum Story-Generator.
- **Die Zusammenfassung sagt, wie viel schon gegeben wurde** — Kein Webinar zum Story-Generator.
- **Drei bis fünf Kundenstimmen, mit Bild und Namen** — Kein Webinar zum Story-Generator.
- **Der Preisanker steht im Pitch** — Kein Webinar zum Story-Generator.
- **Die drei Standardfragen am Schluss beantwortet** — Kein Webinar zum Story-Generator.
- **Die Erinnerungen stehen** — Kein Webinar zum Story-Generator.
- **Nach dem Webinar läuft eine Strecke mit Frist** — Kein Webinar zum Story-Generator.

**Nach dem Start**

- **Verstanden, was die Zahl misst** — Noch keine Messung.
- **Geteilte Tags nicht doppelt gezählt** — Kein Tag vorhanden.
- **Weiter über das Angebot reden, auch wenn der Funnel läuft** — Noch nicht live.
- **Bei Flaute unterschieden: zu wenig Klicks oder zu wenig Käufe** — Noch nicht live.
- **Die Stimmen sind freigegeben** — Keine Stimmen vorhanden.
- **Entschieden: weiterlaufen lassen, nachschärfen oder abstellen** — Noch nicht live.

