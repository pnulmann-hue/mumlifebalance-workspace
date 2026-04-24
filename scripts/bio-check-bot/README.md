# Bio-Check für Network-Mamas — Deploy auf Vercel

Interaktiver Leadmagnet-Bot. User tragen sich auf der WordPress-Landingpage ins ActiveCampaign-Formular ein, bekommen per Mail den Bot-Link, durchlaufen 5-10 Min Dialog und erhalten das PDF via zweiter Mail.

---

## Ordnerstruktur (Vercel-Layout)

```
scripts/bio-check-bot/
├── public/                       # Statisches Frontend
│   ├── index.html
│   ├── styles.css
│   └── chat.js
│
├── api/                          # Vercel Serverless Functions
│   ├── chat.js                   # Claude-API Proxy
│   ├── tag.js                    # AC-Tag bei Pitch-Klick
│   └── pdf.js                    # PDF + AC-Mail-Trigger (Vercel Blob upload)
│
├── lib/
│   └── system-prompt.md          # Bot-Persona, Flow, Pitches
│
├── vercel.json                   # Vercel-Config (Headers, Function-Limits)
├── package.json
├── .env.example
└── README.md
```

---

## Deploy in 5 Schritten

### 1 — Anthropic-Key erstellen

https://console.anthropic.com → **API Keys** → **Create Key** → Name z.B. `bio-check-bot` → kopieren (zeigt Key nur EIN MAL).

**Wichtig:** Diesen Key **nicht** in den Chat posten, direkt im nächsten Schritt in Vercel-ENV eintragen.

### 2 — Lokal vorbereiten

```bash
cd "C:/Users/pnulm/Desktop/Mein Business/scripts/bio-check-bot"
npm install
```

### 3 — Vercel-Projekt anlegen + erster Deploy

```bash
# Vercel CLI falls noch nicht global installiert:
npm install -g vercel

# Einloggen (öffnet Browser):
vercel login

# Projekt im aktuellen Ordner anlegen:
vercel link
# → Set up and link? Yes
# → Which scope? dein Account
# → Link to existing project? No
# → Project name? bio-check-bot
# → Directory? ./ (Enter)
# → Override settings? No

# Blob Store anlegen (für PDF-Hosting):
vercel blob create bio-check-pdfs
# → Notiert den BLOB_READ_WRITE_TOKEN — wird automatisch ins Projekt gesetzt

# Erster Deploy als Preview:
vercel

# Wenn alles gut aussieht → Production:
vercel --prod
```

Vercel gibt dir URLs wie `https://bio-check-bot-abc123.vercel.app`.

### 4 — Environment-Variables in Vercel setzen

Zwei Wege — beide funktionieren:

**Weg A — Im Browser (empfohlen):**
1. https://vercel.com/dashboard → Projekt `bio-check-bot`
2. **Settings** → **Environment Variables**
3. Für jede Variable: Name eingeben, Wert, "Production + Preview + Development" anhaken, **Save**:

| Name | Wert |
|---|---|
| `ANTHROPIC_API_KEY` | [dein Key aus Schritt 1] |
| `AC_API_URL` | `https://mumlifebalance.api-us1.com` |
| `AC_API_KEY` | Aus AC → Settings → Developer |
| `AC_TAG_LEAD` | `59` |
| `AC_TAG_COMPLETED` | `60` |
| `AC_TAG_THEMA` | `61` |
| `AC_TAG_EXPERTIN` | `62` |
| `AC_TAG_KUNDENMASCHINE` | `63` |
| `AC_TAG_INSTA_DM` | `64` |
| `AC_FIELD_PDF_URL` | (leer lassen, kommt in Phase 2) |

`BLOB_READ_WRITE_TOKEN` wurde durch `vercel blob create` automatisch gesetzt — nichts zu tun.

**Weg B — Via CLI:**
```bash
vercel env add ANTHROPIC_API_KEY production
# → Wert einfügen, Enter

vercel env add AC_API_URL production
vercel env add AC_API_KEY production
# ... usw.
```

