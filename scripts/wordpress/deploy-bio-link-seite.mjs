/**
 * Deploy der doTERRA-Bio-Link-Seite (Slug /hormone/).
 *
 * Wie bei der Kickstart-LP: Markup ohne <style>/<script> per REST,
 * CSS gescoped raus für den Customizer (die WAF lässt Styles nicht durch).
 * Die Body-Klasse braucht die echte Seiten-ID, die erst beim Anlegen entsteht —
 * deshalb wird der Platzhalter body.page-hormone danach ersetzt.
 *
 * Aufruf:  node --env-file=.env deploy-bio-link-seite.mjs [--publish]
 */
import { readFileSync, writeFileSync } from 'fs';
import { findPageBySlug, createPage, updatePage, getPage } from './wp-api.js';

const SLUG = 'hormone';
const TITEL = 'Hormone & Energie — starte hier';
const SRC = '../../outputs/produkte/doterra-mama-energie/bio-link-seite.html';
const CSS_OUT = '../../outputs/produkte/doterra-mama-energie/bio-link-customizer.css';
const MARKER = '/* === BIO-LINK doTERRA (auto) === */';

const raw = readFileSync(new URL(SRC, import.meta.url), 'utf8');
const body = raw.slice(raw.indexOf('-->') + 3);

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
markup = markup.replace(/<script[\s\S]*?<\/script>/g, '');

const start = markup.indexOf('<div class="ebio">');
const end = markup.lastIndexOf('</div>');
if (start === -1) throw new Error('Wrapper .ebio nicht gefunden');
markup = markup.slice(start, end + 6).trim();

// Seite anlegen oder aktualisieren
let page = await findPageBySlug(SLUG);
const publish = process.argv.includes('--publish');
if (!page) {
  page = await createPage({ title: TITEL, slug: SLUG, content: markup, status: 'draft' });
  console.log('Seite neu angelegt:', page.id);
} else {
  const fields = { content: markup };
  if (publish) fields.status = 'publish';
  await updatePage(page.id, fields);
  console.log('Seite aktualisiert:', page.id);
}
if (publish) await updatePage(page.id, { status: 'publish' });

// CSS mit der echten Seiten-ID
const css =
  MARKER + '\n' +
  cssChunks.join('\n')
    .replace(/@import\s+url\([^)]*\);?/g, '')
    .replace(/body\.page-hormone/g, `body.page-id-${page.id}`)
    .trim() +
  '\n/* === ENDE BIO-LINK doTERRA === */\n';
writeFileSync(new URL(CSS_OUT, import.meta.url), css, 'utf8');

const nach = await getPage(page.id);
console.log('Markup   :', markup.length, 'Zeichen');
console.log('CSS      :', css.length, 'Zeichen →', CSS_OUT);
console.log('Status   :', nach.status);
console.log('Link     :', nach.link);
