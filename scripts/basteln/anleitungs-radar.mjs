#!/usr/bin/env node
/**
 * Anleitungs-Radar — sammelt Links zu echten Bastelanleitungen
 *
 * Warum: Patricia will LINKS zu Anleitungen, nicht Beschreibungen davon.
 * Videos und Blog-Tutorials kann sie selbst ansehen — das ist mehr wert als
 * eine Nacherzaehlung. Pinterest und Facebook sind zu (Login-Wall), offene
 * Blogs mit RSS dagegen zuverlaessig lesbar.
 *
 * Nutzung:
 *   node scripts/basteln/anleitungs-radar.mjs                  # alle Quellen abrufen
 *   node scripts/basteln/anleitungs-radar.mjs --check           # nur Feeds pruefen
 *   node scripts/basteln/anleitungs-radar.mjs --suche weihnacht # in gesammelten Treffern suchen
 *
 * Output: context/basteln/anleitungen.json  (Datenbank, alle Treffer)
 *         context/basteln/anleitungen.md    (lesbare Liste, nach Thema gruppiert)
 *
 * Idempotent: bekannte Links werden nicht gedoppelt, nur neue kommen dazu.
 */

import { readFile, writeFile } from 'node:fs/promises';

const QUELLEN = 'context/basteln/anleitungs-quellen.json';
const DB = 'context/basteln/anleitungen.json';
const MD = 'context/basteln/anleitungen.md';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)';
const PAUSE = 500;

// Feed-Pfade, die bei den ueblichen Blog-Systemen funktionieren
const FEED_KANDIDATEN = [
  '/feeds/posts/default',      // Blogspot
  '/feed/',                    // WordPress
  '/feed',
  '/rss',
  '/index.xml',
  '/atom.xml',
  '/?feed=rss2',
];

// Themen-Erkennung: Tag -> Suchmuster im Titel/Text
const THEMEN = {
  weihnachten: /weihnacht|christmas|advent|nikolaus|tannenbaum|stern|schneeflocke|winterlich/i,
  advent: /advent|kalender.{0,15}(24|türchen)|adventskalender/i,
  ostern: /ostern|osterhase|osterei|frühling|küken/i,
  geburtstag: /geburtstag|birthday|geburtstagskarte/i,
  geburt: /baby|geburt(?!stag)|taufe|willkommen.{0,10}baby/i,
  hochzeit: /hochzeit|wedding|verlobung|jubiläum/i,
  danke: /danke|dankeschön|thank/i,
  trost: /trost|beileid|genesung|gute besserung|aufmunter/i,
  muttertag: /muttertag|mama|mutter/i,
  vatertag: /vatertag|papa/i,
  einschulung: /einschulung|schulanfang|schulstart|abschluss|prüfung/i,
  verpackung: /verpackung|box|schachtel|tüte|beutel|goodie|geschenkverpackung|milchkarton|explosionsbox/i,
  couvert: /umschlag|couvert|envelope|briefumschlag/i,
  technik: /technik|tutorial|anleitung|schritt für schritt|how ?to|erklär/i,
  aquarell: /aquarell|watercolor|wasserfarbe|distress|ink blending|verwischen/i,
  kolorieren: /kolorier|copic|alkoholmarker|ausmalen|schattier/i,
  embossing: /embossing|präge|heat ?tool|pulver/i,
  stanzen: /stanze|stanzschablone|die ?cut|thinlits/i,
  schablone: /schablone|stencil|maske/i,
  pop_up: /pop.?up|beweglich|mechanik|schiebe|ziehkarte|blubber/i,
  hintergrund: /hintergrund|background|panel/i,
  plotter: /plotter|silhouette|cricut|print.?and.?cut|scan.?n.?cut/i,
  gonis: /gonis|betonpaste|rubbel|spitzencreme|glitzercreme|design ?freezer/i,
  batch: /serie|mehrere|auf vorrat|batch|10 karten|stapel/i,
};

const args = process.argv.slice(2);
const nurCheck = args.includes('--check');
const suchIdx = args.indexOf('--suche');

const schlaf = ms => new Promise(r => setTimeout(r, ms));

