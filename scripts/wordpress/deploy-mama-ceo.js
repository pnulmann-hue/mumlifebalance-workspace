// Deploy Mama-CEO Landing-Page auf mumlifebalance.ch
// Stil: Julia Trost Elevate-Look (Vollbild-Foto-Hero, MEGA-Display, Loop-Banner,
// nummerierte Säulen, 3-Spalten-Pricing, Two-Column Story, Über-mich)
// Inhalt: 5-Säulen-Struktur (Stand 11.5.2026 nach Patricia-Review):
//   1. Du erschaffst dir die Zeit
//   2. Du brichst aus dem Hamsterrad aus
//   3. Du baust die Struktur
//   4. Du delegierst den Adminkram
//   5. Business skalieren
// Brand-Voice: keine "Cohort", "Pilot", "techie", "Backend"
// 3 Boni: Cockpit-Bot · Familien-Bot · Notion-Master-Template
// Ausführen: cd scripts/wordpress && node --env-file=.env deploy-mama-ceo.js

import { createOrUpdatePage } from './wp-api.js';

const CTA_URL = 'https://mumlifebalance.thrivecart.com/mama-ceo/';
const HERO_PHOTO = 'https://mumlifebalance.ch/wp-content/uploads/2026/04/patricia-hero-3-scaled.jpg';
const STORY_PHOTO = HERO_PHOTO;

