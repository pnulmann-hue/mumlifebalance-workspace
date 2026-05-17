---
tags: [produkt]
---

# AC-Setup für Webinar-Mail-Sequenz Mama-CEO (14 Mails · 2-Phasen-Cart)

**Was du brauchst:** AC-Account (hast du), 45-60 Min Zeit, Tasse Kaffee.
**Was du am Ende hast:** Komplett automatisierte 14-Mail-Sequenz die Mai-Launch durchspielt — von Anmelde-Bestätigung bis Cart-Close So 31.5. 23:59.

**Cart-Logik (2-Phasen):**
- 🟠 Mi 20.5. 11:00 → Sa 23.5. 23:59 = **Earlybird CHF 249** (3 Tage)
- 🔵 So 24.5. 00:00 → So 31.5. 23:59 = **Final CHF 333** (8 Tage)
- 🚀 Mo 1.6.2026 = **Pilot-Phase Start**

---

## SCHRITT 1: Tags anlegen

In AC: **„Kontakte → Tags"** → diese Tags neu erstellen (falls nicht schon da):

| Tag | Wofür |
|---|---|
| `mama-ceo-webinar-anmeldung` | Wird automatisch durch das Anmelde-Form gesetzt ✓ (schon konfiguriert) |
| `mama-ceo-webinar-live-teilnehmer` | Setzt du manuell nach Webinar (für die die LIVE da waren) |
| `mama-ceo-webinar-kauf` | Wird gesetzt wenn jemand Mama-CEO via ThriveCart kauft (Webhook) |

---

## SCHRITT 2: ThriveCart — 2 Preis-Stufen anlegen

Wichtig BEVOR du die Mails einrichtest: ThriveCart muss zwei Preise unterstützen.

**Option A (empfohlen): 1 Cart, automatischer Preiswechsel**
1. ThriveCart → Mama-CEO-Produkt → Pricing → **„Scheduled price changes"**
2. Initialpreis: CHF 249 ab Mi 20.5. 11:00
3. Geplanter Preiswechsel auf CHF 333 ab So 24.5. 00:00
4. **Cart deaktivieren ab So 31.5. 23:59:01** (oder über AC-Automation den Cart-Link sperren)

**Option B (einfacher): 2 separate Cart-URLs**
1. Cart-A `?price=earlybird` → CHF 249, manuell deaktivieren Sa 23.5. 23:59:01
2. Cart-B `?price=final` → CHF 333, manuell aktivieren So 24.5. 00:00, deaktivieren So 31.5. 23:59:01

→ Mails 6-9 = Cart-A · Mails 10-14 = Cart-B

---

## SCHRITT 3: Mails als Templates anlegen

In AC: **„Campaigns → Templates"** oder direkt in der Campaign-Erstellung.

Für jede der 14 HTML-Mails (`01-bestaetigung.html` bis `14-close-letzte2h.html`):

