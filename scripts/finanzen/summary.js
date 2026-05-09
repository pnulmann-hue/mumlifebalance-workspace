#!/usr/bin/env node
// Kombiniert PayPal + Bank fuer Monats-Cashflow-Bilanz.
// Schreibt Notion-konformen Text-Block den Patricia in die Monatsplan-Page kopiert.
//
// Verwendung:
//   node summary.js <yyyy-mm>
//   node summary.js 2026-04
//
// Voraussetzung: parse-paypal.js + parse-bank.js wurden vorher gelaufen.

import fs from 'node:fs';
import path from 'node:path';

const month = process.argv[2];
if (!month || !/^\d{4}-\d{2}$/.test(month)) {
  console.error('Usage: node summary.js <yyyy-mm>');
  process.exit(1);
}

const repoRoot = path.resolve(import.meta.dirname, '..', '..');
const outDir = path.join(repoRoot, 'outputs', 'finanzen', month);
const paypalPath = path.join(outDir, 'paypal-parsed.json');
const bankPath = path.join(outDir, 'bank-parsed.json');

const paypal = fs.existsSync(paypalPath) ? JSON.parse(fs.readFileSync(paypalPath, 'utf8')) : null;
const bank = fs.existsSync(bankPath) ? JSON.parse(fs.readFileSync(bankPath, 'utf8')) : null;

if (!paypal && !bank) {
  console.error('Keine PayPal- oder Bank-Daten gefunden — erst parse-paypal.js + parse-bank.js laufen lassen.');
  process.exit(1);
}

let paypalEinnahmenNetto = 0, paypalGebuehren = 0, paypalAusgaben = 0;
if (paypal) {
  paypal.einnahmenListe.forEach(t => { paypalEinnahmenNetto += t.netto; paypalGebuehren += Math.abs(t.gebuehr); });
  paypal.ausgabenListe.forEach(t => { paypalAusgaben += Math.abs(t.brutto); });
}

let bankEinnahmen = 0, bankAusgaben = 0;
if (bank) {
  bank.businessEinnahmenListe.forEach(t => { bankEinnahmen += t.gutschrift; });
  bank.businessAusgabenListe.forEach(t => { bankAusgaben += t.belastung; });
}

// Doppel-Erfassung: PayPal-Auszahlungen tauchen oft in Bank als Gutschrift auf — Patricia muss manuell
// abgleichen. Wir markieren das im Output als Hinweis statt automatisch zu entfernen.

const totalEinnahmen = paypalEinnahmenNetto + bankEinnahmen;
const totalAusgaben = paypalAusgaben + bankAusgaben + paypalGebuehren;
const cashflow = totalEinnahmen - totalAusgaben;

const md = `# Cashflow-Bilanz ${month}

Generiert: ${new Date().toISOString().slice(0, 10)} via \`scripts/finanzen/summary.js\`.

## Bilanz

| Quelle | Einnahmen | Ausgaben |
|---|---|---|
| PayPal | ${paypalEinnahmenNetto.toFixed(2)} CHF (netto, nach Gebuehren ${paypalGebuehren.toFixed(2)}) | ${paypalAusgaben.toFixed(2)} CHF |
| Bank | ${bankEinnahmen.toFixed(2)} CHF | ${bankAusgaben.toFixed(2)} CHF |
| **Total** | **${totalEinnahmen.toFixed(2)} CHF** | **${totalAusgaben.toFixed(2)} CHF** |
| **Cashflow** | | **${cashflow.toFixed(2)} CHF** |

⚠ **Doppel-Erfassung pruefen:** PayPal-Auszahlungen erscheinen in Bank als Gutschrift. Patricia bitte sicherstellen dass Bank-Gutschriften von PayPal NICHT zusaetzlich als Einnahme zaehlen.

## Notion-Block (copy-paste in Mai-Monatsplan-Page → Properties → "Erkenntnis Kennzahlen-Analyse")

\`\`\`
UMSATZ ${month}: ${totalEinnahmen.toFixed(2)} CHF (PayPal netto ${paypalEinnahmenNetto.toFixed(2)} + Bank Business ${bankEinnahmen.toFixed(2)}). Ausgaben ${totalAusgaben.toFixed(2)} CHF (PayPal-Gebuehren ${paypalGebuehren.toFixed(2)} + Tools/Services). Cashflow netto: ${cashflow.toFixed(2)} CHF.
\`\`\`

## Detail-Quellen

- PayPal-Detail: \`outputs/finanzen/${month}/paypal-summary.md\`
- Bank-Detail: \`outputs/finanzen/${month}/bank-summary.md\`
`;

fs.writeFileSync(path.join(outDir, 'cashflow-summary.md'), md);

console.log(`✓ Cashflow ${month}: ${cashflow.toFixed(2)} CHF`);
console.log(`✓ Output: outputs/finanzen/${month}/cashflow-summary.md`);
