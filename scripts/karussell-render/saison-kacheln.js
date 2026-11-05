/**
 * Saison-Kacheln für die Gruppe „Gesund durchs ganze Jahr“ (1080×1080 PNG), eine Vorlage für alle Saisons.
 * Liest die Texte aus paket.json (gebaut von scripts/oelgruppe/paket-bauen.py). Kein Foto, keine KI.
 *
 *   node scripts/karussell-render/saison-kacheln.js outputs/telegram-posts/herbst-2026
 *   -> <ordner>/tiles/post-<nr>.png
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';

const ICONS = {
  drop: '<path d="M32 8 C32 8 16 26 16 38 a16 16 0 0 0 32 0 C48 26 32 8 32 8 Z"/>',
  leaf: '<path d="M12 52 C12 30 30 14 52 12 C54 34 38 52 12 52 Z M22 42 L44 20"/>',
  sun: '<circle cx="32" cy="32" r="12"/><g stroke-width="4"><line x1="32" y1="4" x2="32" y2="14"/><line x1="32" y1="50" x2="32" y2="60"/><line x1="4" y1="32" x2="14" y2="32"/><line x1="50" y1="32" x2="60" y2="32"/><line x1="12" y1="12" x2="19" y2="19"/><line x1="45" y1="45" x2="52" y2="52"/><line x1="52" y1="12" x2="45" y2="19"/><line x1="19" y1="45" x2="12" y2="52"/></g>',
  cup: '<path d="M14 24 h30 v10 a15 15 0 0 1 -30 0 Z M44 26 h6 a5 5 0 0 1 0 10 h-6 M18 8 v6 M26 6 v8 M34 8 v6"/>',
  moon: '<path d="M40 8 A24 24 0 1 0 56 40 A18 18 0 0 1 40 8 Z"/>',
  glass: '<path d="M18 12 h28 l-4 20 a10 10 0 0 1 -20 0 Z M32 32 v14 M24 46 h16"/>',
  spark: '<path d="M32 8 L36 28 L56 32 L36 36 L32 56 L28 36 L8 32 L28 28 Z"/>',
  bath: '<path d="M10 34 h44 v6 a12 12 0 0 1 -12 12 H22 a12 12 0 0 1 -12 -12 Z M16 34 V16 a6 6 0 0 1 12 0"/>',
  mountain: '<path d="M6 52 L24 20 L36 40 L44 26 L58 52 Z"/>',
  bottle: '<path d="M26 8 h12 v8 l4 8 v30 a6 6 0 0 1 -6 6 H28 a6 6 0 0 1 -6 -6 V24 l4 -8 Z M22 34 h20"/>',
  star: '<path d="M32 6 V58 M9 19 L55 45 M55 19 L9 45"/>',
  candle: '<path d="M24 26 h16 v30 h-16 Z M32 26 V18 M32 6 C37 11 37 15 32 18 C27 15 27 11 32 6 Z"/>',
  gift: '<path d="M12 26 h40 v28 h-40 Z M8 18 h48 v8 h-48 Z M32 18 v36 M32 18 C24 6 14 12 20 18 M32 18 C40 6 50 12 44 18"/>',
};
const VOLL = ['drop', 'moon', 'spark', 'mountain'];
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function seite(k) {
  const voll = VOLL.includes(k.icon);
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
.slide{width:1080px;height:1080px;background:#f1ecdd;position:relative;font-family:'Source Sans 3',sans-serif;display:flex;flex-direction:column;align-items:center;overflow:hidden}
.header{width:100%;background:#12828c;color:#fff;text-align:center;padding:26px 0;font-weight:600;font-size:30px;letter-spacing:7px}
.body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 90px 90px;width:100%}
.iconwrap{width:150px;height:150px;border-radius:50%;background:#dbe7e6;display:flex;align-items:center;justify-content:center;margin-bottom:44px}
.iconwrap svg{width:74px;height:74px}
.title{font-family:'Philosopher',serif;font-weight:700;color:#29556d;font-size:100px;line-height:1.03;text-align:center}
.rule{width:96px;height:5px;background:#dc822e;border-radius:3px;margin:38px 0}
.sub{font-size:40px;color:#29556d;text-align:center;max-width:820px;line-height:1.3}
.pill{margin-top:48px;background:#12828c;color:#fff;font-weight:600;font-size:30px;padding:20px 40px;border-radius:999px;text-align:center}
.footer{position:absolute;bottom:40px;left:0;width:100%;text-align:center;color:#29556d;opacity:.75;font-size:27px;font-weight:300;letter-spacing:1.5px}
</style></head><body><div class="slide">
<div class="header">GESUND DURCHS GANZE JAHR</div>
<div class="body"><div class="iconwrap"><svg viewBox="0 0 64 64" fill="${voll ? '#29556d' : 'none'}" stroke="#29556d" stroke-width="${voll ? 0 : 4}" stroke-linecap="round" stroke-linejoin="round">${ICONS[k.icon] || ICONS.drop}</svg></div>
<div class="title">${esc(k.title).replace(/\n/g, '<br>')}</div><div class="rule"></div>
<div class="sub">${esc(k.sub)}</div><div class="pill">${esc(k.pill)}</div></div>
<div class="footer">mum life balance · mit ätherischen Ölen</div></div></body></html>`;
}

const ordner = path.resolve(process.argv[2]);
const paket = JSON.parse(await fs.readFile(path.join(ordner, 'paket.json'), 'utf8'));
await fs.mkdir(path.join(ordner, 'tiles'), { recursive: true });
const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1080 });
for (const b of paket.beitraege) {
  await page.setContent(seite(b.kachel), { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  const ueber = await page.evaluate(() => { const s = document.querySelector('.body'); return s.scrollHeight > s.clientHeight || s.scrollWidth > s.clientWidth; });
  if (ueber) console.log('⚠️ läuft über:', b.nr, b.kachel.title);
  await (await page.$('.slide')).screenshot({ path: path.join(ordner, 'tiles', `post-${b.nr}.png`) });
}
await browser.close();
console.log(paket.beitraege.length, 'Kacheln ->', path.join(ordner, 'tiles'));
