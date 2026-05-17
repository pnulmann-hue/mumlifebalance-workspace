#!/usr/bin/env node
// PayPal Transaction Search API v1 - holt Vormonats-Transaktionen automatisch.
//
// Verwendung:
//   PAYPAL_CLIENT_ID=... PAYPAL_CLIENT_SECRET=... node fetch-paypal-api.js [yyyy-mm]
//
// Wenn yyyy-mm weggelassen: nimmt automatisch Vormonat.
//
// API-Doku: https://developer.paypal.com/docs/api/transaction-search/v1/

import fs from 'node:fs';
import path from 'node:path';

const CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const CLIENT_SECRET = process.env.PAYPAL_CLIENT_SECRET;
const API_BASE = process.env.PAYPAL_ENV === 'sandbox'
  ? 'https://api-m.sandbox.paypal.com'
  : 'https://api-m.paypal.com';

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('Fehlt: PAYPAL_CLIENT_ID + PAYPAL_CLIENT_SECRET');
  console.error('Setup: https://developer.paypal.com/dashboard/applications/live → REST API App erstellen');
  process.exit(1);
}

// Vormonat berechnen wenn nicht angegeben
const monthArg = process.argv[2];
let year, month;
if (monthArg && /^\d{4}-\d{2}$/.test(monthArg)) {
  [year, month] = monthArg.split('-').map(Number);
} else {
  const now = new Date();
  const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  year = lastMonth.getFullYear();
  month = lastMonth.getMonth() + 1;
}
const monthStr = `${year}-${String(month).padStart(2, '0')}`;
const startDate = `${monthStr}-01T00:00:00Z`;
const lastDay = new Date(year, month, 0).getDate();
const endDate = `${monthStr}-${String(lastDay).padStart(2, '0')}T23:59:59Z`;

console.log(`Hole PayPal-Transaktionen ${monthStr} (${startDate} bis ${endDate})`);

// 1. Access Token holen
const tokenRes = await fetch(`${API_BASE}/v1/oauth2/token`, {
  method: 'POST',
  headers: {
    'Authorization': 'Basic ' + Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64'),
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'grant_type=client_credentials',
});
if (!tokenRes.ok) {
  console.error('Token-Fehler:', await tokenRes.text());
  process.exit(1);
}
const { access_token } = await tokenRes.json();
console.log('✓ Access Token erhalten');

// 2. Transactions holen — Pagination beachten
const allTransactions = [];
let page = 1;
const pageSize = 500;
while (true) {
  const url = `${API_BASE}/v1/reporting/transactions?start_date=${startDate}&end_date=${endDate}&fields=all&page_size=${pageSize}&page=${page}`;
  const res = await fetch(url, {
    headers: { 'Authorization': `Bearer ${access_token}` },
  });
  if (!res.ok) {
    console.error('Transactions-Fehler:', await res.text());
    process.exit(1);
  }
  const data = await res.json();
  const txs = data.transaction_details || [];
  allTransactions.push(...txs);
  console.log(`  Seite ${page}: ${txs.length} Transaktionen`);
  if (txs.length < pageSize) break;
  page++;
}
console.log(`✓ Total: ${allTransactions.length} Transaktionen`);

// 3. In CSV-Format konvertieren das parse-paypal.js erwartet (DE-Header)
const headers = ['Datum', 'Typ', 'Status', 'Waehrung', 'Brutto', 'Gebuehr', 'Netto', 'Name', 'Artikelbezeichnung', 'Transaktionscode'];

const rows = allTransactions.map(t => {
  const info = t.transaction_info || {};
  const payer = t.payer_info || {};
  const cart = (t.cart_info && t.cart_info.item_details && t.cart_info.item_details[0]) || {};
  return [
    (info.transaction_initiation_date || '').slice(0, 10),
    info.transaction_event_code || '',
    info.transaction_status || '',
    (info.transaction_amount && info.transaction_amount.currency_code) || 'CHF',
    (info.transaction_amount && info.transaction_amount.value) || '0',
    (info.fee_amount && info.fee_amount.value) || '0',
    String(parseFloat((info.transaction_amount && info.transaction_amount.value) || 0) + parseFloat((info.fee_amount && info.fee_amount.value) || 0)),
    (payer.payer_name && (payer.payer_name.alternate_full_name || `${payer.payer_name.given_name || ''} ${payer.payer_name.surname || ''}`.trim())) || '',
    cart.item_name || '',
    info.transaction_id || '',
  ];
});

const csvEscape = (v) => {
  const s = String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};
const csv = [headers.join(','), ...rows.map(r => r.map(csvEscape).join(','))].join('\n');

const repoRoot = path.resolve(import.meta.dirname, '..', '..');
const outDir = path.join(repoRoot, 'context', 'finanzen', monthStr);
fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, 'paypal-transaktionen.csv');
fs.writeFileSync(outPath, csv);
console.log(`✓ Geschrieben: context/finanzen/${monthStr}/paypal-transaktionen.csv`);
console.log('Naechster Schritt: node parse-paypal.js ' + monthStr);