const entities = s => s
  .replace(/&auml;/g, 'ä').replace(/&ouml;/g, 'ö').replace(/&uuml;/g, 'ü')
  .replace(/&Auml;/g, 'Ä').replace(/&Ouml;/g, 'Ö').replace(/&Uuml;/g, 'Ü')
  .replace(/&szlig;/g, 'ss').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
  .replace(/&apos;|&#39;/g, "'").replace(/&nbsp;/g, ' ')
  .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(+d))
  .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCharCode(parseInt(h, 16)))
  .replace(/\s+/g, ' ').trim();

const strip = h => entities(h.replace(/<[^>]+>/g, ' '));

/**
 * Seite holen und korrekt dekodieren.
 * Wichtig fuer mundartstempel.ch: die Seite ist latin1, nicht UTF-8 —
 * ohne Charset-Erkennung werden aus Umlauten Fragezeichen.
 */
async function holen(url) {
  const res = await fetch(url, { headers: { 'User-Agent': UA }, redirect: 'follow' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const buf = Buffer.from(await res.arrayBuffer());
  let charset = (res.headers.get('content-type') || '').match(/charset=([\w-]+)/i)?.[1];
  if (!charset) {
    // erste 2 KB nach einer Charset-Deklaration absuchen
    const kopf = buf.subarray(0, 2048).toString('latin1');
    charset = kopf.match(/charset=["']?([\w-]+)/i)?.[1]
           || kopf.match(/encoding=["']([\w-]+)["']/i)?.[1];
  }
  const norm = (charset || 'utf-8').toLowerCase();
  const kodierung = /^(iso-8859-1|iso-8859-15|latin1|windows-1252|cp1252)$/.test(norm) ? 'latin1' : 'utf-8';
  return buf.toString(kodierung);
}

function istFeed(text) {
  return /<(rss|feed)[\s>]/i.test(text) && /<(entry|item)[\s>]/i.test(text);
}

/** Feed-URL ermitteln: erst <link rel=alternate>, dann Standardpfade. */
async function findeFeed(basisUrl) {
  const basis = basisUrl.replace(/\/$/, '');
  try {
    const html = await holen(basisUrl);
    const m = html.match(/<link[^>]+type=["']application\/(?:rss|atom)\+xml["'][^>]*>/i);
    if (m) {
      const href = m[0].match(/href=["']([^"']+)["']/i);
      if (href) {
        const abs = href[1].startsWith('http') ? href[1] : new URL(href[1], basisUrl).href;
        try {
          if (istFeed(await holen(abs))) return abs;
        } catch { /* weiter mit Kandidaten */ }
      }
    }
  } catch { /* Startseite nicht lesbar -> Kandidaten probieren */ }

  for (const pfad of FEED_KANDIDATEN) {
    const kandidat = basis + pfad;
    try {
      if (istFeed(await holen(kandidat))) return kandidat;
    } catch { /* naechster */ }
    await schlaf(200);
  }
  return null;
}

/** Eintraege aus RSS oder Atom parsen. */
function parseFeed(xml, quelle) {
  const treffer = [];
  const bloecke = [...xml.matchAll(/<(entry|item)[\s>][\s\S]*?<\/\1>/gi)].map(m => m[0]);

  for (const b of bloecke) {
    const titelRoh = (b.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '';
    const titel = strip(titelRoh);
    if (!titel) continue;

    // Link: Atom <link rel="alternate" href> oder RSS <link>text</link>
    let link = null;
    const atom = b.match(/<link[^>]*rel=["']alternate["'][^>]*href=["']([^"']+)["']/i)
              || b.match(/<link[^>]*href=["']([^"']+)["'][^>]*\/?>/i);
    if (atom) link = atom[1];
    if (!link) {
      const rss = b.match(/<link>([^<]+)<\/link>/i);
      if (rss) link = rss[1].trim();
    }
    if (!link) continue;

    const datum = ((b.match(/<(published|pubDate|updated)>([^<]+)/i) || [])[2] || '').slice(0, 10);
    const inhalt = strip(((b.match(/<(content|summary|description)[^>]*>([\s\S]*?)<\/\1>/i) || [])[2] || '')).slice(0, 400);
    const labels = [...b.matchAll(/(?:category[^>]*term|category[^>]*>)["']?([^"'<>]{2,40})/gi)]
      .map(m => entities(m[1])).filter(x => x && !/^https?:/.test(x)).slice(0, 8);

    const suchbasis = `${titel} ${inhalt} ${labels.join(' ')}`;
    const themen = Object.entries(THEMEN).filter(([, re]) => re.test(suchbasis)).map(([t]) => t);

    treffer.push({ titel, link, datum, quelle: quelle.name, themen, labels, auszug: inhalt.slice(0, 200) });
  }
  return treffer;
}

/**
 * HTML-Quelle scrapen (fuer Seiten ohne Feed, z.B. Mundarts Gratis-Anleitungen).
 * Nimmt alle <a>-Links, deren URL auf quelle.link_muster passt, und benutzt
 * den Linktext als Titel.
 */
function parseHtmlQuelle(html, quelle) {
  const musterLink = new RegExp(quelle.link_muster, 'i');
  const putzen = quelle.titel_putzen ? new RegExp(quelle.titel_putzen, 'i') : null;
  const treffer = [];
  const gesehen = new Set();

  for (const m of html.matchAll(/<a[^>]+href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)) {
    let [, url, innen] = m;
    if (!musterLink.test(url)) continue;

    let titel = strip(innen);
    if (putzen) titel = titel.replace(putzen, '').trim();
    // Navigations- und Blindlinks aussortieren
    if (!titel || titel.length < 6 || /^(anleitungen|kundenlogin|weiter|mehr|hier)$/i.test(titel)) continue;

    const abs = url.startsWith('http') ? url : new URL(url, quelle.url).href;
    if (abs.endsWith('#') || gesehen.has(abs)) continue;
    gesehen.add(abs);

    const themen = Object.entries(THEMEN).filter(([, re]) => re.test(titel)).map(([t]) => t);
    treffer.push({ titel, link: abs, datum: '', quelle: quelle.name, themen, labels: [], auszug: '' });
  }
  return treffer;
}

// ---------- Suche in bestehender DB ----------
if (suchIdx !== -1) {
  const begriff = args.slice(suchIdx + 1).join(' ').toLowerCase();
  if (!begriff) { console.error('Nutzung: --suche <begriff>'); process.exit(1); }
  let db;
  try { db = JSON.parse(await readFile(DB, 'utf-8')); }
  catch { console.error(`Noch keine Datenbank. Erst ohne --suche laufen lassen.`); process.exit(1); }
  const hits = db.anleitungen.filter(a =>
    `${a.titel} ${a.auszug} ${a.themen.join(' ')} ${(a.labels || []).join(' ')}`.toLowerCase().includes(begriff));
  if (!hits.length) { console.log(`Kein Treffer fuer "${begriff}" in ${db.anleitungen.length} Anleitungen.`); process.exit(0); }
  console.log(`\n${hits.length} Treffer fuer "${begriff}":\n`);
  for (const h of hits.slice(0, 40)) {
    console.log(`- **${h.titel}** (${h.quelle}${h.datum ? ', ' + h.datum : ''})`);
    console.log(`  ${h.link}`);
    if (h.themen.length) console.log(`  Themen: ${h.themen.join(' · ')}`);
  }
  process.exit(0);
}

// ---------- Quellen laden ----------
const q = JSON.parse(await readFile(QUELLEN, 'utf-8'));
let quellenGeaendert = false;

// ---------- Feeds pruefen / ermitteln ----------
console.error('Pruefe Feeds …\n');
for (const quelle of q.quellen) {
  if (quelle.typ === 'html') continue;   // braucht keinen Feed
  if (!quelle.feed) {
    const gefunden = await findeFeed(quelle.url);
    if (gefunden) { quelle.feed = gefunden; quellenGeaendert = true; console.error(`  ✓ ${quelle.name}: Feed gefunden -> ${gefunden}`); }
    else console.error(`  ✗ ${quelle.name}: kein Feed gefunden (${quelle.url})`);
  }
}
if (quellenGeaendert) {
  q.quellen_geprueft = new Date().toISOString().slice(0, 10);
  await writeFile(QUELLEN, JSON.stringify(q, null, 2), 'utf-8');
}

// Abrufbar ist alles mit Feed plus alle HTML-Scrape-Quellen
const abrufbar = q.quellen.filter(x => x.feed || (x.typ === 'html' && x.link_muster));
const mitFeed = abrufbar;
console.error(`\n${abrufbar.length} von ${q.quellen.length} Quellen abrufbar `
  + `(${abrufbar.filter(x => x.typ === 'html').length} davon per HTML-Scrape).\n`);
if (nurCheck) process.exit(0);

// ---------- Bestehende DB laden ----------
let db = { stand: null, anleitungen: [] };
try { db = JSON.parse(await readFile(DB, 'utf-8')); } catch { /* erster Lauf */ }
const bekannt = new Set(db.anleitungen.map(a => a.link));

// ---------- Feeds abrufen ----------
let neu = 0;
for (const quelle of abrufbar) {
  try {
    const treffer = quelle.typ === 'html'
      ? parseHtmlQuelle(await holen(quelle.url), quelle)
      : parseFeed(await holen(quelle.feed), quelle);
    let n = 0;
    for (const t of treffer) {
      if (bekannt.has(t.link)) continue;
      bekannt.add(t.link);
      db.anleitungen.push(t);
      n++; neu++;
    }
    console.error(`  ${quelle.name}: ${treffer.length} Eintraege, ${n} neu`);
  } catch (e) {
    console.error(`  ${quelle.name}: Fehler — ${e.message}`);
  }
  await schlaf(PAUSE);
}

db.stand = new Date().toISOString().slice(0, 10);
db.anleitungen.sort((a, b) => (b.datum || '').localeCompare(a.datum || ''));
await writeFile(DB, JSON.stringify(db, null, 1), 'utf-8');

// ---------- Lesbare Markdown-Ansicht ----------
const nachThema = new Map();
for (const a of db.anleitungen) {
  const keys = a.themen.length ? a.themen : ['ohne-thema'];
  for (const k of keys) {
    if (!nachThema.has(k)) nachThema.set(k, []);
    nachThema.get(k).push(a);
  }
}

const L = [
  '---', 'tags: [basteln, ideen, referenz]', '---', '',
  '# Anleitungs-Radar — gesammelte Links',
  '',
  `**Stand:** ${db.stand} · **${db.anleitungen.length} Anleitungen** aus ${mitFeed.length} Blogs · erzeugt von \`scripts/basteln/anleitungs-radar.mjs\``,
  '',
  '> **Wozu:** echte Anleitungen zum Nachbauen — Links, keine Nacherzaehlungen. Videos und Tutorials kannst du selbst ansehen, das ist mehr wert als meine Beschreibung davon.',
  '',
  '```bash',
  'node scripts/basteln/anleitungs-radar.mjs                   # neue Beitraege holen',
  'node scripts/basteln/anleitungs-radar.mjs --suche weihnacht # in den Treffern suchen',
  '```',
  '',
  '→ Quellenliste: `context/basteln/anleitungs-quellen.json` · Material-Register: [[inventar-stempel]]',
  '', '---', '',
];

const sortiert = [...nachThema.entries()]
  .filter(([k]) => k !== 'ohne-thema')
  .sort((a, b) => b[1].length - a[1].length);

L.push('## Nach Thema', '');
for (const [thema, liste] of sortiert) {
  L.push(`### ${thema} (${liste.length})`, '');
  for (const a of liste.slice(0, 25)) {
    L.push(`- [${a.titel}](${a.link}) — ${a.quelle}${a.datum ? `, ${a.datum}` : ''}`);
  }
  if (liste.length > 25) L.push(`- … ${liste.length - 25} weitere — \`--suche ${thema}\``);
  L.push('');
}

const ohne = nachThema.get('ohne-thema') || [];
if (ohne.length) {
  L.push('---', '', `## Ohne erkanntes Thema (${ohne.length})`, '',
    'Kein Themen-Muster getroffen — hier lohnt ein Blick, ob die Erkennung erweitert werden sollte.', '');
  for (const a of ohne.slice(0, 15)) L.push(`- [${a.titel}](${a.link}) — ${a.quelle}`);
  L.push('');
}

L.push('---', '', '## 🔗 Verwandte Notizen',
  '- [[inventar-stempel]] · [[projekt-ideen]] · [[shop-recherche]] · [[README]]', '');

await writeFile(MD, L.join('\n'), 'utf-8');
console.error(`\n✅ ${neu} neue Anleitungen (${db.anleitungen.length} gesamt) → ${MD}`);
