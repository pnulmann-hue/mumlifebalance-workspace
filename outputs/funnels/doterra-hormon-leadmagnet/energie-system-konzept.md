---
tags: [funnel, doterra, tools]
---

# doTERRA Energie-System — Test + Kur-Begleiter als EIN durchgehender Weg

**Erstellt:** 2026-06-09
**Ziel (Patricia):** mehr Kunden · mehr Teampartner · mehr Sichtbarkeit — über einen coolen, Insta-bewerbbaren Leadmagneten + ein interaktives Tool für die Frauen, die „Zurück zu deiner Energie" kaufen.
**Kern-Entscheid:** Wir erfinden nichts neu. Es existiert bereits ein **fertiges 3-Typen-Quiz** (`landingpage/`) + PDF + 4-Mail-Drip + ManyChat-Logik. Wir machen daraus ein **System aus zwei verketteten Tools** — der Energie-Typ trägt vom Test bis in den Begleiter durch.

---

## 0. Der durchgehende Weg (das „System")

```
INSTA-REEL (Energie-Hook)  →  „Kommentier ENERGIE"
        ↓ ManyChat
TOOL 1: ENERGIE-TYP-TEST  (existiert, 5 Fragen → 3 Typen)
        ↓  Lead trägt Email ein  →  AC-Liste 18 (doTERRA)
   Ergebnis-Seite: „Du bist die [Typ]"  +  PDF + 4-Mail-Drip
        ↓  Soft-Pitch zur Energie-Kur (Mail 3)
KAUF: „Zurück zu deiner Energie" (30 Tage, 4 Säulen)
        ↓  Energie-Typ wird übergeben
TOOL 2: KUR-BEGLEITER  (NEU — personalisiert nach Typ)
        ↓  begleitet durch 30 Tage  →  Ergebnis + Testimonial
RETENTION: bleibt auf LRP · empfiehlt weiter · wird evtl. Teampartnerin
```

**Warum das auf alle drei Ziele zahlt:**
- **Mehr Kunden** → der Test ist die Insta-taugliche Front-Tür (Quiz teilt sich besser als ein PDF).
- **Mehr Sichtbarkeit** → „Welcher Energie-Typ bist du?" ist ein Share-/Save-Magnet für Reels.
- **Mehr Teampartner** → wer die Kur durchzieht und Ergebnisse spürt, ist die wärmste Quelle für die Sharer-Frage (knüpft an die Power-of-3-Nachrichten von heute an).

---

## 1. Was schon existiert (nur aktivieren/aufpolieren)

| Asset | Stand | To-do |
|---|---|---|
| Quiz (5 Fragen, 3 Typen, Email-Capture) | ✅ gebaut, `quiz.js` + `quiz.html` | AC-Endpoint einhängen, deployen |
| 3 Ergebnis-Seiten (Energie-Räuberin · Mineral-Mängelin · Darm-Detektivin) | ✅ gebaut | Energie-Framing schärfen |
| PDF „4 Erkenntnisse" | ✅ Konzept fertig | in Canva bauen |
| 4-Mail-Drip + ManyChat-Skript | ✅ getextet | in AC/ManyChat einrichten |
| `sessionStorage`-Typ-Übergabe | ✅ im Code | → Brücke in Tool 2 |

→ **Tool 1 ist zu ~80 % fertig.** Es fehlt im Wesentlichen das Deployment + die AC-Verkabelung.

## 2. Strategische Korrektur: „Hormon" → „Energie"

Das Quiz heisst aktuell intern „Hormon-Typ". Empfehlung, alles auf **ENERGIE** zu vereinheitlichen:
- **Keyword ENERGIE** statt HORMON → deckt sich mit `active-funnels.json` (Energie-Kur, AC-Liste 18).
- **Compliance-sicherer:** „Energie" ist Lifestyle, „Hormonchaos" rutscht Richtung Medizin. Weniger Risiko bei doTERRA-Regeln.
- **Wärmer & breiter:** mehr Frauen fühlen sich von „müde/keine Energie" angesprochen als von „Hormonchaos".
- Öffentlicher Name: **„Welcher Energie-Typ bist du?"** / **„Der Energie-Typ-Test"**.

(Die 3 Typen-Namen bleiben — sie sind gut.)

---

## 3. TOOL 2 — Der Kur-Begleiter (das NEUE Stück)

**Was es ist:** Ein interaktives Web-Tool, das die Frau nach dem Kauf **30 Tage durch ihre Energie-Kur führt** — personalisiert nach ihrem Energie-Typ aus dem Test. Kein PDF, kein „viel Glück", sondern eine geführte Reise.

**Warum es der eigentliche Hebel ist:** Die meisten Kuren scheitern an der Umsetzung, nicht am Produkt. Ein Begleiter, der Tag für Tag anstupst, sorgt dafür, dass die Frau **wirklich durchzieht** → sie spürt Ergebnisse → gibt Testimonials → bleibt auf LRP → wird zur Empfehlerin. Genau die LRP-Substanz, die dir laut heutiger Analyse fehlt.

### Aufbau (4 Säulen × 30 Tage, gegründet auf deine bestehende Kur)

| Säule | Inhalt (aus deinen 4 Erkenntnissen) | Produkt-Begleitung |
|---|---|---|
| 1 · Eiweiss & Sättigung | tägl. Mini-Ziel, Frühstücks-Ideen | — |
| 2 · Reserven auffüllen | Routine-Anker, Einnahme-Erinnerung | VMG+ (Whole-Food-Komplex) |
| 3 · Darm & Verdauung | Mikrobiom-Impulse | PB Assist · Terrazyme |
| 4 · Stress & Regeneration | Mini-Rituale, Schlaf-Anker | (Lifestyle, kein Heilversprechen) |

