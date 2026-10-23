#!/usr/bin/env node
/**
 * Prüft alle veröffentlichten Seiten von mumlifebalance.ch am Computer und am Handy.
 * Patricia, 22.10.2026: „bei einigen seiten ist sie eingezogen bei der ansicht am computer.
 * die ansicht soll bei handy und computer gut aussehen. prüfe bitte auch nochmals alle links
 * zu thrivecart und zu den preisen und ob bei keiner seite noch irgend ein datum steht“
 *
 * Je Seite, ohne etwas zu ändern:
 *   Computer 1440 px — Breite des Textbereichs, Einzug links/rechts, ob er mittig sitzt
 *   Handy 375 px     — seitliches Scrollen, zu kleine Schrift, zu schmale Textspalten
 *   Inhalt           — sichtbarer Text, alle Links, ThriveCart-Links, Preise, Datumsangaben
 *   Bilder           — Bildschirmfoto oben, je Gerät (für die Sichtprüfung)
 *
 * Ausgabe: <ziel>/<slug>.json + <slug>-pc.jpg + <slug>-handy.jpg und uebersicht.json
 *   node --env-file=.env seiten-pruefen.mjs <ziel-ordner> [slug …]
 *
 * Puppeteer kommt aus scripts/karussell-render/node_modules.
 */

import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';

const require = createRequire(new URL('../karussell-render/package.json', import.meta.url));
const puppeteer = require('puppeteer');

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const [ziel, ...nur] = process.argv.slice(2);
if (!ziel || !process.env.WP_APP_PASSWORD) {
  console.error('Aufruf: node --env-file=.env seiten-pruefen.mjs <ziel-ordner> [slug …]');
  process.exit(1);
}
fs.mkdirSync(ziel, { recursive: true });

let seiten = [];
for (let p = 1; p < 6; p++) {
  const r = await fetch(`${WP}/wp-json/wp/v2/pages?status=publish&per_page=100&page=${p}&_fields=id,slug,link,modified,template`, { headers: { Authorization: AUTH } });
  if (!r.ok) break;
  const j = await r.json();
  if (!j.length) break;
  seiten = seiten.concat(j);
}
if (nur.length) seiten = seiten.filter((s) => nur.includes(s.slug));

// Läuft im Browser: Messen und Einsammeln
const messen = () => {
  // Cookie-Banner und andere feste Overlays ausblenden, damit sie nichts verdecken
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if ((s.position === 'fixed' || s.position === 'sticky') && /Privatsph|Cookie|Einwilligung/i.test(el.innerText || '')) el.style.display = 'none';
  }
  const vw = innerWidth;
  const sichtbar = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
  const inHeaderFooter = (el) => !!el.closest('header, footer, .elementor-location-header, .elementor-location-footer, nav');
  const absaetze = [...document.querySelectorAll('p, li, h1, h2, h3')]
    .filter((el) => sichtbar(el) && !inHeaderFooter(el) && (el.innerText || '').trim().length > 40);
  const breiten = absaetze.map((el) => el.getBoundingClientRect()).map((r) => ({ w: Math.round(r.width), l: Math.round(r.left), r: Math.round(vw - r.right) }));
  const median = (a) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
  const schrift = absaetze.filter((el) => el.tagName === 'P' || el.tagName === 'LI').map((el) => parseFloat(getComputedStyle(el).fontSize));
  const links = [...document.querySelectorAll('a[href]')]
    .filter((a) => !inHeaderFooter(a))
    .map((a) => ({ href: a.href, text: (a.innerText || a.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 80) }));
  const main = document.querySelector('main, .elementor[data-elementor-type="wp-page"], .entry-content, #content') || document.body;
  const text = (main.innerText || '').replace(/\n{3,}/g, '\n\n');
  // „Eingezogen“: steht die Seite in einem Kasten statt über die volle Breite?
  // Gemessen an der breitesten Fläche mit eigener Farbe oder eigenem Bild.
  const flaechen = [...main.querySelectorAll('*')].filter((el) => {
    if (!sichtbar(el) || inHeaderFooter(el)) return false;
    const s = getComputedStyle(el);
    const farbig = s.backgroundImage !== 'none' || (s.backgroundColor && !/rgba?\(\s*0,\s*0,\s*0,\s*0\s*\)|transparent/.test(s.backgroundColor) && s.backgroundColor !== 'rgb(255, 255, 255)');
    return farbig && el.getBoundingClientRect().height > 200;
  }).map((el) => Math.round(el.getBoundingClientRect().width));
  return {
    vw,
    scrollBreite: document.documentElement.scrollWidth,
    flaecheMax: flaechen.length ? Math.max(...flaechen) : null,
    textBreiteMedian: median(breiten.map((b) => b.w)),
    einzugLinksMedian: median(breiten.map((b) => b.l)),
    einzugRechtsMedian: median(breiten.map((b) => b.r)),
    schmaleBloecke: breiten.filter((b) => b.w < vw * 0.45).length,
    bloecke: breiten.length,
    schriftMin: schrift.length ? Math.min(...schrift) : null,
    schriftMedian: median(schrift),
    links,
    text,
  };
};

