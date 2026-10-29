// Anmeldeseite Tool-Workshop /tool-workshop/ im ki-salespage-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-tool-workshop-lp.mjs
//
// 1. baut mit scripts/salespage-design/tool-workshop-bauen.py den Inhalt
// 2. schreibt ihn in die Seite (neue Seite als Entwurf, bestehende behält ihren Status)
// Das CSS kommt aus dem Customizer-Block der Story-Generator-Seite (.sg-sp), nichts nachzutragen.
import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/tool-workshop/', import.meta.url);
execSync('python scripts/salespage-design/tool-workshop-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const html = readFileSync(new URL('tool-workshop-wp.html', ORDNER), 'utf8');
if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
const inhalt = '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->';
const felder = { title: 'Tool-Workshop — dein Gratis-Tool, das dir neue Kontakte bringt', slug: 'tool-workshop', content: inhalt, template: 'elementor_canvas' };
const bestehend = await findPageBySlug('tool-workshop');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
