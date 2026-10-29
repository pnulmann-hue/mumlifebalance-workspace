// Anmeldeseite /nischengenerator/ und Danke-Seite /nischengenerator-danke/ im ki-salespage-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-nischengenerator-lp.mjs
//
// 1. baut beide Seiten mit scripts/salespage-design/nischengenerator-bauen.py
// 2. schreibt sie nach WordPress (neue Seite als Entwurf, bestehende behält ihren Status)
// Das CSS kommt aus dem Customizer-Block der Story-Generator-Seite (.sg-sp), nichts nachzutragen.
import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/nischengenerator/', import.meta.url);
execSync('python scripts/salespage-design/nischengenerator-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const SEITEN = [
  { datei: 'nischengenerator-wp.html', slug: 'nischengenerator', title: 'Nischengenerator — finde dein eigenes Thema' },
  { datei: 'nischengenerator-danke-wp.html', slug: 'nischengenerator-danke', title: 'Nischengenerator — fast geschafft' },
];
for (const s of SEITEN) {
  const html = readFileSync(new URL(s.datei, ORDNER), 'utf8');
  if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
  const felder = { title: s.title, slug: s.slug, content: '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->', template: 'elementor_canvas' };
  const bestehend = await findPageBySlug(s.slug);
  const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
  console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', s.slug, seite.id, seite.status, seite.link);
}
