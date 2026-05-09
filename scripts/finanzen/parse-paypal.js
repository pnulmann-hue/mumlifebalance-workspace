#!/usr/bin/env node
// PayPal-CSV-Parser fuer Patricias monatliche Cashflow-Auswertung.
//
// Verwendung:
//   node parse-paypal.js <yyyy-mm>
//   node parse-paypal.js 2026-04
//
// Liest:  context/finanzen/<yyyy-mm>/paypal-transaktionen.csv
// Schreibt: outputs/finanzen/<yyyy-mm>/paypal-parsed.json (gitignored — raw)
//           outputs/finanzen/<yyyy-mm>/paypal-summary.md (committed)

import { parse } from 'csv-parse/sync';
import fs from 'node:fs';
import path from 'node:path';

const month = process.argv[2];
if (!month || !/^\d{4}-\d{2}$/.test(month)) {
  console.error('Usage: node parse-paypal.js <yyyy-mm>  (z.B. 2026-04)');
  process.exit(1);
}

const repoRoot = path.resolve(import.meta.dirname, '..', '..');
const inputPath = path.join(repoRoot, 'context', 'finanzen', month, 'paypal-transaktionen.csv');
const outDir = path.join(repoRoot, 'outputs', 'finanzen', month);

if (!fs.existsSync(inputPath)) {
  console.error(`Datei fehlt: ${inputPath}`);
  console.error('Patricia: PayPal-Transaktionsbericht als CSV in den Monatsordner legen.');
  process.exit(1);
}

const raw = fs.readFileSync(inputPath, 'utf8');
// PayPal-CSV ist UTF-8 mit BOM, Trennzeichen Komma, eingeschlossen in "
const records = parse(raw, {
  columns: true,
  skip_empty_lines: true,
  relax_column_count: true,
  bom: true,
});

if (records.length === 0) {
  console.error('Keine Datensaetze in CSV gefunden — Format pruefen.');
  process.exit(1);
}

// Spaltennamen sind je nach DE/EN unterschiedlich — wir mappen auf einheitliche Keys.
const colMap = (row) => {
  const get = (...keys) => {
    for (const k of keys) {
      if (row[k] !== undefined) return row[k];
    }
    return '';
  };
  return {
    datum: get('Datum', 'Date'),
    typ: get('Typ', 'Type'),
    status: get('Status'),
    waehrung: get('Waehrung', 'Währung', 'Currency'),
    brutto: parseFloat(String(get('Brutto', 'Gross')).replace(/[\s']/g, '').replace(',', '.')) || 0,
    gebuehr: parseFloat(String(get('Gebuehr', 'Gebühr', 'Fee')).replace(/[\s']/g, '').replace(',', '.')) || 0,
    netto: parseFloat(String(get('Netto', 'Net')).replace(/[\s']/g, '').replace(',', '.')) || 0,
    name: get('Name'),
    artikel: get('Artikelbezeichnung', 'Item Title'),
    txn: get('Transaktionscode', 'Transaction ID'),
  };
};

const transactions = records.map(colMap);

// Kategorisierung nach Patricias Business-Logik
const klassifizieren = (t) => {
  const typLower = (t.typ || '').toLowerCase();
  const statusLower = (t.status || '').toLowerCase();

  if (statusLower.includes('storn') || statusLower.includes('refund')) return 'storno';
  if (typLower.includes('auszahlung') || typLower.includes('withdrawal') || typLower.includes('transfer')) return 'auszahlung';
  if (typLower.includes('gebühr') || typLower.includes('gebuehr') || typLower.includes('fee')) return 'gebuehr';
  if (t.brutto > 0 && (typLower.includes('zahlung') || typLower.includes('payment') || typLower.includes('checkout') || typLower.includes('mobile'))) return 'einnahme';
  if (t.brutto < 0) return 'ausgabe';
  return 'unklar';
};

let einnahmenBrutto = 0, einnahmenNetto = 0, gebuehrenTotal = 0;
let ausgabenTotal = 0, stornoTotal = 0;
const einnahmenListe = [], ausgabenListe = [], unklarListe = [];

transactions.forEach((t) => {
  const kat = klassifizieren(t);
  if (kat === 'einnahme') {
    einnahmenBrutto += t.brutto;
    einnahmenNetto += t.netto;
    gebuehrenTotal += Math.abs(t.gebuehr);
    einnahmenListe.push(t);
  } else if (kat === 'ausgabe') {
    ausgabenTotal += Math.abs(t.brutto);
    ausgabenListe.push(t);
  } else if (kat === 'storno') {
    stornoTotal += Math.abs(t.brutto);
  } else if (kat === 'unklar') {
    unklarListe.push(t);
  }
});

fs.mkdirSync(outDir, { recursive: true });

// Raw parsed JSON (gitignored)
fs.writeFileSync(
  path.join(outDir, 'paypal-parsed.json'),
  JSON.stringify({ month, transactions, einnahmenListe, ausgabenListe, unklarListe }, null, 2)
);

// Summary MD (committed)
const md = `# PayPal-Auswertung ${month}

Generiert: ${new Date().toISOString().slice(0, 10)} via \`scripts/finanzen/parse-paypal.js\`.

## Bilanz

| Posten | Betrag |
|---|---|
| Einnahmen brutto | ${einnahmenBrutto.toFixed(2)} CHF |
| PayPal-Gebuehren | -${gebuehrenTotal.toFixed(2)} CHF |
| **Einnahmen netto** | **${einnahmenNetto.toFixed(2)} CHF** |
| Ausgaben | -${ausgabenTotal.toFixed(2)} CHF |
| Stornos | -${stornoTotal.toFixed(2)} CHF |
| Unklar (Patricia pruefen) | ${unklarListe.length} Transaktionen |
| Anzahl Transaktionen | ${transactions.length} |

## Einnahmen-Liste (${einnahmenListe.length} Transaktionen)

${einnahmenListe.map(t => `- **${t.datum}** · ${t.netto.toFixed(2)} ${t.waehrung} · ${t.name} · ${t.artikel || '(kein Artikel)'} · TXN ${t.txn}`).join('\n') || '_keine_'}

## Ausgaben-Liste (${ausgabenListe.length} Transaktionen)

${ausgabenListe.map(t => `- **${t.datum}** · ${t.brutto.toFixed(2)} ${t.waehrung} · ${t.name} · ${t.artikel || '(kein Artikel)'} · TXN ${t.txn}`).join('\n') || '_keine_'}

## Unklar — bitte pruefen (${unklarListe.length})

${unklarListe.map(t => `- **${t.datum}** · ${t.brutto.toFixed(2)} ${t.waehrung} · Typ: ${t.typ} · Status: ${t.status} · ${t.name}`).join('\n') || '_keine_'}
`;

fs.writeFileSync(path.join(outDir, 'paypal-summary.md'), md);

console.log(`✓ ${transactions.length} Transaktionen geparst`);
console.log(`✓ Einnahmen netto: ${einnahmenNetto.toFixed(2)} CHF`);
console.log(`✓ Output: ${path.relative(repoRoot, outDir)}/paypal-summary.md`);
if (unklarListe.length > 0) {
  console.log(`⚠ ${unklarListe.length} unklare Transaktionen — bitte pruefen.`);
}
