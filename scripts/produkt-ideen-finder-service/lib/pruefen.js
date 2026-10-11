/* =============================================================
   Die Pruefung — was nicht durchkommt, geht nicht raus
   =============================================================
   Diese Datei entscheidet nicht "schoen oder nicht schoen".
   Sie prueft, was sich WIRKLICH pruefen laesst — Form, verbotene
   Sprache, erfundene Zahlen, fehlende Teile.

   Warum in Code und nicht im Prompt: Ein Modell, das seine eigene
   Arbeit bewertet, sagt fast immer "passt". Ein regulaerer Ausdruck
   nicht. Beim Content hat genau das den Unterschied gemacht —
   hook-pruefen.py fand 11 von 14 Hooks ohne Network-Anker, nachdem
   dieselben Hooks die Selbstpruefung bestanden hatten.

   Rueckgabe: Array von Klartext-Beschwerden. Leer = sauber.
   Jede Beschwerde ist so formuliert, dass das Modell im zweiten
   Durchgang genau weiss, was zu tun ist.
   ============================================================= */

/* ---------- Was nie drinstehen darf ---------- */

const HEILVERSPRECHEN =
  /\b(heilt|heilung|lindert|kuriert|therapiert|beseitigt|bek[äa]mpft|wirkt gegen|hilft gegen|hilft bei)\b/i;

const FACHWORT =
  /\b(Positionierung|Sichtbarkeit|Hybridmodell|Funnel|Onboarding|Journey|Framework|Blueprint|skalier\w*|Conversion|Leadmagnet|Freebie|Sales?[- ]?Page|Persona|Touchpoint)\b/i;

/* Zahlen, die wie ein Versprechen klingen. "20 Minuten" oder
   "drei Wochen" sind erlaubt — das ist ein Zeitrahmen, kein Ertrag. */
