#!/usr/bin/env node
// Schweizer-Bank-CSV-Parser fuer Patricias monatliche Cashflow-Auswertung.
// Erkennt Format automatisch: PostFinance, Raiffeisen, UBS, ZKB, Migros Bank.
// Wenn Format unbekannt: meldet sich und bittet Patricia das Format zu nennen.
//
// Verwendung:
//   node parse-bank.js <yyyy-mm>
//   node parse-bank.js 2026-04
//
// Liest:  context/finanzen/<yyyy-mm>/bank-auszug.csv
// Schreibt: outputs/finanzen/<yyyy-mm>/bank-parsed.json (gitignored)
//           outputs/finanzen/<yyyy-mm>/bank-summary.md (committed, ohne sensible Details)
//
// WICHTIG: PDF-Bank-Auszuege werden nicht direkt unterstuetzt — Patricia muss CSV/XLSX exportieren.
// Falls keine CSV-Option: PDF in Tabellen-Tool (Excel/Numbers) konvertieren und als CSV speichern.

import { parse } from 'csv-parse/sync';
import fs from 'node:fs';
import path from 'node:path';

const month = process.argv[2];
if (!month || !/^\d{4}-\d{2}$/.test(month)) {
  console.error('Usage: node parse-bank.js <yyyy-mm>');
  process.exit(1);
}

const repoRoot = path.resolve(import.meta.dirname, '..', '..');
const inputPath = path.join(repoRoot, 'context', 'finanzen', month, 'bank-auszug.csv');
const outDir = path.join(repoRoot, 'outputs', 'finanzen', month);

if (!fs.existsSync(inputPath)) {
  console.error(`Datei fehlt: ${inputPath}`);
  process.exit(1);
}

const raw = fs.readFileSync(inputPath, 'utf8');

// Format-Detection — typische Header-Spalten der Schweizer Banken
const detectFormat = (header) => {
  const h = header.toLowerCase();
  if (h.includes('avisierungstext')) return 'postfinance';
  if (h.includes('valutadatum') && h.includes('text') && h.includes('betrag in chf')) return 'raiffeisen';
  if (h.includes('description') && h.includes('debit') && h.includes('credit')) return 'ubs';
  if (h.includes('buchungstext') && h.includes('belastung') && h.includes('gutschrift')) return 'zkb';
  if (h.includes('buchungsdatum') && h.includes('mitteilung')) return 'migrosbank';
  return 'unbekannt';
};

const firstLine = raw.split('\n')[0];
const format = detectFormat(firstLine);

if (format === 'unbekannt') {
  console.error('Bank-Format nicht erkannt. Erste Zeile:', firstLine.slice(0, 200));
  console.error('Bitte Format-Header notieren und Skript erweitern (parse-bank.js Funktion detectFormat).');
  process.exit(1);
}

console.log(`Format erkannt: ${format}`);

// Generischer Parser — auto-detect Trennzeichen, dann pro Format Spalten mappen
const detectDelimiter = (line) => {
  if (line.includes(';')) return ';';
  if (line.includes('\t')) return '\t';
  return ',';
};
const delimiter = detectDelimiter(firstLine);

const records = parse(raw, {
  columns: true,
  skip_empty_lines: true,
  relax_column_count: true,
  bom: true,
  delimiter,
});

