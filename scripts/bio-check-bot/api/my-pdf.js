/* =============================================================
   Vercel API Route: /api/my-pdf?e=<email>
   =============================================================
   Wird von der AC-Mail verlinkt. Liest die E-Mail aus dem Query-
   Parameter, findet das zuletzt generierte PDF dieses Users in
   Vercel Blob und redirectet direkt auf die (public) Blob-URL.

   Mail in AC nutzt dann:
     https://bio-check-bot.vercel.app/api/my-pdf?e=%EMAIL%

   Kein Custom Field in AC nötig — der Dateiname wird aus der
   E-Mail deterministisch abgeleitet (Hash).
   ============================================================= */

import { head } from '@vercel/blob';
import crypto from 'node:crypto';

export const config = { runtime: 'nodejs', maxDuration: 15 };

function sanitizeFilename(email) {
  const base = email.replace(/[^a-zA-Z0-9@._-]/g, '_');
  const hash = crypto.createHash('sha1').update(email).digest('hex').slice(0, 8);
  return `${base}-${hash}`;
}

export default async function handler(req, res) {
  try {
    const email = (req.query?.e || req.query?.email || '').toString().trim();
    if (!email) {
      return res.status(400).send('Missing email parameter (?e=...)');
    }

    const filename = `bio-checks/${sanitizeFilename(email)}.pdf`;

    // Metadata + URL via head() holen (public Blob URL ist in downloadUrl)
    let blob;
    try {
      blob = await head(filename);
    } catch (err) {
      if (String(err.message).includes('not found') || String(err.message).includes('404')) {
        return res.status(404).send(`
          <html>
            <head><meta charset="utf-8"><title>PDF nicht gefunden</title></head>
            <body style="font-family:system-ui;padding:40px;max-width:600px;margin:0 auto;color:#0c1c30;">
              <h1 style="color:#29556d;">PDF noch nicht bereit</h1>
              <p>Dein Bio-Check-PDF wurde noch nicht generiert.</p>
              <p>Wenn du den Bio-Check-Bot noch nicht durchlaufen hast: <a href="https://bio-check-bot.vercel.app" style="color:#dc822e;">jetzt hier starten</a>.</p>
              <p>Wenn du ihn schon durchlaufen hast und das PDF nicht kommt: Schreib Patricia eine Nachricht auf Instagram (@mumlifebalance_patricia_ulmann).</p>
            </body>
          </html>
        `);
      }
      throw err;
    }

    // Redirect auf das Public Blob (inline PDF im Browser)
    res.setHeader('Cache-Control', 'no-store, max-age=0');
    return res.redirect(302, blob.url);
  } catch (err) {
    console.error('my-pdf error:', err);
    return res.status(500).send('Fehler beim Abrufen des PDFs');
  }
}
