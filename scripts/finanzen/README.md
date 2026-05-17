# Finanzen Tracker

Scripts fuer Patricias monatliche Cashflow-Auswertung — kombiniert PayPal + Schweizer-Bank-Auszug.

## Setup (einmalig)

```bash
cd scripts/finanzen
npm install
```

## Verwendung — Stufe 2 (manueller Workflow)

### 1. Patricia legt Quelldaten ab

```
context/finanzen/2026-04/paypal-transaktionen.csv
context/finanzen/2026-04/bank-auszug.csv
```

(Anleitung wie zu exportieren: `context/finanzen/README.md`)

### 2. Claude (oder Patricia selbst) parst

```bash
cd scripts/finanzen
node parse-paypal.js 2026-04
node parse-bank.js 2026-04
node summary.js 2026-04
```

### 3. Output

- `outputs/finanzen/2026-04/paypal-summary.md` — PayPal-Einnahmen + Ausgaben + Unklare
- `outputs/finanzen/2026-04/bank-summary.md` — Bank-Cashflow + Unklare
- `outputs/finanzen/2026-04/cashflow-summary.md` — kombinierte Bilanz + Notion-Block
- `outputs/finanzen/2026-04/*-parsed.json` — Raw-Daten (gitignored)

### 4. Notion-Update

Patricia kopiert den Notion-Block aus `cashflow-summary.md` in die Monatsplan-Page → Property „Erkenntnis Kennzahlen-Analyse". Oder bittet Claude in einer naechsten Session: „Trag den Cashflow April in die Notion-Mai-Page ein".

## Bekannte Limits

- **Bank-PDF:** Wird nicht direkt unterstuetzt. Patricia muss CSV/XLSX exportieren oder PDF in Excel/Numbers oeffnen → als CSV speichern.
- **Doppel-Erfassung:** PayPal-Auszahlungen erscheinen in Bank als Gutschrift. Patricia muss manuell pruefen dass das nicht doppelt zaehlt. (Geplant: Auto-Match via Datum + Betrag.)
- **Bank-Format-Detection:** Aktuell PostFinance, Raiffeisen, UBS, ZKB, Migros Bank. Andere Banken: `parse-bank.js` Funktion `detectFormat` erweitern.

## Stufe 3 — Automatisierung (PayPal via GitHub Action)

Siehe `plans/2026-05-09-cashflow-tracker.md` Stufe 3 + `.github/workflows/paypal-monthly.yml`.

Dort wird PayPal-Token als Repo-Secret hinterlegt, GitHub Action laeuft monatlich am 1. und committet `paypal-transaktionen.csv` automatisch — Patricia muss nur noch Bank-CSV reinwerfen.

## Pflege

`context/finanzen/business-keywords.json` — wenn ein Bank-Posten nicht erkannt wurde: Keyword in die Liste eintragen, parse-bank.js erkennt es beim naechsten Lauf.

Beispiel:
```json
{
  "einnahme": ["paypal", "thrivecart", "stripe", "doterra", "gutschrift kunde"],
  "ausgabe": ["paypal", "canva", "notion", "anthropic", "chatgpt", "openai", "cloudflare", "github", "apify", "wordpress", "thrivecart", "manychat", "blotato", "kit ", "activecampaign", "wispr", "figma", "zapier"]
}
```
