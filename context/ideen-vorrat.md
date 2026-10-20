---
tags: [ideen, planung]
---

# Ideen-Vorrat — was noch nicht umgesetzt ist

Bis 16.10.2026 als Reiter „Ideenkasten“ im Cockpit. Patricia: *„ich muss das nicht sehen. es reicht, wenn du das bei dir im workflow gespeichert hast als idee“*. Gesammelt aus rund 100 Chats. **Wird gelesen von `/strategie` (Schritt Angebot & Warenkorb, `hebel`) und `/monatsplan` (Interview Frage 7 „was läuft nicht“)** — eine Idee von hier wird nie ungefragt gebaut, sondern als Vorschlag genannt. Erledigtes rausstreichen, Neues unten anhängen.

## Als nächstes

- **[Funnel · Aufwand mittel]** Automation für die 4 Brücken-Mails im Produkt-Ideen-Finder bauen
  Texte stehen in outputs/funnels/produkt-ideen-finder/mails-2-4-bruecke.md, Wiring in ac-einrichtung.md. Trigger-Tag 98, Ausschluss-Tag 79, Tag 8 → Tag 87.
- **[Funnel · Aufwand klein]** Kaufpreis-Tag für eigene-produkterstellung bestätigen
  Vermutlich Tag 43 — muss geprüft werden, sonst läuft der Ausschluss in der Brücken-Automation ins Leere.
- **[Funnel · Aufwand klein]** manychat-keywords.md: ENERGIE ist falsch beschrieben
  Dort steht noch „Padlet-Link + Kur-Info Zurück zu deiner Energie". Tatsächlich liefert ENERGIE den 3-Tage-Energie-Kickstart, und die Kur ist abgelöst. Solange das drinsteht, bauen Skills CTAs auf ein Versprechen, das nicht eingelöst wird.
- **[Produkt · Aufwand mittel]** Masterclass „Vom Chat zur Mitarbeiterin“ · Do 8.10., 09:00, 45 Min, Zoom (verschoben 25.09., vorher Di 13.10. 20:00)
  Zeigt WAS möglich ist, nicht WIE (Patricia 25.09.). Kernbotschaft: KI personalisieren + ihr genau sagen, was zu tun ist, ohne jedes Mal neu zu überlegen. Ablauf: 0–5 wer da ist · 5–25 Mitschauen: Cockpit, Assistenten, wie ein Skill entsteht, Kochbot (Menüplanung 1–2 Std → 5–10 Min) · 25–35 was in meinen 18 Stunden drin ist und warum das nur mit KI geht · 35–45 Angebot KI-Kurs 277, Bonus Skill-Rückmeldung bis Sa 10.10. 21:00, „In der MBA ist er gratis dabei“, Fragen. Anmeldung: AC-Formular 69, Tag masterclass-ki-2026-10, Seite /ki-masterclass/. Aufzeichnung Do 16:00 per Mail. Einladungen 29.9. · 1.10. · 6.10.
- **[Technik · Aufwand klein]** Cockpit: der Karussell-Loader wirft fünf Felder weg
  profil, kommentar, kommentarStand, kommentarErledigt, kommentarAntwort werden gespeichert, aber beim Laden nicht zurückgelesen. Folge: jedes Karussell landet in der Mentoring-Spalte, und beim nächsten Speichern wird das Profil in der Datenbank geleert. Fix liegt fertig: scripts/cockpit/patch-karussell-profil.py — braucht nur ein Neu-Veröffentlichen.
- **[Technik · Aufwand klein]** Cockpit: der Freigabe-Knopf bleibt nach einem Fehler abgeschaltet
  Beim Freigeben setzt er disabled=true. Bleibt die Folien-Schleife hängen, bleibt er abgeschaltet — und jeder weitere Klick tut wortlos nichts. Genau das hat am 21.09. zwei Stunden gekostet. Er muss in jedem Fehlerfall wieder anspringen.
- **[Technik · Aufwand klein]** Cockpit: grün erst, wenn wirklich abgelegt ist
  textfrei wird als allererstes gesetzt, vor jeder Prüfung. Die Karte zeigt freigegeben, obwohl in freigaben nur „zurueckgezogen" steht und kein einziges Folienbild da ist. Dieselbe Falle wie am 16.09. bei der Uhrzeit: eine Erfolgsmeldung, die verdeckt, dass nichts passieren wird.
