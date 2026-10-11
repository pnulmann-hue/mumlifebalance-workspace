/* =============================================================
   Ist dieser Kommentar eine Anfrage nach dem Stichwort?
   =============================================================
   Der Ersatz für ManyChats „Kommentar enthält das Wort“. Anlass
   (Patricia, 28.09.2026): „ich stimme dir zu“ löst in ManyChat den
   Stimm-Check aus, obwohl niemand ihn wollte.

   Drei Stufen, damit Claude nur bei den unklaren Fällen gefragt wird:
     1. ja   — das Stichwort steht allein oder mit Höflichkeit
               („Stimme“, „STIMME 🙋‍♀️“, „Stimme, bitte“, „bitte stimme“)
     2. nein — das Wort kommt nicht vor, oder es steht in einem Satz,
               der eindeutig etwas anderes meint („ich stimme dir zu“)
     3. frag — kurz und nicht eindeutig, dann entscheidet Claude
   ============================================================= */

/* Wörter, die neben dem Stichwort stehen dürfen, ohne den Sinn zu ändern. */
const HOEFLICH = new Set([
  "bitte", "gerne", "gern", "ja", "danke", "merci", "please", "pls", "plz",
  "hier", "ich", "auch", "mir", "mal", "bitteschön", "bittesehr", "hallo", "hoi",
  "liebe", "patricia", "und", "gerne!", "juhu", "yes",
]);

/* Stellen, an denen „stimme“ ein Verb ist und keine Anfrage. */
const VERB_MUSTER = [
  /\bstimme\s+(dir|dem|euch|ihr|ihnen|da|voll|total|absolut|100|zu|nicht|komplett|vollkommen|ganz)\b/,
  /\b(ich|da|so|dem|voll|total)\s+stimme\b/,
  /\bstimme\b[^.!?]{0,40}\bzu\b/,
  /\b(meine|deine|seine|ihre|innere|innerer)\s+stimme\b/,
];

function normal(text) {
  return String(text || "")
    .toLowerCase()
    .normalize("NFKC")
    .replace(/[\u{1F000}-\u{1FFFF}\u{2600}-\u{27BF}\u{FE0F}\u{200D}]/gu, " ")  // Emojis
    .replace(/[^\p{L}\p{N}\s]/gu, " ")                                          // Satzzeichen
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * @returns {{ urteil: "ja"|"nein"|"frag", grund: string }}
 */
export function vorpruefen(kommentar, stichwort = "stimme") {
  const roh = String(kommentar || "");
  const n = normal(roh);
  const kw = stichwort.toLowerCase();
  const woerter = n ? n.split(" ") : [];

  if (!woerter.includes(kw)) return { urteil: "nein", grund: "Stichwort kommt nicht vor" };

  const rest = woerter.filter((w) => w !== kw);
  if (rest.every((w) => HOEFLICH.has(w))) {
    return { urteil: "ja", grund: rest.length ? "Stichwort mit Höflichkeit" : "Stichwort allein" };
  }

  // In Grossbuchstaben ist es fast immer das Stichwort, auch mitten im Satz
  // („Hab gerade STIMME geschrieben“).
  if (new RegExp(`\\b${stichwort.toUpperCase()}\\b`).test(roh)) {
    return { urteil: "ja", grund: "Stichwort in Grossbuchstaben" };
  }

  if (VERB_MUSTER.some((m) => m.test(n))) {
    return { urteil: "nein", grund: "„stimme“ als Verb oder als Wort im Satz" };
  }

  // Lange Kommentare, in denen das Wort klein vorkommt, sind Gespräch.
  if (woerter.length > 8) return { urteil: "nein", grund: "langer Kommentar, Wort klein im Satz" };

  return { urteil: "frag", grund: "kurz und nicht eindeutig" };
}

/**
 * Fragt Claude, wenn die Regeln es nicht wissen. Gibt true/false zurück.
 * @param {object} p
 * @param {string} p.kommentar
 * @param {string} p.beitrag   Caption des Beitrags, unter dem kommentiert wurde
 * @param {Function} p.anfrage  async (body) => antwort-JSON (Anthropic Messages API)
 */
export async function claudeFragen({ kommentar, beitrag = "", stichwort = "STIMME", anfrage }) {
  const auftrag =
    `Unter einem Instagram-Beitrag steht ein Kommentar. Wer das Stichwort ${stichwort} ` +
    `kommentiert, bekommt einen Link per Direktnachricht. Entscheide, ob diese Person den ` +
    `Link haben will. „Ich stimme dir zu“ oder ähnliche Sätze, in denen das Wort nur ` +
    `vorkommt, sind KEINE Anfrage.\n\n` +
    `Beitrag (Auszug): ${String(beitrag).slice(0, 600)}\n\nKommentar: ${kommentar}\n\n` +
    `Antworte nur mit ja oder nein.`;
  const antwort = await anfrage({
    model: process.env.ANTHROPIC_MODEL || "claude-haiku-4-5-20251001",
    max_tokens: 5,
    messages: [{ role: "user", content: auftrag }],
  });
  const text = (antwort?.content?.[0]?.text || "").trim().toLowerCase();
  return text.startsWith("ja");
}

/** Beides zusammen. Ohne `anfrage` (lokaler Test) gilt „frag“ als nein. */
export async function istAnfrage({ kommentar, beitrag, anfrage, stichwort = "stimme" }) {
  const v = vorpruefen(kommentar, stichwort);
  if (v.urteil !== "frag") return { ja: v.urteil === "ja", stufe: "regel", grund: v.grund };
  if (!anfrage) return { ja: false, stufe: "ohne-claude", grund: v.grund };
  const ja = await claudeFragen({ kommentar, beitrag, stichwort: stichwort.toUpperCase(), anfrage });
  return { ja, stufe: "claude", grund: v.grund };
}
