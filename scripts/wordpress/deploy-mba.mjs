import { createPage } from './wp-api.js';
import fs from 'fs';

const content = fs.readFileSync(process.argv[2], 'utf8');
const template = process.argv[3] || '';

try {
  const res = await createPage({
    title: 'Mum Business Academy',
    slug: 'mba',
    content,
    status: 'draft',
    template,
  });
  console.log('OK', JSON.stringify({ id: res.id, link: res.link, status: res.status, template: res.template }));
} catch (e) {
  console.error('FEHLER:', e.message);
  process.exit(1);
}
