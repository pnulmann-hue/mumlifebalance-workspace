#!/usr/bin/env node
/**
 * Render 8 Slides für Weiterbildungs-Karussell · V1 Petrol-Solid
 */
import puppeteer from 'puppeteer';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const COLORS = {
  petrol: '#12828c',
  creme: '#f1ecdd',
  cremeSoft: 'rgba(241, 236, 221, 0.7)',
  orange: '#dc822e',
  text: '#0c1c30',
};

const SLIDES = [
  {
    num: 1,
    hero: 'In Weiterbildung zu investieren ist für mich <em>so klar</em>, wie nach dem Toilettengang zu spülen.',
    sub: '',
    heroSize: 76,
    isCover: true,
  },
  {
    num: 2,
    hero: 'Ich reinvestiere einen Teil meines Gewinns immer in Weiterbildung.',
    sub: 'Und das schon seit 2023.',
    heroSize: 80,
  },
  {
    num: 3,
    hero: 'Einerseits ist es mir wichtig, dass ich immer die <em>neusten Infos</em> am Markt habe.',
    sub: '',
    heroSize: 80,
  },
  {
    num: 4,
    hero: 'Andererseits will ich <em>solo bleiben</em> — und meine Kundinnen trotzdem 1:1 betreuen können.',
    sub: '',
    heroSize: 76,
  },
  {
    num: 5,
    hero: 'Gerade letzteres bedarf, dass ich mich im Bereich <em>KI und Automatisierung</em> ständig weiterentwickle.',
    sub: '',
    heroSize: 70,
  },
  {
    num: 6,
    hero: 'Schliesslich will ich ja auch raus aus dem <em>Zeit-gegen-Geld</em>.',
    sub: '',
    heroSize: 84,
  },
  {
    num: 7,
    hero: 'Wenn du einen einzigen Rat von mir hören willst:',
    sub: 'Investiere unbedingt in deine Weiterbildung.',
    heroSize: 70,
  },
  {
    num: 8,
    hero: 'Schick mir ein Herz 🤍 wenn du das genau so siehst.',
    sub: '',
    heroSize: 76,
    isCTA: true,
  },
];

const TOTAL = SLIDES.length;

function renderSlide(slide) {
  const labelText = slide.isCover
    ? 'mein bauchgefühl'
    : slide.isCTA
      ? 'wenn auch du'
      : `${slide.num} / ${TOTAL}`;

  const subBlock = slide.sub
    ? `<p class="sub">${slide.sub}</p>`
    : '';

  return `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Slide ${slide.num}</title>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { background: #000; }
  .slide {
    width: 1080px;
    height: 1350px;
    background: ${COLORS.petrol};
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 200px 100px;
    position: relative;
    font-family: 'Source Sans 3', sans-serif;
  }
  .accent-bar {
    width: 60px;
    height: 3px;
    background: ${COLORS.cremeSoft};
    margin-bottom: 70px;
    border-radius: 2px;
  }
  .hero {
    font-family: 'Philosopher', serif;
    font-weight: 700;
    font-size: ${slide.heroSize}px;
    line-height: 1.18;
    color: ${COLORS.creme};
    text-align: center;
    max-width: 880px;
    margin-bottom: ${slide.sub ? '40px' : '0'};
  }
  .hero em {
    font-style: italic;
    color: ${COLORS.orange};
    font-weight: 400;
  }
  .sub {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 42px;
    line-height: 1.45;
    color: ${COLORS.cremeSoft};
    text-align: center;
    max-width: 880px;
  }
  .footer-brand {
    position: absolute;
    bottom: 60px;
    left: 100px;
    font-family: 'Source Sans 3', sans-serif;
    color: ${COLORS.cremeSoft};
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
  }
  .footer-meta {
    position: absolute;
    bottom: 60px;
    right: 100px;
    font-family: 'Philosopher', serif;
    font-style: italic;
    color: ${COLORS.cremeSoft};
    font-size: 24px;
  }
</style>
</head>
<body>
  <div class="slide">
    <div class="accent-bar"></div>
    <h1 class="hero">${slide.hero}</h1>
    ${subBlock}
    <div class="footer-brand">Mum Life Balance</div>
    <div class="footer-meta">${slide.num} / ${TOTAL}</div>
  </div>
</body>
</html>`;
}

const browser = await puppeteer.launch({ headless: 'new' });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });

for (const slide of SLIDES) {
  const html = renderSlide(slide);
  const htmlPath = path.join(__dirname, `slide-${String(slide.num).padStart(2, '0')}.html`);
  await writeFile(htmlPath, html, 'utf-8');
  await page.goto('file://' + htmlPath.replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 500));
  const pngPath = path.join(__dirname, `slide-${String(slide.num).padStart(2, '0')}.png`);
  await page.screenshot({ path: pngPath, type: 'png', clip: { x: 0, y: 0, width: 1080, height: 1350 } });
  console.log(`Slide ${slide.num} rendered`);
}

await browser.close();
console.log('Done.');
