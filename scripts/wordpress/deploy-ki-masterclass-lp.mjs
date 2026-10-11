// KI-Masterclass-Anmeldeseite /ki-masterclass/ im ki-salespage-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-ki-masterclass-lp.mjs
//
// 1. lädt fehlende Bilder hoch und merkt sich die Adressen in medien.json
// 2. baut mit scripts/salespage-design/ki-masterclass-bauen.py Inhalt + CSS
// 3. schreibt den Inhalt in die Seite (bestehende Seite behält ihren Status)
// 🚨 Das CSS (outputs/salespages/ki-masterclass/ki-masterclass.css) gehört in den Customizer —
//    die Firewall lässt kein <style> in die Seite.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { uploadMedia, findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/ki-masterclass/', import.meta.url);
const MEDIEN = new URL('medien.json', ORDNER);
const medien = existsSync(MEDIEN) ? JSON.parse(readFileSync(MEDIEN, 'utf8')) : {};

const BILDER = {
  'km-hero.jpg': { title: 'KI-Masterclass Hero', altText: 'Patricia im orangen Kleid am See' },
  'km-about.jpg': { title: 'KI-Masterclass Über mich', altText: 'Patricia lachend am See mit einer Mappe' },
};
for (const [datei, info] of Object.entries(BILDER)) {
  if (medien[datei]) continue;
  const m = await uploadMedia(fileURLToPath(new URL('assets/' + datei, ORDNER)), info);
  medien[datei] = m.source_url;
  console.log('hochgeladen:', datei, m.source_url);
}
writeFileSync(MEDIEN, JSON.stringify(medien, null, 1));

execSync('python scripts/salespage-design/ki-masterclass-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const html = readFileSync(new URL('ki-masterclass-wp.html', ORDNER), 'utf8');
if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
const inhalt = '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->';
const felder = { title: 'KI-Masterclass — Vom Chat zur Mitarbeiterin', slug: 'ki-masterclass', content: inhalt, template: 'elementor_canvas' };
const bestehend = await findPageBySlug('ki-masterclass');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
