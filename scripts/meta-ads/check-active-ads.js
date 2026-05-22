/**
 * Meta-Ads Live-Check
 * ===================
 *
 * Liest alle ACTIVE-Kampagnen + Ad-Sets + Insights via Marketing API und
 * baut einen Markdown-Report nach Julia-Trost-Bewertung:
 *
 *   CTR < 0.5%  ODER  CPL > 15  ODER  Frequency > 2.5      →  🛑 PAUSIEREN
 *   CTR < 1%    UND  Spend > 50  UND  Anmeldungen < 3      →  ⚠️ CREATIVE WECHSELN
 *   CTR > 1.5%  UND  CPL < 8  UND  Frequency < 1.8         →  ✅ SKALIEREN
 *
 * Ausführung lokal:    node --env-file=.env check-active-ads.js
 * Ausführung CI:       node check-active-ads.js  (Secrets via env)
 *
 * Output:
 *   - outputs/ads-runs/YYYY-MM-DD-HHMM.md     (committed)
 *   - outputs/ads-runs/latest.md              (Symlink-Kopie für Skill-Lookup)
 *
 * Schreibt auch ein Alert-File wenn 🛑-Fälle auftreten — wird vom Workflow
 * gelesen und ggf. via Telegram gepusht.
 */

import { writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  listCampaigns,
  listAdSets,
  listAds,
  getInsights,
} from './meta-api.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..', '..');
const OUT_DIR = resolve(REPO_ROOT, 'outputs', 'ads-runs');

const CURRENCY = process.env.META_CURRENCY || 'CHF';
const DAYS = parseInt(process.env.LOOKBACK_DAYS || '3', 10);

// ============================================================
// Julia-Trost-Bewertung
// ============================================================

function evaluate(metrics) {
  const { spend = 0, ctr = 0, cpl = null, frequency = 0, leads = 0, impressions = 0 } = metrics;

  const reasons = [];
  let verdict = '⚪ Beobachten';

  if (impressions < 200) {
    return { verdict: '🆕 Zu früh', reasons: ['<200 Impressions — Algorithmus lernt noch'] };
  }

  if (ctr < 0.5) reasons.push(`CTR ${ctr.toFixed(2)}% < 0.5% — Hook funktioniert nicht`);
  if (cpl !== null && cpl > 15) reasons.push(`CPL ${cpl.toFixed(2)} ${CURRENCY} > 15 — zu teuer`);
  if (frequency > 2.5) reasons.push(`Frequency ${frequency.toFixed(2)} > 2.5 — Audience-Fatigue`);
  if (spend > 50 && leads === 0) reasons.push(`Spend ${spend.toFixed(2)} ${CURRENCY}, 0 Leads — Conversion fehlt komplett`);

  if (reasons.length > 0) {
    verdict = '🛑 PAUSIEREN';
    return { verdict, reasons };
  }

  if (ctr < 1.0 && spend > 50 && leads < 3) {
    return { verdict: '⚠️ Creative wechseln', reasons: [`CTR ${ctr.toFixed(2)}% < 1%, ${leads} Leads bei ${spend.toFixed(2)} ${CURRENCY} Spend`] };
  }

  if (ctr > 1.5 && cpl !== null && cpl < 8 && frequency < 1.8) {
    return { verdict: '✅ SKALIEREN (+20-30% Budget)', reasons: [`CTR ${ctr.toFixed(2)}%, CPL ${cpl.toFixed(2)} ${CURRENCY}, Freq ${frequency.toFixed(2)}`] };
  }

  return { verdict, reasons: ['Metriken stabil — Daten weiter sammeln'] };
}

// ============================================================
// Insights-Helper
// ============================================================

function parseInsights(raw) {
  const i = raw || {};
  const leadAction = i.actions?.find((a) => a.action_type === 'lead')
    || i.actions?.find((a) => a.action_type === 'complete_registration');
  const leads = leadAction ? parseInt(leadAction.value, 10) : 0;
  const spend = parseFloat(i.spend || 0);
  const cpl = leads > 0 ? spend / leads : null;
  return {
    spend,
    impressions: parseInt(i.impressions || 0, 10),
    clicks: parseInt(i.clicks || 0, 10),
    ctr: parseFloat(i.ctr || 0),
    cpc: parseFloat(i.cpc || 0),
    cpm: parseFloat(i.cpm || 0),
    reach: parseInt(i.reach || 0, 10),
    frequency: parseFloat(i.frequency || 0),
    leads,
    cpl,
  };
}

