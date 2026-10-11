// Deploy der Startklar-Verkaufsseite (39 CHF) auf mumlifebalance.ch
//
// Quelle: outputs/salespages/startklar/index.html (minikurs-salespage-Design)
//
// Der Weg ist durch zwei frühere Deploys belegt und hat drei Fallen:
//
//  1. Imunify360-WAF blockt dichte POSTs. Deshalb geht NUR das Markup in die
//     Seite — kein <script>, keine Google-Fonts-URL. Das CSS kommt gescopt in
//     den Customizer, dort greift die WAF nicht.
//  2. wpautop zerlegt HTML ohne Gutenberg-Wrapper und setzt <p>-Tags in CSS
//     mit Leerzeilen. Deshalb <!-- wp:html --> aussenrum und keine Leerzeilen
//     im CSS.
//  3. Ohne <script> bleiben die Einblend-Elemente (.rev) unsichtbar, weil der
//     IntersectionObserver fehlt, der sonst .in setzt. Deshalb wird .rev im
//     gescopten CSS auf sichtbar gezwungen.
//
// Ausführen: cd scripts/wordpress && node --env-file=.env deploy-startklar.mjs
import { createOrUpdatePage, uploadMedia, updatePage, findPageBySlug, listMedia } from './wp-api.js';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, '..', '..');
const QUELLE = path.join(REPO, 'outputs', 'salespages', 'startklar', 'index.html');
const FOTO_HERO = path.join(REPO, 'outputs', 'salespages', 'startklar', 'assets', 'patricia-hero.jpg');
const FOTO_PORTRAIT = path.join(REPO, 'outputs', 'salespages', 'startklar', 'assets', 'patricia-portrait.jpg');
const CSS_OUT = path.join(REPO, 'outputs', 'salespages', 'startklar', 'customizer.css');

const SLUG = 'startklar';
const WRAPPER = 'slp-startklar';
const SEO_TITLE = 'Startklar · Dein Instagram-Grundgerüst für 39 CHF';
const SEO_DESC = 'In einer Woche steht dein Instagram-Profil — und du weisst, wo du hindrücken musst. '
  + '12 Lektionen zum Mitmachen für Network-Mamas, die noch nie etwas gepostet haben.';

