#!/usr/bin/env node
/**
 * ActiveCampaign-Report — zieht die Kennzahlen und schreibt sie als Markdown ins Repo.
 *
 * Läuft in GitHub Actions (ausserhalb der Claude-Sandbox), damit die Zahlen auch dann
 * verfügbar sind, wenn der AC-MCP-Connector nicht verbindet oder der Sandbox-Proxy
 * activehosted.com blockt.
 *
 * Env: AC_API_URL, AC_API_KEY (Pflicht)
 *      TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (optional, nur mit SEND_TELEGRAM=1)
 *      MAX_TAGS (optional, Default 50)
 *
 * WICHTIG: Der Report enthält ausschliesslich Aggregate — keine E-Mail-Adressen,
 * keine Namen, keine Kontakt-IDs. Das Repo ist public.
 */

const AC_BASE_URL = process.env.AC_API_URL?.replace(/\/+$/, "");
const AC_API_KEY = process.env.AC_API_KEY;
const MAX_TAGS = Number(process.env.MAX_TAGS || 50);
const SEND_TELEGRAM = process.env.SEND_TELEGRAM === "1";

if (!AC_BASE_URL || !AC_API_KEY) {
  console.error("❌ AC_API_URL und AC_API_KEY müssen gesetzt sein (GitHub-Repo-Secrets).");
  process.exit(1);
}

import { writeFileSync, readFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";

const OUT_DIR = "outputs/activecampaign";
const SNAPSHOT = path.join(OUT_DIR, "_snapshot.json");

// ─── API ──────────────────────────────────────────────────────────────────────

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function ac(pathname, attempt = 1) {
  const url = `${AC_BASE_URL}/api/3${pathname}`;
  let res;
  try {
    res = await fetch(url, { headers: { "Api-Token": AC_API_KEY } });
  } catch (err) {
    if (attempt <= 3) {
      await sleep(attempt * 2000);
      return ac(pathname, attempt + 1);
    }
    throw new Error(`Netzwerkfehler bei ${pathname}: ${err.message}`);
  }
  if (res.status === 429 || res.status >= 500) {
    if (attempt <= 3) {
      await sleep(attempt * 3000);
      return ac(pathname, attempt + 1);
    }
  }
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`AC API ${res.status} bei ${pathname}: ${body.slice(0, 300)}`);
  }
  return res.json();
}

/** Zählt Kontakte über meta.total — holt bewusst nur 1 Datensatz statt der ganzen Liste. */
async function countContacts(params = {}) {
  const p = new URLSearchParams({ limit: "1", ...params });
  const data = await ac(`/contacts?${p}`);
  return Number(data.meta?.total ?? 0);
}

// ─── Hilfen ───────────────────────────────────────────────────────────────────

const isoDay = (d) => d.toISOString().split("T")[0];
const daysAgo = (n) => isoDay(new Date(Date.now() - n * 86400000));
const heute = isoDay(new Date());
const pct = (teil, ganz) => (ganz ? `${((teil / ganz) * 100).toFixed(1)} %` : "–");
const num = (n) => (n === null || n === undefined ? "–" : n.toLocaleString("de-CH"));

function delta(jetzt, vorher) {
  if (vorher === null || vorher === undefined || jetzt === null) return "–";
  const d = jetzt - vorher;
  if (d === 0) return "±0";
  return d > 0 ? `+${num(d)}` : num(d);
}

// ─── Erhebung ─────────────────────────────────────────────────────────────────

async function erhebe() {
  const seit7 = daysAgo(7);
  const seit30 = daysAgo(30);

  const kontakteGesamt = await countContacts();
  const neu7 = await countContacts({ "filters[created_after]": seit7 });
  const neu30 = await countContacts({ "filters[created_after]": seit30 });

  // Listen
  const listenRaw = (await ac("/lists?limit=100")).lists || [];
  const listen = [];
  for (const l of listenRaw) {
    listen.push({
      id: l.id,
      name: l.name,
      abonnentinnen: Number(l.subscriber_count ?? 0),
      neu30: await countContacts({ listid: l.id, "filters[created_after]": seit30 }),
    });
  }
  listen.sort((a, b) => b.abonnentinnen - a.abonnentinnen);

  // Tags — das sind bei Patricia die Freebie-/Funnel-Eintritte
  const tagsRaw = ((await ac("/tags?limit=100")).tags || []).slice(0, MAX_TAGS);
  const tags = [];
  for (const t of tagsRaw) {
    const gesamt = await countContacts({ tagid: t.id });
    if (gesamt === 0) continue; // ungenutzte Tags fliegen raus
    tags.push({
      id: t.id,
      name: t.tag,
      kontakte: gesamt,
      neu30: await countContacts({ tagid: t.id, "filters[created_after]": seit30 }),
    });
  }
  tags.sort((a, b) => b.neu30 - a.neu30 || b.kontakte - a.kontakte);

  // Kampagnen — letzte versendete
  const kampagnenRaw = (await ac("/campaigns?limit=50&orders[sdate]=DESC")).campaigns || [];
  const kampagnen = kampagnenRaw
    .filter((c) => Number(c.sends) > 0)
    .slice(0, 15)
    .map((c) => ({
      name: c.name,
      betreff: c.subject,
      datum: (c.sdate || "").split("T")[0],
      versand: Number(c.sends),
      oeffnungen: Number(c.uniqueopens),
      klicks: Number(c.linkclicks),
      abmeldungen: Number(c.unsubscribes),
    }));

  return { datum: heute, kontakteGesamt, neu7, neu30, listen, tags, kampagnen };
}

