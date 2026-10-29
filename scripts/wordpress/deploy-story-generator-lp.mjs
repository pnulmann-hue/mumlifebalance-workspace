// Story-Generator-Verkaufsseite /story-generator/ im ki-salespage-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-story-generator-lp.mjs
//
// 1. baut mit scripts/salespage-design/story-generator-bauen.py Inhalt + CSS
// 2. schreibt den Inhalt in die Seite (neue Seite als Entwurf, bestehende behält ihren Status)
// 🚨 Das CSS (outputs/salespages/story-generator/story-generator.css) gehört in den Customizer —
//    die Firewall lässt kein <style> in die Seite.
import { readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/story-generator/', import.meta.url);
execSync('python scripts/salespage-design/story-generator-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const html = readFileSync(new URL('story-generator-wp.html', ORDNER), 'utf8');
if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
const inhalt = '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->';
const felder = { title: 'Story-Generator — aus deinem Alltag wird eine Story', slug: 'story-generator', content: inhalt, template: 'elementor_canvas' };
const bestehend = await findPageBySlug('story-generator');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
