#!/usr/bin/env node
// ActiveCampaign MCP Server — Vollumfang
// Kontakte (suchen/details/anlegen) · Tags (add/remove/create) · Listen (abos/erstellen)
// Custom Fields · Kampagnen (schreiben/senden/auswerten) · Automationen (zuweisen/Funnel bauen)
//
// Credentials: aus .env (AC_API_URL, AC_API_KEY) — oder aus dem MCP-Host injiziert.
// AC API V3 wird bevorzugt; V1 (legacy) nur dort, wo V3 nicht zuverlässig ist (Campaign/Message-Create).

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

// ─── .env laden (falls vorhanden) ─────────────────────────────────────────────
// Beim Standalone-Start liest der Server seine .env neben index.js.
// Beim Start durch den MCP-Host kommen die Werte via env-Injection — dann ist .env optional.
const __dirname = dirname(fileURLToPath(import.meta.url));
const envPath = join(__dirname, ".env");
if (existsSync(envPath)) {
  try {
    process.loadEnvFile(envPath);
  } catch (e) {
    console.error(`Warnung: .env konnte nicht geladen werden: ${e.message}`);
  }
}

const AC_BASE_URL = process.env.AC_API_URL?.replace(/\/$/, "");
const AC_API_KEY = process.env.AC_API_KEY;

if (!AC_BASE_URL || !AC_API_KEY) {
  console.error(
    "Fehlende Konfiguration: AC_API_URL und AC_API_KEY müssen gesetzt sein " +
      "(in 04-projects/activecampaign-mcp/.env oder via MCP-Host-env)."
  );
  process.exit(1);
}

// ─── API-Helfer ───────────────────────────────────────────────────────────────

async function ac(path, method = "GET", body = null) {
  const url = `${AC_BASE_URL}/api/3${path}`;
  const opts = {
    method,
    headers: { "Api-Token": AC_API_KEY, "Content-Type": "application/json" },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`ActiveCampaign API ${res.status}: ${err}`);
  }
  // DELETE liefert teils leeren Body
  const text = await res.text();
  return text ? JSON.parse(text) : {};
}

// AC API V1 (legacy) — braucht's nur für Campaign+Message-Create.
// V3 hat dort 405-Restriktionen, V1 funktioniert seit Jahren stabil.
// Wichtig: AC V1 erwartet PHP-Array-Notation (p[0]=2) ohne URL-Encoding der Brackets.
async function acV1(action, params) {
  const url = `${AC_BASE_URL}/admin/api.php?api_action=${action}&api_key=${AC_API_KEY}&api_output=json`;
  const parts = [];
  for (const [k, v] of Object.entries(params)) {
    if (Array.isArray(v)) {
      v.forEach((item, i) => parts.push(`${k}[${i}]=${encodeURIComponent(item)}`));
    } else if (v !== null && v !== undefined) {
      parts.push(`${k}=${encodeURIComponent(String(v))}`);
    }
  }
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: parts.join("&"),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`AC V1 ${action} HTTP ${res.status}: ${err}`);
  }
  const json = await res.json();
  if (json.result_code === 0) {
    throw new Error(`AC V1 ${action} failed: ${json.result_message || JSON.stringify(json)}`);
  }
  return json;
}

