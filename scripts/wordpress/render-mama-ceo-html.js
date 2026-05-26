// Render-Only-Variante von deploy-mama-ceo.js
// Generiert den fertigen HTML-Block (CSS minified + Template-Vars resolved)
// für manuelles Reinkopieren in WP-Admin → Code Editor.
// Kein WordPress-Push, keine Credentials nötig.
//
// Ausführen: cd scripts/wordpress && node render-mama-ceo-html.js
// Output:    outputs/wp-snippets/mama-ceo.html

import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DEPLOY_SCRIPT = resolve(__dirname, 'deploy-mama-ceo.js');
const OUT_DIR = resolve(__dirname, '../../outputs/wp-snippets');
const OUT_FILE = resolve(OUT_DIR, 'mama-ceo.html');

// deploy-mama-ceo.js als Text einlesen und content + minify-Logik daraus extrahieren
const src = readFileSync(DEPLOY_SCRIPT, 'utf8');

// Konstanten aus dem Source ziehen
function pickConst(name) {
  const re = new RegExp(`const ${name}\\s*=\\s*['\\\`]([^'\\\`]+)['\\\`]`);
  const m = src.match(re);
  if (!m) throw new Error(`Konstante ${name} nicht gefunden in deploy-mama-ceo.js`);
  return m[1];
}

const CTA_URL = pickConst('CTA_URL');
const HERO_PHOTO = pickConst('HERO_PHOTO');
const STORY_PHOTO = HERO_PHOTO;

// BRAND_CSS-Block extrahieren (zwischen const BRAND_CSS = ` und `;)
const cssMatch = src.match(/const BRAND_CSS\s*=\s*`([\s\S]*?)`;/);
if (!cssMatch) throw new Error('BRAND_CSS-Block nicht gefunden');
const brandCssRaw = cssMatch[1]
  .replaceAll('${HERO_PHOTO}', HERO_PHOTO)
  .replaceAll('${STORY_PHOTO}', STORY_PHOTO);

// content-Block extrahieren (zwischen const content = ` und `;)
const contentMatch = src.match(/const content\s*=\s*`([\s\S]*?)`;\s*\n/);
if (!contentMatch) throw new Error('content-Block nicht gefunden');
const contentRaw = contentMatch[1]
  .replaceAll('${BRAND_CSS}', brandCssRaw)
  .replaceAll('${CTA_URL}', CTA_URL)
  .replaceAll('${HERO_PHOTO}', HERO_PHOTO)
  .replaceAll('${STORY_PHOTO}', STORY_PHOTO);

// CSS minifizieren (wpautop-Schutz — identisch zu deploy-mama-ceo.js)
const fixed = contentRaw.replace(/<style>([\s\S]*?)<\/style>/g, (match, css) => {
  const minified = css
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\s+/g, ' ')
    .replace(/\s*([{};:,>~+])\s*/g, '$1')
    .trim();
  return '<style>' + minified + '</style>';
});

mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(OUT_FILE, fixed.trim() + '\n', 'utf8');

console.log('✅ HTML-Block geschrieben:');
console.log(`   ${OUT_FILE}`);
console.log(`   ${fixed.length.toLocaleString('de-CH')} Zeichen`);
console.log('\n📝 Patricia: Datei öffnen → alles markieren (Cmd+A) → kopieren (Cmd+C)');
console.log('   → WP-Admin → Mama-CEO → 3-Punkte-Menü → "Code editor"');
console.log('   → alten Code ersetzen → "Aktualisieren"');
