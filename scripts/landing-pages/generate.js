/**
 * Landing-Page-Generator für Mum Life Balance Freebies
 * ----------------------------------------------------
 * Baut aus einem gemeinsamen Brand-Template + pro-Freebie-Content-Config
 * je eine standalone index.html (für WordPress „Individuelles HTML"/Elementor-HTML-Widget).
 *
 * Migration Netlify → WordPress (2026-06-10). Gleiche Optik wie Starterguide.
 *
 * Run:  node scripts/landing-pages/generate.js
 * Output: outputs/funnels/<slug>/landing/index.html  (je Config)
 *
 * Opt-in-Typen:
 *   - 'ac'   → ActiveCampaign-Formular-Platzhalter (Form-ID/Token später einsetzen,
 *              oder kompletten AC-Embed-Code reinkopieren wie beim Starterguide #53)
 *   - 'link' → grosser CTA-Button auf eine externe URL (z.B. Jotform-Quiz)
 */

import { writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const FOTO = 'https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg';

const CSS = `
.slg-wrap * { box-sizing: border-box; margin: 0; padding: 0; }
.slg-wrap { font-family: 'Source Sans 3', system-ui, -apple-system, sans-serif; color: #0c1c30; line-height: 1.65; background: #f1ecdd; font-size: 18px; }
.slg-wrap h1, .slg-wrap h2, .slg-wrap h3, .slg-wrap .slg-kicker { font-family: 'Philosopher', Georgia, serif; }
.slg-inner { max-width: 760px; margin: 0 auto; padding: 0 24px; }
.slg-section { padding: 64px 0; }
.slg-kicker { display: inline-block; color: #12828c; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; font-size: 15px; margin-bottom: 16px; }
.slg-hero { background: linear-gradient(160deg, #29556d 0%, #12828c 100%); color: #f1ecdd; text-align: center; padding: 80px 0 72px; }
.slg-hero h1 { font-size: clamp(32px, 6vw, 52px); line-height: 1.12; color: #ffffff; margin-bottom: 22px; font-weight: 700; }
.slg-hero h1 em { color: #f2c879; font-style: normal; }
.slg-hero p.sub { font-size: clamp(18px, 2.6vw, 22px); max-width: 600px; margin: 0 auto 34px; color: rgba(241, 236, 221, 0.94); }
.slg-badge { display: inline-block; background: rgba(241,236,221,0.16); border: 1px solid rgba(241,236,221,0.35); border-radius: 999px; padding: 7px 18px; font-size: 14px; font-weight: 600; letter-spacing: 0.4px; margin-bottom: 26px; }
.slg-cta { display: inline-block; background: #dc822e; color: #ffffff !important; font-family: 'Source Sans 3', sans-serif; font-weight: 700; font-size: 19px; text-decoration: none; padding: 18px 40px; border-radius: 14px; letter-spacing: 0.3px; transition: transform 0.12s ease, box-shadow 0.2s ease; box-shadow: 0 6px 18px rgba(220,130,46,0.35); }
.slg-cta:hover { transform: translateY(-2px); box-shadow: 0 10px 26px rgba(220,130,46,0.45); }
.slg-cta-note { display: block; margin-top: 14px; font-size: 14px; opacity: 0.8; }
.slg-pain { background: #f1ecdd; }
.slg-pain h2 { font-size: clamp(26px, 4vw, 34px); color: #29556d; margin-bottom: 26px; }
.slg-pain ul { list-style: none; }
.slg-pain li { position: relative; padding: 12px 0 12px 38px; font-size: 19px; border-bottom: 1px solid rgba(41,85,109,0.12); }
.slg-pain li:before { content: "\\2717"; position: absolute; left: 0; top: 11px; color: #c25a3c; font-weight: 700; font-size: 19px; }
.slg-bridge { background: #29556d; color: #f1ecdd; text-align: center; }
.slg-bridge h2 { font-size: clamp(26px, 4vw, 36px); color: #ffffff; margin-bottom: 20px; }
.slg-bridge p { font-size: 20px; max-width: 600px; margin: 0 auto 16px; color: rgba(241,236,221,0.94); }
.slg-bridge .accent { color: #f2c879; font-weight: 700; }
.slg-content { background: #f7f3e8; }
.slg-content h2 { font-size: clamp(26px, 4vw, 34px); color: #29556d; text-align: center; margin-bottom: 14px; }
.slg-content .lead { text-align: center; max-width: 560px; margin: 0 auto 42px; color: #4a5663; }
.slg-cards { display: grid; gap: 20px; }
.slg-card { background: #ffffff; border-radius: 18px; padding: 28px 30px; border-left: 5px solid #12828c; box-shadow: 0 4px 18px rgba(41,85,109,0.07); }
.slg-card h3 { font-size: 22px; color: #12828c; margin-bottom: 8px; }
.slg-card .num { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; background: #12828c; color: #fff; border-radius: 50%; font-weight: 700; font-size: 16px; margin-right: 10px; font-family: 'Source Sans 3', sans-serif; }
.slg-card p { color: #4a5663; font-size: 17px; }
.slg-chips { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 14px; }
.slg-chip { background: #f1ecdd; border: 1.5px solid rgba(18,130,140,0.25); color: #12828c; border-radius: 999px; padding: 8px 16px; font-size: 15px; font-weight: 600; }
.slg-for { background: #f1ecdd; }
.slg-for h2 { font-size: clamp(24px, 4vw, 32px); color: #29556d; text-align: center; margin-bottom: 28px; }
.slg-for ul { list-style: none; max-width: 600px; margin: 0 auto; }
.slg-for li { position: relative; padding: 11px 0 11px 38px; font-size: 18px; }
.slg-for li:before { content: "\\2713"; position: absolute; left: 0; top: 10px; color: #12828c; font-weight: 700; font-size: 19px; }
.slg-about { background: #f7f3e8; }
.slg-about .row { display: flex; gap: 32px; align-items: center; flex-wrap: wrap; }
.slg-about img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #ffffff; box-shadow: 0 6px 20px rgba(41,85,109,0.15); flex-shrink: 0; }
.slg-about .txt { flex: 1; min-width: 260px; }
.slg-about h2 { font-size: 26px; color: #29556d; margin-bottom: 12px; }
.slg-about p { color: #4a5663; font-size: 17px; margin-bottom: 12px; }
.slg-optin { background: linear-gradient(160deg, #12828c 0%, #29556d 100%); text-align: center; }
.slg-optin h2 { font-size: clamp(26px, 4vw, 36px); color: #ffffff; margin-bottom: 14px; }
.slg-optin > .slg-inner > p { color: rgba(241,236,221,0.94); font-size: 19px; max-width: 540px; margin: 0 auto 32px; }
.slg-foot { background: #0c1c30; color: rgba(241,236,221,0.7); text-align: center; padding: 32px 0; font-size: 14px; }
.slg-foot a { color: #f2c879; }
@media (max-width: 560px) { .slg-section { padding: 48px 0; } .slg-hero { padding: 60px 0 54px; } }`;

const li = (items) => items.map((t) => `        <li>${t}</li>`).join('\n');
const ps = (arr, cls = '') => arr.map((t) => `      <p${cls ? ` class="${cls}"` : ''}>${t}</p>`).join('\n');

function cards(list) {
  return list.map((c, i) => {
    const chips = c.chips ? `\n          <div class="slg-chips">${c.chips.map((x) => `<span class="slg-chip">${x}</span>`).join('')}</div>` : '';
    return `        <div class="slg-card">
          <h3><span class="num">${i + 1}</span>${c.h3}</h3>
          <p>${c.p}</p>${chips}
        </div>`;
  }).join('\n');
}

function optinBlock(o) {
  if (o.type === 'link') {
    return `      <a href="${o.url}" class="slg-cta" style="font-size:21px;padding:20px 46px;">${o.buttonLabel}</a>
      ${o.note ? `<span class="slg-cta-note">${o.note}</span>` : ''}`;
  }
  // AC-Formular-Platzhalter
  return `      <!-- ⚠️ ActiveCampaign-Platzhalter — AC-Embed-Code von Patricia einsetzen (u/f/or + Brand-Override), wie beim Starterguide #53 -->
      <form method="POST" action="https://mumlifebalance.activehosted.com/proc.php" id="_form_${o.formId}_" class="_form _inline-form" novalidate data-styles-version="5" style="max-width:500px;margin:0 auto;background:#f1ecdd;padding:32px;border-radius:18px;text-align:left;box-shadow:0 10px 30px rgba(12,28,48,0.18);">
        <input type="hidden" name="u" value="${o.formId}" />
        <input type="hidden" name="f" value="${o.formId}" />
        <input type="hidden" name="s" />
        <input type="hidden" name="c" value="0" />
        <input type="hidden" name="m" value="0" />
        <input type="hidden" name="act" value="sub" />
        <input type="hidden" name="v" value="2" />
        <input type="hidden" name="or" value="${o.token}" />
        <h2 style="font-family:'Philosopher',Georgia,serif;color:#29556d;font-size:22px;text-align:center;margin-bottom:18px;">${o.formTitle}</h2>
        <label style="display:block;color:#29556d;font-weight:700;margin-bottom:5px;">Vorname*</label>
        <input type="text" name="fullname" placeholder="Dein Vorname" required style="display:block;width:100%;background:#fff;border:1.5px solid rgba(41,85,109,0.2);border-radius:10px;padding:12px;margin-bottom:14px;" />
        <label style="display:block;color:#29556d;font-weight:700;margin-bottom:5px;">E-Mail*</label>
        <input type="text" name="email" placeholder="Deine beste E-Mail-Adresse" required style="display:block;width:100%;background:#fff;border:1.5px solid rgba(41,85,109,0.2);border-radius:10px;padding:12px;margin-bottom:14px;" />
        <button type="submit" style="width:100%;background:#dc822e;color:#fff;font-family:'Source Sans 3',sans-serif;font-weight:700;font-size:18px;padding:16px;border:0;border-radius:14px;cursor:pointer;">${o.submitLabel}</button>
      </form>`;
}

function buildPage(c) {
  const aboutP1 = 'Mama, Unternehmerin und Mentorin für Network-Mamas, die nebenbei ein ehrliches Online-Business aufbauen wollen — ohne Druck, ohne Verstellen, im Tempo der Familie.';
  return `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>${c.title}</title>
<style>
/* Mum Life Balance — Landingpage „${c.name}" · Brand Creme/Petrol/Orange · Philosopher + Source Sans 3 */
${CSS}
</style>
</head>
<body>
<div class="slg-wrap">

  <header class="slg-hero">
    <div class="slg-inner">
      <span class="slg-badge">${c.badge}</span>
      <h1>${c.h1}</h1>
      <p class="sub">${c.sub}</p>
      <a href="#anmelden" class="slg-cta">${c.ctaLabel}</a>
      <span class="slg-cta-note">${c.ctaNote}</span>
    </div>
  </header>

  <section class="slg-section slg-pain">
    <div class="slg-inner">
      <span class="slg-kicker">${c.painKicker}</span>
      <h2>${c.painH2}</h2>
      <ul>
${li(c.painItems)}
      </ul>
    </div>
  </section>

  <section class="slg-section slg-bridge">
    <div class="slg-inner">
      <span class="slg-kicker" style="color:#f2c879;">${c.bridgeKicker}</span>
      <h2>${c.bridgeH2}</h2>
${ps(c.bridgeP)}
    </div>
  </section>

  <section class="slg-section slg-content">
    <div class="slg-inner">
      <span class="slg-kicker" style="display:block;text-align:center;">${c.contentKicker}</span>
      <h2>${c.contentH2}</h2>
      <p class="lead">${c.contentLead}</p>
      <div class="slg-cards">
${cards(c.cards)}
      </div>
    </div>
  </section>

  <section class="slg-section slg-for">
    <div class="slg-inner">
      <h2>${c.forH2}</h2>
      <ul>
${li(c.forItems)}
      </ul>
    </div>
  </section>

  <section class="slg-section slg-about">
    <div class="slg-inner">
      <div class="row">
        <img src="${FOTO}" alt="Patricia" />
        <div class="txt">
          <h2>Hi, ich bin Patricia 🌿</h2>
          <p>${aboutP1}</p>
          <p>${c.aboutP2}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="slg-section slg-optin" id="anmelden">
    <div class="slg-inner">
      <span class="slg-kicker" style="color:#f2c879;display:block;">${c.optin.kicker}</span>
      <h2>${c.optin.h2}</h2>
      <p>${c.optin.p}</p>
${optinBlock(c.optin)}
    </div>
  </section>

  <footer class="slg-foot">
    <div class="slg-inner">
      <p>© Mum Life Balance · Patricia &nbsp;|&nbsp; <a href="https://mumlifebalance.ch/impressum">Impressum</a> &nbsp;·&nbsp; <a href="https://mumlifebalance.ch/datenschutz">Datenschutz</a></p>
    </div>
  </footer>

</div>
</body>
</html>`;
}

const CONFIGS = [
  {
    slug: 'lead-challenge',
    name: 'Lead-Challenge',
    title: '0€ Lead-Challenge — In 3 Tagen zu deinem ersten Leadmagneten | Mum Life Balance',
    badge: '🎁 Gratis · 3-Tage-Challenge · Mit Telegram-Begleitung',
    h1: 'In 3 Tagen zu deinem ersten Leadmagneten – und einer Liste, die <em>dir</em> gehört',
    sub: 'Die gratis Lead-Challenge für Network-Mamas: Schluss mit der Abhängigkeit vom Algorithmus. In 3 kleinen Schritten baust du deinen ersten Leadmagneten — fertig statt perfekt.',
    ctaLabel: 'Ja, ich mach mit',
    ctaNote: 'Kostenlos · 3-Tage-Workbook + Telegram-Kanal · In deinem Tempo',
    painKicker: 'Kennst du das?',
    painH2: 'Du hängst komplett am Instagram-Algorithmus',
    painItems: [
      'Wenn ein Post nicht läuft, kommt einfach nichts — keine Anfragen, keine Kundinnen.',
      'Du hast Follower, aber keine eigene Liste, die wirklich dir gehört.',
      'Du würdest gern einen Leadmagneten bauen, weisst aber nicht, wo du anfangen sollst.',
      'Du wartest auf den „perfekten" Moment – und deshalb entsteht er nie.',
    ],
    bridgeKicker: 'Die gute Nachricht',
    bridgeH2: 'Fertig ist besser als <span class="accent">perfekt</span>.',
    bridgeP: [
      'Dein erster Leadmagnet muss gut sein, nicht makellos. In 3 Tagen hast du ihn – und damit den ersten Baustein für eine Liste, die niemand dir wegnehmen kann.',
      'Ich begleite dich täglich im Telegram-Kanal, damit du wirklich dranbleibst und am Ende etwas Fertiges in der Hand hast.',
    ],
    contentKicker: 'Wie die Challenge läuft',
    contentH2: '3 Tage, 3 klare Schritte',
    contentLead: 'Jeden Tag eine Aufgabe zum Ausfüllen + ein Impuls von mir im Telegram-Kanal. Kein Perfektionsdruck – einfach machen.',
    cards: [
      { h3: 'Tag 1 — Dein Thema', p: 'Du klärst, wem du wobei hilfst: von A nach B deiner Wunschkundin. Was weisst DU, was andere nicht wissen? Dein Thema in einem Satz.' },
      { h3: 'Tag 2 — Dein Produkt', p: 'Du wählst dein Format (PDF, Mini-Workbook, Mini-Training oder E-Mail-Kurs), findest die Idee und entwickelst einen Titel, der sofort zieht.' },
      { h3: 'Tag 3 — Zeig dich', p: 'Du bringst deinen Leadmagneten unter die Leute: Bewerbung, Landingpage und der einfache Weg, wie Interessentinnen ihn automatisch bekommen.' },
    ],
    forH2: 'Für dich, wenn …',
    forItems: [
      '… du im Network-Marketing bist und endlich <strong>unabhängiger vom Algorithmus</strong> werden willst.',
      '… du deine <strong>eigene E-Mail-Liste</strong> aufbauen willst, statt nur auf Insta zu hoffen.',
      '… du zum Tüfteln keine Zeit hast und einen klaren 3-Tage-Plan brauchst.',
      '… du lieber heute etwas Fertiges hast als irgendwann etwas Perfektes.',
    ],
    aboutP2: 'Eine eigene Liste war mein Wendepunkt – weg von „hoffentlich sieht es jemand", hin zu „meine Leute erreiche ich direkt". Genau diesen ersten Leadmagneten bring ich dir in 3 Tagen bei.',
    optin: { type: 'ac', formId: 'LEAD_AC_FORM_ID', token: 'LEAD_AC_TOKEN', kicker: 'Jetzt gratis mitmachen', h2: 'Schick mir die Lead-Challenge', p: 'Trag dich ein und du bekommst das 3-Tage-Workbook + den Link zum Telegram-Kanal mit den täglichen Impulsen.', formTitle: 'Lead-Challenge gratis holen', submitLabel: 'Lead-Challenge starten 🌿' },
  },
  {
    slug: 'workbook-von-0-auf-echt',
    name: 'Von 0 auf echt',
    title: '0€ Workbook „Von 0 auf echt" — Dein erster Schritt zum eigenen Business | Mum Life Balance',
    badge: '🎁 Gratis · 25-Seiten-Workbook',
    h1: 'Von 0 auf echt: dein Weg von „irgendwann mal" zu <em>deinem eigenen Business</em>',
    sub: 'Das gratis Workbook für Mamas mit einem Thema, das in ihnen brennt – ohne Business-Erfahrung, ohne perfekte Strategie. Du findest dein Thema und den Mut, anzufangen.',
    ctaLabel: 'Ja, ich will das Workbook',
    ctaNote: 'Kostenlos · 25-Seiten-Workbook · Schritt für Schritt',
    painKicker: 'Jetzt mal ganz ehrlich',
    painH2: 'Dein Tag ist voll – aber dein Herz fühlt sich leer an',
    painItems: [
      'Da ist dieses Thema, das in dir brennt – aber du nimmst dir nie die Zeit dafür.',
      'Du willst mehr, weisst aber nicht, wo und wie du überhaupt anfangen sollst.',
      'Du denkst, du brauchst zuerst die perfekte Strategie, bevor du loslegen darfst.',
      'Tief drin fragst du dich, ob du dich selbst überhaupt so wichtig nehmen darfst.',
    ],
    bridgeKicker: 'Die gute Nachricht',
    bridgeH2: 'Du <span class="accent">darfst</span>. Du <span class="accent">kannst</span>. Und du fängst jetzt an.',
    bridgeP: [
      'Ich weiss, wie es sich anfühlt, wenn dein Tag voll ist, aber dein Herz leer. Du brauchst keine fertige Strategie – du brauchst den ersten ehrlichen Schritt.',
      'Dieses Workbook nimmt dich an die Hand: von deinem Warum bis zu deinem ersten echten Angebot. In deinem Tempo, ohne Druck.',
    ],
    contentKicker: 'Was drin ist',
    contentH2: 'In 6 Schritten von der Idee zum echten Business',
    contentLead: 'Wie eine Pflanze, die wächst – Schritt für Schritt, mit Aufgaben zum Ausfüllen und ganz viel Ermutigung.',
    cards: [
      { h3: 'Dein Boden', p: 'Dein Warum, deine Haltung, deine Werte – das Fundament, auf dem alles aufbaut.' },
      { h3: 'Dein Samen', p: 'Deine Vision und die grosse Idee: Wo willst du eigentlich hin? Dein Zielbild wird klar.' },
      { h3: 'Deine Wurzeln', p: 'Deine Nische und dein Thema – wo deine eigene Geschichte das trifft, was andere wirklich brauchen.' },
      { h3: 'Dein Wasser', p: 'Du formst dein Thema konkret und entwickelst dein erstes Angebot.' },
      { h3: 'Deine Sonne', p: 'Deine Aussenwirkung: Content und Vertrauen aufbauen, damit dich die richtigen Menschen finden.' },
      { h3: 'Dein Dünger', p: 'Routinen und Strukturen, die in deinen Mama-Alltag passen – damit es nicht beim Strohfeuer bleibt.' },
    ],
    forH2: 'Für dich, wenn …',
    forItems: [
      '… ein Thema in dir brennt, du aber noch <strong>keine Business-Erfahrung</strong> hast.',
      '… du nebenbei Mama bist und dir <strong>klare, kleine Schritte</strong> wünschst.',
      '… du dir endlich die Erlaubnis geben willst, dich selbst wichtig zu nehmen.',
      '… du nicht mehr nur „irgendwann mal" sagen, sondern jetzt anfangen willst.',
    ],
    aboutP2: 'Ich hab selbst bei Null angefangen – mit vier Kindern, ohne fertigen Plan, aber mit einem Thema, das mich nicht losgelassen hat. Genau diesen ersten Schritt mach ich dir hier so leicht wie möglich.',
    optin: { type: 'ac', formId: 'ECHT_AC_FORM_ID', token: 'ECHT_AC_TOKEN', kicker: 'Jetzt gratis sichern', h2: 'Schick mir das Workbook „Von 0 auf echt"', p: 'Trag dich ein und du bekommst das 25-Seiten-Workbook direkt in dein Postfach.', formTitle: 'Workbook gratis holen', submitLabel: 'Workbook holen 🌿' },
  },
  {
    slug: 'fahrplan',
    name: 'Fahrplan',
    title: '0€ Fahrplan — Von Produktposts zu doppeltem Einkommen | Mum Life Balance',
    badge: '🎁 Gratis · Der Fahrplan in 10 Schritten',
    h1: 'Von Produktposts zu <em>doppeltem Einkommen</em>',
    sub: 'Der gratis Fahrplan für Networkerinnen: die exakte Strategie, wie aus Produkt-Postings ein echtes Einkommen aus Network UND eigenen Produkten wird.',
    ctaLabel: 'Ja, ich will den Fahrplan',
    ctaNote: 'Kostenlos · Klarer 10-Schritte-Fahrplan · Sofort',
    painKicker: 'Kennst du das?',
    painH2: 'Du postest Produkte – und es kommt einfach nichts zurück',
    painItems: [
      'Du teilst fleissig Produktbilder, aber echte Anfragen bleiben aus.',
      'Du verlässt dich allein aufs Network – ein zweites Standbein fehlt komplett.',
      'Du weisst, dass „mehr posten" nicht die Lösung ist – aber was dann?',
      'Du siehst andere mit eigenen Produkten wachsen und fragst dich, wie sie das machen.',
    ],
    bridgeKicker: 'Die gute Nachricht',
    bridgeH2: 'Dein Produkt ist nicht dein <span class="accent">Thema</span>.',
    bridgeP: [
      'Dein Thema ist das Ergebnis, das du für andere möglich machst. Sobald du das in den Mittelpunkt stellst, kommen die Kundinnen von selbst.',
      'Der Fahrplan zeigt dir den Weg in 4 klaren Phasen – von der Positionierung bis zu deinem ersten eigenen Produkt neben dem Network.',
    ],
    contentKicker: 'Was drin ist',
    contentH2: 'Dein Weg in 4 Phasen',
    contentLead: '10 konkrete Schritte, die aufeinander aufbauen – ohne Fachchinesisch, mit klarem roten Faden.',
    cards: [
      { h3: 'Phase 1 — Das Fundament', p: 'Du findest dein Thema und positionierst dich als Expertin – nicht als Produkt-Verkäuferin.' },
      { h3: 'Phase 2 — Sichtbar werden', p: 'Content, der deine Zielgruppe wirklich abholt, plus tägliche Stories, die Verbindung schaffen.' },
      { h3: 'Phase 3 — Leads sammeln', p: 'Du baust einen Leadmagneten, eine E-Mail-Liste und einen einfachen Funnel – dein eigenes System.' },
      { h3: 'Phase 4 — Eigene Produkte', p: 'Dein erstes eigenes Angebot, deine Produkttreppe und die Komplettlösung neben dem Network.' },
    ],
    forH2: 'Für dich, wenn …',
    forItems: [
      '… du im Network bist und <strong>Produkte postest, aber kaum Anfragen</strong> bekommst.',
      '… du dir ein <strong>zweites Standbein</strong> neben dem Network aufbauen willst.',
      '… du eine klare Reihenfolge willst, statt planlos auszuprobieren.',
      '… du aus „nebenbei posten" ein echtes, planbares Einkommen machen willst.',
    ],
    aboutP2: 'Ich hab selbst gemerkt: Solange ich nur Produkte gepostet habe, kam wenig zurück. Erst mit Thema, Positionierung und eigenen Produkten wurde daraus ein zweites Einkommen – und genau diesen Fahrplan teile ich hier.',
    optin: { type: 'ac', formId: 'FAHRPLAN_AC_FORM_ID', token: 'FAHRPLAN_AC_TOKEN', kicker: 'Jetzt gratis sichern', h2: 'Schick mir den Fahrplan', p: 'Trag dich ein und du bekommst den kompletten Fahrplan direkt in dein Postfach.', formTitle: 'Fahrplan gratis holen', submitLabel: 'Fahrplan holen 🌿' },
  },
  {
    slug: 'potenzial-test',
    name: 'Potenzial-Test',
    title: '0€ Potenzial-Test — Was bremst dein Network-Business? | Mum Life Balance',
    badge: '🎁 Gratis · 7 Fragen · Sofort-Ergebnis',
    h1: 'Was bremst dein Network-Business <em>wirklich</em> aus?',
    sub: 'Der gratis Potenzial-Test für Network-Mamas: 7 kurze Fragen, und du weisst, wo dein grösster Wachstumsblocker liegt – und welcher nächste Schritt zu dir passt.',
    ctaLabel: 'Test jetzt starten',
    ctaNote: 'Kostenlos · 7 Fragen · ca. 3 Minuten',
    painKicker: 'Kennst du das?',
    painH2: 'Du gibst alles – und kommst trotzdem nicht voran',
    painItems: [
      'Du hast Follower, aber irgendwie werden daraus keine Kundinnen.',
      'Du probierst vieles aus, weisst aber nicht, woran es wirklich hakt.',
      'Mal denkst du, es liegt am Profil, mal an der Positionierung, mal an dir.',
      'Dir fehlt ein klarer nächster Schritt, statt immer alles gleichzeitig zu versuchen.',
    ],
    bridgeKicker: 'Die gute Nachricht',
    bridgeH2: 'Du brauchst keinen <span class="accent">grösseren</span> Plan – du brauchst den <span class="accent">richtigen</span> Hebel.',
    bridgeP: [
      'Meistens ist es nur eine Sache, die dich gerade ausbremst. Wenn du die kennst, sparst du dir das Ausprobieren in alle Richtungen.',
      'In 7 Fragen findest du heraus, wo dein grösster Wachstumsblocker liegt – und bekommst direkt den passenden nächsten Schritt dazu.',
    ],
    contentKicker: 'Was dich erwartet',
    contentH2: 'Dein persönliches Ergebnis in einer von 4 Richtungen',
    contentLead: 'Nach 7 Fragen weisst du, welcher Typ dich gerade bremst – und was als Nächstes dran ist.',
    cards: [
      { h3: 'Typ A — Sichtbarkeit', p: 'Dein Profil zeigt noch nicht klar, wofür du stehst. Du erfährst, wie du sichtbar wirst.' },
      { h3: 'Typ B — Positionierung', p: 'Dein Thema ist noch unscharf. Du erfährst, wie du dich als Expertin klar positionierst.' },
      { h3: 'Typ C — Umsetzung', p: 'Dir fehlt die Routine zum Dranbleiben. Du erfährst, wie du ins konsequente Tun kommst.' },
      { h3: 'Typ D — Orientierung', p: 'Dir fehlt der rote Faden. Du erfährst, welcher Weg gerade zu dir passt.' },
    ],
    forH2: 'Für dich, wenn …',
    forItems: [
      '… du im Network-Marketing bist und endlich wissen willst, <strong>woran es wirklich hakt</strong>.',
      '… du Klarheit statt Bauchgefühl willst.',
      '… du deine Energie auf den <strong>einen</strong> richtigen nächsten Schritt lenken willst.',
      '… du in 3 Minuten ein ehrliches Standort-Ergebnis willst.',
    ],
    aboutP2: 'Ich hab gelernt: Wer alles gleichzeitig macht, kommt nirgends an. Dieser Test hilft dir, deinen einen Hebel zu finden – damit du gezielt vorankommst statt dich zu verzetteln.',
    optin: { type: 'link', kicker: 'Jetzt gratis herausfinden', h2: 'Starte deinen Potenzial-Test', p: 'Beantworte 7 kurze Fragen und du bekommst sofort dein persönliches Ergebnis – plus den passenden nächsten Schritt.', buttonLabel: 'Potenzial-Test starten →', url: 'https://eu.jotform.com/form/260726423595058', note: 'Kostenlos · ca. 3 Minuten · Ergebnis direkt im Anschluss' },
  },
];

for (const c of CONFIGS) {
  const dir = resolve(ROOT, 'outputs/funnels', c.slug, 'landing');
  await mkdir(dir, { recursive: true });
  await writeFile(resolve(dir, 'index.html'), buildPage(c), 'utf-8');
  console.log('✓ ' + c.slug + '/landing/index.html');
}
console.log('\\nFertig: ' + CONFIGS.length + ' Landingpages generiert.');
