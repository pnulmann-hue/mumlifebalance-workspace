/**
 * Deploy der Energie-Kickstart-Freebie-Landingpage (doTERRA) auf WP-Seite 3911.
 *
 * Die Imunify360-WAF blockt POSTs mit <style>/<script>, deshalb:
 *   - Markup (ohne <style>) geht per REST in die Seite
 *   - CSS wird gescoped rausgeschrieben → Patricia fügt es im Customizer ein
 *   - der AC-Formular-<script> wird zuerst mitversucht, bei 510 ohne
 *
 * Aufruf:  node --env-file=.env deploy-energie-kickstart.mjs [--publish]
 * Ohne --publish bleibt die Seite Entwurf.
 */
import { readFileSync, writeFileSync } from 'fs';
import { getPage, updatePage } from './wp-api.js';

const PAGE_ID = 3911;
const SRC = '../../outputs/produkte/doterra-mama-energie/freebie-seite-energie-kickstart.html';
const CSS_OUT = '../../outputs/produkte/doterra-mama-energie/energie-kickstart-customizer.css';
const MARKER = '/* === ENERGIE-KICKSTART LP (auto) === */';

const raw = readFileSync(new URL(SRC, import.meta.url), 'utf8');

// 1. Doku-Kommentar oben abschneiden — er erwähnt <style>/<script> als TEXT
//    und würde jede Block-Erkennung vergiften.
const body = raw.slice(raw.indexOf('-->') + 3);

// 2. Alle <style>-Blöcke einsammeln und aus dem Markup entfernen.
const cssChunks = [];
let markup = body;
for (;;) {
  const s = markup.indexOf('<style>');
  if (s === -1) break;
  const e = markup.indexOf('</style>', s);
  if (e === -1) break;
  cssChunks.push(markup.slice(s + 7, e));
  markup = markup.slice(0, s) + markup.slice(e + 8);
}

// 3. Den color-scheme-<script> am Anfang entfernen (nur Kosmetik, nicht nötig).
//    Der AC-Formular-<script> bleibt vorerst drin — den brauchen wir für reCAPTCHA.
const firstScript = markup.indexOf('<script>');
const firstScriptEnd = markup.indexOf('</script>', firstScript);
if (firstScript !== -1 && firstScript < markup.indexOf('<div class="ekp">')) {
  markup = markup.slice(0, firstScript) + markup.slice(firstScriptEnd + 9);
}

// 4. Auf den echten Wrapper zuschneiden.
const start = markup.indexOf('<div class="ekp">');
const end = markup.lastIndexOf('</div>');
if (start === -1 || end === -1) throw new Error('Wrapper .ekp nicht gefunden');
markup = markup.slice(start, end + 6).trim();

// 5. CSS zusammenbauen: @import raus (WAF-Trigger + im Customizer ohnehin unerwünscht).
const css =
  MARKER +
  '\n' +
  cssChunks
    .join('\n')
    .replace(/@import\s+url\([^)]*\);?/g, '')
    .replace(/@import[^;]*;/g, '')
    .trim() +
  '\n/* === ENDE ENERGIE-KICKSTART LP === */\n';
writeFileSync(new URL(CSS_OUT, import.meta.url), css, 'utf8');

const withScript = markup;
const withoutScript = markup.replace(/<script[\s\S]*?<\/script>/g, '');

console.log('Markup mit Script  :', withScript.length, 'Zeichen');
console.log('Markup ohne Script :', withoutScript.length, 'Zeichen');
console.log('CSS für Customizer :', css.length, 'Zeichen →', CSS_OUT);
console.log('');

const publish = process.argv.includes('--publish');

async function tryUpdate(content, label) {
  try {
    const fields = { content };
    if (publish) fields.status = 'publish';
    await updatePage(PAGE_ID, fields);
    console.log(`✅ ${label} — durchgekommen`);
    return true;
  } catch (err) {
    console.log(`❌ ${label} — ${String(err.message).slice(0, 160)}`);
    return false;
  }
}

let ok = await tryUpdate(withScript, 'Versuch 1: Markup MIT AC-Script');
if (!ok) ok = await tryUpdate(withoutScript, 'Versuch 2: Markup OHNE Script');

if (ok) {
  const page = await getPage(PAGE_ID);
  console.log('');
  console.log('Status :', page.status);
  console.log('Link   :', page.link);
  console.log('Länge  :', (page.content?.rendered || '').length, 'Zeichen im Frontend-Content');
} else {
  console.log('');
  console.log('Beide Versuche blockiert. Nächster Weg: Elementor-HTML-Widget über den Browser.');
}
