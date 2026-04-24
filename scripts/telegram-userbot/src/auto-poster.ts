/**
 * Auto-Poster: postet fällige Beiträge in Patricias Telegramgruppe.
 * Läuft stündlich, postet alle posts mit status='scheduled' und scheduled_for <= now().
 *
 * Posting läuft via Userbot (Patricia's Account) — so kommen Posts direkt von ihr,
 * nicht von einem Bot. Sieht organisch aus.
 */

import { TelegramClient } from "telegram";
import { createClient, SupabaseClient } from "@supabase/supabase-js";
import { sendPlainDM } from "./notify";
import { exportDesign } from "./canva";

let _supabase: SupabaseClient | null = null;
function supabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
  }
  return _supabase;
}

interface ScheduledPost {
  id: string;
  post_number: number;
  title: string | null;
  content: string;
  canva_design_id: string | null;
  canva_image_url: string | null;
  telegram_chat_id: number;
  scheduled_for: string;
  retry_count: number;
}

/**
 * Konvertiert Markdown zu Telegram-HTML:
 * **bold** → <b>bold</b>
 * *italic* → <i>italic</i>
 * HTML-Sonderzeichen werden escaped
 */
function markdownToTelegramHtml(md: string): string {
  // Erst HTML-Sonderzeichen escapen
  let out = md.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  // **bold** zuerst (sonst matcht *italic* die doppelten Sterne falsch)
  out = out.replace(/\*\*([^*\n]+)\*\*/g, "<b>$1</b>");
  // Dann *italic* (Sterne mit Inhalt zwischen, kein Stern innen)
  out = out.replace(/\*([^*\n]+)\*/g, "<i>$1</i>");
  return out;
}

/**
 * Postet einen Beitrag in die Telegramgruppe via Userbot-Session.
 * Patricia's User postet — nicht ein Bot.
 */
async function postToGroup(
  client: TelegramClient,
  post: ScheduledPost
): Promise<boolean> {
  try {
    // Falls canva_design_id gesetzt: kurz vor dem Posten exportieren
    let imageUrl = post.canva_image_url;
    if (post.canva_design_id && !imageUrl) {
      console.log(`  🎨 Exportiere Canva-Design ${post.canva_design_id}...`);
      imageUrl = await exportDesign(post.canva_design_id);
      if (!imageUrl) {
        console.error(`  ⚠️  Canva-Export fehlgeschlagen — poste nur Text`);
      }
    }

    // Entity aufloesen (sonst PEER_ID_INVALID bei selten genutzten Gruppen)
    let targetEntity;
    try {
      targetEntity = await client.getInputEntity(post.telegram_chat_id);
    } catch (entityErr) {
      console.log(`  🔍 Entity nicht im Cache, lade Dialogs...`);
      // Dialogs laden bringt alle Gruppen-Entities in den Cache
      await client.getDialogs({ limit: 200 });
      targetEntity = await client.getInputEntity(post.telegram_chat_id);
    }

    const htmlContent = markdownToTelegramHtml(post.content);

    if (imageUrl) {
      await client.sendFile(targetEntity, {
        file: imageUrl,
        caption: htmlContent,
        parseMode: "html",
      });
    } else {
      await client.sendMessage(targetEntity, {
        message: htmlContent,
        parseMode: "html",
      });
    }
    return true;
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`Post ${post.id} failed:`, msg);
    // Fehler in DB persistieren damit wir debuggen können
    await supabase()
      .from("scheduled_posts")
      .update({ last_error: msg.slice(0, 500) })
      .eq("id", post.id);
    return false;
  }
}

/**
 * Master-Funktion: Prüft und postet alle fälligen Beiträge.
 * Wird stündlich vom Userbot-Scheduler aufgerufen.
 */
export async function processPendingPosts(
  client: TelegramClient,
  userIdForNotifications: number
): Promise<void> {
  const now = new Date().toISOString();

  const { data: duePosts, error } = await supabase()
    .from("scheduled_posts")
    .select("*")
    .eq("status", "scheduled")
    .lte("scheduled_for", now)
    .order("scheduled_for", { ascending: true })
    .limit(10);

  if (error) {
    console.error("Fetch due posts error:", error);
    return;
  }

  if (!duePosts || duePosts.length === 0) {
    return;
  }

  console.log(`📤 ${duePosts.length} Posts fällig zum Senden`);

  for (const post of duePosts as ScheduledPost[]) {
    const success = await postToGroup(client, post);

    if (success) {
      await supabase()
        .from("scheduled_posts")
        .update({
          status: "posted",
          posted_at: new Date().toISOString(),
        })
        .eq("id", post.id);

      console.log(`  ✅ Post ${post.post_number} gepostet: ${post.title || ""}`);
    } else {
      // Retry-Logik: 1x nach 10 Min
      const newRetryCount = (post.retry_count || 0) + 1;

      if (newRetryCount === 1) {
        // Erster Fehler: Retry in 10 Min
        const retryAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();
        await supabase()
          .from("scheduled_posts")
          .update({
            retry_count: newRetryCount,
            scheduled_for: retryAt,
            last_error: "First attempt failed, retry in 10 min",
          })
          .eq("id", post.id);
        console.log(`  🔁 Post ${post.post_number} — Retry in 10 Min geplant`);
      } else {
        // Zweiter Fehler: Als failed markieren + DM
        await supabase()
          .from("scheduled_posts")
          .update({
            status: "failed",
            retry_count: newRetryCount,
            last_error: "Second attempt also failed",
          })
          .eq("id", post.id);

        // Plain-Text (kein Markdown) um Parse-Errors zu vermeiden
        await sendPlainDM(
          userIdForNotifications,
          `⚠️ Posting-Fehler\n\nPost ${post.post_number} konnte nicht gesendet werden (2. Versuch).\nTitel: ${String(post.title || "").slice(0, 80)}\n\nBitte manuell prüfen oder neu ansetzen.`
        );
        console.log(`  ❌ Post ${post.post_number} — 2. Fehler, DM gesendet`);
      }
    }

    // Kurze Pause zwischen Posts (um Rate Limits zu vermeiden)
    await new Promise((r) => setTimeout(r, 1500));
  }
}
