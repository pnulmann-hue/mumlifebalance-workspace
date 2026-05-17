---
tags: [funnel]
---

# Werbeanzeige Bio-Check — Komplett-Briefing

**Stand:** 2026-04-25
**Profil:** Mum Life Balance — Mentoring (Profil 1, 1.956 Follower)
**Funnel:** Bio-Check (0€-Magnet)
**Landing:** mumlifebalance.ch/bio-check
**ManyChat-Keyword:** BIO

---

## 🎯 Strategie-Entscheidung (Julia-Trost-Methodik)

**EMPFEHLUNG: BOOST statt Cold Creative.**

Julias Regel: Bewirb einen Post, der **organisch schon gut performt**. Cold Creative von Null aufzubauen ist 5x teurer und liefert oft schlechteren CPL.

→ Dein heutiges Launch-Reel („Schluckauf → läuft") ist der ideale Kandidat:
- Story-Anschluss aus den gestrigen Stories = warme Audience
- Frische Energie = höhere Engagement-Rate
- Erste Lead schon organisch eingegangen = Signal funktioniert

**Aber:** 24-48h organisch beobachten zuerst. Wenn das Reel **mindestens 100 Likes + 5 Saves + 3 Shares** in 48h hat → boosten. Wenn nicht → erst organisch nachschärfen oder Cold-Creative-Variante (siehe Anhang).

---

## 🚀 Setup: Reel-Boost in Meta Ads Manager

### A. Anzeige-Quelle

**Methode:** „Bestehenden Beitrag bewerben" (nicht „Neue Anzeige erstellen")
- Meta Ads Manager → **Erstellen** → **Anzeigengruppen-Ebene**
- Beitragsauswahl: dein heutiges Bio-Check-Reel auf @mumlifebalance

### B. Kampagnen-Setup

| Feld | Wert |
|---|---|
| **Kampagnen-Ziel** | Leads (oder Engagement, falls Pixel-Tracking auf Landing fehlt) |
| **Kaufart** | Auktion |
| **Spending-Limit (Kampagne)** | Optional 200 CHF Cap für 14-Tage-Test |
| **Buying Type** | Auction |

### C. Anzeigengruppe (Audience + Platzierungen)

| Feld | Wert |
|---|---|
| **Optimierungsziel** | Lead (oder Landing Page Views als Fallback) |
| **Budget** | **7 CHF/Tag** (= 100 CHF in 14 Tagen) |
| **Zeitraum** | 14 Tage Test |
| **Platzierungen** | Manuell: Reels + Stories + Feed (NICHT Audience Network, NICHT Right Column) |

### D. Zielgruppe (Audience-Strategie — 3 Varianten testen)

**Audience 1 — Lookalike deiner besten Kontakte (KALT, scharf):**
- Quelle: AC-Export deiner Top-50-Engagers (DM-Schreiberinnen, Kursteilnehmerinnen)
- → Manuell aus AC exportieren als CSV → in Meta als Custom Audience hochladen → 1% Lookalike erstellen
- Land: Schweiz + Deutschland + Österreich
- Alter: 28-50
- Geschlecht: weiblich
- **Erwarteter CPL:** 2-4 CHF

**Audience 2 — Interesse-Targeting (KALT, breiter):**
- Schweiz + Deutschland + Österreich
- Alter: 28-50, weiblich
- Interessen (alle gleichzeitig):
  - Network-Marketing-Begriffe: „doTERRA", „Young Living", „Ringana", „Juice Plus", „Forever Living"
  - + ergänzend (mit ODER): „Mompreneur", „Working Mom", „Network Marketing"
- **Erwarteter CPL:** 3-6 CHF

**Audience 3 — Retargeting (WARM, höchste Conversion):**
- Custom Audience: Profil-Besucher der letzten 90 Tage (über Instagram-Insights aktivierbar)
- + Custom Audience: Reel-Viewer 50%+ der letzten 90 Tage
- **Erwarteter CPL:** 1-3 CHF (sehr scharf)

→ **Zum Start:** Audience 1 + 3 parallel mit je 5 CHF/Tag · Audience 2 erst wenn 1+3 stabil laufen

### E. Anzeige (CTA + Link)

| Feld | Wert |
|---|---|
| **Call-to-Action** | „Mehr dazu" / „Registrieren" |
| **Website-URL** | `https://mumlifebalance.ch/bio-check?utm_source=meta&utm_medium=paid&utm_campaign=biocheck-launch&utm_content=reel-schluckauf` |
| **Anzeigentext** | (im Reel sind Hook + CTA schon enthalten — keine zusätzliche Headline nötig) |

---

## 💰 Budget + KPIs

### Lern-Budget (14 Tage)

| Phase | Tagesbudget | Gesamt |
|---|---|---|
| Tag 1-3 (Lernen) | 5 CHF | 15 CHF |
| Tag 4-7 (Auswerten) | 7 CHF | 28 CHF |
| Tag 8-14 (Skalieren oder pausieren) | 10 CHF | 70 CHF |
| **Total Test** | — | **~110 CHF** |

### Erfolgs-Schwellen

| Metrik | Ziel | Skalieren | Pausieren |
|---|---|---|---|
| **CPL (Cost per Lead)** | < 3 CHF | < 2 CHF → Budget +50% | > 5 CHF → Audience pausieren |
| **CTR (Click-Through-Rate)** | > 1.5% | > 3% sehr stark | < 0.8% Hook prüfen |
| **CPM** | < 15 CHF | — | > 25 CHF Audience zu klein/teuer |
| **Conversion-Rate Landing → Anmeldung** | > 25% | > 40% sehr stark | < 15% Landing-Page-Mismatch |

