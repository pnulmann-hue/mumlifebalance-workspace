# Bio-Check für Network-Mamas — Implementierungsplan

**Datum:** 2026-04-23
**Status:** Entwurf — Patricia zur Freigabe
**Ziel:** Interaktiver Bot als Leadmagnet für Networkerinnen. Analysiert bestehende Bios oder erstellt neue aus 0, nach Julia-Trost × Patricia-Methodik. Pitched am Ende die passende Produkt-Treppe (39 → 97 → 333 CHF).

---

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│  1. WordPress-Landingpage (mumlifebalance.ch/bio-check)          │
│     + eingebettetes ActiveCampaign-Formular                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ Name + E-Mail
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. ActiveCampaign                                               │
│     → Tag "Bio-Check Lead" setzen                                │
│     → Kontakt zu Liste "Bio-Check Kontakte" hinzufügen          │
│     → Automation "Bio-Check Auslieferung" startet                │
│        → Mail 1: "Hier ist dein Bio-Check-Link"                  │
│           (Link enthält Token = E-Mail-Hash)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │ User klickt Bot-Link
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Bot auf Netlify (bio-check.mumlifebalance.ch)                │
│     Frontend: HTML/JS Chat-UI im Patricia-Brand                  │
│     Backend: Netlify Function → Claude API (Sonnet 4.6)          │
│     Dialog: 5-10 Min, zwei Pfade (Analyse / Aufbau)              │
│     Output: 5 Bio-Vorschläge + Experten-Satz + Highlights-Plan   │
│     PDF: generiert und per E-Mail versendet                      │
│     Pitches: inline im Chat + als Buttons zum Thrivecart         │
│                                                                  │
│     Pitch-Klick setzt Tag in AC:                                 │
│       "Bio-Check → Thema-Interesse"     (→ Funnel 53)            │
│       "Bio-Check → Expertin-Interesse"  (→ Funnel 55)            │
│       "Bio-Check → Kundenmaschine-Interesse" (→ Funnel 54)       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Bot-Entwicklung (Kern)

### 1.1 Repo-Struktur

```
scripts/bio-check-bot/
├── public/
│   ├── index.html          # Chat-UI
│   ├── styles.css          # Patricia Brand (Rosa/Cream)
│   └── chat.js             # Frontend-Logic
├── netlify/functions/
│   ├── chat.js             # Claude API Proxy
│   ├── tag-contact.js      # AC-Tag setzen bei Pitch-Klick
│   └── send-pdf.js         # PDF-Gen + Mail-Versand
├── lib/
│   ├── system-prompt.md    # Bot-Persona + Flow + Knowledge
│   ├── questions-a.js      # Analyse-Pfad Fragen
│   ├── questions-b.js      # Aufbau-Pfad Fragen
│   └── bio-templates.js    # 5 Varianten-Logik
├── netlify.toml
├── package.json
└── .env.example            # ANTHROPIC_API_KEY, AC_API_URL, AC_API_KEY
```

### 1.2 Dialog-Ton — DIDAKTISCH, nicht abfragend

**Grundprinzip:** Der Bot ist nicht Formular, sondern Mentorin. Jeder Schritt folgt dem Muster:

```
1. Mini-Lehre (2-3 Sätze): Warum ist dieser Schritt wichtig?
2. Alltagsbeispiel / Metapher: Damit es klickt
3. Frage: Jetzt bist du dran
```

**Leit-Metapher: Das violette Kleid & die Schuhe** (Patricias Kurs-Metapher — korrekt!)