const BRAND_CSS = `
<style>
:root { color-scheme: light only; }
@media (prefers-color-scheme: dark) {
  .mceo, .mceo * { color-scheme: light only !important; }
}

.mceo {
  --creme: #f1ecdd;
  --creme-soft: #faf6ec;
  --gelb: #f5e555;
  --dunkelblau: #29556d;
  --orange: #dc822e;
  --orange-tief: #c06b1e;
  --petrol: #12828c;
  --petrol-dark: #0a5e66;
  --text: #0c1c30;
  --muted: #5a6b7a;
  --white: #ffffff;
  --border: rgba(41, 85, 109, 0.12);
  font-family: 'Source Sans 3', system-ui, -apple-system, sans-serif;
  color: var(--text);
  line-height: 1.65;
}
.mceo *, .mceo *::before, .mceo *::after { box-sizing: border-box; }
.mceo p { margin: 0 0 1.3rem; font-size: 1.1rem; }
.mceo strong { color: var(--dunkelblau); font-weight: 700; }
.mceo em { font-style: italic; }
.mceo a { color: var(--petrol); }

/* === Typografie === */
.mceo__display { font-family: 'Philosopher', Georgia, serif; font-size: clamp(3rem, 8vw, 6rem); font-weight: 700; line-height: 1.05; letter-spacing: -0.02em; margin: 0 0 1.5rem; color: var(--dunkelblau); }
.mceo__h1 { font-family: 'Philosopher', Georgia, serif; font-size: clamp(2.2rem, 5vw, 3.4rem); font-weight: 700; line-height: 1.2; margin: 0 0 1.5rem; color: var(--dunkelblau); }
.mceo__h1 em { color: var(--orange); font-style: italic; }
.mceo__h2 { font-family: 'Philosopher', Georgia, serif; font-size: clamp(2rem, 4.5vw, 3.2rem); font-weight: 700; line-height: 1.15; margin: 0 0 1.5rem; color: var(--dunkelblau); }
.mceo__h2--center { text-align: center; }
.mceo__h2 em { font-style: italic; color: var(--orange); }
.mceo__h2-script { font-family: 'Philosopher', Georgia, serif; font-style: italic; font-weight: 400; font-size: 0.7em; display: block; color: var(--orange); }
.mceo__h3 { font-family: 'Philosopher', Georgia, serif; font-size: clamp(1.4rem, 2.5vw, 1.8rem); font-weight: 700; margin: 0 0 0.8rem; line-height: 1.3; color: var(--dunkelblau); }
.mceo__eyebrow { font-size: 0.8rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--orange); font-weight: 700; margin: 0 0 1.5rem; }
.mceo__lead { font-size: clamp(1.15rem, 2vw, 1.4rem); line-height: 1.55; max-width: 720px; margin: 0 auto 2rem; }
.mceo__quote { font-family: 'Philosopher', Georgia, serif; font-style: italic; font-size: clamp(1.6rem, 3.5vw, 2.4rem); color: var(--orange); text-align: center; margin: 3rem auto; line-height: 1.35; max-width: 800px; }

/* === Sections === */
.mceo__section { padding: 6rem 1.5rem; position: relative; }
.mceo__section--white { background: var(--white); }
.mceo__section--creme { background: var(--creme); }
.mceo__section--cremesoft { background: var(--creme-soft); }
.mceo__section--dark { background: var(--dunkelblau); color: var(--creme); }
.mceo__section--dark .mceo__h1, .mceo__section--dark .mceo__h2, .mceo__section--dark .mceo__h3 { color: var(--creme); }
.mceo__section--dark p { color: var(--creme); }
.mceo__section--dark strong { color: var(--orange); }
.mceo__section--dark .mceo__eyebrow { color: var(--orange); }
.mceo__section--gradient { background: linear-gradient(180deg, var(--petrol) 0%, var(--petrol-dark) 50%, var(--dunkelblau) 100%); color: var(--creme); }
.mceo__section--gradient .mceo__h2 { color: var(--creme); }
.mceo__section--gradient .mceo__h2 em { color: var(--gelb); }
.mceo__section--gradient .mceo__h2-script { color: var(--gelb); }
.mceo__section--gradient p { color: var(--creme); }
.mceo__container { max-width: 1100px; margin: 0 auto; }
.mceo__container--narrow { max-width: 760px; margin: 0 auto; }
.mceo__container--center { max-width: 820px; margin: 0 auto; text-align: center; }

/* ============ HERO mit Foto-Background ============ */
.mceo__hero { position: relative; min-height: 100vh; background-image: url('${HERO_PHOTO}'); background-size: cover; background-position: center 30%; display: flex; flex-direction: column; justify-content: flex-end; padding: 0; overflow: hidden; }
.mceo__hero-overlay { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(41, 85, 109, 0.15) 0%, rgba(41, 85, 109, 0.45) 60%, rgba(41, 85, 109, 0.85) 100%); z-index: 1; }
.mceo__hero-content { position: relative; z-index: 2; padding: 8rem 1.5rem 1.5rem; max-width: 1300px; margin: 0 auto; width: 100%; text-align: center; }
.mceo__hero-eyebrow { font-size: 0.85rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--creme); font-weight: 700; margin: 0 0 1.5rem; opacity: 0.95; }
.mceo__hero h1 { font-family: 'Philosopher', Georgia, serif; font-size: clamp(1.8rem, 3.5vw, 2.6rem); font-weight: 700; line-height: 1.25; color: var(--white); margin: 0 auto 1.2rem; max-width: 920px; text-shadow: 0 2px 18px rgba(0, 0, 0, 0.4); }
.mceo__hero h1 em { font-style: italic; color: var(--gelb); }
.mceo__hero-script { font-family: 'Philosopher', Georgia, serif; font-style: italic; font-size: clamp(1.1rem, 2vw, 1.5rem); color: var(--creme); margin: 0 0 1.5rem; }
.mceo__hero-bar { background: var(--orange); padding: 1.5rem 1rem; margin-top: 2rem; }
.mceo__hero-mega { font-family: 'Philosopher', Georgia, serif; font-size: clamp(4.5rem, 16vw, 13rem); font-weight: 900; line-height: 0.85; letter-spacing: -0.04em; text-transform: uppercase; margin: 0; color: var(--white); text-align: center; }
.mceo__hero-trust { background: var(--dunkelblau); color: var(--creme); padding: 1.2rem 1.5rem; text-align: center; font-size: 0.95rem; font-weight: 500; }
.mceo__hero-trust span { margin: 0 0.6rem; opacity: 0.95; }
.mceo__hero-trust .dot { color: var(--orange); }

/* ============ LOOP-BANNER ============ */
.mceo__loop { background: var(--gelb); color: var(--dunkelblau); padding: 1.4rem 0; overflow: hidden; white-space: nowrap; border-top: 4px solid var(--dunkelblau); border-bottom: 4px solid var(--dunkelblau); }
.mceo__loop-track { display: inline-block; animation: mceo-marquee 28s linear infinite; font-family: 'Philosopher', serif; font-size: clamp(1.2rem, 2.6vw, 1.7rem); font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.mceo__loop-track span { display: inline-block; margin: 0 1.5rem; }
.mceo__loop-track .dot { color: var(--orange); margin: 0 0.8rem; }
@keyframes mceo-marquee { 0% { transform: translateX(0%); } 100% { transform: translateX(-50%); } }

/* ============ Buttons ============ */
.mceo__btn { display: inline-block; padding: 1.15rem 2.6rem; font-family: 'Source Sans 3', sans-serif; font-size: 1rem; font-weight: 700; text-decoration: none; border-radius: 999px; letter-spacing: 0.12em; text-transform: uppercase; transition: transform 0.2s ease, box-shadow 0.2s ease; box-shadow: 0 6px 22px rgba(220, 130, 46, 0.28); }
.mceo__btn--primary { background: var(--dunkelblau); color: var(--creme); }
.mceo__btn--primary:hover { transform: translateY(-2px); background: #1f4258; color: var(--creme); }
.mceo__btn--orange { background: var(--orange); color: var(--white); }
.mceo__btn--orange:hover { transform: translateY(-2px); background: var(--orange-tief); color: var(--white); }
.mceo__btn--cream { background: var(--creme); color: var(--dunkelblau); box-shadow: 0 6px 22px rgba(0, 0, 0, 0.2); }
.mceo__btn--cream:hover { transform: translateY(-2px); color: var(--dunkelblau); }
.mceo__btn--outline { background: transparent; color: var(--dunkelblau); border: 2px solid var(--dunkelblau); box-shadow: none; }
.mceo__btn--outline:hover { background: var(--dunkelblau); color: var(--creme); }

/* ============ Pain-Säulen 01-04 ============ */
.mceo__pillars { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 2.5rem; margin-top: 3.5rem; }
.mceo__pillar-mega { text-align: left; }
.mceo__pillar-mega-num { font-family: 'Philosopher', serif; font-size: clamp(3.5rem, 6vw, 5rem); font-weight: 900; line-height: 1; color: var(--gelb); margin: 0 0 1.5rem; }
.mceo__pillar-mega-num::after { content: "."; color: var(--orange); }
.mceo__pillar-mega h3 { font-family: 'Philosopher', serif; font-size: clamp(1.4rem, 2.5vw, 1.7rem); font-weight: 700; color: var(--creme); margin: 0 0 1rem; line-height: 1.25; }
.mceo__pillar-mega p { font-size: 1rem; color: var(--creme); line-height: 1.55; opacity: 0.92; }

/* ============ Story zwei-Spaltig ============ */
.mceo__story { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }
.mceo__story-img { width: 100%; aspect-ratio: 4/5; background-image: url('${STORY_PHOTO}'); background-size: cover; background-position: center; border-radius: 4px; }
.mceo__story h2 em { font-style: italic; color: var(--orange); }
.mceo__story-accent { font-size: 0.85rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--orange); font-weight: 700; margin: 1.5rem 0 1.2rem; }
.mceo__story-bullets { list-style: none; padding: 0; margin: 0; }
.mceo__story-bullets li { display: flex; gap: 1rem; padding: 0.8rem 0; align-items: flex-start; font-size: 1.05rem; line-height: 1.55; }
.mceo__story-bullets .arrow { display: flex; flex-shrink: 0; align-items: center; justify-content: center; width: 36px; height: 36px; border: 2px solid var(--dunkelblau); border-radius: 50%; color: var(--dunkelblau); font-weight: 700; font-size: 1.1rem; }

/* ============ 5 Säulen (Mama-CEO-Struktur) ============ */
.mceo__pillar-row { display: grid; grid-template-columns: 100px 1fr; gap: 2.5rem; padding: 3rem 0; border-bottom: 1px solid var(--border); align-items: start; }
.mceo__pillar-row:last-child { border-bottom: none; }
.mceo__pillar-row-num { font-family: 'Philosopher', serif; font-size: clamp(3.5rem, 6vw, 5rem); font-weight: 900; color: var(--orange); line-height: 1; }
.mceo__pillar-row h3 { font-family: 'Philosopher', serif; font-size: clamp(1.7rem, 3.2vw, 2.4rem); color: var(--dunkelblau); margin: 0 0 1rem; line-height: 1.2; }
.mceo__pillar-row-promise { font-family: 'Philosopher', serif; font-style: italic; font-size: 1.05rem; color: var(--orange); margin-top: 1rem; }

/* ============ Module ============ */
.mceo__module { background: var(--white); border: 1px solid var(--border); border-radius: 12px; padding: 3rem; margin-bottom: 1.5rem; transition: border-color 0.2s, box-shadow 0.2s; }
.mceo__module:hover { border-color: var(--orange); box-shadow: 0 12px 32px rgba(220, 130, 46, 0.08); }
.mceo__module-num { font-family: 'Philosopher', serif; font-size: 0.85rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--orange); font-weight: 700; margin: 0 0 0.5rem; }
.mceo__module-title { font-family: 'Philosopher', serif; font-style: italic; font-size: clamp(1.7rem, 3vw, 2.2rem); color: var(--dunkelblau); margin: 0 0 1.5rem; line-height: 1.2; }
.mceo__module-bullets { list-style: none; padding: 0; margin: 0 0 1.5rem; }
.mceo__module-bullets li { position: relative; padding: 0.5rem 0 0.5rem 1.8rem; font-size: 1.05rem; font-weight: 600; color: var(--dunkelblau); }
.mceo__module-bullets li::before { content: "→"; position: absolute; left: 0; color: var(--orange); font-weight: 700; }
.mceo__module-meta { font-size: 0.95rem; color: var(--muted); font-style: italic; padding-top: 1.2rem; border-top: 1px solid var(--border); margin: 0; }
.mceo__module--bonus { background: linear-gradient(135deg, var(--petrol), var(--dunkelblau)); color: var(--creme); border-color: var(--petrol); }
.mceo__module--bonus .mceo__module-num { color: var(--gelb); }
.mceo__module--bonus .mceo__module-title { color: var(--creme); }
.mceo__module--bonus .mceo__module-bullets li { color: var(--creme); }
.mceo__module--bonus .mceo__module-bullets li::before { color: var(--gelb); }
.mceo__module--bonus .mceo__module-meta { color: rgba(241, 236, 221, 0.7); border-color: rgba(241, 236, 221, 0.2); }

/* ============ Benefits 3x2 Grid ============ */
.mceo__benefits-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2.5rem 2rem; margin: 3rem 0; }
.mceo__benefit-item h4 { font-family: 'Philosopher', serif; font-size: 1.4rem; color: var(--dunkelblau); margin: 0.8rem 0 0.5rem; line-height: 1.25; }
.mceo__benefit-item p { font-size: 1rem; line-height: 1.55; margin: 0; color: var(--text); }
.mceo__benefit-icon { width: 60px; height: 60px; display: inline-flex; align-items: center; justify-content: center; border: 2px solid var(--orange); border-radius: 50%; font-family: 'Philosopher', serif; font-size: 1.6rem; font-weight: 700; color: var(--orange); margin-bottom: 0.5rem; }

/* ============ Bonus-Boxen ============ */
.mceo__bonuses { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.3rem; margin: 2.5rem 0; }
.mceo__bonus-box { background: var(--white); border-left: 4px solid var(--orange); padding: 1.8rem; border-radius: 6px; }
.mceo__bonus-box-eyebrow { font-size: 0.75rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--petrol); font-weight: 700; margin: 0 0 0.5rem; }
.mceo__bonus-box h4 { font-family: 'Philosopher', serif; font-size: 1.3rem; color: var(--dunkelblau); margin: 0 0 0.8rem; line-height: 1.3; }
.mceo__bonus-box p { font-size: 0.98rem; line-height: 1.55; margin: 0 0 0.8rem; }
.mceo__bonus-box-value { font-size: 0.95rem; color: var(--orange); font-weight: 700; margin: 0; }

/* ============ Pricing 3-Spalten ============ */
.mceo__pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin: 3rem 0 2rem; align-items: stretch; }
.mceo__price-card { background: var(--white); border-radius: 14px; padding: 2.5rem 2rem; text-align: center; position: relative; border: 2px solid var(--border); display: flex; flex-direction: column; }
.mceo__price-card--featured { border-color: var(--orange); transform: scale(1.04); box-shadow: 0 12px 36px rgba(220, 130, 46, 0.18); }
.mceo__price-card--featured::before { content: "BESTE WAHL"; position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: var(--orange); color: var(--white); font-size: 0.75rem; font-weight: 700; letter-spacing: 0.15em; padding: 0.4rem 1.2rem; border-radius: 99px; white-space: nowrap; }
.mceo__price-card-label { font-size: 0.8rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--petrol); font-weight: 700; margin: 0 0 0.5rem; }
.mceo__price-card-amount { font-family: 'Philosopher', serif; font-size: clamp(2.6rem, 6vw, 3.6rem); font-weight: 700; color: var(--dunkelblau); margin: 0.3rem 0; line-height: 1; }
.mceo__price-card-note { font-size: 0.95rem; color: var(--muted); margin: 0 0 1.5rem; }
.mceo__price-card-meta { font-size: 0.92rem; color: var(--muted); margin: 0 0 1.2rem; flex-grow: 1; }

/* ============ FAQ ============ */
.mceo__faq details { border-bottom: 1px solid var(--border); padding: 1.6rem 0; }
.mceo__faq details[open] summary { color: var(--orange); }
.mceo__faq summary { font-family: 'Philosopher', serif; font-size: 1.25rem; font-weight: 700; cursor: pointer; color: var(--dunkelblau); list-style: none; position: relative; padding-right: 2.5rem; }
.mceo__faq summary::after { content: "+"; position: absolute; right: 0; top: -4px; font-size: 1.8rem; color: var(--orange); font-weight: 400; }
.mceo__faq details[open] summary::after { content: "−"; }
.mceo__faq summary::-webkit-details-marker { display: none; }
.mceo__faq p { margin: 1rem 0 0; font-size: 1.05rem; line-height: 1.7; }

/* ============ Über mich Stats ============ */
.mceo__about-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1.5rem; margin: 2rem 0; padding: 1.8rem; background: var(--creme); border-radius: 10px; text-align: center; }
.mceo__about-stat-num { font-family: 'Philosopher', serif; font-size: 2.4rem; font-weight: 700; color: var(--orange); line-height: 1; }
.mceo__about-stat-label { font-size: 0.9rem; color: var(--muted); margin-top: 0.3rem; line-height: 1.3; }

/* ============ Final-CTA ============ */
.mceo__final { text-align: center; }
.mceo__final-signature { font-family: 'Philosopher', serif; font-style: italic; font-size: 1.2rem; color: var(--orange); margin-top: 2rem; }

/* ============ Mobile ============ */
@media (max-width: 720px) {
  .mceo__section { padding: 4rem 1.2rem; }
  .mceo__hero-content { padding: 6rem 1.2rem 1rem; }
  .mceo__story { grid-template-columns: 1fr; gap: 2rem; }
  .mceo__module { padding: 2rem 1.5rem; }
  .mceo__pillar-row { grid-template-columns: 1fr; gap: 0.8rem; }
  .mceo__price-card--featured { transform: none; }
}
</style>
`;

