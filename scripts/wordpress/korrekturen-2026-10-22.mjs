#!/usr/bin/env node
/**
 * Reine Korrekturen aus der Website-Prüfung vom 22.10.2026 (outputs/sonstige/2026-10-22-website-pruefung.md).
 * Kein neuer Text, nur falsche Werte:
 *   /bio/                         „Mini-Kurs · 37 CHF“  → 39 (Kasse eigene-produkterstellung nimmt 39)
 *   /dankesseite-potenzial-quiz/  „CHF 37“              → 39 (Kasse thema-finden nimmt 39)
 *   /mama-ceo/                    Link /instagram-kundenmaschine (404) → ThriveCart-Kasse
 *
 * Sucht in post_content UND in _elementor_data, ändert nur, was genau passt, und liest zurück.
 * Status wird nie mitgeschickt.
 *   node --env-file=.env korrekturen-2026-10-22.mjs [--trocken]
 */

const WP = process.env.WP_URL?.replace(/\/$/, '');
const AUTH = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const TROCKEN = process.argv.includes('--trocken');

const api = async (route, options = {}) => {
  const res = await fetch(`${WP}/wp-json/wp/v2/${route}`, {
    ...options,
    headers: { Authorization: AUTH, 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text.slice(0, 200) }; }
  return { ok: res.ok, status: res.status, data };
};

const KORREKTUREN = [
  { id: 3504, name: 'bio', ersetzen: [['Mini-Kurs · 37 CHF', 'Mini-Kurs · 39 CHF']] },
  { id: 3335, name: 'dankesseite-potenzial-quiz', ersetzen: [['CHF 37', 'CHF 39'], ['<span class="price-main">37</span>', '<span class="price-main">39</span>'], ['<sup>CHF</sup>37<', '<sup>CHF</sup>39<']] },
  { id: 3444, name: 'mama-ceo', ersetzen: [['https://mumlifebalance.ch/instagram-kundenmaschine"', 'https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/"']] },
];

// Elementor-Daten sind JSON mit \/ und · — deshalb entschlüsselt ersetzen, nicht im Rohtext
const ersetzeTief = (wert, alt, neu, zaehler) => {
  if (typeof wert === 'string') { const n = wert.split(alt).length - 1; zaehler.n += n; return n ? wert.split(alt).join(neu) : wert; }
  if (Array.isArray(wert)) return wert.map((w) => ersetzeTief(w, alt, neu, zaehler));
  if (wert && typeof wert === 'object') { for (const k of Object.keys(wert)) wert[k] = ersetzeTief(wert[k], alt, neu, zaehler); }
  return wert;
};

for (const k of KORREKTUREN) {
  const s = await api(`pages/${k.id}?context=edit`);
  if (!s.ok) { console.log(`${k.name}: nicht lesbar (${s.status})`); continue; }
  const felder = {};
  let content = s.data.content.raw || '';
  const roh = s.data.meta?._elementor_data || '';
  let elementor = roh ? JSON.parse(roh) : null;
  const zaehl = [];
  let eGeaendert = false;
  for (const [alt, neu] of k.ersetzen) {
    const nc = content.split(alt).length - 1;
    if (nc) { content = content.split(alt).join(neu); }
    const z = { n: 0 };
    if (elementor) elementor = ersetzeTief(elementor, alt, neu, z);
    if (z.n) eGeaendert = true;
    zaehl.push(`„${alt.slice(0, 40)}“ ${nc}× Inhalt, ${z.n}× Elementor`);
  }
  if (content !== (s.data.content.raw || '')) felder.content = content;
  if (eGeaendert) felder.meta = { _elementor_data: JSON.stringify(elementor) };
  console.log(`${k.name}: ${zaehl.join(' · ')}`);
  if (!Object.keys(felder).length || TROCKEN) continue;
  const r = await api(`pages/${k.id}`, { method: 'POST', body: JSON.stringify(felder) });
  console.log(`  → ${r.ok ? '✓ gespeichert' : `✗ ${r.status} ${JSON.stringify(r.data).slice(0, 100)}`}`);
}
