---
tags: [produkt, funnel, jahresplanung]
---

# Bauplan · Neustart 2027 · Jahresplanungs-Workshop

> Die eine Quelle für Name, Termine, Stichwort und Anschluss. Jeder Baustein übernimmt die Werte von hier.
> Gebaut am 31.10.2026. Patricia: *„ich bitte dich, direkt in meiner planung zu berücksichtigen, dass ich den
> einplanen will, mir auch ein cooles mockup vorzuschlagen und den effekt einzubauen aber was passendes zum
> neujahr. neustart oder sowas und nehme es in die planung auf und rechne rückwärts.“*
> Entscheide vom 31.10. (gesammelte Runde): **gratis · AC-Formular · 09:00 · Aufzeichnung unbefristet ·
> Anschluss MBA, die Januar-Challenge fällt weg.**
> Alles mit **🟠 ENTSCHEID** hat Claude gesetzt und muss einmal bestätigt werden.
> **Freigegeben am 01.11.2026** (Patricia: „Ja, so freigeben“): Name, Stichwort NEUSTART, 90 Minuten, MBA zu 997 ohne Workshop-Preis.
> Offen bleiben nur Aufzeichnungsort und eigene „bestätigt“-Seite.

| | |
|---|---|
| **Name** | Neustart 2027 · Jahresplanungs-Workshop (✅ Patricia 01.11.) |
| **Profil** | Mentoring |
| **Art** | Freebie (Live-Workshop, offener Call aus der MBA) |
| **Preis** | **gratis** (Patricia 31.10.) |
| **Termin** | **Donnerstag, 17. Dezember 2026, 09:00 Uhr**, Zoom (Patricia 31.10.) · Dauer **90 Minuten** (✅ Patricia 01.11.) |
| **Wer ist dabei** | die MBA-Gruppe (Call im Gruppenprogramm) plus alle, die sich eintragen |
| **Aufzeichnung** | ja, **unbefristet** offen für alle Angemeldeten (Patricia 31.10.) · Ort 🟠 ENTSCHEID: Vimeo, Link per Mail |
| **Werkzeug im Workshop** | Seite „Mein Jahresplan“ (Artifact 72vifh23HRaBDoVjqcgx4t, ohne Anmeldung, Fragen aus `scripts/jahresplan/fragen.json`) — muss vorher über das Share-Menü öffentlich geteilt werden |
| **Für wen** | Mamas im Network, mit oder ohne eigenes Angebot daneben, die ihr Business bisher von Monat zu Monat planen |
| **Schmerz davor** | Jeden Morgen neu entscheiden, was sie postet und anbietet · Launch fällt in die Ferien · nach einem Angebot kommt ein Loch · viel Zeit im Network, ohne zu wissen, wie viele Leute es braucht |
| **Veränderung** | Sie hat ihr Jahr 2027 auf einem Blatt: Ferien, Familie und eigene Zeit zuerst eingetragen, ein Fokus-Angebot je Monat, Lücken und Umsatz gegen ihr Ziel gerechnet, und sie weiss, was sie im Januar als Erstes tut. |
| **Der Weg** | die sechs Schritte des Jahresplaners: Rückblick · Vision · Leben zuerst · Angebote (Network mit eigenen Zahlen) · Jahr (mit Lücken-Check) · Woche |
| **Anmeldung** | AC-Formular **„0€ Jahresplanung“** (neu, Kopie von Formular 75 über die Schnittstelle) → Bestätigungsmail (Double Opt-in) → Danke-Seite |
| **AC** | Liste 2 (Mentoring) · **ein** Tag **„0€ Jahresplanung“ (109)** · Formular **76** (angelegt 01.11., Opt-in-Mail entsteht erst nach einmal Speichern im Editor) · Kampagnen-Entwürfe A1–A3 **899–901**, E1–E5 **902–906** (`python scripts/jahresplanung/mails-bauen.py [--hochladen]`) · Automation **„0€ Jahresplanung“** mit Ziel „MBA gekauft“ ganz unten (baut Patricia) |
| **Seiten** | Anmeldeseite `/neustart-2027/` (WP **4469**) · Danke-Seite `/neustart-2027-danke/` (**4470**) · nach dem Bestätigungsklick `/neustart-2027-bestaetigt/` (**4473**) · alle als **Entwurf** seit 01.11., Mockup = WP-Medium **4468** · Deploy `node --env-file=.env deploy-jahresplanung-lp.mjs` in `scripts/wordpress` |
| **Stichwort** | **NEUSTART** (✅ Patricia 01.11., in `context/manychat-keywords.md` frei) → DM mit Link zur Anmeldeseite. Flow in ManyChat anlegen und testen |
| **Anschluss** | **Mum Business Academy** (Patricia 31.10.) · 997 CHF (Pioneer, Listenpreis 1347) · Seite `/mba/` · bezahlte Kurse werden angerechnet, Klärung per DM. **Kein Workshop-Sonderpreis, MBA zu 997** (✅ Patricia 01.11.) |
| **Gestaltung** | dunkles KI-Design der Story-Generator-Seite (wie Tool-Workshop) · Mockup `scripts/salespage-design/jahresplanung-bild.mjs` · Effekt Kalenderblatt 31.12.2026 → 1.1.2027 plus aufsteigende Funken (`jahresplanung-effekt.css`, reines CSS) |

