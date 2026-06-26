# ActiveCampaign MCP Server (v2)

MCP-Server für ActiveCampaign — gibt Claude direkten Zugriff auf Kontakte, Tags, Listen,
Custom Fields, Kampagnen (E-Mails) und Automationen für `mumlifebalance.api-us1.com`.

Registriert in `.mcp.json` als Server `activecampaign` (Tools heissen `mcp__activecampaign__*`).

## Setup

```bash
cd 04-projects/activecampaign-mcp
npm install
cp .env.example .env   # dann AC_API_URL + AC_API_KEY eintragen
```

`.env` ist gitignored und wird nie committed. Beim Start durch Claude (via `.mcp.json`)
werden die Werte zusätzlich aus der `env`-Sektion injiziert — `.env` ist dann optional,
aber praktisch für lokale Standalone-Läufe (`npm start`).

## Selbsttest

```bash
npm start   # startet stdio-Server, "läuft (stdio)" auf stderr = ok
```

## Tools (24)

**Kontakte**
- `search_contacts` — nach E-Mail/Name/Tag/Liste suchen
- `get_contact` — Details + Aktivitätsverlauf (E-Mail oder ID)
- `create_contact` — neu anlegen oder per E-Mail aktualisieren (Upsert), optional direkt Liste + Tags
- `find_inactive_contacts` — seit X Tagen inaktiv (Pagination)
- `find_non_openers` — Kontakte, die eine Kampagne nicht geöffnet haben
- `delete_contacts_by_tag` — Massenlöschung nach Tag (mit `dry_run`)

**Tags**
- `list_tags` · `create_tag`
- `tag_contact` — Tag hinzufügen (contact_id ODER email)
- `untag_contact` — Tag entfernen (contact_id ODER email)

**Listen**
- `list_lists` · `create_list` (Sender-Defaults für Mum Life Balance hinterlegt)
- `subscribe_to_list` — Kontakt abonnieren (Status 1)
- `unsubscribe_from_list` — Kontakt abmelden (Status 2)

**Custom Fields**
- `list_custom_fields` — alle Felder mit IDs/Typen
- `set_custom_field` — Wert für Kontakt setzen (field_id über list_custom_fields ermitteln)

**Kampagnen / E-Mails**
- `list_campaigns` · `get_campaign_report` · `analyze_campaigns`
- `create_campaign` — E-Mail-Entwurf schreiben/anlegen
- `send_campaign` — **nur auf expliziten Befehl** senden oder planen (ISO 8601)

**Automationen**
- `list_automations`
- `add_contact_to_automation` — Kontakt in bestehende Automation
- `build_product_funnel` — Tag + Kampagnen-Entwürfe + Automationsplan vorbereiten

## Technische Hinweise

- **API V3** (`Api-Token`-Header) ist Standard. Für `create_campaign` / Funnel-Mails wird
  **API V1** (legacy) genutzt, weil V3 dort `405` liefert. V1 erwartet `p[0]=list_id`
  (PHP-Array-Notation, Brackets nicht URL-encoden).
- Tools, die einen Kontakt brauchen, akzeptieren `contact_id` **oder** `email`
  (E-Mail wird intern aufgelöst).
- **Automationen** kann die AC-API nicht als Workflow erstellen — `build_product_funnel`
  legt Tag + Entwürfe an und liefert den Klick-Plan für das AC-Automation-Editor.

## Migration

Vorgänger lag unter `scripts/activecampaign-mcp/` (17 Tools). Dieser v2-Server ist ein
Superset (24 Tools) und ersetzt ihn — `.mcp.json` zeigt jetzt hierher. Der alte Ordner
bleibt nur erhalten, weil die Bulk-Upload-Skripte dort (`bulk-upload-*.mjs`) eigenständig
laufen und die Credentials aus `.mcp.json` lesen.
