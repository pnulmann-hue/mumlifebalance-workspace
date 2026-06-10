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

## ⚠️ Offene TODOs vor Live-Schaltung

| # | Aufgabe | Wer |
|---|---------|-----|
| 1 | **AC-Formular** für den Starterguide in ActiveCampaign anlegen (mit Automation: PDF senden) | Patricia |
| 2 | In `landing/index.html` die Platzhalter `STARTERGUIDE_AC_FORM_ID` + `STARTERGUIDE_AC_TOKEN` ersetzen | Patricia / Claude |
| 3 | Deploy: `cd scripts/wordpress && node --env-file=.env deploy-starterguide.js` (braucht `.env` mit WP-App-Password) | Patricia |
| 4 | WP-Seite prüfen & **publizieren** | Patricia |
| 5 | **Bio-Link** „Starterguide" → `https://mumlifebalance.ch/instagram-starterguide` umbiegen | Claude (braucht Bio-HTML oder WP-Zugang) |
| 6 | Alte Netlify-Seite abschalten / weiterleiten | Patricia |

---

## Dateien

- `landing/index.html` — die Landingpage (standalone HTML, Preview-fähig)
- `../../../scripts/wordpress/deploy-starterguide.js` — Deploy-Script (Draft, Slug `instagram-starterguide`)

---

## 🔗 Verwandte Notizen

- [[_INDEX]]
- [[2026-04-23-bio-check-bot|Bio-Check-Funnel (Vorlage für AC-Form)]]
