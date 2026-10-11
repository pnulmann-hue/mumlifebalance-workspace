// Deployt die Magnet-Ich-Onboarding-Seite (mumlifebalance.ch/magnet-ich-onboarding).
// Quelle: outputs/produkte/magnet-ich/onboarding-seite.html (reines Markup, kein <style>/<script> — WAF)
// CSS: outputs/produkte/magnet-ich/onboarding-customizer.css -> von Patricia in den Customizer
// Formular: AC-iframe /f/<FORM_ID>. Aufruf: node --env-file=.env deploy-magnet-ich-onboarding.mjs [FORM_ID]
// Neue Seite als ENTWURF; eine bestehende behaelt ihren Status.
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { findPageBySlug, createPage, updatePage } from './wp-api.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(__dirname, '../../outputs/produkte/magnet-ich/onboarding-seite.html');
const formId = process.argv[2] || 'FORM_ID';

let html = readFileSync(SRC, 'utf8');
if (!html.includes('/f/FORM_ID')) throw new Error('Platzhalter /f/FORM_ID fehlt in der Quelle');
html = html.replace('/f/FORM_ID', `/f/${formId}`);
if (/<style|<script/i.test(html)) throw new Error('Quelle enthaelt <style> oder <script> — die WAF blockt das');

const content = `<!-- wp:html -->\n${html.trim()}\n<!-- /wp:html -->`;
const slug = 'magnet-ich-onboarding';
const title = 'Magnet-Ich — dein Onboarding';
let page = await findPageBySlug(slug);
if (page) {
  page = await updatePage(page.id, { title, content });
  console.log(`Aktualisiert #${page.id} (Status bleibt ${page.status})`);
} else {
  page = await createPage({ slug, title, content, status: 'draft' });
  await updatePage(page.id, { template: 'elementor_canvas' });
  console.log(`Angelegt #${page.id} als ${page.status}`);
}
console.log(`Formular: ${formId === 'FORM_ID' ? 'noch Platzhalter' : '/f/' + formId}`);
