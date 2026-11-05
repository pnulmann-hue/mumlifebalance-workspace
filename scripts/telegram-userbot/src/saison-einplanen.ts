/**
 * Plant Saison-Beiträge ein: Kachel in den Storage, Zeile in scheduled_posts mit status='scheduled'.
 * Gepostet wird danach von .github/workflows/telegram-poster.yml (alle 30 Minuten).
 *
 *   npx tsx src/saison-einplanen.ts <ordner> [--trocken] [--nur 3,4] [--datum 3=2026-12-08T09:15]
 *
 * <ordner> enthält paket.json und tiles/. Wiederholbar: Bereits gepostete Beiträge bleiben unangetastet,
 * und aus dem Skript heraus wird nie etwas gelöscht. Zeiten in paket.json sind Schweizer Ortszeit.
 */
import "dotenv/config";
import fs from "fs";
import path from "path";
import { createClient } from "@supabase/supabase-js";

interface Beitrag { nr: number; titel: string; text: string; datum: string }

function zurichNachUtc(lokal: string): string {
  // Versatz für genau diesen Zeitpunkt ausrechnen (Sommer-/Winterzeit)
  const probe = new Date(lokal + ":00Z");
  const zuerich = new Date(probe.toLocaleString("en-US", { timeZone: "Europe/Zurich" }));
  const utc = new Date(probe.toLocaleString("en-US", { timeZone: "UTC" }));
  return new Date(probe.getTime() - (zuerich.getTime() - utc.getTime())).toISOString();
}

async function main() {
  const ordner = path.resolve(process.argv[2]);
  const paket = JSON.parse(fs.readFileSync(path.join(ordner, "paket.json"), "utf8"));
  const trocken = process.argv.includes("--trocken");
  const i = process.argv.indexOf("--nur");
  const nur = i > 0 ? process.argv[i + 1].split(",").map(Number) : null;
  const j = process.argv.indexOf("--datum");
  const andere: Record<number, string> = {};
  if (j > 0) for (const t of process.argv[j + 1].split(",")) { const [n, d] = t.split("="); andere[+n] = d; }

  const db = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);

  let { data: plan } = await db.from("content_plans").select("id")
    .eq("season", paket.saison).eq("year", paket.jahr).eq("telegram_chat_id", paket.chat).maybeSingle();
  if (!plan && !trocken) {
    const neu = await db.from("content_plans")
      .insert({ season: paket.saison, year: paket.jahr, status: "active", telegram_chat_id: paket.chat })
      .select("id").single();
    if (neu.error) throw neu.error;
    plan = neu.data;
  }

  for (const b of paket.beitraege as Beitrag[]) {
    if (nur && !nur.includes(b.nr)) continue;
    const wann = zurichNachUtc(andere[b.nr] || b.datum);
    const kachel = path.join(ordner, "tiles", `post-${b.nr}.png`);
    if (!fs.existsSync(kachel)) throw new Error("Kachel fehlt: " + kachel);
    // Telegram schneidet Bild-Texte bei 1024 Zeichen ab (Fehler statt Kürzung), der Poster kennt keine Teilung
    if (b.text.replace(/\*/g, "").length > 1024) throw new Error(`Beitrag ${b.nr} ist zu lang für ein Bild: ${b.text.length} Zeichen`);
    if (trocken) { console.log(b.nr, wann, b.titel, b.text.length + " Zeichen"); continue; }

    const { data: da } = await db.from("scheduled_posts").select("id,status")
      .eq("plan_id", plan!.id).eq("post_number", b.nr).maybeSingle();
    if (da?.status === "posted") { console.log(b.nr, "schon gepostet, bleibt"); continue; }

    const ablage = `${paket.saison}-${paket.jahr}/post-${b.nr}.png`;
    const hoch = await db.storage.from("telegram-content")
      .upload(ablage, fs.readFileSync(kachel), { contentType: "image/png", upsert: true });
    if (hoch.error) throw hoch.error;
    const url = db.storage.from("telegram-content").getPublicUrl(ablage).data.publicUrl;

    const zeile = {
      plan_id: plan!.id, post_number: b.nr, title: b.titel, content: b.text, canva_design_id: null,
      canva_image_url: url, telegram_chat_id: paket.chat, scheduled_for: wann, status: "scheduled",
      retry_count: 0, last_error: null,
    };
    const antwort = da
      ? await db.from("scheduled_posts").update(zeile).eq("id", da.id)
      : await db.from("scheduled_posts").insert(zeile);
    if (antwort.error) throw antwort.error;
    console.log("✅", b.nr, wann, b.titel);
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
