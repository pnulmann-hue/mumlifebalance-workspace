#!/usr/bin/env node
/**
 * telegram-send.js — Sendet Text ODER Bild via Patricia's Content-Bot
 *
 * MODUS 1: Text
 *   node telegram-send.js --text="Deine Nachricht" [--parse-mode=Markdown|HTML]
 *   echo "Text" | node telegram-send.js
 *
 * MODUS 2: Bild mit Caption (für Story-Slides)
 *   node telegram-send.js --photo="<pfad-zum-bild>" --caption="Caption-Text" [--parse-mode=HTML]
 *
 * MODUS 3: Bild-Gruppe (Mediagroup, max 10 Bilder)
 *   node telegram-send.js --media-group --photos="bild1.png,bild2.png,bild3.png" --caption-first="Caption nur fürs erste Bild"
 *
 * Umgebungsvariablen aus ../../.env:
 *   TELEGRAM_CONTENT_BOT_TOKEN
 *   TELEGRAM_CHAT_ID
 */

import fs from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');

// --- .env laden ---
const envPath = path.join(WORKSPACE_ROOT, '.env');
const envContent = await fs.readFile(envPath, 'utf8');
const envMap = Object.fromEntries(
  envContent
    .split('\n')
    .filter(l => l.includes('=') && !l.startsWith('#'))
    .map(l => {
      const [k, ...rest] = l.split('=');
      return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
    })
);

const BOT_TOKEN = envMap.TELEGRAM_CONTENT_BOT_TOKEN;
const CHAT_ID = envMap.TELEGRAM_CHAT_ID;

if (!BOT_TOKEN || !CHAT_ID) {
  console.error('FEHLER: TELEGRAM_CONTENT_BOT_TOKEN oder TELEGRAM_CHAT_ID nicht in .env');
  process.exit(1);
}

// --- Args parsen ---
const args = Object.fromEntries(
  process.argv.slice(2).map(a => {
    const [k, ...rest] = a.replace(/^--/, '').split('=');
    return [k, rest.join('=') || true];
  })
);

const TG_API = `https://api.telegram.org/bot${BOT_TOKEN}`;
const PHOTO_CAPTION_MAX = 1024; // Telegram-Limit für Photo-Captions
const TEXT_MAX = 4000;          // Telegram-Limit für sendMessage (4096 mit Puffer)

