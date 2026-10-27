---
tags: [produkt, funnel, produktwelt]
---

# Befund: Trichter Digitale Produktwelt, November 2026

Erster Lauf von `/angebot trichter` (Teil B), am 27.10.2026.

Der Soll-Stand kommt aus `outputs/monatsplaene/2026-11-mentoring.md`:
- Lead-Challenge vom 9. bis 11.11. in einer WhatsApp-Gruppe
- Produkt-Ideen-Finder (STANDBEIN)
- Kasse DPW vom 23. bis 30.11. zu 333
- 199 gibt es nur auf den Danke-Seiten

Am 27.10. live gelesen habe ich die Kasse, `/angebote/`, `/lead-challenge/`, die drei Danke-Seiten und `/produkt-ideen-finder-los/`. Kasse und Lead-Challenge-Seite habe ich ein zweites Mal gegengeprüft. Die Abgleich-Dateien sind vom 26.10.

## Kurzfassung

Was passt:
- Kasse live, 333 einmalig oder 2 × 166.50
- Bump Kundenmaschine 199, also unter 333
- AGB verlinkt
- Storys vom 26.10. bis 30.11.
- Danke-Seiten live mit `DANKE199DPW`
- Kurs komplett aufgenommen

**Was nicht passt, nach Gewicht:**

| # | Befund | Fundstelle | Wer |
|---|---|---|---|
| 1 | ⚠️ **Die Kasse zeigt 16× Vorlagentext** „Enter your bullet points here“ und einen lateinischen Platzhalter „Ut Repellat Officiis Est Velit In Nisi“. Genau diese Seite öffnen die Frauen ab dem 23.11. | thrivecart.com/digitale-produktwelt/ | Patricia in ThriveCart, oder Claude über Chrome |
| 2 | ⚠️ **Die Kasse verkauft über Zahlen:** „6 Kapitel. 20 Lektionen. Lifetime-Zugang.“, dazu Modul 1–6 als Überschriften und in der FAQ „genau dafür ist Kapitel 1“ | Kasse; `outputs/salespages/thrivecart-kassen/digitale-produktwelt.md` Z. 39 | neu texten |
| 3 | ⚠️ **Die Lead-Challenge spricht überall von Telegram**, nie von WhatsApp: Landingpage („Telegram-Kanal · In deinem Tempo“), Bestätigungsmail, Mail der Automation „0€ Lead Challenge“ (47). Auch der Termin 9.–11.11. fehlt | `/lead-challenge/` · `outputs/funnels/bestaetigungsmails/lead-challenge.html` · AC 47 | flicken, sobald der WhatsApp-Link da ist |
| 4 | ⚠️ **Workbook Lead-Challenge, S. 13:** „NEU AB 6. APRIL … Zoom Gruppencall alle 2 Wochen … CHF 333 CHF 249 … Nur begrenzte Plätze“ | `context/freebies/mentoring/0-lead-challenge/lead-challenge.pdf` | Patricia (Canva), steht schon im Monatsplan |
| 5 | ❌ **Nach der Lead-Challenge kommt keine Mail mehr.** AC 47 hat genau eine Mail (Gruppenlink). Es gibt keine Begleitung, keinen Pitch und auch keine Mails für „Kasse offen“ und „letzter Tag“. Geplant sind nur WhatsApp-Texte | AC 47 · `2026-11-angebot-nach-der-lead-challenge.md` | **neu bauen** |
| 6 | ⚠️ **Zwei alte DPW-Automationen laufen noch aktiv:** „Vom Network-Wissen zum digitalen Produkt“ (48) verspricht Start am 6.4. und vier Live-Calls im Mai/Juni mit Zoom-Link. „Vom Network-Wissen zur digitalen Produktwelt“ (51) sagt „Starte mit Kapitel 1“. Ist 48 die Willkommensmail für Käuferinnen, bekommt eine Novemberkäuferin Termine aus dem Frühling | AC 48 Mail 416 · AC 51 Mail 426 | ❓ Auslöser prüfen, dann flicken |
| 7 | ⚠️ **Das Register zeigt aufs falsche Angebot:** Die Lead-Challenge führt laut `produkttreppe_anschluss` zu „Finde dein Thema 39“, `wordpress_landing` steht auf null. Die DPW hat keinen eigenen Funnel-Eintrag | `context/active-funnels.json` | Claude, flicken |
| 8 | ⚠️ **Der Produkt-Ideen-Finder pitcht nur den 39er.** Die DPW kommt in den Mails nicht vor, nur auf der Danke-Seite | `outputs/funnels/produkt-ideen-finder/` Mail 4 | ➖ passt zur Treppe, kein Muss |
| 9 | ❓ Feed-Beiträge November liegen noch nicht im Workspace (`outputs/content/` endet bei KW43) | — | läuft über `/content woche` |