// ============================================================
// Report-Builder
// ============================================================

function fmt(n, dec = 2) {
  return n === null || n === undefined || Number.isNaN(n) ? '—' : Number(n).toFixed(dec);
}

function pad(s, width) {
  return String(s).padEnd(width);
}

async function buildReport() {
  const generatedAt = new Date();
  const isoDate = generatedAt.toISOString().slice(0, 10);
  const isoTime = generatedAt.toISOString().slice(11, 16).replace(':', '');

  const lines = [];
  lines.push('---');
  lines.push('tags: [ads]');
  lines.push('---');
  lines.push('');
  lines.push(`# Meta-Ads Live-Check · ${isoDate} ${generatedAt.toISOString().slice(11, 16)} UTC`);
  lines.push('');
  lines.push(`**Lookback:** letzte ${DAYS} Tag${DAYS === 1 ? '' : 'e'}`);
  lines.push(`**Generated:** ${generatedAt.toISOString()}`);
  lines.push('');

  // Alle Kampagnen holen (alle Status, damit man PAUSED-Kampagnen auch sieht)
  const allCampaigns = await listCampaigns();
  const active = allCampaigns.filter((c) => c.status === 'ACTIVE');
  const paused = allCampaigns.filter((c) => c.status === 'PAUSED');
  const archived = allCampaigns.filter((c) => c.status === 'ARCHIVED' || c.status === 'DELETED');

  lines.push('## Überblick');
  lines.push('');
  lines.push(`- 🟢 **${active.length}** aktive Kampagnen`);
  lines.push(`- ⏸️ **${paused.length}** pausiert`);
  lines.push(`- 📦 **${archived.length}** archiviert/gelöscht`);
  lines.push('');

  if (active.length === 0) {
    lines.push('> **Keine aktiven Kampagnen.** Wenn du dachtest, dass eine Anzeige läuft — sie ist es nicht (mehr).');
    lines.push('');
    if (paused.length > 0) {
      lines.push('### Pausierte Kampagnen (zur Erinnerung)');
      paused.slice(0, 10).forEach((c) => {
        lines.push(`- \`${c.id}\` — ${c.name} (Objective: ${c.objective || '—'})`);
      });
      lines.push('');
    }
  }

  const alerts = [];
  let totalSpend = 0;

  for (const c of active) {
    lines.push(`---`);
    lines.push('');
    lines.push(`## 🟢 ${c.name}`);
    lines.push('');
    lines.push(`- **ID:** \`${c.id}\``);
    lines.push(`- **Objective:** ${c.objective || '—'}`);
    const dailyBudget = c.daily_budget ? `${(parseInt(c.daily_budget) / 100).toFixed(2)} ${CURRENCY}/Tag` : '—';
    lines.push(`- **Daily Budget:** ${dailyBudget}`);
    lines.push(`- **Start:** ${c.start_time || '—'}`);
    if (c.stop_time) lines.push(`- **Stop:** ${c.stop_time}`);
    lines.push('');

    // Kampagnen-Level-Insights
    let cInsights;
    try {
      const raw = await getInsights(c.id, { days: DAYS, level: 'campaign' });
      cInsights = parseInsights(raw[0]);
    } catch (err) {
      lines.push(`> ⚠️ Insights-Fetch fehlgeschlagen: ${err.message.slice(0, 200)}`);
      lines.push('');
      continue;
    }

    totalSpend += cInsights.spend;
    const cVerdict = evaluate(cInsights);

    lines.push(`### Kampagnen-Performance (letzte ${DAYS} Tage)`);
    lines.push('');
    lines.push('| Metrik | Wert |');
    lines.push('|---|---|');
    lines.push(`| Spend | ${fmt(cInsights.spend)} ${CURRENCY} |`);
    lines.push(`| Impressions | ${cInsights.impressions.toLocaleString('de-CH')} |`);
    lines.push(`| Reach | ${cInsights.reach.toLocaleString('de-CH')} |`);
    lines.push(`| Frequency | ${fmt(cInsights.frequency)} |`);
    lines.push(`| Clicks | ${cInsights.clicks} |`);
    lines.push(`| CTR | ${fmt(cInsights.ctr)}% |`);
    lines.push(`| CPC | ${fmt(cInsights.cpc)} ${CURRENCY} |`);
    lines.push(`| CPM | ${fmt(cInsights.cpm)} ${CURRENCY} |`);
    lines.push(`| Leads | ${cInsights.leads} |`);
    lines.push(`| CPL | ${cInsights.cpl === null ? '—' : `${fmt(cInsights.cpl)} ${CURRENCY}`} |`);
    lines.push('');
    lines.push(`**Bewertung:** ${cVerdict.verdict}`);
    cVerdict.reasons.forEach((r) => lines.push(`- ${r}`));
    lines.push('');

    if (cVerdict.verdict.startsWith('🛑')) {
      alerts.push({ campaign: c.name, id: c.id, verdict: cVerdict.verdict, reasons: cVerdict.reasons });
    }

    // Ad-Set-Level
    let adSets = [];
    try {
      adSets = await listAdSets(c.id);
    } catch (err) {
      lines.push(`> ⚠️ Ad-Sets-Fetch fehlgeschlagen: ${err.message.slice(0, 200)}`);
      lines.push('');
    }

    if (adSets.length > 0) {
      lines.push(`### Ad-Sets (${adSets.length})`);
      lines.push('');
      lines.push('| Status | Name | Spend | CTR | CPL | Freq | Leads | Bewertung |');
      lines.push('|---|---|---|---|---|---|---|---|');

      for (const a of adSets) {
        try {
          const raw = await getInsights(a.id, { days: DAYS, level: 'adset' });
          const m = parseInsights(raw[0]);
          const v = evaluate(m);
          const statusIcon = a.status === 'ACTIVE' ? '🟢' : a.status === 'PAUSED' ? '⏸️' : '⚪';
          lines.push(`| ${statusIcon} | ${a.name} | ${fmt(m.spend)} | ${fmt(m.ctr)}% | ${m.cpl === null ? '—' : fmt(m.cpl)} | ${fmt(m.frequency)} | ${m.leads} | ${v.verdict} |`);

          if (v.verdict.startsWith('🛑') && a.status === 'ACTIVE') {
            alerts.push({ campaign: c.name, adSet: a.name, id: a.id, verdict: v.verdict, reasons: v.reasons });
          }
        } catch {
          lines.push(`| ${a.status === 'ACTIVE' ? '🟢' : '⏸️'} | ${a.name} | err | — | — | — | — | — |`);
        }
      }
      lines.push('');
    }
  }

  lines.push('---');
  lines.push('');
  lines.push('## Total');
  lines.push('');
  lines.push(`- **Aktiver Spend (letzte ${DAYS} Tage):** ${fmt(totalSpend)} ${CURRENCY}`);
  lines.push('');

  if (alerts.length > 0) {
    lines.push('## 🛑 Kritische Befunde');
    lines.push('');
    alerts.forEach((a) => {
      const label = a.adSet ? `${a.campaign} → ${a.adSet}` : a.campaign;
      lines.push(`- **${label}** (\`${a.id}\`) — ${a.verdict}`);
      a.reasons.forEach((r) => lines.push(`  - ${r}`));
    });
    lines.push('');
  }

  return { content: lines.join('\n') + '\n', alerts, totalSpend, isoDate, isoTime, activeCount: active.length };
}

