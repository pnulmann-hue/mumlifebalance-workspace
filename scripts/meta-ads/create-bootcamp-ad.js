/**
 * Bootcamp-Ad-Creator — neue Kampagne + AdSet + Creative + Ad (alles PAUSED)
 * =========================================================================
 *
 * Bewirbt das kostenlose 5-Tage-Mama-Business-Bootcamp (29.6.–3.7.).
 * Zielgruppe = bewährtes Set der letzten Kampagne (Frauen 30–45, CH/AT/DE,
 * Interessen Social-Media-Marketing / Female Entrepreneur / Unternehmerin).
 *
 *   node --env-file=.env create-bootcamp-ad.js
 *
 * Alles wird PAUSED angelegt — Patricia reviewt + aktiviert im Ads Manager.
 */

import { readFileSync, statSync, existsSync } from 'node:fs';
import { basename } from 'node:path';

const API_VERSION = 'v21.0';
const BASE = `https://graph.facebook.com/${API_VERSION}`;
const TOKEN = process.env.META_ACCESS_TOKEN;
const ACC = process.env.META_AD_ACCOUNT_ID;
const PAGE_ID = '100753756193662';
const INSTAGRAM_ID = '17841408625189034';
const LANDING_URL = 'https://mumlifebalance.ch/bootcamp/';
const IMAGE_PATH = 'C:/Users/pnulm/Downloads/bootcamp_ad_customer_magnet.png';

const DAILY_BUDGET_CENTS = 2000;          // CHF 20/Tag
const END_TIME = '2026-06-29T00:00:00+0200'; // läuft bis Ende So 28.6.

if (!TOKEN || !ACC) { console.error('❌ META_ACCESS_TOKEN/ACCOUNT fehlt'); process.exit(1); }
if (!existsSync(IMAGE_PATH)) { console.error(`❌ Visual nicht gefunden: ${IMAGE_PATH}`); process.exit(1); }

const PRIMARY_TEXT = `Wie viele Stunden hast du diese Woche in dein Business gesteckt, ohne dass am Ende etwas Fertiges dabei rauskam?

Ich kenne das selber. Du sitzt abends am Laptop, öffnest fünf Tabs, fängst drei Dinge an und um halb elf machst du den Deckel zu, weil die Kinder morgen früh wieder wach sind.

Ich führe mein Business mit vier Kindern in rund 18 Stunden pro Woche. Möglich macht das ein fester Wochenrhythmus und mittlerweile eine KI, die mir die Hälfte der Arbeit abnimmt. Genau diese KI lernst du im Mama-Business-Bootcamp kennen — sie heisst PIA und ist fünf Tage lang deine Mentorin.

So sieht deine Woche aus:

✅ Tag 1: dein Thema wird klar — PIA schreibt dir deine Bio
✅ Tag 2: deine ersten Hooks, mit denen Interessenten beim Scrollen hängenbleiben
✅ Tag 3: eine Mini-Wochenstruktur, die in dein Mama-Leben passt
✅ Tag 4: deine erste eigene Angebots-Idee
✅ Tag 5: dein roter Faden, der alles verbindet

Fünf Tage, kostenlos, alles in einer Telegram-Gruppe. Morgens kommt von mir ein kurzer Impuls, den Rest machst du in deinem Tempo, wann es zwischen Familie und Alltag passt.

Am Ende der Woche hast du deinen ersten Schritt schwarz auf weiss — und zur Abwechslung mal etwas Fertiges in der Hand.

👉 https://mumlifebalance.ch/bootcamp/`;

const TARGETING = {
  geo_locations: { countries: ['CH', 'AT', 'DE'], location_types: ['frequently_in', 'home', 'recent'] },
  age_min: 30,
  age_max: 45,
  genders: [2], // Frauen
  flexible_spec: [{ interests: [
    { id: '6003389760112', name: 'Social-Media-Marketing' },
    { id: '6003723474182', name: 'Female Entrepreneur Association' },
    { id: '6006944110643', name: 'Unternehmerin' },
  ] }],
  publisher_platforms: ['facebook', 'instagram'],
  facebook_positions: ['feed'],
  instagram_positions: ['stream'],
  targeting_automation: { advantage_audience: 0 }, // 0 = exakte Zielgruppe behalten, kein Auto-Erweitern
};