### Personalisierung nach Typ
- **Energie-Räuberin** → Start mit Säule 4 (Stress/Schlaf), weil da ihr lautester Schmerz ist.
- **Mineral-Mängelin** → Start mit Säule 2 (Reserven/Nährstoffe).
- **Darm-Detektivin** → Start mit Säule 3 (Mikrobiom).
→ Jede beginnt da, wo es bei ihr am meisten brennt, statt „Schema F".

### Funktionen MVP (bewusst klein)
- Typ kommt per URL/`sessionStorage` aus Tool 1 (oder einmalige Mini-Abfrage).
- 30 Tages-Karten: 1 Mini-Impuls/Tag (Gewohnheit + ggf. Produkt-Anwendung), abhakbar.
- Fortschritts-Balken (Motivation).
- Tag 7 / 14 / 30: kurze Selbst-Reflexion („wie ist deine Energie auf 1–10?") → liefert dir das Testimonial-Material.
- Kein Login nötig im MVP (Fortschritt im `localStorage`) — schnellster Weg live.

---

## 4. Technik — ja, mit Claude Code baubar

**Präzedenzfall:** Dein **Bio-Check-Bot** läuft als interaktive Web-App (Vercel) — derselbe Stack trägt beide Tools hier.

- **Tool 1 (Test):** statische Site (HTML/CSS/Vanilla-JS), existiert. Deployment Netlify ODER Vercel. AC-Anbindung über eine kleine Serverless-Function (der Code-Haken `AC_API_ENDPOINT` ist schon vorgesehen).
- **Tool 2 (Begleiter):** neue statische Web-App, gleicher Brand-Stack (Petrol/Creme, Philosopher + Source Sans 3). Fortschritt im `localStorage`, Typ-Übergabe via URL-Parameter. MVP braucht **kein** Backend/Login.

**Ehrliche Aufwands-Realität:**
- Tool 1 live bringen: ~Deployment + AC-Function + PDF in Canva = überschaubar, das Meiste ist da.
- Tool 2 MVP: ein echtes Bau-Projekt (Inhalte für 30 Tage × 3 Typen-Einstiege + die App). Mehrere Sessions.
- ⚠️ **Sandbox-Limit beachten:** `.env`/Deployment persistiert nicht zwischen Web-Claude-Sessions; Hosting läuft über Netlify/Vercel + ggf. GitHub Action (wie bei deinen anderen Bots).

---

## 5. Compliance-Leitplanken (Pflicht)

- **Lifestyle, nie Medizin:** Test fragt nach Alltag/Energie/Gewohnheiten — **nicht** „welche Krankheit". Die bestehenden Ergebnis-Texte sind teils symptom-lastig (Haarausfall, Schlaf) → in der Energie-Version Richtung „Energie/Alltag" entschärfen.
- **Keine Heilversprechen:** Produkte als Teil eines Lifestyle, „bei mir war"-Frame. Kein „X heilt/hilft gegen Y".
- **Keine erfundenen Zahlen.**

---

## 6. Empfohlene Reihenfolge

1. **Tool 1 live bringen** (Energie-Typ-Test + ENERGIE-Keyword + AC-Liste 18 + PDF) → bringt sofort Leads + Sichtbarkeit. Schnellster Win.
2. **Insta-Bewerbung:** 1–2 Reels „Welcher Energie-Typ bist du? → Kommentier ENERGIE" (doTERRA = Reels-only laut Content-Radar).
3. **Tool 2 (Begleiter) MVP** für die Käuferinnen → Retention + Testimonials + Teampartner-Pipeline.

---

## 7. Gewählte Bauform: PWA + Telegram (Entscheid 9.6.2026)

**Architektur:**
- **Test (Front-Tür)** — Web-Quiz, Insta → Lead → AC-Liste 18. (Phase 0, grösstenteils gebaut)
- **Begleiter-App (PWA)** — installierbare Web-App „Energie-Begleiter": Homescreen-Icon, Vollbild. Kennt den Energie-Typ, zeigt 30 Tageskarten (4 Säulen), Fortschritts-Balken, Check-ins an Tag 7/14/30. Fortschritt im `localStorage` (MVP, kein Login).
- **Telegram-Reminder** — Bot (Railway) schickt täglich den Impuls + Deep-Link in die App. Im MVP **lose gekoppelt**: Telegram stupst zeitbasiert an (Tag 1–30 ab Start), die PWA trackt den echten Fortschritt. Kein State-Sync nötig fürs MVP.

**Phasenplan:**
1. **Phase 0 — Test live** (schneller Lead-Win, ~80 % gebaut)
2. **Phase 1 — PWA-MVP** (App-Hülle + 30 Tageskarten × 3 Typ-Einstiege + Fortschritt + installierbar via manifest/service-worker)
3. **Phase 2 — Telegram-Reminder-Bot** (30-Tage-Drip, Deep-Links in die App)
4. **Phase 3 — Politur** (Reflexions-Check-ins → Testimonial-Capture, Typ-Übergabe Test→PWA per URL)

**⚠️ Der eigentliche Engpass = Inhalt, nicht Code.** 30 Tage × Mini-Impuls (Gewohnheit + ggf. Produkt-Anwendung), pro Säule, in Patricias Stimme, compliance-sauber. Die App-Hülle ist scaffold-bar; die 30-Tage-Inhalte entstehen gemeinsam (Patricias Input + Voice + doTERRA-Compliance).

---

## 🔗 Verwandte Notizen

- [[leadmagnet-komplett|Bestehendes Leadmagnet-Konzept (Quiz + Drip + ManyChat)]]
- [[../../../context/active-funnels|active-funnels.json — Energie-Kur Funnel]]
- Bio-Check-Bot als technischer Präzedenzfall (`outputs/bio-check-bot/`)
