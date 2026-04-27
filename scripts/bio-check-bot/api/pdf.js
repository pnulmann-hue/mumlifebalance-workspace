/* =============================================================
   Vercel API Route: /api/pdf
   =============================================================
   Generiert strukturiertes Bio-Check-PDF und triggert AC-Mail.

   Flow:
   1. Empfange {email, name, messages[]}
   2. Claude-Call: Chat-Verlauf zu strukturiertem JSON-Summary
      (Bio-Varianten, Pinned Posts, Highlights, Positionierungs-Tipps,
      Bonus-Tipps von Patricia)
   3. PDF mit klaren Sektionen rendern (Patricia-Brand)
   4. Upload zu Vercel Blob → öffentliche URL
   5. AC-Tag "Bio-Check abgeschlossen" setzen → triggert Mail-Automation

   Fallback: Falls Summary-Call fehlschlägt, fällt Layout auf alten
   Chat-Dump zurück (kein Lead verbrannt).

   Environment:
   - ANTHROPIC_API_KEY (für Summary-Call)
   - BLOB_READ_WRITE_TOKEN (Vercel Blob)
   - AC_API_URL, AC_API_KEY
   - AC_TAG_COMPLETED (60), AC_FIELD_PDF_URL (Custom Field ID)
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import PDFDocument from 'pdfkit';
import { put } from '@vercel/blob';
import crypto from 'node:crypto';

export const config = { runtime: 'nodejs', maxDuration: 90 };

const anthropic = new Anthropic();

// =============================================================
// Handler
// =============================================================

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { email, name, messages = [] } = req.body || {};
    if (!email) return res.status(400).json({ error: 'email required' });

    // 1. Strukturierte Zusammenfassung vom Chat-Verlauf erstellen
    const summary = await generateSummary(messages, name).catch((err) => {
      console.warn('Summary-Call fehlgeschlagen, nutze Fallback:', err.message);
      return null;
    });

    // 2. PDF generieren — mit oder ohne Summary
    const pdfBuffer = await generatePDF({
      name: name || '',
      summary,
      fallbackMessages: messages,
    });

    // 3. Upload zu Vercel Blob — deterministischer Filename pro E-Mail
    const filename = `bio-checks/${sanitizeFilename(email)}.pdf`;
    const blob = await put(filename, pdfBuffer, {
      access: 'public',
      contentType: 'application/pdf',
      addRandomSuffix: false,
      allowOverwrite: true,
    });
    const pdfUrl = blob.url;

    // 4. AC: Contact finden
    const contact = await acFindContact(email);
    if (!contact) return res.status(404).json({ error: 'Kontakt nicht in AC gefunden' });

    // 5. Custom Field setzen (wenn konfiguriert)
    if (process.env.AC_FIELD_PDF_URL) {
      await acSetFieldValue(contact.id, process.env.AC_FIELD_PDF_URL, pdfUrl);
    }

    // 6. Tag "abgeschlossen" → triggert AC-Mail-Automation
    if (process.env.AC_TAG_COMPLETED) {
      await acAddTag(contact.id, process.env.AC_TAG_COMPLETED);
    }

    return res.status(200).json({
      ok: true,
      pdfUrl,
      contactId: contact.id,
      structured: summary !== null,
    });
  } catch (err) {
    console.error('PDF error:', err);
    return res.status(500).json({ error: err.message || 'internal error' });
  }
}

// =============================================================
// Claude-Summary: extrahiert die Kern-Inhalte aus dem Chat
// in ein strukturiertes JSON, damit das PDF saubere Sektionen
// rendern kann statt einer Textwüste.
// =============================================================

const SUMMARY_SYSTEM_PROMPT = `Du bist ein Strukturierungs-Assistent für Patricia Ulmann (Mum Life Balance).

Du erhältst einen kompletten Bio-Check-Chat-Verlauf zwischen Patricias Bio-Check-Bot und einer Network-Mama. Deine Aufgabe: extrahiere die Kern-Inhalte als sauberes, strukturiertes JSON für ein hochwertiges PDF.

ANTWORT-FORMAT (Pflicht): NUR valides JSON, kein Markdown-Codeblock, keine Einleitung, kein Outro.

JSON-Schema:
{
  "thema_kompakt": "Das Haupt-Thema der User in EINEM Satz (max. 25 Wörter), als wäre es ihr Experten-Satz",
  "experten_satz": "Die zentrale Positionierungs-Aussage, die im Chat herausgearbeitet wurde — der eine Satz, der ihr Profil definiert",
  "audience_zitat": "Ein wörtliches Zitat der Audience aus dem Chat (z.B. 'Ausgelaugt aber mit dem Gefühl: ist halt so')",
  "bio_varianten": [
    {
      "name": "Stil-Bezeichnung (z.B. 'Warmherzig', 'Direkt-und-konkret')",
      "zeilen": ["Zeile 1 (Profilname/Rolle)", "Zeile 2-3 (Experten-Satz)", "Zeile 4 (Trust-Element)", "Zeile 5 (CTA)"],
      "zeichen": 147
    }
  ],
  "pinned_posts": [
    {
      "titel": "Kurzer Titel des Posts",
      "hook": "Der Aufhänger als kompletter Satz",
      "kernbotschaft": "Was der Post transportiert in 1-2 Sätzen"
    }
  ],
  "highlights": [
    {
      "name": "Highlight-Name (z.B. 'Über mich')",
      "beschreibung": "Was hier rein gehört, 1 prägnanter Satz"
    }
  ],
  "positionierung_tipps": [
    "Konkreter Pflicht-Tipp 1 (basierend auf der Chat-Analyse)",
    "Konkreter Pflicht-Tipp 2",
    "..."
  ],
  "patricia_bonus_tipps": [
    "ZUSÄTZLICHER Tipp den Patricia persönlich raten würde — nicht aus dem Chat",
    "Strategischer Umsetzungs-Hinweis (z.B. 'Teste Bio-Variante 1 für 4 Wochen, dann tausche')",
    "Gefahr/Stolperstein vermeiden",
    "..."
  ]
}

REGELN:
- 2-3 Bio-Varianten (so viele wie im Chat vorgeschlagen wurden)
- 3 Pinned Posts (genau 3)
- 5 Highlights (genau 5)
- 5-7 Positionierungs-Tipps (Pflicht-Inhalte aus dem Chat)
- 4-6 Patricia-Bonus-Tipps (ZUSÄTZLICH zum Chat — was würde Patricia raten, was im Bot-Gespräch nicht aufkam?)
- Patricias Brand-Voice: warmherzig, direkt, ehrlich, Schaufenster-Metapher OK
- Schweizer ss (statt ß), echte Umlaute (ä ö ü)
- KEINE Emojis im JSON
- KEINE Markdown-Sterne (* oder **)
- Bei Bio-Varianten: Zeilen genau wie im Chat, ohne Emojis
- Bei patricia_bonus_tipps: Schreib aus Patricias Perspektive, also "Mein Tipp:" oder "Wenn ich dich beraten würde:" — aber NICHT in jedem Tipp wiederholen, nur im ersten

Wenn der Chat noch nicht vollständig durchgelaufen ist (z.B. keine Bio-Varianten erstellt wurden), nutze sinnvolle Defaults oder lass das Feld als leeres Array.`;

// Tool-Schema: erzwingt strukturierte JSON-Antwort (zuverlaessiger als
// Text-Parsing — Claude liefert garantiert JSON mit korrektem Schema).
const SUMMARY_TOOL = {
  name: 'submit_bio_check_summary',
  description: 'Reicht die strukturierte Bio-Check-Zusammenfassung ein, die im PDF gerendert wird.',
  input_schema: {
    type: 'object',
    properties: {
      thema_kompakt: {
        type: 'string',
        description: 'Das Haupt-Thema der User in EINEM Satz (max. 25 Woerter), wie ihr Experten-Satz',
      },
      experten_satz: {
        type: 'string',
        description: 'Die zentrale Positionierungs-Aussage, der eine Satz, der das Profil definiert',
      },
      audience_zitat: {
        type: 'string',
        description: 'Ein woertliches Audience-Zitat aus dem Chat (z.B. "Ausgelaugt aber mit dem Gefuehl: ist halt so")',
      },
      bio_varianten: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string', description: 'Stil-Bezeichnung (z.B. Warmherzig)' },
            zeilen: {
              type: 'array',
              items: { type: 'string' },
              description: 'Die 4 Zeilen der Bio: Profilname, Experten-Satz, Trust-Element, CTA',
            },
            zeichen: { type: 'integer', description: 'Anzahl Zeichen der gesamten Bio' },
          },
          required: ['name', 'zeilen'],
        },
        description: '2-3 Bio-Varianten (so viele wie im Chat vorgeschlagen)',
      },
      pinned_posts: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            titel: { type: 'string' },
            hook: { type: 'string', description: 'Aufhaenger als kompletter Satz' },
            kernbotschaft: { type: 'string', description: 'Was der Post transportiert in 1-2 Saetzen' },
          },
          required: ['titel', 'hook', 'kernbotschaft'],
        },
        description: 'Genau 3 Pinned Posts',
      },
      highlights: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            beschreibung: { type: 'string', description: '1 praegnanter Satz' },
          },
          required: ['name', 'beschreibung'],
        },
        description: 'Genau 5 Highlights',
      },
      positionierung_tipps: {
        type: 'array',
        items: { type: 'string' },
        description: '5-7 Pflicht-Tipps zur Positionierung aus der Chat-Analyse',
      },
      patricia_bonus_tipps: {
        type: 'array',
        items: { type: 'string' },
        description: '4-6 ZUSAETZLICHE Tipps von Patricia (NICHT aus dem Chat, sondern was sie persoenlich raten wuerde)',
      },
    },
    required: [
      'thema_kompakt',
      'experten_satz',
      'audience_zitat',
      'bio_varianten',
      'pinned_posts',
      'highlights',
      'positionierung_tipps',
      'patricia_bonus_tipps',
    ],
  },
};

async function generateSummary(messages, name) {
  if (!messages || messages.length === 0) return null;

  const chatLog = messages
    .map((m) => `[${m.role.toUpperCase()}]\n${m.content}`)
    .join('\n\n---\n\n');

  const userPrompt = `Hier ist der komplette Bio-Check-Chat-Verlauf fuer ${name || 'die User'}.\n\nReiche die strukturierte Zusammenfassung via submit_bio_check_summary-Tool ein.\n\n=== CHAT-VERLAUF ===\n\n${chatLog}\n\n=== ENDE CHAT-VERLAUF ===`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-5',
    max_tokens: 4000,
    system: SUMMARY_SYSTEM_PROMPT,
    tools: [SUMMARY_TOOL],
    tool_choice: { type: 'tool', name: 'submit_bio_check_summary' },
    messages: [{ role: 'user', content: userPrompt }],
  });

  // Tool-Use-Block extrahieren — Claude muss den Tool aufrufen (forced via tool_choice)
  const toolUseBlock = response.content?.find((b) => b.type === 'tool_use');
  if (!toolUseBlock) {
    throw new Error('Kein tool_use-Block in Summary-Antwort (forced tool_choice fehlgeschlagen)');
  }
  return toolUseBlock.input;
}

// =============================================================
// Text-Cleanup für Fallback-Modus (wenn Summary fehlschlägt)
// =============================================================

const EMOJI_RE = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F700}-\u{1F77F}]|[\u{1F780}-\u{1F7FF}]|[\u{1F800}-\u{1F8FF}]|[\u{1F900}-\u{1F9FF}]|[\u{1FA00}-\u{1FA6F}]|[\u{1FA70}-\u{1FAFF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{2300}-\u{23FF}]|[\u{2B00}-\u{2BFF}]|[\u{1F000}-\u{1F02F}]|[\u{1F0A0}-\u{1F0FF}]|[\u{1F100}-\u{1F1FF}]|[\u{200D}\u{FE0F}\u{20E3}]/gu;

function cleanText(raw) {
  if (!raw) return '';
  return raw
    .replace(/\[\[BUTTON:[^\]]+\]\]/gi, '')
    .replace(/\[\[PITCH:[^\]]+\]\]/gi, '')
    .replace(/\[\[DONE\]\]/gi, '')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*\n]+)\*/g, '$1')
    .replace(/__([^_\n]+)__/g, '$1')
    .replace(/^>\s*/gm, '')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^%[%\s]*$/gm, '———')
    .replace(EMOJI_RE, '')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// =============================================================
