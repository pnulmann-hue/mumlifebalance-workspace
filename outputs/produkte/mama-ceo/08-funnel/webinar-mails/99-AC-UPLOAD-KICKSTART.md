---
tags: [produkt]
---

# AC-Upload-Kickstart — die 14 Mails in 30 Min in AC kriegen

**Was du brauchst:** AC-Tab offen · diesen Cheat-Sheet · alle 14 HTML-Dateien (im gleichen Ordner)
**Letzter Stand:** 2026-05-19 · alle Mails auf Pitch-Variante C + neue 5 Säulen + `%FIRSTNAME%` formatiert

---

## Vor dem Upload — 1 Min Aufräumen

- [ ] **Tag „Mama-CEO" (ID 73) löschen** → AC → Kontakte → Tags → „Mama-CEO" → Aktionen → Löschen *(ungenutzt)*
- [ ] **Tag „mama-ceo-webinar-live-teilnehmer" (ID 74) löschen** → gleiche Stelle *(brauchen wir nicht)*
  *(Behalten: nur `0€ Webinar Mama-CEO` (ID 70) und `mama-ceo-kauf` (ID 71))*
- [ ] **ThriveCart-Cart-Link bereitlegen** → vermutlich `https://mumlifebalance.thrivecart.com/mama-ceo/`
- [ ] **Zoom-Link bereitlegen** für Mail 4 + 5
- [ ] **Replay-Link bereitlegen** für Mail 6 (Vimeo passwortgeschützt, 48h)

---

## Upload-Workflow pro Mail (immer gleich)

1. AC → **Campaigns → Create New → Standard**
2. **Type:** Standard Campaign
3. **List:** Regulärer Newsletter/Interessenten (ID 2)
4. **From-Name:** `Patricia Ulmann`
5. **From-Email:** `patricia@mumlifebalance.ch`
6. **Subject:** aus Tabelle unten kopieren
7. **Preheader:** aus dem `<div style="display:none">` im HTML — ist schon drin, AC erkennt es automatisch
8. **Editor wechseln:** „Custom Code" / „HTML Source" (NICHT der visuelle Drag&Drop-Editor!)
9. **HTML rein:** komplette Datei kopieren + einfügen
10. **Speichern als Draft** (nicht senden)

→ Tipp: Mach erst alle 14 Drafts. Erst dann gehst du in die Automations zum Anhängen.

---

## Die 14 Mails — Subject + Datei + Zielautomation

| # | Datei | Subject | Internal Name | → Wohin |
|---|---|---|---|---|
| 1 | `01-bestaetigung.html` | Du bist drin. Mittwoch 20.5. 09:00 — wir sehen uns. | Mama-CEO 01 Bestätigung | Auto „Webinar Mama-CEO" (ID 60) |
| 2 | `02-1woche-vorher.html` | „Heute mach ich endlich Content" — und am Abend nichts gepostet? | Mama-CEO 02 1Woche-vorher | Mass-Send Mi 13.5. 14:00 |
| 3 | `03-reminder-24h.html` | Morgen 09:00 — und noch eine kleine Bitte | Mama-CEO 03 Reminder-24h | Auto „Webinar Mama-CEO" (ID 60) |
| 4 | `04-reminder-1h.html` | In 1 Stunde — hier ist dein Zoom-Link | Mama-CEO 04 Reminder-1h | Auto „Webinar Mama-CEO" (ID 60) — ⚠️ Zoom-Link einsetzen! |
| 5 | `05-cliffhanger-live.html` | 🔴 LIVE — komm rein, ich zeige in 5 Min meinen Kochassistenten | Mama-CEO 05 Cliffhanger-LIVE | Mass-Send Mi 20.5. 09:15 — Filter: NICHT Tag „0€ Webinar Mama-CEO" — ⚠️ Zoom-Link einsetzen! |
| 6 | `06-cart-open.html` | Es ist soweit. Mama-CEO ist offen — Earlybird CHF 249 (nur bis Sa 23.5.) | Mama-CEO 06 Cart-Open | Mass-Send Mi 20.5. 11:00 — ⚠️ Cart-Link + Replay-Link einsetzen! |
| 7 | `07-painpoint.html` | „Heute schaff ich's wirklich" — und am Abend? | Mama-CEO 07 Painpoint | Auto „Cart-Window" Do 21.5. 08:00 |
| 8 | `08-earlybird-end-morgens.html` | Heute 23:59 endet der Earlybird. 16 Stunden zu CHF 249. | Mama-CEO 08 Earlybird-End-Morgens | Auto „Cart-Window" Sa 23.5. 08:00 |
| 9 | `09-earlybird-end-last2h.html` | Letzte 2 Stunden Earlybird (CHF 249 → 333). | Mama-CEO 09 Earlybird-End-Last2h | Auto „Cart-Window" Sa 23.5. 22:00 |
| 10 | `10-earlybird-vorbei.html` | Earlybird vorbei — Cart bleibt offen bis 31.5. | Mama-CEO 10 Earlybird-Vorbei | Auto „Cart-Window" So 24.5. 09:00 |
| 11 | `11-midweek-antikunden.html` | Für wen Mama-CEO NICHT ist (ehrlich) | Mama-CEO 11 Antikunden | Auto „Cart-Window" Mi 27.5. 08:00 |
| 12 | `12-letzte-tage.html` | 3 Tage noch — und warum ich diesen Kurs unbedingt mit dir machen will | Mama-CEO 12 Letzte-Tage | Auto „Cart-Window" Fr 29.5. 08:00 |
| 13 | `13-close-morgens.html` | Heute 23:59 schliesst Mama-CEO endgültig. 16h noch. | Mama-CEO 13 Close-Morgens | Auto „Cart-Window" So 31.5. 08:00 |
| 14 | `14-close-letzte2h.html` | Letzte 2 Stunden. Cart-Close 23:59. | Mama-CEO 14 Close-Last2h | Auto „Cart-Window" So 31.5. 22:00 |

