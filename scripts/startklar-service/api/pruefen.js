import Anthropic from "@anthropic-ai/sdk";
import { systemtext, STATIONEN } from "../lib/patricia-regeln.js";
import { hatVerbotenesMuster, nachbessern } from "../lib/nachbessern.js";

const client = new Anthropic();

/** Wer das Tool einbetten darf. Zusätzliche Adressen über ERLAUBTE_HERKUNFT (Komma-Liste). */
const HERKUNFT = [
  "https://startklar.mumlifebalance.ch",
  "https://startklar-service.vercel.app",
  "https://mumlifebalance.ch",
  "https://www.mumlifebalance.ch",
  "https://mumlifebalance.thrivecart.com",
  ...(process.env.ERLAUBTE_HERKUNFT || "").split(",").map((s) => s.trim()).filter(Boolean),
];

/** Obergrenze pro Zugangscode. Greift nur, wenn ein KV-Speicher hinterlegt ist. */
const MAX_PRUEFUNGEN = Number(process.env.MAX_PRUEFUNGEN || 150);

/** Hängt an jeder Störungsmeldung, damit Patricia davon erfährt. Über KONTAKT_HINWEIS anpassbar. */
const KONTAKT =
  process.env.KONTAKT_HINWEIS ||
  "Sag Patricia bitte kurz Bescheid, dass das hier gerade nicht ging — sie erfährt es sonst nicht.";

function setzeHerkunft(req, res) {
  const origin = req.headers.origin;
  if (origin && HERKUNFT.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
  }
  res.setHeader("Vary", "Origin");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

function codeGueltig(code) {
  const liste = (process.env.ZUGANGSCODES || "")
    .split(",")
    .map((s) => s.trim().toUpperCase())
    .filter(Boolean);
  if (!liste.length) return true; // keine Codes hinterlegt = offen (nur für deine Tests)
  return liste.includes(String(code || "").trim().toUpperCase());
}

/**
 * Zählt Prüfungen pro Code, wenn ein Upstash-/Vercel-KV hinterlegt ist.
 * Ohne KV läuft alles weiter, nur ohne harte Obergrenze.
 */
async function zaehle(code) {
  const url = process.env.KV_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN;
  if (!url || !token || !code) return { stand: null, ueberschritten: false };
  try {
    const schluessel = "startklar:" + String(code).trim().toUpperCase();
    const antwort = await fetch(`${url}/incr/${encodeURIComponent(schluessel)}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const daten = await antwort.json();
    const stand = Number(daten.result || 0);
    return { stand, ueberschritten: stand > MAX_PRUEFUNGEN };
  } catch (e) {
    console.error("Zähler nicht erreichbar:", e.message);
    return { stand: null, ueberschritten: false };
  }
}

function eingabeAlsText(eingabe) {
  if (!eingabe || typeof eingabe !== "object") return "";
  return Object.entries(eingabe)
    .filter(([, v]) => v && String(v).trim())
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`)
    .join("\n")
    .slice(0, 3000);
}

export default async function handler(req, res) {
  setzeHerkunft(req, res);
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ fehler: "Nur POST." });

  const { station, eingabe, thema, formcheck, code } = req.body || {};

  if (!codeGueltig(code)) {
    return res.status(403).json({
      fehler: "code_ungueltig",
      text: `Diesen Zugangscode kenne ich nicht. Er steht im Kurs in der Lektion »Deine Werkstatt«. Wenn er von dort stammt und trotzdem nicht geht: ${KONTAKT}`,
    });
  }

  const def = STATIONEN[station];
  if (!def) return res.status(400).json({ fehler: "Unbekannte Station." });

  const text = eingabeAlsText(eingabe);
  if (!text) return res.status(400).json({ fehler: "Nichts zu prüfen." });

  const { stand, ueberschritten } = await zaehle(code);
  if (ueberschritten) {
    return res.status(429).json({
      fehler: "grenze_erreicht",
      text: `Du hast die Werkstatt jetzt ${MAX_PRUEFUNGEN} Mal genutzt — mehr als genug für einen Start. Der Formcheck läuft weiter. Wenn du regelmässig Rückmeldung willst, ist die Instagram-Kundenmaschine dein Ort.`,
    });
  }

  const nutzertext = [
    `STATION: ${def.label}`,
    `WORAUF ES HIER ANKOMMT: ${def.fokus}`,
    "",
    `THEMA DER FRAU: ${thema ? String(thema).slice(0, 400) : "— noch nicht ausgefüllt —"}`,
    "",
    "WAS SIE GESCHRIEBEN HAT:",
    text,
    "",
    "FORMCHECK (lief schon automatisch, wiederhol das nicht):",
    Array.isArray(formcheck) && formcheck.length
      ? formcheck.map((z) => `- ${z}`).join("\n").slice(0, 1500)
      : "- (keine Auffälligkeiten)",
  ].join("\n");

  try {
    const antwort = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 900,
      output_config: { effort: "low" },
      system: [
        { type: "text", text: systemtext(), cache_control: { type: "ephemeral" } },
      ],
      messages: [{ role: "user", content: nutzertext }],
    });

    if (antwort.stop_reason === "refusal") {
      return res.status(200).json({
        text: `Dazu sag ich lieber nichts. Schau nochmal auf den Formcheck oben — der hilft dir hier weiter. Wenn dir das komisch vorkommt: ${KONTAKT}`,
      });
    }

    let ausgabe = antwort.content
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("\n")
      .trim();

    // Nachkontrolle: Das Nicht-Sondern-Muster rutscht trotz Anweisung manchmal durch.
    // Kostet nur dann einen zweiten Aufruf, wenn es wirklich drin ist.
    if (hatVerbotenesMuster(ausgabe)) {
      ausgabe = await nachbessern(client, ausgabe);
    }

    return res.status(200).json({ text: ausgabe, stand });
  } catch (fehler) {
    if (fehler instanceof Anthropic.RateLimitError) {
      return res.status(503).json({
        fehler: "ausgelastet",
        text: `Gerade ist viel los. Probier es in einer Minute nochmal — der Formcheck oben gilt trotzdem. Wenn es dauerhaft klemmt: ${KONTAKT}`,
      });
    }
    if (fehler instanceof Anthropic.AuthenticationError) {
      console.error("Schlüssel fehlt oder ist falsch.");
      return res.status(500).json({ fehler: "schluessel", text: `Der Dienst ist gerade nicht erreichbar. ${KONTAKT}` });
    }
    if (fehler instanceof Anthropic.APIError) {
      console.error("API-Fehler", fehler.status, fehler.message);
      return res.status(502).json({ fehler: "api", text: `Der Dienst antwortet gerade nicht. Der Formcheck oben gilt trotzdem. ${KONTAKT}` });
    }
    console.error(fehler);
    return res.status(500).json({ fehler: "unbekannt", text: `Da ist etwas schiefgelaufen. ${KONTAKT}` });
  }
}
