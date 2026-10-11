/* =============================================================
   Vercel API Route: /api/chat
   =============================================================
   Proxy fuer Claude API. Nimmt messages[] entgegen, haengt
   System-Prompt davor, ruft Anthropic API, liefert Text zurueck.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)

   Request:  POST /api/chat  { messages: [{role, content}], user: {name, email} }
   Response: { text: string }
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const config = { runtime: 'nodejs', maxDuration: 60 };

const __dirname = dirname(fileURLToPath(import.meta.url));
let systemPromptCache = null;

async function loadSystemPrompt() {
  if (systemPromptCache) return systemPromptCache;
  const candidates = [
    join(process.cwd(), 'lib', 'system-prompt.md'),
    join(__dirname, '..', 'lib', 'system-prompt.md'),
    join(process.cwd(), 'scripts/produkt-ideen-finder-service/lib/system-prompt.md'),
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
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { messages = [], user = {} } = req.body || {};
    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'messages required' });
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY nicht gesetzt' });

    const systemPrompt = await loadSystemPrompt();
    const userContext = `\n\n---\n**User-Kontext:**\n- Name: ${user.name || '(unbekannt)'}\n- E-Mail: ${user.email || '(nicht übergeben)'}\n\nSprich sie persönlich an, wenn du den Vornamen hast. Wenn die E-Mail schon bekannt ist, überspring den E-Mail-Schritt am Ende.`;

    const client = new Anthropic({ apiKey });

    async function callAnthropic(attempt = 1) {
      try {
        return await client.messages.create({
          model: 'claude-sonnet-4-5',
          max_tokens: 4000,
          system: systemPrompt + userContext,
          messages: messages.map((m) => ({
            role: m.role === 'assistant' ? 'assistant' : 'user',
            content: m.content,
          })),
        });
      } catch (err) {
        const transient = err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (transient && attempt < 2) {
          await new Promise((r) => setTimeout(r, 1500));
          return callAnthropic(attempt + 1);
        }
        throw err;
      }
    }

    const response = await callAnthropic();

    const text = response.content
      .filter((block) => block.type === 'text')
      .map((block) => block.text)
      .join('\n')
      .trim();

    const usage = response.usage || {};
    console.log('Chat OK:', {
      input: usage.input_tokens,
      output: usage.output_tokens,
      stop_reason: response.stop_reason,
      messages_count: messages.length,
    });

    return res.status(200).json({
      text,
      meta: { retryable: false, stop_reason: response.stop_reason },
    });
  } catch (err) {
    console.error('Chat error:', {
      name: err.name, message: err.message, status: err.status, type: err.error?.type,
    });
    const retryable =
      err.status >= 500 || err.status === 429 ||
      err.name === 'APIConnectionError' || err.name === 'APITimeoutError';
    return res.status(retryable ? 503 : 500).json({
      error: 'Bot-Antwort hat nicht geklappt — bitte nochmal probieren.',
      type: err.name || 'Error',
      retryable,
    });
  }
}
