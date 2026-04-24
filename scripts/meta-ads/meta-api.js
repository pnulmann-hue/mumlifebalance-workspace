/**
 * Meta (Facebook) Ads API Helper
 * ================================
 *
 * Zwei Funktionen in einem:
 *   1. Marketing API  — Patricia's eigene Ads lesen + vollständig managen
 *      (Kampagnen/AdSets/Ads erstellen, Budget ändern, pausieren, Insights)
 *   2. Ad Library API — Wettbewerbs-Ads durchsuchen (öffentliche Meta Ad Library)
 *
 * Voraussetzungen (Setup siehe README.md):
 *   - Meta App im Developer Portal angelegt
 *   - System User + Access Token mit Permissions:
 *       ads_read, ads_management, business_management, pages_read_engagement
 *   - Ad Account ID (z.B. act_1234567890)
 *   - Im .env: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, optional META_APP_ID
 *
 * CLI:
 *   node --env-file=.env meta-api.js <command> [args]
 *
 * Commands:
 *   whoami                                    Token verifizieren
 *   list-campaigns [status]                  Alle Kampagnen (optional filter)
 *   insights <entity> <id> [days]            Performance-Insights
 *   pause-campaign <id>                      Kampagne pausieren
 *   activate-campaign <id>                   Kampagne aktivieren
 *   set-budget <campaign-id> <amount-chf>    Tagesbudget ändern
 *   competitors <keyword> [country]          Meta Ad Library durchsuchen
 *   page-ads <page-id>                       Alle aktuellen Ads einer Page
 *   analyze [days]                           Auto-Analyse + Empfehlungen
 */

const API_VERSION = 'v21.0';
const BASE_URL = `https://graph.facebook.com/${API_VERSION}`;

const ACCESS_TOKEN = process.env.META_ACCESS_TOKEN;
const AD_ACCOUNT_ID = process.env.META_AD_ACCOUNT_ID; // Format: act_1234567890
const CURRENCY = process.env.META_CURRENCY || 'CHF';

if (!ACCESS_TOKEN) {
  throw new Error('META_ACCESS_TOKEN fehlt in .env. Siehe scripts/meta-ads/README.md für Setup.');
}

// ============================================================
// Low-Level
// ============================================================

async function metaRequest(path, options = {}) {
  const url = `${BASE_URL}${path}${path.includes('?') ? '&' : '?'}access_token=${ACCESS_TOKEN}`;
  const res = await fetch(url, options);
  const body = await res.text();
  if (!res.ok) throw new Error(`Meta API ${res.status} ${path}: ${body.slice(0, 500)}`);
  try { return JSON.parse(body); } catch { return body; }
}

