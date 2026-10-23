// KI-Launch-Seite /stimm-check-los/ (nach der Bestätigung).
// /stimm-check/ baut deploy-stimm-check-lp.mjs (Minikurs-Baukasten, eigenes CSS im Customizer).
// (/ki-masterclass-danke/ hat ein eigenes Skript: deploy-ki-masterclass-danke.mjs)
//
//   cd scripts/wordpress && node --env-file=.env deploy-stimm-check-seiten.mjs
//
// Quelle: outputs/salespages/stimm-check-los.html
// Gestaltung: .pif aus dem Customizer (dieselbe wie beim Produkt-Ideen-Finder), kein eigenes CSS.
// Neue Seiten als Entwurf; eine bestehende Seite behält ihren Status.
import { readFileSync } from 'node:fs';
import { createPage, updatePage, findPageBySlug } from './wp-api.js';

// 🚨 Offene Adressen — solange sie mit '#' beginnen, zeigen die Knöpfe ins Leere.
const TOOL = 'https://stimm-check.vercel.app/';                    // Stimm-Check-Tool auf Vercel
const MASTERCLASS = 'https://mumlifebalance.ch/ki-masterclass/';   // seit 23.10.2026 die Aufzeichnung (vorher Anmeldeformular 69)

const SEITEN = [
  { quelle: '../../outputs/salespages/stimm-check-los.html', slug: 'stimm-check-los', titel: 'Stimm-Check — los geht’s' },
  // /ki-masterclass/ baut seit 26.09. deploy-ki-masterclass-lp.mjs (ki-salespage-Baukasten)
];

for (const s of SEITEN) {
  let html = readFileSync(new URL(s.quelle, import.meta.url), 'utf8');
  html = html.replace(/<!--[\s\S]*?-->\s*/, '');           // Quellkommentar raus
  html = html.replaceAll('{{TOOL}}', TOOL).replaceAll('{{MASTERCLASS}}', MASTERCLASS);
  if (/\{\{[A-Z]+\}\}/.test(html)) throw new Error('Platzhalter übrig in ' + s.slug);
  if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall — ' + s.slug);
  const inhalt = '<!-- wp:html -->\n' + html.trim() + '\n<!-- /wp:html -->';
  const bestehend = await findPageBySlug(s.slug);
  const felder = { title: s.titel, slug: s.slug, content: inhalt, template: 'elementor_canvas' };
  const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
  console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
}
for (const [name, wert] of Object.entries({ TOOL })) {
  if (wert.startsWith('#')) console.log('⚠ ' + name + ' fehlt noch — Knopf zeigt ins Leere, Seite nicht veröffentlichen.');
}
