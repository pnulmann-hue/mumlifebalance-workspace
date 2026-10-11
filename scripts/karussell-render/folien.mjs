/**
 * Rendert Karussell-Folien (1080x1350) aus einer JSON-Definition.
 *   node folien.mjs <definition.json> <ausgabe-ordner>
 * Bildpfade in der Definition sind relativ zum Ordner der Definition.
 * Doku: siehe CLAUDE.md, Abschnitt Karussell-Render-Pipeline.
 */
import puppeteer from 'puppeteer';
import { readFileSync, mkdirSync } from 'fs';
import { dirname, resolve, join } from 'path';
import { pathToFileURL } from 'url';

const [defPfad, ausgabe] = process.argv.slice(2);
if (!defPfad || !ausgabe) { console.error('Aufruf: node folien.mjs <def.json> <ordner>'); process.exit(1); }

const def = JSON.parse(readFileSync(defPfad, 'utf8'));
const basis = dirname(resolve(defPfad));
mkdirSync(ausgabe, { recursive: true });

const F = {
  creme: '#f1ecdd', petrol: '#12828c', blau: '#0c1c30',
  tief: '#29556d', orange: '#dc822e', weiss: '#ffffff',
};

const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// *Wort* wird orange hervorgehoben
const hv = s => esc(s).replace(/\*(.+?)\*/g, '<em>$1</em>').replace(/&lt;br&gt;/g, '<br>');

function folieHtml(f) {
  const dunkel = f.grund === 'blau' || f.grund === 'petrol';
  const bg = f.grund === 'blau' ? F.blau : f.grund === 'petrol' ? F.petrol : F.creme;
  const fg = dunkel ? F.creme : F.blau;
  const sub = dunkel ? 'rgba(241,236,221,.78)' : F.tief;

  const kopf = f.pille
    ? `<div class="kopf"><span class="pille">${esc(f.pille)}</span>${f.zaehler ? `<span class="zaehler">${esc(f.zaehler)}</span>` : ''}</div>`
    : '';

  const bild = f.bild ? `
    <div class="buehne">
      ${f.zeiger ? `<div class="zeiger">${hv(f.zeiger)}</div>` : ''}
      <div class="karte">
        <img src="${esc(f.bild)}" alt="">
        ${(f.marken || []).map(m => `<div class="mark${m.streich ? ' streich' : ''}" style="top:${m.top}%;height:${m.hoehe}%;left:${m.links ?? 1}%;right:${m.rechts ?? 12}%"></div>`).join('')}
      </div>
    </div>` : '';

  const nach = (f.mitte ? `<div class="mitte${f.gross ? ' gross' : ''}${f.klein ? ' klein' : ''}"><p>${hv(f.mitte)}</p></div>` : '')
    + (f.schluss ? `<div class="schluss">${hv(f.schluss)}</div>` : '');

  const fuss = f.fuss
    ? `<div class="fuss"><p>${hv(f.fuss)}</p>${f.letzte ? '' : '<span class="weiter">→</span>'}</div>`
    : (f.letzte ? '' : '<div class="fuss"><span class="weiter" style="margin-left:auto">→</span></div>');

  if (f.biokarte) {
    const b = f.biokarte;
    return `<div class="slide" style="background:${bg};color:${fg}">
      ${kopf}
      ${f.titel ? `<h1 style="color:${fg}">${hv(f.titel)}</h1>` : ''}
      ${f.unter ? `<p class="unter" style="color:${sub}">${hv(f.unter)}</p>` : ''}
      <div class="buehne">
        <div class="karte bioblatt${b.gut ? ' gut' : ''}">
          <div class="bioname">${hv(b.name)}</div>
          ${b.kategorie ? `<div class="biokat">${hv(b.kategorie)}</div>` : ''}
          ${(b.zeilen || []).map(z => `<div class="biozeile">${hv(z)}</div>`).join('')}
          ${b.link ? `<div class="biolink">${esc(b.link)}</div>` : ''}
        </div>
      </div>
      ${f.fuss ? `<div class="fuss"><p>${hv(f.fuss)}</p>${f.letzte ? '' : '<span class="weiter">→</span>'}</div>` : ''}
    </div>`;
  }
  if (f.cover) {
    return `<div class="slide cover" style="background:${bg};color:${fg}">
      <div class="marke">${esc(f.marke ?? '')}</div>
      <div class="hookraum">
        <h1 class="hook" style="color:${fg}">${hv(f.titel)}</h1>
        ${f.unter ? `<p class="hookunter" style="color:${sub}">${hv(f.unter)}</p>` : ''}
      </div>
      ${f.fuss ? `<div class="fuss"><p>${hv(f.fuss)}</p><span class="weiter">→</span></div>` : ''}
    </div>`;
  }
  return `<div class="slide" style="background:${bg};color:${fg}">
    ${kopf}
    ${f.titel ? `<h1 style="color:${fg}">${hv(f.titel)}</h1>` : ''}
    ${f.unter ? `<p class="unter" style="color:${sub}">${hv(f.unter)}</p>` : ''}
    ${bild}${nach}${fuss}
  </div>`;
}

