import { updatePage } from './wp-api.js';
import fs from 'fs';

const id = process.argv[2];
const content = fs.readFileSync(process.argv[3], 'utf8');
try {
  const res = await updatePage(id, { content });
  console.log('OK', JSON.stringify({ id: res.id, status: res.status, link: res.link }));
} catch (e) {
  console.error('FEHLER:', e.message);
  process.exit(1);
}
