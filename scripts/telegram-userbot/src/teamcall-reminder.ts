/**
 * Teamcall-Reminder: jeden 2. Montag im Monat ist Teamcall.
 * 1 Woche vorher (also am Montag davor) schickt der Bot eine DM mit:
 * - Erinnerung an die Einladung
 * - Brainstorming-Vorschläge für Call-Thema
 *
 * Wird einmal pro Tag aufgerufen (via setInterval im Userbot oder via Cron).
 */

import Anthropic from "@anthropic-ai/sdk";
import { sendPlainDM } from "./notify";

let _anthropic: Anthropic | null = null;
function anthropic(): Anthropic {
  if (!_anthropic) {
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

/**
 * Liefert das Datum des 2. Montags im gegebenen Monat.
 */
export function secondMondayOfMonth(year: number, month: number): Date {
  // month ist 0-indexiert (Januar = 0)
  const firstDay = new Date(year, month, 1);
  const firstDayOfWeek = firstDay.getDay(); // 0 = Sonntag, 1 = Montag, ...
  let daysToFirstMonday: number;
  if (firstDayOfWeek === 0) {
    daysToFirstMonday = 1;
  } else if (firstDayOfWeek === 1) {
    daysToFirstMonday = 0;
  } else {
    daysToFirstMonday = 8 - firstDayOfWeek;
  }
  return new Date(year, month, 1 + daysToFirstMonday + 7);
}

/**
 * Liefert das Datum 1 Woche vor dem 2. Montag (also typischerweise 1. Montag).
 */
export function reminderDate(year: number, month: number): Date {
  const teamcall = secondMondayOfMonth(year, month);
  const reminder = new Date(teamcall);
  reminder.setDate(teamcall.getDate() - 7);
  return reminder;
}

/**
 * Ist heute der Reminder-Tag? (1 Woche vor dem 2. Montag)
 */
export function isReminderToday(today: Date = new Date()): boolean {
  const reminder = reminderDate(today.getFullYear(), today.getMonth());
  return (
    reminder.getFullYear() === today.getFullYear() &&
    reminder.getMonth() === today.getMonth() &&
    reminder.getDate() === today.getDate()
  );
}

/**
 * Generiert Brainstorming-Ideen für das nächste Teamcall-Thema via Claude.
 */
async function brainstormCallTopic(monthName: string): Promise<string> {
  try {
    const prompt = `Du bist der Business-Coach von Patricia, einer doTERRA-Teamleaderin bei "Mum Life Balance".

Sie hält jeden 2. Montag im Monat einen Teamcall mit ihrem doTERRA-Team (Beraterinnen und Mamas im Network Marketing).

Brainstorme 5 konkrete, inspirierende Themen für den Teamcall im ${monthName}. Berücksichtige:
- Saison und aktuelle doTERRA-Aktionen (falls relevant für den Monat)
- Patricias Philosophie: Themenbasierte Positionierung statt Produktfokus
- Mix aus Business-Strategie (Instagram, Positionierung, Teamaufbau) und Mindset/Motivation
- Konkret und umsetzbar, nicht zu allgemein

Format: 5 nummerierte Themenvorschläge, jeweils 1 Titel + 1-2 Sätze Beschreibung.
Antworte direkt auf Deutsch, warm und ermutigend.`;

    const response = await anthropic().messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 800,
      messages: [{ role: "user", content: prompt }],
    });

    const content = response.content[0];
    if (content.type === "text") return content.text;
    return "Konnte keine Ideen generieren.";
  } catch (err) {
    console.error("Brainstorm error:", err);
    return "Fehler beim Generieren der Ideen.";
  }
}

/**
 * Schickt die Reminder-DM mit Einladungs-Reminder + Brainstorming.
 */
export async function sendTeamcallReminder(userId: number): Promise<void> {
  const today = new Date();
  const teamcall = secondMondayOfMonth(today.getFullYear(), today.getMonth());

  const monthNames = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
  ];
  const monthName = monthNames[today.getMonth()];
  const callDateStr = `${teamcall.getDate()}. ${monthName}`;

  console.log(`📅 Generating teamcall reminder for ${callDateStr}...`);
  const brainstorm = await brainstormCallTopic(monthName);

  const message = `🎯 *Teamcall-Reminder*

Hey Patricia! In genau einer Woche ist wieder Teamcall — am *Montag, ${callDateStr}* 💪

━━━━━━━━━━━━━━━━━
📨 *Einladung versenden*
━━━━━━━━━━━━━━━━━
Jetzt wäre der perfekte Moment die Einladung rauszuschicken!
- WhatsApp-Gruppe an dein Team
- Kalender-Einträge
- Ggf. persönliche DMs an inaktive Beraterinnen

━━━━━━━━━━━━━━━━━
💡 *Ideen für das Thema*
━━━━━━━━━━━━━━━━━
${brainstorm}

━━━━━━━━━━━━━━━━━
Sag mir welches Thema dich anspricht — dann helfe ich dir beim Ausarbeiten! ✨`;

  await sendPlainDM(userId, message);
  console.log(`✅ Teamcall reminder sent to ${userId}`);
}

/**
 * Täglicher Check ob heute der Reminder-Tag ist.
 * Wird vom Userbot-Scheduler aufgerufen.
 */
export async function checkAndSendReminder(userId: number): Promise<void> {
  if (isReminderToday()) {
    await sendTeamcallReminder(userId);
  }
}
