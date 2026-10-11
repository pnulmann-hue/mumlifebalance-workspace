/**
 * Verlinkt den "Jetzt starten"-Knopf auf der Seite nach dem Eintragen mit dem
 * echten Tool. Vorher zeigte er auf `#tool-kommt-bald` — also ins Leere.
 *
 * Aufruf:
 *   node --env-file=.env scripts/wordpress/finder-knopf-verlinken.mjs --trocken
 *   node --env-file=.env scripts/wordpress/finder-knopf-verlinken.mjs
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WP = 'https://mumlifebalance.ch/wp-json/wp/v2';
const SEITE = 4085;                       // produkt-ideen-finder-los
const PLATZHALTER = process.env.PLATZHALTER || '#tool-kommt-bald';
const TOOL = process.env.ZIEL || 'https://produkt-ideen-finder-service.vercel.app/';

const env = Object.fromEntries(
  (await fs.readFile(path.join(__dirname, '.env'), 'utf8'))
    .split('\n').filter(l => l.includes('=') && !l.trimStart().startsWith('#'))
    .map(l => { const [k, ...r] = l.split('='); return [k.trim(), r.join('=').trim().replace(/^["']|["']$/g, '')]; })
);
const auth = 'Basic ' + Buffer.from(`${env.WP_USER}:${env.WP_APP_PASSWORD}`).toString('base64');
const trocken = process.argv.includes('--trocken');

const res = await fetch(`${WP}/pages/${SEITE}?context=edit`, { headers: { Authorization: auth } });
if (!res.ok) throw new Error(`Seite ${SEITE} nicht lesbar (HTTP ${res.status})`);
const seite = await res.json();
const alt = seite.content.raw;

const treffer = (alt.match(new RegExp(PLATZHALTER, 'g')) || []).length;
console.log(`Seite: ${seite.title.raw}`);
console.log(`Platzhalter "${PLATZHALTER}" gefunden: ${treffer}x`);
if (!treffer) {
  console.log('Nichts zu tun — der Knopf zeigt schon woandershin.');
  process.exit(0);
}

// Nur den Platzhalter ersetzen, sonst nichts am Inhalt anfassen.
// Der Knopf soll in einem neuen Tab aufgehen, damit die Seite bestehen bleibt.
let neu = alt.replaceAll(`href="${PLATZHALTER}"`, `href="${TOOL}" target="_blank" rel="noopener"`);
neu = neu.replaceAll(PLATZHALTER, TOOL);

console.log(`Laenge vorher ${alt.length}, nachher ${neu.length}`);
if (trocken) {
  const i = neu.indexOf(TOOL);
  console.log('Ausschnitt:', neu.slice(Math.max(0, i - 120), i + 90).replace(/\s+/g, ' '));
  console.log('\nTROCKENLAUF — nichts gespeichert.');
  process.exit(0);
}

const put = await fetch(`${WP}/pages/${SEITE}`, {
  method: 'POST',
  headers: { Authorization: auth, 'Content-Type': 'application/json' },
  body: JSON.stringify({ content: neu }),
});
const text = await put.text();
if (!put.ok) throw new Error(`Speichern fehlgeschlagen (HTTP ${put.status}): ${text.slice(0, 300)}`);
console.log('Gespeichert. Der Knopf zeigt jetzt auf das Tool.');
