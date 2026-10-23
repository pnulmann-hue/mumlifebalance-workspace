#!/usr/bin/env node
/**
 * Dritter Durchgang auf der Angebote-Seite (/angebote/, WP 3099) — 22.10.2026, Patricia:
 * „KI Kurs gehört für mich unter die 3. Säule und ergänze bitte bei allen grossen Kursen,
 * dass in der MBA das schon dabei ist.“
 *
 *   - Karte „Easy KI“ wandert von Säule 2 (Businessaufbau) in Säule 3 (Mama-Business-Alltag)
 *   - Instagram-Kundenmaschine, Digitale Produktwelt, Mama-CEO und Easy KI tragen denselben
 *     MBA-Satz (Easy KI hatte ihn schon)
 *
 * Setzt angebote-ergaenzen.mjs voraus. Wiederholbar.
 *   node --env-file=.env angebote-mba-hinweis.mjs [--trocken]
 * Danach Elementor → Werkzeuge → „Lösche Dateien und Daten“.
 */

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const SEITE = 3099;
const TROCKEN = process.argv.includes('--trocken');

if (!process.env.WP_APP_PASSWORD) {
  console.error('WP_APP_PASSWORD fehlt — mit --env-file=.env starten.');
  process.exit(1);
}

const api = async (route, options = {}) => {
  const res = await fetch(`${WP}/wp-json/wp/v2/${route}`, {
    ...options,
    headers: { Authorization: AUTH, 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 300) }; }
  return { ok: res.ok, status: res.status, data };
};

const finde = (knoten, id) => {
  for (const e of knoten) {
    if (e.id === id) return e;
    const r = finde(e.elements || [], id);
    if (r) return r;
  }
  return null;
};

const SAEULE_2 = '04c7f1b';
const SAEULE_3 = 'f23c15a';
const MBA_SATZ = 'In der Mum Business Academy ist der Kurs schon mit dabei.';

// Karte über ihren Titel finden (die neuen Karten haben zufällige IDs)
const karteIn = (saeule, titelAnfang) =>
  saeule.elements.find((k) => (k.elements || []).some((e) => e.widgetType === 'heading' && e.settings.title.startsWith(titelAnfang)));

const GROSSE_KURSE = [
  ['f8aba19', 'Instagram Kundenmaschine'],      // Säule 1 liegt unter #positionierung, gesucht wird im ganzen Baum
  [null, 'Vom Network-Wissen zur digitalen Produktwelt'],
  [null, 'Mama-CEO'],
  [null, 'Easy KI'],
];

const seite = await api(`pages/${SEITE}?context=edit`);
if (!seite.ok) { console.error('Seite nicht lesbar:', seite.status); process.exit(1); }
const daten = JSON.parse(seite.data.meta._elementor_data);
const s2 = finde(daten, SAEULE_2);
const s3 = finde(daten, SAEULE_3);
if (!s2 || !s3) { console.error('Säulen nicht gefunden — wurde die Seite im Editor umgebaut?'); process.exit(1); }

const getan = [];

const ki = karteIn(s2, 'Easy KI');
if (ki) {
  s2.elements.splice(s2.elements.indexOf(ki), 1);
  s3.elements.push(ki);
  getan.push('Easy KI → Säule 3');
}

// alle Karten-Container der Seite einsammeln
const karten = [];
const sammle = (n) => { for (const e of n) { if (e.elType === 'container' && (e.elements || []).some((w) => w.widgetType === 'heading') && (e.elements || []).some((w) => w.widgetType === 'button')) karten.push(e); sammle(e.elements || []); } };
sammle(daten);

for (const [, titel] of GROSSE_KURSE) {
  const k = karten.find((c) => c.elements.some((w) => w.widgetType === 'heading' && w.settings.title.startsWith(titel)));
  if (!k) { console.error(`Karte „${titel}“ nicht gefunden`); process.exit(1); }
  const text = k.elements.find((w) => w.widgetType === 'text-editor');
  if (text.settings.editor.includes(MBA_SATZ)) continue;
  text.settings.editor += `<p>${MBA_SATZ}</p>`;
  getan.push(`MBA-Satz: ${titel}`);
}

if (!getan.length) { console.log('Nichts zu tun — alles schon da.'); process.exit(0); }
console.log('Änderungen:\n - ' + getan.join('\n - '));
if (TROCKEN) { console.log('(--trocken: nichts gespeichert)'); process.exit(0); }

const r = await api(`pages/${SEITE}`, { method: 'POST', body: JSON.stringify({ meta: { _elementor_data: JSON.stringify(daten) } }) });
if (!r.ok) { console.error('Speichern fehlgeschlagen:', r.status, JSON.stringify(r.data).slice(0, 300)); process.exit(1); }
console.log('Gespeichert.');
