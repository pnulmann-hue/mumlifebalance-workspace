/**
 * Zeigt den Stand der Saison-Beiträge in scheduled_posts, nur lesend.
 *   npx tsx src/saison-stand.ts
 */
import "dotenv/config";
import { createClient } from "@supabase/supabase-js";

async function main() {
  const db = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
  const { data, error } = await db
    .from("scheduled_posts")
    .select("post_number,title,status,scheduled_for,posted_at,telegram_chat_id,canva_image_url,last_error")
    .order("scheduled_for", { ascending: false })
    .limit(30);
  if (error) throw error;
  for (const p of data || []) {
    console.log(
      [p.scheduled_for?.slice(0, 16), p.status, p.telegram_chat_id, p.post_number, (p.title || "").slice(0, 40),
       p.canva_image_url ? "Bild" : "-", p.posted_at?.slice(0, 10) || "", p.last_error || ""].join(" | ")
    );
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
