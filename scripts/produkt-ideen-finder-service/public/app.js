/* =============================================================
   Produkt-Ideen-Finder — Formular in drei Schritten
   =============================================================
   Dein Thema  ->  Deine Ideen  ->  Inhaltsverzeichnis

   Alles laeuft ueber /api/finder, der Modus steht im Body.
   ============================================================= */

/* ⬇️⬇️⬇️  PATRICIA: hier der echte ThriveCart-Link des 39er-Kurses  ⬇️⬇️⬇️ */
const KURS_LINK = 'https://mumlifebalance.thrivecart.com/eigene-produkterstellung/';

const $ = (w) => document.querySelector(w);

const thema        = $('#thema');
const network      = $('#network');
const huerden      = $('#huerden');
const los          = $('#los');
const fehlerPlatz  = $('#fehler');

const tafelEingabe    = $('#tafel-eingabe');
const tafelWarten     = $('#tafel-warten');
const tafelIdeen      = $('#tafel-ideen');
const tafelGliederung = $('#tafel-gliederung');

const wartenText = $('#warten-text');
const spiegel    = $('#spiegel');
const karten     = $('#karten');

const gTitel     = $('#gliederung-titel');
const gVerspr    = $('#gliederung-versprechen');
const gErgebnis  = $('#gliederung-ergebnis');
const gModule    = $('#module');
const gAbschluss = $('#gliederung-abschluss');

let ideen = [];
let gliederungAlsText = '';

$('#angebot-link').href = KURS_LINK;

/* ---------- Kleinkram ---------- */

const schlafen = (ms) => new Promise((r) => setTimeout(r, ms));