## Kette

| | Angebot | Preis | Regel |
|---|---|---|---|
| Einstieg | Neustart 2027 (Workshop) | gratis | Freebie, Anmeldung über AC |
| Danke-Seite | Hinweis MBA mit Link `/mba/` | 997 CHF regulär | kein Workshop-Preis (✅ Patricia 01.11.) |
| Nach dem Workshop | MBA-Pitch in Mail E3–E5 und Storys 17.–20.12. | 997 CHF | Pitch erst nach dem Workshop: dann ist das neue Problem da (*„Der Plan steht, wer hilft mir, ihn umzusetzen?“*) |

## Fahrplan rückwärts ab Do 17.12.

Fest im Kalender: Tool-Workshop **Di 10. + Mi 11.11.** (19:00), Begleitung bis Sa 14.11. · KI-Kurs-Live-Call **Mi 18.11.**
und **Do 10.12.** · Black Friday Fr 27.11. (nichts) · **Weihnachtsferien 21.12.–3.1.**

| Datum | Was | Wer |
|---|---|---|
| **So 15.11.** | Bauplan freigeben (Name, Stichwort, Dauer, Aufzeichnungsort) | Patricia |
| Mo 16.–Fr 20.11. | Texte final · WP-Seiten als Entwurf · AC-Formular, Tag, Bestätigungsmail und Mails als Entwürfe · Mockup als webp in WP | Claude (nach Go) |
| **Fr 20.11.** | Zoom-Termin 17.12. 09:00 anlegen, Link an Claude · Jahresplaner-Seite öffentlich teilen | Patricia |
| Mo 23.11. | Automation „0€ Jahresplanung“ bauen, ManyChat-Flow NEUSTART, Testanmeldung von A bis Z | Patricia + Claude |
| **Mo 23.–So 29.11.** (KW48) | **Anwärmen:** Storys mit Rückblick-Fragen („Was lief 2026 gut?“), Umfrage „planst du schon für 2027?“ · Feed Mo 23.11. Reel 1 (Reichweite, ohne Stichwort) | Patricia (Storys), Claude (Texte) |
| **Mi 25.11.** | Seiten live schalten (Patricias Go), Effekt am Handy prüfen | Claude |
| **Mo 30.11.** | **Anmeldung offen.** Storys Einladung · Mail **A1** an Liste 2 | beide |
| Di 1.12. | Feed Karussell 2 (Lead, NEUSTART) | |
| Mo 7.12. | Mail **A2** an alle, die noch nicht angemeldet sind | |
| Do 10.12. | KI-Kurs-Live-Call (nur Käuferinnen) — an dem Tag nur eine kurze Workshop-Story | |
| Fr 11.12. | Feed Reel 3 (Lead, NEUSTART) | |
| **Di 15.12.** | Mail **A3** „übermorgen“ · Storys „noch zwei Tage“ | |
| Mi 16.12. 18:00 | Mail **E1** an Angemeldete: was bereitlegen, Link zum Jahresplaner | |
| **Do 17.12. 08:00** | Mail **E2** „in einer Stunde“ mit Zoom-Link | |
| **Do 17.12. 09:00** | **Workshop live** · Storys davor und danach | Patricia |
| Do 17.12. abends | Mail **E3**: Aufzeichnung + MBA | |
| Fr 18.12. | Mail **E4** MBA (Einwand Zeit) · Storys MBA | |
| So 20.12. | Mail **E5** MBA, die letzte vor den Ferien · Storys | |
| 21.12.–3.1. | Ferien. Nichts live, Aufzeichnung und `/mba/` bleiben offen | |

⚠️ **Offen und nicht von hier aus entscheidbar:** Der 1:1 Postingplan (1149 CHF, „14 Tage Launch im Dezember, Start
Januar“, Plan 26.10.) läge genau auf der Workshop-Einladung (30.11.–17.12.) und auf dem MBA-Pitch. Zwei Verkäufe im
selben Fenster ziehen sich gegenseitig die Aufmerksamkeit ab. Patricia entscheidet: Postingplan verschieben (z.B. Pitch im
Januar, Start Februar) oder nur leise an die MBA-Käuferinnen.

## Bausteine

01 Ablauf · 02 Anmeldeseite (gebaut: `outputs/salespages/jahresplanung/`) · 03 Danke-Seite · 04 Mails · 05 Storys ·
06 Feed · 07 Stichwort-Automation · 08 Anzeigen · 09 Einrichte-Liste
