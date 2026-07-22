/**
 * Einmaliger Import: Sommer-Beiträge 2026 in die Auto-Poster-Pipeline laden.
 *
 * - Liest den Eröffnungspost (Post 0) + 16 Haupt-Beiträge aus der Markdown-Datei
 * - Reine Text-Posts (keine Canva-Designs für Sommer)
 * - Plant Posting-Zeiten (3x/Woche, Di/Do/Sa, variierende Uhrzeiten — organisch)
 * - Speichert alles als content_plan + scheduled_posts (status='pending_approval')
 * - Schickt Patricia eine DM mit der Übersicht zum Freigeben
 *
 * Analog zu import-fruehling-2026.ts, angepasst für 17 Posts inkl. Eröffnung.
 */

import "dotenv/config";
import fs from "fs";
import path from "path";
import { createClient } from "@supabase/supabase-js";
import { sendPlainDM } from "./notify";

const MARKDOWN_PATH = path.join(
  process.cwd(),
  "..",
  "..",
  "outputs",
  "telegram-posts",
  "sommer-2026",
  "sommer-2026-alle-beitraege.md"
);

// Gruppe "Gesund durchs ganze Jahr mit ätherischen Ölen"
const TELEGRAM_CHAT_ID = -4518699226;

interface ParsedPost {
  number: number; // 0 = Eröffnungspost
  title: string;
  content: string;
}

/**
 * Robustes Parsing: splittet an jeder "## "-Überschrift und behält nur
 * den Eröffnungspost + die nummerierten Beiträge. Content = alles bis zur
 * ersten Zeile die exakt "---" ist (Beitrags-Ende-Trenner).
 * Kommt mit beliebigen Emoji-Headern klar (auch ZWJ-Sequenzen wie 🧖‍♀️).
 */