// ============================================================
// Main
// ============================================================

async function main() {
  if (!process.env.META_ACCESS_TOKEN) {
    console.error('❌ META_ACCESS_TOKEN fehlt');
    process.exit(1);
  }
  if (!process.env.META_AD_ACCOUNT_ID) {
    console.error('❌ META_AD_ACCOUNT_ID fehlt');
    process.exit(1);
  }

  console.log(`🔎 Lese Meta-Ads (Lookback ${DAYS} Tage)…`);
  const report = await buildReport();

  mkdirSync(OUT_DIR, { recursive: true });
  const filename = `${report.isoDate}-${report.isoTime}.md`;
  const filepath = resolve(OUT_DIR, filename);
  writeFileSync(filepath, report.content, 'utf-8');
  copyFileSync(filepath, resolve(OUT_DIR, 'latest.md'));

  console.log(`✅ Report geschrieben: outputs/ads-runs/${filename}`);
  console.log(`   Aktive Kampagnen: ${report.activeCount}`);
  console.log(`   Total Spend (${DAYS}d): ${report.totalSpend.toFixed(2)} ${CURRENCY}`);
  console.log(`   Kritische Befunde: ${report.alerts.length}`);

  if (report.alerts.length > 0) {
    const alertFile = resolve(OUT_DIR, 'alerts.json');
    writeFileSync(alertFile, JSON.stringify(report.alerts, null, 2), 'utf-8');
    console.log(`   ⚠️ Alerts in: outputs/ads-runs/alerts.json`);
  }
}

main().catch((err) => {
  console.error('❌', err.message);
  process.exit(1);
});
