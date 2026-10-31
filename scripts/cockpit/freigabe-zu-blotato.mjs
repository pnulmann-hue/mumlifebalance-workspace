/**
 * Letzte Meile: freigegebenes Karussell aus dem Cockpit -> Instagram.
 *
 * Patricia gibt im Cockpit ein Karussell frei (Datum, Uhrzeit, Profil).
 * Claude liest die Freigabe aus der Cockpit-Datenbank in einen Ordner und
 * ruft dann dieses Skript auf. Es macht den Rest:
 *
 *   1. Bilder aus den abgelegten JSON-Dateien zurueck in JPEGs (Ablage zum Nachsehen)
 *   2. Blotato /v2/media  -> nimmt die data:-URL direkt, legt sie auf sein CDN
 *      (nur das Reel-Video geht noch ueber WordPress)
 *   3. Blotato /v2/posts  -> Beitrag zum gewuenschten Zeitpunkt eingeplant
 *
 * Aufruf:
 *   node scripts/cockpit/freigabe-zu-blotato.mjs --ordner <pfad> [--trocken] [--proxy]
 *
 * --proxy  Cloud-Lauf: kein eigener Blotato-Schluessel, den setzt der Proxy der
 *          Umgebung ein. Account-IDs kommen dann aus den Umgebungsvariablen.
 *
 * Erwartet im Ordner:
 *   freigaben/<id>.json                 die Freigabe (caption, datum, zeit, profil)
 *   freigaben/<id>/bilder/slide-01.json … die Folien als dataUrl
 *
 * --trocken laedt nichts hoch und plant nichts ein, zeigt nur, was passieren wuerde.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');

const BLOTATO_BASE = 'https://backend.blotato.com';
const WP_BASE = 'https://mumlifebalance.ch/wp-json/wp/v2';
// Instagram-Namen je Profil, falls die Blotato-IDs nicht in der Umgebung stehen
const INSTAGRAM_KONTO = { mentoring: 'mumlifebalance_patricia_ulmann', doterra: 'patricia_ulmann' };

/* ------------------------------------------------------------------ Helfer */

function log(msg) {
  const t = new Date().toTimeString().slice(0, 8);
  console.log(`[${t}] ${msg}`);
}

