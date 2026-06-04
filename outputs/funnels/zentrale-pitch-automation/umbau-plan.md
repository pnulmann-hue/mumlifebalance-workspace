---
tags: [funnel, mba, pitch-automation, intern]
---

# Umbau-Plan — vom Ist-Zustand zur MBA-Maschine

> INTERN. Basiert auf [[ac-ist-zustand]] (Live-Check 2026-06-02). Leitidee: **auf dem aufbauen, was schon da ist** — erweitern, anketten, MBA oben draufsetzen, aufräumen. Nicht neu bauen.

## Grundprinzip

Dein System ist faktisch schon Variante B (aufsteigend, über Tags verkettet). Es fehlt nur die Spitze. Statt alles in EINE Automation umzuschreiben, bauen wir **eine neue „MBA-Pitch"-Automation als Konvergenzpunkt** — dort laufen alle Nicht-Käuferinnen zusammen, nachdem sie die Mid-Stufe gesehen haben. Das ist deine „eine zentrale Pitch-Automation", nur eben oben statt überall.

```
Freebie → (Auslieferung) → #53 Finde dein Thema (39)
   → [Diagnose] EIN passender Mid-Kurs:
        Instagram-Themen   → #54 IG-Kundenmaschine (333)
        Produkt/Brand      → #56 digitale Produktwelt (333)
        Zeit/Familie       → (neu) Mama-CEO-Pitch (333)
   → NEU: MBA-Pitch-Automation (Webinar-Brücke → MBA 997)
        → kein Kauf → grosser Verteiler (Launch-Pitches)
```

---

## Phase 1 — Die fehlende Spitze bauen (höchster Hebel)

**1.1 Neue Automation „MBA-Pitch"**
- **Trigger:** Tag `mba-pitch-start` hinzugefügt
- **Inhalt:** die 4 Mails aus [[variante-B-mailsequenz]] Phase 2 (Webinar-Brücke → MBA-Wert → für-wen → Deadline). Webinar-Link = Platzhalter `[WEBINAR-LINK]`.
- **Ziel/Exit:** neues Ziel „Kurs gekauft MBA" (Tag `mba-kauf`) → Automation endet. Wer kauft, wird sofort rausgenommen.

**1.2 Neue Tags + Ziel anlegen**
- Tag `mba-pitch-start` (Eintritt in die Spitze)
- Tag `mba-kauf` (von der MBA-Verkaufsseite/ThriveCart bei Kauf gesetzt) → als Ziel in MBA-Pitch hinterlegen

**1.3 Die zwei LIVE-Ketten in die Spitze münden lassen**
Aktuell enden #54 (IG-Kundenmaschine) und #55 (Expertin) mit „Kurs gekauft"-Ziel → Ende. Am natürlichen Ende (= Nicht-Käuferinnen) je einen Block ergänzen:
- **am Ende von #54:** Tag `mba-pitch-start` hinzufügen
- **am Ende von #55:** Tag `mba-pitch-start` hinzufügen

→ Damit fliessen alle, die die Mid-Stufe durchlaufen aber nicht gekauft haben, automatisch in den MBA-Pitch. (Tag doppelt = unkritisch, Trigger feuert einmal.)

**Ergebnis Phase 1:** Quiz #52 und Von-0-auf-echt #40 führen jetzt durchgängig bis zum MBA. Die grösste Lücke ist zu.

---

## Phase 2 — Diagnose-Routing + verwaiste Stufen einketten

Aktuell bekommt jede Freebie-Lead linear #53 → #54. Besser (weil deine 3 Kurse verschiedene Probleme lösen): nach #53 auf den EINEN passenden Mid-Kurs routen.

**2.1 Routing-Logik (über Einstiegs-Freebie/Tag) am Ende von #53:**
- Tag aus Instagram-Freebies (BIO/LEAD/STORY) → `Automation IG Kundenmaschine` (#54)
- Tag aus Produkt/Brand-Freebies (QUIZ/ECHT1) → `Automation zur digitalen Produktwelt` (#56)
- Tag aus Zeit/Familie-Thema → Mama-CEO-Pitch (siehe Phase 4)

**2.2 Verwaiste Pitch-Funnels aktivieren oder stilllegen:**
- #56 (digitale Produktwelt) — einketten (Trigger-Tag + am Ende `mba-pitch-start`)
- #57 (eigenes Angebot) — entscheiden: in #56 integrieren ODER als eigener Track
- #55 (Expertin, 97) — entscheiden: als Zwischenschritt im IG-Track ODER stilllegen (passt preislich unter 333)

**Offene Entscheidung für Patricia:** Sollen alle drei Mid-Kurse (IG / Produktwelt / Mama-CEO) als getrennte Diagnose-Tracks laufen, oder bleibt es vorerst bei der linearen Kette + nur MBA oben drauf (= weniger Aufwand, schneller live)?

---

## Phase 3 — Aufräumen (verhindert Doppel-Mails + Chaos)

- **#46 (Alt-Mischfunnel)** gegen #53/#54 prüfen: setzt noch jemand den Tag `Thema finden`? Wenn ja → Doppel-Pitch-Risiko. Empfehlung: #46 stilllegen, sobald #53/#54 alles abdecken.
- **#49 (Alle Minikurse)** — Stub ohne Trigger: löschen oder fertig bauen.
- **#42 (Magnet-ich)** — nie genutzt: prüfen, ob noch gebraucht.
- **Post-Kauf-Cross-Sell:** #44/#48/#51 enden nach dem Willkommen. Optional je einen sanften Hinweis auf die nächste Stufe ergänzen (Käuferinnen sind die besten nächsten Käuferinnen).

---

## Phase 4 — Mama-CEO + Webinar (nach dem Launch)

- **Mama-CEO Pre-Sale fehlt komplett** (nur Post-Kauf #62). Für den Zeit/Familie-Track brauchen wir eine Mama-CEO-Pitch-Sequenz — analog zu #54, mit den passenden Mails.
- **Webinar:** Live im MBA-Launch aufnehmen → als Evergreen in den MBA-Pitch (`[WEBINAR-LINK]` → Replay). Siehe [[blueprint]] „Live → Evergreen".
- **Webinar-Funnels #60/#63 sind tot** — beim Launch eine frische, saubere Anmelde-Automation bauen.

---

## Noch offen (braucht Chrome wieder offen)

- [ ] Bio-Check #58/#59 auslesen (Auslieferung + ob sie ketten)
- [ ] Mama-Zeit #15 + Willkommens-Sequenz #1 auslesen (Alt-Bestand?)
- [ ] Pitch-Mails #53/#54 inhaltlich lesen → was behalten / polieren (Blacklist-Phrasen wie „Kennst du das?" fixen)
- [ ] Prüfen, welche Tags die Bio-Check-Leads setzen → ans Routing anschliessen

---

## 🔗 Verwandte Notizen

- [[ac-ist-zustand]]
- [[blueprint]]
- [[variante-B-mailsequenz]]
- [[variante-C-mailsequenz]]
