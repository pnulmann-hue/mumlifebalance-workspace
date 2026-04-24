/**
 * Canva Connect API Integration.
 * Holt gespeicherte Tokens aus Supabase, refreshed bei Bedarf, generiert Designs.
 */

import { createClient, SupabaseClient } from "@supabase/supabase-js";

const CANVA_API = "https://api.canva.com/rest/v1";
const TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token";

let _supabase: SupabaseClient | null = null;
function supabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
  }
  return _supabase;
}

interface TokenRow {
  access_token: string;
  refresh_token: string;
  expires_at: string;
  scope: string | null;
}

/**
 * Holt aktuellen Access Token. Wenn abgelaufen → refresh automatisch.
 */
export async function getAccessToken(): Promise<string | null> {
  const { data, error } = await supabase()
    .from("canva_tokens")
    .select("access_token, refresh_token, expires_at, scope")
    .eq("id", "default")
    .maybeSingle();

  if (error || !data) {
    console.error("Canva tokens nicht in DB gefunden:", error?.message);
    return null;
  }

  const row = data as TokenRow;
  const expiresAt = new Date(row.expires_at);
  const now = new Date();

  // Wenn in weniger als 5 Min abläuft → refreshen
  if (expiresAt.getTime() - now.getTime() > 5 * 60 * 1000) {
    return row.access_token;
  }

  // Refreshen
  return await refreshAccessToken(row.refresh_token);
}

async function refreshAccessToken(refreshToken: string): Promise<string | null> {
  const clientId = process.env.CANVA_CLIENT_ID;
  const clientSecret = process.env.CANVA_CLIENT_SECRET;
  if (!clientId || !clientSecret) return null;

  const basic = Buffer.from(`${clientId}:${clientSecret}`).toString("base64");
  const body = new URLSearchParams({
    grant_type: "refresh_token",
    refresh_token: refreshToken,
  });

  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: {
      Authorization: `Basic ${basic}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });

  if (!res.ok) {
    console.error("Token refresh failed:", res.status, await res.text());
    return null;
  }

  const tokens = (await res.json()) as {
    access_token: string;
    refresh_token: string;
    expires_in: number;
    scope: string;
  };
  const expiresAt = new Date(Date.now() + tokens.expires_in * 1000).toISOString();

  await supabase()
    .from("canva_tokens")
    .update({
      access_token: tokens.access_token,
      refresh_token: tokens.refresh_token,
      expires_at: expiresAt,
      scope: tokens.scope,
      updated_at: new Date().toISOString(),
    })
    .eq("id", "default");

  return tokens.access_token;
}

// ========== Design Generation ==========

export interface GenerateDesignResult {
  designId: string | null;
  imageUrl: string | null;
  editUrl: string | null;
  error?: string;
}

/**
 * Erstellt ein neues Design via Canva Connect API mit Magic Design / generate-design endpoint.
 * Hinweis: Canva Connect API hat `POST /v1/designs` für neue leere Designs.
 * Für AI-Generierung nutzen wir das URL-Import oder einen anderen Workflow.
 *
 * Hier: Wir erstellen ein leeres Design im passenden Format und lassen Patricia
 * es selbst ausfüllen, ODER wir nutzen Brand Templates + Autofill wenn eins da ist.
 */
export async function createDesign(params: {
  title: string;
  designType?: string; // z.B. "InstagramPost"
}): Promise<GenerateDesignResult> {
  const token = await getAccessToken();
  if (!token) return { designId: null, imageUrl: null, editUrl: null, error: "no token" };

  try {
    const res = await fetch(`${CANVA_API}/designs`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        design_type: {
          type: "preset",
          name: params.designType || "InstagramPost",
        },
        title: params.title,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Canva createDesign failed:", res.status, err);
      return { designId: null, imageUrl: null, editUrl: null, error: err };
    }

    const data = (await res.json()) as {
      design?: { id?: string; thumbnail?: { url?: string }; urls?: { edit_url?: string } };
    };
    return {
      designId: data.design?.id || null,
      imageUrl: data.design?.thumbnail?.url || null,
      editUrl: data.design?.urls?.edit_url || null,
    };
  } catch (err) {
    return {
      designId: null,
      imageUrl: null,
      editUrl: null,
      error: err instanceof Error ? err.message : String(err),
    };
  }
}

/**
 * Startet einen Export des Designs als PNG und wartet bis fertig.
 */
export async function exportDesign(designId: string): Promise<string | null> {
  const token = await getAccessToken();
  if (!token) return null;

  try {
    // Job starten
    const startRes = await fetch(`${CANVA_API}/exports`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        design_id: designId,
        format: { type: "png" },
      }),
    });

    if (!startRes.ok) {
      console.error("Canva export start failed:", await startRes.text());
      return null;
    }

    type ExportJob = {
      job?: { id?: string; status?: string; urls?: string[]; error?: unknown };
    };
    const startData = (await startRes.json()) as ExportJob;
    const jobId = startData.job?.id;
    if (!jobId) return null;

    // Poll bis fertig (max 60s, Canva kann bei grossen Designs l\u00e4nger brauchen)
    for (let i = 0; i < 30; i++) {
      await new Promise((r) => setTimeout(r, 2000));

      const statusRes = await fetch(`${CANVA_API}/exports/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!statusRes.ok) continue;

      const status = (await statusRes.json()) as ExportJob;
      if (status.job?.status === "success") {
        return status.job.urls?.[0] || null;
      }
      if (status.job?.status === "failed") {
        console.error("Export failed:", status.job.error);
        return null;
      }
    }

    console.error("Export timed out after 30s");
    return null;
  } catch (err) {
    console.error("Export error:", err);
    return null;
  }
}

/**
 * Helper: Ist Canva verbunden?
 */
export async function isCanvaConnected(): Promise<boolean> {
  const token = await getAccessToken();
  return token !== null;
}
