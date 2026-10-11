/* =============================================================
   Vercel API Route: /api/finder
   =============================================================
   Ein Endpunkt fuer alle drei Schritte des Formulars. Der Modus
   steht im Body, der passende Prompt liegt in lib/.

     modus "ideen"      -> 3 Produktideen            (lib/prompt-ideen.md)
     modus "titel"      -> ein neuer Name zur Idee   (lib/prompt-titel.md)
     modus "gliederung" -> das Inhaltsverzeichnis    (lib/prompt-gliederung.md)

   Vor JEDEN dieser Prompts kommt lib/wissen-produkterstellung.md —
   Patricias eigene Methode aus "Vom Networkwissen zur digitalen
   Produktwelt". Ohne die baut das Werkzeug allgemeine Marketing-Kurse
   statt Minikurse nach ihrer Struktur.

   Antwort immer: { daten: <geparstes JSON>, meta: {...} }

   Qualitaet laeuft in drei Stufen:
     1. der Prompt sagt, was eine gute Idee ausmacht
     2. lib/pruefen.js prueft in Code nach — Form, verbotene Sprache,
        erfundene Zahlen, fehlende Teile. Das ist die Stufe, die
        wirklich scheitert.
     3. findet Stufe 2 etwas, laeuft EIN Nachbesserungs-Durchgang mit
        den konkreten Beanstandungen. Wird es dabei nicht besser,
        bleibt der erste Entwurf.
   Was am Ende offen bleibt, steht in meta.offen und im Log.

   🚨 Ausdruecklich OHNE extended thinking. Beim Vorbild-Tool, das wir
   am 14.09. untersucht haben, laeuft das Denken mit: es frisst die
   Laufzeit der Funktion auf, und beim Browser kommt kein einziges
   text_delta an -> "Die KI hat keine lesbare Antwort geschickt."
   Hier wird nicht gedacht, sondern geantwortet.

   Environment:
   - ANTHROPIC_API_KEY (Pflicht)
   ============================================================= */

import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pruefeIdeen, pruefeGliederung } from '../lib/pruefen.js';
import { nachbessern } from '../lib/nachbessern.js';

export const config = { runtime: 'nodejs', maxDuration: 60 };

const __dirname = dirname(fileURLToPath(import.meta.url));

const MODI = {
  ideen:      { datei: 'prompt-ideen.md',      tokens: 3500, pruefer: pruefeIdeen },
  titel:      { datei: 'prompt-titel.md',      tokens: 500  },
  gliederung: { datei: 'prompt-gliederung.md', tokens: 6000, pruefer: pruefeGliederung },

  /* Eigener Aufruf nur zum Nachbessern — siehe unten. Die Datei ist
     dieselbe wie beim Erstentwurf, damit der Auftrag wieder danebensteht. */
  nachbessern: { tokens: 3500 },
};

const WISSEN = 'wissen-produkterstellung.md';
const NACHBESSERN = 'prompt-nachbessern.md';

const promptCache = new Map();

async function ladePrompt(datei) {
  if (promptCache.has(datei)) return promptCache.get(datei);
  const kandidaten = [
    join(process.cwd(), 'lib', datei),
    join(__dirname, '..', 'lib', datei),
    join(process.cwd(), 'scripts/produkt-ideen-finder-service/lib', datei),
  ];
  for (const pfad of kandidaten) {
    try {
      const inhalt = await readFile(pfad, 'utf-8');
      promptCache.set(datei, inhalt);
      return inhalt;
    } catch {
      /* naechster Pfad */
    }
  }
  throw new Error(`${datei} nicht gefunden — pruefe includeFiles in vercel.json`);
}

/* Schneidet aus der Antwort das JSON heraus. Faengt ab, wenn das Modell
   doch einen Code-Zaun oder einen Satz davorsetzt. */
