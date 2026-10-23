// AGB-Seite /agb/ auf mumlifebalance.ch — aus dem Entwurf in outputs/sonstige/.
//
//   cd scripts/wordpress && node --env-file=.env deploy-agb.mjs [--vorschau]
//
// Quelle ist der Markdown-Entwurf (Abschnitt „## Allgemeine Geschäftsbedingungen“ bis
// „## Was danach passiert“). Interne Hinweise für die Fachperson (Absätze, die mit ⚠️ **
// beginnen) kommen nicht auf die Seite; kurze ⚠️-Marken im Fliesstext bleiben sichtbar,
// damit niemand eine offene Stelle übersieht.
// 🚨 Neue Seite immer als Entwurf. Eine bestehende behält ihren Status — veröffentlicht
//    wird erst nach der Prüfung, von Patricia selbst.
import { readFileSync, writeFileSync } from 'node:fs';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const QUELLE = new URL('../../outputs/sonstige/2026-10-23-agb-entwurf.md', import.meta.url);
const ZIEL = new URL('../../outputs/sonstige/agb-seite.html', import.meta.url);

const md = readFileSync(QUELLE, 'utf8');
const a = md.indexOf('## Allgemeine Geschäftsbedingungen');
const e = md.indexOf('## Was danach passiert');
if (a < 0 || e < 0) throw new Error('Abschnitt im Entwurf nicht gefunden');
const teil = md.slice(a, e).replace(/\n---\s*$/, '').trim();

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const inline = (s) => esc(s)
  .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  .replace(/\*(.+?)\*/g, '<em>$1</em>')
  .replace(/(https:\/\/mumlifebalance\.ch\/[\w\-/]*)/g, '<a href="$1">$1</a>');

const H2 = 'font-family:Philosopher,Georgia,serif;font-size:24px;color:#0c1c30;margin:34px 0 10px;';
const P = 'font-size:17px;line-height:1.65;color:#0c1c30;margin:0 0 14px;';

// Absätze: Leerzeile trennt, Folgezeilen eines Absatzes werden verbunden
const bloecke = teil.split(/\n\s*\n/).map((b) => b.trim()).filter(Boolean);
const html = [];
for (const b of bloecke) {
  if (b.startsWith('## ')) continue;                       // Titel kommt aus WordPress
  if (b.startsWith('⚠️ **')) continue;                     // interne Notiz für die Fachperson
  if (b.startsWith('### ')) { html.push(`<h2 style="${H2}">${inline(b.slice(4))}</h2>`); continue; }
  if (b.startsWith('- ')) {
    const items = b.split(/\n(?=- )/).map((i) => i.replace(/^- /, '').replace(/\n\s*/g, ' '));
    html.push(`<ul style="${P}padding-left:22px;">` + items.map((i) => `<li style="margin:0 0 8px;">${inline(i)}</li>`).join('') + '</ul>');
    continue;
  }
  html.push(`<p style="${P}">${inline(b.replace(/\n\s*/g, ' '))}</p>`);
}

const inhalt = '<!-- wp:html -->\n<div class="mlb-agb" style="max-width:760px;margin:0 auto;padding:40px 20px;font-family:\'Source Sans 3\',Arial,sans-serif;">\n'
  + html.join('\n') + '\n</div>\n<!-- /wp:html -->';
if (/<style|<script/i.test(inhalt)) throw new Error('<style>/<script> blockt die Firewall');
writeFileSync(ZIEL, inhalt);

const offen = (inhalt.match(/⚠️/g) || []).length;
console.log(`Abschnitte: ${html.filter((h) => h.startsWith('<h2')).length} · offene ⚠️ auf der Seite: ${offen} · ${inhalt.length} Zeichen → ${ZIEL.pathname}`);
if (process.argv.includes('--vorschau')) process.exit(0);

const felder = { title: 'Allgemeine Geschäftsbedingungen', slug: 'agb', content: inhalt };
const da = await findPageBySlug('agb');
const seite = da ? await updatePage(da.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log(`${da ? 'aktualisiert' : 'angelegt'}: ${seite.id} · Status ${seite.status} · ${seite.link}`);