### Umsatz-Logik (40k-Ziel-Beitrag)

- 100 Leads/Monat à 3 CHF CPL = 300 CHF Ad-Budget
- 25% durchlaufen Bot komplett = 25 PDF-Empfänger
- 5-10% kaufen Mid-Ticket-Pitch (39-97 CHF) = 1-3 Verkäufe = 100-300 CHF Umsatz
- **ROAS-Test-Phase:** ROI ist meist negativ am Anfang. Nurture-Mails 4-6 (siehe `phase-2-ac-setup.md`) holen die Conversion in Woche 2-4 nach.

---

## 📡 Tracking-Setup

### 1. UTM-Parameter (für jede Variante eindeutig)

```
?utm_source=meta&utm_medium=paid&utm_campaign=biocheck-launch&utm_content=reel-schluckauf
```

Bei Cold-Creative-Variante:
```
?utm_source=meta&utm_medium=paid&utm_campaign=biocheck-launch&utm_content=cold-img
```

### 2. Meta Pixel auf Landing prüfen

- Browser → mumlifebalance.ch/bio-check öffnen
- Chrome Extension **Facebook Pixel Helper** installieren
- Auf Seite klicken: muss ein grünes Häkchen + PageView-Event zeigen
- Falls Pixel fehlt: bei `/wp` einbauen lassen oder über WP-Plugin (PixelYourSite, etc.)

### 3. Conversion-Events

- **Lead-Event** = Form-Submit auf der Landing (AC-Form)
- Falls Pixel das nicht automatisch erkennt → Custom Conversion in Meta einrichten:
  - Trigger: URL enthält `bio-check-danke` (oder deine Thank-You-URL)

### 4. ManyChat-Keyword-Tracking

- AC-Tag 64 (`Bio-Check → Insta-DM`) zeigt wer aus DM zur Bot-Conversion kam
- Vergleich: AC-Lead-Tag 66 mit UTM `meta` vs. organisch

---

## ✅ Pre-Flight-Checkliste (vor Anzeige live)

- [ ] Reel hat ≥ 100 Likes / 5 Saves / 3 Shares organisch (48h-Check)
- [ ] Health-Endpoint grün: bio-check-bot.vercel.app/api/health
- [ ] End-to-End-Test der ganzen Funnel-Strecke heute durchgespielt
- [ ] AC-Automation #58 + neue PDF-Automation aktiv
- [ ] Meta Pixel feuert auf Landing (Facebook Pixel Helper)
- [ ] UTM-Parameter in Anzeigen-Link eingetragen
- [ ] Custom Audience 1 (Lookalike) erstellt
- [ ] Custom Audience 3 (Retargeting) erstellt
- [ ] Tagesbudget startet bei 5-7 CHF (nicht direkt 20+)
- [ ] Datenschutz-Erklärung erwähnt Vercel + Anthropic + AC + Meta
- [ ] Telegram-Alarm-Channel funktioniert (Bot-Down würde dich erreichen?)

---

## 🔄 Skalierungs-Regeln (nach 14 Tagen)

### Skalieren (Budget +50%) wenn:
- CPL < 2 CHF konstant über 5 Tage
- ROAS > 2.5
- Engagement organisch wächst parallel

### Audience tauschen wenn:
- CPL > 5 CHF nach 7 Tagen → andere Audience testen
- CTR < 0.8% → Hook-Problem (anderes Reel boosten)

### Komplett pausieren wenn:
- 14 Tage CPL > 7 CHF → grundsätzlich Targeting/Hook prüfen
- Lead-Qualität schlecht (kaum Bot-Abschlüsse) → Bot-Friction prüfen

---

## 🆘 Backup: Cold-Creative-Variante (falls Reel-Boost nicht zieht)

### Variante A — Statisches Karussell

**Hook (Slide 1):**
> Dein Schaufenster ist leer.
> Kein Wunder, dass keiner reinkommt.

**Slide 2-4:** Bio-Beispiele (was funktioniert nicht / was funktioniert)
**Slide 5:** Bio-Check als Lösung
**Slide 6:** CTA — Klick zum Bot

### Variante B — Single Image Ad

**Visual:** Patricia-Foto + Quote-Overlay
**Quote-Overlay:**
> „Ich hab in 48h einen KI-Bot gebaut, der deine Instagram-Bio checkt."

**Body-Copy unten:**
```
Schreib „BIO" in den Kommentar oder klick hier.
Du tippst deine Bio rein. 3 Minuten später hast du Experten-Satz, 5 Bio-Vorschläge, Pinned Posts, alles als PDF.

Heute gratis. Für Network-Mamas, die müde sind, sich hinter Fläschchen zu verstecken.
```

**CTA-Button:** „Mehr dazu"
**Visual-Brief:** Foto aus `context/Shootingbilder/` mit Patricia + Laptop, Creme-Hintergrund, Quote in Petrol/Orange

---

## 📝 Was Patricia konkret tun muss

1. **Heute:** Reel posten ✅ (erledigt)
2. **In 48h:** Reel-Performance prüfen (Likes/Saves/Shares-Schwelle)
3. **Wenn Schwelle erreicht:** Meta Ads Manager öffnen + Setup wie oben
4. **Tag 1-3 nach Schaltung:** täglich CPL prüfen (Meta Ads Dashboard)
5. **Tag 7:** Erste Skalierungsentscheidung (Budget halten / hoch / pausieren)
6. **Tag 14:** Vollanalyse + nächste Schritte planen

---

_Dokument basiert auf Julia-Trost-Werbeanzeigen-Methodik (Reichweiten-Booster-Kurs + Leadgewinnung leicht gemacht) + Patricia's Brand-Voice + Bio-Check-Funnel-Architektur._
