/* =============================================================
   Vercel API Route: /api/webhook — Kommentar-Antwort (ManyChat-Ersatz)
   =============================================================
   Instagram meldet jeden neuen Kommentar hierher. Ist er eine Anfrage
   nach dem Stichwort (lib/entscheiden.mjs), bekommt die Person
   1. eine kurze öffentliche Antwort unter dem Kommentar und
   2. eine private Nachricht mit dem Link.

   Plan: plans/2026-09-28-manychat-ersatz-stimme.md

   Environment (nur in Vercel bzw. .env, nie im Code):
   - WEBHOOK_VERIFY_TOKEN   frei gewählt, dasselbe steht im Meta-Formular
   - IG_APP_SECRET          „Instagram-App-Geheimcode“ (prüft die Signatur)
   - IG_ACCESS_TOKEN        Instagram-Token des Kontos (aus „Konto hinzufügen“)
   - IG_USER_ID             die eigene Instagram-Konto-ID (eigene Kommentare ignorieren)
   - ANTHROPIC_API_KEY      nur für unklare Fälle
   - SCHARF                 "ja" = wirklich antworten; sonst nur protokollieren
   ============================================================= */

import crypto from "node:crypto";
import { istAnfrage } from "../lib/entscheiden.mjs";

export const config = { runtime: "nodejs", maxDuration: 30 };

const GRAPH = "https://graph.instagram.com/v21.0";

/* Je Stichwort: was öffentlich und was privat geantwortet wird.
   Erst einmal nur STIMME (Patricia, 28.09.2026). */
/* Bis zum Start der Masterclass (Do 8.10.2026, 09:00 Zürich = 07:00 UTC) kommt die
   Einladung in dieselbe Nachricht (Patricia, 28.09.2026). Danach fällt sie von selbst weg. */
const MASTERCLASS_BIS = Date.parse("2026-10-08T07:00:00Z");
/* 🚨 Nie Wort für Wort dieselbe Nachricht (13.10.2026): Meta hat das Konto für Links in
   DMs gesperrt, vermutlich weil immer derselbe Text mit demselben Link rausging. Deshalb
   wechseln Begrüssung, Mittelteil und Schluss zufällig — der Link bleibt gleich. */
const STIMM_LINK = "https://mumlifebalance.ch/stimm-check/";
const ANFANG = [
  "Hier ist dein Stimm-Check 💛",
  "Schön, dass du dabei bist! Hier kommt dein Stimm-Check 💛",
  "Da ist er, dein Stimm-Check ✨",
  "Gern! Hier ist der Stimm-Check für dich 💛",
  "Hallo du 😊 Hier kommt dein Stimm-Check.",
];
const MITTE = [
  "In rund 15 Minuten sammelst du die sechs Angaben, die deine KI von dir braucht, damit sie nach dir klingt:",
  "Er fragt dich sechs Dinge ab, und danach weiss deine KI, wie du klingst. Nimm dir etwa eine Viertelstunde dafür:",
  "Eine Viertelstunde, sechs Angaben, und deine KI schreibt endlich so, wie du redest:",
  "Damit deine Texte nach dir klingen, sammelst du hier in etwa 15 Minuten die sechs wichtigsten Angaben:",
];
const SCHLUSS = [
  "",
  "\n\nSag mir gern, wie es dir damit gegangen ist.",
  "\n\nViel Freude beim Ausprobieren!",
  "\n\nWenn etwas hakt, schreib mir einfach hier.",
];
const zufall = (liste) => liste[Math.floor(Math.random() * liste.length)];
const stimmCheckText = () =>
  `${zufall(ANFANG)} ${zufall(MITTE)}\n${STIMM_LINK}${zufall(SCHLUSS)}`;
const OEFFENTLICH = [
  "Schau in deine Nachrichten, ich hab dir den Stimm-Check geschickt 💌",
  "Ist unterwegs, schau mal in deine Nachrichten 💛",
  "Hab ihn dir gerade geschickt, schau in deine DMs ✨",
  "Liegt in deinen Nachrichten für dich bereit 💌",
];
const MASTERCLASS_TEXT =
  "\n\nUnd am Donnerstag, 8. Oktober, um 9 Uhr zeig ich dir in meiner kostenlosen " +
  "Masterclass live, was sonst noch alles mit KI geht. Hier meldest du dich an:\n" +
  "https://mumlifebalance.ch/ki-masterclass/";

