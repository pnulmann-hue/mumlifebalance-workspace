/**
 * Bot-Einspeisung aus Mails.
 *
 *  - feedGarten  → Notion-Wissensarchiv (Property-Schema 1:1 vom garten-telegram-bot)
 *  - feedKochbot → Rezept staget IMMER lokal nach outputs/kochbot-eingang/ (credential-frei)
 *                  und embedded zusätzlich live in den Kochbot-RAG, FALLS dessen
 *                  Supabase-Creds gesetzt sind.
 *
 * Beide Funktionen sind credential-guarded: fehlt die nötige ENV-Var, wird sauber
 * übersprungen (skipped=true, kein Throw), damit der Mail-Sweep ungestört weiterläuft.
 *
 * Nötige ENV zum Scharfschalten (optional):
 *   NOTION_TOKEN                – Garten-Einspeisung (Wissensarchiv)
 *   NOTION_WISSENSARCHIV_DS     – optionaler Override der DB-ID
 *   KOCHBOT_SUPABASE_URL        – Live-Ingest ins Rezept-RAG
 *   KOCHBOT_SUPABASE_KEY        – dito (Service-Key des Kochbot-Projekts)
 */

import { createClient } from "@supabase/supabase-js";
import OpenAI from "openai";
import * as fs from "fs";
import * as path from "path";

const NOTION_API = "https://api.notion.com/v1";
const NOTION_VERSION = "2022-06-28";
// Hardcoded-Fallback = Wissensarchiv-Data-Source aus garten-telegram-bot/config.py
const WISSENSARCHIV_DS = process.env.NOTION_WISSENSARCHIV_DS || "3497078e-8b7e-81e4-b974-e1f6a91d2064";

const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");
const KOCHBOT_INBOX = path.join(REPO_ROOT, "outputs", "kochbot-eingang");

export interface FeedInput {
  title: string;
  content: string;
  source: string; // z.B. "Gmail: Zaubertopf-Club"
  date?: Date;
}

export interface FeedResult {
  ok: boolean;
  skipped: boolean;
  detail: string;
}

function slugify(s: string): string {
  return (
    s
      .toLowerCase()
      .replace(/[äöü]/g, (m) => ({ ä: "ae", ö: "oe", ü: "ue" }[m] || m))
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || "eintrag"
  );
}

/** Notion-Wissensarchiv-Eintrag. */
async function gartenToNotion(input: FeedInput, token: string): Promise<{ ok: boolean; detail: string }> {
  try {
    const props: Record<string, unknown> = {
      Titel: { title: [{ text: { content: input.title.slice(0, 100) } }] },
      Datum: { date: { start: (input.date ?? new Date()).toISOString().slice(0, 10) } },
      Zusammenfassung: { rich_text: [{ text: { content: input.content.slice(0, 2000) } }] },
      Quelle: { select: { name: input.source.slice(0, 100) } },
    };
    const res = await fetch(`${NOTION_API}/pages`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ parent: { database_id: WISSENSARCHIV_DS }, properties: props }),
    });
    if (!res.ok) return { ok: false, detail: `Notion ${res.status}: ${(await res.text()).slice(0, 120)}` };
    return { ok: true, detail: "Notion-Wissensarchiv" };
  } catch (err) {
    return { ok: false, detail: `Notion-Fehler: ${err instanceof Error ? err.message : err}` };
  }
}

/** Garten-RAG-Embedding (figvpw-Projekt, category-Schema wie der garten-telegram-bot). */
async function gartenToRag(input: FeedInput, url: string, key: string): Promise<{ ok: boolean; detail: string }> {
  try {
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const sb = createClient(url, key);
    const content = `${input.title}\n\n${input.content}`.slice(0, 8000);
    const emb = await openai.embeddings.create({ model: "text-embedding-3-small", input: content });
    const { error } = await sb.from("documents").insert({
      content,
      embedding: emb.data[0].embedding,
      source_file: `Mail: ${input.title.slice(0, 80)}`,
      category: "garten",
    });
    if (error) return { ok: false, detail: `Garten-RAG: ${error.message}` };
    return { ok: true, detail: "Garten-RAG" };
  } catch (err) {
    return { ok: false, detail: `Garten-RAG-Fehler: ${err instanceof Error ? err.message : err}` };
  }
}