const ERFUNDENE_ZAHL =
  /\d[\d'.,]*\s*(%|Prozent|CHF|Franken|Fr\.|€|EUR|Euro|Kund(?:in|en)|Teilnehmer\w*|Follower)/i;

/* Die Seite setzt "Am Ende hast du:" selbst davor — steht es auch im
   Feld, liest es sich doppelt. */
const DOPPELTE_EINLEITUNG = /^(am ende|danach|zum schluss|nach dem kurs)/i;

/* Ergebnisse, die nichts in der Hand sind. */
const LUFTIGES_ERGEBNIS =
  /^(mehr |ein besseres |ein gutes |endlich )?(klarheit|selbstvertrauen|sicherheit|gefühl|mindset|motivation|leichtigkeit|fokus|struktur|ruhe)\b/i;

/* ---------- Kleine Helfer ---------- */

const txt = (v) => String(v == null ? '' : v).trim();

function woerter(s) {
  return txt(s).split(/\s+/).filter(Boolean).length;
}

/* Drei sehr kurze Saetze hintereinander = Stakkato. */
function stakkato(s) {
  const saetze = txt(s).split(/(?<=[.!?])\s+/).filter(Boolean);
  let kurz = 0;
  for (const satz of saetze) {
    kurz = woerter(satz) <= 4 ? kurz + 1 : 0;
    if (kurz >= 3) return true;
  }
  return false;
}

/* Umlaute ausschreiben, damit "Öl" und "Oele" denselben Stamm ergeben. */
function glatt(s) {
  return txt(s).toLowerCase()
    .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss');
}

/* Woerter, die im Network-Feld stehen, aber nichts benennen. */
const FUELLWORT = new Set([
  'vor', 'allem', 'die', 'der', 'das', 'den', 'dem', 'und', 'oder', 'mit', 'bei',
  'von', 'im', 'in', 'fuer', 'aus', 'meine', 'mein', 'meinem', 'als', 'auch',
  'produkt', 'produkte', 'produkten', 'firma', 'network', 'marketing', 'team',
  'seit', 'jahren', 'partnerin', 'beraterin', 'vertrieb',
]);

/* Macht aus dem Network-Feld Wortstaemme, die im Kursnamen nichts
   verloren haben. "doTERRA, vor allem die aetherischen Oele"
   -> ["doterra", "aetherisch", "oel"]

   Warum der Stamm und nicht das ganze Wort: Der erste echte Durchlauf
   lieferte eine Idee namens "Oelritual" bei Network "aetherische Oele".
   Das ist das Produkt als Aufhaenger — und es rutschte durch, weil nur
   auf "doTERRA" geprueft wurde. */
function staemme(network) {
  return glatt(network)
    .split(/[^a-z0-9]+/)
    .filter((w) => w.length >= 3 && !FUELLWORT.has(w))
    .map((w) => w.replace(/(en|er|es|em|n|e|s)$/, ''))
    .filter((w) => w.length >= 3);
}

/* Alle Texte eines Objekts als ein String — fuer die Sprachpruefung. */
function allerText(o) {
  return Object.values(o || {})
    .flatMap((v) => (Array.isArray(v) ? v.map(allerText) : [txt(v)]))
    .join(' \n ');
}

/* Sprachregeln, die ueberall gelten. */
function sprache(text, wo, raus) {
  if (text.includes('ß')) raus.push(`${wo}: enthält ein ß. Patricia schreibt Schweizer ss.`);
  if (HEILVERSPRECHEN.test(text)) {
    raus.push(
      `${wo}: enthält ein Heilversprechen ("${text.match(HEILVERSPRECHEN)[0]}"). ` +
      `Ein Network-Produkt ist ein Ritual oder ein Schritt — nie ein Mittel gegen etwas. Umformulieren.`
    );
  }
  if (FACHWORT.test(text)) {
    raus.push(
      `${wo}: enthält das Fachwort "${text.match(FACHWORT)[0]}". ` +
      `Ersetzen durch das, was sie danach tatsächlich hat.`
    );
  }
  if (ERFUNDENE_ZAHL.test(text)) {
    raus.push(
      `${wo}: enthält eine erfundene Zahl ("${text.match(ERFUNDENE_ZAHL)[0]}"). ` +
      `Zahlen nur als Zeitrahmen, nie als Ertrag oder Menge. Streichen.`
    );
  }
  if (stakkato(text)) {
    raus.push(`${wo}: drei sehr kurze Sätze hintereinander. Zu ganzen Sätzen verbinden.`);
  }
}

/* ---------- Schritt 2: die drei Ideen ---------- */

export function pruefeIdeen(ergebnis, eingabe = {}) {
  const raus = [];
  const ideen = Array.isArray(ergebnis?.ideen) ? ergebnis.ideen : [];

  if (ideen.length !== 3) raus.push(`Es müssen genau drei Ideen sein, es sind ${ideen.length}.`);

  const quellen = new Set();
  const namen = new Set();
  const verboten = staemme(eingabe.network);

  ideen.forEach((idee, i) => {
    const wo = `Idee ${i + 1} ("${txt(idee.name) || 'ohne Namen'}")`;

    /* --- Name --- */
    const n = txt(idee.name);
    if (!n) raus.push(`${wo}: hat keinen Namen.`);
    else if (woerter(n) > 3) raus.push(`${wo}: der Name hat ${woerter(n)} Wörter. Höchstens drei.`);
    if (n && namen.has(n.toLowerCase())) raus.push(`${wo}: dieser Name kommt zweimal vor.`);
    namen.add(n.toLowerCase());

    /* --- Versprechen: die Formel muss vollständig sein --- */
    const v = txt(idee.versprechen);
    if (!v) {
      raus.push(`${wo}: das Versprechen fehlt.`);
    } else {
      if (!/\bohne\b/i.test(v)) {
        raus.push(`${wo}: im Versprechen fehlt der Teil "ohne …" — was sie dabei NICHT tun muss.`);
      }
      if (!/auch wenn\b/i.test(v)) {
        raus.push(`${wo}: im Versprechen fehlt der Teil "auch wenn …" — ihr echter Einwand.`);
      }
      if (woerter(v) < 12) raus.push(`${wo}: das Versprechen ist zu knapp für die Formel.`);
    }

    /* --- Inhalt --- */
    if (woerter(idee.fuer_wen) < 5) {
      raus.push(`${wo}: "für wen" ist zu allgemein. Eine konkrete Person beschreiben, kein Publikum.`);
    }
    if (woerter(idee.problem) < 8) {
      raus.push(`${wo}: das Problem ist keine Szene, sondern ein Stichwort. Beschreib den Moment.`);
    }
    const e = txt(idee.ergebnis);
    if (!e) raus.push(`${wo}: das Ergebnis fehlt.`);
    else if (LUFTIGES_ERGEBNIS.test(e)) {
      raus.push(
        `${wo}: das Ergebnis ist ein Gefühl ("${e.slice(0, 40)}…"), nichts in der Hand. ` +
        `Nenn etwas Anfassbares — ein ausgefüllter Plan, ein geschriebener Satz, eine Routine, die läuft.`
      );
    } else if (DOPPELTE_EINLEITUNG.test(e)) {
      raus.push(
        `${wo}: das Ergebnis fängt mit "${e.split(/\s+/).slice(0, 3).join(' ')}…" an. ` +
        `Nur das Ding selbst nennen — die Seite setzt die Einleitung selbst davor.`
      );
    }
    if (!txt(idee.erster_schritt)) raus.push(`${wo}: der erste Schritt fehlt.`);
    if (!txt(idee.beleg_check)) {
      raus.push(`${wo}: es fehlt, wie sie prüft, ob das Thema wirklich gefragt ist.`);
    }

    /* --- Das Network-Produkt darf nicht der Hauptdarsteller sein ---
       Geprüft wird der Wortstamm, nicht das ganze Wort: "Ölritual"
       enthält "oel" und fällt damit auf, obwohl die Firma nicht
       dasteht. Geprüft werden Name, Versprechen und das Ergebnis —
       an diesen drei Stellen entscheidet sich, worum der Kurs geht. */
    const schaufenster = glatt(`${n} ${v} ${txt(idee.ergebnis)}`);
    const treffer = verboten.find((s) => schaufenster.includes(s));
    if (treffer) {
      raus.push(
        `${wo}: "${treffer}…" steht im Namen, im Versprechen oder im Ergebnis — das ist ihr ` +
        `Network-Produkt. Es ist ein Baustein in der Lösung, nie der Aufhänger des Kurses. ` +
        `Der Kurs löst das Problem, das VOR dem Produkt kommt. Umbauen.`
      );
    }

    quellen.add(txt(idee.quelle).toLowerCase());
    sprache(allerText(idee), wo, raus);
  });

  if (ideen.length === 3 && quellen.size < 3) {
    raus.push(
      'Die drei Ideen kommen nicht aus drei verschiedenen Quellen. ' +
      'Eine aus ihrer Geschichte, eine aus ihrer Expertise, eine aus dem Alltag ihrer Leute.'
    );
  }

  return raus;
}

/* ---------- Schritt 3: das Inhaltsverzeichnis ---------- */

export function pruefeGliederung(g) {
  const raus = [];
  const module = Array.isArray(g?.module) ? g.module : [];

  if (module.length < 6 || module.length > 8) {
    raus.push(`Es müssen sechs bis acht Module sein, es sind ${module.length}.`);
  }

  const alleTitel = module.map((m) => `${txt(m.nummer)} ${txt(m.titel)} ${txt(m.klammer)}`).join(' | ');

  if (!/willkommen|ankommen|start/i.test(txt(module[0]?.titel) + txt(module[0]?.klammer))) {
    raus.push('Das erste Modul ist kein Willkommen-Modul. Modul 0 heisst Willkommen und bereitet vor.');
  }
  if (!/nicht l[äa]uft|nicht klappt|stolper|blockad|zweifel|dazwischenkommt/i.test(alleTitel)) {
    raus.push(
      'Es fehlt das Modul "Wenn es nicht läuft" — Zeitmangel, Zweifel, Blockaden, ' +
      'mit einem Notplan für genau die Hürden, die sie genannt hat.'
    );
  }
  if (!/n[äa]chster schritt|wie es weitergeht|danach/i.test(alleTitel)) {
    raus.push('Es fehlt das letzte Modul "Dein nächster Schritt" mit dem Plan für die nächsten sieben Tage.');
  }

  const e = txt(g?.ergebnis);
  if (!e) raus.push('Das Ergebnis des Kurses fehlt.');
  else if (LUFTIGES_ERGEBNIS.test(e)) {
    raus.push(`Das Kurs-Ergebnis ist ein Gefühl, nichts in der Hand: "${e.slice(0, 50)}…". Etwas Anfassbares nennen.`);
  } else if (DOPPELTE_EINLEITUNG.test(e)) {
    raus.push(
      `Das Kurs-Ergebnis fängt mit "${e.split(/\s+/).slice(0, 3).join(' ')}…" an. ` +
      `Nur das Ding selbst nennen — die Seite setzt "Am Ende hast du:" selbst davor.`
    );
  }

  const v = txt(g?.versprechen);
  if (v && (!/\bohne\b/i.test(v) || !/auch wenn\b/i.test(v))) {
    raus.push('Im Kurs-Versprechen fehlt "ohne …" oder "auch wenn …". Die Formel muss vollständig sein.');
  }

  module.forEach((m, i) => {
    const wo = `${txt(m.nummer) || `Modul ${i}`} ("${txt(m.titel)}")`;
    const lekt = Array.isArray(m.lektionen) ? m.lektionen : [];
    /* Die erwartete Lektionsnummer kommt aus der Modulnummer selbst,
       nicht aus der Position — sonst meckert die Pruefung, sobald ein
       Modul bewusst anders nummeriert ist. */
    const modulZahl = (txt(m.nummer).match(/\d+/) || [String(i)])[0];

    if (lekt.length < 2 || lekt.length > 4) {
      raus.push(`${wo}: hat ${lekt.length} Lektionen. Es müssen zwei bis vier sein.`);
    }
    if (!txt(m.titel)) raus.push(`${wo}: hat keinen Titel.`);
    if (!txt(m.klammer)) raus.push(`${wo}: die Klammer dahinter fehlt.`);
    if (!txt(m.material) && i < module.length - 1) {
      raus.push(`${wo}: es fehlt das Material — ein Arbeitsblatt, eine Vorlage, eine Checkliste.`);
    }

    lekt.forEach((l, k) => {
      const lt = typeof l === 'string' ? l : txt(l?.titel);
      const ln = typeof l === 'string' ? '' : txt(l?.nummer);
      if (!lt) raus.push(`${wo}, Lektion ${k + 1}: hat keinen Titel.`);
      if (/^(einführung|einleitung|grundlagen|basics|überblick|theorie)$/i.test(lt)) {
        raus.push(`${wo}, Lektion "${lt}": das ist eine Überschrift, kein Handgriff. Sag, was sie hier tut.`);
      }
      if (ln && !ln.startsWith(`${modulZahl}.`)) {
        raus.push(
          `${wo}, Lektion "${lt}": die Nummer "${ln}" passt nicht zum Modul. ` +
          `Sie muss mit "${modulZahl}." beginnen.`
        );
      }
    });
  });

  sprache(allerText(g), 'Das Inhaltsverzeichnis', raus);
  return raus;
}
