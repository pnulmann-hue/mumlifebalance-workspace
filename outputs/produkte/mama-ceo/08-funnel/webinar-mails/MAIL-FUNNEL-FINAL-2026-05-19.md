---
tags: [produkt, mama-ceo, launch]
---

# Mama-CEO Mail-Funnel — FINAL 2026-05-19

**Stand:** 2026-05-19, Webinar-Tag: Mi 20.5.2026 09:00
**Total:** 15 Mails über 3 Strecken
**Voice:** Patricia-Brand, Schweizer ss, Hormozi-Layer, bgcolor-Fallbacks für mobile Clients

---

## 📋 Komplett-Übersicht

### Anmelder-Strecke (Tag `0€ Webinar Mama-CEO` JA, Tag `mama-ceo-kauf` NEIN)

| # | Wann | Mail | HTML im Chat? |
|---|---|---|---|
| 1 | Sofort nach Anmeldung | Anmelde-Bestätigung | im Archiv `01-bestaetigung.html` |
| 2 | Mi 20.5. 08:00 | 1h-Reminder mit Zoom-Link | ✓ Chat-Version (mit bgcolor-Fix) |
| 3 | Mi 20.5. ~11:00 | Replay-Mail mit Cart-Open | ✓ Chat-Version |
| 4 | Do 21.5. 08:00 | Painpoint #1 „Heute schaff ich's wirklich" | ✓ Chat-Version |
| 5 | Sa 23.5. 19:00 | Earlybird Last 5h | ✓ Chat-Version |
| 6 | Mi 27.5. 08:00 | Antikunden „Für wen NICHT" | ✓ Chat-Version |
| 7 | Fr 29.5. 08:00 | Persönlicher Brief (Wendepunkt-Story) | ✓ Chat-Version |
| 8 | So 31.5. 19:00 | Cart-Close Last 5h | ✓ Chat-Version |

### Käufer-Strecke (Tag `mama-ceo-kauf` JA — Automation-Trigger)

| # | Wann | Mail | HTML im Chat? |
|---|---|---|---|
| 9 | Sofort nach Kauf | Welcome-Mail mit Telegram + Live-Termine + Zoom | ✓ Chat-Version |

### Newsletter-Mass-Send (Liste 2 · Tag `0€ Webinar Mama-CEO` NEIN · Tag `mama-ceo-kauf` NEIN)

| # | Wann | Mail | HTML im Chat? |
|---|---|---|---|
| M1 | Mi 20.5. 14:00 | Recap nach Webinar | ✓ Chat-Version |
| M2 | Do 21.5. 08:00 | Painpoint Newsletter | ✓ Chat-Version |
| M3 | Sa 23.5. 19:00 | Earlybird Last 5h Newsletter | ✓ Chat-Version |
| M4 | Mi 27.5. 08:00 | Persönlicher Brief light | ✓ Chat-Version |
| M5 | Fr 29.5. 08:00 | Antikunden Newsletter | ✓ Chat-Version |
| M6 | So 31.5. 19:00 | Cart-Close Last 5h Newsletter | ✓ Chat-Version |

---

## 🚨 Platzhalter — ALLE Mails durchsuchen + ersetzen

| Platzhalter | Was rein | Wo |
|---|---|---|
| `%FIRSTNAME%` | AC-Personalisations-Tag (automatisch durch AC) | Alle Mails |
| `[MAMA-CEO CART-LINK]` | `https://mumlifebalance.thrivecart.com/mama-ceo/` (oder deine echte URL) | Alle Pitch + Welcome + Mass-Send |
| `[VIMEO-REPLAY-LINK]` | Vimeo-URL (passwortgeschützt, 48h) | Mail 3 + Mail 4 |
| `[TELEGRAM-GRUPPE-LINK]` | `https://t.me/+ZLzeEEok6A02MjRk` | Mail 9 (Welcome) ✓ schon drin |
| Zoom-Link | `https://us06web.zoom.us/j/87272928633?pwd=...` | Mail 9 (Welcome) ✓ schon drin |
| `Fr 22.5. 11:00` (Replay-Ende) | Anpassen falls Replay-Fenster anders | Mail 3 + Mail 4 P.S. |

---

## ⚙️ AC-Setup pro Strecke

### Anmelder-Automation („0€ Webinar Mama-CEO" Auto, ID 60)
Bereits in AC aktiv. Du musst:
1. Mail 2 (1h-Reminder) mit Zoom-Link bestücken
2. Mails 3-8 als geplante Campaigns anlegen mit Filter „Tag `0€ Webinar Mama-CEO` ist gesetzt UND Tag `mama-ceo-kauf` ist nicht gesetzt"

