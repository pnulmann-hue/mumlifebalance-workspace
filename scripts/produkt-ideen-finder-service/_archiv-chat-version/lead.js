/* =============================================================
   Vercel API Route: /api/lead
   =============================================================
   Lead-Capture fuers Tool: legt in ActiveCampaign einen Kontakt an
   (oder findet den bestehenden), traegt ihn in die Liste ein und
   setzt den Tag "produkt-ideen-finder-lead". Schlaegt weich fehl
   (ok:false), damit das Tool auch ohne AC-Config funktioniert.

   Environment:
   - AC_API_URL, AC_API_KEY
   - AC_LIST_ID  (Liste fuer neue Leads)
   - AC_TAG_LEAD (Tag-ID "produkt-ideen-finder-lead")

   Body: { email: string, name?: string }
   ============================================================= */

export const config = { runtime: 'nodejs', maxDuration: 15 };

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

async function ac(apiUrl, apiKey, path, method = 'GET', body) {
  const res = await fetch(`${apiUrl}/api/3/${path}`, {
    method,
    headers: {
      'Api-Token': apiKey,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json = null;
  try { json = text ? JSON.parse(text) : null; } catch {}
  return { ok: res.ok, status: res.status, json, text };
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { email, name } = req.body || {};
    if (!email || !EMAIL_RE.test(email)) {
      return res.status(400).json({ ok: false, error: 'gueltige email required' });
    }

    const apiUrl = process.env.AC_API_URL;
    const apiKey = process.env.AC_API_KEY;
    // Ohne AC-Config: weich durchwinken, Tool laeuft trotzdem
    if (!apiUrl || !apiKey) {
      console.warn('Lead ohne AC-Config — uebersprungen', { email });
      return res.status(200).json({ ok: false, skipped: 'ac-config-fehlt' });
    }

    // 1. Kontakt anlegen/aktualisieren (sync ist idempotent)
    const firstName = (name || '').trim().split(/\s+/)[0] || '';
    const sync = await ac(apiUrl, apiKey, 'contact/sync', 'POST', {
      contact: { email, firstName },
    });
    if (!sync.ok) {
      console.error('AC contact/sync failed', sync.status, sync.text?.slice(0, 300));
      return res.status(200).json({ ok: false, error: 'ac-sync-failed' });
    }
    const contactId = sync.json?.contact?.id;
    if (!contactId) return res.status(200).json({ ok: false, error: 'keine contactId' });

    // 2. In Liste eintragen (status 1 = subscribed)
    const listId = process.env.AC_LIST_ID;
    if (listId) {
      const l = await ac(apiUrl, apiKey, 'contactLists', 'POST', {
        contactList: { list: listId, contact: contactId, status: 1 },
      });
      if (!l.ok) console.error('AC list add failed', l.status, l.text?.slice(0, 200));
    }

    // 3. Tag setzen
    const tagId = process.env.AC_TAG_LEAD;
    if (tagId) {
      const t = await ac(apiUrl, apiKey, 'contactTags', 'POST', {
        contactTag: { contact: contactId, tag: tagId },
      });
      if (!t.ok) console.error('AC tag failed', t.status, t.text?.slice(0, 200));
    }

    return res.status(200).json({ ok: true, contactId });
  } catch (err) {
    console.error('Lead error:', err);
    return res.status(200).json({ ok: false, error: err.message || 'internal error' });
  }
}
