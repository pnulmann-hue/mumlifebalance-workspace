// Zwei echte Bildschirme des Nischengenerators fürs Hero-Bild der Anmeldeseite.
// Schritt 1 so, wie ihn jede sieht; das Ergebnis mit der erfundenen Beispiel-Person Sandra
// (Energie für Mamas ab 35), über die Anzeige-Funktion des Tools selbst. Kein KI-Aufruf, keine Mail an AC.
//
//   node scripts/salespage-design/nischengenerator-bildschirme.mjs
// -> outputs/salespages/nischengenerator/bild/schirm-frage.png · schirm-ergebnis.png
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');
const ZIEL = fileURLToPath(new URL('../../outputs/salespages/nischengenerator/bild/', import.meta.url));

const SANDRA = {
  spiegel: 'Du hast deinen eigenen Nachmittag zurückgeholt, und genau danach fragen dich die anderen Mamas.',
  rest: 9, max: 10,
  themen: [{
    titel: 'Energie für Mamas ab 35', themenfeld: 'Alltag & Energie',
    satz: 'Ich helfe Mamas ab 35 dabei, mit kleinen Routinen wieder Kraft für den Nachmittag zu haben, damit der Feierabend wieder ihnen gehört.',
    warum: 'Du hast es selbst erlebt und kannst zeigen, was bei dir heute funktioniert.',
    abhebung: 'Du redest aus dem Alltag mit Kindern, nicht aus dem Lehrbuch.',
    produkt: 'Deine Öle sind ein Zimmer im Haus: Teil deiner Routine, nicht ihr Fundament.',
    beitraege: ['Mein Nachmittag vor einem Jahr', 'Drei Minuten, die meinen Tag tragen'],
    tool: 'Ein Energie-Check für den Familienalltag',
  }],
};

const browser = await puppeteer.launch({ headless: 'new' });
const s = await browser.newPage();
await s.setViewport({ width: 390, height: 780, deviceScaleFactor: 2 });
await s.goto('https://mlb-nischengenerator.vercel.app/', { waitUntil: 'networkidle0' });
await s.evaluate(() => document.fonts.ready);
await s.screenshot({ path: ZIEL + 'schirm-frage.png' });
await s.evaluate((j) => zeigeThemen(j), SANDRA);
await s.evaluate(() => { document.querySelector('.ergebnis').scrollIntoView(); window.scrollBy(0, -10); });
await new Promise(r => setTimeout(r, 400));
await s.screenshot({ path: ZIEL + 'schirm-ergebnis.png' });
await browser.close();
console.log('->', ZIEL);
