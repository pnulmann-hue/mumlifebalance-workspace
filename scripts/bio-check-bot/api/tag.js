/* =============================================================
   Vercel API Route: /api/tag
   =============================================================
   Setzt einen ActiveCampaign-Tag beim Pitch-Klick.

   Environment:
   - AC_API_URL, AC_API_KEY
   - AC_TAG_THEMA (61), AC_TAG_EXPERTIN (62),
     AC_TAG_KUNDENMASCHINE (63), AC_TAG_INSTA_DM (64)

   Body: { email: string, pitch: 'thema'|'expertin'|'kundenmaschine'|'insta' }
   ============================================================= */

export const config = { runtime: 'nodejs', maxDuration: 15 };

const PITCH_TO_ENV = {
  thema: 'AC_TAG_THEMA',
  expertin: 'AC_TAG_EXPERTIN',
  kundenmaschine: 'AC_TAG_KUNDENMASCHINE',
  insta: 'AC_TAG_INSTA_DM',
};

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { email, pitch } = req.body || {};
    if (!email || !pitch) return res.status(400).json({ error: 'email + pitch required' });

    const tagEnv = PITCH_TO_ENV[pitch];
    const tagId = tagEnv ? process.env[tagEnv] : null;
    if (!tagId) return res.status(400).json({ error: `unbekannter pitch: ${pitch}` });

    const apiUrl = process.env.AC_API_URL;
    const apiKey = process.env.AC_API_KEY;
    if (!apiUrl || !apiKey) return res.status(500).json({ error: 'AC-Credentials fehlen' });

    // Kontakt finden
    const findRes = await fetch(
      `${apiUrl}/api/3/contacts?email=${encodeURIComponent(email)}`,
      { headers: { 'Api-Token': apiKey, 'Accept': 'application/json' } },
    );
    if (!findRes.ok) {
      console.error('AC find failed', findRes.status, await findRes.text());
      return res.status(500).json({ error: 'Kontakt-Suche fehlgeschlagen' });
    }
    const findData = await findRes.json();
    const contact = findData.contacts?.[0];
    if (!contact) return res.status(404).json({ error: 'Kontakt nicht gefunden' });

    // Tag setzen
    const tagRes = await fetch(`${apiUrl}/api/3/contactTags`, {
      method: 'POST',
      headers: {
        'Api-Token': apiKey,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ contactTag: { contact: contact.id, tag: tagId } }),
    });
    if (!tagRes.ok) {
      console.error('AC tag failed', tagRes.status, await tagRes.text());
      return res.status(500).json({ error: 'Tag-Setzung fehlgeschlagen' });
    }

    return res.status(200).json({ ok: true, contactId: contact.id, tagId });
  } catch (err) {
    console.error('Tag error:', err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}
