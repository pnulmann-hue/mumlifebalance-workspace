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
      orange: '#dc822e',
      text: '#0c1c30',
    };

    // === Cover ===
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);
    doc
      .fillColor(colors.dunkelblau)
      .font('Helvetica-Bold')
      .fontSize(36)
      .text('Dein Bio-Check', 60, 220, { align: 'center', width: doc.page.width - 120 });
    doc
      .fillColor(colors.petrol)
      .fontSize(18)
      .font('Helvetica')
      .text('für Network-Mamas', { align: 'center' });

    if (name) {
      doc.moveDown(4);
      doc.fillColor(colors.orange).fontSize(16).text(`Für ${name}`, { align: 'center' });
    }

    doc.moveDown(6);
    doc
      .fillColor(colors.text)
      .fontSize(12)
      .text('Von Patricia Ulmann · Mum Life Balance', { align: 'center' });

    // === Inhalt ===
    doc.addPage();
    doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');

    doc
      .fillColor(colors.dunkelblau)
      .font('Helvetica-Bold')
      .fontSize(22)
      .text('Deine Bio-Analyse', 60, 60);

    doc.moveDown(0.5);
    doc
      .fillColor(colors.text)
      .font('Helvetica')
      .fontSize(10)
      .text(`Generiert am ${new Date().toLocaleDateString('de-CH', { day: '2-digit', month: 'long', year: 'numeric' })}`);

    doc.moveDown(1.5);

    const botMessages = messages.filter((m) => m.role === 'assistant');

    botMessages.forEach((msg, idx) => {
      const text = msg.content
        .replace(/\[\[BUTTON:[^\]]+\]\]/gi, '')
        .replace(/\[\[PITCH:[^\]]+\]\]/gi, '')
        .replace(/\[\[DONE\]\]/gi, '')
        .replace(/\*\*/g, '')
        .trim();

      if (!text) return;

      if (idx > 0) {
        doc.moveDown(0.8);
        doc
          .strokeColor(colors.creme)
          .lineWidth(1)
          .moveTo(60, doc.y)
          .lineTo(doc.page.width - 60, doc.y)
          .stroke();
        doc.moveDown(0.8);
      }

      doc.fillColor(colors.text).font('Helvetica').fontSize(11).text(text, {
        align: 'left',
        lineGap: 3,
      });
    });

    // === Nächste Schritte ===
    doc.addPage();
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);
    doc
      .fillColor(colors.dunkelblau)
      .font('Helvetica-Bold')
      .fontSize(24)
      .text('Deine nächsten Schritte', 60, 80);

    doc.moveDown(1);

    const pitches = [
      {
        title: '🎯 Finde dein Thema als Network-Mama',
        price: '39 CHF',
        promise: 'Du öffnest morgens Instagram und weisst sofort, worüber du schreibst — weil dein Thema klar ist.',
        url: 'https://mumlifebalance.thrivecart.com/thema-finden/',
      },
      {
        title: '⭐ Expertin statt Verkäuferin',
        price: '97 CHF',
        promise: 'In 3 Monaten: Fremde schreiben dir „Du hast mich endlich verstanden." Du verkaufst nicht mehr — du wirst empfohlen.',
        url: 'https://mumlifebalance.thrivecart.com/expertin/',
      },
      {
        title: '🚀 Instagram-Kundenmaschine',
        price: '333 CHF',
        promise: 'In 8 Wochen: Dein Business läuft. Aus Reaktionen werden Gespräche, aus Gesprächen Kundinnen.',
        url: 'https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/',
      },
    ];

    pitches.forEach((p) => {
      doc.moveDown(1);
      doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(14).text(p.title);
      doc.fillColor(colors.orange).fontSize(12).text(p.price);
      doc.fillColor(colors.text).font('Helvetica').fontSize(11).text(p.promise, { lineGap: 2 });
      doc.fillColor(colors.petrol).fontSize(10).text(p.url, { link: p.url, underline: true });
    });

    doc.moveDown(3);
    doc
      .fillColor(colors.text)
      .font('Helvetica-Oblique')
      .fontSize(11)
      .text(
        'Du machst das nicht, um dein Upline-Team zu beeindrucken. Du machst das, damit du deine Kinder selbst betreuen kannst und trotzdem dein eigenes Einkommen hast. Genau dafür.',
        60,
        doc.y,
        { align: 'center', width: doc.page.width - 120 },
      );

    doc.moveDown(0.5);
    doc.fillColor(colors.petrol).fontSize(14).text('— Patricia', { align: 'center' });

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