async function envLesen(datei) {
  try {
    const inhalt = await fs.readFile(datei, 'utf8');
    return Object.fromEntries(
      inhalt.split('\n')
        .filter(l => l.includes('=') && !l.trimStart().startsWith('#'))
        .map(l => {
          const [k, ...rest] = l.split('=');
          return [k.trim(), rest.join('=').trim().replace(/^["']|["']$/g, '')];
        })
    );
  } catch {
    return {};
  }
}

/** Findet die Freigabe-Datei und die zugehoerigen Bild-Dateien im Ordner. */
async function freigabeEinlesen(ordner) {
  const dateien = [];
  async function durchgehen(p) {
    for (const e of await fs.readdir(p, { withFileTypes: true })) {
      const voll = path.join(p, e.name);
      if (e.isDirectory()) await durchgehen(voll);
      else if (e.name.endsWith('.json')) dateien.push(voll);
    }
  }
  await durchgehen(ordner);

  let steuer = null;
  const bilder = [];
  for (const d of dateien) {
    const inhalt = JSON.parse(await fs.readFile(d, 'utf8'));
    if (inhalt.dataUrl) {
      bilder.push({ datei: d, name: path.basename(d, '.json'), dataUrl: inhalt.dataUrl, nr: inhalt.nr || 0 });
    } else if (inhalt.caption !== undefined || inhalt.status !== undefined) {
      steuer = inhalt;
    }
  }
  if (!steuer) throw new Error(`Keine Freigabe-Datei in ${ordner} gefunden (erwartet: caption/status).`);
  bilder.sort((a, b) => (a.nr || 0) - (b.nr || 0) || a.name.localeCompare(b.name));
  return { steuer, bilder };
}

function dataUrlZuBuffer(dataUrl) {
  const treffer = /^data:(image\/[a-z+]+);base64,(.*)$/s.exec(dataUrl);
  if (!treffer) throw new Error('Unbekanntes Bildformat in der Freigabe.');
  return { typ: treffer[1], buffer: Buffer.from(treffer[2], 'base64') };
}

/* ----------------------------------------------------------------- Video */

/**
 * Bringt das gerenderte Video auf Instagram-Mass.
 * HyperFrames rendert mit sehr hoher Bitrate — 144 MB fuer zwei Minuten sind
 * normal. Instagram kodiert ohnehin neu, deshalb wird hier vorher auf eine
 * vernuenftige Groesse gebracht. Sichtbar ist der Unterschied nicht.
 */
async function fuerInstagram(quelle, ziel) {
  const { spawn } = await import('node:child_process');
  await new Promise((res, rej) => {
    const ff = spawn('ffmpeg', [
      '-y', '-loglevel', 'error', '-i', quelle,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
      '-maxrate', '8M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-b:a', '128k', '-ar', '48000',
      '-movflags', '+faststart', ziel,
    ]);
    let fehler = '';
    ff.stderr.on('data', d => { fehler += d.toString(); });
    ff.on('close', code => code === 0 ? res() : rej(new Error('ffmpeg: ' + fehler.slice(0, 300))));
  });
  return ziel;
}

/* ------------------------------------------------------------- WordPress */

async function wpHochladen(buffer, dateiname, typ, wpEnv) {
  const auth = 'Basic ' + Buffer.from(`${wpEnv.WP_USER}:${wpEnv.WP_APP_PASSWORD}`).toString('base64');
  const res = await fetch(`${WP_BASE}/media`, {
    method: 'POST',
    headers: {
      Authorization: auth,
      'Content-Type': typ,
      'Content-Disposition': `attachment; filename="${dateiname}"`,
    },
    body: buffer,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`WordPress-Upload ${dateiname} fehlgeschlagen (HTTP ${res.status}): ${text.slice(0, 240)}`);
  const json = JSON.parse(text);
  if (!json.source_url) throw new Error(`WordPress lieferte keine URL für ${dateiname}.`);
  return json.source_url;
}

/* ---------------------------------------------------------------- Blotato */

/**
 * Kopf fuer Blotato. In der Cloud (--proxy) setzt ein Proxy den Schluessel
 * selbst ein; dann schicken wir keinen eigenen mit.
 */
function blotatoKopf(key) {
  const kopf = { 'Content-Type': 'application/json' };
  if (key) kopf['blotato-api-key'] = key;
  return kopf;
}

/**
 * Im Proxy-Modus geht jeder Aufruf ueber curl: Nodes fetch ignoriert HTTPS_PROXY,
 * ging in der Cloud am Proxy vorbei und bekam deshalb 401 (Probelauf 31.10.2026).
 * Gibt dasselbe zurueck, was hier von fetch gebraucht wird: ok, status, text().
 */
let ueberCurl = false;
async function abruf(url, { method = 'GET', headers = {}, body } = {}) {
  if (!ueberCurl) return fetch(url, { method, headers, body });
  const { spawnSync } = await import('node:child_process');
  const args = ['-s', '-X', method, '-w', '\n%{http_code}'];
  for (const [k, v] of Object.entries(headers)) args.push('-H', `${k}: ${v}`);
  if (body !== undefined) args.push('--data-binary', '@-');
  args.push(url);
  const r = spawnSync('curl', args, { input: body, maxBuffer: 64 * 1024 * 1024, encoding: 'utf8' });
  if (r.status !== 0) throw new Error(`curl fehlgeschlagen: ${(r.stderr || '').slice(0, 200)}`);
  const i = r.stdout.lastIndexOf('\n');
  const status = Number(r.stdout.slice(i + 1));
  const text = r.stdout.slice(0, i);
  return { ok: status >= 200 && status < 300, status, text: async () => text, json: async () => JSON.parse(text) };
}

/** url darf eine oeffentliche Adresse oder eine data:-URL sein (getestet 31.10.2026). */
async function blotatoMedia(url, key) {
  const res = await abruf(`${BLOTATO_BASE}/v2/media`, {
    method: 'POST',
    headers: blotatoKopf(key),
    body: JSON.stringify({ url }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Blotato-Media fehlgeschlagen (HTTP ${res.status}): ${text.slice(0, 240)}`);
  const json = JSON.parse(text);
  const gehostet = json.url || json.mediaUrl || json.publicUrl;
  if (!gehostet) throw new Error(`Blotato-Media ohne URL: ${text.slice(0, 240)}`);
  return gehostet;
}

async function blotatoPlanen({ accountId, text, mediaUrls, zeitpunkt, key, coverUrl }) {
  // Fuer Reels braucht Instagram mediaType und darf ein eigenes Coverbild bekommen.
  const target = { targetType: 'instagram' };
  if (coverUrl) {
    target.mediaType = 'reel';
    target.coverImageUrl = coverUrl;
  }
  const res = await abruf(`${BLOTATO_BASE}/v2/posts`, {
    method: 'POST',
    headers: blotatoKopf(key),
    body: JSON.stringify({
      post: {
        accountId,
        content: { text, mediaUrls, platform: 'instagram' },
        target,
      },
      scheduledTime: zeitpunkt,
    }),
  });
  const antwort = await res.text();
  if (!res.ok) throw new Error(`Blotato-Planung fehlgeschlagen (HTTP ${res.status}): ${antwort.slice(0, 300)}`);
  return JSON.parse(antwort);
}

/* ------------------------------------------------------------------- Lauf */

async function main() {
  const args = process.argv.slice(2);
  const holen = (name) => {
    const i = args.indexOf(name);
    return i === -1 ? null : args[i + 1];
  };
  const ordner = holen('--ordner');
  const trocken = args.includes('--trocken');
  // --proxy: Cloud-Lauf. Der Blotato-Schluessel kommt dort vom Proxy, nicht aus einer .env.
  const proxy = args.includes('--proxy');
  ueberCurl = proxy;
  if (!ordner) {
    console.error('Bitte --ordner <pfad> angeben (dort liegen die Freigabe-JSONs).');
    process.exit(1);
  }

  // Erst die Umgebung, dann die .env-Dateien (in der Cloud gibt es keine .env)
  const haupt = { ...(await envLesen(path.join(ROOT, '.env'))), ...process.env };
  const wpEnv = { ...(await envLesen(path.join(ROOT, 'scripts', 'wordpress', '.env'))), ...process.env };
  const key = proxy ? null : haupt.BLOTATO_API_KEY;
  const konten = {
    mentoring: haupt.BLOTATO_ACCOUNT_ID_MENTORING,
    doterra: haupt.BLOTATO_ACCOUNT_ID_DOTERRA,
  };

  const { steuer, bilder } = await freigabeEinlesen(path.resolve(ROOT, ordner));

  log(`Freigabe: ${steuer.name || 'ohne Namen'}`);
  log(`  Profil ${steuer.profil === 'doterra' ? 'doTERRA' : 'Mentoring'} · ` +
      (steuer.typ === 'reel' ? 'Reel' : `${bilder.length} Folien`));
  log(`  geplant für ${steuer.datum} ${steuer.zeit} (${steuer.zeitpunktISO || 'kein ISO-Zeitpunkt'})`);

  if (steuer.status !== 'wartet') {
    log(`  ACHTUNG: Status ist "${steuer.status}", nicht "wartet". Abbruch.`);
    process.exit(2);
  }
  if (!(steuer.caption || '').trim()) throw new Error('Die Freigabe hat keine Caption.');
  if (!steuer.zeitpunktISO) throw new Error('Die Freigabe hat keinen Zeitpunkt.');
  if (new Date(steuer.zeitpunktISO) <= new Date()) {
    throw new Error(`Der Zeitpunkt ${steuer.zeitpunktISO} liegt in der Vergangenheit.`);
  }
  const istReel = (steuer.typ === 'reel');
  if (istReel) {
    if (!steuer.videodatei) throw new Error('Die Reel-Freigabe hat keine videodatei.');
    if (bilder.length > 1) log(`  Hinweis: ${bilder.length} Bilder dabei, es wird nur das erste als Cover benutzt.`);
  } else {
    if (!bilder.length) throw new Error('Keine Folien-Bilder im Ordner gefunden.');
    if (bilder.length > 10) throw new Error(`${bilder.length} Folien — Instagram nimmt über Blotato maximal 10.`);
    if (bilder.length !== (steuer.anzahl || bilder.length)) {
      log(`  ACHTUNG: ${bilder.length} Bilder gefunden, ${steuer.anzahl} erwartet.`);
    }
  }

  // Fehlen die IDs (Cloud ohne .env), fragt das Skript Blotato nach den Konten.
  if (!konten.mentoring || !konten.doterra) {
    const res = await abruf(`${BLOTATO_BASE}/v2/users/me/accounts`, { headers: blotatoKopf(key) });
    if (!res.ok) throw new Error(`Blotato-Konten nicht lesbar (HTTP ${res.status}).`);
    const liste = (await res.json()).items || [];
    const nachName = (n) => liste.find(a => a.platform === 'instagram' && a.username === n)?.id;
    konten.mentoring ||= nachName(INSTAGRAM_KONTO.mentoring);
    konten.doterra ||= nachName(INSTAGRAM_KONTO.doterra);
  }
  const accountId = konten[steuer.profil === 'doterra' ? 'doterra' : 'mentoring'];
  if (!accountId) throw new Error('Keine Blotato-Account-ID für dieses Profil in der .env.');
  if (!key && !proxy) throw new Error('BLOTATO_API_KEY fehlt in der .env.');
  // WordPress braucht nur noch das Reel-Video; Folien und Cover gehen direkt zu Blotato.
  if (!trocken && istReel && (!wpEnv.WP_USER || !wpEnv.WP_APP_PASSWORD)) {
    throw new Error('WordPress-Zugang fehlt (scripts/wordpress/.env: WP_USER, WP_APP_PASSWORD).');
  }

  // Ergebnis sichern, damit man nachher nachschauen kann, was rausging
  const slug = (steuer.name || (istReel ? 'reel' : 'karussell')).toLowerCase()
    .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40) || 'post';
  const ablage = path.join(ROOT, 'outputs', istReel ? 'reels' : 'karussells',
                           'cockpit', `${steuer.datum}-${slug}`);
  await fs.mkdir(ablage, { recursive: true });

  const mediaUrls = [];
  let coverUrl = null;

  if (istReel) {
    // 1. das Video selbst
    const videoPfad = path.isAbsolute(steuer.videodatei)
      ? steuer.videodatei : path.join(ROOT, steuer.videodatei);
    let videoBuf = await fs.readFile(videoPfad).catch(() => {
      throw new Error(`Video nicht gefunden: ${steuer.videodatei}`);
    });
    let mb = videoBuf.length / 1024 / 1024;
    log(`  Video: ${path.basename(videoPfad)} (${mb.toFixed(1)} MB)`);

    // Immer auf Instagram-Mass bringen — das spart beim Hochladen viel Zeit.
    const kleinPfad = path.join(ablage, `${slug}.mp4`);
    await fuerInstagram(videoPfad, kleinPfad);
    videoBuf = await fs.readFile(kleinPfad);
    const neuMb = videoBuf.length / 1024 / 1024;
    log(`    umkodiert: ${neuMb.toFixed(1)} MB (${(100 - neuMb / mb * 100).toFixed(0)} % kleiner)`);
    mb = neuMb;
    if (mb > 300) throw new Error(`Video ist auch nach dem Umkodieren ${mb.toFixed(0)} MB — zu gross.`);

    // 2. das Cover
    if (bilder.length) {
      const { typ, buffer } = dataUrlZuBuffer(bilder[0].dataUrl);
      const coverName = `${slug}-cover.${typ === 'image/png' ? 'png' : 'jpg'}`;
      await fs.writeFile(path.join(ablage, coverName), buffer);
      const coverMb = buffer.length / 1024 / 1024;
      log(`  Cover: ${coverName} (${(buffer.length / 1024).toFixed(0)} KB)`);
      if (coverMb > 8) throw new Error('Das Cover ist über 8 MB — Instagram nimmt es so nicht.');
      if (!trocken) {
        coverUrl = await blotatoMedia(bilder[0].dataUrl, key);
        log(`    Cover hochgeladen -> ${coverUrl.slice(0, 70)}…`);
      } else {
        coverUrl = `(trocken) ${coverName}`;
      }
    } else {
      log('  Hinweis: kein Cover dabei — Instagram nimmt dann selbst ein Standbild.');
    }

    if (!trocken) {
      const videoName = `${slug}.mp4`;
      log('    lade Video zu WordPress …');
      const wpVideo = await wpHochladen(videoBuf, videoName, 'video/mp4', wpEnv);
      const hosted = await blotatoMedia(wpVideo, key);
      mediaUrls.push(hosted);
      log(`    Video hochgeladen -> ${hosted.slice(0, 70)}…`);
    } else {
      mediaUrls.push(`(trocken) ${slug}.mp4`);
    }
  }

  for (let i = 0; istReel ? false : i < bilder.length; i++) {
    const { typ, buffer } = dataUrlZuBuffer(bilder[i].dataUrl);
    const endung = typ === 'image/png' ? 'png' : 'jpg';
    const dateiname = `${slug}-${String(i + 1).padStart(2, '0')}.${endung}`;
    await fs.writeFile(path.join(ablage, dateiname), buffer);
    log(`  Folie ${i + 1}: ${(buffer.length / 1024).toFixed(0)} KB -> ${dateiname}`);

    if (trocken) { mediaUrls.push(`(trocken) ${dateiname}`); continue; }

    const hosted = await blotatoMedia(bilder[i].dataUrl, key);
    mediaUrls.push(hosted);
    log(`    hochgeladen -> ${hosted.slice(0, 70)}…`);
  }

  log(`Ergebnis liegt in ${path.relative(ROOT, ablage)}`);

  if (trocken) {
    log('');
    log('TROCKENLAUF — es wurde nichts hochgeladen und nichts eingeplant.');
    log(`Es würde gepostet: ${steuer.zeitpunktISO}, Konto ${accountId}, ` +
        (istReel ? `als Reel${coverUrl ? ' mit eigenem Cover' : ' ohne Cover'}.`
                 : `${mediaUrls.length} Folien.`));
    log(`Caption-Anfang: ${(steuer.caption || '').slice(0, 90).replace(/\n/g, ' ')}…`);
    return;
  }

  const ergebnis = await blotatoPlanen({
    accountId, text: steuer.caption, mediaUrls,
    zeitpunkt: steuer.zeitpunktISO, key, coverUrl,
  });
  log('');
  log(`EINGEPLANT für ${steuer.datum} ${steuer.zeit}.`);
  log(`Blotato-Antwort: ${JSON.stringify(ergebnis).slice(0, 200)}`);

  await fs.writeFile(
    path.join(ablage, 'blotato-ergebnis.json'),
    JSON.stringify({ steuer, mediaUrls, ergebnis, eingeplantAm: new Date().toISOString() }, null, 2),
    'utf8'
  );
}

main().catch((e) => {
  console.error('\nFEHLER: ' + e.message);
  process.exit(1);
});
