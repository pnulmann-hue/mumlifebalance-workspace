# AC-Setup für Webinar-Mail-Sequenz Mama-CEO

**Was du brauchst:** AC-Account (hast du), 30-45 Min Zeit, Tasse Kaffee.
**Was du am Ende hast:** Komplett automatisierte 16-Mail-Sequenz die Mai-Launch durchspielt.

---

## SCHRITT 1: Tags anlegen

In AC: **„Kontakte → Tags"** → diese Tags neu erstellen (falls nicht schon da):

| Tag | Wofür |
|---|---|
| `mama-ceo-webinar-anmeldung` | Wird automatisch durch das Anmelde-Form gesetzt ✓ (schon konfiguriert) |
| `mama-ceo-webinar-live-teilnehmer` | Setzt du manuell nach Webinar (für die die LIVE da waren) |
| `mama-ceo-webinar-replay-watcher` | Setzt du manuell wenn jemand Replay schaut |
| `mama-ceo-webinar-kauf` | Wird gesetzt wenn jemand Mama-CEO kauft (via ThriveCart-Webhook) |

---

## SCHRITT 2: Mails als Templates anlegen

In AC: **„Campaigns → Templates"** oder direkt in der Campaign-Erstellung.

Für jede der 16 Mails (`01-bestaetigung.html` bis `16-close-letzte2h.html`):

1. **„Neue Vorlage"** klicken
2. Name: z.B. „Webinar Mail 01 — Bestätigung"
3. **Subject** aus Mail-File kopieren (Zeile mit `**SUBJECT:**`)
4. **Pre-Header** aus Mail-File kopieren (Zeile mit `**PRE-HEADER:**`)
5. **Body** aus Mail-File kopieren (alles unter dem `---`)
   - Personalisierung: `{{first_name}}` mit AC-Personalisations-Tag ersetzen (in AC: Variable einfügen → Vorname)
6. **Speichern**

→ Das machst du 16x (~30 Min mit Kaffee). Tipp: Erst alle anlegen, dann Automations bauen.

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
   - **Wait:** bis Sonntag 17.5. 09:00 (oder „Wait until specific date")
   - **Send Email:** Mail 03 (Story-Mail)
   - **Wait:** bis Dienstag 19.5. 09:00
   - **Send Email:** Mail 04 (Reminder 24h)
   - **Wait:** bis Mittwoch 20.5. 08:00
   - **Send Email:** Mail 05 (Reminder 1h, mit Zoom-Link!)

⚠️ **Wichtig:** Zoom-Link in Mail 05 vor Activierung einsetzen (Platzhalter `https://us02web.zoom.us/j/DEIN-ZOOM-LINK` ersetzen).

**Aktivieren** wenn das AC-Form live ist und Anmeldungen reinkommen.

---

## SCHRITT 4: Automation 2 — „Webinar-Day Mass-Send"

**Trigger:** Date-based — manuell ausgelöst oder via Calendar
**Mails:** 2, 6, 7

Diese 3 Mails gehen an **GANZE LISTE** (nicht nur Webinar-Anmelder).

**Setup:**

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

⚠️ **Vor Aktivierung Cart-Link einsetzen!** (`[Mama-CEO Link]` Platzhalter ersetzen mit ThriveCart-URL)
⚠️ **Replay-Link einsetzen!**

---

## SCHRITT 5: Automation 3 — „Cart-Window-Sequenz"

**Trigger:** Date-based — startet nach Cart-Open am 20.5.
**Mails:** 8-16

**Setup:** Eine Automation die nacheinander die 9 Cart-Window-Mails schickt.

1. AC → **„Automations → New"**
2. Name: „Mama-CEO Cart-Window"
3. Start-Trigger: **„Wait until date: Do 21.5.2026 08:00"** (manuelle Aktivierung am Webinar-Tag)
4. Aktionen:
   - **Send Email:** Mail 08 (Painpoint) — Do 21.5. 08:00
   - **Wait until:** Fr 22.5. 08:00
   - **Send Email:** Mail 09 (Aha KI)
   - **Wait until:** Sa 23.5. 08:00
   - **Send Email:** Mail 10 (Sozial-Beweis)
   - **Wait until:** So 24.5. 09:00
   - **Send Email:** Mail 11 (Replay aus)
   - **Wait until:** Mo 25.5. 09:00
   - **Send Email:** Mail 12 (Letzte Tage)
   - **Wait until:** Di 26.5. 09:00
   - **Send Email:** Mail 13 (Final Push)
   - **Wait until:** Mi 27.5. 08:00
   - **Send Email:** Mail 14 (Close morgens)
   - **Wait until:** Mi 27.5. 18:00
   - **Send Email:** Mail 15 (Close abends)
   - **Wait until:** Mi 27.5. 22:00
   - **Send Email:** Mail 16 (Close letzte 2h)

**Wichtig — Käufer ausschliessen:**
Bei jeder Mail einen **„Conditional Split"** vorschalten: Wenn Tag `mama-ceo-webinar-kauf` vorhanden → Mail überspringen. So bekommt niemand Verkaufs-Mails der schon gekauft hat.

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

**Vor Activierung der Automation 1:**

1. Geh auf https://webinar.mumlifebalance.ch
2. Trag dich selbst mit Test-E-Mail ein
3. Check ob:
   - Tag `mama-ceo-webinar-anmeldung` wird gesetzt ✓
   - Mail 01 (Bestätigung) kommt sofort an ✓
   - Mail 03/04/05 kommen am richtigen Datum (kannst du im AC-Automation-Log sehen)

Wenn alles klappt: **Activieren** und Mai-Launch beginnt automatisch zu laufen.

---

## CHECKLISTE vor Activierung

- [ ] Alle 16 Templates angelegt + getestet (richtige Subjects + keine Broken-Links)
- [ ] Zoom-Link in Mail 5 + Mail 6 eingesetzt
- [ ] Cart-Link (ThriveCart-URL) in Mails 7-16 eingesetzt
- [ ] Replay-Link in Mail 11 eingesetzt
- [ ] Real-Quotes in Mail 10 eingesetzt (sobald erste Pilot-Käufer da sind!)
- [ ] Tag `mama-ceo-webinar-anmeldung` triggert Automation 1
- [ ] ThriveCart-Webhook für Tag `mama-ceo-webinar-kauf` eingerichtet
- [ ] Test-Anmeldung gemacht — alle Mails kommen wie geplant
- [ ] „Käufer-Ausschluss" in Cart-Window-Sequenz aktiv

---

## Fehler-Vermeidung

❌ **Doppel-Mails an Käufer:**
→ Conditional Split mit „Tag mama-ceo-webinar-kauf" in jeder Cart-Window-Mail

❌ **Zoom-Link fehlt am Live-Tag:**
→ Mail 5 + Mail 6 vor Activierung 2x prüfen

❌ **Cart-Link fehlt:**
→ Vor Mi 20.5. 11:00 in allen Mails 7-16 einsetzen

❌ **Falsche Empfänger-Liste:**
→ Mail 6 (Cliffhanger): Filter „NICHT Tag mama-ceo-webinar-anmeldung" damit Live-Teilnehmer es nicht bekommen

---

**Bei Problemen:** Sag mir welche Mail/Automation hängt, ich helf gezielt.

**Wenn alles läuft:** Ab 13.5. läuft die Maschine selbst. Du musst nur am 20.5. live im Webinar sein.

🚀
