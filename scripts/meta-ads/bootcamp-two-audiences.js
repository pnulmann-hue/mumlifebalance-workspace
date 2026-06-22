/**
 * Bootcamp-Anzeige · Facebook-only · zwei Zielgruppen zum A/B-Test
 * ================================================================
 * - AdSet A (bestehend): bewährte Zielgruppe (3 Interessen)
 * - AdSet B (neu): breit, ohne Interessen (Advantage+ sucht selbst)
 * - Ein Creative (Feed 4:5 + FB-Story/Reels 9:16) in beiden AdSets
 * Alles PAUSED. Instagram bewusst weggelassen (IG-Konto noch nicht zugewiesen).
 *
 *   node --env-file=.env bootcamp-two-audiences.js
 */

import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const V = 'v21.0';
const BASE = `https://graph.facebook.com/${V}`;
const TOKEN = process.env.META_ACCESS_TOKEN;
const ACC = process.env.META_AD_ACCOUNT_ID;
const PAGE_ID = '100753756193662';
const LANDING_URL = 'https://mumlifebalance.ch/bootcamp/';

const CAMPAIGN_ID = '120252800999900054';
const ADSET_A = '120252801002370054';            // bestehend (bewährte Zielgruppe)
const END_TIME = '2026-06-29T00:00:00+0200';
const BUDGET_CENTS = 1500;                        // CHF 15/Tag je AdSet

const FEED_IMG = 'C:/Users/pnulm/Downloads/bootcamp_ad_customer_magnet.png';
const STORY_IMG = 'C:/Users/pnulm/Downloads/bootcamp_story_ad_magnet.png';

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

const FB_ONLY = {
  publisher_platforms: ['facebook'],
  facebook_positions: ['feed'],
};

const TARGET_A = {
  geo_locations: { countries: ['CH', 'AT', 'DE'], location_types: ['frequently_in', 'home', 'recent'] },
  age_min: 30, age_max: 45, genders: [2],
  flexible_spec: [{ interests: [{ id: '6003389760112' }, { id: '6003723474182' }, { id: '6006944110643' }] }],
  targeting_automation: { advantage_audience: 0 },
  ...FB_ONLY,
};

const TARGET_B = {
  geo_locations: { countries: ['CH', 'AT', 'DE'], location_types: ['frequently_in', 'home', 'recent'] },
  age_min: 30, age_max: 45, genders: [2],
  targeting_automation: { advantage_audience: 1 }, // breit, Meta erweitert selbst
  ...FB_ONLY,
};

async function post(path, params) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ ...params, access_token: TOKEN }),
  });
  const t = await res.text();
  if (!res.ok) throw new Error(`${path} → ${res.status}: ${t.slice(0, 700)}`);
  return JSON.parse(t);
}
async function upload(p) {
  const form = new FormData();
  form.append('access_token', TOKEN);
  form.append('source', new Blob([readFileSync(p)], { type: 'image/png' }), basename(p));
  const res = await fetch(`${BASE}/${ACC}/adimages`, { method: 'POST', body: form });
  const t = await res.text();
  if (!res.ok) throw new Error(`adimages → ${res.status}: ${t.slice(0, 600)}`);
  const d = JSON.parse(t);
  return d.images[Object.keys(d.images)[0]].hash;
}

(async () => {
  try {
    console.log('1️⃣  Bestehendes AdSet A auf Facebook-only + CHF 15/Tag setzen...');
    await post(`/${ADSET_A}`, { targeting: JSON.stringify(TARGET_A), daily_budget: String(BUDGET_CENTS) });
    console.log('   ✅ AdSet A aktualisiert');

    console.log('2️⃣  Feed-Bild (4:5) hochladen...');
    const feedHash = await upload(FEED_IMG);
    console.log(`   ✅ feed ${feedHash}`);

    console.log('3️⃣  Einfaches Feed-Creative (4:5)...');
    const creative = await post(`/${ACC}/adcreatives`, {
      name: 'Bootcamp Creative — Feed 4:5',
      object_story_spec: JSON.stringify({
        page_id: PAGE_ID,
        link_data: {
          link: LANDING_URL,
          message: PRIMARY_TEXT,
          name: '5 Tage zum ersten Business-Schritt',
          description: 'Kostenloses Mama-Business-Bootcamp, 29.6.–3.7. · per Telegram, mit PIA.',
          image_hash: feedHash,
          call_to_action: { type: 'SIGN_UP', value: { link: LANDING_URL } },
        },
      }),
    });
    console.log(`   ✅ creative ${creative.id}`);

    console.log('4️⃣  Anzeige in AdSet A (bewährte Zielgruppe)...');
    const adA = await post(`/${ACC}/ads`, {
      name: 'Bootcamp · Zielgruppe A (Interessen)',
      adset_id: ADSET_A, creative: JSON.stringify({ creative_id: creative.id }), status: 'PAUSED',
    });
    console.log(`   ✅ ad A ${adA.id}`);

    console.log('5️⃣  AdSet B (breit) anlegen...');
    const adsetB = await post(`/${ACC}/adsets`, {
      name: 'Breit DACH Frauen 30-45 · Feed+Story · CHF 15/Tag',
      campaign_id: CAMPAIGN_ID, daily_budget: String(BUDGET_CENTS),
      bid_strategy: 'LOWEST_COST_WITHOUT_CAP', billing_event: 'IMPRESSIONS',
      optimization_goal: 'LANDING_PAGE_VIEWS', end_time: END_TIME,
      targeting: JSON.stringify(TARGET_B), status: 'PAUSED',
    });
    console.log(`   ✅ AdSet B ${adsetB.id}`);

    console.log('6️⃣  Anzeige in AdSet B (breit)...');
    const adB = await post(`/${ACC}/ads`, {
      name: 'Bootcamp · Zielgruppe B (breit)',
      adset_id: adsetB.id, creative: JSON.stringify({ creative_id: creative.id }), status: 'PAUSED',
    });
    console.log(`   ✅ ad B ${adB.id}`);

    console.log('\n🎉 Fertig — A/B-Zielgruppen-Test, alles PAUSED.');
    console.log(`   Kampagne: ${CAMPAIGN_ID}`);
    console.log(`   AdSet A (Interessen): ${ADSET_A}  → Ad ${adA.id}`);
    console.log(`   AdSet B (breit):      ${adsetB.id}  → Ad ${adB.id}`);
    console.log('   Budget: CHF 15/Tag je AdSet = CHF 30/Tag gesamt');
  } catch (e) {
    console.error('\n❌ Fehler:', e.message);
    process.exitCode = 1;
  }
})();
