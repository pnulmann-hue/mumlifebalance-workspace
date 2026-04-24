/**
 * Speichert klassifizierte Nachrichten als Embeddings in Supabase.
 * Inhalte landen in der gleichen documents-Tabelle wie der doterra-bot
 * mit category='business' und source_file='Telegram: {Gruppe}'.
 */

import { createClient, SupabaseClient } from "@supabase/supabase-js";
import OpenAI from "openai";

let _supabase: SupabaseClient | null = null;
let _openai: OpenAI | null = null;

function supabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );
  }
  return _supabase;
}

function openai(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }
  return _openai;
}

export async function saveToKnowledgeBase(params: {
  text: string;
  summary: string;
  chatTitle: string;
  senderName: string;
  messageDate: Date;
  category: string;
}): Promise<boolean> {
  try {
    // Erstelle kontextualisierten Content für besseres Retrieval
    const content = `[${params.chatTitle} — ${params.senderName}, ${params.messageDate.toISOString().slice(0, 10)}]
Kategorie: ${params.category}
Zusammenfassung: ${params.summary}

Original:
${params.text}`;

    // Embedding erzeugen
    const embedding = await openai().embeddings.create({
      model: "text-embedding-3-small",
      input: content.slice(0, 8000),
    });

    // In Supabase speichern
    const { error } = await supabase().from("documents").insert({
      content,
      embedding: embedding.data[0].embedding,
      source_file: `Telegram: ${params.chatTitle}`,
      category: "business",
    });

    if (error) {
      console.error("Supabase insert error:", error.message);
      return false;
    }

    return true;
  } catch (err) {
    console.error("Knowledge save error:", err);
    return false;
  }
}

/**
 * Trackt eine eingehende Telegram-Nachricht in der telegram_messages Tabelle
 * zur Analyse und für spätere Zusammenfassungen.
 */
export async function trackMessage(params: {
  chatId: number;
  chatTitle: string;
  messageId: number;
  senderName: string;
  text: string;
  date: Date;
  isImportant: boolean;
  category: string;
  summary: string;
  hasFiles: boolean;
}): Promise<void> {
  await supabase().from("telegram_messages").insert({
    chat_id: params.chatId,
    chat_title: params.chatTitle,
    telegram_message_id: params.messageId,
    sender_name: params.senderName,
    message_text: params.text,
    message_date: params.date.toISOString(),
    is_important: params.isImportant,
    importance_category: params.category,
    summary: params.summary,
    has_files: params.hasFiles,
    processed: false,
  });
}