const css = `
*{margin:0;padding:0;box-sizing:border-box}
body{background:#777}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;
  font-family:'Source Sans 3',sans-serif;display:flex;flex-direction:column;
  padding:150px 62px 146px}
.kopf{display:flex;align-items:center;gap:15px;margin-bottom:20px}
.pille{background:${F.petrol};color:#fff;font-weight:600;font-size:25px;
  letter-spacing:.08em;text-transform:uppercase;padding:9px 23px;border-radius:999px}
.zaehler{font-size:25px;opacity:.6}
h1{font-family:'Philosopher',serif;font-size:76px;line-height:1.05;font-weight:700;margin-bottom:12px}
h1 em{font-style:normal;color:${F.orange}}
.unter{font-size:30px;line-height:1.4;font-weight:300;max-width:860px}
.unter em{font-style:normal;color:${F.orange};font-weight:400}
.buehne{flex:1;display:flex;align-items:center;justify-content:flex-end;margin:22px 0 14px;position:relative}
.karte{position:relative;width:846px;border-radius:22px;background:#fff;
  box-shadow:0 20px 48px rgba(12,28,48,.19);overflow:hidden;border:1px solid rgba(12,28,48,.07)}
.karte img{display:block;width:100%}
.mark{position:absolute;border:5px solid ${F.orange};border-radius:9px}
.mark.streich{border-color:#c0392b}
.mark.streich::after{content:"";position:absolute;left:3%;right:3%;top:50%;
  height:5px;background:#c0392b;transform:translateY(-50%)}
.zeiger{position:absolute;right:802px;top:50%;transform:translateY(-50%);width:150px;
  font-size:23px;font-weight:600;color:${F.orange};text-align:right;line-height:1.22}
.mitte{flex:1;display:flex;flex-direction:column;justify-content:center;padding:10px 0}
.mitte>p{font-size:44px;line-height:1.36;font-weight:300}
.mitte em{font-style:normal;color:${F.orange};font-weight:600}
.mitte.klein>p{font-size:37px;line-height:1.4}
.mitte.gross>p{font-size:60px;line-height:1.24;font-weight:400}
.schluss{font-size:38px;font-weight:600;color:${F.orange};padding:6px 0 14px}
.fuss{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;min-height:52px}
.fuss p{font-size:30px;line-height:1.42;max-width:810px}
.fuss em{font-style:normal;color:${F.petrol};font-weight:600}
.weiter{font-size:44px;color:${F.petrol};flex-shrink:0;padding-bottom:4px}
.slide.cover{padding:160px 78px 150px}
.marke{font-size:24px;letter-spacing:.14em;text-transform:uppercase;opacity:.52;
  font-weight:600;margin-bottom:8px}
.hookraum{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:30px}
h1.hook{font-family:'Philosopher',serif;font-size:88px;line-height:1.08;font-weight:700;
  margin:0 0 30px;max-width:900px}
.hookunter{font-size:38px;line-height:1.36;font-weight:300;max-width:840px}
.bioblatt{width:846px;padding:44px 46px 46px;font-family:'Source Sans 3',sans-serif;
  color:#111;border-left:12px solid #c0392b}
.bioblatt.gut{border-left-color:${F.petrol}}
.bioname{font-size:35px;font-weight:600;margin-bottom:6px}
.bioname em{font-style:normal;color:${F.petrol}}
.biokat{font-size:31px;color:#8a8a8a;margin-bottom:12px}
.biozeile{font-size:33px;line-height:1.46}
.biozeile em{font-style:normal;color:${F.orange};font-weight:600}
.biolink{font-size:33px;color:#2d4fd6;margin-top:10px;font-weight:600}
`;

const html = `<!doctype html><html lang="de"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
<style>${css}</style></head><body>${def.folien.map(folieHtml).join('')}</body></html>`;

const tmp = join(basis, '_folien.html');
(await import('fs')).writeFileSync(tmp, html, 'utf8');

const b = await puppeteer.launch({ headless: 'new' });
const p = await b.newPage();
await p.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0' });
await p.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
});
const els = await p.$$('.slide');
for (let i = 0; i < els.length; i++) {
  const n = String(i + 1).padStart(2, '0');
  await els[i].screenshot({ path: join(ausgabe, `${n}.png`) });
  console.log(`  ${n}.png`);
}
await b.close();
console.log(`${els.length} Folien -> ${ausgabe}`);
