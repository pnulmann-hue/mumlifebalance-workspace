#!/usr/bin/env node
/**
 * Baut die Kurs-Beilagen als A4-PDF in Patricias Branding.
 *
 *   node scripts/ki-treppe/beilagen-bauen.mjs [teilname ...]
 *
 * Quelle: outputs/produkte/ki-treppe/beilagen/*.md
 * Ziel:   outputs/produkte/ki-treppe/beilagen/pdf/*.pdf
 *
 * Sprache: echte Umlaute, Schweizer ss. Das Skript prueft das am Ende und
 * meldet jeden umschriebenen Umlaut — genau dieser Fehler ist am 18.09. bei den
 * Startklar-Mails bis in den Kundentext durchgerutscht.
 *
 * Puppeteer liegt in scripts/karussell-render/node_modules — das Skript wird
 * von dort aus aufgerufen (siehe README).
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const QUELLE = path.join(ROOT, 'outputs', 'produkte', 'ki-treppe', 'beilagen');
const ZIEL = path.join(QUELLE, 'pdf');

const F = { creme: '#f1ecdd', petrol: '#12828c', blau: '#0c1c30',
            tief: '#29556d', orange: '#dc822e' };

const esc = s => String(s ?? '')
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Fett, kursiv und Code innerhalb einer Zeile
function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[\s(])\*([^*]+)\*(?=[\s).,;:!?]|$)/g, '$1<em>$2</em>');
}

/** Markdown der Beilagen -> HTML. Deckt ab, was wirklich vorkommt:
 *  Ueberschriften, Absaetze, Listen, Haekchen-Listen, Zitate, Trenner,
 *  Tabellen und Code-Bloecke. */