const parseAmount = (s) => {
  if (!s) return 0;
  return parseFloat(String(s).replace(/[\s']/g, '').replace(',', '.')) || 0;
};

const mapper = {
  postfinance: (r) => ({
    datum: r['Datum'] || r['Buchungsdatum'] || '',
    text: r['Avisierungstext'] || r['Text'] || '',
    belastung: parseAmount(r['Belastung']),
    gutschrift: parseAmount(r['Gutschrift']),
    saldo: parseAmount(r['Saldo']),
  }),
  raiffeisen: (r) => ({
    datum: r['Buchungsdatum'] || r['Valutadatum'] || '',
    text: r['Text'] || r['Buchungstext'] || '',
    belastung: parseAmount(r['Betrag in CHF']) < 0 ? Math.abs(parseAmount(r['Betrag in CHF'])) : 0,
    gutschrift: parseAmount(r['Betrag in CHF']) > 0 ? parseAmount(r['Betrag in CHF']) : 0,
    saldo: parseAmount(r['Saldo'] || ''),
  }),
  ubs: (r) => ({
    datum: r['Trade date'] || r['Booking date'] || '',
    text: r['Description'] || r['Description 1'] || '',
    belastung: parseAmount(r['Debit']),
    gutschrift: parseAmount(r['Credit']),
    saldo: parseAmount(r['Balance'] || ''),
  }),
  zkb: (r) => ({
    datum: r['Datum'] || r['Buchungsdatum'] || '',
    text: r['Buchungstext'] || '',
    belastung: parseAmount(r['Belastung CHF'] || r['Belastung']),
    gutschrift: parseAmount(r['Gutschrift CHF'] || r['Gutschrift']),
    saldo: parseAmount(r['Saldo'] || ''),
  }),
  migrosbank: (r) => ({
    datum: r['Buchungsdatum'] || '',
    text: r['Mitteilung'] || r['Verwendungszweck'] || '',
    belastung: parseAmount(r['Belastung'] || (parseAmount(r['Betrag']) < 0 ? Math.abs(parseAmount(r['Betrag'])) : 0)),
    gutschrift: parseAmount(r['Gutschrift'] || (parseAmount(r['Betrag']) > 0 ? parseAmount(r['Betrag']) : 0)),
    saldo: parseAmount(r['Saldo'] || ''),
  }),
};

const transactions = records.map(mapper[format]);

// Business-Heuristik: Patricia kann diese Liste pflegen unter context/finanzen/business-keywords.json
const businessKeywordsPath = path.join(repoRoot, 'context', 'finanzen', 'business-keywords.json');
let businessKeywords = {
  einnahme: ['paypal', 'thrivecart', 'stripe', 'doterra', 'gutschrift kunde'],
  ausgabe: ['paypal', 'canva', 'notion', 'anthropic', 'chatgpt', 'openai', 'cloudflare', 'github', 'apify', 'wordpress', 'thrivecart', 'manychat', 'blotato', 'kit ', 'activecampaign', 'wispr', 'figma', 'zapier'],
};
if (fs.existsSync(businessKeywordsPath)) {
  businessKeywords = JSON.parse(fs.readFileSync(businessKeywordsPath, 'utf8'));
}

const klassifizieren = (t) => {
  const tx = (t.text || '').toLowerCase();
  if (t.gutschrift > 0) {
    if (businessKeywords.einnahme.some(k => tx.includes(k))) return 'business-einnahme';
    return 'einnahme-unklar';
  }
  if (t.belastung > 0) {
    if (businessKeywords.ausgabe.some(k => tx.includes(k))) return 'business-ausgabe';
    return 'ausgabe-unklar';
  }
  return 'unklar';
};

let businessEinnahmen = 0, businessAusgaben = 0;
const businessEinnahmenListe = [], businessAusgabenListe = [], unklarListe = [];

transactions.forEach((t) => {
  const kat = klassifizieren(t);
  if (kat === 'business-einnahme') {
    businessEinnahmen += t.gutschrift;
    businessEinnahmenListe.push({ ...t, kat });
  } else if (kat === 'business-ausgabe') {
    businessAusgaben += t.belastung;
    businessAusgabenListe.push({ ...t, kat });
  } else {
    unklarListe.push({ ...t, kat });
  }
});

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(
  path.join(outDir, 'bank-parsed.json'),
  JSON.stringify({ month, format, transactions, businessEinnahmenListe, businessAusgabenListe, unklarListe }, null, 2)
);

// Summary MD — KEINE personenbezogenen Details (nur Beschreibung anonymisiert)
const anonymize = (s) => s.replace(/(IBAN|BIC|Konto)[\s:]*[A-Z0-9]+/gi, '[KONTO_REDACTED]');

const md = `# Bank-Auswertung ${month} (Format: ${format})

Generiert: ${new Date().toISOString().slice(0, 10)} via \`scripts/finanzen/parse-bank.js\`.

## Bilanz Business-Posten

| Posten | Betrag |
|---|---|
| **Business-Einnahmen** | **${businessEinnahmen.toFixed(2)} CHF** |
| **Business-Ausgaben** | **-${businessAusgaben.toFixed(2)} CHF** |
| **Business-Cashflow** | **${(businessEinnahmen - businessAusgaben).toFixed(2)} CHF** |
| Unklar (Patricia pruefen) | ${unklarListe.length} Transaktionen |
| Anzahl Transaktionen total | ${transactions.length} |

## Business-Einnahmen (${businessEinnahmenListe.length})

${businessEinnahmenListe.map(t => `- **${t.datum}** · +${t.gutschrift.toFixed(2)} CHF · ${anonymize(t.text).slice(0, 80)}`).join('\n') || '_keine_'}

## Business-Ausgaben (${businessAusgabenListe.length})

${businessAusgabenListe.map(t => `- **${t.datum}** · -${t.belastung.toFixed(2)} CHF · ${anonymize(t.text).slice(0, 80)}`).join('\n') || '_keine_'}

## Unklar — Patricia pruefen ob privat oder Business (${unklarListe.length})

${unklarListe.slice(0, 30).map(t => `- **${t.datum}** · ${t.gutschrift > 0 ? '+' + t.gutschrift.toFixed(2) : '-' + t.belastung.toFixed(2)} CHF · ${anonymize(t.text).slice(0, 60)}`).join('\n') || '_keine_'}

${unklarListe.length > 30 ? `\n_(weitere ${unklarListe.length - 30} unklare Posten in \`bank-parsed.json\`)_` : ''}

---

**Hinweis:** Business-Heuristik basiert auf Keywords. Pflege \`context/finanzen/business-keywords.json\` um Treffer zu verbessern.
`;

fs.writeFileSync(path.join(outDir, 'bank-summary.md'), md);

console.log(`✓ ${transactions.length} Bank-Transaktionen geparst`);
console.log(`✓ Business-Cashflow: ${(businessEinnahmen - businessAusgaben).toFixed(2)} CHF`);
console.log(`✓ Output: ${path.relative(repoRoot, outDir)}/bank-summary.md`);
if (unklarListe.length > 0) {
  console.log(`⚠ ${unklarListe.length} unklare Transaktionen — pruefen ob privat/business.`);
}
