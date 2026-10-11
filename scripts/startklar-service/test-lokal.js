/**
 * Schneller Testlauf ohne Vercel.
 *
 *   cd scripts/startklar-service
 *   npm install
 *   node --env-file=.env test-lokal.js
 *
 * Ruft dieselbe Logik auf wie der Endpunkt und zeigt, was eine Käuferin lesen würde.
 */
import Anthropic from "@anthropic-ai/sdk";
import { systemtext, STATIONEN } from "./lib/patricia-regeln.js";
import { hatVerbotenesMuster, nachbessern } from "./lib/nachbessern.js";

const client = new Anthropic();

const FAELLE = [
  {
    name: "Bananen-Fall (Thema passt nicht)",
    station: "hook",
    thema: "Sandra · Natürliche Hautpflege für Mamas ab 35 · 3 Jahre unreine Haut, dann kam die Umstellung",
    eingabe: { hook: "Unser Frühstück heute sind Bananen" },
    formcheck: ["9 Wörter — die Länge sitzt.", "Weder Zeitanker noch Zahl."],
  },
  {
    name: "Guter Fall (sollte grün durchgehen)",
    station: "hook",
    thema: "Sandra · Natürliche Hautpflege für Mamas ab 35 · 3 Jahre unreine Haut, dann kam die Umstellung",
    eingabe: { hook: "Gestern hat mich meine Tochter gefragt, warum ich nie ohne Make-up rausgehe." },
    formcheck: ["Zeitanker drin.", "13 Wörter."],
  },
  {
    name: "Karussell (blass, keine Themenverbindung)",
    station: "karussell",
    thema: "Sandra · Natürliche Hautpflege für Mamas ab 35 · 3 Jahre unreine Haut",
    eingabe: {
      f1: "5 Tipps für einen guten Start in den Tag",
      f2: "Früh aufstehen ist wichtig. Dann hast du mehr vom Tag und bist entspannter.",
      f3: "Trink genug Wasser",
      f4: "Mach Sport",
      f5: "Denk positiv",
      f6: "Ich hoffe die Tipps helfen dir",
    },
    formcheck: ["Folie 2 hat 2 Sätze.", "Auf der letzten Folie steht keine Aufforderung."],
  },
  {
    name: "Story-Umfrage (zu allgemein)",
    station: "story",
    thema: "Sandra · Natürliche Hautpflege für Mamas ab 35 · 3 Jahre unreine Haut",
    eingabe: { frage: "Wie geht es dir heute?", a: "Gut", b: "Nicht so gut" },
    formcheck: ["5 Wörter — schnell erfassbar.", "Zwei echte Möglichkeiten."],
  },
  {
    name: "Caption (Begrüssung + zu viele Hashtags)",
    station: "caption",
    thema: "Sandra · Natürliche Hautpflege für Mamas ab 35 · 3 Jahre unreine Haut",
    eingabe: {
      text: "Hallo ihr Lieben ☀️\n\nheute möchte ich euch mal wieder etwas zu meiner Hautpflege erzählen. Ich benutze jetzt seit einiger Zeit neue Produkte und bin sehr zufrieden damit.\n\n#hautpflege #beauty #mama #naturkosmetik #glow #selfcare #skincare #mamaleben",
    },
    formcheck: ["Deine Caption fängt mit „hallo\" an.", "8 Hashtags."],
  },
  {
    name: "Bio mit Firmenname",
    station: "bio",
    thema: "Sandra · Beraterin",
    eingabe: {
      z1: "Sandra, Beraterin bei doTERRA",
      z2: "Mama von 2",
      z3: "Öle für die ganze Familie",
      z4: "Schreib mir",
    },
    formcheck: ["Ich lese „doterra\" in deiner Bio.", "In Zeile 4 fehlt die Aufforderung."],
  },
];

function nutzertext(f) {
  const def = STATIONEN[f.station];
  return [
    `STATION: ${def.label}`,
    `WORAUF ES HIER ANKOMMT: ${def.fokus}`,
    "",
    `THEMA DER FRAU: ${f.thema}`,
    "",
    "WAS SIE GESCHRIEBEN HAT:",
    Object.entries(f.eingabe).map(([k, v]) => `${k}: ${v}`).join("\n"),
    "",
    "FORMCHECK (lief schon automatisch, wiederhol das nicht):",
    f.formcheck.map((z) => `- ${z}`).join("\n"),
  ].join("\n");
}

for (const f of FAELLE) {
  console.log("\n" + "=".repeat(70));
  console.log(f.name);
  console.log("=".repeat(70));
  const antwort = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 900,
    output_config: { effort: "low" },
    system: [{ type: "text", text: systemtext(), cache_control: { type: "ephemeral" } }],
    messages: [{ role: "user", content: nutzertext(f) }],
  });
  let ausgabe = antwort.content
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();

  if (hatVerbotenesMuster(ausgabe)) {
    console.log("[Nachkontrolle greift — Nicht-Sondern-Muster gefunden]\n");
    ausgabe = await nachbessern(client, ausgabe);
  }

  console.log(ausgabe);
  console.log(`\n[Wörter: ${ausgabe.split(/\s+/).filter(Boolean).length}]`);
  const u = antwort.usage;
  console.log(
    `\n[ein: ${u.input_tokens} · aus Zwischenspeicher: ${u.cache_read_input_tokens ?? 0} · aus: ${u.output_tokens}]`
  );
}
