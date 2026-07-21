/* =============================================================
   Vercel API Route: /api/generate
   =============================================================
   KI-Gehirn für den Produktwelt-Companion. Konversationell:
   führt die Nutzerin in 8 Stufen durch den Bau ihrer Produktwelt.
   Voice/Regeln/Ablauf kommen aus lib/system-prompt.md.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)

   Request:  POST { messages: [{role:'user'|'assistant', content:'...'}] }
   Response: { reply: "<Antwort-Text>" }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = { runtime: 'nodejs', maxDuration: 60 };

const MODEL = 'claude-sonnet-4-5';
const MAX_TURNS = 60; // Sicherheitsnetz gegen zu lange Verläufe

let promptCache = null;
async function loadFile(name) {
  const candidates = [
    join(process.cwd(), 'lib', name),
    join(process.cwd(), 'scripts/produktwelt-companion/lib', name),
  ];
  for (const path of candidates) {
    try { return await readFile(path, 'utf-8'); } catch { /* next */ }
  }
  return null;
}
async function loadSystemPrompt() {
  if (promptCache) return promptCache;
  const sys = await loadFile('system-prompt.md');
  if (!sys) throw new Error('system-prompt.md nicht gefunden');
  const wissen = await loadFile('wissensgrundlage.md');
  promptCache = wissen
    ? `${sys}\n\n---\n\n# WISSENSGRUNDLAGE (wende dieses Wissen bei jeder Stufe an)\n\n${wissen}`
    : sys;
  return promptCache;
}

function sanitizeMessages(messages) {
  if (!Array.isArray(messages)) return null;
  const clean = messages
    .filter((m) => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map((m) => ({ role: m.role, content: m.content.slice(0, 8000) }))
    .slice(-MAX_TURNS);
  // Anthropic braucht als erste Nachricht eine user-Rolle
  while (clean.length && clean[0].role !== 'user') clean.shift();
  return clean.length ? clean : null;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const messages = sanitizeMessages(req.body?.messages);
    if (!messages) return res.status(400).json({ error: 'messages (user/assistant) erforderlich' });

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });

    const systemPrompt = await loadSystemPrompt();
    const client = new Anthropic({ apiKey });

    async function call(attempt = 1) {
      try {
        return await client.messages.create({
          model: MODEL,
          max_tokens: 4000,
          system: systemPrompt,
          messages,
        });
      } catch (err) {
        const transient = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (transient && attempt < 2) { await new Promise((r) => setTimeout(r, 1500)); return call(attempt + 1); }
        throw err;
      }
    }

    const response = await call();
    const reply = response.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n').trim();
    if (!reply) return res.status(502).json({ error: 'Leere Antwort — bitte nochmal.', retryable: true });

    console.log('generate OK', { turns: messages.length, in: response.usage?.input_tokens, out: response.usage?.output_tokens });
    return res.status(200).json({ reply });
  } catch (err) {
    console.error('generate error:', { name: err.name, message: err.message, status: err.status });
    const retryable = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError' || err.name === 'APITimeoutError';
    return res.status(retryable ? 503 : 500).json({ error: 'Hat nicht geklappt — bitte nochmal.', retryable });
  }
}
