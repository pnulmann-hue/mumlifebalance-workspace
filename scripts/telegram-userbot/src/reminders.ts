/**
 * Alle zeitgesteuerten Reminder für Patricia.
 * Wird vom Userbot täglich geprüft (einmal morgens).
 *
 * Reminder-Typen:
 * 1. Teamcall-Reminder — 1 Woche vor dem 2. Montag im Monat
 * 2. Saison-Reminder — 1 Woche vor meteorologischem Saisonstart
 * 3. Monats-Aktions-Reminder — 1. des Monats (Newsletter + Aktionen)
 */

import Anthropic from "@anthropic-ai/sdk";
import { sendPlainDM } from "./notify";
import { generateSeasonPlan, Season as ContentSeason } from "./content-generator";

let _anthropic: Anthropic | null = null;
function anthropic(): Anthropic {
  if (!_anthropic) {
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

const MONTHS_DE = [
  "Januar", "Februar", "März", "April", "Mai", "Juni",
  "Juli", "August", "September", "Oktober", "November", "Dezember",
];

// ========== TEAMCALL ==========

export function secondMondayOfMonth(year: number, month: number): Date {
  const firstDay = new Date(year, month, 1);
  const firstDow = firstDay.getDay();
  let daysToFirstMonday: number;
  if (firstDow === 0) daysToFirstMonday = 1;
  else if (firstDow === 1) daysToFirstMonday = 0;
  else daysToFirstMonday = 8 - firstDow;
  return new Date(year, month, 1 + daysToFirstMonday + 7);
}

function teamcallReminderDate(year: number, month: number): Date {
  const tc = secondMondayOfMonth(year, month);
  const r = new Date(tc);
  r.setDate(tc.getDate() - 7);
  return r;
}

export function isTeamcallReminderToday(today: Date = new Date()): boolean {
  const r = teamcallReminderDate(today.getFullYear(), today.getMonth());
  return (
    r.getFullYear() === today.getFullYear() &&
    r.getMonth() === today.getMonth() &&
    r.getDate() === today.getDate()
  );
}

async function brainstormCallTopic(monthName: string): Promise<string> {
  const prompt = `Du bist Business-Coach von Patricia, doTERRA Teamleaderin bei "Mum Life Balance" mit Positionierung "erschöpfte Mamas aus dem Überlebensmodus holen" (5 Säulen: Schlaf, Ernährung, Stressmanagement, NEM, Bewegung).

Brainstorme 5 konkrete Themen für den Teamcall im ${monthName} (2. Montag). Mix aus Business (Instagram, Positionierung, Teamaufbau) und Mindset. Konkret, umsetzbar, saisonal passend.

Format: 5 nummerierte Vorschläge, je Titel + 1-2 Sätze Beschreibung. Deutsch, warm.`;

  try {
    const r = await anthropic().messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 800,
      messages: [{ role: "user", content: prompt }],
    });
    const c = r.content[0];
    return c.type === "text" ? c.text : "";
  } catch {
    return "Konnte keine Ideen generieren.";
  }
}

export async function sendTeamcallReminder(userId: number): Promise<void> {
  const today = new Date();
  const tc = secondMondayOfMonth(today.getFullYear(), today.getMonth());
  const monthName = MONTHS_DE[today.getMonth()];
  const callDateStr = `${tc.getDate()}. ${monthName}`;

  const brainstorm = await brainstormCallTopic(monthName);

  const msg = `🎯 *Teamcall-Reminder*

Hey Patricia! In genau einer Woche ist Teamcall — *Montag, ${callDateStr}* 💪

━━━━━━━━━━━━━━━━━
📨 *Einladung rausschicken*
━━━━━━━━━━━━━━━━━
Jetzt der richtige Moment:
• WhatsApp-Gruppe ans Team
• Kalender-Einträge
• Persönliche DMs an inaktive Beraterinnen

━━━━━━━━━━━━━━━━━
💡 *Themen-Ideen*
━━━━━━━━━━━━━━━━━
${brainstorm}

━━━━━━━━━━━━━━━━━
Sag mir welches Thema dich anspricht — dann helfe ich beim Ausarbeiten! ✨`;

  await sendPlainDM(userId, msg);
}

// ========== SAISON ==========

/**
 * Meteorologische Saisons:
 * - Frühling: 1. März
 * - Sommer: 1. Juni
 * - Herbst: 1. September
 * - Winter: 1. Dezember
 *
 * Reminder: 7 Tage vor Saisonstart.
 */

const SEASON_STARTS = [
  { month: 2, day: 1, name: "Frühling", emoji: "🌸" }, // März
  { month: 5, day: 1, name: "Sommer", emoji: "☀️" }, // Juni
  { month: 8, day: 1, name: "Herbst", emoji: "🍂" }, // September
  { month: 11, day: 1, name: "Winter", emoji: "❄️" }, // Dezember
];

