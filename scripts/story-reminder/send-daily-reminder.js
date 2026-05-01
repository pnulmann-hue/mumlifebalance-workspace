/**
 * Story Daily Reminder — Mo-So 06:30 Schweiz
 *
 * Liest active-funnels.json + wochen-log.json + wochen-kontext-KW##.json + Override.
 * Berechnet: Profil · Modus · DISG-Achse · Aktives Produkt.
 * Schickt Telegram-DM an Patricia_content_bot.
 * Initialisiert _state/briefing-pending.json mit Status "warten_auf_antwort".
 *
 * Aufruf:
 *   node send-daily-reminder.js
 *
 * Env-Vars (in GitHub Actions als Secrets):
 *   STORY_BOT_TOKEN — Patricia_content_bot Telegram-Token
 *   STORY_CHAT_ID — Patricia's Chat-ID mit dem Bot
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..', '..');

const TELEGRAM_TOKEN = process.env.STORY_BOT_TOKEN;
const CHAT_ID = process.env.STORY_CHAT_ID;

if (!TELEGRAM_TOKEN || !CHAT_ID) {
  console.error('FEHLER: STORY_BOT_TOKEN oder STORY_CHAT_ID fehlt in env.');
  process.exit(1);
}

// ---------- Helpers ----------

function getCH_DateInfo() {
  const now = new Date();
  // Schweiz CET/CEST — vereinfacht: für Cron ist UTC angegeben, hier rechnen wir lokal weiter
  const wochentage = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
  const wochentagFull = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  const day = now.getUTCDay();

  // ISO-Wochennummer
  const target = new Date(now.valueOf());
  const dayNr = (now.getUTCDay() + 6) % 7;
  target.setUTCDate(target.getUTCDate() - dayNr + 3);
  const firstThursday = target.valueOf();
  target.setUTCMonth(0, 1);
  if (target.getUTCDay() !== 4) {
    target.setUTCMonth(0, 1 + ((4 - target.getUTCDay()) + 7) % 7);
  }
  const week = 1 + Math.ceil((firstThursday - target) / 604800000);

  return {
    wochentag_kurz: wochentage[day],
    wochentag: wochentagFull[day],
    datum_iso: now.toISOString().slice(0, 10),
    datum_de: now.toLocaleDateString('de-CH', { day: '2-digit', month: '2-digit', year: 'numeric' }),
    kw: week,
    day_index: day, // 0=So, 1=Mo, ..., 6=Sa
  };
}

async function readJsonSafe(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    return null;
  }
}

// ---------- Logik ----------

function pickProfil(dayIndex) {
  // Mo/Mi/Fr → Mentoring  · Di/Do/Sa → doTERRA · So → Mentoring (Default)
  const map = {
    0: 'mentoring',  // So
    1: 'mentoring',  // Mo
    2: 'doterra',    // Di
    3: 'mentoring',  // Mi
    4: 'doterra',    // Do
    5: 'mentoring',  // Fr
    6: 'doterra',    // Sa
  };
  return map[dayIndex];
}

function pickDisgAchse(wochenLog, dayIndex) {
  // Standard-Rotation
  const standard = {
    0: { haupt: 'Rot', sek: 'Blau' },     // So
    1: { haupt: 'Grün', sek: 'Gelb' },    // Mo
    2: { haupt: 'Rot', sek: 'Blau' },     // Di
    3: { haupt: 'Gelb', sek: 'Grün' },    // Mi
    4: { haupt: 'Blau', sek: 'Rot' },     // Do
    5: { haupt: 'Gelb', sek: 'Grün' },    // Fr
    6: { haupt: 'Grün', sek: 'Gelb' },    // Sa
  };

  if (!wochenLog) return standard[dayIndex];

  // Welche Achsen wurden in den letzten 7 Tagen abgedeckt?
  const heute = new Date();
  const vor7Tagen = new Date(heute.valueOf() - 7 * 24 * 3600 * 1000);
  const abgedeckt = new Set();

  for (const [datum, eintrag] of Object.entries(wochenLog)) {
    const eintragDate = new Date(datum);
    if (eintragDate >= vor7Tagen && eintrag.disg) {
      abgedeckt.add(eintrag.disg);
    }
  }

  // Welche Achsen fehlen noch in dieser Woche?
  const alle = ['Rot', 'Gelb', 'Grün', 'Blau'];
  const fehlend = alle.filter(t => !abgedeckt.has(t));

  if (fehlend.length > 0) {
    return { haupt: fehlend[0], sek: fehlend[1] || standard[dayIndex].sek };
  }
  return standard[dayIndex];
}

function disgToNadja(disg) {
  const map = {
    'Rot': 'Charlie / Stefan',
    'Gelb': 'Isabell',
    'Grün': 'Werner / Petra',
    'Blau': 'Wilma / Bärbel',
  };
  return map[disg] || disg;
}

function pickModus(activeFunnels, dayIndex, profil) {
  // Wenn ein Funnel `live-launch-woche` für dieses Profil hat → Sales-Day
  if (activeFunnels && Array.isArray(activeFunnels.funnels)) {
    for (const f of activeFunnels.funnels) {
      if ((f.status === 'live-launch-woche' || f.status === 'launching') &&
          (f.profil === profil || f.profil === 'beide')) {
        return 'sales-day';
      }
    }
  }

  // Sonntag = Tagesplan mit Reflexions-Akzent
  if (dayIndex === 0) return 'tagesplan';

  // Mo-Sa = Tagesplan
  return 'tagesplan';
}

function pickAktivesProdukt(activeFunnels, profil, override) {
  if (override && override.produkt) return override.produkt;

  if (!activeFunnels || !Array.isArray(activeFunnels.funnels)) {
    return profil === 'mentoring' ? 'Bio-Check' : 'doTERRA Lifestyle';
  }

  // Priorität: live-launch-woche > launching > live
  const prio = ['live-launch-woche', 'launching', 'live'];
  for (const status of prio) {
    const found = activeFunnels.funnels.find(f =>
      f.status === status && (f.profil === profil || f.profil === 'beide')
    );
    if (found) return found.name || found.slug || 'Unbekannt';
  }

  return profil === 'mentoring' ? 'Bio-Check' : 'doTERRA Lifestyle';
}

function pickStorySaeule(disg) {
  // Grobe Heuristik nach 3-Säulen-Bibliothek
  if (disg === 'Rot' || disg === 'Blau') return 'Expertise';
  if (disg === 'Gelb') return 'Inspiration';
  return 'Persönlichkeit'; // Grün
}

// ---------- Telegram ----------

async function sendTelegramMessage(text) {
  const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text,
      parse_mode: 'HTML',
    }),
  });
  const data = await response.json();
  if (!data.ok) {
    throw new Error(`Telegram-Send failed: ${JSON.stringify(data)}`);
  }
  return data.result;
}

// ---------- Main ----------

async function main() {
  const dateInfo = getCH_DateInfo();

  // Daten lesen
  const activeFunnelsPath = path.join(REPO_ROOT, 'context', 'active-funnels.json');
  const wochenLogPath = path.join(REPO_ROOT, 'outputs', 'stories', 'wochen-log.json');
  const wochenKontextPath = path.join(REPO_ROOT, 'outputs', 'stories', `wochen-kontext-KW${dateInfo.kw}.json`);
  const overridePath = path.join(REPO_ROOT, 'outputs', 'stories', '_state', 'wochen-fokus-override.json');
  const briefingPendingPath = path.join(REPO_ROOT, 'outputs', 'stories', '_state', 'briefing-pending.json');

  const [activeFunnels, wochenLog, wochenKontext, override] = await Promise.all([
    readJsonSafe(activeFunnelsPath),
    readJsonSafe(wochenLogPath),
    readJsonSafe(wochenKontextPath),
    readJsonSafe(overridePath),
  ]);

  // Logik
  const profil = pickProfil(dateInfo.day_index);
  const disg = pickDisgAchse(wochenLog, dateInfo.day_index);
  const modus = pickModus(activeFunnels, dateInfo.day_index, profil);
  const aktivesProdukt = pickAktivesProdukt(activeFunnels, profil, override);
  const storySaeule = pickStorySaeule(disg.haupt);
  const nadjaPersona = disgToNadja(disg.haupt);

  // Wochen-Fokus aus Notion-Cache
  const wochenFokus = wochenKontext?.fokus_der_woche || override?.thema || '(kein Fokus eingetragen)';

  // Telegram-DM bauen
  const profileLabel = profil === 'mentoring' ? '🟦 Mentoring' : '🟠 doTERRA';
  const modusLabel = modus === 'sales-day' ? '🔥 Sales-Day (Launch aktiv)' : '📅 Tagesplan';

  const text = `🌅 <b>Guten Morgen, Patricia!</b>

<b>Heute:</b> ${dateInfo.wochentag}, ${dateInfo.datum_de}
<b>Profil:</b> ${profileLabel}
<b>Modus:</b> ${modusLabel}
<b>Aktives Produkt:</b> ${aktivesProdukt}
<b>Wochen-Fokus:</b> ${wochenFokus}

<b>Käufertyp heute:</b> ${disg.haupt} (${nadjaPersona})
<b>Story-Säule:</b> ${storySaeule}

—

Bevor ich rendere — was war heute / gestern bei dir?

• Was hast du erlebt? (Konflikt, Erfolg, peinlicher Moment, Erkenntnis, Familien-Szene...)
• Hast du grad einen Gedanken zum Thema?
• Oder soll ich aus deinem Standard-Pool ziehen? Tipp dann nur "<b>standard</b>".

Schick mir Sprachnotiz (Wispr Flow) oder kurz tippen.

—

<i>Wenn du heute keine Stories machen willst: tipp "skip" und ich frag morgen wieder.</i>`;

  // Schicke Telegram
  console.log(`Schicke Reminder für ${dateInfo.datum_de} (${profil}, ${modus}, ${disg.haupt})...`);
  const result = await sendTelegramMessage(text);
  console.log(`✅ Reminder gesendet — Message-ID: ${result.message_id}`);

  // Schreibe briefing-pending.json
  const stateDir = path.dirname(briefingPendingPath);
  await fs.mkdir(stateDir, { recursive: true });

  const briefingState = {
    profil,
    modus,
    disg: disg.haupt,
    disg_sekundaer: disg.sek,
    nadja_persona: nadjaPersona,
    story_saeule: storySaeule,
    aktives_produkt: aktivesProdukt,
    wochen_fokus: wochenFokus,
    kontext_snapshot: {
      kw: dateInfo.kw,
      wochentag: dateInfo.wochentag,
      datum: dateInfo.datum_iso,
    },
    fragen: [
      'Was hast du erlebt?',
      'Hast du grad einen Gedanken zum Thema?',
      'Oder Standard-Pool?',
    ],
    gesendet_am: new Date().toISOString(),
    telegram_message_id: result.message_id,
    patricia_antworten: [],
    patricia_fotos: [],
    patricia_videos: [],
    status: 'warten_auf_antwort',
  };

  await fs.writeFile(briefingPendingPath, JSON.stringify(briefingState, null, 2) + '\n', 'utf8');
  console.log(`✅ State geschrieben: ${briefingPendingPath}`);

  console.log('\nFertig.');
}

main().catch(err => {
  console.error('FEHLER:', err);
  process.exit(1);
});
