#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const AC_BASE_URL = process.env.AC_API_URL?.replace(/\/$/, "");
const AC_API_KEY = process.env.AC_API_KEY;

if (!AC_BASE_URL || !AC_API_KEY) {
  console.error("Missing AC_API_URL or AC_API_KEY environment variables.");
  process.exit(1);
}

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
  return res.json();
}

// ─── Tool Definitions ─────────────────────────────────────────────────────────

const TOOLS = [
  // CONTACTS
  {
    name: "search_contacts",
    description:
      "Kontakte suchen nach E-Mail, Name, Tag oder Liste. Gibt Kontaktdetails zurück.",
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
    description:
      "Vollständige Details und Aktivitätsverlauf eines Kontakts abrufen (per E-Mail oder ID).",
    inputSchema: {
      type: "object",
      properties: {
        email: { type: "string" },
        id: { type: "string" },
      },
    },
  },
  {
    name: "find_inactive_contacts",
    description:
      "Inaktive Kontakte finden, die seit X Tagen nicht reagiert haben. Für Listenpflege und Bereinigung. Unterstützt Pagination via offset.",
    inputSchema: {
      type: "object",
      properties: {
        days: { type: "number", description: "Inaktivitäts-Tage (Standard: 90)" },
        list_id: { type: "string", description: "Optional: auf Liste einschränken" },
        limit: { type: "number", description: "Max. Ergebnisse pro Seite (Standard: 100)" },
        offset: { type: "number", description: "Ergebnisse überspringen für Pagination (Standard: 0)" },
      },
    },
  },
  {
    name: "find_non_openers",
    description:
      "Kontakte finden, die eine bestimmte Kampagne NICHT geöffnet haben.",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: {
        campaign_id: { type: "string" },
        limit: { type: "number" },
      },
    },
  },

  // LISTS
  {
    name: "list_lists",
    description: "Alle Kontaktlisten in ActiveCampaign abrufen.",
    inputSchema: { type: "object", properties: {} },
  },

  // TAGS
  {
    name: "list_tags",
    description: "Alle Tags abrufen. Optional nach Name filtern.",
    inputSchema: {
      type: "object",
      properties: {
        search: { type: "string", description: "Tags nach Name filtern" },
      },
    },
  },
  {
    name: "create_tag",
    description: "Einen neuen Tag in ActiveCampaign erstellen.",
    inputSchema: {
      type: "object",
      required: ["name"],
      properties: {
        name: { type: "string" },
        description: { type: "string" },
      },
    },
  },
  {
    name: "tag_contact",
    description: "Einem Kontakt einen Tag hinzufügen.",
    inputSchema: {
      type: "object",
      required: ["contact_id", "tag_id"],
      properties: {
        contact_id: { type: "string" },
        tag_id: { type: "string" },
      },
    },
  },

  // CAMPAIGNS
  {
    name: "list_campaigns",
    description:
      "Alle Kampagnen mit Statistiken abrufen (Öffnungsrate, Klickrate etc.).",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "number",
          description: "0=Entwurf, 1=geplant, 2=sendet, 4=gesendet",
        },
        limit: { type: "number" },
      },
    },
  },
  {
    name: "get_campaign_report",
    description:
      "Detaillierte Analyse einer Kampagne: Öffnungen, Klicks, Abmeldungen, Bounces, Link-Performance.",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: {
        campaign_id: { type: "string" },
      },
    },
  },
  {
    name: "analyze_campaigns",
    description:
      "Alle gesendeten Kampagnen vergleichen. Zeigt beste und schlechteste nach Öffnungs- und Klickrate.",
    inputSchema: {
      type: "object",
      properties: {
        limit: { type: "number", description: "Anzahl Kampagnen (Standard: 30)" },
      },
    },
  },
  {
    name: "create_campaign",
    description: "Eine neue E-Mail-Kampagne als Entwurf erstellen.",
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
        text_content: { type: "string", description: "Plaintext-Version" },
      },
    },
  },
  {
    name: "send_campaign",
    description:
      "Eine Kampagne jetzt senden oder zu einem Datum planen (ISO 8601).",
    inputSchema: {
      type: "object",
      required: ["campaign_id"],
      properties: {
        campaign_id: { type: "string" },
        scheduled_date: {
          type: "string",
          description: "ISO 8601 Datum/Zeit für Planung — weglassen für sofortigen Versand",
        },
      },
    },
  },

  // AUTOMATIONS
  {
    name: "list_automations",
    description: "Alle Automationen mit Statistiken abrufen.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "add_contact_to_automation",
    description: "Eine Automation für einen bestimmten Kontakt starten.",
    inputSchema: {
      type: "object",
      required: ["contact_id", "automation_id"],
      properties: {
        contact_id: { type: "string" },
        automation_id: { type: "string" },
      },
    },
  },

  // CONTACT MANAGEMENT
  {
    name: "delete_contacts_by_tag",
    description:
      "Alle Kontakte mit einem bestimmten Tag löschen. Für Listenpflege (z.B. alle 'Inaktiv'- oder 'Bot'-Kontakte entfernen). Gibt Anzahl gelöschter Kontakte zurück.",
    inputSchema: {
      type: "object",
      required: ["tag_id"],
      properties: {
        tag_id: { type: "string", description: "ID des Tags (z.B. '53' für Inaktiv)" },
        dry_run: { type: "boolean", description: "Wenn true: nur zählen, nicht löschen (Probelauf)" },
      },
    },
  },

  // FUNNEL BUILDER
  {
    name: "build_product_funnel",
    description:
      "Kompletten E-Mail-Funnel für ein Produkt aufbauen: erstellt Tag, Kampagnen-Entwürfe und einen Automationsplan. Perfekt für Produkt-Launches.",
    inputSchema: {
      type: "object",
      required: [
        "product_name",
        "product_price",
        "product_description",
        "from_name",
        "from_email",
        "list_id",
      ],
      properties: {
        product_name: { type: "string" },
        product_price: { type: "string", description: "z.B. CHF 777" },
        product_description: { type: "string", description: "Kurze Produktbeschreibung (2–3 Sätze)" },
        target_audience: { type: "string", description: "Zielgruppe (z.B. Mamas im Network Marketing)" },
        from_name: { type: "string" },
        from_email: { type: "string" },
        list_id: { type: "string" },
        num_emails: {
          type: "number",
          description: "Anzahl Mails in der Sequenz (Standard: 3, max: 5)",
        },
      },
    },
  },
];

