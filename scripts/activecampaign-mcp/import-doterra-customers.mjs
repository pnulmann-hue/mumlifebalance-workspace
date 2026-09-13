/**
 * Importiert die direkten doTERRA-Kunden in ActiveCampaign:
 * - Kontakt erstellen/aktualisieren (contact/sync ist idempotent)
 * - Liste 20 "doTERRA Kunden" zuweisen
 * - Tag 56 "doterra-kunde" + Mitgliedsart-Tag
 *
 * Ausgeschlossen: 3 Ghost Legs + 4 DSGVO-inforemoval
 *
 * 🚨 Die Kundendaten stehen NICHT in dieser Datei.
 * Namen, Mailadressen und Telefonnummern gehoeren anderen Menschen und haben
 * im Repo nichts verloren. Sie liegen in doterra-kunden.json daneben, und die
 * Datei ist ausgeschlossen. Fehlt sie, bricht das Skript mit einem Hinweis ab.
 *
 * Ebenso der API-Schluessel: kommt aus der Umgebung, steht nirgends im Code.
 *
 * Aufruf:
 *   node --env-file=../../04-projects/activecampaign-mcp/.env import-doterra-customers.mjs
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const HIER = path.dirname(fileURLToPath(import.meta.url));

const AC_URL = process.env.AC_API_URL || "https://mumlifebalance.api-us1.com";
const AC_KEY = process.env.AC_API_KEY;
const LIST_ID = 20;
const TAG_ALL = 56; // doterra-kunde
const TAG_VK = 57;  // doterra-vorteilskunde
const TAG_WA = 58;  // doterra-wellness-advocate

if (!AC_KEY) {
  console.error(
    "AC_API_KEY fehlt.\n" +
    "Das Skript so aufrufen, damit der Schlüssel aus der .env kommt:\n" +
    "  node --env-file=../../04-projects/activecampaign-mcp/.env import-doterra-customers.mjs"
  );
  process.exit(1);
}

const KUNDEN_DATEI = path.join(HIER, "doterra-kunden.json");
let customers;
try {
  customers = JSON.parse(readFileSync(KUNDEN_DATEI, "utf-8"));
} catch (e) {
  console.error(
    `Kundendaten nicht lesbar: ${KUNDEN_DATEI}\n` +
    "Die Datei ist absichtlich nicht im Repo (Daten Dritter).\n" +
    "Format: [{ name, email, phone, type: \"WA\"|\"VK\", doterraId }, ...]"
  );
  process.exit(1);
}

async function ac(method, path, body) {
  const res = await fetch(`${AC_URL}/api/3/${path}`, {
    method,
    headers: { "Api-Token": AC_KEY, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`AC ${res.status}: ${JSON.stringify(data).slice(0, 200)}`);
  return data;
}

async function importCustomer(c) {
  // Name aufteilen
  const parts = c.name.trim().split(/\s+/);
  const firstName = parts[0];
  const lastName = parts.slice(1).join(" ");

  // 1. Contact sync (idempotent: create or update)
  const syncRes = await ac("POST", "contact/sync", {
    contact: {
      email: c.email,
      firstName,
      lastName,
      phone: c.phone || undefined,
      fieldValues: [], // Custom fields later
    },
  });
  const contactId = syncRes.contact.id;

  // 2. Liste 20 zuweisen (status 1 = subscribed)
  try {
    await ac("POST", "contactLists", {
      contactList: { list: LIST_ID, contact: contactId, status: 1 },
    });
  } catch (e) {
    // falls schon in Liste: ignorieren
    if (!String(e.message).includes("already")) console.warn(`  ⚠ List: ${e.message.slice(0,80)}`);
  }

  // 3. Tags
  const tagsToAdd = [TAG_ALL, c.type === "WA" ? TAG_WA : TAG_VK];
  for (const tagId of tagsToAdd) {
    try {
      await ac("POST", "contactTags", {
        contactTag: { contact: contactId, tag: tagId },
      });
    } catch (e) {
      // schon getaggt: ignorieren
    }
  }

  return contactId;
}

async function main() {
  console.log(`📥 Importiere ${customers.length} doTERRA-Kunden in AC Liste ${LIST_ID}...`);
  let ok = 0, fail = 0;
  for (const c of customers) {
    try {
      const id = await importCustomer(c);
      console.log(`  ✅ ${c.name.padEnd(32)} → AC-ID ${id} (${c.type})`);
      ok++;
    } catch (e) {
      console.error(`  ❌ ${c.name}: ${e.message}`);
      fail++;
    }
  }
  console.log(`\n🎉 Fertig: ${ok} importiert, ${fail} Fehler`);
}

main();