async function metaPost(path, params) {
  const body = new URLSearchParams({ ...params, access_token: ACCESS_TOKEN });
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Meta POST ${res.status} ${path}: ${text.slice(0, 500)}`);
  return JSON.parse(text);
}

// ============================================================
// Marketing API — Patricia's Ad Account
// ============================================================

export async function getMe() {
  return metaRequest('/me?fields=id,name');
}

export async function listCampaigns({ status, limit = 100 } = {}) {
  if (!AD_ACCOUNT_ID) throw new Error('META_AD_ACCOUNT_ID fehlt');
  const fields = 'id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time,created_time';
  let path = `/${AD_ACCOUNT_ID}/campaigns?fields=${fields}&limit=${limit}`;
  if (status) path += `&effective_status=["${status}"]`;
  const res = await metaRequest(path);
  return res.data || [];
}

export async function listAdSets(campaignId) {
  const fields = 'id,name,status,daily_budget,targeting,optimization_goal,bid_strategy,created_time';
  const res = await metaRequest(`/${campaignId}/adsets?fields=${fields}&limit=100`);
  return res.data || [];
}

export async function listAds(adSetId) {
  const fields = 'id,name,status,creative{id,name,title,body,image_url,thumbnail_url},created_time';
  const res = await metaRequest(`/${adSetId}/ads?fields=${fields}&limit=100`);
  return res.data || [];
}

export async function getInsights(entityId, { days = 7, level = 'campaign' } = {}) {
  const fields = 'impressions,clicks,ctr,cpc,cpm,spend,reach,frequency,actions,cost_per_action_type,purchase_roas';
  const datePreset = days <= 1 ? 'today' : days <= 7 ? 'last_7d' : days <= 30 ? 'last_30d' : 'last_90d';
  const res = await metaRequest(`/${entityId}/insights?fields=${fields}&date_preset=${datePreset}&level=${level}`);
  return res.data || [];
}

export async function updateCampaignStatus(campaignId, status) {
  if (!['ACTIVE', 'PAUSED', 'ARCHIVED', 'DELETED'].includes(status)) {
    throw new Error(`Invalid status: ${status}`);
  }
  return metaPost(`/${campaignId}`, { status });
}

export async function setCampaignBudget(campaignId, dailyBudgetChf) {
  // Meta erwartet Budget in Cents
  const cents = Math.round(dailyBudgetChf * 100);
  return metaPost(`/${campaignId}`, { daily_budget: String(cents) });
}

// ============================================================
// Ad Library API — Wettbewerbsanalyse
// ============================================================

export async function searchAdLibrary({ keyword, country = 'DE', limit = 50 }) {
  const fields = 'id,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_descriptions,page_name,page_id,ad_delivery_start_time,ad_delivery_stop_time,impressions,publisher_platforms';
  const path = `/ads_archive?search_terms=${encodeURIComponent(keyword)}&ad_type=ALL&ad_reached_countries=["${country}"]&fields=${fields}&limit=${limit}`;
  const res = await metaRequest(path);
  return res.data || [];
}

export async function getPageAds(pageId, { country = 'DE', limit = 50 }) {
  const fields = 'id,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_descriptions,ad_delivery_start_time,ad_delivery_stop_time,publisher_platforms';
  const path = `/ads_archive?search_page_ids=${pageId}&ad_type=ALL&ad_reached_countries=["${country}"]&fields=${fields}&limit=${limit}`;
  const res = await metaRequest(path);
  return res.data || [];
}

// ============================================================
// Auto-Analyse + Empfehlungen
// ============================================================

export async function analyzePerformance({ days = 7, minRoas = 2.5, maxCplByType = {} } = {}) {
  const campaigns = await listCampaigns();
  const result = {
    generated: new Date().toISOString(),
    days,
    thresholds: { minRoas, maxCplByType },
    overview: { total: campaigns.length, active: 0, paused: 0, totalSpend: 0 },
    recommendations: [],
    winners: [],
    losers: [],
  };

  for (const c of campaigns) {
    if (c.status === 'ACTIVE') result.overview.active++;
    if (c.status === 'PAUSED') result.overview.paused++;

    if (c.status !== 'ACTIVE') continue;

    try {
      const insights = await getInsights(c.id, { days, level: 'campaign' });
      const i = insights[0];
      if (!i) continue;

      const spend = parseFloat(i.spend || 0);
      result.overview.totalSpend += spend;

      const roas = parseFloat(i.purchase_roas?.[0]?.value || 0);
      const leadAction = i.actions?.find((a) => a.action_type === 'lead');
      const leads = leadAction ? parseInt(leadAction.value) : 0;
      const cpl = leads > 0 ? spend / leads : null;

      const enriched = { id: c.id, name: c.name, spend, leads, cpl, roas, objective: c.objective };

      // Winner: ROAS > minRoas
      if (roas >= minRoas) {
        result.winners.push(enriched);
        result.recommendations.push({
          campaignId: c.id,
          action: 'boost',
          reason: `ROAS ${roas.toFixed(2)} >= ${minRoas} → Budget erhöhen (+20-30%)`,
        });
      }

      // Loser: Spend > 50 CHF aber keine Leads oder CPL zu hoch
      if (spend > 50 && (leads === 0 || (cpl && cpl > 50))) {
        result.losers.push(enriched);
        result.recommendations.push({
          campaignId: c.id,
          action: 'pause-or-review',
          reason: leads === 0
            ? `${spend.toFixed(2)} ${CURRENCY} ausgegeben, 0 Leads → Creative/Targeting kritisch überprüfen`
            : `CPL ${cpl.toFixed(2)} ${CURRENCY} zu hoch → Creative wechseln oder pausieren`,
        });
      }
    } catch (err) {
      result.recommendations.push({ campaignId: c.id, action: 'error', reason: err.message.slice(0, 200) });
    }
  }

  return result;
}

// ============================================================
// CLI
// ============================================================

const thisFile = new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const executedFile = process.argv[1]?.replace(/\\/g, '/');

if (executedFile && thisFile.endsWith(executedFile.split('/').pop())) {
  const [cmd, ...args] = process.argv.slice(2);
  const run = async () => {
    switch (cmd) {
      case 'whoami': {
        const me = await getMe();
        console.log(`Meta-User: ${me.name} (ID ${me.id})`);
        console.log(`Ad Account: ${AD_ACCOUNT_ID || 'nicht gesetzt'}`);
        break;
      }
      case 'list-campaigns': {
        const items = await listCampaigns({ status: args[0] });
        items.forEach((c) => console.log(`[${c.id}] ${c.status.padEnd(10)} ${c.objective?.padEnd(20)} ${c.name}`));
        console.log(`\n${items.length} Kampagnen`);
        break;
      }
      case 'insights': {
        const data = await getInsights(args[1], { days: parseInt(args[2] || '7'), level: args[0] || 'campaign' });
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      case 'pause-campaign': {
        await updateCampaignStatus(args[0], 'PAUSED');
        console.log(`✅ Kampagne ${args[0]} pausiert`);
        break;
      }
      case 'activate-campaign': {
        await updateCampaignStatus(args[0], 'ACTIVE');
        console.log(`✅ Kampagne ${args[0]} aktiviert`);
        break;
      }
      case 'set-budget': {
        await setCampaignBudget(args[0], parseFloat(args[1]));
        console.log(`✅ Tagesbudget von ${args[0]} auf ${args[1]} ${CURRENCY}`);
        break;
      }
      case 'competitors': {
        const data = await searchAdLibrary({ keyword: args[0], country: args[1] || 'DE' });
        data.forEach((a) => {
          const body = (a.ad_creative_bodies?.[0] || '').slice(0, 120);
          console.log(`${a.page_name}: "${body}${body.length >= 120 ? '...' : ''}"`);
        });
        console.log(`\n${data.length} Ads gefunden zu "${args[0]}"`);
        break;
      }
      case 'page-ads': {
        const data = await getPageAds(args[0], { country: args[1] || 'DE' });
        data.forEach((a) => {
          const body = (a.ad_creative_bodies?.[0] || '').slice(0, 120);
          console.log(`${a.ad_delivery_start_time}: "${body}${body.length >= 120 ? '...' : ''}"`);
        });
        console.log(`\n${data.length} aktive Ads`);
        break;
      }
      case 'analyze': {
        const report = await analyzePerformance({ days: parseInt(args[0] || '7') });
        console.log('\n📊 Performance-Report');
        console.log(`   Zeitraum: letzte ${report.days} Tage`);
        console.log(`   Aktiv: ${report.overview.active} / Pausiert: ${report.overview.paused}`);
        console.log(`   Total Spend: ${report.overview.totalSpend.toFixed(2)} ${CURRENCY}\n`);

        if (report.winners.length > 0) {
          console.log('🏆 Winners (ROAS >= 2.5):');
          report.winners.forEach((w) => console.log(`   ${w.name}: ROAS ${w.roas.toFixed(2)}, CPL ${w.cpl?.toFixed(2) || '—'} ${CURRENCY}`));
        }
        if (report.losers.length > 0) {
          console.log('\n⚠️ Losers:');
          report.losers.forEach((l) => console.log(`   ${l.name}: Spend ${l.spend.toFixed(2)}, Leads ${l.leads}`));
        }
        console.log('\n💡 Empfehlungen:');
        report.recommendations.forEach((r) => console.log(`   [${r.action}] ${r.campaignId}: ${r.reason}`));
        break;
      }
      default:
        console.error('Commands: whoami, list-campaigns, insights, pause-campaign, activate-campaign, set-budget, competitors, page-ads, analyze');
        process.exit(1);
    }
  };
  run().catch((err) => { console.error('❌', err.message); process.exit(1); });
}
