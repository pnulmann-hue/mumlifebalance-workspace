/* =============================================================
   Der Reparatur-Durchgang
   =============================================================
   Bekommt den Entwurf und die Beanstandungen aus lib/pruefen.js und
   schickt beides ein zweites Mal zu Claude.

   Zwei Regeln, die den Unterschied machen:

   1. So klein wie moeglich. Betreffen alle Beanstandungen einzelne
      Ideen, geht auch nur die eine kaputte Idee zurueck — das dauert
      ein paar Sekunden statt einer halben Minute und kann die guten
      Ideen nicht kaputtmachen.

   2. Nur uebernehmen, wenn es besser wurde. Kommt die Reparatur mit
      gleich vielen oder mehr Beanstandungen zurueck, bleibt der erste
      Entwurf stehen.

   Liegt in einer eigenen Datei, damit sich der Weg testen laesst,
   ohne die ganze Route aufzurufen: lib/nachbessern.test.mjs
   ============================================================= */

/* Jede Beanstandung nennt vorn ihre Stelle — "Idee 2 (…)" oder
   "Modul 6 (…)". Laesst sich jede einer Stelle zuordnen, wird gezielt
   repariert. Eine Beanstandung ohne Stelle ("die drei Quellen stimmen
   nicht", "es müssen sechs bis acht Module sein") betrifft das Ganze —
   dann geht alles zusammen zurueck.

   @returns {{feld: string, treffer: Map<number, string[]>}|null} */
export function nurEinzelne(beanstandet, ergebnis, modus) {
  const feld = modus === 'ideen' ? 'ideen' : 'module';
  const liste = Array.isArray(ergebnis?.[feld]) ? ergebnis[feld] : [];
  if (!liste.length) return null;

  const treffer = new Map();
  for (const b of beanstandet) {
    let i = -1;
    if (modus === 'ideen') {
      const m = b.match(/^Idee (\d+)/);
      if (m) i = Number(m[1]) - 1;
    } else {
      /* Beim Inhaltsverzeichnis steht die Modulnummer im Klartext
         davor — ueber sie wird die Stelle gesucht, nicht ueber die
         Position, denn die muss nicht uebereinstimmen. */
      const m = b.match(/^(Modul \d+)/);
      if (m) i = liste.findIndex((x) => String(x?.nummer || '').trim() === m[1]);
    }
    if (i < 0 || i >= liste.length) return null;
    if (!treffer.has(i)) treffer.set(i, []);
    treffer.get(i).push(b);
  }
  return treffer.size ? { feld, treffer } : null;
}

/* Schneidet aus der Antwort das JSON heraus. */
export function ausschneiden(text) {
  const roh = String(text || '').trim().replace(/^```(?:json)?/i, '').replace(/```$/, '').trim();
  const von = roh.indexOf('{');
  const bis = roh.lastIndexOf('}');
  if (von === -1 || bis <= von) throw new Error('keine verwertbare Antwort');
  return JSON.parse(roh.slice(von, bis + 1));
}

/**
 * @returns {{ergebnis, beanstandet, nachgebessert, grund?}}
 *   ergebnis      der bessere von beiden Entwuerfen
 *   beanstandet   was danach noch offen ist
 *   nachgebessert ob die Reparatur uebernommen wurde
 *   grund         warum nicht, falls nicht
 */
export async function nachbessern({
  claude,          // async (nachrichten, maxTokens) => Text
  modus,
  ergebnis,
  beanstandet,
  pruefer,
  eingabe,
  erstAuftrag,     // der urspruengliche Auftragstext
  tokens,          // max_tokens fuer die grosse Reparatur
  sekundenUebrig,  // wie viel Zeit die Funktion noch hat
}) {
  const einzelne = nurEinzelne(beanstandet, ergebnis, modus);
  const noetig = einzelne ? 12 : 26;

  if (sekundenUebrig < noetig) {
    return { ergebnis, beanstandet, nachgebessert: false, grund: 'zu wenig Zeit' };
  }

  const feld = einzelne?.feld;
  const stellen = einzelne ? [...einzelne.treffer.keys()] : null;
  const wort = feld === 'ideen' ? 'Idee' : 'Modul';
  const entwurf = einzelne ? { [feld]: stellen.map((i) => ergebnis[feld][i]) } : ergebnis;

  /* Bei den Ideen wird auf den kleinen Ausschnitt umnummeriert; die
     Modulnummern bleiben, weil sie inhaltlich gemeint sind. */
  const punkte = einzelne
    ? stellen.flatMap((i, k) =>
        einzelne.treffer.get(i).map((b) =>
          feld === 'ideen' ? b.replace(/^Idee \d+/, `Idee ${k + 1}`) : b))
    : beanstandet;

  const auftrag =
    `${erstAuftrag}\n\n---\n\n` +
    (einzelne
      ? `Von deinem Entwurf ${stellen.length === 1 ? `ist nur ${wort === 'Idee' ? 'diese eine Idee' : 'dieses eine Modul'}` : `sind nur diese ${wort === 'Idee' ? 'Ideen' : 'Module'}`} ` +
        `betroffen. Schick ${stellen.length === 1 ? 'genau das zurück' : 'genau die zurück'}, in derselben ` +
        `Reihenfolge, als { "${feld}": [ … ] } mit allen Feldern. Alles andere bleibt, wie es ist.\n\n`
      : '') +
    `DEIN ENTWURF:\n${JSON.stringify(entwurf, null, 1)}\n\n` +
    `---\n\nDIE BEANSTANDUNGEN:\n` +
    punkte.map((b, i) => `${i + 1}. ${b}`).join('\n') +
    `\n\nSchick den korrigierten Entwurf als JSON zurück.`;

  try {
    const text = await claude([{ role: 'user', content: auftrag }], einzelne ? 1600 : tokens);
    const zurueck = ausschneiden(text);

    let verbessert;
    if (einzelne) {
      const neu = Array.isArray(zurueck?.[feld]) ? zurueck[feld] : null;
      if (!neu || neu.length !== stellen.length) throw new Error('Reparatur passt nicht zum Ausschnitt');
      verbessert = { ...ergebnis, [feld]: [...ergebnis[feld]] };
      stellen.forEach((i, k) => { verbessert[feld][i] = neu[k]; });
    } else {
      verbessert = Array.isArray(zurueck) ? { spiegel: '', ideen: zurueck } : zurueck;
    }

    const uebrig = pruefer(verbessert, eingabe);
    if (uebrig.length >= beanstandet.length) {
      return { ergebnis, beanstandet, nachgebessert: false, grund: 'nicht besser geworden' };
    }
    return { ergebnis: verbessert, beanstandet: uebrig, nachgebessert: true };
  } catch (err) {
    /* Nachbessern ist Kuer. Faellt es aus, geht der erste Entwurf raus. */
    return { ergebnis, beanstandet, nachgebessert: false, grund: err.message };
  }
}
