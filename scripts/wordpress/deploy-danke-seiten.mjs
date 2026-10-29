/**
 * Danke-Seiten nach dem Absenden der 0€-Formulare — je Funnel eine eigene.
 *
 *   cd scripts/wordpress && node --env-file=.env deploy-danke-seiten.mjs --vorschau   # lokal ansehen
 *   cd scripts/wordpress && node --env-file=.env deploy-danke-seiten.mjs              # als WP-Entwürfe
 *
 * Julias erste Verkaufsstelle („Bonus Deine Danke Seite“): kurz „Postfach öffnen“, dann
 * „Halt, eins noch“ mit einem Angebot, das es nur an dieser Stelle gibt. Patricias Entscheid
 * vom 23.10.2026: der grosse Kurs für 199 statt 333, Satz „nur hier, direkt nach deiner
 * Anmeldung“ — OHNE Uhr und ohne „nur heute“ (die Seite hat eine feste Adresse).
 * Der Preis läuft über ThriveCart-Gutscheine (134 fest, nur Einmalzahlung), weil ThriveCart
 * keine versteckte Preisoption kennt: DANKE199IKM · DANKE199CEO.
 *
 * Gestaltung: CSS der Verkaufsseite /energieroutine/ (Wrapper .enr, liegt im Customizer) —
 * dieselben Markenfarben und Schriften, hier kein eigenes CSS (WAF blockt <style>).
 * Neue Seiten als Entwurf, bestehende behalten ihren Status.
 * Prüfbericht: outputs/funnels/2026-10-23-formular-pruefung.md
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createOrUpdatePage, updatePage, findPageBySlug } from "./wp-api.js";

const HIER = path.dirname(fileURLToPath(import.meta.url));
const VORSCHAU = path.join(HIER, "../../outputs/funnels/danke-seiten");

const HAKEN = '<svg width="15" height="12" viewBox="0 0 14 11" fill="none"><path d="M1 5.5L5 9.5L13 1" stroke="#e8913f" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const KURSE = {
  ikm: {
    name: "Instagram-Kundenmaschine",
    link: "https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/?coupon=DANKE199IKM",
    bild: "https://mumlifebalance.ch/wp-content/uploads/2026/10/instagram-kundenmaschine-mockup.jpg",
    bildAlt: "Die Instagram-Kundenmaschine auf Bildschirm, Tablet und Handy",
    punkte: [
      ["Ein Profil, bei dem die Leute fragen", "vom Produktkatalog zum Schaufenster deiner Expertise"],
      ["Hooks und Captions, die gelesen werden", "und Storys, auf die jemand antwortet"],
      ["Gespräche statt Funkstille", "aus Reaktionen werden Anfragen, Kundschaft und Teampartner"],
      ["Eine Routine, die ohne Motivation läuft", "alles ab dem ersten Tag offen, in deinem Tempo"],
      ["Telegram-Gruppe", "ich beantworte deine Fragen dienstags und donnerstags"],
      ["Aufzeichnungen der Live-Calls", "aus der ersten Runde, in der Gruppe"],
      ["Dauerhafter Zugriff", "auf alle Module"],
    ],
  },
  dpw: {
    name: "Digitale Produktwelt",
    link: "https://mumlifebalance.thrivecart.com/digitale-produktwelt/?coupon=DANKE199DPW",
    bild: "https://mumlifebalance.ch/wp-content/uploads/2026/10/digitale-produktwelt-mockup.jpg",
    bildAlt: "Kurs „Vom Network-Wissen zur digitalen Produktwelt“",
    punkte: [
      ["Dein eigenes Produkt neben dem Network", "vom Hybridmodell-Fundament bis zum Verkaufen ohne Druck"],
      ["Dein Produkt entwickeln und bauen", "Kurs, Workbook oder 0€-Produkt, Schritt für Schritt mit KI und Canva"],
      ["Verkaufen & automatisieren", "Storytelling, Preise, Checkout, E-Mail und Produkttreppe"],
      ["Worksheets und Vorlagen", "damit du nie vor einer leeren Seite sitzt"],
      ["Telegram-Gruppe", "ich beantworte deine Fragen dienstags und donnerstags"],
      ["Lebenslanger Zugang", "sofort verfügbar"],
    ],
  },
  ceo: {
    name: "Mama-CEO",
    link: "https://mumlifebalance.thrivecart.com/mama-ceo/?coupon=DANKE199CEO",
    bild: "https://mumlifebalance.ch/wp-content/uploads/2026/10/mama-ceo-mockup.jpg",
    bildAlt: "Mama-CEO: vom Zeit-Erschaffen bis zum Skalieren",
    punkte: [
      ["Zeit für dein Business, ohne dass die Familie zu kurz kommt", "vom Wochenrhythmus bis zum Plan fürs ganze Quartal"],
      ["Kurze Lektionen", "hörbar beim Spazieren"],
      ["Vorlagen für Cockpit-Bot und Familien-Bot", "mein eigener Auftrag, einfach nachgebaut"],
      ["Notion-Vorlage", "eine abgespeckte Kopie meines echten Workspaces"],
      ["Telegram-Gruppe", "ich beantworte deine Fragen dienstags und donnerstags"],
      ["Lebenslanger Zugang", "alle Inhalte und Updates bleiben deins"],
    ],
  },
};

// Je Funnel: Slug, Formular, was gerade passiert ist, und der eine Satz, der vom Freebie zum Kurs führt.
// „mail“ ist der Betreff der Bestätigungsmail (scripts/mails/bestaetigung-bauen.py) —
// so findet sie die richtige Mail im Postfach.
const SEITEN = [
  { slug: "danke-story-challenge", titel: "Danke – Story-Challenge", formular: 45, kurs: "ikm",
    mail: "Ein Klick noch, dann startet deine Story-Challenge",
    bruecke: "In der Story-Challenge baust du sieben Tage lang Storys, auf die jemand antwortet. In der Kundenmaschine machst du daraus eine Instagram-Routine, die bleibt: Storys, Beiträge und die Gespräche, aus denen Kundschaft und neue Teampartner werden." },
  { slug: "danke-starterguide", titel: "Danke – Instagram-Starterguide", formular: 53, kurs: "ikm",
    mail: "Ein Klick noch, dann kommt dein Instagram-Starterguide",
    bruecke: "Der Starterguide zeigt dir die ersten Schritte. In der Kundenmaschine gehst du den ganzen Weg: vom klaren Profil über Storys und Beiträge bis zu den Gesprächen, aus denen Kundschaft und neue Teampartner werden." },
  { slug: "danke-bio-check", titel: "Danke – Bio-Check", formular: 47, kurs: "ikm",
    mail: "Ein Klick noch, dann ist dein Bio-Check startklar 🌿",
    bruecke: "Deine Bio entscheidet, ob jemand auf deinem Profil bleibt. Was danach kommt, baust du in der Kundenmaschine: Inhalte, die Vertrauen aufbauen, und Gespräche, aus denen Kundschaft und neue Teampartner werden." },
  // Lead-Challenge führt seit 26.10.2026 auf die Produktwelt (November-Fokus Hybridmodell, Patricias Entscheid)
  { slug: "danke-lead-challenge", titel: "Danke – Lead-Challenge", formular: 51, kurs: "dpw",
    mail: "Ein Klick noch, dann bist du bei der Lead-Challenge dabei",
    bruecke: "Mit deinem Leadmagneten baust du dein erstes eigenes Produkt, gratis. In der Digitalen Produktwelt baust du die Treppe dahinter: ein Produkt, das du verkaufst, neben deinem Network, Schritt für Schritt mit KI und Canva." },
  // Businessfahrplan und Ideen-Finder führen aufs eigene Produkt (Patricias Entscheid 23.10.2026)
  { slug: "danke-businessfahrplan", titel: "Danke – Businessfahrplan", formular: 49, kurs: "dpw",
    mail: "Ein Klick noch, dann kommt dein Businessfahrplan",
    bruecke: "Der Fahrplan zeigt dir den Weg vom Produktposten zu einem Business, das dir gehört. In der Digitalen Produktwelt baust du den Kern davon: dein eigenes digitales Produkt neben deinem Network, Schritt für Schritt mit KI und Canva." },
  { slug: "danke-ideen-finder", titel: "Danke – Produkt-Ideen-Finder", formular: 66, kurs: "dpw",
    mail: "Ein Klick noch, dann startet dein Produkt-Ideen-Finder ✨",
    bruecke: "Der Ideen-Finder gibt dir die Idee. In der Digitalen Produktwelt machst du daraus ein Produkt, das sich verkauft: vom Workbook oder Kurs über den Checkout bis zu den Automationen, die verkaufen, während du offline bist." },
  { slug: "danke-von-0-auf-echt", titel: "Danke – Von 0 auf echt", formular: 41, kurs: "ikm",
    mail: "Ein Klick noch, dann kommt dein Workbook „Von 0 auf echt“",
    bruecke: "Wenn du weisst, wofür du stehst, fehlt noch ein Profil, das es zeigt. In der Kundenmaschine machst du daraus Inhalte, die Vertrauen aufbauen, und Gespräche, aus denen Kundschaft und neue Teampartner werden." },
  // Freischaufeln verschickt KEINE Bestätigungsmail — der Link kommt direkt.
  { slug: "danke-freischaufeln", titel: "Danke – Freischaufeln", formular: 62, kurs: "ceo",
    ohneBestaetigung: true, mail: "Dein Freischaufeln-Link ist da",
    bruecke: "Das Tool schafft dir heute ein erstes Zeitfenster. In Mama-CEO baust du daraus einen Wochenrhythmus, der mit Kindern funktioniert, und ein KI-Team, das dir den Adminkram abnimmt." },
];

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function schritte(s) {
  const liste = s.ohneBestaetigung
    ? [["Öffne dein Postfach", "In ein paar Minuten liegt dort eine Mail von info@mumlifebalance.ch."],
       ["Finde die Mail", `Sie heisst „${esc(s.mail)}“. Falls sie nicht im Posteingang ist, schau im Spam oder unter „Werbung“ nach.`],
       ["Leg los", "Ein Klick auf den Link in der Mail, und du kannst direkt anfangen."]]
    : [["Öffne dein Postfach", "Die Mail kommt von info@mumlifebalance.ch, meistens innerhalb von zwei Minuten."],
       ["Finde die Mail", `Sie heisst „${esc(s.mail)}“. Falls sie nicht im Posteingang ist, schau im Spam oder unter „Werbung“ nach.`],
       ["Klick auf den Knopf", "Erst mit diesem Klick bestätigst du deine Adresse, und erst dann kann ich dir alles schicken."]];
  return liste.map(([t, d], i) =>
    `<div class="pnum"><div class="n">${i + 1}</div><div><h3>${t}</h3><p>${d}</p></div></div>`).join("\n      ");
}

function seite(s) {
  const k = KURSE[s.kurs];
  const feats = k.punkte.map(([b, r]) =>
    `<div class="feat">${HAKEN}<span><b>${esc(b)}</b> — ${esc(r)}</span></div>`).join("\n          ");
  return `<!-- POSTFACH -->
<section class="bg-blush">
  <div class="wrap narrow" style="max-width:760px;">
    <div class="sec-head" style="margin-bottom:28px;"><span class="eyebrow">${s.ohneBestaetigung ? "Das hat geklappt" : "Fast geschafft"}</span><h1 style="font-size:clamp(34px,6vw,58px);margin-bottom:0;">${s.ohneBestaetigung ? "Dein Link ist unterwegs" : "Schau jetzt in dein Postfach"}</h1></div>
    <div class="promise">
      ${schritte(s)}
    </div>
  </div>
</section>

<!-- HALT, EINS NOCH -->
<section class="bg-white">
  <div class="wrap narrow" style="max-width:760px;">
    <div class="sec-head" style="margin-bottom:24px;"><span class="eyebrow">Halt, eins noch</span><h2 style="font-size:clamp(30px,5vw,52px);">Nur hier: ${esc(k.name)} für 199 statt 333&nbsp;CHF</h2></div>
    <p class="lead">${esc(s.bruecke)}</p>
    <img src="${k.bild}" alt="${esc(k.bildAlt)}" style="width:100%;max-width:620px;margin:28px auto 0;border-radius:14px;">
  </div>
</section>

<!-- PREIS -->
<section class="pricing2">
  <div class="wrap">
    <div class="ptiers" style="grid-template-columns:minmax(0,520px);justify-content:center;">
      <div class="ptier hot">
        <span class="rec">Nur hier</span>
        <div class="tt">${esc(k.name)}</div>
        <div class="pp">199 CHF</div>
        <div class="pm"><s>333 CHF</s> &middot; einmalig &middot; diesen Preis gibt es nur hier, direkt nach deiner Anmeldung</div>
        <div class="feats">
          ${feats}
        </div>
        <a href="${k.link}" class="btn btn-lg" style="width:100%;">Alles ansehen und für 199 CHF dabei sein &#8594;</a>
      </div>
    </div>
  </div>
</section>

<!-- AUSWEG -->
<section class="bg-blush">
  <div class="wrap narrow" style="text-align:center;max-width:680px;">
    <p class="lead">Kein Interesse? Völlig in Ordnung. Dann schau einfach in dein Postfach, deine Mail wartet schon.</p>
  </div>
</section>`;
}

const vorschau = process.argv.includes("--vorschau");
if (vorschau) fs.mkdirSync(VORSCHAU, { recursive: true });
const css = vorschau ? fs.readFileSync(path.join(HIER, "../../outputs/produkte/doterra-mama-energie/landingpage/customizer-css.txt"), "utf8") : "";

// --nur danke-lead-challenge[,…]: nur diese Seiten bauen, damit Änderungen in WordPress an den anderen bleiben
const nurIdx = process.argv.indexOf("--nur");
const nur = nurIdx > -1 ? process.argv[nurIdx + 1].split(",") : null;
if (nur) for (const n of nur) if (!SEITEN.some((s) => s.slug === n)) throw new Error(`Unbekannte Seite: ${n}`);

for (const s of SEITEN.filter((x) => !nur || nur.includes(x.slug))) {
  const inhalt = seite(s);
  for (const verboten of ["<style", "<script", '<link rel="stylesheet"', "@import"]) {
    if (inhalt.includes(verboten)) throw new Error(`ABBRUCH: "${verboten}" im Markup — das blockt die WAF.`);
  }
  if (vorschau) {
    fs.writeFileSync(path.join(VORSCHAU, `${s.slug}.html`), `<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(s.titel)}</title>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{margin:0}${css}</style></head><body><div class="enr">${inhalt}</div></body></html>`, "utf8");
    console.log("Vorschau:", s.slug);
    continue;
  }
  const block = `<!-- wp:html -->\n<div class="enr">\n${inhalt}\n</div>\n<!-- /wp:html -->`;
  const bestehend = await findPageBySlug(s.slug);
  const p = await createOrUpdatePage({ title: s.titel, slug: s.slug, content: block, ...(bestehend ? {} : { status: "draft" }) });
  await updatePage(p.id, { template: "elementor_canvas" });
  console.log(`✅ ${p.id} · /${s.slug}/ · ${p.status} · Formular ${s.formular}`);
}