> „Stell dir vor: Du gehst an eine Hochzeit. Du hast ein richtig geiles violettes Kleid. Nur die Schuhe fehlen. Du läufst durch die Stadt und weisst genau: Ich brauche einen passenden Schuh.
>
> Du wirst NIEMALS in einen Laden gehen, wo im Schaufenster lauter Krimskrams liegt und nicht direkt klar ist: Aha, hier gibt es Schuhe. Du gehst dort rein, wo sofort klar ist: Hier. Gibt. Es. Schuhe.
>
> So geht es deinen Kunden auf Instagram. Sie scrollen herum und fühlen sich gecatcht, wenn du ihr **konkretes Problem** ansprichst — das, was sie schon lange lösen wollen.
>
> Und by the way: Niemand wacht morgens auf und denkt 'Shit, ich muss unbedingt ätherische Öle haben.' 😅
>
> Aber eine Mama wacht auf und denkt: 'Ich hab schon wieder schlecht geschlafen.' Oder: 'Ich bin so erschöpft.' Oder: 'Ich will endlich ruhig mit meinen Kindern umgehen.' **DAS** ist dein Thema. Die Öle sind nur das Werkzeug."

Diese Metapher zieht sich als roter Faden durch den Bot:
- Bio-Analyse: „In deinem Schaufenster liegt Krimskrams / ist es leer / sind nur Produkte"
- Themenfindung: „Was verkaufst du wirklich? Schuhe — oder das Gefühl, elegant zur Hochzeit zu gehen?"
- Pinned Posts: „Das sind die 3 Produkte, die du ins Schaufenster stellst"
- Highlights: „Das sind die Regale hinter der Ladentheke"
- CTA: „Das ist die Türklinke"

**Weitere Alltags-Hooks** (Bot generiert passend — Patricia-Voice-konform):

| Schritt | Alltags-Hook |
|---|---|
| Warum Produkt ≠ Thema | „Niemand wacht morgens auf und denkt 'Ich brauche dringend Shakes.' Aber viele wachen auf und denken: 'Ich will endlich wieder in meine alten Jeans passen.' Shake = Werkzeug. Jeans-Gefühl = Thema." |
| Warum Experten-Satz nötig | „Wenn dich jemand auf dem Spielplatz fragt 'Was machst du beruflich?' und du sagst 'Ich verkaufe Öle' — was denkt die andere Mama? Wenn du sagst 'Ich helfe erschöpften Mamas, wieder zu Energie zu kommen' — was denkt sie jetzt?" |
| Warum Zielgruppe schärfen | „Ein Schuhladen für alle ist austauschbar. Ein Laden für bequeme Brautschuhe mit Pfennigabsatz-Gefühl — da fährt die Braut quer durch die Schweiz für." |
| Warum Pinned Posts wichtig | „Das sind die 3 Paar Schuhe, die du direkt ins Schaufenster stellst. Deine Bestseller. Die, die jeder sofort sehen soll." |
| Warum Highlights wichtig | „Das sind die Regale im Laden. Wer interessiert ist, geht rein und stöbert — über dich, dein 0€-Geschenk, deine Angebote, deine Kundinnen." |

**Start:**
- Bot begrüsst mit Name, erklärt was kommt (5-10 Min, am Ende PDF per Mail)
- Startet direkt mit Schaufenster-Metapher als Einstieg
- „Hast du schon ein Schaufenster, das wir aufpolieren — oder bauen wir dein Schaufenster von Grund auf?"

**Pfad A — Analyse (3-5 Min):**
1. Paste deine Bio rein (alle 4 Zeilen)
2. Wie viele Anfragen/DMs pro Woche?
3. Bot-Analyse: Experten-Satz? Zielgruppe? Produkt = Thema? CTA?
4. 🚦-Ergebnis pro Zeile + Haupt-Diagnose
5. Weiter zu Fragen-Set

