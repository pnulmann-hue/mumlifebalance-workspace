// Hero-Bild der Anmeldeseite /nischengenerator/: zwei Handys mit echten Bildschirmen des Tools
// (aus nischengenerator-bildschirme.mjs), Aufkleber in Patricias Farben. Ganz in HTML/CSS, keine KI-Bilder.
//
//   node scripts/salespage-design/nischengenerator-bildschirme.mjs   (zuerst, holt die Bildschirme)
//   node scripts/salespage-design/nischengenerator-bild.mjs
// -> outputs/salespages/nischengenerator/bild/hero.png (1400x1000, durchsichtig)
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');
const ZIEL = fileURLToPath(new URL('../../outputs/salespages/nischengenerator/bild/', import.meta.url));
const b64 = (n) => 'data:image/png;base64,' + readFileSync(ZIEL + n).toString('base64');

const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@700;800&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}html,body{background:transparent}
.b{position:relative;width:1400px;height:1000px;font-family:'Source Sans 3',sans-serif}
.schatten{box-shadow:0 34px 80px rgba(0,0,0,.5),0 10px 24px rgba(0,0,0,.3)}
.handy{position:absolute;width:390px;height:780px;background:#0c1c30;border-radius:56px;padding:14px;border:2px solid #3b5f74}
.scr{width:100%;height:100%;border-radius:44px;background:#f1ecdd;padding-top:58px;overflow:hidden}
.handy img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
.handy::before{content:"";position:absolute;top:26px;left:50%;transform:translateX(-50%);width:110px;height:26px;border-radius:14px;background:#0c1c30;z-index:2}
.links{left:250px;top:150px;transform:rotate(-7deg)}
.rechts{left:740px;top:90px;transform:rotate(6deg)}
.kl{position:absolute;z-index:5;font-weight:800;color:#fff;border-radius:999px;padding:18px 30px;font-size:32px;white-space:nowrap}
.k1{left:120px;top:110px;background:#dc822e;transform:rotate(-8deg)}
.k2{left:1000px;top:800px;background:#12828c;transform:rotate(5deg)}
.k3{left:150px;top:820px;background:#f1ecdd;color:#29556d;transform:rotate(-4deg)}
</style></head><body><div class="b">
<div class="handy links schatten"><div class="scr"><img src="${b64('schirm-frage.png')}"></div></div>
<div class="handy rechts schatten"><div class="scr"><img src="${b64('schirm-ergebnis.png')}"></div></div>
<div class="kl k1 schatten">Gratis</div>
<div class="kl k3 schatten">Mit deinem Experten-Satz</div>
<div class="kl k2 schatten">Mit Tool-Ideen</div>
</div></body></html>`;

writeFileSync(ZIEL + 'hero.html', html);
const browser = await puppeteer.launch({ headless: 'new' });
const s = await browser.newPage();
await s.setViewport({ width: 1400, height: 1000 });
await s.setContent(html, { waitUntil: 'networkidle0' });
await s.evaluate(() => document.fonts.ready);
await s.screenshot({ path: ZIEL + 'hero.png', omitBackground: true });
await browser.close();
console.log('->', ZIEL + 'hero.png');
