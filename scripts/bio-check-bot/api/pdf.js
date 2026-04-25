/* =============================================================
   Vercel API Route: /api/pdf
   =============================================================
   Generiert PDF aus Chat-History und triggert AC-Mail-Versand.

   Flow:
   1. Empfange {email, name, messages[]}
   2. Baue PDF mit PDFKit (Patricia-Brand)
   3. Upload zu Vercel Blob → öffentliche URL
   4. Update AC-Contact: Custom Field "bio_check_pdf_url" = URL
   5. Setze AC-Tag "Bio-Check abgeschlossen" (ID 60)
      → triggert AC-Automation mit PDF-Link-Mail

   Environment:
   - BLOB_READ_WRITE_TOKEN (Vercel Blob)
   - AC_API_URL, AC_API_KEY
   - AC_TAG_COMPLETED (60), AC_FIELD_PDF_URL (Custom Field ID)
   ============================================================= */

import PDFDocument from 'pdfkit';
import { put } from '@vercel/blob';
import crypto from 'node:crypto';

export const config = { runtime: 'nodejs', maxDuration: 60 };

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { email, name, messages = [] } = req.body || {};
    if (!email) return res.status(400).json({ error: 'email required' });

    // 1. PDF generieren
    const pdfBuffer = await generatePDF({ name: name || '', messages });

    // 2. Upload zu Vercel Blob — DETERMINISTISCHER Dateiname (pro E-Mail immer gleich, wird ueberschrieben)
    // Damit /api/my-pdf?e=EMAIL das aktuelle PDF des Users findet ohne Custom Field in AC
    const filename = `bio-checks/${sanitizeFilename(email)}.pdf`;
    const blob = await put(filename, pdfBuffer, {
      access: 'public',
      contentType: 'application/pdf',
      addRandomSuffix: false,
      allowOverwrite: true,
    });
    const pdfUrl = blob.url;

    // 3. AC: Contact finden
    const contact = await acFindContact(email);
    if (!contact) return res.status(404).json({ error: 'Kontakt nicht in AC gefunden' });

    // 4. Custom Field setzen (wenn konfiguriert)
    if (process.env.AC_FIELD_PDF_URL) {
      await acSetFieldValue(contact.id, process.env.AC_FIELD_PDF_URL, pdfUrl);
    }

    // 5. Tag "abgeschlossen" setzen → triggert AC-Mail-Automation
    if (process.env.AC_TAG_COMPLETED) {
      await acAddTag(contact.id, process.env.AC_TAG_COMPLETED);
    }

    return res.status(200).json({ ok: true, pdfUrl, contactId: contact.id });
  } catch (err) {
    console.error('PDF error:', err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}

// =============================================================
// Text-Cleanup: Emojis + Markdown raus, bevor PDFKit das Helvetica-
// Standard-Encoding zerschiesst (Helvetica unterstuetzt kein Unicode).
// =============================================================

const EMOJI_RE = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F700}-\u{1F77F}]|[\u{1F780}-\u{1F7FF}]|[\u{1F800}-\u{1F8FF}]|[\u{1F900}-\u{1F9FF}]|[\u{1FA00}-\u{1FA6F}]|[\u{1FA70}-\u{1FAFF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{2300}-\u{23FF}]|[\u{2B00}-\u{2BFF}]|[\u{1F000}-\u{1F02F}]|[\u{1F0A0}-\u{1F0FF}]|[\u{1F100}-\u{1F1FF}]|[\u{200D}\u{FE0F}\u{20E3}]/gu;

function cleanText(raw) {
  if (!raw) return '';
  return raw
    // Bot-Marker raus
    .replace(/\[\[BUTTON:[^\]]+\]\]/gi, '')
    .replace(/\[\[PITCH:[^\]]+\]\]/gi, '')
    .replace(/\[\[DONE\]\]/gi, '')
    // Markdown raus
    .replace(/```[\s\S]*?```/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*\n]+)\*/g, '$1')
    .replace(/__([^_\n]+)__/g, '$1')
    .replace(/^>\s*/gm, '')
    .replace(/^#{1,6}\s+/gm, '')
    // %%%-Trenner zu sauberer Linie
    .replace(/^%[%\s]*$/gm, '———')
    // Emojis raus (Helvetica kann sie nicht rendern)
    .replace(EMOJI_RE, '')
    // Whitespace normalisieren
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// Heuristik: erkennt Section-Marker am Anfang einer Bot-Antwort,
// damit wir grosse Headlines im PDF setzen koennen.
function detectSection(text) {
  const firstLine = text.split('\n')[0].slice(0, 100).toLowerCase();
  if (/(meine analyse|analyse deiner bio)/.test(firstLine)) return 'Deine Bio-Analyse';
  if (/(deine ersten? \d? ?bio-varianten|bio-varianten — copy-paste)/.test(firstLine)) return 'Deine Bio-Varianten';
  if (/(3 paar schuhen|pinned posts?|deine pinned)/.test(firstLine)) return 'Deine Pinned Posts';
  if (/(deine highlights|regale in deinem laden)/.test(firstLine)) return 'Deine Highlights';
  return null;
}

// =============================================================
// PDF-Generator
// =============================================================

function generatePDF({ name, messages }) {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({
      size: 'A4',
      margins: { top: 60, bottom: 60, left: 60, right: 60 },
    });

    const chunks = [];
    doc.on('data', (c) => chunks.push(c));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);

    const colors = {
      petrol: '#12828c',
      dunkelblau: '#29556d',
      creme: '#f1ecdd',
      cremeLight: '#faf6ec',
      orange: '#dc822e',
      text: '#0c1c30',
      muted: '#6b6052',
      divider: '#d8cfb6',
    };

    const today = new Date().toLocaleDateString('de-CH', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
    });

    // === COVER ===
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);

    // Akzent-Linie oben links
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, 80).lineTo(120, 80).stroke();

    // Brand-Label
    doc.fillColor(colors.petrol).font('Helvetica-Bold').fontSize(10)
      .text('MUM LIFE BALANCE  ·  BIO-CHECK', 60, 95, { characterSpacing: 2 });

    // Big Title
    doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(48)
      .text('Dein\nBio-Check', 60, 240, { lineGap: 6 });

    // Subtitle
    doc.fillColor(colors.petrol).fontSize(20).font('Helvetica')
      .text('für Network-Mamas', 60, 380);

    // Personalisierung
    if (name) {
      doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(14)
        .text(`Persönlich für ${name}`, 60, 460);
    }

    doc.fillColor(colors.muted).font('Helvetica').fontSize(11)
      .text(today, 60, name ? 482 : 460);

    // Footer Cover
    doc.fillColor(colors.text).font('Helvetica-Bold').fontSize(11)
      .text('Patricia Ulmann', 60, doc.page.height - 110);
    doc.fillColor(colors.muted).font('Helvetica').fontSize(10)
      .text('Mentorin für Mamas im Network Marketing', 60, doc.page.height - 92);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, doc.page.height - 70).lineTo(120, doc.page.height - 70).stroke();

    // === ANALYSE & BIO-VARIANTEN ===
    doc.addPage();
    doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');

    doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(28)
      .text('Deine Bio-Analyse', 60, 60);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, 105).lineTo(110, 105).stroke();

    doc.moveDown(2);
    doc.fillColor(colors.muted).font('Helvetica-Oblique').fontSize(10)
      .text(`Generiert am ${today}  ·  Aussuchen, einsetzen, fertig`);

    doc.moveDown(2);

    // Bot-Antworten rendern
    const botMessages = messages.filter((m) => m.role === 'assistant');
    let lastSection = 'Deine Bio-Analyse';

    botMessages.forEach((msg, idx) => {
      const text = cleanText(msg.content);
      if (!text) return;

      // Section-Header wenn neuer Abschnitt erkannt wird
      const section = detectSection(text);
      if (section && section !== lastSection) {
        doc.moveDown(1.5);
        if (doc.y > doc.page.height - 200) doc.addPage();
        doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(20)
          .text(section, { align: 'left' });
        doc.strokeColor(colors.orange).lineWidth(3)
          .moveTo(60, doc.y + 4).lineTo(110, doc.y + 4).stroke();
        doc.moveDown(1.5);
        lastSection = section;
      } else if (idx > 0) {
        // Sanfte Trennung zwischen Messages innerhalb derselben Section
        doc.moveDown(0.8);
        doc.strokeColor(colors.divider).lineWidth(0.5)
          .moveTo(180, doc.y).lineTo(doc.page.width - 180, doc.y).stroke();
        doc.moveDown(0.8);
      }

      doc.fillColor(colors.text).font('Helvetica').fontSize(11)
        .text(text, { align: 'left', lineGap: 4, paragraphGap: 6 });
    });

    // === PITCHES (Karten-Layout) ===
    doc.addPage();
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);

    doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(28)
      .text('Deine nächsten Schritte', 60, 80);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, 125).lineTo(110, 125).stroke();

    doc.moveDown(2);
    doc.fillColor(colors.muted).font('Helvetica-Oblique').fontSize(11)
      .text('Nach deiner Bio kommt die Frage: Wie schreibst du jetzt Content, der wirklich verkauft? Drei Wege — je nachdem, wo du gerade stehst.', {
        width: doc.page.width - 120, lineGap: 3,
      });

    doc.moveDown(2);

    const pitches = [
      {
        title: 'Finde dein Thema als Network-Mama',
        price: '39 CHF',
        promise: 'Du öffnest morgens Instagram und weisst sofort, worüber du schreibst — weil dein Thema klar ist.',
        url: 'https://mumlifebalance.thrivecart.com/thema-finden/',
      },
      {
        title: 'Expertin statt Verkäuferin',
        price: '97 CHF',
        promise: 'In 3 Monaten: Fremde schreiben dir „Du hast mich endlich verstanden." Du verkaufst nicht mehr — du wirst empfohlen.',
        url: 'https://mumlifebalance.thrivecart.com/expertin/',
      },
      {
        title: 'Instagram-Kundenmaschine',
        price: '333 CHF',
        promise: 'In 8 Wochen: Dein Business läuft. Aus Reaktionen werden Gespräche, aus Gesprächen Kundinnen.',
        url: 'https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/',
      },
    ];

    pitches.forEach((p) => {
      const cardY = doc.y;
      const cardWidth = doc.page.width - 120;
      const cardHeight = 100;

      // Karten-Hintergrund
      doc.roundedRect(60, cardY, cardWidth, cardHeight, 8).fill('#ffffff');
      // Akzent-Strich links
      doc.rect(60, cardY, 4, cardHeight).fill(colors.orange);

      // Titel
      doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(14)
        .text(p.title, 80, cardY + 16, { width: cardWidth - 100 });

      // Preis (rechts oben)
      doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(14)
        .text(p.price, 60, cardY + 16, { align: 'right', width: cardWidth - 20 });

      // Promise
      doc.fillColor(colors.text).font('Helvetica').fontSize(10)
        .text(p.promise, 80, cardY + 44, { width: cardWidth - 40, lineGap: 2 });

      // Link
      doc.fillColor(colors.petrol).font('Helvetica-Oblique').fontSize(9)
        .text(p.url, 80, cardY + cardHeight - 22, {
          width: cardWidth - 40, link: p.url, underline: true,
        });

      doc.y = cardY + cardHeight + 14;
    });

    // Closing
    doc.moveDown(1.5);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, doc.y).lineTo(120, doc.y).stroke();
    doc.moveDown(0.8);

    doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(11)
      .text(
        'Du machst das nicht, um dein Upline-Team zu beeindrucken. Du machst das, damit du deine Kinder selbst betreuen kannst und trotzdem dein eigenes Einkommen hast. Genau dafür.',
        60, doc.y, { align: 'left', width: doc.page.width - 120, lineGap: 3 },
      );

    doc.moveDown(0.8);
    doc.fillColor(colors.petrol).font('Helvetica-Bold').fontSize(14)
      .text('— Patricia', { align: 'left' });

    doc.end();
  });
}