/** Alle Selektoren unter den Wrapper hängen, damit das CSS nicht die ganze Website trifft. */
function scopen(css, wrapper) {
  // 🚨 Kommentare zuerst raus. Sonst behandelt die Schleife unten einen
  // Kommentar vor einer Regel als Teil des Selektors und zerlegt ihn an
  // seinen Kommas — das CSS ist danach kaputt.
  css = css.replace(/\/\*[\s\S]*?\*\//g, '');
  // Einfacher, robuster Weg: jede Selektorliste auf oberster Ebene umschreiben
  let out = '';
  const regeln = [];
  let tiefe = 0, start = 0;
  for (let i = 0; i < css.length; i++) {
    if (css[i] === '{') {
      if (tiefe === 0) {
        const sel = css.slice(start, i).trim();
        regeln.push({ sel, von: i });
      }
      tiefe++;
    } else if (css[i] === '}') {
      tiefe--;
      if (tiefe === 0) {
        const r = regeln[regeln.length - 1];
        r.koerper = css.slice(r.von + 1, i);
        r.bis = i;
        start = i + 1;
      }
    }
  }
  for (const r of regeln) {
    if (r.sel.startsWith('@media') || r.sel.startsWith('@supports')) {
      out += `${r.sel}{${scopen(r.koerper, wrapper)}}\n`;
    } else if (r.sel.startsWith('@')) {
      out += `${r.sel}{${r.koerper}}\n`;            // @font-face, @keyframes: unverändert
    } else {
      const sel = r.sel.split(',').map((s) => {
        s = s.trim();
        if (!s) return s;
        if (s === '*') return `.${wrapper} *`;
        if (s === 'body' || s === 'html') return `.${wrapper}`;
        if (s.startsWith(':root')) return `.${wrapper}`;
        return `.${wrapper} ${s}`;
      }).join(',');
      out += `${sel}{${r.koerper}}\n`;
    }
  }
  return out;
}

async function main() {
  console.log('① Fotos in die Mediathek …');
  // Mehrfach laufen lassen soll keine Dubletten anlegen: erst nachsehen,
  // ob das Bild schon oben liegt. WordPress haengt sonst -1, -2, -3 an.
  const vorhanden = await listMedia({ search: 'Startklar LP' }).catch(() => []);
  const finde = (titel) => (vorhanden || []).find(
    (m) => (m.title?.rendered || '').includes(titel));
  const holen = async (datei, titel, alt) => {
    const da = finde(titel);
    if (da) { console.log('   schon da:', titel); return da; }
    return uploadMedia(datei, { title: 'Startklar LP · ' + titel, altText: alt });
  };
  const hero = await holen(FOTO_HERO, 'Patricia Hero', 'Patricia Ulmann am Bodensee');
  const portrait = await holen(FOTO_PORTRAIT, 'Patricia Portrait',
    'Patricia Ulmann, vierfache Mama und Mentorin für Networkerinnen');
  console.log('   Hero    :', hero.source_url);
  console.log('   Portrait:', portrait.source_url);

  console.log('② HTML und CSS trennen …');
  const roh = await readFile(QUELLE, 'utf-8');
  const cssVon = roh.indexOf('<style>') + 7;
  const cssBis = roh.lastIndexOf('</style>');
  let css = roh.slice(cssVon, cssBis);
  let body = roh.slice(roh.indexOf('<body>') + 6, roh.lastIndexOf('<script>'));

  // Bildpfade auf die Mediathek zeigen lassen — in BEIDEN Teilen
  const bild = (s) => s
    .replace(/assets\/patricia-hero\.jpg/g, hero.source_url)
    .replace(/assets\/patricia-portrait\.jpg/g, portrait.source_url);
  css = bild(css);
  body = bild(body);

  // Den Arbeits-Hinweiskasten entfernen — der gehört nicht auf die Kundenseite
  const hinweisVon = body.indexOf('<!-- ===== HINWEIS FÜR PATRICIA');
  const hinweisBis = body.indexOf('<!-- ===== HERO ===== -->');
  if (hinweisVon !== -1 && hinweisBis !== -1) {
    body = body.slice(0, hinweisVon) + body.slice(hinweisBis);
    console.log('   Hinweiskasten entfernt');
  }

  console.log('③ CSS scopen auf .' + WRAPPER + ' …');
  let gescopt = scopen(css, WRAPPER);
  // Ohne das Script bleiben die Einblend-Elemente sonst auf opacity:0 stehen.
  gescopt += `.${WRAPPER} .rev{opacity:1;transform:none}\n`;
  // wpautop setzt <p>-Tags in Leerzeilen — die müssen raus (CRLF beachten)
  gescopt = gescopt.replace(/\r/g, '').split('\n').filter((z) => z.trim()).join('\n');
  await writeFile(CSS_OUT, gescopt, 'utf-8');
  console.log('   ' + Math.round(gescopt.length / 1024) + ' KB -> ' + CSS_OUT);

  console.log('④ Seite anlegen (nur Markup, kein Script, kein Font-Link) …');
  const inhalt = '<!-- wp:html -->\n<div class="' + WRAPPER + '">\n' + body.trim() + '\n</div>\n<!-- /wp:html -->';
  console.log('   Markup: ' + Math.round(inhalt.length / 1024) + ' KB');

  const seite = await createOrUpdatePage({
    title: 'Startklar',
    slug: SLUG,
    content: inhalt,
    status: 'draft',
    excerpt: SEO_DESC,
  });
  console.log('   Seite ' + seite.id + ' (' + seite.status + ')');

  // Vollbreite ohne Theme-Header und ohne doppelten Seitentitel
  await updatePage(seite.id, { template: 'elementor_canvas' });
  console.log('   Template: elementor_canvas');

  const gegenprobe = await findPageBySlug(SLUG);
  console.log('\nFertig.');
  console.log('  Vorschau : ' + (gegenprobe?.link || '—'));
  console.log('  Status   : ' + gegenprobe?.status);
  console.log('\nNoch von Hand: das CSS aus ' + path.basename(CSS_OUT));
  console.log('  in den Customizer unter "Zusätzliches CSS" einfügen,');
  console.log('  dann die Seite veröffentlichen.');
  console.log('\n🚨 Danach die Seite NICHT im WP- oder Elementor-Editor öffnen —');
  console.log('   das Markup geht dabei verloren. Änderungen laufen über dieses Skript.');
}

main().catch((e) => { console.error('FEHLER:', e.message); process.exit(1); });
