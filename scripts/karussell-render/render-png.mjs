/** HTML → full-page PNG (QA-Screenshot). node render-png.mjs --input=... --output=... */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const args = Object.fromEntries(process.argv.slice(2).map(a => {
  const [k, ...r] = a.replace(/^--/, '').split('='); return [k, r.join('=') || true];
}));
const inputPath = path.resolve(args.input);
const outputPath = path.resolve(args.output);
await fs.mkdir(path.dirname(outputPath), { recursive: true });

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});
try {
  const page = await browser.newPage();
  // A4 @ ~96dpi ≈ 794x1123
  await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$('.page');
  await el.screenshot({ path: outputPath, type: 'png' });
  console.log('OK', outputPath);
} finally { await browser.close(); }