// ─── Report ───────────────────────────────────────────────────────────────────

function baueReport(d, vorher) {
  const v = vorher || {};
  const vListe = (id) => (v.listen || []).find((x) => x.id === id);
  const vTag = (id) => (v.tags || []).find((x) => x.id === id);

  const oeffnungsraten = d.kampagnen.filter((k) => k.versand > 0).map((k) => (k.oeffnungen / k.versand) * 100);
  const schnittOeffnung = oeffnungsraten.length
    ? oeffnungsraten.reduce((a, b) => a + b, 0) / oeffnungsraten.length
    : null;
  const klickraten = d.kampagnen.filter((k) => k.versand > 0).map((k) => (k.klicks / k.versand) * 100);
  const schnittKlick = klickraten.length ? klickraten.reduce((a, b) => a + b, 0) / klickraten.length : null;

  const proWoche = (d.neu30 / 30) * 7;

  const L = [];
  L.push("---");
  L.push("tags: [ac, kennzahlen]");
  L.push("---");
  L.push("");
  L.push(`# ActiveCampaign — Report ${d.datum}`);
  L.push("");
  L.push(`**Erhoben:** ${new Date().toISOString().replace("T", " ").slice(0, 16)} UTC · automatisch via GitHub Action`);
  L.push(v.datum ? `**Vergleich:** gegen Snapshot vom ${v.datum}` : "**Vergleich:** kein Vorlauf vorhanden (erster Lauf)");
  L.push("");
  L.push("> Nur Aggregate — keine Namen, keine Adressen. Das Repo ist public.");
  L.push("");

  L.push("## Auf einen Blick");
  L.push("");
  L.push("| Kennzahl | Wert | Δ seit letztem Report |");
  L.push("|---|---:|---:|");
  L.push(`| Kontakte gesamt | ${num(d.kontakteGesamt)} | ${delta(d.kontakteGesamt, v.kontakteGesamt)} |`);
  L.push(`| Neue Kontakte (7 Tage) | ${num(d.neu7)} | ${delta(d.neu7, v.neu7)} |`);
  L.push(`| Neue Kontakte (30 Tage) | ${num(d.neu30)} | ${delta(d.neu30, v.neu30)} |`);
  L.push(`| Ø neue Kontakte pro Woche | ${proWoche.toFixed(1)} | – |`);
  L.push(
    `| Ø Öffnungsrate (letzte ${d.kampagnen.length} Kampagnen) | ${
      schnittOeffnung === null ? "–" : schnittOeffnung.toFixed(1) + " %"
    } | – |`
  );
  L.push(`| Ø Klickrate | ${schnittKlick === null ? "–" : schnittKlick.toFixed(1) + " %"} | – |`);
  L.push("");

  L.push("## Listen");
  L.push("");
  L.push("| Liste | Abonnentinnen | Neu (30 T) | Δ Abonnentinnen |");
  L.push("|---|---:|---:|---:|");
  for (const l of d.listen) {
    L.push(`| ${l.name} | ${num(l.abonnentinnen)} | ${num(l.neu30)} | ${delta(l.abonnentinnen, vListe(l.id)?.abonnentinnen)} |`);
  }
  L.push("");

  L.push("## Tags — Freebie- und Funnel-Eintritte");
  L.push("");
  L.push("_Sortiert nach Zuwachs der letzten 30 Tage. Das ist die Intake-Sicht pro Einstieg._");
  L.push("");
  L.push("| Tag | Kontakte | Neu (30 T) | Δ Kontakte |");
  L.push("|---|---:|---:|---:|");
  for (const t of d.tags) {
    L.push(`| ${t.name} | ${num(t.kontakte)} | ${num(t.neu30)} | ${delta(t.kontakte, vTag(t.id)?.kontakte)} |`);
  }
  L.push("");

  L.push("## Kampagnen — letzte versendete");
  L.push("");
  L.push("| Datum | Kampagne | Versand | Öffnungen | Öffnungsrate | Klicks | Klickrate | Abmeldungen |");
  L.push("|---|---|---:|---:|---:|---:|---:|---:|");
  for (const k of d.kampagnen) {
    L.push(
      `| ${k.datum} | ${k.name} | ${num(k.versand)} | ${num(k.oeffnungen)} | ${pct(k.oeffnungen, k.versand)} | ${num(
        k.klicks
      )} | ${pct(k.klicks, k.versand)} | ${num(k.abmeldungen)} |`
    );
  }
  L.push("");

  // Beobachtungen — rein regelbasiert aus den eigenen Zahlen, keine Fremd-Benchmarks
  L.push("## Beobachtungen");
  L.push("");
  const beob = [];
  const toteListen = d.listen.filter((l) => l.neu30 === 0 && l.abonnentinnen > 0);
  if (toteListen.length) beob.push(`Ohne einen einzigen Neuzugang in 30 Tagen: ${toteListen.map((l) => l.name).join(", ")}.`);
  const toteTags = d.tags.filter((t) => t.neu30 === 0);
  if (toteTags.length)
    beob.push(`Tags ohne Zuwachs in 30 Tagen (Einstieg läuft nicht): ${toteTags.map((t) => t.name).join(", ")}.`);
  const topTag = d.tags[0];
  if (topTag && topTag.neu30 > 0)
    beob.push(`Stärkster Einstieg der letzten 30 Tage: **${topTag.name}** mit ${topTag.neu30} neuen Kontakten.`);
  if (schnittOeffnung !== null) {
    const schwach = d.kampagnen.filter((k) => k.versand > 0 && (k.oeffnungen / k.versand) * 100 < schnittOeffnung);
    if (schwach.length)
      beob.push(`Unter dem eigenen Öffnungs-Schnitt: ${schwach.map((k) => `${k.name} (${pct(k.oeffnungen, k.versand)})`).join(", ")}.`);
  }
  beob.push(`Rechnerischer Intake: **${proWoche.toFixed(1)} neue Kontakte pro Woche** über alle Einstiege zusammen.`);
  for (const b of beob) L.push(`- ${b}`);
  L.push("");
  L.push("---");
  L.push("");
  L.push("## 🔗 Verwandte Notizen");
  L.push("");
  L.push("- [[active-funnels|Funnel-Register]]");
  L.push("- [[strategy]]");
  L.push("- [[_MOCs/MOC-Produkte-Funnels|Produkte & Funnels (Map)]]");
  L.push("");

  return { markdown: L.join("\n"), proWoche, schnittOeffnung, topTag };
}