function ausschneiden(text, erwartet) {
  const roh = String(text || '').trim().replace(/^```(?:json)?/i, '').replace(/```$/, '').trim();
  const auf = erwartet === 'array' ? '[' : '{';
  const zu  = erwartet === 'array' ? ']' : '}';
  const von = roh.indexOf(auf);
  const bis = roh.lastIndexOf(zu);
  if (von === -1 || bis <= von) throw new Error('keine verwertbare Antwort');
  return JSON.parse(roh.slice(von, bis + 1));
}

function auftrag(modus, b) {
  const thema = (b.thema || '').trim();
  const huerden = (b.herausforderungen || '').trim();
  const netzwerk = (b.network || '').trim();
  const basis =
    `Ihr Thema:\n${thema}\n\n` +
    (netzwerk ? `Ihr Network und ihr Produkt darin:\n${netzwerk}\n\n` : '') +
    (huerden ? `Die groessten Huerden ihrer Zielgruppe:\n${huerden}\n\n` : '');

  if (modus === 'ideen') return basis + 'Gib mir jetzt die drei Ideen als JSON.';

  if (modus === 'titel') {
    return basis + 'Die Idee, um die es geht:\n' + idee(b) +
      'Schreib genau einen neuen Namen samt Versprechen als JSON.';
  }

  return basis + 'Sie hat sich fuer diese Idee entschieden:\n' + idee(b) +
    'Bau daraus das Inhaltsverzeichnis als JSON.';
}

/* Faengt den Fall ab, dass das Modell statt { spiegel, ideen[] }
   nur das nackte Array schickt. */
function formen(daten, modus) {
  if (modus === 'ideen' && Array.isArray(daten)) return { spiegel: '', ideen: daten };
  return daten;
}

/* Fehlt das Wesentliche, wird nicht nachgebessert — dann war der
   Durchgang kaputt und die Frau bekommt lieber einen Hinweis. */
function vollstaendig(e, modus) {
  if (modus === 'ideen' && (!Array.isArray(e?.ideen) || !e.ideen.length)) {
    throw new Error('keine Ideen im Ergebnis');
  }
  if (modus === 'gliederung' && (!Array.isArray(e?.module) || !e.module.length)) {
    throw new Error('keine Module im Ergebnis');
  }
  if (modus === 'titel' && !String(e?.name || '').trim()) {
    throw new Error('kein Titel im Ergebnis');
  }
}

