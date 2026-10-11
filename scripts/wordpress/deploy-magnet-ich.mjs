// Deployt die Magnet-Ich-Salespage (mumlifebalance.ch/magnet-ich) — Signature-Design.
// Quelle: outputs/salespages/magnet-ich/magnet-ich-inhalt.html (reines Markup, kein <style>/<script> — WAF)
// CSS:    outputs/salespages/magnet-ich/magnet-ich.css -> von Patricia in den Customizer (gescopt auf .mi-sp)
// Bilder: outputs/salespages/magnet-ich/assets/mi-*.jpg -> Mediathek (Zuordnung in medien.json, wiederholbar)
// Neue Seite als ENTWURF; eine bestehende behaelt ihren Status.
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { findPageBySlug, createPage, updatePage, uploadMedia } from './wp-api.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIR = resolve(__dirname, '../../outputs/salespages/magnet-ich');
const KASSE = 'https://mumlifebalance.thrivecart.com/magnet-ich/';
const MEDIEN = resolve(DIR, 'medien.json');

let html = readFileSync(resolve(DIR, 'magnet-ich-inhalt.html'), 'utf8');
if (/<style|<script|<link/i.test(html)) throw new Error('Quelle enthaelt <style>/<script>/<link> — die WAF blockt das');

const medien = existsSync(MEDIEN) ? JSON.parse(readFileSync(MEDIEN, 'utf8')) : {};
const bilder = [...new Set([...html.matchAll(/assets\/(mi-[a-z]+\.jpg)/g)].map((m) => m[1]))];
for (const b of bilder) {
  if (!medien[b]) {
    const m = await uploadMedia(resolve(DIR, 'assets', b), { title: `Magnet-Ich ${b}`, altText: 'Patricia Ulmann' });
    medien[b] = m.source_url;
    console.log('hochgeladen', b, '->', m.source_url);
    writeFileSync(MEDIEN, JSON.stringify(medien, null, 1));
  }
  html = html.split(`assets/${b}`).join(medien[b]);
}
html = html.split('#CHECKOUT').join(KASSE);
if (html.includes('assets/')) throw new Error('Nicht ersetzter Bildpfad in der Seite');

const content = `<!-- wp:html -->\n${html.trim()}\n<!-- /wp:html -->`;
const slug = 'magnet-ich';
const title = 'Magnet-Ich — 3 Wochen 1:1 mit Patricia';
let page = await findPageBySlug(slug);
if (page) {
  page = await updatePage(page.id, { title, content });
  console.log(`Aktualisiert #${page.id} (Status bleibt ${page.status})`);
} else {
  page = await createPage({ slug, title, content, status: 'draft' });
  await updatePage(page.id, { template: 'elementor_canvas' });
  console.log(`Angelegt #${page.id} als ${page.status}`);
}
console.log(`Groesse: ${Math.round(content.length / 1024)} KB`);