function htmlToText(html) {
  return (html || "")
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

// E-Mail → Kontakt-ID auflösen (Helfer für Tools, die mit E-Mail ODER ID arbeiten)
async function resolveContactId({ contact_id, email }) {
  if (contact_id) return contact_id;
  if (!email) throw new Error("contact_id oder email erforderlich.");
  const s = await ac(`/contacts?email=${encodeURIComponent(email)}`);
  const id = s.contacts?.[0]?.id;
  if (!id) throw new Error(`Kein Kontakt mit E-Mail: ${email}`);
  return id;
}

// ─── Tool-Definitionen ─────────────────────────────────────────────────────────

const TOOLS = [
  // ── KONTAKTE ──────────────────────────────────────────────────────────────
  {
    name: "search_contacts",
    description: "Kontakte suchen nach E-Mail, Name, Tag oder Liste. Gibt Kontaktdetails zurück.",
    inputSchema: {
      type: "object",
      properties: {
        email: { type: "string", description: "Nach E-Mail filtern" },
        search: { type: "string", description: "Suche nach Name oder E-Mail" },
        tag_id: { type: "string", description: "Nach Tag-ID filtern" },
        list_id: { type: "string", description: "Nach Listen-ID filtern" },
        limit: { type: "number", description: "Max. Ergebnisse (Standard: 20)" },
      },
    },
  },
  {
    name: "get_contact",
    description: "Vollständige Details + Aktivitätsverlauf eines Kontakts abrufen (per E-Mail oder ID).",
    inputSchema: {
      type: "object",
      properties: { email: { type: "string" }, id: { type: "string" } },
    },
  },
  {
    name: "create_contact",
    description:
      "Neuen Kontakt anlegen (oder bestehenden per E-Mail aktualisieren — Upsert via contact/sync). " +
      "Optional direkt einer Liste hinzufügen und Tags setzen.",
    inputSchema: {
      type: "object",
      required: ["email"],
      properties: {
        email: { type: "string" },
        first_name: { type: "string" },
        last_name: { type: "string" },
        phone: { type: "string" },
        list_id: { type: "string", description: "Optional: Kontakt sofort dieser Liste hinzufügen (abonniert)" },
        tag_ids: { type: "array", items: { type: "string" }, description: "Optional: Tag-IDs, die gesetzt werden" },
      },
    },
  },
  {
    name: "find_inactive_contacts",
    description:
      "Inaktive Kontakte finden, die seit X Tagen nicht aktualisiert wurden. Für Listenpflege. Pagination via offset.",
    inputSchema: {
      type: "object",
      properties: {
        days: { type: "number", description: "Inaktivitäts-Tage (Standard: 90)" },
        list_id: { type: "string", description: "Optional: auf Liste einschränken" },
        limit: { type: "number", description: "Max. pro Seite (Standard: 100)" },
        offset: { type: "number", description: "Pagination-Offset (Standard: 0)" },
      },
    },
  },
  {
    name: "find_non_openers",
    description: "Kontakte finden, die eine bestimmte Kampagne NICHT geöffnet haben.",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: { campaign_id: { type: "string" }, limit: { type: "number" } },
    },
  },
  {
    name: "delete_contacts_by_tag",
    description:
      "Alle Kontakte mit einem Tag löschen (Listenpflege). dry_run=true zählt nur. Gibt Anzahl zurück.",
    inputSchema: {
      type: "object",
      required: ["tag_id"],
      properties: {
        tag_id: { type: "string" },
        dry_run: { type: "boolean", description: "true = nur zählen, nicht löschen" },
      },
    },
  },

  // ── TAGS ──────────────────────────────────────────────────────────────────
  {
    name: "list_tags",
    description: "Alle Tags abrufen. Optional nach Name filtern.",
    inputSchema: {
      type: "object",
      properties: { search: { type: "string", description: "Tags nach Name filtern" } },
    },
  },
  {
    name: "create_tag",
    description: "Einen neuen Tag erstellen.",
    inputSchema: {
      type: "object",
      required: ["name"],
      properties: { name: { type: "string" }, description: { type: "string" } },
    },
  },
  {
    name: "tag_contact",
    description: "Einem Kontakt einen Tag HINZUFÜGEN (per contact_id oder email + tag_id).",
    inputSchema: {
      type: "object",
      required: ["tag_id"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        tag_id: { type: "string" },
      },
    },
  },
  {
    name: "untag_contact",
    description: "Einem Kontakt einen Tag ENTFERNEN (per contact_id oder email + tag_id).",
    inputSchema: {
      type: "object",
      required: ["tag_id"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        tag_id: { type: "string" },
      },
    },
  },

  // ── LISTEN ────────────────────────────────────────────────────────────────
  {
    name: "list_lists",
    description: "Alle Kontaktlisten abrufen.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "create_list",
    description:
      "Neue Kontaktliste erstellen. sender_url + sender_reminder sind in AC gesetzlich Pflicht (Impressum/Warum-bekommst-du-das); Defaults für Mum Life Balance sind hinterlegt.",
    inputSchema: {
      type: "object",
      required: ["name"],
      properties: {
        name: { type: "string" },
        sender_url: { type: "string", description: "Default: https://mumlifebalance.ch" },
        sender_reminder: {
          type: "string",
          description: "Warum bekommt der Kontakt diese Mails? Default vorhanden.",
        },
      },
    },
  },
  {
    name: "subscribe_to_list",
    description: "Kontakt einer Liste hinzufügen / abonnieren (per contact_id oder email + list_id).",
    inputSchema: {
      type: "object",
      required: ["list_id"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        list_id: { type: "string" },
      },
    },
  },
  {
    name: "unsubscribe_from_list",
    description: "Kontakt von einer Liste abmelden (Status 2, per contact_id oder email + list_id).",
    inputSchema: {
      type: "object",
      required: ["list_id"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        list_id: { type: "string" },
      },
    },
  },

  // ── CUSTOM FIELDS ─────────────────────────────────────────────────────────
  {
    name: "list_custom_fields",
    description: "Alle Custom Fields (benutzerdefinierte Kontaktfelder) mit IDs und Typen abrufen.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "set_custom_field",
    description:
      "Custom-Field-Wert für einen Kontakt setzen (per contact_id oder email). field_id über list_custom_fields ermitteln. Upsert: vorhandener Wert wird überschrieben.",
    inputSchema: {
      type: "object",
      required: ["field_id", "value"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        field_id: { type: "string" },
        value: { type: "string" },
      },
    },
  },

  // ── KAMPAGNEN / E-MAILS ───────────────────────────────────────────────────
  {
    name: "list_campaigns",
    description: "Alle Kampagnen mit Statistiken abrufen (Öffnungsrate, Klickrate etc.).",
    inputSchema: {
      type: "object",
      properties: {
        status: { type: "number", description: "0=Entwurf,1=geplant,2=sendet,4=gesendet" },
        limit: { type: "number" },
      },
    },
  },
  {
    name: "get_campaign_report",
    description: "Detaillierte Analyse einer Kampagne: Öffnungen, Klicks, Abmeldungen, Bounces, Link-Performance.",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: { campaign_id: { type: "string" } },
    },
  },
  {
    name: "analyze_campaigns",
    description: "Alle gesendeten Kampagnen vergleichen. Beste/schlechteste nach Öffnungs- und Klickrate.",
    inputSchema: {
      type: "object",
      properties: { limit: { type: "number", description: "Anzahl (Standard: 30)" } },
    },
  },
  {
    name: "create_campaign",
    description: "Eine neue E-Mail-Kampagne als Entwurf schreiben/anlegen (über V1, da V3 hier 405 liefert).",
    inputSchema: {
      type: "object",
      required: ["name", "subject", "from_name", "from_email", "list_id", "html_content"],
      properties: {
        name: { type: "string", description: "Interner Kampagnenname" },
        subject: { type: "string", description: "Betreffzeile" },
        from_name: { type: "string" },
        from_email: { type: "string" },
        list_id: { type: "string" },
        html_content: { type: "string", description: "HTML-Inhalt der E-Mail" },
        text_content: { type: "string", description: "Plaintext-Version (optional, wird sonst generiert)" },
      },
    },
  },
  {
    name: "send_campaign",
    description: "Eine Kampagne JETZT senden oder zu einem Datum planen (ISO 8601). Nur auf expliziten Befehl.",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: {
        campaign_id: { type: "string" },
        scheduled_date: { type: "string", description: "ISO 8601 — weglassen für Sofortversand" },
      },
    },
  },

  // ── AUTOMATIONEN ──────────────────────────────────────────────────────────
  {
    name: "list_automations",
    description: "Alle Automationen mit Statistiken abrufen.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "add_contact_to_automation",
    description: "Eine bestehende Automation für einen Kontakt starten (per contact_id oder email + automation_id).",
    inputSchema: {
      type: "object",
      required: ["automation_id"],
      properties: {
        contact_id: { type: "string" },
        email: { type: "string", description: "Alternativ zu contact_id" },
        automation_id: { type: "string" },
      },
    },
  },
  {
    name: "build_product_funnel",
    description:
      "Kompletten E-Mail-Funnel für ein Produkt vorbereiten: erstellt Tag + Kampagnen-Entwürfe + Automationsplan. " +
      "Hinweis: Die AC-API kann den Automation-Workflow selbst nicht erstellen — der Plan zeigt die Schritte zum Zusammenklicken.",
    inputSchema: {
      type: "object",
      required: ["product_name", "product_price", "product_description", "from_name", "from_email", "list_id"],
      properties: {
        product_name: { type: "string" },
        product_price: { type: "string", description: "z.B. CHF 777" },
        product_description: { type: "string", description: "Kurze Beschreibung (2–3 Sätze)" },
        target_audience: { type: "string", description: "Zielgruppe" },
        from_name: { type: "string" },
        from_email: { type: "string" },
        list_id: { type: "string" },
        num_emails: { type: "number", description: "Mails in Sequenz (Standard: 3, max: 5)" },
      },
    },
  },
];