function sicher(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function zeigeSchritt(n) {
  document.querySelectorAll('.schritt').forEach((el) => {
    el.classList.toggle('is-aktiv', Number(el.dataset.schritt) === n);
    el.classList.toggle('is-erledigt', Number(el.dataset.schritt) < n);
  });
}

function nurZeigen(tafel) {
  [tafelEingabe, tafelWarten, tafelIdeen, tafelGliederung].forEach((t) => {
    t.hidden = t !== tafel;
  });
}

function fehlerZeigen(text) {
  fehlerPlatz.innerHTML = `<p class="fehler">⚠️ ${sicher(text)}</p>`;
}
function fehlerWeg() {
  fehlerPlatz.innerHTML = '';
}

function nachOben() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* Wechselnde Zeilen waehrend des Wartens. */
let wartenTakt = null;
function wartenStarten(zeilen) {
  let i = 0;
  wartenText.textContent = zeilen[0];
  wartenTakt = setInterval(() => {
    i = (i + 1) % zeilen.length;
    wartenText.textContent = zeilen[i];
  }, 2200);
}
function wartenStoppen() {
  if (wartenTakt) clearInterval(wartenTakt);
  wartenTakt = null;
}

/* Was bei jedem Schritt mitgeht. */
function grunddaten() {
  return {
    thema: thema.value.trim(),
    network: network.value.trim(),
    herausforderungen: huerden.value.trim(),
  };
}

/* Die gewaehlte Idee, in der Form, die api/finder.js erwartet. */
function ideeDaten(i) {
  return {
    name: i.name,
    versprechen: i.versprechen,
    fuer_wen: i.fuer_wen,
    problem: i.problem,
    ergebnis: i.ergebnis,
    network_baustein: i.network_baustein,
  };
}

/* ---------- Der Ruf an den Server ---------- */

let letzteMeta = null;

async function rufen(body, versuche = 2) {
  let letzter = null;
  letzteMeta = null;
  for (let v = 1; v <= versuche; v++) {
    try {
      const antwort = await fetch('/api/finder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      let inhalt = null;
      try { inhalt = await antwort.json(); } catch { /* kein JSON zurueck */ }

      if (antwort.ok && inhalt && inhalt.daten) {
        letzteMeta = inhalt.meta || null;
        return inhalt.daten;
      }

      const meldung = (inhalt && inhalt.fehler) ||
        'Das hat gerade nicht geklappt. Probier es nochmal.';
      const nochmal = Boolean(inhalt && inhalt.nochmal) || antwort.status >= 500;

      letzter = new Error(meldung);
      if (nochmal && v < versuche) { await schlafen(2000); continue; }
      throw letzter;
    } catch (err) {
      letzter = err;
      // Netz weg oder abgebrochen — einmal nachfassen
      if (err.name === 'TypeError' && v < versuche) { await schlafen(2000); continue; }
      throw err;
    }
  }
  throw letzter;
}

/* Hat die Prüfung im Server etwas gefunden, das dort aus Zeitgründen
   nicht mehr repariert werden konnte, holen wir die Reparatur in einem
   zweiten Ruf nach. Der hat sein eigenes Zeitbudget.

   Geht das schief, bleibt der erste Entwurf stehen — er ist brauchbar,
   nur nicht perfekt. Lieber das als eine Fehlermeldung. */
async function nachschaerfen(art, entwurf, meta, sagen) {
  if (!meta || !Array.isArray(meta.offen) || !meta.offen.length) return entwurf;
  if (sagen) sagen();
  try {
    return await rufen({ modus: 'nachbessern', art, entwurf, ...grunddaten() }, 1);
  } catch {
    return entwurf;
  }
}

/* ---------- Schritt 2: die drei Ideen ---------- */

function ideenZeichnen(ergebnis) {
  spiegel.textContent = ergebnis.spiegel || '';
  spiegel.hidden = !ergebnis.spiegel;

  karten.innerHTML = '';
  ideen.slice(0, 3).forEach((idee, i) => {
    const karte = document.createElement('article');
    karte.className = 'karte';
    karte.dataset.nr = i;
    karte.style.animationDelay = `${i * 0.12}s`;
    karte.innerHTML = `
      <p class="karte__zahl">Idee ${i + 1}${idee.quelle ? ` · aus deiner ${sicher(idee.quelle)}` : ''}</p>
      <h3 class="karte__name">${sicher(idee.name)}</h3>
      <p class="karte__versprechen">${sicher(idee.versprechen)}</p>
      ${idee.fuer_wen ? `<p class="karte__zeile"><b>Für wen:</b> ${sicher(idee.fuer_wen)}</p>` : ''}
      ${idee.problem ? `<p class="karte__zeile"><b>Das eine Problem:</b> ${sicher(idee.problem)}</p>` : ''}
      ${idee.ergebnis ? `<p class="karte__zeile"><b>Am Ende hat sie:</b> ${sicher(idee.ergebnis)}</p>` : ''}
      ${idee.network_baustein ? `<p class="karte__zeile karte__zeile--network"><b>Dein Network-Produkt darin:</b> ${sicher(idee.network_baustein)}</p>` : ''}
      ${idee.erster_schritt ? `<p class="karte__schritt"><b>Dein erster Schritt:</b> ${sicher(idee.erster_schritt)}</p>` : ''}
      ${idee.beleg_check ? `<p class="karte__beleg"><b>Ob das wirklich gefragt ist, findest du so raus:</b> ${sicher(idee.beleg_check)}</p>` : ''}
      <div class="karte__knoepfe">
        <button class="knopf knopf--voll" data-tun="gliederung" data-nr="${i}">Inhaltsverzeichnis bauen →</button>
        <button class="knopf knopf--klein" data-tun="titel" data-nr="${i}">↻ Anderer Name</button>
      </div>
    `;
    karten.appendChild(karte);
  });

  if (ergebnis.hinweis) {
    const h = document.createElement('p');
    h.className = 'nachsatz';
    h.textContent = ergebnis.hinweis;
    karten.appendChild(h);
  }
}

async function ideenHolen() {
  const text = thema.value.trim();
  if (!text) {
    fehlerZeigen('Schreib zuerst kurz, worüber du mehr weisst als andere.');
    thema.focus();
    return;
  }

  fehlerWeg();
  nurZeigen(tafelWarten);
  los.disabled = true;
  wartenStarten([
    'Ich schau mir dein Thema an …',
    'Was können deine Leute noch nicht, das du kannst?',
    'Ich suche, was vor dem Produkt kommt …',
    'Namen schärfen …',
  ]);

  try {
    let ergebnis = await rufen({ modus: 'ideen', ...grunddaten() });
    ergebnis = await nachschaerfen('ideen', ergebnis, letzteMeta, () => {
      wartenStoppen();
      wartenStarten(['Ich schärfe noch nach …']);
    });
    ideen = ergebnis.ideen || [];
    wartenStoppen();
    ideenZeichnen(ergebnis);
    nurZeigen(tafelIdeen);
    zeigeSchritt(2);
    nachOben();
  } catch (err) {
    wartenStoppen();
    nurZeigen(tafelEingabe);
    zeigeSchritt(1);
    fehlerZeigen(err.message);
  } finally {
    los.disabled = false;
  }
}

/* ---------- Name neu ---------- */

async function titelNeu(nr, knopf) {
  const idee = ideen[nr];
  if (!idee) return;

  const karte = karten.querySelector(`.karte[data-nr="${nr}"]`);
  const nameEl = karte && karte.querySelector('.karte__name');
  const versprEl = karte && karte.querySelector('.karte__versprechen');
  const alt = knopf.textContent;

  knopf.disabled = true;
  knopf.textContent = '↻ …';
  fehlerWeg();

  try {
    const ergebnis = await rufen({
      modus: 'titel',
      ...grunddaten(),
      ...ideeDaten(idee),
    });
    idee.name = String(ergebnis.name || '').trim() || idee.name;
    idee.versprechen = String(ergebnis.versprechen || '').trim() || idee.versprechen;
    if (nameEl) {
      nameEl.textContent = idee.name;
      nameEl.style.animation = 'none';
      void nameEl.offsetHeight;
      nameEl.style.animation = 'titelAuf .4s ease';
    }
    if (versprEl) versprEl.textContent = idee.versprechen;
  } catch (err) {
    fehlerZeigen(err.message);
  } finally {
    knopf.disabled = false;
    knopf.textContent = alt;
  }
}

/* ---------- Schritt 3: das Inhaltsverzeichnis ---------- */

/* Eine Lektion kommt als {nummer, titel} — aeltere Antworten schicken
   manchmal nur einen String. Beides muss gehen. */
function lektionText(l, modulNr, i) {
  if (typeof l === 'string') return { nummer: `${modulNr}.${i + 1}`, titel: l };
  return { nummer: l.nummer || `${modulNr}.${i + 1}`, titel: l.titel || '' };
}

function gliederungZeichnen(g) {
  gTitel.textContent = g.name || '';
  gVerspr.textContent = g.versprechen || '';
  gVerspr.hidden = !g.versprechen;
  gErgebnis.textContent = g.ergebnis ? `Am Ende hast du: ${g.ergebnis}` : '';
  gErgebnis.hidden = !g.ergebnis;
  gAbschluss.textContent = g.abschluss || '';
  gAbschluss.hidden = !g.abschluss;

  gModule.innerHTML = '';
  (g.module || []).forEach((m, i) => {
    const el = document.createElement('article');
    el.className = 'modul';
    el.style.animationDelay = `${i * 0.07}s`;
    const lektionen = (m.lektionen || [])
      .map((l, k) => lektionText(l, i, k))
      .map((l) => `<li><span class="lek__nr">${sicher(l.nummer)}</span>${sicher(l.titel)}</li>`)
      .join('');
    el.innerHTML = `
      <p class="modul__zahl">${sicher(m.nummer || `Modul ${i}`)}</p>
      <h4 class="modul__titel">${sicher(m.titel || '')}</h4>
      ${m.klammer ? `<p class="modul__unter">${sicher(m.klammer)}</p>` : ''}
      ${lektionen ? `<ul class="modul__liste">${lektionen}</ul>` : ''}
      ${m.material ? `<p class="modul__material">📎 ${sicher(m.material)}</p>` : ''}
    `;
    gModule.appendChild(el);
  });

  // Fassung zum Kopieren
  let t = `${g.name || ''}${g.versprechen ? ` — ${g.versprechen}` : ''}\n`;
  if (g.fuer_wen) t += `Für wen: ${g.fuer_wen}\n`;
  if (g.ergebnis) t += `Am Ende hast du: ${g.ergebnis}\n`;
  t += '\n';
  (g.module || []).forEach((m, i) => {
    t += `${m.nummer ? `${m.nummer} — ` : ''}${m.titel || ''}`;
    t += m.klammer ? ` (${m.klammer})\n` : '\n';
    (m.lektionen || []).map((l, k) => lektionText(l, i, k))
      .forEach((l) => { t += `  - ${l.nummer} ${l.titel}\n`; });
    if (m.material) t += `  📎 ${m.material}\n`;
    t += '\n';
  });
  if (g.abschluss) t += `${g.abschluss}\n`;
  gliederungAlsText = t.trim();
}

async function gliederungHolen(nr) {
  const idee = ideen[nr];
  if (!idee) return;

  fehlerWeg();
  nurZeigen(tafelWarten);
  wartenStarten([
    'Ich denk vom Ende her …',
    'Was muss sie am Schluss in den Händen halten?',
    'Module in die richtige Reihenfolge bringen …',
    'Was kann weg, ohne dass etwas fehlt?',
    'Material zuordnen …',
  ]);

  try {
    let g = await rufen({
      modus: 'gliederung',
      ...grunddaten(),
      ...ideeDaten(idee),
    });
    g = await nachschaerfen('gliederung', g, letzteMeta, () => {
      wartenStoppen();
      wartenStarten(['Ich schärfe noch nach …']);
    });
    wartenStoppen();
    gliederungZeichnen(g);
    nurZeigen(tafelGliederung);
    zeigeSchritt(3);
    nachOben();
  } catch (err) {
    wartenStoppen();
    nurZeigen(tafelIdeen);
    zeigeSchritt(2);
    fehlerZeigen(err.message);
  }
}

/* ---------- Knoepfe ---------- */

los.addEventListener('click', ideenHolen);

thema.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ideenHolen(); }
});

