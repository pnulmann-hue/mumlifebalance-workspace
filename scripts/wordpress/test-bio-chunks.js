import { readFile } from 'node:fs/promises';
const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

let html = await readFile('C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html', 'utf-8');

const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
const fullStyle = `<style>${styleMatch[1]}</style>`;
const fullBody = bodyMatch[1];

const tests = [
  // Test 1: nur Style, simple body
  { name: 'Style only + simple', content: `<!-- wp:html -->\n${fullStyle}\n<div>simple</div>\n<!-- /wp:html -->` },
  // Test 2: simple style, full body (ohne iframe)
  { name: 'No style + body (no iframe)', content: `<!-- wp:html -->\n<div>${fullBody.replace(/<!-- VIMEO[\s\S]*?\/script>/m, '')}</div>\n<!-- /wp:html -->` },
  // Test 3: erstes Drittel des Bodys
  { name: 'Body first third', content: `<!-- wp:html -->\n${fullBody.slice(0, Math.floor(fullBody.length / 3))}\n<!-- /wp:html -->` },
  // Test 4: zweites Drittel
  { name: 'Body second third', content: `<!-- wp:html -->\n${fullBody.slice(Math.floor(fullBody.length / 3), Math.floor(fullBody.length * 2 / 3))}\n<!-- /wp:html -->` },
  // Test 5: drittes Drittel
  { name: 'Body last third', content: `<!-- wp:html -->\n${fullBody.slice(Math.floor(fullBody.length * 2 / 3))}\n<!-- /wp:html -->` },
];

for (const t of tests) {
  const res = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages`, {
    method: 'POST',
    headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: `T: ${t.name}`, slug: `t-${Date.now()}-${Math.random().toString(36).slice(2,6)}`, content: t.content, status: 'draft' }),
  });
  console.log(`${t.name} (${t.content.length}c): ${res.status === 200 || res.status === 201 ? '✅ OK' : '❌ ' + res.status}`);
  if (res.status === 200 || res.status === 201) {
    const data = await res.json();
    await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/${data.id}?force=true`, { method: 'DELETE', headers: { 'Authorization': auth } });
  }
}
