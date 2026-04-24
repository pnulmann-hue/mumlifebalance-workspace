/**
 * Einmaliger Import: Frühlings-Beiträge 2026 in die Auto-Poster-Pipeline laden.
 *
 * - Liest 10 Haupt-Texte aus der Markdown-Datei
 * - Ordnet jedem Text ein Canva-Design zu (Variante 1)
 * - Plant Posting-Zeiten mit Aufhol-Strategie (3x/Woche, Di/Do/Sa)
 * - Speichert alles als content_plan + scheduled_posts (status='pending_approval')
 * - Schickt Patricia eine DM mit der Übersicht zum Freigeben
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
  "fruehling-2026",
  "fruehling-2026-alle-beitraege.md"
);

// Gruppe "Gesund durchs ganze Jahr mit ätherischen Ölen"
const TELEGRAM_CHAT_ID = -4518699226;

// Canva Design IDs (Variante 1 pro Beitrag) aus canva-designs-uebersicht.md
const CANVA_DESIGN_IDS: Record<number, string> = {
  1: "iAATr3CER6Gx3ZF",
  2: "9oZuuW-hF0ziEwG",
  3: "Dm1fuMar2mR3oKr",
  4: "n4yfzvIYxNVdD9Q",
  5: "-OAMVJL1ILTdnco",
  6: "B7z_deEGVT5RzE9",
  7: "XAIh7DUe3PmBwP7",
  8: "F_UkC3vZWtptZ6V",
  9: "rzSBz08rz9UkMs1",
  10: "kuWT89j4WNp_H0n",
};

interface ParsedPost {
  number: number;
  title: string;
  content: string;
}

/**
 * Parsed die Markdown-Datei in 10 einzelne Posts.
 */
function parseMarkdown(md: string): ParsedPost[] {
  const posts: ParsedPost[] = [];
  // Splitte an "## 🌱 Beitrag X — Titel" oder ähnlichem Emoji
  const sections = md.split(/^## .{1,3}\s*Beitrag\s+(\d+)\s*—\s*/m);

  // sections[0] ist Header, dann alternierend [number, content, number, content, ...]
  for (let i = 1; i < sections.length; i += 2) {
    const num = parseInt(sections[i], 10);
    const rest = sections[i + 1] || "";
    const lines = rest.split("\n");
    const title = lines[0].trim();
    // Inhalt = alles bis zum nächsten "---" auf eigener Zeile
    const contentLines: string[] = [];
    for (let j = 1; j < lines.length; j++) {
      if (lines[j].trim() === "---") break;
      contentLines.push(lines[j]);
    }
    const content = contentLines.join("\n").trim();
    posts.push({ number: num, title, content });
  }

  return posts;
}

/**
 * Berechnet 10 Posting-Zeiten mit Aufhol-Strategie:
 * 3 Posts pro Woche (Di/Do/Sa), variierende Uhrzeiten (nicht KI-mässig).
 * Startet am nächsten Di nach heute.
 */
function calculatePostingSchedule(): Date[] {
  const dates: Date[] = [];
  const now = new Date();

  // Nächster Dienstag finden
  const nextTue = new Date(now);
  const dayOfWeek = now.getDay(); // 0=So, 1=Mo, 2=Di, ...
  const daysUntilTue = (2 - dayOfWeek + 7) % 7 || 7; // wenn heute Di, nimm nächsten Di
  nextTue.setDate(now.getDate() + daysUntilTue);
  nextTue.setHours(0, 0, 0, 0);

  // Variierende Uhrzeiten — wirkt organisch, nicht KI-mässig
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
  ];

  // Wochenmuster: Di (offset 0), Do (offset 2), Sa (offset 4)
  const weekdayOffsets = [0, 2, 4]; // Di, Do, Sa

  let postIdx = 0;
  let weekOffset = 0;
  while (postIdx < 10) {
    for (const dayOffset of weekdayOffsets) {
      if (postIdx >= 10) break;
      const date = new Date(nextTue);
      date.setDate(nextTue.getDate() + weekOffset * 7 + dayOffset);
      const t = times[postIdx];
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
  console.log("🌱 Frühlings-Import 2026 startet...");

  // 1. Markdown einlesen
  if (!fs.existsSync(MARKDOWN_PATH)) {
    console.error("❌ Markdown-Datei nicht gefunden:", MARKDOWN_PATH);
    process.exit(1);
  }
  const md = fs.readFileSync(MARKDOWN_PATH, "utf-8");
  const posts = parseMarkdown(md);

  if (posts.length !== 10) {
    console.error(`❌ Erwartet 10 Posts, gefunden: ${posts.length}`);
    posts.forEach((p) => console.log(`  ${p.number}: ${p.title}`));
    process.exit(1);
  }
  console.log(`✅ ${posts.length} Texte geparsed`);

  // 2. Posting-Plan berechnen
  const schedule = calculatePostingSchedule();
  console.log("📅 Posting-Plan:");
  posts.forEach((p, i) => {
    console.log(`  ${i + 1}. ${formatDate(schedule[i])} — ${p.title}`);
  });

  // 3. Supabase Verbindung
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  // 4. content_plan anlegen (oder existierenden aktualisieren)
  const { data: existingPlan } = await supabase
    .from("content_plans")
    .select("id, status")
    .eq("season", "fruehling")
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
      season: "fruehling",
      year: 2026,
      status: "pending_approval",
      telegram_chat_id: TELEGRAM_CHAT_ID,
    });
  }

  // Plan-ID holen
  const { data: plan } = await supabase
    .from("content_plans")
    .select("id")
    .eq("season", "fruehling")
    .eq("year", 2026)
    .eq("telegram_chat_id", TELEGRAM_CHAT_ID)
    .single();

  if (!plan) {
    console.error("❌ Plan konnte nicht geladen werden");
    process.exit(1);
  }

  const planId = plan.id;

  // 5. scheduled_posts einfügen
  const postsToInsert = posts.map((p, i) => ({
    plan_id: planId,
    post_number: p.number,
    title: p.title,
    content: p.content,
    canva_design_id: CANVA_DESIGN_IDS[p.number] || null,
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

  console.log("✅ 10 Posts in DB gespeichert");

  // 6. DM an Patricia
  const adminId = process.env.TELEGRAM_ADMIN_USER_ID || process.env.PATRICIA_TELEGRAM_USER_ID;
  if (!adminId) {
    console.error("❌ TELEGRAM_ADMIN_USER_ID nicht gesetzt — keine DM gesendet");
    return;
  }

  const planTable = posts
    .map((p, i) => `${i + 1}. *${formatDate(schedule[i])}*\n    ${p.title}`)
    .join("\n");

  const dm = `🌱 *Frühlings-Content bereit!*

10 Beiträge sind generiert und warten auf deine Freigabe.

📅 *Posting-Plan (Aufhol-Modus: 3x/Woche Di/Do/Sa):*

${planTable}

📍 *Gruppe:* Gesund durchs ganze Jahr mit ätherischen Ölen
🎨 *Canva-Designs:* Variante 1 pro Post (aus Frühling 2026-Ordner)

━━━━━━━━━━━━━━━━━━

*Was jetzt?*

• Schreib *"OK"* → Auto-Posting startet
• Schreib *"zeig mir Post 3"* → siehst den vollen Text
• Schreib *"Übersicht"* → alle 10 Posts nacheinander
• Schreib *"abbrechen"* → Plan wird verworfen

💡 Die Canva-Bilder werden automatisch exportiert und mit dem Text gepostet.

🖼️ *Alle Posts mit Bildern & Texten in der Übersicht:*
https://bot.mumlifebalance.ch/content`;

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