// ─── Tool Handler ─────────────────────────────────────────────────────────────

const server = new Server(
  { name: "activecampaign-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      // ── CONTACTS ──────────────────────────────────────────────────────────
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
        let id = args.id;
        if (!id) {
          const s = await ac(`/contacts?email=${encodeURIComponent(args.email)}`);
          id = s.contacts?.[0]?.id;
          if (!id) throw new Error(`Kein Kontakt mit E-Mail: ${args.email}`);
        }
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

      case "find_inactive_contacts": {
        const days = args.days || 90;
        const cutoff = new Date(Date.now() - days * 86400000)
          .toISOString()
          .split("T")[0];
        const p = new URLSearchParams({
          limit: args.limit || 100,
          offset: args.offset || 0,
        });
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
        const data = await ac(
          `/campaigns/${args.campaign_id}/nonOpens?limit=${args.limit || 50}`
        );
        result = {
          campaignId: args.campaign_id,
          nonOpeners: data.nonopeners || data,
        };
        break;
      }

      // ── LISTS ─────────────────────────────────────────────────────────────
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

      // ── TAGS ──────────────────────────────────────────────────────────────
      case "list_tags": {
        const q = args.search
          ? `?search=${encodeURIComponent(args.search)}`
          : "?limit=100";
        const data = await ac(`/tags${q}`);
        result = (data.tags || []).map((t) => ({
          id: t.id,
          name: t.tag,
          description: t.description,
        }));
        break;
      }

      case "create_tag": {
        const data = await ac("/tags", "POST", {
          tag: {
            tag: args.name,
            tagType: "contact",
            description: args.description || "",
          },
        });
        result = { id: data.tag.id, name: data.tag.tag, created: true };
        break;
      }

      case "tag_contact": {
        const data = await ac("/contactTags", "POST", {
          contactTag: { contact: args.contact_id, tag: args.tag_id },
        });
        result = { success: true, id: data.contactTag?.id };
        break;
      }

      // ── CAMPAIGNS ─────────────────────────────────────────────────────────
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
          openRate: c.sends
            ? `${((c.uniqueopens / c.sends) * 100).toFixed(1)}%`
            : "–",
          clickRate: c.sends
            ? `${((c.linkclicks / c.sends) * 100).toFixed(1)}%`
            : "–",
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
          openRate: c.sends
            ? `${((c.uniqueopens / c.sends) * 100).toFixed(1)}%`
            : "–",
          clicks: c.linkclicks,
          clickRate: c.sends
            ? `${((c.linkclicks / c.sends) * 100).toFixed(1)}%`
            : "–",
          unsubscribes: c.unsubscribes,
          hardBounces: c.hardbounces,
          softBounces: c.softbounces,
          links: (links.links || []).map((l) => ({
            url: l.link,
            clicks: l.clicks,
          })),
        };
        break;
      }

      case "analyze_campaigns": {
        const data = await ac(
          `/campaigns?limit=${args.limit || 30}&filters[status]=4`
        );
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
        const data = await ac("/campaigns", "POST", {
          campaign: {
            type: "single",
            name: args.name,
            subject: args.subject,
            fromname: args.from_name,
            fromemail: args.from_email,
            list: args.list_id,
            htmlcontent: args.html_content,
            textcontent: args.text_content || "",
            status: 0,
          },
        });
        result = {
          id: data.campaign.id,
          name: data.campaign.name,
          status: "draft",
          created: true,
        };
        break;
      }

      case "send_campaign": {
        if (args.scheduled_date) {
          const data = await ac("/campaignSchedules", "POST", {
            campaignSchedule: {
              campaign: args.campaign_id,
              sdate: args.scheduled_date,
              status: 1,
            },
          });
          result = {
            scheduled: true,
            date: args.scheduled_date,
            id: data.campaignSchedule?.id,
          };
        } else {
          await ac(`/campaigns/${args.campaign_id}`, "PUT", {
            campaign: { status: 1 },
          });
          result = { sent: true, campaignId: args.campaign_id };
        }
        break;
      }

      // ── AUTOMATIONS ───────────────────────────────────────────────────────
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
        const data = await ac("/contactAutomations", "POST", {
          contactAutomation: {
            contact: args.contact_id,
            automation: args.automation_id,
          },
        });
        result = { success: true, id: data.contactAutomation?.id };
        break;
      }

      // ── CONTACT MANAGEMENT ────────────────────────────────────────────────
      case "delete_contacts_by_tag": {
        const dryRun = args.dry_run || false;
        let offset = 0;
        const limit = 100;
        let totalDeleted = 0;
        let allContacts = [];

        // Alle Kontakte mit dem Tag sammeln
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
            preview: allContacts.slice(0, 10).map(c => ({ id: c.id, email: c.email, name: `${c.firstName} ${c.lastName}`.trim() })),
          };
          break;
        }

        // Kontakte in Batches von 10 löschen
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
                if (res.ok || res.status === 404) {
                  totalDeleted++;
                } else {
                  errors.push({ id: c.id, email: c.email, status: res.status });
                }
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
          errors: errors.length > 0 ? errors : undefined,
          message: `✅ ${totalDeleted} von ${allContacts.length} Kontakten erfolgreich gelöscht.`,
        };
        break;
      }

      // ── FUNNEL BUILDER ────────────────────────────────────────────────────
      case "build_product_funnel": {
        const numEmails = Math.min(args.num_emails || 3, 5);

        // 1. Funnel-Tag erstellen
        const tagRes = await ac("/tags", "POST", {
          tag: {
            tag: `Funnel: ${args.product_name}`,
            tagType: "contact",
            description: `Auto-Funnel für ${args.product_name} (${args.product_price})`,
          },
        });
        const tagId = tagRes.tag.id;

        // 2. Kampagnen-Entwürfe erstellen
        const templates = buildFunnelEmails(
          args.product_name,
          args.product_price,
          args.product_description,
          args.target_audience || "Mamas im Network Marketing",
          numEmails
        );

        const campaigns = [];
        for (const t of templates) {
          const r = await ac("/campaigns", "POST", {
            campaign: {
              type: "single",
              name: `[Funnel: ${args.product_name}] ${t.name}`,
              subject: t.subject,
              fromname: args.from_name,
              fromemail: args.from_email,
              list: args.list_id,
              htmlcontent: t.html,
              textcontent: t.text,
              status: 0,
            },
          });
          campaigns.push({
            id: r.campaign.id,
            name: t.name,
            subject: t.subject,
          });
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
            `⚙️ Gehe in ActiveCampaign → Automationen → Neu erstellen`,
            `⚙️ Trigger: Tag wird hinzugefügt → "Funnel: ${args.product_name}"`,
            `⚙️ Füge die Kampagnen mit 2-Tage-Wartezeiten als Schritte ein`,
          ],
        };
        break;
      }

      default:
        throw new Error(`Unbekanntes Tool: ${name}`);
    }

    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  } catch (err) {
    return {
      content: [{ type: "text", text: `❌ Fehler: ${err.message}` }],
      isError: true,
    };
  }
});

