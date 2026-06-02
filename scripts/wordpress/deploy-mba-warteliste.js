// Deployt die MBA-Warteliste-Seite als WordPress-ENTWURF (mumlifebalance.ch/mba-warteliste).
// Quelle: outputs/salespages/umsetzerinnen-pioneer/salespage-warteliste.html
// Wichtig:
//  - WordPress-WAF (NinjaFirewall) blockt <script>-Embeds + reCAPTCHA → AC-Formular als IFRAME (/f/57)
//  - Beide <style>-Bloecke (Haupt-CSS + Warteliste-CSS) einsammeln, sonst fehlt das Hero-Styling
//  - Fonts als @import oben rein (das <head><link> geht beim Body-Extrakt verloren)
//  - Status: DRAFT — Patricia prueft + publiziert selbst

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { findPageBySlug, createPage, updatePage } from './wp-api.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(__dirname, '../../outputs/salespages/umsetzerinnen-pioneer/salespage-warteliste.html');

async function main() {
  console.log('=== MBA-Warteliste Deploy (Entwurf) ===\n');
  let html = readFileSync(SRC, 'utf8');

  // 1) AC Script-Embed -> iframe (WAF blockt <script>)
  html = html.replace(
    /<div class="_form_57"><\/div>\s*<script src="https:\/\/mumlifebalance\.activehosted\.com\/f\/embed\.php\?id=57"[^>]*><\/script>/i,
    '<iframe src="https://mumlifebalance.activehosted.com/f/57" style="width:100%;min-height:620px;border:0;background:transparent;" loading="lazy" title="MBA Warteliste"></iframe>'
  );

  // 2) ALLE <style>-Bloecke einsammeln (head + body), minifyen
  const styles = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]).join('\n');
  const minifiedCss = (styles)
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\s*\n\s*/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .replace(/\s*([{}:;,])\s*/g, '$1');

  // 3) Body-Content extrahieren, Scripts/noscript/inline-styles raus
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  let body = (bodyMatch ? bodyMatch[1] : html)
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '');

  const wpContent = `<!-- wp:html -->\n<style>${minifiedCss}</style>\n${body.replace(/\n+/g, '\n').trim()}\n<!-- /wp:html -->`;

  // 4) Page als Entwurf anlegen/aktualisieren
  const slug = 'mba-warteliste';
  const title = 'Mum Business Academy — Warteliste';
  let page = await findPageBySlug(slug);
  if (page) {
    console.log(`Update bestehende Page #${page.id} (Status bleibt ${page.status})...`);
    page = await updatePage(page.id, { title, content: wpContent });
  } else {
    console.log('Erstelle neue Page als ENTWURF...');
    page = await createPage({ slug, title, content: wpContent, status: 'draft' });
  }

  console.log(`\n=== ✅ FERTIG ===`);
  console.log(`Page-ID: ${page.id}`);
  console.log(`Status:  ${page.status}`);
  console.log(`URL:     https://mumlifebalance.ch/${slug}  (erst nach deinem Publish sichtbar)`);
  console.log(`AC-Formular: iframe /f/57 (Tag mba-warteliste)`);
  console.log(`\n👉 In WP pruefen, ggf. Seiten-Template auf "Canvas/Volle Breite" setzen, dann publizieren.`);
}

main().catch((e) => {
  console.error('\n=== ❌ FEHLER ===');
  console.error(e.message);
  process.exit(1);
});
