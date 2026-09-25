---
tags: [produkt, funnel, ki-launch]
---

# Funnel-Gerüst KI-Launch — Stimm-Check + Masterclass

**Stand:** 25.09.2026 · Getestet wird am Schluss, wenn alles steht (Patricia).

```
Feed STIMME / Story-Link ─► /stimm-check/ ─► AC-Formular ─► Opt-in-Mail ─► /stimm-check-los/ ─► Tool
                                                                              │
Newsletter / Storys ─► /ki-masterclass/ ─► Formular 69 ─► Opt-in-Mail ─► /ki-masterclass-danke/
                              ▲                                               │
                              └──────── Masterclass-Hinweis ◄─────────────────┘ (Seite, Mail, Tool-Ende)
```

## Seiten (WordPress, alle mit der .pif-Gestaltung aus dem Customizer)

| Seite | WP | Status | Was fehlt noch |
|---|---|---|---|
| `/stimm-check/` Landingpage | 4262 | Entwurf | Adresse des Stimm-Check-Formulars |
| `/stimm-check-los/` nach der Bestätigung, mit Masterclass-Hinweis | 4263 | Entwurf | Adresse des Tools |
| `/ki-masterclass/` Landingpage | 4266 | Entwurf | nichts — Knöpfe zeigen auf Formular 69 |
| `/ki-masterclass-danke/` nach der Bestätigung | 4258 | **live** | Stimm-Check-Block erscheint, sobald das Tool läuft |

Deploy: `scripts/wordpress/deploy-stimm-check-seiten.mjs` (die ersten drei) und
`deploy-ki-masterclass-danke.mjs`. Quellen in `outputs/salespages/*.html`.

## ActiveCampaign

**Tags — je Funnel einer (Patricias Entscheid 25.09.):** 100 `0€ KI Webinar` · 105 `0€ Stimmcheck`

### Formular 69 — Masterclass (umstellen, 👩)
- Tag **`0€ KI Webinar`** (100) statt „0€ Idee“ · Liste 2 bleibt
- Nach dem Absenden: **Danke-Nachricht** — *Fast geschafft! Schau kurz in dein Postfach und klick auf „Ja, ich bin dabei“, erst dann kommt dein Zoom-Link. Keine Mail da? Schau im Spam-Ordner nach.*
- Opt-in-Mail: `mails/masterclass-00-optin.html` · nach der Bestätigung weiterleiten auf `https://mumlifebalance.ch/ki-masterclass-danke/`
- Du statt Sie in den Feldern, Datenschutz-Häkchen **nicht** vorangekreuzt, Untertitel „hinter **die** Kulissen“

### Neues Formular — Stimm-Check (anlegen, 👩: Formular 69 duplizieren)
- **Name:** 0€ Stimm-Check · **Titel:** Dein Stimm-Check · **Untertitel:** Die sechs Angaben, die deine KI von dir braucht, damit sie klingt wie du
- **Felder:** Vorname („Dein Vorname“) · E-Mail („Deine E-Mail“) · Datenschutz, nicht vorangekreuzt
- **Knopf:** Zum Stimm-Check
- **Aktion:** Tag **`0€ Stimmcheck`** (105) · Liste 2
- **Nach dem Absenden:** Danke-Nachricht — *Fast geschafft! Schau kurz in dein Postfach und klick auf „Ja, ich will meinen Stimm-Check“, dann kannst du sofort loslegen.*
- **Opt-in-Mail:** `mails/stimm-00-optin.html` · nach der Bestätigung weiterleiten auf `https://mumlifebalance.ch/stimm-check-los/`
- **Danach mir die Formular-ID schicken** → kommt in `FORMULAR` im Deploy-Skript

### Automationen (👩, Texte liegen fertig)
- **„Stimm-Check“**: Auslöser Tag `0€ Stimmcheck` → sofort Mail `stimm-01-auslieferung.html` (persönlicher Tool-Link mit `?e=%EMAIL%&n=%FIRSTNAME%`, Masterclass-Kasten)
- **„KI-Masterclass Okt 2026“**: Auslöser Tag `0€ KI Webinar` → Erinnerung Mi 7.10. 19:00 · „Wir sind live“ Do 8.10. 08:55 · Aufzeichnung Do 16:00 · Pitch Fr 9.10. + Sa 10.10. (Texte folgen, Plan im Launch-Kalender)

Alle Mails zum Kopieren: `preview_start {"name": "ki-masterclass-mail"}` → Knopf „Ganzes HTML“.
Gebaut von `scripts/ki-kurs/masterclass-mails-bauen.py`.

## Das Tool

`scripts/stimm-check/` — Gehirn lokal getestet (Sonnet 5, ohne Denkphase, rund 20 + 10 Sekunden,
Blacklisten-Prüfung mit Korrekturrunde, Zielgruppe neutral, Schreibsprache folgt der Textprobe).
Lokal: `preview_start {"name": "stimm-check"}` → Port 4397. Knopf am Ende → Formular 69.

**Offen:** Deploy auf Vercel + ENV `ANTHROPIC_API_KEY` (keine Tag-Variablen — ohne sie setzt
das Tool keine Tags, und genau das ist gewollt). Danach die Adresse an drei
Stellen eintragen: `TOOL` in `deploy-stimm-check-seiten.mjs` · `TOOL_URL` in
`masterclass-mails-bauen.py` · `STIMM_CHECK` in `deploy-ki-masterclass-danke.mjs`.

## Reihenfolge bis zum Test

1. 👩 Formular 69 umstellen, Stimm-Check-Formular anlegen → ID an Claude
2. 🤖 Tool auf Vercel (mit deinem OK), Adressen eintragen, Seiten neu ausspielen
3. 👩 Automationen „Stimm-Check“ und „KI-Masterclass“ anlegen, Mails einfügen
4. 👩 Seiten veröffentlichen
5. 🧪 **Test von vorne bis hinten** mit deiner eigenen Adresse: Landingpage → Formular →
   Opt-in → Seite → Tool → Mail → Masterclass-Anmeldung
6. 🤖 ManyChat `STIMME` → DM mit Link auf `/stimm-check/`
