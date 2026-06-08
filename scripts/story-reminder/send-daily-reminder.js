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

// Fallback auf lokale .env-Variablennamen wenn die GitHub-Secret-Namen fehlen
const TELEGRAM_TOKEN = process.env.STORY_BOT_TOKEN || process.env.TELEGRAM_CONTENT_BOT_TOKEN;
const CHAT_ID = process.env.STORY_CHAT_ID || process.env.TELEGRAM_CHAT_ID;

// Notion (Wochenplan der aktuellen Woche live lesen)
const NOTION_TOKEN = process.env.NOTION_API_KEY || process.env.NOTION_TOKEN;
const NOTION_WOCHEN_DB = process.env.NOTION_DB_WOCHENPLANUNG || '2ae7078e-8b7e-81ef-a769-cdb1a6584c70';
const NOTION_MONAT_DB = process.env.NOTION_DB_MONATSPLANUNG || '2ae7078e-8b7e-8171-a760-c233083c26b6';

// Anthropic (für den proaktiven Julia-Story-Vorschlag im Kein-Launch-Modus)
const ANTHROPIC_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_MODEL = process.env.STORY_IDEE_MODEL || 'claude-haiku-4-5-20251001';

console.log('Story-Reminder gestartet.');
console.log(`STORY_BOT_TOKEN: ${TELEGRAM_TOKEN ? '✅ gesetzt (Länge ' + TELEGRAM_TOKEN.length + ')' : '❌ fehlt'}`);
console.log(`STORY_CHAT_ID: ${CHAT_ID ? '✅ gesetzt (' + CHAT_ID + ')' : '❌ fehlt'}`);

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

function notionRichText(prop) {
  if (!prop) return '';
  const arr = prop.rich_text || prop.title || [];
  return arr.map(t => t.plain_text || '').join('').trim();
}

// Liest den Wochenplan der AKTUELLEN Woche aus Notion (Zeitraum enthält heute).
// Liefert { title, fokus, salesPattern } oder null (kein Token / keine passende Woche).
async function fetchNotionWoche(dateIso) {
  if (!NOTION_TOKEN) {
    console.log('NOTION_API_KEY/NOTION_TOKEN fehlt — Wochen-Fokus aus Notion wird uebersprungen.');
    return null;
  }
  try {
    const res = await fetch(`https://api.notion.com/v1/databases/${NOTION_WOCHEN_DB}/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sorts: [{ property: 'Zeitraum', direction: 'descending' }],
        page_size: 25,
      }),
    });
    if (!res.ok) {
      console.log(`Notion-Query fehlgeschlagen (HTTP ${res.status}).`);
      return null;
    }
    const data = await res.json();
    for (const page of data.results || []) {
      const z = page.properties?.['Zeitraum']?.date;
      if (!z || !z.start) continue;
      const start = z.start.slice(0, 10);
      const end = (z.end || z.start).slice(0, 10);
      if (start <= dateIso && dateIso <= end) {
        return {
          title: notionRichText(page.properties?.['Woche']),
          fokus: notionRichText(page.properties?.['Fokus der Woche']),
          salesPattern: notionRichText(page.properties?.['📅 Sales-Pattern']),
          cta: notionRichText(page.properties?.['Wochen-CTA']),
        };
      }
    }
    console.log('Keine Notion-Woche enthaelt das heutige Datum — Fallback.');
    return null;
  } catch (err) {
    console.log('Notion-Fehler:', err.message);
    return null;
  }
}

// Liest den Monatsplan des AKTUELLEN Monats aus Notion (Zeitraum enthält heute).
// Gibt dem Bot den Monats-Kontext (Verkaufs-Storyline). Liefert { title, fokus } oder null.
async function fetchNotionMonat(dateIso) {
  if (!NOTION_TOKEN) return null;
  try {
    const res = await fetch(`https://api.notion.com/v1/databases/${NOTION_MONAT_DB}/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ sorts: [{ property: 'Zeitraum', direction: 'descending' }], page_size: 25 }),
    });
    if (!res.ok) { console.log(`Monatsplan-Query fehlgeschlagen (HTTP ${res.status}).`); return null; }
    const data = await res.json();
    for (const page of data.results || []) {
      const z = page.properties?.['Zeitraum']?.date;
      if (!z || !z.start) continue;
      const start = z.start.slice(0, 10);
      const end = (z.end || z.start).slice(0, 10);
      if (start <= dateIso && dateIso <= end) {
        return {
          title: notionRichText(page.properties?.['Monat + Jahr']),
          fokus: notionRichText(page.properties?.['✏️ Begründung Fokus']),
        };
      }
    }
    return null;
  } catch (err) {
    console.log('Monatsplan-Fehler:', err.message);
    return null;
  }
}

