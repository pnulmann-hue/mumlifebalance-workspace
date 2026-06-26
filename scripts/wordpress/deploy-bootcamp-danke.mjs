// Widmet die obsolete Webinar-Seite (ID 3795) zur Bootcamp-Willkommens-/Danke-Seite um.
// NinjaFirewall blockt CREATE (POST /pages) -> daher UPDATE per ID statt createOrUpdatePage.
// Aufruf: cd scripts/wordpress && node --env-file=.env deploy-bootcamp-danke.mjs
import { readFile } from 'node:fs/promises';
import { updatePage } from './wp-api.js';

const PAGE_ID = 3795;
const html = await readFile(new URL('../../outputs/produkte/bootcamp/danke-landingpage.html', import.meta.url), 'utf8');
const res = await updatePage(PAGE_ID, {
  slug: 'bootcamp-willkommen',
  title: 'Willkommen im Bootcamp',
  content: html,
  status: 'publish',
  template: 'elementor_canvas',
});
console.log('✅ Seite:', res.id, '· Slug:', res.slug, '· Status:', res.status, '· Template:', res.template, '· Link:', res.link);