- **[Technik · Aufwand klein]** Zusätzlichen Einplan-Lauf um 06:00 einrichten (Patricia: „mach es morgen vormittag", 22.09.2026)
  freigaben-einplanen-2000 läuft alle zwei Stunden von 08:00 bis 22:00 — der erste Lauf des Tages kommt also NACH der Karussell-Vorgabezeit 07:30. Genau daran ist das Dienstags-Karussell am 22.09. gescheitert: letzter Lauf am 21.09. um 16:14, die Läufe um 18/20/22 Uhr fielen aus (App zu), der nächste kam um 07:59 — 29 Minuten zu spät. Ein 06:00-Lauf fängt das ab, solange die App läuft. Achtung: Titel und Doku sagen noch „20:00", der Cron ist längst 0 8,10,12,14,16,18,20,22.
- **[Technik · Aufwand klein]** Transkripte für „Expertin statt Verkäuferin“ erzeugen
  Der Kurs hat 13 Videos, aber keine Transkripte — deshalb steht er als einziger ohne Stichwörter im Kurs-Register. Die Videoschnitt-Pipeline kann das erledigen.
- **[Website · Aufwand klein]** Anker #zum-minikurs auf WordPress-Seite 4085 ist tot
  Der Link in der Mail zeigt auf eine Sprungmarke, die es auf der Seite nicht gibt.
- **[doTERRA · Aufwand gross]** 30-Tage-Energie-Routine fertig aufsetzen
  Offen: Landingpage, ThriveCart-Checkout, Entscheid RevitaZen ja oder nein. Solange das nicht steht, darf in keinem Beitrag ein Preis, ein Starttermin oder eine Frist stehen — die KW39-Beiträge bewarben noch die alte Kur mit Deadline 25.09.

## Idee

- **[Produkt · Aufwand mittel]** Minikurs „Dein eigenes Werkzeug" — bauen und verkaufen
  Patricias Idee vom 19.10.2026, nachdem der KI-Tool-Workshop der Mentorin abgeglichen war. Passt genau zwischen KI-Kurs (333) und Academy: Wer Arbeitsplatz, Skill und Bot hat, kann als Nächstes etwas bauen, das er selbst verkauft. Zwei Arten unterscheiden — eines, das im Browser rechnet (Quiz, Planer, Rechner, **keine laufenden Kosten**) und eines, das die KI anruft (Rappen je Benutzung). Der Unterbau liegt schon: Prompt 33 der Prompt-Bibliothek (Werkzeug mit sicherem Schlüssel), die Netlify-Prompts 31 und 32, und der Abgleich in `outputs/produkte/ki-treppe/10-abgleich-julia-claude-kurse.md` („KI Tool Workshop"). 🚨 **Nicht vor Dezember** — bis dahin sind 61 Videos des KI-Kurses aufzunehmen, und ein neues Produkt zu planen, während ein verkaufter Kurs noch nicht ausgeliefert ist, ist genau das Muster, das den Umsatz an Launches kettet. 🚨 Nie den Trick übernehmen, mit dem fremde Seiten trotz Urheberrechts-Warnung nachgebaut werden.
- **[Content · Aufwand klein]** Keyword-Karten (2 Folien) für die drei Werkzeuge mit laufender Automation
  Produkt-Ideen-Finder (STANDBEIN), Bio-Check (BIO), Freischaufeln (ZEITFENSTER). Nur diese drei, weil dort die Automation wirklich läuft. Bauweise B1 im Karussell-Arsenal. Höchstens ein bis zwei pro Woche.
- **[Content · Aufwand klein]** Gewinner nach zwei Wochen wiederholen
  Im beobachteten Vorbild-Feed laufen starke Beiträge nach rund zwei Wochen fast unverändert nochmal. Bei uns gibt es dafür keinen Schritt — der Monats-Repost greift erst nach vier Wochen und nur für Best-Performer.
- **[Content · Aufwand mittel]** Das greifbare Werkzeug ins Keyword-Angebot, statt „ich zeige dir, wie du …"
  Die zwei stärksten Beiträge im beobachteten Zeitraum waren lange Karussells, die eine Vorlage oder ein Tool versprachen (373 und 176 Kommentare) — deutlich stärker als jede Keyword-Karte. Patricia hat genau solche Werkzeuge; sie stehen aber selten im CTA.
- **[Content · Aufwand klein]** Mentoring-Feed und Storys zeigen diese Woche auf verschiedene Angebote
  Die Storys verkaufen Startklar, die Feed-Beiträge führen auf den Produkt-Ideen-Finder und ECHT1. Beides ist vertretbar (Feed wärmt an, Story verkauft) — es sollte nur eine Entscheidung sein und kein Zufall.
- **[Content · Aufwand klein]** Hütchenmethode in den Content holen
  Chat vom 07.07.2026: „vielleicht könnte man die hutmethode etwas reinnehmen?“ Steht als Lektion 2.3 in Mama-CEO.
- **[Content · Aufwand klein]** Hook-Idee: „Nichts für ungut …“
  Chat vom 31.07.2026: „hatte gerade eine mega geile hook idee: Nichts für ungut..“ — nie ausgebaut.
- **[Content · Aufwand klein]** Auflockerungs-Foto von dir fehlt in den Designs
  Chat vom 05.08.2026: „mir fehlt noch ein foto von mir als auflockerung.“
- **[Content · Aufwand mittel]** Einwand-Content: warum sie nicht mit Instagram anfangen
  Chat vom 24.08.2026: „könnten wir bei dem was sie nicht brauchen auf konkrete Einwände gehen, warum sie nicht mit Instagram anfangen?“
- **[Funnel · Aufwand mittel]** Keyword SICHTBAR hat keine Automation
  0€ Starterguide wird nur über ManyChat ausgeliefert, danach passiert nichts.
- **[Funnel · Aufwand mittel]** Keyword STORY hat keine Automation
  Story-Challenge liefert aus, aber es gibt keine Nurture-Strecke.
- **[Funnel · Aufwand mittel]** Keyword ZEITFENSTER hat keine Automation
  Freischaufeln läuft ohne Anschluss.
- **[Funnel · Aufwand klein]** Loop 1: Sprungbedingung für ideen-finder-durchlaufen ergänzen
  In Automation 72 fehlt die Bedingung bei „Springen zu M1“, sonst bekommen Leute aus dem Ideen-Finder die Strecke doppelt.
- **[Funnel · Aufwand klein]** Drei Listen stehen auf 0 Kontakten
  Quiz-Kontakte, MBA Webinar und Willkommenssequenz. Entweder ist das Wiring kaputt oder die Listen sind Karteileichen.
- **[Funnel · Aufwand mittel]** Freebie für Block 2 fehlt
  In den Chats vom 04. und 07.07.2026 zweimal gefragt: „für Block 2 fehlt mir doch aktuell noch ein geeignetes Freebie oder?“
- **[Produkt · Aufwand klein]** Storyideen als Order Bump für 19 statt als Einzelprodukt
  Chat vom 28.08.2026: „storyideen könnte man doch als orderbump für 19 anbieten — wäre ja viel mehr wert“ Heute hängt es umgekehrt: die Content-Box ist der Bump am Storyideen-Checkout.
- **[Produkt · Aufwand mittel]** Zwei MBA-fremde Kurse als Appetitmacher einsetzen
  Chat vom 02.08.2026: „Zwei davon sind NICHT in der MBA — wäre cool, wenn ich sie damit etwas gluschtig machen könnte“ Am MBA-Checkout hängt bis heute weder Bump noch Upsell.
- **[Produkt · Aufwand klein]** Powerslot-Finder umbenennen
  Chat vom 04.07.2026: „Könnte man den Powerslot finder anders benennen?“
- **[Reichweite · Aufwand mittel]** Kommentar-Assistent statt GrowProImpact — täglich 20 neue Beiträge aus der Zielgruppe, je ein Kommentarvorschlag mit echtem Bezug zum Inhalt. Patricia klickt durch und postet selbst.
  Ersatz für das GrowProImpact-Abo, aber bewusst OHNE Automatik. Auf fremden Beiträgen kommentieren und folgen gibt die offizielle Meta-API nicht her — Tools, die das tun, steuern Instagram über Browser oder interne Schnittstellen, gegen die Nutzungsbedingungen, Risiko ist Kontosperrung. Erlaubt und schneller: Vorschläge liefern, sie postet. Ein generischer KI-Kommentar schadet dem Ruf ohnehin mehr, als die Reichweite bringt. Offen: woher die Beitragsliste kommt (Hashtag-Scrape via Apify läuft schon, scripts/apify/). Notiert 24.09.2026 auf Patricias Wunsch.
- **[Technik · Aufwand mittel]** Umsatz aus outputs/finanzen in den Abgleich hängen
  Die Cashflow-Auswertungen liegen als Markdown vor und könnten in „Zahlen & Ziele“ landen, statt von Hand eingetippt zu werden.
- **[Technik · Aufwand klein]** Cockpit: Folienbilder werden auf 700'000 Zeichen gedrückt, die Datenbank nimmt 256 KB
  slideJpeg hört bei 700'000 auf herunterzurechnen — das liegt über dem Dokument-Limit. Bei einem Folienbild mit Foto kann die Ablage deshalb scheitern. scripts/cockpit/freigabe-folien.mjs macht es schon richtig (240 KB); im Cockpit fehlt es noch.
- **[Technik · Aufwand klein]** Eine doTERRA-Markenpalette, die kein Gold hat
  Vier Karussells standen auf brand „doterra" — den Wert kennt das Cockpit nicht, er fällt still auf Mentoring-Dunkelblau zurück. Die vorhandene Palette „oele" hat Gold als Akzent und verstösst damit gegen die Regel „kein Gelb". Es braucht eine echte doTERRA-Palette (Creme/Dunkelblau mit Orange) unter dem Schlüssel, der in den Daten steht.
- **[Technik · Aufwand klein]** Markenwechsel überschreibt den Handle
  Die Auswahl setzt handle = BRANDS[wert].handle mit. Dadurch stand am 21.09. der Mentoring-Handle auf einem doTERRA-Karussell — auf jeder der neun Folien. Der Handle sollte dem Profil folgen, nicht der Farbpalette.
- **[Technik · Aufwand mittel]** ThriveCart /transactions anbinden — echte Bump-Quote statt geraten
  Im „Weg zum Monatsziel" wird bewusst mit zwei Zahlen gerechnet, weil es keine gemessene Bump-Quote gibt. Die Schnittstelle hat /transactions; damit würde aus der Schätzung ein Wert.
- **[Technik · Aufwand mittel]** Visuals der einzelnen Kurse im Cockpit zeigen
  Chat vom 30.06.2026: „vielleicht könnte man bei den einzelnen kursen noch die visuals rein nehmen?“ Die Mockups liegen in den Kursordnern.
- **[doTERRA · Aufwand mittel]** 3-Tage-Energie-Kickstart entschlacken und umbenennen
  Patricias Befund: „der energie kickstart freebie ist zu sehr auf doterra produkte getrimmt". Dazu heisst der Link noch /hormone statt Energie. Das Freebie soll ohne Produktkauf funktionieren — sonst hält es nicht, was der CTA verspricht.
- **[doTERRA · Aufwand mittel]** Mini-Notfallapotheke als doTERRA-Freebie reaktivieren — Landingpage + Kommentar-Stichwort, CTA weg vom veralteten „Mama wird Hausapothekerin“
  Fertiges 10-Seiten-PDF liegt in OneDrive, war nirgends erfasst. Inhalt und offene Punkte: context/doterra/mini-notfallapotheke.md

## Erledigt

- **[Technik · Aufwand mittel]** ThriveCart anbinden
  Am 11.09.2026 angebunden: Produkte, Bumps, Upsells und Downsells kommen jetzt automatisch.
- **[doTERRA · Aufwand gross]** doTERRA-Zahlen ins Cockpit
  Rang-Tracker steht. Die Zahlen kommen aus dem Schlagdistanz-Bericht und werden monatlich von Hand angestossen.
