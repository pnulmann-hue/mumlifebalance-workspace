/* =============================================================
   Vercel API Route: /api/health
   =============================================================
   Health-Check fuer UptimeRobot oder andere Monitore.

   Prueft:
   - Alle Pflicht-ENV-Variables vorhanden?
   - System-Prompt-Datei laedbar? (= Stammverzeichnis korrekt deployed)

   Antwort:
   - 200 OK + { status: "ok", checks: {...} } wenn alles passt
   - 503 Service Unavailable + Details wenn was fehlt

   UptimeRobot ruft die URL auf, prueft auf HTTP 200 — bei 503
   wird Patricia per Mail/Push alarmiert.

   GET /api/health
   ============================================================= */

import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 10 };

const REQUIRED_ENV = [
  'ANTHROPIC_API_KEY',
  'AC_API_URL',
  'AC_API_KEY',
  'AC_TAG_LEAD',
  'AC_TAG_COMPLETED',
  'AC_TAG_THEMA',
  'AC_TAG_EXPERTIN',
  'AC_TAG_KUNDENMASCHINE',
  'AC_TAG_INSTA_DM',
  'BLOB_READ_WRITE_TOKEN',
];

async function checkSystemPromptLoadable() {
  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
    join(process.cwd(), 'scripts/bio-check-bot/lib/system-prompt.md'),
  ];
  for (const path of candidates) {
    try {
      await readFile(path, 'utf-8');
      return { ok: true, path };
    } catch {
      // try next
    }
  }
  return { ok: false, path: null };
}

export default async function handler(req, res) {
  const checks = {
    env: { ok: true, missing: [] },
    systemPrompt: { ok: false, path: null },
    timestamp: new Date().toISOString(),
  };

  for (const key of REQUIRED_ENV) {
    if (!process.env[key]) {
      checks.env.ok = false;
      checks.env.missing.push(key);
    }
  }

  const promptCheck = await checkSystemPromptLoadable();
  checks.systemPrompt = promptCheck;

  const allOk = checks.env.ok && checks.systemPrompt.ok;

  res.setHeader('Cache-Control', 'no-store, max-age=0');
  return res.status(allOk ? 200 : 503).json({
    status: allOk ? 'ok' : 'unhealthy',
    checks,
  });
}
