// Anmeldeseite /neustart-2027/ und Danke-Seite /neustart-2027-danke/, Seite nach dem Bestätigungsklick /neustart-2027-bestaetigt/ (Jahresplanungs-Workshop Do 17.12.2026).
//
//   cd scripts/wordpress && node --env-file=.env deploy-jahresplanung-lp.mjs
//
// 1. baut beide Seiten mit scripts/salespage-design/jahresplanung-bauen.py
// 2. schreibt sie nach WordPress (neue Seite als Entwurf, bestehende behält ihren Status)
// CSS: .sg-sp der Story-Generator-Seite liegt schon im Customizer. Der Neujahrs-Effekt
// (outputs/salespages/jahresplanung/neustart-2027-effekt.css) muss als eigener Block
// „NEUSTART-2027-EFFEKT“ in den Customizer, sonst stehen Kalenderblatt und Funken ungestaltet da.
import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/jahresplanung/', import.meta.url);
execSync('python scripts/salespage-design/jahresplanung-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const SEITEN = [
  { datei: 'index-wp.html', slug: 'neustart-2027', title: 'Neustart 2027 — Jahresplanungs-Workshop' },
  { datei: 'danke-wp.html', slug: 'neustart-2027-danke', title: 'Neustart 2027 — fast geschafft' },
  { datei: 'bestaetigt-wp.html', slug: 'neustart-2027-bestaetigt', title: 'Neustart 2027 — du bist dabei' },
];
for (const s of SEITEN) {
  const html = readFileSync(new URL(s.datei, ORDNER), 'utf8');
  if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
  if (html.includes('BILD_HERO_FEHLT')) throw new Error('BILD_WP fehlt in jahresplanung-bauen.py');
  const felder = { title: s.title, slug: s.slug, content: '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->', template: 'elementor_canvas' };
  const bestehend = await findPageBySlug(s.slug);
  const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
  console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', s.slug, seite.id, seite.status, seite.link);
}
