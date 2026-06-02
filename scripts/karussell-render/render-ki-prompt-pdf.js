#!/usr/bin/env node
import puppeteer from 'puppeteer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const HTML_PATH = path.join(REPO_ROOT, 'outputs', 'freebies', 'ki-strategie-prompt.html');
const OUTPUT_PDF = path.join(REPO_ROOT, 'outputs', 'freebies', 'KI-Strategie-Prompts-Patricia-Ulmann.pdf');

async function main() {
  console.log(`Loading HTML: ${path.relative(REPO_ROOT, HTML_PATH)}`);
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none']
  });
  try {
    const page = await browser.newPage();
    const fileUrl = 'file://' + HTML_PATH;
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1500));

    console.log('Generating PDF...');
    await page.pdf({
      path: OUTPUT_PDF,
      format: 'A4',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      preferCSSPageSize: true
    });

    const stat = await fs.stat(OUTPUT_PDF);
    console.log(`✓ PDF generated: ${path.relative(REPO_ROOT, OUTPUT_PDF)}`);
    console.log(`  Size: ${(stat.size / 1024).toFixed(0)} KB`);
  } finally {
    await browser.close();
  }
}

main().catch(err => { console.error(err); process.exit(1); });
