---
tags: [produkt, launch, mba, intern]
---

# AC-Setup — MBA-Webinar-Mail-Funnel (14 Mails · 2-Phasen-Cart)

**Produkt:** Mum Business Academy (MBA) · **Webinar:** Mi 24.6.2026 09:00
**Cart-Logik:** 🟢 Pioneer CHF 997 (Mi 24.6. 11:00 → Sa 27.6. 23:59) → 🔵 Final CHF 1347 (So 28.6. → Cart-Close So 5.7. 23:59) · Programmstart Juli
**Status:** Alle 14 Mails als **Draft-Campaigns in AC hochgeladen** (#596–#609, Liste 2, Absender Patricia Ulmann / patricia@mumlifebalance.ch). Quelle: `outputs/produkte/mba-launch/webinar-mails/*.html`. Re-Upload: `node scripts/activecampaign-mcp/bulk-upload-mba.mjs`.

---

## Tags

| Tag | ID | Wofür |
|---|---|---|
| `mba-webinar-anmeldung` | **78** | Wird durch das Webinar-Anmelde-Formular (Form 59, /mba-webinar) gesetzt → triggert Anmelder-Sequenz |
| `mba-kauf` | **79** | Wird via ThriveCart-Webhook bei Kauf gesetzt → Käufer-Ausschluss in Verkaufsstrecke |

---

## Die 14 Mails — Campaign-IDs · Subject · Wann · Automation

| # | Campaign | Datei / Subject | Wann | → Wohin |
|---|---|---|---|---|
| 1 | **#596** | `01-bestaetigung` · „Du bist drin. Mittwoch 24.6. 09:00 — wir sehen uns." | sofort nach Anmeldung | Auto 1 (Anmelder) |
| 2 | **#597** | `02-1woche-vorher` · „Abends halb zehn — und fürs Business hat der Tag wieder nicht gereicht?" | Mi 17.6. 14:00 | Mass-Send (ganze Liste) |
| 3 | **#598** | `03-reminder-24h` · „Morgen 09:00 — und eine kleine Bitte vorher" | Di 23.6. 09:00 | Auto 1 (Anmelder) |
| 4 | **#599** | `04-reminder-1h` · „In 1 Stunde live — hier ist dein Zoom-Link" | Mi 24.6. 08:00 | Auto 1 (Anmelder) — ⚠️ Zoom-Link |
| 5 | **#600** | `05-cliffhanger-live` · „🔴 Wir sind live — komm rein" | Mi 24.6. 09:15 | Mass-Send — Filter: NICHT Tag 78 — ⚠️ Zoom-Link |
| 6 | **#601** | `06-cart-open` · „Es ist offen: die MBA — Pioneer-Preis 997 …" | Mi 24.6. 11:00 | Mass-Send — ⚠️ Cart- + Replay-Link |
| 7 | **#602** | `07-painpoint` · „Ich kann heute 25× essen gehen — und das hat einen Grund." | Do 25.6. 08:00 | Auto 2 (Cart-Window) |
| 8 | **#603** | `08-pioneer-end-morgens` · „Heute 23:59 endet der Pioneer-Preis. 16 Stunden zu CHF 997." | Sa 27.6. 08:00 | Auto 2 |
| 9 | **#604** | `09-pioneer-end-abend` · „Heute Abend endet der Pioneer-Preis (997 → 1347)." | **Sa 27.6. 19:00** | Auto 2 |
| 10 | **#605** | `10-pioneer-vorbei` · „Pioneer vorbei — die MBA bleibt offen bis So 5.7." | So 28.6. 09:00 | Auto 2 |
| 11 | **#606** | `11-antikunden` · „Für wen die MBA NICHT ist (ehrlich)" | Di 30.6. 08:00 | Auto 2 |
| 12 | **#607** | `12-letzte-tage` · „2 Tage noch — und warum ich diese Academy mit dir bauen will" | Fr 3.7. 08:00 | Auto 2 |
| 13 | **#608** | `13-close-morgens` · „Heute 23:59 schliesst die MBA. 16 Stunden noch." | So 5.7. 08:00 | Auto 2 |
| 14 | **#609** | `14-close-abend` · „Heute Abend schliesst die MBA — letzter Aufruf." | **So 5.7. 19:00** | Auto 2 |

---

## Platzhalter, die VOR dem Aktivieren rein müssen

| Platzhalter | In Mails | Was eintragen |
|---|---|---|
| `%FIRSTNAME%` | alle | AC-Personalisierung (bereits AC-Syntax, sollte automatisch ziehen) |
| `[ZOOM-LINK]` | 4, 5 | echter Zoom-Webinar-Link |
| `[MBA-CART-LINK]` | 6, 7, 8, 9, 10, 11, 12, 13, 14 | ThriveCart-Checkout der MBA |
| `[REPLAY-LINK]` | 6 | Replay-URL (48h gültig) |

> **Webinar-Uhrzeit:** überall **09:00** angenommen — bitte gegen die Anmeldeseite prüfen, falls anders.
> **Cart-Preis-Wechsel:** ThriveCart „Scheduled price change" 997 → 1347 ab **So 28.6. 00:00** einstellen (dann gleicher `[MBA-CART-LINK]` überall). Cart-Close So 5.7. 23:59.

---

## Automation 1 — „MBA Webinar Anmelder" (NEU bauen)

- **Start-Trigger:** Tag `mba-webinar-anmeldung` (78) wird hinzugefügt
- Send Email: **#596** (Bestätigung) — sofort
- Wait until: Di 23.6. 09:00 → Send Email: **#598** (Reminder 24h)
- Wait until: Mi 24.6. 08:00 → Send Email: **#599** (Reminder 1h) — ⚠️ Zoom-Link einsetzen

## Mass-Send (geplante Campaigns, nicht Automation)

- **#597** schedule Mi 17.6. 14:00 → Liste 2 (alle aktiven)
- **#600** schedule Mi 24.6. 09:15 → Liste 2 mit Filter „NICHT Tag 78"
- **#601** schedule Mi 24.6. 11:00 → Liste 2 (alle aktiven) — ⚠️ Cart- + Replay-Link

## Automation 2 — „MBA Cart-Window 2-Phasen" (NEU bauen)

- **Start-Trigger:** Wait until date Do 25.6.2026 08:00
- **Vor JEDER Mail ein Conditional Split:** Hat Tag `mba-kauf` (79)? → JA = END
- Reihenfolge mit Wait-Until-Date dazwischen:
  - **#602** Do 25.6. 08:00 → **#603** Sa 27.6. 08:00 → **#604** Sa 27.6. **19:00** → **#605** So 28.6. 09:00 → **#606** Di 30.6. 08:00 → **#607** Fr 3.7. 08:00 → **#608** So 5.7. 08:00 → **#609** So 5.7. **19:00** → END

## ThriveCart-Webhook

- Bei „Successful purchase" → **Add Tag `mba-kauf` (79)** in AC → schliesst Käuferinnen automatisch aus Auto 2 aus.

---

## Checkliste vor Aktivierung

- [ ] Zoom-Link in #599 + #600
- [ ] Cart-Link in #601–#609 (bzw. ThriveCart Scheduled Price Change 997→1347 ab So 28.6.)
- [ ] Replay-Link in #601
- [ ] Webinar-Uhrzeit geprüft (09:00?)
- [ ] Auto 1 mit Trigger Tag 78 gebaut + aktiviert
- [ ] Auto 2 mit Conditional Split auf Tag 79 gebaut
- [ ] Mass-Sends #597 / #600 / #601 geplant
- [ ] ThriveCart-Webhook setzt Tag 79
- [ ] Test-Anmeldung (Mail #596 kommt sofort)