async function post(path, params) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ ...params, access_token: TOKEN }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${path} → ${res.status}: ${text.slice(0, 600)}`);
  return JSON.parse(text);
}

async function uploadImage() {
  const buf = readFileSync(IMAGE_PATH);
  const name = basename(IMAGE_PATH);
  const form = new FormData();
  form.append('access_token', TOKEN);
  form.append('source', new Blob([buf], { type: 'image/png' }), name);
  const res = await fetch(`${BASE}/${ACC}/adimages`, { method: 'POST', body: form });
  const text = await res.text();
  if (!res.ok) throw new Error(`adimages → ${res.status}: ${text.slice(0, 600)}`);
  const data = JSON.parse(text);
  const key = Object.keys(data.images || {})[0];
  if (!key) throw new Error(`Kein image_hash: ${text}`);
  return data.images[key].hash;
}

(async () => {
  try {
    let campId = process.env.REUSE_CAMPAIGN;
    let adsetId = process.env.REUSE_ADSET;

    if (adsetId) {
      console.log(`♻️  Verwende bestehendes AdSet ${adsetId} (campaign ${campId || 'unbekannt'})`);
    } else {
      console.log('1️⃣  Kampagne anlegen (Traffic, PAUSED)...');
      const camp = await post(`/${ACC}/campaigns`, {
        name: 'Bootcamp Juni 2026 — Kunden finden statt suchen',
        objective: 'OUTCOME_TRAFFIC',
        status: 'PAUSED',
        special_ad_categories: '[]',
        is_adset_budget_sharing_enabled: 'false',
      });
      campId = camp.id;
      console.log(`   ✅ campaign_id: ${campId}`);

      console.log('2️⃣  AdSet anlegen (CHF 20/Tag, bis 28.6., PAUSED)...');
      const adset = await post(`/${ACC}/adsets`, {
        name: 'Cold DACH Frauen 30-45 · Feed · CHF 20/Tag',
        campaign_id: campId,
        daily_budget: String(DAILY_BUDGET_CENTS),
        bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
        billing_event: 'IMPRESSIONS',
        optimization_goal: 'LANDING_PAGE_VIEWS',
        end_time: END_TIME,
        targeting: JSON.stringify(TARGETING),
        status: 'PAUSED',
      });
      adsetId = adset.id;
      console.log(`   ✅ adset_id: ${adsetId}`);
    }

    console.log('3️⃣  Bild hochladen...');
    const hash = await uploadImage();
    console.log(`   ✅ image_hash: ${hash}`);

    console.log('4️⃣  Ad-Creative erstellen...');
    const creative = await post(`/${ACC}/adcreatives`, {
      name: 'Bootcamp Creative — Mix (Zeit-Frust + 5 Tage)',
      object_story_spec: JSON.stringify({
        page_id: PAGE_ID,
        link_data: {
          link: LANDING_URL,
          message: PRIMARY_TEXT,
          name: '5 Tage zum ersten Business-Schritt',
          description: 'Kostenloses Mama-Business-Bootcamp, 29.6.–3.7. · per Telegram, mit PIA.',
          image_hash: hash,
          call_to_action: { type: 'SIGN_UP', value: { link: LANDING_URL } },
        },
      }),
    });
    console.log(`   ✅ creative_id: ${creative.id}`);

    console.log('5️⃣  Ad erstellen (PAUSED)...');
    const ad = await post(`/${ACC}/ads`, {
      name: 'Bootcamp Mix · 4:5 · Kunden finden statt suchen',
      adset_id: adsetId,
      creative: JSON.stringify({ creative_id: creative.id }),
      status: 'PAUSED',
    });
    console.log(`   ✅ ad_id: ${ad.id}`);

    console.log('\n🎉 Fertig — alles als PAUSED-Entwurf angelegt.');
    console.log(`   Kampagne:  ${campId}`);
    console.log(`   AdSet:     ${adsetId}`);
    console.log(`   Ad:        ${ad.id}`);
    console.log('\nReviewen + aktivieren: https://business.facebook.com/adsmanager/');
  } catch (e) {
    console.error('\n❌ Fehler:', e.message);
    process.exit(1);
  }
})();
