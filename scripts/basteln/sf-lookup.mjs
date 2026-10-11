#!/usr/bin/env node
/**
 * Scrapbook-Forever Set-Lookup
 *
 * Holt zu einer Artikelnummer (z.B. SF363) den Set-Namen, die exakte
 * Inhaltsangabe (Anzahl Stempel + Masse) und alle Beispielkarten-Bilder
 * des Design-Teams.
 *
 * Nutzung:
 *   node scripts/basteln/sf-lookup.mjs SF363
 *   node scripts/basteln/sf-lookup.mjs SF363 SF370 SF353      # mehrere
 *   node scripts/basteln/sf-lookup.mjs SF363 --bilder          # Bilder lokal speichern
 *
 * Output: Markdown-Block auf stdout -> in context/basteln/stempelsets-sf.md einfuegen.
 * Bilder landen in context/persoenlich/basteln-shopbilder/ (GITIGNORED) —
 * fremde Produktfotos gehoeren nicht in ein oeffentliches Repo.
 */

import { writeFile, mkdir } from 'node:fs/promises';

const SHOP = 'https://scrapbookforever-shop.de';
const SHOP_ID = '94de3903-8ad2-4b60-92a8-e22e061112e7';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)';
const BILD_DIR = 'context/persoenlich/basteln-shopbilder';

const args = process.argv.slice(2);
const mitBilder = args.includes('--bilder');
const nummern = args.filter(a => !a.startsWith('--')).map(a => a.toUpperCase());

if (nummern.length === 0) {
  console.error('Nutzung: node sf-lookup.mjs SF363 [SF370 ...] [--bilder]');
  process.exit(1);
}

const entities = s => s
  .replace(/&auml;/g, 'ä').replace(/&ouml;/g, 'ö').replace(/&uuml;/g, 'ü')
  .replace(/&Auml;/g, 'Ä').replace(/&Ouml;/g, 'Ö').replace(/&Uuml;/g, 'Ü')
  .replace(/&szlig;/g, 'ss').replace(/&amp;/g, '&').replace(/&quot;/g, '"')
  .replace(/&nbsp;/g, ' ').replace(/&#(\d+);/g, (_, d) => String.fromCharCode(+d))
  .replace(/\s+/g, ' ').trim();

const strip = html => entities(html.replace(/<[^>]+>/g, ' '));

async function lookup(nr) {
  const url = `${SHOP}/epages/${SHOP_ID}.sf/de_DE/?ObjectPath=/Shops/${SHOP_ID}/Products/${nr}`;
  const res = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!res.ok) return { nr, fehler: `HTTP ${res.status}` };
  const html = await res.text();

  const titleMatch = html.match(/<title>([^<]*)<\/title>/i);
  const name = titleMatch ? entities(titleMatch[1]).replace(/ - Scrapbook Forever$/, '') : null;
  if (!name || /nicht gefunden|not found/i.test(name)) return { nr, fehler: 'Set nicht gefunden' };

  // Beschreibung — der Absatz mit der Inhaltsangabe.
  // WICHTIG: case-SENSITIVE, sonst matcht "...a8-e22e061112e7" aus der Shop-URL als "A8".
  let beschreibung = null;
  const kandidaten = [
    /(A[4-8] gro[^<]{20,700})/,
    /(Stempelset bestehend[^<]{10,700})/,
    /(Stempelset[^<]{30,700})/,
  ];
  for (const re of kandidaten) {
    const m = html.match(re);
    if (m) { beschreibung = entities(m[1]); break; }
  }

  // Preis — Schema.org-Markup, nicht der durchgestrichene Altpreis
  const pm = html.match(/itemprop=['"]price['"]\s+content=['"]([\d.]+)['"]/i);
  const preis = pm ? pm[1].replace('.', ',') + ' €' : null;
  const am = html.match(/Alter Preis[^\d]{0,40}(\d+[.,]\d{2})/i);
  const altpreis = am ? am[1].replace('.', ',') + ' €' : null;

  // Beispielkarten (die _ml-Varianten sind die grossen Bilder)
  const beispiele = [...new Set(
    [...html.matchAll(/\/WebRoot\/[^"'\s]*?_ml\.jpg/gi)].map(m => m[0])
  )].filter(p => /Bild/i.test(p)).map(p => SHOP + p);

  const hb = (html.match(/\/WebRoot\/[^"'\s]*?_ml\.jpg/i) || [])[0];

  return { nr, name, preis, altpreis, beschreibung, url, hauptbild: hb ? SHOP + hb : null, beispiele };
}

async function speichereBilder(set) {
  const dir = `${BILD_DIR}/${set.nr}`;
  await mkdir(dir, { recursive: true });
  let n = 0;
  for (const [i, bild] of set.beispiele.entries()) {
    try {
      const r = await fetch(bild, { headers: { 'User-Agent': UA } });
      if (!r.ok) continue;
      await writeFile(`${dir}/beispiel-${String(i + 1).padStart(2, '0')}.jpg`,
                      Buffer.from(await r.arrayBuffer()));
      n++;
    } catch { /* einzelnes Bild egal */ }
  }
  return { dir, n };
}

for (const nr of nummern) {
  const set = await lookup(nr);

  if (set.fehler) {
    console.log(`\n### ❌ ${nr} — ${set.fehler}\n`);
    continue;
  }

  console.log(`\n### ${set.name}`);
  const p = set.preis ? ` · **Preis:** ${set.preis}${set.altpreis && set.altpreis !== set.preis ? ` (statt ${set.altpreis})` : ''}` : '';
  console.log(`- **Artikel-Nr.:** ${set.nr}${p}`);
  if (set.beschreibung) console.log(`- **Inhalt:** ${set.beschreibung}`);
  console.log(`- **Shop:** ${set.url}`);
  console.log(`- **Beispielkarten des Design-Teams:** ${set.beispiele.length}`);

  if (mitBilder && set.beispiele.length) {
    const { dir, n } = await speichereBilder(set);
    console.log(`- **Lokal:** \`${dir}/\` (${n} Bilder) — Claude kann sie lesen und die Techniken beschreiben`);
  } else if (set.beispiele.length) {
    set.beispiele.forEach((b, i) => console.log(`  ${i + 1}. ${b}`));
  }
  console.log(`- **Techniken aus den Beispielkarten:** _(noch nicht ausgewertet — Claude fragen)_`);
}
