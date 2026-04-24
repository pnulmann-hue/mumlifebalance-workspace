/**
 * Kurs-Transkription via OpenAI Whisper API
 * ==========================================
 *
 * Nimmt alle Video-Files in einem Ordner, extrahiert Audio via ffmpeg,
 * transkribiert via Whisper API, und speichert .txt im Zielordner.
 *
 * Setup:
 *   1. ffmpeg muss installiert sein (https://ffmpeg.org/download.html)
 *      Windows: `winget install ffmpeg` oder https://www.gyan.dev/ffmpeg/builds/
 *   2. OPENAI_API_KEY in .env eintragen
 *   3. npm install (nur fetch-Polyfill, sonst nichts)
 *
 * Lauf:
 *   node --env-file=.env transcribe.js <input-dir> <output-dir>
 *
 * Beispiel:
 *   node --env-file=.env transcribe.js \
 *     "../../reference/julia-trost/Werbeanzeigen-Videos" \
 *     "../../reference/julia-trost/Transkripte Videocalls/_sortiert/Werbeanzeigen"
 *
 * Kosten: ca 0.006 USD/Minute (Whisper API)
 */

import { readFile, readdir, writeFile, unlink, mkdir, stat } from 'node:fs/promises';
import { join, basename, extname } from 'node:path';
import { spawn } from 'node:child_process';

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY || OPENAI_API_KEY.startsWith('sk-proj-DEIN')) {
  console.error('❌ OPENAI_API_KEY fehlt in .env');
  process.exit(1);
}

const VIDEO_EXTS = ['.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v'];

async function run(cmd, args) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => { err += d.toString(); });
    p.on('close', (code) => code === 0 ? resolve() : reject(new Error(`${cmd} exit ${code}\n${err.slice(-500)}`)));
    p.on('error', reject);
  });
}

async function extractAudio(videoPath, audioPath) {
  await run('ffmpeg', ['-y', '-i', videoPath, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '32k', audioPath]);
}

async function transcribeWithWhisper(audioPath, language = 'de') {
  const buffer = await readFile(audioPath);
  const filename = basename(audioPath);

  const boundary = '----claude-' + Math.random().toString(36).slice(2);
  const parts = [];

  function appendField(name, value) {
    parts.push(Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="${name}"\r\n\r\n${value}\r\n`
    ));
  }

  appendField('model', 'whisper-1');
  appendField('language', language);
  appendField('response_format', 'text');
  appendField('temperature', '0');

  parts.push(Buffer.from(
    `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: audio/mpeg\r\n\r\n`
  ));
  parts.push(buffer);
  parts.push(Buffer.from(`\r\n--${boundary}--\r\n`));

  const body = Buffer.concat(parts);

  const res = await fetch('https://api.openai.com/v1/audio/transcriptions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': `multipart/form-data; boundary=${boundary}`,
      'Content-Length': String(body.length),
    },
    body,
  });

  if (!res.ok) {
    const errTxt = await res.text();
    throw new Error(`Whisper API ${res.status}: ${errTxt.slice(0, 500)}`);
  }
  return res.text();
}

async function main() {
  const [inputDir, outputDir] = process.argv.slice(2);
  if (!inputDir || !outputDir) {
    console.error('Usage: node transcribe.js <input-dir> <output-dir>');
    process.exit(1);
  }

  await mkdir(outputDir, { recursive: true });

  const files = await readdir(inputDir);
  const videos = files
    .filter((f) => VIDEO_EXTS.includes(extname(f).toLowerCase()))
    .sort();

  if (videos.length === 0) {
    console.log(`Keine Videos in ${inputDir} gefunden (unterstuetzte Formate: ${VIDEO_EXTS.join(' ')})`);
    return;
  }

  console.log(`🎬 ${videos.length} Video(s) gefunden`);

  for (const videoFile of videos) {
    const videoPath = join(inputDir, videoFile);
    const baseName = videoFile.replace(/\.[^.]+$/, '');
    const audioPath = join(inputDir, `${baseName}.mp3`);
    const txtPath = join(outputDir, `${baseName}.txt`);

    // Skip wenn Transkript schon existiert
    try {
      const existing = await stat(txtPath);
      if (existing.size > 100) {
        console.log(`⏭️  ${baseName} — Transkript existiert bereits, überspringe`);
        continue;
      }
    } catch {}

    try {
      console.log(`\n📽️  ${videoFile}`);
      console.log('  → Audio extrahieren...');
      await extractAudio(videoPath, audioPath);

      const audioSize = (await stat(audioPath)).size;
      console.log(`  → ${(audioSize / 1024 / 1024).toFixed(1)} MB Audio → Whisper API`);
      const transcript = await transcribeWithWhisper(audioPath);

      // Header mit Metadaten
      const header = `# ${baseName}\n\nQuelle: ${videoFile}\nTranskribiert: ${new Date().toISOString().slice(0, 10)}\nModel: whisper-1\n\n---\n\n`;
      await writeFile(txtPath, header + transcript.trim() + '\n', 'utf-8');
      console.log(`  ✅ ${txtPath}`);

      // Audio-Temp-File loeschen
      await unlink(audioPath).catch(() => {});
    } catch (err) {
      console.error(`  ❌ ${videoFile}: ${err.message}`);
    }
  }

  console.log('\n🎉 Fertig.');
}

main().catch((err) => { console.error('❌', err.message); process.exit(1); });