**Pfad B — Aufbau (5-7 Min):**
Fragen aus Julia-Workbook + Patricia-Kurs:
1. In welchem Network bist du? (Dropdown: doTERRA, Ringana, Young Living, Juice Plus, Amway, Herbalife, andere)
2. Was verkaufst du konkret? (1 Satz)
3. **Kernfrage:** Welches konkrete Problem hast DU mit dem Produkt gelöst? (z.B. 10 kg abgenommen / Migräne weg / Energie zurück / erste 1000 CHF)
4. Seit wann nutzt du es selbst? (Expertise-Proof)
5. Was fragen dich andere immer wieder? (aus Patricia-Kurs Übung)
6. Wer warst du, bevor du das Produkt/Business kanntest?
7. Mit wem würdest du am liebsten arbeiten? (Anfänger-Workbook)
8. Welches der 5 Themenfelder trifft dich? (Themenlandkarte)
9. Duzen oder siezen?
10. Name + Emoji-Style?

**Nach Fragen:**
- Bot liefert 3 Varianten Experten-Satz
- Bot liefert 5 Bio-Vorschläge (je ≤150 Zeichen)
- Bot erklärt: „Produkt ≠ Thema" (aus Patricia-Kurs)
- Bot liefert Bonus: 3 Pinned-Posts-Ideen + Highlights-Struktur

### 1.3 Pitch-Logik (3 strategische Trigger)

| Trigger | Pitch | Tag |
|---|---|---|
| Wenn Bot „Produkt = Thema" diagnostiziert ODER User sagt „weiss nicht was mein Thema ist" | **Finde dein Thema (39 CHF)** → https://mumlifebalance.thrivecart.com/thema-finden/ | `Bio-Check → Thema-Interesse` |
| Nach Lieferung der 5 Bio-Vorschläge (HAUPT-Pitch) | **Expertin statt Verkäuferin (97 CHF)** — Patricia analysiert deine Bio persönlich → https://mumlifebalance.thrivecart.com/expertin/ | `Bio-Check → Expertin-Interesse` |
| Wenn User Tiefe/Begleitung signalisiert | **Instagram-Kundenmaschine (333 CHF)** mit Telegram-Gruppe → https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/ | `Bio-Check → Kundenmaschine-Interesse` |
| Safety-Net am Ende + bei Zögern | DM @patricianulmann.mentorin auf Instagram | `Bio-Check → Insta-DM` |

### 1.4 PDF-Output

- Cover: Patricia-Brand + „Dein Bio-Check"
- Seite 1: Dein Experten-Satz (3 Varianten)
- Seite 2: Deine 5 Bio-Vorschläge (copy-paste-ready)
- Seite 3: Highlights-Struktur + 3 Pinned-Posts-Ideen
- Seite 4: „So nutzt du das"-Anleitung
- Seite 5: Deine nächsten Schritte (mit Pitch-Buttons zu den 3 Funnels)

### 1.5 Knowledge-Quellen für System-Prompt

- `context/Kurse/aktuelle kurse/Finde dein Thema als Network-Mama in 60 Minuten/Transkripte/*` (kompletter Kurs)
- `reference/julia-trost/2. Instagram Profil (1).pdf` (Bio-Anatomie)
- `reference/julia-trost/1. Kopie von 1. Nische, Positionierung & Zielgruppe (1).pdf`
- Drive: „Anfänger-Version: Zielgruppe verstehen"
- Drive: „Profi-Version: Zielgruppe vertiefen"
- `context/brand-voice.md` + `context/hook-framework.md`

---

## Phase 2 — ActiveCampaign Setup

### 2.1 AC-Tags (erstellt 2026-04-23 via MCP)

- [x] Tag ID **59**: `Bio-Check Lead` — neuer Eintrag
- [x] Tag ID **60**: `Bio-Check abgeschlossen` — PDF wurde gesendet
- [x] Tag ID **61**: `Bio-Check → Thema-Interesse` → triggert Funnel 53
- [x] Tag ID **62**: `Bio-Check → Expertin-Interesse` → triggert Funnel 55
- [x] Tag ID **63**: `Bio-Check → Kundenmaschine-Interesse` → triggert Funnel 54
- [x] Tag ID **64**: `Bio-Check → Insta-DM`

### 2.2 Was Patricia manuell in AC-UI machen muss (ich liefere Anleitung + Mail-Texte)