function baueTelegram(d, r, vorher) {
  const z = [];
  z.push(`📊 ActiveCampaign — Stand ${d.datum}`);
  z.push("");
  z.push(`Kontakte gesamt: ${num(d.kontakteGesamt)} (${delta(d.kontakteGesamt, vorher?.kontakteGesamt)})`);
  z.push(`Neu in 7 Tagen: ${num(d.neu7)}`);
  z.push(`Neu in 30 Tagen: ${num(d.neu30)} — das sind ${r.proWoche.toFixed(1)} pro Woche`);
  if (r.schnittOeffnung !== null) z.push(`Ø Öffnungsrate: ${r.schnittOeffnung.toFixed(1)} %`);
  if (r.topTag && r.topTag.neu30 > 0) z.push(`Stärkster Einstieg: ${r.topTag.name} (+${r.topTag.neu30})`);
  z.push("");
  z.push(`Voller Report: outputs/activecampaign/${d.datum}-report.md`);
  return z.join("\n");
}

async function sendeTelegram(text) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chat = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) {
    console.log("ℹ️  Telegram übersprungen — Token oder Chat-ID fehlt.");
    return;
  }
  const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chat, text, disable_web_page_preview: true }),
  });
  if (!res.ok) console.error(`⚠️  Telegram ${res.status}: ${(await res.text()).slice(0, 200)}`);
  else console.log("✅ Telegram verschickt.");
}

// ─── Hauptlauf ────────────────────────────────────────────────────────────────

async function main() {
  mkdirSync(OUT_DIR, { recursive: true });

  const vorher = existsSync(SNAPSHOT) ? JSON.parse(readFileSync(SNAPSHOT, "utf8")) : null;

  console.log("→ Erhebe ActiveCampaign-Kennzahlen …");
  const daten = await erhebe();
  console.log(
    `   ${daten.kontakteGesamt} Kontakte · ${daten.listen.length} Listen · ${daten.tags.length} genutzte Tags · ${daten.kampagnen.length} Kampagnen`
  );

  const report = baueReport(daten, vorher);
  const ziel = path.join(OUT_DIR, `${daten.datum}-report.md`);
  writeFileSync(ziel, report.markdown);
  writeFileSync(SNAPSHOT, JSON.stringify(daten, null, 2) + "\n");
  console.log(`✅ Report geschrieben: ${ziel}`);

  // _INDEX.md für den Obsidian-Vault nachziehen
  const dateien = readdirSync(OUT_DIR)
    .filter((f) => f.endsWith(".md") && f !== "_INDEX.md")
    .sort();
  const idx = [
    "---",
    "tags: [moc, ac, kennzahlen]",
    "---",
    "",
    "# 📊 ActiveCampaign — Index",
    "",
    "Auto-generiert von `scripts/activecampaign-report/fetch-report.mjs`.",
    "",
    "## Dateien",
    "",
    ...dateien.map((f) => `- [[${f.replace(/\.md$/, "")}]]`),
    "",
  ].join("\n");
  writeFileSync(path.join(OUT_DIR, "_INDEX.md"), idx);

  if (SEND_TELEGRAM) await sendeTelegram(baueTelegram(daten, report, vorher));
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});
