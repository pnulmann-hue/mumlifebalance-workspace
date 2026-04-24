/**
 * Vimeo-Transkripte direkt ziehen (ohne Video-Download, ohne Whisper)
 * ===================================================================
 *
 * Nutzt yt-dlp um die auto-generierten Untertitel direkt von Vimeo zu holen.
 * Funktioniert für Julia-Trost-Kurse (auf Vimeo gehostet) mit Login-Cookies aus Chrome.
 *
 * Setup (einmalig):
 *   1. yt-dlp muss installiert sein → `pip install yt-dlp`
 *   2. In Chrome eingeloggt sein auf kurse.juliatrost.de (oder wo die Videos liegen)
 *   3. ffmpeg (für Subtitle-Konvertierung VTT → clean Text)
 *
 * Lauf:
 *   node fetch-vimeo-transcripts.js <urls-file> <output-dir>
 *
 * Beispiel:
 *   # Datei mit Vimeo-URLs (eine pro Zeile, # für Kommentare):
 *   #   # Werbeanzeigen-Kurs Julia Trost
 *   #   https://vimeo.com/1234567890
 *   #   https://vimeo.com/1234567891
 *
 *   node fetch-vimeo-transcripts.js \
 *     vimeo-urls-werbeanzeigen.txt \
 *     "../../reference/julia-trost/Transkripte Videocalls/_sortiert/Werbeanzeigen"
 *
 * Kostet: 0 EUR (keine API-Calls).
 */

import { readFile, readdir, writeFile, mkdir, unlink, rename, access } from 'node:fs/promises';
import { join, basename, extname } from 'node:path';
import { spawn } from 'node:child_process';

// Entweder cookies.txt in diesem Ordner (bevorzugt, fuer Windows-DPAPI-Probleme)
// oder Fallback auf Chrome-Cookies via --cookies-from-browser
const COOKIES_FILE = 'cookies.txt';
async function hasCookiesFile() {
  try { await access(COOKIES_FILE); return true; } catch { return false; }
}

async function run(cmd, args, options = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'], ...options });
    let out = '';
    let err = '';
    p.stdout.on('data', (d) => { out += d.toString(); process.stdout.write(d); });
    p.stderr.on('data', (d) => { err += d.toString(); process.stderr.write(d); });
    p.on('close', (code) => code === 0 ? resolve({ out, err }) : reject(new Error(`${cmd} exit ${code}`)));
    p.on('error', reject);
  });
}

function vttToText(vttContent) {
  const lines = vttContent.split(/\r?\n/);
  const textLines = [];
  let prevText = '';
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.startsWith('WEBVTT')) continue;
    if (trimmed.startsWith('Kind:') || trimmed.startsWith('Language:')) continue;
    if (trimmed.includes('-->')) continue; // Timestamp-Zeile
    if (/^\d+$/.test(trimmed)) continue; // Numeric index
    const cleaned = trimmed.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&quot;/g, '"');
    if (cleaned && cleaned !== prevText) {
      textLines.push(cleaned);
      prevText = cleaned;
    }
  }
  return textLines.join(' ').replace(/\s+/g, ' ').trim();
}

async function fetchOne(url, outputDir, index) {
  console.log(`\n[${index}] ${url}`);

  // Temp-Ordner fuer yt-dlp Output
  const tempPrefix = join(outputDir, `_tmp_${index}`);

  try {
    const useFile = await hasCookiesFile();
    const cookieArgs = useFile
      ? ['--cookies', COOKIES_FILE]
      : ['--cookies-from-browser', 'chrome'];

    // yt-dlp: Auto-Untertitel in Deutsch, kein Video-Download, als VTT
    await run('yt-dlp', [
      ...cookieArgs,
      '--write-auto-subs',
      '--write-subs',
      '--sub-lang', 'de,de-DE,en',
      '--skip-download',
      '--convert-subs', 'vtt',
      '--no-warnings',
      '-o', `${tempPrefix}.%(ext)s`,
      url,
    ]);

    // Finde die generierte VTT-Datei
    const dirFiles = await readdir(outputDir);
    const vttFile = dirFiles.find((f) => f.startsWith(`_tmp_${index}`) && f.endsWith('.vtt'));
    if (!vttFile) {
      console.warn(`  ⚠️ Keine VTT-Untertitel gefunden für ${url}`);
      return;
    }

    // VTT → Clean Text
    const vttPath = join(outputDir, vttFile);
    const vttContent = await readFile(vttPath, 'utf-8');
    const text = vttToText(vttContent);

    // Titel aus vtt-Dateinamen extrahieren (yt-dlp schreibt den Video-Titel)
    const cleanTitle = vttFile
      .replace(`_tmp_${index}`, '')
      .replace(/\.de(-DE)?\.vtt$/, '')
      .replace(/\.vtt$/, '')
      .replace(/\.en\.vtt$/, '')
      .replace(/^[.\s_-]+/, '')
      .replace(/[\/\\:*?"<>|]/g, '_');

    // Final TXT ablegen
    const txtPath = join(outputDir, `${cleanTitle || `video-${index}`}.txt`);
    const header = `# ${cleanTitle || `Video ${index}`}\n\nQuelle: ${url}\nTranskribiert: ${new Date().toISOString().slice(0, 10)}\nMethode: Vimeo Auto-Untertitel (via yt-dlp)\n\n---\n\n`;
    await writeFile(txtPath, header + text + '\n', 'utf-8');

    // VTT-Temp löschen
    await unlink(vttPath).catch(() => {});
    for (const f of dirFiles.filter((f) => f.startsWith(`_tmp_${index}`))) {
      await unlink(join(outputDir, f)).catch(() => {});
    }

    console.log(`  ✅ ${txtPath}`);
  } catch (err) {
    console.error(`  ❌ ${err.message}`);
    // Temp-Files aufräumen
    try {
      const dirFiles = await readdir(outputDir);
      for (const f of dirFiles.filter((f) => f.startsWith(`_tmp_${index}`))) {
        await unlink(join(outputDir, f)).catch(() => {});
      }
    } catch {}
  }
}

async function main() {
  const [urlsFile, outputDir] = process.argv.slice(2);
  if (!urlsFile || !outputDir) {
    console.error('Usage: node fetch-vimeo-transcripts.js <urls-file> <output-dir>');
    console.error('\nBeispiel urls-file:');
    console.error('  # Werbeanzeigen-Kurs');
    console.error('  https://vimeo.com/1234567890');
    console.error('  https://vimeo.com/1234567891');
    process.exit(1);
  }

  await mkdir(outputDir, { recursive: true });

  const content = await readFile(urlsFile, 'utf-8');
  const urls = content
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));

  if (urls.length === 0) {
    console.log('Keine URLs in der Datei.');
    return;
  }

  console.log(`🎬 ${urls.length} Vimeo-URL(s) zum Transkribieren\n`);

  for (let i = 0; i < urls.length; i++) {
    await fetchOne(urls[i], outputDir, i + 1);
  }

  console.log('\n🎉 Fertig. Cleanup pruefen:');
  console.log(`   ls "${outputDir}"`);
}

main().catch((err) => { console.error('❌', err.message); process.exit(1); });
