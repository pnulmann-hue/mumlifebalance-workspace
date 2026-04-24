/* =============================================================
   Vercel API Route: /api/chat
   =============================================================
   Proxy fuer Claude API. Nimmt messages[] entgegen, haengt
   System-Prompt davor, ruft Anthropic API, liefert Text zurueck.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)

   Request:
   POST /api/chat
   Body: { messages: [{role, content}], user: {name, email} }

   Response:
   { text: string }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

export const config = {
  runtime: 'nodejs',
  maxDuration: 30,
};

let systemPromptCache = null;

async function loadSystemPrompt() {
  if (systemPromptCache) return systemPromptCache;

  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
    join(process.cwd(), 'scripts/bio-check-bot/lib/system-prompt.md'),
  ];

  for (const path of candidates) {
    try {
      const content = await readFile(path, 'utf-8');
      systemPromptCache = content;
      return content;
    } catch {
      // try next
    }
  }
  throw new Error('system-prompt.md nicht gefunden — prüfe den Pfad im Deploy');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { messages = [], user = {} } = req.body || {};

    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'messages required' });
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });
    }

    const systemPrompt = await loadSystemPrompt();
    const userContext = `\n\n---\n**User-Kontext:**\n- Name: ${user.name || '(unbekannt)'}\n- E-Mail: ${user.email || '(nicht übergeben)'}\n\nSprich sie persönlich an, wenn du den Vornamen hast.`;

    const client = new Anthropic({ apiKey });

    const response = await client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 2000,
      system: systemPrompt + userContext,
      messages: messages.map((m) => ({
        role: m.role === 'assistant' ? 'assistant' : 'user',
        content: m.content,
      })),
    });

    const text = response.content
      .filter((block) => block.type === 'text')
      .map((block) => block.text)
      .join('\n')
      .trim();

    return res.status(200).json({ text });
  } catch (err) {
    console.error('Chat error:', err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}