---

## Nach dem Upload — 3 Automations bauen

### Automation 1: „Webinar Mama-CEO" (existiert schon, ID 60)
Reingucken — ist die schon mit Mails 1, 3, 4 bestückt?
- Wenn JA → nur Zoom-Link in Mail 4 einsetzen, fertig
- Wenn NEIN → Mails 1, 3, 4 anhängen wie folgt:
  - Start-Trigger: Tag `0€ Webinar Mama-CEO` (ID 70) wird hinzugefügt
  - → Send Email: Mama-CEO 01 Bestätigung (sofort)
  - → Wait until: Di 19.5. 09:00
  - → Send Email: Mama-CEO 03 Reminder-24h
  - → Wait until: Mi 20.5. 08:00
  - → Send Email: Mama-CEO 04 Reminder-1h

### Mass-Send Mails 2, 5, 6 (nicht Automation, sondern geplante Campaigns)
- **Mail 2** Schedule Mi 13.5. 14:00 → Liste 2 (alle aktiven)
  ⚠️ Mi 13.5. ist schon vorbei (heute 19.5.). Diese Mail ggf. weglassen oder als „heute" + 1 Tag neu planen.
- **Mail 5** Schedule Mi 20.5. 09:15 → Liste 2 mit Filter „NICHT Tag 0€ Webinar Mama-CEO"
- **Mail 6** Schedule Mi 20.5. 11:00 → Liste 2 (alle aktiven)

### Automation 3: „Mama-CEO Cart-Window 2-Phasen" (NEU bauen)
- Start-Trigger: Wait until date: Do 21.5.2026 08:00
- Conditional Split vor JEDER Mail: Hat Tag `mama-ceo-kauf` (ID 71)? → JA = END
- Mails 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 mit Wait-Until-Date dazwischen
- Genaue Setup-Anleitung: `99-AC-SETUP.md` (Schritt 6)

---

## Vor dem Aktivieren — letzte Checks

- [ ] Test-Anmeldung gemacht (Mail 1 muss ankommen)
- [ ] Zoom-Link in Mails 4 + 5 eingesetzt
- [ ] Cart-Link in Mails 6-14 eingesetzt (`[Mama-CEO Cart-Link]` durch echte URL ersetzen)
- [ ] Replay-Link in Mail 6 eingesetzt
- [ ] ThriveCart-Webhook setzt Tag `mama-ceo-kauf` auf Käufer (Patricia: ✅ schon eingerichtet)
- [ ] ThriveCart-Preis-Switch eingestellt (CHF 249 → 333 ab So 24.5. 00:00)
- [ ] Cart-Close So 31.5. 23:59 eingestellt

---

## Wenn was hängt

Sag mir welche Mail oder Automation klemmt, ich helf gezielt. Die wichtigsten Mails für **morgen Mi 20.5.** sind 4, 5 und 6 — die müssen heute Abend stehen.
