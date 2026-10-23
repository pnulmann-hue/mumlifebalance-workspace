#!/usr/bin/env node
/**
 * Findet die Folien, auf denen im Praesentationsmodus Text doppelt erscheint.
 *
 *   cd scripts/karussell-render
 *   cp ../ki-kurs/folien-platz-pruefen.mjs ./_p.mjs && node ./_p.mjs <ordner> ...; rm -f ./_p.mjs
 *
 * 🚨 Der Fehler, den Patricia am 20.10.2026 gemeldet hat, sah so aus:
 *
 *      Dein Business, deine Kundin, dein Ton.
 *      Ton.
 *      Ohne das schreibt sie fuer irgendwen.   <- halb verdeckt
 *
 *    Das ist KEIN Umbruch, das sind zwei Fassungen uebereinander. Die Folie
 *    wird zuerst mit der Ersatzschrift gezeichnet — da passt der Satz in EINE
 *    Zeile. Dann laedt Philosopher nach, ist breiter, braucht ZWEI Zeilen,
 *    aber der Kasten behaelt die Hoehe von einer. Der Rest laeuft heraus und
 *    legt sich ueber den naechsten Block. Dieselbe Ursache zerreisst die
 *    Buchstabenabstaende in der Ueberschrift.
 *
 * 🚨 Es ist ein WETTLAUF: beim ersten Oeffnen kaputt, nach dem Neuladen
 *    (Schrift im Cache) sauber. Wer nur einmal hinschaut, sieht es nie.
 *
 * Gefaehrlich ist deshalb nicht „bricht um“, sondern „bricht UNTERSCHIEDLICH
 * um“ — ein Block, der mit der einen Schrift eine Zeile braucht und mit der
 * anderen zwei. Genau das misst dieses Skript: jede Folie zweimal, und
 * gemeldet wird nur, wo die Zeilenzahl kippt.
 *
 * Ein Block, der in BEIDEN Schriften gleich viele Zeilen hat, ist sicher —
 * auch wenn er dreizeilig ist.
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';

const HREF = 'https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700' +
             '&family=Source+Sans+3:wght@300;400;600;700&display=swap';

const ordner = process.argv.slice(2);
if (!ordner.length) {
  console.error('Aufruf: node folien-platz-pruefen.mjs <ordner mit project/slides> ...');
  process.exit(1);
}

// Im Browser: je Textblock die Zeilenzahl und ob er der letzte in seinem Kasten ist.
function zeilen() {
  const sec = document.querySelector('section');
  if (!sec) return [];
  const raus = [];
  for (const el of sec.querySelectorAll('h1, h2, h3, p, li')) {
    const r = el.getBoundingClientRect();
    if (!r.height) continue;
    const zh = parseFloat(getComputedStyle(el).lineHeight) || r.height;
    // Wie viel Luft ist bis zu dem, was darunter steht? Ein Block, unter dem
    // ein Abstandshalter sitzt (Cover: flex:1 vor der Fusszeile), kann eine
    // Zeile mehr vertragen, ohne irgendetwas zu verdecken. Ohne diese Messung
    // meldet der Pruefer genau diese Faelle — und nach dem dritten Fehlalarm
    // liest niemand mehr hin.
    let luft = Infinity;
    const naechste = [...el.parentElement.children];
    const i = naechste.indexOf(el);
    for (let j = i + 1; j < naechste.length; j++) {
      const n = naechste[j].getBoundingClientRect();
      if (!n.height) continue;
      if (n.left >= r.right - 2 || r.left >= n.right - 2) continue;  // steht daneben
      // 🚨 Leere Elemente ueberspringen. Auf dem Cover klebt ein
      // <div style="flex:1"> direkt unter dem Text und schiebt die Fusszeile
      // nach unten. Gemessen waeren das null Pixel Luft — verdeckt wird aber
      // nichts, weil dort kein Text steht.
      if (!(naechste[j].textContent || '').trim()) continue;
      luft = n.top - r.bottom;
      break;
    }
    const geschwister = [...el.parentElement.children]
      .filter(k => /^(P|LI|H1|H2|H3)$/.test(k.tagName));
    raus.push({
      text: (el.textContent || '').replace(/\s+/g, ' ').trim(),
      n: Math.max(1, Math.round(r.height / zh)),
      letzter: geschwister[geschwister.length - 1] === el,
      luft, zh,
    });
  }
  return raus;
}

const browser = await puppeteer.launch({ headless: 'new' });

async function lauf(mitSchrift) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  if (!mitSchrift) {
    await page.setRequestInterception(true);
    page.on('request', r => /fonts\.(googleapis|gstatic)/.test(r.url())
      ? r.abort() : r.continue());
  }
  const alles = new Map();
  for (const o of ordner) {
    const verz = path.join(o, 'project', 'slides');
    let dateien;
    try { dateien = (await fs.readdir(verz)).filter(f => f.endsWith('.html')).sort(); }
    catch { continue; }
    const name = path.basename(o.replace(/[\\/]$/, ''));
    for (const d of dateien) {
      const roh = await fs.readFile(path.join(verz, d), 'utf8');
      await page.setContent(
        '<!doctype html><html><head><meta charset="utf-8">' +
        '<link rel="stylesheet" href="' + HREF + '">' +
        '<style>html,body{margin:0;padding:0}' +
        'section{width:1920px;height:1080px;box-sizing:border-box}</style>' +
        '</head><body>' + roh + '</body></html>',
        { waitUntil: mitSchrift ? 'networkidle0' : 'domcontentloaded' });
      if (mitSchrift) { try { await page.evaluate(() => document.fonts.ready); } catch {} }
      alles.set(name + '/' + d.replace(/\.html$/, ''), await page.evaluate(zeilen));
    }
  }
  await page.close();
  return alles;
}

const mit  = await lauf(true);
const ohne = await lauf(false);
await browser.close();

let wackelt = 0, harmlos = 0;
console.log('\n🚨 Blöcke, deren Zeilenzahl zwischen den Schriften kippt');
console.log('   (die können im Präsentationsmodus doppelt erscheinen)\n');

for (const [folie, a] of mit) {
  const b = ohne.get(folie) || [];
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i].n === b[i].n) continue;
    // Zwei Bedingungen muessen zusammenkommen, sonst meldet der Pruefer zu viel:
    //
    //   1 · Der Block ist NICHT der letzte in seinem Kasten. Nur dann steht
    //       ueberhaupt etwas darunter, das verdeckt werden kann. (Im Browser
    //       schiebt Flexbox den naechsten Block weg — in PowerPoint sitzt
    //       jede Textbox fest, und genau dort entsteht der Fehler.)
    //
    //   2 · Darunter ist kein Abstandshalter. 🚨 Die Luft im Browser sagt
    //       NICHTS ueber PowerPoint — dort sitzt jede Textbox fest, egal wie
    //       viel Platz das HTML laesst. Auf Patricias kaputter Folie waren im
    //       Browser 70 px Luft, und sie hat trotzdem ueberlappt. Deshalb ist
    //       die Schwelle grosszuegig: sie soll nur die Faelle wegnehmen, in
    //       denen wirklich ein Abstandshalter folgt (Cover: flex:1 vor der
    //       Fusszeile, mehrere hundert Pixel), nicht die engen in den Karten.
    //
    // Nur die erste Bedingung meldete das Cover als Fehlalarm, nur die zweite
    // liess Patricias echten Fehler durch. Beide zusammen treffen es.
    const zusatz = (Math.max(a[i].n, b[i].n) - Math.min(a[i].n, b[i].n)) * a[i].zh;
    const luft = Math.min(a[i].luft, b[i].luft);
    const schlimm = !a[i].letzter && luft < zusatz * 4;
    if (schlimm) wackelt++; else harmlos++;
    if (!schlimm) continue;
    console.log('  ' + folie.padEnd(24) +
                b[i].n + ' Zeile(n) ohne Schrift → ' + a[i].n + ' mit Schrift');
    console.log('    „' + a[i].text.slice(0, 74) + '“');
  }
}

console.log('\n  ' + wackelt + ' Stellen, an denen Text über den nächsten Block laufen kann.');
console.log('  ' + harmlos + ' weitere kippen auch, haben aber genug Platz darunter —');
console.log('  die rutschen höchstens etwas tiefer und überdecken nichts.');
console.log('\n  Behoben ist eine Stelle, wenn der Text in BEIDEN Schriften gleich');
console.log('  viele Zeilen braucht. Kürzen hilft nur, wenn es unter die Grenze fällt.');
