# Pre-Launch & Monitoring Checkliste — Bio-Check-Bot

> Pflicht-Routine bevor du Werbebudget reinpumpst, plus Daily/Weekly-Check während aktiver Kampagnen.

---

## Vor jeder Ad-Kampagne (15 Min)

- [ ] **Health-Check** grün: https://bio-check-bot.vercel.app/api/health → muss `{"status":"ok"}` zeigen
- [ ] **Bot live testen** — kompletter Flow:
  - [ ] URL aufrufen mit Test-Params: `?e=test@example.com&n=Test`
  - [ ] Bot lädt mit Patricia-Foto + Begrüssung
  - [ ] Ein paar Antworten geben — Bot reagiert sinnvoll
  - [ ] Bis zum Ende durchklicken
  - [ ] PDF-Mail kommt in Test-Inbox an
  - [ ] AC-Tag „Bio-Check abgeschlossen" (60) ist gesetzt am Test-Kontakt
- [ ] **Mail-Sequenz testen** — neuen Test-Lead ins AC-Formular eintragen:
  - [ ] DOI-Mail kommt sofort
  - [ ] Bestätigung klicken → Auslieferungs-Mail kommt
  - [ ] Link in Auslieferungs-Mail funktioniert (führt zum Bot, nicht 404)
- [ ] **Vercel Dashboard** — letzte Bereitstellung „Bereit", keine Fehler
- [ ] **UptimeRobot** zeigt Status „Up" für mindestens 24h
- [ ] **AC-Automationen** aktiv (kein „Pausiert"-Status)

---

## Daily während aktiver Kampagne (2 Min)

- [ ] Mail-Inbox: keine UptimeRobot-Down-Mails übersehen?
- [ ] Vercel Dashboard kurz öffnen: Fehlerrate < 5%?
- [ ] Bot-URL einmal aufrufen — lädt sofort?
- [ ] Neue Bio-Check-Leads im AC sichtbar?

---

## Weekly (15 Min)

- [ ] **Vercel → Beobachtbarkeit** öffnen — Fehlerrate-Trend ansehen
- [ ] **Vercel → Verwendung** — bist du noch im Free-Tier? (oder läuft Pro-Subscription?)
- [ ] **Anthropic Console → Usage** — API-Kosten unter Plan?
- [ ] **AC** → wieviele Leads diese Woche? Conversion zu „Bio-Check abgeschlossen"-Tag?
- [ ] **Echter End-to-End-Test** mit neuer Test-Mailadresse — alles funktioniert?

---

## Bei Bot-Ausfall (Notfall-Protokoll)

1. **Zuerst:** Ads pausieren! Sonst Geld in 404-Klicks verbrannt.
   - Meta Ads Manager → alle Bio-Check-Ads → Pause
2. **Diagnose:**
   - `https://bio-check-bot.vercel.app/api/health` aufrufen
   - Vercel Dashboard → letzte Bereitstellung checken
   - Siehe `VERCEL-SETTINGS.md` → Recovery-Steps
3. **Nach Fix:**
   - 10 Min UptimeRobot-Status warten (mindestens 2 Up-Checks)
   - End-to-End-Test (kompletter Flow inkl. PDF)
   - Ads wieder aktivieren

---

## Monitoring-Setup (einmalig)

### UptimeRobot
- Account: https://uptimerobot.com (kostenlos)
- Monitor 1: `https://bio-check-bot.vercel.app/api/health`
  - Type: HTTP(s)
  - Interval: 5 Min
  - Alert Contacts: deine Mail
  - **Wichtig:** Erwartet HTTP 200 — bei 503 (= ENV fehlt) wird automatisch alarmiert
- Monitor 2: `https://bio-check-bot.vercel.app/`
  - Type: HTTP(s)
  - Interval: 5 Min
  - Erkennt komplettes Down (404, DNS-Fehler, Timeout)

### Vercel-Notifications
- Account Settings → Notifications
- Aktivieren: „Failed Deployments", „Deployment Status Changes"

### Optional: Telegram-Push für UptimeRobot
- Telegram-Bot @BotFather → neuen Bot erstellen → Token
- UptimeRobot → My Settings → Add Alert Contact → Telegram → Token + Chat-ID eintragen
- Bei Down-Event: sofortige Push-Nachricht aufs Handy (statt nur Mail)

---

## Was bei welcher Art von Fehler tun

| Symptom | Wahrscheinliche Ursache | Fix |
|---|---|---|
| 404 auf Bot-URL | Stammverzeichnis-Setting verloren | `VERCEL-SETTINGS.md` → Recovery-Steps |
| 503 auf `/api/health` | ENV-Variable fehlt | Im Health-Response steht welche → in Vercel ergänzen |
| Bot lädt aber antwortet nicht | `ANTHROPIC_API_KEY` ungültig oder Limit erreicht | Anthropic Console → Key prüfen, Plan-Limit checken |
| Bot lädt, kein PDF | `BLOB_READ_WRITE_TOKEN` fehlt oder PDF-API-Bug | Vercel → Storage → Blob-Token prüfen, Logs |
| AC-Tag wird nicht gesetzt | `AC_API_KEY` ungültig oder falsche Tag-IDs | AC → Settings → Developer → Key prüfen |
| Mail kommt nicht | AC-Automation pausiert oder Trigger falsch | AC → Automations → Status prüfen |

---

_Letztes Update: 2026-04-25 — Health-Endpoint live mit Commit Stufe-2-Monitoring_
