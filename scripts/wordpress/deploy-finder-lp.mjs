/**
 * Deploy der Produkt-Ideen-Finder-Landingpage (Ordner-Version) als WP-Entwurf.
 * WAF-safe: CSS wird unter `.pif` gescoped und separat rausgeschrieben (Customizer),
 * Markup geht per REST als wp:html rein. Body-Inhalt wird in <div class="pif"> gewickelt.
 *
 *   node --env-file=.env deploy-finder-lp.mjs            # nur bauen + QA-Preview, kein Upload
 *   node --env-file=.env deploy-finder-lp.mjs --deploy   # als Entwurf hochladen
 *   node --env-file=.env deploy-finder-lp.mjs --deploy --publish
 */
import { readFileSync, writeFileSync } from 'fs';

const SRC = new URL('../../outputs/salespages/produkt-ideen-finder-landingpage/index.html', import.meta.url);
const CSS_OUT = new URL('../../outputs/salespages/produkt-ideen-finder-customizer.css', import.meta.url);
const PREVIEW = new URL('../../outputs/salespages/produkt-ideen-finder-landingpage/_wp-preview.html', import.meta.url);
const SLUG = 'produkt-ideen-finder';
const TITLE = 'Produkt-Ideen-Finder';
const PREFIX = '.pif';

const raw = readFileSync(SRC, 'utf8');

// 1) <style> herausziehen (es gibt genau einen Block im <head>)
const styleStart = raw.indexOf('<style>');
const styleEnd = raw.indexOf('</style>', styleStart);
let css = raw.slice(styleStart + 7, styleEnd);

// 2) <body>-Innenhalt holen, <script> entfernen
let body = raw.slice(raw.indexOf('<body>') + 6, raw.indexOf('</body>'));
body = body.replace(/<!--([\s\S]*?)-->/g, '');            // HTML-Kommentare raus
// WAF (NinjaFirewall) blockt <script> im POST -> raus. AC-Embed + Reveal fuegt
// Patricia im WP-Editor (Custom-HTML-Block) ein; Reveal wird per CSS ersetzt.
body = body.replace(/<script[\s\S]*?<\/script>/gi, '');
// Marker, wo das AC-Formular-Script hin soll
body = body.replace(/<div class="_form_66"><\/div>/,
  '<div class="_form_66"></div>\n<p style="font-size:13px;color:#5c6b75;text-align:center">[Hier im WP-Editor den ActiveCampaign-Embed-Code fuer Formular 66 als Custom-HTML einfuegen]</p>');

// 3) CSS unter .pif scopen (brace-aware)
function scopeCss(input, prefix) {
  input = input.replace(/@import[^;]+;/g, '');
  let out = '';
  let i = 0;
  const n = input.length;
  // liest einen Deklarations-Block { ... } ab Position der oeffnenden Klammer, gibt Endindex zurueck
  function copyDeclBlock(start) {
    let depth = 0, j = start;
    for (; j < n; j++) {
      if (input[j] === '{') depth++;
      else if (input[j] === '}') { depth--; if (depth === 0) { j++; break; } }
    }
    return j;
  }
  function prefixSelector(sel) {
    return sel.split(',').map(s => {
      s = s.trim();
      if (!s) return s;
      if (/^(\.pif\b|#optin\b|#_form_66_\b)/.test(s)) return s;   // schon gescoped
      if (s === ':root' || s === 'html' || s === 'body' || s === 'html,body' || s === 'html, body') return prefix;
      return prefix + ' ' + s;
    }).join(', ');
  }
  function process(str) {
    let res = '';
    let k = 0;
    const m = str.length;
    while (k < m) {
      const brace = str.indexOf('{', k);
      if (brace === -1) { res += str.slice(k); break; }
      let sel = str.slice(k, brace).trim();
      // finde Blockende relativ zu str
      let depth = 0, j = brace;
      for (; j < m; j++) { if (str[j] === '{') depth++; else if (str[j] === '}') { depth--; if (depth === 0) { j++; break; } } }
      const inner = str.slice(brace + 1, j - 1);
      if (/^@media|^@supports/i.test(sel)) {
        res += sel + ' {\n' + process(inner) + '\n}\n';                     // rekursiv: innere Selektoren scopen
      } else if (/^@(keyframes|font-face|page|import|charset)/i.test(sel)) {
        res += sel + ' {' + inner + '}\n';                                   // nicht scopen
      } else {
        res += prefixSelector(sel) + ' {' + inner + '}\n';
      }
      k = j;
    }
    return res;
  }
  out = process(input);
  return out.trim();
}

let scoped = scopeCss(css, PREFIX);
// Ohne Reveal-JS muessen die .rev-Elemente sichtbar sein
scoped += '\n' + PREFIX + ' .rev{opacity:1 !important;transform:none !important}';

// 4) Markup + Preview + Customizer-CSS schreiben
const wrapped = '<div class="pif">\n' + body.trim() + '\n</div>';
const markup = '<!-- wp:html -->\n' + wrapped + '\n<!-- /wp:html -->';

const MARKER = '/* === PRODUKT-IDEEN-FINDER LP (auto, gescoped unter .pif) === */';
const cssFile = MARKER + '\n' + scoped + '\n/* === ENDE === */\n';
writeFileSync(CSS_OUT, cssFile, 'utf8');

// QA-Preview: eigenstaendige Datei mit gescoptem CSS (zeigt, ob im Theme nichts bricht)
const preview = '<!doctype html><html lang="de"><head><meta charset="utf-8">' +
  '<link href="https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">' +
  '<style>' + scoped + '</style></head><body style="margin:0;background:#eee">' + wrapped + '</body></html>';
writeFileSync(PREVIEW, preview, 'utf8');

console.log('Markup  :', markup.length, 'Zeichen');
console.log('CSS     :', cssFile.length, 'Zeichen ->', CSS_OUT.pathname.split('/').pop());
console.log('Preview :', PREVIEW.pathname.split('/').pop());

if (process.argv.includes('--deploy')) {
  const { createOrUpdatePage } = await import('./wp-api.js');
  const publish = process.argv.includes('--publish');
  const page = await createOrUpdatePage({ title: TITLE, slug: SLUG, content: markup, status: publish ? 'publish' : 'draft' });
  console.log('\nWP-Seite:', page.link, '| Status:', page.status, '| ID:', page.id);
  console.log('CSS in Customizer -> Design -> Zusaetzliches CSS einfuegen:', CSS_OUT.pathname.split('/').pop());
} else {
  console.log('\n(Nur gebaut. Mit --deploy als Entwurf hochladen.)');
}
