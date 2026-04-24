/**
 * Generiert einen kompletten Saison-Content-Plan automatisch.
 * Triggered vom Reminder-System 7 Tage vor Saisonstart.
 *
 * Erzeugt:
 * - 10 Beitrags-Texte (Claude, basierend auf Enjoils-Hefte aus Wissensbasis)
 * - Variierte Posting-Zeiten (Mo-So, 07:00-20:00, verschiedene Minuten — nicht KI-mässig)
 * - content_plans + scheduled_posts Einträge (status=pending_approval)
 *
 * Sendet dann DM mit Übersicht an Patricia.
 */

import Anthropic from "@anthropic-ai/sdk";
import { createClient, SupabaseClient } from "@supabase/supabase-js";
import { sendPlainDM } from "./notify";

let _anthropic: Anthropic | null = null;
function anthropic(): Anthropic {
  if (!_anthropic) {
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

let _supabase: SupabaseClient | null = null;
function supabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
  }
  return _supabase;
}

export type Season = "fruehling" | "sommer" | "herbst" | "winter";

const SEASON_META: Record<Season, { name: string; months: [number, number, number]; emoji: string; themes: string[] }> = {
  fruehling: {
    name: "Frühling",
    months: [2, 3, 4], // März, April, Mai
    emoji: "🌱",
    themes: ["Frühjahrsmüdigkeit", "Pollenflug", "Detox", "Stoffwechsel", "Ölziehen", "Mama-Energie", "Hormone", "Haut", "Wild Orange", "5 Säulen"],
  },
  sommer: {
    name: "Sommer",
    months: [5, 6, 7], // Juni, Juli, August
    emoji: "☀️",
    themes: ["Sonnenschutz", "Kühlen bei Hitze", "Insektenschutz", "Reiseapotheke", "Verdauung", "Energie ohne Hitze", "Haut im Sommer", "Zitrusöle", "Kinder & Sommer", "Erfrischung"],
  },
  herbst: {
    name: "Herbst",
    months: [8, 9, 10], // September, Oktober, November
    emoji: "🍂",
    themes: ["Immunsystem stärken", "Erkältungs-Prävention", "Raumluftreinigung", "Kinder in der Kita", "Atemwege", "Schlaf wird wichtig", "Wärmende Öle", "Emotionale Balance", "Ingwer & Zimt", "Rauhnächte-Vorbereitung"],
  },
  winter: {
    name: "Winter",
    months: [11, 0, 1], // Dezember, Januar, Februar
    emoji: "❄️",
    themes: ["Lichtmangel & Stimmung", "Erkältung akut", "Rauhnächte", "Festliche Diffuser", "Stress im Advent", "Haut im Winter", "Neujahr-Vorsätze & Öle", "Immunsystem", "Inneres Feuer", "Neustart"],
  },
};

/**
 * Generiert variierte Posting-Zeiten — sieht nicht nach Bot aus.
 * Mix aus Wochentagen, versetzte Minuten.
 */
export function generateVariedSchedule(
  startDate: Date,
  numPosts: number
): Date[] {
  const schedule: Date[] = [];
  const times = [
    { day: 1, hour: 9, min: 30 }, // Mo 09:30
    { day: 3, hour: 14, min: 15 }, // Mi 14:15
    { day: 4, hour: 8, min: 0 }, // Do 08:00
    { day: 2, hour: 19, min: 0 }, // Di 19:00
    { day: 6, hour: 10, min: 30 }, // Sa 10:30
    { day: 1, hour: 7, min: 15 }, // Mo 07:15
    { day: 5, hour: 17, min: 45 }, // Fr 17:45
    { day: 3, hour: 12, min: 30 }, // Mi 12:30
    { day: 0, hour: 19, min: 0 }, // So 19:00
    { day: 4, hour: 9, min: 15 }, // Do 09:15
  ];

  let currentWeek = new Date(startDate);
  // Auf nächsten Montag stellen
  const dow = currentWeek.getDay();
  const daysUntilMon = (1 - dow + 7) % 7;
  currentWeek.setDate(currentWeek.getDate() + daysUntilMon);
  currentWeek.setHours(0, 0, 0, 0);

  for (let i = 0; i < numPosts; i++) {
    const slot = times[i % times.length];
    const postDate = new Date(currentWeek);
    // slot.day: 0=Sonntag, 1=Montag, ...
    const adjustedDay = slot.day === 0 ? 7 : slot.day; // Sonntag ans Wochenende
    postDate.setDate(currentWeek.getDate() + (adjustedDay - 1));
    postDate.setHours(slot.hour, slot.min, 0, 0);
    schedule.push(postDate);
    currentWeek.setDate(currentWeek.getDate() + 7); // nächste Woche
  }

  return schedule;
}

