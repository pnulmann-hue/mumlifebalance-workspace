// Danke-Seite nach dem Kauf des Tool-Workshops: /tool-workshop-danke/ im ki-salespage-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-tool-workshop-danke.mjs
//
// 1. baut mit scripts/salespage-design/tool-workshop-bauen.py (Inhalt tool-workshop-danke-body.html)
// 2. schreibt die Seite nach WordPress (neue Seite als Entwurf, bestehende behält ihren Status)
// Das CSS kommt aus dem Customizer-Block der Story-Generator-Seite (.sg-sp), nichts nachzutragen.
// Danach in ThriveCart (Produkt 53 und 54) die Erfolgsseite auf diese Adresse umleiten.
import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/tool-workshop/', import.meta.url);
execSync('python scripts/salespage-design/tool-workshop-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const html = readFileSync(new URL('tool-workshop-danke-wp.html', ORDNER), 'utf8');
if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
const felder = {
  title: 'Willkommen im Tool-Workshop', slug: 'tool-workshop-danke',
  content: '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->', template: 'elementor_canvas',
};
const bestehend = await findPageBySlug('tool-workshop-danke');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
