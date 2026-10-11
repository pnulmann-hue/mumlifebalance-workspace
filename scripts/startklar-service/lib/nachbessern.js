/**
 * Nachkontrolle gegen das Nicht-Sondern-Muster.
 *
 * Warum überhaupt: Das Muster steht in Patricias Floskel-Blackliste ganz oben,
 * und Sprachmodelle bauen es reflexartig, weil es rhetorisch schlau klingt.
 * Die Anweisung im Systemtext senkt die Quote, killt sie aber nicht.
 * Deshalb hier ein harter Filter — er kostet nur dann einen zweiten Aufruf,
 * wenn das Muster tatsächlich drin ist.
 */

const MUSTER = /\bsondern\b/i;

export function hatVerbotenesMuster(text) {
  return MUSTER.test(text || "");
}

/** Findet den Satz, in dem das Muster steckt. */
function betroffenerSatz(text) {
  const saetze = String(text).split(/(?<=[.!?])\s+/);
  return saetze.find((s) => MUSTER.test(s)) || "";
}

/**
 * Lässt die betroffene Stelle einmal umschreiben.
 * Gibt den korrigierten Text zurück — oder den ursprünglichen, wenn es nicht klappt.
 */
export async function nachbessern(client, text) {
  const satz = betroffenerSatz(text);
  if (!satz) return text;

  try {
    const antwort = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 400,
      output_config: { effort: "low" },
      system:
        "Du korrigierst deutschen Text. Das Wort „sondern\" und das Muster " +
        "„nicht X, sondern Y\" sind verboten. Schreib die Stelle in zwei eigenen " +
        "Sätzen neu, ohne den Inhalt zu ändern und ohne den Ton zu verändern. " +
        "Schweizer ss statt ß. Antworte ausschliesslich mit dem korrigierten Satz, " +
        "ohne Anführungszeichen, ohne Erklärung.",
      messages: [{ role: "user", content: satz }],
    });

    const neu = antwort.content
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join(" ")
      .trim()
      .replace(/^["„»]|["“«]$/g, "");

    if (!neu || hatVerbotenesMuster(neu)) return text;
    return text.replace(satz, neu);
  } catch (e) {
    console.error("Nachbesserung fehlgeschlagen:", e.message);
    return text;
  }
}