const DATUM = /\b(\d{1,2}\.\s?\d{1,2}\.(\s?20\d\d)?|\d{1,2}\.\s?(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)(\s20\d\d)?|(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s20\d\d|20(2[3-7])\b|(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),?\s+\d{1,2}\.)/g;
const PREIS = /(CHF|Fr\.|€|EUR)\s?\d[\d'’.,]*(\.–|\.-)?|\d[\d'’.,]*\s?(CHF|Franken|€)/g;

const browser = await puppeteer.launch({ headless: 'new' });
const uebersicht = [];

for (const s of seiten) {
  const eintrag = { id: s.id, slug: s.slug, link: s.link, geaendert: s.modified.slice(0, 10), template: s.template || '' };
  try {
    for (const [geraet, breite, hoehe, mobil] of [['pc', 1440, 900, false], ['handy', 375, 812, true]]) {
      const page = await browser.newPage();
      await page.setViewport({ width: breite, height: hoehe, isMobile: mobil, hasTouch: mobil, deviceScaleFactor: 1 });
      if (mobil) await page.setUserAgent('Mozilla/5.0 (Linux; Android 14; SM-S931B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36');
      else await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36');
      const antwort = await page.goto(s.link, { waitUntil: 'networkidle2', timeout: 60000 });
      eintrag.status = antwort?.status();
      // Einblend-Animationen auslösen: einmal durchscrollen
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } scrollTo(0, 0); });
      await new Promise((r) => setTimeout(r, 800));
      const m = await page.evaluate(messen);
      await page.screenshot({ path: path.join(ziel, `${s.slug}-${geraet}.jpg`), type: 'jpeg', quality: 60 });
      eintrag[geraet] = { ...m, links: undefined, text: undefined };
      if (geraet === 'pc') {
        eintrag.text = m.text;
        eintrag.links = m.links;
      }
      await page.close();
    }
    const t = eintrag.text || '';
    eintrag.daten = [...new Set(t.match(DATUM) || [])];
    eintrag.preise = [...new Set(t.match(PREIS) || [])];
    eintrag.thrivecart = [...new Set(eintrag.links.filter((l) => /thrivecart\.com/.test(l.href)).map((l) => l.href.split('?')[0]))];
  } catch (e) {
    eintrag.fehler = String(e.message || e).slice(0, 200);
  }
  fs.writeFileSync(path.join(ziel, `${s.slug}.json`), JSON.stringify(eintrag, null, 1));
  const { text, links, ...kurz } = eintrag;
  uebersicht.push(kurz);
  console.log(`${s.slug.padEnd(36)} pc: Fläche ${eintrag.pc?.flaecheMax ?? '-'} · Text ${eintrag.pc?.textBreiteMedian ?? '-'}px · handy scroll ${eintrag.handy?.scrollBreite ?? '-'} · TC ${eintrag.thrivecart?.length ?? 0} · Daten ${eintrag.daten?.length ?? 0}${eintrag.fehler ? ' · FEHLER ' + eintrag.fehler : ''}`);
}

await browser.close();
fs.writeFileSync(path.join(ziel, 'uebersicht.json'), JSON.stringify(uebersicht, null, 1));