// ─── Funnel Email Templates ───────────────────────────────────────────────────

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
<ul>
  <li>✅ [Vorteil 1 einfügen]</li>
  <li>✅ [Vorteil 2 einfügen]</li>
  <li>✅ [Vorteil 3 einfügen]</li>
</ul>
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
<blockquote><em>"[Testimonial 1 einfügen]" — Name, Ort</em></blockquote>
<blockquote><em>"[Testimonial 2 einfügen]" — Name, Ort</em></blockquote>
<p>Das ist, was ich mir für dich wünsche.</p>
<p><a href="[DEIN LINK]">Ich bin dabei →</a></p>
<p>Herzlich,<br>Patricia</p>`,
      text: `Hey {{contact.first_name}}, hier sind Stimmen anderer Mamas...`,
    },
    {
      name: "Email 5 – Letzte Chance",
      subject: `Das ist meine letzte Mail dazu.`,
      html: `<p>Hey {{contact.first_name}},</p>
<p>ich mache es kurz.</p>
<p>Das ist meine letzte Mail zu <strong>${name}</strong> (${price}).</p>
<p>Wenn du dir denkst: <em>"Ja, das ist meins"</em> — dann ist jetzt der Moment.</p>
<p><a href="[DEIN LINK]">Ja, ich bin dabei →</a></p>
<p>Falls nicht: kein Problem. Ich schreibe dir bald wieder über etwas anderes. 😊</p>
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
    tip: "Füge zwischen den E-Mails If/Else-Bedingungen ein (z.B. 'Hat gekauft?' → Automation beenden)",
  };
}

// ─── Start Server ─────────────────────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
