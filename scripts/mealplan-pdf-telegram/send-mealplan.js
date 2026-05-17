#!/usr/bin/env node
/**
 * Mealplan → PDF → Telegram
 *
 * Usage:
 *   node send-mealplan.js <markdown-file> <kw-label>
 *
 * Example:
 *   node send-mealplan.js ../../outputs/mealplans/2026-KW20-wochenplan.md "KW20"
 *
 * Reads Markdown, renders to a nicely-styled PDF (klickbare Hyperlinks intakt),
 * sendet via Telegram Bot API an Patricias Chat.
 *
 * Env (lädt aus ../telegram-news-bot/.env):
 *   TELEGRAM_BOT_TOKEN
 *   TELEGRAM_CHAT_ID
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from '../md-to-pdf/node_modules/marked/lib/marked.esm.js';
import puppeteer from '../md-to-pdf/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------- Args ----------
const [mdPathArg, kwLabel] = process.argv.slice(2);
if (!mdPathArg) {
  console.error('Usage: node send-mealplan.js <markdown-file> [kw-label]');
  process.exit(1);
}
const mdPath = resolve(__dirname, mdPathArg);
if (!existsSync(mdPath)) {
  console.error(`Markdown nicht gefunden: ${mdPath}`);
  process.exit(1);
}
const label = kwLabel || basename(mdPath, '.md');

// ---------- Env ----------
const envPath = resolve(__dirname, '../telegram-news-bot/.env');
if (!existsSync(envPath)) {
  console.error(`.env nicht gefunden: ${envPath}`);
  process.exit(1);
}
const envContent = readFileSync(envPath, 'utf8');
const env = Object.fromEntries(
  envContent.split('\n')
    .filter(l => l && !l.startsWith('#') && l.includes('='))
    .map(l => {
      const idx = l.indexOf('=');
      return [l.slice(0, idx).trim(), l.slice(idx + 1).trim()];
    })
);
const BOT_TOKEN = env.TELEGRAM_BOT_TOKEN;
const CHAT_ID = env.TELEGRAM_CHAT_ID;
if (!BOT_TOKEN || !CHAT_ID) {
  console.error('TELEGRAM_BOT_TOKEN oder TELEGRAM_CHAT_ID fehlen in .env');
  process.exit(1);
}

// ---------- Markdown → HTML ----------
const md = readFileSync(mdPath, 'utf8');
const bodyHtml = marked.parse(md, { gfm: true, breaks: true });

const html = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Wochenplan ${label}</title>
<style>
  @page { size: A4; margin: 18mm 14mm; }
  body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1f2937; font-size: 11pt; line-height: 1.45; }
  h1 { color: #0d9488; font-size: 22pt; margin: 0 0 8pt; border-bottom: 3px solid #0d9488; padding-bottom: 6pt; }
  h2 { color: #0d9488; font-size: 15pt; margin: 18pt 0 6pt; border-bottom: 1px solid #d1d5db; padding-bottom: 3pt; }
  h3 { color: #d97706; font-size: 12pt; margin: 12pt 0 4pt; }
  h4 { color: #374151; font-size: 11pt; margin: 8pt 0 4pt; }
  table { width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 9.5pt; page-break-inside: avoid; }
  th { background: #0d9488; color: white; padding: 5pt 6pt; text-align: left; font-weight: 600; }
  td { border: 1px solid #d1d5db; padding: 5pt 6pt; vertical-align: top; }
  tr:nth-child(even) td { background: #f9fafb; }
  a { color: #0d9488; text-decoration: underline; font-weight: 600; }
  a:hover { color: #d97706; }
  ul, ol { margin: 4pt 0 8pt 18pt; padding: 0; }
  li { margin: 2pt 0; }
  code { background: #f3f4f6; padding: 1pt 4pt; border-radius: 3px; font-family: "SF Mono", Consolas, monospace; font-size: 9.5pt; }
  blockquote { border-left: 4px solid #d97706; background: #fef3c7; padding: 8pt 12pt; margin: 8pt 0; }
  hr { border: 0; border-top: 1px dashed #d1d5db; margin: 14pt 0; }
  .footer { margin-top: 24pt; padding-top: 8pt; border-top: 1px solid #d1d5db; color: #6b7280; font-size: 8.5pt; text-align: center; }
  /* Vermeide Seitenumbruch mitten in Tabellenzeile */
  tr { page-break-inside: avoid; }
  /* Tagestabelle visuell hervorheben */
  table.menuplan th { font-size: 9pt; }
  table.menuplan td { font-size: 9pt; }
</style>
</head>
<body>
${bodyHtml}
<div class="footer">
  🍳 Patricias Kochbot · Wochenplan ${label} · Rezepte aus eigener DB + Coaching-Makros 1850/135P/180KH/63F<br>
  Erstellt: ${new Date().toLocaleString('de-CH')}
</div>
</body>
</html>`;

// Save HTML next to MD for debugging
const htmlPath = mdPath.replace(/\.md$/, '.html');
writeFileSync(htmlPath, html, 'utf8');

// ---------- HTML → PDF ----------
console.log(`🧱  Rendere PDF: ${label}`);
const browser = await puppeteer.launch({ headless: 'new' });
const page = await browser.newPage();
await page.setContent(html, { waitUntil: 'networkidle0' });
const pdfPath = mdPath.replace(/\.md$/, '.pdf');
await page.pdf({
  path: pdfPath,
  format: 'A4',
  margin: { top: '18mm', bottom: '18mm', left: '14mm', right: '14mm' },
  printBackground: true,
  preferCSSPageSize: true,
});
await browser.close();
console.log(`✅  PDF erstellt: ${pdfPath}`);

// ---------- Telegram Send ----------
console.log(`📲  Sende an Telegram (Chat ${CHAT_ID.slice(0, 4)}…)`);

const FormData = (await import('node:stream/web')).FormData
  || globalThis.FormData;
const formData = new FormData();
formData.append('chat_id', CHAT_ID);
formData.append(
  'caption',
  `🍳 *Wochenplan ${label}*\n\nMenuplan + Rezepte + Einkaufsliste — Rezept-Links im PDF sind klickbar.\n\nViel Spass beim Kochen 💚`
);
formData.append('parse_mode', 'Markdown');

const pdfBlob = new Blob([readFileSync(pdfPath)], { type: 'application/pdf' });
formData.append('document', pdfBlob, `Wochenplan_${label}.pdf`);

const resp = await fetch(
  `https://api.telegram.org/bot${BOT_TOKEN}/sendDocument`,
  { method: 'POST', body: formData }
);
const json = await resp.json();
if (!json.ok) {
  console.error('❌  Telegram-Fehler:', JSON.stringify(json, null, 2));
  process.exit(1);
}
console.log(`✅  PDF an Telegram geschickt (message_id ${json.result.message_id})`);