function markdown(md) {
  const zeilen = md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').split(/\r?\n/);
  const raus = [];
  let absatz = [], liste = null, zitat = [], code = null, tabelle = null;

  const absatzZu = () => {
    if (absatz.length) { raus.push('<p>' + inline(absatz.join(' ')) + '</p>'); absatz = []; }
  };
  const listeZu = () => {
    if (liste) { raus.push('<ul class="' + liste.art + '">' + liste.punkte.join('') + '</ul>'); liste = null; }
  };
  const zitatZu = () => {
    if (zitat.length) { raus.push('<blockquote>' + inline(zitat.join(' ')) + '</blockquote>'); zitat = []; }
  };
  const tabelleZu = () => {
    if (!tabelle) return;
    const kopf = tabelle[0], rest = tabelle.slice(1);
    raus.push('<table><thead><tr>' +
      kopf.map(z => '<th>' + inline(z) + '</th>').join('') +
      '</tr></thead><tbody>' +
      rest.map(r => '<tr>' + r.map(z => '<td>' + inline(z) + '</td>').join('') + '</tr>').join('') +
      '</tbody></table>');
    tabelle = null;
  };
  const allesZu = () => { absatzZu(); listeZu(); zitatZu(); tabelleZu(); };

  for (const zeile of zeilen) {
    if (code !== null) {
      if (/^```/.test(zeile)) { raus.push('<pre>' + esc(code.join('\n')) + '</pre>'); code = null; }
      else code.push(zeile);
      continue;
    }
    if (/^```/.test(zeile)) { allesZu(); code = []; continue; }

    const t = zeile.trim();
    if (!t) { allesZu(); continue; }
    if (/^---+$/.test(t)) { allesZu(); raus.push('<hr>'); continue; }

    const ueber = t.match(/^(#{1,4})\s+(.*)$/);
    if (ueber) {
      allesZu();
      const n = ueber[1].length;
      raus.push('<h' + n + '>' + inline(ueber[2]) + '</h' + n + '>');
      continue;
    }

    if (/^\|/.test(t)) {
      absatzZu(); listeZu(); zitatZu();
      const felder = t.replace(/^\||\|$/g, '').split('|').map(x => x.trim());
      if (felder.every(x => /^:?-{2,}:?$/.test(x))) continue;   // Trennzeile
      (tabelle = tabelle || []).push(felder);
      continue;
    }
    tabelleZu();

    if (/^>\s?/.test(t)) { absatzZu(); listeZu(); zitat.push(t.replace(/^>\s?/, '')); continue; }
    zitatZu();

    const haken = t.match(/^[-*]\s+\[([ xX])\]\s+(.*)$/);
    if (haken) {
      absatzZu();
      if (!liste || liste.art !== 'haken') { listeZu(); liste = { art: 'haken', punkte: [] }; }
      liste.punkte.push('<li><span class="kasten"></span>' + inline(haken[2]) + '</li>');
      continue;
    }
    const punkt = t.match(/^[-*]\s+(.*)$/);
    if (punkt) {
      absatzZu();
      if (!liste || liste.art !== 'punkte') { listeZu(); liste = { art: 'punkte', punkte: [] }; }
      liste.punkte.push('<li>' + inline(punkt[1]) + '</li>');
      continue;
    }
    listeZu();
    absatz.push(t);
  }
  allesZu();
  return raus.join('\n');
}

const CSS = [
  '@page { size: A4; margin: 17mm 16mm 20mm; }',
  '* { box-sizing: border-box; }',
  'body { margin: 0; background: #fff; color: ' + F.blau + ';',
  "  font-family: 'Source Sans 3', sans-serif; font-size: 11.4pt; line-height: 1.58; }",
  '.kopf { border-bottom: 3px solid ' + F.orange + '; padding-bottom: 9px; margin-bottom: 22px;',
  '  display: flex; align-items: baseline; gap: 10px; }',
  ".kopf .marke { font-family: 'Philosopher', serif; font-size: 13pt; color: " + F.petrol + '; }',
  '.kopf .reihe { font-size: 8.6pt; letter-spacing: .14em; text-transform: uppercase;',
  '  color: ' + F.tief + '; opacity: .75; margin-left: auto; }',
  "h1 { font-family: 'Philosopher', serif; font-size: 25pt; line-height: 1.16;",
  '  color: ' + F.blau + '; margin: 0 0 14px; font-weight: 700; }',
  "h2 { font-family: 'Philosopher', serif; font-size: 16pt; color: " + F.petrol + ';',
  '  margin: 26px 0 8px; font-weight: 700; break-after: avoid; }',
  "h3 { font-family: 'Philosopher', serif; font-size: 13pt; color: " + F.tief + ';',
  '  margin: 18px 0 6px; font-weight: 700; break-after: avoid; }',
  'h4 { font-size: 11.4pt; color: ' + F.tief + '; margin: 14px 0 4px; break-after: avoid; }',
  'p { margin: 0 0 10px; }',
  'strong { color: ' + F.blau + '; font-weight: 600; }',
  "code { font-family: 'Source Sans 3', monospace; background: " + F.creme + ';',
  '  border-radius: 4px; padding: 1px 5px; font-size: 10.4pt; }',
  'pre { background: ' + F.creme + '; border-left: 3px solid ' + F.petrol + ';',
  '  border-radius: 0 7px 7px 0; padding: 11px 14px; font-size: 10pt; line-height: 1.5;',
  '  white-space: pre-wrap; overflow-wrap: anywhere; margin: 0 0 12px; }',
  'hr { border: 0; border-top: 1px solid rgba(12,28,48,.14); margin: 20px 0; }',
  'ul { margin: 0 0 12px; padding-left: 0; list-style: none; }',
  'ul.punkte li { position: relative; padding-left: 19px; margin-bottom: 5px; }',
  'ul.punkte li::before { content: ""; position: absolute; left: 3px; top: .62em;',
  '  width: 6px; height: 6px; border-radius: 50%; background: ' + F.orange + '; }',
  'ul.haken li { position: relative; padding-left: 30px; margin-bottom: 9px; break-inside: avoid; }',
  'ul.haken .kasten { position: absolute; left: 0; top: .18em; width: 15px; height: 15px;',
  '  border: 1.8px solid ' + F.petrol + '; border-radius: 4px; }',
  'blockquote { background: ' + F.creme + '; border-left: 3px solid ' + F.orange + ';',
  '  border-radius: 0 8px 8px 0; padding: 12px 15px; margin: 0 0 14px; break-inside: avoid; }',
  'blockquote p:last-child { margin-bottom: 0; }',
  'table { width: 100%; border-collapse: collapse; margin: 0 0 14px; font-size: 10.6pt; }',
  'th { text-align: left; background: ' + F.petrol + '; color: #fff; font-weight: 600; padding: 7px 10px; }',
  'td { padding: 7px 10px; border-bottom: 1px solid rgba(12,28,48,.12); vertical-align: top; }',
  'tr:nth-child(even) td { background: rgba(241,236,221,.5); }',
  '.fuss { margin-top: 26px; padding-top: 9px; border-top: 1px solid rgba(12,28,48,.14);',
  '  font-size: 8.8pt; color: ' + F.tief + '; opacity: .8; }'
].join('\n');

function seite(inhalt) {
  return '<!doctype html><html lang="de"><head><meta charset="utf-8">' +
    '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700' +
    '&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">' +
    '<style>' + CSS + '</style></head><body>' +
    '<div class="kopf"><span class="marke">Mum Life Balance</span>' +
    '<span class="reihe">Deine KI-Mitarbeiterin</span></div>' +
    inhalt +
    '<div class="fuss">Patricia Ulmann · mumlifebalance.ch — für Teilnehmerinnen ' +
    'des Kurses. Bitte nicht weitergeben.</div></body></html>';
}

/** Umschriebene Umlaute und scharfes s im sichtbaren Text. Echte ae/oe/ue-Woerter
 *  stehen in der Ausnahmeliste — nach dem dritten Fehlalarm liest niemand mehr hin. */
const ERLAUBT = new Set(['bauen', 'dauert', 'frauen', 'heute', 'zuerst', 'abenteuer',
  'neues', 'neue', 'genauso', 'genau', 'draussen', 'aussen', 'aufbauen', 'blauen',
  'vertrauen', 'zutrauen', 'schauen', 'pause', 'pausen', 'auge', 'augen', 'laufen',
  'kaufen', 'glauben', 'erlauben', 'brauchen', 'gebrauch', 'hausaufgaben']);
const VERDACHT = /(haett|koenn|muess|fuer|ueber|waer|groess|schoen|moeg|hoer|spaet|naech|zurueck|aender|waehl|taeg|jaehr|laeuft|haeng|erklaer|gehoer|loes|stueck|fuenf|zwoelf|ueb|maess|gemaess|zaehl|faell|haelt)/;

function sprachPruefung(text) {
  const raus = [];
  for (const w of text.match(/\b[A-Za-zÄÖÜäöüß]+\b/g) || []) {
    const k = w.toLowerCase();
    if (/ß/.test(w)) { raus.push(w + ' (scharfes s)'); continue; }
    if (ERLAUBT.has(k)) continue;
    if (/(ae|oe|ue)/.test(k) && VERDACHT.test(k)) raus.push(w + ' (umschriebener Umlaut)');
  }
  return [...new Set(raus)];
}

const nur = process.argv.slice(2);
await fs.mkdir(ZIEL, { recursive: true });
const dateien = (await fs.readdir(QUELLE))
  .filter(f => f.endsWith('.md'))
  .filter(f => !nur.length || nur.some(n => f.includes(n)))
  .sort();

if (!dateien.length) { console.error('Keine Beilagen gefunden.'); process.exit(1); }

const browser = await puppeteer.launch({ headless: 'new' });
const page = await browser.newPage();
let warnungen = 0;

for (const datei of dateien) {
  const md = await fs.readFile(path.join(QUELLE, datei), 'utf8');
  const inhalt = markdown(md);

  const funde = sprachPruefung(md.replace(/^---[\s\S]*?---/, ''));
  if (funde.length) { warnungen++; console.log('  ACHTUNG ' + datei + ': ' + funde.join(' · ')); }

  const htmlPfad = path.join(ZIEL, datei.replace(/\.md$/, '.html'));
  await fs.writeFile(htmlPfad, seite(inhalt), 'utf8');
  await page.goto(pathToFileURL(htmlPfad).href, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  const pdfPfad = path.join(ZIEL, datei.replace(/\.md$/, '.pdf'));
  await page.pdf({ path: pdfPfad, format: 'A4', printBackground: true });
  const gr = (await fs.stat(pdfPfad)).size;
  console.log('  ' + datei.replace(/\.md$/, '.pdf').padEnd(34) +
              String(Math.round(gr / 1024)).padStart(4) + ' KB');
}

await browser.close();
console.log('\n' + dateien.length + ' Beilagen -> ' + path.relative(ROOT, ZIEL));
console.log(warnungen
  ? 'ACHTUNG: ' + warnungen + ' Datei(en) mit Sprachfund — oben nachsehen und korrigieren.'
  : 'Sprachpruefung: echte Umlaute, kein scharfes s. In Ordnung.');