// =============================================================
// ActiveCampaign helpers
// =============================================================

async function acFindContact(email) {
  const res = await fetch(
    `${process.env.AC_API_URL}/api/3/contacts?email=${encodeURIComponent(email)}`,
    { headers: { 'Api-Token': process.env.AC_API_KEY, 'Accept': 'application/json' } },
  );
  if (!res.ok) return null;
  const data = await res.json();
  return data.contacts?.[0] || null;
}

async function acSetFieldValue(contactId, fieldId, value) {
  await fetch(`${process.env.AC_API_URL}/api/3/fieldValues`, {
    method: 'POST',
    headers: {
      'Api-Token': process.env.AC_API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      fieldValue: { contact: contactId, field: fieldId, value },
    }),
  });
}

async function acAddTag(contactId, tagId) {
  await fetch(`${process.env.AC_API_URL}/api/3/contactTags`, {
    method: 'POST',
    headers: {
      'Api-Token': process.env.AC_API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      contactTag: { contact: contactId, tag: tagId },
    }),
  });
}

function sanitizeFilename(email) {
  const base = email.replace(/[^a-zA-Z0-9@._-]/g, '_');
  const hash = crypto.createHash('sha1').update(email).digest('hex').slice(0, 8);
  return `${base}-${hash}`;
}
