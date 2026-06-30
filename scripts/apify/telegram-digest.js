#!/usr/bin/env node
// Wöchentliche Konkurrenz-Zusammenfassung per Telegram.
// Liest den neuesten outputs/apify-runs/competitors-*.md, lässt Claude die
// für Patricia relevanten Erkenntnisse herausziehen und schickt sie als
// Telegram-Nachricht. Keine npm-Pakete — nur fetch (wie scrape-competitors.js).

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const RUNS_DIR = path.join(REPO_ROOT, 'outputs', 'apify-runs');

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
const MODEL = 'claude-opus-4-8';

function need(name, val) {
  if (!val) { console.error(`FEHLT: ${name}`); process.exit(1); }
}

async function newestCompetitorMd() {
  const files = await fs.readdir(RUNS_DIR);
  const md = files
    .filter((f) => f.startsWith('competitors-') && f.endsWith('.md'))
    .sort()
    .reverse();
  if (md.length === 0) return null;
  const file = md[0];
  const text = await fs.readFile(path.join(RUNS_DIR, file), 'utf8');
  return { file, text };
}

const SYSTEM = `Du bist Patricias Konkurrenz-Scout. Patricia ist Mama-Unternehmerin (Mentoring für Network-Marketing-Mamas + doTERRA). Du bekommst rohe Instagram-Scrape-Daten ihrer Konkurrentinnen und ziehst daraus die paar Dinge raus, die ihr WIRKLICH helfen.

Schreibe wie eine gute Freundin, die kurz Bescheid gibt: warm, du-Anrede, Schweizer ss (kein ß), keine abgehackten Stakkato-Sätze. Erfinde keine Zahlen — nutze nur, was in den Daten steht.

Halte dich KURZ (Telegram-Nachricht, max ~15 Zeilen). Struktur:
🔎 Diese Woche bei deiner Konkurrenz
- 2-3 konkrete Beobachtungen: wer hat was Erfolgreiches gepostet (Format + grobes Thema/Hook, mit Engagement-Zahl wenn vorhanden)
- 1 Muster: welches Format/welche Hook-Art läuft gerade
💡 Für dich: 1-2 konkrete Content-Ideen, die du daraus ableiten könntest (in deiner Nische, nicht 1:1 kopieren)

Lass Konkurrentinnen ohne Posts/mit 0 Followern im Sample weg (Scrape unvollständig). Keine Vorrede, leg direkt los.`;

async function summarize(md) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1200,
      system: SYSTEM,
      messages: [
        { role: 'user', content: `Hier der aktuelle Konkurrenz-Scrape. Zieh mir die relevanten Erkenntnisse raus:\n\n${md}` },
      ],
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Anthropic API ${res.status}: ${body.slice(0, 500)}`);
  }
  const data = await res.json();
  if (data.stop_reason === 'refusal') throw new Error('Anthropic refusal');
  const text = (data.content || [])
    .filter((b) => b.type === 'text')
    .map((b) => b.text)
    .join('')
    .trim();
  if (!text) throw new Error('Leere Antwort vom Modell');
  return text;
}

async function sendTelegram(text) {
  // Telegram-Limit 4096 Zeichen
  const msg = text.length > 4000 ? text.slice(0, 3990) + '\n…' : text;
  const res = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: msg, disable_web_page_preview: true }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Telegram ${res.status}: ${body.slice(0, 300)}`);
  }
}

async function main() {
  need('ANTHROPIC_API_KEY', ANTHROPIC_API_KEY);
  need('TELEGRAM_BOT_TOKEN', TELEGRAM_BOT_TOKEN);
  need('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID);

  const data = await newestCompetitorMd();
  if (!data) {
    await sendTelegram('🔎 Konkurrenz-Scout: Diese Woche keine Scrape-Daten gefunden — der tägliche Scraper hat (noch) nichts geliefert.');
    console.log('Keine competitors-*.md gefunden — Hinweis gesendet.');
    return;
  }
  console.log(`Nutze ${data.file} (${data.text.length} Zeichen).`);
  const summary = await summarize(data.text);
  const datum = data.file.replace('competitors-', '').replace('.md', '');
  await sendTelegram(`${summary}\n\n— Stand ${datum}`);
  console.log('Zusammenfassung gesendet.');
}

main().catch((err) => { console.error(err.message || err); process.exit(1); });