// ─── Server + Handler ───────────────────────────────────────────────────────

const server = new Server(
  { name: "activecampaign-mcp", version: "2.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      // ── KONTAKTE ────────────────────────────────────────────────────────
      case "search_contacts": {
        const p = new URLSearchParams({ limit: args.limit || 20 });
        if (args.email) p.set("email", args.email);
        if (args.search) p.set("search", args.search);
        if (args.tag_id) p.set("tagid", args.tag_id);
        if (args.list_id) p.set("listid", args.list_id);
        const data = await ac(`/contacts?${p}`);
        result = (data.contacts || []).map((c) => ({
          id: c.id,
          email: c.email,
          name: `${c.firstName} ${c.lastName}`.trim(),
          phone: c.phone,
          score: c.score,
          created: c.cdate,
          updated: c.udate,
        }));
        break;
      }

      case "get_contact": {
        const id = await resolveContactId({ contact_id: args.id, email: args.email });
        const [contactRes, activityRes] = await Promise.all([
          ac(`/contacts/${id}`),
          ac(`/contacts/${id}/activities`),
        ]);
        result = {
          contact: contactRes.contact,
          recentActivity: (activityRes.activities || []).slice(0, 15),
        };
        break;
      }

      case "create_contact": {
        // contact/sync = Upsert (anlegen ODER per E-Mail aktualisieren)
        const sync = await ac("/contact/sync", "POST", {
          contact: {
            email: args.email,
            firstName: args.first_name || "",
            lastName: args.last_name || "",
            phone: args.phone || "",
          },
        });
        const contactId = sync.contact?.id;
        const extras = [];

        if (args.list_id && contactId) {
          await ac("/contactLists", "POST", {
            contactList: { list: args.list_id, contact: contactId, status: 1 },
          });
          extras.push(`Liste ${args.list_id} abonniert`);
        }
        if (Array.isArray(args.tag_ids) && contactId) {
          for (const tagId of args.tag_ids) {
            await ac("/contactTags", "POST", {
              contactTag: { contact: contactId, tag: tagId },
            }).catch(() => {});
          }
          extras.push(`${args.tag_ids.length} Tag(s) gesetzt`);
        }

        result = {
          success: true,
          id: contactId,
          email: args.email,
          name: `${args.first_name || ""} ${args.last_name || ""}`.trim(),
          extras: extras.length ? extras : undefined,
        };
        break;
      }

      case "find_inactive_contacts": {
        const days = args.days || 90;
        const cutoff = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];
        const p = new URLSearchParams({ limit: args.limit || 100, offset: args.offset || 0 });
        p.set("filters[updated_before]", cutoff);
        if (args.list_id) p.set("listid", args.list_id);
        const data = await ac(`/contacts?${p}`);
        const contacts = (data.contacts || []).map((c) => ({
          id: c.id,
          email: c.email,
          name: `${c.firstName} ${c.lastName}`.trim(),
          lastUpdated: c.udate,
        }));
        result = {
          days,
          total: data.meta?.total || 0,
          offset: args.offset || 0,
          returned: contacts.length,
          contacts,
        };
        break;
      }

      case "find_non_openers": {
        const data = await ac(`/campaigns/${args.campaign_id}/nonOpens?limit=${args.limit || 50}`);
        result = { campaignId: args.campaign_id, nonOpeners: data.nonopeners || data };
        break;
      }

      case "delete_contacts_by_tag": {
        const dryRun = args.dry_run || false;
        let offset = 0;
        const limit = 100;
        let totalDeleted = 0;
        let allContacts = [];

        while (true) {
          const p = new URLSearchParams({ limit, offset, tagid: args.tag_id });
          const data = await ac(`/contacts?${p}`);
          const contacts = data.contacts || [];
          if (contacts.length === 0) break;
          allContacts = allContacts.concat(contacts);
          if (contacts.length < limit) break;
          offset += limit;
        }

        if (dryRun) {
          result = {
            dryRun: true,
            tagId: args.tag_id,
            contactsFound: allContacts.length,
            message: `Probelauf: ${allContacts.length} Kontakte würden gelöscht.`,
            preview: allContacts.slice(0, 10).map((c) => ({
              id: c.id,
              email: c.email,
              name: `${c.firstName} ${c.lastName}`.trim(),
            })),
          };
          break;
        }

        const errors = [];
        for (let i = 0; i < allContacts.length; i += 10) {
          const batch = allContacts.slice(i, i + 10);
          await Promise.all(
            batch.map(async (c) => {
              try {
                const res = await fetch(`${AC_BASE_URL}/api/3/contacts/${c.id}`, {
                  method: "DELETE",
                  headers: { "Api-Token": AC_API_KEY },
                });
                if (res.ok || res.status === 404) totalDeleted++;
                else errors.push({ id: c.id, email: c.email, status: res.status });
              } catch (e) {
                errors.push({ id: c.id, email: c.email, error: e.message });
              }
            })
          );
        }

        result = {
          success: true,
          tagId: args.tag_id,
          totalFound: allContacts.length,
          deleted: totalDeleted,
          errors: errors.length ? errors : undefined,
          message: `✅ ${totalDeleted} von ${allContacts.length} Kontakten gelöscht.`,
        };
        break;
      }

      // ── TAGS ────────────────────────────────────────────────────────────
      case "list_tags": {
        const q = args.search ? `?search=${encodeURIComponent(args.search)}` : "?limit=100";
        const data = await ac(`/tags${q}`);
        result = (data.tags || []).map((t) => ({ id: t.id, name: t.tag, description: t.description }));
        break;
      }

      case "create_tag": {
        const data = await ac("/tags", "POST", {
          tag: { tag: args.name, tagType: "contact", description: args.description || "" },
        });
        result = { id: data.tag.id, name: data.tag.tag, created: true };
        break;
      }

      case "tag_contact": {
        const contactId = await resolveContactId(args);
        const data = await ac("/contactTags", "POST", {
          contactTag: { contact: contactId, tag: args.tag_id },
        });
        result = { success: true, contactId, tagId: args.tag_id, id: data.contactTag?.id };
        break;
      }

      case "untag_contact": {
        const contactId = await resolveContactId(args);
        // contactTag-Verknüpfung suchen, dann gezielt löschen
        const data = await ac(`/contacts/${contactId}/contactTags`);
        const link = (data.contactTags || []).find((ct) => String(ct.tag) === String(args.tag_id));
        if (!link) {
          result = { success: true, removed: false, message: "Tag war nicht gesetzt.", contactId, tagId: args.tag_id };
          break;
        }
        await ac(`/contactTags/${link.id}`, "DELETE");
        result = { success: true, removed: true, contactId, tagId: args.tag_id };
        break;
      }

      // ── LISTEN ──────────────────────────────────────────────────────────
      case "list_lists": {
        const data = await ac("/lists?limit=100");
        result = (data.lists || []).map((l) => ({
          id: l.id,
          name: l.name,
          subscribers: l.subscriber_count,
          created: l.cdate,
        }));
        break;
      }

      case "create_list": {
        const stringid = args.name
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-+|-+$/g, "")
          .slice(0, 60);
        const data = await ac("/lists", "POST", {
          list: {
            name: args.name,
            stringid,
            sender_url: args.sender_url || "https://mumlifebalance.ch",
            sender_reminder:
              args.sender_reminder ||
              "Du erhältst diese E-Mails, weil du dich bei Mum Life Balance eingetragen hast.",
          },
        });
        result = { id: data.list.id, name: data.list.name, stringid, created: true };
        break;
      }

      case "subscribe_to_list": {
        const contactId = await resolveContactId(args);
        const data = await ac("/contactLists", "POST", {
          contactList: { list: args.list_id, contact: contactId, status: 1 },
        });
        result = { success: true, contactId, listId: args.list_id, status: "subscribed", id: data.contactList?.id };
        break;
      }

      case "unsubscribe_from_list": {
        const contactId = await resolveContactId(args);
        const data = await ac("/contactLists", "POST", {
          contactList: { list: args.list_id, contact: contactId, status: 2 },
        });
        result = { success: true, contactId, listId: args.list_id, status: "unsubscribed", id: data.contactList?.id };
        break;
      }

      // ── CUSTOM FIELDS ───────────────────────────────────────────────────
      case "list_custom_fields": {
        const data = await ac("/fields?limit=100");
        result = (data.fields || []).map((f) => ({
          id: f.id,
          title: f.title,
          type: f.type,
          perstag: f.perstag,
          description: f.descript,
        }));
        break;
      }

      case "set_custom_field": {
        const contactId = await resolveContactId(args);
        const data = await ac("/fieldValues", "POST", {
          fieldValue: { contact: contactId, field: args.field_id, value: args.value },
          useDefaults: false,
        });
        result = {
          success: true,
          contactId,
          fieldId: args.field_id,
          value: args.value,
          id: data.fieldValue?.id,
        };
        break;
      }

      // ── KAMPAGNEN ───────────────────────────────────────────────────────
      case "list_campaigns": {
        const p = new URLSearchParams({ limit: args.limit || 20 });
        if (args.status !== undefined) p.set("filters[status]", args.status);
        const data = await ac(`/campaigns?${p}`);
        result = (data.campaigns || []).map((c) => ({
          id: c.id,
          name: c.name,
          subject: c.subject,
          status: c.status,
          sent: c.sends,
          opens: c.uniqueopens,
          clicks: c.linkclicks,
          unsubscribes: c.unsubscribes,
          openRate: c.sends ? `${((c.uniqueopens / c.sends) * 100).toFixed(1)}%` : "–",
          clickRate: c.sends ? `${((c.linkclicks / c.sends) * 100).toFixed(1)}%` : "–",
          sentDate: c.sdate,
        }));
        break;
      }

      case "get_campaign_report": {
        const [camp, links] = await Promise.all([
          ac(`/campaigns/${args.campaign_id}`),
          ac(`/campaigns/${args.campaign_id}/links`),
        ]);
        const c = camp.campaign;
        result = {
          id: c.id,
          name: c.name,
          subject: c.subject,
          sentDate: c.sdate,
          totalSent: c.sends,
          uniqueOpens: c.uniqueopens,
          openRate: c.sends ? `${((c.uniqueopens / c.sends) * 100).toFixed(1)}%` : "–",
          clicks: c.linkclicks,
          clickRate: c.sends ? `${((c.linkclicks / c.sends) * 100).toFixed(1)}%` : "–",
          unsubscribes: c.unsubscribes,
          hardBounces: c.hardbounces,
          softBounces: c.softbounces,
          links: (links.links || []).map((l) => ({ url: l.link, clicks: l.clicks })),
        };
        break;
      }

      case "analyze_campaigns": {
        const data = await ac(`/campaigns?limit=${args.limit || 30}&filters[status]=4`);
        const campaigns = (data.campaigns || [])
          .filter((c) => c.sends > 0)
          .map((c) => ({
            id: c.id,
            name: c.name,
            subject: c.subject,
            sent: c.sends,
            openRate: parseFloat(((c.uniqueopens / c.sends) * 100).toFixed(1)),
            clickRate: parseFloat(((c.linkclicks / c.sends) * 100).toFixed(1)),
            unsubscribes: c.unsubscribes,
            sentDate: c.sdate,
          }))
          .sort((a, b) => b.openRate - a.openRate);

        const avg = (key) =>
          campaigns.length
            ? `${(campaigns.reduce((s, c) => s + c[key], 0) / campaigns.length).toFixed(1)}%`
            : "–";

        result = {
          totalAnalyzed: campaigns.length,
          avgOpenRate: avg("openRate"),
          avgClickRate: avg("clickRate"),
          topPerformers: campaigns.slice(0, 5),
          lowPerformers: [...campaigns].sort((a, b) => a.openRate - b.openRate).slice(0, 5),
          all: campaigns,
        };
        break;
      }

      case "create_campaign": {
        // V3 liefert für message/campaign-Create 405 → V1 (legacy), seit Jahren stabil.
        const plainText = args.text_content || htmlToText(args.html_content);

        // 1) Message anlegen — V1 erwartet p[0]=list_id (NICHT list[0])
        const msgResp = await acV1("message_add", {
          format: "html",
          htmlconstructor: "external",
          textconstructor: "external",
          subject: args.subject,
          fromname: args.from_name,
          fromemail: args.from_email,
          reply2: args.from_email,
          html: args.html_content,
          text: plainText,
          "p[0]": args.list_id,
        });
        const messageId = msgResp.id;

        // 2) Campaign (Draft) anlegen + Message verknüpfen — m[messageId]=weight
        const campResp = await acV1("campaign_create", {
          type: "single",
          name: args.name,
          sdate: "",
          status: 0,
          public: 0,
          tracklinks: "all",
          subject: args.subject,
          fromname: args.from_name,
          fromemail: args.from_email,
          reply2: args.from_email,
          "p[0]": args.list_id,
          [`m[${messageId}]`]: 100,
        });

        result = {
          id: campResp.id,
          name: args.name,
          message_id: messageId,
          status: "draft",
          created: true,
        };
        break;
      }

      case "send_campaign": {
        if (args.scheduled_date) {
          const data = await ac("/campaignSchedules", "POST", {
            campaignSchedule: { campaign: args.campaign_id, sdate: args.scheduled_date, status: 1 },
          });
          result = { scheduled: true, date: args.scheduled_date, id: data.campaignSchedule?.id };
        } else {
          await ac(`/campaigns/${args.campaign_id}`, "PUT", { campaign: { status: 1 } });
          result = { sent: true, campaignId: args.campaign_id };
        }
        break;
      }

      // ── AUTOMATIONEN ────────────────────────────────────────────────────
      case "list_automations": {
        const data = await ac("/automations?limit=50");
        result = (data.automations || []).map((a) => ({
          id: a.id,
          name: a.name,
          status: a.status,
          contacts: a.contactcount,
          created: a.cdate,
        }));
        break;
      }

      case "add_contact_to_automation": {
        const contactId = await resolveContactId(args);
        const data = await ac("/contactAutomations", "POST", {
          contactAutomation: { contact: contactId, automation: args.automation_id },
        });
        result = { success: true, contactId, automationId: args.automation_id, id: data.contactAutomation?.id };
        break;
      }

      case "build_product_funnel": {
        const numEmails = Math.min(args.num_emails || 3, 5);

        const tagRes = await ac("/tags", "POST", {
          tag: {
            tag: `Funnel: ${args.product_name}`,
            tagType: "contact",
            description: `Auto-Funnel für ${args.product_name} (${args.product_price})`,
          },
        });
        const tagId = tagRes.tag.id;

        const templates = buildFunnelEmails(
          args.product_name,
          args.product_price,
          args.product_description,
          args.target_audience || "Mamas im Network Marketing",
          numEmails
        );

        const campaigns = [];
        for (const t of templates) {
          // Konsistent über V1 (gleicher Pfad wie create_campaign)
          const msgResp = await acV1("message_add", {
            format: "html",
            htmlconstructor: "external",
            textconstructor: "external",
            subject: t.subject,
            fromname: args.from_name,
            fromemail: args.from_email,
            reply2: args.from_email,
            html: t.html,
            text: t.text,
            "p[0]": args.list_id,
          });
          const campResp = await acV1("campaign_create", {
            type: "single",
            name: `[Funnel: ${args.product_name}] ${t.name}`,
            sdate: "",
            status: 0,
            public: 0,
            tracklinks: "all",
            subject: t.subject,
            fromname: args.from_name,
            fromemail: args.from_email,
            reply2: args.from_email,
            "p[0]": args.list_id,
            [`m[${msgResp.id}]`]: 100,
          });
          campaigns.push({ id: campResp.id, name: t.name, subject: t.subject });
        }

        result = {
          success: true,
          product: args.product_name,
          price: args.product_price,
          tag: { id: tagId, name: `Funnel: ${args.product_name}` },
          campaigns,
          automationPlan: buildAutomationPlan(args.product_name, campaigns, tagId),
          nextSteps: [
            `✅ Tag erstellt: "Funnel: ${args.product_name}" (ID: ${tagId})`,
            `✅ ${campaigns.length} Kampagnen-Entwürfe erstellt`,
            `⚙️ ActiveCampaign → Automationen → Neu`,
            `⚙️ Trigger: Tag "Funnel: ${args.product_name}" wird hinzugefügt`,
            `⚙️ Kampagnen mit 2-Tage-Wartezeiten als Schritte einfügen`,
          ],
        };
        break;
      }

      default:
        throw new Error(`Unbekanntes Tool: ${name}`);
    }

    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `❌ Fehler: ${err.message}` }], isError: true };
  }
});

