# Freischaufeln — 0€-KI-Tool (Deploy auf Vercel)

Interaktives Freebie: Network-Mamas kippen ihre Familien-Woche rein, das Tool schlägt die typischen Aufgaben vor, **halbiert** mit ihnen (weg / delegieren / zusammenlegen / behalten) und **schaufelt ein geschütztes Business-Fenster frei**. Bio-Check-Zwilling.

**Funnel:** WordPress-Anmeldeseite (AC-Formular, E-Mail) → Auslieferungs-Mail mit Tool-Link (`?e=%EMAIL%&n=%FIRSTNAME%`) → Tool → Ergebnis „Deine neue Woche" → weicher CTA (Juli: MBA, später Minikurs). Keyword: **`ZEIT`** (ManyChat).

---

## Ordnerstruktur

```
scripts/freischaufeln/
├── public/index.html      # komplette geführte Web-App (Frontend, self-contained)
├── api/generate.js        # Claude-Proxy für die 3 Schritte
├── api/tag.js             # AC-Tag (Abschluss + Interesse-Klicks)
├── lib/system-prompt.md   # KI-Gehirn (Voice, Regeln, JSON-Contract)
├── vercel.json · package.json · .env.example · README.md
```

---

## Deploy in 5 Schritten

### 1 — Anthropic-Key
Du kannst den Key aus einem bestehenden Bot wiederverwenden (z.B. Bio-Check) oder einen neuen erstellen: https://console.anthropic.com → API Keys. **Nicht** in den Chat posten — direkt in Vercel-ENV.

### 2 — AC-Tags anlegen
In ActiveCampaign 3 Tags erstellen und die IDs notieren:
- `Freischaufeln abgeschlossen`
- `Freischaufeln → MBA-Interesse`
- `Freischaufeln → Minikurs-Interesse`
(+ optional `Freischaufeln Lead` fürs Anmelde-Formular / die Auslieferungs-Automation.)

### 3 — Deploy
```bash
cd "C:/Users/pnulm/Desktop/Mein Business/scripts/freischaufeln"
npm install
npx vercel login       # falls nötig
npx vercel link        # Projektname: freischaufeln · Directory ./
npx vercel             # Preview-Deploy
npx vercel --prod      # Production → https://freischaufeln-xxxx.vercel.app
```

### 4 — Environment-Variables in Vercel (Settings → Environment Variables)
| Name | Wert |
|---|---|
| `ANTHROPIC_API_KEY` | dein Key |
| `AC_API_URL` | `https://mumlifebalance.api-us1.com` |
| `AC_API_KEY` | AC → Settings → Developer |
| `AC_TAG_ABGESCHLOSSEN` | ID aus Schritt 2 |
| `AC_TAG_MBA_INTERESSE` | ID aus Schritt 2 |
| `AC_TAG_MINIKURS_INTERESSE` | ID aus Schritt 2 |

Danach nochmal `npx vercel --prod`, damit die Werte in die Functions kommen.

### 5 — Custom Domain (optional, später)
`freischaufeln.mumlifebalance.ch` → Vercel Settings → Domains → CNAME auf `cname.vercel-dns.com`. Für den Start reicht die `*.vercel.app`-URL.

---

## Danach (Funnel scharfstellen)
1. **ManyChat-Keyword `ZEIT`** → DM mit Anmelde-Link/Landing.
2. **WordPress-Anmeldeseite** `/freischaufeln` mit AC-Inline-Formular (wie Bio-Check, wegen WAF kein AC-Embed-Script).
3. **AC-Automation „Freischaufeln Auslieferung"**: Formular → Mail mit Tool-Link `https://<vercel-url>/?e=%EMAIL%&n=%FIRSTNAME%`.
4. **`active-funnels.json`**: Eintrag `todo-halbieren` auf `freischaufeln` + Live-URL aktualisieren.
5. **End-CTA-Link:** in `public/index.html` die Konstante `CTA_URL` (aktuell `https://mumlifebalance.ch`) auf das gewünschte Ziel setzen (MBA-Cart / Minikurs).

---

## Lokal testen
```bash
npx vercel dev   # http://localhost:3000/?e=test@example.com&n=Patricia
```
Braucht die ENV-Werte lokal (`.env` aus `.env.example`) für die API-Routen. Ohne Keys lädt nur das Frontend.

## System-Prompt / Voice ändern
`lib/system-prompt.md` editieren → `npx vercel --prod`.

## Kosten
Vercel Free-Tier reicht locker; Claude ~0.01–0.03 CHF pro Durchlauf (3 Sonnet-Calls).
