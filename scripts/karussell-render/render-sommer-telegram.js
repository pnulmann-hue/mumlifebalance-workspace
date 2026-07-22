/**
 * Sommer-Telegram-Kacheln — Typo-Design im Frühlings-Look (1080×1080 PNG).
 *
 * Reines Text-Template in Patricias Brand (Creme + Petrol + Orange + Philosopher).
 * Kein Foto, kein KI-Bild — volle Textkontrolle, Schweizer ss.
 *
 * Nutzung:  node render-sommer-telegram.js
 * Output:   ../../outputs/telegram-posts/sommer-2026/tiles/post-<N>.png
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, '..', '..', 'outputs', 'telegram-posts', 'sommer-2026', 'tiles');

// Icons (schlichte Linien-Symbole, dunkelpetrol) — je nach Thema
const ICONS = {
  drop: '<path d="M32 8 C32 8 16 26 16 38 a16 16 0 0 0 32 0 C48 26 32 8 32 8 Z"/>',
  leaf: '<path d="M12 52 C12 30 30 14 52 12 C54 34 38 52 12 52 Z M22 42 L44 20"/>',
  sun: '<circle cx="32" cy="32" r="12"/><g stroke-width="4"><line x1="32" y1="4" x2="32" y2="14"/><line x1="32" y1="50" x2="32" y2="60"/><line x1="4" y1="32" x2="14" y2="32"/><line x1="50" y1="32" x2="60" y2="32"/><line x1="12" y1="12" x2="19" y2="19"/><line x1="45" y1="45" x2="52" y2="52"/><line x1="52" y1="12" x2="45" y2="19"/><line x1="19" y1="45" x2="12" y2="52"/></g>',
  cup: '<path d="M14 24 h30 v10 a15 15 0 0 1 -30 0 Z M44 26 h6 a5 5 0 0 1 0 10 h-6 M18 8 v6 M26 6 v8 M34 8 v6"/>',
  moon: '<path d="M40 8 A24 24 0 1 0 56 40 A18 18 0 0 1 40 8 Z"/>',
  glass: '<path d="M18 12 h28 l-4 20 a10 10 0 0 1 -20 0 Z M32 32 v14 M24 46 h16"/>',
  spark: '<path d="M32 8 L36 28 L56 32 L36 36 L32 56 L28 36 L8 32 L28 28 Z"/>',
  shield: '<path d="M32 8 L52 16 V34 C52 46 42 54 32 58 C22 54 12 46 12 34 V16 Z M24 32 l6 6 l12 -14"/>',
  bath: '<path d="M10 34 h44 v6 a12 12 0 0 1 -12 12 H22 a12 12 0 0 1 -12 -12 Z M16 34 V16 a6 6 0 0 1 12 0"/>',
  mountain: '<path d="M6 52 L24 20 L36 40 L44 26 L58 52 Z"/>',
  bottle: '<path d="M26 8 h12 v8 l4 8 v30 a6 6 0 0 1 -6 6 H28 a6 6 0 0 1 -6 -6 V24 l4 -8 Z M22 34 h20"/>',
  suitcase: '<path d="M14 24 h36 v30 h-36 Z M24 24 v-8 h16 v8 M14 38 h36"/>',
};

// Header konstant (wie Frühling: Gruppenname, nicht Saison)
const HEADER = 'GESUND DURCHS GANZE JAHR';
const FOOTER = 'mum life balance · mit ätherischen Ölen';

// 16 Beiträge — Titel (mit \n-Umbruch), Untertitel, Pill (Kern-Öle), Icon
const POSTS = [
  { n: 1,  icon: 'bottle',   title: 'Erfrischungs-\nSpray',  sub: 'Sofort-Abkühlung an heissen Tagen',   pill: 'Peppermint · Wild Orange' },
  { n: 2,  icon: 'drop',     title: 'Kühler Kopf',           sub: 'Wenn die Hitze in den Nacken steigt',  pill: 'Peppermint · Rosmarin · Spearmint' },
  { n: 3,  icon: 'bath',     title: 'Fussbad-\nRitual',      sub: 'Der Feierabend für müde Füsse',        pill: 'Peppermint · Lavender' },
  { n: 4,  icon: 'leaf',     title: 'Kühle\nKompresse',      sub: 'Runterkühlen bei Hitze-Kopf',          pill: 'Peppermint · Lavender · Geranium' },
  { n: 5,  icon: 'sun',      title: 'Nach der\nSonne',       sub: 'Pflege für sonnenverwöhnte Haut',      pill: 'Lavender · Frankincense' },
  { n: 6,  icon: 'shield',   title: 'Sanfter\nSchutz',       sub: 'Wenn’s summt und surrt',           pill: 'Citronella · Lemongrass · Tea Tree' },
  { n: 7,  icon: 'bath',     title: 'Entspannungs-\nBad',    sub: 'Laue Abende, tiefes Durchatmen',       pill: 'Lavender · Ylang Ylang' },
  { n: 8,  icon: 'spark',    title: 'Achtsamkeit',           sub: 'Kleine Pausen im Sommer',              pill: 'Sandelholz · Weihrauch · Myrrhe' },
  { n: 9,  icon: 'moon',     title: 'Sonnen-\nuntergang',    sub: 'Diffuser-Magie für laue Abende',       pill: 'Bergamotte · Lavender · Vetiver' },
  { n: 10, icon: 'glass',    title: 'Sommer-\nLimonade',     sub: 'Erfrischung für heisse Tage',          pill: 'Lemon · Peppermint' },
  { n: 11, icon: 'drop',     title: 'Aroma-\nWürfel',        sub: 'Dein Wasser mit Wow-Effekt',           pill: 'Lemon · Lime · Lavender' },
  { n: 12, icon: 'glass',    title: 'Sommer-\nDrinks',       sub: 'Alkoholfrei und aromatisch',           pill: 'Lavender · Rosmarin · Spearmint' },
  { n: 13, icon: 'cup',      title: 'Wach &\nWohlig',        sub: 'Morgens Energie, abends Ruhe',         pill: 'Lemon · Grapefruit · Ingwer' },
  { n: 14, icon: 'leaf',     title: 'Sommer-\nKüche',        sub: 'Würzen mit ätherischen Ölen',          pill: 'Basilikum · Oregano · Rosmarin' },
  { n: 15, icon: 'suitcase', title: 'Reise-\nBegleiter',     sub: 'Deine Öle für unterwegs',              pill: 'Lavender · Peppermint · Ingwer' },
  { n: 16, icon: 'mountain', title: 'Öle\ndraussen',         sub: 'Wandern, Lagerfeuer, Garten',          pill: 'Zypresse · Kiefer · Eukalyptus' },
];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const titleHtml = (t) => esc(t).replace(/\n/g, '<br>');

function buildHtml(p) {
  const iconSvg = ICONS[p.icon] || ICONS.drop;
  const strokeIcons = ['leaf', 'sun', 'cup', 'glass', 'shield', 'bath', 'bottle', 'suitcase'];
  const isStroke = strokeIcons.includes(p.icon);
  return `<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
.slide{width:1080px;height:1080px;background:#f1ecdd;position:relative;font-family:'Source Sans 3',sans-serif;color:#0c1c30;display:flex;flex-direction:column;align-items:center;overflow:hidden}
.header{width:100%;background:#12828c;color:#fff;text-align:center;padding:26px 0;font-weight:600;font-size:30px;letter-spacing:7px}
.body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 90px;width:100%}
.iconwrap{width:150px;height:150px;border-radius:50%;background:#dbe7e6;display:flex;align-items:center;justify-content:center;margin-bottom:44px}
.iconwrap svg{width:74px;height:74px}
.title{font-family:'Philosopher',serif;font-weight:700;color:#29556d;font-size:104px;line-height:1.03;text-align:center}
.rule{width:96px;height:5px;background:#dc822e;border-radius:3px;margin:40px 0}
.sub{font-size:40px;color:#29556d;text-align:center;font-weight:400;max-width:820px;line-height:1.3}
.pill{margin-top:54px;background:#12828c;color:#fff;font-weight:600;font-size:32px;padding:20px 46px;border-radius:999px;text-align:center}
.footer{position:absolute;bottom:44px;left:0;width:100%;text-align:center;color:#29556d;opacity:.75;font-size:27px;font-weight:300;letter-spacing:1.5px}
</style></head>
<body><div class="slide">
  <div class="header">${esc(HEADER)}</div>
  <div class="body">
    <div class="iconwrap">
      <svg viewBox="0 0 64 64" fill="${isStroke ? 'none' : '#29556d'}" stroke="#29556d" stroke-width="${isStroke ? '4' : '0'}" stroke-linecap="round" stroke-linejoin="round">${iconSvg}</svg>
    </div>
    <div class="title">${titleHtml(p.title)}</div>
    <div class="rule"></div>
    <div class="sub">${esc(p.sub)}</div>
    <div class="pill">${esc(p.pill)}</div>
  </div>
  <div class="footer">${esc(FOOTER)}</div>
</div></body></html>`;
}

await fs.mkdir(OUT_DIR, { recursive: true });
const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1080, deviceScaleFactor: 1 });

const only = process.argv.includes('--only') ? Number(process.argv[process.argv.indexOf('--only') + 1]) : null;
const todo = only ? POSTS.filter(p => p.n === only) : POSTS;

for (const p of todo) {
  await page.setContent(buildHtml(p), { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 400));
  const el = await page.$('.slide');
  const out = path.join(OUT_DIR, `post-${p.n}.png`);
  await el.screenshot({ path: out, type: 'png' });
  console.log(`✅ post-${p.n}.png — ${p.title.replace(/\n/g, ' ')}`);
}

await browser.close();
console.log(`\nFertig: ${todo.length} Kacheln in ${OUT_DIR}`);
