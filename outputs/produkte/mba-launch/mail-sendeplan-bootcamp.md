---
tags: [produkt, launch, mba, bootcamp, intern]
---

# Mail-Sendeplan — Bootcamp + MBA-Cart (Pivot vom Webinar)

**Erstellt:** 2026-06-11 · **Ersetzt** die Webinar-Sendelogik aus [[99-AC-SETUP-MBA]] (die 14 Mails #596–#609 bleiben als Rohmaterial, werden aber neu getaktet + teils umgeschrieben).

> **Warum neu:** Launch ist seit 8.6. ein **5-Tage-Bootcamp** statt Webinar (siehe [[challenge-launch-plan]]). Heisst: kein Webinar-Reminder, kein Zoom-Link, kein 2-Phasen-Cart (997→1347 mitten im Launch). Stattdessen: Bootcamp-Tagesmails + **einphasiger Pioneer-997-Flash-Cart** (Fr 3.7. → So 6.7. 23:59).

---

## Timeline (Abgleich mit story-plan.json)

| Datum | Was | Mail-Track |
|---|---|---|
| **15.–28.6.** | Aufwärm — Bootcamp bewerben, Anmeldungen sammeln | Warteliste-Nudge (D) |
| **So 28.6. abends** | Letzte Anmelde-Chance | A2 |
| **Mo 29.6.–Fr 3.7.** | 🔥 Bootcamp läuft (Telegram-Gruppe + PIA) | Bootcamp-Tagesmails (B) |
| **Fr 3.7. abends** | Tag-5-Finale → **Cart-Open MBA (Pioneer 997)** | C1 |
| **Sa 4.7.–So 6.7.** | Cart offen, Pioneer 997 | C2–C7 |
| **So 6.7. 23:59** | 🚨 Cart-Close endgültig | C7 |
| **7.–9.7.** | Nachkauf — Wins zeigen, Nachzügler | (Stories tragen das, keine Pflicht-Mail) |

**Segmente / AC-Tags:**
- `bootcamp-anmeldung` (**Tag 80**, via Form **60** auf /bootcamp/) → Bootcamp-Strecke (A + B)
- `mba-warteliste` (**Tag 77**, Form 57 /mba-warteliste) → Warteliste-Vorsprung (D)
- `mba-kauf` (**Tag 79**, ThriveCart-Webhook) → schliesst aus Cart-Strecke (C) aus

---

## Track A — Bootcamp-Anmelder-Onboarding · Automation, Trigger Tag 80

| # | Wann | Betreff (Entwurf) | Inhalt | Quelle |
|---|---|---|---|---|
| **A1** | sofort nach Anmeldung | „Du bist drin — so läuft dein Bootcamp" | Bestätigung + **Telegram-Gruppe** (t.me/+HW6lvdlbTBhiOWM0) + was die 5 Tage bringen + dass PIA dabei ist | ♻️ **#596** anpassen (Webinar→Bootcamp, Zoom raus, Gruppenlink rein) |
| **A2** | So 28.6. 18:00 | „Morgen früh starten wir — kurz noch das hier" | Vorfreude + Gruppe beitreten + wie der Morgen-Impuls + PIA funktioniert | 🆕 neu (kurz) |

---

## Track B — Bootcamp-Tagesmails · Automation Tag 80, Mo–Fr je ~07:00

> Backup-/Nudge-Kanal für alle, die nicht ständig in Telegram sind. Kurz halten — die Mission lebt in der Gruppe.

| # | Tag | Betreff (Entwurf) | Inhalt |
|---|---|---|---|
| **B1** | Mo 29.6. | „Tag 1: dein Thema wird klar" | Heutige Mission (Bio/Positionierung) + PIA-Link + Gruppe |
| **B2** | Di 30.6. | „Tag 2: 3 Hooks, die deine Leute stoppen" | Mission Hooks + PIA |
| **B3** | Mi 1.7. | „Tag 3: endlich Zeit (ohne dich zu zerreissen)" | Mission Struktur/KI-Impuls |
| **B4** | Do 2.7. | „Tag 4: dein erster Schritt zur Liste" | Mission Leadmagnet-Skelett |
| **B5** | Fr 3.7. | „Tag 5: dein roter Faden — und heute Abend kommt was" | Finale-Mission + **Cart-Teaser** (heute Abend öffnet sich was) |

→ alle 5 **🆕 neu**, leicht. PIA-/Gruppen-Link als Platzhalter.

---

## Track C — MBA-Cart · Automation, an Tag 80 + Tag 77, Conditional Split „hat Tag 79? → END"

> Einphasig Pioneer 997 durchgehend (kein Preiswechsel im Cart). Die Webinar-Earlybird-/Pioneer-Ende-Mails (#603/#604/#605) entfallen als Preis-Switch-Mails — #603 wird zu Social Proof umgewidmet.

| # | Wann | Betreff (Entwurf) | Inhalt | Quelle |
|---|---|---|---|---|
| **C1** | Fr 3.7. ~19:30 | „Es ist offen: die MBA — Pioneer 997" | Cart-Open, was drin ist (3 Kurse + 2 Calls/Monat + PIA), Transformation, Link | ♻️ **#601** anpassen (Replay raus, Bootcamp-Finale rein) |
| **C2** | Sa 4.7. 08:00 | „Ich kann heute 25× essen gehen — und das hat einen Grund" | Painpoint → Lösung MBA | ♻️ **#602** (passt fast 1:1) |
| **C3** | Sa 4.7. 19:00 | „Was die Gründungs-Mamas schon erlebt haben" | Social Proof Pilot-Mamas + Bootcamp-Wins (anonym, keine erfundenen Zahlen) | ♻️ **#603** umwidmen zu Social Proof |
| **C4** | So 5.7. 08:00 | „Für wen die MBA NICHT ist (ehrlich)" | Antikunden-Frame + keine Geld-zurück ehrlich rahmen | ♻️ **#606** (passt) |
| **C5** | So 5.7. 19:00 | „Morgen 23:59 ist Schluss — und warum ich das mit dir bauen will" | Letzte-Tage + persönlicher Brief | ♻️ **#607** anpassen (Datum) |
| **C6** | So 6.7. 08:00 | „Heute 23:59 schliesst die MBA — 16 Stunden noch" | Close-Morgens | ♻️ **#608** anpassen (Datum) |
| **C7** | So 6.7. 20:00 | „Heute Abend schliesst die MBA — letzter Aufruf" | Close-Abend last call | ♻️ **#609** anpassen (Datum) |

**Nicht mehr gebraucht (Webinar-only):** #597 (1-Woche-Webinar), #598 (24h-Reminder), #599 (1h-Reminder + Zoom), #600 (Cliffhanger-Live), #604/#605 (Pioneer-Ende-Preisswitch). → in AC pausiert lassen, nicht löschen.

---

## Track D — Warteliste-Vorsprung · Automation Tag 77

| # | Wann | Betreff (Entwurf) | Inhalt |
|---|---|---|---|
| **D1** | ~Fr 26.6. | „Bevor's losgeht — dein Platz im Bootcamp" | Warteliste zuerst ins **kostenlose Bootcamp** einladen (DM/Link BOOTCAMP) |
| **D2** | Fr 3.7. 18:30 | „Du zuerst: die MBA öffnet in 1 Stunde" | Warteliste kriegt Cart-Link 1h vor allen anderen |

→ beide **🆕 neu**, kurz.

---

## Track E — Käufer-Welcome · Trigger Tag 79 (ThriveCart-Webhook)

| # | Wann | Betreff (Entwurf) | Inhalt |
|---|---|---|---|
| **E1** | sofort bei Kauf | „Willkommen in der MBA 🎉" | Bestätigung + Zugang + **Programmstart Mitte August** + erster Live-Call nach den Ferien + Telegram | 🆕 neu |

---

## ThriveCart + Cart-Technik

- **Preis:** Pioneer **997** durchgehend Fr 3.7. → So 6.7. 23:59. **Kein** Scheduled Price Change im Launch (1347 ist erst der spätere Listenpreis).
- **Webhook:** „Successful purchase" → Add Tag `mba-kauf` (79) → END in Track C.
- **Cart-Link-Platzhalter** `[MBA-CART-LINK]` in C1–C7 + E1 + D2.

---

## Was zu tun ist (Reihenfolge)

1. **🆕 schreiben** (8 Mails): A2, B1–B5, D1, D2, E1 — kurz, Patricia-Voice. → kann ich als nächstes bauen.
2. **♻️ anpassen** (7 Mails): #596→A1, #601→C1, #603→C3, #607→C5, #608→C6, #609→C7 (Daten/Bootcamp-Bezug); #602/#606 fast 1:1.
3. **AC umbauen** (manuell, Sandbox-Limit): 3 Automationen (A: Tag 80 · B: Tag 80 Tagesmails · C: Cart mit Split auf 79 · D: Tag 77) + Käufer-Mail E. Re-Upload via `node scripts/activecampaign-mcp/bulk-upload-mba.mjs`.
4. **Webhook** Tag 79 in ThriveCart prüfen.

---

## 🔗 Verwandte Notizen
- [[challenge-launch-plan]]
- [[99-AC-SETUP-MBA]] (Webinar-Vorgänger — Rohmaterial)
- [[story-plan]] (Story-Seite desselben Launches)
