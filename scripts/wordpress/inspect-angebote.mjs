const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const page = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/3099`, { headers: { 'Authorization': auth } }).then(r => r.json());
const text = page.content.rendered
  .replace(/<[^>]+>/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const lines = text.split(/(?=[A-ZÄÖÜ])/);
for (const line of lines) {
  if (line.match(/Workbook|Quiz|Fahrplan|Starter|Story-Challenge|Lead-Challenge|Bio-Check|kostenlos|0€|Freebie|Geschenk/i)) {
    console.log('→', line.trim().slice(0, 200));
  }
}