// ─── Funnel-E-Mail-Vorlagen ────────────────────────────────────────────────

function buildFunnelEmails(name, price, description, audience, count) {
  const all = [
    {
      name: "Email 1 – Story & Problem",
      subject: `Darf ich dir kurz etwas erzählen?`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>ich möchte dir heute etwas erzählen, das ich lange mit mir getragen habe.</p>
<p>[Hier deine persönliche Geschichte einfügen — was hat dich zu diesem Angebot geführt?]</p>
<p>Genau deshalb habe ich <strong>${name}</strong> entwickelt.</p>
<p>${description}</p>
<p>Mehr dazu morgen. 💛</p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, [deine Geschichte hier]...`,
    },
    {
      name: "Email 2 – Lösung & Nutzen",
      subject: `Was ${name} für dich verändert`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>gestern habe ich dir von meiner Geschichte erzählt.</p>
<p>Heute geht es darum, was das konkret für <em>dich</em> bedeutet.</p>
<p>Mit <strong>${name}</strong> (${price}) bekommst du:</p>
<ul><li>✅ [Vorteil 1]</li><li>✅ [Vorteil 2]</li><li>✅ [Vorteil 3]</li></ul>
<p>Gemacht für ${audience} — damit es wirklich zu deinem Leben passt.</p>
<p><a href="[DEIN LINK]">Hier mehr erfahren →</a></p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, hier sind die Vorteile von ${name}...`,
    },
    {
      name: "Email 3 – Einwände & Vertrauen",
      subject: `"Ist das wirklich für mich?" — Meine ehrliche Antwort`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>ich kenne die Fragen, die du vielleicht gerade hast:</p>
<p><em>"Habe ich genug Zeit?" "Klappt das auch für mich?" "Ist der Preis gerechtfertigt?"</em></p>
<p>Lass mich ehrlich antworten: [Hier auf echte Einwände eingehen]</p>
<p><strong>${name}</strong> (${price}) ist für dich, wenn du [Beschreibung der idealen Kundin].</p>
<p><a href="[DEIN LINK]">Jetzt mehr erfahren →</a></p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, lass mich deine Fragen ehrlich beantworten...`,
    },
    {
      name: "Email 4 – Social Proof",
      subject: `Was andere Mamas sagen...`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>manchmal sagen andere es besser, als ich es könnte:</p>
<blockquote><em>"[Testimonial 1]" — Name, Ort</em></blockquote>
<blockquote><em>"[Testimonial 2]" — Name, Ort</em></blockquote>
<p>Das ist, was ich mir für dich wünsche.</p>
<p><a href="[DEIN LINK]">Ich bin dabei →</a></p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, hier sind Stimmen anderer Mamas...`,
    },
    {
      name: "Email 5 – Letzte Chance",
      subject: `Das ist meine letzte Mail dazu.`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>ich mache es kurz. Das ist meine letzte Mail zu <strong>${name}</strong> (${price}).</p>
<p>Wenn du dir denkst: <em>"Ja, das ist meins"</em> — dann ist jetzt der Moment.</p>
<p><a href="[DEIN LINK]">Ja, ich bin dabei →</a></p>
<p>Falls nicht: kein Problem. 😊</p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, letzte Chance für ${name} (${price})...`,
    },
  ];
  return all.slice(0, count);
}

function buildAutomationPlan(productName, campaigns, tagId) {
  const steps = [];
  campaigns.forEach((c, i) => {
    if (i > 0) steps.push(`⏱ Warten: 2 Tage`);
    steps.push(`📧 Kampagne senden: "${c.name}" (ID: ${c.id})`);
  });
  steps.push(`🏷 Tag entfernen: "Funnel: ${productName}" (oder in nächste Automation überführen)`);
  return {
    trigger: `Tag hinzugefügt: "Funnel: ${productName}" (ID: ${tagId})`,
    steps,
    tip: "Zwischen den E-Mails If/Else einbauen (z.B. 'Hat gekauft?' → Automation beenden)",
  };
}

// ─── Start ──────────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("ActiveCampaign MCP Server v2.0.0 läuft (stdio).");
