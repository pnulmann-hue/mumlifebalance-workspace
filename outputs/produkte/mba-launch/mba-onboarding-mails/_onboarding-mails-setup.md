---
tags: [produkt, mba, mails, funnel, intern]
---

# MBA-Onboarding-Mails — die Auslieferungs-Strecke (nach dem Kauf)

> Diese 3 Mails gehen raus, **sobald jemand die MBA kauft** (ThriveCart → ActiveCampaign-Tag `MBA-Kauf`).
> Nicht zu verwechseln mit den Bootcamp-Mails (`bootcamp-mails/`) — die laden ins kostenlose Bootcamp ein.
> Voice-Regeln: Freundin-Ton, keine Stakkato-Sätze, Schweizer ss, keine erfundenen Zahlen, kein Mentor-Name.

---

## 📨 Die Strecke

| Mail | Wann | Zweck |
|---|---|---|
| **M1 · Willkommen** | sofort nach Kauf | Du bist drin · alle 3 Zugänge · du startest SOFORT (Live-Calls ab August) |
| **M2 · Wegweiser** | Tag 2 nach Kauf | „3 Kurse — wo fang ich an?" → klare Reihenfolge, kein Überforderungs-Abbruch |
| **M3 · Calls starten** | Anfang August | Erinnerung Live-Calls + Termin + Vorfreude |

---

## ⚠️ 3 Platzhalter — die musst nur DU einmal füllen

In allen 3 HTML-Dateien sind diese Platzhalter (einmal mit Suchen/Ersetzen austauschen, dann fertig):

1. **`[ACADEMY-LINK]`** — der Login-Link zu deiner ThriveCart Academy (wo die 3 Kurse liegen).
   → Tipp: ThriveCart schickt die Zugangsdaten zur Academy automatisch in einer eigenen Mail. M1 verweist darauf + verlinkt zusätzlich den Login.
2. **`[UMSETZERINNEN-GRUPPE-LINK]`** — der Link zum **Community-/Austausch-Bereich deiner ThriveAcademy** (NICHT mehr Telegram — Entscheidung 30.6.2026: die MBA-Community läuft komplett in der Academy).
   → Kein separates Telegram für die MBA mehr erstellen. Stattdessen in ThriveAcademy die Spaces einrichten (Q&A + Lounge + Announcements) und hier den Community-Link einsetzen. Die Mail-Wörter „Gruppe / Der Gruppe beitreten" passen weiterhin — sie meinen jetzt diesen Academy-Bereich.
3. **`[ERSTER-CALL-DATUM]`** (nur in M3) — Datum/Uhrzeit eures ersten Experten-Calls nach den Sommerferien.

**PIA-Link** ist schon fix drin: `https://pia.mumlifebalance.ch` (Mitglieder registrieren sich mit ihrer Kauf-Mail).

---

## ⚙️ ActiveCampaign-Setup (wenn du sie scharf schaltest)

- **Auslöser:** ThriveCart sendet Tag `MBA-Kauf` (oder Listen-Eintrag) → Automation startet.
- **M1** sofort · **M2** +2 Tage · **M3** als Datum-Mail Anfang August (oder manuell als Broadcast an alle MBA-Käuferinnen).
- Absender: Patricia · Reply-To: info@mumlifebalance.ch
- `%FIRSTNAME%` = AC-Personalisierungs-Tag (wie in deinen anderen Mails).

## 🔗 Verwandte Notizen
- [[mba-thrivecart-bausteine]] · [[telegram-gruppe-bootcamp]] · [[network-mama-tiefenanalyse]]
