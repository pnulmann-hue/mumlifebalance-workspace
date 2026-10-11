/* Gegenproben für den Entscheider: was anschlagen MUSS und was NICHT darf.
   node scripts/kommentar-antwort/test/entscheiden-test.mjs */
import { vorpruefen } from "../lib/entscheiden.mjs";

const JA = [
  "Stimme", "STIMME", "stimme", "Stimme!", "Stimme 🙋‍♀️", "Stimme, bitte", "stimme bitte 🙏",
  "Bitte Stimme", "Stimme gerne", "Ja, Stimme!", "Stimme please", "Hab gerade STIMME geschrieben",
  "STIMME 😍😍", "Stimme bitte, liebe Patricia",
];
const NEIN = [
  "Ich stimme dir zu", "stimme dir voll zu!", "Da stimme ich dir total zu 👏", "Stimme zu",
  "ich stimme zu 100 % zu", "Meine innere Stimme sagt dasselbe", "Deine Stimme ist so beruhigend",
  "Wow, super Beitrag!", "Ich höre immer auf meine Stimme und das hat mir schon so oft geholfen, echt",
  "stimme nicht ganz zu", "Da stimme ich zu",
];
const FRAG = ["will auch die stimme haben", "stimme für mich?"];

let fehler = 0;
function pruefe(liste, soll) {
  for (const k of liste) {
    const r = vorpruefen(k);
    const ok = r.urteil === soll;
    if (!ok) fehler++;
    console.log(`${ok ? "✓" : "✗"} ${soll.padEnd(4)} ${r.urteil.padEnd(4)} „${k}“ — ${r.grund}`);
  }
}
pruefe(JA, "ja");
pruefe(NEIN, "nein");
pruefe(FRAG, "frag");
console.log(fehler ? `\n${fehler} falsch` : "\nalle richtig");
process.exit(fehler ? 1 : 0);