// ============================================================
// HELPER: HTML-Sonderzeichen escapen für parse_mode=HTML
// ============================================================
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// ============================================================
// MODUS 1: TEXT senden (mit Auto-Splitting bei >4000 Zeichen)
// ============================================================
async function sendText(text, parseMode = null) {
  const parts = [];
  if (text.length <= TEXT_MAX) {
    parts.push(text);
  } else {
    let remaining = text;
    while (remaining.length > 0) {
      if (remaining.length <= TEXT_MAX) {
        parts.push(remaining);
        break;
      }
      let cut = remaining.lastIndexOf('\n', TEXT_MAX);
      if (cut < TEXT_MAX / 2) cut = TEXT_MAX;
      parts.push(remaining.slice(0, cut));
      remaining = remaining.slice(cut).trimStart();
    }
  }

  const messageIds = [];
  for (let i = 0; i < parts.length; i++) {
    const body = {
      chat_id: CHAT_ID,
      text: parts[i],
    };
    if (parseMode) body.parse_mode = parseMode;
    if (parts.length > 1) body.text = `(${i + 1}/${parts.length})\n\n${body.text}`;

    const response = await fetch(`${TG_API}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const json = await response.json();
    if (!json.ok) {
      console.error(`FEHLER beim Senden (Teil ${i + 1}/${parts.length}):`, JSON.stringify(json, null, 2));
      process.exit(1);
    }
    messageIds.push(json.result.message_id);
  }
  return messageIds;
}

// ============================================================
// MODUS 2: BILD mit Caption senden (für Story-Slides)
// ============================================================
async function sendPhoto(photoPath, caption = '', parseMode = null) {
  // Pfad absolut machen
  const absPath = path.isAbsolute(photoPath) ? photoPath : path.resolve(photoPath);
  await fs.access(absPath); // Existiert die Datei?

  // Caption auf 1024 Zeichen kürzen (Telegram-Limit)
  let finalCaption = caption;
  let extraText = '';
  if (caption && caption.length > PHOTO_CAPTION_MAX) {
    finalCaption = caption.slice(0, PHOTO_CAPTION_MAX - 3) + '...';
    extraText = caption.slice(PHOTO_CAPTION_MAX - 3);
  }

  const formData = new FormData();
  formData.append('chat_id', CHAT_ID);
  formData.append('photo', new Blob([await fs.readFile(absPath)]), path.basename(absPath));
  if (finalCaption) formData.append('caption', finalCaption);
  if (parseMode) formData.append('parse_mode', parseMode);

  const response = await fetch(`${TG_API}/sendPhoto`, {
    method: 'POST',
    body: formData,
  });
  const json = await response.json();
  if (!json.ok) {
    console.error(`FEHLER beim Senden des Bildes:`, JSON.stringify(json, null, 2));
    process.exit(1);
  }

  // Falls Caption gekürzt wurde: Rest als Folge-Text-Nachricht
  if (extraText) {
    await sendText(`[Fortsetzung Caption]\n\n${extraText}`, parseMode);
  }

  return json.result.message_id;
}

// ============================================================
// MODUS 3: MEDIAGROUP (mehrere Bilder als Karussell, max 10)
// ============================================================
async function sendMediaGroup(photoPaths, captionFirst = '', parseMode = null) {
  if (photoPaths.length === 0) {
    console.error('FEHLER: Keine Bilder für Mediagroup angegeben.');
    process.exit(1);
  }
  if (photoPaths.length > 10) {
    console.error('FEHLER: Mediagroup max. 10 Bilder. Splitten oder einzeln senden.');
    process.exit(1);
  }

  const formData = new FormData();
  formData.append('chat_id', CHAT_ID);

  const media = photoPaths.map((p, i) => {
    const item = {
      type: 'photo',
      media: `attach://photo${i}`,
    };
    // Caption nur aufs erste Bild (Telegram-Konvention)
    if (i === 0 && captionFirst) {
      item.caption = captionFirst.slice(0, PHOTO_CAPTION_MAX);
      if (parseMode) item.parse_mode = parseMode;
    }
    return item;
  });

  formData.append('media', JSON.stringify(media));

  for (let i = 0; i < photoPaths.length; i++) {
    const absPath = path.isAbsolute(photoPaths[i]) ? photoPaths[i] : path.resolve(photoPaths[i]);
    await fs.access(absPath);
    formData.append(`photo${i}`, new Blob([await fs.readFile(absPath)]), path.basename(absPath));
  }

  const response = await fetch(`${TG_API}/sendMediaGroup`, {
    method: 'POST',
    body: formData,
  });
  const json = await response.json();
  if (!json.ok) {
    console.error(`FEHLER beim Senden der Mediagroup:`, JSON.stringify(json, null, 2));
    process.exit(1);
  }

  return json.result.map(r => r.message_id);
}

// ============================================================
// MAIN: Modus-Auswahl basierend auf Args
// ============================================================
const parseMode = args['parse-mode'] || null;

// MODUS 3: Mediagroup
if (args['media-group']) {
  const photos = (args.photos || '').split(',').map(s => s.trim()).filter(Boolean);
  const captionFirst = args['caption-first'] || '';
  if (photos.length === 0) {
    console.error('FEHLER: --media-group braucht --photos="bild1.png,bild2.png,..."');
    process.exit(1);
  }
  const ids = await sendMediaGroup(photos, captionFirst, parseMode);
  console.log(`OK: Mediagroup gesendet (${photos.length} Bilder). message_ids:`, ids.join(', '));
  process.exit(0);
}

// MODUS 2: Einzelbild mit Caption
if (args.photo) {
  const caption = args.caption || '';
  const id = await sendPhoto(args.photo, caption, parseMode);
  console.log(`OK: Bild gesendet. message_id: ${id}`);
  process.exit(0);
}

// MODUS 1: Text (Default — auch via stdin)
let text = args.text;
if (!text) {
  // stdin lesen
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  text = Buffer.concat(chunks).toString('utf8').trim();
}

if (!text) {
  console.error('FEHLER: Kein Text. Optionen:');
  console.error('  Text: --text="..." oder pipe via stdin');
  console.error('  Bild: --photo="pfad" --caption="..."');
  console.error('  Mediagroup: --media-group --photos="bild1.png,bild2.png" --caption-first="..."');
  process.exit(1);
}

const ids = await sendText(text, parseMode);
console.log(`OK: ${ids.length} Nachricht(en) gesendet. message_ids:`, ids.join(', '));
