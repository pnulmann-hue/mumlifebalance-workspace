// Deploy Mama-CEO Landing-Page auf mumlifebalance.ch
// Stil: gescopetes CSS .mceo (analog .bcp aus bio-check) — Brand-CSS-Variablen, Force-Light-Mode, Gradient-Buttons
// Wörter Patricia-konform: keine "Cohort", kein "techie", neuer Pitch
// Ausführen: cd scripts/wordpress && node --env-file=.env deploy-mama-ceo.js
// Status: draft (Patricia prüft + publiziert selbst)

import { createOrUpdatePage } from './wp-api.js';

const CTA_URL = 'https://mumlifebalance.thrivecart.com/mama-ceo/';

// Brand-Farben (aus bio-check übernommen, identisch)
const BRAND_CSS = `
<style>
/* === Force Light Mode (Mobile-Browser-Dark-Mode-Kill) === */
:root { color-scheme: light only; }
@media (prefers-color-scheme: dark) {
  .mceo, .mceo * { color-scheme: light only !important; }
}

/* === Brand-Variablen === */
.mceo {
  --creme: #f1ecdd;
  --dunkelblau: #29556d;
  --orange: #dc822e;
  --petrol: #12828c;
  --text: #0c1c30;
  --white: #ffffff;
  font-family: 'Source Sans 3', system-ui, -apple-system, sans-serif;
  color: var(--text);
  line-height: 1.6;
}
.mceo *, .mceo *::before, .mceo *::after { box-sizing: border-box; }

/* === Typografie === */
.mceo__h1 {
  font-family: 'Philosopher', Georgia, serif;
  font-size: clamp(2.4rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1.12;
  color: var(--dunkelblau);
  margin: 0 0 1.5rem;
}
.mceo__h1 em { font-style: italic; color: var(--petrol); }
.mceo__h2 {
  font-family: 'Philosopher', Georgia, serif;
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 700;
  line-height: 1.2;
  color: var(--dunkelblau);
  margin: 0 0 1.5rem;
}
.mceo__h2--center { text-align: center; }
.mceo__h2 em { font-style: italic; color: var(--petrol); }
.mceo__h3 {
  font-family: 'Philosopher', Georgia, serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--dunkelblau);
  margin: 0 0 1rem;
}
.mceo__eyebrow {
  font-size: 0.85rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--petrol);
  font-weight: 600;
  margin: 0 0 1.5rem;
}
.mceo__lead {
  font-size: clamp(1.1rem, 2vw, 1.3rem);
  line-height: 1.6;
  color: var(--text);
  max-width: 720px;
  margin: 0 auto 2rem;
}
.mceo__quote {
  font-family: 'Philosopher', Georgia, serif;
  font-style: italic;
  font-size: clamp(1.4rem, 3vw, 1.85rem);
  color: var(--petrol);
  text-align: center;
  margin: 3rem 0;
  line-height: 1.4;
}
.mceo p { margin: 0 0 1.2rem; font-size: 1.08rem; }
.mceo strong { color: var(--dunkelblau); }
.mceo em.accent { color: var(--orange); font-style: normal; font-weight: 600; }

/* === Sektionen === */
.mceo__section { padding: 5rem 1.5rem; }
.mceo__section--creme { background: var(--creme); }
.mceo__section--white { background: var(--white); }
.mceo__section--dark { background: var(--dunkelblau); color: var(--white); }
.mceo__section--dark .mceo__h2,
.mceo__section--dark .mceo__h3,
.mceo__section--dark .mceo__quote { color: var(--white); }
.mceo__section--dark strong { color: var(--orange); }
.mceo__container { max-width: 900px; margin: 0 auto; }
.mceo__container--wide { max-width: 1100px; margin: 0 auto; }
.mceo__container--narrow { max-width: 720px; margin: 0 auto; text-align: center; }

/* === Hero === */
.mceo__hero {
  min-height: 88vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  background: linear-gradient(180deg, var(--creme) 0%, #faf6ec 100%);
}
.mceo__hero-trust {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem 1.5rem;
  margin-top: 2rem;
  font-size: 0.95rem;
  color: var(--text);
  opacity: 0.85;
}
.mceo__hero-trust span { white-space: nowrap; }

/* === Buttons === */
.mceo__btn {
  display: inline-block;
  padding: 1.1rem 2.4rem;
  font-family: 'Source Sans 3', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 6px;
  letter-spacing: 0.03em;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 16px rgba(18, 130, 140, 0.2);
}
.mceo__btn--primary {
  background: linear-gradient(135deg, var(--petrol), var(--dunkelblau));
  color: var(--creme);
}
.mceo__btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(18, 130, 140, 0.35);
  color: var(--creme);
}
.mceo__btn--orange {
  background: var(--orange);
  color: var(--white);
}
.mceo__btn--orange:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(220, 130, 46, 0.4);
  color: var(--white);
}
.mceo__btn--cream {
  background: var(--creme);
  color: var(--dunkelblau);
}
.mceo__btn--cream:hover {
  transform: translateY(-2px);
  color: var(--dunkelblau);
}

/* === Pain-Block === */
.mceo__quote-block {
  font-family: 'Philosopher', Georgia, serif;
  font-style: italic;
  font-size: 1.4rem;
  color: var(--petrol);
  border-left: 4px solid var(--orange);
  padding: 0.5rem 0 0.5rem 1.5rem;
  margin: 2rem 0;
  line-height: 1.6;
}
.mceo__pain-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}
.mceo__pain-list li {
  font-size: 1.08rem;
  line-height: 1.7;
  padding: 0.6rem 0 0.6rem 2rem;
  position: relative;
  border-bottom: 1px dashed rgba(41, 85, 109, 0.15);
}
.mceo__pain-list li::before {
  content: "—";
  position: absolute;
  left: 0;
  color: var(--orange);
  font-weight: 700;
}
.mceo__punch {
  font-size: 1.3rem;
  line-height: 1.5;
  color: var(--dunkelblau);
  text-align: center;
  margin: 2.5rem 0 0;
  font-weight: 600;
}

/* === Modul-Grid === */
.mceo__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}
.mceo__module {
  background: var(--white);
  border: 2px solid rgba(18, 130, 140, 0.15);
  border-radius: 12px;
  padding: 2rem 1.8rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.mceo__module:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(41, 85, 109, 0.1);
  border-color: var(--petrol);
}
.mceo__module-eyebrow {
  font-family: 'Philosopher', serif;
  font-size: 0.95rem;
  letter-spacing: 0.05em;
  color: var(--orange);
  margin: 0 0 0.5rem;
  font-weight: 600;
}
.mceo__module h3 {
  font-family: 'Philosopher', serif;
  font-size: 1.35rem;
  color: var(--dunkelblau);
  margin: 0 0 1rem;
  line-height: 1.3;
}
.mceo__module p { font-size: 1rem; line-height: 1.6; color: var(--text); margin: 0 0 1rem; }
.mceo__module-meta {
  font-size: 0.9rem;
  color: var(--petrol);
  font-weight: 600;
  margin: 0;
  padding-top: 1rem;
  border-top: 1px solid rgba(18, 130, 140, 0.15);
}
.mceo__module--bonus {
  background: linear-gradient(135deg, var(--petrol), var(--dunkelblau));
  color: var(--creme);
  border-color: var(--petrol);
  grid-column: 1 / -1;
}
.mceo__module--bonus h3 { color: var(--creme); }
.mceo__module--bonus .mceo__module-eyebrow { color: var(--orange); }
.mceo__module--bonus p { color: var(--creme); }
.mceo__module--bonus .mceo__module-meta { color: var(--orange); border-color: rgba(241, 236, 221, 0.25); }

/* === Bonus-Liste === */
.mceo__bonus-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 1rem;
}
.mceo__bonus-list li {
  background: var(--white);
  padding: 1.2rem 1.5rem;
  border-radius: 10px;
  border-left: 4px solid var(--orange);
  font-size: 1.05rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.mceo__bonus-list li strong { color: var(--dunkelblau); }
.mceo__bonus-list li span { color: var(--petrol); font-weight: 600; white-space: nowrap; }

/* === Ja/Nein-Grid === */
.mceo__yesno {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
.mceo__yesno-card { padding: 2rem; border-radius: 12px; }
.mceo__yesno-card--yes {
  background: linear-gradient(135deg, rgba(18, 130, 140, 0.08), rgba(41, 85, 109, 0.04));
  border: 2px solid var(--petrol);
}
.mceo__yesno-card--no {
  background: linear-gradient(135deg, rgba(220, 130, 46, 0.08), rgba(220, 130, 46, 0.02));
  border: 2px solid rgba(220, 130, 46, 0.4);
}
.mceo__yesno-card h3 { display: flex; align-items: center; gap: 0.5rem; }
.mceo__yesno-card ul { padding-left: 1.2rem; margin: 0; }
.mceo__yesno-card li { font-size: 1rem; line-height: 1.7; margin-bottom: 0.6rem; }

/* === Pricing-Box === */
.mceo__price {
  background: var(--white);
  border-radius: 16px;
  padding: 2.5rem 2rem;
  margin: 1.5rem auto;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(41, 85, 109, 0.08);
  text-align: center;
  position: relative;
}
.mceo__price--featured {
  background: linear-gradient(135deg, var(--white), #fff8ed);
  border: 3px solid var(--orange);
}
.mceo__price--featured::before {
  content: "🔥 NUR 72 STUNDEN";
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--orange);
  color: var(--white);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 0.4rem 1.2rem;
  border-radius: 99px;
}
.mceo__price-label {
  font-size: 0.85rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--petrol);
  font-weight: 600;
  margin: 0 0 0.5rem;
}
.mceo__price-amount {
  font-family: 'Philosopher', serif;
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: 700;
  color: var(--dunkelblau);
  margin: 0.3rem 0;
  line-height: 1;
}
.mceo__price-note {
  font-size: 0.95rem;
  color: var(--text);
  opacity: 0.7;
  margin: 0;
}
.mceo__pricing-meta {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(18, 130, 140, 0.06);
  border-radius: 10px;
  font-size: 1rem;
  color: var(--text);
}

/* === FAQ === */
.mceo__faq details {
  border-bottom: 1px solid rgba(41, 85, 109, 0.15);
  padding: 1.5rem 0;
}
.mceo__faq details[open] summary { color: var(--petrol); }
.mceo__faq summary {
  font-family: 'Philosopher', serif;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  color: var(--dunkelblau);
  list-style: none;
  position: relative;
  padding-right: 2rem;
  transition: color 0.2s ease;
}
.mceo__faq summary::after {
  content: "+";
  position: absolute;
  right: 0;
  top: -2px;
  font-size: 1.6rem;
  color: var(--orange);
  font-weight: 400;
  transition: transform 0.2s ease;
}
.mceo__faq details[open] summary::after { content: "−"; }
.mceo__faq summary::-webkit-details-marker { display: none; }
.mceo__faq p {
  margin: 1rem 0 0;
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--text);
}

/* === CTA-Final === */
.mceo__final {
  text-align: center;
}
.mceo__final .mceo__quote {
  color: var(--orange);
  margin-top: 3rem;
}
.mceo__signature {
  font-size: 0.95rem;
  opacity: 0.8;
  margin-top: 0.5rem;
  font-style: italic;
}

/* === Mobile === */
@media (max-width: 640px) {
  .mceo__section { padding: 3.5rem 1.2rem; }
  .mceo__hero { min-height: 78vh; }
  .mceo__module, .mceo__yesno-card { padding: 1.5rem 1.3rem; }
  .mceo__price { padding: 2rem 1.5rem; }
}
</style>
`;