Zum Einordnen der Zahlen:
- DPW-Käufe seit Februar in ThriveCart: **0**. Produkt 41 kommt in `umsatz.json` nicht vor.
- Eintragungen seit 30.06.: LEAD 2, STANDBEIN 2.
- Daraus folgt kein Urteil gegen das Produkt, denn es wurde nie richtig verkauft. Der Befund heisst: **Der Einstieg trägt noch nicht viel**, deshalb muss der Weg nach der Challenge umso dichter sein.

## Empfehlung je Baustein

| Baustein | Empfehlung | warum |
|---|---|---|
| Kasse DPW | **neu texten** (Kassentext) | Platzhalter und Zahlen. Preis, Bump und AGB bleiben |
| Verkaufsseite | **bleibt die Kasse**, ein eigener Seitenbau lohnt im November nicht | Die Danke-Seiten und `/angebote/` führen direkt auf die Kasse |
| Lead-Challenge-Landingpage + Bestätigungsmail + AC 47 | **flicken** | Telegram → WhatsApp, Termin rein. Die Struktur trägt |
| Workbook S. 13 | **flicken** (Patricia) | eine Seite |
| Mails nach der Challenge | **neu bauen** | Es gibt sie nicht. Nötig sind: drei Begleitmails vom 9. bis 11.11., eine Brücke bis zum 22.11. und drei Kassenmails am 23., 26. und 30.11. |
| AC 48 / 51 | **erst prüfen, dann flicken** | Auslöser unbekannt |
| Register | **flicken** | Anschluss → DPW 333, Landing eintragen, DPW-Eintrag anlegen |
| Neuer Trichter | **nein** | Lead-Challenge und Ideen-Finder passen genau zum Monatsfokus. Es fehlt der Weg dazwischen, kein Einstieg |

## Ausführliche Fundstellen

Kasse (ThriveCart 41):
- Status `live`, 333 einmalig oder Raten 2 × 166.50, keine Staffel
- Bump „Instagram-Kundenmaschine gleich dazu: 199 statt 333 CHF“, keine Upsells oder Downsells
- FAQ „Gibt es Live-Calls? Nein, der Kurs ist ein Selbstlernprogramm“, das passt
- Umgekehrt hängt die DPW als Bump an der Kundenmaschinen-Kasse. Dieser Preis ist nicht geprüft ❓

Verkaufsseite:
- `/digitale-produktwelt/` antwortet mit 404
- `/angebote/#aufbau` beschreibt die DPW ohne Preis und ohne Kapitelzahl und verlinkt auf die Kasse

Danke-Seiten:
- `/danke-lead-challenge/`, `/danke-businessfahrplan/` und `/danke-ideen-finder/` sind live korrekt (199 per Gutschein, keine Kapitelzahl)
- Die lokalen Exporte in `outputs/funnels/danke-seiten/*.html` Z. 391 nennen noch „6 Kapitel, 20 Lektionen“. Das ist nur die Exportdatei; beim nächsten `deploy-danke-seiten.mjs --vorschau` wird sie neu erzeugt

Stichwörter:
- LEAD und STANDBEIN sind in `manychat-keywords.md` eingetragen
- `manychat-flow-STANDBEIN.md` Z. 154 meldet „Minikurs-Link tot“ (Stand 10.09.). Die Kasse `/eigene-produkterstellung/` antwortet heute mit 200, die Notiz ist veraltet. Ob der Link im Werkzeug stimmt: ❓

Storys 26.10.–30.11.:
- 333 erst ab dem 23.11.
- Termine 9.–11.11. und 23.–30.11. stimmen
- keine Kapitelzahlen, keine Live-Calls

Produkt:
- 24 von 24 Lektionen transkribiert
- `00-UEBERSICHT…`, `01-status-audit.md` und `03-fehlende-lektionen-roadmap.md` sind vom April und veraltet („14 Lektionen fehlen“, „Start 6. April“). Es sind interne Notizen, nichts davon wird ausgeliefert

## Was dieser Lauf nicht geprüft hat

- Die 138 Punkte der Funnel-Checkliste habe ich nicht einzeln abgehakt. Geprüft wurde der Weg Baustein für Baustein, gegen den Monatsplan und gegen die Regeln, die quer gelten: Termine, Preise, Veränderung statt Zahlen. Die volle Punkt-Liste erzeugt `python scripts/cockpit/funnel-checkliste-bauen.py --punkte`.
- Ob die ausgelieferte Workbook-Fassung dieselbe Datei ist wie im Workspace: ❓
- Der ManyChat-Flow STANDBEIN im Werkzeug selbst: ❓

## 🔗 Verwandte Notizen

- [[2026-11-mentoring]]
- [[2026-11-angebot-nach-der-lead-challenge]]
