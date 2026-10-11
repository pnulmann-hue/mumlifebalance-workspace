/* =============================================================
   Vercel API Route: /api/health
   Simpler Health-Check + zeigt, welche ENV-Variablen gesetzt sind
   (ohne Werte preiszugeben).
   ============================================================= */

export const config = { runtime: 'nodejs', maxDuration: 10 };

export default function handler(req, res) {
  const env = {
    ANTHROPIC_API_KEY: !!process.env.ANTHROPIC_API_KEY,
    AC_API_URL: !!process.env.AC_API_URL,
    AC_API_KEY: !!process.env.AC_API_KEY,
    AC_LIST_ID: !!process.env.AC_LIST_ID,
    AC_TAG_LEAD: !!process.env.AC_TAG_LEAD,
  };
  return res.status(200).json({ ok: true, service: 'produkt-ideen-finder', env, ts: Date.now() });
}