1. **„Neue Vorlage"** klicken → **„Code Editor"** wählen (HTML-Modus)
2. Name: z.B. „Webinar Mail 01 — Bestätigung"
3. **HTML-Code** aus der Datei komplett kopieren + einfügen
4. **Subject** aus dem `<title>`-Tag im HTML kopieren (oder aus Übersicht)
5. **Pre-Header** ist im HTML schon drin (im versteckten `<div>` ganz oben)
6. **Personalisierung:** `{{first_name}}` mit AC-Variable ersetzen (in AC: „Personalize" → Vorname-Tag einfügen)
7. **Speichern**

→ Das machst du 14x (~45 Min mit Kaffee). Tipp: Erst alle Templates anlegen, dann Automations bauen.

---

## SCHRITT 4: Automation 1 — „Webinar-Anmelder-Flow"

**Trigger:** Tag `mama-ceo-webinar-anmeldung` wird hinzugefügt
**Mails:** 1, 3, 4

**Setup:**
1. AC → **„Automations → New"**
2. Name: „Mama-CEO Webinar — Anmelder"
3. Start-Trigger: **„Tag is added: mama-ceo-webinar-anmeldung"**
4. Aktionen nacheinander:
   - **Send Email:** Mail 01 (Bestätigung) — sofort
   - **Wait until:** Dienstag 19.5. 09:00
   - **Send Email:** Mail 03 (Reminder 24h)
   - **Wait until:** Mittwoch 20.5. 08:00
   - **Send Email:** Mail 04 (Reminder 1h, mit Zoom-Link!)

⚠️ **Wichtig:** Zoom-Link in Mail 04 vor Aktivierung einsetzen (Platzhalter `https://us02web.zoom.us/j/DEIN-ZOOM-LINK` ersetzen).

**Aktivieren** wenn das AC-Form live ist und Anmeldungen reinkommen.

---

## SCHRITT 5: Automation 2 — „Webinar-Day Mass-Send"

**Trigger:** Date-based — manuell ausgelöst oder als 3 separate Campaigns
**Mails:** 2, 5, 6

Diese 3 Mails gehen an **GANZE LISTE** (nicht nur Webinar-Anmelder).

### Mail 2 (1 Woche vor Webinar)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Sender: deine Adresse
3. Empfänger: deine Hauptliste (alle aktiven Kontakte)
4. Template: Webinar Mail 02
5. **Schedule:** Mi 13.5.2026 14:00
6. Senden

### Mail 5 ⭐ CLIFFHANGER (während Webinar läuft)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Empfänger: deine Hauptliste **MINUS** alle die schon Tag `mama-ceo-webinar-anmeldung` haben
   (Damit Anmelder die Cliffhanger-Mail NICHT bekommen — sie sind ja schon im Webinar)
   - Filter: „Empfänger hat NICHT Tag mama-ceo-webinar-anmeldung"
3. Template: Webinar Mail 05
4. **Schedule:** Mi 20.5.2026 09:15
5. Senden

⚠️ **Vor Aktivierung Zoom-Link in Mail 5 einsetzen!**

### Mail 6 (Cart-Open EARLYBIRD direkt nach Webinar)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Empfänger: deine Hauptliste (alle)
3. Template: Webinar Mail 06
4. **Schedule:** Mi 20.5.2026 11:00
5. Senden

⚠️ **Vor Aktivierung Cart-Link einsetzen!** (`[Mama-CEO Cart-Link]` Platzhalter ersetzen mit ThriveCart-URL — Cart-A bzw. Earlybird-URL)
⚠️ **Replay-Link einsetzen!**

---

## SCHRITT 6: Automation 3 — „Cart-Window-Sequenz" (8 Mails · 2-Phasen-Cart)

**Trigger:** Date-based — startet Do 21.5.
**Mails:** 7-14

**Setup:** Eine Automation die nacheinander alle 8 Cart-Mails schickt.

1. AC → **„Automations → New"**
2. Name: „Mama-CEO Cart-Window 2-Phasen"
3. Start-Trigger: **„Wait until date: Do 21.5.2026 08:00"** (manuelle Aktivierung am Webinar-Tag)
4. Aktionen:

```
[START Do 21.5. 08:00]
↓
Conditional Split: Hat Tag mama-ceo-webinar-kauf? → JA = END
↓
Send Email: Mail 07 (Painpoint + Aha-KI)         ← Do 21.5. 08:00
↓
Wait until Sa 23.5. 08:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 08 (Earlybird endet heute, 16h)  ← Sa 23.5. 08:00
↓
Wait until Sa 23.5. 22:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 09 (Earlybird Last 2h)           ← Sa 23.5. 22:00

==== EARLYBIRD-ENDE Sa 23.5. 23:59 ====
==== Cart-Preis-Switch CHF 249 → 333 ====
==== Vorab Mails 10-14 auf Cart-Link Final umstellen! ====

↓
Wait until So 24.5. 09:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 10 (Earlybird vorbei, Cart läuft) ← So 24.5. 09:00
↓
Wait until Mi 27.5. 08:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 11 (Antikunden / Wer es NICHT ist) ← Mi 27.5. 08:00
↓
Wait until Fr 29.5. 08:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 12 (Persönlicher Brief)           ← Fr 29.5. 08:00
↓
Wait until So 31.5. 08:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 13 (Heute schliesst Cart, 16h)    ← So 31.5. 08:00
↓
Wait until So 31.5. 22:00
↓
Conditional Split: Hat Tag …kauf? → JA = END
↓
Send Email: Mail 14 (Last 2h)                      ← So 31.5. 22:00
↓
[END So 31.5. 23:59]
```

**Wichtig — Käufer ausschliessen:**
Jede Mail mit einem **Conditional Split** vorgeschaltet: Wenn Tag `mama-ceo-webinar-kauf` vorhanden → Mail überspringen. So bekommt niemand Verkaufs-Mails der schon gekauft hat.

**Wichtig — Cart-Link-Wechsel:**
- Mails 6, 7, 8, 9 → Cart-Link Earlybird (CHF 249)
- Mails 10, 11, 12, 13, 14 → Cart-Link Final (CHF 333)
Wenn du Option A (1 Cart, Scheduled Price Change) gewählt hast: gleicher Link überall.
Wenn Option B: vor So 24.5. 00:00 alle Mails 10-14 auf Cart-B-URL umstellen!

---

## SCHRITT 7: ThriveCart-Webhook

Wenn jemand Mama-CEO via ThriveCart kauft, soll automatisch Tag `mama-ceo-webinar-kauf` in AC gesetzt werden.

**Setup in ThriveCart:**
1. ThriveCart → Mama-CEO-Produkt → Settings → Integrations
2. ActiveCampaign verbinden (falls noch nicht)
3. Bei „Successful purchase" → **Add Tag: mama-ceo-webinar-kauf**

→ Damit werden Käufer automatisch aus den weiteren Verkaufs-Mails ausgeschlossen.

---

## SCHRITT 8: Onboarding-Mail Mo 1.6.

Eine separate Automation für Käuferinnen:

1. **Trigger:** Tag `mama-ceo-webinar-kauf` wird hinzugefügt
2. **Wait until:** Mo 1.6.2026 06:00
3. **Send Email:** „Willkommen in Mama-CEO — Pilot-Start heute" (Onboarding-Mail, separates Template, nicht Teil dieser 14er-Sequenz)

---

## SCHRITT 9: Test-Anmeldung

**Vor Aktivierung der Automation 1:**

1. Geh auf https://webinar.mumlifebalance.ch
2. Trag dich selbst mit Test-E-Mail ein
3. Check ob:
   - Tag `mama-ceo-webinar-anmeldung` wird gesetzt ✓
   - Mail 01 (Bestätigung) kommt sofort an ✓
   - Mail 03/04 kommen am richtigen Datum (kannst du im AC-Automation-Log sehen)

Wenn alles klappt: **Aktivieren** und Mai-Launch beginnt automatisch zu laufen.

---

## CHECKLISTE vor Aktivierung

- [ ] **Alle 14 Templates** angelegt + getestet (richtige Subjects + keine Broken-Links)
- [ ] **Zoom-Link** in Mail 4 + Mail 5 eingesetzt
- [ ] **Cart-Link Earlybird** in Mails 6, 7, 8, 9 eingesetzt
- [ ] **Cart-Link Final** in Mails 10, 11, 12, 13, 14 eingesetzt (oder gleicher Link bei Option A)
- [ ] **Replay-Link** in Mail 6 eingesetzt
- [ ] **Tag** `mama-ceo-webinar-anmeldung` triggert Automation 1
- [ ] **ThriveCart Scheduled Price Change** Sa 23.5. 23:59 → CHF 333
- [ ] **ThriveCart Cart-Close** So 31.5. 23:59 (oder Webhook der Cart sperrt)
- [ ] **ThriveCart-Webhook** für Tag `mama-ceo-webinar-kauf` eingerichtet
- [ ] **Test-Anmeldung** gemacht — alle Mails kommen wie geplant
- [ ] **„Käufer-Ausschluss"** in Cart-Window-Sequenz aktiv (Conditional Split bei jeder Mail)
- [ ] **Onboarding-Mail Mo 1.6.** als separate Automation angelegt

---

## Fehler-Vermeidung

❌ **Doppel-Mails an Käufer:**
→ Conditional Split mit „Tag mama-ceo-webinar-kauf" in jeder Cart-Window-Mail (Mails 7-14)

❌ **Zoom-Link fehlt am Live-Tag:**
→ Mail 4 + Mail 5 vor Aktivierung 2x prüfen

❌ **Falscher Cart-Preis in Final-Phase:**
→ Vor So 24.5. 00:00 testen ob ThriveCart automatisch auf CHF 333 wechselt (oder Mails 10-14 auf Cart-B-Link umstellen)

❌ **Falsche Empfänger-Liste:**
→ Mail 5 (Cliffhanger): Filter „NICHT Tag mama-ceo-webinar-anmeldung" damit Live-Teilnehmer es nicht bekommen

❌ **HTML-Email zeigt komische Zeichen oder „<table>"-Tags:**
→ Sicherstellen dass du im AC-Editor auf „Code Editor" / „HTML Source" gewechselt hast, nicht im visuellen Editor

❌ **Cart bleibt nach So 31.5. 23:59 offen:**
→ ThriveCart-Pricing prüfen oder Cart-Link manuell auf „Sold out"-Page umleiten

---

**Bei Problemen:** Sag mir welche Mail/Automation hängt, ich helf gezielt.

**Wenn alles läuft:** Ab 13.5. läuft die Maschine selbst. Du musst nur am 20.5. live im Webinar sein. Und am 31.5. um 23:59 den Cart manuell schliessen (falls Option B). 🚀
