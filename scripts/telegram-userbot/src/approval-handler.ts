/**
 * Verarbeitet Patricias "OK" / "Post X: ..." Nachrichten zur Approval des Saison-Plans.
 */

import { createClient, SupabaseClient } from "@supabase/supabase-js";
import { sendPlainDM } from "./notify";

let _supabase: SupabaseClient | null = null;
function supabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
  }
  return _supabase;
}

/**
 * Prüft ob Patricia gerade einen pending Plan hat.
 */
async function getPendingPlan(): Promise<{ id: string; season: string; year: number } | null> {
  const { data } = await supabase()
    .from("content_plans")
    .select("id, season, year")
    .eq("status", "pending_approval")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  return data || null;
}

/**
 * Handhabt "OK" → aktiviert Posting-Plan.
 */
export async function handleApproval(userId: number): Promise<boolean> {
  const plan = await getPendingPlan();
  if (!plan) return false;

  // Aktiviere alle Posts
  await supabase()
    .from("scheduled_posts")
    .update({ status: "scheduled" })
    .eq("plan_id", plan.id)
    .eq("status", "pending_approval");

  // Plan aktivieren
  await supabase()
    .from("content_plans")
    .update({ status: "active", approved_at: new Date().toISOString() })
    .eq("id", plan.id);

  const { data: posts } = await supabase()
    .from("scheduled_posts")
    .select("post_number, title, scheduled_for")
    .eq("plan_id", plan.id)
    .order("post_number");

  const list = (posts || [])
    .map((p) => {
      const d = new Date(p.scheduled_for);
      return `${p.post_number}. ${d.toLocaleDateString("de-CH")} ${d.toLocaleTimeString("de-CH", { hour: "2-digit", minute: "2-digit" })} — ${p.title || ""}`;
    })
    .join("\n");

  await sendPlainDM(
    userId,
    `✅ *${plan.season}-Plan ${plan.year} aktiviert!*

Alle 10 Beiträge sind eingeplant und werden automatisch gepostet:

${list}

Lehn dich zurück — ich übernehme. 💪
Bei jedem Post bekommst du keine DM (damit du nicht genervt wirst). Bei Fehlern melde ich mich.`
  );

  return true;
}

/**
 * Handhabt "zeig mir Post X" → schickt den Text.
 */
export async function handleShowPost(userId: number, postNumber: number): Promise<boolean> {
  const plan = await getPendingPlan();
  if (!plan) return false;

  const { data: post } = await supabase()
    .from("scheduled_posts")
    .select("title, content, scheduled_for, post_number")
    .eq("plan_id", plan.id)
    .eq("post_number", postNumber)
    .maybeSingle();

  if (!post) {
    await sendPlainDM(userId, `❌ Post ${postNumber} nicht gefunden.`);
    return true;
  }

  const d = new Date(post.scheduled_for);
  const scheduleStr = `${d.toLocaleDateString("de-CH", { weekday: "long", day: "2-digit", month: "2-digit" })} um ${d.toLocaleTimeString("de-CH", { hour: "2-digit", minute: "2-digit" })}`;

  await sendPlainDM(
    userId,
    `📝 *Post ${post.post_number}: ${post.title || ""}*
📅 Geplant: ${scheduleStr}

━━━━━━━━━━━━━━━━━

${post.content}

━━━━━━━━━━━━━━━━━
Alles OK? Dann schreib "OK" um alle Posts zu aktivieren.
Oder: "Post ${post.post_number}: [neuer Text]" um diesen zu ersetzen.`
  );

  return true;
}

/**
 * Handhabt "Post X: [neuer Text]" → ersetzt den Text.
 */
export async function handleEditPost(
  userId: number,
  postNumber: number,
  newContent: string
): Promise<boolean> {
  const plan = await getPendingPlan();
  if (!plan) return false;

  const { error } = await supabase()
    .from("scheduled_posts")
    .update({ content: newContent })
    .eq("plan_id", plan.id)
    .eq("post_number", postNumber);

  if (error) {
    await sendPlainDM(userId, `❌ Fehler beim Ändern: ${error.message}`);
    return true;
  }

  await sendPlainDM(
    userId,
    `✅ Post ${postNumber} wurde aktualisiert.\n\nAndere Änderungen? Oder "OK" zum Aktivieren.`
  );
  return true;
}

/**
 * Zeigt Übersicht aller Posts im pending Plan.
 */
export async function handleShowAllPosts(userId: number): Promise<boolean> {
  const plan = await getPendingPlan();
  if (!plan) return false;

  const { data: posts } = await supabase()
    .from("scheduled_posts")
    .select("post_number, title, scheduled_for")
    .eq("plan_id", plan.id)
    .order("post_number");

  const list = (posts || [])
    .map((p) => {
      const d = new Date(p.scheduled_for);
      return `${p.post_number}. ${d.toLocaleDateString("de-CH", { weekday: "short", day: "2-digit", month: "2-digit" })} ${d.toLocaleTimeString("de-CH", { hour: "2-digit", minute: "2-digit" })} — ${p.title || ""}`;
    })
    .join("\n");

  await sendPlainDM(
    userId,
    `📋 *Alle Posts im Plan (${plan.season} ${plan.year})*

${list}

━━━━━━━━━━━━━━━━━
• "zeig mir Post 3" — Text ansehen
• "Post 3: [neuer Text]" — Text ersetzen
• "OK" — Alle aktivieren & posten lassen`
  );
  return true;
}

/**
 * Parst eine Nachricht und versucht Approval-Command zu erkennen.
 * Returns true wenn verarbeitet, false wenn kein Approval-Command.
 */
export async function tryHandleApprovalMessage(
  userId: number,
  text: string
): Promise<boolean> {
  const cleaned = text.trim();

  // "OK" (case-insensitive)
  if (/^(ok|okay|ok!|okay!|klar|passt|jepp|ja\s*ok)$/i.test(cleaned)) {
    return await handleApproval(userId);
  }

  // "zeig mir Post X" oder "Post X anzeigen"
  const showMatch = cleaned.match(/(?:zeig|show).+post\s+(\d+)/i);
  if (showMatch) {
    return await handleShowPost(userId, parseInt(showMatch[1]));
  }

  // "Alle Posts zeigen" / "Übersicht"
  if (/^(alle posts|\u00fcbersicht|overview|liste)$/i.test(cleaned)) {
    return await handleShowAllPosts(userId);
  }

  // "Post X: [text]" (edit)
  const editMatch = cleaned.match(/^post\s+(\d+)\s*:\s*(.+)$/is);
  if (editMatch) {
    return await handleEditPost(
      userId,
      parseInt(editMatch[1]),
      editMatch[2].trim()
    );
  }

  return false; // Kein Match
}