// PDF-Generator: nutzt strukturiertes Summary wenn vorhanden,
// sonst Fallback auf Chat-Dump.
// =============================================================

function generatePDF({ name, summary, fallbackMessages }) {
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
      cremeBox: '#f7f1e2',
      orange: '#dc822e',
      text: '#0c1c30',
      muted: '#6b6052',
      divider: '#d8cfb6',
    };

    const today = new Date().toLocaleDateString('de-CH', {
      day: '2-digit', month: 'long', year: 'numeric',
    });

    // Helper: Section-Headline
    const sectionHeader = (title, subtitle) => {
      if (doc.y > doc.page.height - 200) doc.addPage();
      doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(24)
        .text(title, 60, doc.y);
      doc.strokeColor(colors.orange).lineWidth(3)
        .moveTo(60, doc.y + 4).lineTo(110, doc.y + 4).stroke();
      doc.moveDown(1.2);
      if (subtitle) {
        doc.fillColor(colors.muted).font('Helvetica-Oblique').fontSize(11)
          .text(subtitle, { width: doc.page.width - 120, lineGap: 2 });
        doc.moveDown(1.5);
      }
    };

    // ===== COVER =====
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);

    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, 80).lineTo(120, 80).stroke();
    doc.fillColor(colors.petrol).font('Helvetica-Bold').fontSize(10)
      .text('MUM LIFE BALANCE  ·  BIO-CHECK', 60, 95, { characterSpacing: 2 });

    doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(48)
      .text('Dein\nBio-Check', 60, 240, { lineGap: 6 });
    doc.fillColor(colors.petrol).fontSize(20).font('Helvetica')
      .text('für Network-Mamas', 60, 380);

    if (name) {
      doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(14)
        .text(`Persönlich für ${name}`, 60, 460);
    }
    doc.fillColor(colors.muted).font('Helvetica').fontSize(11)
      .text(today, 60, name ? 482 : 460);

    doc.fillColor(colors.text).font('Helvetica-Bold').fontSize(11)
      .text('Patricia Ulmann', 60, doc.page.height - 110);
    doc.fillColor(colors.muted).font('Helvetica').fontSize(10)
      .text('Mentorin für Mamas im Network Marketing', 60, doc.page.height - 92);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, doc.page.height - 70).lineTo(120, doc.page.height - 70).stroke();

    // ===== STRUKTURIERTER MODUS =====
    if (summary) {
      // === SEITE 2: Dein Thema + Experten-Satz ===
      doc.addPage();
      doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');

      sectionHeader('Dein Thema in einem Satz', `Generiert am ${today}`);

      // Highlight-Box mit Thema
      if (summary.thema_kompakt) {
        const boxY = doc.y;
        doc.roundedRect(60, boxY, doc.page.width - 120, 80, 8).fill(colors.cremeBox);
        doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(13)
          .text('Dein Thema', 80, boxY + 16);
        doc.fillColor(colors.text).font('Helvetica').fontSize(13)
          .text(summary.thema_kompakt, 80, boxY + 36, {
            width: doc.page.width - 160, lineGap: 3,
          });
        doc.y = boxY + 100;
      }

      doc.moveDown(1);

      if (summary.experten_satz) {
        const boxY = doc.y;
        doc.roundedRect(60, boxY, doc.page.width - 120, 90, 8).fill('#ffffff');
        doc.rect(60, boxY, 4, 90).fill(colors.petrol);
        doc.fillColor(colors.petrol).font('Helvetica-Bold').fontSize(11)
          .text('DEIN EXPERTEN-SATZ', 80, boxY + 14, { characterSpacing: 1.5 });
        doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(13)
          .text(`„${summary.experten_satz}"`, 80, boxY + 36, {
            width: doc.page.width - 160, lineGap: 3,
          });
        doc.y = boxY + 110;
      }

      if (summary.audience_zitat) {
        const boxY = doc.y;
        doc.roundedRect(60, boxY, doc.page.width - 120, 90, 8).fill('#ffffff');
        doc.rect(60, boxY, 4, 90).fill(colors.orange);
        doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(11)
          .text('SO SPRICHT DEINE AUDIENCE', 80, boxY + 14, { characterSpacing: 1.5 });
        doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(13)
          .text(`„${summary.audience_zitat}"`, 80, boxY + 36, {
            width: doc.page.width - 160, lineGap: 3,
          });
        doc.y = boxY + 110;
      }

      // === SEITE 3: Bio-Varianten ===
      if (Array.isArray(summary.bio_varianten) && summary.bio_varianten.length > 0) {
        doc.addPage();
        doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');
        sectionHeader('Deine Bio-Varianten', 'Copy-paste-ready für deine Instagram-Bio. Aussuchen, einsetzen, fertig.');

        summary.bio_varianten.forEach((v, idx) => {
          if (doc.y > doc.page.height - 250) doc.addPage();
          // Variante-Label
          doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(11)
            .text(`VARIANTE ${idx + 1} — ${(v.name || '').toUpperCase()}`,
              60, doc.y, { characterSpacing: 1.5 });
          doc.moveDown(0.4);

          const lines = Array.isArray(v.zeilen) ? v.zeilen : [];
          const innerWidth = doc.page.width - 160; // Box-Innenraum

          // Box-Höhe dynamisch berechnen — jede Zeile kann mehrzeilig umbrechen
          doc.font('Helvetica').fontSize(11);
          const lineSpacing = 6; // Abstand zwischen den Zeilen
          let contentHeight = 16; // Top-Padding
          lines.forEach((line) => {
            contentHeight += doc.heightOfString(line, { width: innerWidth });
            contentHeight += lineSpacing;
          });
          contentHeight += 22; // Bottom-Padding + Platz für Zeichenzähler

          // Box rendern
          const boxY = doc.y;
          doc.roundedRect(60, boxY, doc.page.width - 120, contentHeight, 8)
            .fill(colors.cremeBox);

          // Zeilen rendern — nutzt doc.y für automatische Höhenverfolgung
          doc.y = boxY + 14;
          lines.forEach((line) => {
            doc.fillColor(colors.text).font('Helvetica').fontSize(11)
              .text(line, 80, doc.y, { width: innerWidth });
            doc.y += lineSpacing - 2;
          });

          // Zeichenanzahl unten rechts in der Box
          if (v.zeichen) {
            doc.fillColor(colors.muted).font('Helvetica-Oblique').fontSize(9)
              .text(`${v.zeichen} Zeichen`, 60, boxY + contentHeight - 16,
                { width: doc.page.width - 140, align: 'right' });
          }

          // Cursor unter die Box positionieren
          doc.y = boxY + contentHeight + 20;
        });
      }

      // === SEITE 4: Pinned Posts ===
      if (Array.isArray(summary.pinned_posts) && summary.pinned_posts.length > 0) {
        doc.addPage();
        doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');
        sectionHeader('Deine 3 Pinned Posts', 'Die ersten 3 Posts auf deinem Profil — wie 3 Paar Schuhe im Schaufenster.');

        summary.pinned_posts.forEach((p, idx) => {
          if (doc.y > doc.page.height - 200) doc.addPage();
          const boxY = doc.y;

          // Karte mit Akzentstrich
          doc.roundedRect(60, boxY, doc.page.width - 120, 130, 8).fill(colors.cremeBox);
          doc.rect(60, boxY, 4, 130).fill(colors.petrol);

          // Nummer
          doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(11)
            .text(`POST ${idx + 1}`, 80, boxY + 14, { characterSpacing: 1.5 });

          // Titel
          doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(14)
            .text(p.titel || '', 80, boxY + 32, { width: doc.page.width - 160 });

          // Hook
          if (p.hook) {
            doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(11)
              .text(`Hook: „${p.hook}"`, 80, boxY + 60,
                { width: doc.page.width - 160, lineGap: 2 });
          }

          // Kernbotschaft
          if (p.kernbotschaft) {
            doc.fillColor(colors.text).font('Helvetica').fontSize(10)
              .text(p.kernbotschaft, 80, boxY + 92,
                { width: doc.page.width - 160, lineGap: 2 });
          }

          doc.y = boxY + 145;
        });
      }

      // === SEITE 5: Highlights ===
      if (Array.isArray(summary.highlights) && summary.highlights.length > 0) {
        doc.addPage();
        doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');
        sectionHeader('Deine 5 Highlights', 'Die Regale in deinem Laden. Wer interessiert ist, stöbert hier.');

        summary.highlights.forEach((h, idx) => {
          if (doc.y > doc.page.height - 100) doc.addPage();
          const boxY = doc.y;
          // Nummer in Petrol-Kreis
          doc.circle(78, boxY + 16, 14).fill(colors.petrol);
          doc.fillColor('#ffffff').font('Helvetica-Bold').fontSize(13)
            .text(`${idx + 1}`, 73, boxY + 9);

          // Name + Beschreibung
          doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(13)
            .text(h.name || '', 105, boxY + 4, { width: doc.page.width - 165 });
          doc.fillColor(colors.text).font('Helvetica').fontSize(11)
            .text(h.beschreibung || '', 105, boxY + 22,
              { width: doc.page.width - 165, lineGap: 2 });

          doc.y = Math.max(boxY + 50, doc.y);
        });
      }

      // === SEITE 6: Positionierungs-Tipps ===
      if (Array.isArray(summary.positionierung_tipps) && summary.positionierung_tipps.length > 0) {
        doc.addPage();
        doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.cremeLight);
        sectionHeader('Was du bei deiner Positionierung beachten musst', 'Die wichtigsten Punkte aus deinem Bio-Check — auf einen Blick.');

        summary.positionierung_tipps.forEach((tip, idx) => {
          if (doc.y > doc.page.height - 100) doc.addPage();
          const startY = doc.y;
          // Orange Akzent-Bullet
          doc.circle(72, startY + 8, 4).fill(colors.orange);
          doc.fillColor(colors.text).font('Helvetica').fontSize(11)
            .text(tip, 90, startY,
              { width: doc.page.width - 150, lineGap: 3, paragraphGap: 4 });
          doc.moveDown(0.5);
        });
      }

      // === SEITE 7: Patricia's Bonus-Tipps ===
      if (Array.isArray(summary.patricia_bonus_tipps) && summary.patricia_bonus_tipps.length > 0) {
        doc.addPage();
        doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');

        sectionHeader('Patricias Bonus-Tipps', 'Was ich dir als Mentorin zusätzlich raten würde — über das Bot-Gespräch hinaus.');

        // Vorab Patricia-Quote-Box
        const qY = doc.y;
        doc.roundedRect(60, qY, doc.page.width - 120, 70, 8).fill(colors.cremeBox);
        doc.rect(60, qY, 4, 70).fill(colors.orange);
        doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(11)
          .text('„Eine starke Bio ist erst der Anfang. Was zählt, ist die Konsistenz danach — und der Mut, dich zu zeigen wie du wirklich bist."',
            80, qY + 18, { width: doc.page.width - 160, lineGap: 2 });
        doc.fillColor(colors.petrol).font('Helvetica-Bold').fontSize(10)
          .text('— Patricia', 80, qY + 50, { width: doc.page.width - 160, align: 'right' });
        doc.y = qY + 90;

        summary.patricia_bonus_tipps.forEach((tip, idx) => {
          if (doc.y > doc.page.height - 100) doc.addPage();
          const startY = doc.y;
          // Petrol Akzent-Bullet
          doc.circle(72, startY + 8, 4).fill(colors.petrol);
          doc.fillColor(colors.text).font('Helvetica').fontSize(11)
            .text(tip, 90, startY,
              { width: doc.page.width - 150, lineGap: 3, paragraphGap: 4 });
          doc.moveDown(0.6);
        });
      }
    } else {
      // ===== FALLBACK: Chat-Dump (alter Modus) =====
      doc.addPage();
      doc.rect(0, 0, doc.page.width, doc.page.height).fill('#ffffff');
      sectionHeader('Deine Bio-Analyse', `Generiert am ${today}`);

      const botMessages = (fallbackMessages || []).filter((m) => m.role === 'assistant');
      botMessages.forEach((msg, idx) => {
        const text = cleanText(msg.content);
        if (!text) return;
        if (idx > 0) {
          doc.moveDown(0.8);
          doc.strokeColor(colors.divider).lineWidth(0.5)
            .moveTo(180, doc.y).lineTo(doc.page.width - 180, doc.y).stroke();
          doc.moveDown(0.8);
        }
        doc.fillColor(colors.text).font('Helvetica').fontSize(11)
          .text(text, { align: 'left', lineGap: 4, paragraphGap: 6 });
      });
    }

    // ===== FINALE SEITE: Nächste Schritte (Pitches) =====
    doc.addPage();
    doc.rect(0, 0, doc.page.width, doc.page.height).fill(colors.creme);

    doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(28)
      .text('Deine nächsten Schritte', 60, 80);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, 125).lineTo(110, 125).stroke();

    doc.moveDown(2);
    doc.fillColor(colors.muted).font('Helvetica-Oblique').fontSize(11)
      .text('Nach deiner Bio kommt die Frage: Wie schreibst du jetzt Content, der wirklich verkauft? Drei Wege — je nachdem, wo du gerade stehst.',
        { width: doc.page.width - 120, lineGap: 3 });

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
      doc.roundedRect(60, cardY, cardWidth, cardHeight, 8).fill('#ffffff');
      doc.rect(60, cardY, 4, cardHeight).fill(colors.orange);
      doc.fillColor(colors.dunkelblau).font('Helvetica-Bold').fontSize(14)
        .text(p.title, 80, cardY + 16, { width: cardWidth - 100 });
      doc.fillColor(colors.orange).font('Helvetica-Bold').fontSize(14)
        .text(p.price, 60, cardY + 16, { align: 'right', width: cardWidth - 20 });
      doc.fillColor(colors.text).font('Helvetica').fontSize(10)
        .text(p.promise, 80, cardY + 44, { width: cardWidth - 40, lineGap: 2 });
      doc.fillColor(colors.petrol).font('Helvetica-Oblique').fontSize(9)
        .text(p.url, 80, cardY + cardHeight - 22, {
          width: cardWidth - 40, link: p.url, underline: true,
        });
      doc.y = cardY + cardHeight + 14;
    });

    doc.moveDown(1.5);
    doc.strokeColor(colors.orange).lineWidth(3)
      .moveTo(60, doc.y).lineTo(120, doc.y).stroke();
    doc.moveDown(0.8);

    doc.fillColor(colors.text).font('Helvetica-Oblique').fontSize(11)
      .text('Du machst das nicht, um dein Upline-Team zu beeindrucken. Du machst das, damit du deine Kinder selbst betreuen kannst und trotzdem dein eigenes Einkommen hast. Genau dafür.',
        60, doc.y, { align: 'left', width: doc.page.width - 120, lineGap: 3 });

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
    { headers: { 'Api-Token': process.env.AC_API_KEY, Accept: 'application/json' } },
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
      Accept: 'application/json',
    },
    body: JSON.stringify({ fieldValue: { contact: contactId, field: fieldId, value } }),
  });
}

async function acAddTag(contactId, tagId) {
  await fetch(`${process.env.AC_API_URL}/api/3/contactTags`, {
    method: 'POST',
    headers: {
      'Api-Token': process.env.AC_API_KEY,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ contactTag: { contact: contactId, tag: tagId } }),
  });
}

function sanitizeFilename(email) {
  const base = email.replace(/[^a-zA-Z0-9@._-]/g, '_');
  const hash = crypto.createHash('sha1').update(email).digest('hex').slice(0, 8);
  return `${base}-${hash}`;
}