Nach ENV-Änderung: **nochmal deployen**, damit die neuen Werte in die Functions kommen:
```bash
vercel --prod
```

### 5 — Custom Domain `bio-check.mumlifebalance.ch`

1. Vercel → Projekt → **Settings** → **Domains**
2. `bio-check.mumlifebalance.ch` eintragen → **Add**
3. Vercel zeigt dir den DNS-Eintrag an:
   - **Typ:** CNAME
   - **Name:** `bio-check`
   - **Value:** `cname.vercel-dns.com`
4. Bei deinem DNS-Provider (wo `mumlifebalance.ch` registriert ist) den CNAME-Record anlegen
5. Zurück in Vercel → warten, bis grüner Haken ✓ (5-60 Min)
6. SSL wird automatisch ausgestellt

---

## Lokal entwickeln

```bash
vercel dev
# öffnet http://localhost:3000
```

Mit Token-Params für Persönlichkeit:
```
http://localhost:3000/?e=deine-test@example.com&n=Patricia
```

---

## Daten-Flow (End-to-End)

```
1. User → WordPress-Landingpage /bio-check
2. AC-Formular: Name + E-Mail
3. AC Tag "Bio-Check Lead" (59) → Automation "Bio-Check Auslieferung"
4. Mail 1: "Hier ist dein Link" → https://bio-check.mumlifebalance.ch/?e=%EMAIL%&n=%FIRSTNAME%
5. User klickt Link → Bot lädt
6. Chat via /api/chat (Claude)
7. Pitch-Klick → /api/tag → Tag 61/62/63 → triggert Funnel 53/54/55
8. Am Ende → /api/pdf
   - PDF wird generiert
   - Upload zu Vercel Blob (öffentliche URL)
   - AC Custom Field "bio_check_pdf_url" = URL
   - AC Tag "Bio-Check abgeschlossen" (60) → Mail 2 mit PDF-Link
```

---

## Kosten

| Service | Free-Tier | Ab wann kostet es? |
|---|---|---|
| **Vercel Hosting** | 100 GB/Monat | Ab ca. 10k User/Monat |
| **Vercel Functions** | 1M Invocations/Monat | Fast nie relevant |
| **Vercel Blob** | 1 GB Storage + 10 GB Bandwidth | 5000+ PDFs |
| **Anthropic Claude** | Pay-as-you-go | ~0.02-0.05 CHF pro User |

Bei 100 User/Monat: ~5 CHF. Bei 1000: ~50 CHF.

---

## Wartung

**System-Prompt ändern:**
1. `lib/system-prompt.md` editieren
2. `vercel --prod` → neuer Deploy

**Pitch-Texte anpassen:** Gleicher Prozess — alles im System-Prompt.

**Neue Preise:**
- `public/chat.js` → `PITCHES` Objekt
- `lib/system-prompt.md` → Pitch-Blöcke
- `public/index.html` → Done-Screen-Links
- `api/pdf.js` → `pitches` Array im PDF

---

## Troubleshooting

**Bot antwortet nicht:**
- Vercel → Projekt → **Logs** → `api/chat` prüfen
- Häufigste Ursache: `ANTHROPIC_API_KEY` nicht gesetzt oder falsch

**PDF kommt nicht per Mail:**
- Vercel → Logs → `api/pdf`
- Prüfen: Custom Field `bio_check_pdf_url` in AC erstellt? (kommt in Phase 2)
- Prüfen: AC-Automation „PDF-Versand" triggert bei Tag 60?

**Tag wird nicht gesetzt:**
- Vercel → Logs → `api/tag`
- Prüfen: `AC_API_KEY` hat Admin-Rechte?

---

## Nächste Schritte nach Deploy

- **Phase 2:** AC-Automation + Mail-Texte (schreibe ich dir als nächstes)
- **Phase 3:** WordPress-Elementor-Landingpage
