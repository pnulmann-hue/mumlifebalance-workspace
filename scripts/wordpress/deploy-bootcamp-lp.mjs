// Deployt die Bootcamp-Landingpage als Entwurf nach WordPress (Slug /bootcamp).
// Aufruf: cd scripts/wordpress && node --env-file=.env deploy-bootcamp-lp.mjs
import { readFile } from 'node:fs/promises';
import { createOrUpdatePage, updatePage } from './wp-api.js';

const html = await readFile(new URL('../../outputs/produkte/bootcamp/bootcamp-landingpage.html', import.meta.url), 'utf8');
// Kein status hier: neue Seite -> createPage-Default (draft); bestehende Seite -> Status bleibt (kein versehentliches Un-Publish).
const res = await createOrUpdatePage({
  slug: 'bootcamp',
  title: 'Mama Business Bootcamp',
  content: html,
});
// Canvas-Template: kein Theme-Header/Menue/Footer -> Sektionen randlos, Mobile sauber.
const tpl = await updatePage(res.id, { template: 'elementor_canvas' });
console.log('✅ Seite:', res.id, '· Status:', res.status, '· Template:', tpl.template, '· Link:', res.link);
