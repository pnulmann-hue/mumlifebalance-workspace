---
tags: [tools, activecampaign, mcp, funnel]
---

# ActiveCampaign MCP — Tool-Referenz (für ALLE Skills)

**Single Source of Truth** für den ActiveCampaign-Zugriff. Jeder Skill, der mit AC arbeitet
(`/funnel`, `/cockpit`, `/produkt`, `/montag`, Bots …), liest diese Datei statt zu raten.

- **Server:** `04-projects/activecampaign-mcp/` (v2, seit 2026-06-12)
- **Registriert in:** `.mcp.json` als `activecampaign`
- **Tools heissen:** `mcp__activecampaign__<toolname>` — global verfügbar in jeder Session,
  sobald Claude Code geladen ist. Kein Skill muss etwas „verbinden".
- **Account:** `https://mumlifebalance.api-us1.com` · Credentials in `04-projects/activecampaign-mcp/.env` (gitignored)

> ⚠️ **`send_campaign` versendet echte E-Mails** — nur auf ausdrücklichen Befehl von Patricia aufrufen.
> ⚠️ **`delete_contacts_by_tag`** löscht echte Kontakte — immer erst mit `dry_run: true` zeigen.

## Die 24 Tools

### Kontakte
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `search_contacts` | Suchen nach E-Mail/Name/Tag/Liste | — (Filter optional) |
| `get_contact` | Details + Aktivitätsverlauf | `email` ODER `id` |
| `create_contact` | Anlegen/aktualisieren (Upsert), optional Liste + Tags | `email` |
| `find_inactive_contacts` | Seit X Tagen inaktiv (Pagination) | — (`days` Standard 90) |
| `find_non_openers` | Hat Kampagne nicht geöffnet | `campaign_id` |
| `delete_contacts_by_tag` | Massenlöschung nach Tag (⚠️ `dry_run` zuerst) | `tag_id` |

### Tags
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `list_tags` | Alle Tags (optional `search`) | — |
| `create_tag` | Neuen Tag erstellen | `name` |
| `tag_contact` | Tag **hinzufügen** | `tag_id` + (`contact_id` ODER `email`) |
| `untag_contact` | Tag **entfernen** | `tag_id` + (`contact_id` ODER `email`) |

### Listen
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `list_lists` | Alle Listen + Abonnenten-Zahl | — |
| `create_list` | Neue Liste (Sender-Defaults Mum Life Balance) | `name` |
| `subscribe_to_list` | Kontakt abonnieren (Status 1) | `list_id` + (`contact_id` ODER `email`) |
| `unsubscribe_from_list` | Kontakt abmelden (Status 2) | `list_id` + (`contact_id` ODER `email`) |

### Custom Fields
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `list_custom_fields` | Alle Felder mit IDs/Typen | — |
| `set_custom_field` | Wert für Kontakt setzen | `field_id` + `value` + (`contact_id` ODER `email`) |

### Kampagnen / E-Mails
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `list_campaigns` | Alle Kampagnen + Stats | — |
| `get_campaign_report` | Detail-Report (Öffnungen/Klicks/Links) | `campaign_id` |
| `analyze_campaigns` | Top/Flop nach Öffnungs-/Klickrate | — |
| `create_campaign` | E-Mail-**Entwurf** schreiben/anlegen ✅ (funktioniert, via V1) | `name`, `subject`, `from_name`, `from_email`, `list_id`, `html_content` |
| `send_campaign` | ⚠️ Senden ODER planen (ISO 8601) | `campaign_id` |

### Automationen
| Tool | Zweck | Pflicht-Args |
|---|---|---|
| `list_automations` | Alle Automationen + Kontaktzahl | — |
| `add_contact_to_automation` | Kontakt in bestehende Automation | `automation_id` + (`contact_id` ODER `email`) |
| `build_product_funnel` | Tag + Mail-Entwürfe + Automationsplan vorbereiten | `product_name`, `product_price`, `product_description`, `from_name`, `from_email`, `list_id` |

## Bekannte Listen-IDs (Stand 2026-06-12)
- **2** — Regulärer Newsletter/Interessenten
- **3** — Willkommenssequenz

(Aktuelle Liste immer per `list_lists` ziehen.)

## Wichtige Limits / Eigenheiten
- **Automation-Workflows** kann die AC-API **nicht erstellen** — nur Kontakte in bestehende
  schieben. `build_product_funnel` legt Tag + Mail-Entwürfe an und liefert den Klick-Plan
  fürs AC-Automation-Editor.
- **Formulare** werden im AC-UI gebaut (keine API) — Embed-Code liefern.
- `create_campaign` nutzt intern **AC API V1** (V3 liefert dort 405). Funktioniert stabil.
- Kontakt-Tools akzeptieren `contact_id` **oder** `email` — E-Mail wird intern aufgelöst.

## 🔗 Verwandte Notizen
- [[project_funnel-system]]
- `04-projects/activecampaign-mcp/README.md`
