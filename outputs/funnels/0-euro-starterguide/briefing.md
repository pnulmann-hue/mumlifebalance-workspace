---
tags: [funnel, mentoring, starterguide]
---

# 0€ Instagram-Starterguide — Landingpage (WordPress-Migration)

**Erstellt:** 2026-06-10
**Status:** WP-Draft gebaut, noch nicht publiziert
**Funnel-ID:** `0-euro-starterguide` (siehe `context/active-funnels.json`)

---

## Warum dieser Funnel umgebaut wird

Der Starterguide lag bisher auf einer **Netlify-Seite** (`starterguide-mumlifebalance.netlify.app`).
Zwei Probleme:

1. **Vermutlich falscher Inhalt:** Patricia hat festgestellt, dass auf der Netlify-Seite die **Lead-Challenge** statt des Starterguide-Inhalts steht — wahrscheinlich wurde beim Aufsetzen eine Lead-Challenge-Vorlage kopiert und nie ausgetauscht. (Konnte aus der Sandbox nicht verifiziert werden — Netlify ist `host_not_allowed`.)
2. **Falscher Bio-Link:** Der „Starterguide"-Button auf `mumlifebalance.ch/bio` zeigt auf die Bio-Seite selbst (Endlosschleife) statt zum Guide.

**Lösung:** Native WordPress-Seite `/instagram-starterguide` mit korrektem Starterguide-Inhalt, frisch gebaut nach Julia-Trost-Landing-Struktur + Hormozi-Hooks + Patricia-Brand.

---

## Seiten-Aufbau (Julia-Trost-Landing)

1. **Hero** — Hormozi-Headline (Ergebnis + Avatar): „von ‚mich sieht niemand' zu einem Profil, das deine Wunschkundin anzieht"
2. **Pain** — „Instagram fühlt sich an wie eine Bühne, auf die sich niemand setzt"
3. **Bridge** — „Sichtbar werden ist keine Typ-Frage, sondern eine Struktur-Frage" (Schaufenster-Metapher)
4. **Inhalt** — 4 Schritte aus dem Guide: ① Die Idee · ② Die Nische · ③ Das IG-Profil · ④ Checkliste
5. **Für wen** — Qualifizierung Network-Mamas
6. **Über Patricia** — kurze Authority + Foto
7. **Opt-in** — ActiveCampaign-Formular (Anker `#anmelden`)
8. **Footer**

Inhaltsquelle: `context/patricia-freebies.md` → Abschnitt „3. 0€ Starter-Guide für Instagram".

---

## ✅ Erledigt

- **AC-Formular** angelegt: **Form #53**, Token `db2daad7-aa19-4b73-a6de-63c5735b0fc0` (Headline: „Deine ersten Schritte, die du auf Instagram beachten musst, um daraus für dein Network Kunden zu finden")
- Echter Embed-Code (inkl. reCAPTCHA + AC-Script) in `landing/index.html` eingesetzt, Brand-Override drübergelegt (Creme-Karte / Petrol-Titel / oranger Button)

## ✅ Erledigt (Fortsetzung)

- **AC-Auslieferung** steht bereits (Form #53 war schon vorhanden + verschickt das PDF) — von Patricia bestätigt 2026-06-10

## ⚠️ Offene TODOs vor Live-Schaltung

| # | Aufgabe | Wer |
|---|---------|-----|
| 1 | Deploy: `cd scripts/wordpress && node --env-file=.env deploy-starterguide.js` (braucht `.env` mit WP-App-Password) — **muss lokal laufen** (Sandbox blockt mumlifebalance.ch) | Patricia lokal |
| 2 | WP-Seite prüfen & **publizieren** | Patricia |
| 3 | **Bio-Link** „Starterguide" → `https://mumlifebalance.ch/instagram-starterguide` umbiegen | Claude (braucht Bio-HTML) |
| 4 | Alte Netlify-Seite abschalten / weiterleiten | Patricia |

---

## Dateien

- `landing/index.html` — die Landingpage (standalone HTML, Preview-fähig)
- `../../../scripts/wordpress/deploy-starterguide.js` — Deploy-Script (Draft, Slug `instagram-starterguide`)

---

## 🔗 Verwandte Notizen

- [[_INDEX]]
- [[2026-04-23-bio-check-bot|Bio-Check-Funnel (Vorlage für AC-Form)]]
