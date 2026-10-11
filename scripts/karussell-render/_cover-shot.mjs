import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
const a = Object.fromEntries(process.argv.slice(2).map(x => {
  const [k, ...r] = x.replace(/^--/, '').split('='); return [k, r.join('=') || true];
}));
await fs.mkdir(path.dirname(path.resolve(a.output)), { recursive: true });
const browser = await puppeteer.launch({ headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: Number(a.w), height: Number(a.h), deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.resolve(a.input)).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 400));
  const el = await page.$('.cover');
  await el.screenshot({ path: path.resolve(a.output), type: 'png' });
  console.log('OK');
} finally { await browser.close(); }