karten.addEventListener('click', (e) => {
  const knopf = e.target.closest('button[data-tun]');
  if (!knopf) return;
  const nr = Number(knopf.dataset.nr);
  if (knopf.dataset.tun === 'gliederung') gliederungHolen(nr);
  if (knopf.dataset.tun === 'titel') titelNeu(nr, knopf);
});

$('#zurueck-thema').addEventListener('click', () => {
  fehlerWeg();
  nurZeigen(tafelEingabe);
  zeigeSchritt(1);
  karten.innerHTML = '';
  gModule.innerHTML = '';
  thema.focus();
  thema.select();
});

$('#zurueck-ideen').addEventListener('click', () => {
  fehlerWeg();
  nurZeigen(tafelIdeen);
  zeigeSchritt(2);
  nachOben();
});

$('#kopieren').addEventListener('click', (e) => {
  const knopf = e.currentTarget;
  const alt = knopf.textContent;
  const fertig = () => {
    knopf.textContent = 'Kopiert ✓';
    setTimeout(() => { knopf.textContent = alt; }, 1800);
  };
  if (navigator.clipboard) {
    navigator.clipboard.writeText(gliederungAlsText).then(fertig).catch(() => {
      fehlerZeigen('Kopieren ging nicht — markier den Text und kopier ihn von Hand.');
    });
  } else {
    fehlerZeigen('Kopieren ging nicht — markier den Text und kopier ihn von Hand.');
  }
});

thema.focus();
