/* Testfaelle fuer lib/nachbessern.js — Aufruf: node lib/nachbessern.test.mjs
   Laeuft OHNE Anthropic-Schluessel: "claude" ist hier eine Attrappe.
   Geprueft wird die Mechanik, nicht die Textqualitaet. */
import { nachbessern, nurEinzelne } from './nachbessern.js';
import { pruefeIdeen, pruefeGliederung } from './pruefen.js';

const EINGABE = { network: 'doTERRA, vor allem die aetherischen Oele' };

const gut = (n) => ({
  name: n, quelle: 'Geschichte',
  versprechen: 'Bau dir in drei Abenden eine Routine, die deine Kinder ohne Geschrei ins Bett bringt, ohne stundenlang zu suchen, auch wenn du bisher jeden Abend improvisierst.',
  fuer_wen: 'Mamas mit Kindern zwischen drei und acht Jahren, die abends nicht mehr können',
  problem: 'Es ist halb acht, die Kinder drehen auf, und sie hört sich schreien, obwohl sie es sich anders vorgenommen hatte.',
  ergebnis: 'einen ausgedruckten Ablaufplan für die letzten neunzig Minuten des Tages',
  network_baustein: 'Ein Tropfen auf dem Kissen gehört als kleines Ritual dazu.',
  erster_schritt: 'Schreib heute auf, an welcher Minute der Abend das erste Mal kippt.',
  beleg_check: 'Tipp „ins Bett" in die Chat-Suche. Mehr als drei Treffer aus zwei Monaten heisst: das Thema ist da.',
});

const entwurf = {
  spiegel: 'x',
  ideen: [
    gut('Abendfrieden'),
    { ...gut('Ölritual'), quelle: 'Expertise',
      ergebnis: 'drei Sätze, mit denen sie erzählt, wie sie Öle im Alltag nutzt' },
    { ...gut('Tagesanker'), quelle: 'Alltag' },
  ],
};

let fehler = 0;
const pruef = (name, bedingung, zusatz = '') => {
  console.log(`${bedingung ? '  OK  ' : '  FEHLT'}  ${name}${zusatz ? ' — ' + zusatz : ''}`);
  if (!bedingung) fehler++;
};

/* ---------- 1. Zuordnung der Beanstandungen ---------- */
console.log('\n1. Beanstandungen einer Idee zuordnen');
pruef('eine Idee betroffen',
  nurEinzelne(['Idee 2 ("x"): kaputt'], entwurf, 'ideen')?.treffer.size === 1);
pruef('globale Beanstandung sperrt die gezielte Reparatur',
  nurEinzelne(['Idee 2 ("x"): kaputt', 'Die drei Ideen kommen nicht aus drei Quellen.'], entwurf, 'ideen') === null);
pruef('Modul wird über seine Nummer gefunden, nicht über die Position',
  (() => {
    const g = { module: [{ nummer: 'Modul 0' }, { nummer: 'Modul 1' }, { nummer: 'Modul 6' }] };
    const e = nurEinzelne(['Modul 6 ("x"): Material fehlt.'], g, 'gliederung');
    return e?.feld === 'module' && [...e.treffer.keys()][0] === 2;
  })());
pruef('unbekanntes Modul sperrt die gezielte Reparatur',
  nurEinzelne(['Modul 9 ("x"): kaputt.'], { module: [{ nummer: 'Modul 0' }] }, 'gliederung') === null);

/* ---------- 2. Gezielte Reparatur ---------- */
console.log('\n2. Gezielte Reparatur');
const beanstandet = pruefeIdeen(entwurf, EINGABE);
pruef('Prüfung findet genau die kaputte Idee', beanstandet.length === 1,
  beanstandet[0]?.slice(0, 48) + '…');

let gesehen = null;
const r = await nachbessern({
  claude: async (n, maxTokens) => {
    gesehen = { auftrag: n[0].content, maxTokens };
    return JSON.stringify({ ideen: [{ ...gut('Abendanker'), quelle: 'Expertise' }] });
  },
  modus: 'ideen', ergebnis: entwurf, beanstandet,
  pruefer: pruefeIdeen, eingabe: EINGABE,
  erstAuftrag: 'Ihr Thema: …', tokens: 3500, sekundenUebrig: 40,
});

pruef('nur EINE Idee ging zurück', (gesehen.auftrag.match(/"name":/g) || []).length === 1);
pruef('kleineres Token-Budget für die kleine Reparatur', gesehen.maxTokens === 1600);
pruef('Beanstandung wurde auf "Idee 1" umnummeriert', /1\. Idee 1 \("Ölritual"\)/.test(gesehen.auftrag));
pruef('übernommen', r.nachgebessert === true);
pruef('danach sauber', r.beanstandet.length === 0);
pruef('reparierte Idee sitzt an Position 2', r.ergebnis.ideen[1].name === 'Abendanker');
pruef('die guten Ideen sind unverändert',
  r.ergebnis.ideen[0].name === 'Abendfrieden' && r.ergebnis.ideen[2].name === 'Tagesanker');
pruef('der erste Entwurf wurde nicht verändert', entwurf.ideen[1].name === 'Ölritual');