const content = `
${BRAND_CSS}
<div class="mceo">

<!-- HERO -->
<section class="mceo__section mceo__hero">
  <div class="mceo__container--narrow">
    <p class="mceo__eyebrow">Live-Programm · Start 1. Juni 2026 · 15 Plätze</p>
    <h1 class="mceo__h1">
      Mama-CEO.<br>
      Lerne, wie du als Mama mit wenig Zeit<br>
      <em>genug aus deinem Business holst — um nicht mehr auswärts arbeiten zu gehen.</em>
    </h1>
    <p class="mceo__lead">
      Stell dir vor: du machst dein Business in 18 Stunden die Woche — und das Einkommen reicht, um den alten Job zu kündigen. Du hast einen Wochenrhythmus, der zu deinem Mama-Alltag passt. Klare Strukturen. Tools, die für dich mitarbeiten (KI gehört dazu, ist aber nicht alles).<br>
      <strong>Genau das baust du in 8 Wochen Mama-CEO.</strong>
    </p>
    <a href="${CTA_URL}" class="mceo__btn mceo__btn--orange" target="_blank" rel="noopener">
      Platz sichern · 249 CHF Frühbucher
    </a>
    <div class="mceo__hero-trust">
      <span>🇨🇭 Schweizer Boden</span>
      <span>👩‍👧‍👦 4-fach-Mama</span>
      <span>🤖 13 KI-Mitarbeiter</span>
      <span>⏱ 18h die Woche</span>
      <span>💸 Kein Monat ohne Verkauf seit Mai 2025</span>
    </div>
  </div>
</section>

<!-- PROBLEM -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <h2 class="mceo__h2 mceo__h2--center">Du erkennst dich gerade wieder.</h2>
    <blockquote class="mceo__quote-block">
      „Wie finde ich Kunden?"<br>
      „Wo soll ich überhaupt anfangen?"<br>
      „Was poste ich jetzt?"
    </blockquote>
    <p>Diese drei Fragen kriege ich jeden Tag in die DMs. Von Mamas im Network, die seit einer Weile dabei sind. Frustriert. Viele Follower. Null Anfragen.</p>
    <p><strong>Und dazu der ehrliche Hintergrund, den niemand schreibt:</strong></p>
    <ul class="mceo__pain-list">
      <li>Du arbeitest noch 60–80% in deinem alten Job. Das frisst dich auf.</li>
      <li>Dein Mann schaut dein Business als Hobby an. Als „Instagram-Ding".</li>
      <li>Du machst alles selbst. Posten. Antworten. Strategie. Reels schneiden. Captions schreiben. Bis es 22 Uhr ist und du am Sofa sitzt und nicht weisst, was heute eigentlich passiert ist.</li>
      <li>Du sagst dir: <em>„Diesen Monat können wir nicht auswärts essen, das ist zu viel."</em> Und etwas in dir fragt: <em>„Oh shit, wie viel hab ich noch auf dem Konto?"</em></li>
    </ul>
    <p class="mceo__punch">Du bist nicht faul. Du hast nur ein <em class="accent">System-Problem</em>.<br>Das ist der Unterschied.</p>
  </div>
</section>

<!-- REFRAME + STORY -->
<section class="mceo__section mceo__section--creme">
  <div class="mceo__container">
    <h2 class="mceo__h2">Jetzt mal ganz ehrlich:</h2>
    <p><strong>Mental Load ist kein persönliches Versagen.</strong> Du hast einfach <strong>kein System gebaut</strong> — genau wie 95% der Mamas im Network.</p>
    <p>Niemand hat es dir gezeigt, weil die meisten Mentorinnen, die du auf Instagram siehst, <strong>das alles gar nicht selbst aufgebaut haben</strong>. Sie haben ein Team. Au-Pairs. VAs. Geld für Personal.</p>
    <p><strong>Ich nicht.</strong> Kein Au-Pair. Keine Putzfrau. Keine VA. Mein Mann arbeitet 80% auswärts, die ganze Woche. Ich hab 4 Kinder. 18 Stunden pro Woche fürs Business. Mehr nicht.</p>
    <p>Und trotzdem: <strong>kein Monat ohne Verkauf seit Mai 2025</strong>. Vierstellig pro Monat aus Mentoring. Vierstellig aus doTERRA.</p>
    <p class="mceo__quote">„Mein Erfolg ist nicht Bali.<br>Mein Erfolg ist eine Alp."</p>
    <p>Wie ich dahin gekommen bin: ich hab drei Sachen geändert. <strong>Mein Wochenrhythmus stand</strong> — 5:15 Krafttraining, 8:00–11:00 Fokuszeit, 19 Uhr Wand. <strong>Meine Strukturen waren klar</strong> — Notion als zentraler Ort, klare 5 CEO-Aufgaben, der Rest läuft über System. <strong>Und ich hab mir Tools gebaut</strong> — 13 Bots solo, ohne Vorwissen, weil ich keine Putzfrau und keine VA bezahlen kann.</p>
    <p><strong>Diese drei Bausteine — Rhythmus, Strukturen, Tools — baust du in 8 Wochen Mama-CEO. Damit du in deinen 18 Stunden die Woche endlich genug verdienst.</strong></p>
  </div>
</section>

<!-- WAS BEKOMMST DU -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container--wide">
    <h2 class="mceo__h2 mceo__h2--center">Was du in 8 Wochen aufbaust</h2>
    <p style="text-align:center; color:var(--petrol); font-weight:600; margin-bottom:2.5rem;">4 Hauptmodule + 1 Bonus · 23 Lektionen · 4 Live-Termine · Telegram-Gruppe</p>
    <div class="mceo__grid">
      <div class="mceo__module">
        <p class="mceo__module-eyebrow">Modul 1 · Wo. 1–2</p>
        <h3>Mindset-Reset für Mama-CEO</h3>
        <p>Du kennst deine 5 CEO-Aufgaben. Alles andere wird delegiert oder automatisiert. Wochenrhythmus, der zu deinem Mama-Alltag passt.</p>
        <p class="mceo__module-meta">+ Live 1: Hot-Seat Wochenrhythmus · 90 Min</p>
      </div>
      <div class="mceo__module">
        <p class="mceo__module-eyebrow">Modul 2 · Wo. 3–4</p>
        <h3>Dein KI-System: Architektur</h3>
        <p>Notion als dein Business-Brain. Erster KI-Mitarbeiter live. Du briefst KI wie ein Team-Mitglied — nicht wie ein Tool.</p>
        <p class="mceo__module-meta">+ Live 2: Q&amp;A KI-Architektur · 60 Min</p>
      </div>
      <div class="mceo__module">
        <p class="mceo__module-eyebrow">Modul 3 · Wo. 5–6</p>
        <h3>Akquise-KI: DMs auf Autopilot</h3>
        <p>Dein Funnel läuft: Keyword → Bot → Mail-Sequenz → Verkauf. ManyChat + ActiveCampaign + Blotato. Du hast es einmal komplett selbst durchgespielt — und deinen ersten Verkauf damit gemacht.</p>
        <p class="mceo__module-meta">+ Live 3: Werkstatt Funnel-Bau · 120 Min</p>
      </div>
      <div class="mceo__module">
        <p class="mceo__module-eyebrow">Modul 4 · Wo. 7–8</p>
        <h3>Service-KI: Skalieren ohne Burn-out</h3>
        <p>FAQ-Bot, Welcome-Päckchen, Mail-Sortier-Helfer. Deine Kundinnen werden begleitet — auch wenn du gerade nicht am Rechner bist.</p>
        <p class="mceo__module-meta">+ Live 4: Hot-Seat Kundinnen-Reise · 90 Min</p>
      </div>
      <div class="mceo__module mceo__module--bonus">
        <p class="mceo__module-eyebrow">🎁 Bonus-Modul · jederzeit zugänglich</p>
        <h3>Content-KI Quick-Setup</h3>
        <p>Hook-Bot + Karussell-Bot + Content-Wochen-Bot. Content-Wochenpipeline in 30 Min — wenn du schon weisst, WAS du sagen willst.</p>
        <p class="mceo__module-meta">B.1 Brand-Voice · B.2 Hook-Bot · B.3 Wochen-Bot</p>
      </div>
    </div>
  </div>
</section>

<!-- BONUS-PACK -->
<section class="mceo__section mceo__section--creme">
  <div class="mceo__container">
    <h2 class="mceo__h2 mceo__h2--center">Dein Bonus-Pack</h2>
    <p style="text-align:center; color:var(--petrol); font-size:1.2rem; font-weight:600; margin-bottom:2.5rem;">692 CHF Wert · im Preis enthalten</p>
    <ul class="mceo__bonus-list">
      <li><strong>Notion-Master-Template für Mama-CEOs</strong><span>99 CHF</span></li>
      <li><strong>ManyChat-Template-Pack</strong> (3 fertige Funnel-Vorlagen)<span>79 CHF</span></li>
      <li><strong>Q&amp;A-Custom-GPT-Vorlage</strong> + 5-Mail-Onboarding-Sequenz<span>59 CHF</span></li>
      <li><strong>Hook-Bot + Karussell-Bot</strong> Custom-GPT-Vorlagen<span>59 CHF</span></li>
      <li><strong>8 Wochen Telegram-Gruppe</strong> (Sparringpartnerinnen, Sound-Boards, Frust-Container)<span>unbezahlbar</span></li>
      <li><strong>4 Live-Termine</strong> (2× Hot-Seat + 1× Q&amp;A + 1× Werkstatt)<span>396 CHF</span></li>
    </ul>
  </div>
</section>

<!-- FÜR / NICHT-FÜR -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container--wide">
    <h2 class="mceo__h2 mceo__h2--center">Ist Mama-CEO für dich?</h2>
    <div class="mceo__yesno" style="margin-top:2.5rem;">
      <div class="mceo__yesno-card mceo__yesno-card--yes">
        <h3 style="color:var(--petrol);">✅ Ja, wenn …</h3>
        <ul>
          <li>Du seit mindestens 6 Monaten im Network bist und schon erste Kundinnen hattest — aber nicht durchbrichst.</li>
          <li>Du dein Thema schon weisst (zumindest grob).</li>
          <li>Du bereit bist, in 8 Wochen aktiv mitzubauen — nicht nur zu konsumieren.</li>
          <li>Du Notion + KI einsetzen willst, auch wenn du gerade nicht weisst wie. Du musst nichts können — ich zeig dir alles Schritt für Schritt.</li>
          <li>Du ehrlich zu dir bist: du machst alles zu Fuss und genau das frisst dich auf.</li>
        </ul>
      </div>
      <div class="mceo__yesno-card mceo__yesno-card--no">
        <h3 style="color:var(--orange);">❌ Nein, wenn …</h3>
        <ul>
          <li>Du noch nicht weisst, was du anbietest. → <a href="https://mumlifebalance.ch/instagram-kundenmaschine" style="color:var(--petrol); font-weight:600;">Instagram-Kundenmaschine</a> zuerst.</li>
          <li>Du sofort 6-stellig verdienen willst.</li>
          <li>Du erwartest, dass ich dein Business für dich baue.</li>
          <li>Du keine Lust hast, mit Tools wie Notion oder ChatGPT überhaupt zu starten.</li>
          <li>Du seit 5 Jahren Kurse buchst und nichts umsetzt.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- PREIS -->
<section class="mceo__section mceo__section--creme">
  <div class="mceo__container--narrow">
    <h2 class="mceo__h2 mceo__h2--center">Komm in die erste Runde — solange's noch 333 sind.</h2>
    <p class="mceo__lead">
      Bei der zweiten Runde sind's <strong>444</strong>. Die Boni werden mehr, das Programm tiefer.<br>
      <strong>Sichere dir jetzt den niedrigsten Preis — und einen der 15 Plätze direkt mit mir.</strong>
    </p>

    <div class="mceo__price mceo__price--featured">
      <p class="mceo__price-label">Frühbucher · 72 Stunden</p>
      <p class="mceo__price-amount">249 CHF</p>
      <p class="mceo__price-note">20.5. 09:00 — 22.5. 23:59</p>
    </div>

    <div class="mceo__price">
      <p class="mceo__price-label">Final · Erste Runde</p>
      <p class="mceo__price-amount">333 CHF</p>
      <p class="mceo__price-note">23.5. 00:00 — 31.5. 23:59 (Schluss)</p>
    </div>

    <div class="mceo__pricing-meta">
      <strong>Start:</strong> 1. Juni 2026<br>
      <strong>Plätze:</strong> 15 (strikt — wegen der 4 Live-Termine)<br>
      <strong>Runde 2 (Herbst 2026):</strong> 444 CHF
    </div>

    <a href="${CTA_URL}" class="mceo__btn mceo__btn--orange" target="_blank" rel="noopener" style="margin-top:2rem;">
      Platz sichern →
    </a>
  </div>
</section>

<!-- FAQ -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <h2 class="mceo__h2 mceo__h2--center" style="margin-bottom:2.5rem;">Häufige Fragen</h2>
    <div class="mceo__faq">
      <details>
        <summary>Ich hab keine Zeit für noch einen Kurs.</summary>
        <p>Genau deshalb baust du Mama-CEO. Du brauchst nicht „mehr Zeit fürs Lernen" — du brauchst „weniger Zeit fürs Tun". Modul 1 zeigt dir den Wochenrhythmus, der ab Tag 1 für dich arbeitet. Lektionen sind in 8–28 Min portioniert. Hör es beim Spazieren, beim Bügeln, beim Auto-Fahren.</p>
      </details>
      <details>
        <summary>Ich kann das nicht. Ich bin nicht die mit den Tools.</summary>
        <p>Genau dafür gibt's das Programm. Bis Mai 2025 wusste ich nicht, was ein Custom GPT ist. Heute hab ich 13 Slash-Commands. Jede Lektion läuft Schritt für Schritt — mit Vorlagen, mit fertigen Briefings, mit den 4 Live-Terminen, wenn's klemmt. Du musst nichts vorher können.</p>
      </details>
      <details>
        <summary>Ist das nicht das Gleiche wie deine Instagram-Kundenmaschine?</summary>
        <p>Nein. Instagram-Kundenmaschine lehrt dich <strong>WAS</strong> du sagst (Thema, Positionierung, Reels, Captions). Mama-CEO lehrt dich <strong>WIE</strong> du es tust ohne dich zu zerreissen (KI, Notion, Wochenrhythmus, Automation). Wer noch nicht weiss WAS sie verkauft → Instagram-Kundenmaschine zuerst. Wer's weiss aber keine Zeit hat → Mama-CEO.</p>
      </details>
      <details>
        <summary>Was, wenn ich mich nicht zu den Live-Terminen schalten kann?</summary>
        <p>Aufzeichnungen kommen alle ins Telegram. Hot-Seat-Fragen kannst du vorab schicken — ich nehme sie für dich auf. Aber: Live ist Live. Wenn du kannst, komm.</p>
      </details>
      <details>
        <summary>Was, wenn es bei mir nicht funktioniert?</summary>
        <p>Ehrlich: wenn du nicht implementierst, funktioniert nichts. Mama-CEO ist für Frauen, die TUN. Wenn du in den 8 Wochen die Mastery-Lektionen machst, an den Live-Terminen teilnimmst und in der Telegram-Gruppe aktiv bist — dann hast du das System. Wenn du konsumierst, hast du nichts. <strong>Es liegt an dir. 100%.</strong></p>
      </details>
      <details>
        <summary>Wieso erste Runde nur 333 — und dann teurer?</summary>
        <p>Schau, jetzt nehme ich zum ersten Mal 15 Frauen rein. Beim zweiten Mal weiss ich noch genauer, wo's bei euch hakt — und beim dritten Mal sind die Boni nochmal ausgebauter. Dann sind's 444 oder 555. Wer jetzt einsteigt, zahlt am wenigsten und hat mich am nähesten dran in den 4 Live-Terminen.</p>
      </details>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="mceo__section mceo__section--dark mceo__final">
  <div class="mceo__container--narrow">
    <h2 class="mceo__h2">Sichere dir deinen Platz.</h2>
    <p class="mceo__lead" style="color:var(--creme);">
      Erste Runde startet am 1. Juni. Anmeldung öffnet am 20. Mai um 09:00. Frühbucher-Preis läuft 72 Stunden.<br><br>
      Wenn du das hier zu Ende gelesen hast — <strong style="color:var(--orange);">du bist die richtige Frau für diese Runde.</strong>
    </p>
    <a href="${CTA_URL}" class="mceo__btn mceo__btn--cream" target="_blank" rel="noopener">
      Komm rein →
    </a>
    <p class="mceo__quote" style="color:var(--orange);">„Funktionieren war gestern."</p>
    <p class="mceo__signature">— Patricia</p>
  </div>
</section>

</div>
`;

const result = await createOrUpdatePage({
  title: 'Mama-CEO · Live-Programm für Mamas im Network',
  slug: 'mama-ceo',
  content: content.trim(),
  status: 'draft',
  excerpt: 'Lerne, wie du als Mama mit wenig Zeit genug aus deinem Business holst — um nicht mehr auswärts arbeiten zu gehen. 8 Wochen Live-Programm. Anmeldung öffnet 20. Mai 2026.',
});

console.log('\n✅ Page aktualisiert:');
console.log(`   ID:     ${result.id}`);
console.log(`   Title:  ${result.title?.rendered || result.title}`);
console.log(`   Slug:   ${result.slug}`);
console.log(`   Status: ${result.status}`);
console.log(`   Link:   ${result.link}`);
console.log('\n📝 Patricia: WP-Admin → Pages → Mama-CEO → Preview-Button.\n');
