---
tags: [produkt]
---

# 09 · Einrichte-Liste Tool-Workshop

Was von Hand angelegt wird. Reihenfolge = Dringlichkeit, weil die Kasse sofort offen sein soll.

## Heute

- [ ] **Entscheide bestätigen** aus `00-bauplan.md` (🟠): Bump Story-Generator 17 · Upsell Begleitung 27 · Stichwort NISCHE · Gruppe (Telegram?)
- [x] **Nischengenerator öffentlich:** https://mlb-nischengenerator.vercel.app (KI, nach dem Kurs „Finde dein Thema“, Quelle `scripts/tool-ideen/`). Die alte regelbasierte Fassung liegt als Workshop-Beispiel auf Netlify.
- [ ] **ThriveCart-Produkt** „Tool-Workshop“, 39 CHF, AGB-Link `https://mumlifebalance.ch/agb/`, Kasse live (Claude kann es in deinem Chrome anlegen, sobald du Ja sagst)
- [ ] Kassentext aus `03-kasse.md` (Zeitplan, Bump, Upsell)
- [ ] **ThriveCart Learn:** Kurs „Tool-Workshop“ mit den Lektionen aus `01-aufbau.md` (Aufzeichnungen kommen nach dem 10./11.)
- [ ] **Anmeldeseite** in WordPress (Entwurf liegt bereit, siehe unten) → prüfen → veröffentlichen, Knopf auf die ThriveCart-Kasse
- [ ] **Link-Sticker** in den Cockpit-Storys einsetzen: Anmeldeseite + Nischengenerator
- [ ] **Sprechreel:** Stichwort im Schluss auf NISCHE stellen (`06-feed.md`)

## Bis Montag 2.11.

- [x] AC-Tag **Tool-Workshop** (107), ThriveCart setzt ihn beim Kauf
- [x] **Alle 7 Mails als Kampagnen-Entwurf in AC** (29.10., `python scripts/tool-workshop/mails-bauen.py --hochladen`): A1 852 · A2 853 · A3 854 (Liste 2) · B0 855 · B1 856 · B2 857 · B3 858 (Liste 16)
- [ ] **A1 (852) verschicken** an Liste 2, A2 (853) für Fr 6.11. und A3 (854) für Mo 9.11. planen, jeweils ohne Kontakte mit Tag 107
- [ ] **Automation „Tool-Workshop“ von Hand anlegen** (geht nicht über die Schnittstelle): Auslöser Tag 107 hinzugefügt → E-Mail B0 (Vorlage: Kampagne 855) → warten bis Mo 9.11. 18:00 → B1 (856) → warten bis Mi 11.11. 07:00 → B2 (857) → warten bis Sa 14.11. 09:00 → B3 (858)
- [ ] **✏️-Stellen in B0–B3 füllen:** Zoom-Links, Gruppen-Link, Aufzeichnung, Produktwelt. Am einfachsten oben in `scripts/tool-workshop/mails-bauen.py` (ZOOM_1, ZOOM_2, GRUPPE) eintragen, neu bauen und in AC ersetzen
- [ ] **Stichwort NISCHE:** gespeicherte Antwort in Instagram anlegen (`07-automation.md`, Weg 1)
- [ ] **Zoom:** zwei Meetings 10. und 11.11. mit Aufzeichnung in die Cloud, Links in Mail B0/B1/B2
- [ ] **Gruppe** für die Begleitung anlegen, Link in Mail B0

## Nach dem Workshop

- [ ] Aufzeichnungen in ThriveCart Learn ablegen
- [ ] Kasse am 10.11. auf „disabled“ (oder Evergreen mit Aufzeichnung, falls du willst)
- [ ] Meta-App-Review für den eigenen Kommentar-Dienst beantragen (Weg 2)
- [ ] Echte Stimmen der Teilnehmerinnen mit Freigabe in `context/kundinnen-geschichten.md`

## Prüfaufträge (❓ nicht von hier aus prüfbar)

- [ ] Story-Generator-Kasse existiert noch nicht → ohne sie keinen Bump einrichten
- [ ] Hat die Digitale Produktwelt im November/Dezember einen Termin? Mail B3 braucht Link und Zeitraum

## Nischengenerator mit Tool-Ideen (seit 29.10.)

- [x] Tool-Ideen sind im Nischengenerator aufgegangen (zweiter Schritt je Thema), Tag 0€ Nischengenerator 108, 10 Durchgänge je Mail
- [ ] Automation in AC am Tag **0€ Nischengenerator** anlegen: Auslöser Tag hinzugefügt, eine Mail = Entwurf „Tool-Ideen C0 · Willkommen“ (Betreff „Dein Thema, und was du jetzt damit machst“) (Kampagne 859) als Vorlage. Nach dem 9.11. den Workshop-Absatz austauschen.
- [ ] Link in Storys und in der gespeicherten Instagram-Antwort zu NISCHE ergänzen
- [x] Nischengenerator auf Netlify übernommen

## Anmeldeseite Nischengenerator (seit 29.10. abends)

- [x] AC-Formular **75 „0€ Nischengenerator“**: Tag 0€ Nischengenerator, Liste 2, Bestätigungsmail (Nachricht 718, aus `scripts/mails/bestaetigung-bauen.py`), nach dem Klick weiter zum Tool, nach dem Absenden auf die Danke-Seite
- [ ] **WP 4441 `/nischengenerator/` veröffentlichen** (Entwurf)
- [ ] **WP 4442 `/nischengenerator-danke/` veröffentlichen** (Entwurf; ohne sie landet das Formular nach dem Absenden auf einer 404)
- [ ] Formular einmal selbst durchspielen (reCAPTCHA, Bestätigungsmail, Weiterleitung zum Tool)
- [ ] Gespeicherte Instagram-Antwort zu NISCHE auf https://mumlifebalance.ch/nischengenerator/ stellen
- [ ] Nach dem 11.11.: Workshop-Kasten der Danke-Seite auf Aufzeichnung umstellen (`scripts/salespage-design/nischengenerator-danke-body.html`, dann `deploy-nischengenerator-lp.mjs`)
