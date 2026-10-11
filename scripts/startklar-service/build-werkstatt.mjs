/**
 * Kopiert die Werkstatt aus outputs/ nach public/, damit Vercel sie ausliefert.
 *
 *   node build-werkstatt.mjs
 *
 * Warum überhaupt: Wenn Seite und Dienst auf derselben Adresse liegen, entfällt
 * die Herkunftsprüfung komplett — kein CORS, keine Blockade durch fremde Seiten.
 * Die Werkstatt liegt dann unter https://startklar-service.vercel.app
 *
 * Die Datei in outputs/ bleibt die Quelle. Hier wird nur kopiert und ein
 * Grundgerüst drumherum gelegt.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const hier = path.dirname(fileURLToPath(import.meta.url));
const quelle = path.resolve(
  hier,
  "../../outputs/produkte/instagram-startklar/04-arbeitsblaetter/startklar-werkstatt.html"
);
const zielOrdner = path.join(hier, "public");
const ziel = path.join(zielOrdner, "index.html");

const inhalt = fs.readFileSync(quelle, "utf8");

const seite = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
${inhalt}
</html>
`;

fs.mkdirSync(zielOrdner, { recursive: true });
fs.writeFileSync(ziel, seite, "utf8");
console.log(`geschrieben: ${ziel} (${(seite.length / 1024).toFixed(1)} KB)`);
