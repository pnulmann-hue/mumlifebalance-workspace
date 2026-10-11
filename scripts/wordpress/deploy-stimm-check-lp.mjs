// Stimm-Check-Landingpage /stimm-check/ im Minikurs-Baukasten.
//
//   cd scripts/wordpress && node --env-file=.env deploy-stimm-check-lp.mjs
//
// 1. lädt fehlende Bilder hoch und merkt sich die Adressen in medien.json
// 2. baut mit scripts/salespage-design/stimm-check-bauen.py Inhalt + CSS
// 3. schreibt den Inhalt in die Seite (bestehende Seite behält ihren Status)
// 🚨 Das CSS (outputs/salespages/stimm-check/stimm-check.css) gehört in den Customizer —
//    die Firewall lässt kein <style> in die Seite.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { uploadMedia, findPageBySlug, updatePage, createPage } from './wp-api.js';

const ORDNER = new URL('../../outputs/salespages/stimm-check/', import.meta.url);
const MEDIEN = new URL('medien.json', ORDNER);
const medien = existsSync(MEDIEN) ? JSON.parse(readFileSync(MEDIEN, 'utf8')) : {};

for (const datei of ['stimm-ergebnis.png']) {
  if (medien[datei]) continue;
  const m = await uploadMedia(fileURLToPath(new URL('assets/' + datei, ORDNER)),
    { title: 'Stimm-Check Ergebnis', altText: 'So sieht dein Ergebnis im Stimm-Check aus' });
  medien[datei] = m.source_url;
  console.log('hochgeladen:', datei, m.source_url);
}
writeFileSync(MEDIEN, JSON.stringify(medien, null, 1));

execSync('python scripts/salespage-design/stimm-check-bauen.py', { cwd: fileURLToPath(new URL('../../', import.meta.url)), stdio: 'inherit' });

const html = readFileSync(new URL('stimm-check-wp.html', ORDNER), 'utf8');
if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
const inhalt = '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->';
const felder = { title: 'Der Stimm-Check', slug: 'stimm-check', content: inhalt, template: 'elementor_canvas' };
const bestehend = await findPageBySlug('stimm-check');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
