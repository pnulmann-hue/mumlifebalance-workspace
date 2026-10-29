// Cover (Folie 1) des Pin-Karussells Nischengenerator, in der Bildsprache des Stimm-Check-Covers:
// grosser Titel, Tablet mit echtem Ergebnis-Bildschirm vor dem Bogen, Karte „Deine 3 Themen“,
// Sprechblase, orange Pille. Ganz in HTML/CSS, keine KI-Bilder.
//
//   node scripts/salespage-design/pin-nische-cover.mjs
// -> outputs/karussells/renders/2026-10-29-pin-nische/01.png (1080x1350)
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');
const R = (p) => fileURLToPath(new URL('../../' + p, import.meta.url));
const schirm = 'data:image/png;base64,' + readFileSync(R('outputs/salespages/nischengenerator/bild/schirm-ergebnis.png')).toString('base64');

const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700;800&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}
.b{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:'Source Sans 3',sans-serif;color:#0c1c30;
  background:radial-gradient(ellipse at 50% 18%,#f8f4ea 0%,#f1ecdd 55%,#e7dfcb 100%)}
.titel{position:absolute;top:70px;left:0;right:0;text-align:center;font-family:'Philosopher',serif;font-weight:700;
  font-size:128px;line-height:.95;letter-spacing:-1px}
.unter{position:absolute;top:350px;left:0;right:0;text-align:center;font-size:50px;line-height:1.2;color:#0c1c30}
.bogen{position:absolute;left:180px;top:610px;width:720px;height:720px;border-radius:50%;background:#12828c}
.tisch{position:absolute;left:0;right:0;top:1120px;bottom:0;background:linear-gradient(#e2d8c2,#d8cdb4)}
.tablet{position:absolute;left:215px;top:540px;width:430px;height:600px;background:#0c1c30;border-radius:34px;padding:18px;
  box-shadow:0 30px 60px rgba(12,28,48,.35);transform:rotate(-2deg)}
.tablet img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:18px;display:block}
.karte{position:absolute;left:600px;top:720px;width:300px;background:#fbf8f0;border-radius:22px;padding:26px 24px;
  box-shadow:0 24px 50px rgba(12,28,48,.3);transform:rotate(4deg)}
.karte h3{font-family:'Philosopher',serif;font-size:32px;display:flex;align-items:center;gap:12px;margin-bottom:18px}
.haken{width:44px;height:44px;border-radius:50%;background:#12828c;color:#fff;font-size:28px;display:grid;place-items:center;flex:none}
.z{display:flex;align-items:center;gap:12px;margin:14px 0}
.n{width:34px;height:34px;border-radius:50%;background:#f3c38f;color:#7a3f0d;font-weight:800;font-size:18px;display:grid;place-items:center;flex:none}
.l{flex:1}.l i{display:block;height:9px;border-radius:5px;background:#12828c;margin-bottom:7px}.l i+i{background:#cfd6d8;width:80%}
.blase{position:absolute;left:640px;top:520px;background:#f3c38f;color:#0c1c30;font-family:'Philosopher',serif;font-weight:700;
  font-size:38px;line-height:1.1;text-align:center;padding:24px 32px;border-radius:60px;transform:rotate(-3deg)}
.blase::after{content:"";position:absolute;left:58px;bottom:-22px;border:16px solid transparent;border-top:24px solid #f3c38f;border-bottom:0}
.pille{position:absolute;left:50%;transform:translateX(-50%);top:1180px;background:#dc822e;color:#fff;font-weight:700;
  font-size:40px;padding:16px 46px;border-radius:999px;white-space:nowrap}
.fuss{position:absolute;left:0;right:0;top:1282px;text-align:center;font-family:'Philosopher',serif;font-size:30px;letter-spacing:.14em;color:#0c1c30}
</style></head><body><div class="b">
<div class="titel">Der Nischen&shy;-<br>generator</div>
<div class="unter">Damit du endlich weisst,<br>wofür du stehst.</div>
<div class="bogen"></div><div class="tisch"></div>
<div class="tablet"><img src="${schirm}"></div>
<div class="karte"><h3><span class="haken">✓</span>Deine 3 Themen</h3>
  <div class="z"><span class="n">1</span><span class="l"><i></i><i></i></span></div>
  <div class="z"><span class="n">2</span><span class="l"><i></i><i></i></span></div>
  <div class="z"><span class="n">3</span><span class="l"><i></i><i></i></span></div>
</div>
<div class="blase">Dein Thema.<br>Dein Satz.</div>
<div class="pille">Kostenlos · ca. 10 Minuten</div>
<div class="fuss">Mum Life Balance</div>
</div></body></html>`;

const browser = await puppeteer.launch({ headless: 'new' });
const s = await browser.newPage();
await s.setViewport({ width: 1080, height: 1350 });
await s.setContent(html, { waitUntil: 'networkidle0' });
await s.evaluate(() => document.fonts.ready);
await s.screenshot({ path: R('outputs/karussells/renders/2026-10-29-pin-nische/01.png') });
await browser.close();
console.log('-> 01.png');
