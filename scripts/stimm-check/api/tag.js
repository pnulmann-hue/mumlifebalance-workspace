/* =============================================================
   Vercel API Route: /api/tag
   =============================================================
   Setzt einen ActiveCampaign-Tag (Abschluss + Interesse-Klicks).

   Environment:
   - AC_API_URL, AC_API_KEY
   - AC_TAG_ABGESCHLOSSEN   (Plan generiert)
   - AC_TAG_MASTERCLASS_INTERESSE (CTA-Klick → Masterclass)
   - AC_TAG_KURS_INTERESSE (CTA-Klick → KI-Kurs)

   Body: { email: string, tag: 'abgeschlossen'|'masterclass'|'kurs' }
   ============================================================= */

export const config = { runtime: 'nodejs', maxDuration: 15 };

const TAG_TO_ENV = {
  abgeschlossen: 'AC_TAG_ABGESCHLOSSEN',
  masterclass: 'AC_TAG_MASTERCLASS_INTERESSE',
  kurs: 'AC_TAG_KURS_INTERESSE',
};

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  try {
    const { email, tag } = req.body || {};
    if (!email || !tag) return res.status(400).json({ error: 'email + tag required' });

    const tagId = TAG_TO_ENV[tag] ? process.env[TAG_TO_ENV[tag]] : null;
    if (!tagId) return res.status(400).json({ error: `unbekannter tag: ${tag}` });

    const apiUrl = process.env.AC_API_URL;
    const apiKey = process.env.AC_API_KEY;
    if (!apiUrl || !apiKey) return res.status(500).json({ error: 'AC-Credentials fehlen' });

    const findRes = await fetch(`${apiUrl}/api/3/contacts?email=${encodeURIComponent(email)}`, {
      headers: { 'Api-Token': apiKey, 'Accept': 'application/json' },
    });
    if (!findRes.ok) return res.status(500).json({ error: 'Kontakt-Suche fehlgeschlagen' });
    const contact = (await findRes.json()).contacts?.[0];
    if (!contact) return res.status(404).json({ error: 'Kontakt nicht gefunden' });

    const tagRes = await fetch(`${apiUrl}/api/3/contactTags`, {
      method: 'POST',
      headers: { 'Api-Token': apiKey, 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ contactTag: { contact: contact.id, tag: tagId } }),
    });
    if (!tagRes.ok) return res.status(500).json({ error: 'Tag-Setzung fehlgeschlagen' });

    return res.status(200).json({ ok: true, contactId: contact.id, tagId });
  } catch (err) {
    console.error('Tag error:', err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}