// Findet das Produkt/den Funnel, der zur aktuellen Woche passt (Match über ID/Name/Keyword
// im Wochen-Text), damit der Content sich auf dessen Themen beziehen kann.
function matchProdukt(textBlob, activeFunnels) {
  if (!activeFunnels || !Array.isArray(activeFunnels.funnels) || !textBlob) return null;
  const blob = textBlob.toLowerCase();
  const treffer = activeFunnels.funnels.filter(f => {
    const name = (f.name || '').toLowerCase();
    const id = (f.id || '').toLowerCase();
    const kw = (f.content_hinweise?.primaer_keyword || '').toLowerCase();
    return (id && blob.includes(id)) ||
           (name && name.length > 4 && blob.includes(name)) ||
           (kw && blob.includes(kw));
  });
  if (!treffer.length) return null;
  treffer.sort((a, b) => (b.name || '').length - (a.name || '').length); // spezifischster zuerst
  const f = treffer[0];
  return {
    name: f.name || '',
    painpoint: f.problem || '',
    transformation: f.transformation || '',
    zielgruppe: f.zielgruppe || '',
    pillar: f.content_hinweise?.pillar || '',
  };
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

// ---------- Julia-Story-Vorschlag (Kein-Launch-Modus) ----------

// Findet den nächsten/aktiven Launch (Funnel mit launch_window, dessen Cart-Close noch nicht vorbei ist).
function findUpcomingLaunch(activeFunnels, todayIso) {
  if (!activeFunnels || !Array.isArray(activeFunnels.funnels)) return null;
  let best = null;
  for (const f of activeFunnels.funnels) {
    const lw = f.launch_window;
    if (!lw) continue;
    const aufw = String(lw.aufwaerm_start_datum || lw.aufwaerm_start || '').slice(0, 10);
    const close = String(lw.cart_close_datum || lw.cart_close || '').slice(0, 10);
    if (!close || todayIso > close) continue; // Launch ist vorbei
    if (!best || (aufw && aufw < best.aufw)) best = { id: f.id, name: f.name || f.id, aufw, close };
  }
  return best;
}

// Generiert EINEN konkreten, spezifischen Story-Vorschlag aus Julias 3-Säulen-Ideen,
// gematcht auf den heutigen Kontext. Gibt einen kurzen Text zurück oder null (kein Key / Fehler).
async function generateJuliaIdee(ctx) {
  if (!ANTHROPIC_KEY) {
    console.log('ANTHROPIC_API_KEY fehlt — proaktiver Julia-Vorschlag wird uebersprungen.');
    return null;
  }
  let bibliothek = '';
  try {
    bibliothek = await fs.readFile(path.join(REPO_ROOT, 'context', 'julia-story-ideen.md'), 'utf8');
    bibliothek = bibliothek.slice(0, 8000);
  } catch {
    console.log('julia-story-ideen.md nicht lesbar — Vorschlag wird uebersprungen.');
    return null;
  }

  const prompt = `Du bist Patricias Story-Ideen-Assistentin und machst ihr EINEN konkreten, spezifischen Vorschlag, was sie HEUTE in ihre Instagram-Stories packen könnte. Kein generischer Allgemeinplatz — etwas, das zum heutigen Kontext passt und sofort umsetzbar ist.

HEUTIGER KONTEXT:
- Profil: ${ctx.profil === 'mentoring' ? 'Mentoring (Network-Mamas, die ein eigenes Business aufbauen wollen)' : 'doTERRA (erschöpfte Mamas 35+, Vormenopause/Energie)'}
- Story-Säule heute: ${ctx.storySaeule}
- Käufertyp heute: ${ctx.disg} (${ctx.persona})
- Aktives Produkt/Funnel: ${ctx.produkt}${ctx.painpoint ? `\n- Painpoint des Produkts: ${ctx.painpoint}` : ''}${ctx.wochenFokus ? `\n- Wochen-Fokus: ${ctx.wochenFokus}` : ''}${ctx.monatKontext ? `\n- Monats-Kontext: ${ctx.monatKontext}` : ''}${ctx.wochenCTA ? `\n- CTA der Woche: ${ctx.wochenCTA}` : ''}
${ctx.phaseHinweis ? `\n⏰ LAUNCH-TIMING (HAT VORRANG vor allem oben):\n${ctx.phaseHinweis}\n` : ''}
JULIAS STORY-IDEEN-BIBLIOTHEK (Muster, nicht 1:1 kopieren):
${bibliothek}

REGELN (zwingend):
- Patricias Stimme: warm, wie am Küchentisch mit einer Freundin, DU-Anrede für den Schmerz.
- KEINE Stakkato-Sätze (nie 3 abgehackte Subjekt-Verb-Punkt-Sätze; verbinde mit "und", "weil", "aber", "bis").
- Schweizer ss statt ß, echte Umlaute (ä/ö/ü).
- KEINE erfundenen Zahlen.
- NIEMALS die Formulierung "stell dir vor".
- Erwähne NIEMALS den Namen "Julia" oder eine Mentorin.
- ${ctx.profil === 'doterra' ? 'doTERRA: kein Heilversprechen, "bei mir war"-Frame.' : 'Network-Mama-Realität konkret (Teamchat, Downline, Produktbilder, warme Liste).'}

ANTWORTE GENAU IN DIESEM FORMAT (max 60 Wörter, kein Vorspann):
Idee: <1-2 Sätze: konkreter Aufhänger/Szene, die sie heute zeigen oder erzählen könnte>
Muster: <Säule + welches Julia-Muster, kurz>
CTA: <konkreter CTA, passend zum aktiven Produkt>`;

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': ANTHROPIC_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 350,
        messages: [{ role: 'user', content: prompt }],
      }),
    });
    if (!res.ok) {
      console.log(`Anthropic-Call fehlgeschlagen (HTTP ${res.status}) — Vorschlag wird uebersprungen.`);
      return null;
    }
    const data = await res.json();
    const text = (data.content || []).map(b => b.text || '').join('').trim();
    return text || null;
  } catch (err) {
    console.log('Anthropic-Fehler:', err.message);
    return null;
  }
}

