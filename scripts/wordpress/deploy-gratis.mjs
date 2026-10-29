// Freebie-Übersicht /angebote/gratis/ — alle laufenden 0€-Angebote auf einen Blick (Mentoring).
//
//   cd scripts/wordpress && node --env-file=.env deploy-gratis.mjs [--vorschau]
//
// Idee aus dem Funnel einer Mentorin (29.10.2026): eine Seite, auf der jedes Freebie mit Art, einem Satz
// Nutzen und Knopf steht. Gestaltung mit Inline-Stilen, weil die Firewall <style> im Inhalt blockt;
// Seitenvorlage Standard, damit Kopf- und Fusszeile der Website bleiben. Kindseite von „Angebote“ (3099).
// Quelle der Links: context/link-uebersicht.md. Neue Seite als Entwurf, bestehende behält ihren Status.
import { writeFileSync } from 'node:fs';
import { findPageBySlug, updatePage, createPage } from './wp-api.js';

const GRUPPEN = [
  { titel: 'Tools', art: 'Tool', satz: 'Kleine Helfer, die dir sofort ein Ergebnis geben, statt einer Datei, die du nie öffnest.', karten: [
    ['Nischengenerator', 'Ein paar Fragen zu dir, danach hast du drei Themen, deinen Experten-Satz und Ideen für dein erstes Gratis-Tool.', 'https://mumlifebalance.ch/nischengenerator/'],
    ['Stimm-Check', 'Die Angaben, die deine KI von dir braucht, damit sie klingt wie du, und ein erster Text dazu.', 'https://mumlifebalance.ch/stimm-check/'],
    ['Bio-Check', 'Ein Helfer geht deine Instagram-Bio mit dir durch und macht dir Vorschläge, die zu deinem Thema passen.', 'https://mumlifebalance.ch/bio-check/'],
    ['Produkt-Ideen-Finder', 'Aus deinen Antworten werden konkrete Ideen für dein erstes eigenes Produkt.', 'https://mumlifebalance.ch/produkt-ideen-finder/'],
    ['Freischaufeln', 'In drei Schritten halbierst du deine To-do-Liste und machst Platz für dein Business.', 'https://mumlifebalance.ch/freischaufeln/'],
    ['Potenzial-Test', 'Sieben kurze Fragen, und du weisst, wo dein grösster Wachstumsblocker liegt und welcher Schritt jetzt passt.', 'https://mumlifebalance.ch/potenzial-test/'],
  ]},
  { titel: 'Challenges', art: 'Challenge', satz: 'Ein paar Tage, jeden Tag eine kleine Aufgabe, und am Schluss steht etwas.', karten: [
    ['Story-Challenge', 'Sieben Tage, mit Workbook und Gruppe, bis auf deine Storys wieder jemand antwortet.', 'https://mumlifebalance.ch/story-challenge/'],
    ['Lead-Challenge', 'Drei Tage, in denen du lernst, wie aus Followern Kontakte werden.', 'https://mumlifebalance.ch/lead-challenge/'],
  ]},
  { titel: 'Guides', art: 'Guide', satz: 'Zum Nachlesen, wenn du Schritt für Schritt vorgehen willst.', karten: [
    ['Businessfahrplan', 'In vier Phasen vom Produktposten zu einem eigenen Angebot.', 'https://mumlifebalance.ch/fahrplan/'],
    ['Instagram-Starterguide', 'Schritt für Schritt zu einem Profil, das Anfragen bringt statt nur Likes.', 'https://mumlifebalance.ch/instagram-starterguide/'],
    ['Workbook „Von 0 auf echt“', 'Finde heraus, wofür du stehst, damit dein Profil nach dir klingt.', 'https://mumlifebalance.ch/von-0-auf-echt/'],
  ]},
];

const F = { creme: '#f1ecdd', weiss: '#fbf8f0', blau: '#29556d', petrol: '#12828c', orange: '#dc822e', tinte: '#0c1c30', grau: '#4f5d68', linie: '#dcd3bd' };
const SERIF = "font-family:'Philosopher',Georgia,serif;";
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function karte(art, [name, satz, link]) {
  return `<a href="${link}" style="display:flex;flex-direction:column;gap:6px;background:${F.weiss};border:1.5px solid ${F.linie};border-radius:16px;padding:18px 18px 16px;text-decoration:none;color:${F.tinte};">
  <span style="font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:${F.petrol};">${art} · 0 CHF</span>
  <span style="${SERIF}font-size:22px;line-height:1.2;color:${F.blau};">${esc(name)}</span>
  <span style="font-size:16px;line-height:1.5;color:${F.grau};flex:1;">${esc(satz)}</span>
  <span style="align-self:flex-start;margin-top:8px;background:${F.orange};color:${F.tinte};font-weight:700;border-radius:999px;padding:9px 18px;font-size:15px;">Gratis holen →</span>
</a>`;
}

const html = `<div style="background:${F.creme};padding:36px 16px 56px;font-family:'Source Sans 3','Segoe UI',Arial,sans-serif;color:${F.tinte};">
<div style="max-width:1080px;margin:0 auto;">
  <p style="text-align:center;font-size:14px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${F.petrol};margin:0 0 10px;">Kostenlos</p>
  <h1 style="${SERIF}text-align:center;font-size:clamp(34px,6vw,52px);line-height:1.1;color:${F.blau};margin:0 0 16px;">Alle Gratis-Angebote auf einen Blick</h1>
  <p style="text-align:center;font-size:19px;line-height:1.6;color:${F.grau};max-width:640px;margin:0 auto 22px;">Such dir aus, was dein Business gerade am meisten weiterbringt. Alles kostenlos, für Mamas im Network, die mehr Kontakte und Klarheit in ihr Business bringen wollen.</p>
  <p style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0 0 8px;">${GRUPPEN.map((g) => `<a href="#${g.titel.toLowerCase()}" style="background:${F.weiss};border:1.5px solid ${F.linie};border-radius:999px;padding:7px 16px;font-size:15px;font-weight:700;color:${F.blau};text-decoration:none;">${g.titel}</a>`).join('')}</p>
${GRUPPEN.map((g) => `  <h2 id="${g.titel.toLowerCase()}" style="${SERIF}font-size:28px;color:${F.blau};margin:34px 0 4px;scroll-margin-top:90px;">${g.titel}</h2>
  <p style="font-size:16px;line-height:1.5;color:${F.grau};margin:0 0 14px;">${esc(g.satz)}</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr));gap:14px;">
${g.karten.map((k) => karte(g.art, k)).join('\n')}
  </div>`).join('\n')}
</div>
</div>`;

if (/<style|<script/i.test(html)) throw new Error('<style>/<script> blockt die Firewall');
writeFileSync(new URL('../../outputs/salespages/gratis-uebersicht.html', import.meta.url),
  `<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gratis</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap"></head><body style="margin:0;">${html}</body></html>`);
console.log('→ outputs/salespages/gratis-uebersicht.html');
if (process.argv.includes('--vorschau')) process.exit(0);

// elementor_header_footer: Kopf- und Fusszeile bleiben, ohne Seitentitel und ohne Rand der Vorlage (Handy, 29.10.)
const felder = { title: 'Gratis', slug: 'gratis', parent: 3099, template: 'elementor_header_footer', content: '<!-- wp:html -->\n' + html + '\n<!-- /wp:html -->' };
const bestehend = await findPageBySlug('gratis');
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