/**
 * Holt relevante Enjoils-Inhalte zur Saison aus der Wissensbasis.
 */
async function getSeasonKnowledge(season: Season): Promise<string> {
  const seasonName = SEASON_META[season].name;
  const { data } = await supabase()
    .from("documents")
    .select("content, source_file")
    .eq("category", "product")
    .ilike("source_file", `%${seasonName}%`)
    .limit(30);

  if (!data || data.length === 0) return "";

  return data
    .slice(0, 15)
    .map((d) => `Quelle: ${d.source_file}\n${d.content.slice(0, 600)}`)
    .join("\n\n---\n\n");
}

/**
 * Generiert einen einzelnen Post via Claude.
 */
async function generatePost(
  season: Season,
  topic: string,
  postNumber: number,
  enjoilsContext: string
): Promise<{ title: string; content: string }> {
  const prompt = `Du bist Patricia, vierfache Mama und doTERRA-Beraterin mit der Marke "Mum Life Balance". Deine Positionierung: Du hilfst erschöpften Mamas sich mit Ölen körperlich und emotional zu erholen (5 Säulen: Schlaf, Ernährung, Stressmanagement, NEM, Bewegung).

Schreibe EINEN Telegram-Beitrag für deine Kundengruppe "Gesund durchs ganze Jahr mit ätherischen Ölen" — ${SEASON_META[season].emoji} ${SEASON_META[season].name}, Beitrag ${postNumber}/10.

**Thema diesmal:** ${topic}

**Inhaltliche Grundlage** (aus Enjoils-Heften und dem Produktwissen):
${enjoilsContext.slice(0, 4000)}

**Dein Ton:**
- Warm, direkt, persönlich — wie eine Freundin schreibt
- Schweizer Hochdeutsch (immer "ss" statt "ß")
- Du duzt
- Hook am Anfang, konkreter Tipp/Rezept in der Mitte, Frage zur Interaktion am Ende
- Emojis sparsam & passend
- Compliance: KEINE Heilversprechen — "kann unterstützen", "trägt bei zu", nie "heilt"
- Doterra-Ölnamen korrekt (Air statt Breathe, Deep Blue, On Guard, MetaPWR Öl statt Slim & Sassy, etc.)
- Lang: ~6-12 Sätze, Telegram/WhatsApp-tauglich

**Format als reines JSON (kein Markdown drumherum):**
{
  "title": "kurzer Beitragstitel (max 50 Zeichen)",
  "content": "der komplette Beitragstext mit Emojis, Zeilenumbrüchen und Markdown (Telegram-Style)"
}`;

  const res = await anthropic().messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1500,
    messages: [{ role: "user", content: prompt }],
  });

  const c = res.content[0];
  if (c.type !== "text") throw new Error("Unexpected response type");

  // Strip markdown fences if present
  const jsonText = c.text
    .replace(/^```json\s*/i, "")
    .replace(/^```\s*/, "")
    .replace(/\s*```$/, "")
    .trim();

  const parsed = JSON.parse(jsonText);
  return {
    title: parsed.title || `${SEASON_META[season].name} ${postNumber}`,
    content: parsed.content || "",
  };
}

/**
 * Master-Funktion: Generiert kompletten Saison-Plan.
 */
export async function generateSeasonPlan(
  season: Season,
  year: number,
  telegramChatId: number,
  userId: number
): Promise<void> {
  console.log(`🎨 Generiere ${season}-Plan ${year}...`);

  // 1. Check: Existiert schon ein Plan?
  const { data: existing } = await supabase()
    .from("content_plans")
    .select("id, status")
    .eq("season", season)
    .eq("year", year)
    .eq("telegram_chat_id", telegramChatId)
    .maybeSingle();

  if (existing && existing.status !== "completed") {
    console.log(`Plan existiert bereits: ${existing.id} (${existing.status})`);
    return;
  }

  // 2. Neuer Plan
  const { data: plan, error: planError } = await supabase()
    .from("content_plans")
    .insert({
      season,
      year,
      telegram_chat_id: telegramChatId,
      status: "generating",
    })
    .select("id")
    .single();

  if (planError || !plan) {
    console.error("Plan create error:", planError);
    return;
  }

  // 3. Wissen holen
  const enjoilsContext = await getSeasonKnowledge(season);

  // 4. Posting-Zeiten (Saisonstart bestimmen)
  const startMonth = SEASON_META[season].months[0];
  const seasonStart = new Date(year, startMonth, 1);
  const schedule = generateVariedSchedule(seasonStart, 10);

  // 5. Für jedes Thema einen Post generieren
  const themes = SEASON_META[season].themes;
  for (let i = 0; i < 10; i++) {
    try {
      const topic = themes[i] || `Beitrag ${i + 1}`;
      console.log(`  Generiere Post ${i + 1}/10: ${topic}`);
      const post = await generatePost(season, topic, i + 1, enjoilsContext);

      await supabase().from("scheduled_posts").insert({
        plan_id: plan.id,
        post_number: i + 1,
        title: post.title,
        content: post.content,
        telegram_chat_id: telegramChatId,
        scheduled_for: schedule[i].toISOString(),
        status: "pending_approval",
      });
    } catch (err) {
      console.error(`Post ${i + 1} failed:`, err);
    }
  }

  // 6. Status auf "pending_approval"
  await supabase()
    .from("content_plans")
    .update({ status: "pending_approval" })
    .eq("id", plan.id);

  // 7. DM an Patricia
  await sendApprovalDM(userId, plan.id, season, schedule);
  console.log(`✅ ${season}-Plan fertig, wartet auf Approval`);
}

async function sendApprovalDM(
  userId: number,
  planId: string,
  season: Season,
  schedule: Date[]
): Promise<void> {
  const meta = SEASON_META[season];
  const scheduleText = schedule
    .map(
      (d, i) =>
        `${i + 1}. ${d.toLocaleDateString("de-CH", { weekday: "short", day: "2-digit", month: "2-digit" })} um ${d.toLocaleTimeString("de-CH", { hour: "2-digit", minute: "2-digit" })}`
    )
    .join("\n");

  const msg = `${meta.emoji} *${meta.name}s-Content bereit!*

10 Beiträge für "Gesund durchs ganze Jahr" sind generiert und warten auf deine Freigabe.

━━━━━━━━━━━━━━━━━
📅 *Posting-Plan*
━━━━━━━━━━━━━━━━━
${scheduleText}

━━━━━━━━━━━━━━━━━
📋 *Nächste Schritte*
━━━━━━━━━━━━━━━━━
1. Schau dir die Beiträge an (ich schicke sie dir gleich einzeln oder du sagst "zeig mir Post X")
2. Canva-Designs kommen separat (nach OAuth-Setup)
3. Schreib *"OK"* zum Freigeben — dann posten sie automatisch gemäss Plan
4. Oder schreib *"Post X: [neuer Text]"* um einen einzelnen Beitrag zu ändern

Plan-ID: \`${planId.slice(0, 8)}\``;

  await sendPlainDM(userId, msg);
}
