import puppeteer from 'puppeteer';
import { pathToFileURL } from 'node:url';
// Ganze Seite am Handy (390 px) in Stücke à 1400 px Höhe fotografieren
const [,, src, prefix] = process.argv;
const b = await puppeteer.launch();
const p = await b.newPage();
await p.setViewport({ width: 390, height: 844, deviceScaleFactor: 1, isMobile: true });
await p.goto(pathToFileURL(src).href, { waitUntil: 'networkidle0' });
await p.evaluate(async () => { await document.fonts.ready; document.querySelectorAll('img').forEach(i => i.loading = 'eager'); });
await new Promise(r => setTimeout(r, 800));
const h = await p.evaluate(() => document.documentElement.scrollHeight);
let n = 0;
for (let y = 0; y < h; y += 1400) {
  await p.screenshot({ path: `${prefix}-${String(++n).padStart(2, '0')}.png`, clip: { x: 0, y, width: 390, height: Math.min(1400, h - y) }, captureBeyondViewport: true });
}
console.log('Höhe', h, 'Teile', n);
await b.close();