const content = `
${BRAND_CSS}
<div class="mceo">

<!-- ============ HERO ============ -->
<section class="mceo__hero">
  <div class="mceo__hero-overlay"></div>
  <div class="mceo__hero-content">
    <p class="mceo__hero-eyebrow">Live-Programm · Start 1. Juni 2026 · 15 Plätze</p>
    <h1>
      Lerne, wie du als Mama mit wenig Zeit <em>genug aus deinem Business holst</em> — um nicht mehr auswärts arbeiten zu gehen.
    </h1>
    <p class="mceo__hero-script">Mit Wochenrhythmus, Strukturen und KI als Hebel.</p>
    <a href="${CTA_URL}" class="mceo__btn mceo__btn--orange" target="_blank" rel="noopener">
      Platz sichern · 249 CHF Frühbucher
    </a>
  </div>
  <div class="mceo__hero-bar">
    <p class="mceo__hero-mega">MAMA-CEO</p>
  </div>
  <div class="mceo__hero-trust">
    <span>🇨🇭 Schweiz</span><span class="dot">·</span>
    <span>👩‍👧‍👦 4-fach-Mama</span><span class="dot">·</span>
    <span>🤖 13 KI-Mitarbeiter</span><span class="dot">·</span>
    <span>⏱ 18h die Woche</span><span class="dot">·</span>
    <span>💸 Kein Monat ohne Verkauf seit Mai 2025</span>
  </div>
</section>

<!-- ============ LOOP-BANNER ============ -->
<div class="mceo__loop" aria-hidden="true">
  <div class="mceo__loop-track">
    <span>ANMELDUNG OFFEN AB 20. MAI</span><span class="dot">●</span>
    <span>NUR 15 PLÄTZE</span><span class="dot">●</span>
    <span>FRÜHBUCHER 249 CHF</span><span class="dot">●</span>
    <span>START 1. JUNI</span><span class="dot">●</span>
    <span>ANMELDUNG OFFEN AB 20. MAI</span><span class="dot">●</span>
    <span>NUR 15 PLÄTZE</span><span class="dot">●</span>
    <span>FRÜHBUCHER 249 CHF</span><span class="dot">●</span>
    <span>START 1. JUNI</span><span class="dot">●</span>
  </div>
</div>

<!-- ============ PAIN-SEKTION (Petrol-Gradient mit MEGA-Nummern) ============ -->
<section class="mceo__section mceo__section--gradient">
  <div class="mceo__container--center">
    <h2 class="mceo__h2 mceo__h2--center">
      WAS WÄRE WENN ICH DIR SAGE: <em>Mit nur 18 Stunden die Woche</em>
      <span class="mceo__h2-script">kannst du in 8 Wochen das hier aufbauen?</span>
    </h2>
  </div>
  <div class="mceo__container">
    <div class="mceo__pillars">
      <div class="mceo__pillar-mega">
        <p class="mceo__pillar-mega-num">01</p>
        <h3>Wochenrhythmus, der zu deinem Mama-Alltag passt</h3>
        <p>Schluss mit „heute mache ich das, morgen schau ich". Du baust einen festen Rhythmus mit Power-Zeiten, 4 Wochen-Rollen und Abend-Wand.</p>
      </div>
      <div class="mceo__pillar-mega">
        <p class="mceo__pillar-mega-num">02</p>
        <h3>Strukturen, die dein Business tragen</h3>
        <p>Brain Dump · Hütchenmethode · Notion Business Brain. Du wirst Entscheiderin, nicht mehr Macherin.</p>
      </div>
      <div class="mceo__pillar-mega">
        <p class="mceo__pillar-mega-num">03</p>
        <h3>Tools, die für dich mitarbeiten</h3>
        <p>KI-Mitarbeiter, ManyChat, Auto-Posting, Mail-Sequenzen. Du baust sie selbst — Schritt für Schritt mit Vorlagen.</p>
      </div>
      <div class="mceo__pillar-mega">
        <p class="mceo__pillar-mega-num">04</p>
        <h3>Einkommen, das dich aus dem Job rausholt</h3>
        <p>Das Ziel: Business-Einkommen, das reicht, um den alten Job zu kündigen. So wie ich's 2023 gemacht hab.</p>
      </div>
    </div>
    <p style="text-align:center; margin-top:3.5rem;">
      <a href="${CTA_URL}" class="mceo__btn mceo__btn--cream" target="_blank" rel="noopener">
        Komm rein · 249 CHF Frühbucher
      </a>
    </p>
  </div>
</section>

<!-- ============ STORY (Two-Column) ============ -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <div class="mceo__story">
      <div class="mceo__story-img" role="img" aria-label="Patricia bei der Arbeit"></div>
      <div>
        <h2 class="mceo__h2">Ich weiss <em>genau</em> wie du dich fühlst.</h2>
        <p>Den Spagat zwischen den ToDo's, Mama-Alltag und dem Wunsch nach finanzieller Unabhängigkeit zu schaffen — das ist eine echte Herausforderung.</p>
        <p class="mceo__story-accent">& MIR GING ES BIS 2023 GENAUSO</p>
        <ul class="mceo__story-bullets">
          <li><span class="arrow">→</span><span>Ich war Sachbearbeiterin in der Sozialverwaltung. Hab den Job geliebt — aber sonntags hatte ich die Hose voll vor Montag.</span></li>
          <li><span class="arrow">→</span><span>Mama-Logistik-Discos jeden Morgen. „Wer kommt früher, wer holt das Kind ab, wenn's krank ist."</span></li>
          <li><span class="arrow">→</span><span>Mit 4 Kindern konnte ich nicht regulär arbeiten gehen — die Kinderbetreuung kostete mehr als mein Lohn.</span></li>
          <li><span class="arrow">→</span><span>Ich hab heimlich gekündigt. Niemand wusste's, auch mein Mann nicht. Heute: vierstellig pro Monat aus dem Business. 18h Wochenarbeit.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============ DIE 5 SÄULEN ============ -->
<section class="mceo__section mceo__section--cremesoft">
  <div class="mceo__container">
    <p class="mceo__eyebrow" style="text-align:center;">Das Programm im Überblick</p>
    <h2 class="mceo__h2 mceo__h2--center">Die 5 Säulen, die dich aus dem Hamsterrad holen</h2>
    <p style="text-align:center; max-width:680px; margin:1rem auto 3rem; color:var(--muted);">
      8 Wochen. 5 Säulen. Jede Säule ein klarer Sprung — vom Hamsterrad zur Mama-CEO, die ihr Business mit System führt.
    </p>

    <div class="mceo__pillar-row">
      <div class="mceo__pillar-row-num">01</div>
      <div>
        <h3>Du erschaffst dir die Zeit</h3>
        <p>Productivity-Tipps für Mamas (Pomodoro, Time-Blocking, Eisenhower — was greift bei 4 Kindern). Deine Realität verstehen: Kids in der Schule? Morgen-/Abend-Typ? Daraus deine Business-Fokuszeit ableiten. Plus: was bringt dein Business wirklich vorwärts? Die 3 Säulen — Plattform · Produkt · Verkauf — alle drei müssen laufen.</p>
        <p class="mceo__pillar-row-promise">→ Sprung: „Ich kenne meine Realität, weiss was zählt und habe meinen Rhythmus."</p>
      </div>
    </div>

    <div class="mceo__pillar-row">
      <div class="mceo__pillar-row-num">02</div>
      <div>
        <h3>Du brichst aus dem Hamsterrad aus</h3>
        <p>Das Hamsterrad erkennen + benennen. Hütchenmethode: Brain Dump aller Aufgaben + Hüte sortieren (Mama · Tochter · Vereinsmitglied · Networkerin · ...). Was kann weg — bewusst zugunsten Business loslassen. 5 Mama-CEO-Blockaden auflösen. Plus: dein Sonntag-Ritual.</p>
        <p class="mceo__pillar-row-promise">→ Sprung: „Ich tue, was dran ist. Ohne Schuld."</p>
      </div>
    </div>

    <div class="mceo__pillar-row">
      <div class="mceo__pillar-row-num">03</div>
      <div>
        <h3>Du baust die Struktur</h3>
        <p>Aus dem Brain Dump → Aufgaben auf Tage/Wochen verteilen (Haushalt + Business — nie zu viel an einem Tag). Die 5 Kern-Workflows einer Mama-CEO als Schritt-Listen. Dein Notion Business Brain aufsetzen — mit Master-Template als Vorlage. Plus: Notfall-Modus, wenn Kinder krank sind.</p>
        <p class="mceo__pillar-row-promise">→ Sprung: „Ich habe Workflows, die immer gleich laufen — und einen 50%-Plan."</p>
      </div>
    </div>

    <div class="mceo__pillar-row">
      <div class="mceo__pillar-row-num">04</div>
      <div>
        <h3>Du delegierst den Adminkram</h3>
        <p>KI-Mythos vs. Realität — KI ist nur so gut wie dein Input. Cockpit-Bot (Live-Demo Patricia) für strategische Planung + Reflexion. Haushalts-Helfer (Live-Demo Kochassistent + Garten) — Mentee baut den Bot, den SIE braucht. Bot-Audit: massgeschneidert für deine Realität, kein Schema F. KI-Wochenplan: wann tust DU, wann delegierst du.</p>
        <p class="mceo__pillar-row-promise">→ Sprung: „KI-Mitarbeiter nehmen mir den Adminkram ab — Business UND Haushalt."</p>
      </div>
    </div>

    <div class="mceo__pillar-row">
      <div class="mceo__pillar-row-num">05</div>
      <div>
        <h3>Business skalieren</h3>
        <p>Mama-CEO-Matrix: 4 Felder (ich · KI · System · raus) — 25 Tasks sortieren. Was DEINS bleibt: 1:1-Beziehungen · Projekte · Events. 90-Tage-Wachstums-Plan: 1 Fokus pro 30 Tage. Plus: was du JETZT NICHT machst — Brücke zum nächsten Schritt (Insta-Selling-Tiefe, eigene Produkte erstellen, Umsetzerinnen-Community).</p>
        <p class="mceo__pillar-row-promise">→ Sprung: „Ich weiss was DEINS bleibt, was die KI macht, was raus muss und was als nächstes wächst."</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ LIVE-CALLS + COMMUNITY ============ -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <p class="mceo__eyebrow" style="text-align:center;">Plus persönliche Begleitung</p>
    <h2 class="mceo__h2 mceo__h2--center">4 Live-Termine direkt mit mir</h2>
    <p style="text-align:center; color:var(--muted); margin-bottom:3rem;">Alle 2 Wochen, am Ende des jeweiligen Säulen-Blocks.</p>
    <div class="mceo__benefits-grid">
      <div class="mceo__benefit-item">
        <span class="mceo__benefit-icon">1</span>
        <h4>Ende Woche 2 · Kick-Off</h4>
        <p>Hot-Seat „Zeig mir deinen Wochenrhythmus" — du kommst mit deinem Plan, wir feilen ihn gemeinsam.</p>
      </div>
      <div class="mceo__benefit-item">
        <span class="mceo__benefit-icon">2</span>
        <h4>Ende Woche 4 · Workflow-Review</h4>
        <p>Notion-Brain-Sprechstunde — wir schauen dein System an, identifizieren Lücken, ich gebe Verbesserungen.</p>
      </div>
      <div class="mceo__benefit-item">
        <span class="mceo__benefit-icon">3</span>
        <h4>Ende Woche 6 · KI-Demo</h4>
        <p>Bot-Bau-Sprechstunde — ich zeige live wie ich meine Bots aufsetze, du baust deinen mit.</p>
      </div>
      <div class="mceo__benefit-item">
        <span class="mceo__benefit-icon">4</span>
        <h4>Ende Woche 8 · Abschluss</h4>
        <p>90-Tage-Vision — wir setzen deinen Quartals-Plan, du gehst mit klarem Bild raus.</p>
      </div>
    </div>
    <p style="text-align:center; color:var(--muted); margin-top:2rem;">
      Plus: <strong>Telegram-Gruppe</strong> für 8 Wochen — Sparring zwischen den Live-Terminen, schnelle Antworten, Frust-Container. Bleibt offen auch danach.
    </p>
  </div>
</section>

<!-- ============ WAS DU AM ENDE HAST ============ -->
<section class="mceo__section mceo__section--cremesoft">
  <div class="mceo__container">
    <p class="mceo__eyebrow" style="text-align:center;">Nach 8 Wochen</p>
    <h2 class="mceo__h2 mceo__h2--center">Was du dann hast</h2>
    <ul class="mceo__benefits-grid" style="list-style:none; padding:0;">
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>Klarer Wochenrhythmus</h4><p>Du weisst Sonntagabend, wie deine Woche läuft. Power-Zeiten, 4 Rollen, Abend-Wand.</p></li>
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>Notion Business Brain</h4><p>Alles an einem Ort — Wochenplanung, Workflows, Produkte, Kundinnen, Finanzen.</p></li>
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>1-3 KI-Mitarbeiter live</h4><p>Cockpit-Bot + Haushalts-Helfer + was DU brauchst — solo gebaut, keine Tech-Abhängigkeit.</p></li>
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>Hütchenmethode beherrscht</h4><p>Du weisst: welche Rolle wann, was kann weg, was bleibt.</p></li>
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>Mama-CEO-Matrix gefüllt</h4><p>25 Tasks sortiert: ich · KI · System · raus. Plus 90-Tage-Plan.</p></li>
      <li class="mceo__benefit-item"><span class="mceo__benefit-icon">✓</span><h4>Mama-CEO-Mindset</h4><p>Vom Macherin- zum Entscheiderin-Modus. So bleibt Energie für die Menschen.</p></li>
    </ul>
  </div>
</section>

<!-- ============ BONUS-PACK (3 Boni) ============ -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <p class="mceo__eyebrow" style="text-align:center;">Bonus-Pack im Preis enthalten</p>
    <h2 class="mceo__h2 mceo__h2--center">3 Boni, die du direkt nutzt</h2>
    <p style="text-align:center; color:var(--muted); max-width:680px; margin:1rem auto 2.5rem;">
      Keine zusammengewürfelten Standard-Templates — sondern Patricias eigene Tools, die sie selbst nutzt.
    </p>

    <div class="mceo__bonuses">
      <div class="mceo__bonus-box">
        <p class="mceo__bonus-box-eyebrow">Bonus 01 · Mein eigener Bot</p>
        <h4>🌅 Cockpit-Bot Vorlage</h4>
        <p>Mein eigener Cockpit-Bot als System-Prompt + Anleitung. Strategische Planung, Reflexion, Tagesbriefing per Telegram. Du baust deinen in 30 Min nach.</p>
      </div>
      <div class="mceo__bonus-box">
        <p class="mceo__bonus-box-eyebrow">Bonus 02 · Mental-Load-Killer</p>
        <h4>🏠 Familien-Bot Vorlage</h4>
        <p>System-Prompt für deinen Mental-Load-Speicher: Familienkalender, Geschenke, Arzt-Termine, Reisen. Plus Anleitung wie du ihn auf deine Familie anpasst.</p>
      </div>
      <div class="mceo__bonus-box">
        <p class="mceo__bonus-box-eyebrow">Bonus 03 · Mein Notion-Setup</p>
        <h4>📂 Notion-Master-Template</h4>
        <p>Abgespeckte Kopie meines echten Notion-Workspaces: Wochenplanung, Aufgaben, Content, Produkte, Workflows, Mama-CEO-Matrix, 90-Tage-Tracker — alles als Vorlage, du duplizierst und passt an.</p>
      </div>
    </div>

    <p style="text-align:center; color:var(--muted); margin-top:1.5rem; font-size:0.95rem;">
      Plus: <strong>Claude-Code-Einrichtungs-Anleitung</strong> als Material in Modul 4 — du startest mit Patricia-Setup, nicht aus dem Nichts.
    </p>
  </div>
</section>

<!-- ============ PRICING ============ -->
<section class="mceo__section mceo__section--cremesoft">
  <div class="mceo__container">
    <p class="mceo__eyebrow" style="text-align:center;">Erste Runde · 15 Plätze</p>
    <h2 class="mceo__h2 mceo__h2--center">Komm jetzt rein — solange's noch 333 sind.</h2>
    <p style="text-align:center; color:var(--muted); max-width:640px; margin:1rem auto 0;">
      Bei der zweiten Runde sind's <strong>444</strong>. Die Boni werden mehr, das Programm tiefer. Wer jetzt einsteigt, zahlt am wenigsten und hat mich am nähesten dran.
    </p>

    <div class="mceo__pricing">
      <div class="mceo__price-card mceo__price-card--featured">
        <p class="mceo__price-card-label">🔥 Frühbucher · 72 Std</p>
        <p class="mceo__price-card-amount">249<span style="font-size:1.5rem; vertical-align:top;">CHF</span></p>
        <p class="mceo__price-card-note">20.5. 09:00 — 22.5. 23:59</p>
        <p class="mceo__price-card-meta">Komplettes Programm + alle 3 Boni + 4 Live-Termine + Telegram-Gruppe</p>
        <a href="${CTA_URL}" class="mceo__btn mceo__btn--orange" target="_blank" rel="noopener" style="margin-top:auto;">Jetzt sichern</a>
      </div>
      <div class="mceo__price-card">
        <p class="mceo__price-card-label">Final · Erste Runde</p>
        <p class="mceo__price-card-amount">333<span style="font-size:1.5rem; vertical-align:top;">CHF</span></p>
        <p class="mceo__price-card-note">23.5. 00:00 — 31.5. 23:59</p>
        <p class="mceo__price-card-meta">Selbe Inhalte. Gleiche Boni. Anmeldung schliesst am 31.5.</p>
        <a href="${CTA_URL}" class="mceo__btn mceo__btn--outline" target="_blank" rel="noopener" style="margin-top:auto;">Platz buchen</a>
      </div>
      <div class="mceo__price-card">
        <p class="mceo__price-card-label">Runde 2 · Herbst 2026</p>
        <p class="mceo__price-card-amount">444<span style="font-size:1.5rem; vertical-align:top;">CHF</span></p>
        <p class="mceo__price-card-note">Mehr Boni · vertieftes Programm</p>
        <p class="mceo__price-card-meta">So siehst du: jetzt ist der beste Zeitpunkt.</p>
        <span style="color:var(--muted); font-size:0.9rem; margin-top:auto;">Anmeldung folgt im Sommer</span>
      </div>
    </div>

    <p style="text-align:center; color:var(--muted); margin-top:2rem; font-size:0.95rem;">
      <strong>Programm-Start:</strong> 1. Juni 2026 · <strong>Plätze:</strong> 15 (strikt limitiert wegen 4 Live-Terminen)
    </p>
  </div>
</section>

<!-- ============ FÜR / NICHT FÜR ============ -->
<section class="mceo__section mceo__section--white">
  <div class="mceo__container">
    <h2 class="mceo__h2 mceo__h2--center">Ist Mama-CEO für dich?</h2>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:2rem; margin-top:2.5rem;">
      <div style="padding:2.5rem; background:var(--creme); border-radius:12px;">
        <h3 class="mceo__h3" style="color:var(--petrol);">✓ JA, wenn …</h3>
        <ul style="padding-left:1.2rem; margin:0;">
          <li style="margin-bottom:0.8rem;">Du seit min. 6 Monaten im Network bist und schon erste Kundinnen hattest.</li>
          <li style="margin-bottom:0.8rem;">Du dein Thema schon weisst (zumindest grob).</li>
          <li style="margin-bottom:0.8rem;">Du bereit bist, in 8 Wochen aktiv mitzubauen — nicht nur zu konsumieren.</li>
          <li style="margin-bottom:0.8rem;">Du Notion + KI einsetzen willst, auch wenn du gerade nicht weisst wie.</li>
          <li>Du ehrlich zu dir bist: du machst alles zu Fuss und es frisst dich auf.</li>
        </ul>
      </div>
      <div style="padding:2.5rem; background:var(--white); border-radius:12px; border-left:4px solid var(--orange);">
        <h3 class="mceo__h3" style="color:var(--orange);">✗ NEIN, wenn …</h3>
        <ul style="padding-left:1.2rem; margin:0;">
          <li style="margin-bottom:0.8rem;">Du noch nicht weisst, was du anbietest. → <a href="https://mumlifebalance.ch/instagram-kundenmaschine">Instagram-Kundenmaschine</a> zuerst.</li>
          <li style="margin-bottom:0.8rem;">Du sofort 6-stellig verdienen willst.</li>
          <li style="margin-bottom:0.8rem;">Du erwartest, dass ich dein Business für dich baue.</li>
          <li style="margin-bottom:0.8rem;">Du keine Lust hast, mit Tools wie Notion oder ChatGPT zu starten.</li>
          <li>Du seit Jahren Kurse buchst und nichts umsetzt.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============ FAQ ============ -->
<section class="mceo__section mceo__section--cremesoft">
  <div class="mceo__container--narrow">
    <p class="mceo__eyebrow" style="text-align:center;">Was du noch wissen willst</p>
    <h2 class="mceo__h2 mceo__h2--center" style="margin-bottom:2.5rem;">Häufige Fragen</h2>
    <div class="mceo__faq">
      <details>
        <summary>Ich hab keine Zeit für noch einen Kurs.</summary>
        <p>Genau deshalb baust du Mama-CEO. Du brauchst nicht „mehr Zeit fürs Lernen" — du brauchst „weniger Zeit fürs Tun". Säule 1 zeigt dir den Wochenrhythmus, der ab Tag 1 für dich arbeitet. Lektionen sind in 8–15 Min portioniert. Hör es beim Spazieren, beim Bügeln, beim Auto-Fahren.</p>
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
        <summary>Brauche ich eine grosse Reichweite, damit das funktioniert?</summary>
        <p>Nein. Ich hatte selbst keine grosse Reichweite, als ich den ersten Funnel gebaut habe. Mein erstes Mid-Tier-Programm hat 7 Kundinnen aus einer kleinen warmen Liste verkauft. Was zählt: dein Thema, dein Funnel, deine Strukturen — nicht deine Followerzahl.</p>
      </details>
      <details>
        <summary>Was, wenn es bei mir nicht funktioniert?</summary>
        <p>Ehrlich: wenn du nicht implementierst, funktioniert nichts. Mama-CEO ist für Frauen, die TUN. Wenn du in den 8 Wochen die Säulen-Lektionen machst, an den Live-Terminen teilnimmst und in der Telegram-Gruppe aktiv bist — dann hast du das System. Wenn du konsumierst, hast du nichts. <strong>Es liegt an dir. 100%.</strong></p>
      </details>
      <details>
        <summary>Wieso erste Runde nur 333 — und dann teurer?</summary>
        <p>Schau, jetzt nehme ich zum ersten Mal 15 Frauen rein. Beim zweiten Mal weiss ich noch genauer, wo's bei euch hakt — und beim dritten Mal sind die Boni nochmal ausgebauter. Dann sind's 444 oder 555. Wer jetzt einsteigt, zahlt am wenigsten und hat mich am nähesten dran in den 4 Live-Terminen.</p>
      </details>
      <details>
        <summary>Was ist mit dem Mann/der Familie? Ich hab kaum Zeit.</summary>
        <p>Ich hab 4 Kinder, mein Mann arbeitet 80% auswärts (Mo–Do). Ich verstehe das. Mama-CEO ist genau für diese Realität gebaut. Die Lektionen sind in 8–15 Min portioniert. Live-Termine sind vormittags (Power-Window — Kids in der Schule). Telegram-Gruppe ist asynchron. Du machst's in deinem Tempo.</p>
      </details>
    </div>
  </div>
</section>

<!-- ============ ÜBER PATRICIA ============ -->
<section class="mceo__section mceo__section--creme">
  <div class="mceo__container">
    <p class="mceo__eyebrow">Über mich</p>
    <h2 class="mceo__h2">Hey, ich bin Patricia.</h2>
    <p>Schweizerin. 36. Vier Kinder zwischen 8 und 13. Wohne im Appenzellerland, 920 Meter über dem Meer. Mein Mann arbeitet 80% auswärts, die ganze Woche. Ich hab keine Putzfrau, keine VA, kein Au-Pair.</p>
    <p>2023 hab ich heimlich mein Business angemeldet — niemand wusste es, auch mein Mann nicht. Er hat's erfahren, weil Freunde meine Insta-Story gesehen haben. Im April 2023 hab ich gekündigt. Erste Kundin: 1.500 CHF für 3 Monate. <em>„Mega puff."</em> Zwei Jahre Bauen. Frust. Programme die niemand gekauft hat.</p>
    <p>Mai 2025: Wendepunkt. Ich hab aufgehört, manuell zu arbeiten. Hab angefangen, mir KI-Mitarbeiter zu bauen. Hab meinen Wochenrhythmus aufgesetzt. Hab mein Thema verschoben — von „Mental Load Coaching" zu „Mama-CEO".</p>
    <p>Seitdem: <strong>kein Monat ohne Verkauf</strong>. Vierstellig pro Monat aus Mentoring + vierstellig aus doTERRA. 18 Stunden Wochenarbeit. Mehr nicht.</p>

    <div class="mceo__about-stats">
      <div>
        <p class="mceo__about-stat-num">18h</p>
        <p class="mceo__about-stat-label">Wochenarbeit</p>
      </div>
      <div>
        <p class="mceo__about-stat-num">4</p>
        <p class="mceo__about-stat-label">Kinder</p>
      </div>
      <div>
        <p class="mceo__about-stat-num">13</p>
        <p class="mceo__about-stat-label">KI-Mitarbeiter</p>
      </div>
      <div>
        <p class="mceo__about-stat-num">12+</p>
        <p class="mceo__about-stat-label">Monate ohne Pause-Verkauf</p>
      </div>
    </div>

    <p><strong>Geh zu jemandem anders, wenn du in 6 Monaten 6-stellig verdienen willst.</strong> Komm zu mir, wenn du ehrliche Mama-CEO-Realität willst — Schweizer Boden, 18h Woche, kein Bali-Postkarten-Coaching.</p>
  </div>
</section>

<!-- ============ FINAL-CTA ============ -->
<section class="mceo__section mceo__section--dark mceo__final">
  <div class="mceo__container--center">
    <h2 class="mceo__h1">Sichere dir deinen Platz.</h2>
    <p class="mceo__lead" style="color:var(--creme);">
      Erste Runde startet am <strong>1. Juni</strong>. Anmeldung öffnet am <strong>20. Mai um 09:00</strong>. Frühbucher-Preis läuft <strong>72 Stunden</strong>.
    </p>
    <p style="color:var(--creme); font-size:1.2rem; margin:2rem 0;">
      Wenn du das hier zu Ende gelesen hast — <em style="color:var(--orange);">du bist die richtige Frau für diese Runde.</em>
    </p>
    <a href="${CTA_URL}" class="mceo__btn mceo__btn--cream" target="_blank" rel="noopener">
      Komm rein →
    </a>
    <p class="mceo__final-signature">„Funktionieren war gestern."<br><span style="font-size:0.9rem; opacity:0.7;">— Patricia</span></p>
  </div>
</section>

</div>
`;

const result = await createOrUpdatePage({
  title: 'Mama-CEO · Live-Programm für Mamas im Network',
  slug: 'mama-ceo',
  content: content.trim(),
  status: 'draft',
  excerpt: 'Lerne, wie du als Mama mit wenig Zeit genug aus deinem Business holst — um nicht mehr auswärts arbeiten zu gehen. 8 Wochen Live-Programm in 5 Säulen. Anmeldung öffnet 20. Mai 2026.',
});

console.log('\n✅ Page aktualisiert:');
console.log(`   ID:     ${result.id}`);
console.log(`   Title:  ${result.title?.rendered || result.title}`);
console.log(`   Slug:   ${result.slug}`);
console.log(`   Status: ${result.status}`);
console.log(`   Link:   ${result.link}`);
console.log('\n📝 Patricia: WP-Admin → Pages → Mama-CEO → Preview-Button (oben rechts).\n');
