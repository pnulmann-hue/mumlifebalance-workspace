import { readFileSync } from 'node:fs';

const T = process.env.META_ACCESS_TOKEN;
const ACT = process.env.META_AD_ACCOUNT_ID;
const PAGE = '100753756193662';
const PIXEL = '786558836285851';
const CHECKOUT = 'https://mumlifebalance.thrivecart.com/storyideen/';
const DIR = 'C:/Users/pnulm/Downloads/';
const DESC = 'Sofort-Download für 19 CHF. Für Mamas, die nebenbei ein Business aufbauen.';
const HEADLINE = '90 Storyideen für dein Mama-Business';

const post = (p, params) => fetch('https://graph.facebook.com/v20.0/' + p, { method: 'POST', body: new URLSearchParams({ ...params, access_token: T }) }).then(r => r.json());

const MSG = `Kennst du diesen Moment? Die Kinder schlafen endlich, du hast zum ersten Mal seit Stunden kurz Ruhe – und statt durchzuatmen, sitzt du mit dem Handy da: „Was soll ich bloss in meine Story posten?"

Du willst ja sichtbar sein. Du baust dir als Mama nebenbei was Eigenes auf, und tief drin weisst du: deine Story ist der Ort, wo Menschen dir vertrauen, dich anschreiben, bei dir kaufen.

Aber jeden Abend neu was Kluges auszudenken? Dafür hast du zwischen Wäsche, Znüni und Gutenachtgeschichte einfach keinen Kopf mehr.

Also postest du wieder den Kaffee. Oder gar nichts. Und das schlechte Gewissen nimmst du gleich mit ins Bett.

Ich kenn das so gut. Genau deshalb gibt's meine 90 Storyideen.

📲 Jeden Tag schnappst du dir eine Idee – zu jeder gibt's ein Beispiel, damit du sofort siehst, wie's aussieht. Nachmachen, posten, fertig. In zwei Minuten statt einer halben Stunde.

✅ 90 sofort umsetzbare Ideen, mit Beispiel zu jeder
✅ für Mamas im Network & Onlinebusiness
✅ Sofort-Download aufs Handy · 19 CHF

An der Kasse wartet noch eine Content-Box, mit der du gleich wochenweise vorbereitet bist.

Ich bin Patricia, Mama von vier Kindern – und ich hab mir mein Business genau in diesen kleinen Zeitfenstern aufgebaut.

👉 Hol dir die 90 Storyideen und mach dir die Abende wieder leicht.`;

const IMAGES = [
  { file: 'storyideen_ad_quadrat_01_2minuten.png', name: 'Storyideen Verkauf · Bild 01 (2 Minuten)' },
  { file: 'storyideen_ad_quadrat_02_baelle.png', name: 'Storyideen Verkauf · Bild 02 (Bälle)' },
  { file: 'storyideen_ad_orange_variant_zeitersparnis.png', name: 'Storyideen Verkauf · Bild 03 (Orange)' },
];

// 1) Kampagne: Ziel VERKÄUFE (aktiv, aber Anzeigen pausiert → kein Spend)
const camp = await post(ACT + '/campaigns', {
  name: 'Storyideen · Verkauf (Mama nebenbei)',
  objective: 'OUTCOME_SALES',
  special_ad_categories: JSON.stringify([]),
  is_adset_budget_sharing_enabled: 'false',
  status: 'ACTIVE',
});
console.log('KAMPAGNE:', camp.id || JSON.stringify(camp));
if (!camp.id) process.exit(1);

// 2) Anzeigengruppe: optimiert auf KAUF, broad + Advantage, Frauen DACH
const targeting = { geo_locations: { countries: ['CH', 'AT', 'DE'] }, genders: [2], age_min: 25, age_max: 65, targeting_automation: { advantage_audience: 1 } };
const adset = await post(ACT + '/adsets', {
  name: 'Kauf · Frauen DACH · broad+Advantage',
  campaign_id: camp.id,
  daily_budget: 2000, // 20 CHF/Tag
  billing_event: 'IMPRESSIONS',
  optimization_goal: 'OFFSITE_CONVERSIONS',
  bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
  destination_type: 'WEBSITE',
  promoted_object: JSON.stringify({ pixel_id: PIXEL, custom_event_type: 'PURCHASE' }),
  targeting: JSON.stringify(targeting),
  is_adset_budget_sharing_enabled: 'false',
  status: 'ACTIVE',
});
console.log('AD-SET:', adset.id || JSON.stringify(adset));
if (!adset.id) process.exit(1);

// 3) Pro Bild: hochladen → Creative → Anzeige (PAUSIERT)
for (const im of IMAGES) {
  const buf = readFileSync(DIR + im.file);
  const fd = new FormData();
  fd.append('filename', new Blob([buf]), im.file);
  fd.append('access_token', T);
  const up = await fetch('https://graph.facebook.com/v20.0/' + ACT + '/adimages', { method: 'POST', body: fd }).then(r => r.json());
  const hash = up.images ? Object.values(up.images)[0].hash : null;
  if (!hash) { console.log(im.name, 'BILD-FEHLER:', JSON.stringify(up.error || up)); continue; }
  const oss = { page_id: PAGE, link_data: { message: MSG, link: CHECKOUT, name: HEADLINE, description: DESC, image_hash: hash, call_to_action: { type: 'SHOP_NOW' } } };
  const cr = await post(ACT + '/adcreatives', { name: im.name + ' · Creative', object_story_spec: JSON.stringify(oss) });
  if (!cr.id) { console.log(im.name, 'CREATIVE-FEHLER:', JSON.stringify(cr.error || cr)); continue; }
  const ad = await post(ACT + '/ads', { name: im.name, adset_id: adset.id, creative: JSON.stringify({ creative_id: cr.id }), status: 'PAUSED' });
  console.log(im.name, '→ AD:', ad.id || JSON.stringify(ad.error || ad));
}
console.log('\\nFERTIG. Kampagne', camp.id, '— Anzeigen PAUSIERT (kein Spend, bis du freigibst).');
