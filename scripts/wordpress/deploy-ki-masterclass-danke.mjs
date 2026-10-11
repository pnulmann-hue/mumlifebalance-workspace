// Bestätigungsseite der KI-Masterclass (Do 8.10.2026, 09:00): hier landet sie NACH dem Klick
// auf „Ja, ich bin dabei“ in der Opt-in-Mail (Formular 69 → Opt-in → Weiterleitung).
// Die Meldung direkt nach dem Absenden („schau in dein Postfach“) ist die Danke-Nachricht im Formular.
//
//   cd scripts/wordpress && node --env-file=.env deploy-ki-masterclass-danke.mjs
//
// Nutzt die Gestaltung der Produkt-Ideen-Finder-Danke-Seite (Klasse .pif, CSS liegt im
// Customizer) — deshalb kein eigenes CSS. Die Ideen-Finder-Seite /produkt-ideen-finder-los/
// (WP 4085) bleibt UNVERÄNDERT: sie ist die Live-Danke-Seite des STANDBEIN-Funnels.
//
// Neue Seite als Entwurf. Eine bestehende Seite behält ihren Status (sonst würde ein
// erneuter Lauf eine veröffentlichte Seite vom Netz nehmen).
import { createPage, updatePage, findPageBySlug } from './wp-api.js';

const SLUG = 'ki-masterclass-danke';
// 🚨 Stimm-Check ist noch nicht live — sobald die Adresse steht, hier eintragen.
const STIMM_CHECK = 'https://stimm-check.vercel.app/';   // direkt aufs Tool: sie ist schon auf der Liste, kein zweites Opt-in

// Der Stimm-Check-Block erscheint erst, wenn die Adresse eingetragen ist — ein Knopf ins
// Leere auf einer Live-Seite ist schlimmer als keiner.
const STIMM_BLOCK = STIMM_CHECK.startsWith('#') ? '' : `  <section class="band">
    <div class="w">
      <div class="kicker" style="color:#ffd9b3">Bis Donnerstag schon mal ausprobieren</div>
      <h2>Deine KI soll klingen wie du?</h2>
      <p>Am Donnerstag zeige ich dir, was möglich ist, wenn deine KI dich kennt und weiss, was zu tun ist. Den ersten Teil davon kannst du heute schon machen: Im Stimm-Check sammelst du in rund 15 Minuten die sechs Angaben, die deine KI von dir braucht, und bekommst einen ersten Text, den du so posten würdest.</p>
      <p class="lead">Kostenlos, und du kannst ihn am Donnerstag gleich mitbringen.</p>
      <a class="cta big" href="${STIMM_CHECK}" target="_blank" rel="noopener" style="margin-top:6px">Zum Stimm-Check</a>
    </div>
  </section>
`;

const inhalt = `<!-- wp:html -->
<div class="pif">

  <section class="hero">
    <div class="w">
      <span class="badge">Das hat geklappt ✨</span>
      <h1>Cool, du bist dabei!</h1>
      <p class="sub">Dein Platz für die Masterclass am Donnerstag, 8. Oktober, um 9 Uhr ist sicher. Der Zoom-Link ist schon unterwegs in dein Postfach.</p>
      <div class="trust">📅 <b>Do 8. Oktober</b> &nbsp;·&nbsp; ⏰ <b>9 Uhr</b> &nbsp;·&nbsp; 🎥 <b>Aufzeichnung am selben Tag</b></div>
      <p class="sub" style="margin-top:18px">Am Mittwochabend erinnere ich dich nochmal. Und wenn du am Morgen nicht live dabei sein kannst, bekommst du die Aufzeichnung trotzdem.</p>
    </div>
  </section>

${STIMM_BLOCK}
  <section class="sec" style="text-align:center">
    <div class="w">
      <p style="color:#5a6b76;margin:0">Ich freu mich auf dich am Donnerstag. 🤍</p>
    </div>
  </section>

</div>
<!-- /wp:html -->`;

const bestehend = await findPageBySlug(SLUG);
const felder = {
  title: 'KI-Masterclass — du bist dabei',
  slug: SLUG,
  content: inhalt,
  template: 'elementor_canvas',
};
const seite = bestehend ? await updatePage(bestehend.id, felder) : await createPage({ ...felder, status: 'draft' });
console.log((bestehend ? 'aktualisiert' : 'angelegt') + ':', seite.id, seite.status, seite.link);
if (STIMM_CHECK.startsWith('#')) console.log('ℹ Stimm-Check-Block ausgeblendet, bis die Adresse in STIMM_CHECK steht.');
