// Prueft, ob eine Folie unten aus dem 1920x1080-Rahmen laeuft.
//
// 🚨 Node sucht puppeteer am Ort des SKRIPTS, nicht im Arbeitsverzeichnis.
//    Darum wie beim Schwesterskript erst hinueberkopieren:
//
//   cd scripts/karussell-render
//   cp ../ki-kurs/folien-hoehe-pruefen.mjs ./_h.mjs
//   node ./_h.mjs <deckordner>; rm -f ./_h.mjs
//
// 🚨 Der Rand-Reset ist der ganze Trick. Ohne "h2,p,ul{margin:0}" rechnet der
//    Browser die Standard-Abstaende von <h2> und <p> mit — und dann sieht jede
//    zweite Folie aus, als liefe sie 60 bis 140 Pixel ueber den Rand, obwohl
//    sie passt. Genau darauf bin ich am 04.11.2026 hereingefallen und habe
//    drei Folien gekuerzt, die in Ordnung waren. Das Deck ist mit "gap" gebaut,
//    also OHNE Standard-Abstaende; so muss auch gemessen werden.
//
// Ergaenzt folien-platz-pruefen.mjs: das prueft kippende Zeilenzahlen, dieses
// hier die Gesamthoehe. Beide gehoeren vor jedes Veroeffentlichen.
import puppeteer from "puppeteer";
import { readFileSync, readdirSync } from "fs";

const dir = process.argv[2];
if (!dir) { console.error("Ordner fehlt."); process.exit(1); }
let ids = process.argv.slice(3);
if (!ids.length) ids = readdirSync(`${dir}/project/slides`)
  .filter(f => f.endsWith(".html")).map(f => f.replace(/\.html$/, "")).sort();

const RESET = '<style>html,body{margin:0;padding:0}'
  + 'h1,h2,h3,h4,p,ul,ol,li,blockquote{margin:0}aside{display:none!important}'
  + 'section{width:1920px;height:1080px;box-sizing:border-box}</style>';

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });

let drueber = 0;
for (const id of ids) {
  await page.setContent(RESET + readFileSync(`${dir}/project/slides/${id}.html`, "utf-8"),
    { waitUntil: "networkidle0" });
  try { await page.evaluate(() => document.fonts.ready); } catch {}
  const r = await page.evaluate(() => {
    const s = document.querySelector("section");
    const pb = parseFloat(getComputedStyle(s).paddingBottom);
    let u = 0;
    for (const el of s.children) if (el.tagName !== "ASIDE") {
      const x = el.getBoundingClientRect().bottom; if (x > u) u = x;
    }
    return { unten: Math.round(u), grenze: Math.round(1080 - pb) };
  });
  const zuviel = r.unten - r.grenze;
  if (zuviel > 0) {
    drueber++;
    console.log(`  ${id.padEnd(20)} ${zuviel}px ueber den Rand  (Kante ${r.unten} / erlaubt ${r.grenze})`);
  }
}
console.log(drueber
  ? `\n🚨 ${drueber} von ${ids.length} Folien laufen unten raus.`
  : `\nAlle ${ids.length} Folien passen in den Rahmen.`);
await browser.close();