### Käufer-Automation (NEU bauen)
1. Trigger: Tag `mama-ceo-kauf` wird hinzugefügt (via ThriveCart-Webhook)
2. Send Email: Welcome-Mail (Mail 9) sofort
3. Done — keine weiteren Mails nötig (Telegram + Live-Termine sind im Welcome erklärt)

### Newsletter-Mass-Send (6 geplante Campaigns)
Pro Campaign:
1. Empfänger: Liste 2 (Regulärer Newsletter)
2. Add condition: Tag `0€ Webinar Mama-CEO` **does NOT have**
3. Add condition: Tag `mama-ceo-kauf` **does NOT have**
4. Schedule: laut Timing-Tabelle oben

---

## ✅ Operative Checklist für morgen

**Heute Abend / vor Mi 20.5. 09:00:**
- [ ] Mail 2 (1h-Reminder) Zoom-Link in AC bestücken
- [ ] AC-Automation Anmelder-Strecke aktivieren
- [ ] Werbeanzeige URL umstellen auf `https://mumlifebalance.ch/ki-webinar`
- [ ] Test-Anmeldung machen (eigene E-Mail) → check ob Mail 1 ankommt
- [ ] Tag 73 + 74 in AC-UI löschen (Cleanup)

**Mi 20.5. nach Webinar (ca. 11:00):**
- [ ] Vimeo-Replay-Link hochladen + passwortgeschützt
- [ ] Mail 3 (Replay) in AC bestücken (Vimeo-Link + Cart-Link) + senden
- [ ] Mail M1 (Mass-Send Recap) senden um 14:00 mit Doppel-Ausschluss-Filter

**Do 21.5. 08:00:**
- [ ] Mail 4 (Anmelder Painpoint) senden
- [ ] Mail M2 (Newsletter Painpoint) senden

**Sa 23.5. 19:00:**
- [ ] Mail 5 (Anmelder Earlybird Last 5h) senden
- [ ] Mail M3 (Newsletter Earlybird Last 5h) senden

**Mi 27.5. 08:00:**
- [ ] Mail 6 (Anmelder Antikunden) senden
- [ ] Mail M4 (Newsletter Persönlicher Brief light) senden

**Fr 29.5. 08:00:**
- [ ] Mail 7 (Anmelder Persönlicher Brief) senden
- [ ] Mail M5 (Newsletter Antikunden) senden

**So 31.5. 19:00:**
- [ ] Mail 8 (Anmelder Cart-Close Last 5h) senden
- [ ] Mail M6 (Newsletter Cart-Close Last 5h) senden

**ThriveCart-Webhook** (sollte schon laufen):
- Bei erfolgreichem Kauf → Tag `mama-ceo-kauf` setzen → Welcome-Automation triggert sofort

---

## 📞 Im Notfall

Wenn was hängt oder eine Mail nicht stimmt: `claude --continue` → diesen Chat öffnen → Mail-HTML neu rauskopieren.

Alle 15 Mail-HTMLs sind im Konversations-Verlauf gespeichert. Falls Chat verloren geht: Backup wäre Patricia's WordPress-LP (`https://mumlifebalance.ch/ki-webinar`) — die nutzt das gleiche Brand-Voice + Layout-Pattern als Referenz.

---

## 🎯 Brand-Voice-Regeln (für alle Mails konsistent eingehalten)

- Schweizer ss durchgängig
- Keine Stakkato-Sätze (Konjunktionen, fließend)
- Keine Wortverbote: „Mompreneur", „Cohort", „techie", „Pilot-Preis", „Mastermind"
- Patricia-Story-Chronologie korrekt: Schwester †2019 mit 44 · Patricia kündigte 2023 · Mai 2025 Wendepunkt
- Hormozi-Pattern: 1 Idee pro Mail, Pain-First, Bold-Claim → Reason-Why, P.S. als 2. Subject-Line
- bgcolor-Fallbacks in JEDEM `<td style="background-color:...">` für mobile Clients
- Farben: Petrol #29556d · Dunkelblau #0c1c30 · Creme #f1ecdd · Orange #dc822e
- Fonts: Georgia (Headlines) + Arial (Body)

---

**Letzter Stand:** 2026-05-19 spätabends
**Patricia:** schlafen gegangen 🌙
**Next:** Webinar morgen Mi 20.5. 09:00 — Säule 1 Lektion-Skripte folgen
