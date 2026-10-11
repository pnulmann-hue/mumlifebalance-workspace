/**
 * Deploy der Produkt-Ideen-Finder-Freebie-Landingpage (Mentoring) als WP-Entwurf.
 * WAF-safe: Markup (ohne <style>) geht per REST rein, das CSS wird gescoped
 * rausgeschrieben -> Patricia fuegt es im Customizer ein.
 *
 * Aufruf:  node --env-file=.env deploy-produkt-ideen-finder.mjs [--publish]
 * Ohne --publish bleibt die Seite Entwurf.
 */
import { readFileSync, writeFileSync } from 'fs';
import { createOrUpdatePage, findPageBySlug } from './wp-api.js';

const SRC = '../../outputs/salespages/produkt-ideen-finder-landingpage.html';
const CSS_OUT = '../../outputs/salespages/produkt-ideen-finder-customizer.css';
const SLUG = 'produkt-ideen-finder';
const TITLE = 'Produkt-Ideen-Finder';
const MARKER = '/* === PRODUKT-IDEEN-FINDER LP (auto) === */';

const raw = readFileSync(new URL(SRC, import.meta.url), 'utf8');
const body = raw.slice(raw.indexOf('-->') + 3);

// <style>-Bloecke einsammeln + aus dem Markup entfernen
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

// auf den .pif-Wrapper zuschneiden
const start = markup.indexOf('<div class="pif">');
const end = markup.lastIndexOf('</div>');
if (start === -1 || end === -1) throw new Error('Wrapper .pif nicht gefunden');
markup = markup.slice(start, end + 6).trim();

// Gutenberg-Raw-HTML-Wrapper -> verhindert wpautop, das sonst die <div>-Struktur zerlegt
markup = '<!-- wp:html -->\n' + markup + '\n<!-- /wp:html -->';

const css =
  MARKER + '\n' +
  cssChunks.join('\n').replace(/@import\s+url\([^)]*\);?/g, '').replace(/@import[^;]*;/g, '').trim() +
  '\n/* === ENDE PRODUKT-IDEEN-FINDER LP === */\n';
writeFileSync(new URL(CSS_OUT, import.meta.url), css, 'utf8');

console.log('Markup :', markup.length, 'Zeichen');
console.log('CSS    :', css.length, 'Zeichen ->', CSS_OUT);
console.log('');

const publish = process.argv.includes('--publish');
try {
  const existing = await findPageBySlug(SLUG);
  const page = await createOrUpdatePage({
    title: TITLE,
    slug: SLUG,
    content: markup,
    status: publish ? 'publish' : 'draft',
  });
  console.log(existing ? 'Bestehende Seite aktualisiert.' : 'Neue Seite angelegt.');
  console.log('ID     :', page.id);
  console.log('Status :', page.status);
  console.log('Link   :', page.link);
  console.log('Edit   : /wp-admin/post.php?post=' + page.id + '&action=edit');
} catch (err) {
  console.log('FEHLER :', String(err.message).slice(0, 300));
}
