/** HTML -> transparent full-viewport PNG. node render-transparent.mjs --input=... --output=... [--w=1080 --h=1920] */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const args = Object.fromEntries(process.argv.slice(2).map(a => {
  const [k, ...r] = a.replace(/^--/, '').split('='); return [k, r.join('=') || true];
}));
const inputPath = path.resolve(args.input);
const outputPath = path.resolve(args.output);
const W = parseInt(args.w || '1080', 10), H = parseInt(args.h || '1920', 10);
await fs.mkdir(path.dirname(outputPath), { recursive: true });

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: outputPath, type: 'png', omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } });
  console.log('OK', outputPath);
} finally { await browser.close(); }