const STICHWOERTER = {
  stimme: {
    get oeffentlich() {
      return zufall(OEFFENTLICH);
    },
    get privat() {
      return stimmCheckText() + (Date.now() < MASTERCLASS_BIS ? MASTERCLASS_TEXT : "");
    },
  },
};

function signaturOk(roh, kopf) {
  const geheim = process.env.IG_APP_SECRET;
  if (!geheim) return false;
  if (!kopf || !kopf.startsWith("sha256=")) return false;
  const soll = crypto.createHmac("sha256", geheim).update(roh).digest("hex");
  const ist = kopf.slice(7);
  return soll.length === ist.length && crypto.timingSafeEqual(Buffer.from(soll), Buffer.from(ist));
}

async function rohText(req) {
  const teile = [];
  for await (const t of req) teile.push(t);
  return Buffer.concat(teile).toString("utf8");
}

async function graph(pfad, body) {
  const r = await fetch(`${GRAPH}/${pfad}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${process.env.IG_ACCESS_TOKEN}` },
    body: JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`${pfad}: ${r.status} ${JSON.stringify(j).slice(0, 300)}`);
  return j;
}

async function claudeAnfrage(body) {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error("ANTHROPIC_API_KEY fehlt");
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

async function kommentarBehandeln(wert) {
  const kommentarId = wert?.id;
  const text = wert?.text || "";
  const von = wert?.from?.id || "";
  if (!kommentarId) return;
  if (process.env.IG_USER_ID && von === process.env.IG_USER_ID) return; // eigene Antworten

  for (const [stichwort, antwort] of Object.entries(STICHWOERTER)) {
    const urteil = await istAnfrage({ kommentar: text, stichwort, anfrage: claudeAnfrage });
    // Protokoll ohne Namen: das Repo ist öffentlich, und der Name braucht es nicht.
    console.log(JSON.stringify({ art: "entscheid", stichwort, kommentarId, text, ...urteil }));
    if (!urteil.ja) continue;
    if (process.env.SCHARF !== "ja") {
      console.log(JSON.stringify({ art: "trocken", kommentarId, hinweis: "SCHARF ist nicht ja" }));
      return;
    }
    // 🚨 Erst die private Nachricht. Nur wenn sie wirklich rausging, kommt die
    // öffentliche Antwort — sonst stünde „Schau in deine Nachrichten“ da, und
    // in den Nachrichten wäre nichts (z. B. solange Meta die App nicht geprüft hat).
    await graph(`${process.env.IG_USER_ID}/messages`, {
      recipient: { comment_id: kommentarId },
      message: { text: antwort.privat },
    });
    await graph(`${kommentarId}/replies`, { message: antwort.oeffentlich });
    console.log(JSON.stringify({ art: "geantwortet", stichwort, kommentarId }));
    return;
  }
}

export default async function handler(req, res) {
  // 1 · Meta prüft die Adresse beim Eintragen
  if (req.method === "GET") {
    const q = req.query || {};
    if (q["hub.mode"] === "subscribe" && q["hub.verify_token"] &&
        q["hub.verify_token"] === process.env.WEBHOOK_VERIFY_TOKEN) {
      return res.status(200).send(q["hub.challenge"]);
    }
    return res.status(403).send("nein");
  }
  if (req.method !== "POST") return res.status(405).send("");

  // 2 · Neue Ereignisse. Ohne gültige Signatur wird nichts angefasst.
  const roh = await rohText(req);
  if (!signaturOk(roh, req.headers["x-hub-signature-256"])) {
    console.log(JSON.stringify({ art: "signatur-falsch" }));
    return res.status(401).send("");
  }
  let daten = {};
  try { daten = JSON.parse(roh); } catch { return res.status(400).send(""); }

  const aufgaben = [];
  for (const eintrag of daten.entry || []) {
    for (const aenderung of eintrag.changes || []) {
      if (aenderung.field === "comments") aufgaben.push(kommentarBehandeln(aenderung.value));
    }
  }
  const ergebnisse = await Promise.allSettled(aufgaben);
  for (const e of ergebnisse) if (e.status === "rejected") console.log(JSON.stringify({ art: "fehler", grund: String(e.reason) }));
  // Meta will schnell eine 200 — sonst schickt es dasselbe Ereignis nochmal.
  return res.status(200).send("ok");
}

