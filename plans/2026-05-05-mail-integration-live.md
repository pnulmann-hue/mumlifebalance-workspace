# Mail-Integration für Briefing-System (LIVE)

> **Erstellt:** 2026-04-21 · Live seit 2026-05-05
> **Status:** Phase 1 + 2 umgesetzt (täglich automatisch). Phase 3 (PDF-Briefing) offen.

## Ziel

3 Mailboxen mit ungelesenem Backlog (GMX 730+, Gmail 730, Hoststar 77) automatisch sortieren. Bot prüft täglich, klassifiziert mit Claude, verschiebt in passende Ordner, schickt DMs nur bei wirklich wichtigen Mails.

## ✅ Was umgesetzt ist (Stand 2026-05-05)

### Mailboxen via IMAP
- **GMX:** imap.gmx.net:993 SSL (pnulmann@gmx.ch)
- **Hoststar:** lx30.hoststar.hosting:143 STARTTLS (info@mumlifebalance.ch)
- **Gmail:** imap.gmail.com:993 SSL (pnulmann@gmail.com — App-Password mit 2FA)

Credentials lokal in `.secrets/mail-credentials.txt` (gitignored).
Auf Railway als ENV-Vars: `GMX_IMAP_*`, `HOSTSTAR_IMAP_*`, `GMAIL_IMAP_*`.

### Klassifikation 7 Kategorien
| Kategorie | Aktion |
|---|---|
| 🚨 wichtig | bleibt INBOX (ungelesen) + Telegram-PUSH |
| 💡 learning | INBOX/Learnings, gelesen |
| 🧾 rechnung | INBOX/Rechnungen, gelesen |
| 📢 werbung | INBOX/Werbung, gelesen |
| 🚫 spam | Spam-Ordner, gelesen |
| ℹ️ info | bleibt INBOX, gelesen |
| 🤐 ignored | unverändert |

**Bestehende Patricia-Ordner werden bevorzugt:**
INBOX/Business · /Garteninfos · /Backen · /Niklaus · /Kreuzfahrt · /Kurszugänge (Hoststar) · /Zeitschriften (Hoststar)

**Standard-Ordner werden auto-erstellt:** INBOX/Wichtig · /Learnings · /Rechnungen · /Werbung

**Spam-Mapping pro Mailbox:** GMX→Spamverdacht · Hoststar→Junk-E-Mail · Gmail→[Gmail]/Spam

### Sicherheit
**NIEMALS** automatisch endgültig löschen. Nur in Spam-Ordner verschieben + als gelesen markieren. Endgültiges Löschen nur auf manuellen Befehl (kommt mit Phase 3).

### Automatisierung
- **Daily Cron 07:00** auf Railway (in `index.ts` integriert)
- **Mailassistent-Bot** @mailassistent_mumlifebalance_bot sendet PUSH-DMs + Zusammenfassung am Ende jedes Sweeps

### Code-Files
- `scripts/telegram-userbot/src/mail-classifier.ts` — Claude-Prompt für 7 Kategorien + Audience-Mapping
- `scripts/telegram-userbot/src/mail-poller.ts` — IMAP-Fetcher, Folder-Management, Move + Read-Flag
- `scripts/telegram-userbot/src/mailassistant.ts` — DM-Sender via Bot-Token
- `scripts/telegram-userbot/src/run-mail-sweep-all.ts` — Manueller Trigger
- `scripts/telegram-userbot/src/index.ts` — Cron-Integration (`isMailSweepTime` 07:00-Check)

### Erster Sweep-Lauf 2026-05-05
- GMX: 290 Mails sortiert, 14 PUSH
- Hoststar: 78 Mails sortiert, 2 PUSH
- Gmail: 730 Mails sortiert, 41 PUSH (allein!)
- **Total: 1100+ Mails geordnet, 57 PUSH-DMs**

## ⏸️ Phase 3 (offen — separate Session)

### Wöchentliches PDF-Briefing (Sonntagabend 18:00)
PDF mit allen Mails der Woche, gruppiert:
- 🚨 Wichtig · 💡 Learnings · 🧾 Rechnungen · 📢 Werbung · 🚫 Spam (nur Anzahl)

Format pro Mail: `[Mail #3] Von: ... | Betreff: ... | Auszug: ... | [Vollständiger Inhalt auf Seite 4]`

### Chat-Commands für Korrekturen
Patricia interagiert via Mailassistent-Bot:
- `Mail 3 → Kochbot` → Bot sendet Rezept an Notion-Rezepte-DB
- `Mail 5 → Business-Wissen` → Newsletter-Inhalt in `documents` (category=business)
- `Mail 7 → Rechnungen zu bezahlen` → IMAP-Move
- `Mails 12-18 löschen` → endgültiges Löschen (manuell ausgelöst)
- `Mail 4 antworten: Hallo Anne...` → Draft im Mail-Account
- `Mail 5 war keine Werbung` → Korrektur-Lerneffekt

### Tech-Details Phase 3
- PDF-Generator: wiederverwende `scripts/md-to-pdf/` (Puppeteer + Brand-Look)
- Chat-Parser: erweitere bestehende approval-handler.ts mit Mail-Commands
- Notion-Integration: Rezepte-DB + Business-Wissen-DB als Ziele

### Geschätzter Aufwand Phase 3
~3-5h aufgeteilt auf 1-2 Sessions.

## Nächste Schritte

1. Phase 3 starten wenn Patricia bereit ist (PDF-Briefing + Chat-Commands)
2. Optional: Filter-Tuning falls Klassifikator danebenliegt (Patricia kann Beispiel-Mails zur Korrektur schicken)
3. Mail-Korrektur-Lernpfad: Wenn Patricia "Mail 5 war keine Werbung" sagt → Bot lernt für ähnliche Sender