- [ ] Formular „Bio-Check Anmeldung" erstellen (Name + E-Mail, DSGVO-Checkbox)
  → Action: Tag `Bio-Check Lead` setzen + Liste hinzufügen
- [ ] Automation „Bio-Check Auslieferung" bauen:
  - Trigger: Tag `Bio-Check Lead` hinzugefügt
  - Wartezeit: 1 Minute
  - Mail 1: „Hier ist dein Bio-Check-Link" (Text liefere ich)
  - Link-Format: `https://bio-check.mumlifebalance.ch/?t=[SUB:CONTACT_HASH]`
  - Wartezeit: 24h (falls PDF nicht gekommen, d.h. Tag `Bio-Check abgeschlossen` nicht gesetzt)
  - Mail 2: Reminder „Hast du schon deinen Bio-Check gemacht?"
- [ ] Verknüpfung der Pitch-Tags mit Funnels 53/54/55 prüfen + ggf. korrigieren

### 2.3 E-Mail-Texte für Welcome + Reminder

- Ich liefere beide Texte als Markdown-Blöcke im Brand-Voice.

---

## Phase 3 — WordPress-Landingpage

### 3.1 Was ich liefere

- [ ] Komplettes HTML/CSS für `/bio-check` Landingpage (responsive, 1-Spalte)
- [ ] Copy-Paste-Block für Elementor / Gutenberg / Divi (je nach WP-Builder)
- [ ] Struktur:
  - Hero: Hook („Deine Bio verkauft für dich oder gegen dich") + Formular
  - Bullet-Section: „Was du bekommst" (5 Bio-Varianten + Experten-Satz + Highlights-Plan + PDF)
  - Social Proof: 2-3 Testimonial-Slots (Patricia füllt)
  - So funktioniert's: 3 Schritte
  - Patricia-Section: kurze Vorstellung
  - FAQ: 4 Fragen
  - Final CTA: Formular nochmal
- [ ] AC-Formular-Embed-Code eingebaut

### 3.2 Was Patricia macht

- [ ] WP-Seite anlegen (`/bio-check`) und HTML einfügen
- [ ] 2-3 Testimonials eintragen
- [ ] SEO-Meta (Titel + Beschreibung liefere ich)
- [ ] Navigation ergänzen (optional)

---

## Reihenfolge & Abhängigkeiten

1. **Bot bauen + testen** (ohne AC-Anbindung, mit Dummy-Tag-Endpoint) — ca. 2-3 Std
2. **AC-Tags via MCP erstellen** (5 Min)
3. **AC-Formular + Automation** bauen (Patricia manuell, 30 Min, mit meiner Anleitung)
4. **Bot-Netlify-Deploy** + ENV-Vars (Patricia, mit Anleitung)
5. **End-to-End-Test** (Formular → Mail → Bot → PDF → Pitch-Tag → Funnel)
6. **WordPress-Landingpage** einfügen (Patricia mit meinem Code)
7. **Final-Test + Go-Live**

---

## Offene Fragen zur Plan-Freigabe

1. **Subdomain** für Bot: `bio-check.mumlifebalance.ch` — ok? (Patricia muss DNS-Record setzen)
2. **WP-Page-Slug**: `/bio-check` — ok?
3. **Welcher WP-Builder** ist aktiv (Elementor / Divi / Gutenberg / anderes)?
4. **PDF-Versand**: via Resend / SendGrid / SMTP? Oder via AC-Automation „PDF als Attachment"? (Resend ist am einfachsten)
5. **Anthropic-API-Key**: Hat Patricia schon einen (aus doTERRA-Bots wiederverwendbar) oder neuen erstellen?

---

## Abgeschätzter Aufwand

- Bot: ~3-4h Dev
- AC-Setup: ~30 Min (MCP + Anleitung)
- WP-Landingpage: ~1h Code + Patricia ~30 Min einfügen
- Testing: ~1h

**Gesamt**: ~6h bis Live — in 2-3 Sessions durchziehbar.
