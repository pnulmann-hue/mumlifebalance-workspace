/* =============================================================
   Vercel API Route: /api/tag
   =============================================================
   Setzt einen ActiveCampaign-Tag fuer einen User wenn er auf
   einen Pitch klickt. Triggert dann eine AC-Automation.

   Request:
   POST /api/tag
   Body: { email, pitch }   // pitch = key aus PITCHES-Map

   Optional — kann leer bleiben wenn der Bot keine AC-Integration
   braucht. Dann wird /api/tag einfach nicht aufgerufen.
   ============================================================= */

export const config = {
  runtime: 'nodejs',
  maxDuration: 30,
};

const TAG_MAP = {
  // Mapping: pitch-key (frontend) → AC_TAG_* env-var
  // Patricia legt die AC-Tags an und traegt die IDs in .env ein.
  mitgliedschaft: 'AC_TAG_MITGLIEDSCHAFT_INTERESSE',
  telegram: 'AC_TAG_IKM_TELEGRAM_KLICK',
  insta: 'AC_TAG_INSTA_DM',
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email, pitch } = req.body || {};

    if (!email || !pitch) {
      return res.status(400).json({ error: 'email und pitch required' });
    }

    const acUrl = process.env.AC_API_URL;
    const acKey = process.env.AC_API_KEY;
    if (!acUrl || !acKey) {
      console.warn('AC nicht konfiguriert — skip tag');
      return res.status(200).json({ skipped: true });
    }

    const tagEnvVar = TAG_MAP[pitch];
    const tagId = tagEnvVar ? process.env[tagEnvVar] : null;
    if (!tagId) {
      console.warn(`Kein Tag fuer pitch=${pitch}`);
      return res.status(200).json({ skipped: true });
    }

    // 1. Contact-ID via E-Mail finden
    const findRes = await fetch(`${acUrl}/api/3/contacts?email=${encodeURIComponent(email)}`, {
      headers: { 'Api-Token': acKey, 'Accept': 'application/json' },
    });
    if (!findRes.ok) throw new Error(`AC contact lookup ${findRes.status}`);
    const findData = await findRes.json();
    const contact = findData.contacts?.[0];
    if (!contact) {
      console.warn('Contact nicht gefunden:', email);
      return res.status(200).json({ skipped: true, reason: 'contact_not_found' });
    }

    // 2. Tag setzen
    const tagRes = await fetch(`${acUrl}/api/3/contactTags`, {
      method: 'POST',
      headers: {
        'Api-Token': acKey,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        contactTag: { contact: contact.id, tag: tagId },
      }),
    });
    if (!tagRes.ok) {
      const errText = await tagRes.text();
      throw new Error(`AC tag set ${tagRes.status}: ${errText}`);
    }

    console.log('Tag gesetzt:', { email, pitch, tagId });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Tag error:', err);
    return res.status(500).json({ error: err.message });
  }
}
