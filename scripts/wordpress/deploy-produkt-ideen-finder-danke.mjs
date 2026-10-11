/**
 * Deploy der Produkt-Ideen-Finder DANKE-/Weiterleitungsseite als WP-Entwurf.
 * Nutzt die .pif-Klassen der Landingpage -> KEIN eigenes CSS noetig
 * (das gleiche Customizer-CSS deckt beide Seiten ab).
 *
 * Aufruf:  node --env-file=.env deploy-produkt-ideen-finder-danke.mjs [--publish]
 */
import { readFileSync } from 'fs';
import { createOrUpdatePage, findPageBySlug } from './wp-api.js';

const SRC = '../../outputs/salespages/produkt-ideen-finder-danke.html';
const SLUG = 'produkt-ideen-finder-los';
const TITLE = 'Produkt-Ideen-Finder — los geht’s';

const raw = readFileSync(new URL(SRC, import.meta.url), 'utf8');
let markup = raw.slice(raw.indexOf('-->') + 3);
const start = markup.indexOf('<div class="pif">');
const end = markup.lastIndexOf('</div>');
if (start === -1 || end === -1) throw new Error('Wrapper .pif nicht gefunden');
markup = markup.slice(start, end + 6).trim();

// Gutenberg-Raw-HTML-Wrapper -> verhindert wpautop, das sonst die <div>-Struktur zerlegt
markup = '<!-- wp:html -->\n' + markup + '\n<!-- /wp:html -->';

console.log('Markup :', markup.length, 'Zeichen');
const publish = process.argv.includes('--publish');
try {
  const existing = await findPageBySlug(SLUG);
  const page = await createOrUpdatePage({ title: TITLE, slug: SLUG, content: markup, status: publish ? 'publish' : 'draft' });
  console.log(existing ? 'Bestehende Seite aktualisiert.' : 'Neue Seite angelegt.');
  console.log('ID     :', page.id);
  console.log('Status :', page.status);
  console.log('Link   :', page.link);
  console.log('Edit   : /wp-admin/post.php?post=' + page.id + '&action=edit');
} catch (err) {
  console.log('FEHLER :', String(err.message).slice(0, 300));
}