function parseMarkdown(md: string): ParsedPost[] {
  const posts: ParsedPost[] = [];
  const blocks = md.split(/^## /m);

  for (const block of blocks) {
    const lines = block.split("\n");
    const header = lines[0].trim();

    let number: number | null = null;
    let title = "";

    if (/Eröffnungspost/i.test(header)) {
      number = 0;
      const dash = header.split(/\s[—-]\s/);
      title = (dash[1] || "Eröffnungspost").trim();
    } else {
      const m = header.match(/Beitrag\s+(\d+)\s*[—-]\s*(.+)$/);
      if (m) {
        number = parseInt(m[1], 10);
        title = m[2].trim();
      }
    }

    if (number === null) continue; // Meta-Sektionen (Kalender, Quellen, ...) überspringen

    const contentLines: string[] = [];
    for (let j = 1; j < lines.length; j++) {
      if (lines[j].trim() === "---") break;
      contentLines.push(lines[j]);
    }
    const content = contentLines.join("\n").trim();
    posts.push({ number, title, content });
  }

  posts.sort((a, b) => a.number - b.number);
  return posts;
}

/**
 * Berechnet Posting-Zeiten: 3 Posts pro Woche (Di/Do/Sa),
 * variierende Uhrzeiten (wirkt organisch, nicht KI-mässig).
 * Startet am nächsten Di nach heute.
 */
function calculatePostingSchedule(count: number): Date[] {
  const dates: Date[] = [];
  const now = new Date();

  const nextTue = new Date(now);
  const dayOfWeek = now.getDay(); // 0=So, 1=Mo, 2=Di, ...
  const daysUntilTue = (2 - dayOfWeek + 7) % 7 || 7;
  nextTue.setDate(now.getDate() + daysUntilTue);
  nextTue.setHours(0, 0, 0, 0);

  // Variierende Uhrzeiten (rotieren) — organisch
  const times = [
    { h: 8, m: 30 },
    { h: 14, m: 15 },
    { h: 19, m: 45 },
    { h: 9, m: 15 },
    { h: 16, m: 30 },
    { h: 11, m: 0 },
    { h: 15, m: 20 },
    { h: 20, m: 10 },
    { h: 7, m: 45 },
    { h: 17, m: 30 },
    { h: 10, m: 20 },
    { h: 13, m: 40 },
    { h: 18, m: 15 },
    { h: 9, m: 45 },
    { h: 15, m: 50 },
    { h: 8, m: 15 },
    { h: 20, m: 30 },
  ];

  const weekdayOffsets = [0, 2, 4]; // Di, Do, Sa

  let postIdx = 0;
  let weekOffset = 0;
  while (postIdx < count) {
    for (const dayOffset of weekdayOffsets) {
      if (postIdx >= count) break;
      const date = new Date(nextTue);
      date.setDate(nextTue.getDate() + weekOffset * 7 + dayOffset);
      const t = times[postIdx % times.length];
      date.setHours(t.h, t.m, 0, 0);
      dates.push(date);
      postIdx++;
    }
    weekOffset++;
  }

  return dates;
}

function formatDate(d: Date): string {
  const weekdays = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
  return `${weekdays[d.getDay()]} ${d.getDate().toString().padStart(2, "0")}.${(
    d.getMonth() + 1
  )
    .toString()
    .padStart(2, "0")}. um ${d.getHours().toString().padStart(2, "0")}:${d
    .getMinutes()
    .toString()
    .padStart(2, "0")}`;
}

async function main() {
  console.log("☀️ Sommer-Import 2026 startet...");

  if (!fs.existsSync(MARKDOWN_PATH)) {
    console.error("❌ Markdown-Datei nicht gefunden:", MARKDOWN_PATH);
    process.exit(1);
  }
  const md = fs.readFileSync(MARKDOWN_PATH, "utf-8");
  const posts = parseMarkdown(md);

  const expected = 17; // Eröffnung (0) + 16 Beiträge
  if (posts.length !== expected) {
    console.error(`❌ Erwartet ${expected} Posts, gefunden: ${posts.length}`);
    posts.forEach((p) => console.log(`  ${p.number}: ${p.title}`));
    process.exit(1);
  }
  console.log(`✅ ${posts.length} Texte geparsed (inkl. Eröffnungspost)`);

  const schedule = calculatePostingSchedule(posts.length);
  console.log("📅 Posting-Plan:");
  posts.forEach((p, i) => {
    console.log(`  ${formatDate(schedule[i])} — [${p.number}] ${p.title}`);
    console.log(`      Content-Länge: ${p.content.length} Zeichen`);
  });

  if (process.argv.includes("--dry-run")) {
    console.log("\n🧪 Dry-Run — nichts in DB geschrieben, keine DM gesendet.");
    return;
  }

  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  const { data: existingPlan } = await supabase
    .from("content_plans")
    .select("id, status")
    .eq("season", "sommer")
    .eq("year", 2026)
    .eq("telegram_chat_id", TELEGRAM_CHAT_ID)
    .maybeSingle();

  if (existingPlan) {
    console.log(`⚠️  Bestehender Plan gefunden (id=${existingPlan.id}, status=${existingPlan.status})`);
    console.log("   Lösche alte scheduled_posts + aktualisiere Plan...");
    await supabase.from("scheduled_posts").delete().eq("plan_id", existingPlan.id);
    await supabase
      .from("content_plans")
      .update({ status: "pending_approval", generation_started_at: new Date().toISOString() })
      .eq("id", existingPlan.id);
  } else {
    await supabase.from("content_plans").insert({
      season: "sommer",
      year: 2026,
      status: "pending_approval",
      telegram_chat_id: TELEGRAM_CHAT_ID,
    });
  }

  const { data: plan } = await supabase
    .from("content_plans")
    .select("id")
    .eq("season", "sommer")
    .eq("year", 2026)
    .eq("telegram_chat_id", TELEGRAM_CHAT_ID)
    .single();

  if (!plan) {
    console.error("❌ Plan konnte nicht geladen werden");
    process.exit(1);
  }

  const planId = plan.id;

  const postsToInsert = posts.map((p, i) => ({
    plan_id: planId,
    post_number: p.number,
    title: p.title,
    content: p.content,
    canva_design_id: null, // Sommer = reine Text-Posts
    telegram_chat_id: TELEGRAM_CHAT_ID,
    scheduled_for: schedule[i].toISOString(),
    status: "pending_approval",
  }));

  const { error: insertError } = await supabase
    .from("scheduled_posts")
    .insert(postsToInsert);

  if (insertError) {
    console.error("❌ Insert-Fehler:", insertError);
    process.exit(1);
  }

  console.log(`✅ ${postsToInsert.length} Posts in DB gespeichert`);

  const adminId = process.env.TELEGRAM_ADMIN_USER_ID || process.env.PATRICIA_TELEGRAM_USER_ID;
  if (!adminId) {
    console.error("❌ TELEGRAM_ADMIN_USER_ID nicht gesetzt — keine DM gesendet");
    return;
  }

  const planTable = posts
    .map((p, i) => {
      const label = p.number === 0 ? "📢 Eröffnungspost" : `${p.number}. ${p.title}`;
      return `*${formatDate(schedule[i])}*\n    ${label}`;
    })
    .join("\n");

  const dm = `☀️ *Sommer-Content bereit!*

17 Beiträge (Eröffnungspost + 16 Rezept-Posts) sind geladen und warten auf deine Freigabe.

📅 *Posting-Plan (3x/Woche Di/Do/Sa, variierende Zeiten):*

${planTable}

📍 *Gruppe:* Gesund durchs ganze Jahr mit ätherischen Ölen
📝 *Format:* reine Text-Posts (keine Bilder) — alle Rezepte aus den Enjoils-Sommerheften

━━━━━━━━━━━━━━━━━━

*Was jetzt?*

• Schreib *"OK"* → Auto-Posting startet
• Schreib *"zeig mir Post 3"* → siehst den vollen Text
• Schreib *"Übersicht"* → alle Posts nacheinander
• Schreib *"abbrechen"* → Plan wird verworfen`;

  const sent = await sendPlainDM(parseInt(adminId, 10), dm);
  if (sent) {
    console.log("✅ DM an Patricia gesendet");
  } else {
    console.error("❌ DM konnte nicht gesendet werden");
  }

  console.log("\n🎉 Import abgeschlossen. Warte auf 'OK' von Patricia.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
