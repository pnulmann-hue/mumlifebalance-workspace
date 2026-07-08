#!/usr/bin/env node
import puppeteer from '/home/user/mumlifebalance-workspace/scripts/karussell-render/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const HTML = path.join(__dirname, 'workbook.html');
const PDF = path.join(__dirname, 'content-box-30-hook-vorlagen.pdf');
const QA_DIR = path.join(__dirname, 'qa-pages');

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  try {
    const page = await browser.newPage();
    await page.goto('file://' + HTML, { waitUntil: 'networkidle0', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1500));

    await page.pdf({
      path: PDF, format: 'A4', printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      preferCSSPageSize: true,
    });
    const stat = await fs.stat(PDF);
    console.log(`PDF: ${(stat.size / 1024).toFixed(0)} KB`);

    // QA: screenshot each .page at ~140 DPI for visual check
    await fs.mkdir(QA_DIR, { recursive: true });
    await page.setViewport({ width: 1160, height: 1640, deviceScaleFactor: 1 });
    const count = await page.evaluate(() => document.querySelectorAll('.page').length);
    for (let i = 0; i < count; i++) {
      const el = await page.$(`.page:nth-of-type(${i + 1})`);
      await el.screenshot({ path: path.join(QA_DIR, `p${String(i + 1).padStart(2, '0')}.png`) });
    }
    console.log(`QA pages: ${count}`);
  } finally {
    await browser.close();
  }
}
main().catch(e => { console.error(e); process.exit(1); });
