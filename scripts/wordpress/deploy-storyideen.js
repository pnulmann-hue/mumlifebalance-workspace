// Deploy Landing-Page "90 Storyideen für Networkerinnen" (19 CHF) auf mumlifebalance.ch
// Quelle: outputs/salespages/90-storyideen-landingpage.html (Elevate-Look, Brand-Farben, 2 Fotos)
// - Lädt die 2 Fotos in die Mediathek, ersetzt die img/-Pfade durch WP-URLs
// - wpautop-Fix (CSS minifiziert), versteckt Theme-Page-Title, Status: draft
// Ausführen: cd scripts/wordpress && node --env-file=.env deploy-storyideen.js
import { createOrUpdatePage, uploadMedia, updatePage, findPageBySlug } from './wp-api.js';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '..', '..');
const HTML_PATH = path.join(REPO, 'outputs', 'salespages', '90-storyideen-landingpage.html');
const IMG_STORY = path.join(REPO, 'outputs', 'salespages', 'img', 'patricia-story.jpg');
const IMG_ABOUT = path.join(REPO, 'outputs', 'salespages', 'img', 'patricia-about.jpg');

const SLUG = 'storyideen';
const CSS_OUT = path.join(REPO, 'outputs', 'salespages', 'storyideen-customizer.css');
const SEO_TITLE = '90 Storyideen für Networkerinnen · 19 CHF Workbook';
const SEO_DESC = 'Endlich wissen, was du posten sollst — ohne ständig dein Produkt in den Vordergrund zu stellen. 90 fertige Storyideen für Networkerinnen. Sofort-Download, 19 CHF.';
const SEO_FOCUS = 'Storyideen für Networkerinnen';

// WAF-Workaround (Imunify360): CSS NICHT in den Page-POST (dichte {};:# blocken).
// → HTML un-minifiziert in die Seite, CSS gescopt auf .si in den Customizer (Admin umgeht WAF).
async function main() {
  console.log('① Fotos hochladen …');
  const story = await uploadMedia(IMG_STORY, {
    title: 'Storyideen LP · Patricia Story',
    altText: 'Patricia Nulmann, Mentorin für Networkerinnen',
  });
  const about = await uploadMedia(IMG_ABOUT, {
    title: 'Storyideen LP · Patricia Ueber',
    altText: 'Patricia Nulmann, vierfache Mama und Networkerin',
  });
  console.log(`   Story-Foto: ${story.source_url}`);
  console.log(`   Ueber-Foto: ${about.source_url}`);

  console.log('② HTML + CSS trennen, Bildpfade → WP-URLs …');
  const raw = await readFile(HTML_PATH, 'utf-8');
  // ECHTE Blöcke via lastIndexOf (der Datei-Kommentar oben erwähnt <style>/<div class="si"> als Text!)
  const cssEnd = raw.lastIndexOf('</style>');
  const css = raw.slice(raw.lastIndexOf('<style>') + 7, cssEnd).trim()
    .replace(/img\/patricia-story\.jpg/g, story.source_url)
    .replace(/img\/patricia-about\.jpg/g, about.source_url);
  // reines HTML-Markup (kein <style>), un-minifiziert — geht durch die WAF
  const bodyHtml = raw.slice(raw.indexOf('<div class="si">', cssEnd), raw.lastIndexOf('</div>') + 6)
    .replace(/img\/patricia-story\.jpg/g, story.source_url)
    .replace(/img\/patricia-about\.jpg/g, about.source_url);

  await writeFile(CSS_OUT, css, 'utf-8');
  console.log(`   CSS geschrieben → ${path.relative(REPO, CSS_OUT)} (${(css.length/1024).toFixed(1)} KB)`);

  const meta = {
    rank_math_focus_keyword: SEO_FOCUS,
    rank_math_title: SEO_TITLE,
    rank_math_description: SEO_DESC,
    _yoast_wpseo_focuskw: SEO_FOCUS,
    _yoast_wpseo_title: SEO_TITLE,
    _yoast_wpseo_metadesc: SEO_DESC,
  };

  console.log('③ Seite als Draft anlegen (nur HTML) …');
  let result = await createOrUpdatePage({
    title: '90 Storyideen für Networkerinnen',
    slug: SLUG,
    content: bodyHtml,
    status: 'draft',
    excerpt: SEO_DESC,
    meta,
  });

  console.log('④ Canvas-Template setzen (kein Theme-Header/Doppel-Titel) …');
  try {
    await updatePage(result.id, { template: 'elementor_canvas' });
    console.log('   template=elementor_canvas gesetzt');
  } catch (e) {
    console.log('   ⚠️ Template konnte nicht gesetzt werden:', e.message);
  }

  console.log('\n✅ Draft deployed:');
  console.log(`   ID:     ${result.id}`);
  console.log(`   Slug:   ${result.slug}`);
  console.log(`   Status: ${result.status}`);
  console.log(`   Link:   ${result.link}`);
  console.log('\n📝 NÄCHSTE SCHRITTE für Patricia:');
  console.log('   1. WP-Admin → Design → Customizer → Zusätzliches CSS');
  console.log(`      → Inhalt von outputs/salespages/storyideen-customizer.css einfügen + Veröffentlichen`);
  console.log('   2. WP-Admin → Seiten → „90 Storyideen…" → Vorschau (jetzt gestylt)');
  console.log('   3. CHECKOUT-Buttons: ThriveCart-Link setzen · dann publizieren');
}

main().catch((e) => { console.error('\n❌ Deploy fehlgeschlagen:', e.message); process.exit(1); });
