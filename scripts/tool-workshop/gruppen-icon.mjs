// WhatsApp-Gruppenbild für die Workshop-Gruppe: 1024x1024, WhatsApp schneidet rund aus,
// deshalb liegt alles Wichtige im inneren Kreis. Ganz in HTML/CSS, keine KI-Bilder.
//
//   node scripts/tool-workshop/gruppen-icon.mjs
// -> outputs/produkte/tool-workshop/whatsapp/gruppen-icon.png (+ -kreis.png zur Kontrolle)
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');
const ZIEL = fileURLToPath(new URL('../../outputs/produkte/tool-workshop/whatsapp/', import.meta.url));

const html = (kreis) => `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@600;800&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1024px;height:1024px;background:${kreis ? '#ffffff' : '#0c1c30'}}
.b{position:relative;width:1024px;height:1024px;overflow:hidden;
  background:radial-gradient(circle at 30% 25%,#29556d 0%,#0c1c30 70%);
  ${kreis ? 'border-radius:50%;' : ''}display:flex;flex-direction:column;align-items:center;justify-content:center}
.handy{width:150px;height:250px;border-radius:30px;border:9px solid #dc822e;position:relative;margin-bottom:34px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.handy::before{content:"";position:absolute;top:14px;width:42px;height:8px;border-radius:4px;background:#dc822e}
.zeile{width:82px;height:12px;border-radius:6px;background:rgba(241,236,221,.35)}
.haken{width:74px;height:74px;border-radius:50%;background:#dc822e;color:#0c1c30;font-family:'Source Sans 3',sans-serif;
  font-weight:800;font-size:50px;line-height:74px;text-align:center}
.t{font-family:'Philosopher',serif;font-weight:700;font-size:170px;line-height:.95;color:#f1ecdd}
.w{font-family:'Source Sans 3',sans-serif;font-weight:800;font-size:58px;letter-spacing:.28em;color:#f1ecdd;margin-top:18px;padding-left:.28em}
.d{font-family:'Source Sans 3',sans-serif;font-weight:600;font-size:46px;color:#f3c38f;margin-top:26px;letter-spacing:.04em}
</style></head><body><div class="b"><div class="handy"><div class="zeile"></div><div class="haken">✓</div><div class="zeile"></div></div><div class="t">Tool</div><div class="w">WORKSHOP</div><div class="d">November 2026</div>
</div></body></html>`;

const browser = await puppeteer.launch({ headless: 'new' });
for (const [kreis, name] of [[false, 'gruppen-icon.png'], [true, 'gruppen-icon-kreis.png']]) {
  const s = await browser.newPage();
  await s.setViewport({ width: 1024, height: 1024 });
  await s.setContent(html(kreis), { waitUntil: 'networkidle0' });
  await s.evaluate(() => document.fonts.ready);
  await s.screenshot({ path: ZIEL + name });
}
await browser.close();
console.log('->', ZIEL);
