# AC-Setup für Webinar-Mail-Sequenz Mama-CEO (3-Tage-Cart)

**Was du brauchst:** AC-Account (hast du), 30-45 Min Zeit, Tasse Kaffee.
**Was du am Ende hast:** Komplett automatisierte 12-Mail-Sequenz die Mai-Launch durchspielt.

---

## SCHRITT 1: Tags anlegen

In AC: **„Kontakte → Tags"** → diese Tags neu erstellen (falls nicht schon da):

| Tag | Wofür |
|---|---|
| `mama-ceo-webinar-anmeldung` | Wird automatisch durch das Anmelde-Form gesetzt ✓ (schon konfiguriert) |
| `mama-ceo-webinar-live-teilnehmer` | Setzt du manuell nach Webinar (für die die LIVE da waren) |
| `mama-ceo-webinar-kauf` | Wird gesetzt wenn jemand Mama-CEO via ThriveCart kauft (Webhook) |

---

## SCHRITT 2: Mails als Templates anlegen

In AC: **„Campaigns → Templates"** oder direkt in der Campaign-Erstellung.

Für jede der 12 HTML-Mails (`01-bestaetigung.html` bis `12-close-letzte2h.html`):

1. **„Neue Vorlage"** klicken → **„Code Editor"** wählen (HTML-Modus)
2. Name: z.B. „Webinar Mail 01 — Bestätigung"
3. **HTML-Code** aus der Datei komplett kopieren + einfügen
4. **Subject** aus dem `<title>`-Tag im HTML kopieren (oder aus Übersicht)
5. **Pre-Header** ist im HTML schon drin (im versteckten `<div>` ganz oben)
6. **Personalisierung:** `{{first_name}}` mit AC-Variable ersetzen (in AC: „Personalize" → Vorname-Tag einfügen)
7. **Speichern**

→ Das machst du 12x (~30 Min mit Kaffee). Tipp: Erst alle Templates anlegen, dann Automations bauen.

---

## SCHRITT 3: Automation 1 — „Webinar-Anmelder-Flow"

**Trigger:** Tag `mama-ceo-webinar-anmeldung` wird hinzugefügt
**Mails:** 1, 3, 4, 5

**Setup:**
1. AC → **„Automations → New"**
2. Name: „Mama-CEO Webinar — Anmelder"
3. Start-Trigger: **„Tag is added: mama-ceo-webinar-anmeldung"**
4. Aktionen nacheinander:
   - **Send Email:** Mail 01 (Bestätigung) — sofort
   - **Wait until:** Sonntag 17.5. 09:00
   - **Send Email:** Mail 03 (Story-Mail)
   - **Wait until:** Dienstag 19.5. 09:00
   - **Send Email:** Mail 04 (Reminder 24h)
   - **Wait until:** Mittwoch 20.5. 08:00
   - **Send Email:** Mail 05 (Reminder 1h, mit Zoom-Link!)

⚠️ **Wichtig:** Zoom-Link in Mail 05 vor Aktivierung einsetzen (Platzhalter `https://us02web.zoom.us/j/DEIN-ZOOM-LINK` ersetzen).

**Aktivieren** wenn das AC-Form live ist und Anmeldungen reinkommen.

---

## SCHRITT 4: Automation 2 — „Webinar-Day Mass-Send"

**Trigger:** Date-based — manuell ausgelöst oder als 3 separate Campaigns
**Mails:** 2, 6, 7

Diese 3 Mails gehen an **GANZE LISTE** (nicht nur Webinar-Anmelder).

### Mail 2 (1 Woche vor Webinar)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Sender: deine Adresse
3. Empfänger: deine Hauptliste (alle aktiven Kontakte)
4. Template: Webinar Mail 02
5. **Schedule:** Mi 13.5.2026 14:00
6. Senden

### Mail 6 ⭐ CLIFFHANGER (während Webinar läuft)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Empfänger: deine Hauptliste **MINUS** alle die schon Tag `mama-ceo-webinar-anmeldung` haben
   (Damit Anmelder die Cliffhanger-Mail NICHT bekommen — sie sind ja schon im Webinar)
   - Filter: „Empfänger hat NICHT Tag mama-ceo-webinar-anmeldung"
3. Template: Webinar Mail 06
4. **Schedule:** Mi 20.5.2026 09:15
5. Senden

⚠️ **Vor Aktivierung Zoom-Link in Mail 6 einsetzen!**

### Mail 7 (Cart-Open direkt nach Webinar)
1. AC → **„Campaigns → New Campaign → Standard"**
2. Empfänger: deine Hauptliste (alle)
3. Template: Webinar Mail 07
4. **Schedule:** Mi 20.5.2026 11:00
5. Senden

⚠️ **Vor Aktivierung Cart-Link einsetzen!** (`[Mama-CEO Cart-Link]` Platzhalter ersetzen mit ThriveCart-URL)
⚠️ **Replay-Link einsetzen!**

---

## SCHRITT 5: Automation 3 — „Cart-Window-Sequenz" (3-Tage-Cart)

**Trigger:** Date-based — startet Do 21.5.
**Mails:** 8-12

**Setup:** Eine Automation die nacheinander die 5 Cart-Mails schickt.

1. AC → **„Automations → New"**
2. Name: „Mama-CEO Cart-Window 3-Tage"
3. Start-Trigger: **„Wait until date: Do 21.5.2026 08:00"** (manuelle Aktivierung am Webinar-Tag)
4. Aktionen:
   - **Conditional Split:** Hat Tag `mama-ceo-webinar-kauf`? Wenn ja → END. Wenn nein → weiter.
   - **Send Email:** Mail 08 (Painpoint) — Do 21.5. 08:00
   - **Wait until:** Fr 22.5. 08:00
   - **Conditional Split:** Hat Tag `mama-ceo-webinar-kauf`? Wenn ja → END.
   - **Send Email:** Mail 09 (Aha KI, „morgen schliesst")
   - **Wait until:** Sa 23.5. 08:00
   - **Conditional Split:** Hat Tag `mama-ceo-webinar-kauf`? Wenn ja → END.
   - **Send Email:** Mail 10 (Close-Morgens, 16h)
   - **Wait until:** Sa 23.5. 18:00
   - **Conditional Split:** Hat Tag `mama-ceo-webinar-kauf`? Wenn ja → END.
   - **Send Email:** Mail 11 (Close-Abends, 6h)
   - **Wait until:** Sa 23.5. 22:00
   - **Conditional Split:** Hat Tag `mama-ceo-webinar-kauf`? Wenn ja → END.
   - **Send Email:** Mail 12 (Close-Last-2h)

**Wichtig — Käufer ausschliessen:**
Jede Mail mit einem **Conditional Split** vorgeschaltet: Wenn Tag `mama-ceo-webinar-kauf` vorhanden → Mail überspringen. So bekommt niemand Verkaufs-Mails der schon gekauft hat.

---

## SCHRITT 6: ThriveCart-Webhook

Wenn jemand Mama-CEO via ThriveCart kauft, soll automatisch Tag `mama-ceo-webinar-kauf` in AC gesetzt werden.

**Setup in ThriveCart:**
1. ThriveCart → Mama-CEO-Produkt → Settings → Integrations
2. ActiveCampaign verbinden (falls noch nicht)
3. Bei „Successful purchase" → **Add Tag: mama-ceo-webinar-kauf**

→ Damit werden Käufer automatisch aus den weiteren Verkaufs-Mails ausgeschlossen.

---

## SCHRITT 7: Test-Anmeldung

**Vor Aktivierung der Automation 1:**

1. Geh auf https://webinar.mumlifebalance.ch
2. Trag dich selbst mit Test-E-Mail ein
3. Check ob:
   - Tag `mama-ceo-webinar-anmeldung` wird gesetzt ✓
   - Mail 01 (Bestätigung) kommt sofort an ✓
   - Mail 03/04/05 kommen am richtigen Datum (kannst du im AC-Automation-Log sehen)

Wenn alles klappt: **Aktivieren** und Mai-Launch beginnt automatisch zu laufen.

---

## CHECKLISTE vor Aktivierung

- [ ] Alle 12 Templates angelegt + getestet (richtige Subjects + keine Broken-Links)
- [ ] **Zoom-Link** in Mail 5 + Mail 6 eingesetzt
- [ ] **Cart-Link** (ThriveCart-URL) in Mails 7-12 eingesetzt
- [ ] **Replay-Link** in Mail 7 eingesetzt
- [ ] Tag `mama-ceo-webinar-anmeldung` triggert Automation 1
- [ ] **ThriveCart-Webhook** für Tag `mama-ceo-webinar-kauf` eingerichtet
- [ ] Test-Anmeldung gemacht — alle Mails kommen wie geplant
- [ ] „Käufer-Ausschluss" in Cart-Window-Sequenz aktiv

---

## Fehler-Vermeidung

❌ **Doppel-Mails an Käufer:**
→ Conditional Split mit „Tag mama-ceo-webinar-kauf" in jeder Cart-Window-Mail

❌ **Zoom-Link fehlt am Live-Tag:**
→ Mail 5 + Mail 6 vor Aktivierung 2x prüfen

❌ **Cart-Link fehlt:**
→ Vor Mi 20.5. 11:00 in allen Mails 7-12 einsetzen

❌ **Falsche Empfänger-Liste:**
→ Mail 6 (Cliffhanger): Filter „NICHT Tag mama-ceo-webinar-anmeldung" damit Live-Teilnehmer es nicht bekommen

❌ **HTML-Email zeigt komische Zeichen oder „<table>"-Tags:**
→ Sicherstellen dass du im AC-Editor auf „Code Editor" / „HTML Source" gewechselt hast, nicht im visuellen Editor

---

**Bei Problemen:** Sag mir welche Mail/Automation hängt, ich helf gezielt.

**Wenn alles läuft:** Ab 13.5. läuft die Maschine selbst. Du musst nur am 20.5. live im Webinar sein. 🚀