export function getSeasonReminderToday(today: Date = new Date()): typeof SEASON_STARTS[number] | null {
  for (const s of SEASON_STARTS) {
    const seasonStart = new Date(today.getFullYear(), s.month, s.day);
    // Wenn Saison im nächsten Jahr liegt (z.B. jetzt ist Feb, Reminder für nächstes Jahr Winter?)
    // Für Jahreswechsel: Dez-Reminder ist im Nov des gleichen Jahres — daher egal
    const reminder = new Date(seasonStart);
    reminder.setDate(seasonStart.getDate() - 7);
    if (
      reminder.getFullYear() === today.getFullYear() &&
      reminder.getMonth() === today.getMonth() &&
      reminder.getDate() === today.getDate()
    ) {
      return s;
    }
  }
  return null;
}

export async function sendSeasonReminder(
  userId: number,
  season: typeof SEASON_STARTS[number]
): Promise<void> {
  // Neue Version: Startet automatisch die Content-Generierung!
  const groupId = parseInt(process.env.TELEGRAM_CONTENT_GROUP_ID || "-4518699226");
  const seasonKey = seasonToKey(season.name);
  const year = new Date().getFullYear();

  // Initial-DM
  await sendPlainDM(
    userId,
    `${season.emoji} *${season.name} naht — ich starte die Content-Pipeline!*

Ich generiere jetzt automatisch 10 Beiträge für die ${season.name}s-Saison deiner Telegramgruppe. Das dauert 2-3 Minuten.

Sobald fertig bekommst du hier eine DM mit:
• Übersicht aller 10 Beiträge
• Posting-Daten (variiert, nicht KI-mässig)
• Freigabe-Option

━━━━━━━━━━━━━━━━━
Lehn dich zurück, ich melde mich gleich wieder. ☕`
  );

  // Content-Pipeline starten (async, im Hintergrund)
  generateSeasonPlan(seasonKey, year, groupId, userId).catch((err) => {
    console.error("Content-Generierung fehlgeschlagen:", err);
    sendPlainDM(
      userId,
      `⚠️ Content-Generierung fehlgeschlagen: ${err instanceof Error ? err.message : "unbekannt"}\n\nBitte melde dich — ich mach's manuell.`
    );
  });
}

function seasonToKey(name: string): ContentSeason {
  if (name === "Frühling") return "fruehling";
  if (name === "Sommer") return "sommer";
  if (name === "Herbst") return "herbst";
  return "winter";
}

// ========== MONATSAKTIONEN & NEWSLETTER ==========

export function isMonthlyNewsletterReminderToday(today: Date = new Date()): boolean {
  return today.getDate() === 1;
}

export async function sendMonthlyNewsletterReminder(userId: number): Promise<void> {
  const monthName = MONTHS_DE[new Date().getMonth()];

  const msg = `📬 *Neuer Monat — ${monthName}!*

Guten Morgen Patricia! Der 1. ist da.

━━━━━━━━━━━━━━━━━
🎁 *Newsletter ${monthName}*
━━━━━━━━━━━━━━━━━
Schick mir die doTERRA-Aktionen als eine Nachricht, beginnend mit "newsletter:", z.B.:

\`newsletter: Wild Orange 15% reduziert, neue MetaPWR Promo-Pack für 199.-, LRP-Belohnung Lemon gratis ab 125 PV\`

Ich generiere dann sofort einen Entwurf mit:
• Monatsaktionen prominent platziert
• Saisonthema passend zum ${monthName}
• Deine 5-Säulen-Philosophie
• Warmer, persönlicher Ton in deinem Stil

Du kriegst einen Preview-Link — schauen, prüfen, optional anpassen.

━━━━━━━━━━━━━━━━━
📊 *Empfänger-Status*
━━━━━━━━━━━━━━━━━
AC-Liste "doTERRA Kunden": 32 aktive Kontakte

━━━━━━━━━━━━━━━━━
🌿 *Telegram-Gruppenbeitrag*
━━━━━━━━━━━━━━━━━
Falls diese Woche ein neuer Beitrag ansteht — sag mir welcher.

Ich bin ready wenn du bist! 💛`;

  await sendPlainDM(userId, msg);
}

// ========== MASTER CHECK ==========

/**
 * Prüft alle Reminder-Typen. Wird täglich einmal morgens aufgerufen.
 */
export async function checkAllReminders(userId: number): Promise<void> {
  const today = new Date();

  if (isTeamcallReminderToday(today)) {
    console.log("🎯 Teamcall-Reminder heute");
    await sendTeamcallReminder(userId);
  }

  const season = getSeasonReminderToday(today);
  if (season) {
    console.log(`${season.emoji} Saison-Reminder heute: ${season.name}`);
    await sendSeasonReminder(userId, season);
  }

  if (isMonthlyNewsletterReminderToday(today)) {
    console.log("📬 Monatsaktions/Newsletter-Reminder heute");
    await sendMonthlyNewsletterReminder(userId);
  }
}
