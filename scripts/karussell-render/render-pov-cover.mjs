import puppeteer from 'puppeteer';
import path from 'node:path';

const WORKSPACE = 'C:/Users/pnulm/Desktop/Mein Business';
const htmlPath = `${WORKSPACE}/scripts/reel-cover/pov-dorf-cover-v2.html`;
const outPath = `${WORKSPACE}/scripts/reel-cover/covers/pov-dorf-cover-v2.png`;

const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
await page.goto(`file:///${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });
await page.evaluate(() => Promise.all(
  Array.from(document.images).filter(i => !i.complete).map(i => new Promise(r => { i.onload = r; i.onerror = r; }))
));
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: outPath, type: 'png', fullPage: false });
await browser.close();
console.log('Saved:', outPath);
