/* Testfaelle fuer lib/pruefen.js — Aufruf: node lib/pruefen.test.mjs
   Der gute Entwurf MUSS 0 Beanstandungen haben. Kommt dort etwas,
   ist die Pruefung zu streng geworden und wirft gute Ideen weg. */
import { pruefeIdeen, pruefeGliederung } from './pruefen.js';

/* --- 1. Absichtlich schlecht: genau das, was so ein Werkzeug sonst ausspuckt --- */
const schlecht = {
  spiegel: 'Toll!',
  ideen: [
    { name: 'Der grosse Klarheits-Kurs für Mamas', quelle: 'Geschichte',
      versprechen: 'Finde deine Positionierung.',
      fuer_wen: 'gestresste Frauen',
      problem: 'Zeitmangel',
      ergebnis: 'mehr Klarheit über dein Thema',
      network_baustein: 'Das Öl hilft gegen ihre Erschöpfung.',
      erster_schritt: 'Fang an.', beleg_check: '' },
    { name: 'Ölkurs', quelle: 'Geschichte',
      versprechen: 'Verdiene 2000 CHF im Monat mit deinem Wissen, ohne Stress, auch wenn du wenig Zeit hast.',
      fuer_wen: 'Mamas', problem: 'Sie will mehr.', ergebnis: 'ein Plan',
      network_baustein: 'doTERRA', erster_schritt: 'Los.', beleg_check: 'Frag deine Zielgruppe.' },
    { name: 'doTERRA Starter', quelle: 'Geschichte',
      versprechen: 'Mehr Ruhe. Mehr Zeit. Mehr Geld.',
      fuer_wen: 'alle', problem: 'Stress', ergebnis: 'Selbstvertrauen',
      network_baustein: 'Öle', erster_schritt: 'Mach.', beleg_check: 'Schau mal.' },
  ],
};

/* --- 2. Gut: die Ideen aus dem Vorschau-Test --- */
const gut = {
  spiegel: 'Du weisst, wie ein Abend kippt.',
  ideen: [
    { name: 'Kursfunke', quelle: 'Geschichte',
      versprechen: 'Finde in 20 Minuten dein erstes verkaufbares Kursthema, ohne stundenlang zu grübeln, auch wenn du bisher nur dein Networkprodukt kennst.',
      fuer_wen: 'Mamas im Network, die neben dem Team was Eigenes wollen, ohne auszusteigen',
      problem: 'Sie sitzt abends vor dem Handy, scrollt durch die Kurse von anderen und denkt, sie hätte selbst nichts, worauf jemand warten würde.',
      ergebnis: 'einen aufgeschriebenen Satz, der sagt, wem sie wobei hilft',
      network_baustein: 'Ihr Produkt kommt als der Schritt vor, der nach dem Thema dran ist.',
      erster_schritt: 'Geh in die Suche deiner Chats und tipp „wie machst du" ein.',
      beleg_check: 'Tipp „wie machst du" in die Chat-Suche. Mehr als drei Treffer aus drei Monaten heisst: das Thema ist da.' },
    { name: 'Mama-Sprint', quelle: 'Expertise',
      versprechen: 'Bau dir an einem Nachmittag deinen ersten Mini-Onlinekurs, ohne ein neues Business zu starten, auch wenn deine Zeit knapp ist.',
      fuer_wen: 'Frauen, die ihr Wissen schon zwanzig Mal per Sprachnachricht verschenkt haben',
      problem: 'Sie erklärt dasselbe zum fünften Mal im Chat und denkt jedes Mal, das müsste man aufschreiben.',
      ergebnis: 'das fertige Gerüst ihres ersten Minikurses',
      network_baustein: 'Eine Lektion zeigt, wie ihr Produkt im Alltag vorkommt — als Ritual.',
      erster_schritt: 'Stell den Timer auf zehn Minuten und schreib auf, was du erklärt hast.',
      beleg_check: 'Frag in der Story „Wer hat mich diesen Monat um Tipps gefragt?" mit Ja-Nein-Sticker.' },
    { name: 'Abendanker', quelle: 'Alltag',
      versprechen: 'Bring deinen Abend in eine Reihenfolge, an die sich alle halten, in einer Woche, ohne Erziehungsprogramm, auch wenn es bisher jeden Tag anders läuft.',
      fuer_wen: 'Mamas mit Kindern im Kindergartenalter, die ab halb sieben nur noch funktionieren',
      problem: 'Um sieben ist die Luft raus, die Kinder drehen auf, und sie hört sich schreien.',
      ergebnis: 'einen aufgeschriebenen Abendablauf, der drei Wochen gelaufen ist',
      network_baustein: 'Ein Duft, der jeden Abend am gleichen Punkt dazugehört.',
      erster_schritt: 'Schreib auf, an welcher Minute der Abend das erste Mal kippt.',
      beleg_check: 'Frag in der Story „Kippt bei euch der Abend auch immer zur gleichen Zeit?" — mehr als zehn Ja heisst weitermachen.' },
  ],
};

function zeig(titel, punkte) {
  console.log(`\n${'='.repeat(64)}\n${titel}: ${punkte.length} Beanstandungen\n${'='.repeat(64)}`);
  punkte.forEach((p, i) => console.log(` ${i + 1}. ${p}`));
  if (!punkte.length) console.log(' (sauber)');
}

zeig('SCHLECHTER ENTWURF', pruefeIdeen(schlecht, { network: 'doTERRA, ätherische Öle' }));

/* --- Der echte Fall vom 14.09.: Produkt als Aufhänger, Firma taucht nirgends auf.
   Die alte Prüfung liess das durch, weil sie nur nach "doTERRA" suchte. --- */
const oelfalle = {
  spiegel: 'x',
  ideen: [
    { ...gut.ideen[0] },
    { ...gut.ideen[1], name: 'Ölritual',
      ergebnis: 'drei ausformulierte Sätze, mit denen sie anderen Mamas erzählt, wie sie Öle im Alltag nutzt' },
    { ...gut.ideen[2] },
  ],
};
zeig('GUTER ENTWURF', pruefeIdeen(gut, { network: 'doTERRA, ätherische Öle' }));
zeig('PRODUKT ALS AUFHÄNGER', pruefeIdeen(oelfalle, { network: 'doTERRA, vor allem die aetherischen Oele' }));
zeig('OHNE NETWORK-ANGABE (darf nichts finden)', pruefeIdeen(gut, {}));

/* --- 3. Gliederung: einmal kaputt --- */
zeig('GLIEDERUNG KAPUTT', pruefeGliederung({
  name: 'Kurs', versprechen: 'Mach was.', ergebnis: 'mehr Klarheit',
  module: [
    { nummer: 'Modul 1', titel: 'Grundlagen', klammer: '', lektionen: [{ nummer: '3.1', titel: 'Einführung' }], material: '' },
    { nummer: 'Modul 2', titel: 'Vertiefung', klammer: 'mehr davon', lektionen: [{ nummer: '2.1', titel: 'Noch mehr' }, { nummer: '2.2', titel: 'Und mehr' }], material: 'Blatt' },
  ],
}));