/* ---------- 3. Reparatur, die nichts besser macht ---------- */
console.log('\n3. Reparatur, die nichts besser macht');
const schlechter = await nachbessern({
  claude: async () => JSON.stringify({ ideen: [{ ...gut('Ölkurs'), quelle: 'Expertise', ergebnis: 'Öle im Alltag' }] }),
  modus: 'ideen', ergebnis: entwurf, beanstandet,
  pruefer: pruefeIdeen, eingabe: EINGABE,
  erstAuftrag: 'x', tokens: 3500, sekundenUebrig: 40,
});
pruef('wird verworfen', schlechter.nachgebessert === false, schlechter.grund);
pruef('erster Entwurf bleibt', schlechter.ergebnis.ideen[1].name === 'Ölritual');

/* ---------- 4. Zeit reicht nicht ---------- */
console.log('\n4. Zeit reicht nicht');
let gerufen = false;
const knapp = await nachbessern({
  claude: async () => { gerufen = true; return '{}'; },
  modus: 'ideen', ergebnis: entwurf, beanstandet,
  pruefer: pruefeIdeen, eingabe: EINGABE,
  erstAuftrag: 'x', tokens: 3500, sekundenUebrig: 5,
});
pruef('Claude wird gar nicht erst gerufen', gerufen === false);
pruef('Grund wird genannt', knapp.grund === 'zu wenig Zeit');

/* ---------- 5. Kaputte Antwort ---------- */
console.log('\n5. Kaputte Antwort vom Modell');
const kaputt = await nachbessern({
  claude: async () => 'Klar, hier bitte!',
  modus: 'ideen', ergebnis: entwurf, beanstandet,
  pruefer: pruefeIdeen, eingabe: EINGABE,
  erstAuftrag: 'x', tokens: 3500, sekundenUebrig: 40,
});
pruef('faellt sauber zurück', kaputt.nachgebessert === false && kaputt.ergebnis === entwurf, kaputt.grund);

/* ---------- 6. Gliederung: nur das kaputte Modul ---------- */
console.log('\n6. Inhaltsverzeichnis — nur das kaputte Modul');
const modul = (nr, titel, klammer, material) => ({
  nummer: `Modul ${nr}`, titel, klammer, material,
  lektionen: [{ nummer: `${nr}.1`, titel: 'Schreib deine drei Szenen auf' },
              { nummer: `${nr}.2`, titel: 'Markier die, die am häufigsten kommt' }],
});
const glied = {
  name: 'Abendfrieden',
  versprechen: 'Bau dir in drei Abenden eine Routine, ohne stundenlang zu suchen, auch wenn es bisher jeden Abend eskaliert.',
  ergebnis: 'einen ausgedruckten Ablaufplan für die letzten neunzig Minuten des Tages',
  fuer_wen: 'Mamas mit Kindern zwischen drei und acht Jahren',
  module: [
    modul(0, 'Willkommen', 'Ankommen und vorbereiten', 'Fahrplan zum Ausdrucken'),
    modul(1, 'Kein zweites Business', 'Warum das eine Ergänzung ist', 'Checkliste'),
    modul(2, 'Deine drei Szenen', 'Wo der Abend kippt', 'Arbeitsblatt'),
    modul(3, 'Der Ablauf', 'Vom Problem zum Plan', 'Vorlage'),
    modul(4, 'Der Notfallsatz', 'Was du sagst, wenn es trotzdem kippt', 'Karte'),
    modul(5, 'Wenn es nicht läuft', 'Zeitmangel und Zweifel', ''),
    modul(6, 'Dein nächster Schritt', 'Was jetzt kommt', 'Wochenplan'),
  ],
  abschluss: 'Du hast jetzt einen Plan, der zu euch passt.',
};
const gb = pruefeGliederung(glied);
pruef('Prüfung findet das fehlende Material', gb.length === 1, gb[0]?.slice(0, 52) + '…');

let gesehen2 = null;
const gr = await nachbessern({
  claude: async (n, maxTokens) => {
    gesehen2 = { auftrag: n[0].content, maxTokens };
    return JSON.stringify({
      module: [modul(5, 'Wenn es nicht läuft', 'Zeitmangel und Zweifel',
        'Entscheidungsbaum für die häufigsten Stolpersteine')],
    });
  },
  modus: 'gliederung', ergebnis: glied, beanstandet: gb,
  pruefer: pruefeGliederung, eingabe: {},
  erstAuftrag: 'x', tokens: 6000, sekundenUebrig: 20,
});
pruef('nur EIN Modul ging zurück', (gesehen2.auftrag.match(/"nummer": "Modul/g) || []).length === 1);
pruef('kleines Token-Budget', gesehen2.maxTokens === 1600);
pruef('übernommen', gr.nachgebessert === true, gr.grund || '');
pruef('danach sauber', gr.beanstandet.length === 0);
pruef('repariertes Modul sitzt an seiner Stelle', Boolean(gr.ergebnis.module[5].material));
pruef('die anderen Module sind unverändert',
  gr.ergebnis.module.length === 7 && gr.ergebnis.module[6].titel === 'Dein nächster Schritt');
pruef('für die grosse Reparatur hätten 20 Sekunden nicht gereicht', 20 < 26);

console.log(fehler ? `\n${fehler} Prüfung(en) fehlgeschlagen.` : '\nAlles grün.');
process.exit(fehler ? 1 : 0);