/* Die gewaehlte Idee, so wie Schritt 2 sie geliefert hat. */
function idee(b) {
  return (
    `Name: ${b.name || ''}\n` +
    `Versprechen: ${b.versprechen || ''}\n` +
    `Fuer wen: ${b.fuer_wen || ''}\n` +
    `Das eine Problem: ${b.problem || ''}\n` +
    `Ergebnis in den Haenden: ${b.ergebnis || ''}\n` +
    `Das Network-Produkt kommt so vor: ${b.network_baustein || ''}\n\n`
  );
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ fehler: 'Nur POST.' });

  const body = req.body || {};
  const modus = String(body.modus || 'ideen');
  const einstellung = MODI[modus];

  if (!einstellung) return res.status(400).json({ fehler: 'Unbekannter Schritt.' });
  if (!String(body.thema || '').trim()) {
    return res.status(400).json({ fehler: 'Schreib zuerst kurz, worueber du mehr weisst als andere.' });
  }

  const schluessel = process.env.ANTHROPIC_API_KEY;
  if (!schluessel) {
    console.error('ANTHROPIC_API_KEY fehlt');
    return res.status(500).json({ fehler: 'Das Werkzeug ist gerade nicht erreichbar. Melde dich bei Patricia.' });
  }

  const begonnen = Date.now();

  /* ---------------------------------------------------------------
     Nachbessern als eigener Aufruf
     ---------------------------------------------------------------
     🚨 Warum das noetig ist (gemessen live am 14.09.2026): Der erste
     Entwurf braucht 33 bis 39 Sekunden. maxDuration steht bei 60. Ein
     Reparatur-Durchgang braucht rund 10 — das passt rechnerisch, aber
     nur knapp, und im Live-Test ging es um eine Sekunde nicht mehr
     auf. Ergebnis: die Pruefung fand drei Maengel (zweimal das
     Network-Produkt als Aufhaenger, einmal "hilft bei"), und alle drei
     gingen ungefiltert raus.

     Deshalb holt die Seite die Reparatur jetzt in einem ZWEITEN Ruf
     mit eigenem Zeitbudget. Die Beanstandungen werden hier neu
     gerechnet, nicht vom Browser uebernommen — die Pruefung ist die
     einzige Instanz, die entscheidet, was ein Mangel ist. */
  if (modus === 'nachbessern') {
    const art = String(body.art || '');
    const pruefer = art === 'ideen' ? pruefeIdeen : art === 'gliederung' ? pruefeGliederung : null;
    if (!pruefer) return res.status(400).json({ fehler: 'Unbekannter Schritt.' });

    const entwurf = body.entwurf;
    if (!entwurf || typeof entwurf !== 'object') {
      return res.status(400).json({ fehler: 'Kein Entwurf zum Nachbessern.' });
    }

    try {
      vollstaendig(entwurf, art);
      const offen = pruefer(entwurf, body);
      if (!offen.length) {
        return res.status(200).json({ daten: entwurf, meta: { nachgebessert: false, offen: [] } });
      }

      const [fundament, anleitung] = await Promise.all([
        ladePrompt(WISSEN), ladePrompt(NACHBESSERN),
      ]);
      const system = `${fundament}\n\n---\n\n${anleitung}`;
      const client = new Anthropic({ apiKey: schluessel });

      const ergebnis = await nachbessern({
        claude: async (nachrichten, maxTokens) => {
          const a = await client.messages.create({
            model: 'claude-sonnet-4-5', max_tokens: maxTokens, system, messages: nachrichten,
          });
          if (a.stop_reason === 'max_tokens') throw new Error('Reparatur abgeschnitten');
          return a.content.filter((b) => b.type === 'text').map((b) => b.text).join('').trim();
        },
        modus: art, ergebnis: entwurf, beanstandet: offen,
        pruefer, eingabe: body,
        erstAuftrag: auftrag(art, body),
        tokens: einstellung.tokens,
        sekundenUebrig: 50,
      });

      console.log('Nachbessern:', {
        art, vorher: offen.length, nachher: ergebnis.beanstandet.length,
        uebernommen: ergebnis.nachgebessert, sekunden: ((Date.now() - begonnen) / 1000).toFixed(1),
      });

      return res.status(200).json({
        daten: ergebnis.ergebnis,
        meta: { nachgebessert: ergebnis.nachgebessert, offen: ergebnis.beanstandet },
      });
    } catch (err) {
      console.error('Nachbessern fehlgeschlagen:', err.message);
      /* Der Entwurf ist schon beim Browser — hier faellt nichts weg. */
      return res.status(200).json({ daten: entwurf, meta: { nachgebessert: false, offen: [] } });
    }
  }

  try {
    const [fundament, schritt] = await Promise.all([
      ladePrompt(WISSEN),
      ladePrompt(einstellung.datei),
    ]);
    const system = `${fundament}

---

${schritt}`;
    const client = new Anthropic({ apiKey: schluessel });

    /* Ein Ruf an Claude. Bei 5xx/429 bis zu dreimal. */
    async function rufen(nachrichten, versuch = 1) {
      try {
        const antwort = await client.messages.create({
          model: 'claude-sonnet-4-5',
          max_tokens: einstellung.tokens,
          system,
          messages: nachrichten,
        });
        if (antwort.stop_reason === 'max_tokens') {
          const e = new Error('Antwort abgeschnitten');
          e.abgeschnitten = true;
          throw e;
        }
        return antwort;
      } catch (err) {
        const voruebergehend =
          err.status >= 500 || err.status === 429 || err.name === 'APIConnectionError';
        if (voruebergehend && versuch < 3) {
          await new Promise((r) => setTimeout(r, versuch * 1500));
          return rufen(nachrichten, versuch + 1);
        }
        throw err;
      }
    }

    const nurText = (a) =>
      a.content.filter((b) => b.type === 'text').map((b) => b.text).join('').trim();

    /* --- Erster Entwurf --- */
    const erster = auftrag(modus, body);
    const antwort = await rufen([{ role: 'user', content: erster }]);
    const text = nurText(antwort);

    let ergebnis = formen(ausschneiden(text, 'objekt'), modus);
    vollstaendig(ergebnis, modus);

    /* --- Die Pruefung --- */
    let beanstandet = einstellung.pruefer ? einstellung.pruefer(ergebnis, body) : [];
    let nachgebessert = false;

    /* --- Nachbessern, wenn die Pruefung etwas gefunden hat ---
       Der Weg steckt in lib/nachbessern.js, damit er einzeln testbar
       ist. Genau EIN Durchgang: wer zweimal nachbessert, dreht sich im
       Kreis und laesst die Frau unnoetig warten.

       🚨 maxDuration steht bei 60 Sekunden, der erste Entwurf braucht
       gemessen 20 bis 36. Deshalb geht die Restzeit mit — reicht sie
       nicht, geht der erste Entwurf raus statt gar nichts. */
    const verbraucht = () => (Date.now() - begonnen) / 1000;

    if (beanstandet.length && einstellung.pruefer) {
      console.warn('Pruefung:', { modus, anzahl: beanstandet.length, punkte: beanstandet });

      const system2 = `${fundament}

---

${await ladePrompt(NACHBESSERN)}`;
      const ergebnis2 = await nachbessern({
        claude: async (nachrichten, maxTokens) => {
          const a = await client.messages.create({
            model: 'claude-sonnet-4-5', max_tokens: maxTokens,
            system: system2, messages: nachrichten,
          });
          if (a.stop_reason === 'max_tokens') throw new Error('Reparatur abgeschnitten');
          return nurText(a);
        },
        modus, ergebnis, beanstandet,
        pruefer: einstellung.pruefer,
        eingabe: body,
        erstAuftrag: erster,
        tokens: einstellung.tokens,
        sekundenUebrig: 50 - verbraucht(),
      });

      ergebnis = ergebnis2.ergebnis;
      beanstandet = ergebnis2.beanstandet;
      nachgebessert = ergebnis2.nachgebessert;
      if (!nachgebessert) console.warn('Nicht nachgebessert:', ergebnis2.grund);
    }

    if (beanstandet.length) {
      console.warn('Bleibt beanstandet:', { modus, punkte: beanstandet });
    }


    console.log('OK:', {
      modus,
      sekunden: verbraucht().toFixed(1),
      rein: antwort.usage?.input_tokens,
      raus: antwort.usage?.output_tokens,
      nachgebessert,
      offen: beanstandet.length,
    });

    return res.status(200).json({
      daten: ergebnis,
      meta: { nachgebessert, offen: beanstandet },
    });
  } catch (err) {
    console.error('Fehler:', { modus, name: err.name, message: err.message, status: err.status });
    if (err.abgeschnitten) {
      return res.status(502).json({
        fehler: 'Die Antwort kam nur halb an. Probier es gleich nochmal.',
        nochmal: true,
      });
    }
    const nochmal =
      err.status >= 500 || err.status === 429 ||
      err.name === 'APIConnectionError' || err.name === 'APITimeoutError' ||
      /verwertbare|Ideen|Module|Titel/.test(err.message);
    return res.status(nochmal ? 503 : 500).json({
      fehler: nochmal
        ? 'Das hat gerade nicht geklappt. Probier es nochmal — meistens geht es beim zweiten Mal.'
        : 'Da ist etwas schiefgelaufen. Melde dich bei Patricia, wenn es bleibt.',
      nochmal,
    });
  }
}
