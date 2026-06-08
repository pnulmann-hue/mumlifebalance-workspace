---
tags: [handoff, intern]
---

# Session-Handoff — 2026-06-07

> Für die Fortsetzung in einem neuen Chat. Lies das + `MEMORY.md` + `CLAUDE.md`, dann hast du den Stand.

## TL;DR
Riesen-Session: Buchhaltung Jan–Mai aufgearbeitet, Kosten optimiert + gedeckelt, MBA-Webinar-Launch-Trichter gestartet, Story-Bot komplett auf Notion umgebaut, `/monatsplan` zu Content-Vorplanung erweitert, Juni-Content-Plan + datenbelegte Marktanalyse erstellt, Apify-Watchlist erweitert.

---

## 1. Buchhaltung / Finanzen (Jan–Mai 2026)
- **Beleg-Index:** `context/finanzen/2026/belege-index-2026.md` (gitignored) — alle Business-Belege Jan–Mai (Gmail + PayPal-Funde), tax-ready.
- **Kennzahlen-DB (Notion) korrigiert:** doTERRA-Verdienst (Primär+Sekundär) Jan **1'072.78** · Feb **552.51** · März **583.05** · April **581.86**. Neue Spalte **„Umsatz Mama-CEO"**, Mai = **1'321**. April-Mentoring = 0 (geprüft).
- **Kosten Werbung (Meta-Ads) eingetragen:** Jan 93.43 · Feb 107.03 · März 69.76 · April 23.78 · Mai 12.75 = **306.75 CHF**.
- **doTERRA-Produkt-Orders ~1'231 €** = separates doTERRA-Buch, NICHT Online-Business-Kosten.
- **OFFEN:** doTERRA-Verdienst Mai (wartet Abrechnung) · Tools+Fortbildung final in CHF (Karten-CHF von Patricia) · **ActiveCampaign-Kosten** (weder Mail noch PayPal → direkte Kartenbelastung / evtl. Postfach info@mumlifebalance.ch) · **M-Budget Internet** + **Handyabo TalkTalk** (nicht im gmail → Portal/info@-Postfach).
- **❓ einzuordnen (Patricia prüft):** wondershare, UseAI, Verifone/avangate, Unikati, Hearttell.

## 2. Kosten-Optimierung
- **Erledigt (Code):** Cockpit-Bot → Haiku + 1×/Tag · Anthropic **API-Limit auf $150/Monat** gedeckelt.
- **Patricia macht:** Later kündigen (Auto-Renew) · Supabase Pro→**Free** (Funktion behalten) · Vimeo bei Renewal (April 2027) prüfen (ThriveCart Academy / YouTube unlisted).
- **Content-Assistent + Bio-Check bleiben Sonnet** (Qualität).
- **Meta-Token abgelaufen (16.5.)** → **System-User-Token „Ablauf: Nie"** neu generieren (Patricia) → dann IG-Insights + Ads automatisch.

## 3. MBA-Webinar-Launch (Juni/Juli)
- **Webinar Mi 24.6. 9:00** · Cart-Open 24.6 (**Pioneer 997 / Final 1347**) · Cart-Close **So 5.7.** · Programmstart Juli.
- **Anmeldeseite LIVE + getestet:** `mumlifebalance.ch/mba-webinar` (WP 3795, AC-Formular 59).
- **Launch-Build (Tasks offen):**
  - **#2 Show-up-Mail-Sequenz** (Notion-Aufgabe **Prio 1** — der Launch-Hebel; Mai-Webinar floppte, weil sie fehlte). Patricia macht; Vorlage: `outputs/produkte/mama-ceo/08-funnel/webinar-mails/`. Strecke für Formular 59: Bestätigung + 24h/1h/live + No-Show + ManyChat-DM.
  - **#3 Webinar-Pitch auf MBA anpassen** (Vorlage `outputs/produkte/mama-ceo/06-webinar-pitch-slides.md`).
  - **#4 Meta-Ad** (warm targeten + CHF 10/Tag, Creative erst organisch testen — **NICHT Mai-Ad recyceln**, floppte: 3 Anmeldungen, niemand live). Erst nach frischem Token + Link-Test + Budget-OK.
  - **#7 Launch-Kalender + story-plan.json:** längere Webinar-Werbungsphase (12.–24.6.) feinziehen.
- **Strategie:** erst Trichter dicht (Show-up!), dann warm + klein werben.

## 4. Story-Bot — umgebaut + LIVE (gepusht)
- `scripts/story-reminder/send-daily-reminder.js` liest jetzt **Notion: Monat + Woche** (Fokus/Sales-Pattern/Wochen-CTA) + matcht Produkt → `active-funnels.json` (Painpoint/Transformation/Pillar). Workflow gibt `NOTION_API_KEY` mit.
- **Funktioniert ab KW24** (KW23 hatte keinen Plan → war generisch).
- **Notion-Wochenpläne KW24–27 angelegt** (Fokus + Produkt + Wochen-CTA gesetzt). DB hat neue Spalte „Wochen-CTA".

## 5. active-funnels.json — aktualisiert
- Mama-CEO → `pilot-laeuft-und-solo-verkauf` · **MBA neu** (Endprodukt 997/1347, Warteliste). Architektur: 3 Produkttreppen → alle führen zur MBA.

## 6. /monatsplan — erweitert (Phase 4.5 Content-Vorplanung)
- Liefert jetzt: Marktanalyse + Vormonats-Analyse + **5 Beiträge/Woche** (≥2 Reichweiten) + **Reel-Dreh-Liste** (Batch) + **Blog** + **Newsletter** + Story-Logik (Launch=Drehbuch, sonst Vorlagen). CLAUDE.md aktualisiert.

## 7. Juni-Content (erstellt)
- **`outputs/content-monat/2026-06.md`** — kompletter Plan, beide Profile Mo–Fr, KW24–27, Reel-Dreh-Liste, Blog, Newsletter-Plan.
- **`outputs/content-monat/2026-06-marktanalyse.md`** — datenbelegte Marktanalyse (Apify-Discovery + Web). Verdikt: Content trifft den wunden Punkt; 3 Schärfungen eingearbeitet.
- Neue Memory-Regel: **Hooks spezifisch aus Network-Mama-Realität** (nicht abstrakt).

## 8. Apify-Watchlist — v3, 16 Accounts
- Ergänzt: @powerfrauenfocus · @alleinerziehend.erfolgreich · @digitalmamashift.

---

## Nächste sinnvolle Schritte
1. **Webinar Show-up-Mail-Sequenz** bauen (Prio 1).
2. **Juni-Reels abdrehen** (Reel-Dreh-Liste, Blocks A–D) — 1-2 Tage.
3. **Webinar-Pitch auf MBA** anpassen.
4. **Frischen Meta-Token** → Webinar-Ad (warm, klein) + Link-Test.
5. **Kosten finalisieren** (Karten-CHF + AC + Internet/Handy).
6. **doTERRA-Verdienst Mai** eintragen, wenn Abrechnung da.

## Dauerregeln (immer)
echte Umlaute/ss · keine Stakkato · keine erfundenen Zahlen · Hooks spezifisch (Network-Mama-/Vormenopause-Welt) · ≥2 Reichweiten-Posts/Woche · doTERRA Reels-only + Compliance (kein Heilversprechen) · **kein „Julia Trost"-Name im Kunden-Output** · MBA = 997/1347 · 5 Mamas im Mama-CEO-Pilot · Patricia hat 4 Kinder · „Stell dir vor" gesperrt.