// Wandelt den Vorschlags-Rohtext (Idee/Muster/CTA-Zeilen) in HTML für Telegram um.
function formatVorschlagHtml(roh) {
  if (!roh) return '';
  const escaped = roh
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const withBold = escaped
    .replace(/^Idee:/im, '<b>Idee:</b>')
    .replace(/^Muster:/im, '<b>Muster:</b>')
    .replace(/^CTA:/im, '<b>CTA:</b>');
  return `💡 <b>Mein Vorschlag für heute</b> (aus deiner Story-Ideen-Bibliothek):\n${withBold}`;
}

// ---------- Telegram ----------

async function sendTelegramMessage(text) {
  const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;
  console.log(`Schicke Telegram-DM an chat_id=${CHAT_ID}...`);

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: CHAT_ID,
        text,
        parse_mode: 'HTML',
      }),
    });
  } catch (err) {
    throw new Error(`Network error beim Telegram-Call: ${err.message}`);
  }

  const responseText = await response.text();
  let data;
  try {
    data = JSON.parse(responseText);
  } catch {
    throw new Error(`Telegram-Response war kein JSON (HTTP ${response.status}): ${responseText.slice(0, 500)}`);
  }

  if (!data.ok) {
    // Häufige Fehler erklären
    let hint = '';
    if (data.error_code === 401) hint = '\n→ Token ungültig. Check STORY_BOT_TOKEN bei @BotFather.';
    if (data.error_code === 400 && data.description?.includes('chat not found')) {
      hint = '\n→ Chat-ID falsch ODER Bot wurde noch nie /start im Chat. Schreib dem Bot zuerst ein „/start" im Telegram.';
    }
    if (data.error_code === 403) hint = '\n→ Bot wurde blockiert oder hat keine Schreibrechte in dem Chat.';

    throw new Error(`Telegram-API hat abgelehnt (HTTP ${response.status}): ${JSON.stringify(data)}${hint}`);
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

  const storyPlanPath = path.join(REPO_ROOT, 'outputs', 'produkte', 'mba-launch', 'story-plan.json');

  const [activeFunnels, wochenLog, wochenKontext, override, storyPlan] = await Promise.all([
    readJsonSafe(activeFunnelsPath),
    readJsonSafe(wochenLogPath),
    readJsonSafe(wochenKontextPath),
    readJsonSafe(overridePath),
    readJsonSafe(storyPlanPath),
  ]);

  // 🚀 MBA-Launch-Modus: Wenn heute ein Tag im Launch-Story-Plan ist, hat das VORRANG.
  const launchTag = storyPlan?.tage?.[dateInfo.datum_iso] || null;

  // 📅 Wochenplan + 📆 Monatsplan der aktuellen Periode LIVE aus Notion (statt aus Funnel-Status zu raten).
  const notionWoche = await fetchNotionWoche(dateInfo.datum_iso);
  const notionMonat = await fetchNotionMonat(dateInfo.datum_iso);

  // Logik
  const profil = pickProfil(dateInfo.day_index);
  const disg = pickDisgAchse(wochenLog, dateInfo.day_index);
  const modus = pickModus(activeFunnels, dateInfo.day_index, profil);
  const aktivesProdukt = override?.produkt || notionWoche?.title || pickAktivesProdukt(activeFunnels, profil, override);
  const storySaeule = pickStorySaeule(disg.haupt);
  const nadjaPersona = disgToNadja(disg.haupt);

  // Wochen-Fokus: Notion-Live zuerst, dann Cache/Override.
  const wochenFokus = notionWoche?.fokus || wochenKontext?.fokus_der_woche || override?.thema || '(kein Fokus eingetragen)';
  const salesPattern = notionWoche?.salesPattern || '';
  const wochenCTA = notionWoche?.cta || '';
  const monatKontext = notionMonat?.fokus || notionMonat?.title || '';
  // 🎯 Produkt-Themen zum aktuellen Wochen-Produkt (Painpoint/Transformation/Pillar) für zielgenauen Content.
  const produktThemen = matchProdukt(`${notionWoche?.title || ''} ${wochenFokus} ${wochenCTA}`, activeFunnels);

  // ⏰ Launch-Timing-Disziplin: VOR der Aufwärmphase noch kein Produkt/Webinar pushen (nur Reichweite).
  let phaseHinweis = null;
  if (!launchTag) {
    const launch = findUpcomingLaunch(activeFunnels, dateInfo.datum_iso);
    if (launch && launch.aufw && dateInfo.datum_iso < launch.aufw) {
      phaseHinweis = `Die Launch-Aufwärmphase für „${launch.name}" startet erst am ${launch.aufw}. Heute (${dateInfo.datum_iso}) ist noch DAVOR — mach deshalb KEINEN Verkaufs-, Webinar- oder Anmelde-CTA und bewirb das Produkt/Programm NICHT. Heute zählt nur Reichweite und echte Verbindung; der CTA ist eine weiche Engagement-Frage oder „Teile das in deiner Story", niemals ein Link oder eine Anmeldung. Diese Regel hat Vorrang vor dem aktiven Produkt und dem Wochen-CTA.`;
    }
  }

  // 💡 Kein-Launch-Modus: proaktiven, konkreten Story-Vorschlag aus Julias Ideen-Bibliothek generieren.
  let vorschlagRoh = null;
  if (!launchTag) {
    vorschlagRoh = await generateJuliaIdee({
      profil,
      storySaeule,
      disg: disg.haupt,
      persona: nadjaPersona,
      produkt: aktivesProdukt,
      painpoint: produktThemen?.painpoint || '',
      wochenFokus,
      monatKontext,
      wochenCTA,
      phaseHinweis,
    });
  }
  const vorschlagBlock = vorschlagRoh ? `${formatVorschlagHtml(vorschlagRoh)}\n\n—\n\n` : '';

  // Telegram-DM bauen
  const profileLabel = profil === 'mentoring' ? '🟦 Mentoring' : '🟠 doTERRA';
  const modusLabel = launchTag
    ? `🚀 MBA-LAUNCH (${launchTag.phase})`
    : (modus === 'sales-day' ? '🔥 Sales-Day (Launch aktiv)' : '📅 Tagesplan');

  const launchBlock = launchTag ? `🚀 <b>HEUTE IM MBA-LAUNCH</b> — Phase: ${launchTag.phase}
<b>Story:</b> ${launchTag.story_typ}
<b>Käufertyp heute:</b> ${launchTag.kaeufertyp}
<b>Das soll rein:</b> ${launchTag.inhalt}
<b>CTA:</b> ${launchTag.cta}
<i>(Julia-Vorlage ${launchTag.beleg} · Bausteine: context/julia-launch-story-bausteine.md)</i>

—

` : '';

  const frageBlock = launchTag
    ? `Schick mir, was heute/gestern bei dir war, das ich für DIESE Story nutzen kann (Erlebnis, Szene, Gedanke) — den Hook + Aufbau mach ich nach Julias Vorlage.

• Sprachnotiz (Wispr Flow) oder kurz tippen.
• Kein Erlebnis? Tipp "<b>standard</b>" — dann bau ich die Story aus dem Plan + deinem Profil.`
    : `Bevor ich rendere — was war heute / gestern bei dir?

• Was hast du erlebt? (Konflikt, Erfolg, peinlicher Moment, Erkenntnis, Familien-Szene...)
• Hast du grad einen Gedanken zum Thema?${vorschlagRoh ? '\n• Gefällt dir mein Vorschlag oben? Tipp "<b>ja</b>" — dann bau ich den.\n• Oder "<b>standard</b>" für eine andere Idee aus dem Pool.' : '\n• Oder soll ich aus deinem Standard-Pool ziehen? Tipp dann nur "<b>standard</b>".'}

Schick mir Sprachnotiz (Wispr Flow) oder kurz tippen.`;

  const text = `🌅 <b>Guten Morgen, Patricia!</b>

<b>Heute:</b> ${dateInfo.wochentag}, ${dateInfo.datum_de}
<b>Profil:</b> ${profileLabel}${monatKontext ? `\n<b>📆 Monat:</b> ${monatKontext}` : ''}
<b>Modus:</b> ${modusLabel}
<b>Aktives Produkt:</b> ${aktivesProdukt}
<b>Wochen-Fokus:</b> ${wochenFokus}${salesPattern ? `\n<b>Sales-Pattern:</b> ${salesPattern}` : ''}${wochenCTA ? `\n<b>🔗 CTA diese Woche:</b> ${wochenCTA}` : ''}${produktThemen?.painpoint ? `\n<b>🎯 Painpoint des Produkts:</b> ${produktThemen.painpoint}` : ''}

${launchBlock}<b>Käufertyp heute:</b> ${disg.haupt} (${nadjaPersona})
<b>Story-Säule:</b> ${storySaeule}

—

${vorschlagBlock}${frageBlock}

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
    sales_pattern: salesPattern,
    wochen_cta: wochenCTA,
    monat_kontext: monatKontext,
    produkt_themen: produktThemen,
    vorschlag_idee: vorschlagRoh,
    wochen_fokus_quelle: notionWoche ? 'notion-live' : 'fallback',
    launch_tag: launchTag,
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