/**
 * Garten-Wissen → Notion-Wissensarchiv (+ optional Garten-RAG-Embedding).
 * Inert wenn weder NOTION_TOKEN noch GARTEN_SUPABASE_* gesetzt sind.
 */
export async function feedGarten(input: FeedInput): Promise<FeedResult> {
  const token = process.env.NOTION_TOKEN;
  const ragUrl = process.env.GARTEN_SUPABASE_URL;
  const ragKey = process.env.GARTEN_SUPABASE_KEY;

  if (!token && !(ragUrl && ragKey)) {
    return { ok: false, skipped: true, detail: "NOTION_TOKEN/GARTEN_SUPABASE_* fehlen → Garten-Einspeisung übersprungen" };
  }

  const done: string[] = [];
  let anyOk = false;
  if (token) {
    const r = await gartenToNotion(input, token);
    anyOk = anyOk || r.ok;
    done.push(r.detail);
  }
  if (ragUrl && ragKey) {
    const r = await gartenToRag(input, ragUrl, ragKey);
    anyOk = anyOk || r.ok;
    done.push(r.detail);
  }
  return { ok: anyOk, skipped: false, detail: `Garten → ${done.join(" + ")}: „${input.title.slice(0, 50)}"` };
}

/** Rezept → lokales Staging (immer) + Live-Ingest in Kochbot-RAG (falls Creds). */
export async function feedKochbot(input: FeedInput): Promise<FeedResult> {
  // 1) Immer lokal stagen — geht ohne jegliche Credentials nicht verloren.
  let stagedFile = "";
  try {
    fs.mkdirSync(KOCHBOT_INBOX, { recursive: true });
    const dateStr = (input.date ?? new Date()).toISOString().slice(0, 10);
    const file = path.join(KOCHBOT_INBOX, `${dateStr}-${slugify(input.title)}.md`);
    const md = `---\ntags: [kochen, rezept, aus-mail]\nquelle: ${input.source}\ndatum: ${dateStr}\n---\n\n# ${input.title}\n\n${input.content}\n`;
    fs.writeFileSync(file, md, "utf-8");
    stagedFile = path.basename(file);
  } catch {
    // Staging-Fehler ist nicht fatal — Live-Ingest wird trotzdem versucht.
  }

  // 2) Live in den Kochbot-RAG, falls dessen Supabase-Creds gesetzt sind.
  const url = process.env.KOCHBOT_SUPABASE_URL;
  const key = process.env.KOCHBOT_SUPABASE_KEY;
  if (!url || !key) {
    return {
      ok: Boolean(stagedFile),
      skipped: true,
      detail: stagedFile
        ? `Rezept gestaged (outputs/kochbot-eingang/${stagedFile}) — Kochbot-Supabase-Creds fehlen für Live-Ingest`
        : "Kochbot-Creds fehlen und Staging fehlgeschlagen",
    };
  }
  try {
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const sb = createClient(url, key);
    const content = `${input.title}\n\n${input.content}`.slice(0, 8000);
    const emb = await openai.embeddings.create({ model: "text-embedding-3-small", input: content });
    const { error } = await sb.from("documents").insert({
      source_file: `Mail: ${input.title.slice(0, 80)}`,
      source_folder: "rezepte",
      chunk_index: 0,
      content,
      embedding: emb.data[0].embedding,
      metadata: { origin: "mail", source: input.source },
    });
    if (error) {
      return { ok: Boolean(stagedFile), skipped: false, detail: `Kochbot-Supabase-Fehler: ${error.message} (Rezept ist gestaged)` };
    }
    return { ok: true, skipped: false, detail: `Rezept → Kochbot-RAG + Staging: „${input.title.slice(0, 60)}"` };
  } catch (err) {
    return {
      ok: Boolean(stagedFile),
      skipped: false,
      detail: `Kochbot-Live-Ingest-Fehler: ${err instanceof Error ? err.message : err} (Rezept ist gestaged)`,
    };
  }
}
