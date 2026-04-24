/**
 * ManyChat REST API Helper
 * =========================
 *
 * Wrapper um die ManyChat Public API fuer mumlifebalance-Profile (Mentoring + doTERRA).
 * Credentials: scripts/manychat/.env (MANYCHAT_API_KEY).
 *
 * API-Referenz: https://api.manychat.com/swagger
 *
 * Was die ManyChat API KANN:
 *   - Subscriber/Contacts verwalten (tags, custom fields, subscriber-info)
 *   - Flows triggern (einen bestehenden Flow an einen Subscriber senden)
 *   - Custom Fields anlegen/lesen
 *   - Tags anlegen/lesen
 *   - Growth Tools (Entry-Points) lesen
 *
 * Was sie NICHT kann:
 *   - Flows komplett programmatisch bauen (drag-drop-Builder ist UI-only)
 *   - Keywords definieren (auch UI-only)
 *   - Comment-Triggers konfigurieren (UI-only)
 *
 * Das heisst: Der Skill kann Subscriber-Daten managen + Flows triggern,
 * aber neue Keywords + Flow-Logic muss manuell im ManyChat-UI gebaut werden.
 *
 * CLI-Modus:
 *   node --env-file=.env mc-api.js <command> [args]
 *
 * Commands:
 *   whoami                         Account + Page-Info
 *   list-tags                      Alle Tags im Account
 *   list-custom-fields             Alle Custom Fields
 *   find-subscriber <value>        Subscriber via ID/email/phone finden
 *   tag-subscriber <id> <tag>      Tag setzen
 *   send-flow <sub-id> <flow-id>   Flow an Subscriber senden
 */

import { readFile } from 'node:fs/promises';

const API_KEY = process.env.MANYCHAT_API_KEY;
const BASE_URL = 'https://api.manychat.com';

if (!API_KEY || API_KEY.startsWith('DEIN-') || API_KEY === 'your-api-key-here') {
  throw new Error(
    'MANYCHAT_API_KEY nicht gesetzt. Traeg ihn in scripts/manychat/.env ein.\n' +
    'Hol den Key via ManyChat → Settings → API → "Generate your API Token"'
  );
}

// ============================================================
// Low-Level Request-Helper
// ============================================================

async function mcRequest(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  };
  const res = await fetch(url, { ...options, headers });
  const body = await res.text();
  if (!res.ok) {
    throw new Error(`ManyChat ${res.status} ${path}: ${body.slice(0, 500)}`);
  }
  try { return JSON.parse(body); } catch { return body; }
}

// ============================================================
// Account + Page
// ============================================================

export async function getPageInfo() {
  return mcRequest('/fb/page/getInfo');
}

// ============================================================
// Tags
// ============================================================

export async function listTags() {
  const res = await mcRequest('/fb/page/getTags');
  return res.data || [];
}

export async function createTag(name) {
  return mcRequest('/fb/page/createTag', {
    method: 'POST',
    body: JSON.stringify({ name }),
  });
}

export async function removeTag(name) {
  return mcRequest('/fb/page/removeTag', {
    method: 'POST',
    body: JSON.stringify({ name }),
  });
}

// ============================================================
// Custom Fields
// ============================================================

export async function listCustomFields() {
  const res = await mcRequest('/fb/page/getCustomFields');
  return res.data || [];
}

export async function createCustomField({ caption, type = 'text', description = '' }) {
  return mcRequest('/fb/page/createCustomField', {
    method: 'POST',
    body: JSON.stringify({ caption, type, description }),
  });
}

// ============================================================
// Subscribers
// ============================================================

export async function findSubscriberByEmail(email) {
  const res = await mcRequest(`/fb/subscriber/findByName?name=${encodeURIComponent(email)}`);
  return res.data?.find((s) => s.email === email) || null;
}

export async function getSubscriberInfo(subscriberId) {
  return mcRequest(`/fb/subscriber/getInfo?subscriber_id=${subscriberId}`);
}

export async function addTagToSubscriber(subscriberId, tagName) {
  return mcRequest('/fb/subscriber/addTagByName', {
    method: 'POST',
    body: JSON.stringify({ subscriber_id: subscriberId, tag_name: tagName }),
  });
}

export async function removeTagFromSubscriber(subscriberId, tagName) {
  return mcRequest('/fb/subscriber/removeTagByName', {
    method: 'POST',
    body: JSON.stringify({ subscriber_id: subscriberId, tag_name: tagName }),
  });
}

export async function setCustomFieldValue(subscriberId, fieldName, value) {
  return mcRequest('/fb/subscriber/setCustomFieldByName', {
    method: 'POST',
    body: JSON.stringify({
      subscriber_id: subscriberId,
      field_name: fieldName,
      field_value: value,
    }),
  });
}

// ============================================================
// Flows
// ============================================================

export async function sendFlow(subscriberId, flowNs) {
  return mcRequest('/fb/sending/sendFlow', {
    method: 'POST',
    body: JSON.stringify({
      subscriber_id: subscriberId,
      flow_ns: flowNs,
    }),
  });
}

export async function sendContent(subscriberId, data) {
  return mcRequest('/fb/sending/sendContent', {
    method: 'POST',
    body: JSON.stringify({
      subscriber_id: subscriberId,
      data,
      message_tag: 'ACCOUNT_UPDATE',
    }),
  });
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
        const info = await getPageInfo();
        console.log(`Page: ${info.data?.name} (ID ${info.data?.id})`);
        console.log(`Category: ${info.data?.category}`);
        break;
      }
      case 'list-tags': {
        const tags = await listTags();
        tags.forEach((t) => console.log(`[${t.id}] ${t.name}`));
        break;
      }
      case 'list-custom-fields': {
        const fields = await listCustomFields();
        fields.forEach((f) => console.log(`[${f.id}] ${f.caption.padEnd(30)} ${f.type}`));
        break;
      }
      case 'tag-subscriber': {
        await addTagToSubscriber(args[0], args[1]);
        console.log(`✅ Tag "${args[1]}" gesetzt an Subscriber ${args[0]}`);
        break;
      }
      default:
        console.error('Unbekannter Command. Verfügbar: whoami, list-tags, list-custom-fields, tag-subscriber');
        process.exit(1);
    }
  };
  run().catch((err) => { console.error('❌', err.message); process.exit(1); });
}
